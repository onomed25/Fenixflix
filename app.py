from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio
import httpx
import uvicorn
import inspect
import unicodedata
import re

import serve
import archive
import justwatch

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

def slugify(text):
    if not text: return ""
    text = str(text).lower()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    manifest_data = {
        "name": "FENIXFLIX",
        "description": "Filmes e Séries via Archive & Bysebuho",
        "types": ["movie", "series"]
    }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "manifest": manifest_data,
        "version": VERSION
    })

@app.get("/manifest.json")
async def manifest_endpoint():
    return JSONResponse(content={
        "id": "com.fenixflix",
        "version": VERSION,
        "name": "FENIXFLIX",
        "description": "Filmes e Séries via Archive & Bysebuho",
        "resources": ["stream", "catalog", "meta"],
        "types": ["movie", "series"],
        "catalogs": [
            {"type": "movie", "id": "popular", "name": "Populares (Fenix)"},
            {"type": "series", "id": "popular", "name": "Populares (Fenix)"}
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
        except: pass

    def create_task(func, *args):
        if inspect.iscoroutinefunction(func):
            return func(*args)
        return asyncio.to_thread(func, *args)

    # Inicia as buscas nas fontes (JSON local e Archive)
    tasks = [
        create_task(serve.search_serve, clean_id, type, season, episode),
        create_task(archive.search_serve, clean_id, type, season, episode)
    ]

    resultados = await asyncio.gather(*tasks, return_exceptions=True)
    final_streams = []

    async with httpx.AsyncClient() as client:
        for res in resultados:
            if isinstance(res, list):
                for stream_info in res:
                    url_original = stream_info.get("url", "")

                    # Se o URL não começar por http, é um ID que precisa de extração pelo Go
                    if url_original and not url_original.startswith("http"):
                        try:
                            # Chama o extrator/proxy em Go na porta 8080
                            response = await client.get(
                                f"http://localhost:8080/extract?id={url_original}",
                                timeout=40.0
                            )
                            dados_go = response.json()

                            if "m3u8" in dados_go:
                                # Substitui o ID pelo link final (ou link do proxy) gerado pelo Go
                                stream_info["url"] = dados_go["m3u8"]
                                final_streams.append(stream_info)
                            else:
                                print(f"Erro no extrator Go: {dados_go.get('erro')}")
                        except Exception as e:
                            print(f"Falha na comunicação com o servidor Go: {e}")
                    else:
                        # Links diretos (como os do Archive) são mantidos como estão
                        final_streams.append(stream_info)

    return JSONResponse(content={"streams": final_streams})

@app.get("/meta/{type}/{id}.json")
async def meta_endpoint(type: str, id: str):
    try:
        meta = await asyncio.to_thread(justwatch.fetch_meta, id, type)
        if meta:
            return JSONResponse(content={"meta": meta})
    except: pass
    return JSONResponse(content={"meta": {"id": id, "type": type, "name": "Conteúdo Desconhecido"}})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
