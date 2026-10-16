/* Real local browser flow; synthetic participant/one-time link only. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const puppeteer = require(process.env.PUPPETEER_MODULE || "puppeteer");

(async () => {
  const url = fs.readFileSync(process.argv[2], "utf8").trim();
  if (!/^http:\/\/127\.0\.0\.1:\d+\/finish#token=/.test(url)) {
    throw new Error("Only the localhost synthetic link may be exercised.");
  }
  const expectedOrigin = new URL(url).origin;
  const browser = await puppeteer.launch({
    headless: true, args: ["--no-sandbox", "--disable-dev-shm-usage"]
  });
  try {
    for (const width of [390, 1280]) {
      const page = await browser.newPage();
      await page.setViewport({width, height: 920});
      const pageErrors = [];
      const externalRequests = [];
      page.on("pageerror", error => pageErrors.push(error.message));
      page.on("request", request => {
        if (!request.url().startsWith(expectedOrigin)) externalRequests.push(request.url());
      });
      if (width === 390) {
        await page.goto(url, {waitUntil: "networkidle0"});
      } else {
        // A one-time token cannot be redeemed by a second browser. Test the
        // static responsive rendering without accidentally reusing it.
        await page.goto(expectedOrigin + "/finish", {waitUntil: "load"});
      }
      await page.waitForSelector(".shell");
      const overflow = await page.evaluate(() =>
        document.documentElement.scrollWidth > window.innerWidth
      );
      assert.equal(overflow, false, "Horizontal overflow on " + width);
      if (width === 390) {
        await page.waitForFunction(() => !document.getElementById("review-panel").hidden,
          {timeout: 15000});
        assert.equal(new URL(page.url()).hash, "", "Link token remained in address");
        const source = await page.$eval("#review-items", el => el.textContent);
        assert(source.includes("<img src=x onerror="), "Synthetic malicious quote not visible");
        assert.equal(await page.$$("img").then(items => items.length), 0,
          "Participant evidence was interpreted as unsafe HTML");
        await page.click("#confirm-review");
        await page.click("#next-button");
        assert.equal(await page.$eval("#questions-panel", el => el.hidden), false);
        await page.evaluate(() => {
          document.querySelectorAll("#cf003-items textarea").forEach((textarea, index) => {
            textarea.value = "Synthetic answer number " + (index + 1);
            textarea.dispatchEvent(new Event("input", {bubbles: true}));
          });
          document.querySelectorAll("#finish-form select").forEach(select => {
            select.value = "unsure";
            select.dispatchEvent(new Event("change", {bubbles: true}));
          });
        });
        await page.click("#final-consent");
        await page.click("#submit-button");
        await page.waitForFunction(() => !document.getElementById("done-panel").hidden,
          {timeout: 15000});
        const receipt = await page.$eval("#receipt-text", el => el.textContent);
        assert(receipt.includes("GPT-"), "No real synthetic encrypted receipt");
        await page.reload({waitUntil: "networkidle0"});
        await page.waitForFunction(() => !document.getElementById("done-panel").hidden);
        assert.equal(await page.$eval("#done-panel", el => el.hidden), false);
      }
      assert.deepEqual(pageErrors, [], "Browser JS errors");
      assert.deepEqual(externalRequests, [], "Unapproved external network requests");
      await page.close();
    }
    console.log("PASS synthetic encrypted browser finish: mobile, desktop, exact review, XSS-safe, CF003, receipt, refresh, no external calls");
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
