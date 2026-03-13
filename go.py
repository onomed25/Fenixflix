import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import re

def search_gofilmes(titles, content_type, season=None, episode=None):
    """
    Busca por um filme ou série no gofilmes e retorna o link do player para o item específico.
    """
    base_url = "https://gofilmess.top"

    if content_type == 'series':
        path = 'series'
        selector = 'div.ep a[href]'
    else:
        path = ''
        selector = 'div.link a[href]'

    for title in titles:
        search_slug = title.replace('.', '').replace(' ', '-').lower()

        if path:
            url = f"{base_url}/{path}/{quote(search_slug)}"
        else:
            url = f"{base_url}/{quote(search_slug)}"

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
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
    """
    stream_url = ''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/88.0.4324.96 Safari/537.36"}

    try:
        page_headers = headers.copy()
        page_headers.update({'Referer': 'https://gofilmess.top/'})

        r = requests.get(player_url, headers=page_headers, timeout=10, allow_redirects=True)
        soup = BeautifulSoup(r.text, 'html.parser')

        iframe = soup.find('iframe')
        if iframe and iframe.has_attr('src'):
            stream_url = iframe['src']
            return stream_url, headers

        video_tag = soup.find('video')
        if video_tag:
            source_tag = video_tag.find('source')
            if source_tag and source_tag.has_attr('src'):
                stream_url = source_tag['src']
                return stream_url, headers

        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'playlist' in script.string:
                match = re.search(r'"file"\s*:\s*"([^"]+)"', script.string)
                if match:
                    stream_url = match.group(1)
                    return stream_url, headers

        api_url = None
        for script in scripts:
            if script.string and 'fetchVideoLink' in script.string:
                match = re.search(r'const apiUrl = `([^`]+)`;', script.string)
                if match:
                    api_url = match.group(1)
                    api_headers = headers.copy()
                    api_headers['Referer'] = player_url

                    api_response = requests.get(api_url, headers=api_headers, timeout=15)
                    api_response.raise_for_status()

                    stream_url = api_response.text.strip()
                    return stream_url, headers

    except Exception:
        pass

    return stream_url, headers

# ---------------------------------------------------------
# NOVA FUNÇÃO ADICIONADA: Filtro e Orquestração
# ---------------------------------------------------------
def search_serve(titles, content_type, season=None, episode=None):
    """
    Função orquestradora que o app.py chama para buscar e já devolver o link final filtrado.
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

    return final_streams
