from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from jinja2 import Environment, FileSystemLoader
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import requests
import re
from html import unescape
import os
import json
import logging
import asyncio
from typing import Optional, Tuple, List, Any

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from netcine import catalog_search, search_link, search_term
#from serve import search_serve

VERSION = "0.0.4" 
MANIFEST = {
    "id": "com.fenixflix", "version": VERSION, "name": "FENIXFLIX",
    "description": "Sua fonte para filmes e séries.",
    "logo": "https://i.imgur.com/9SKgxfU.png", "resources": ["catalog", "meta", "stream"],
    "types": ["movie", "series"], "catalogs": [
        {"type": "movie", "id": "fenixflix", "name": "FENIXFLIX", "extraSupported": ["search"]},
        {"type": "series", "id": "fenixflix", "name": "FENIXFLIX", "extraSupported": ["search"]}
    ], "idPrefixes": ["fenixflix", "tt"]
}
templates = Environment(loader=FileSystemLoader("templates"))
limiter = Limiter(key_func=get_remote_address)
rate_limit = '5/second'

app = FastAPI()


skyflixapi  = "https://da5f663b4690-skyflixfork14.baby-beamup.club"

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(content={"error": "Too many requests"}, status_code=429)

def add_cors(response: Response) -> Response:
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.get("/", response_class=HTMLResponse)
@limiter.limit(rate_limit)
async def home(request: Request):
    template = templates.get_template("index.html")
    response_content = template.render(
        name=MANIFEST['name'], 
        types=MANIFEST['types'], 
        logo=MANIFEST['logo'], 
        description=MANIFEST['description'], 
        version=MANIFEST['version']
    )
    return add_cors(HTMLResponse(response_content))

@app.get("/manifest.json")
@limiter.limit(rate_limit)
async def manifest_endpoint(request: Request):
    return add_cors(JSONResponse(content=MANIFEST))

@app.get("/catalog/{type}/fenixflix/search={query}.json")
@limiter.limit(rate_limit)
async def search(type: str, query: str, request: Request):
    catalog = catalog_search(query)
    results = [item for item in catalog if item.get("type") == type] if catalog else []
    return add_cors(JSONResponse(content={"metas": results}))

@app.get("/meta/{type}/{id}.json")
@limiter.limit(rate_limit)
async def meta(type: str, id: str, request: Request):
    return add_cors(JSONResponse(content={"meta": {}}))



async def search_term_async(imdb_id: str) -> Tuple[List[str], Optional[str]]:
   
    try:
        loop = asyncio.get_event_loop()
        titles, year = await loop.run_in_executor(None, search_term, imdb_id)
        return titles, year
    except Exception as e:
        return [], None

async def search_serve_async(imdb_id: str, content_type: str, season: Optional[int], episode: Optional[int]):
    try:
        loop = asyncio.get_event_loop()
        streams = await loop.run_in_executor(None, search_serve, imdb_id, content_type, season, episode)
        return streams
    except Exception as e:
        return []

async def search_link_async(id: str):
    try:
        loop = asyncio.get_event_loop()
        streams = await loop.run_in_executor(None, search_link, id)
        
        for stream_item in streams:
            original_description = stream_item.get('description', 'Stream VOD').lower()
            audio_tag = ""

            if "dublado" in original_description or "dub" in original_description:
                audio_tag = " (Dublado)"
            elif "legendado" in original_description or "leg" in original_description:
                audio_tag = " (Legendado)"

            stream_item['name'] = "FENIXFLIX"
            stream_item['description'] = f"NC{audio_tag}"
            
        return streams
    except Exception as e:
        return []

async def search_skyflix_async(content_type: str, content_id: str):
    streams = []
    url = f"{skyflixapi}/stream/{content_type}/{content_id}.json"
    try:
        loop = asyncio.get_event_loop()
        
        fetch_data = lambda: requests.get(url, timeout=10)
        response = await loop.run_in_executor(None, fetch_data)
        
        if response.status_code == 200:
            data = response.json()
            if 'streams' in data:
                streams = data['streams']
                for stream_item in streams:
                    original_description = stream_item.get('description', 'Stream VOD').lower()

                    stream_item['name'] = "FENIXFLIX"
                    stream_item['description'] = f"Skyflix API"
                
    except requests.exceptions.Timeout:
       pass
    except Exception as e:
       pass 
    return streams

@app.get("/stream/{type}/{id}.json")
@limiter.limit(rate_limit)
async def stream(type: str, id: str, request: Request):
    if type not in ["movie", "series"]:
        return add_cors(JSONResponse(content={"streams": []}))

    imdb_id = id.split(':')[0]
    season, episode = None, None

    if type == 'series':
        try:
            parts = id.split(':')
            season = int(parts[1])
            episode = int(parts[2])
        except (IndexError, ValueError):
            return add_cors(JSONResponse(content={"streams": []}))

    titles, year = await search_term_async(imdb_id)
    
    searches = [
        search_serve_async(imdb_id, type, season, episode),
        search_skyflix_async(type, id)
    ]

    if titles and year:
        searches.append(search_link_async(id))

    results = await asyncio.gather(*searches)

    all_streams = [stream for result in results for stream in result]        
    return add_cors(JSONResponse(content={"streams": all_streams}))

@app.options("/{path:path}")
@limiter.limit(rate_limit)
async def options_handler(path: str, request: Request):
    return add_cors(Response(status_code=204))
