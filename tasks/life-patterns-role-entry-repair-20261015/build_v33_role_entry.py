# ruff: noqa: E501
"""Build a V3.3 offline role-entry repair from the unchanged V3.2 questionnaire.

No rewriting historical answers, no chart-key inputs, no automatic astrology scoring.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = (
    ROOT / "tasks/life-patterns-v32-owner-comparison-20261015/LIFE_PATTERNS_V32_OFFLINE_PILOT.html"
)
PROTOCOL = HERE / "ROLE_ENTRY_MEASUREMENT_V1.json"
OUTPUT = HERE / "LIFE_PATTERNS_V33_ROLE_ENTRY_OFFLINE_PILOT.html"

SECTION = """
<section id="role-entry-section" aria-labelledby="role-title">
<h2 id="role-title" tabindex="-1">One short question about helping or taking responsibility</h2>
<p class="small">Your earlier answers are already saved. One or two sentences is enough. No examples are required.</p>
<p id="role-prompt"></p>
<label for="role-short">Your answer (or simply say "it depends")</label>
<textarea id="role-short" rows="2" placeholder="It depends on the situation..."></textarea>
<div class="row">
<label class="example"><input type="checkbox" id="role-no-event"> I cannot think of a relevant situation</label>
<label class="example"><input type="checkbox" id="role-skip"> Prefer to skip</label>
</div>
<details id="role-details">
<summary>Add detail or review existing examples (optional)</summary>
<p id="role-definition" class="small"></p>
<details id="role-earlier"><summary>Prior related V3 answers</summary><div id="role-prior"></div></details>
<div id="role-episodes"></div>
<label for="role-pattern" id="role-overall-label"></label><select id="role-pattern"></select>
<label for="role-conditions">Conditions and exceptions (optional)</label>
<textarea id="role-conditions" rows="3"></textarea>
</details>
<p id="role-status" class="small" role="status" aria-live="polite"></p>
<div class="row"><button type="button" id="role-export">Export answers</button>
<button type="button" id="role-clear">Clear only this answer</button>
<button type="button" id="role-show-existing">Show previous questions</button></div>
<p class="small">No astrological inference is made here. It is valid not to have a typical response.</p>
</section>
"""

SCRIPT = r"""
// Versioned neutral role-entry measurement. The original TF1 and V3.2 answer sets are immutable
// during this module's input handling, and no chart hypothesis or target is consulted here.
const roleProtocol=d.role_probe;
const roleOrigins=roleProtocol.allowed_origins,rolePatterns=roleProtocol.pattern_choices;
const roleKeys=['role-origin-1','role-origin-2','role-origin-3'];
function roleHasData(r){
 return Boolean(r && (r.skip || r.no_event || (r.summary||'').trim() || r.pattern || (r.conditions||'').trim() ||
   r.episodes.some(e=>e.origin || (e.example||'').trim())));
}
function roleEmpty(){
 return {episodes:Array.from({length:3},()=>({origin:'',example:''})),
   summary:'',pattern:'',conditions:'',skip:false,no_event:false};
}
const rolePrior=el('role-prior');
const roleCases=el('role-episodes');
el('role-prompt').textContent=roleProtocol.prompt;
el('role-definition').textContent=roleProtocol.role_definition;
el('role-overall-label').textContent=roleProtocol.overall_question;
for(let i=0;i<3;i++){
 const wrap=document.createElement('div');wrap.className='followup';
 const heading=document.createElement('h3');heading.textContent='Real occasion '+(i+1)+' of 3 (optional)';
 const what=document.createElement('label');what.htmlFor='role-case-'+i;
 what.textContent='What role did you actually take, what came first, and (if invited) what reason did they give?';
 const detail=document.createElement('textarea');detail.id='role-case-'+i;detail.rows=2;
 detail.placeholder='If you cannot recall one, leave this blank.';
 const originLabel=document.createElement('label');originLabel.htmlFor='role-origin-'+i;
 originLabel.textContent='How did you come to take responsibility?';
 const origin=document.createElement('select');origin.id='role-origin-'+i;
 const empty=document.createElement('option');empty.value='';empty.textContent='No occasion recorded';origin.append(empty);
 for(const o of roleOrigins){
  const choice=document.createElement('option');choice.value=o.id;choice.textContent=o.label;origin.append(choice);
 }
 wrap.append(heading,what,detail,originLabel,origin);roleCases.append(wrap);
 detail.addEventListener('input',roleRemember);origin.addEventListener('change',roleRemember);
}
const rolePatternEl=el('role-pattern');
const patternEmpty=document.createElement('option');patternEmpty.value='';
patternEmpty.textContent='Choose a pattern, or leave unknown';rolePatternEl.append(patternEmpty);
for(const o of rolePatterns){
 const choice=document.createElement('option');choice.value=o.id;choice.textContent=o.label;
 rolePatternEl.append(choice);
}
function roleRead(){
 return {
  episodes:Array.from({length:3},(_,i)=>({
   origin:el('role-origin-'+i).value,example:el('role-case-'+i).value
  })),
  summary:el('role-short').value,
  pattern:rolePatternEl.value,
  conditions:el('role-conditions').value,
  skip:el('role-skip').checked,
  no_event:el('role-no-event').checked
 };
}
function roleRemember(){
 const updated=roleRead();
 if(updated.skip){
  updated.no_event=false;
 }else if(updated.no_event){updated.skip=false;}
 state.roleEntry=roleHasData(updated)?updated:null;
 el('role-status').textContent=state.roleEntry
  ?'Saved in this tab only. Export JSON to retain your response; no chart interpretation is assigned.'
  :'No new role-entry response. The earlier source has not been rewritten.';
}
function roleShow(){
 const val=state.roleEntry || roleEmpty();
 el('role-short').value=val.summary||'';
 for(let i=0;i<3;i++){
  el('role-origin-'+i).value=val.episodes[i].origin;
  el('role-case-'+i).value=val.episodes[i].example;
 }
 rolePatternEl.value=val.pattern;
 el('role-conditions').value=val.conditions;
 el('role-skip').checked=val.skip===true;
 el('role-no-event').checked=val.no_event===true;
 const existing=state.answers||{};
 rolePrior.replaceChildren();
 for(const route of ['TF1-G06','TF1-G23']){
  const item=existing[route];if(!item)continue;
  const p=document.createElement('p'),strong=document.createElement('strong');
  strong.textContent=route+' — previous response: ';
  const text=(item.selected||[]).join(' / ')+(item.other?' | '+item.other:'')+
      (item.context_rule?' | Condition: '+item.context_rule:'')+
      (item.recent_case?' | Example: '+item.recent_case:'');
  p.append(strong,document.createTextNode(text));rolePrior.append(p);
 }
 el('role-earlier').hidden=!rolePrior.childNodes.length;
 el('role-status').textContent=roleHasData(state.roleEntry)
  ?'Your earlier answer is already saved; no further examples or explanation are needed.'
  :'One or two sentences is enough; a context-dependent answer is complete.';
}
el('role-short').addEventListener('input',roleRemember);
rolePatternEl.addEventListener('change',roleRemember);
el('role-conditions').addEventListener('input',roleRemember);
el('role-no-event').addEventListener('change',()=>{
 if(el('role-no-event').checked){
  const anyExample=Array.from({length:3},(_,i)=>(
    el('role-case-'+i).value.trim()||el('role-origin-'+i).value)).some(Boolean);
  if(anyExample){
   el('role-no-event').checked=false;
   el('role-status').textContent='Existing episode details were kept. Clear them first only if you intend to report no examples.';
   return;
  }
  el('role-skip').checked=false;
 }
 roleRemember();
});
el('role-skip').addEventListener('change',()=>{
 if(el('role-skip').checked){
  const before=roleRead();
  const hasDetail=before.episodes.some(x=>x.origin||x.example.trim())||
    before.summary.trim()||before.pattern||before.conditions.trim();
  if(hasDetail && !window.confirm('Skip this question and discard its unsaved draft response?')){
   el('role-skip').checked=false;
   return;
  }
  el('role-no-event').checked=false;
  for(let i=0;i<3;i++){el('role-origin-'+i).value='';el('role-case-'+i).value='';}
  rolePatternEl.value='';el('role-conditions').value='';el('role-short').value='';
 }
 roleRemember();
});
el('role-clear').onclick=()=>{
 if(state.roleEntry && !window.confirm('Clear only the new role-entry response? Earlier 25 V3 and eight V3.2 answers remain.'))return;
 state.roleEntry=null;roleShow();
};
el('role-export').onclick=()=>el('export').click();
function roleFocus(){
 document.body.classList.add('role-focus');
 el('role-show-existing').textContent='Show previous questions';
}
el('role-show-existing').onclick=()=>{
 const hidden=document.body.classList.toggle('role-focus');
 el('role-show-existing').textContent=hidden?'Show previous questions':'Hide previous questions';
};

