/* Actual browser/API pilot using fabricated records and a local server only. */
const fs = require("fs");
const assert = require("node:assert/strict");
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || "playwright");

(async () => {
  const fixture = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  assert.match(fixture.origin, /^http:\/\/127\.0\.0\.1:\d+$/);
  const browser = await chromium.launch({headless:true});
  const report = {schema:"shared-evidence-browser-pilot-v1", synthetic_only:true, checks:[], errors:[], external_requests:[]};
  async function start(index, viewport={width:1280,height:1000}) {
    const context = await browser.newContext({viewport});
    const page = await context.newPage();
    page.on("pageerror", error => report.errors.push(error.message));
    page.on("request", request => {
      if (!request.url().startsWith(fixture.origin)) report.external_requests.push(request.url());
    });
    await page.goto(fixture.links[index]);
    await page.locator("#confirm-review").check();
    await page.locator("#next-button").click();
    const areas = page.locator("#cf003-items textarea");
    for (let i=0;i<3;i++) await areas.nth(i).fill("  Synthetic final answer " + i + ".  ");
    for (const name of ["rising_sign_previously_known","previous_natal_chart_reading","target_information_exposure"]) {
      await page.locator('select[name="'+name+'"]').selectOption("unsure");
    }
    await page.locator("#final-consent").check();
    return {context,page};
  }
  async function submit(page) {
    const response = page.waitForResponse(r => r.url().endsWith("/api/finish/submit"));
    await page.locator("#submit-button").click();
    const r = await response;
    return {status:r.status(),body:await r.json()};
  }
  try {
    const first = await start(0);
    let saved = await submit(first.page);
    assert.equal(saved.status,200);
    assert.equal(saved.body.shared_evidence_record_sha256,undefined);
    report.checks.push("Decline-all preserves ordinary final submission");
    await first.context.close();

    const second = await start(1,{width:375,height:812});
    const page = second.page;
    await page.locator("#shared-opt-in").check();
    const topics=page.locator("#shared-topic-options input");
    for(let i=0;i<5;i++) await topics.nth(i).check();
    assert.equal(await topics.nth(5).isDisabled(),true);
    for(let i=0;i<5;i++) await topics.nth(i).uncheck();
    await page.locator('input[name="shared-topic-VOCATION"]').check();
    await page.locator('input[name="shared-topic-STATUS"]').check();
    await page.locator("#shared-start").click();
    // The frozen source order places VOCATION before STATUS.
    const raw="  I coordinated a volunteer team from around 2018-09-14 at 08:30.\nI preferred sharing decisions.  ";
    await page.locator("#shared-answer").fill(raw);
    await page.locator("#shared-next").click();
    await page.locator("#shared-state").selectOption("ALREADY_COVERED");
    await page.locator("#shared-source").selectOption("/shared/sittings/0/responses/0/answer_text");
    await page.locator("#shared-next").click();
    let record=await page.evaluate(()=>window.LifePatternsSharedEvidence.collect());
    assert.equal(record.sittings[0].responses[0].answer_text,raw);
    assert.equal(record.sittings[0].responses[1].source_quote,raw);
    report.checks.push("Five-topic limit, exact whitespace/date capture and earlier shared-answer reuse");
    await page.locator("#shared-details summary").click();
    await page.locator("#shared-detail-options").selectOption("probe|EP-LEADERSHIP-HISTORY|VOCATION");
    await page.locator("#shared-detail-reason").fill("I have not distinguished responsibility from preference.");
    await page.locator("#shared-detail-start").click();
    await page.locator("#shared-answer").fill("The work was informal and unpaid; I usually preferred sharing the role.");
    await page.locator("#shared-next").click();
    await page.locator("#shared-more").click();
    assert.equal(await page.locator('input[name="shared-topic-VOCATION"]').isDisabled(),true);
    await page.locator('input[name="shared-topic-DREAM"]').check();
    await page.locator("#shared-start").click();
    await page.locator("#shared-feedback").fill("I prefer not to discuss this topic.");
    await page.locator("#shared-stop").click();
    record=await page.evaluate(()=>window.LifePatternsSharedEvidence.collect());
    assert.equal(record.sittings.length,2);
    assert.equal(record.sittings[1].responses[0].state,"SKIPPED");
    assert.deepEqual(record.sittings[1].responses[0].process_feedback,["I prefer not to discuss this topic."]);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth),true);
    saved=await submit(page);
    assert.equal(saved.status,200,JSON.stringify(saved.body));
    assert.match(saved.body.shared_evidence_record_sha256,/^[a-f0-9]{64}$/);
    await page.reload();
    await page.locator("#done-panel").waitFor({state:"visible"});
    report.checks.push("Justified probe, voluntary second sitting, skip feedback and 375px layout");
    report.checks.push("Real final storage and reload receipt");
    await second.context.close();

    const third=await start(2);
    const repair=third.page;
    await repair.locator("#shared-opt-in").check();
    await repair.locator('input[name="shared-topic-DREAM"]').check();
    await repair.locator("#shared-start").click();
    await repair.locator("#shared-state").selectOption("ALREADY_COVERED");
    await repair.locator("#shared-source").selectOption("/cf003/turns/0/answer_text");
    await repair.locator("#shared-next").click();
    const changed="  Corrected synthetic final answer.  ";
    await repair.locator("#cf003-items textarea").nth(0).fill(changed);
    const rejected=await submit(repair);
    assert.equal(rejected.status,422);
    assert.equal(await repair.locator("#cf003-items textarea").nth(0).inputValue(),changed);
    await repair.getByText("Review or edit these optional drafts",{exact:true}).click();
    await repair.getByRole("button",{name:"Edit this draft",exact:true}).click();
    await repair.locator("#shared-source").selectOption("/cf003/turns/0/answer_text");
    await repair.locator("#shared-next").click();
    const fixed=await repair.evaluate(()=>window.LifePatternsSharedEvidence.collect());
    assert.equal(fixed.sittings[0].responses[0].source_quote,changed);
    const accepted=await submit(repair);
    assert.equal(accepted.status,200,JSON.stringify(accepted.body));
    report.checks.push("Stale source rejected without data loss; draft reference repaired and submitted");
    await third.context.close();

    const fourth=await start(3);
    const reused=fourth.page;
    await reused.locator("#experience-opt-in").check();
    await reused.locator('select[name="EM03-value"]').selectOption("never");
    const note="  No such experience in the past year.\nEarlier years were different.  ";
    const experienceItem=reused.locator('fieldset.experience-item').filter({has:reused.locator('select[name="EM03-value"]')});
    await experienceItem.locator("textarea").fill(note);
    const unfinished=reused.locator('fieldset.experience-item').filter({has:reused.locator('select[name="EM01-value"]')}).locator("textarea");
    await unfinished.fill("  An unfinished independent optional draft.  ");
    await reused.locator("#shared-opt-in").check();
    await reused.locator('input[name="shared-topic-DREAM"]').check();
    await reused.locator("#shared-start").click();
    assert.equal(await unfinished.inputValue(),"  An unfinished independent optional draft.  ");
    await reused.locator("#shared-state").selectOption("ALREADY_COVERED");
    await reused.locator("#shared-source").selectOption("/experience/responses/2/note");
    await reused.locator("#shared-next").click();
    await unfinished.fill("");
    const reusedRecords=await reused.evaluate(()=>({
      experience:window.LifePatternsExperience.collect(),
      shared:window.LifePatternsSharedEvidence.collect(),
    }));
    assert.equal(reusedRecords.experience.responses[2].note,note);
    assert.equal(reusedRecords.shared.sittings[0].responses[0].source_quote,note);
    const bothSaved=await submit(reused);
    assert.equal(bothSaved.status,200,JSON.stringify(bothSaved.body));
    assert.match(bothSaved.body.experience_record_sha256,/^[a-f0-9]{64}$/);
    assert.match(bothSaved.body.shared_evidence_record_sha256,/^[a-f0-9]{64}$/);
    report.checks.push("Separately consented experience note reused with exact whitespace in both stored addenda");
    await fourth.context.close();
    assert.deepEqual(report.errors,[]);
    assert.deepEqual(report.external_requests,[]);
    report.status="PASS";
    fs.writeFileSync(process.argv[3],JSON.stringify(report,null,2)+"\n");
    console.log(JSON.stringify(report));
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
