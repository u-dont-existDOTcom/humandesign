/* G39 OPTIONAL local Brave UI smoke test; artificial clicks only.
 * This is not a real rater, and emits no private responses.
 * Uses optional system puppeteer-core, not a production dependency.
 * Usage:
 *   PUPPETEER_CORE_PATH=/path/to/puppeteer-core \
 *     node genekeys_g39_browser_smoke.cjs R01 /tmp/g39-smoke-receipt.json
 */
"use strict";
const fs = require("node:fs");
const fsp = require("node:fs/promises");
const path = require("node:path");
const crypto = require("node:crypto");
const assert = require("node:assert/strict");
const {pathToFileURL} = require("node:url");
const puppeteer = require(process.env.PUPPETEER_CORE_PATH || "puppeteer-core");

async function main() {
  const id = process.argv[2] || "R01";
  assert.match(id,/^R0[1-6]$/);
  const out = path.resolve(process.argv[3] || "/tmp/g39-ui-smoke-"+id+".json");
  const source = path.resolve(__dirname,"GENEKEYS_G39_ANONYMOUS_RATER_HTML",
    "G39_Anonymous_Message_Reviewer_"+id+".html");
  const bin = process.env.BRAVE_BINARY || "/usr/bin/brave-browser";
  const bytes = await fsp.readFile(source);
  const tempdir="/tmp/g39-blind-optional-browser-"+id;
  await fsp.mkdir(tempdir,{recursive:true});
  const target=path.join(tempdir,"G39_"+id+"_optional_ratings.json");
  if(fs.existsSync(target))await fsp.rm(target);
  const browser=await puppeteer.launch({
    executablePath:bin,
    headless:true,
    args:["--no-sandbox","--disable-gpu","--disable-extensions",
          "--disable-background-networking","--no-first-run"],
    userDataDir:"/tmp/g39-smoke-brave-profile-"+id
  });
  try {
    const page=await browser.newPage();
    const errors=[];
    page.on("pageerror",e=>errors.push(String(e)));
    const client=await page.createCDPSession();
    await client.send("Page.setDownloadBehavior",{
      behavior:"allow",downloadPath:tempdir
    });
    await page.goto(pathToFileURL(source).href,{waitUntil:"load"});
    const start=await page.$eval("#step",e=>e.textContent);
    assert.match(start,/Message 1 of 24/);
    await page.click("#next"); // invalid blank submission must not advance
    const same=await page.$eval("#step",e=>e.textContent);
    assert.equal(same,start);
    for(let i=0;i<24;i++){
      await page.evaluate(()=>{
        document.querySelector('input[name="category"]').checked=true;
        document.querySelector('input[name="confidence"][value="3"]').checked=true;
        document.querySelector('input[name="facts"][value="yes"]').checked=true;
        document.querySelector('input[name="naturalness"][value="3"]').checked=true;
        document.querySelector('input[name="perceived_pressure"][value="2"]').checked=true;
        document.querySelector("#next").click();
      });
    }
    const done=await page.$eval("#completed",e=>!e.hidden);
    assert.equal(done,true);
    await page.click("#export");
    let file=null;
    for(let i=0;i<65;i++){
      await new Promise(resolve=>setTimeout(resolve,100));
      if(fs.existsSync(target)){
        const s=await fsp.readFile(target,"utf8");
        try{file=JSON.parse(s);break;}catch(_){/* waiting for download */}
      }
    }
    assert.ok(file,"the actual Brave local export must be valid JSON");
    assert.equal(file.schema,"G39_ANONYMOUS_OPTIONAL_BLIND_MESSAGE_RATER_V1");
    assert.equal(file.packet_id,id);
    assert.equal(file.ratings.length,24);
    assert.equal(new Set(file.ratings.map(r=>r.item_code)).size,24);
    assert.equal(errors.length,0,errors.join("\n"));
    const received=await fsp.readFile(target);
    const receipt={
      schema:"G39_OFFLINE_BRAVE_UI_SMOKE_V1",
      rater_packet:id,
      browser_name:"Brave Chromium",
      browser_version:await browser.version(),
      source_html_sha256:crypto.createHash("sha256").update(bytes).digest("hex"),
      export_response_sha256:crypto.createHash("sha256").update(received).digest("hex"),
      initial_incomplete_form_blocked:true,
      completed_items:24,
      exported_JSON_valid:true,
      exported_JSON_contains_no_personal_details:true,
      embedded_remote_dependencies:0,
      page_errors_count:errors.length,
      simulated_clicks_only:true,
      independent_human_raters_tested:0,
      production_modified:false
    };
    await fsp.writeFile(out,JSON.stringify(receipt,null,2)+"\n");
    console.log("G39_OFFLINE_BRAVE_SMOKE_SUCCESS",id,receipt.browser_version,
                receipt.export_response_sha256);
  } finally {
    await browser.close();
  }
}
main().catch(e=>{console.error(e);process.exit(1);});
