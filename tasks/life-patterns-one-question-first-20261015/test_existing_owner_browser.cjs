/* Private V3.3 resume: all prior answers remain byte-equivalent after one-field UI repair. */
const fs=require('fs'),assert=require('node:assert/strict'),os=require('os'),path=require('path');
const puppeteer=require(process.env.PUPPETEER_MODULE||'puppeteer');
const html=process.argv[2],source=process.argv[3];
if(!html||!source)throw Error('Both private HTML and source required');
const old=JSON.parse(fs.readFileSync(source));
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'life-simple-'));
const output=path.join(temp,'my-life-patterns-v3-3-role-entry.json');
(async()=>{
 assert.equal(fs.statSync(html).mode&0o777,0o600);
 const browser=await puppeteer.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
 try {
  const page=await browser.newPage(),errors=[],network=[];
  await page.setViewport({width:390,height:844});
  page.on('pageerror',e=>errors.push(e.message));
  page.on('request',r=>{if(!r.url().startsWith('file:'))network.push(r.url());});
  await page.goto('file://'+path.resolve(html),{waitUntil:'load'});
  assert.equal(await page.$eval('#route',e=>e.options.length),25);
  assert.equal(await page.$eval('#count',e=>e.textContent),'3 of 20');
  assert.equal(await page.$eval('#guided-overview',e=>e.textContent),'8 of 8 follow-ups addressed.');
  assert.equal(await page.$eval('#role-pattern',e=>e.value),'context_dependent');
  assert.equal(await page.$eval('#role-details',e=>e.open),false);
  assert.equal(await page.$eval('body',e=>e.classList.contains('role-focus')),true);
  assert.equal(await page.$eval('#role-short',e=>e.value),'');
  assert(await page.$eval('#role-status',e=>e.textContent.includes('already saved')));
  assert(await page.$eval('#role-title',e=>e.textContent.includes('short question')));
  // No obligation to answer again; export old role response unchanged.
  const cdp=await page.target().createCDPSession();
  await cdp.send('Page.setDownloadBehavior',{behavior:'allow',downloadPath:temp});
  await page.click('#role-export');
  for(let i=0;i<50&&!fs.existsSync(output);i++)await new Promise(r=>setTimeout(r,75));
  assert(fs.existsSync(output));
  await new Promise(r=>setTimeout(r,100));
  const latest=JSON.parse(fs.readFileSync(output));
  assert.deepEqual(latest.answers,old.answers);
  assert.deepEqual(latest.unique_behaviors,old.unique_behaviors);
  assert.deepEqual(latest.v3_2_answers,old.v3_2_answers);
  const record={...latest.role_entry_review};delete record.summary;
  assert.deepEqual(record,old.role_entry_review);
  assert.equal(latest.role_entry_review.summary,'');
  await page.click('#role-show-existing');
  assert.equal(await page.$eval('body',e=>e.classList.contains('role-focus')),false);
  await page.click('#role-show-existing');
  assert.equal(await page.$eval('body',e=>e.classList.contains('role-focus')),true);
  assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
  console.log('PASS: real owner V3.3 answers retained, 3 episodes/one contextual code, 25 original answers, 8 guided contexts, 3 behaviors; no re-answer, one-field focus, lossless export, no network/errors');
 }finally{await browser.close();fs.rmSync(temp,{recursive:true,force:true});}
})().catch(e=>{console.error(e);process.exitCode=1;});
