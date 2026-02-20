from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio
import uvicorn
import serve   
import archive 
import justwatch

VERSION = "1.0.1"

FIXED_CATALOGS = [
    {"type": "movie", "id": "jw_popular", "name": "Populares (Fenix)"},
    {"type": "series", "id": "jw_popular", "name": "Populares (Fenix)"}
]

templates = Jinja2Templates(directory="templates")
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

def add_cors(response: Response) -> Response:
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

def get_manifest(config_str: str = None):
    return {
        "id": "com.fenixflix", 
        "version": VERSION, 
        "name": "FENIXFLIX",
        "description": "Filmes e Séries Populares",
        "logo": "https://i.imgur.com/9SKgxfU.png", 
      
        "resources": ["stream", "catalog", "meta"], 
        "types": ["movie", "series"], 
        "catalogs": FIXED_CATALOGS, 
        "idPrefixes": ["tt", "tmdb"] 
    }

@app.get("/")
async def root(request: Request):
    manifest_data = get_manifest(None)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "manifest": manifest_data,
        "version": VERSION
    })

@app.get("/manifest.json")
async def manifest_endpoint():
    return add_cors(JSONResponse(content=get_manifest(None)))

@app.get("/providers={config_str}/manifest.json")
async def manifest_config_endpoint(config_str: str):
    return add_cors(JSONResponse(content=get_manifest(config_str)))

@app.get("/catalog/{type}/{id}.json")
@app.get("/providers={config_str}/catalog/{type}/{id}.json")
async def catalog_endpoint(type: str, id: str, config_str: str = None):
    if id == "jw_popular":
        metas = await asyncio.to_thread(justwatch.fetch_catalog, "popular", type)
        return add_cors(JSONResponse(content={"metas": metas}))
    return add_cors(JSONResponse(content={"metas": []}))


@app.get("/meta/{type}/{id}.json")
@app.get("/providers={config_str}/meta/{type}/{id}.json")
async def meta_endpoint(type: str, id: str, config_str: str = None):

    meta = await asyncio.to_thread(justwatch.fetch_meta, id, type)
    
    if meta:
        return add_cors(JSONResponse(content={"meta": meta}))
  
    return add_cors(JSONResponse(content={"meta": None})) 

@app.get("/stream/{type}/{id}.json")
@app.get("/providers={config_str}/stream/{type}/{id}.json")
@limiter.limit("10/minute")
async def stream(type: str, id: str, request: Request, config_str: str = None):
    clean_id = id.split(':')[0] 
    season, episode = None, None

    if type == 'series':
        try:
            parts = id.split(':')
            season = int(parts[1])
            episode = int(parts[2])
        except: pass

    final_streams = []
    
    task_serve = asyncio.to_thread(serve.search_serve, clean_id, type, season, episode)
    task_archive = asyncio.to_thread(archive.search_serve, clean_id, type, season, episode)
    
    resultados = await asyncio.gather(task_serve, task_archive, return_exceptions=True)
    
    serve_streams = resultados[0]
    archive_streams = resultados[1]

    if isinstance(serve_streams, list) and serve_streams:
        final_streams.extend(serve_streams)
        
    if isinstance(archive_streams, list) and archive_streams:
        final_streams.extend(archive_streams)

    
    return add_cors(JSONResponse(content={"streams": final_streams}))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)