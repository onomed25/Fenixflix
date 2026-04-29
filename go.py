import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin, urlparse
import re
import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

def evp_kdf(password, salt, key_size, iv_size):
    d = d_i = b''
    while len(d) < key_size + iv_size:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_size], d[key_size:key_size+iv_size]

def descriptografar_link(encrypted_str, password):
    try:
        obj = json.loads(encrypted_str)
        salt = bytes.fromhex(obj['s'])
        ct = base64.b64decode(obj['ct'])
        iv = bytes.fromhex(obj['iv'])
        key, _ = evp_kdf(password.encode('utf-8'), salt, 32, 16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ct), AES.block_size)
        return decrypted.decode('utf-8').replace('"', '')
    except Exception as e:
        print(f"[Go Debug] Erro ao descriptografar: {e}")
        return None

def decodificar_ck(ck_raw):
    try:
        hexvals = re.findall(r'\\x([0-9a-fA-F]{2})', ck_raw)
        if hexvals:
            b64_str = bytes.fromhex(''.join(hexvals)).decode('utf-8')
            try:
                return base64.b64decode(b64_str + '==').decode('utf-8')
            except Exception:
                return b64_str
        return ck_raw
    except:
        return ck_raw

async def resolver_master_txt(client, master_url, referer):
    headers = {'Referer': referer}
    try:
        res = await client.get(master_url, headers=headers)
        conteudo = res.text.strip()
        base = master_url.rsplit('/master.txt', 1)[0]

        b64s = re.findall(r'([a-zA-Z0-9+/]{30,}={0,2})', conteudo)
        for b64 in reversed(b64s):
            try:
                caminho = base64.b64decode(b64 + '==').decode('utf-8').strip()
                if caminho.endswith('.m3u8') or '/hls/' in caminho:
                    return caminho if caminho.startswith('http') else base + '/' + caminho.lstrip('/')
            except:
                continue

        for linha in conteudo.splitlines():
            linha = linha.strip()
            if linha.endswith('.m3u8') or '/hls/' in linha:
                return linha if linha.startswith('http') else base + '/' + linha.lstrip('/')
    except Exception as e:
        print(f"[Go Debug] Erro ao resolver master.txt: {e}")
    return None

async def extrair_embedplayer1(client, url_video):
    video_id = url_video.split('/')[-1].split('?')[0]
    api_url = f'https://embedplayer1.xyz/player/index.php?data={video_id}&do=getVideo'

    headers_get  = {'Referer': 'https://gofilmeshd.top/'}
    headers_post = {**headers_get, 'X-Requested-With': 'XMLHttpRequest'}

    try:
        await client.get(url_video, headers=headers_get)
        response = await client.post(api_url, headers=headers_post, data={'hash': video_id, 'r': 'https://gofilmeshd.top/'})
        dados = response.json()

        secured = dados.get('securedLink', '')
        if secured and '.m3u8' in secured:
            return secured

        video_source = dados.get('videoSource', '')
        if video_source:
            if 'master.txt' in video_source:
                url_real = await resolver_master_txt(client, video_source, 'https://embedplayer1.xyz/')
                if url_real:
                    return url_real
            if video_source.endswith('.m3u8') or '/hls/' in video_source:
                return video_source

        ck_raw   = dados.get('ck', '')
        chave_ck = decodificar_ck(ck_raw) if ck_raw else ''
        if 'videoSources' in dados:
            for source in dados['videoSources']:
                raw_file = source.get('file', '')
                if '{"ct":' in raw_file:
                    dec = descriptografar_link(raw_file, chave_ck)
                    if dec:
                        if dec.startswith('http'): return dec
                        if '/m3/' in dec or '/hls/' in dec: return urljoin('https://embedplayer1.xyz', dec)
                elif raw_file.startswith('http'): return raw_file
                elif '/m3/' in raw_file or '/hls/' in raw_file: return urljoin('https://embedplayer1.xyz', raw_file)

        return None
    except Exception as e:
        print(f"[Go Debug] Erro no embedplayer1: {e}")
        return None

