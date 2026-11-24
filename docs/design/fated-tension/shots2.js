const { chromium } = require('playwright');
const OUT = __dirname + '/';
const BASE = 'http://127.0.0.1:8765';
const pages = [
  ['fated', '/fated/', null],
  ['knots_tyrell', '/fated/knots/?as=Tyrell', null],
  ['season', '/season/', '#fated'],
  ['portal_loom', '/portal/?as=Tyrell', '#threads'],
];
(async () => {
  const browser = await chromium.launch();
  for (const [w, label] of [[390, 'phone'], [1280, 'desktop']]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
    for (const [name, path, anchor] of pages) {
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      await page.goto(BASE + path, { waitUntil: 'networkidle' });
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
      if (anchor) await page.evaluate(a => { const n = document.querySelector(a); if (n) n.scrollIntoView(); }, anchor);
      await page.screenshot({ path: `${OUT}${name}_${label}.png`, fullPage: !anchor });
      console.log(`${name} ${label}: overflow=${overflow} errors=${errors.length ? errors.join(' | ') : 'none'}`);
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
})();
