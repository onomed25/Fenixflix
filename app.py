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

load_dotenv()

VERSION = "1.0.5"
CACHE_DIR = "cache"
CATALOG_CACHE_TIME  = 6  * 60 * 60
POPULAR_CACHE_TIME  = 24 * 60 * 60
SCRAPER_STATUS_FILE = os.path.join(CACHE_DIR, "scrapers_status.json")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

_http_client: httpx.AsyncClient = None
_serve_client: httpx.AsyncClient = None
tmdb_semaphore = asyncio.Semaphore(7)


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


async def _resolve_popular_item(tmdb_id: str, content_type: str):
    tmdb_type = "movie" if content_type == "movie" else "tv"
    url_pt = f"https://api.themoviedb.org/3/{tmdb_type}/{tmdb_id}?api_key={TMDB_API_KEY}&language=pt-BR&append_to_response=external_ids"
    url_en = f"https://api.themoviedb.org/3/{tmdb_type}/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US&append_to_response=external_ids"

    try:
        async with tmdb_semaphore:
            res_pt, res_en = await asyncio.gather(
                _http_client.get(url_pt, timeout=5.0),
                _http_client.get(url_en, timeout=5.0),
                return_exceptions=True,
            )

        imdb_id = None
        titles  = []

        for res in (res_pt, res_en):
            if isinstance(res, Exception) or res.status_code != 200:
                continue
            data = res.json()
            if not imdb_id:
                ext = data.get("external_ids") or {}
                imdb_id = ext.get("imdb_id") or None
            name = data.get("title") or data.get("name")
            if name and name not in titles:
                titles.append(name)

        if imdb_id:
            return imdb_id, tmdb_id, titles
    except Exception as e:
        print(f"[SCRAPER-CACHE] Erro ao resolver tmdb_id {tmdb_id}: {e}")

    return None


async def sync_scraper_cache_from_items(items: list, content_type: str):
    scraper_cache = load_scraper_cache()
    known_tmdb_ids = {v.get("tmdb_id") for v in scraper_cache.values() if v.get("tmdb_id")}

    novos = []
    for item in items:
        item_id = item.get("id", "")
        if not item_id.startswith("tmdb:"):
            continue
        tmdb_id = item_id.split(":")[1]
        if tmdb_id not in known_tmdb_ids:
            novos.append(tmdb_id)

    if not novos:
        print(f"[SCRAPER-CACHE] Nada de novo em '{content_type}' — cache já actualizado.")
        return

    print(f"[SCRAPER-CACHE] {len(novos)} itens novos em '{content_type}' — resolvendo imdb_id+titles...")

    results = await asyncio.gather(
        *[_resolve_popular_item(tmdb_id, content_type) for tmdb_id in novos],
        return_exceptions=True,
    )

    count = 0
    for result in results:
        if isinstance(result, Exception) or result is None:
            continue
        imdb_id, tmdb_id_r, titles = result
        if imdb_id and imdb_id not in scraper_cache:
            scraper_cache[imdb_id] = {
                "tmdb_id":  tmdb_id_r,
                "titles":   titles,
                "type":     content_type,
                "scrapers": {},
            }
            count += 1

    if count:
        save_scraper_cache(scraper_cache)
        print(f"[SCRAPER-CACHE] {count} itens novos adicionados ao cache de scrapers.")


async def prepopulate_scraper_cache_from_popular():
    for content_type in ("movie", "series"):
        cache_file = os.path.join(CACHE_DIR, f"tmdb_popular_{content_type}.json")
        if not os.path.exists(cache_file):
            continue
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                items = json.load(f)
            await sync_scraper_cache_from_items(items, content_type)
        except Exception as e:
            print(f"[SCRAPER-CACHE] Erro ao ler cache popular '{content_type}': {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _http_client, _serve_client

    # Cliente Global (TMDB, Scrapers diversos)
    _http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(15.0, connect=5.0),
        follow_redirects=True,
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=30, keepalive_expiry=30),
        verify=False,
    )

    # Cliente Dedicado (Isolamento para o servidor principal de streaming)
    _serve_client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0, connect=3.0),
        follow_redirects=True,
        limits=httpx.Limits(max_connections=50, max_keepalive_connections=20, keepalive_expiry=60),
        verify=False,
    )

    await prepopulate_scraper_cache_from_popular()

    yield

    await _http_client.aclose()
    await _serve_client.aclose()



app = FastAPI(lifespan=lifespan)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

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


