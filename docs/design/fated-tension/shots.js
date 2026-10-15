const { chromium } = require('/opt/node-tools/node_modules/playwright');
const OUT = '/tmp/claude-0/-home-user-ishar-web/f631e60d-2c23-527e-b7f0-18ab25133956/scratchpad/shots/';
const BASE = 'http://127.0.0.1:8765';
const pages = [
  ['player_aelwyn', '/player/Aelwyn/?as=Tyrell', '#tension'],
  ['portal_tyrell', '/portal/?as=Tyrell', '#loom'],
  ['leaders_tension', '/leaders/tension/?as=Tyrell', null],
  ['leaders_lifetime', '/leaders/tension/lifetime/?as=Tyrell', null],
  ['leaders', '/leaders/?as=Tyrell', null],
  ['achievements_tyrell', '/achievements/?as=Tyrell', null],
  ['achievements_anon', '/achievements/', null],
  ['player_lanya', '/player/Lanya/?as=Boric', '#tension'],
  ['player_wren', '/player/Wren/?as=Eternal', '#tension'],
  ['help_tension', '/help/Tension/', null],
];
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [w, label] of [[390, 'phone'], [1280, 'desktop']]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
    for (const [name, path, anchor] of pages) {
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      await page.goto(BASE + path, { waitUntil: 'networkidle' });
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
      if (anchor) { await page.evaluate(a => { const n = document.querySelector(a); if (n) n.scrollIntoView(); }, anchor); }
      await page.screenshot({ path: `${OUT}${name}_${label}.png`, fullPage: !anchor });
      console.log(`${name} ${label}: overflow=${overflow} errors=${errors.length ? errors.join(' | ') : 'none'}`);
      await page.close();
    }
    // The web client in demo mode: open the Season overlay from the Tension pill.
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(BASE + '/connect/?demo=1', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1200);
    await page.screenshot({ path: `${OUT}hud_topbar_${label}.png` });
    const pill = page.locator('.v-tension');
    console.log(`hud ${label}: tension pill = ${await pill.count() ? await pill.first().textContent() : 'MISSING'}`);
    if (await pill.count()) {
      await pill.first().click();
      await page.waitForTimeout(600);
      const host = label === 'phone' ? '#hud-sheet' : '#hud-overlay';
      await page.evaluate(h => { const n = document.querySelector(h + ' .season-sec'); if (n) n.scrollIntoView(); }, host);
      await page.screenshot({ path: `${OUT}hud_season_${label}.png` });
      const txt = await page.locator(host).innerText();
      console.log(`hud ${label}: overlay has tension section = ${/Tension/.test(txt)}; ${txt.replace(/\s+/g, ' ').slice(0, 420)}`);
    }
    console.log(`hud ${label}: errors=${errors.length ? errors.join(' | ') : 'none'}`);
    await page.close();
    await ctx.close();
  }
  await browser.close();
})();
