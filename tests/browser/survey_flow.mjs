/** Local synthetic end-to-end tests. Refuses non-loopback service targets. */
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {existsSync} from 'node:fs';
import {mkdir,writeFile} from 'node:fs/promises';
const require=createRequire(import.meta.url);
const modulePath=process.env.PUPPETEER_MODULE || 'puppeteer';
const {default:puppeteer}=await import(modulePath.startsWith('/')?modulePath:require.resolve(modulePath));
const base=process.env.LIFE_PATTERNS_TEST_URL || 'http://127.0.0.1:18765';
assert(['localhost','127.0.0.1','[::1]'].includes(new URL(base).hostname),'Never run synthetic mutations against a live participant service.');
const output=process.env.LIFE_PATTERNS_TEST_OUTPUT || '/tmp/life-patterns-browser-results';
await mkdir(output,{recursive:true});
const browser=await puppeteer.launch({headless:true,executablePath:process.env.BROWSER_PATH||(existsSync('/usr/bin/brave-browser')?'/usr/bin/brave-browser':undefined),args:['--disable-dev-shm-usage']});
const report={schema:'life-patterns-browser-regressions-v1',live_model_calls:0,tests:[],widths:[],page_errors:[]};
let fault=null,held=null,count=0;
try{
 const page=await browser.newPage();await page.setViewport({width:1440,height:900});
 page.on('pageerror',e=>report.page_errors.push(String(e)));
 await page.setRequestInterception(true);
 page.on('request',async req=>{
   try{
     const path=new URL(req.url()).pathname;const data=req.postData()?JSON.parse(req.postData()):{};
     if(path.endsWith('/operations'))count++;
     if(fault==='restore'&&path.endsWith('/recovery'))return req.respond({status:404,contentType:'application/json',body:'{}'});
     if(fault==='restore'&&path.endsWith('/restore'))return req.respond({status:503,contentType:'application/json',body:'{"detail":"Synthetic restoration failure"}'});
     if(fault==='advance'&&data.kind==='advance'){fault=null;return req.respond({status:503,contentType:'application/json',body:'{"detail":"Synthetic next-question failure"}'});}
     if(fault==='answer'&&data.kind==='answer'){fault=null;return req.respond({status:503,contentType:'application/json',body:'{"detail":"Synthetic answer failure"}'});}
     if(fault==='lost-response'&&data.kind==='answer'){
       fault=null;await fetch(req.url(),{method:'POST',headers:{'content-type':'application/json'},body:req.postData()});
       return req.respond({status:503,contentType:'application/json',body:'{"detail":"Synthetic lost response after commit"}'});
     }
     if(fault==='delay-advance'&&data.kind==='advance'){fault=null;held=()=>req.continue();return;}
     await req.continue();
   }catch(e){report.page_errors.push('interception: '+e.message);if(!req.isInterceptResolutionHandled())await req.abort();}
 });
 const state=()=>page.evaluate(()=>({phase:lifePatternsClient.state.view?.phase,busy:lifePatternsClient.state.busy,
   pending:lifePatternsClient.state.pending,paused:lifePatternsClient.state.paused,error:lifePatternsClient.state.error,
   draft:lifePatternsClient.state.draft,revision:lifePatternsClient.state.view?.revision}));
 const visible=id=>page.$eval('#'+id,e=>!!e.getClientRects().length);
 const settle=()=>page.waitForFunction(()=>!lifePatternsClient.state.loading&&!lifePatternsClient.state.busy,{timeout:12000});
 const fresh=async()=>{fault=null;await page.goto(base);await settle();await page.evaluate(()=>{lifePatternsClient.state.restoreError=true;localStorage.clear()});await page.reload();await settle();};
 const send=async text=>{await page.$eval('#message',(e,t)=>{e.value=t;e.dispatchEvent(new Event('input',{bubbles:true}))},text);await page.click('#send');await settle();};
 const test=async(name,fn)=>{try{await fn();report.tests.push({name,status:'pass'});console.log('PASS',name);}catch(e){report.tests.push({name,status:'fail',error:e.stack});console.log('FAIL',name,e.message);await page.screenshot({path:output+'/'+name+'.png',fullPage:true});throw e;}};
 await test('initial-one-labeled-response',async()=>{await fresh();assert.equal(await page.$$eval('textarea',els=>els.length),1);assert.equal(await page.$eval('#messageLabel',e=>e.textContent),'Your response');assert.equal(await visible('finishForNow'),true);});
 await test('restore-failure-preserves-original-checkpoint',async()=>{
   const before=await page.evaluate(()=>localStorage.getItem('lifePatternsExactRecoveryV2'));
   fault='restore';await page.reload();await settle();assert.equal(await visible('errorArea'),true);
   assert.equal(await page.evaluate(()=>localStorage.getItem('lifePatternsExactRecoveryV2')),before);
   assert.equal(await visible('retryAction'),true);fault=null;await page.click('#retryAction');await settle();assert.equal((await state()).error,'');
 });
 await test('next-question-failure-exposes-retry',async()=>{
   fault='advance';await send('Please end this area.');assert.equal((await state()).pending.kind,'advance');
   assert.equal(await visible('errorArea'),true);assert.equal(await visible('retryAction'),true);
   await page.click('#retryAction');await settle();assert.equal((await state()).phase,'awaiting_answer');assert.equal((await state()).pending,null);
 });
 await test('failed-answer-retains-editable-draft-and-once-only-retry',async()=>{
   await fresh();fault='answer';await send('Keep this synthetic answer.');assert.equal((await state()).draft,'Keep this synthetic answer.');
   assert.equal(await page.$eval('#message',e=>e.value),'Keep this synthetic answer.');
   assert.equal(await page.evaluate(()=>lifePatternsClient.state.view.conversation.filter(r=>r.role==='user').length),0);
   await page.click('#retryAction');await settle();assert.equal((await state()).draft,'');
   assert.equal(await page.evaluate(()=>lifePatternsClient.state.view.conversation.filter(r=>r.role==='user').length),1);
 });
 await test('lost-response-reconciles-without-repeating-answer',async()=>{
   await fresh();fault='lost-response';await send('A response whose acknowledgement is lost.');
   const before=count;await page.click('#reconcileAction');await settle();assert.equal(count,before);assert.equal((await state()).pending,null);
   assert.equal(await page.evaluate(()=>lifePatternsClient.state.view.conversation.filter(r=>r.role==='user').length),1);
 });
 await test('double-send-is-single-flight',async()=>{
   await fresh();const before=count;
   await page.evaluate(()=>{lifePatternsClient.state.draft='One synthetic answer.';return Promise.all([lifePatternsClient.send(),lifePatternsClient.send()])});
   await settle();assert.equal(count-before,1);
 });
 await test('pause-late-response-reload-resume',async()=>{
   await fresh();fault='delay-advance';
   await page.$eval('#message',e=>{e.value='Please end this area.';e.dispatchEvent(new Event('input',{bubbles:true}))});await page.click('#send');
   for(let i=0;i<100&&!held;i++)await new Promise(r=>setTimeout(r,20));assert(held,'advance was intercepted');
   await page.click('#finishForNow');assert.equal(await visible('pausedPanel'),true);assert.equal(await visible('composer'),false);
   await held();held=null;await settle();assert.equal((await state()).phase,'paused');assert.equal(await visible('composer'),false);
   const before=count;await page.evaluate(()=>{lifePatternsClient.state.draft='Should not send while paused';return lifePatternsClient.send()});assert.equal(count,before);
   await page.reload();await settle();assert.equal((await state()).phase,'paused');assert.equal(await visible('resumeInterview'),true);
   await page.click('#resumeInterview');await settle();assert.equal((await state()).phase,'awaiting_answer');assert.equal(await visible('composer'),true);
 });
 await test('old-acceptance-cannot-replace-new-awaiting-question-on-restore',async()=>{
   await fresh();await send('A direct pattern: I think alone before group decisions.');
   assert.equal((await state()).phase,'awaiting_answer');
   const before=await page.evaluate(()=>lifePatternsClient.state.view.conversation.at(-1).text);
   const sid=await page.evaluate(()=>lifePatternsClient.state.view.session_id);await fetch(base+'/__test/drop/'+sid,{method:'POST'});
   await page.reload();await settle();assert.equal((await state()).phase,'awaiting_answer');assert.equal(await visible('composer'),true);
   assert.equal(await page.evaluate(()=>lifePatternsClient.state.view.conversation.at(-1).text),before);
 });
 await test('patterns-remain-visible-and-correction-is-append-only',async()=>{
   await page.$eval('#message',e=>{e.value='An unfinished ordinary answer.';e.dispatchEvent(new Event('input',{bubbles:true}))});
   await page.click('#viewPatterns');assert.equal(await page.$eval('#patternsDialog',e=>e.open),true);
   assert((await page.$eval('#patternsList',e=>e.textContent)).includes('Directly stated by you'));
   await page.click('#patternsList button');await send('Only with unfamiliar groups.');
   assert.equal(await page.$eval('#message',e=>e.value),'An unfinished ordinary answer.');
   assert.equal(await page.evaluate(()=>lifePatternsClient.state.view.patterns[0].status),'disputed');
   assert.equal(await page.evaluate(()=>lifePatternsClient.state.view.patterns[0].corrections[0].text),'Only with unfamiliar groups.');
 });
 await test('inference-judgment-is-distinct-and-auto-continues',async()=>{
   await fresh();await send('Please explore an inference.');assert.equal((await state()).phase,'synthesis_review');
   assert.equal(await visible('patternPanel'),true);assert.equal(await visible('composer'),true);
   await page.click('#accept');await settle();assert.equal((await state()).phase,'awaiting_answer');
   assert.equal(await page.evaluate(()=>lifePatternsClient.state.view.patterns[0].status),'accepted');
 });
 await test('no-worthwhile-question-does-not-fake-coverage',async()=>{
   await fresh();await send('There is no useful next distinction.');assert.equal((await state()).phase,'bounded');
   assert.equal(await page.$eval('#progressBar',e=>e.value),0);assert.equal(await visible('boundedPanel'),true);
 });
 await test('zero-pattern-freeze-has-source-and-blueprint',async()=>{
   await fresh();const sid=await page.evaluate(()=>lifePatternsClient.state.view.session_id);
   const data=await(await fetch(base+'/api/owner-v2/conversation/sessions/'+sid+'/measurement')).json();
   assert(data.blueprint_version&&data.blueprint_sha256);assert(data.evidence_archive.record);assert.equal(data.completed_results.length,0);
 });
 await test('responsive-and-reduced-motion',async()=>{
   await fresh();await page.emulateMediaFeatures([{name:'prefers-reduced-motion',value:'reduce'}]);
   for(const width of [320,375,414,768,1024,1440]){await page.setViewport({width,height:900});
     const geometry=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
       scrollBehavior:getComputedStyle(document.documentElement).scrollBehavior,label:document.getElementById('message').labels.length}));
     report.widths.push(geometry);assert.equal(geometry.scrollWidth,width);assert.equal(geometry.scrollBehavior,'auto');assert.equal(geometry.label,1);
   }
   await page.screenshot({path:output+'/desktop.png',fullPage:true});await page.setViewport({width:375,height:812});await page.screenshot({path:output+'/mobile.png',fullPage:true});
 });
 assert.equal(report.page_errors.length,0);report.status='pass';
} catch(e){report.status='fail';process.exitCode=1;}
finally{await writeFile(output+'/results.json',JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,tests:report.tests.length,errors:report.page_errors}));await browser.close();}
