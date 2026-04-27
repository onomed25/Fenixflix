import httpx
import re
import asyncio
import time
import unicodedata

BASE_URL = "https://streamflix.live"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://streamflix.live/"
}

cache_vod = {"data": None, "time": 0}
cache_series = {"data": None, "time": 0}
CACHE_TTL = 3600 

def clean_title(title):
    """Limpa o título para uma comparação EXATA e rigorosa, evitando filmes errados."""
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
        resp = await client.get(url, headers=HEADERS, timeout=15)
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
        resp = await client.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            cache_series["data"] = data
            cache_series["time"] = now
            return data
    except Exception as e:
        print(f"[StreamFlix Debug] Erro ao buscar séries: {e}")
    return []

async def search_serve(titles_to_search, content_type, season=None, episode=None):
    streams = []
    if not titles_to_search:
        return streams

    clean_search_titles = [clean_title(t) for t in titles_to_search]
    print(f"\n[StreamFlix Debug] Iniciando busca | TMDB Limpos: {clean_search_titles}")

    async with httpx.AsyncClient(verify=False) as client:
        try:
            item_id = None
            
            if content_type == "movie":
                movies = await get_all_movies(client)
                for movie in movies:
                    raw_name = movie.get("name", "")
                    c_name = clean_title(raw_name)
                    
                    if any(t == c_name for t in clean_search_titles):
                        item_id = movie.get("stream_id")
                        print(f"[StreamFlix Debug] MATCH EXATO! '{raw_name}' -> ID: {item_id}")
                        break
                
                if item_id:
                    stream_url_req = f"{BASE_URL}/api_proxy.php?action=get_stream_url&type=movie&id={item_id}"
                    s_resp = await client.get(stream_url_req, headers=HEADERS, timeout=10)
                    s_data = s_resp.json()
                    
                    if "stream_url" in s_data:
                        streams.append({
                            "name": "FenixFlix",
                            "title": "Dublado\nStream",
                            "url": s_data["stream_url"],
                            "behaviorHints": {"notWebReady": False, "bingeGroup": "fenixflix-streamflix"}
                        })

            elif content_type == "series" and season is not None and episode is not None:
                series_list = await get_all_series(client)
                for s in series_list:
                    raw_name = s.get("name", "")
                    c_name = clean_title(raw_name)
                    
                    if any(t == c_name for t in clean_search_titles):
                        item_id = s.get("series_id")
                        print(f"[StreamFlix Debug] MATCH EXATO DE SÉRIE! '{raw_name}' -> ID: {item_id}")
                        break
                
                if item_id:
                    info_url = f"{BASE_URL}/api_proxy.php?action=get_series_info&series_id={item_id}"
                    i_resp = await client.get(info_url, headers=HEADERS, timeout=10)
                    i_data = i_resp.json()
                    
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
                            stream_url_req = f"{BASE_URL}/api_proxy.php?action=get_stream_url&type=series&id={ep_id}"
                            s_resp = await client.get(stream_url_req, headers=HEADERS, timeout=10)
                            s_data = s_resp.json()
                            
                            if "stream_url" in s_data:
                                streams.append({
                                    "name": "FenixFlix",
                                    "title": "Dublado\nStream",
                                    "url": s_data["stream_url"],
                                    "behaviorHints": {"notWebReady": False, "bingeGroup": "fenixflix-streamflix"}
                                })
        except Exception as e:
            print(f"[StreamFlix Debug] Erro global: {e}")

    return streams