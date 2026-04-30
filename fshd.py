import httpx
from bs4 import BeautifulSoup
import re
import asyncio

def js_unpack(source):
    """Função utilitária para descompactar JavaScript ofuscado (P.A.C.K.E.R)."""
    source = source.strip()

    full_pattern = r"eval\s*\(\s*function\s*\(\s*p\s*,\s*a\s*,\s*c\s*,\s*k\s*,\s*e\s*,\s*d\s*\).+?\}\s*\(\s*['\"](.+?)['\"]\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*['\"](.+?)['\"]\s*\.split\s*\(\s*['\"]\|['\"]\s*\)"
    match = re.search(full_pattern, source, re.DOTALL)

    if not match:
        return None

    try:
        payload  = match.group(1)
        radix    = int(match.group(2))
        count    = int(match.group(3))
        keywords = match.group(4).split('|')

        def base_encode(n):
            chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if n < len(chars): return chars[n]
            return base_encode(n // len(chars)) + chars[n % len(chars)]

        symtab = {}
        for i in range(count):
            key = base_encode(i)
            val = keywords[i] if i < len(keywords) and keywords[i] else key
            symtab[key] = val

        def replace_token(m):
            return symtab.get(m.group(0), m.group(0))

        result = re.sub(r'\b\w+\b', replace_token, payload)
        return result.replace('\\', '')
    except Exception as e:
        print(f"[FSHD Debug] Erro no unpack JS: {e}")
        return None


async def _resolve_redirect(client, url, referer):
    try:
        resp = await client.get(url, headers={"Referer": referer})
        match = re.search(r'window\.location\.href\s*=\s*"([^"]+)"', resp.text)
        if match:
            return match.group(1)
        return url
    except Exception as e:
        print(f"[FSHD Debug] Erro redirecionamento: {e}")
        return url


async def _extract_internal_player(client, player_url, referer):
    try:
        resp = await client.get(player_url, headers={"Referer": referer})
        html = resp.text

        base_url = ""
        m_base = re.search(r'var player_base_url\s*=\s*"([^"]+)"', html)
        if m_base:
            base_url = m_base.group(1)

        packed_match = re.search(r'eval\s*\((function\(p,a,c,k,e,d\).+?)\)\s*;?\s*</script>', html, re.DOTALL)

        unpacked = None
        if packed_match:
            full_packed = f"eval({packed_match.group(1)})"
            unpacked = js_unpack(full_packed)

        if not unpacked:
            unpacked = js_unpack(html)

        if not unpacked:
            return None

        m_vid = re.search(r'videoUrl\s*[:=]\s*["\'](.*?)["\']', unpacked)
        if not m_vid:
            m_vid = re.search(r'["\']([^"\']+\.(?:m3u8|hls|txt)[^"\']*)["\']', unpacked)

        if m_vid:
            path = m_vid.group(1).replace("\\/", "/")
            if path.startswith("http"):
                return path
            return f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    except Exception as e:
        print(f"[FSHD Debug] Internal Player Error: {e}")
    return None


async def search_serve(tmdb_id: str, content_type: str, season=None, episode=None, client: httpx.AsyncClient = None):
    """
    Aceita um cliente httpx partilhado (pool de conexões) ou cria o seu próprio.
    """
    streams = []

    if content_type.strip().lower() != "series":
        print(f"[FSHD Debug] Ignorando busca para TMDB {tmdb_id}. Motivo: O tipo é '{content_type}', e este script agora é exclusivo para séries.")
        return streams

    base_url = "https://fshd.link"
    print(f"\n[FSHD Debug] A procurar TMDB ID: {tmdb_id} | Tipo: {content_type} | S{season}E{episode}")

    url = f"{base_url}/serie/{tmdb_id}/{season}/{episode}"
    c_type = "2"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Referer": f"{base_url}/"
    }

    async def _run(c):
        try:
            res = await c.get(url, headers=headers)
            if res.status_code != 200:
                print(f"[FSHD Debug] Falha ao aceder à página base. Status: {res.status_code}")
                return streams

            html = res.text
            soup = BeautifulSoup(html, 'lxml')

            content_info = None
            active_ep = soup.select_one(".episodeOption.active")
            if active_ep and active_ep.get("data-contentid"):
                content_info = active_ep.get("data-contentid")

            if not content_info:
                m = re.search(r"var CONTENT_INFO = '(\d+)';", html)
                if m:
                    content_info = m.group(1)

            if not content_info:
                content_info = tmdb_id

            print(f"[FSHD Debug] CONTENT_INFO resolvido: {content_info}")

            server_ids = []
            pl = {"content_id": int(content_info), "content_type": c_type}
            h_ajax = headers.copy()
            h_ajax.update({"X-Requested-With": "XMLHttpRequest", "Accept": "application/json", "Referer": url})

            try:
                res_opt = await c.post(f"{base_url}/api/options", data=pl, headers=h_ajax)
                server_ids = re.findall(r'["\']ID["\']\s*:\s*(\d+)', res_opt.text)
            except Exception as e:
                print(f"[FSHD Debug] API Opt Error: {e}")

            unique_servers = list(set(server_ids))
            print(f"[FSHD Debug] Servidores encontrados: {unique_servers}")

            for vid_id in unique_servers:
                try:
                    pl_data = {
                        "content_info": int(content_info),
                        "content_type": c_type,
                        "video_id": int(vid_id)
                    }
                    h_ajax2 = headers.copy()
                    h_ajax2.update({"X-Requested-With": "XMLHttpRequest", "Referer": url})

                    res_player = await c.post(f"{base_url}/api/players", data=pl_data, headers=h_ajax2)
                    m_url = re.search(r'["\']video_url["\']\s*:\s*["\'](.*?)["\']', res_player.text)
                    if not m_url:
                        continue

                    player_url = m_url.group(1).replace("\\/", "/")
                    print(f"[FSHD Debug] Player URL (ID {vid_id}): {player_url}")

                    final_url = await _resolve_redirect(c, player_url, url)
                    if not final_url:
                        continue

                    stream_url = final_url
                    if "112234152.xyz" in final_url or "/player/" in final_url:
                        final_m3u8 = await _extract_internal_player(c, final_url, player_url)
                        if final_m3u8:
                            stream_url = final_m3u8
                            print(f"[FSHD Debug] Link M3U8 extraído: {stream_url}")

                    streams.append({
                        "name": "FenixFlix",
                        "description": f"Dublado\nFlix",
                        "url": stream_url,
                        "behaviorHints": {"notWebReady": False, "bingeGroup": "fenixflix-fshd"}
                    })

                except Exception as e:
                    print(f"[FSHD Debug] Error fetching player {vid_id}: {e}")

            if not streams:
                print("[FSHD Debug] Processo terminou, mas nenhum link de stream válido foi extraído.")

        except Exception as e:
            print(f"[FSHD Debug] Erro global: {e}")

        return streams

    if client is not None:
        return await _run(client)
    else:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as c:
            return await _run(c)