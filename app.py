from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from jinja2 import Environment, FileSystemLoader 
import asyncio
import serve   # Mantido (antigo)
import archive # Mantido (novo com Session)
# import stb removido

VERSION = "1.0.2" # Incrementei a versão
MANIFEST = {
    "id": "com.fenixflix", 
    "version": VERSION, 
    "name": "FENIXFLIX",
    "description": "Sua fonte para filmes e séries.",
    "logo": "https://i.imgur.com/9SKgxfU.png", 
    "resources": ["stream"],
    "types": ["movie", "series"], 
    "catalogs": [], 
    "idPrefixes": ["fenixflix", "tt"]
}

templates = Environment(loader=FileSystemLoader("templates"))
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

def add_cors(response: Response) -> Response:
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.get("/")
async def root(request: Request):
    template = templates.get_template("index.html")
    return HTMLResponse(content=template.render(manifest=MANIFEST, version=VERSION))

@app.get("/manifest.json")
async def manifest_endpoint():
    return add_cors(JSONResponse(content=MANIFEST))

# Removi a função get_cinemeta_name e client_session pois só eram usadas pelo STB

async def search_serve_async(imdb_id, content_type, season, episode):
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, serve.search_serve, imdb_id, content_type, season, episode)
    except:
        return []

async def search_archive_async(imdb_id, content_type, season, episode):
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, archive.search_serve, imdb_id, content_type, season, episode)
    except:
        return []

@app.get("/stream/{type}/{id}.json")
@limiter.limit("5/minute")
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
        except:
            return add_cors(JSONResponse(content={"streams": []}))

    final_streams = []

    # 1. Busca no Serve (Antigo)
    serve_streams = await search_serve_async(imdb_id, type, season, episode)
    if serve_streams:
        final_streams.extend(serve_streams)

    # 2. Busca no Archive (Novo)
    archive_streams = await search_archive_async(imdb_id, type, season, episode)
    if archive_streams:
        final_streams.extend(archive_streams)
    
    # 3. STB removido
    
    return add_cors(JSONResponse(content={"streams": final_streams}))
