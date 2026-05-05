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
SCRAPER_STATUS_FILE = os.path.join(CACHE_DIR, "scrapers_status.json")
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

# --- FUNÇÕES DE PERSISTÊNCIA ---

def load_scraper_cache():
    if os.path.exists(SCRAPER_STATUS_FILE):
        try:
            with open(SCRAPER_STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_scraper_cache(cache_data):
    try:
        with open(SCRAPER_STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except:
        pass

# --- AUXILIARES TMDB ---

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

# --- ENDPOINTS ---

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "version": VERSION})

@app.get("/manifest.json")
async def manifest():
    return {
        "id": "com.fenixflix", "version": VERSION, "name": "FENIXFLIX",
        "resources": ["stream", "catalog", "meta"], "types": ["movie", "series"],
        "idPrefixes": ["tt", "tmdb"]
    }

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

    # 1. LOGICA DE CACHE AGRUPADA
    cache_status = load_scraper_cache()
    base_id = clean_id # Agrupa todos os episódios sob o ID principal da obra
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

    # 2. FILTRAGEM DE SCRAPERS (S/N)
    # Serve.py é disparado sempre
    tasks_to_run = {
        "serve": serve.search_serve(clean_id, type, season, episode, client=_http_client)
    }

    if scraper_flags.get("doramogo") != "N":
        tasks_to_run["doramogo"] = doramogo.search_serve(tmdb_id, titles, type, season, episode, client=_http_client)
    
    if scraper_flags.get("on") != "N":
        tasks_to_run["on"] = on.search_serve(tmdb_id, type, season, episode, client=_http_client)
        
    if scraper_flags.get("mywallpaper") != "N":
        tasks_to_run["mywallpaper"] = mywallpaper.search_serve(tmdb_id, titles, type, season, episode, client=_http_client)
        
    if scraper_flags.get("streamflix") != "N":
        tasks_to_run["streamflix"] = streamflix.search_serve(titles, type, season, episode, client=_http_client)

    # 3. EXECUÇÃO
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
                todos_streams.append(stream_info)

    # 4. SALVAMENTO NO CACHE OTIMIZADO
    if base_id not in cache_status:
        cache_status[base_id] = {"tmdb_id": tmdb_id, "titles": titles, "type": type}

    if type == "series":
        if "episodes" not in cache_status[base_id]:
            cache_status[base_id]["episodes"] = {}
        cache_status[base_id]["episodes"][f"{season}:{episode}"] = novos_flags
    else:
        cache_status[base_id]["scrapers"] = novos_flags

    save_scraper_cache(cache_status)
    return JSONResponse(content={"streams": todos_streams})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
