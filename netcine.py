from urllib.parse import urlparse, quote_plus
import requests
from bs4 import BeautifulSoup
import re
import json

def catalog_search(text):
    catalog = []
    url = 'https://v3.sg.media-imdb.com/suggestion/x/' + quote_plus(text) + '.json?includeVideos=1'
    try:
        data = requests.get(url).json()['d']
        for i in data:
            try:
                poster = i['i']['imageUrl']
                id = i['id']
                title = i['l']
                tp = i['qid']
                if 'series' in tp.lower():
                    tp = 'series'
                y = i['y']
                if 'tt' in id:
                    catalog.append({
                        "id": id,
                        "type": tp,
                        "title": title,
                        "year": int(y),
                        "poster": poster
                    })
            except:
                pass
    except:
        pass
    return catalog

def resolve_stream(url):
    """
    Função modificada para extrair o link do stream diretamente do iframe na página.
    """
    parsed_url = urlparse(url)
    referer = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    stream = ''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "Referer": referer
    }
    
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Procura pelo player "Dublado" primeiro
        player_dub = soup.select_one('#play-1 iframe')
        if player_dub and player_dub.has_attr('src'):
            iframe_src = player_dub['src']
            # Se o src for um caminho relativo, constrói a URL completa
            if iframe_src.startswith('/'):
                 stream = f"{parsed_url.scheme}://{parsed_url.netloc}{iframe_src}"
            else:
                 stream = iframe_src
            return stream, headers

        # Se não encontrar dublado, procura pelo "Legendado"
        player_leg = soup.select_one('#play-2 iframe')
        if player_leg and player_leg.has_attr('src'):
            iframe_src = player_leg['src']
            if iframe_src.startswith('/'):
                 stream = f"{parsed_url.scheme}://{parsed_url.netloc}{iframe_src}"
            else:
                 stream = iframe_src
            return stream, headers
            
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL do player: {e}")
    except Exception as e:
        print(f"Erro ao processar a página do player: {e}")
        
    return stream, headers

def search_term(imdb):
    url = f'https://www.imdb.com/title/{imdb}/'
    keys = []
    year = ''
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0', 'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3'})
        r.raise_for_status()
        src = r.text
        
        script = re.search('json">(.*?)</script>', src, re.DOTALL)
        if script:
            data = json.loads(script.group(1))
            name = data.get('name', '')
            alternate_name = data.get('alternateName', '')
            if name:
                keys.append(name)
            if alternate_name:
                keys.append(alternate_name)

        title_tag = re.search('<title>(.*?)</title>', src)
        if title_tag:
            title = title_tag.group(1)
            year_match = re.search(r'\(.*?(\d{4}).*?\)', title)
            if year_match:
                year = year_match.group(1)

    except Exception as e:
        print(f"Erro ao buscar termo no IMDB: {e}")
        pass
    return keys, year

def opcoes_filmes(url, headers, host):
    """
    Função ajustada para lidar com a nova estrutura e retornar os links das opções de player.
    """
    player_links = []
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        player_menu = soup.select('.player-menu li a')
        if not player_menu:
            return player_links

        for item in player_menu:
            player_id = item.get('href', '').replace('#', '')
            player_name = item.get_text(strip=True).upper()
            
            iframe_container = soup.select_one(f'#{player_id} iframe')
            if iframe_container and iframe_container.has_attr('src'):
                iframe_src = iframe_container['src']
                # Constrói a URL completa se for um caminho relativo
                link = urlparse(url).scheme + "://" + urlparse(url).netloc + iframe_src if iframe_src.startswith('/') else iframe_src
                
                if not 'streamtape' in link: # Evita links do streamtape conforme lógica original
                    player_links.append({'name': player_name.replace(' 1', ''), 'url': link})

    except Exception as e:
        print(f"Erro ao obter opções de filmes: {e}")
        pass
        
    return player_links

def check_item(search,headers,year_imdb,text):
    r = requests.get(search,headers=headers)
    src = r.text
    soup = BeautifulSoup(src,'html.parser')
    box = soup.find("div", {"id": "box_movies"})
    if not box:
        return []
    movies = box.findAll("div", {"class": "movie"})
    count = 0
    for i in movies:
        try:
            year = i.find('span', {'class': 'year'}).text
            year = year.replace('–', '')
        except:
            year = ''
        name = i.find('h2').text
        
        if ':' in text:
            text_search = text.split(':')[1].replace(' ', '').lower()
            name_search = name.replace(' ', '').lower()
            if text_search in name_search:
                count += 1
                break
        else:
            if str(year_imdb) in str(year) or \
               (year_imdb and str(int(year_imdb) + 1) in str(year)) or \
               (year_imdb and str(int(year_imdb) - 1) in str(year)):
                count += 1
                break
    if count > 0:
        return movies
    else:
        return []

