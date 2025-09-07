from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from jinja2 import Environment, FileSystemLoader
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import logging
import asyncio
from cachetools import cached, TTLCache

# Importações dos seus módulos
from netcine import catalog_search, search_link, search_term
from gofilmes import search_gofilmes, resolve_stream as resolve_gofilmes_stream
from serve import search_serve

VERSION = "0.0.3" # Versão otimizada
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

logging.basicConfig(level=logging.INFO)

# Cache para os resultados de stream, com duração de 2 horas (7200 segundos)
stream_cache = TTLCache(maxsize=1000, ttl=7200)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(content={"error": "Too many requests"}, status_code=429)

def add_cors(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.get("/", response_class=HTMLResponse)
@limiter.limit(rate_limit)
async def home(request: Request):
    template = templates.get_template("index.html")
    return add_cors(HTMLResponse(template.render(name=MANIFEST['name'], types=MANIFEST['types'], logo=MANIFEST['logo'], description=MANIFEST['description'], version=MANIFEST['version'])))

@app.get("/manifest.json")
@limiter.limit(rate_limit)
async def manifest(request: Request):
    return add_cors(JSONResponse(content=MANIFEST))

@app.get("/catalog/{type}/fenixsky/search={query}.json")
@limiter.limit(rate_limit)
async def search(type: str, query: str, request: Request):
    loop = asyncio.get_running_loop()
    # Executa a busca síncrona em um executor para não bloquear
    catalog = await loop.run_in_executor(None, catalog_search, query)
    results = [item for item in catalog if item.get("type") == type] if catalog else []
    return add_cors(JSONResponse(content={"metas": results}))

@app.get("/meta/{type}/{id}.json")
@limiter.limit(rate_limit)
async def meta(type: str, id: str, request: Request):
    return add_cors(JSONResponse(content={"meta": {}}))

# --- Funções de busca assíncrona ---

async def fetch_netcine(id: str):
    loop = asyncio.get_running_loop()
    try:
        # Executa a função síncrona num thread pool para não bloquear o loop de eventos
        netcine_streams = await loop.run_in_executor(None, search_link, id)
        return netcine_streams if netcine_streams else []
    except Exception as e:
        logging.error(f"Erro ao buscar em Netcine para {id}: {e}")
        return []

async def fetch_gofilmes(titles, type, season, episode):
    loop = asyncio.get_running_loop()
    try:
        gofilmes_player_options = await loop.run_in_executor(None, search_gofilmes, titles, type, season, episode)
        
        streams = []
        for option in gofilmes_player_options:
            # resolve_stream também é síncrono, então executamos no executor
            stream_url, stream_headers = await loop.run_in_executor(None, resolve_gofilmes_stream, option['url'])
            if stream_url:
                stream_name = option['name']
                if 'mediafire.com' in stream_url:
                    stream_name += " (Só no Navegador)"
                
                stream_obj = {"name": stream_name, "url": stream_url}
                if stream_headers:
                    stream_obj["behaviorHints"] = {"proxyHeaders": {"request": stream_headers}}
                streams.append(stream_obj)
        return streams
    except Exception as e:
        logging.error(f"Erro ao buscar em GoFilmes: {e}")
        return []

@app.get("/stream/{type}/{id}.json")
@limiter.limit(rate_limit)
@cached(stream_cache)
async def stream(type: str, id: str, request: Request):
    all_streams = []

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

    # 1. Busca local (síncrona, pois é rápida)
    try:
        local_streams = search_serve(imdb_id, type, season, episode)
        if local_streams:
            all_streams.extend(local_streams)
    except Exception as e:
        logging.error(f"Erro ao buscar em JSON local para {imdb_id}: {e}")

    loop = asyncio.get_running_loop()
    titles, _ = await loop.run_in_executor(None, search_term, imdb_id)
    if not titles:
        return add_cors(JSONResponse(content={"streams": all_streams}))

    # 2. Busca fontes externas em paralelo
    tasks = [
        fetch_netcine(id),
        fetch_gofilmes(titles, type, season, episode)
    ]
    
    results = await asyncio.gather(*tasks)
    
    for result_list in results:
        all_streams.extend(result_list)
        
    return add_cors(JSONResponse(content={"streams": all_streams}))

@app.options("/{path:path}")
@limiter.limit(rate_limit)
async def options_handler(path: str, request: Request):
    return add_cors(Response(status_code=204))
