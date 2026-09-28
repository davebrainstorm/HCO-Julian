// Render a local HTML file to PNG (screenshot) or PDF using Playwright/Chromium.
// usage: node render.mjs in.html out.png|out.pdf [widthPx heightPx] [scale]
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const [,, input, out, w = '1600', h = '1000', scale = '1'] = process.argv;
const path = require('path');
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +scale });
await page.goto('file://' + path.resolve(input));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(150);
const bad = await page.evaluate(() => [...document.fonts].filter(f => f.status !== 'loaded').map(f => f.family + ' ' + f.status));
if (bad.length) console.error('FONT NOT LOADED:', bad.join(', '));
if (out.endsWith('.pdf')) {
  await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
} else {
  await page.screenshot({ path: out, fullPage: true });
}
await browser.close();
console.log('wrote', out);
