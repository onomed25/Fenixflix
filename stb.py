import cloudscraper
import requests
import re
import json
import unicodedata
import asyncio
from bs4 import BeautifulSoup
# Remova ou comente a linha do playwright para não gastar memória importando
# from playwright.async_api import async_playwright 

# ... (mantenha as funções limpar_slug, limpar_titulo_imdb, get_nomes_imdb, obter_url_final iguais) ...

# NOVA FUNÇÃO LEVE (Substitui o Playwright)
def buscar_m3u8_leve(url_alvo):
    links = []
    # Cria um scraper que simula um navegador, mas sem abrir janela (muito leve)
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    
    try:
        resp = scraper.get(url_alvo, timeout=15)
        if resp.status_code == 200:
            html = resp.text
            
            # Tenta encontrar links .m3u8 diretamente no texto (regex)
            # Procura por strings que começam com http e terminam com .m3u8
            matches = re.findall(r'(https?://[^\s"\'<>]+\.m3u8)', html)
            
            for m in matches:
                # Às vezes o link vem com barras escapadas (\/), precisamos corrigir
                m = m.replace('\\/', '/')
                if m not in links:
                    links.append(m)
                    
            # Se não achou com regex simples, tenta procurar dentro de tags source (caso use player HTML5 padrão)
            if not links:
                soup = BeautifulSoup(html, 'html.parser')
                for source in soup.find_all('source'):
                    src = source.get('src')
                    if src and '.m3u8' in src and src not in links:
                        links.append(src)

    except Exception as e:
        print(f"Erro ao buscar m3u8: {e}")
        pass
        
    return links

async def search_streamberry(imdb_id, tipo, nome_original, temporada=None, episodio=None):
    loop = asyncio.get_running_loop()
    
    # ... (mantenha a lógica de busca de nomes igual) ...
    # (Copie a parte inicial da função original até o "if not url_found: return []")
    
    if tipo == 'movie':
        lista_nomes = await loop.run_in_executor(None, get_nomes_imdb, imdb_id)
    else:
        lista_nomes = await loop.run_in_executor(None, get_nomes_imdb, imdb_id)
    
    if nome_original and nome_original not in lista_nomes:
        lista_nomes.append(nome_original)

    url_found = None
    nome_sucesso = ""

    for nome in lista_nomes:
        slug = limpar_slug(nome)
        if len(slug) < 2: continue
        
        url_player = await loop.run_in_executor(None, obter_url_final, tipo, slug, temporada, episodio)
        
        if url_player:
            url_found = url_player
            nome_sucesso = nome
            break
        
    if not url_found:
        return []

    # --- AQUI É A MUDANÇA PRINCIPAL ---
    # Em vez de chamar o firefox, chamamos a função leve no executor
    links = await loop.run_in_executor(None, buscar_m3u8_leve, url_found)
    # ----------------------------------
    
    streams = []
    for link in links:
        if tipo == 'movie':
            titulo_display = f"Filme - {nome_sucesso}"
        else:
            titulo_display = f"S{temporada}E{episodio} - {nome_sucesso}"

        streams.append({
            "name": "FenixFlix",
            "title": titulo_display,
            "url": link,
            "behaviorHints": {
                "bingeGroup": "streamberry-vip",
                "notWebReady": True
            }
        })
    
    return streams