async def resolve_stream_async(client, player_url):
    try:
        r = await client.get(player_url)
        html = r.text

        m_match = re.search(r"const\s+videoSrc\s*=\s*['\"]([^'\"]+)['\"]", html)
        if not m_match:
            m_match = re.search(r'(https?://[^"\'\s]+/master\.txt[^"\'\s]*)', html)

        if m_match:
            m_url    = m_match.group(1).split('#')[0]
            referer  = 'https://watch.brstream.cc/' if 'brstream' in m_url else 'https://gofilmeshd.top/'
            url_real = await resolver_master_txt(client, m_url, referer)
            return url_real or m_url, {'Referer': referer, 'Origin': referer.rstrip('/')}

        mf_match = re.search(r'(https?://[^\s"\']+mediafire\.com[^\s"\']*)', html)
        if mf_match:
            print(f"[Go Debug] Mediafire encontrado na página principal.")
            return mf_match.group(1), {'Referer': player_url}

        soup   = BeautifulSoup(html, 'lxml')
        iframe = soup.find('iframe')
        src    = iframe.get('src') if iframe else None

        if src:
            if src.startswith('//'):
                src = 'https:' + src

            if 'embedplayer1.xyz' in src:
                link = await extrair_embedplayer1(client, src)
                if link:
                    return link, {'Referer': 'https://embedplayer1.xyz/', 'Origin': 'https://embedplayer1.xyz'}

            elif '112234152.xyz' in src:
                vid        = src.split('?data=')[-1].split('&')[0]
                master_url = f'https://112234152.xyz/hls/{vid}/master.txt'
                referer    = 'https://112234152.xyz/'
                url_real   = await resolver_master_txt(client, master_url, referer)
                return url_real or f'https://112234152.xyz/hls/{vid}/index.m3u8', {'Referer': referer}

            elif 'mediafire.com' in src:
                return src, {'Referer': player_url}

            else:
                res_iframe = await client.get(src, headers={'Referer': player_url})

                m_match = re.search(r"const\s+videoSrc\s*=\s*['\"]([^'\"]+)['\"]", res_iframe.text)
                if m_match:
                    stream_url = m_match.group(1)
                    origin     = f"https://{urlparse(src).netloc}"
                    return stream_url, {'Origin': origin, 'Referer': origin + '/'}

                m_match = re.search(r'(https?://[^"\'\s]+/master\.txt[^"\'\s]*)', res_iframe.text)
                if m_match:
                    m_url    = m_match.group(1).split('#')[0]
                    referer  = f"https://{urlparse(src).netloc}/"
                    url_real = await resolver_master_txt(client, m_url, referer)
                    return url_real or m_url, {'Referer': referer, 'Origin': referer.rstrip('/')}

                mf_match = re.search(r'(https?://[^\s"\']+mediafire\.com[^\s"\']*)', res_iframe.text)
                if mf_match:
                    return mf_match.group(1), {'Referer': src}

    except Exception as e:
        print(f"[Go Debug] Erro no resolve_stream_async: {e}")

    return '', {}

def gerar_slugs(title):
    limpo = re.sub(r'[^\w\s-]', '', title)
    limpo = re.sub(r'\s+', ' ', limpo).strip()
    slug_principal = re.sub(r'-+', '-', limpo.replace(' ', '-')).lower()

    slugs = [slug_principal]

    sem_artigos = re.sub(r'\b(o|a|os|as|the|de|da|do|dos|das|em|por|para)\b', '', limpo, flags=re.IGNORECASE)
    sem_artigos = re.sub(r'\s+', ' ', sem_artigos).strip()
    slug_sem_artigos = re.sub(r'-+', '-', sem_artigos.replace(' ', '-')).lower()
    if slug_sem_artigos != slug_principal:
        slugs.append(slug_sem_artigos)

    palavras = limpo.split()
    if len(palavras) > 3:
        slug_curto = '-'.join(palavras[:3]).lower()
        slugs.append(slug_curto)

    return slugs

