# app.py
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
from contextlib import asynccontextmanager
from dotenv import load_dotenv

import serve
import justwatch
import streamflix
import doramogo
import mywallpaper
import on

load_dotenv()

VERSION = "1.0.5"

CACHE_DIR = "cache"
CATALOG_CACHE_TIME = 6 * 60 * 60

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

_http_client: httpx.AsyncClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _http_client
    _http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(15.0, connect=5.0),
        follow_redirects=True,
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=30),
        verify=False,
    )
    yield
    await _http_client.aclose()

app = FastAPI(lifespan=lifespan)

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


async def obter_dados_base_tmdb(imdb_id: str, content_type: str):
    """
    Faz uma única busca no TMDB e retorna tanto o tmdb_id quanto a lista de títulos.
    """
    tmdb_id_final = None
    titulos = []
    tmdb_type = "movie" if content_type == "movie" else "tv"

    if imdb_id.startswith("tmdb:"):
        tmdb_id_final = imdb_id.split(":")[1]

        req_ptbr, req_orig = await asyncio.gather(
            _http_client.get(f"https://api.themoviedb.org/3/{tmdb_type}/{tmdb_id_final}?api_key={TMDB_API_KEY}&language=pt-BR"),
            _http_client.get(f"https://api.themoviedb.org/3/{tmdb_type}/{tmdb_id_final}?api_key={TMDB_API_KEY}&language=en-US"),
            return_exceptions=True
        )

        if not isinstance(req_ptbr, Exception) and req_ptbr.status_code == 200:
            name = req_ptbr.json().get("title") or req_ptbr.json().get("name")
            if name: titulos.append(name)

        if not isinstance(req_orig, Exception) and req_orig.status_code == 200:
            name = req_orig.json().get("title") or req_orig.json().get("name")
            if name and name not in titulos: titulos.append(name)

    else:
        req_ptbr, req_orig = await asyncio.gather(
            _http_client.get(f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=pt-BR"),
            _http_client.get(f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=en-US"),
            return_exceptions=True
        )

        def extrair_dados_find(resp, tipo):
            if isinstance(resp, Exception) or resp.status_code != 200:
                return None, None

            data = resp.json()
            results = data.get(f"{tipo}_results", [])

            if results:
                result_id = str(results[0].get("id"))
                result_name = results[0].get("title") or results[0].get("name")
                return result_id, result_name
            return None, None

        id_ptbr, nome_ptbr = extrair_dados_find(req_ptbr, tmdb_type)
        if id_ptbr: tmdb_id_final = id_ptbr
        if nome_ptbr: titulos.append(nome_ptbr)

        id_orig, nome_orig = extrair_dados_find(req_orig, tmdb_type)
        if id_orig and not tmdb_id_final: tmdb_id_final = id_orig
        if nome_orig and nome_orig not in titulos: titulos.append(nome_orig)

    return tmdb_id_final, titulos


async def notificar_falta_servidor(imdb_id, content_type, season=None, episode=None):
    msg = f"Falta {content_type}: {imdb_id}"
    if content_type == 'series' and season and episode:
        msg += f" (Temporada {season}, Episódio {episode})"
    url = "http://87.106.82.84:14923/aviso_falta"
    try:
        await _http_client.get(url, params={"msg": msg})
    except Exception:
        pass


async def fetch_cinemeta(imdb_id, content_type):
    for url in [
        f"https://94c8cb9f702d-tmdb-addon.baby-beamup.club/pt-BR/meta/{content_type}/{imdb_id}.json",
        f"https://v3-cinemeta.strem.io/meta/{content_type}/{imdb_id}.json"
    ]:
        try:
            resp = await _http_client.get(url)
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


async def build_recent_catalog():
    url = "http://87.106.82.84:14923/api/all"
    movies = []
    series = []
    try:
        resp = await _http_client.get(url)
        if resp.status_code != 200:
            return {"movie": [], "series": []}
        all_data = resp.json()
    except Exception:
        return {"movie": [], "series": []}

    for data in list(all_data.values()):
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
                    return json.load(f).get(content_type, [])
            except Exception:
                pass
    catalogs = await build_recent_catalog()
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(catalogs, f, ensure_ascii=False)
    except Exception:
        pass
    return catalogs.get(content_type, [])


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    manifest_data = {"name": "FENIXFLIX", "description": "Addon de Filmes e Séries", "types": ["movie", "series"]}
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "manifest": manifest_data, "version": VERSION})


