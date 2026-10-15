/* Private-owner prefill: test dimensions, not personal answer text. */
const fs=require('fs'),assert=require('node:assert/strict'),path=require('path');
const puppeteer=require(process.env.PUPPETEER_MODULE||'puppeteer');
const source=process.argv[2];if(!source||!fs.existsSync(source))throw Error('Missing private file');
(async()=>{
 const stats=fs.statSync(source);assert.equal(stats.mode&0o777,0o600);
 const browser=await puppeteer.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
 try{
  const page=await browser.newPage(),errors=[],external=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('request',r=>{if(!r.url().startsWith('file:'))external.push(r.url());});
  await page.goto('file://'+path.resolve(source),{waitUntil:'load'});
  assert.equal(await page.$eval('#route',e=>e.options.length),25);
  assert.equal(await page.$eval('#count',e=>e.textContent),'3 of 20');
  assert.equal(await page.$eval('#v32-route',e=>e.options.length),8);
  assert.equal(await page.$eval('#guided-overview',e=>e.textContent),'8 of 8 follow-ups addressed.');
  assert.equal(await page.$eval('#role-pattern',e=>e.value),'');
  assert(await page.$eval('#role-prior',e=>e.textContent.length)>60);
  assert(await page.$eval('#role-status',e=>e.textContent.includes('One or two sentences is enough')));
  assert.equal(await page.$eval('#role-details',e=>e.open),false);
  assert.equal(await page.$eval('body',e=>e.classList.contains('role-focus')),true);
  assert.equal(await page.evaluate(()=>document.activeElement?.id),'role-title');
  assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
  console.log('PASS: real private file; 25 prior answers, 8 guided details, 3 behaviors, 8 V3.2 prompts, no invented role choice, automatically shown missing role item, no remote calls/errors; file 0600');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
