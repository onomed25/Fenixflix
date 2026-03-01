from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse, RedirectResponse
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
from urllib.parse import quote, urljoin

from playwright.async_api import async_playwright

import serve
import archive
import justwatch

VERSION = "1.0.4" # Versão atualizada

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

# Função extraindo diretamente com o Playwright pelo Python
async def extrair_m3u8_streamberry(url_video, referer_site="https://streamberry.com.br/"):
    print(f"[*] Iniciando extração Playwright no Python para: {url_video}")
    link_m3u8 = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        await page.set_extra_http_headers({
            "Referer": referer_site,
            "Origin": referer_site.rstrip('/'),
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        })

        async def capturar_rede(request):
            nonlocal link_m3u8
            url = request.url
            if ".m3u8" in url and ("master" in url or "index" in url) and not link_m3u8:
                print(f"\n[+] Link interceptado pelo Python: {url}\n")
                link_m3u8 = url

        page.on("request", capturar_rede)

        try:
            await page.goto(url_video, wait_until="load", timeout=30000)
            for _ in range(15):
                if link_m3u8:
                    break
                await asyncio.sleep(1)
        except Exception as e:
            print(f"[-] Erro na extração do Playwright: {e}")
        finally:
            await browser.close()

    return link_m3u8

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
                    # ENVIA O BOTÃO IMEDIATAMENTE PARA O STREMIO NÃO DAR TIMEOUT
                    # Ele vai apontar para a nossa nova rota /play
                    base_url = str(request.base_url)
                    stream_info["url"] = f"{base_url}play?id={url}"
                    
                    if "behaviorHints" in stream_info:
                        del stream_info["behaviorHints"]
                        
                    final_streams.append(stream_info)
                else:
                    final_streams.append(stream_info)

    return JSONResponse(content={"streams": final_streams})

# --- NOVA ROTA QUE FAZ A EXTRAÇÃO LENTA SÓ QUANDO O USUÁRIO DÁ PLAY ---
@app.get("/play")
async def play_video(id: str, request: Request):
    url_do_embed = f"https://byseraguci.com/e/{id}"
    
    # Roda o Playwright enquanto o player do Stremio está a pensar...
    m3u8_extraido = await extrair_m3u8_streamberry(url_do_embed)
    
    if m3u8_extraido:
        # Quando encontra, redireciona para o nosso proxy para tocar o vídeo
        base_url = str(request.base_url)
        link_do_proxy = f"{base_url}proxy?url={quote(m3u8_extraido)}"
        return RedirectResponse(url=link_do_proxy)
    else:
        return HTMLResponse("Erro: Não foi possível extrair o vídeo.")

@app.get("/proxy")
async def proxy_m3u8(url: str, request: Request):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://streamberry.com.br/",
        "Origin": "https://streamberry.com.br"
    }
    
    client = httpx.AsyncClient(follow_redirects=True, timeout=30.0)
    req = client.build_request("GET", url, headers=headers)
    
    try:
        r = await client.send(req, stream=True)
    except Exception as e:
        await client.aclose()
        print(f"[-] Erro no proxy: {e}")
        return JSONResponse(status_code=502, content={"erro": f"Falha de conexão com a CDN: {str(e)}"})

    content_type = r.headers.get("Content-Type", "")
    
    if "mpegurl" in content_type.lower() or ".m3u8" in url.lower():
        content = await r.aread()
        await r.aclose()
        await client.aclose() 
        
        linhas = content.decode('utf-8').split('\n')
        for i, linha in enumerate(linhas):
            linha = linha.strip()
            if linha and not linha.startswith("#"):
                chunk_url = urljoin(str(r.url), linha)
                linhas[i] = f"{request.base_url}proxy?url={quote(chunk_url)}"
                
        return StreamingResponse(
            iter([("\n".join(linhas)).encode('utf-8')]),
            media_type=content_type or "application/vnd.apple.mpegurl"
        )
    else:
        async def stream_generator():
            try:
                async for chunk in r.aiter_bytes():
                    yield chunk
            finally:
                await r.aclose()
                await client.aclose()
            
        return StreamingResponse(
            stream_generator(),
            media_type=content_type or "video/mp2t"
        )

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
