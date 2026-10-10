"""Build an offline, never-submitted Life Patterns answer-scaffolding pilot."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V3 = json.loads((HERE / "tendency-first-v3-scaffold-development.json").read_text())
MODULE = json.loads((HERE / "unusual-behavior-inventory-v0.json").read_text())
client_data = json.dumps(
    {"questions": V3["questions"], "inventory": MODULE}, ensure_ascii=False
).replace("<", "\\u003c")

head = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Life Patterns — Guided response and unusual behaviors pilot</title>
<style>
:root{color-scheme:light;font:16px/1.5 system-ui,sans-serif;color:#1d2834;background:#fafbfc}
*{box-sizing:border-box}body{margin:0}main{max-width:920px;margin:auto;padding:1.4rem 1rem 4rem}
h1{font-size:1.7rem;letter-spacing:-.025em}h2{font-size:1.23rem;margin:0 0 .6rem}
header{border-bottom:1px solid #dbe1e5;padding:0 0 1rem;margin-bottom:1.2rem}
section{border:1px solid #d6dee7;border-radius:12px;background:#fff;padding:1.2rem;margin:1.1rem 0}
label{display:block;margin-top:.5rem;font-weight:600}input[type=text],input[type=search],select,textarea{font:inherit;color:inherit;border:1px solid #9dabb9;border-radius:8px;padding:.55rem .7rem;width:100%;max-width:100%}
textarea{min-height:5rem;resize:vertical}button{font:inherit;border:1px solid #8796a6;background:#f3f6f8;border-radius:8px;padding:.48rem .9rem;cursor:pointer}button:hover{background:#e3ecf5}
button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible{outline:3px solid #557bb4;outline-offset:2px}
.small{font-size:.86rem;color:#546170}.dim{color:#4f6173}.notice{border-left:3px solid #536c8c;padding:.4rem 1rem;background:#f5f7f9}.row{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap}.example{display:block;font-weight:400;padding:.35rem .2rem;margin:.2rem 0}.example input{margin-right:.6rem;accent-color:#204a7a}
fieldset{border:0;padding:0;margin:.8rem 0}legend{font-weight:700;margin:0 0 .35rem}
#question-text{font-size:1.13rem;font-weight:620;margin:1rem 0 .6rem}
.followup{border-left:3px solid #d1dae3;padding-left:.75rem;margin:.65rem 0}
#unique-list li{padding:.35rem 0;overflow-wrap:anywhere}.count{font-variant-numeric:tabular-nums;font-weight:600}.tag{font-size:.76rem;background:#ebeff4;padding:.12rem .5rem;border-radius:99px}
pre{overflow:auto;font:12px/1.4 ui-monospace,monospace;background:#f3f5f7;border-radius:8px;padding:1rem}
[hidden]{display:none!important}details{margin-top:.6rem}summary{cursor:pointer;font-weight:600}
@media(max-width:550px){main{padding:1rem .7rem}section{padding:.9rem}h1{font-size:1.45rem}}
</style></head><body><main><header><h1>Life Patterns — guided responses and distinctive habits</h1>
<p class="notice"><strong>Research prototype only.</strong> Not your live GPT survey, not connected to Railway, and not a birth-chart test. This page does not upload or retain anything. Your input stays in this browser tab unless you explicitly export a local JSON file.</p>
<p>Try the 25 proposed answer-example sets, or explore the optional unusual-behavior inventory. Example paths are suggestions, not correct answers or diagnostic trait labels.</p></header>
<section aria-labelledby="section-questions"><h2 id="section-questions">Question examples (25 proposed variants)</h2>
<label for="route">Choose a question</label><select id="route"></select>
<p id="question-text"></p>
<fieldset><legend>For example, one or more of these might apply:</legend><div id="options"></div></fieldset>
<label for="other">Other / explain it in your own words (equally valid)</label><textarea id="other" placeholder="What you actually tend to do, with conditions or exceptions..." rows="3"></textarea>
<div class="row"><label class="example"><input type="checkbox" id="unsure">I don't know or can't recall</label><label class="example"><input type="checkbox" id="skip">Prefer to skip</label></div>
<details id="followups"><summary>Potential clarification only if an important distinction was not already answered</summary><div id="followup-items"></div></details>
<p class="small" id="selected-summary" aria-live="polite"></p>
</section>
<section aria-labelledby="section-unique"><h2 id="section-unique">Unusual behaviors inventory (optional)</h2>
<p id="inventory-question"></p><p class="small">Begin with one to three if you can. You can add up to 20 over time, or stop at zero. This is not a test of whether your personality is special or your birth time is identifiable.</p>
<details><summary>Example areas, if nothing comes to mind</summary><ul id="categories"></ul></details>
<label for="behavior">Something you do that may differ from people around you</label><textarea id="behavior" rows="3" placeholder="Describe a concrete behavior, not a personality adjective"></textarea>
<label for="context">How often, and in what circumstances? (optional)</label><input id="context" type="text" placeholder="Frequency / situation / when you don't do it">
<label for="comparison">Compared with whom? What makes you think it's uncommon? (optional)</label><input id="comparison" type="text" placeholder="Friends, family, coworkers, people I know; or not sure">
<label for="reason">What motivates it, if anything? (optional)</label><input id="reason" type="text" placeholder="Convenience, curiosity, necessity, preference, etc.">
<div class="row"><button type="button" id="add">Add a behavior</button><button type="button" id="clear">Clear list</button><span class="count" id="count" aria-live="polite">0 of 20</span></div>
<ol id="unique-list"></ol><p class="small" id="inventory-feedback" aria-live="polite">Not recalling unusual behaviors is normal and not scored against you. No item is presumed objectively rare.</p>
</section>
<section aria-labelledby="method"><h2 id="method">What this study would—and would not—measure</h2>
<p>Self-chosen unusual habits may uncover overlooked behavioral details. They may also depend on resources, memory, culture, social comparison, opportunity, and willingness to describe oneself. A rare habit is not evidence of a rare birth chart.</p>
<p>An appropriate future comparison would test whether these accounts add held-out chart-identification information beyond ordinary questionnaire responses and non-chart controls. The 20-behavior count is never itself a birth-date score.</p>
<div class="row"><button type="button" id="export">Export my temporary responses as JSON</button><button type="button" id="reset">Reset this pilot</button></div>
<p class="small">Only export intentionally. The file is local and may include private details. Do not send it as a survey submission; the live instrument is unchanged.</p>
</section></main>
<script id="pilot-data" type="application/json">"""

