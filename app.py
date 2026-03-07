from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio
import httpx
import re
import os
import time
import json
from datetime import datetime
from urllib.parse import quote
import uvicorn
from dotenv import load_dotenv

import serve
import archive
import justwatch

load_dotenv()

VERSION = "1.0.4"
app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)

CACHE_DIR = "cache"
CATALOG_CACHE_TIME = 6 * 60 * 60

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

async def notificar_falta_servidor(imdb_id, content_type, season=None, episode=None):
    msg = f"Falta {content_type}: {imdb_id}"
    if content_type == 'series' and season and episode:
        msg += f" (Temporada {season}, Episódio {episode})"

    url = "http://87.106.82.84:14923/aviso_falta"
    async with httpx.AsyncClient() as client:
        try:
            await client.get(url, params={"msg": msg}, timeout=3)
        except:
            pass

async def fetch_cinemeta(imdb_id, content_type):
    url_tmdb = f"https://94c8cb9f702d-tmdb-addon.baby-beamup.club/pt-BR/meta/{content_type}/{imdb_id}.json"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            resp = await client.get(url_tmdb, timeout=5)
            if resp.status_code == 200:
                meta = resp.json().get("meta", {})
                if meta: return {"id": imdb_id, "type": content_type, "name": meta.get("name", f"Conteúdo {imdb_id}"), "poster": meta.get("poster"), "description": meta.get("description", "Sinopse não disponível.")}
        except: pass

        url_cinemeta = f"https://v3-cinemeta.strem.io/meta/{content_type}/{imdb_id}.json"
        try:
            resp = await client.get(url_cinemeta, timeout=5)
            if resp.status_code == 200:
                meta = resp.json().get("meta", {})
                if meta: return {"id": imdb_id, "type": content_type, "name": meta.get("name", f"Conteúdo {imdb_id}"), "poster": meta.get("poster"), "description": meta.get("description", "Sinopse não disponível.")}
        except: pass

    return {"id": imdb_id, "type": content_type, "name": f"Conteúdo {imdb_id}"}

async def build_recent_catalog():
    # Nova rota da API que retorna tudo de uma vez do banco SQLite
    url = "http://87.106.82.84:14923/api/all"
    movies = []
    series = []

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            if resp.status_code != 200:
                return {"movie": [], "series": []}
            all_data = resp.json()
    except Exception as e:
        print(f"Erro ao buscar catálogo: {e}")
        return {"movie": [], "series": []}

    # Transformar os valores do dicionário recebido em uma lista
    items = list(all_data.values())

    # Iterar sobre os itens retornados do banco de dados
    for data in items:
        # Se já preencheu 25 de cada, pode parar para não sobrecarregar
        if len(movies) >= 25 and len(series) >= 25:
            break

        imdb_id = data.get("id")
        if not imdb_id:
            continue

        # Ler os dados direto do JSON recebido pela API
        content_type = data.get("type", "movie")
        streams = data.get("streams", {})

        # Separar Séries e Filmes buscando os metadados
        if content_type == "series" and isinstance(streams, dict) and len(series) < 25:
            meta = await fetch_cinemeta(imdb_id, "series")
            if meta: series.append(meta)

        elif (content_type == "movie" or isinstance(streams, list)) and len(movies) < 25:
            meta = await fetch_cinemeta(imdb_id, "movie")
            if meta: movies.append(meta)

    return {"movie": movies, "series": series}

async def get_recent_catalog_cached(content_type):
    cache_file = os.path.join(CACHE_DIR, "server_recent_catalog.json")
    if os.path.exists(cache_file):
        if (time.time() - os.path.getmtime(cache_file)) < CATALOG_CACHE_TIME:
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get(content_type, [])
            except: pass

    catalogs = await build_recent_catalog()
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(catalogs, f, ensure_ascii=False)
    except: pass

    return catalogs.get(content_type, [])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    manifest_data = {"name": "FENIXFLIX", "description": "Addon de Filmes e Séries", "types": ["movie", "series"]}
    return templates.TemplateResponse("index.html", {"request": request, "manifest": manifest_data, "version": VERSION})

@app.get("/manifest.json")
async def manifest_endpoint():
    return JSONResponse(content={
        "id": "com.fenixflix", "version": VERSION, "name": "FENIXFLIX",
        "description": "Addon de Filmes e Séries",
        "logo": "https://i.imgur.com/9SKgxfU.png",
        "background": "https://dl.strem.io/addon-background.jpg",
        "resources": ["stream", "catalog", "meta"], "types": ["movie", "series"],
        "catalogs": [
            {"type": "movie", "id": "popular", "name": "Populares"},
            {"type": "movie", "id": "recentes_servidor", "name": "Recém Adicionado (Fenix)"},
            {"type": "series", "id": "popular", "name": "Populares"},
            {"type": "series", "id": "recentes_servidor", "name": "Recém Adicionado (Fenix)"}
        ],
        "idPrefixes": ["tt", "tmdb"]
    })

# Adicionamos a segunda rota para suportar parâmetros extras como paginação
@app.get("/catalog/{type}/{id}.json")
@app.get("/catalog/{type}/{id}/{extra}.json")
async def catalog_endpoint(type: str, id: str, extra: str = None):

    # Se o Stremio estiver pedindo a página 2 em diante (skip=25, skip=50...)
    # Por enquanto, retornamos vazio para ele parar de procurar e não dar erro.
    if extra and "skip" in extra:
        return JSONResponse(content={"metas": []})

    if id == "recentes_servidor":
        catalogo = await get_recent_catalog_cached(type)
        return JSONResponse(content={"metas": catalogo})
    elif id == "popular":
        catalogo = await asyncio.to_thread(justwatch.fetch_catalog, id, type)
        return JSONResponse(content={"metas": catalogo})

    return JSONResponse(content={"metas": []})

@app.get("/stream/{type}/{id}.json")
@limiter.limit("15/minute")
async def stream(type: str, id: str, request: Request):
    clean_id = id.split(':')[0]
    season, episode = None, None
    if type == 'series':
        try:
            parts = id.split(':')
            season, episode = int(parts[1]), int(parts[2])
        except: pass

    def create_task(func, *args):
        if asyncio.iscoroutinefunction(func): return func(*args)
        return asyncio.to_thread(func, *args)

    tasks = [
        create_task(serve.search_serve, clean_id, type, season, episode),
        create_task(archive.search_serve, clean_id, type, season, episode)
    ]

    resultados = await asyncio.gather(*tasks, return_exceptions=True)
    final_streams = []

    for res in resultados:
        if isinstance(res, list):
            for stream_info in res:
                if "behaviorHints" in stream_info: del stream_info["behaviorHints"]

                url = stream_info.get("url", "")

                final_streams.append(stream_info)

    if not final_streams:
        asyncio.create_task(notificar_falta_servidor(clean_id, type, season, episode))

    return JSONResponse(content={"streams": final_streams})

@app.get("/meta/{type}/{id}.json")
async def meta_endpoint(type: str, id: str):
    url_tmdb = f"https://94c8cb9f702d-tmdb-addon.baby-beamup.club/pt-BR/meta/{type}/{id}.json"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            resp = await client.get(url_tmdb, timeout=5)
            if resp.status_code == 200: return JSONResponse(content=resp.json())
        except: pass

        url_cinemeta = f"https://v3-cinemeta.strem.io/meta/{type}/{id}.json"
        try:
            resp = await client.get(url_cinemeta, timeout=5)
            if resp.status_code == 200: return JSONResponse(content=resp.json())
        except: pass

    return JSONResponse(content={"meta": {"id": id, "type": type, "name": f"Conteúdo {id}"}})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
