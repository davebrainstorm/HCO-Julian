// QA: screenshot pages, log console errors, horizontal overflow and font status. usage: node qa.mjs <outdir> <width> <height> [theme] [pages...]
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const [,, outdir, w = '1440', h = '900', theme = 'dark', ...list] = process.argv;
fs.mkdirSync(outdir, { recursive: true });
const pages = list.length ? list : fs.readdirSync('../../review/hco').filter(f => f.endsWith('.html'));
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1, reducedMotion: 'reduce', ignoreHTTPSErrors: true });
await ctx.addInitScript(t => { try { localStorage.setItem('gw-theme', t); } catch (e) {} }, theme);
const FONTDIR = '../fonts-ofl/instrumentsans/';
await ctx.route('https://fonts.googleapis.com/**', r => r.fulfill({ contentType: 'text/css', headers: { 'Access-Control-Allow-Origin': '*' }, body: `@font-face{font-family:'Instrument Sans';src:url('https://fonts.gstatic.com/qa/roman.ttf') format('truetype');font-weight:400 700;font-stretch:75% 100%;font-style:normal}@font-face{font-family:'Instrument Sans';src:url('https://fonts.gstatic.com/qa/italic.ttf') format('truetype');font-weight:400 700;font-stretch:75% 100%;font-style:italic}` }));
await ctx.route('https://fonts.gstatic.com/qa/**', r => r.fulfill({ contentType: 'font/ttf', headers: { 'Access-Control-Allow-Origin': '*' }, body: fs.readFileSync(FONTDIR + (r.request().url().includes('italic') ? 'InstrumentSans-Italic[wdth,wght].ttf' : 'InstrumentSans[wdth,wght].ttf')) }));
for (const p of pages) {
  const page = await ctx.newPage(); const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  page.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  page.on('requestfailed', r => errs.push('REQFAIL ' + r.url().slice(0, 100)));
  await page.goto('http://127.0.0.1:8765/' + p, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(400);
  const info = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, h: document.documentElement.scrollHeight,
    fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.stretch).slice(0, 3) }));
  await page.screenshot({ path: `${outdir}/${p.replace('.html', '')}.png`, fullPage: true });
  console.log(p, `h=${info.h}`, info.sw > info.cw ? `OVERFLOW ${info.sw}>${info.cw}` : 'ok', info.fonts.length ? 'fonts:' + info.fonts.join('|') : 'NO WEBFONT', errs.length ? 'ERR ' + errs.join(' ; ').slice(0, 300) : '');
  await page.close();
}
await browser.close();
