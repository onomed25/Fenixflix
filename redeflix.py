import time
import httpx
import re

_RE_DEFAULT_URL = re.compile(r'const\s+defaultUrl\s*=\s*["\'](.*?)["\']')
_RE_GENERIC_URL = re.compile(r'(https?://[^"\']*\.(?:mp4|m3u8)[^"\']*)')

async def resolve_redeflix(url: str, client: httpx.AsyncClient = None) -> str:
    """
    Extrai o link direto (mp4/m3u8) da página HTML da RedeFlix.
    """
    start_time = time.time()
    print(f"[RedeFlix Debug] Iniciando extração para: {url}")
    
    should_close = False
    if client is None:
        client = httpx.AsyncClient(http2=True, verify=False)
        should_close = True

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Referer": "https://redeflixapi.store/"
        }

        print(f"[RedeFlix Debug] Fazendo GET request (timeout=15s)...")
        req_start = time.time()
        resp = await client.get(url, headers=headers, timeout=15.0)
        req_end = time.time()
        print(f"[RedeFlix Debug] GET finalizado em {req_end - req_start:.3f}s | HTTP {resp.status_code} | Len: {len(resp.text)} bytes")
        
        if resp.status_code == 200:
            parse_start = time.time()
            # Tenta encontrar a variável defaultUrl = "link"
            match = _RE_DEFAULT_URL.search(resp.text)
            if match:
                parse_end = time.time()
                print(f"[RedeFlix Debug] Regex (defaultUrl) demorou {parse_end - parse_start:.4f}s. Link encontrado!")
                return match.group(1)
            
            # Se não achar defaultUrl, procura por mp4/m3u8 genérico no código
            match_generic = _RE_GENERIC_URL.search(resp.text)
            if match_generic:
                parse_end = time.time()
                print(f"[RedeFlix Debug] Regex (genérico) demorou {parse_end - parse_start:.4f}s. Link encontrado!")
                return match_generic.group(1)
            
            print(f"[RedeFlix Debug] Nenhuma regex encontrou o link no HTML retornado.")
        
        return None
    except Exception as e:
        print(f"[RedeFlix Resolver] Erro ao extrair link de {url}: {e}")
        return None
    finally:
        if should_close:
            await client.aclose()
