import requests
import json
import os
import time

CACHE_DIR = "cache"
CATALOG_CACHE_TIME = 6 * 60 * 60  

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

PROVIDERS = {
    "popular": ["nfx", "amp", "dnp", "hbm", "atp", "gla"] 
}

QUERY_CATALOG = """
query GetPopularTitles($country: Country!, $popularTitlesFilter: TitleFilter, $popularTitlesSortBy: PopularTitlesSorting! = POPULAR, $first: Int!, $language: Language!) {
  popularTitles(country: $country, filter: $popularTitlesFilter, sortBy: $popularTitlesSortBy, first: $first) {
    edges { node { content(country: $country, language: $language) {
      externalIds { imdbId }
      title
      shortDescription
      posterUrl(profile: S332, format: JPG)
      backdrops(profile: S1920, format: JPG) { backdropUrl }
    }}}
  }
}
"""

def get_cached_data(filename, duration):
    filepath = os.path.join(CACHE_DIR, filename)
    if not os.path.exists(filepath): return None
    if (time.time() - os.path.getmtime(filepath)) < duration:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: pass
    return None

def save_to_cache(filename, data):
    filepath = os.path.join(CACHE_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    except: pass

def fetch_catalog(provider_key, content_type="movie", country="BR"):
    if provider_key != "popular":
        return []

    cache_name = f"{provider_key}_{content_type}_{country}.json"
    cached = get_cached_data(cache_name, CATALOG_CACHE_TIME)
    if cached: return cached

    url = "https://apis.justwatch.com/graphql"
    
    packages = PROVIDERS.get("popular") 
    jw_type = "MOVIE" if content_type == "movie" else "SHOW"

    variables = {
        "country": country,
        "language": "pt-BR", 
        "first": 60,
        "popularTitlesSortBy": "TRENDING",
        "popularTitlesFilter": {
            "objectTypes": [jw_type],
            "packages": packages,
            "excludeIrrelevantTitles": False
        }
    }

    try:
        response = requests.post(url, json={"operationName": "GetPopularTitles", "variables": variables, "query": QUERY_CATALOG}, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        data = response.json()
        edges = data.get("data", {}).get("popularTitles", {}).get("edges", [])
        
        metas = []
        for item in edges:
            node = item.get("node", {}).get("content", {})
            imdb_id = node.get("externalIds", {}).get("imdbId")
            
            description = node.get("shortDescription")
            
            if imdb_id:
                poster = f"https://images.justwatch.com{node.get('posterUrl')}".replace("{profile}", "s332").replace("{format}", "jpg") if node.get('posterUrl') else None
                metas.append({
                    "id": imdb_id,
                    "type": content_type,
                    "name": node.get("title"),
                    "poster": poster,
                    "description": description 
                })
        
        if metas: save_to_cache(cache_name, metas)
        return metas
    except: return []