import httpx
import asyncio
import time
import re
from rapidfuzz import fuzz
import os
from cachetools import TTLCache

USER_AGENT = "Dart/3.0 (dart:io)"
BASE_URL = "https://animes-api-v6.homura.online"

HOMURA_CACHE = TTLCache(maxsize=10, ttl=24*3600)

async def _get_catalog(client: httpx.AsyncClient):
    """Obtém o catálogo completo e faz cache em RAM por 24h."""
    catalog = HOMURA_CACHE.get("catalog")
    index = HOMURA_CACHE.get("index")
    if catalog is not None and index is not None:
        return catalog, index
        
    url = f"{BASE_URL}/anime/list"
    try:
        auth_token = os.getenv("HOMURA_TOKEN")
        res = await client.get(url, headers={"Authorization": auth_token, "User-Agent": USER_AGENT}, timeout=20.0)
        data = res.json()
        if isinstance(data, list) and len(data) > 0:
            HOMURA_CACHE["catalog"] = data
            
            # Construir o índice O(1)
            new_index = {}
            for item in data:
                name = (item.get("name") or "").lower()
                alt = (item.get("alternative_name") or "").lower()
                if name:
                    new_index[name] = item
                if alt:
                    new_index[alt] = item
            HOMURA_CACHE["index"] = new_index
            
            return data, new_index
    except Exception as e:
        print(f"[Homura] Erro ao buscar catálogo completo: {e}")
    return [], {}

def _fuzzy_match(titles, catalog, index):
    titles_lower = [t.lower() for t in titles if t]
    if not titles_lower:
        return None

    # Tenta achar exato no Dicionário O(1)
    for t in titles_lower:
        if t in index:
            return index[t]

    # Fallback para fuzzy search em caso de erro de digitação/typo
    best_match = None
    best_score = 0
    for item in catalog:
        name = (item.get("name") or "").lower()
        alt_name = (item.get("alternative_name") or "").lower()
        
        for t in titles_lower:
            score1 = fuzz.ratio(t, name)
            score2 = fuzz.ratio(t, alt_name) if alt_name else 0
            
            max_score = max(score1, score2)
            if max_score > best_score:
                best_score = max_score
                best_match = item
                
    if best_score > 85:
        return best_match
    return None

async def search_serve(tmdb_id: str, content_type: str, season=None, episode=None, client: httpx.AsyncClient = None, titles: list = None, **kwargs):
    streams = []
    
    if not titles:
        print(f"[Homura] Sem títulos fornecidos para {tmdb_id}, abortando.")
        return streams
        
    close_client = False
    if client is None:
        print("[Aviso] Criando client HTTPX local em homura (sem pool). Use 'client=' para otimizar!")
        client = httpx.AsyncClient(timeout=15.0, follow_redirects=True, verify=False)
        close_client = True
        
    try:
        catalog, index = await _get_catalog(client)
        if not catalog:
            return streams
            
        anime = _fuzzy_match(titles, catalog, index)
        if not anime:
            print(f"[Homura] Nenhum anime encontrado para {titles[0]} ({tmdb_id})")
            return streams
            
        anime_id = anime["id"]
        print(f"[Homura] Encontrou anime: {anime.get('name')} (ID: {anime_id})")
        
        # Obter episódios
        ep_url = f"{BASE_URL}/anime/episodes/{anime_id}"
        auth_token = os.getenv("HOMURA_TOKEN")
        ep_res = await client.get(ep_url, headers={"Authorization": auth_token, "User-Agent": USER_AGENT})
        episodes_list = ep_res.json()
        
        if not episodes_list:
            print(f"[Homura] Nenhum episódio encontrado para {anime.get('name')}")
            return streams
            
        target_ep_id = None
        
        if content_type == "movie":
            target_ep_id = episodes_list[0]["id"]
        else:
            ep_str = str(episode)
            ep_str_pad = f"{int(episode):02d}" if str(episode).isdigit() else str(episode)
            
            for ep in episodes_list:
                ep_name = ep.get("name", "")
                nums = re.findall(r'\d+', ep_name)
                if ep_str in nums or ep_str_pad in nums:
                    target_ep_id = ep["id"]
                    break
                    
            if not target_ep_id:
                idx = int(episode) - 1
                if 0 <= idx < len(episodes_list):
                    target_ep_id = episodes_list[idx]["id"]
                    
        if not target_ep_id:
            print(f"[Homura] Episódio {episode} não mapeado.")
            return streams
            
        # Obter o stream URL
        stream_url = f"{BASE_URL}/episode/stream/{target_ep_id}"
        st_res = await client.get(stream_url, headers={"Authorization": auth_token, "User-Agent": USER_AGENT})
        st_data = st_res.json()
        
        final_mp4 = st_data.get("stream")
        if final_mp4:
            is_dub = anime.get("dubbed", 0) == 1
            lang_label = "Dublado" if is_dub else "Legendado"
            
            partes = []
            if titles:
                partes.append(titles[0])
            if content_type == "series":
                s_pad = f"{int(season):02d}"
                e_pad = f"{int(episode):02d}"
                partes.append(f"T{s_pad} EP{e_pad}")
            
            partes.append(f"{lang_label}\nAluado")
            desc = "\n".join(partes)
            
            streams.append({
                "name": "FenixFlix",
                "description": desc,
                "url": final_mp4,
                "behaviorHints": {"notWebReady": False, "bingeGroup": f"fenixflix-homura-{anime_id}"},
                "_cache_key": "D" if is_dub else "L",
                "_label": lang_label
            })
            print(f"[Homura] Sucesso! Retornando stream {lang_label} para {titles[0]}.")
            
    except Exception as e:
        print(f"[Homura] Erro ao buscar stream para {tmdb_id}: {e}")
    finally:
        if close_client:
            await client.aclose()
            
    return streams
