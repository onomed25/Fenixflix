try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

def resolver_streamtape_url(url):
    video_final = None
    viu_get_video = False

    if not PLAYWRIGHT_AVAILABLE:
        print("[Streamtape] Playwright não disponível no ambiente. Retornando URL original.")
        return url

    try:
        with sync_playwright() as p:
            # Configuração otimizada para rodar dentro de containers Docker (Render/Koyeb)
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--mute-audio',
                    '--no-sandbox',             # Necessário para rodar como root/Docker
                    '--disable-setuid-sandbox', # Complemento para desativar a sandbox
                    '--disable-dev-shm-usage'   # Evita crash por falta de memória compartilhada
                ]
            )
            page = browser.new_page()

            def interceptar(response):
                nonlocal video_final, viu_get_video
                try:
                    u = response.url
                    if "get_video" in u:
                        viu_get_video = True
                    elif viu_get_video and "tapecontent.net" in u:
                        video_final = u
                except Exception as inner_e:
                    print(f"[Streamtape - Intercept] Erro: {inner_e}")

            page.on("response", interceptar)

            print(f"[Streamtape] Abrindo navegador para: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=15000)

            try:
                viewport = page.viewport_size
                if viewport:
                    x = viewport['width'] / 2
                    y = viewport['height'] / 2
                    for _ in range(2):
                        page.mouse.click(x, y)
                        page.wait_for_timeout(500)
            except Exception as click_e:
                print(f"[Streamtape - Click] Erro ao clicar no player: {click_e}")

            for _ in range(10):
                if video_final:
                    print(f"[Streamtape] Link direto extraído com sucesso: {video_final}")
                    break
                page.wait_for_timeout(1000)

            page.close()
            browser.close()

    except Exception as e:
        # Mostra o erro exato nos logs do Render caso o Playwright quebre
        print(f"[Streamtape - Erro Fatal] Ocorreu um problema no Playwright: {e}")

    return video_final if video_final else url
