import requests
import json
import re


session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
})

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
          
            response = session.get(metadata_url, timeout=4)
            if response.status_code != 200:
                continue 

            data = response.json()
            if 'files' not in data or not data.get('server'):
                continue

            files = data['files']
            server = data['server']
            directory = data['dir']
            
            # CORREÇÃO: Adicionado (?![sS]) para impedir que capture 'S' (de Season) como episódio
            regex = rf"(?i)(?:e|x|ep|episode|\s|^)(?![sS])\D?0*{e_num}(?:[^\d]|$)"
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
                
                label = "Dual" if "dual" in archive_id else "Leg"
                
                return [{
                    "name": "FenixFlix ", 
                    "description": f"{label}", # Corrigido de 'Aechive' para 'Archive'
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