def scrape_search(host,headers,text,alternate,year_imdb,type):
    text = text.replace('&amp;', '&')
    alternate = alternate.replace('&amp;', '&')
    url = requests.get(host,headers=headers).url
    url_parsed = urlparse(url)
    new_host = url_parsed.scheme + '://' + url_parsed.hostname + '/'
    try:
        keys_search = text.split(' ')
        search_ = ' '.join(keys_search[:-1]) if len(keys_search) > 2 else text
    except: search_ = text
    try:
        if len(search_.split(' ')) > 2 and ':' in text:
            search_ = text.split(': ')[1]
    except: pass   
    url_search = new_host + '?s=' + quote_plus(search_)
    headers.update({'Cookie': 'XCRF%3DXCRF'})
    movies = check_item(url_search,headers,year_imdb,text)
    if not movies:
        try:
            if ':' in text:
                param_search = text.split(':')[1]
                url_search2 = new_host + '?s=' + quote_plus(param_search)
                movies = check_item(url_search2,headers,year_imdb,text)
        except: movies = []
    for i in movies:
        name = i.find('h2').text
        name_backup = name
        text_backup = text
        textalternate_backup = alternate
        
        # Simplificação e normalização dos nomes para comparação
        name_norm = name.lower().replace(':', '').strip()
        text_norm = text.lower().replace(':', '').strip()
        alternate_norm = alternate.lower().replace(':', '').strip()
        
        year = i.find('span', {'class': 'year'}).text.replace('–', '') if i.find('span', {'class': 'year'}) else ''
        link = i.find('div', {'class': 'imagen'}).find('a').get('href', '') if i.find('div', {'class': 'imagen'}) else ''

        # Condições de match
        year_match = str(year_imdb) in str(year) or \
                     (year_imdb and str(int(year_imdb) + 1) in str(year)) or \
                     (year_imdb and str(int(year_imdb) - 1) in str(year))
        
        title_match = text_norm in name_norm or alternate_norm in name_norm

        if year_match and title_match:
            if type == 'tvshows' and '/tvshows/' in link:
                return link, new_host
            elif type == 'movies' and not '/tvshows/' in link:
                return link, new_host
                                                           
    return '', ''   

def search_link(id):
    streams = []
    host = 'https://nccios.xyz/' # Domínio atualizado
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/88.0.4324.96 Safari/537.36"}
    
    try:
        if ':' in id: # Lógica para Séries
            parts = id.split(':')
            imdb, season, episode = parts[0], parts[1], parts[2]
            search_text, year_imdb = search_term(imdb)
            if search_text and year_imdb:
                text, alternate = search_text[-1], search_text[0]
                link, new_host = scrape_search(host, headers, text, alternate, year_imdb, 'tvshows')
                if '/tvshows/' in link:
                    r = requests.get(link, headers=headers)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    s = soup.select('#seasons .se-c .episodiotitle a')
                    for ep_link in s:
                        # Extrai o número da temporada e episódio do próprio link
                        match = re.search(r'-(\d+)x(\d+)$', ep_link.get('href', ''))
                        if match:
                            s_num, ep_num = match.groups()
                            if int(s_num) == int(season) and int(ep_num) == int(episode):
                                link_ep = ep_link.get('href')
                                player_options = opcoes_filmes(link_ep, headers, new_host)
                                for option in player_options:
                                    stream_url, stream_headers = resolve_stream(option['url'])
                                    if stream_url:
                                        streams.append({
                                            "name": f"Netcine - {option['name']}",
                                            "url": stream_url,
                                            "behaviorHints": {"notWebReady": True, "proxyHeaders": {"request": stream_headers}}
                                        })
                                break # Encontrou o episódio, pode parar o loop
                    if streams: return streams
                                    
        else: # Lógica para Filmes
            imdb = id
            search_text, year_imdb = search_term(imdb)
            if search_text and year_imdb:
                text, alternate = search_text[-1], search_text[0]
                link, new_host = scrape_search(host, headers, text, alternate, year_imdb, 'movies')
                if link and not '/tvshows/' in link:
                    player_options = opcoes_filmes(link, headers, new_host)
                    for option in player_options:
                        stream_url, stream_headers = resolve_stream(option['url'])
                        if stream_url:
                            streams.append({
                                "name": f"FenixFlix",
                                "description": f"{option['name']}", 
                                "url": stream_url,
                                "behaviorHints": {"notWebReady": True, "proxyHeaders": {"request": stream_headers}}
                            })
    except Exception as e:
        print(f"Erro na busca de link: {e}")
        pass
    return streams
