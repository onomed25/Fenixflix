import httpx
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import asyncio

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

async def extrair_link(label, cache_key, target_url, client, cached_mediafire_url=None):
    mediafire_url = cached_mediafire_url

    # 1. Se o cache disser "N", significa que já sabemos que não existe. PULA TUDO!
    if mediafire_url == "N":
        print(f"[Azullog Debug] ⏭️ Cache negativo ('N') encontrado para {label} ({cache_key}). Pulando busca pesada!")
        return {"_cache_key": cache_key, "_label": label, "_mediafire_url": "N"} # Retorna 'N' e a letra 'D' ou 'L' pro app.py

    # 2. Se tem um link real do Mediafire no cache, usa ele
    elif mediafire_url:
        print(f"[Azullog Debug] ⚡ Usando cache do scrapers_status.json pro Mediafire {label} ({cache_key}): {mediafire_url}")
    
    # 3. Se não tem nada no cache, faz o scraping pesado do player
    else:
        try:
            print(f"[Azullog Debug] 🔍 Testando link direto: {target_url}")
            res = await client.get(target_url, headers={"User-Agent": USER_AGENT, "accept": "*/*"})

            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'lxml')
                iframe = soup.select_one("iframe[src*='player_2.php']")

                if iframe:
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
                            print(f"[Azullog Debug] Mediafire URL encontrada ({label})!")
        except Exception as e:
            print(f"[Azullog Debug] Erro durante a extração de {label}: {e}")

    # 4. Aborta se não conseguiu a URL base (Marca como "N" pro cache)
    if not mediafire_url:
        print(f"[Azullog Debug] ❌ Falha ao obter link base para {label}. Marcando cache como 'N'.")
        return {"_cache_key": cache_key, "_label": label, "_mediafire_url": "N"}

    # 5. Tendo o link base, entra no Mediafire e pega o botão MP4 fresco
    try:
        mf_res = await client.get(mediafire_url, headers={"User-Agent": USER_AGENT})
        mf_soup = BeautifulSoup(mf_res.text, 'lxml')
        download_btn = mf_soup.select_one("a#downloadButton")

        if download_btn:
            final_mp4 = download_btn.get("href")
            print(f"[Azullog Debug] ✅ Sucesso ({label})! Link final MP4 fresco extraído.")

            return {
                "name": "FenixFlix",
                "description": f"{label}\nON",  # O usuário continua vendo "Dublado/Legendado" no app
                "url": final_mp4,
                "behaviorHints": {"notWebReady": False, "bingeGroup": f"fenixflix-azullog-{label.lower()}"},
                "_mediafire_url": mediafire_url,
                "_cache_key": cache_key, # "D" ou "L" -> use isso no app.py para salvar no JSON
                "_label": label
            }
        else:
            print(f"[Azullog Debug] ❌ Botão MP4 final não encontrado no Mediafire ({label}). Arquivo pode ter caído. Marcando como 'N'.")
            return {"_cache_key": cache_key, "_label": label, "_mediafire_url": "N"}
            
    except Exception as e:
        print(f"[Azullog Debug] ❌ Erro ao extrair o botão MP4 para {label}: {e}. Marcando cache como 'N'.")
        return {"_cache_key": cache_key, "_label": label, "_mediafire_url": "N"}

    return None

async def search_serve(tmdb_id: str, content_type: str, season=None, episode=None, client: httpx.AsyncClient = None, cached_links=None):
    streams = []
    urls_to_check = []
    
    # Agora o cached_links que chega aqui é algo como: {"D": "link...", "L": "N"}
    if cached_links is None:
        cached_links = {}

    print(f"\n[Azullog Debug] Iniciando busca para TMDB ID: {tmdb_id} | Tipo: {content_type} | S{season}E{episode}")

    # Adicionamos a letra 'D' e 'L' nas tuplas para repassar pra função de extração
    if content_type == "movie":
        urls_to_check.append(("Dublado", "D", f"https://1take.lat/e/tmdb{tmdb_id}dub"))
        urls_to_check.append(("Legendado", "L", f"https://1take.lat/e/tmdb{tmdb_id}leg"))
    else:
        urls_to_check.append(("Dublado", "D", f"https://1take.lat/e/tvtmdb{tmdb_id}t{season}e{episode}dub"))
        urls_to_check.append(("Legendado", "L", f"https://1take.lat/e/tvtmdb{tmdb_id}t{season}e{episode}leg"))

    close_client = False
    if client is None:
        client = httpx.AsyncClient(timeout=15.0, follow_redirects=True)
        close_client = True

    try:
        # Puxa do dicionário usando a chave curta ('D' ou 'L')
        tarefas = [extrair_link(label, cache_key, target_url, client, cached_links.get(cache_key)) for label, cache_key, target_url in urls_to_check]
        resultados = await asyncio.gather(*tarefas)

        dublado_ok = False
        legendado_ok = False

        for res in resultados:
            if res:
                streams.append(res)
                
                # Verifica se deu certo mesmo (se tem 'url' e não apenas 'N')
                if res.get("url"): 
                    if res.get("_cache_key") == "D":
                        dublado_ok = True
                    elif res.get("_cache_key") == "L":
                        legendado_ok = True

        if dublado_ok and not legendado_ok:
            print(f"[Azullog Debug] É dublado, mas não tem legendado disponível pro TMDB {tmdb_id}.")
        elif legendado_ok and not dublado_ok:
            print(f"[Azullog Debug] Tem legendado, mas não achamos o dublado pro TMDB {tmdb_id}.")
        elif dublado_ok and legendado_ok:
            print(f"[Azullog Debug] Tudo certo, achei as versões dublado e legendado pro TMDB {tmdb_id}.")
        else:
            print(f"[Azullog Debug] Infelizmente nenhum link foi encontrado pro TMDB {tmdb_id}.")

    finally:
        if close_client:
            await client.aclose()

    return streams

if __name__ == "__main__":
    async def rodar_teste():
        # Exemplo simulando que o JSON já tem "D" salvo e "L" vazio
        cache_simulado = {"D": "https://www.mediafire.com/file_premium/simulacao_filme", "L": "N"}
        
        streams_filme = await search_serve("550", "movie", cached_links=cache_simulado)
        print("\nFilme Resultado Final:", streams_filme)

    asyncio.run(rodar_teste())