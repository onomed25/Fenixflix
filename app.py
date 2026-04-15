from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import asyncio
import httpx
import os
import time
import json
import uvicorn
import random  
from dotenv import load_dotenv

import serve
import justwatch
import on
import go
import fshd
import fimoo

load_dotenv()

VERSION = "1.0.5"
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
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

CACHE_DIR = "cache"
CATALOG_CACHE_TIME = 6 * 60 * 60
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

KOYEB = [
    "https://passing-melinda-onomed1-d0cbec40.koyeb.app",
    "https://husky-denny-fenixflixaddon-ec8e842b.koyeb.app"
]

async def converter_imdb_para_tmdb(imdb_id: str):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("movie_results"):
                    return str(data["movie_results"][0]["id"])
                elif data.get("tv_results"):
                    return str(data["tv_results"][0]["id"])
        except Exception:
            pass
    return None

async def notificar_falta_servidor(imdb_id, content_type, season=None, episode=None):
    msg = f"Falta {content_type}: {imdb_id}"
    if content_type == 'series' and season and episode:
        msg += f" (Temporada {season}, Episódio {episode})"
    url = "http://87.106.82.84:14923/aviso_falta"
    async with httpx.AsyncClient() as client:
        try:
            await client.get(url, params={"msg": msg}, timeout=3)
        except Exception:
            pass

async def fetch_cinemeta(imdb_id, content_type):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        for url in [
            f"https://94c8cb9f702d-tmdb-addon.baby-beamup.club/pt-BR/meta/{content_type}/{imdb_id}.json",
            f"https://v3-cinemeta.strem.io/meta/{content_type}/{imdb_id}.json"
        ]:
            try:
                resp = await client.get(url, timeout=5)
                if resp.status_code == 200:
                    meta = resp.json().get("meta", {})
                    if meta:
                        return {
                            "id": imdb_id,
                            "type": content_type,
                            "name": meta.get("name", f"Conteúdo {imdb_id}"),
                            "poster": meta.get("poster"),
                            "description": meta.get("description", "Sinopse não disponível.")
                        }
            except Exception:
                pass
    return {"id": imdb_id, "type": content_type, "name": f"Conteúdo {imdb_id}"}

async def obter_titulos_publicos(imdb_id, content_type):
    titulos = []
    tmdb_type = "movie" if content_type == "movie" else "tv"
    url_tmdb_ptbr = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=pt-BR"
    url_tmdb_orig = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=en-US"

    async with httpx.AsyncClient() as client:
        try:
            req_ptbr, req_orig = await asyncio.gather(
                client.get(url_tmdb_ptbr, timeout=5),
                client.get(url_tmdb_orig, timeout=5),
                return_exceptions=True
            )

            def extrair_nome_tmdb(resp, tipo):
                if isinstance(resp, Exception) or resp.status_code != 200:
                    return None
                data = resp.json()
                results = data.get(f"{tipo}_results", [])
                if results:
                    return results[0].get("title") or results[0].get("name")
                return None

            nome_ptbr = extrair_nome_tmdb(req_ptbr, tmdb_type)
            nome_orig = extrair_nome_tmdb(req_orig, tmdb_type)

            if nome_ptbr: titulos.append(nome_ptbr)
            if nome_orig and nome_orig not in titulos: titulos.append(nome_orig)
        except Exception:
            pass
    return titulos

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    manifest_data = {"name": "FENIXFLIX", "description": "Addon de Filmes e Séries", "types": ["movie", "series"]}
    return templates.TemplateResponse(name="index.html", context={"request": request, "manifest": manifest_data, "version": VERSION})

@app.get("/manifest.json")
async def manifest_endpoint():
    return JSONResponse(content={
        "id": "com.fenixflix", "version": VERSION, "name": "FENIXFLIX",
        "description": "Addon de Filmes e Séries",
        "logo": "https://i.imgur.com/9SKgxfU.png",
        "resources": ["stream", "catalog", "meta"],
        "types": ["movie", "series"],
        "catalogs": [
            {"type": "movie", "id": "popular", "name": "Populares"},
            {"type": "movie", "id": "recentes_servidor", "name": "Recém Adicionado (Fenix)"},
            {"type": "series", "id": "popular", "name": "Populares"},
            {"type": "series", "id": "recentes_servidor", "name": "Recém Adicionado (Fenix)"}
        ],
        "idPrefixes": ["tt", "tmdb"]
    })

@app.get("/stream/{type}/{id}.json")
@limiter.limit("15/minute")
async def stream(type: str, id: str, request: Request):
    clean_id = id.split(':')[0]
    season, episode = None, None
    if type == 'series':
        try:
            parts = id.split(':')
            season, episode = int(parts[1]), int(parts[2])
        except Exception: pass

    tmdb_id = await converter_imdb_para_tmdb(clean_id)
    titles_to_search = await obter_titulos_publicos(clean_id, type)

    def create_task(func, *args):
        if asyncio.iscoroutinefunction(func): return func(*args)
        return asyncio.to_thread(func, *args)

    tasks = [
        create_task(serve.search_serve, clean_id, type, season, episode),
    ]
    if tmdb_id:
        tasks.extend([
            create_task(on.search_serve, tmdb_id, type, season, episode),
            create_task(fshd.search_serve, tmdb_id, type, season, episode),
            create_task(fimoo.search_serve, tmdb_id, type, season, episode)
        ])
    if titles_to_search:
        tasks.append(create_task(go.search_serve, titles_to_search, type, season, episode))

    resultados = await asyncio.gather(*tasks, return_exceptions=True)
    todos_streams = []

    for res in resultados:
        if isinstance(res, list):
            for stream_info in res:
                url = stream_info.get("url", "")
                if not url: continue

                escolhido = random.choice(KOYEB)

                if "87.106.82.84:14923" in url:
                    path = url.split(":14923")[-1]
                    stream_info["url"] = f"{escolhido}{path}"

                elif "passing-melinda-onomed1-d0cbec40.koyeb.app" in url:
                    stream_info["url"] = url.replace("https://passing-melinda-onomed1-d0cbec40.koyeb.app", escolhido)

                if "behaviorHints" not in stream_info:
                    stream_info["behaviorHints"] = {"notWebReady": False, "bingeGroup": "fenixflix"}

                todos_streams.append(stream_info)

    if not todos_streams:
        asyncio.create_task(notificar_falta_servidor(clean_id, type, season, episode))

    return JSONResponse(content={"streams": todos_streams})

@app.get("/meta/{type}/{id}.json")
async def meta_endpoint(type: str, id: str):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        for url in [
            f"https://94c8cb9f702d-tmdb-addon.baby-beamup.club/pt-BR/meta/{type}/{id}.json",
            f"https://v3-cinemeta.strem.io/meta/{type}/{id}.json"
        ]:
            try:
                resp = await client.get(url, timeout=5)
                if resp.status_code == 200: return JSONResponse(content=resp.json())
            except Exception: pass
    return JSONResponse(content={"meta": {"id": id, "type": type, "name": f"Conteúdo {id}"}})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
