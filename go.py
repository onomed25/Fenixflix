import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin, urlparse
import re
import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import logging

logger = logging.getLogger(__name__)


session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

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
        logger.debug(f"Erro ao descriptografar: {e}")
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


def resolver_master_txt(master_url, referer):
    headers = {'Referer': referer}
    try:
        res = session.get(master_url, headers=headers, timeout=10)
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
        logger.debug(f"Erro ao resolver master.txt: {e}")
    return None


def extrair_embedplayer1(url_video):
    video_id = url_video.split('/')[-1].split('?')[0]
    api_url = 'https://embedplayer1.xyz/player/index.php?data=' + video_id + '&do=getVideo'

    headers_get  = {'Referer': 'https://gofilmeshd.top/'}
    headers_post = {**headers_get, 'X-Requested-With': 'XMLHttpRequest'}

    try:
        session.get(url_video, headers=headers_get, timeout=10)
        response = session.post(api_url, headers=headers_post, data={'hash': video_id, 'r': 'https://gofilmeshd.top/'}, timeout=10)

        dados = response.json()

        secured = dados.get('securedLink', '')
        if secured and '.m3u8' in secured:
            return secured

        video_source = dados.get('videoSource', '')
        if video_source:
            if 'master.txt' in video_source:
                url_real = resolver_master_txt(video_source, 'https://embedplayer1.xyz/')
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
        logger.debug(f"Erro no embedplayer1: {e}")
        return None

# ---------------------------------------------------------
# GERAR VARIAÇÕES DO SLUG PARA BUSCA
# ---------------------------------------------------------
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


