"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||"playwright");
const root=path.resolve(__dirname,"../../apps/life-patterns-participant/participant");
const bank=JSON.parse(fs.readFileSync(path.join(root,"static/experience-meaning-v2.json"),"utf8"));
const questions=["CF003-ID-01","CF003-CENTRAL-01","CF003-PERIPH-01"]
  .map(question_id=>({question_id,question:"Synthetic prompt "+question_id}));
const state={status:"ready",review_summary:[],original_turn_count:3,clarification_count:1,
  cf003_questions:questions,csrf_token:"synthetic-csrf",experience_instrument:bank,submission:null};
const origin="https://life-patterns.example.invalid";

async function testJourney(context,optIn) {
  const page=await context.newPage();
  const unexpected=[],errors=[],submissions=[];
  page.on("pageerror",error=>errors.push(error.message));
  await page.route("**/*",async route=>{
    const req=route.request(),url=new URL(req.url()),pathname=url.pathname;
    if(url.origin!==origin){unexpected.push(url.href);return route.abort();}
    const files={
      "/finish":["static/finish.html","text/html"],
      "/assets/finish.js":["static/finish.js","text/javascript"],
      "/assets/experience.js":["static/experience.js","text/javascript"],
      "/assets/finish.css":["static/finish.css","text/css"]
    };
    if(files[pathname])return route.fulfill({status:200,
      body:fs.readFileSync(path.join(root,files[pathname][0])),
      contentType:files[pathname][1]});
    if(pathname==="/api/finish/state"&&req.method()==="GET")
      return route.fulfill({status:200,contentType:"application/json",body:JSON.stringify(state)});
    if(pathname==="/api/finish/submit"&&req.method()==="POST"){
      submissions.push(req.postDataJSON());
      return route.fulfill({status:200,contentType:"application/json",
        body:JSON.stringify({schema:"life-patterns-gpt-submission-receipt-v1",
          submission_id:"GPT-synthetic-only",stored_encrypted:true})});
    }
    unexpected.push(pathname);return route.abort();
  });
  await page.setViewportSize({width:375,height:812});
  await page.goto(origin+"/finish");
  await page.waitForSelector("#review-panel:not([hidden])");
  await page.locator("#confirm-review").check();
  await page.locator("#next-button").click();
  assert.equal(await page.locator("#questions-panel").isVisible(),true);
  assert.equal(await page.locator("#experience-optional").isVisible(),true);
  for(const question of questions){
    await page.locator('#cf003-items textarea[name="'+question.question_id+'"]')
      .fill("Synthetic example, not a participant answer.");
  }
  for(const [key,val] of [
    ["rising_sign_previously_known","no"],
    ["previous_natal_chart_reading","unsure"],
    ["target_information_exposure","prefer_not_to_say"]
  ])await page.locator('select[name="'+key+'"]').selectOption(val);
  if(optIn){
    await page.locator("#experience-opt-in").check();
    await page.locator("#experience-core-items > fieldset:first-child textarea")
      .fill("A note must not silently disappear if no rating is chosen.");
    await page.locator("#final-consent").check();
    await page.locator("#submit-button").click();
    assert.equal(submissions.length,0,"Note-only answer must not be silently dropped.");
    assert.match(await page.locator("#alert").innerText(),/Choose a response/);
    await page.locator('select[name="EM01-value"]').selectOption("most_days");
    await page.locator('select[name="EM01-typical"]').selectOption("strong");
    await page.locator('select[name="EM01-peak"]').selectOption("overwhelming");
    await page.locator('select[name="EM03-value"]').selectOption("never");
    await page.locator('select[name="EM04-value"]').selectOption("unknown");
    await page.locator('select[name="EM08-personal"]').selectOption("varies");
    await page.locator('select[name="EM08-contribution"]').selectOption("strong");
    await page.locator('input[name="experience-topic-EM06"]').check();
    await page.locator('select[name="EM06-value"]').selectOption("weekly");
    await page.locator('select[name="EM06-peak"]').selectOption("strong");
  }
  await page.locator("#final-consent").check();
  await page.locator("#submit-button").click();
  await page.waitForSelector("#done-panel:not([hidden])");
  assert.equal(submissions.length,1);
  assert.equal(submissions[0].answers.length,3);
  if(!optIn)assert.equal("experience_record" in submissions[0],false);
  else{
    const rec=submissions[0].experience_record;
    assert.equal(rec.research_use_consented,true);
    assert.equal(rec.status,"post_review_exploratory_not_scored");
    assert.deepEqual(rec.topics_selected,["EM06"]);
    assert.equal(rec.responses.length,8);
    const get=id=>rec.responses.find(r=>r.question_id===id);
    assert.deepEqual([get("EM01").value,get("EM01").typical_intensity,
      get("EM01").peak_intensity],["most_days","strong","overwhelming"]);
    assert.equal(get("EM03").state,"NEVER");
    assert.equal(get("EM04").state,"UNKNOWN");
    assert.equal(get("EM02").state,"NOT_ASKED");
    assert.equal(get("EM07").state,"NOT_ASKED");
    assert.equal(get("EM06").peak_intensity,"strong");
    assert.deepEqual(get("EM08").values,
      {personal_meaning:"varies",perceived_contribution:"strong"});
  }
  const width=await page.evaluate(()=>({viewport:document.documentElement.clientWidth,
    scroll:document.documentElement.scrollWidth}));
  assert.ok(width.scroll<=width.viewport+1,"Mobile page has horizontal overflow");
  assert.deepEqual(unexpected,[]);
  assert.deepEqual(errors,[]);
  await page.close();
  return {optIn,optionalRecord:"experience_record" in submissions[0],width};
}
(async()=>{
  const opts={headless:true,args:["--no-sandbox"]};
  if(process.env.PLAYWRIGHT_EXECUTABLE)opts.executablePath=process.env.PLAYWRIGHT_EXECUTABLE;
  const browser=await chromium.launch(opts);
  try{
    const ctx=await browser.newContext();
    const baseline=await testJourney(ctx,false);
    const optional=await testJourney(ctx,true);
    console.log("EXPERIENCE_FINISH_BROWSER_PASS",JSON.stringify({baseline,optional}));
    await ctx.close();
  }finally{await browser.close();}
})().catch(e=>{console.error(e.stack||e);process.exitCode=1;});
