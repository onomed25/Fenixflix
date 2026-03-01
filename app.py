from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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

VERSION = "1.0.3"

app = FastAPI()

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

# Nova função: apenas pede para o Go!
async def extrair_m3u8_streamberry(url_video):
    video_id = url_video.split('/')[-1]
    try:
        async with httpx.AsyncClient(timeout=35.0) as client:
            resposta = await client.get(f"http://127.0.0.1:8080/extract?id={video_id}")
            if resposta.status_code == 200:
                dados = resposta.json()
                if dados.get("m3u8"):
                    return dados["m3u8"]
    except Exception:
        pass
    return None

@app.get("/")
async def root():
    return {"status": "online", "addon": "FENIXFLIX", "version": VERSION}

@app.get("/manifest.json")
async def manifest_endpoint():
    return JSONResponse(content={
        "id": "com.fenixflix",
        "version": VERSION,
        "name": "FENIXFLIX",
        "description": "Filmes e Séries via Archive & Bysebuho (Go Powered)",
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

    tasks = [
        create_task(serve.search_serve, clean_id, type, season, episode),
        create_task(archive.search_serve, clean_id, type, season, episode)
    ]

    resultados = await asyncio.gather(*tasks, return_exceptions=True)
    final_streams = []

    for res in resultados:
        if isinstance(res, list):
            for stream_info in res:
                url = stream_info.get("url", "")

                if url and not url.startswith("http"):
                    url_do_embed = f"https://byseraguci.com/e/{url}"
                    m3u8_extraido = await extrair_m3u8_streamberry(url_do_embed)

                    if m3u8_extraido:
                        stream_info["url"] = m3u8_extraido
                        final_streams.append(stream_info)
                else:
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
