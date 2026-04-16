import httpx
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import asyncio

async def search_serve(tmdb_id: str, content_type: str, season=None, episode=None):
    streams = []

    print(f"\n[Azullog Debug] Iniciando busca para TMDB ID: {tmdb_id} | Tipo: {content_type} | S{season}E{episode}")

    # Este else foi mantido pois define a URL corretamente
    if content_type == "movie":
        url = f"https://azullog.site/filme/{tmdb_id}"
    else:
        url = f"https://azullog.site/serie/{tmdb_id}/{season}/{episode}"

    print(f"[Azullog Debug] URL alvo: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "accept": "*/*"
    }

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        try:
            res = await client.get(url, headers=headers)

            if res.status_code != 200:
                print("[Azullog Debug] Falha ao aceder à página. Abortando extração.")
                return streams

            soup = BeautifulSoup(res.text, 'html.parser')
            select_items = soup.select("div.player_select_item")

            if not select_items:
                iframe = soup.select_one("iframe")
                if iframe and iframe.get("src"):
                    src = iframe.get("src")
                    final_url = "https:" + src if src.startswith("//") else src
                    streams.append({"name": "FenixFlix", "description": "Player Direto\nAzullog", "url": final_url, "behaviorHints": {"notWebReady": False}})
                
                return streams

            for item in select_items:
                data_embed = item.get("data-embed")
                name_el = item.select_one("div.player_select_name")
                label = name_el.text.strip() if name_el else "Player"

                if not data_embed:
                    continue

                if "filecdn" in data_embed:
                    data_embed = re.sub(r"filecdn\d*\.site", "1take.lat", data_embed)

                try:
                    print(f"[Azullog Debug] Acessando link do embed...")
                    res2 = await client.get(data_embed, headers={"referer": url, "User-Agent": headers["User-Agent"]})
                    soup2 = BeautifulSoup(res2.text, 'html.parser')

                    iframe = soup2.select_one("iframe[src*='player_2.php']")
                    if iframe:
                        player_url = iframe.get("src")
                        if player_url.startswith("//"):
                            player_url = "https:" + player_url

                        res3 = await client.get(player_url, headers={"referer": data_embed, "User-Agent": headers["User-Agent"]})
                        api_url_match = re.search(r"const apiUrl = `([^`]+)`", res3.text)

                        if api_url_match:
                            api_url = api_url_match.group(1)
                            mediafire_enc_match = re.search(r"[?&]url=([^&]+)", api_url)

                            if mediafire_enc_match:
                                mediafire_url = unquote(mediafire_enc_match.group(1))

                                mf_res = await client.get(mediafire_url, headers={"Referer": player_url, "User-Agent": headers["User-Agent"]})
                                mf_soup = BeautifulSoup(mf_res.text, 'html.parser')
                                download_btn = mf_soup.select_one("a#downloadButton")

                                if download_btn:
                                    final_mf_link = download_btn.get("href")
                                    streams.append({
                                        "name": "FenixFlix",
                                        "description": f"{label}\nON",
                                        "url": final_mf_link,
                                        "behaviorHints": {"notWebReady": False, "bingeGroup": "fenixflix-azullog"}
                                    })
                                    continue

                    print("[Azullog Debug] Tentando extrair um iframe genérico do embed...")
                    any_iframe = soup2.select_one("iframe")
                    print("[Azullog Debug] Nenhum iframe de vídeo encontrado neste player.")

                except Exception as inner_e:
                    continue

        except Exception as e:
            print(f"[Azullog Debug] Erro global na execução do scraper: {e}")

    return streams