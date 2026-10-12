/* Offline-only behavioral coding test. No real user responses in fixtures. */
const fs=require('fs'); const path=require('path');const os=require('os');const assert=require('assert');
const puppeteer=require(process.env.PUPPETEER_MODULE||'puppeteer');
const ROOT=path.resolve(__dirname,'../..');
(async()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lp-context-v4-'));
 const p=path.join(ROOT,'tasks/life-patterns-idiographic-20261010');
 const survey=JSON.parse(fs.readFileSync(path.join(p,'tendency-first-v3-scaffold-development.json'),'utf8'));
 const answers=Object.fromEntries(survey.questions.map(q=>[q.id,{selected:[q.example_answer_paths[0]],other:'',unsure:false,skip:false}]));
 answers['TF1-G04'].selected=[...survey.questions.find(q=>q.id==='TF1-G04').example_answer_paths];
 const original={schema:'local_life_patterns_v3_pilot_unsubmitted',answers,unique_behaviors:[{behavior:'I sort receipts by weekday.',context:'monthly',comparison:'friends',reason:'organization'}]};
 const source=path.join(tmp,'source.json');fs.writeFileSync(source,JSON.stringify(original));
 const browser=await puppeteer.launch({headless:true,executablePath:process.env.CHROME_EXECUTABLE||undefined,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});
 try{
 const page=await browser.newPage(),requests=[],errors=[];
 page.on('request',r=>{if(!r.url().startsWith('file:'))requests.push(r.url());});page.on('pageerror',e=>errors.push(e.message));
 await page.setViewport({width:390,height:820});
 await page.goto('file://'+path.join(p,'LIFE_PATTERNS_V3_OFFLINE_PILOT.html'),{waitUntil:'load',timeout:15000});
 await (await page.$('#import-file')).uploadFile(source);
 await page.waitForFunction(()=>document.getElementById('import-feedback').textContent.includes('Restored 25'),{timeout:7000});
 await page.select('#route','TF1-G04');
 assert.strictEqual(await page.$eval('#context-probe',e=>e.open),true);
 await page.select('#route','TF1-G20');
 for(const checkbox of await page.$$('#options input')){if(!(await checkbox.evaluate(el=>el.checked)))await checkbox.click();}
 assert.strictEqual(await page.$eval('#context-probe',e=>e.open),true);
 await page.select('#route','TF1-G04');
 assert((await page.$eval('#context-probe-prompt',e=>e.textContent)).includes('troubleshooting'));
 await page.type('#context-rule','The evidence of the failure determines which method I try.');
 await page.type('#recent-case','For a synthetic broken link, I tested the URL before changing browsers.');
 await page.click('#no-stable-default');
 await page.select('#route','TF1-G23');
 assert((await page.$eval('#context-probe-prompt',e=>e.textContent)).includes('unfamiliar group'));
 await page.select('#route','TF1-G04');
 assert.strictEqual(await page.$eval('#context-rule',e=>e.value),'The evidence of the failure determines which method I try.');
 assert.strictEqual(await page.$eval('#no-stable-default',e=>e.checked),true);
 const cdp=await page.target().createCDPSession(); await cdp.send('Page.setDownloadBehavior',{behavior:'allow',downloadPath:tmp});
 await page.click('#export');
 const target=path.join(tmp,'my-life-patterns-v3-local-pilot.json');
 for(let i=0;i<80&&!fs.existsSync(target);i++)await new Promise(r=>setTimeout(r,80));
 assert(fs.existsSync(target));
 const updated=JSON.parse(fs.readFileSync(target,'utf8'));
 assert.deepStrictEqual(updated.answers['TF1-G04'].selected,original.answers['TF1-G04'].selected);
 assert.deepStrictEqual(updated.unique_behaviors,original.unique_behaviors);
 assert.strictEqual(updated.answers['TF1-G04'].no_stable_default,true);
 assert(updated.answers['TF1-G04'].recent_case.startsWith('For a synthetic'));
 // A fresh browser tab imports newly created annotations without losing the source.
 const clean=await browser.newPage();await clean.goto('file://'+path.join(p,'LIFE_PATTERNS_V3_OFFLINE_PILOT.html'),{waitUntil:'load'});
 await (await clean.$('#import-file')).uploadFile(target);
 await clean.waitForFunction(()=>document.getElementById('import-feedback').textContent.includes('Restored 25'),{timeout:7000});
 await clean.select('#route','TF1-G04');
 assert.strictEqual(await clean.$eval('#recent-case',e=>e.value),updated.answers['TF1-G04'].recent_case);
 assert.strictEqual(await clean.$eval('#no-stable-default',e=>e.checked),true);
 // Invalid typed metadata is rejected before replacing existing answers.
 const malformed={...updated,answers:{...updated.answers,'TF1-G04':{...updated.answers['TF1-G04'],context_rule:{unexpected:'object'}}}};
 const bad=path.join(tmp,'malformed.json');fs.writeFileSync(bad,JSON.stringify(malformed));
 await (await clean.$('#import-file')).uploadFile(bad);
 await clean.waitForFunction(()=>document.getElementById('import-feedback').textContent.includes('Import failed'),{timeout:7000});
 assert.strictEqual(await clean.$eval('#no-stable-default',e=>e.checked),true);
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
 assert.strictEqual(overflow,false);assert.deepStrictEqual(requests,[]);assert.deepStrictEqual(errors,[]);
 const html=fs.readFileSync(path.join(p,'LIFE_PATTERNS_V3_OFFLINE_PILOT.html'),'utf8');
 assert(!html.includes('Neptune')&&!html.includes('Pisces')&&!html.includes('Human Design gate'));
 console.log(JSON.stringify({status:'PASS',old_export_imported:true,all_four_question_prompted:true,conditions_saved:true,switch_restores:true,export_reimport_preserves:true,original_answers_preserved:true,optional_invalid_type_rejected:true,mobile_no_overflow:true,external_requests:0,page_errors:0}));
 }finally{await browser.close();fs.rmSync(tmp,{recursive:true,force:true});}
})().catch(e=>{console.error(e.stack);process.exit(1);});
