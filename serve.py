import httpx
import logging
import random

logger = logging.getLogger(__name__)

# Headers para o tapecontent
TAPECONTENT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "http://87.106.82.84:14923/",
    "Origin": "http://87.106.82.84:14923"
}

async def search_serve(imdb_id, content_type, season=None, episode=None):
    """
    Busca streams no servidor remoto e formata para o Stremio usando httpx.
    """
    url = f"http://87.106.82.84:14923/{imdb_id}"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)

        if response.status_code == 404:
            print("[DEBUG - SERVE] ❌ Conteúdo não encontrado (404)")
            return []

        response.raise_for_status()
        local_data = response.json()

        streams_formatados = []

        # 🔥 SÉRIES
        if content_type == 'series' and season and episode:
            season_str = str(season)
            episode_str = str(episode)

            streams_data = local_data.get('streams', {})

            if season_str not in streams_data:
                print(f"[DEBUG] ❌ Temporada {season_str} não encontrada")
                return []

            stream_objects = streams_data.get(season_str, {}).get(episode_str, [])

            if not stream_objects:
                print(f"[DEBUG] ❌ Episódio {episode_str} não encontrado")
                return []

            for stream_obj in stream_objects:
                if isinstance(stream_obj, dict):
                    label = stream_obj.get("name") or stream_obj.get("description") or "Dublado"
                    url_stream = stream_obj.get("url")
                else:
                    label = "Dublado"
                    url_stream = stream_obj

                streams_formatados.append(montar_stream(url_stream, label))

            return streams_formatados

        # 🔥 FILMES
        elif content_type == 'movie':
            potential_streams = local_data.get('streams', [])

            if not potential_streams:
                print("[DEBUG] ❌ 'streams' vazio")
                return []

            for stream_obj in potential_streams:
                if isinstance(stream_obj, dict):
                    label = stream_obj.get("name") or stream_obj.get("description") or "Dublado"
                    url_stream = stream_obj.get("url")
                else:
                    label = "Dublado"
                    url_stream = stream_obj

                streams_formatados.append(montar_stream(url_stream, label))

            return streams_formatados

        else:
            print(f"[DEBUG] ⚠️ Tipo desconhecido: {content_type}")

    except httpx.RequestError as e:
        print(f"[ERRO HTTP] {e}")
    except Exception as e:
        print(f"[ERRO GERAL] {type(e).__name__}: {e}")

    return []


def montar_stream(url_stream, label):
    # Lista de URLs base para balanceamento
    bases = [
        "https://passing-melinda-onomed1-d0cbec40.koyeb.app",
        "https://husky-denny-fenixflixaddon-ec8e842b.koyeb.app"
    ]
    
    if url_stream and "/stream/" in url_stream:
        path_index = url_stream.find("/stream/")
        path = url_stream[path_index:]
        
        # Sorteia uma das URLs da lista para distribuir a carga
        base_escolhida = random.choice(bases)
        url_stream = f"{base_escolhida}{path}"

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