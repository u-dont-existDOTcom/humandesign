/* Synthetic only, local browser, both answer and end-questions routes. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const puppeteer = require(process.env.PUPPETEER_MODULE || "puppeteer");

(async () => {
  const link = fs.readFileSync(process.argv[2], "utf8").trim();
  const mode = process.argv[3];
  assert(["answer", "close", "legacy"].includes(mode));
  assert(/^http:\/\/127\.0\.0\.1:\d+\/finish#token=/.test(link));
  const origin = new URL(link).origin;
  const browser = await puppeteer.launch({
    headless: true, args: ["--no-sandbox", "--disable-dev-shm-usage"]
  });
  try {
    const page = await browser.newPage();
    await page.setViewport({width: 390, height: 900});
    const errors = [], external = [];
    page.on("pageerror", error => errors.push(error.message));
    page.on("request", request => {
      if (!request.url().startsWith(origin)) external.push(request.url());
    });
    await page.goto(link, {waitUntil: "networkidle0"});
    await page.waitForFunction(() => !document.getElementById("progress-panel").hidden);
    assert.equal(new URL(page.url()).hash, "", "Link token persisted in URL");
    assert(await page.$eval("#review-count", el => el.textContent.includes("earlier responses")));
    if (mode === "answer" || mode === "legacy") {
      await page.waitForFunction(() => !document.getElementById("clarification-panel").hidden);
      assert((await page.$eval("#clarification-panel", el => el.textContent)).includes("in this batch"));
      await page.$eval("#clarification-items textarea", el => {
        el.value = "I first check what matters to me.";
        el.dispatchEvent(new Event("input", {bubbles: true}));
      });
      await page.click("#save-clarifications");
    } else {
      await page.click("#close-ack");
      await page.click("#close-questions");
      await page.waitForFunction(() =>
        document.getElementById("review-stage-message").textContent.includes("No further clarification questions"));
    }
    // No GPT message or manual refresh: the browser checks Railway itself.
    await page.waitForFunction(
      () => !document.getElementById("review-panel").hidden,
      {timeout: 49000}
    );
    assert.equal(await page.$eval("#review-panel", el => el.hidden), false);
    assert.equal(await page.$eval("#clarification-panel", el => el.hidden), true);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.click("#confirm-review");
    await page.click("#next-button");
    await page.evaluate(() => {
      document.querySelectorAll("#cf003-items textarea").forEach((el, i) => {
        el.value = "Synthetic response " + (i + 1);
      });
      document.querySelectorAll("#finish-form select").forEach(select => {
        select.value = "unsure";
      });
    });
    await page.click("#final-consent");
    await page.click("#submit-button");
    await page.waitForFunction(() => !document.getElementById("done-panel").hidden);
    assert((await page.$eval("#receipt-text", el => el.textContent)).includes("GPT-"));
    await page.reload({waitUntil: "networkidle0"});
    await page.waitForFunction(() => !document.getElementById("done-panel").hidden);
    assert.deepEqual(errors, []);
    assert.deepEqual(external, []);
    console.log("PASS synthetic early Railway " + mode +
      ": saved review, autonomous progress, three final questions, encrypted receipt, refresh.");
  } finally {
    await browser.close();
  }
})().catch(e => {console.error(e); process.exitCode = 1;});
