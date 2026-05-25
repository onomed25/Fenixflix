import httpx
import re
import asyncio
import time
import unicodedata
import traceback

BASE_URL = "https://streamflix.live"

# Headers atualizados para simular um navegador real e evitar bloqueios
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://streamflix.live/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

# --- CACHES EM MEMÓRIA RAM (SEM ARQUIVOS JSON) ---
cache_vod = {"data": None, "time": 0}
cache_series = {"data": None, "time": 0}
cache_series_info = {}
CACHE_TTL = 3600  # Mantém a lista na RAM por 1h no máximo
known_series_ids = {}

# --- CLIENTE DEDICADO DO STREAMFLIX ---
_streamflix_client = None

def get_streamflix_client():
    global _streamflix_client
    if _streamflix_client is None or _streamflix_client.is_closed:
        _streamflix_client = httpx.AsyncClient(
            verify=False,
            limits=httpx.Limits(max_connections=50, max_keepalive_connections=20, keepalive_expiry=60.0),
            timeout=httpx.Timeout(25.0, connect=5.0)
        )
    return _streamflix_client

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
    print(f"[StreamFlix Debug] Baixando catálogo completo de filmes na RAM.")
    try:
        resp = await client.get(url, headers=HEADERS)
        if resp.status_code == 200:
            data_list = resp.json()
            # OTIMIZAÇÃO O(1): Cria um dicionário instantâneo -> {"titulo limpo": "id", ...}
            movies_dict = {clean_title(m.get("name", "")): m.get("stream_id") for m in data_list if m.get("name")}
            cache_vod["data"] = movies_dict
            cache_vod["time"] = now
            return movies_dict
    except Exception as e:
        print(f"[StreamFlix Debug] Erro ao buscar filmes: {e}")
    return {}

async def get_all_series(client):
    now = time.time()
    if cache_series["data"] and (now - cache_series["time"]) < CACHE_TTL:
        return cache_series["data"]

    url = f"{BASE_URL}/api_proxy.php?action=get_series"
    print(f"[StreamFlix Debug] Baixando catálogo completo de séries na RAM.")
    try:
        resp = await client.get(url, headers=HEADERS)
        if resp.status_code == 200:
            data_list = resp.json()
            # OTIMIZAÇÃO O(1): Cria um dicionário instantâneo -> {"titulo limpo": "id", ...}
            series_dict = {clean_title(s.get("name", "")): s.get("series_id") for s in data_list if s.get("name")}
            cache_series["data"] = series_dict
            cache_series["time"] = now
            return series_dict
    except Exception as e:
        print(f"[StreamFlix Debug] Erro ao buscar séries: {e}")
    return {}

async def search_serve(titles_to_search, content_type, season=None, episode=None, client=None, cached_series_id=None):
    streams = []
    if not titles_to_search:
        return streams

    c = get_streamflix_client()
    item_id = None
    clean_search_titles = []

    # 1. VERIFICAÇÃO INSTANTÂNEA: Se o ID já veio do app.py, pula todo o processamento de texto!
    if content_type == "series" and cached_series_id and cached_series_id != "N":
        item_id = cached_series_id
        print(f"\n[StreamFlix Debug] ⚡ BUSCA DIRETA (CACHE RAIZ) -> Série ID: {item_id} | S{season}E{episode}")
    else:
        # Só processa os títulos e imprime o bloco de busca se não tiver no cache
        clean_search_titles = [clean_title(t) for t in titles_to_search]
        print(f"\n==================================================")
        print(f"[StreamFlix Debug Completo] NOVA BUSCA INICIADA")
        print(f"[StreamFlix Debug Completo] Tipo: {content_type} | Títulos: {clean_search_titles}")
        if content_type == "series":
            print(f"[StreamFlix Debug Completo] Procurando -> S{season}E{episode}")
        print(f"==================================================")

    try:
        if content_type == "movie":
            movies_dict = await get_all_movies(c)
            # OTIMIZAÇÃO O(1): Busca instantânea sem loop pela lista inteira
            for search_t in clean_search_titles:
                if search_t in movies_dict:
                    item_id = movies_dict[search_t]
                    print(f"[StreamFlix Debug Completo] MATCH EXATO DE FILME! ID: {item_id}")
                    break

            if item_id:
                direct_url = f"{BASE_URL}/api_proxy.php?action=stream&type=movie&id={item_id}"
                streams.append({
                    "name": "FenixFlix",
                    "title": "Dublado\nStream",
                    "url": direct_url,
                    "behaviorHints": {"notWebReady": False, "bingeGroup": "fenixflix-streamflix"}
                })
            else:
                print(f"[StreamFlix Debug Completo] Nenhum filme encontrado.")

        elif content_type == "series" and season is not None and episode is not None:
            
            # Se não tínhamos o ID no cache raiz, tenta buscar na RAM ou na lista geral
            if not item_id:
                for t in clean_search_titles:
                    if t in known_series_ids:
                        item_id = known_series_ids[t]
                        break

                if not item_id:
                    series_dict = await get_all_series(c)
                    for search_t in clean_search_titles:
                        if search_t in series_dict:
                            item_id = series_dict[search_t]
                            print(f"[StreamFlix Debug Completo] MATCH EXATO DE SÉRIE! ID: {item_id}")
                            
                            # Salva os títulos de busca nesta série para acelerar os próximos episódios
                            for t_save in clean_search_titles:
                                known_series_ids[t_save] = item_id
                            break

            # Processamento dos episódios
            if item_id:
                streams.append({"_streamflix_series_id": item_id})

                now = time.time()
                i_data = None

                if item_id in cache_series_info and (now - cache_series_info[item_id]["time"]) < CACHE_TTL:
                    print(f"[StreamFlix Debug Completo] ⚡ Usando cache rápido de episódios para a série ID {item_id}!")
                    i_data = cache_series_info[item_id]["data"]
                else:
                    info_url = f"{BASE_URL}/api_proxy.php?action=get_series_info&series_id={item_id}"
                    
                    max_tentativas = 3
                    for tentativa in range(max_tentativas):
                        try:
                            i_resp = await c.get(info_url, headers=HEADERS)
                            i_resp.raise_for_status()
                            i_data = i_resp.json()

                            cache_series_info[item_id] = {"data": i_data, "time": now}
                            break
                        except httpx.ReadTimeout:
                            print(f"[StreamFlix Debug Completo] ⚠️ Timeout na tentativa {tentativa + 1}/{max_tentativas}.")
                            if tentativa < max_tentativas - 1:
                                await asyncio.sleep(2)
                        except Exception as ex:
                            break

                if not i_data:
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
                    else:
                        print(f"[StreamFlix Debug Completo] ❌ O site tem a temporada {season}, mas NÃO TEM o episódio {episode}.")
                else:
                    print(f"[StreamFlix Debug Completo] ❌ O site NÃO TEM a temporada {season_str} cadastrada para a série ID {item_id}.")
            else:
                print(f"[StreamFlix Debug Completo] Série não encontrada na lista do site. Retornando flag 'N' para o raiz.")
                streams.append({"_streamflix_series_id": "N"})

    except Exception as e:
        print(f"[StreamFlix Debug Completo] Erro global detectado!")
        traceback.print_exc()

    return streams

if __name__ == "__main__":
    pass