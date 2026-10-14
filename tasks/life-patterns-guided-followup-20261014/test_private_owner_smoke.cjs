const fs=require('fs'),assert=require('assert'),{pathToFileURL}=require('url');
const puppeteer=require(process.env.PUPPETEER_MODULE||'puppeteer');
(async()=>{
 const b=await puppeteer.launch({headless:true,executablePath:process.env.CHROME_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await b.newPage(), errors=[],network=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('request',r=>{if(!r.url().startsWith('file:'))network.push(r.url());});
  await page.goto(pathToFileURL(process.env.PRIVATE_GUIDED_HTML).href,{waitUntil:'load'});
  const d=await page.evaluate(()=>({visible:!document.getElementById('guided-section').hidden,
   first:document.getElementById('guided-count').textContent,
   count:Object.keys(state.answers).length,unique:state.unique.length}));
  const old=JSON.parse(fs.readFileSync(process.env.PRIVATE_PILOT_JSON,'utf8'));
  assert(d.visible && d.first.includes('TF1-G01') && d.count===25);
  assert.strictEqual(d.unique,old.unique_behaviors.length);
  assert.deepStrictEqual(errors,[]);assert.deepStrictEqual(network,[]);
  console.log(JSON.stringify({status:'PASS',owner_private_prefill:true,starts_first_question:true,source_answers:25,original_behaviors:d.unique,no_network:true,errors:0}));
 }finally{await b.close();}
})().catch(e=>{console.error(e.message);process.exit(1)});
