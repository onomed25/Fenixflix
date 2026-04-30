# mywallpaper.py
import re
import unicodedata
import asyncio
from datetime import datetime, timezone
import httpx

TMDB_API_KEY = 'b64d2f3a4212a99d64a7d4485faed7b3'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
CDN_BASE = 'https://cdn-s01.mywallpaper-4k-image.net'

def title_to_slug(title: str) -> str:
    if not title: return ''
    title = title.lower()
    title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore').decode('utf-8')
    title = re.sub(r'[^a-z0-9]+', '-', title)
    return title.strip('-')

async def test_url(client: httpx.AsyncClient, url: str) -> bool:
    print(f"[DEBUG - MyWallpaper] Se testează URL-ul: {url}")
    try:
        response = await client.head(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code in (200, 206):
            print(f"[DEBUG - MyWallpaper] URL valid (Status {response.status_code}): {url}")
            return True
        return False
    except Exception as e:
        print(f"[DEBUG - MyWallpaper] Eroare la verificarea URL-ului: {e}")
        return False

async def get_tmdb_episode_date(client: httpx.AsyncClient, tmdb_id, season, episode):
    url = f"{TMDB_BASE_URL}/tv/{tmdb_id}/season/{season}/episode/{episode}?api_key={TMDB_API_KEY}"
    try:
        response = await client.get(url)
        if response.status_code != 200: return None
        data = response.json()
        if data.get('air_date'):
            dt = datetime.strptime(data['air_date'], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return dt.timestamp() * 1000
    except Exception:
        return None
    return None

async def get_tmdb_title(client: httpx.AsyncClient, tmdb_id):
    url = f"{TMDB_BASE_URL}/tv/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json().get('name')
    except Exception:
        pass
    return None

async def get_tmdb_seasons_info(client: httpx.AsyncClient, tmdb_id):
    url = f"{TMDB_BASE_URL}/tv/{tmdb_id}?api_key={TMDB_API_KEY}&append_to_response=seasons"
    try:
        response = await client.get(url, headers={'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0'})
        if response.status_code != 200: return None
        data = response.json()
        
        seasons = data.get('seasons', [])
        seasons_info = []
        total_episodes_before = 0
        
        seasons.sort(key=lambda x: x.get('season_number', 0))
        
        for season in seasons:
            if season.get('season_number', 0) > 0:
                seasons_info.append({
                    'seasonNumber': season['season_number'],
                    'episodeCount': season.get('episode_count', 0),
                    'totalBefore': total_episodes_before
                })
                total_episodes_before += season.get('episode_count', 0)
        return seasons_info
    except Exception:
        return None

def calculate_absolute_episode(seasons_info, target_season, target_episode):
    if not seasons_info: return None
    season_info = next((s for s in seasons_info if s['seasonNumber'] == target_season), None)
    if not season_info: return None
    return season_info['totalBefore'] + target_episode

async def get_anime_details(client: httpx.AsyncClient, anime_id):
    print(f"[DEBUG - MyWallpaper] Interogare AniList GraphQL pentru ID: {anime_id}")
    query = """
        query ($id: Int) {
            Media(id: $id) {
                id
                title { romaji english }
                startDate { year month day }
                episodes
                relations {
                    edges {
                        node {
                            id
                            title { romaji english }
                            startDate { year month day }
                            episodes
                        }
                        relationType
                    }
                }
            }
        }
    """
    try:
        response = await client.post('https://graphql.anilist.co', json={'query': query, 'variables': {'id': anime_id}})
        if response.status_code == 200:
            return response.json().get('data', {}).get('Media')
        else:
            print(f"[DEBUG - MyWallpaper] Eroare AniList (Status {response.status_code})")
    except Exception as e:
        print(f"[DEBUG - MyWallpaper] Excepție AniList: {e}")
    return None

def date_to_timestamp(date_obj):
    if not date_obj or not date_obj.get('year'): return None
    try:
        dt = datetime(date_obj['year'], date_obj.get('month') or 1, date_obj.get('day') or 1, tzinfo=timezone.utc)
        return dt.timestamp() * 1000
    except ValueError:
        return None

async def search_anilist_id(client: httpx.AsyncClient, title):
    print(f"[DEBUG - MyWallpaper] Căutare ID AniList pentru titlul: {title}")
    query = """
        query ($search: String) {
            Media(search: $search, type: ANIME) { id }
        }
    """
    try:
        response = await client.post('https://graphql.anilist.co', json={'query': query, 'variables': {'search': title}})
        if response.status_code == 200:
            anime_id = response.json().get('data', {}).get('Media', {}).get('id')
            print(f"[DEBUG - MyWallpaper] AniList ID găsit: {anime_id}")
            return anime_id
    except Exception:
        pass
    return None

def filter_invalid_seasons(seasons):
    if len(seasons) <= 2: return seasons
    filtered = []
    for i, season in enumerate(seasons):
        is_last_season = i == len(seasons) - 1
        if season.get('episodes', 0) <= 1:
            if i > 0 and not is_last_season:
                prev_season = seasons[i - 1]
                next_season = seasons[i + 1]
                if prev_season.get('episodes', 0) > 1 and next_season.get('episodes', 0) > 1:
                    continue
        filtered.append(season)
    return filtered

async def get_all_seasons(client: httpx.AsyncClient, start_id):
    all_seasons = []
    visited = set()

    async def follow_chain(anime_id, season_num):
        if anime_id in visited: return
        visited.add(anime_id)
        await asyncio.sleep(1)

        anime = await get_anime_details(client, anime_id)
        if not anime: return

        title = anime.get('title', {}).get('romaji') or anime.get('title', {}).get('english')
        all_seasons.append({
            'id': anime_id,
            'title': title,
            'date': date_to_timestamp(anime.get('startDate')),
            'season': season_num,
            'episodes': anime.get('episodes') or 0
        })

        edges = anime.get('relations', {}).get('edges', [])
        for edge in edges:
            if edge.get('relationType') == 'SEQUEL':
                await follow_chain(edge['node']['id'], season_num + 1)
                break

    await follow_chain(start_id, 1)
    all_seasons.sort(key=lambda x: x.get('date') or 0)
    
    for i, season in enumerate(all_seasons):
        season['season'] = i + 1

    filtered_seasons = filter_invalid_seasons(all_seasons)
    for i, season in enumerate(filtered_seasons):
        season['season'] = i + 1

    return filtered_seasons

def find_season_by_date(seasons, target_date):
    closest = None
    min_diff = float('inf')
    for s in seasons:
        if not s.get('date'): continue
        diff = abs(target_date - s['date'])
        days = diff / (1000 * 60 * 60 * 24)
        if days < 180 and diff < min_diff:
            min_diff = diff
            closest = s
    return closest

def analyze_parts(seasons, target_episode, episode_date):
    closest = find_season_by_date(seasons, episode_date)
    if not closest: return None

    groups = {}
    for s in seasons:
        base = re.sub(r'[:\s]*(?:Part|Parte)\s*\d+$', '', s['title'], flags=re.IGNORECASE)
        base = re.sub(r'\s+\d+$', '', base)
        base = re.sub(r'[:\s]*(?:Season|Cour)\s*\d+$', '', base).strip()
        if len(base) < 3: base = s['title']
        
        if base not in groups: groups[base] = []
        groups[base].append(s)

    for base in groups:
        groups[base].sort(key=lambda x: x.get('date') or 0)

    for base, group in groups.items():
        index = next((i for i, s in enumerate(group) if s['id'] == closest['id']), -1)
        if index != -1:
            has_multiple_parts = len(group) > 1
            part_number = index + 1
            episodes_before = sum(group[k]['episodes'] for k in range(index))
            episode_in_part = target_episode - episodes_before

            return {
                'id': closest['id'],
                'title': closest['title'],
                'date': closest['date'],
                'season': closest['season'],
                'episodes': closest['episodes'],
                'baseTitle': base,
                'partNumber': part_number,
                'totalParts': len(group),
                'hasMultipleParts': has_multiple_parts,
                'episodesBefore': episodes_before,
                'episodeInPart': episode_in_part
            }

    return {
        'id': closest['id'],
        'title': closest['title'],
        'date': closest['date'],
        'season': closest['season'],
        'episodes': closest['episodes'],
        'baseTitle': closest['title'],
        'partNumber': 1,
        'totalParts': 1,
        'hasMultipleParts': False,
        'episodesBefore': 0,
        'episodeInPart': target_episode
    }

def generate_minimal_slugs(season_info, target_season):
    slugs = []
    base_title = season_info.get('baseTitle') or re.sub(r'[:\s]*(?:Part|Parte)?\s*\d+', '', season_info['title'], flags=re.IGNORECASE).strip()
    base_slug = title_to_slug(base_title)
    
    if season_info.get('hasMultipleParts'):
        if season_info['partNumber'] == 1:
            slugs.append(base_slug)
        else:
            slugs.append(f"{base_slug}-{season_info['partNumber']}")
    else:
        slugs.append(base_slug)
        
    if target_season > 1:
        slugs.append(f"{base_slug}-{target_season}")
        
    return list(dict.fromkeys(slugs))

async def get_anilist_titles(client: httpx.AsyncClient, tmdb_id, media_type):
    endpoint = 'tv' if media_type == 'series' else 'movie'
    tmdb_url = f"{TMDB_BASE_URL}/{endpoint}/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"

    try:
        response = await client.get(tmdb_url)
        if response.status_code != 200: return []
        tmdb_data = response.json()
        search_title = tmdb_data.get('name') if media_type == 'series' else tmdb_data.get('title')

        query = """
            query ($search: String) {
                Media(search: $search, type: ANIME) {
                    title { romaji english }
                    synonyms
                }
            }
        """
        anilist_resp = await client.post('https://graphql.anilist.co', json={'query': query, 'variables': {'search': search_title}})
        if anilist_resp.status_code != 200: return []
        
        media = anilist_resp.json().get('data', {}).get('Media', {})
        titles = []

        if media.get('title', {}).get('romaji'):
            titles.append({'name': media['title']['romaji'], 'type': 'romaji'})
        if media.get('title', {}).get('english') and media['title']['english'] != media['title']['romaji']:
            titles.append({'name': media['title']['english'], 'type': 'english'})
        if media.get('synonyms'):
            for syn in media['synonyms']:
                if not any(t['name'].lower() == syn.lower() for t in titles):
                    titles.append({'name': syn, 'type': 'synonym'})
        
        print(f"[DEBUG - MyWallpaper] Titluri AniList găsite: {titles}")
        return titles
    except Exception as e:
        print(f"[DEBUG - MyWallpaper] Eroare la obținerea titlurilor AniList: {e}")
        return []

def generate_slug_variations(base_title, season):
    base_slug = title_to_slug(base_title)
    variations = []
    seen = set()

    def add(slug):
        if slug not in seen:
            seen.add(slug)
            variations.append(slug)

    words = base_slug.split('-')

    if season == 1:
        add(base_slug)
    else:
        add(f"{base_slug}-{season}")

    if len(words) > 3:
        for i in range(3, len(words)):
            reduced_base = '-'.join(words[:i])
            if season == 1:
                add(reduced_base)
            else:
                add(f"{reduced_base}-{season}")

    return variations

async def search_serve(tmdb_id, media_type, season, episode, client: httpx.AsyncClient):
    print(f"[DEBUG - MyWallpaper] Pornire căutare - ID: {tmdb_id}, Tip: {media_type}, S: {season}, E: {episode}")
    target_season = 1 if media_type == 'movie' else (season or 1)
    target_episode = 1 if media_type == 'movie' else (episode or 1)
    ep_padded = f"{target_episode:02d}"

    try:
        valid_streams = []
        titles = await get_anilist_titles(client, tmdb_id, media_type)

        if titles:
            stream_map = {}
            for title_info in titles:
                if title_info['type'] not in ('romaji', 'english'): continue
                slug_variations = generate_slug_variations(title_info['name'], target_season)

                for slug in slug_variations:
                    first_letter = slug[0] if slug else 't'
                    key = f"{title_info['name']} ({title_info['type']})"

                    if key not in stream_map: stream_map[key] = []
                    
                    stream_map[key].append({
                        'url': f"{CDN_BASE}/stream/{first_letter}/{slug}/{ep_padded}.mp4/index.m3u8",
                        'type': 'leg',
                        'titleKey': title_info['name']
                    })
                    stream_map[key].append({
                        'url': f"{CDN_BASE}/stream/{first_letter}/{slug}-dublado/{ep_padded}.mp4/index.m3u8",
                        'type': 'dub',
                        'titleKey': title_info['name']
                    })

            all_urls = [item for sublist in stream_map.values() for item in sublist]
            print(f"[DEBUG - MyWallpaper] Au fost pregătite {len(all_urls)} adrese URL pentru testare simultană.")

            async def validate_url(item):
                if await test_url(client, item['url']):
                    original_title = ''
                    for k, v in stream_map.items():
                        if any(u['url'] == item['url'] for u in v):
                            original_title = k.split(' (')[0]
                            break
                    print(f"[DEBUG - MyWallpaper] Flux valid găsit în prima fază: {item['url']}")
                    return {
                        "url": item['url'],
                        "name": f"FenixFlix\n1080p",
                        "title": f"{'Dublado' if item['type'] == 'dub' else 'Legendado'}\nMy",
                        "behaviorHints": {"bingeGroup": "mywallpaper"}
                    }
                return None

            results = await asyncio.gather(*(validate_url(item) for item in all_urls))
            valid_streams.extend([res for res in results if res])

        if not valid_streams:
            print("[DEBUG - MyWallpaper] Începerea căutării pe baza episoadelor absolute (Faza 2)")
            seasons_info = await get_tmdb_seasons_info(client, tmdb_id)
            if seasons_info:
                absolute_episode = calculate_absolute_episode(seasons_info, target_season, target_episode)
                if absolute_episode:
                    abs_ep_padded = f"{absolute_episode:02d}"
                    anime_title = await get_tmdb_title(client, tmdb_id)
                    
                    if anime_title:
                        base_slug = title_to_slug(anime_title)
                        absolute_slugs = [base_slug]
                        
                        words = base_slug.split('-')
                        if len(words) > 3:
                            for i in range(3, len(words)):
                                absolute_slugs.append('-'.join(words[:i]))
                        
                        unique_slugs = list(dict.fromkeys(absolute_slugs))

                        for slug in unique_slugs:
                            first_letter = slug[0] if slug else 't'

                            leg_url = f"{CDN_BASE}/stream/{first_letter}/{slug}/{abs_ep_padded}.mp4/index.m3u8"
                            if await test_url(client, leg_url):
                                print(f"[DEBUG - MyWallpaper] Flux valid găsit (episod absolut leg): {leg_url}")
                                valid_streams.append({
                                    "url": leg_url,
                                    "name": "My Wallpaper Legendado 1080p",
                                    "title": f"{anime_title} EP{absolute_episode}",
                                    "behaviorHints": {"bingeGroup": "mywallpaper"}
                                })

                            dub_url = f"{CDN_BASE}/stream/{first_letter}/{slug}-dublado/{abs_ep_padded}.mp4/index.m3u8"
                            if await test_url(client, dub_url):
                                print(f"[DEBUG - MyWallpaper] Flux valid găsit (episod absolut dub): {dub_url}")
                                valid_streams.append({
                                    "url": dub_url,
                                    "name": "My Wallpaper Dublado 1080p",
                                    "title": f"{anime_title} EP{absolute_episode}",
                                    "behaviorHints": {"bingeGroup": "mywallpaper"}
                                })

        if not valid_streams:
            print("[DEBUG - MyWallpaper] Începerea căutării pe baza datei de difuzare (Faza 3)")
            episode_date = await get_tmdb_episode_date(client, tmdb_id, target_season, target_episode)
            if episode_date:
                anime_title = await get_tmdb_title(client, tmdb_id)
                if anime_title:
                    anilist_id = await search_anilist_id(client, anime_title)
                    if anilist_id:
                        all_seasons = await get_all_seasons(client, anilist_id)
                        if all_seasons:
                            season_info = analyze_parts(all_seasons, target_episode, episode_date)
                            if season_info:
                                slugs = generate_minimal_slugs(season_info, target_season)
                                test_episode = season_info.get('episodeInPart', target_episode)
                                test_ep_padded = f"{test_episode:02d}"

                                for slug in slugs:
                                    first_letter = slug[0] if slug else 't'

                                    leg_url = f"{CDN_BASE}/stream/{first_letter}/{slug}/{test_ep_padded}.mp4/index.m3u8"
                                    if await test_url(client, leg_url):
                                        print(f"[DEBUG - MyWallpaper] Flux găsit pe baza datei (leg): {leg_url}")
                                        valid_streams.append({
                                            "url": leg_url,
                                            "name": "FenixFlix",
                                            "title": "Legendado\n1080p",
                                            "behaviorHints": {"bingeGroup": "mywallpaper"}
                                        })

                                    dub_url = f"{CDN_BASE}/stream/{first_letter}/{slug}-dublado/{test_ep_padded}.mp4/index.m3u8"
                                    if await test_url(client, dub_url):
                                        print(f"[DEBUG - MyWallpaper] Flux găsit pe baza datei (dub): {dub_url}")
                                        valid_streams.append({
                                            "url": dub_url,
                                            "name": "FenixFlix",
                                            "title": "Dublado\n1080p",
                                            "behaviorHints": {"bingeGroup": "mywallpaper"}
                                        })

        print(f"[DEBUG - MyWallpaper] Proces finalizat. Total fluxuri valide returnate: {len(valid_streams)}")
        return valid_streams
    except Exception as e:
        print(f"[DEBUG - MyWallpaper] Eroare majoră în timpul căutării MyWallpaper: {e}")
        return []

# --- BLOCO DE TESTES ---
if __name__ == "__main__":
    async def testar_mywallpaper():
        print("=== Teste Isolado: MYWALLPAPER ===")
        async with httpx.AsyncClient(verify=False) as client:
            resultados = await search_serve("85937", "series", 1, 1, client)
            print("\nResultados Encontrados:", resultados)

    asyncio.run(testar_mywallpaper())