async def obter_dados_base_tmdb(imdb_id: str, content_type: str, client: httpx.AsyncClient = None):
    """Devolve (tmdb_id, real_imdb_id, titulos). real_imdb_id pode ser None se nao encontrado."""
    tmdb_id_final = None
    real_imdb_id  = None
    titulos = []
    tmdb_type = "movie" if content_type == "movie" else "tv"

    async def _do_requests(c):
        nonlocal tmdb_id_final, real_imdb_id
        if imdb_id.startswith("tmdb:"):
            tmdb_id_final = imdb_id.split(":")[1]
            url_pt = f"https://api.themoviedb.org/3/{tmdb_type}/{tmdb_id_final}?api_key={TMDB_API_KEY}&language=pt-BR&append_to_response=external_ids"
            url_en = f"https://api.themoviedb.org/3/{tmdb_type}/{tmdb_id_final}?api_key={TMDB_API_KEY}&language=en-US&append_to_response=external_ids"
            reqs = await asyncio.gather(c.get(url_pt), c.get(url_en), return_exceptions=True)
            for r in reqs:
                if not isinstance(r, Exception) and r.status_code == 200:
                    data = r.json()
                    if not real_imdb_id:
                        real_imdb_id = (data.get("external_ids") or {}).get("imdb_id") or None
                    name = data.get("title") or data.get("name")
                    if name and name not in titulos:
                        titulos.append(name)
        else:
            real_imdb_id = imdb_id
            url_pt = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=pt-BR"
            url_en = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=en-US"
            reqs = await asyncio.gather(c.get(url_pt), c.get(url_en), return_exceptions=True)
            for r in reqs:
                if not isinstance(r, Exception) and r.status_code == 200:
                    data = r.json()
                    results = data.get(f"{tmdb_type}_results", [])
                    if results:
                        if not tmdb_id_final:
                            tmdb_id_final = str(results[0].get("id"))
                        name = results[0].get("title") or results[0].get("name")
                        if name and name not in titulos:
                            titulos.append(name)

    try:
        await _do_requests(client or _http_client)
    except Exception as e:
        print(f"[TMDB] Cliente global falhou ({e}), a criar cliente temporario...")
        try:
            async with httpx.AsyncClient(timeout=10.0, verify=False) as tmp:
                await _do_requests(tmp)
        except Exception as e2:
            print(f"[TMDB] Cliente temporario tambem falhou: {e2}")

    return tmdb_id_final, real_imdb_id, titulos


async def fetch_tmdb_meta_ptbr(item_id: str, content_type: str):
    async with tmdb_semaphore:
        tmdb_id_final = None
        true_type = content_type
        tmdb_type = "movie" if content_type == "movie" else "tv"

        if item_id.startswith("tmdb:"):
            tmdb_id_final = item_id.split(":")[1]
        else:
            url_find = f"https://api.themoviedb.org/3/find/{item_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=pt-BR"
            try:
                resp = await _http_client.get(url_find, timeout=5.0)
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get(f"{tmdb_type}_results", [])
                    if results:
                        tmdb_id_final = str(results[0].get("id"))
                    else:
                        other_type = "tv" if tmdb_type == "movie" else "movie"
                        other_results = data.get(f"{other_type}_results", [])
                        if other_results:
                            tmdb_id_final = str(other_results[0].get("id"))
                            tmdb_type = other_type
                            true_type = "series" if other_type == "tv" else "movie"
            except:
                pass

        if tmdb_id_final:
            url_details = f"https://api.themoviedb.org/3/{tmdb_type}/{tmdb_id_final}?api_key={TMDB_API_KEY}&language=pt-BR"
            try:
                resp = await _http_client.get(url_details, timeout=5.0)
                if resp.status_code == 200:
                    data = resp.json()
                    title = data.get("title") or data.get("name") or f"Conteúdo {item_id}"
                    poster_path = data.get("poster_path")
                    poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                    description = data.get("overview") or ""

                    return {
                        "id": item_id,
                        "type": true_type,
                        "name": title,
                        "poster": poster,
                        "description": description,
                        "_tmdb_id": tmdb_id_final,
                    }
            except:
                pass

        return {"id": item_id, "type": true_type, "name": f"Conteúdo {item_id}"}


