import cloudscraper
import requests
import re
import json
import unicodedata
import asyncio
from bs4 import BeautifulSoup
# Playwright removido para economizar memória

def limpar_slug(texto):
    if not texto: return ""
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = texto.lower().strip().replace(":", "").replace("'", "").replace("!", "").replace("?", "").replace(".", "")
    return texto.replace(" ", "-")

def limpar_titulo_imdb(texto):
    if not texto: return None
    texto = re.sub(r'\s\(\d{4}\).*', '', texto) 
    texto = re.sub(r'\s-\sIMDb.*', '', texto) 
    return texto.strip()

def get_nomes_imdb(imdb_id):
    nomes_candidatos = []
    url = f'https://www.imdb.com/pt/title/{imdb_id}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=8)
        src = r.text
        
        title_matches = re.findall('<title>(.*?)</title>', src)
        if title_matches:
            raw_title = title_matches[0]
            clean_title = limpar_titulo_imdb(raw_title)
            if clean_title and clean_title not in nomes_candidatos:
                nomes_candidatos.append(clean_title)

        script_match = re.findall('json">(.*?)</script>', src, re.DOTALL)
        if script_match:
            data = json.loads(script_match[0])
            name = data.get('name', '')
            alternate = data.get('alternateName', '')
            
            if alternate and alternate not in nomes_candidatos:
                nomes_candidatos.append(alternate)
            if name and name not in nomes_candidatos:
                nomes_candidatos.append(name)
                
    except Exception:
        pass
    
    return nomes_candidatos

def obter_url_final(tipo, nome_slug, temporada=None, episodio=None):
    if tipo == 'movie':
        url_inicial = f"https://streamberry.com.br/filmes/{nome_slug}/"
    else:
        url_inicial = f"https://streamberry.com.br/episodios/{nome_slug}-{temporada}x{episodio}/"
    
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    
    try:
        resp = scraper.get(url_inicial, timeout=10)
        
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, 'html.parser')
        link_intermediario = None
        
        caixa_downloads = soup.find('div', id='download')
        if caixa_downloads:
            for link in caixa_downloads.find_all('a'):
                href = link.get('href', '')
                if "links/" in href:
                    link_intermediario = href
                    break
        
        if not link_intermediario:
            for a in soup.find_all('a', href=True):
                if '/links/' in a['href']:
                    link_intermediario = a['href']
                    break

        if not link_intermediario:
            return None

        resp_final = scraper.get(link_intermediario)
        url_final = resp_final.url
        
        if "/download/" in url_final:
            return url_final.replace("/download/", "/d/")
        return url_final

    except Exception:
        return None

# Nova função LEVE substituindo o Playwright
def buscar_m3u8_leve(url_alvo):
    links = []
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    
    try:
        resp = scraper.get(url_alvo, timeout=15)
        if resp.status_code == 200:
            html = resp.text
            
            # Busca links .m3u8 usando regex no código fonte
            matches = re.findall(r'(https?://[^\s"\'<>]+\.m3u8)', html)
            
            for m in matches:
                m = m.replace('\\/', '/')
                if m not in links:
                    links.append(m)
            
            # Busca fallback em tags source
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

    # Usa a função leve em vez do firefox pesado
    links = await loop.run_in_executor(None, buscar_m3u8_leve, url_found)
    
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
