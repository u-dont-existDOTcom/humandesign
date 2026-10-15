/* Browser delivery smoke: owner-readable audit, next protocol and local guide links. */
const fs = require('fs');
const path = require('path');
const assert = require('node:assert/strict');
const puppeteer = require(process.env.PUPPETEER_MODULE || 'puppeteer');

const downloads = process.argv[2];
if (!downloads) throw new Error('Downloads directory required');
const pages = [
  'AstroHD-V15-Structural-Null-Audit-2026-10-15.html',
  'AstroHD-V15-Next-Human-Test-2026-10-15.html',
  'Life-Patterns-Researcher-Guide.html'
];

(async () => {
  const browser = await puppeteer.launch({
    headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage']
  });
  try {
    let tested = 0;
    for (const file of pages) {
      const filepath = path.join(downloads, file);
      assert(fs.existsSync(filepath), 'Missing owner delivery ' + file);
      const page = await browser.newPage();
      const errs = [], requests = [];
      page.on('pageerror', err => errs.push(err.message));
      page.on('request', req => {
        if (!req.url().startsWith('file:')) requests.push(req.url());
      });
      await page.setViewport({width: 390, height: 844});
      await page.goto('file://' + filepath, {waitUntil:'load'});
      const body = await page.$eval('body', elem => elem.textContent);
      assert(body.length > 150 && (body.includes('AstroHD') || (file.includes('Researcher-Guide') && body.includes('first-place birth-date'))), 'Unexpected page '+file);
      assert.deepEqual(errs, []);
      assert.deepEqual(requests, []);
      if (file.includes('Structural-Null-Audit')) {
        assert(body.includes('956') && body.includes('1,037'));
        assert(await page.$eval('table', el=>el.rows.length) > 2);
      }
      if (file.includes('Researcher-Guide')) {
        assert(await page.$eval('body', elem =>
          [...elem.querySelectorAll('a')].some(
            a=>a.getAttribute('href') === 'AstroHD-V15-Structural-Null-Audit-2026-10-15.html'
          )));
      }
      await page.close();
      tested += 1;
    }
    console.log('PASS owner audit + prospective protocol + researcher guide; 3 readable local pages; no external calls or page errors');
  } finally {
    await browser.close();
  }
})().catch(err => { console.error(err); process.exitCode=1; });
