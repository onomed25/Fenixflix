from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from jinja2 import Environment, FileSystemLoader
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import logging
from netcine import catalog_search, search_link
import requests
import canais
import os
from urllib.parse import quote_plus, quote

templates = Environment(loader=FileSystemLoader("templates"))
limiter = Limiter(key_func=get_remote_address)
rate_limit = '3/second'

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

def get_external_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        return response.json().get("ip")
    except requests.RequestException:
        return None

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(content={"error": "Too many requests"}, status_code=429)

def add_cors(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.get("/", response_class=HTMLResponse)
@limiter.limit(rate_limit)
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
async def proxy_logo(url: str):
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
@limiter.limit(rate_limit)
async def manifest(request: Request):
    return add_cors(JSONResponse(content=MANIFEST))

@app.get("/catalog/tv/skyflix/genre={id}.json")
@limiter.limit(rate_limit)
async def genres(id: str, request: Request):
    server = f"https://{request.url.hostname}/logo?url="
    canais_ = [canal for canal in canais.canais_list(server) if id in canal["genres"]]
    return add_cors(JSONResponse(content={"metas": canais_}))

@app.get("/catalog/{type}/{id}.json")
@limiter.limit(rate_limit)
async def catalog_route(type: str, id: str, request: Request):
    server = f"https://{request.url.hostname}/logo?url="
    canais_ = [canal for canal in canais.canais_list(server)] if type == "tv" else []
    return add_cors(JSONResponse(content={"metas": canais_}))

@app.get("/catalog/{type}/skyflix/search={query}.json")
@limiter.limit(rate_limit)
async def search(type: str, query: str, request: Request):
    catalog = catalog_search(query)
    results = [item for item in catalog if item.get("type") == type] if catalog else []
    return add_cors(JSONResponse(content={"metas": results}))

@app.get("/meta/{type}/{id}.json")
@limiter.limit(rate_limit)
async def meta(type: str, id: str, request: Request):
    server = f"https://{request.url.hostname}/logo?url="
    meta_data = next((canal for canal in canais.canais_list(server) if canal["id"] == id), {}) if type == "tv" else {}
    if meta_data:
        meta_data.pop("streams", None)
    return add_cors(JSONResponse(content={"meta": meta_data}))

@app.get("/stream/{type}/{id}.json")
@limiter.limit(rate_limit)
async def stream(type: str, id: str, request: Request):
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
                            try:
                                streams_list[0]["behaviorHints"]["proxyHeaders"]["request"]["Cookie"] = "modalVisited=true"
                            except:
                                pass
                    except:
                        pass               
                scrape_ = streams_list
                break
    elif type in ["movie", "series"]:
        # try:
        #     ip_host = get_external_ip()
        # except:
        #     ip_host = ''
        try:
            stream_, headers = search_link(id)
            # if ip_host:
            #     scrape_ = [{
            #         "url": stream_,
            #         "name": "SKYFLIX",
            #         "description": "NTC Server",
            #         "behaviorHints": {
            #             "notWebReady": True,
            #             "proxyHeaders": {
            #                 "request": {
            #                     "User-Agent": headers["User-Agent"],
            #                     "Referer": headers["Referer"],
            #                     "Cookie": headers["Cookie"],
            #                     "X-Forwarded-For": ip_host
            #                 }
            #             }
            #         }
            #     }]
            # else:               
            scrape_ = [{
                "url": stream_,
                "name": "SKYFLIX",
                "description": "NTC Server",
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
@limiter.limit(rate_limit)
async def options_handler(path: str, request: Request):
    return add_cors(Response(status_code=204))
