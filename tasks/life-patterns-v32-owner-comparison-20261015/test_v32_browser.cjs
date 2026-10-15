/* Browser check: original V3 is preserved, V3.2 is separately versioned. */
const fs=require('fs'),path=require('path'),os=require('os'),assert=require('assert');
const puppeteer=require(process.env.PUPPETEER_MODULE||'puppeteer');
const ROOT=path.resolve(__dirname,'../..');
const HTML=path.join(__dirname,'LIFE_PATTERNS_V32_OFFLINE_PILOT.html');
const BANK=JSON.parse(fs.readFileSync(path.join(ROOT,'tasks/life-patterns-idiographic-20261010/tendency-first-v3-scaffold-development.json')));
const REV=JSON.parse(fs.readFileSync(path.join(ROOT,'tasks/life-patterns-guided-eight-assessment-20261015/V3_2_COGNITIVE_QUESTION_CANDIDATES.json')));
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lp-v32-'));
const savedName=path.join(temp,'my-life-patterns-v3-2-local-pilot.json');
const generated={
 schema:'local_life_patterns_v3_pilot_unsubmitted',
 answers:Object.fromEntries(BANK.questions.map((q,i)=>[q.id,{
  selected:q.example_answer_paths.slice(0,i%4+1),
  other:'Synthetic original V3 answer '+q.id,
  unsure:false,skip:false,
  ...(['TF1-G01','TF1-G02','TF1-G16','TF1-G23','TF1-M05','TF1-G20','TF1-M01','TF1-M03'].includes(q.id)
   ? {context_rule:'Original prior decision '+q.id,recent_case:'Prior example '+q.id,no_stable_default:false,context_skipped:false}:{})
 }])),
 unique_behaviors:[
  {behavior:'Catalog spare parts.',context:'monthly',comparison:'colleagues',reason:'utility'},
  {behavior:'Compare travel options.',context:'weekly',comparison:'friends',reason:'cost'},
  {behavior:'Use paper schedules.',context:'weekly',comparison:'family',reason:'simplicity'}
 ]
};
fs.writeFileSync(path.join(temp,'prior.json'),JSON.stringify(generated));
async function importFile(page,file){
 await (await page.$('#import-file')).uploadFile(file);
 await page.waitForFunction(()=>document.querySelector('#import-feedback').textContent.includes('Restored'),{timeout:9000});
}
async function exported(page){
 const cdp=await page.target().createCDPSession();
 await cdp.send('Page.setDownloadBehavior',{behavior:'allow',downloadPath:temp});
 fs.rmSync(savedName,{force:true});
 await page.click('#v32-export');
 for(let i=0;i<70&&!fs.existsSync(savedName);i++)await new Promise(r=>setTimeout(r,80));
 assert(fs.existsSync(savedName),'Expected new V3.2 download');
 await new Promise(r=>setTimeout(r,130));
 return JSON.parse(fs.readFileSync(savedName));
}
(async()=>{
 const browser=await puppeteer.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
 const allErrors=[],network=[];
 async function newPage(){
  const page=await browser.newPage();
  page.on('pageerror',e=>allErrors.push(e.message));
  page.on('request',r=>{if(!r.url().startsWith('file:'))network.push(r.url());});
  await page.setViewport({width:390,height:844});
  await page.goto('file://'+HTML,{waitUntil:'load'});
  return page;
 }
 try{
  const page=await newPage();
  assert.strictEqual(await page.$eval('#v32-route',e=>e.options.length),8);
  assert((await page.$eval('#v32-question',e=>e.textContent)).includes(REV.items[0].candidate_question));
  await importFile(page,path.join(temp,'prior.json'));
  assert((await page.$eval('#v32-old',e=>e.textContent)).includes('Original prior decision TF1-G01'));
  assert((await page.$eval('#guided-overview',e=>e.textContent)).includes('8 of 8'));
  await page.type('#v32-response','V32 synthetic new episode, different from the old response.');
  await page.click('#v32-next');
  assert.strictEqual(await page.$eval('#v32-route',e=>e.value),'TF1-G02');
  await page.click('#v32-no-event');
  await page.select('#v32-route','TF1-M05');
  assert((await page.$eval('#v32-purpose',e=>e.textContent)).includes('scoring suspended'));
  await page.click('#v32-skip');
  const changed=await exported(page);
  assert.strictEqual(changed.schema,'local_life_patterns_v3_2_pilot_unsubmitted');
  assert.deepStrictEqual(changed.answers,generated.answers);
  assert.deepStrictEqual(changed.unique_behaviors,generated.unique_behaviors);
  assert(changed.v3_2_answers['TF1-G01'].response.includes('different from the old'));
  assert(changed.v3_2_answers['TF1-G02'].no_event);
  assert(changed.v3_2_answers['TF1-M05'].skip);
  assert.strictEqual(Object.keys(changed.v3_2_answers).length,3);
  await page.close();
  const p2=await newPage();await importFile(p2,savedName);
  assert((await p2.$eval('#v32-response',e=>e.value)).includes('different from the old'));
  assert((await p2.$eval('#v32-progress',e=>e.textContent)).includes('3 of 8'));
  assert.strictEqual(await p2.$eval('#count',e=>e.textContent),'3 of 20');
  assert.strictEqual(await p2.$eval('#route',e=>e.options.length),25);
  // Original V3 questions and unusual behaviors remain editable after V3.2 import.
  await p2.select('#route','TF1-G01');
  assert((await p2.$eval('#other',e=>e.value)).includes('Synthetic original V3 answer TF1-G01'));
  await p2.close();
  assert.deepStrictEqual(allErrors,[]);
  assert.deepStrictEqual(network,[]);
  console.log('PASS: 8 revised prompts; 25 legacy answers and 3 behaviors unchanged; V3.2 independent export/re-import; edited source accessible; 0 external requests; 0 errors');
 }finally{await browser.close();fs.rmSync(temp,{recursive:true,force:true});}
})().catch(e=>{console.error(e);process.exitCode=1;});
