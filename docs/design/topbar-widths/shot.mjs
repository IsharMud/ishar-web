// Screenshot the real #hud-topbar at a given viewport width.
//
//   node shot.mjs <preview.html> <out.png> <width> [name,name,...]
//
// A stub WebSocket opens immediately and stays silent, so each session takes
// the ordinary connect path to "connected" without a bridge; the roster is
// seeded in sessionStorage so tabs carry real character names and a
// multi-session shot needs no interaction.
//
// Playwright rather than `chromium --screenshot`: Chromium clamps a headless
// window to 500px wide, so --window-size=390 yields a 500px layout cropped to
// 390 — a phone-width proof that silently isn't one.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';

const [file, out, width, names = 'Ekard'] = process.argv.slice(2);
const roster = names.split(',').map((character, i) => ({
  slot: i + 1, character, isImmortal: false,
}));

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
});
const page = await browser.newPage({
  viewport: { width: Number(width), height: 800 },
  deviceScaleFactor: 2,
});
await page.addInitScript(({ roster }) => {
  class StubWS {
    constructor(url) {
      this.url = url;
      this.readyState = 0;
      setTimeout(() => { this.readyState = 1; this.onopen && this.onopen({}); }, 20);
    }
    send() {}
    close() { this.readyState = 3; this.onclose && this.onclose({ code: 1000 }); }
    addEventListener(type, fn) { this['on' + type] = fn; }
  }
  Object.assign(StubWS, { CONNECTING: 0, OPEN: 1, CLOSING: 2, CLOSED: 3 });
  window.WebSocket = StubWS;
  sessionStorage.setItem('ishar.sessions',
    JSON.stringify({ focused: roster[0].slot, list: roster }));
}, { roster });

await page.goto(`file://${file}?demo=1`);
await page.waitForTimeout(1500);
await page.locator('#hud-topbar').screenshot({ path: out });
await browser.close();
console.log('wrote', out);
