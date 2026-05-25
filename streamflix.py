import httpx
import re
import asyncio
import time
import unicodedata
import json
import traceback

BASE_URL = "https://streamflix.live"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://streamflix.live/"
}

cache_vod = {"data": None, "time": 0}
cache_series = {"data": None, "time": 0}
CACHE_TTL = 3600

known_series_ids = {}

def clean_title(title):
    cleaned = str(title).lower().strip()
    cleaned = re.sub(r'\[.*?\]|\(.*?\)', ' ', cleaned)
    cleaned = unicodedata.normalize('NFKD', cleaned).encode('ASCII', 'ignore').decode('utf-8')
    cleaned = re.sub(r'\b(4k|hd|fullhd|uhd|hdr|hybrid|dublado|legendado|leg|dub|dual|audio|cam|ts)\b', ' ', cleaned)
    cleaned = re.sub(r'\b(19|20)\d{2}\b', ' ', cleaned)
    cleaned = re.sub(r'[^a-z0-9\s]', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

async def get_all_movies(client):
    now = time.time()
    if cache_vod["data"] and (now - cache_vod["time"]) < CACHE_TTL:
        return cache_vod["data"]

    url = f"{BASE_URL}/api_proxy.php?action=get_vod_streams"
    try:
        resp = await client.get(url, headers=HEADERS)
        if resp.status_code == 200:
            data = resp.json()
            cache_vod["data"] = data
            cache_vod["time"] = now
            return data
    except Exception as e:
        print(f"[StreamFlix Debug] Erro ao buscar filmes: {e}")
    return []

async def get_all_series(client):
    now = time.time()
    if cache_series["data"] and (now - cache_series["time"]) < CACHE_TTL:
        return cache_series["data"]

    url = f"{BASE_URL}/api_proxy.php?action=get_series"
    try:
        resp = await client.get(url, headers=HEADERS)
        if resp.status_code == 200:
            data = resp.json()
            cache_series["data"] = data
            cache_series["time"] = now
            return data
    except Exception as e:
        print(f"[StreamFlix Debug] Erro ao buscar séries: {e}")
    return []

async def search_serve(titles_to_search, content_type, season=None, episode=None, client: httpx.AsyncClient = None, cached_series_id=None):
    streams = []
    if not titles_to_search:
        return streams

    clean_search_titles = [clean_title(t) for t in titles_to_search]
    print(f"\n[StreamFlix Debug] Iniciando busca | TMDB Limpos: {clean_search_titles}")

    async def _run(c):
        try:
            item_id = None

            if content_type == "movie":
                movies = await get_all_movies(c)
                for movie in movies:
                    raw_name = movie.get("name", "")
                    c_name = clean_title(raw_name)
                    if any(t == c_name for t in clean_search_titles):
                        item_id = movie.get("stream_id")
                        print(f"[StreamFlix Debug] MATCH EXATO! '{raw_name}' -> ID: {item_id}")
                        break

                if item_id:
                    direct_url = f"{BASE_URL}/api_proxy.php?action=stream&type=movie&id={item_id}"
                    streams.append({
                        "name": "FenixFlix",
                        "title": "Dublado\nStream",
                        "url": direct_url,
                        "behaviorHints": {"notWebReady": False, "bingeGroup": "fenixflix-streamflix"}
                    })
                    print(f"[StreamFlix Debug] URL enviada ao Stremio (Filme): {direct_url}")

            elif content_type == "series" and season is not None and episode is not None:
                if cached_series_id:
                    item_id = cached_series_id
                    print(f"[StreamFlix Debug] Usando ID DIRETO do JSON: {item_id}")
                else:
                    for t in clean_search_titles:
                        if t in known_series_ids:
                            item_id = known_series_ids[t]
                            print(f"[StreamFlix Debug] Usando ID da série salvo na base de memória: {item_id}")
                            break

                    if not item_id:
                        series_list = await get_all_series(c)
                        for s in series_list:
                            raw_name = s.get("name", "")
                            c_name = clean_title(raw_name)
                            if any(t == c_name for t in clean_search_titles):
                                item_id = s.get("series_id")
                                print(f"[StreamFlix Debug] MATCH EXATO DE SÉRIE! '{raw_name}' -> ID: {item_id}")

                                for t_save in clean_search_titles:
                                    known_series_ids[t_save] = item_id
                                break

                if item_id:
                    streams.append({"_streamflix_series_id": item_id})

                    info_url = f"{BASE_URL}/api_proxy.php?action=get_series_info&series_id={item_id}"

                    # Bloco Try-Except específico para a proteção contra o Timeout
                    try:
                        i_resp = await c.get(info_url, headers=HEADERS)
                        i_resp.raise_for_status()
                        i_data = i_resp.json()
                    except httpx.ReadTimeout:
                        print(f"[StreamFlix Debug] Timeout! O servidor demorou muito para responder sobre a série ID {item_id}.")
                        return streams
                    except Exception as ex:
                        print(f"[StreamFlix Debug] Falha ao baixar informações dos episódios: {ex}")
                        return streams

                    episodes_dict = i_data.get("episodes", {})
                    season_str = str(season)

                    if season_str in episodes_dict:
                        eps = episodes_dict[season_str]
                        ep_id = None
                        for ep in eps:
                            if str(ep.get("episode_num")) == str(episode):
                                ep_id = ep.get("id")
                                break

                        if ep_id:
                            direct_url = f"{BASE_URL}/api_proxy.php?action=stream&type=series&id={ep_id}"
                            streams.append({
                                "name": "FenixFlix",
                                "title": "Dublado\nStream",
                                "url": direct_url,
                                "behaviorHints": {"notWebReady": False, "bingeGroup": "fenixflix-streamflix"},
                                "_streamflix_series_id": item_id
                            })
                            print(f"[StreamFlix Debug] URL enviada ao Stremio (Série): {direct_url}")
                    else:
                        print(f"[StreamFlix Debug] Temporada {season} não encontrada para a série ID {item_id}")
                else:
                    print(f"[StreamFlix Debug] Série não encontrada no site. Retornando flag 'N' para o raiz.")
                    streams.append({"_streamflix_series_id": "N"})

        except Exception as e:
            print(f"[StreamFlix Debug] Erro global detectado!")
            traceback.print_exc()

        return streams

    if client is not None:
        return await _run(client)
    else:
        # Aumentamos o timeout global para 20 segundos
        async with httpx.AsyncClient(verify=False, timeout=30.0) as c:
            return await _run(c)

# --- BLOCO DE EXECUÇÃO ISOLADA ---
if __name__ == "__main__":
    async def testar_streamflix():
        print("==================================================")
        print("🎬 INICIANDO TESTE ISOLADO DO STREAMFLIX 🎬")
        print("==================================================\n")

        # Aumentamos o timeout também no teste local
        async with httpx.AsyncClient(verify=False, timeout=20.0) as client:

            print("👉 TESTE 1: Buscando Série ('The Last of Us', S01E03)...")
            titulos_serie = ["the last of us", "the last of us (2023)"]
            resultado_serie = await search_serve(
                titles_to_search=titulos_serie,
                content_type="series",
                season=1,
                episode=3,
                client=client
            )
            print("\n✅ RETORNO FINAL DA SÉRIE:")
            print(json.dumps(resultado_serie, indent=4, ensure_ascii=False))
            print("\n--------------------------------------------------\n")

            print("👉 TESTE 2: Buscando Filme ('Avatar')...")
            titulos_filme = ["avatar", "avatar the way of water"]
            resultado_filme = await search_serve(
                titles_to_search=titulos_filme,
                content_type="movie",
                client=client
            )
            print("\n✅ RETORNO FINAL DO FILME:")
            print(json.dumps(resultado_filme, indent=4, ensure_ascii=False))
            print("\n==================================================")

    asyncio.run(testar_streamflix())
