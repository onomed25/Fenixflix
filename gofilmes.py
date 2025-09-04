import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import re

def search_gofilmes(titles, content_type, season=None, episode=None):
    """
    Busca por um filme ou série no GoFilmes e retorna os links dos players com informação de idioma na descrição.
    """
    base_url = "https://gofilmess.top"
    for title in titles:
        if not title or len(title) < 2: 
            continue
        
        search_slug = title.replace('.', '').replace(' ', '-').lower()
        path = 'series' if content_type == 'series' else 'filmes'
        
        url = f"{base_url}/{path}/{quote(search_slug)}" if content_type == 'series' else f"{base_url}/{quote(search_slug)}"
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                if content_type == 'series':
                    if not (season and episode): continue
                    
                    season_panels = soup.select('div.seasons > div.season')
                    if not (0 < season <= len(season_panels)): continue

                    selected_panel = season_panels[season - 1]
                    episode_links = selected_panel.select('ul.episodios li a')
                    if not (0 < episode <= len(episode_links)): continue
                    
                    episode_url = urljoin(base_url, episode_links[episode - 1]['href'])
                    episode_response = requests.get(episode_url, headers=headers, timeout=10)
                    if episode_response.status_code != 200: continue
                    
                    episode_soup = BeautifulSoup(episode_response.text, 'html.parser')
                    # A lógica de extração de players da página do episódio é a mesma de filmes
                    soup = episode_soup
                
                # Lógica de extração de players para filmes e episódios
                player_options = []
                options_divs = soup.select('div.options')
                for options_div in options_divs:
                    lang_span = options_div.find('span')
                    language = lang_span.get_text(strip=True) if lang_span else "Indefinido"
                    links = options_div.select('div.link a')
                    for idx, link in enumerate(links, 1):
                        player_name = link.get_text(strip=True)
                        player_url = link.get('href')
                        if player_url:
                            player_options.append({
                                "name": "FenixFlix",
                                "description": f"{language} {player_name}",
                                "url": urljoin(base_url, player_url)
                            })
                return player_options

        except requests.exceptions.RequestException:
            continue
            
    return []


def resolve_stream(player_url):
    """
    Resolve o stream com múltiplos métodos.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://gofilmess.top/'
        }
        response = requests.get(player_url, headers=headers, timeout=15)
        response.raise_for_status()
        page_html = response.text

        # --- MÉTODO 1 (Busca por 'videoSrc') ---
        match_new = re.search(r"const videoSrc = '([^']+)'", page_html)
        if match_new:
            stream_url = match_new.group(1)
            return stream_url, None

        # --- MÉTODO 2 (Busca por iframe) ---
        soup = BeautifulSoup(page_html, 'html.parser')
        headers_for_stremio = headers.copy()
        headers_for_stremio['Referer'] = player_url

        iframe = soup.find('iframe')
        if iframe and iframe.has_attr('src'):
            stream_url = iframe['src']
            return stream_url, headers_for_stremio

        # --- MÉTODO 3 (Busca por 'file' em scripts) ---
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                match_old = re.search(r'"file"\s*:\s*"([^"]+)"', script.string)
                if match_old:
                    stream_url = match_old.group(1)
                    return stream_url, headers_for_stremio
        return None, None

    except Exception:
        return None, None
