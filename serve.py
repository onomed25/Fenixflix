import httpx
import logging

logger = logging.getLogger(__name__)

async def search_serve(imdb_id, content_type, season=None, episode=None):

    url = f"http://87.106.82.84:14923/{imdb_id}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)

            if response.status_code == 404:
                return []

            response.raise_for_status()
            local_data = response.json()

            streams_formatados = []

            if content_type == 'series' and season and episode:
                season_str = str(season)
                episode_str = str(episode)
                streams_data = local_data.get('streams', {})

                if season_str not in streams_data:
                    return []

                stream_objects = streams_data.get(season_str, {}).get(episode_str, [])

                if not stream_objects:
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
                    return []

                for stream_obj in potential_streams:
                    if isinstance(stream_obj, dict):
                        label = stream_obj.get("name") or stream_obj.get("description") or "Dublado"
                        url_stream = stream_obj.get("url")
                        streams_formatados.append(montar_stream(url_stream, label))
                    elif isinstance(stream_obj, str):
                        streams_formatados.append(montar_stream(stream_obj, "Dublado"))

                return streams_formatados

        except Exception as e:
            logger.error(f"[SERVE] Erro na busca assíncrona: {e}")

    return []


def montar_stream(url_stream, label):

    return {
        "name": "FenixFlix",
        "description": label,
        "url": url_stream,
        "behaviorHints": {
            "notWebReady": False,
            "bingeGroup": "fenixflix-serve"
        }
    }