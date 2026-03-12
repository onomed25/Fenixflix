import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import re

def search_gofilmes(titles, content_type, season=None, episode=None):
    """
    Busca por um filme ou série no gofilmes e retorna o link do player para o item específico.
    """
    base_url = "https://gofilmess.top"
    print(f"\n[DEBUG - GO] Iniciando busca no GoFilmes para: {titles} | Tipo: {content_type}")

    if content_type == 'series':
        path = 'series'
        selector = 'div.ep a[href]'
    else:
        path = ''
        selector = '.player_select_item a[href], div.link a[href]'  # fallback para ambos

    for title in titles:
        # CORRIGIDO: usando a mesma lógica do gofilmes.py antigo que funcionava
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

def resolve_stream(player_url):
    """
    Recebe a URL da página do player do GoFilmes e extrai o link do stream final.
    Tenta requests+BeautifulSoup primeiro; se resultado for blob://, usa Playwright.
    """
    stream_url = ''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    # --- ETAPA 1: Tentativa rápida com requests ---
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

    # --- ETAPA 2: Playwright para capturar o .m3u8 real por trás do blob ---
    try:
        from playwright.sync_api import sync_playwright

        captured_url = None

        def intercept(request):
            nonlocal captured_url
            url = request.url
            if captured_url:
                return
            if url.startswith('blob:'):
                return
            # Captura por extensão conhecida de stream
            extensoes = ('.m3u8', '.mp4', '.mkv', '.ts')
            # Captura por padrão de URL de stream (ex: master.txt?...&cache=)
            padrao_stream = 'm3u8' in url or 'master.txt' in url or '/stream/' in url or 'cache=' in url
            if any(url.split('?')[0].endswith(e) for e in extensoes) or padrao_stream:
                captured_url = url

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=headers["User-Agent"],
                extra_http_headers={"Referer": "https://gofilmess.top/"}
            )
            page = context.new_page()
            page.on("request", intercept)

            # Tenta navegar, ignora timeout pois a URL pode já ter sido capturada
            try:
                page.goto(player_url, timeout=20000, wait_until="domcontentloaded")
            except Exception:
                pass

            # Aguarda até 10s para a URL aparecer mesmo após erro de timeout
            import time as _time
            for _ in range(20):
                if captured_url:
                    break
                _time.sleep(0.5)

            browser.close()

        if captured_url:
            stream_url = captured_url

    except Exception as e:
        print(f"[DEBUG - GO] Playwright falhou: {e}")

    return stream_url, headers

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
            "behaviorHints": { "proxyHeaders": {"request": proxy_headers} }
        })

        print(f"[DEBUG - GO] Stream aceito: {stream_url}")

        # Limita a 2 resoluções para não estourar o tempo limite do Stremio
        if len(final_streams) >= 2:
            print("[DEBUG - GO] Limite de streams atingido.")
            break

    if not final_streams:
        notificar_falta_go(titles, content_type, season, episode)

    return final_streams
