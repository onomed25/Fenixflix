try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

def resolver_streamtape_url(url):
    video_final = None
    viu_get_video = False

    if not PLAYWRIGHT_AVAILABLE:
        return url

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--mute-audio'])
            page = browser.new_page()

            def interceptar(response):
                nonlocal video_final, viu_get_video
                try:
                    u = response.url
                    if "get_video" in u:
                        viu_get_video = True
                    elif viu_get_video and "tapecontent.net" in u:
                        video_final = u
                except Exception:
                    pass

            page.on("response", interceptar)
            page.goto(url, wait_until="domcontentloaded", timeout=15000)

            try:
                viewport = page.viewport_size
                if viewport:
                    x = viewport['width'] / 2
                    y = viewport['height'] / 2
                    for _ in range(2):
                        page.mouse.click(x, y)
                        page.wait_for_timeout(500)
            except Exception:
                pass

            for _ in range(10):
                if video_final: break
                page.wait_for_timeout(1000)

            page.close()
            browser.close()
    except Exception:
        pass

    return video_final if video_final else url
