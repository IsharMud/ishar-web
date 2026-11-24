const { chromium } = require('playwright');
const OUT = __dirname + '/';
const BASE = 'http://127.0.0.1:8765';
const pages = [
  ['corwen', '/player/Corwen/?as=Maren'],
  ['brannoc', '/player/Brannoc/?as=Isolde'],
  ['tam', '/player/Tam/?as=Boric'],
  ['portal_maren', '/portal/?as=Maren'],
];
(async () => {
  const browser = await chromium.launch();
  for (const [w, label, scale] of [[390, 'phone', 2], [1280, 'desktop', 1]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: scale });
    for (const [name, path] of pages) {
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
      await page.goto(BASE + path, { waitUntil: 'networkidle' });
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
      const panel = page.locator('.ac-panel', { has: page.locator('#season-essence') });
      await panel.screenshot({ path: OUT + 'essence_' + name + '_' + label + '.png' });
      console.log(name, label, 'overflow=' + overflow, 'errors=' + (errors.join(' | ') || 'none'));
      await page.close();
    }
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(BASE + '/connect/?demo=1', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1200);
    await page.locator('.v-tension').first().click();
    await page.waitForTimeout(600);
    const lines = await page.evaluate(() => Array.from(document.querySelectorAll('.tn-line')).map(n => n.textContent));
    const tiles = await page.evaluate(() => Array.from(document.querySelectorAll('.season-tile')).map(n => n.textContent.trim()));
    console.log('hud', label, JSON.stringify(lines), JSON.stringify(tiles), 'errors=' + (errors.join(' | ') || 'none'));
    await page.evaluate(() => { const n = Array.from(document.querySelectorAll('.tn-h')).find(h => /This season/i.test(h.textContent)); if (n) n.scrollIntoView(); });
    await page.waitForTimeout(300);
    await page.screenshot({ path: OUT + 'hud_essence_' + label + '.png' });
    await ctx.close();
  }
  await browser.close();
})();
