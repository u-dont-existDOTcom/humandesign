/* V3.3 actual browser acceptance: neutral role question, versioned export, zero network. */
const fs=require('fs'),path=require('path'),os=require('os'),assert=require('node:assert/strict');
const puppeteer=require(process.env.PUPPETEER_MODULE||'puppeteer');
const ROOT=path.resolve(__dirname,'../..');
const FILE=path.join(__dirname,'LIFE_PATTERNS_V33_ROLE_ENTRY_OFFLINE_PILOT.html');
const BANK=JSON.parse(fs.readFileSync(path.join(ROOT,'tasks/life-patterns-idiographic-20261010/tendency-first-v3-scaffold-development.json')));
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'role-entry-'));
const exportFile=path.join(temp,'my-life-patterns-v3-3-role-entry.json');
const routes=['TF1-G01','TF1-G02','TF1-G16','TF1-G23','TF1-M05','TF1-G20','TF1-M01','TF1-M03'];
const prior={schema:'local_life_patterns_v3_2_pilot_unsubmitted',
 answers:Object.fromEntries(BANK.questions.map((q,i)=>[q.id,{
  selected:q.example_answer_paths.slice(0,1+(i%4)),
  other:'Synthetic original response '+q.id,skip:false,unsure:false,
  ...(routes.includes(q.id)?{context_rule:'Synthetic context '+q.id,recent_case:'Example '+q.id,
   no_stable_default:false,context_skipped:false}:{})
 }])),
 unique_behaviors:[
  {behavior:'Use paper receipts',context:'weekly',comparison:'family',reason:'planning'},
  {behavior:'Track garden weather',context:'monthly',comparison:'friends',reason:'curiosity'},
  {behavior:'Test recipe ratios',context:'weekly',comparison:'friends',reason:'consistency'}
 ],
 v3_2_answers:{'TF1-G16':{response:'Synthetic motivation example',no_event:false,skip:false}}
};
fs.writeFileSync(path.join(temp,'source-v32.json'),JSON.stringify(prior));
function errorsOn(page,errors,network){
 page.on('pageerror',e=>errors.push(e.message));
 page.on('request',r=>{if(!r.url().startsWith('file:'))network.push(r.url());});
}
async function newPage(browser,errors,network){
 const page=await browser.newPage();await page.setViewport({width:390,height:844});
 errorsOn(page,errors,network);await page.goto('file://'+FILE,{waitUntil:'load'});return page;
}
async function importJson(page,file){
 await (await page.$('#import-file')).uploadFile(file);
 await page.waitForFunction(()=>document.getElementById('import-feedback').textContent.includes('Restored'),{timeout:8500});
}
async function exportJson(page){
 const cdp=await page.target().createCDPSession();
 await cdp.send('Page.setDownloadBehavior',{behavior:'allow',downloadPath:temp});
 fs.rmSync(exportFile,{force:true});
 await page.click('#role-export');
 for(let i=0;i<70&&!fs.existsSync(exportFile);i++)await new Promise(r=>setTimeout(r,70));
 assert(fs.existsSync(exportFile),'Expected V3.3 JSON export');
 await new Promise(r=>setTimeout(r,95));
 return JSON.parse(fs.readFileSync(exportFile,'utf8'));
}
(async()=>{
 const browser=await puppeteer.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
 const errors=[],network=[];
 try{
  const page=await newPage(browser,errors,network);
  assert.equal(await page.$eval('#role-entry-section',e=>e.hidden),false);
  assert.equal(await page.$eval('#role-pattern',e=>e.options.length),7);
  assert.equal(await page.$eval('#role-origin-0',e=>e.options.length),8);
  const head=await page.$eval('#role-entry-section',e=>e.textContent);
  assert(!/astrology|V1.4d|lilly|recognition_entry|birth date|#1/.test(head.toLowerCase()),
         'Chart/answer key must not be visible in respondent role prompt');
  await importJson(page,path.join(temp,'source-v32.json'));
  assert((await page.$eval('#role-prior',e=>e.textContent)).includes('Synthetic original response TF1-G06'));
  assert((await page.$eval('#guided-overview',e=>e.textContent)).startsWith('8 of 8'));
  assert.equal(await page.$eval('#role-pattern',e=>e.value),'');
  // Simple answer is sufficient with all supplementary detail collapsed.
  assert.equal(await page.$eval('#role-details',e=>e.open),false);
  assert.equal(await page.$eval('body',e=>e.classList.contains('role-focus')),true);
  await page.type('#role-short','I sometimes offer help and sometimes do not; it depends.');
  const short=await exportJson(page);
  assert(short.role_entry_review.summary.includes('sometimes offer help'));
  assert.equal(short.role_entry_review.episodes.filter(e=>e.origin||e.example).length,0);
  assert.deepEqual(short.answers,prior.answers);
  await page.click('#role-details > summary');
  await page.type('#role-case-0','I volunteered to handle the supplies.');
  await page.select('#role-origin-0','self_initiated');
  await page.type('#role-case-1','A colleague asked me to coordinate a meeting.');
  await page.select('#role-origin-1','invited_unprompted');
  await page.select('#role-origin-2','offer_only');
  await page.select('#role-pattern','context_dependent');
  await page.type('#role-conditions','Depends on team and responsibility.');
  let saved=await exportJson(page);
  assert.equal(saved.schema,'local_life_patterns_v3_3_pilot_unsubmitted');
  assert.deepEqual(saved.answers,prior.answers);
  assert.deepEqual(saved.unique_behaviors,prior.unique_behaviors);
  assert.deepEqual(saved.v3_2_answers,prior.v3_2_answers);
  assert.equal(saved.role_entry_review.episodes[0].origin,'self_initiated');
  assert.equal(saved.role_entry_review.episodes[1].origin,'invited_unprompted');
  assert.equal(saved.role_entry_review.episodes[2].origin,'offer_only');
  assert.equal(saved.role_entry_review.pattern,'context_dependent');
  assert(saved.role_entry_review.summary.includes('depends.'));
  await page.close();

  const restored=await newPage(browser,errors,network);
  await importJson(restored,exportFile);
  assert.equal(await restored.$eval('#role-pattern',e=>e.value),'context_dependent');
  assert.equal(await restored.$eval('#role-details',e=>e.open),false);
  assert((await restored.$eval('#role-short',e=>e.value)).includes('sometimes offer'));
  assert((await restored.$eval('#role-case-1',e=>e.value)).includes('colleague'));
  assert.equal(await restored.$eval('#count',e=>e.textContent),'3 of 20');
  assert.equal(await restored.$eval('#v32-route',e=>e.options.length),8);
  await restored.close();

  const malicious=JSON.parse(JSON.stringify(saved));
  malicious.role_entry_review.episodes[0].origin='invited_you_will_rank_first';
  fs.writeFileSync(path.join(temp,'tampered.json'),JSON.stringify(malicious));
  const reject=await newPage(browser,errors,network);
  await (await reject.$('#import-file')).uploadFile(path.join(temp,'tampered.json'));
  await reject.waitForFunction(()=>document.getElementById('import-feedback').textContent.includes('Import failed'));
  assert.equal(await reject.$eval('#role-pattern',e=>e.value),'');
  await reject.close();

  const empty=await newPage(browser,errors,network);
  await importJson(empty,path.join(temp,'source-v32.json'));
  await empty.click('#role-skip');
  const declined=await exportJson(empty);
  assert.equal(declined.role_entry_review.skip,true);
  assert.deepEqual(declined.answers,prior.answers);
  await empty.close();
  assert.deepEqual(errors,[]);
  assert.deepEqual(network,[]);
  console.log('PASS: V3.3 role-entry prompt, neutral labels, 25 prior answers, 8 guided contexts, V3.2 answers, 3 behaviors preserved; input/save/export/reimport/skip/tamper-rejection; 0 network/errors');
 }finally{await browser.close();fs.rmSync(temp,{recursive:true,force:true});}
})().catch(e=>{console.error(e);process.exitCode=1;});
