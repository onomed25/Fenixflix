import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import re
import threading
import time as _time

# ─────────────────────────────────────────────
#  Singleton do Playwright
# ─────────────────────────────────────────────
_playwright_instance = None
_browser_instance = None
_browser_lock = threading.Lock()

def get_browser():
    global _playwright_instance, _browser_instance
    with _browser_lock:
        if _browser_instance is None or not _browser_instance.is_connected():
            try:
                from playwright.sync_api import sync_playwright
                if _playwright_instance:
                    try:
                        _playwright_instance.stop()
                    except Exception:
                        pass
                _playwright_instance = sync_playwright().start()
                _browser_instance = _playwright_instance.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-dev-shm-usage",       # não usa /dev/shm (economiza RAM)
                        "--disable-gpu",                  # sem GPU
                        "--disable-extensions",           # sem extensões
                        "--disable-background-networking",
                        "--disable-sync",
                        "--disable-translate",
                        "--disable-default-apps",
                        "--mute-audio",
                        "--no-first-run",
                        "--disable-infobars",
                        "--disable-features=site-per-process",  # reduz processos isolados
                        "--js-flags=--max-old-space-size=128",  # limita heap JS a 128MB
                        "--memory-pressure-off",
                        "--single-process",              # tudo num processo só (menos RAM)
                    ]
                )
                print("[GO - Browser] Instância do Chromium iniciada com sucesso.")
            except Exception as e:
                print(f"[GO - Browser] Erro ao iniciar Chromium: {e}")
                return None
    return _browser_instance

def close_browser():
    global _playwright_instance, _browser_instance
    with _browser_lock:
        if _browser_instance:
            try:
                _browser_instance.close()
                print("[GO - Browser] Browser encerrado.")
            except Exception:
                pass
            _browser_instance = None
        if _playwright_instance:
            try:
                _playwright_instance.stop()
                print("[GO - Browser] Playwright encerrado.")
            except Exception:
                pass
            _playwright_instance = None


# ─────────────────────────────────────────────
#  Busca no GoFilmes
# ─────────────────────────────────────────────
def search_gofilmes(titles, content_type, season=None, episode=None):
    """
    Busca por um filme ou série no GoFilmes e retorna o link do player para o item específico.
    """
    base_url = "https://gofilmess.top"
    print(f"\n[DEBUG - GO] Iniciando busca no GoFilmes para: {titles} | Tipo: {content_type}")

    if content_type == 'series':
        path = 'series'
        selector = 'div.ep a[href]'
    else:
        path = ''
        selector = '.player_select_item a[href], div.link a[href]'

    for title in titles:
        search_slug = title.replace('.', '').replace(' ', '-').lower()

        if path:
            url = f"{base_url}/{path}/{quote(search_slug)}"
        else:
            url = f"{base_url}/{quote(search_slug)}"

        print(f"[DEBUG - GO] Testando URL: {url}")

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                player_options = []

                player_links = soup.select(selector)
                if not player_links:
                    continue

                if content_type == 'series':
                    if episode and 0 < episode <= len(player_links):
                        target_link = player_links[episode - 1]
                        player_options.append({
                            "name": f"GoFilmes - S{season}E{episode}",
                            "url": urljoin(base_url, target_link.get('href'))
                        })
                else:
                    for link in player_links:
                        player_options.append({
                            "name": f"GoFilmes - {link.get_text(strip=True)}",
                            "url": urljoin(base_url, link.get('href'))
                        })

                if player_options:
                    return player_options

        except requests.RequestException:
            pass
        except Exception:
            pass

    return []


