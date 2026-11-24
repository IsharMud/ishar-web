const { chromium } = require('playwright');
const OUT = __dirname + '/';
(async () => {
  const browser = await chromium.launch();
  for (const [w, label] of [[390, 'phone'], [1280, 'desktop']]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
    const page = await ctx.newPage();
    await page.goto('http://127.0.0.1:8765/connect/?demo=1', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);
    // A real pointer tap on the pill, as a player would do it.
    await page.locator('.v-tension').first().click();
    await page.waitForTimeout(500);
    const open = await page.evaluate(() => {
      const ov = document.getElementById('hud-overlay'), sh = document.getElementById('hud-sheet');
      return { overlay: ov && !ov.hidden, sheet: sh && !sh.hidden };
    });
    console.log(label, 'after tap:', JSON.stringify(open));
    await page.screenshot({ path: `${OUT}hud_tension_${label}.png` });
    await ctx.close();
  }
  await browser.close();
})();
