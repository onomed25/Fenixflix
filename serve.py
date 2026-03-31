import requests
import logging
import json
import os
import itertools

logger = logging.getLogger(__name__)
session = requests.Session()

TAPECONTENT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://87.106.82.84:14923/",
    "Origin": "http://87.106.82.84:14923"
}

# ==========================================
# SISTEMA DE ROTAÇÃO DE HOSTS (ROUND-ROBIN)
# ==========================================
# Lê as variáveis do ambiente (pode ser do arquivo .env ou do painel da nuvem)
HOST = os.getenv("HOST")
HOST_1 = os.getenv("HOST_1")

valid_hosts = []
if HOST:
    valid_hosts.append(HOST.rstrip('/'))
if HOST_1:
    valid_hosts.append(HOST_1.rstrip('/'))

# Cria um ciclo infinito com os hosts disponíveis. 
# Se tiver 2, ele alterna: HOST, HOST_1, HOST, HOST_1...
# Se tiver 1, ele repete sempre o mesmo.
host_cycle = itertools.cycle(valid_hosts) if valid_hosts else None

def get_next_host():
    if host_cycle:
        return next(host_cycle)
    return None
# ==========================================

def search_serve(imdb_id, content_type, season=None, episode=None):
    url = f"http://87.106.82.84:14923/{imdb_id}"

    try:
        response = session.get(url, timeout=10)

        if response.status_code == 404:
            print(f"[DEBUG - SERVE] ❌ Conteúdo não encontrado no servidor (404)")
            return []

        response.raise_for_status()
        local_data = response.json()

        streams_formatados = []

        if content_type == 'series' and season and episode:
            season_str = str(season)
            episode_str = str(episode)
            streams_data = local_data.get('streams', {})

            if season_str not in streams_data:
                print(f"[DEBUG - SERVE] ❌ Temporada '{season_str}' não encontrada no servidor")
                return []

            episodios_disponiveis = list(streams_data.get(season_str, {}).keys())

            stream_objects = streams_data.get(season_str, {}).get(episode_str, [])

            if not stream_objects:
                print(f"[DEBUG - SERVE] ❌ Episódio '{episode_str}' não encontrado na temporada '{season_str}'")
                return []

            for stream_obj in stream_objects:
                if isinstance(stream_obj, dict):
                    label = stream_obj.get("name") or stream_obj.get("description") or "Dublado"
                    url_stream = stream_obj.get("url")
                    streams_formatados.append(montar_stream(url_stream, label))
                elif isinstance(stream_obj, str):
                    streams_formatados.append(montar_stream(stream_obj, "Dublado"))

            return streams_formatados

        elif content_type == 'movie':
            potential_streams = local_data.get('streams', [])

            if not potential_streams:
                print(f"[DEBUG - SERVE] ❌ Campo 'streams' está vazio ou ausente no JSON")
                return []

            for stream_obj in potential_streams:
                if isinstance(stream_obj, dict):
                    label = stream_obj.get("name") or stream_obj.get("description") or "Dublado"
                    url_stream = stream_obj.get("url")
                    streams_formatados.append(montar_stream(url_stream, label))
                elif isinstance(stream_obj, str):
                    streams_formatados.append(montar_stream(stream_obj, "Dublado"))

            return streams_formatados

        else:
            print(f"[DEBUG - SERVE] ⚠️ Tipo de conteúdo desconhecido: '{content_type}'")

    except requests.exceptions.ConnectionError as e:
        print(f"[DEBUG - SERVE] ❌ ERRO DE CONEXÃO - Servidor inacessível: {e}")
    except requests.exceptions.Timeout:
        print(f"[DEBUG - SERVE] ❌ TIMEOUT - O servidor demorou mais de 10s para responder")
    except requests.exceptions.HTTPError as e:
        print(f"[DEBUG - SERVE] ❌ ERRO HTTP: {e}")
    except json.JSONDecodeError as e:
        print(f"[DEBUG - SERVE] ❌ ERRO AO PARSEAR JSON - Resposta inválida: {e}")
    except Exception as e:
        print(f"[DEBUG - SERVE] ❌ ERRO INESPERADO: {type(e).__name__}: {e}")

    return []


def montar_stream(url_stream, label):
    """
    Monta o objeto de stream no formato correto para o Stremio.
    Faz a substituição do proxy alternando entre os hosts configurados.
    """
    # Lógica de substituição da Vercel para os seus HOSTs customizados
    if url_stream and "verel-fenixflix-proxy.vercel.app" in url_stream:
        next_host = get_next_host()
        if next_host:
            # Substitui o domínio antigo pelo domínio da vez
            url_stream = url_stream.replace("https://verel-fenixflix-proxy.vercel.app", next_host)

    stream = {
        "name": "FenixFlix",
        "description": label,
        "url": url_stream,
        "behaviorHints": {
            "notWebReady": False,
            "bingeGroup": "fenixflix-serve"
        }
    }

    if url_stream and "tapecontent.net" in url_stream:
        stream["behaviorHints"]["proxyHeaders"] = {
            "request": TAPECONTENT_HEADERS
        }

    return stream
