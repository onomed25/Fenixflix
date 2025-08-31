import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import json
import os

def search_topflix(imdb_id, content_type, season=None, episode=None):

    json_path = os.path.join("Json", f"{imdb_id}.json")
    
    if not os.path.exists(json_path):
        return []

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            local_data = json.load(f)

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

    except (IOError, json.JSONDecodeError):
        return []

    return []