async def build_recent_catalog():

    url = "http://87.106.82.84:14923/api/all"
    try:
        resp = await _serve_client.get(url, timeout=30.0) # Atualizado para usar o cliente dedicado
        all_data = resp.json() if resp.status_code == 200 else []
    except:
        return {"movie": [], "series": []}

    items = all_data if isinstance(all_data, list) else list(all_data.values())
    movie_ids, series_ids = [], []
    for data in items:
        if len(movie_ids) >= 27 and len(series_ids) >= 27:
            break
        imdb_id = data.get("id")
        if not imdb_id:
            continue
        content_type = data.get("type", "movie")
        streams = data.get("streams", {})

        if content_type == "series" and isinstance(streams, dict) and len(series_ids) < 27:
            series_ids.append(imdb_id)
        elif (content_type == "movie" or isinstance(streams, list)) and len(movie_ids) < 27:
            movie_ids.append(imdb_id)

    movie_tasks  = [fetch_tmdb_meta_ptbr(i, "movie")  for i in movie_ids]
    series_tasks = [fetch_tmdb_meta_ptbr(i, "series") for i in series_ids]
    movies_raw  = await asyncio.gather(*movie_tasks,  return_exceptions=True)
    series_raw  = await asyncio.gather(*series_tasks, return_exceptions=True)

    def clean(item):
        if isinstance(item, dict):
            return {k: v for k, v in item.items() if k != "_tmdb_id"}
        return item

    movies = [clean(m) for m in movies_raw if isinstance(m, dict) and m.get("type") == "movie"][:25]
    series = [clean(s) for s in series_raw if isinstance(s, dict) and s.get("type") == "series"][:25]
    return {"movie": movies, "series": series}


async def get_recent_catalog_cached(content_type):
    cache_file = os.path.join(CACHE_DIR, "server_recent_catalog.json")

    if os.path.exists(cache_file) and (time.time() - os.path.getmtime(cache_file)) < CATALOG_CACHE_TIME:
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                dados_salvos = json.load(f)
                itens_salvos = dados_salvos.get(content_type, [])
                if itens_salvos:
                    return itens_salvos
        except:
            pass

    catalogs = await build_recent_catalog()
    if catalogs.get("movie") or catalogs.get("series"):
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(catalogs, f, ensure_ascii=False, indent=2)
        except:
            pass
    return catalogs.get(content_type, [])



async def get_popular_catalog_cached(content_type):
    cache_file = os.path.join(CACHE_DIR, f"tmdb_popular_{content_type}.json")

    if os.path.exists(cache_file) and (time.time() - os.path.getmtime(cache_file)) < POPULAR_CACHE_TIME:
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                dados_salvos = json.load(f)
                if dados_salvos:
                    return dados_salvos
        except:
            pass

    tmdb_type = "movie" if content_type == "movie" else "tv"
    url = f"https://api.themoviedb.org/3/trending/{tmdb_type}/week?api_key={TMDB_API_KEY}&language=pt-BR&region=BR"

    try:
        resp = await _http_client.get(url, timeout=10.0)
        data = resp.json()
        metas = []
        for item in data.get("results", []):
            title = item.get("title") or item.get("name")
            poster_path = item.get("poster_path")
            if poster_path:
                metas.append({
                    "id": f"tmdb:{item.get('id')}",
                    "type": content_type,
                    "name": title,
                    "poster": f"https://image.tmdb.org/t/p/w500{poster_path}",
                    "description": item.get("overview", "")
                })

        if metas:
            try:
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(metas, f, ensure_ascii=False, indent=2)
            except:
                pass

            asyncio.create_task(sync_scraper_cache_from_items(metas, content_type))

        return metas
    except:
        return []



@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    manifest_data = {"name": "FENIXFLIX", "description": "Addon de Filmes e Séries", "types": ["movie", "series"]}
    return templates.TemplateResponse(request=request, name="index.html", context={"manifest": manifest_data, "version": VERSION})

@app.get("/manifest.json")
async def manifest_endpoint():
    return JSONResponse(content={
        "id": "com.fenixflix", "version": VERSION, "name": "FENIXFLIX",
        "description": "Addon de Filmes e Séries",
        "logo": "https://i.imgur.com/9SKgxfU.png",
        "background": "https://dl.strem.io/addon-background.jpg",
        "resources": ["stream", "catalog"],
        "types": ["movie", "series"],
        "catalogs": [
            {"type": "movie",  "id": "popular",           "name": "Populares"},
            {"type": "movie",  "id": "recentes_servidor", "name": "Recém Adicionado (Fenix)"},
            {"type": "series", "id": "popular",           "name": "Populares"},
            {"type": "series", "id": "recentes_servidor", "name": "Recém Adicionado (Fenix)"}
        ],
        "idPrefixes": ["tt", "tmdb"]
    })

