import httpx
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import asyncio

async def search_serve(tmdb_id: str, content_type: str, season=None, episode=None):
    streams = []

    print(f"\n[Azullog Debug] Iniciando busca para TMDB ID: {tmdb_id} | Tipo: {content_type} | S{season}E{episode}")

    # Monta a URL do Azullog usando o TMDB ID
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
            print(f"[Azullog Debug] A fazer requisição à página principal...")
            res = await client.get(url, headers=headers)
            print(f"[Azullog Debug] Status HTTP da página principal: {res.status_code}")

            if res.status_code != 200:
                print("[Azullog Debug] Falha ao aceder à página. Abortando extração.")
                return streams

            soup = BeautifulSoup(res.text, 'html.parser')
            select_items = soup.select("div.player_select_item")
            print(f"[Azullog Debug] Encontrados {len(select_items)} players na lista 'player_select_item'.")

            # Fallback caso não tenha a lista de players, mas apenas um iframe na página principal
            if not select_items:
                print("[Azullog Debug] Nenhum player encontrado na lista. Tentando fallback para iframe único...")
                iframe = soup.select_one("iframe")
                if iframe and iframe.get("src"):
                    src = iframe.get("src")
                    final_url = "https:" + src if src.startswith("//") else src
                    print(f"[Azullog Debug] Fallback iframe encontrado: {final_url}")
                    streams.append({"name": "Azullog", "title": "Player Direto", "url": final_url})
                else:
                    print("[Azullog Debug] Nenhum iframe de fallback encontrado.")
                return streams

            # Iterar pelos players disponíveis (Ex: Dublado, Legendado)
            for item in select_items:
                data_embed = item.get("data-embed")
                name_el = item.select_one("div.player_select_name")
                label = name_el.text.strip() if name_el else "Player"

                print(f"\n[Azullog Debug] -> Processando player: '{label}'")
                print(f"[Azullog Debug] Embed original: {data_embed}")

                if not data_embed:
                    print("[Azullog Debug] Sem data-embed. A ignorar...")
                    continue

                # Regra antiga: converter filecdn para 1take
                if "filecdn" in data_embed:
                    data_embed = re.sub(r"filecdn\d*\.site", "1take.lat", data_embed)
                    print(f"[Azullog Debug] Substituído filecdn por 1take: {data_embed}")

                try:
                    print(f"[Azullog Debug] Acessando link do embed...")
                    res2 = await client.get(data_embed, headers={"referer": url, "User-Agent": headers["User-Agent"]})
                    soup2 = BeautifulSoup(res2.text, 'html.parser')

                    # Procura o iframe do player_2.php que contém a API
                    iframe = soup2.select_one("iframe[src*='player_2.php']")
                    if iframe:
                        player_url = iframe.get("src")
                        if player_url.startswith("//"):
                            player_url = "https:" + player_url

                        print(f"[Azullog Debug] Encontrado player_2.php. URL: {player_url}")

                        # Acede ao player final para extrair o MediaFire
                        res3 = await client.get(player_url, headers={"referer": data_embed, "User-Agent": headers["User-Agent"]})
                        api_url_match = re.search(r"const apiUrl = `([^`]+)`", res3.text)

                        if api_url_match:
                            api_url = api_url_match.group(1)
                            print(f"[Azullog Debug] apiUrl encontrada: {api_url}")

                            mediafire_enc_match = re.search(r"[?&]url=([^&]+)", api_url)

                            if mediafire_enc_match:
                                mediafire_url = unquote(mediafire_enc_match.group(1))
                                print(f"[Azullog Debug] URL do MediaFire identificada: {mediafire_url}")

                                # Acede ao MediaFire para sacar o botão de Download direto
                                print("[Azullog Debug] Acessando a página do MediaFire...")
                                mf_res = await client.get(mediafire_url, headers={"Referer": player_url, "User-Agent": headers["User-Agent"]})
                                mf_soup = BeautifulSoup(mf_res.text, 'html.parser')
                                download_btn = mf_soup.select_one("a#downloadButton")

                                if download_btn:
                                    final_mf_link = download_btn.get("href")
                                    print(f"[Azullog Debug] SUCESSO! Link direto do MediaFire extraído: {final_mf_link}")
                                    streams.append({
                                        "name": "FenixFlix",
                                        "title": f"{label}\nON",
                                        "url": final_mf_link
                                    })
                                    continue
                                else:
                                    print("[Azullog Debug] Botão 'downloadButton' não encontrado na página do MediaFire.")
                            else:
                                print("[Azullog Debug] Parâmetro 'url' não encontrado na apiUrl.")
                        else:
                            print("[Azullog Debug] Variável 'apiUrl' não encontrada no código-fonte do player_2.php.")
                    else:
                        print("[Azullog Debug] iframe 'player_2.php' não encontrado.")

                    # Se não passar na lógica do MediaFire, devolve o embed normal caso exista
                    print("[Azullog Debug] Tentando extrair um iframe genérico do embed...")
                    any_iframe = soup2.select_one("iframe")
                    if any_iframe and any_iframe.get("src"):
                        src = any_iframe.get("src")
                        final_embed = "https:" + src if src.startswith("//") else src
                        print(f"[Azullog Debug] SUCESSO! Iframe genérico encontrado: {final_embed}")
                        streams.append({
                            "name": "Azullog",
                            "title": f"Embed - {label}",
                            "url": final_embed
                        })
                    else:
                        print("[Azullog Debug] Nenhum iframe de vídeo encontrado neste player.")

                except Exception as inner_e:
                    print(f"[Azullog Debug] Erro a processar o player '{label}': {inner_e}")
                    continue

        except Exception as e:
            print(f"[Azullog Debug] Erro global na execução do scraper: {e}")

    print(f"[Azullog Debug] Fim da busca. Total de streams adicionados: {len(streams)}\n")
    return streams