def search_gofilmes(titles, content_type, season=None, episode=None):
    base_url = 'https://gofilmeshd.top'
    path     = 'series' if content_type == 'series' else ''

    slugs_para_tentar = []
    for title in titles:
        slugs_para_tentar.extend(gerar_slugs(title))

    vistos = set()
    slugs_unicos = []
    for s in slugs_para_tentar:
        if s not in vistos:
            vistos.add(s)
            slugs_unicos.append(s)

    for slug in slugs_unicos:
        url = f"{base_url}/{path}/{quote(slug)}" if path else f"{base_url}/{quote(slug)}"
        logger.debug(f"Tentando URL: {url}")
        try:
            res = session.get(url, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                opts = []

                if content_type == 'series' and season and episode:
                    # Busca os botões de temporada e os painéis de episódios
                    buttons = soup.select('div.temps button.accordion')
                    panels = soup.select('div.temps div.panel')

                    target_panel = None

                    # 1. Tenta encontrar a temporada correta pelo texto do botão (Ex: "2º Temporada")
                    for i, btn in enumerate(buttons):
                        btn_text = btn.get_text(strip=True)
                        match = re.search(r'(\d+)º?\s*[Tt]emporada', btn_text, re.IGNORECASE)
                        if match and int(match.group(1)) == int(season):
                            if i < len(panels):
                                target_panel = panels[i]
                            break

                    # 2. Fallback: Tenta acessar pelo índice caso o regex falhe
                    if not target_panel and len(panels) >= int(season):
                        target_panel = panels[int(season) - 1]

                    # 3. Extrai os episódios apenas do painel da temporada certa
                    if target_panel:
                        links = target_panel.select('div.ep a[href]')
                        ep_idx = int(episode) - 1

                        if 0 <= ep_idx < len(links):
                            opts.append({
                                'name': f"GoFilmes - S{season}E{episode}",
                                'url': urljoin(base_url, links[ep_idx].get('href'))
                            })
                else:
                    # Filmes
                    links = soup.select('div.link a[href]')
                    for l in links:
                        opts.append({
                            'name': f"GoFilmes - {l.get_text(strip=True)}",
                            'url': urljoin(base_url, l.get('href'))
                        })

                if opts:
                    return opts
        except Exception as e:
            logger.debug(f"Erro ao buscar slug '{slug}': {e}")

    return []


def resolve_stream(player_url):
    try:
        r    = session.get(player_url, timeout=10)
        html = r.text

        # 1. VERIFICA SE O LINK JÁ ESTÁ NA PRÓPRIA PÁGINA
        m_match = re.search(r"const\s+videoSrc\s*=\s*['\"]([^'\"]+)['\"]", html)
        if not m_match:
            m_match = re.search(r'(https?://[^"\'\s]+/master\.txt[^"\'\s]*)', html)

        if m_match:
            m_url    = m_match.group(1).split('#')[0]
            referer  = 'https://watch.brstream.cc/' if 'brstream' in m_url else 'https://gofilmeshd.top/'
            url_real = resolver_master_txt(m_url, referer)
            return url_real or m_url, {'Referer': referer, 'Origin': referer.rstrip('/')}

        # Procura Mediafire direto na página principal
        mf_match = re.search(r'(https?://[^\s"\']+mediafire\.com[^\s"\']*)', html)
        if mf_match:
            logger.debug(f"Mediafire encontrado na página principal: {mf_match.group(1)}")
            return mf_match.group(1), {'Referer': player_url}

        # 2. PROCURA POR IFRAMES
        soup   = BeautifulSoup(html, 'html.parser')
        iframe = soup.find('iframe')
        src    = iframe.get('src') if iframe else None

        if src:
            if src.startswith('//'):
                src = 'https:' + src

            if 'embedplayer1.xyz' in src:
                link = extrair_embedplayer1(src)
                if link:
                    return link, {'Referer': 'https://embedplayer1.xyz/', 'Origin': 'https://embedplayer1.xyz'}

            elif '112234152.xyz' in src:
                vid        = src.split('?data=')[-1].split('&')[0]
                master_url = f'https://112234152.xyz/hls/{vid}/master.txt'
                referer    = 'https://112234152.xyz/'
                url_real   = resolver_master_txt(master_url, referer)
                return url_real or f'https://112234152.xyz/hls/{vid}/index.m3u8', {'Referer': referer}

            # Iframe é direto do Mediafire
            elif 'mediafire.com' in src:
                logger.debug(f"Mediafire encontrado direto no iframe: {src}")
                return src, {'Referer': player_url}

            # Fallback genérico — acessa o iframe e procura o link lá dentro
            else:
                res_iframe = session.get(src, headers={'Referer': player_url}, timeout=10)

                # Procura videoSrc
                m_match = re.search(r"const\s+videoSrc\s*=\s*['\"]([^'\"]+)['\"]", res_iframe.text)
                if m_match:
                    stream_url = m_match.group(1)
                    origin     = f"https://{urlparse(src).netloc}"
                    return stream_url, {'Origin': origin, 'Referer': origin + '/'}

                # Procura master.txt
                m_match = re.search(r'(https?://[^"\'\s]+/master\.txt[^"\'\s]*)', res_iframe.text)
                if m_match:
                    m_url    = m_match.group(1).split('#')[0]
                    referer  = f"https://{urlparse(src).netloc}/"
                    url_real = resolver_master_txt(m_url, referer)
                    return url_real or m_url, {'Referer': referer, 'Origin': referer.rstrip('/')}

                # Procura Mediafire dentro do iframe
                mf_match = re.search(r'(https?://[^\s"\']+mediafire\.com[^\s"\']*)', res_iframe.text)
                if mf_match:
                    logger.debug(f"Mediafire encontrado dentro do iframe: {mf_match.group(1)}")
                    return mf_match.group(1), {'Referer': src}

    except Exception as e:
        logger.error(f"Erro no resolve_stream: {e}")

    return '', {}


def search_serve(titles, content_type, season=None, episode=None):
    options = search_gofilmes(titles, content_type, season, episode)
    results = []

    for opt in options:
        url, head = resolve_stream(opt['url'])

        if url and ('master.txt' in url or '.m3u8' in url or 'mediafire' in url or '.mp4' in url):
            entry = {
                'name': 'FenixFlix',
                'title': 'Leg/Dub\nGO',
                'url': url,
            }
            if head:
                entry['behaviorHints'] = {'proxyHeaders': {'request': head}}
            results.append(entry)
            logger.debug(f"Stream aceito: {url}")

        if len(results) >= 2:
            break

    return results
