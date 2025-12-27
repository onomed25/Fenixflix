import cloudscraper
import requests
import re
import json
import unicodedata
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# =========================
# UTILIDADES
# =========================

def limpar_slug(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = texto.lower().strip()
    texto = re.sub(r"[^\w\s-]", "", texto)
    return texto.replace(" ", "-")

def limpar_titulo_imdb(texto):
    if not texto:
        return None
    texto = re.sub(r'\s\(\d{4}\).*', '', texto)
    texto = re.sub(r'\s-\sIMDb.*', '', texto)
    return texto.strip()

# =========================
# IMDB
# =========================

def get_nomes_imdb(imdb_id):
    nomes = []
    url = f'https://www.imdb.com/pt/title/{imdb_id}/'

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8'
    }

    try:
        r = requests.get(url, headers=headers, timeout=8)
        src = r.text

        title = re.findall(r'<title>(.*?)</title>', src)
        if title:
            nome = limpar_titulo_imdb(title[0])
            if nome:
                nomes.append(nome)

        script = re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.DOTALL)
        if script:
            data = json.loads(script[0])
            for campo in ("name", "alternateName"):
                if campo in data and data[campo] not in nomes:
                    nomes.append(data[campo])

    except Exception:
        pass

    return nomes

# =========================
# STREAMBERRY
# =========================

def obter_url_final(tipo, slug, temporada=None, episodio=None):
    if tipo == "movie":
        url = f"https://streamberry.com.br/filmes/{slug}/"
    else:
        url = f"https://streamberry.com.br/episodios/{slug}-{temporada}x{episodio}/"

    scraper = cloudscraper.create_scraper()

    try:
        r = scraper.get(url, timeout=10)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        link = None

        for a in soup.find_all("a", href=True):
            if "/links/" in a["href"]:
                link = a["href"]
                break

        if not link:
            return None

        r2 = scraper.get(link, timeout=10)
        final_url = r2.url

        if "/download/" in final_url:
            final_url = final_url.replace("/download/", "/d/")

        return final_url

    except Exception:
        return None

# =========================
# PLAYWRIGHT (REUTILIZÁVEL)
# =========================

_playwright = None
_browser = None

async def get_browser():
    global _playwright, _browser

    if _browser is None:
        _playwright = await async_playwright().start()
        _browser = await _playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-extensions"
            ]
        )
    return _browser

# =========================
# BUSCAR M3U8 (PARA CEDO)
# =========================

async def buscar_m3u8(url):
    browser = await get_browser()
    context = await browser.new_context()
    page = await context.new_page()

    links = []

    async def interceptar(response):
        url_resp = response.url
        if ".m3u8" in url_resp:
            links.append(url_resp)
            await page.close()  # PARA IMEDIATAMENTE

    page.on("response", interceptar)

    try:
        await page.route(
            "**/*",
            lambda route: route.abort()
            if route.request.resource_type in ["image", "font", "media"]
            else route.continue_()
        )

        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(3000)

    except (PlaywrightTimeout, Exception):
        pass

    await context.close()
    return links

# =========================
# FUNÇÃO PRINCIPAL
# =========================

async def search_streamberry(imdb_id, tipo, nome_original, temporada=None, episodio=None):
    loop = asyncio.get_running_loop()
    nomes = await loop.run_in_executor(None, get_nomes_imdb, imdb_id)

    if nome_original and nome_original not in nomes:
        nomes.append(nome_original)

    for nome in nomes:
        slug = limpar_slug(nome)
        if len(slug) < 2:
            continue

        url_player = await loop.run_in_executor(
            None,
            obter_url_final,
            tipo,
            slug,
            temporada,
            episodio
        )

        if not url_player:
            continue

        links = await buscar_m3u8(url_player)

        if links:
            titulo = (
                f"Filme - {nome}"
                if tipo == "movie"
                else f"S{temporada}E{episodio} - {nome}"
            )

            return [{
                "name": "FenixFlix",
                "title": titulo,
                "url": links[0],
                "behaviorHints": {
                    "bingeGroup": "streamberry-vip",
                    "notWebReady": True
                }
            }]

    return []
