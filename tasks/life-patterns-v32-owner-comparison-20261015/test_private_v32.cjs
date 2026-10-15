/* Private owner prefill smoke test. Does not print any personal answer or identifier. */
const fs=require('fs'),assert=require('assert'),path=require('path');
const puppeteer=require(process.env.PUPPETEER_MODULE||'puppeteer');
const filename=process.argv[2];
if(!filename){console.error('Usage: node test_private_v32.cjs /absolute/private/file.html');process.exit(2);}
(async()=>{
 const stat=fs.statSync(filename);assert.strictEqual(stat.mode&0o777,0o600);
 const browser=await puppeteer.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
 try{
  const page=await browser.newPage(),errors=[],network=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('request',r=>{if(!r.url().startsWith('file:'))network.push(r.url());});
  await page.goto('file://'+path.resolve(filename),{waitUntil:'load'});
  assert.strictEqual(await page.$eval('#route',e=>e.options.length),25);
  assert.strictEqual(await page.$eval('#v32-route',e=>e.options.length),8);
  assert.strictEqual(await page.$eval('#count',e=>e.textContent),'3 of 20');
  assert((await page.$eval('#import-feedback',e=>e.textContent)).includes('saved pilot answers were loaded privately'));
  assert.strictEqual(await page.$eval('#guided-overview',e=>e.textContent),'8 of 8 follow-ups addressed.');
  assert(await page.$eval('#v32-old',e=>e.textContent.length)>70);
  assert((await page.$eval('#v32-progress',e=>e.textContent)).startsWith('0 of 8'));
  assert.deepStrictEqual(errors,[]);assert.deepStrictEqual(network,[]);
  console.log('PASS: prefilled V3.2 private source imports all 25 originals, 8 contexts, 3 behavior items; 0 V3.2 answers invented; mode 0600; 0 script errors or requests');
 }finally{await browser.close();}
})().catch(err=>{console.error(err);process.exitCode=1;});