@app.get("/manifest.json")
async def manifest_endpoint():
    return JSONResponse(content={
        "id": "com.fenixflix", "version": VERSION, "name": "FENIXFLIX",
        "description": "Addon de Filmes e Séries",
        "logo": "https://i.imgur.com/9SKgxfU.png",
        "background": "https://dl.strem.io/addon-background.jpg",
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


@app.get("/catalog/{type}/{id}.json")
@app.get("/catalog/{type}/{id}/{extra}.json")
async def catalog_endpoint(type: str, id: str, extra: str = None):
    if extra and "skip" in extra:
        return JSONResponse(content={"metas": []})
    if id == "recentes_servidor":
        return JSONResponse(content={"metas": await get_recent_catalog_cached(type)})
    elif id == "popular":
        return JSONResponse(content={"metas": await asyncio.to_thread(justwatch.fetch_catalog, id, type)})
    return JSONResponse(content={"metas": []})


@app.get("/stream/{type}/{id}.json")
@limiter.limit("15/minute")
async def stream(type: str, id: str, request: Request):
    print(f"\n=======================================================")
    print(f"[DEBUG - APP] 🎬 NOVO PEDIDO RECEBIDO - ID: {id}, Tipo: {type}")
    season, episode = None, None

    if id.startswith("tmdb:"):
        parts = id.split(':')
        clean_id = f"tmdb:{parts[1]}"
        if type == 'series' and len(parts) >= 4:
            season, episode = int(parts[2]), int(parts[3])
    else:
        parts = id.split(':')
        clean_id = parts[0]
        if type == 'series' and len(parts) >= 3:
            season, episode = int(parts[1]), int(parts[2])

    print("[DEBUG - APP] Buscando informações no TMDB...")
    tmdb_id, titles = await obter_dados_base_tmdb(clean_id, type)

    print(f"[DEBUG - APP] Resultado TMDB -> ID: {tmdb_id} | Títulos encontrados: {titles}")

    async def fetch_serve():
        try:
            res = await serve.search_serve(clean_id, type, season, episode, client=_http_client)
            return res if res else []
        except Exception as e:
            return []

    async def fetch_streamflix():
        try:
            if not titles: return []
            res = await streamflix.search_serve(titles, type, season, episode, client=_http_client)
            return res if res else []
        except Exception as e:
            return []

    async def fetch_doramogo():
        try:
            if not tmdb_id or not titles:
                print(f"[DEBUG - APP -> Doramogo] ❌ Cancelado. Faltam Títulos ou TMDB ID.")
                return []

            res = await doramogo.search_serve(tmdb_id, titles, type, season, episode, client=_http_client)

            return res if res else []
        except Exception as e:
            return []

    async def fetch_mywallpaper():
        try:
            if not tmdb_id or not titles: return []
            res = await mywallpaper.search_serve(tmdb_id, titles, type, season, episode, client=_http_client)
            return res if res else []
        except Exception as e:
            return []

    async def fetch_on():
        try:
            if not tmdb_id: return []
            res = await on.search_serve(tmdb_id, type, season, episode, client=_http_client)
            return res if res else []
        except Exception as e:
            return []

    print("[DEBUG - APP] Disparando todos os scrapers simultaneamente...")

    resultados = await asyncio.gather(
        fetch_serve(),
        fetch_streamflix(),
        fetch_doramogo(),
        fetch_mywallpaper(),
        fetch_on(),
        return_exceptions=True
    )

    todos_streams = []

    for res in resultados:
        if isinstance(res, Exception):
            continue
        if isinstance(res, list):
            for stream_info in res:
                if not stream_info.get("url"):
                    continue
                if "behaviorHints" not in stream_info:
                    stream_info["behaviorHints"] = {
                        "notWebReady": False,
                        "bingeGroup": "fenixflix"
                    }
                todos_streams.append(stream_info)

    if not todos_streams:
        print("[DEBUG - APP] Nenhum fluxo encontrado por nenhum scraper.")
        asyncio.create_task(notificar_falta_servidor(clean_id, type, season, episode))
    else:
        print(f"[DEBUG - APP] Concluído! Foram enviados {len(todos_streams)} links para o usuário.")
    print(f"=======================================================\n")

    return JSONResponse(content={"streams": todos_streams})


@app.get("/meta/{type}/{id}.json")
async def meta_endpoint(type: str, id: str):
    for url in [
        f"https://94c8cb9f702d-tmdb-addon.baby-beamup.club/pt-BR/meta/{type}/{id}.json",
        f"https://v3-cinemeta.strem.io/meta/{type}/{id}.json"
    ]:
        try:
            resp = await _http_client.get(url)
            if resp.status_code == 200:
                return JSONResponse(content=resp.json())
        except Exception:
            pass
    return JSONResponse(content={"meta": {"id": id, "type": type, "name": f"Conteúdo {id}"}})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
