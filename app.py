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
import streamflix
import doramogo
import mywallpaper
import on
import justwatch

load_dotenv()

VERSION = "1.0.5"
CACHE_DIR = "cache"
CATALOG_CACHE_TIME = 6 * 60 * 60
SCRAPER_STATUS_FILE = os.path.join(CACHE_DIR, "scrapers_status.json")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

_http_client: httpx.AsyncClient = None
tmdb_semaphore = asyncio.Semaphore(20)

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


def load_scraper_cache():
    if os.path.exists(SCRAPER_STATUS_FILE):
        try:
            with open(SCRAPER_STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    return {}

def save_scraper_cache(cache_data):
    try:
        with open(SCRAPER_STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except: pass

# --- FUNÇÕES TMDB ---

async def obter_dados_base_tmdb(imdb_id: str, content_type: str):
    tmdb_id_final = None
    titulos = []
    tmdb_type = "movie" if content_type == "movie" else "tv"

    if imdb_id.startswith("tmdb:"):
        tmdb_id_final = imdb_id.split(":")[1]
        url_pt = f"https://api.themoviedb.org/3/{tmdb_type}/{tmdb_id_final}?api_key={TMDB_API_KEY}&language=pt-BR"
        url_en = f"https://api.themoviedb.org/3/{tmdb_type}/{tmdb_id_final}?api_key={TMDB_API_KEY}&language=en-US"
        
        reqs = await asyncio.gather(_http_client.get(url_pt), _http_client.get(url_en), return_exceptions=True)
        for r in reqs:
            if not isinstance(r, Exception) and r.status_code == 200:
                name = r.json().get("title") or r.json().get("name")
                if name and name not in titulos: titulos.append(name)
    else:
        url_pt = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=pt-BR"
        url_en = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=en-US"
        
        reqs = await asyncio.gather(_http_client.get(url_pt), _http_client.get(url_en), return_exceptions=True)
        for r in reqs:
            if not isinstance(r, Exception) and r.status_code == 200:
                data = r.json()
                results = data.get(f"{tmdb_type}_results", [])
                if results:
                    if not tmdb_id_final: tmdb_id_final = str(results[0].get("id"))
                    name = results[0].get("title") or results[0].get("name")
                    if name and name not in titulos: titulos.append(name)

    return tmdb_id_final, titulos

async def fetch_tmdb_meta_ptbr(item_id: str, content_type: str, full_meta=False):
    async with tmdb_semaphore:
        tmdb_type = "movie" if content_type == "movie" else "tv"
        tmdb_id_final = None
        
        if item_id.startswith("tmdb:"):
            tmdb_id_final = item_id.split(":")[1]
        else:
            url_find = f"https://api.themoviedb.org/3/find/{item_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=pt-BR"
            try:
                resp = await _http_client.get(url_find, timeout=5.0)
                if resp.status_code == 200:
                    results = resp.json().get(f"{tmdb_type}_results", [])
                    if results:
                        tmdb_id_final = str(results[0].get("id"))
            except: pass

        if tmdb_id_final:
            url_details = f"https://api.themoviedb.org/3/{tmdb_type}/{tmdb_id_final}?api_key={TMDB_API_KEY}&language=pt-BR"
            try:
                resp = await _http_client.get(url_details, timeout=5.0)
                if resp.status_code == 200:
                    data = resp.json()
                    title = data.get("title") or data.get("name") or f"Conteúdo {item_id}"
                    
                    poster_path = data.get("poster_path")
                    poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                    
                    backdrop_path = data.get("backdrop_path")
                    background = f"https://image.tmdb.org/t/p/original{backdrop_path}" if backdrop_path else None
                    
                    description = data.get("overview") or "Sinopse não disponível."
                    
                    meta_obj = {
                        "id": item_id,
                        "type": content_type,
                        "name": title,
                        "poster": poster,
                        "background": background,
                        "description": description
                    }
                    
                    if full_meta:
                        meta_obj["releaseInfo"] = data.get("release_date", "")[:4] if content_type == "movie" else data.get("first_air_date", "")[:4]
                        meta_obj["voteAverage"] = data.get("vote_average")
                    
                    return meta_obj
            except: pass
            
        return {"id": item_id, "type": content_type, "name": f"Conteúdo {item_id}"}


async def notificar_falta_servidor(imdb_id, content_type, season=None, episode=None):
    msg = f"Falta {content_type}: {imdb_id}"
    if content_type == 'series' and season and episode:
        msg += f" (Temporada {season}, Episódio {episode})"
    url = "http://87.106.82.84:14923/aviso_falta"
    try: await _http_client.get(url, params={"msg": msg})
    except: pass


async def build_recent_catalog():
    url = "http://87.106.82.84:14923/api/all"
    print(f"[DEBUG - CATÁLOGO] Acessando a API do servidor: {url}")
    
    try:
        resp = await _http_client.get(url, timeout=30.0) 
        if resp.status_code == 200:
            all_data = resp.json()
        else:
            return {"movie": [], "series": []}
    except:
        return {"movie": [], "series": []}
    
    items = all_data if isinstance(all_data, list) else list(all_data.values())
    
    movie_ids, series_ids = [], []
    for data in items:
        if len(movie_ids) >= 25 and len(series_ids) >= 25: break
        imdb_id = data.get("id")
        if not imdb_id: continue
        content_type = data.get("type", "movie")
        streams = data.get("streams", {})
        
        if content_type == "series" and isinstance(streams, dict) and len(series_ids) < 25:
            series_ids.append(imdb_id)
        elif (content_type == "movie" or isinstance(streams, list)) and len(movie_ids) < 25:
            movie_ids.append(imdb_id)

    print(f"[DEBUG - CATÁLOGO] Traduzindo {len(movie_ids)} filmes e {len(series_ids)} séries (Recentes) para PT-BR...")

    movie_tasks = [fetch_tmdb_meta_ptbr(i, "movie") for i in movie_ids]
    series_tasks = [fetch_tmdb_meta_ptbr(i, "series") for i in series_ids]

    movies_raw = await asyncio.gather(*movie_tasks, return_exceptions=True)
    series_raw = await asyncio.gather(*series_tasks, return_exceptions=True)

    movies = [m for m in movies_raw if isinstance(m, dict)]
    series = [s for s in series_raw if isinstance(s, dict)]
            
    return {"movie": movies, "series": series}

async def get_recent_catalog_cached(content_type):
    cache_file = os.path.join(CACHE_DIR, "server_recent_catalog.json")
    
    if os.path.exists(cache_file) and (time.time() - os.path.getmtime(cache_file)) < CATALOG_CACHE_TIME:
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                dados_salvos = json.load(f)
                itens_salvos = dados_salvos.get(content_type, [])
                if len(itens_salvos) > 0: return itens_salvos
        except: pass

    catalogs = await build_recent_catalog()
    
    if len(catalogs.get("movie", [])) > 0 or len(catalogs.get("series", [])) > 0:
        try:
            with open(cache_file, "w", encoding="utf-8") as f: 
                json.dump(catalogs, f, ensure_ascii=False, indent=2)
        except: pass
            
    return catalogs.get(content_type, [])

async def get_popular_catalog_cached(content_type):
    cache_file = os.path.join(CACHE_DIR, f"tmdb_popular_{content_type}.json")
    
    if os.path.exists(cache_file) and (time.time() - os.path.getmtime(cache_file)) < CATALOG_CACHE_TIME:
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                dados_salvos = json.load(f)
                if len(dados_salvos) > 0: return dados_salvos
        except: pass

    jw_metas = await asyncio.to_thread(justwatch.fetch_catalog, "popular", content_type)
    if not jw_metas: return []

    print(f"[DEBUG - CATÁLOGO] Traduzindo {len(jw_metas)} títulos populares para PT-BR pelo TMDB...")
    tasks = [fetch_tmdb_meta_ptbr(m["id"], content_type) for m in jw_metas]
    resultados = await asyncio.gather(*tasks, return_exceptions=True)

    metas_finais = []
    for i, res in enumerate(resultados):
        if isinstance(res, dict) and res.get("name"):
            metas_finais.append(res)
        else:
            metas_finais.append(jw_metas[i])

    if metas_finais:
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(metas_finais, f, ensure_ascii=False, indent=2)
        except: pass

    return metas_finais


# --- ENDPOINTS PRINCIPAIS ---

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
async def catalog_endpoint(type: str, id: str, extra: str = None, skip: int = 0):
    if extra and extra.startswith("skip="):
        try:
            val_str = extra.replace(".json", "").split("=")[1]
            skip_val = int(val_str)
            if skip_val > 0:
                return JSONResponse(content={"metas": []})
        except:
            pass
            
    if skip > 0:
        return JSONResponse(content={"metas": []})

    if id == "recentes_servidor":
        metas = await get_recent_catalog_cached(type)
        return JSONResponse(content={"metas": metas})
        
    elif id == "popular":
        metas = await get_popular_catalog_cached(type)
        return JSONResponse(content={"metas": metas})
    
    return JSONResponse(content={"metas": []})

@app.get("/meta/{type}/{id}.json")
async def meta_endpoint(type: str, id: str):
    # 1. Pega os metadados base do Cinemeta (Padrão em Inglês)
    base_meta = None
    for url in [f"https://v3-cinemeta.strem.io/meta/{type}/{id}.json", f"https://94c8cb9f702d-tmdb-addon.baby-beamup.club/meta/{type}/{id}.json"]:
        try:
            resp = await _http_client.get(url, timeout=8.0)
            if resp.status_code == 200:
                base_meta = resp.json().get("meta")
                if base_meta:
                    break
        except:
            pass
    
    if not base_meta:
        base_meta = {"id": id, "type": type, "name": f"Conteúdo {id}"}

    # 2. Puxa a tradução forçada em PT-BR do nosso TMDB
    tmdb_ptbr = await fetch_tmdb_meta_ptbr(id, type, full_meta=True)
    
    # 3. Mescla APENAS a Capa e o Título. O resto fica em inglês!
    if tmdb_ptbr:
        if tmdb_ptbr.get("name"):
            base_meta["name"] = tmdb_ptbr.get("name")
        if tmdb_ptbr.get("poster"):
            base_meta["poster"] = tmdb_ptbr.get("poster")

    return JSONResponse(content={"meta": base_meta})

@app.get("/stream/{type}/{id}.json")
@limiter.limit("20/minute")
async def stream(type: str, id: str, request: Request):
    print(f"\n[DEBUG] 🎬 Pedido: {id} | Tipo: {type}")
    
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

    cache_status = load_scraper_cache()
    base_id = clean_id 
    entry = cache_status.get(base_id, {})
    
    if entry:
        tmdb_id = entry.get("tmdb_id")
        titles = entry.get("titles", [])
        if type == "series":
            ep_key = f"{season}:{episode}"
            scraper_flags = entry.get("episodes", {}).get(ep_key, {})
        else:
            scraper_flags = entry.get("scrapers", {})
        print(f"[DEBUG] 🧠 Cache carregado para {base_id}")
    else:
        tmdb_id, titles = await obter_dados_base_tmdb(clean_id, type)
        scraper_flags = {}

    tasks_to_run = {
        "serve": serve.search_serve(clean_id, type, season, episode, client=_http_client)
    }

    if scraper_flags.get("doramogo") != "N": tasks_to_run["doramogo"] = doramogo.search_serve(tmdb_id, titles, type, season, episode, client=_http_client)
    if scraper_flags.get("on") != "N": tasks_to_run["on"] = on.search_serve(tmdb_id, type, season, episode, client=_http_client)
    if scraper_flags.get("mywallpaper") != "N": tasks_to_run["mywallpaper"] = mywallpaper.search_serve(tmdb_id, titles, type, season, episode, client=_http_client)
    if scraper_flags.get("streamflix") != "N": tasks_to_run["streamflix"] = streamflix.search_serve(titles, type, season, episode, client=_http_client)

    names = list(tasks_to_run.keys())
    results = await asyncio.gather(*tasks_to_run.values(), return_exceptions=True)
    
    todos_streams = []
    novos_flags = scraper_flags.copy()

    for i, res in enumerate(results):
        nome = names[i]
        if isinstance(res, Exception) or not res:
            if nome != "serve": novos_flags[nome] = "N"
            continue
        
        if nome != "serve": novos_flags[nome] = "S"
        
        for stream_info in res:
            if stream_info.get("url"):
                if "behaviorHints" not in stream_info:
                    stream_info["behaviorHints"] = {"notWebReady": False, "bingeGroup": "fenixflix"}
                todos_streams.append(stream_info)

    if base_id not in cache_status:
        cache_status[base_id] = {"tmdb_id": tmdb_id, "titles": titles, "type": type}

    if type == "series":
        if "episodes" not in cache_status[base_id]:
            cache_status[base_id]["episodes"] = {}
        cache_status[base_id]["episodes"][f"{season}:{episode}"] = novos_flags
    else:
        cache_status[base_id]["scrapers"] = novos_flags

    save_scraper_cache(cache_status)
    
    if not todos_streams:
        asyncio.create_task(notificar_falta_servidor(clean_id, type, season, episode))
        
    return JSONResponse(content={"streams": todos_streams})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)