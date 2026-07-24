import asyncio
import re
import orjson
import httpx
import urllib.parse
import cloudscraper
from cachetools import TTLCache

# Cache de IDs (tmdb/imdb) que já sabemos que não existem no site (retornaram 404)
# para não bombardear o site à toa. Duração: 2 horas.
_shop_404_cache = TTLCache(maxsize=500, ttl=7200)

_RE_DIV_TAG = re.compile(r'<div\s([^>]+)>', re.IGNORECASE)

def _get_attr(attrs, name):
    m = re.search(r'\b' + name + r'\s*=\s*(?:["\']([^"\']+)["\']|([^\s>]+))', attrs, re.IGNORECASE)
    if m:
        return m.group(1) if m.group(1) is not None else m.group(2)
    return None

# Headers básicos simulando um navegador
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Origin": "https://v1.watchplay.shop",
    "Referer": "https://v1.watchplay.shop/"
}

def _fetch_cf(url, method="GET", data=None):
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    if method == "GET":
        return scraper.get(url, headers=HEADERS, timeout=15.0)
    else:
        return scraper.post(url, data=data, headers=HEADERS, timeout=15.0)

async def resolve_shop(imdb_id: str = None, tmdb_id: str = None, content_type: str = None, season: int = None, episode: int = None, client: httpx.AsyncClient = None):
    """
    Busca links do provedor Shop (v1.watchplay.shop) usando Cloudscraper
    """
    base_domain = "https://v1.watchplay.shop"
    player_ids = []

    print(f"[Shop Resolver] Iniciando busca para {content_type} (IMDB: {imdb_id} / TMDB: {tmdb_id})")

    if content_type == "movie":
        if not imdb_id:
            return []
            
        if f"movie_{imdb_id}" in _shop_404_cache:
            print(f"[Shop Resolver] {imdb_id} está no cache de 404. Ignorando.")
            return []

        url = f"{base_domain}/movie/{imdb_id}"
        print(f"[Shop Resolver] Acessando {url}")
        
        try:
            resp = await asyncio.to_thread(_fetch_cf, url, "GET")
        except Exception as e:
            print(f"[Shop Resolver] Erro Cloudscraper: {e}")
            return []

        if resp.status_code == 404 or "página não encontrada" in resp.text.lower():
            _shop_404_cache[f"movie_{imdb_id}"] = True
            
        if resp.status_code != 200:
            print(f"[Shop Resolver] Erro {resp.status_code} ao acessar página do filme.")
            return []
            
        player_ids = []
        for m in _RE_DIV_TAG.finditer(resp.text):
            attrs = m.group(1)
            if 'player_select_item' in attrs:
                p_id = _get_attr(attrs, 'data-id')
                if p_id:
                    player_ids.append(p_id)

    elif content_type == "series":
        if not tmdb_id and not imdb_id:
            return []
            
        if f"series_{tmdb_id}" in _shop_404_cache or f"anime_{imdb_id}" in _shop_404_cache:
            print(f"[Shop Resolver] TMDB {tmdb_id} ou IMDB {imdb_id} no cache de 404. Ignorando.")
            return []
            
        url_tv = f"{base_domain}/tvshow/{tmdb_id}"
        url_anime = f"{base_domain}/anime/{imdb_id}"
        
        print(f"[Shop Resolver] Acessando {url_tv}")
        try:
            resp = await asyncio.to_thread(_fetch_cf, url_tv, "GET")
        except Exception:
            resp = None
            
        if not resp or resp.status_code == 404 or "página não encontrada" in resp.text.lower():
            print(f"[Shop Resolver] Acessando {url_anime}")
            try:
                resp = await asyncio.to_thread(_fetch_cf, url_anime, "GET")
            except Exception:
                resp = None
            
        if not resp or resp.status_code == 404 or "página não encontrada" in resp.text.lower():
            _shop_404_cache[f"series_{tmdb_id}"] = True
            _shop_404_cache[f"anime_{imdb_id}"] = True
            
        if not resp or resp.status_code != 200:
            print(f"[Shop Resolver] Erro ao acessar página da série/anime.")
            return []
            
        contentid = None
        season_str = str(season)
        episode_str = str(episode)
        
        for m in _RE_DIV_TAG.finditer(resp.text):
            attrs = m.group(1)
            if 'episodeOption' in attrs:
                s = _get_attr(attrs, 'data-season')
                e = _get_attr(attrs, 'data-episode')
                if s == season_str and e == episode_str:
                    contentid = _get_attr(attrs, 'data-contentid')
                    if contentid:
                        break
        
        if not contentid:
            print(f"[Shop Resolver] Episódio S{season}E{episode} não encontrado na página.")
            return []
            
        print(f"[Shop Resolver] Obtendo opções para contentid={contentid}")
        try:
            resp_opts = await asyncio.to_thread(_fetch_cf, f"{base_domain}/api", "POST", {"action": "getOptions", "contentid": contentid})
            opts_json = orjson.loads(resp_opts.content)
            options = opts_json.get("data", {}).get("options", [])
            player_ids = [str(opt.get("ID")) for opt in options if opt.get("ID")]
        except Exception as e:
            print(f"[Shop Resolver] Erro ao parsear JSON de opções: {e}")
            return []

    if not player_ids:
        print("[Shop Resolver] Nenhum player_id encontrado.")
        return []

    print(f"[Shop Resolver] Encontrados {len(player_ids)} players: {player_ids}")
    
    streams = []
    
    for pid in player_ids:
        try:
            print(f"[Shop Resolver] Solicitando link final para video_id={pid}")
            resp_player = await asyncio.to_thread(_fetch_cf, f"{base_domain}/api", "POST", {"action": "getPlayer", "video_id": pid})
            player_json = orjson.loads(resp_player.content)
            
            video_url = player_json.get("data", {}).get("video_url")
            
            if video_url:
                print(f"[Shop Resolver] Sucesso: {video_url}")
                resolution = "HD"
                if ".m3u8" in video_url:
                    resolution = "HLS"
                elif ".mp4" in video_url:
                    resolution = "MP4"
                    
                streams.append({
                    "name": "FenixFlix",
                    "title": f"{resolution}\nMoody",
                    "url": video_url,
                    "behaviorHints": {
                        "notWebReady": False, 
                        "bingeGroup": "fenixflix-shop",
                        "proxyHeaders": {
                            "request": {
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                "Referer": "https://v1.watchplay.shop/",
                                "Origin": "https://v1.watchplay.shop"
                            }
                        }
                    }
                })
        except Exception as e:
            print(f"[Shop Resolver] Erro ao obter player {pid}: {e}")

    return streams
