import httpx
import logging
import random
import os 
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)

SERVE_ = os.getenv("serve")

TAPECONTENT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

async def search_serve(imdb_id, content_type, season=None, episode=None, client: httpx.AsyncClient = None, titles=None):
    url = f"{SERVE_}/{imdb_id}"

    async def _fetch(c):
        response = await c.get(url)
        if response.status_code == 404:
            print("[DEBUG - SERVE] ❌ Conteúdo não encontrado (404)")
            return None
        response.raise_for_status()
        return response.json()

    try:
        if client is not None:
            local_data = await _fetch(client)
        else:
            async with httpx.AsyncClient(timeout=10) as c:
                local_data = await _fetch(c)

        if local_data is None:
            return []

        streams_formatados = []

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
                streams_formatados.append(montar_stream(url_stream, label, content_type, season, episode, titles))

            return streams_formatados

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
                streams_formatados.append(montar_stream(url_stream, label, content_type, season, episode, titles))

            return streams_formatados

        else:
            print(f"[DEBUG] ⚠️ Tipo desconhecido: {content_type}")

    except httpx.RequestError as e:
        print(f"[ERRO HTTP] {e}")
    except Exception as e:
        print(f"[ERRO GERAL] {type(e).__name__}: {e}")

    return []


import re

def montar_stream(url_stream, label, content_type, season=None, episode=None, titles=None):
    bases = [
        "https://husky-denny-fenixflixaddon-ec8e842b.koyeb.app",
        "https://passing-melinda-onomed1-d0cbec40.koyeb.app"
    ]
    base = random.choice(bases)

    if url_stream and "/stream/" in url_stream:
        path_index = url_stream.find("/stream/")
        path = url_stream[path_index:]
        url_stream = f"{base}{path}"

    # 1. Procurar qualidade
    qualidade = "HD"
    label_lower = label.lower()
    url_lower = (url_stream or "").lower()
    if "1080" in label_lower or "1080" in url_lower:
        qualidade = "1080p"
    elif "720" in label_lower or "720" in url_lower:
        qualidade = "720p"
    elif "4k" in label_lower or "2160" in url_lower:
        qualidade = "4K"
    elif "hd" in label_lower or "hd" in url_lower:
        qualidade = "HD"

    # 2. Limpar label para a descrição (remover qualidade e FenixFlix)
    desc_label = label
    desc_label = re.sub(r'(?i)\bFenixflix\b', '', desc_label)
    desc_label = re.sub(r'(?i)\b(1080p|720p|4k|2160p|hd)\b', '', desc_label)
    # Remover múltiplos espaços/hifens/pontos extras
    desc_label = re.sub(r'\s*-\s*', ' ', desc_label)
    desc_label = re.sub(r'\s+', ' ', desc_label).strip()

    if not desc_label:
        if "legen" in label_lower:
            desc_label = "Legendado"
        else:
            desc_label = "Dublado"

    # 3. Obter nome do filme/série
    nome = ""
    if titles:
        if isinstance(titles, list) or isinstance(titles, tuple):
            nome = titles[0] if len(titles) > 0 else ""
        else:
            nome = str(titles)

    # 4. Formatar temporada/episódio
    tep = ""
    if content_type == "series" and season and episode:
        try:
            s_pad = f"{int(season):02d}"
            e_pad = f"{int(episode):02d}"
            tep = f"T{s_pad} EP{e_pad}"
        except Exception:
            tep = f"T{season} EP{episode}"

    # 5. Montar descrição ("nome no topo")
    partes = []
    if nome:
        partes.append(nome)
    if tep:
        partes.append(tep)
    partes.append(desc_label)
    description_str = "\n".join(partes)

    stream = {
        "name": f"FenixFlix\n{qualidade}",
        "description": description_str,
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
