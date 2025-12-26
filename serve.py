import requests
import json
import re

def search_archive_series(imdb_id, season, episode):
    try:
        s_num = int(season)
        e_num = int(episode)
    except (ValueError, TypeError):
        return []

    season_str = f"s{s_num:02d}"
    
    archive_ids_to_try = [
        f"fenix-{imdb_id}-{season_str}-dual",
        f"fenix-{imdb_id}-{season_str}"
    ]

    for archive_id in archive_ids_to_try:
        metadata_url = f"https://archive.org/metadata/{archive_id}"
        
        try:
            response = requests.get(metadata_url, timeout=4)
            if response.status_code != 200:
                continue 

            data = response.json()
            if 'files' not in data or not data.get('server'):
                continue

            files = data['files']
            server = data['server']
            directory = data['dir']
            
            regex = rf"(?i)(?:e|x|ep|episode|\s|^)\D?0*{e_num}(?:[^\d]|$)"
            regex_simple = rf"(?i)(^|\W)0*{e_num}\.(mp4|mkv|avi)$"

            found_file = None
            for file in files:
                filename = file['name']
                if not filename.lower().endswith(('.mp4', '.mkv', '.avi')):
                    continue
                if re.search(regex, filename) or re.search(regex_simple, filename):
                    found_file = filename
                    break
            
            if found_file:
                final_url = f"https://{server}{directory}/{found_file}"
                
                label = "Dual" if "dual" in archive_id else "Leg/Orig"
                
                return [{
                    "name": "Archive",
                    "description": f"S{s_num}E{e_num} - {label}",
                    "url": final_url
                }]

        except Exception:
            continue

    return []

def search_serve(imdb_id, content_type, season=None, episode=None):
    streams_finais = []
    if content_type == 'series' and season and episode:
        try:
            archive_results = search_archive_series(imdb_id, season, episode)
            if archive_results:
                streams_finais.extend(archive_results)
        except Exception:
            pass

    return streams_finais