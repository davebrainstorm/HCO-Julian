// Screenshot every .page element of an HTML file at a given scale, and print a PDF.
// usage: node pages.mjs in.html outdir prefix scale [pdfPath]
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'); const fs = require('fs');
const [,, input, outdir, prefix = 'page', scale = '2', pdf] = process.argv;
fs.mkdirSync(outdir, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: +scale });
await page.goto('file://' + path.resolve(input));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(200);
const faces = await page.evaluate(() => [...document.fonts].map(f => `${f.family}|${f.style}|${f.status}`));
const bad = faces.filter(f => f.endsWith('|error'));
const used = faces.filter(f => f.endsWith('|loaded'));
console.log('loaded faces:', used.join(', '));
console.log('font faces:', faces.length, 'not loaded:', bad.length ? bad.join(', ') : 'none');
const els = await page.$$('.page');
for (let i = 0; i < els.length; i++) {
  await els[i].screenshot({ path: path.join(outdir, `${prefix}-${String(i + 1).padStart(2, '0')}.png`) });
}
if (pdf) { await page.emulateMedia({ media: 'print' }); await page.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true }); console.log('pdf', pdf); }
await browser.close();
console.log('pages:', els.length);