# ─────────────────────────────────────────────
#  Resolve o stream final
# ─────────────────────────────────────────────
def resolve_stream(player_url):
    """
    Recebe a URL da página do player do GoFilmes e extrai o link do stream final.
    Tenta requests+BeautifulSoup primeiro; se necessário, usa Playwright com instância singleton.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    # ── ETAPA 1: Tentativa rápida com requests ──
    try:
        page_headers = headers.copy()
        page_headers.update({'Referer': 'https://gofilmess.top/'})

        r = requests.get(player_url, headers=page_headers, timeout=10, allow_redirects=True)
        soup = BeautifulSoup(r.text, 'html.parser')

        iframe = soup.find('iframe')
        if iframe and iframe.has_attr('src'):
            candidate = iframe['src']
            if not candidate.startswith('blob:'):
                return candidate, headers

        video_tag = soup.find('video')
        if video_tag:
            source_tag = video_tag.find('source')
            if source_tag and source_tag.has_attr('src'):
                candidate = source_tag['src']
                if not candidate.startswith('blob:'):
                    return candidate, headers

        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'playlist' in script.string:
                match = re.search(r'"file"\s*:\s*"([^"]+)"', script.string)
                if match:
                    return match.group(1), headers

        for script in scripts:
            if script.string and 'fetchVideoLink' in script.string:
                match = re.search(r'const apiUrl = `([^`]+)`;', script.string)
                if match:
                    api_url = match.group(1)
                    api_headers = headers.copy()
                    api_headers['Referer'] = player_url
                    api_response = requests.get(api_url, headers=api_headers, timeout=15)
                    api_response.raise_for_status()
                    return api_response.text.strip(), headers

    except Exception:
        pass

    # ── ETAPA 2: Playwright com instância singleton ──
    stream_url = ''
    try:
        browser = get_browser()
        if browser is None:
            print("[DEBUG - GO] Browser indisponível, pulando Playwright.")
            return stream_url, headers

        captured_url = None
        captured_lock = threading.Lock()

        def intercept(request):
            nonlocal captured_url
            with captured_lock:
                if captured_url:
                    return
            url = request.url
            if url.startswith('blob:'):
                return
            extensoes = ('.m3u8', '.mp4', '.mkv', '.ts')
            padrao_stream = 'm3u8' in url or 'master.txt' in url or '/stream/' in url or 'cache=' in url
            if any(url.split('?')[0].endswith(e) for e in extensoes) or padrao_stream:
                with captured_lock:
                    captured_url = url

        # Usa um contexto isolado por request (não compartilha cookies/estado)
        context = browser.new_context(
            user_agent=headers["User-Agent"],
            extra_http_headers={"Referer": "https://gofilmess.top/"}
        )
        page = context.new_page()
        page.on("request", intercept)

        try:
            page.goto(player_url, timeout=20000, wait_until="domcontentloaded")
        except Exception:
            pass

        # Aguarda até 10s para a URL aparecer
        for _ in range(20):
            with captured_lock:
                if captured_url:
                    break
            _time.sleep(0.5)

        # Fecha apenas o contexto, NÃO o browser
        try:
            context.close()
        except Exception:
            pass

        with captured_lock:
            if captured_url:
                stream_url = captured_url

    except Exception as e:
        print(f"[DEBUG - GO] Playwright falhou: {e}")

    return stream_url, headers


# ─────────────────────────────────────────────
#  Notificação de falta
# ─────────────────────────────────────────────
def notificar_falta_go(titles, content_type, season=None, episode=None):
    """Avisa o servidor que o GoFilmes não encontrou stream válido."""
    titulo = titles[0] if titles else "desconhecido"
    msg = f"[GoFilmes] Sem stream válido para {content_type}: '{titulo}'"
    if content_type == 'series' and season and episode:
        msg += f" (T{season}E{episode})"
    try:
        requests.get(
            "http://87.106.82.84:14923/aviso_falta",
            params={"msg": msg},
            timeout=3
        )
    except Exception:
        pass


# ─────────────────────────────────────────────
#  Função principal chamada pelo app.py
# ─────────────────────────────────────────────
def search_serve(titles, content_type, season=None, episode=None):
    """
    Função orquestradora que o app.py chama para buscar e já devolver o link final.
    """
    player_options = search_gofilmes(titles, content_type, season, episode)
    final_streams = []

    for option in player_options:
        stream_url, proxy_headers = resolve_stream(option["url"])
        if not stream_url:
            continue

        # Só aceita Mediafire ou master.txt — os outros dão erro de reprodução
        url_lower = stream_url.lower()
        if "mediafire" not in url_lower and "master.txt" not in url_lower:
            print(f"[DEBUG - GO] URL ignorada (não é Mediafire nem master.txt): {stream_url}")
            continue

        final_streams.append({
            "name": "FenixFlix",
            "title": "Legendado\nGo" if "leg" in option["name"].lower() else "Dublado\nGo",
            "url": stream_url,
            "behaviorHints": {"proxyHeaders": {"request": proxy_headers}}
        })

        print(f"[DEBUG - GO] Stream aceito: {stream_url}")

        # Limita a 2 streams para não estourar o tempo limite do Stremio
        if len(final_streams) >= 2:
            print("[DEBUG - GO] Limite de streams atingido.")
            break

    if not final_streams:
        notificar_falta_go(titles, content_type, season, episode)

    return final_streams
