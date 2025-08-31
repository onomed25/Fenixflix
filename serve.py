import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import json
import os

def search_serve(imdb_id, content_type, season=None, episode=None):
    url = f"http://sudo.wisp.uno:13435/{imdb_id}.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        local_data = response.json()

        if local_data.get('id') != imdb_id:
            return []

        if content_type == 'series' and season and episode:
            try:
                season_str = str(season)
                episode_str = str(episode)

                streams_data = local_data.get('streams', {})
                
                urls = streams_data.get(season_str, {}).get(episode_str, [])

                streams_formatados = []
                for url in urls:
                    streams_formatados.append({
                        "name": "Fenixflix",
                        "url": url
                    })
                return streams_formatados
                
            except Exception:
                return []
        
        elif content_type == 'movie':
            return local_data.get('streams', [])

    except (requests.exceptions.RequestException, json.JSONDecodeError):
        return []

    return []
