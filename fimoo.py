import httpx
import re
import json
import asyncio
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://player.fimoo.site/"
}

async def extrair_link_mp4(url_episodio):
    """Acessa a página do episódio gerada pelo JSON e extrai o link direto do vídeo"""
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(url_episodio, headers=HEADERS, timeout=10)
            html = response.text

            # --- PLANO A: Procurar o link no botão de Download ---
            soup = BeautifulSoup(html, 'html.parser')
            botao_download = soup.select_one('#down-list a')
            if botao_download and botao_download.get('href'):
                return botao_download.get('href')

            # --- PLANO B: Pegar direto do JWPlayer com Regex ---
            match_jwplayer = re.search(r'file:\s*["\'](http.*?)["\']', html)
            if match_jwplayer:
                return match_jwplayer.group(1)

        except Exception as e:
            print(f"[Fimoo] Erro ao extrair mp4: {e}")

    return None

async def search_serve(tmdb_id: str, content_type: str, season: int = None, episode: int = None):
    """Função principal chamada pelo app.py do FenixFlix"""

    # Aplicando a sua dica: manda direto para a temporada se for série
    url_player = f"https://player.fimoo.site/embed/{tmdb_id}"
    if content_type == "series" and season:
        url_player += f"?season={season}"

    streams = []

    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(url_player, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                return streams

            # Extrai o JSON de dentro do JavaScript da página
            padrao_regex = r'var TRACKS\s*=\s*(\{.*?\});'
            match = re.search(padrao_regex, response.text)

            if match:
                catalogo = json.loads(match.group(1))
                links_pagina = []

                for audio_key, audio_data in catalogo.items():
                    idioma = audio_data.get('label', audio_key.upper())
                    link_pagina = None

                    # --- LÓGICA PARA SÉRIES ---
                    if content_type == "series" and season and episode:
                        temporadas = audio_data.get("seasons", {})
                        temp_data = temporadas.get(str(season), {})
                        episodios = temp_data.get("episodes", [])

                        for ep in episodios:
                            # Procura o episódio exato
                            if str(ep.get('ep')) == str(episode):
                                link_pagina = ep.get('url')
                                break

                    # --- LÓGICA PARA FILMES ---
                    elif content_type == "movie":
                        link_pagina = audio_data.get('url')

                    # --- SE ACHOU O LINK, ADICIONA NA LISTA PARA BUSCAR DEPOIS ---
                    if link_pagina:
                        links_pagina.append((idioma, link_pagina))

                # --- EXTRAÇÃO EM PARALELO DE TODOS OS ÁUDIOS ENCONTRADOS ---
                if links_pagina:
                    resultados_mp4 = await asyncio.gather(
                        *[extrair_link_mp4(lp) for _, lp in links_pagina],
                        return_exceptions=True
                    )

                    for (idioma, _), link_mp4 in zip(links_pagina, resultados_mp4):
                        if isinstance(link_mp4, str) and link_mp4.startswith("http"):
                            streams.append({
                                "name": "FenixFlix",
                                "title": f"{idioma}\nFimoo",
                                "url": link_mp4
                            })

        except Exception as e:
            print(f"[Fimoo] Erro geral: {e}")

    return streams