import re
import unicodedata
import time
import asyncio
import httpx

TMDB_API_KEY = 'b64d2f3a4212a99d64a7d4485faed7b3'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
CDN_PROXY = 'https://ondemand.mylifekorea.shop'

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://www.doramogo.net/'
}

CACHE = {}

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

async def get_tmdb_title(client: httpx.AsyncClient, tmdb_id: str, media_type: str):
    cache_key = f"{tmdb_id}_{media_type}"
    if cache_key in CACHE:
        print(f"[DEBUG - Doramogo] A usar cache para TMDB ID: {tmdb_id}")
        return CACHE[cache_key]

    endpoint = 'tv' if media_type == 'series' else 'movie'
    url = f"{TMDB_BASE_URL}/{endpoint}/{tmdb_id}?api_key={TMDB_API_KEY}&language=pt-BR"

    print(f"[DEBUG - Doramogo] A consultar TMDB API: {url}")
    try:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            title = data.get('name') if endpoint == 'tv' else data.get('title')

            ano = None
            if endpoint == 'tv' and data.get('first_air_date'):
                ano = data['first_air_date'][:4]
            elif endpoint == 'movie' and data.get('release_date'):
                ano = data['release_date'][:4]

            result = {'title': title, 'ano': ano}
            CACHE[cache_key] = result
            print(f"[DEBUG - Doramogo] Informações encontradas - Título: {title}, Ano: {ano}")
            return result
        else:
            print(f"[DEBUG - Doramogo] Erro TMDB API (Status {response.status_code})")
    except Exception as e:
        print(f"[DEBUG - Doramogo] Exceção ao consultar TMDB: {e}")
    return None

def generate_slug_variations(base_title: str, season: int, ano: str):
    base_slug = title_to_slug(base_title)
    variations = []
    seen = set()

    def add(slug):
        if slug not in seen:
            seen.add(slug)
            variations.append(slug)

    words = base_slug.split('-')

    add(base_slug)
    if ano:
        add(f"{base_slug}-{ano}")
    add(f"{base_slug}-legendado")
    add(f"{base_slug}-dublado")

    if ano:
        add(f"{base_slug}-{ano}-legendado")
        add(f"{base_slug}-{ano}-dublado")

    if season > 1:
        add(f"{base_slug}-{season}")
        if ano:
            add(f"{base_slug}-{ano}-{season}")

    if len(words) > 3:
        for i in range(3, len(words)):
            reduced = '-'.join(words[:i])
            add(reduced)
            if ano:
                add(f"{reduced}-{ano}")
            if season > 1:
                add(f"{reduced}-{season}")

    print(f"[DEBUG - Doramogo] Variações de slug geradas: {variations}")
    return variations

async def search_serve(tmdb_id, media_type, season, episode, client: httpx.AsyncClient):
    print(f"[DEBUG - Doramogo] A iniciar pesquisa - ID: {tmdb_id}, Tipo: {media_type}, S: {season}, E: {episode}")
    target_season = 1 if media_type == 'movie' else (season or 1)
    target_episode = 1 if media_type == 'movie' else (episode or 1)
    ep_padded = f"{target_episode:02d}"
    season_padded = f"{target_season:02d}"
    timestamp = int(time.time() * 1000)

    info = await get_tmdb_title(client, tmdb_id, media_type)
    if not info:
        print("[DEBUG - Doramogo] Não foi possível obter as informações do TMDB, pesquisa cancelada.")
        return []

    title = info.get('title')
    ano = info.get('ano')

    slug_variations = generate_slug_variations(title, target_season, ano)
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
                "title": title if media_type == 'movie' else f"Dublado\ndoramogo",
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

# --- FUNÇÃO DE TESTE ISOLADA ---
async def testar_doramogo():
    # O cliente (client) é aberto aqui e passado para a função que precisa dele
    async with httpx.AsyncClient(verify=False) as client:
        print("\n--- Iniciando teste manual do script ---")
        # Exemplo: Testando com Game of Thrones (ID: 1399), série, temporada 1, ep 1
        resultado = await search_serve('1399', 'series', 1, 1, client)
        print("\n--- Resultado Final ---")
        print(resultado)

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    # O asyncio.run roda a função de teste assíncrona
    asyncio.run(testar_doramogo())
