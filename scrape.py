import requests
import base64
import re
from urllib.parse import urlparse

# frembed.live
def movie_frembed(imdb):
    stream = ''
    headers_ = {}
    # convert to themoviedb
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    url = f'https://api.themoviedb.org/3/find/{imdb}?api_key=92c1507cc18d85290e7a0b96abb37316&external_source=imdb_id'
    try:
        tmdbid = requests.get(url, headers={'User-Agent': user_agent}).json()['movie_results'][0]['id']
    except:
        tmdbid = ''
    if tmdbid:
        url = f'https://frembed.live/api/films?id={tmdbid}&idType=tmdb'
        referer = f'https://frembed.live/films?id={tmdbid}'
        r = requests.get(url,headers={'User-Agent': user_agent, 'Referer': referer})
        if r.status_code == 200:
            data = r.json()
            url = data.get('link3', '')
            referer = 'https://frembed.live/'
            if url:
                parsed_url = urlparse(url)
                referer = parsed_url.scheme + '://' + parsed_url.hostname + '/'
                origin = parsed_url.scheme + '://' + parsed_url.hostname
                r = requests.get(url,headers={'User-Agent': user_agent, 'Referer': referer})
                if r.status_code == 200:
                    html = r.text
                    base64id = re.findall("'hls': '(.*?)',", html)
                    if base64id:
                        base64id = base64id[0]
                    else:
                        base64id = ''
                    if base64id:
                        stream = base64.b64decode(base64id).decode()
                        headers_['User-Agent'] = user_agent
                        headers_['Origin'] = origin
                        headers_['Referer'] = referer
    try:
        stream_ = [{
            "url": stream,
            "name": "SKYFLIX",
            "description": "Frembed API",
            "behaviorHints": {
                "notWebReady": True,
                "proxyHeaders": {
                    "request": {
                        "User-Agent": headers_['User-Agent'],
                        "Origin": headers_['Origin'],
                        "Referer": headers_['Referer']
                    }
                }
            }
        }]
    except:
        stream_ = []
    return stream_


def serie_frembed(id):
    parts = id.split(':')
    imdb = parts[0] 
    season = parts[1] 
    episode = parts[2]
    stream = ''
    headers_ = {}    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    url = f'https://api.themoviedb.org/3/find/{imdb}?api_key=92c1507cc18d85290e7a0b96abb37316&external_source=imdb_id'
    try:
        tmdbid = requests.get(url, headers={'User-Agent': user_agent}).json()['tv_results'][0]['id']
    except:
        tmdbid = ''
    if tmdbid:
        url = f'https://frembed.live/api/series?id={tmdbid}&sa={str(season)}&epi={str(episode)}&idType=tmdb'
        referer = f'https://frembed.live/series?id={tmdbid}&sa={str(season)}&epi={str(episode)}'
        r = requests.get(url,headers={'User-Agent': user_agent, 'Referer': referer})
        if r.status_code == 200:
            data = r.json()
            url = data.get('link3', '')
            referer = 'https://frembed.live/'
            if url:
                parsed_url = urlparse(url)
                referer = parsed_url.scheme + '://' + parsed_url.hostname + '/'
                origin = parsed_url.scheme + '://' + parsed_url.hostname
                r = requests.get(url,headers={'User-Agent': user_agent, 'Referer': referer})
                if r.status_code == 200:
                    html = r.text
                    base64id = re.findall("'hls': '(.*?)',", html)
                    if base64id:
                        base64id = base64id[0]
                    else:
                        base64id = ''
                    if base64id:
                        stream = base64.b64decode(base64id).decode()
                        headers_['User-Agent'] = user_agent
                        headers_['Origin'] = origin
                        headers_['Referer'] = referer

    try:
        stream_ = [{
            "url": stream,
            "name": "SKYFLIX",
            "description": "Frembed API",
            "behaviorHints": {
                "notWebReady": True,
                "proxyHeaders": {
                    "request": {
                        "User-Agent": headers_['User-Agent'],
                        "Origin": headers_['Origin'],
                        "Referer": headers_['Referer']
                    }
                }
            }
        }]
    except:
        stream_ = []
    return stream_
            





# stream = movie_frembed('tt0133093')
# streams = {'streams': stream}
# print(streams)