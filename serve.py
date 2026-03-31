import requests
import logging
import json

logger = logging.getLogger(__name__)
session = requests.Session()

# Headers para o tapecontent (se necessário)
TAPECONTENT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://87.106.82.84:14923/",
    "Origin": "http://87.106.82.84:14923"
}

def search_serve(imdb_id, content_type, season=None, episode=None):
    """
    Busca streams no servidor remoto e formata para o Stremio.
    """
    url = f"http://87.106.82.84:14923/{imdb_id}"

    try:
        response = session.get(url, timeout=10)

        if response.status_code == 404:
            print(f"[DEBUG - SERVE] ❌ Conteúdo não encontrado no servidor (404)")
            return []

        response.raise_for_status()
        local_data = response.json()

        streams_formatados = []

        # Lógica para Séries
        if content_type == 'series' and season and episode:
            season_str = str(season)
            episode_str = str(episode)
            streams_data = local_data.get('streams', {})

            if season_str not in streams_data:
                print(f"[DEBUG - SERVE] ❌ Temporada '{season_str}' não encontrada")
                return []

            stream_objects = streams_data.get(season_str, {}).get(episode_str, [])

            if not stream_objects:
                print(f"[DEBUG - SERVE] ❌ Episódio '{episode_str}' não encontrado")
                return []

            for stream_obj in stream_objects:
                if isinstance(stream_obj, dict):
                    label = stream_obj.get("name") or stream_obj.get("description") or "Dublado"
                    url_stream = stream_obj.get("url")
                    streams_formatados.append(montar_stream(url_stream, label))
                elif isinstance(stream_obj, str):
                    streams_formatados.append(montar_stream(stream_obj, "Dublado"))

            return streams_formatados

        # Lógica para Filmes
        elif content_type == 'movie':
            potential_streams = local_data.get('streams', [])

            if not potential_streams:
                print(f"[DEBUG - SERVE] ❌ Campo 'streams' está vazio ou ausente")
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

    except Exception as e:
        print(f"[DEBUG - SERVE] ❌ ERRO: {type(e).__name__}: {e}")

    return []


def montar_stream(url_stream, label):
    """
    Monta o objeto de stream e redireciona para o Proxy da Vercel/Koyeb.
    """
    # Configure aqui o seu proxy principal
    PROXY_BASE = "https://verel-fenixflix-proxy.vercel.app"
    
    # Se a URL original tiver '/stream/', nós a reconstruímos usando o Proxy
    if url_stream and "/stream/" in url_stream:
        # Encontra onde começa o caminho do stream
        path_index = url_stream.find("/stream/")
        path = url_stream[path_index:]
        # Substitui o IP/Host antigo pelo seu Proxy
        url_stream = f"{PROXY_BASE}{path}"

    stream = {
        "name": "FenixFlix",
        "description": label,
        "url": url_stream,
        "behaviorHints": {
            "notWebReady": False,
            "bingeGroup": "fenixflix-serve"
        }
    }

    # Headers específicos para tapecontent se o link for desse provedor
    if url_stream and "tapecontent.net" in url_stream:
        stream["behaviorHints"]["proxyHeaders"] = {
            "request": TAPECONTENT_HEADERS
        }

    return stream