@app.get("/catalog/{type}/{id}.json")
@app.get("/catalog/{type}/{id}/{extra}.json")
async def catalog_endpoint(type: str, id: str, extra: str = None, skip: int = 0):
    if (extra and "skip=" in extra) or skip > 0:
        return JSONResponse(content={"metas": []})

    if id == "recentes_servidor":
        metas = await get_recent_catalog_cached(type)
        return JSONResponse(content={"metas": metas})
    elif id == "popular":
        metas = await get_popular_catalog_cached(type)
        return JSONResponse(content={"metas": metas})

    return JSONResponse(content={"metas": []})


@app.get("/stream/{type}/{id}.json")
@limiter.limit("20/minute")
async def stream(type: str, id: str, request: Request):
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

    # 🔥 INJETANDO O CLIENTE DEDICADO AQUI 🔥
    tarefa_serve = asyncio.create_task(
        serve.search_serve(clean_id, type, season, episode, client=_serve_client)
    )

    cache_status = load_scraper_cache()

    entry = cache_status.get(clean_id)
    base_id = clean_id

    if entry is None and clean_id.startswith("tmdb:"):
        tmdb_id_raw = clean_id.split(":")[1]
        for key, val in cache_status.items():
            if val.get("tmdb_id") == tmdb_id_raw:
                entry = val
                base_id = key
                print(f"[APP] Cache hit por tmdb_id: '{clean_id}' -> '{base_id}'")
                break

    if entry and entry.get("tmdb_id"):
        tmdb_id = entry.get("tmdb_id")
        titles  = entry.get("titles", [])
        scraper_flags = (
            entry.get("episodes", {}).get(f"{season}:{episode}", {})
            if type == "series"
            else entry.get("scrapers", {})
        )
        print(f"[APP] Cache hit para '{base_id}' — tmdb_id={tmdb_id}")
    else:
        tmdb_id, real_imdb_id, titles = await obter_dados_base_tmdb(clean_id, type, client=_http_client)
        scraper_flags = {}
        if real_imdb_id and real_imdb_id.startswith("tt"):
            base_id = real_imdb_id
        else:
            base_id = clean_id

    outras_tarefas = {}
    if tmdb_id:
        if scraper_flags.get("doramogo")    != "N": outras_tarefas["doramogo"]    = asyncio.create_task(doramogo.search_serve(tmdb_id, titles, type, season, episode, client=_http_client))
        if scraper_flags.get("on")          != "N": outras_tarefas["on"]          = asyncio.create_task(on.search_serve(tmdb_id, type, season, episode, client=_http_client))
        if scraper_flags.get("mywallpaper") != "N": outras_tarefas["mywallpaper"] = asyncio.create_task(mywallpaper.search_serve(tmdb_id, titles, type, season, episode, client=_http_client))
        if scraper_flags.get("streamflix")  != "N": outras_tarefas["streamflix"]  = asyncio.create_task(streamflix.search_serve(titles, type, season, episode, client=_http_client))
    else:
        print(f"[APP] tmdb_id nao resolvido para '{clean_id}' — scrapers ignorados.")

    tarefas_para_aguardar = [tarefa_serve] + list(outras_tarefas.values())
    names   = ["serve"] + list(outras_tarefas.keys())
    results = await asyncio.gather(*tarefas_para_aguardar, return_exceptions=True)

    todos_streams = []
    novos_flags   = scraper_flags.copy()

    for i, res in enumerate(results):
        nome = names[i]
        if isinstance(res, Exception) or not res:
            if nome != "serve":
                novos_flags[nome] = "N"
            continue
        if nome != "serve":
            novos_flags[nome] = "S"
        for s_info in res:
            if s_info.get("url"):
                if "behaviorHints" not in s_info:
                    s_info["behaviorHints"] = {"notWebReady": False, "bingeGroup": "fenixflix"}
                todos_streams.append(s_info)

    if base_id not in cache_status:
        cache_status[base_id] = {"tmdb_id": tmdb_id, "titles": titles, "type": type}
    if tmdb_id and type == "series":
        if "episodes" not in cache_status[base_id]:
            cache_status[base_id]["episodes"] = {}
        cache_status[base_id]["episodes"][f"{season}:{episode}"] = novos_flags
    elif tmdb_id:
        cache_status[base_id]["scrapers"] = novos_flags

    save_scraper_cache(cache_status)
    return JSONResponse(content={"streams": todos_streams})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
