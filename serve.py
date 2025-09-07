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
                
                # Pega a lista de objetos de stream do JSON
                stream_objects = streams_data.get(season_str, {}).get(episode_str, [])

                streams_formatados = []
                # Itera sobre cada objeto na lista
                for stream_obj in stream_objects:
                    # Verifica se o item é um dicionário (novo formato) ou uma string (formato antigo)
                    if isinstance(stream_obj, dict):
                        # Novo formato: extrai URL e descrição do objeto
                        streams_formatados.append({
                            "name": "FenixFlix",
                            "url": stream_obj.get("url"),
                            "description": stream_obj.get("description", "Player Padrão") # Usa a descrição do JSON
                        })
                    elif isinstance(stream_obj, str):
                        # Formato antigo: mantém a compatibilidade
                        streams_formatados.append({
                            "name": "FenixFlix",
                            "url": stream_obj
                        })
                return streams_formatados
                
            except Exception:
                return []
        
        elif content_type == 'movie':
            # Para filmes, assume que a estrutura pode ser a antiga ou a nova
            streams_formatados = []
            potential_streams = local_data.get('streams', [])
            for stream_obj in potential_streams:
                 if isinstance(stream_obj, dict):
                    streams_formatados.append({
                        "name": stream_obj.get("name", "FenixFlix"),
                        "url": stream_obj.get("url"),
                        "description": stream_obj.get("description")
                    })
                 elif isinstance(stream_obj, str):
                    streams_formatados.append({
                        "name": "FenixFlix",
                        "url": stream_obj
                    })
            return streams_formatados

    except (requests.exceptions.RequestException, json.JSONDecodeError):
        return []

    return []
