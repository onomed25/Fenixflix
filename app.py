from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Environment, FileSystemLoader
import logging
from netcine import catalog_search, search_link
import requests
import canais
import os
from urllib.parse import quote_plus, quote

templates = Environment(loader=FileSystemLoader("templates"))
app = FastAPI()


# Configure o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
VERSION = "1.0.0"
logger.info(f"Versão da aplicação: {VERSION}")

MANIFEST = {
    "id": "com.skyflix",
    "version": "1.0.0",
    "name": "SKYFLIX",
    "description": "Tenha o melhor dos filmes e séries com Skyflix",
    "logo": "https://i.imgur.com/qVgkbYn.png",
    "resources": ["catalog", "meta", "stream"],
    "types": ["tv", "movie", "series"],
    "catalogs": [
        {
            "type": "tv",
            "id": "skyflix",
            "name": "SKYFLIX",
            "extra": [
                {
                    "name": "genre",
                    "options": [
                        "Canais Abertos",
                        "Variedades",
                        "Filmes e Series",
                        "Documentarios",
                        "Esportes",
                        "Infantil",
                        "Noticias",
                        "PLUTO TV",
                        "CANAL 24H"
                    ],
                    "isRequired": False
                }
            ]
        },
        {
            "type": "movie",
            "id": "skyflix",
            "name": "SKYFLIX",
            "extraSupported": ["search"]
        },
        {
            "type": "series",
            "id": "skyflix",
            "name": "SKYFLIX",
            "extraSupported": ["search"]
        }
    ],
    "idPrefixes": ["skyflix", "tt"]
}

def add_cors(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    template = templates.get_template("index.html")
    response = HTMLResponse(template.render(
        name=MANIFEST['name'],
        types=MANIFEST['types'],
        logo=MANIFEST['logo'],
        description=MANIFEST['description'],
        version=MANIFEST['version']
    ))
    return add_cors(response)

@app.get("/logo")
def proxy_logo(url: str):
    if not url:
        return add_cors(JSONResponse(content={"error": "Nenhuma URL fornecida"}, status_code=400))
    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            return add_cors(JSONResponse(content={"error": f"Erro ao buscar a imagem: {response.status_code}"}, status_code=400))
        content_type = response.headers.get("Content-Type", "image/jpeg")
        return add_cors(Response(content=response.content, media_type=content_type))
    except requests.exceptions.RequestException as e:
        return add_cors(JSONResponse(content={"error": f"Erro ao buscar a imagem: {str(e)}"}, status_code=500))

@app.get("/manifest.json")
def manifest():
    return add_cors(JSONResponse(content=MANIFEST))

@app.get("/catalog/tv/skyflix/genre={id}.json")
def genres(id: str, request: Request):
    server = f"https://{request.url.hostname}/logo?url="
    canais_ = [canal for canal in canais.canais_list(server) if id in canal["genres"]]
    return add_cors(JSONResponse(content={"metas": canais_}))

@app.get("/catalog/{type}/{id}.json")
def catalog_route(type: str, id: str, request: Request):
    server = f"https://{request.url.hostname}/logo?url="
    canais_ = [canal for canal in canais.canais_list(server)] if type == "tv" else []
    return add_cors(JSONResponse(content={"metas": canais_}))

@app.get("/catalog/{type}/skyflix/search={query}.json")
def search(type: str, query: str):
    catalog = catalog_search(query)
    results = [item for item in catalog if item.get("type") == type] if catalog else []
    return add_cors(JSONResponse(content={"metas": results}))

@app.get("/meta/{type}/{id}.json")
def meta(type: str, id: str, request: Request):
    server = f"https://{request.url.hostname}/logo?url="
    meta_data = next((canal for canal in canais.canais_list(server) if canal["id"] == id), {}) if type == "tv" else {}
    if meta_data:
        meta_data.pop("streams", None)
    return add_cors(JSONResponse(content={"meta": meta_data}))

@app.get("/stream/{type}/{id}.json")
def stream(type: str, id: str, request: Request):
    server = f"https://{request.url.hostname}/logo?url="
    if type == "tv":
        scrape_ = []
        list_canais = canais.canais_list(server)
        for canal in list_canais:
            if canal['id'] == id:
                rc = canal.get('rc', {})
                streams_list = canal['streams']
                if rc:
                    try:
                        token = rc.get('token', '')
                        channel = rc.get('channel', '')
                        if token and channel:
                            stream_rc = canais.get_rc(channel,token)
                            streams_list[0]['url'] = stream_rc
                    except:
                        pass               
                scrape_ = streams_list
                break
    elif type in ["movie", "series"]:
        try:
            stream_, headers = search_link(id)
            scrape_ = [{
                "url": stream_,
                "name": "SKYFLIX",
                "description": "Netcine",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": headers["User-Agent"],
                            "Referer": headers["Referer"],
                            "Cookie": headers["Cookie"]
                        }
                    }
                }
            }]
        except:
            scrape_ = []
    else:
        scrape_ = []
    return add_cors(JSONResponse(content={"streams": scrape_}))

@app.options("/{path:path}")
def options_handler(path: str):
    return add_cors(Response(status_code=204))