def extrair_opcoes(html, content_type, season, episode):
    soup = BeautifulSoup(html, 'lxml')
    opts = []
    base_url = 'https://gofilmeshd.top'

    if content_type == 'series' and season and episode:
        buttons = soup.select('div.temps button.accordion')
        panels = soup.select('div.temps div.panel')
        target_panel = None

        for i, btn in enumerate(buttons):
            btn_text = btn.get_text(strip=True)
            match = re.search(r'(\d+)º?\s*[Tt]emporada', btn_text, re.IGNORECASE)
            if match and int(match.group(1)) == int(season):
                if i < len(panels):
                    target_panel = panels[i]
                break

        if not target_panel and len(panels) >= int(season):
            target_panel = panels[int(season) - 1]

        if target_panel:
            links = target_panel.select('div.ep a[href]')
            ep_idx = int(episode) - 1
            if 0 <= ep_idx < len(links):
                opts.append({
                    'name': f"GoFilmes - S{season}E{episode}",
                    'url': urljoin(base_url, links[ep_idx].get('href'))
                })
    else:
        links = soup.select('div.link a[href]')
        for l in links:
            opts.append({
                'name': f"GoFilmes - {l.get_text(strip=True)}",
                'url': urljoin(base_url, l.get('href'))
            })
    return opts

async def tentar_slug(client, slug, content_type, season, episode):
    base_url = 'https://gofilmeshd.top'
    path = 'series' if content_type == 'series' else ''
    url = f"{base_url}/{path}/{quote(slug)}" if path else f"{base_url}/{quote(slug)}"
    print(f"[Go Debug] Testando URL: {url}")
    
    try:
        res = await client.get(url)
        if res.status_code == 200:
            print(f"[Go Debug] Sucesso! Página encontrada para '{slug}'")
            return extrair_opcoes(res.text, content_type, season, episode)
    except Exception as e:
        print(f"[Go Debug] Erro ao buscar slug '{slug}': {e}")
    return None

async def search_gofilmes(client, titles, content_type, season=None, episode=None):
    slugs_para_tentar = []
    for title in titles:
        slugs_para_tentar.extend(gerar_slugs(title))

    vistos = set()
    slugs_unicos = [s for s in slugs_para_tentar if not (s in vistos or vistos.add(s))]

    print(f"[Go Debug] Total de variações de nomes a testar em paralelo: {len(slugs_unicos)}")

    sem = asyncio.Semaphore(6)

    async def tentar_com_semaforo(slug):
        async with sem:
            return await tentar_slug(client, slug, content_type, season, episode)

    tarefas = [asyncio.create_task(tentar_com_semaforo(slug)) for slug in slugs_unicos]

    for resultado_futuro in asyncio.as_completed(tarefas):
        try:
            opcoes = await resultado_futuro
            if opcoes:
                print("[Go Debug] Sucesso! Encontramos o certo. Cancelando o resto para acelerar.")
                for t in tarefas:
                    if not t.done():
                        t.cancel()
                return opcoes
        except Exception as e:
            pass
            
    return []

async def search_serve(titles, content_type, season=None, episode=None):
    results = []
    print(f"\n[Go Debug] Iniciando busca para títulos: {titles} | Tipo: {content_type}")

    async with httpx.AsyncClient(
        headers=HEADERS,
        timeout=10.0,
        follow_redirects=True
    ) as client:
        
        options = await search_gofilmes(client, titles, content_type, season, episode)

        if not options:
            print("[Go Debug] Nenhuma opção de link encontrada no site principal.")
            return results

        print(f"[Go Debug] Encontradas {len(options)} opções de players. Resolvendo...")

        tasks = [resolve_stream_async(client, opt['url']) for opt in options[:2]]
        resolved_streams = await asyncio.gather(*tasks, return_exceptions=True)

        for res in resolved_streams:
            if isinstance(res, Exception):
                print(f"[Go Debug] Exceção durante a resolução de stream: {res}")
                continue

            url, head = res

            if url and ('master.txt' in url or '.m3u8' in url or 'mediafire' in url or '.mp4' in url):
                print(f"[Go Debug] Stream extraído com sucesso: {url[:60]}...")
                entry = {
                    'name': 'FenixFlix',
                    'title': 'Leg/Dub\nGO',
                    'url': url,
                }
                if head:
                    entry['behaviorHints'] = {'proxyHeaders': {'request': head}}
                results.append(entry)

    return results