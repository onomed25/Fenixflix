import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import re

def search_gofilmes(titles, content_type, season=None, episode=None):
    """
    Busca por um filme ou série no GoFilmes e retorna o link da página do player.
    """
    base_url = "https://gofilmess.top"
    for title in titles:
        if not title or len(title) < 2: 
            continue
        search_slug = title.replace('.', '').replace(' ', '-').lower()
        path = 'series' if content_type == 'series' else 'filmes'
        # Corrigido para o caminho correto de busca do site
        url = f"{base_url}/buscar/{quote(search_slug)}"
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # A lógica de busca agora precisa encontrar o link na página de resultados
                search_results = soup.select('div.item a[href]')
                if not search_results:
                    continue

                # Assume que o primeiro resultado é o mais relevante
                content_url = urljoin(base_url, search_results[0]['href'])
                
                content_response = requests.get(content_url, headers=headers, timeout=10)
                if content_response.status_code != 200:
                    continue

                content_soup = BeautifulSoup(content_response.text, 'html.parser')
                player_options = []

                if content_type == 'series':
                    # Seletor atualizado para temporadas
                    season_panels = content_soup.select('div.seasons > div') 
                    if not (season_panels and season and episode and 0 < season <= len(season_panels)):
                        continue
                    
                    selected_panel = season_panels[season - 1]
                    # Seletor atualizado para episódios
                    episode_links = selected_panel.select('ul.episodios > li > a')

                    if 0 < episode <= len(episode_links):
                        episode_page_url = urljoin(base_url, episode_links[episode - 1]['href'])
                        ep_response = requests.get(episode_page_url, headers=headers, timeout=10)
                        if ep_response.status_code == 200:
                            ep_soup = BeautifulSoup(ep_response.text, 'html.parser')
                            # Seletor atualizado para os players de dublado/legendado
                            links = ep_soup.select('div.links-ep a[href]')
                            for link in links:
                                language = re.sub(r'\s*\d+\s*$', '', link.get_text(strip=True)).strip()
                                player_options.append({"name": f"FenixFlix - {language}", "url": urljoin(base_url, link['href'])})
                else: # Para filmes
                    # Seletor atualizado para os players de filmes
                    links = content_soup.select('div.links-ep a[href]')
                    for link in links:
                        language = re.sub(r'\s*\d+\s*$', '', link.get_text(strip=True)).strip()
                        player_options.append({"name": f"FenixFlix - {language}", "url": urljoin(base_url, link['href'])})
                
                if player_options:
                    return player_options
        except Exception:
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

        # Tenta encontrar o link direto do vídeo
        match_new = re.search(r"const videoSrc = '([^']+)'", page_html)
        if match_new:
            stream_url = match_new.group(1)
            return stream_url, None

        # Fallback para iframe
        soup = BeautifulSoup(page_html, 'html.parser')
        headers_for_stremio = headers.copy()
        headers_for_stremio['Referer'] = player_url

        iframe = soup.find('iframe')
        if iframe and iframe.has_attr('src'):
            stream_url = iframe['src']
            return stream_url, headers_for_stremio

        # Fallback para scripts
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
