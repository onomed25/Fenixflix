import requests
import logging
import json

logger = logging.getLogger(__name__)

session = requests.Session()

def search_serve(imdb_id, content_type, season=None, episode=None):
    """
    Busca streams usando uma Sessão persistente para ser mais rápido
    nas requisições seguintes.
    """
    url = f"http://217.160.125.125:13435/{imdb_id}.json"
    
    try:
      
        response = session.get(url, timeout=4)
        
        response.raise_for_status()
        local_data = response.json()

        
        if local_data.get('id') != imdb_id:
            logger.warning(f"ID do IMDB não corresponde no JSON para {imdb_id}.")
            return []

        streams_formatados = []

        if content_type == 'series' and season and episode:
            try:
                season_str = str(season)
                episode_str = str(episode)

                streams_data = local_data.get('streams', {})
        
                stream_objects = streams_data.get(season_str, {}).get(episode_str, [])

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
                logger.error(f"Erro ao processar streams de séries: {e}")
                return []
        
        elif content_type == 'movie':
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
        logger.error(f"Falha na conexão (Session): {e}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Falha ao ler JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return []

    return []