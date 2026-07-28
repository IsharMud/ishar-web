import sys
from playwright.sync_api import sync_playwright
path, out, w, h, full = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "full"
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": w, "height": h})
    pg.goto("file://" + path)
    pg.wait_for_timeout(300)
    print(pg.evaluate("() => { var r = document.getElementById('keys-pop').getBoundingClientRect(); return [innerWidth, Math.round(r.width), Math.round(r.left), Math.round(r.height)]; }"))
    pg.screenshot(path=out, full_page=full)
    b.close()
