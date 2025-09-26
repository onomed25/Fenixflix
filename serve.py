import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import json
import os
import logging

# Configura o logging para este módulo
logger = logging.getLogger(__name__)

def search_serve(imdb_id, content_type, season=None, episode=None):
    """
    Busca streams de um serviço externo com base no IMDb ID.
    Adicionado logging para depuração de falhas de conexão ou parsing.
    """
    url = f"http://sudo.wisp.uno:13435/{imdb_id}.json"
    
    try:
        # Adicionado um timeout para a requisição não ficar presa indefinidamente
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lança uma exceção para status de erro (4xx ou 5xx)
        local_data = response.json()

        if local_data.get('id') != imdb_id:
            logger.warning(f"ID do IMDB não corresponde no JSON para {imdb_id}. Esperado: {imdb_id}, Recebido: {local_data.get('id')}")
            return []

        if content_type == 'series' and season and episode:
            try:
                season_str = str(season)
                episode_str = str(episode)

                streams_data = local_data.get('streams', {})
                stream_objects = streams_data.get(season_str, {}).get(episode_str, [])

                streams_formatados = []
                for stream_obj in stream_objects:
                    if isinstance(stream_obj, dict):
                        streams_formatados.append({
                            "name": "FenixFlix",
                            "url": stream_obj.get("url"),
                            "description": stream_obj.get("description", "Player Padrão")
                        })
                    elif isinstance(stream_obj, str):
                        streams_formatados.append({
                            "name": "FenixFlix",
                            "url": stream_obj
                        })
                return streams_formatados
                
            except Exception as e:
                logger.error(f"Erro ao processar streams de séries para {imdb_id} S{season}E{episode}: {e}")
                return []
        
        elif content_type == 'movie':
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

    except requests.exceptions.RequestException as e:
        # Loga o erro de conexão
        logger.error(f"Falha ao conectar com o servidor de streams para {imdb_id}. Erro: {e}")
        return []
    except json.JSONDecodeError as e:
        # Loga o erro de parsing do JSON
        logger.error(f"Falha ao decodificar o JSON da resposta para {imdb_id}. Erro: {e}")
        return []
    except Exception as e:
        # Pega qualquer outra exceção inesperada
        logger.error(f"Ocorreu um erro inesperado em search_serve para {imdb_id}: {e}")
        return []

    return []