roleShow();
"""


def once(s: str, old: str, new: str) -> str:
    n = s.count(old)
    if n != 1:
        raise ValueError(f"Unique V3.2 anchor missing or repeated {n}: {old[:80]}")
    return s.replace(old, new, 1)


def build() -> bytes:
    s = BASE.read_text(encoding="utf-8")
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert protocol["status"] == "DEVELOPMENT_ONLY_NOT_SCORED"
    assert len(protocol["allowed_origins"]) == 7
    assert len(protocol["pattern_choices"]) == 6
    start = '<script id="pilot-data" type="application/json">'
    i = s.index(start) + len(start)
    j = s.index("</script>", i)
    payload = json.loads(s[i:j])
    assert len(payload["questions"]) == 25
    assert len(payload["v32"]["items"]) == 8
    payload["role_probe"] = protocol
    encoded = (
        json.dumps(payload, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )
    s = s[:i] + encoded + s[j:]
    s = once(
        s,
        "<title>Life Patterns — V3.2 experimental questionnaire</title>",
        "<title>Life Patterns — V3.3 optional role-entry clarification</title>",
    )
    s = once(
        s,
        "<h1>Life Patterns — V3.2 experimental questionnaire</h1>",
        "<h1>Life Patterns — V3.3 optional role-entry clarification</h1>",
    )
    s = once(
        s,
        '<section aria-labelledby="section-import">',
        SECTION + '<section aria-labelledby="section-import">',
    )
    s = once(
        s,
        "const state={answers:{},unique:[],v32:{}};",
        "const state={answers:{},unique:[],v32:{},roleEntry:null};",
    )
    s = once(
        s,
        "![storedSchema,'local_life_patterns_v3_2_pilot_unsubmitted'].includes(input.schema)",
        "![storedSchema,'local_life_patterns_v3_2_pilot_unsubmitted','local_life_patterns_v3_3_pilot_unsubmitted'].includes(input.schema)",
    )
    s = once(
        s,
        "return {answers,unique,v32};",
        """const roleRecord=input.role_entry_review;
 let roleEntry=null;
 if(roleRecord!==undefined && roleRecord!==null){
  const origins=new Set(d.role_probe.allowed_origins.map(x=>x.id));
  const patterns=new Set(d.role_probe.pattern_choices.map(x=>x.id));
  if(typeof roleRecord!=='object'||Array.isArray(roleRecord)||
     !Array.isArray(roleRecord.episodes)||roleRecord.episodes.length!==3||
     typeof roleRecord.pattern!=='string'||!(['',...patterns].includes(roleRecord.pattern))||
     (roleRecord.summary!=null && typeof roleRecord.summary!=='string')||
     typeof roleRecord.conditions!=='string'||typeof roleRecord.skip!=='boolean'||
     typeof roleRecord.no_event!=='boolean')throw new Error('Invalid role-entry response.');
  for(const ep of roleRecord.episodes){
   if(!ep||typeof ep!=='object'||Array.isArray(ep)||typeof ep.origin!=='string'||
      typeof ep.example!=='string'||(ep.origin!==''&&!origins.has(ep.origin)))
     throw new Error('Invalid role-entry occasion.');
  }
  roleEntry={
   summary:roleRecord.summary||'',
   episodes:roleRecord.episodes.map(ep=>({origin:ep.origin,example:ep.example})),
   pattern:roleRecord.pattern,conditions:roleRecord.conditions,
   skip:roleRecord.skip,no_event:roleRecord.no_event
  };
 }
 return {answers,unique,v32,roleEntry};""",
    )
    s = once(
        s,
        "Object.keys(state.v32).length>0 || state.unique.length>0 ||",
        "Object.keys(state.v32).length>0 || roleHasData(state.roleEntry) || state.unique.length>0 ||",
    )
    s = once(
        s,
        "JSON.stringify({schema:'local_life_patterns_v3_2_pilot_unsubmitted',answers:state.answers,unique_behaviors:state.unique,v3_2_answers:state.v32},null,2)",
        "JSON.stringify({schema:'local_life_patterns_v3_3_pilot_unsubmitted',answers:state.answers,unique_behaviors:state.unique,v3_2_answers:state.v32,role_entry_review:state.roleEntry},null,2)",
    )
    s = once(
        s,
        "link.download='my-life-patterns-v3-2-local-pilot.json'",
        "link.download='my-life-patterns-v3-3-role-entry.json'",
    )
    s = once(
        s,
        "state.answers={};state.unique=[];state.v32={};emptyEditor();v32Show();",
        "state.answers={};state.unique=[];state.v32={};state.roleEntry=null;emptyEditor();v32Show();roleShow();",
    )
    s = once(
        s,
        "state.answers=parsed.answers;state.unique=parsed.unique;state.v32=parsed.v32;v32Show();",
        "state.answers=parsed.answers;state.unique=parsed.unique;state.v32=parsed.v32;state.roleEntry=parsed.roleEntry;v32Show();roleShow();roleFocus();",
    )
    s = once(
        s,
        "state.answers=restored.answers;state.unique=restored.unique;state.v32=restored.v32;v32Show();",
        "state.answers=restored.answers;state.unique=restored.unique;state.v32=restored.v32;state.roleEntry=restored.roleEntry;v32Show();roleShow();roleFocus();",
    )
    s = once(
        s,
        "</style></head>",
        "body.role-focus main > section:not(#role-entry-section){display:none!important}</style></head>",
    )
    s = once(s, "if(d.prefilled_export){", SCRIPT + "if(d.prefilled_export){")
    # Prefilled respondent is automatically led to the missing distinction,
    # but skipped/answered sources must not be re-prompted.
    s = once(
        s,
        "el('import-feedback').textContent='Your saved pilot answers were loaded privately. Continue with the first outstanding follow-up.';",
        """el('import-feedback').textContent='Your saved answers were loaded privately. The only new role-entry clarification is above.';
  if(!roleHasData(state.roleEntry) && Object.keys(state.answers).length===25){
   el('role-entry-section').scrollIntoView({block:'start'});
   el('role-title').focus({preventScroll:true});
  }""",
    )
    return s.encode("utf-8")


if __name__ == "__main__":
    import sys

    content = build()
    if "--check" in sys.argv:
        assert OUTPUT.read_bytes() == content, "Generated role-entry pilot has drifted"
        print("V33_GENERATED_MATCH", len(content))
    else:
        OUTPUT.write_bytes(content)
        print("V33_GENERATED", len(content))