foot = """</script><script>
const d=JSON.parse(document.getElementById('pilot-data').textContent);
const el=id=>document.getElementById(id);
const state={answers:{},unique:[]};
const universal=['Other — my own words','Not sure / cannot recall','Prefer to skip'];
const escapeText=x=>String(x==null?'':x);
function remember(){
 const id=el('route').value;
 if(!id)return;
 state.answers[id]={
  selected:[...document.querySelectorAll('#options input:checked')].map(x=>x.value),
  other:el('other').value,
  unsure:el('unsure').checked,
  skip:el('skip').checked
 };
 el('selected-summary').textContent='The examples are prompts only; a checked label is not automatically a trait.';
}
function showQuestion(){
 const id=el('route').value,q=d.questions.find(x=>x.id===id);
 el('question-text').textContent=q.question;
 el('options').replaceChildren();
 const prior=state.answers[id]||{selected:[],other:'',unsure:false,skip:false};
 q.example_answer_paths.forEach((text,i)=>{
  const label=document.createElement('label');label.className='example';
  const box=document.createElement('input');box.type='checkbox';box.value=text;
  box.checked=prior.selected.includes(text);box.addEventListener('change',remember);
  label.append(box,document.createTextNode(text));el('options').append(label);
 });
 el('other').value=prior.other;el('unsure').checked=prior.unsure;el('skip').checked=prior.skip;
 el('followups').hidden=!q.follow_up_only_if_not_already_answered?.length;
 el('followups').open=false;el('followup-items').replaceChildren();
 (q.follow_up_only_if_not_already_answered||[]).forEach(x=>{
  const paragraph=document.createElement('p');paragraph.className='followup';paragraph.textContent=x.question;
  el('followup-items').append(paragraph);
 });
 el('selected-summary').textContent='Answer in your own words, combine options, or choose none. This is not a scored test.';
}
function renderList(){
 const list=el('unique-list');list.replaceChildren();
 state.unique.forEach((item,i)=>{
  const li=document.createElement('li');
  const label=document.createElement('span');label.textContent=item.behavior;
  const del=document.createElement('button');del.type='button';del.textContent='Remove';del.style.marginLeft='.5rem';
  del.setAttribute('aria-label','Remove behavior '+(i+1));
  del.onclick=()=>{state.unique.splice(i,1);renderList();};
  li.append(label,del);list.append(li);
 });
 el('count').textContent=state.unique.length+' of 20';
 el('add').disabled=state.unique.length>=20;
}
d.questions.forEach(q=>{const opt=document.createElement('option');opt.value=q.id;opt.textContent=q.id+' · '+q.family;el('route').append(opt);});
el('route').addEventListener('change',showQuestion);
['other','unsure','skip'].forEach(id=>el(id).addEventListener('input',()=>{
 if(id==='unsure'&&el('unsure').checked)el('skip').checked=false;
 if(id==='skip'&&el('skip').checked)el('unsure').checked=false;
 remember();
}));
el('inventory-question').textContent=d.inventory.opening_prompt;
d.inventory.example_categories_if_stuck.forEach(x=>{const li=document.createElement('li');li.textContent=x;el('categories').append(li);});
el('add').onclick=()=>{
 const behavior=el('behavior').value.trim();
 if(!behavior){el('inventory-feedback').textContent='Write a behavior first, or leave this section blank.';return;}
 if(state.unique.length>=20)return;
 state.unique.push({behavior,context:el('context').value,comparison:el('comparison').value,reason:el('reason').value});
 ['behavior','context','comparison','reason'].forEach(id=>el(id).value='');
 el('inventory-feedback').textContent='Recorded only in this tab. You can add more or stop.';renderList();el('behavior').focus();
};
el('clear').onclick=()=>{state.unique=[];renderList();el('inventory-feedback').textContent='List cleared.';};
el('export').onclick=()=>{
 const data=JSON.stringify({schema:'local_life_patterns_v3_pilot_unsubmitted',answers:state.answers,unique_behaviors:state.unique},null,2);
 const blob=new Blob([data],{type:'application/json'}),url=URL.createObjectURL(blob);
 const link=document.createElement('a');link.href=url;link.download='my-life-patterns-v3-local-pilot.json';link.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
};
el('reset').onclick=()=>{state.answers={};state.unique=[];showQuestion();renderList();el('inventory-feedback').textContent='All temporary responses reset.';};
showQuestion();renderList();
</script></body></html>"""

(HERE / "LIFE_PATTERNS_V3_OFFLINE_PILOT.html").write_text(
    head + client_data + foot, encoding="utf-8"
)
print("PILOT_HTML_BYTES", (HERE / "LIFE_PATTERNS_V3_OFFLINE_PILOT.html").stat().st_size)
