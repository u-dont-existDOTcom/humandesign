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
#unique-list li{padding:.65rem .25rem;overflow-wrap:anywhere;border-bottom:1px solid #e5eaf0}#unique-list li.editing{background:#f0f5fa;border-radius:8px;padding:.65rem}.metadata{display:block;color:#526070;font-size:.85rem;white-space:pre-wrap}.count{font-variant-numeric:tabular-nums;font-weight:600}.tag{font-size:.76rem;background:#ebeff4;padding:.12rem .5rem;border-radius:99px}
pre{overflow:auto;font:12px/1.4 ui-monospace,monospace;background:#f3f5f7;border-radius:8px;padding:1rem}
[hidden]{display:none!important}details{margin-top:.6rem}summary{cursor:pointer;font-weight:600}
@media(max-width:550px){main{padding:1rem .7rem}section{padding:.9rem}h1{font-size:1.45rem}}
</style></head><body><main><header><h1>Life Patterns — guided responses and distinctive habits</h1>
<p class="notice"><strong>Research prototype only.</strong> Not your live GPT survey, not connected to Railway, and not a birth-chart test. This page does not upload or automatically save anything. You can import a previous JSON export, edit it locally, and export an updated file.</p>
<p>Try the 25 proposed answer-example sets, or explore the optional unusual-behavior inventory. Example paths are suggestions, not correct answers or diagnostic trait labels.</p></header>
<section aria-labelledby="section-import"><h2 id="section-import">Continue a previous pilot</h2>
<p>Already exported answers? Import that JSON here to restore your 25 question responses and unusual behaviors before editing. Nothing is uploaded; importing replaces in-tab responses only after confirmation when needed.</p>
<label for="import-file">Choose your previous Life Patterns JSON file</label>
<input id="import-file" type="file" accept=".json,application/json">
<p id="import-feedback" class="small" role="status" aria-live="polite">No imported file yet. You can also start a new response below.</p>
</section>
<section id="guided-section" aria-labelledby="guided-title" hidden>
<h2 id="guided-title" tabindex="-1">Eight context follow-ups</h2>
<p>We already have your answers. Answer one clarification at a time, or skip. Nothing is submitted automatically.</p>
<progress id="guided-progress" max="8" value="0"></progress>
<p id="guided-overview" role="status" aria-live="polite"></p>
<div id="guided-active">
<h3 id="guided-count"></h3><p id="guided-question"></p><p id="guided-prompt"></p>
<details><summary>See your earlier answer</summary><div id="guided-prior"></div></details>
<label for="guided-rule">What determines which response you choose? (optional)</label>
<textarea id="guided-rule" rows="3" placeholder="Describe the conditions, if any."></textarea>
<label for="guided-example">One recent real example or counterexample (optional)</label>
<textarea id="guided-example" rows="3" placeholder="What happened? What did you do first?"></textarea>
<label class="example"><input type="checkbox" id="guided-no-default">No stable default across situations</label>
<p id="guided-status" role="status" aria-live="polite"></p>
<div class="row"><button type="button" id="guided-previous">Previous</button><button type="button" id="guided-skip">Skip for now</button><button type="button" id="guided-next">Save &amp; next</button></div>
</div>
<div id="guided-complete" hidden><h3>Context check complete</h3>
<p id="guided-complete-summary"></p>
<p><strong>To keep your answers, export the updated JSON below.</strong> The browser does not save them automatically.</p>
<div class="row"><button type="button" id="guided-download">Export updated JSON</button><button type="button" id="guided-review">Review all eight</button></div>
</div>
</section>
<section aria-labelledby="section-questions"><h2 id="section-questions">Question examples (25 proposed variants)</h2>
<label for="route">Choose a question</label><select id="route"></select>
<p id="question-text"></p>
<fieldset><legend>For example, one or more of these might apply:</legend><div id="options"></div></fieldset>
<label for="other">Other / explain it in your own words (equally valid)</label><textarea id="other" placeholder="What you actually tend to do, with conditions or exceptions..." rows="3"></textarea>
<div class="row"><label class="example"><input type="checkbox" id="unsure">I don't know or can't recall</label><label class="example"><input type="checkbox" id="skip">Prefer to skip</label></div>
<details id="context-probe"><summary>Explore the conditions (optional, especially when several answers apply)</summary>
<p id="context-probe-prompt" class="small"></p>
<label for="context-rule">When do different options apply? What determines the choice? (optional)</label>
<textarea id="context-rule" rows="3" placeholder="Describe the circumstances or decision rule, or say there is no stable default."></textarea>
<label for="recent-case">One recent real example or counterexample (optional)</label>
<textarea id="recent-case" rows="3" placeholder="What happened, what did you do first, and how was it different another time?"></textarea>
<label class="example"><input type="checkbox" id="no-stable-default">I don't have one usual response across situations</label>
</details>
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
<div class="row"><button type="button" id="add">Add a behavior</button><button type="button" id="cancel-edit" hidden>Cancel editing</button><button type="button" id="clear">Clear list</button><span class="count" id="count" aria-live="polite">0 of 20</span></div>
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
let editingIndex=null;
const inventoryFields=['behavior','context','comparison','reason'];
const storedSchema='local_life_patterns_v3_pilot_unsubmitted';
const contextualProbes={"TF1-G01":"Think of the most recent unfamiliar task that mattered to you. What did you do first, and what made that step preferable to the other available methods?","TF1-G02":"Think of the last time you explained something difficult. Which step did you try first, what did you know about the listener, and how did they respond?","TF1-D0":"Recall a skill you were already competent at. When did you repeat details for enjoyment versus to achieve a necessary result?","TF1-G04":"For the latest task that went wrong, what specific evidence guided the first troubleshooting method? When would you use a different one?","TF1-G15":"Compare two recent worthwhile work sessions of different duration or effort. How did your energy respond, and what changed?","TF1-G16":"Recall a recent task where your interest faded. Which reason actually kept you going, if any? What would have made you stop?","TF1-G18":"After recent time with people you enjoy, when did you want more company and when did you want to be alone? What changed?","TF1-G23":"Recall an actual unfamiliar group task. What did you first notice, and what happened next? Can you remember a different kind of group?","TF1-M05":"Recall a recent uncertain or potentially unsafe situation. What was the first observable cue, and did your assessment change after more evidence?","TF1-B0":"Recall a recent interaction with someone upset. What happened to your mood during the interaction and after separating? What was your role?","TF1-G20":"Think of a real discretionary resource decision you made rather than a hypothetical windfall. Which goal took priority and what did you sacrifice?","TF1-M01":"Compare times when the objective deadline was similar but other people's pressure differed. How, if at all, did your pace change?","TF1-M03":"Think of one important feasible promise and one minor favor. How did your follow-through differ when enthusiasm changed?","TF1-STATUS":"Recall recognition you appreciated and recognition you didn't. What specifically made it meaningful or not, aside from practical benefits?","TF1-G17":"Recall noticing a harmless versus consequential factual error. Did you feel like correcting it, and what actually determined whether you spoke up?","TF1-ROUTINE-CHANGE":"Recall one domain where you chose novelty and another where you kept a routine despite an attractive alternative. What conditions mattered?"};
function emptyEditor(){
 inventoryFields.forEach(id=>el(id).value='');
 editingIndex=null;
 el('add').textContent='Add a behavior';
 el('cancel-edit').hidden=true;
}
function startEditing(i){
 const item=state.unique[i];if(!item)return;
 editingIndex=i;
 inventoryFields.forEach(id=>el(id).value=item[id]||'');
 el('add').textContent='Save changes';
 el('cancel-edit').hidden=false;
 el('inventory-feedback').textContent=`Editing behavior ${i+1} of ${state.unique.length}; Save changes or Cancel editing.`;
 renderList();el('behavior').focus();
}
function shouldWarnBeforeImport(){
 return Object.keys(state.answers).length>0 || state.unique.length>0 ||
   inventoryFields.some(id=>el(id).value.trim().length>0);
}
function parseExistingExport(input){
 if(!input || typeof input!=='object' || Array.isArray(input) || input.schema!==storedSchema)
  throw new Error('This is not a compatible V3 local pilot export.');
 const sourceAnswers=input.answers;
 if(!sourceAnswers || typeof sourceAnswers!=='object' || Array.isArray(sourceAnswers))
  throw new Error('The imported answers object is missing.');
 const known=new Map(d.questions.map(q=>[q.id,q]));
 const answers={};
 for(const [route,answer] of Object.entries(sourceAnswers)){
  const q=known.get(route);
  if(!q)throw new Error(`Unknown question ${route}; no answers were replaced.`);
  if(!answer || typeof answer!=='object' || Array.isArray(answer) ||
     (answer.context_rule!=null && typeof answer.context_rule!=='string') ||
     (answer.recent_case!=null && typeof answer.recent_case!=='string') ||
     (answer.no_stable_default!=null && typeof answer.no_stable_default!=='boolean') ||
     (answer.context_skipped!=null && typeof answer.context_skipped!=='boolean') ||
     !Array.isArray(answer.selected) ||
     !answer.selected.every(v=>typeof v==='string' && q.example_answer_paths.includes(v)) ||
     (answer.other!=null && typeof answer.other!=='string') ||
     (answer.unsure!=null && typeof answer.unsure!=='boolean') ||
     (answer.skip!=null && typeof answer.skip!=='boolean'))
    throw new Error(`Invalid answer for ${route}; no answers were replaced.`);
  answers[route]={...answer,selected:[...answer.selected],other:answer.other||'',
    unsure:answer.unsure===true,skip:answer.skip===true};
 }
 if(!Array.isArray(input.unique_behaviors) || input.unique_behaviors.length>20)
  throw new Error('Expected a list of at most 20 unusual behaviors; no data were replaced.');
 const unique=input.unique_behaviors.map((item,i)=>{
  if(!item || typeof item!=='object' || Array.isArray(item) ||
      typeof item.behavior!=='string' || !item.behavior.trim() ||
      inventoryFields.some(field=>item[field]!=null && typeof item[field]!=='string'))
    throw new Error(`Invalid unusual behavior ${i+1}; no data were replaced.`);
  return {...item,context:item.context||'',comparison:item.comparison||'',reason:item.reason||''};
 });
 return {answers,unique};
}
// Research-only guided review of the eight route-level weaknesses from the
// frozen V3-versus-historical audit. Never derive a chart prediction here.
const guidedRoutes=['TF1-G01','TF1-G02','TF1-G16','TF1-G23','TF1-M05','TF1-G20','TF1-M01','TF1-M03'];
let guidedIndex=-1;
let guidedReviewAll=false;
function guidedAddressed(answer){
 return Boolean(answer && (
   (typeof answer.context_rule==='string' && answer.context_rule.trim()) ||
   (typeof answer.recent_case==='string' && answer.recent_case.trim()) ||
   answer.no_stable_default===true || answer.context_skipped===true
 ));
}
function guidedStatistics(){
 const completed=guidedRoutes.filter(id=>guidedAddressed(state.answers[id])).length;
 const skipped=guidedRoutes.filter(id=>state.answers[id]?.context_skipped===true).length;
 el('guided-progress').value=completed;
 el('guided-overview').textContent=completed+' of 8 follow-ups addressed'+(skipped?' ('+skipped+' skipped)':'')+'.';
 return completed;
}
function guidedNextOutstanding(from){
 for(let delta=1;delta<=guidedRoutes.length;delta++){
  const idx=(from+delta)%guidedRoutes.length;
  if(!guidedAddressed(state.answers[guidedRoutes[idx]]))return idx;
 }
 return -1;
}
function guidedRenderPrior(answer){
 const target=el('guided-prior');
 target.replaceChildren();
 const items=(answer?.selected||[]);
 const list=document.createElement('ul');
 for(const choice of items){
  const li=document.createElement('li');li.textContent=choice;list.append(li);
 }
 if(items.length)target.append(list);
 if(answer?.other){
  const p=document.createElement('p');
  p.textContent='You also said: '+answer.other;
  target.append(p);
 }
 if(!items.length&&!answer?.other){
  const p=document.createElement('p');p.textContent='No earlier answer recorded for this route.';target.append(p);
 }
}
function guidedShow(){
 const section=el('guided-section');
 section.hidden=false;
 const count=guidedStatistics();
 const active=el('guided-active'),complete=el('guided-complete');
 if(guidedIndex<0){
  active.hidden=true;complete.hidden=false;
  el('guided-complete-summary').textContent='All eight prompts have been reviewed: '+count+' addressed. Skipped items can be revisited with Review all eight.';
  return;
 }
 active.hidden=false;complete.hidden=true;
 const id=guidedRoutes[guidedIndex],q=d.questions.find(v=>v.id===id);
 const a=state.answers[id]||{};
 el('guided-count').textContent='Follow-up '+(guidedIndex+1)+' of 8 · '+id;
 el('guided-question').textContent=q.question;
 el('guided-prompt').textContent=contextualProbes[id]||'Describe a recent choice and what determined your response.';
 guidedRenderPrior(a);
 el('guided-rule').value=a.context_rule||'';
 el('guided-example').value=a.recent_case||'';
 el('guided-no-default').checked=a.no_stable_default===true;
 el('guided-previous').disabled=guidedIndex===0;
 el('guided-status').textContent=a.context_skipped?'Previously skipped. You can answer now or skip again.':
  'Only the missing context is being requested. Your earlier answer will not be replaced.';
}
function guidedSaveDraft(){
 if(guidedIndex<0)return;
 const id=guidedRoutes[guidedIndex];
 const a=state.answers[id]||{};
 const changed=el('guided-rule').value!==String(a.context_rule||'')||
   el('guided-example').value!==String(a.recent_case||'')||
   el('guided-no-default').checked!==(a.no_stable_default===true);
 state.answers[id]={
  ...a,
  context_rule:el('guided-rule').value,
  recent_case:el('guided-example').value,
  no_stable_default:el('guided-no-default').checked,
  context_skipped:changed?false:a.context_skipped===true,
 };
 guidedStatistics();
}
function guidedBegin({focus=true}={}){
 guidedReviewAll=false;
 guidedIndex=guidedNextOutstanding(-1);
 guidedShow();
 if(focus){
  el('guided-section').scrollIntoView({block:'start'});
  el('guided-title').focus({preventScroll:true});
 }
}
function guidedAdvance(){
 guidedIndex=guidedReviewAll?(guidedIndex<guidedRoutes.length-1?guidedIndex+1:-1):
   guidedNextOutstanding(guidedIndex);
 guidedShow();
 if(guidedIndex>=0)el('guided-rule').focus();
}
el('guided-rule').addEventListener('input',guidedSaveDraft);
el('guided-example').addEventListener('input',guidedSaveDraft);
el('guided-no-default').addEventListener('change',guidedSaveDraft);
el('guided-next').onclick=()=>{
 if(guidedIndex<0)return;
 guidedSaveDraft();
 const id=guidedRoutes[guidedIndex];
 if(!guidedAddressed(state.answers[id])){
  el('guided-status').textContent='Write an example or condition, select No stable default, or choose Skip for now.';
  el('guided-rule').focus();return;
 }
 guidedAdvance();
};
el('guided-skip').onclick=()=>{
 if(guidedIndex<0)return;
 guidedSaveDraft();
 state.answers[guidedRoutes[guidedIndex]].context_skipped=true;
 guidedAdvance();
};
el('guided-previous').onclick=()=>{
 if(guidedIndex<=0)return;
 guidedSaveDraft();
 guidedIndex--;
 guidedShow();
 el('guided-rule').focus();
};
el('guided-download').onclick=()=>el('export').click();
el('guided-review').onclick=()=>{
 guidedReviewAll=true;guidedIndex=0;guidedShow();el('guided-rule').focus();
};
function remember(){
 const id=el('route').value;
 if(!id)return;
 const previous=state.answers[id]||{};
 const chosen=[...document.querySelectorAll('#options input:checked')].map(x=>x.value);
 if(chosen.length===4 && (previous.selected||[]).length!==4)el('context-probe').open=true;
 state.answers[id]={
  ...previous,
  selected:chosen,
  other:el('other').value,
  unsure:el('unsure').checked,
  skip:el('skip').checked,
  context_rule:el('context-rule').value,
  recent_case:el('recent-case').value,
  no_stable_default:el('no-stable-default').checked
 };
 explainExampleCoverage();
}
function explainExampleCoverage(){
 const route=d.questions.find(q=>q.id===el('route').value);
 const checked=document.querySelectorAll('#options input:checked').length;
 el('selected-summary').textContent=route && checked===route.example_answer_paths.length
  ?'All four examples selected. They may fit under different conditions, so the optional conditions section is especially relevant. A single typical response is not required.'
  :'Examples help recall. They are not independent evidence or fixed personality traits. Free text and conditions are welcome.';
}
function showQuestion(){
 const id=el('route').value,q=d.questions.find(x=>x.id===id);
 el('question-text').textContent=q.question;
 el('options').replaceChildren();
 const prior=state.answers[id]||{selected:[],other:'',unsure:false,skip:false};
 el('context-probe-prompt').textContent=contextualProbes[id] || 'Recall a real situation: which option did you use first, what circumstances mattered, and what happened on another occasion?';
 el('context-rule').value=prior.context_rule||'';
 el('recent-case').value=prior.recent_case||'';
 el('no-stable-default').checked=prior.no_stable_default===true;
 el('context-probe').open=prior.selected?.length===4;
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
 explainExampleCoverage();
}
function renderList(){
 const list=el('unique-list');list.replaceChildren();
 state.unique.forEach((item,i)=>{
  const li=document.createElement('li');
  if(i===editingIndex)li.classList.add('editing');
  const label=document.createElement('span');label.textContent=item.behavior;
  const metadata=document.createElement('small');metadata.className='metadata';
  const details=[];
  if(item.context)details.push('When/how often: '+item.context);
  if(item.comparison)details.push('Compared with: '+item.comparison);
  if(item.reason)details.push('Why: '+item.reason);
  metadata.textContent=details.join(' · ');
  const actions=document.createElement('div');actions.className='row';
  const edit=document.createElement('button');edit.type='button';edit.textContent='Edit';
  edit.setAttribute('aria-label',`Edit unusual behavior ${i+1}`);
  edit.onclick=()=>startEditing(i);
  const del=document.createElement('button');del.type='button';del.textContent='Remove';
  del.setAttribute('aria-label',`Remove unusual behavior ${i+1}`);
  del.onclick=()=>{
   if(!window.confirm('Remove this behavior? You can cancel or import an earlier JSON export again.'))return;
   state.unique.splice(i,1);emptyEditor();renderList();
   el('inventory-feedback').textContent=`Behavior ${i+1} removed.`;
  };
  actions.append(edit,del);li.append(label,metadata,actions);list.append(li);
 });
 el('count').textContent=state.unique.length+' of 20';
 el('add').disabled=editingIndex===null && state.unique.length>=20;
}
d.questions.forEach(q=>{const opt=document.createElement('option');opt.value=q.id;opt.textContent=q.id+' · '+q.family;el('route').append(opt);});
el('route').addEventListener('change',showQuestion);
['other','unsure','skip','context-rule','recent-case','no-stable-default'].forEach(id=>el(id).addEventListener('input',()=>{
 if(id==='unsure'&&el('unsure').checked)el('skip').checked=false;
 if(id==='skip'&&el('skip').checked)el('unsure').checked=false;
 remember();
}));
el('inventory-question').textContent=d.inventory.opening_prompt;
d.inventory.example_categories_if_stuck.forEach(x=>{const li=document.createElement('li');li.textContent=x;el('categories').append(li);});
el('add').onclick=()=>{
 const behavior=el('behavior').value.trim();
 if(!behavior){el('inventory-feedback').textContent='Describe the behavior before saving, or Cancel editing.';return;}
 if(editingIndex===null && state.unique.length>=20)return;
 const update={behavior,context:el('context').value,comparison:el('comparison').value,reason:el('reason').value};
 const wasEditing=editingIndex!==null;
 if(wasEditing)state.unique[editingIndex]={...state.unique[editingIndex],...update};
 else state.unique.push(update);
 emptyEditor();renderList();
 el('inventory-feedback').textContent=wasEditing?'Changes saved in this tab. Export JSON to retain them.':'Behavior added in this tab. Export JSON to retain it.';
 el('behavior').focus();
};
el('cancel-edit').onclick=()=>{
 emptyEditor();renderList();
 el('inventory-feedback').textContent='Editing canceled. The saved item was not changed.';
};
el('clear').onclick=()=>{
 if(state.unique.length && !window.confirm('Clear all saved unusual behaviors in this tab? This cannot be undone without re-importing your earlier export.'))return;
 state.unique=[];emptyEditor();renderList();el('inventory-feedback').textContent='List cleared.';
};
el('export').onclick=()=>{
 const data=JSON.stringify({schema:storedSchema,answers:state.answers,unique_behaviors:state.unique},null,2);
 const blob=new Blob([data],{type:'application/json'}),url=URL.createObjectURL(blob);
 const link=document.createElement('a');link.href=url;link.download='my-life-patterns-v3-local-pilot.json';link.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
};
el('reset').onclick=()=>{
 if(shouldWarnBeforeImport() && !window.confirm('Reset all 25 question answers and unusual behaviors in this tab? You can re-import a prior export.'))return;
 state.answers={};state.unique=[];emptyEditor();showQuestion();renderList();
 el('inventory-feedback').textContent='All temporary responses reset.';
};
el('import-file').addEventListener('change',async event=>{
 const file=event.target.files?.[0];if(!file)return;
 try{
  if(file.size>5_000_000)throw new Error('The JSON file exceeds the 5 MB local-import limit.');
  const parsed=parseExistingExport(JSON.parse(await file.text()));
  if(shouldWarnBeforeImport() && !window.confirm('Replace current in-tab responses with the imported file? Export first if you want to keep both.')){
   el('import-feedback').textContent='Import canceled. Existing in-tab responses were kept.';return;
  }
  state.answers=parsed.answers;state.unique=parsed.unique;
  emptyEditor();showQuestion();renderList();
  guidedBegin();
  el('import-feedback').textContent=`Restored ${Object.keys(state.answers).length} question answers and ${state.unique.length} unusual behaviors from ${file.name}. Edit, then export JSON to keep changes.`;
  el('inventory-feedback').textContent='Imported details can now be edited, removed, or supplemented.';
 }catch(error){el('import-feedback').textContent='Import failed: '+error.message;}
 finally{event.target.value='';}
});
showQuestion();renderList();
if(d.prefilled_export){
 try{
  const restored=parseExistingExport(d.prefilled_export);
  state.answers=restored.answers;state.unique=restored.unique;
  showQuestion();renderList();guidedBegin();
  el('import-feedback').textContent='Your saved pilot answers were loaded privately. Continue with the first outstanding follow-up.';
 }catch(error){
  el('import-feedback').textContent='The private prefill could not be loaded: '+error.message;
 }
}
</script></body></html>"""

(HERE / "LIFE_PATTERNS_V3_OFFLINE_PILOT.html").write_text(
    head + client_data + foot, encoding="utf-8"
)
print("PILOT_HTML_BYTES", (HERE / "LIFE_PATTERNS_V3_OFFLINE_PILOT.html").stat().st_size)
