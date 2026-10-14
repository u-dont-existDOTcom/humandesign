/* Browser acceptance: synthetic V3 file, guided prompts, privacy and exact export. */
const fs=require('fs'),path=require('path'),os=require('os'),assert=require('assert');
const {execFileSync}=require('child_process');
const puppeteer=require(process.env.PUPPETEER_MODULE||'puppeteer');
const ROOT=path.resolve(__dirname,'../..');
const HTML=path.join(ROOT,'tasks/life-patterns-idiographic-20261010/LIFE_PATTERNS_V3_OFFLINE_PILOT.html');
const BANK=JSON.parse(fs.readFileSync(path.join(ROOT,'tasks/life-patterns-idiographic-20261010/tendency-first-v3-scaffold-development.json'),'utf8'));
const ROUTES=['TF1-G01','TF1-G02','TF1-G16','TF1-G23','TF1-M05','TF1-G20','TF1-M01','TF1-M03'];
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lp-guided-'));
const exportedName='my-life-patterns-v3-local-pilot.json';
function sourceData(){
 const answers=Object.fromEntries(BANK.questions.map((q,i)=>[
  q.id,{selected:i%2?[q.example_answer_paths[0]]:q.example_answer_paths.slice(0,4),
    other:'Synthetic prior answer for '+q.id,unsure:false,skip:false}
 ]));
 return {schema:'local_life_patterns_v3_pilot_unsubmitted',answers,unique_behaviors:[
  {behavior:'Sort bookmarks by topic.',context:'monthly',comparison:'friends',reason:'convenience'},
  {behavior:'Make a recipe calendar.',context:'weekly',comparison:'household',reason:'planning'},
  {behavior:'Catalogue books <img src=x onerror=alert(1)>.',context:'monthly',comparison:'neighbors',reason:'curiosity'}
 ]};
}
function writeJson(filename,data){const target=path.join(tmp,filename);fs.writeFileSync(target,JSON.stringify(data));return target;}
async function importSaved(page,file){
 await (await page.$('#import-file')).uploadFile(file);
 await page.waitForFunction(()=>document.getElementById('import-feedback').textContent.includes('Restored'),{timeout:8000});
}
async function download(page){
 const cdp=await page.target().createCDPSession();
 await cdp.send('Page.setDownloadBehavior',{behavior:'allow',downloadPath:tmp});
 const dest=path.join(tmp,exportedName);
 fs.rmSync(dest,{force:true});
 await page.click('#export');
 for(let i=0;i<70 && !fs.existsSync(dest);i++)await new Promise(r=>setTimeout(r,90));
 assert(fs.existsSync(dest),'No output JSON');
 await new Promise(r=>setTimeout(r,90));
 return JSON.parse(fs.readFileSync(dest,'utf8'));
}
async function currentRoute(page){return await page.$eval('#guided-count',e=>e.textContent);}
async function newPage(browser,file){
 const p=await browser.newPage();
 await p.setViewport({width:390,height:820});
 await p.goto('file://'+file,{waitUntil:'load',timeout:12000});
 return p;
}
(async()=>{
 const original=sourceData();const f=writeJson('synthetic-v3.json',original);
 const browser=await puppeteer.launch({headless:true,executablePath:process.env.CHROME_EXECUTABLE||undefined,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});
 try{
 const errors=[],external=[];
 const page=await newPage(browser,HTML);
 page.on('pageerror',e=>errors.push(e.message));
 page.on('request',r=>{if(!r.url().startsWith('file:'))external.push(r.url());});
 assert.strictEqual(await page.$eval('#guided-section',e=>e.hidden),true);
 await importSaved(page,f);
 assert.strictEqual(await page.$eval('#guided-section',e=>e.hidden),false);
 assert((await currentRoute(page)).includes('TF1-G01'));
 assert((await page.$eval('#guided-prior',e=>e.textContent)).includes(original.answers['TF1-G01'].other));
 assert.strictEqual(await page.$eval('#guided-overview',e=>e.textContent),'0 of 8 follow-ups addressed.');
 await page.type('#guided-rule','First I determine which fact is missing.');
 await page.type('#guided-example','When a timetable conflicted, I compared dates before testing other ideas.');
 await page.click('#guided-next');
 assert((await currentRoute(page)).includes('TF1-G02'));
 await page.click('#guided-no-default');await page.click('#guided-next');
 assert((await currentRoute(page)).includes('TF1-G16'));
 await page.click('#guided-skip');
 assert((await currentRoute(page)).includes('TF1-G23'));
 await page.type('#guided-rule','There is no universal thing I see first; context controls it.');
 await page.click('#guided-next');
 assert((await currentRoute(page)).includes('TF1-M05'));
 assert((await page.$eval('#guided-overview',e=>e.textContent)).includes('4 of 8'));
 const partial=await download(page);
 for(const id of Object.keys(original.answers)){
   assert.deepStrictEqual(partial.answers[id].selected,original.answers[id].selected,id);
   assert.strictEqual(partial.answers[id].other,original.answers[id].other,id);
 }
 assert.deepStrictEqual(partial.unique_behaviors,original.unique_behaviors);
 assert(partial.answers['TF1-G01'].context_rule.includes('which fact'));
 assert.strictEqual(partial.answers['TF1-G02'].no_stable_default,true);
 assert.strictEqual(partial.answers['TF1-G16'].context_skipped,true);
 // Reopening a partial export automatically begins at the first unresolved route.
 const partialFile=writeJson('synthetic-partial.json',partial);
 const reopened=await newPage(browser,HTML);
 await importSaved(reopened,partialFile);
 assert((await currentRoute(reopened)).includes('TF1-M05'));
 for(let i=0;i<4;i++){
  await reopened.click('#guided-no-default');
  await reopened.click('#guided-next');
 }
 assert.strictEqual(await reopened.$eval('#guided-active',e=>e.hidden),true);
 assert.strictEqual(await reopened.$eval('#guided-complete',e=>e.hidden),false);
 assert.strictEqual(await reopened.$eval('#guided-progress',e=>e.value),8);
 await reopened.click('#guided-review');
 assert((await currentRoute(reopened)).includes('TF1-G01'));
 assert((await reopened.$eval('#guided-rule',e=>e.value)).includes('which fact'));
 const after=await download(reopened);
 assert.strictEqual(Object.keys(after.answers).length,25);
 assert.deepStrictEqual(after.unique_behaviors,original.unique_behaviors);
 assert.strictEqual(after.answers['TF1-G16'].context_skipped,true);
 // A private prefilled HTML auto-starts the same flow without even choosing a file.
 const fullPrefilled=path.join(tmp,'prefilled.html');
 execFileSync('python3',[
  path.join(ROOT,'tasks/life-patterns-guided-followup-20261014/make_private_prefilled.py'),
  '--html',HTML,'--source',f,'--output',fullPrefilled],{stdio:'ignore'});
 const privatePage=await newPage(browser,fullPrefilled);
 assert((await currentRoute(privatePage)).includes('TF1-G01'));
 assert.strictEqual(await privatePage.$eval('#count',e=>e.textContent),'3 of 20');
 assert.strictEqual(await privatePage.$eval('#guided-section',e=>e.hidden),false);
 assert.strictEqual(fs.statSync(fullPrefilled).mode&0o777,0o600);
 // A previously completed context must not be asked again after import.
 const skipPrefilled={...original,answers:JSON.parse(JSON.stringify(original.answers))};
 skipPrefilled.answers['TF1-G01'].context_rule='Existing answer already supplied.';
 const already=writeJson('already.json',skipPrefilled);
 const loaded=await newPage(browser,HTML);
 await importSaved(loaded,already);
 assert((await currentRoute(loaded)).includes('TF1-G02'));
 assert.strictEqual(await loaded.$eval('#guided-overview',e=>e.textContent),'1 of 8 follow-ups addressed.');
 // No XSS or external data sharing from respondent text.
 assert.strictEqual(await privatePage.$$eval('#guided-prior img',l=>l.length),0);
 assert.deepStrictEqual(errors,[]);assert.deepStrictEqual(external,[]);
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
 assert.strictEqual(overflow,false);
 console.log(JSON.stringify({status:'PASS',queued:8,auto_after_import:true,one_at_a_time:true,respond_skip_resume:true,
  initial_saved_answers_preserved:25,unique_behaviors_preserved:3,private_prefill_starts_without_import:true,
  existing_context_skipped:true,completed_review_revisit:true,file_private:true,
  network_requests:0,js_errors:0,mobile_overflow:false}));
 }finally{await browser.close();fs.rmSync(tmp,{recursive:true,force:true});}
})().catch(e=>{console.error(e.stack);process.exit(1);});
