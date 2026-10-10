const fs = require('fs');
const assert = require('assert');
const path = require('path');
const puppeteer = require(process.env.PUPPETEER_MODULE || 'puppeteer');
(async () => {
 const browser=await puppeteer.launch({executablePath:process.env.CHROME_EXECUTABLE || undefined,headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
 try {
  const page=await browser.newPage();
  const errors=[]; const network=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('request',q=>{if(!q.url().startsWith('file://')) network.push(q.url());});
  await page.setViewport({width:400,height:770});
  await page.goto('file://'+path.resolve(__dirname,'LIFE_PATTERNS_V3_OFFLINE_PILOT.html'),{waitUntil:'load',timeout:10000});
  const initial=await page.evaluate(()=>({q:document.getElementById('question-text').textContent,options:document.querySelectorAll('#options input').length,routeCount:document.querySelectorAll('#route option').length,overflow:document.documentElement.scrollWidth>window.innerWidth}));
  assert.strictEqual(initial.routeCount,25);assert.strictEqual(initial.options,4);assert(initial.q.includes('enjoy spending time alone'));assert(!initial.overflow);
  await page.select('#route','TF1-STATUS');
  const recognition=await page.evaluate(()=>({question:document.getElementById('question-text').textContent,choices:document.getElementById('options').textContent}));
  assert(recognition.question.toLowerCase().includes('recognition'));assert(!recognition.choices.toLowerCase().includes('laptop'));
  await page.type('#behavior','I arrange stationery by a rule I chose.');
  await page.click('#add');
  const count=await page.$eval('#count',e=>e.textContent);
  assert.strictEqual(count,'1 of 20');
  assert.deepStrictEqual(errors,[]);assert.deepStrictEqual(network,[]);
  console.log(JSON.stringify({status:'PASS',route_count:initial.routeCount,first_question_rendered:true,recognition_scoped:true,unique_list_add:true,mobile_horizontal_overflow:false,external_requests:0,script_errors:0}));
 } finally {await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1);});
