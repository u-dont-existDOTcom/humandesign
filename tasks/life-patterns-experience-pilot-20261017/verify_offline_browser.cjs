"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const {pathToFileURL} = require("node:url");
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || "playwright");
(async () => {
  const root = __dirname;
  const launch = {headless:true,args:["--no-sandbox"]};
  if (process.env.PLAYWRIGHT_EXECUTABLE) launch.executablePath = process.env.PLAYWRIGHT_EXECUTABLE;
  const browser = await chromium.launch(launch);
  try {
    const context = await browser.newContext({acceptDownloads:true});
    const page = await context.newPage();
    const requests = [], errors=[];
    page.on("request", x => {if(!x.url().startsWith("file:")) requests.push(x.url());});
    page.on("pageerror", error=>errors.push(error.message));
    await page.goto(pathToFileURL(path.join(root,"EXPERIENCE-MEANING-PILOT-v1.html")).href);
    assert.equal(await page.locator("#question-panel").isHidden(),true);
    await page.locator("#begin").click();
    assert.match(await page.locator("#progress").innerText(), /1 of 4/i);
    await page.locator("#primary-answer").selectOption("never");
    await page.locator("#save").click();
    assert.match(await page.locator("#progress").innerText(), /2 of 4/i);
    await page.locator("#primary-answer").selectOption("weekly");
    await page.locator("#intensity").selectOption("strong");
    await page.locator("#save").click();
    await page.locator("#unknown").click();
    await page.locator("#personal_meaning").selectOption("strong");
    await page.locator("#perceived_contribution").selectOption("none");
    await page.locator("#save").click();
    assert.equal(await page.locator("#topics").isVisible(),true);
    await page.locator('#topic-options input[value="EM06"]').check();
    await page.locator('#topic-options input[value="EM07"]').check();
    await page.locator("#topics-done").click();
    assert.match(await page.locator("#progress").innerText(), /1 of 2/i);
    await page.locator("#primary-answer").selectOption("never");
    await page.locator("#save").click();
    await page.locator("#primary-answer").selectOption("once_twice");
    await page.locator("#intensity").selectOption("noticeable");
    await page.locator("#save").click();
    assert.equal(await page.locator("#complete").isVisible(),true);
    let downloadEvent=page.waitForEvent("download");
    await page.locator("#export").click();
    let download=await downloadEvent;
    let data=JSON.parse(fs.readFileSync(await download.path(),"utf8"));
    const get=id=>data.responses.find(x=>x.question_id===id);
    assert.equal(get("EM01").state,"NEVER");
    assert.deepEqual([get("EM03").value,get("EM03").intensity],["weekly","strong"]);
    assert.equal(get("EM04").state,"UNKNOWN");
    assert.deepEqual(get("EM08").values,{personal_meaning:"strong",perceived_contribution:"none"});
    assert.equal(get("EM06").state,"NEVER");
    assert.equal(get("EM07").intensity,"noticeable");
    assert.equal(get("EM02").state,"NOT_ASKED");
    assert.equal(get("EM05").state,"NOT_ASKED");
    await page.locator("#review-select").selectOption("EM04");
    await page.locator("#edit").click();
    await page.locator("#primary-answer").selectOption("once_twice");
    await page.locator("#save").click();
    downloadEvent=page.waitForEvent("download");
    await page.locator("#export").click();
    download=await downloadEvent;
    data=JSON.parse(fs.readFileSync(await download.path(),"utf8"));
    assert.equal(data.responses.find(x=>x.question_id==="EM04").value,"once_twice");
    const next=await context.newPage();
    next.on("request", x=>{if(!x.url().startsWith("file:"))requests.push(x.url());});
    next.on("pageerror",x=>errors.push(x.message));
    await next.goto(pathToFileURL(path.join(root,"EXPERIENCE-MEANING-PILOT-v1.html")).href);
    await next.locator("#import").setInputFiles({name:"export.json",mimeType:"application/json",buffer:Buffer.from(JSON.stringify(data))});
    assert.equal(await next.locator("#complete").isVisible(),true);
    assert.match(await next.locator("#import-message").innerText(), /Imported successfully/);
    await next.locator("#review-select").selectOption("EM03");
    await next.locator("#edit").click();
    assert.equal(await next.locator("#primary-answer").inputValue(),"weekly");
    assert.equal(await next.locator("#intensity").inputValue(),"strong");
    await next.setViewportSize({width:375,height:812});
    const viewport = await next.evaluate(() => ({
      width:document.documentElement.clientWidth,
      content_width:document.documentElement.scrollWidth
    }));
    assert.ok(viewport.content_width <= viewport.width + 1, "Mobile page has horizontal overflow");
    if (process.env.PILOT_BROWSER_SCREENSHOT) {
      await next.screenshot({path:process.env.PILOT_BROWSER_SCREENSHOT});
    }
    if (process.env.PILOT_OWNER_PACKET_PATH) {
      const packet=JSON.parse(fs.readFileSync(process.env.PILOT_OWNER_PACKET_PATH,"utf8"));
      assert.equal(packet.schema,"life-patterns-owner-source-packet-v1");
      const ownerPage=await context.newPage();
      ownerPage.on("request", x=>{if(!x.url().startsWith("file:"))requests.push(x.url());});
      ownerPage.on("pageerror", x=>errors.push(x.message));
      await ownerPage.goto(pathToFileURL(path.join(root,"EXPERIENCE-MEANING-PILOT-v1.html")).href);
      await ownerPage.locator("#import").setInputFiles(process.env.PILOT_OWNER_PACKET_PATH);
      assert.match(await ownerPage.locator("#import-message").innerText(),/3 previous survey files/);
      assert.equal(await ownerPage.locator("#question-panel").isHidden(),true,"Import must not bypass opt-in.");
      await ownerPage.locator("#begin").click();
      assert.match(await ownerPage.locator("#prior-count").textContent(),/116/);
      await ownerPage.locator("#prior-context summary").click();
      await ownerPage.locator("#prior-search").fill("TF1-A0");
      assert.ok(await ownerPage.locator(".prior-match").count()>=1);
      await ownerPage.locator(".prior-match button").first().click();
      assert.equal(await ownerPage.locator("#earlier-source").inputValue(),"latest_v33:TF1-A0");
      assert.match(await ownerPage.locator("#progress").innerText(),/1 of 4/i,
        "Inserting a reference must not auto-mark a new experience answer as covered.");
      await ownerPage.locator("#primary-answer").selectOption("never");
      await ownerPage.locator("#save").click();
      await ownerPage.locator("#skip").click();
      await ownerPage.locator("#unknown").click();
      await ownerPage.locator("#personal_meaning").selectOption("strong");
      await ownerPage.locator("#perceived_contribution").selectOption("not_answered");
      await ownerPage.locator("#save").click();
      await ownerPage.locator("#topics-done").click();
      const ownerDownloadEvent=ownerPage.waitForEvent("download");
      await ownerPage.locator("#export").click();
      const ownerDownload=await ownerDownloadEvent;
      const ownerData=JSON.parse(fs.readFileSync(await ownerDownload.path(),"utf8"));
      assert.equal(ownerData.prior_sources.length,3);
      for(let i=0;i<3;i++) assert.equal(ownerData.prior_sources[i].text,packet.sources[i].text,
        "Round trip must preserve every complete original source text.");
      assert.equal(ownerData.responses.find(x=>x.question_id==="EM01").state,"NEVER");
      assert.equal(ownerData.responses.find(x=>x.question_id==="EM02").state,"NOT_ASKED");
      assert.equal(ownerData.responses.find(x=>x.question_id==="EM04").state,"UNKNOWN");
      assert.equal(ownerData.responses.find(x=>x.question_id==="EM08").values.perceived_contribution,
        "not_answered");
      const ownerResumed=await context.newPage();
      await ownerResumed.goto(pathToFileURL(path.join(root,"EXPERIENCE-MEANING-PILOT-v1.html")).href);
      await ownerResumed.locator("#import").setInputFiles({name:"owner-reimport.json",mimeType:"application/json",
        buffer:Buffer.from(JSON.stringify(ownerData))});
      assert.match(await ownerResumed.locator("#import-message").innerText(),/Imported successfully/);
      assert.equal(await ownerResumed.locator("#complete").isVisible(),true);
      await ownerResumed.locator("#review-select").selectOption("EM01");
      await ownerResumed.locator("#edit").click();
      assert.match(await ownerResumed.locator("#prior-count").textContent(),/116/);
      await ownerPage.close();
      await ownerResumed.close();
    }
    assert.deepEqual(requests,[],"Offline page attempted external requests");
    assert.deepEqual(errors,[],"Browser reported script error");
    console.log("BROWSER_SMOKE_PASS",JSON.stringify({core:4,selected_optional:2,verified_states:8,export:true,edit:true,import:true,mobile_width:viewport.width,mobile_content:viewport.content_width,network_requests:requests.length,script_errors:errors.length}));
    await context.close();
  } finally {await browser.close();}
})().catch(e => { console.error(e.stack||e); process.exitCode=1; });
