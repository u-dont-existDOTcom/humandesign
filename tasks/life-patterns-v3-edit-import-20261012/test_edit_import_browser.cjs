/* Deterministic local-only browser regression with entirely SYNTHETIC answers. */
const fs=require('fs');
const os=require('os');
const path=require('path');
const assert=require('assert');
const puppeteer=require(process.env.PUPPETEER_MODULE||'puppeteer');
const ROOT=path.resolve(__dirname,'../..');
const p=path.join(ROOT,'tasks/life-patterns-idiographic-20261010');
(async()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'life-patterns-ui-'));
 const v3=JSON.parse(fs.readFileSync(path.join(p,'tendency-first-v3-scaffold-development.json'),'utf8'));
 const answers=Object.fromEntries(v3.questions.map((q,i)=>[q.id,{selected:[q.example_answer_paths[i%4]],other:i%5===0?'Synthetic detail for '+q.id:'',unsure:false,skip:false}]));
 answers['TF1-G01'].selected=[...v3.questions.find(q=>q.id==='TF1-G01').example_answer_paths];
 const unique=[
  {behavior:'I inventory seed packets by printed lot number.',context:'weekly',comparison:'neighbors',reason:'organization',extra_synthetic_metadata:'preserve'},
  {behavior:'I write recipes backwards from serving time.',context:'weekends',comparison:'friends',reason:'planning'},
  {behavior:'I count birds <img src=x onerror=alert(1)>.',context:'mornings',comparison:'neighbors',reason:'curiosity'}
 ];
 const input={schema:'local_life_patterns_v3_pilot_unsubmitted',answers,unique_behaviors:unique};
 const fixture=path.join(dir,'synthetic-pilot.json');fs.writeFileSync(fixture,JSON.stringify(input));
 const browser=await puppeteer.launch({headless:true,executablePath:process.env.CHROME_EXECUTABLE||undefined,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage();const errors=[];const external=[];
  page.on('pageerror',err=>errors.push(err.message));
  page.on('request',req=>{if(!req.url().startsWith('file:'))external.push(req.url());});
  await page.setViewport({width:390,height:800});
  await page.goto('file://'+(process.env.PILOT_HTML_PATH||path.join(p,'LIFE_PATTERNS_V3_OFFLINE_PILOT.html')),{waitUntil:'load',timeout:12000});
  assert.strictEqual(await page.$$eval('#route option',l=>l.length),25);
  let confirmations=[];let permission=false;
  page.on('dialog',async dialog=>{confirmations.push(dialog.message());if(permission)await dialog.accept();else await dialog.dismiss();});
  // Import all 25 answers plus 3 detailed unusual behaviors.
  let upload=await page.$('#import-file');await upload.uploadFile(fixture);
  await page.waitForFunction(()=>document.getElementById('import-feedback').textContent.includes('Restored 25 question answers'));
  assert.strictEqual(await page.$eval('#count',e=>e.textContent),'3 of 20');
  assert.strictEqual(await page.$$eval('#options input:checked',l=>l.length),1);
  await page.select('#route','TF1-G01');
  assert((await page.$eval('#selected-summary',e=>e.textContent)).includes('All four examples selected'));
  assert.strictEqual(await page.$$eval('#unique-list img',l=>l.length),0);
  await page.select('#route','TF1-G17');
  const expectedG17=answers['TF1-G17'].selected[0];
  assert.strictEqual(await page.$eval('#options input:checked',e=>e.value),expectedG17);
  // An editing session loads all saved attributes; Cancel retains original.
  await page.click('#unique-list li:nth-child(2) button[aria-label^="Edit"]');
  assert.strictEqual(await page.$eval('#context',e=>e.value),'weekends');
  assert.strictEqual(await page.$eval('#reason',e=>e.value),'planning');
  assert.strictEqual(await page.$eval('#add',e=>e.textContent),'Save changes');
  await page.focus('#behavior');await page.keyboard.down('Control');await page.keyboard.press('KeyA');await page.keyboard.up('Control');await page.keyboard.type('Changed but canceled');
  await page.click('#cancel-edit');
  assert.strictEqual(await page.$eval('#unique-list li:nth-child(2) span',e=>e.textContent),unique[1].behavior);
  // Edit a pre-existing imported item and preserve its position and remaining items.
  await page.click('#unique-list li:nth-child(2) button[aria-label^="Edit"]');
  await page.focus('#behavior');await page.keyboard.down('Control');await page.keyboard.press('KeyA');await page.keyboard.up('Control');await page.keyboard.type('I test a new recipe on weekends.');
  await page.focus('#context');await page.keyboard.down('Control');await page.keyboard.press('KeyA');await page.keyboard.up('Control');await page.keyboard.type('every second weekend');
  await page.click('#add');
  assert.strictEqual(await page.$eval('#unique-list li:nth-child(2) span',e=>e.textContent),'I test a new recipe on weekends.');
  assert.strictEqual(await page.$eval('#unique-list li:nth-child(3) span',e=>e.textContent),unique[2].behavior);
  // Destructive Clear and Reset must both be explicitly declined without loss.
  permission=false;await page.click('#clear');await page.click('#reset');
  assert.strictEqual(await page.$eval('#count',e=>e.textContent),'3 of 20');
  assert(confirmations.length>=2);
  // Malformed import never clobbers the restored data.
  fs.writeFileSync(path.join(dir,'invalid.json'),JSON.stringify({schema:'not-compatible',answers:{},unique_behaviors:[]}));
  upload=await page.$('#import-file');await upload.uploadFile(path.join(dir,'invalid.json'));
  await page.waitForFunction(()=>document.getElementById('import-feedback').textContent.includes('Import failed'));
  assert.strictEqual(await page.$eval('#count',e=>e.textContent),'3 of 20');
  // When a modified state exists, an import requires deliberate approval.
  upload=await page.$('#import-file');await upload.uploadFile(fixture);
  await page.waitForFunction(()=>document.getElementById('import-feedback').textContent.includes('Import canceled'));
  assert.strictEqual(await page.$eval('#unique-list li:nth-child(2) span',e=>e.textContent),'I test a new recipe on weekends.');
  // Reimport after consent restores all source details.
  permission=true;upload=await page.$('#import-file');await upload.uploadFile(fixture);
  await page.waitForFunction(()=>document.getElementById('import-feedback').textContent.includes('Restored 25 question answers'));
  assert.strictEqual(await page.$eval('#unique-list li:nth-child(2) span',e=>e.textContent),unique[1].behavior);
  // Re-edit, and use the normal export button to prove the updated JSON roundtrip.
  await page.click('#unique-list li:nth-child(1) button[aria-label^="Edit"]');
  await page.focus('#reason');await page.keyboard.down('Control');await page.keyboard.press('KeyA');await page.keyboard.up('Control');await page.keyboard.type('new planning rationale');
  await page.click('#add');
  const cdp=await page.target().createCDPSession();
  await cdp.send('Page.setDownloadBehavior',{behavior:'allow',downloadPath:dir});
  await page.click('#export');
  const file=path.join(dir,'my-life-patterns-v3-local-pilot.json');
  for(let i=0;i<40&&!fs.existsSync(file);i++) await new Promise(resolve=>setTimeout(resolve,125));
  assert(fs.existsSync(file),'Exported local JSON file missing');
  const output=JSON.parse(fs.readFileSync(file,'utf8'));
  assert.deepStrictEqual(output.answers,answers);
  assert.strictEqual(output.unique_behaviors.length,3);
  assert.strictEqual(output.unique_behaviors[0].reason,'new planning rationale');
  assert.strictEqual(output.unique_behaviors[0].extra_synthetic_metadata,'preserve');
  assert.deepStrictEqual(output.unique_behaviors.slice(1),unique.slice(1));
  if(process.env.PRIVATE_PILOT_JSON){
   const realFile=process.env.PRIVATE_PILOT_JSON;
   const original=JSON.parse(fs.readFileSync(realFile,'utf8'));
   permission=true;
   upload=await page.$('#import-file');await upload.uploadFile(realFile);
   await new Promise(resolve=>setTimeout(resolve,400));
   const privateImportStatus=await page.$eval('#import-feedback',e=>e.textContent);
   assert(privateImportStatus.includes('Restored 25 question answers'),'Private source import did not complete: '+privateImportStatus);
   assert.strictEqual(await page.$eval('#count',e=>e.textContent),String(original.unique_behaviors.length)+' of 20');
   fs.rmSync(file,{force:true});await page.click('#export');
   for(let i=0;i<40&&!fs.existsSync(file);i++)await new Promise(resolve=>setTimeout(resolve,125));
   assert(fs.existsSync(file),'Private source export check file missing');
   const roundtripped=JSON.parse(fs.readFileSync(file,'utf8'));
   assert(JSON.stringify(roundtripped.answers)===JSON.stringify(original.answers),'Private question answers changed during roundtrip.');
   assert(JSON.stringify(roundtripped.unique_behaviors)===JSON.stringify(original.unique_behaviors),'Private unusual behaviors changed during roundtrip.');
   console.log('PRIVATE_SOURCE_ROUNDTRIP_PASS: 25 complete questions and '+original.unique_behaviors.length+' unique behaviors, no private text printed.');
  }
  const mobileOverflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
  assert.strictEqual(mobileOverflow,false);
  assert.deepStrictEqual(errors,[]);assert.deepStrictEqual(external,[]);
  console.log(JSON.stringify({status:'PASS',imported_question_answers:25,imported_unique_behaviors:3,edit_cancel:true,edit_save:true,reimport_confirm_gate:true,malformed_import_rejected:true,roundtrip_export:true,unknown_metadata_preserved:true,external_requests:0,page_errors:0,mobile_overflow:false}));
 } finally{await browser.close();fs.rmSync(dir,{recursive:true,force:true});}
})().catch(e=>{console.error(e.stack);process.exit(1);});
