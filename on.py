import httpx
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import asyncio

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

async def extrair_link(label, target_url, client):
    try:
        print(f"[Azullog Debug] Testando link direto: {target_url}")
        res = await client.get(target_url, headers={"User-Agent": USER_AGENT, "accept": "*/*"})
        
        if res.status_code != 200:
            print(f"[Azullog Debug] Status {res.status_code} - Ignorando {label}.")
            return None

        soup = BeautifulSoup(res.text, 'lxml')
        
        iframe = soup.select_one("iframe[src*='player_2.php']")
        if not iframe:
            print(f"[Azullog Debug] Nenhum iframe do player_2 encontrado para {label}.")
            return None
            
        player_url = iframe.get("src")
        if player_url.startswith("//"):
            player_url = "https:" + player_url
            
        print(f"[Azullog Debug] Resolvendo player ({label}): {player_url}")
        
        res2 = await client.get(player_url, headers={"referer": target_url, "User-Agent": USER_AGENT})
        
        api_url_match = re.search(r"const apiUrl = `([^`]+)`", res2.text)
        if api_url_match:
            api_url = api_url_match.group(1)
            mediafire_enc_match = re.search(r"[?&]url=([^&]+)", api_url)
            if mediafire_enc_match:
                mediafire_url = unquote(mediafire_enc_match.group(1))
                print(f"[Azullog Debug] Mediafire URL encontrada ({label}): {mediafire_url}")
                
                mf_res = await client.get(mediafire_url, headers={"User-Agent": USER_AGENT})
                mf_soup = BeautifulSoup(mf_res.text, 'lxml')
                download_btn = mf_soup.select_one("a#downloadButton")
                
                if download_btn:
                    final_mp4 = download_btn.get("href")
                    print(f"[Azullog Debug] Sucesso ({label})! MP4 extraído.")
                    return {
                        "name": "FenixFlix",
                        "description": f"{label}\nON",
                        "url": final_mp4,
                        "behaviorHints": {"notWebReady": False, "bingeGroup": f"fenixflix-azullog-{label.lower()}"}
                    }
                else:
                    print(f"[Azullog Debug] Botão MP4 não encontrado no Mediafire ({label}).")
    except Exception as e:
        print(f"[Azullog Debug] Erro durante a extração de {label}: {e}")
    
    return None

async def search_serve(tmdb_id: str, content_type: str, season=None, episode=None, client: httpx.AsyncClient = None):
    streams = []
    urls_to_check = []

    print(f"\n[Azullog Debug] Iniciando busca inteligente para TMDB ID: {tmdb_id} | Tipo: {content_type} | S{season}E{episode}")

    if content_type == "movie":
        urls_to_check.append(("Dublado", f"https://1take.lat/e/tmdb{tmdb_id}dub"))
        urls_to_check.append(("Legendado", f"https://1take.lat/e/tmdb{tmdb_id}leg"))
    else:
        urls_to_check.append(("Dublado", f"https://1take.lat/e/tvtmdb{tmdb_id}t{season}e{episode}dub"))
        urls_to_check.append(("Legendado", f"https://1take.lat/e/tvtmdb{tmdb_id}t{season}e{episode}leg"))

    close_client = False
    if client is None:
        client = httpx.AsyncClient(timeout=15.0, follow_redirects=True)
        close_client = True

    try:
        # Dispara a busca de ambos (Dublado e Legendado) ao mesmo tempo
        tarefas = [extrair_link(label, target_url, client) for label, target_url in urls_to_check]
        resultados = await asyncio.gather(*tarefas)
        
        # Filtra e adiciona apenas os links que foram encontrados com sucesso
        streams.extend([res for res in resultados if res])

    finally:
        if close_client:
            await client.aclose()

    return streams

if __name__ == "__main__":
    async def rodar_teste():
        streams_serie = await search_serve("65493", "series", season=1, episode=2)
        print("Série:", streams_serie)
        streams_filme = await search_serve("550", "movie")
        print("Filme:", streams_filme)

    asyncio.run(rodar_teste())