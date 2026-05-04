import re
import unicodedata
import time
import asyncio
import httpx

CDN_PROXY = 'https://ondemand.mylifekorea.shop'

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://www.doramogo.net/'
}

def title_to_slug(title: str) -> str:
    if not title:
        return ''
    title = title.lower()
    title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore').decode('utf-8')
    title = re.sub(r'[^a-z0-9]+', '-', title)
    return title.strip('-')

async def test_url(client: httpx.AsyncClient, url: str) -> bool:
    print(f"[DEBUG - Doramogo] A testar URL: {url}")
    try:
        response = await client.head(url, headers=HEADERS)
        if response.status_code in (200, 206):
            print(f"[DEBUG - Doramogo] Sucesso (Status {response.status_code}): {url}")
            return True
        else:
            print(f"[DEBUG - Doramogo] Falhou (Status {response.status_code}): {url}")
            return False
    except Exception as e:
        print(f"[DEBUG - Doramogo] Erro de ligação ao testar URL: {e}")
        return False

def generate_slug_variations(base_title: str, season: int):
    base_slug = title_to_slug(base_title)
    variations = []
    seen = set()

    def add(slug):
        if slug not in seen:
            seen.add(slug)
            variations.append(slug)

    words = base_slug.split('-')

    add(base_slug)
    add(f"{base_slug}-legendado")
    add(f"{base_slug}-dublado")

    if season > 1:
        add(f"{base_slug}-{season}")

    if len(words) > 3:
        for i in range(3, len(words)):
            reduced = '-'.join(words[:i])
            add(reduced)
            if season > 1:
                add(f"{reduced}-{season}")

    return variations

async def search_serve(tmdb_id, titles, media_type, season, episode, client: httpx.AsyncClient):
    print(f"[DEBUG - Doramogo] A iniciar pesquisa - ID: {tmdb_id}, Tipo: {media_type}, S: {season}, E: {episode}")
    target_season = 1 if media_type == 'movie' else (season or 1)
    target_episode = 1 if media_type == 'movie' else (episode or 1)
    ep_padded = f"{target_episode:02d}"
    season_padded = f"{target_season:02d}"
    timestamp = int(time.time() * 1000)

    if not titles:
        print("[DEBUG - Doramogo] Nenhum título fornecido pelo app.py, pesquisa cancelada.")
        return []

    todas_variacoes = []
    for title in titles:
        todas_variacoes.extend(generate_slug_variations(title, target_season))

    slug_variations = list(dict.fromkeys(todas_variacoes))
    print(f"[DEBUG - Doramogo] Total de variações de slug geradas: {len(slug_variations)}")

    streams = []

    async def test_and_return(slug):
        first_letter = slug[0].upper() if slug else 'T'

        if media_type == 'movie':
            stream_url = f"{CDN_PROXY}/{first_letter}/{slug}/stream/stream.m3u8?nocache={timestamp}"
        else:
            stream_url = f"{CDN_PROXY}/{first_letter}/{slug}/{season_padded}-temporada/{ep_padded}/stream.m3u8?nocache={timestamp}"

        if await test_url(client, stream_url):
            print(f"[DEBUG - Doramogo] Fluxo final encontrado e adicionado com sucesso! URL: {stream_url}")
            return {
                "url": stream_url,
                "name": 'FenixFlix\n1080p',
                "title": titles[0] if media_type == 'movie' else f"Dublado\ndoramogo",
                "type": "hls",
                "behaviorHints": {
                    "bingeGroup": "doramogo",
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "Referer": "https://www.doramogo.net/",
                            "Origin": "https://www.doramogo.net",
                            "User-Agent": "Mozilla/5.0"
                        }
                    }
                }
            }
        return None

    tasks = [asyncio.create_task(test_and_return(slug)) for slug in slug_variations]

    for task_result in asyncio.as_completed(tasks):
        try:
            resultado = await task_result
            if resultado:
                streams.append(resultado)

                for t in tasks:
                    if not t.done():
                        t.cancel()

                break
        except Exception as e:
            print(f"[DEBUG - Doramogo] Erro ao aguardar tarefa: {e}")

    if not streams:
        print("[DEBUG - Doramogo] Nenhum fluxo encontrado para as variações testadas.")

    return streams

if __name__ == "__main__":
    async def testar_doramogo():
        async with httpx.AsyncClient(verify=False) as client:
            resultados = await search_serve("93405", ["Squid Game", "Round 6"], "series", 1, 1, client)

    asyncio.run(testar_doramogo())
