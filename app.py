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
from contextlib import asynccontextmanager

# Importações para o cache
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

# Importações dos seus módulos
from netcine import catalog_search, search_link, search_term
from gofilmes import search_gofilmes, resolve_stream as resolve_gofilmes_stream
from serve import search_serve

# Configuração do ciclo de vida da aplicação para o cache
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Conecta ao Redis. Certifique-se de que o Redis está a correr.
    # Se estiver a usar Docker, o nome do host será o nome do serviço do Redis (ex: "redis://redis").
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    # Limpa a conexão ao finalizar
    await FastAPICache.clear()

VERSION = "0.0.3" # Versão atualizada com otimizações
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
app = FastAPI(lifespan=lifespan)

logging.basicConfig(level=logging.INFO)

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

@app.get("/catalog/{type}/fenixflix/search={query}.json")
@cache(expire=86400) # Cache de 24 horas
@limiter.limit(rate_limit)
async def search(type: str, query: str, request: Request):
    catalog = catalog_search(query)
    results = [item for item in catalog if item.get("type") == type] if catalog else []
    return add_cors(JSONResponse(content={"metas": results}))

@app.get("/meta/{type}/{id}.json")
@cache(expire=86400) # Cache de 24 horas
@limiter.limit(rate_limit)
async def meta(type: str, id: str, request: Request):
    # A lógica de metadados pode ser expandida aqui, se necessário.
    return add_cors(JSONResponse(content={"meta": {}}))


# Funções de busca assíncronas para serem executadas em paralelo
async def search_serve_async(imdb_id, content_type, season, episode):
    try:
        loop = asyncio.get_event_loop()
        # Executa a função síncrona num executor para não bloquear o loop de eventos
        return await loop.run_in_executor(None, search_serve, imdb_id, content_type, season, episode)
    except Exception as e:
        logging.error(f"Erro ao buscar em JSON local para {imdb_id}: {e}")
        return []

async def search_link_async(id):
    try:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, search_link, id)
    except Exception as e:
        logging.error(f"Erro ao buscar em Netcine para {id}: {e}")
        return []

async def search_gofilmes_async(titles, type, season, episode):
    try:
        loop = asyncio.get_event_loop()
        player_options = await loop.run_in_executor(None, search_gofilmes, titles, type, season, episode)
        
        streams = []
        for option in player_options:
            stream_url, stream_headers = await loop.run_in_executor(None, resolve_gofilmes_stream, option['url'])
            if stream_url:
                stream_name = option.get('name', 'GoFilmes')
                if 'mediafire.com' in stream_url:
                    stream_name += " (Só no Navegador)"
                
                stream_obj = {"name": stream_name, "url": stream_url}
                if stream_headers:
                    stream_obj["behaviorHints"] = {"proxyHeaders": {"request": stream_headers}}
                streams.append(stream_obj)
        return streams
    except Exception as e:
        logging.error(f"Erro ao buscar em GoFilmes para {titles}: {e}")
        return []

@app.get("/stream/{type}/{id}.json")
@cache(expire=3600) # Cache de 1 hora
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

    titles, _ = search_term(imdb_id)
    if not titles:
        # Se não encontrar títulos, ainda tenta a busca local
        local_streams = await search_serve_async(imdb_id, type, season, episode)
        return add_cors(JSONResponse(content={"streams": local_streams}))

    # Executa todas as buscas em paralelo
    results = await asyncio.gather(
        search_serve_async(imdb_id, type, season, episode),
        search_link_async(id),
        search_gofilmes_async(titles, type, season, episode)
    )

    # Junta os resultados de todas as fontes
    all_streams = [stream for result in results for stream in result]
        
    return add_cors(JSONResponse(content={"streams": all_streams}))

@app.options("/{path:path}")
@limiter.limit(rate_limit)
async def options_handler(path: str, request: Request):
    return add_cors(Response(status_code=204))
