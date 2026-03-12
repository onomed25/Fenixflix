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
import on
import go  # <- Importando o novo módulo go.py

# Carrega as variáveis do arquivo .env
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

# Pega a chave do TMDB EXCLUSIVAMENTE do arquivo .env
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    print("AVISO: A variável TMDB_API_KEY não foi encontrada no arquivo .env!")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

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
    url_tmdb = f"https://94c8cb9f702d-tmdb-addon.baby-beamup.club/pt-BR/meta/{content_type}/{imdb_id}.json"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            resp = await client.get(url_tmdb, timeout=5)
            if resp.status_code == 200:
                meta = resp.json().get("meta", {})
                if meta: return {"id": imdb_id, "type": content_type, "name": meta.get("name", f"Conteúdo {imdb_id}"), "poster": meta.get("poster"), "description": meta.get("description", "Sinopse não disponível.")}
        except Exception: pass

        url_cinemeta = f"https://v3-cinemeta.strem.io/meta/{content_type}/{imdb_id}.json"
        try:
            resp = await client.get(url_cinemeta, timeout=5)
            if resp.status_code == 200:
                meta = resp.json().get("meta", {})
                if meta: return {"id": imdb_id, "type": content_type, "name": meta.get("name", f"Conteúdo {imdb_id}"), "poster": meta.get("poster"), "description": meta.get("description", "Sinopse não disponível.")}
        except Exception: pass

    return {"id": imdb_id, "type": content_type, "name": f"Conteúdo {imdb_id}"}

# --- FUNÇÃO COM TMDB DIRETO PARA TÍTULOS PT-BR CONFIÁVEIS ---
async def obter_titulos_publicos(imdb_id, content_type):
    titulos = []
    print(f"\n[DEBUG - APP] Buscando títulos públicos para o ID: {imdb_id} | Tipo: {content_type}")

    # Fonte 1: TMDB direto com pt-BR (mais confiável)
    tmdb_type = "movie" if content_type == "movie" else "tv"
    url_tmdb_ptbr = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=pt-BR"
    url_tmdb_orig = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=en-US"

    # Fonte 2: addons públicos como fallback
    url_ptbr_addon = f"https://94c8cb9f702d-tmdb-addon.baby-beamup.club/pt-BR/meta/{content_type}/{imdb_id}.json"
    url_cinemeta = f"https://v3-cinemeta.strem.io/meta/{content_type}/{imdb_id}.json"

    async with httpx.AsyncClient() as client:
        # --- Tenta TMDB direto primeiro ---
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

            if nome_ptbr:
                titulos.append(nome_ptbr)
                print(f"[DEBUG - APP] Título PT-BR (TMDB direto): '{nome_ptbr}'")

            if nome_orig and nome_orig not in titulos:
                titulos.append(nome_orig)
                print(f"[DEBUG - APP] Título Original (TMDB direto): '{nome_orig}'")

        except Exception as e:
            print(f"[DEBUG - APP] Falha no TMDB direto: {e}")

        # --- Fallback: addons públicos se TMDB não retornou nada ---
        if not titulos:
            print(f"[DEBUG - APP] TMDB direto falhou, tentando addons públicos...")
            try:
                req_pt_addon, req_cinemeta = await asyncio.gather(
                    client.get(url_ptbr_addon, timeout=5),
                    client.get(url_cinemeta, timeout=5),
                    return_exceptions=True
                )

                if not isinstance(req_pt_addon, Exception) and req_pt_addon.status_code == 200:
                    nome_pt = req_pt_addon.json().get("meta", {}).get("name")
                    if nome_pt and not nome_pt.startswith("Conteúdo "):
                        titulos.append(nome_pt)
                        print(f"[DEBUG - APP] Título PT-BR (addon): '{nome_pt}'")

                if not isinstance(req_cinemeta, Exception) and req_cinemeta.status_code == 200:
                    nome_en = req_cinemeta.json().get("meta", {}).get("name")
                    if nome_en and not nome_en.startswith("Conteúdo ") and nome_en not in titulos:
                        titulos.append(nome_en)
                        print(f"[DEBUG - APP] Título Original (cinemeta): '{nome_en}'")

            except Exception as e:
                print(f"[DEBUG - APP] Falha nos addons públicos: {e}")

    print(f"[DEBUG - APP] Lista final de títulos enviada para busca: {titulos}")
    return titulos

async def build_recent_catalog():
    url = "http://87.106.82.84:14923/api/all"
    movies = []
    series = []

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            if resp.status_code != 200:
                return {"movie": [], "series": []}
            all_data = resp.json()
    except Exception:
        return {"movie": [], "series": []}

    items = list(all_data.values())

    for data in items:
        if len(movies) >= 25 and len(series) >= 25:
            break

        imdb_id = data.get("id")
        if not imdb_id:
            continue

        content_type = data.get("type", "movie")
        streams = data.get("streams", {})

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
            except Exception: pass

    catalogs = await build_recent_catalog()
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(catalogs, f, ensure_ascii=False)
    except Exception: pass

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

@app.get("/catalog/{type}/{id}.json")
@app.get("/catalog/{type}/{id}/{extra}.json")
async def catalog_endpoint(type: str, id: str, extra: str = None):
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
        except Exception: pass

    tmdb_id = await converter_imdb_para_tmdb(clean_id)

    # Função sem API buscando os títulos agora com debug no terminal
    titles_to_search = await obter_titulos_publicos(clean_id, type)

    def create_task(func, *args):
        if asyncio.iscoroutinefunction(func): return func(*args)
        return asyncio.to_thread(func, *args)

    tasks = [
        create_task(serve.search_serve, clean_id, type, season, episode),
        create_task(archive.search_serve, clean_id, type, season, episode)
    ]

    if tmdb_id:
        tasks.append(create_task(on.search_serve, tmdb_id, type, season, episode))

    if titles_to_search:
        tasks.append(create_task(go.search_serve, titles_to_search, type, season, episode))

    resultados = await asyncio.gather(*tasks, return_exceptions=True)
    todos_streams = []

    for res in resultados:
        if isinstance(res, list):
            for stream_info in res:
                if "behaviorHints" in stream_info:
                    del stream_info["behaviorHints"]

                todos_streams.append(stream_info)

    # Prioridade: só mostra Mediafire; se não tiver, mostra tudo
    mediafire_streams = [s for s in todos_streams if "mediafire" in s.get("url", "").lower()]

    if mediafire_streams:
        print(f"[DEBUG - APP] {len(mediafire_streams)} stream(s) Mediafire encontrado(s), exibindo apenas eles.")
        final_streams = mediafire_streams
    else:
        print(f"[DEBUG - APP] Nenhum Mediafire encontrado, exibindo todos os {len(todos_streams)} stream(s).")
        final_streams = todos_streams

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
        except Exception: pass

        url_cinemeta = f"https://v3-cinemeta.strem.io/meta/{type}/{id}.json"
        try:
            resp = await client.get(url_cinemeta, timeout=5)
            if resp.status_code == 200: return JSONResponse(content=resp.json())
        except Exception: pass

    return JSONResponse(content={"meta": {"id": id, "type": type, "name": f"Conteúdo {id}"}})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
