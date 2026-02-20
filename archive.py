import httpx
import asyncio
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Esta é a função que vai no Archive.org. Ela será executada 3 vezes ao mesmo tempo.
async def fetch_archive_metadata(client, archive_id, is_series=False, e_num=None):
    metadata_url = f"https://archive.org/metadata/{archive_id}"
    try:
        response = await client.get(metadata_url, timeout=4.0)
        if response.status_code != 200:
            return None 

        data = response.json()
        if 'files' not in data or not data.get('server'):
            return None

        files = data['files']
        server = data['server']
        directory = data['dir']
        
        found_file = None
        
        if is_series and e_num is not None:
            regex = rf"(?i)(?:e|x|ep|episode|\s|^)(?![sS])\D?0*{e_num}(?:[^\d]|$)"
            regex_simple = rf"(?i)(^|\W)0*{e_num}\.(mp4|mkv|avi)$"

            for file in files:
                filename = file['name']
                if not filename.lower().endswith(('.mp4', '.mkv', '.avi')):
                    continue
                if re.search(regex, filename) or re.search(regex_simple, filename):
                    found_file = filename
                    break
                    
        else:
            for file in files:
                filename = file['name']
                if filename.lower().endswith(('.mp4', '.mkv', '.avi')):
                    found_file = filename
                    break
        
        if found_file:
            final_url = f"https://{server}{directory}/{found_file}"
            
            label = "Leg"
            if "nacional" in archive_id: label = "Nacional"
            elif "dual" in archive_id: label = "Dual"
            
            return {
                "name": "FenixFlix", 
                "description": f"{label}",
                "url": final_url
            }
    except:
        return None

async def search_archive_movies(imdb_id):
    archive_ids_to_try = [
        f"fenix-{imdb_id}-nacional",
        f"fenix-{imdb_id}-dual",
        f"fenix-{imdb_id}"
    ]
    
    async with httpx.AsyncClient(headers=HEADERS) as client:
        tasks = [fetch_archive_metadata(client, archive_id) for archive_id in archive_ids_to_try]
        
        results = await asyncio.gather(*tasks)
        
    return [res for res in results if res is not None]

async def search_archive_series(imdb_id, season, episode):
    try:
        s_num = int(season)
        e_num = int(episode)
    except (ValueError, TypeError):
        return []

    season_str = f"s{s_num:02d}"
    
    archive_ids_to_try = [
        f"fenix-{imdb_id}-{season_str}-nacional",
        f"fenix-{imdb_id}-{season_str}-dual",
        f"fenix-{imdb_id}-{season_str}"
    ]

    async with httpx.AsyncClient(headers=HEADERS) as client:
        tasks = [fetch_archive_metadata(client, archive_id, is_series=True, e_num=e_num) for archive_id in archive_ids_to_try]
        
        results = await asyncio.gather(*tasks)
        
    return [res for res in results if res is not None]

async def search_serve(imdb_id, content_type, season=None, episode=None):
    if content_type == 'series' and season and episode:
        return await search_archive_series(imdb_id, season, episode)
    elif content_type == 'movie':
        return await search_archive_movies(imdb_id)
    return []