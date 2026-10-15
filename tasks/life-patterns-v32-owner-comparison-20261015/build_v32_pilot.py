# ruff: noqa: E501  # Long embedded HTML/JS and private report text are kept readable as strings.
"""Build an offline V3.2 cognitive questionnaire; never modify frozen V3."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / "tasks/life-patterns-idiographic-20261010/LIFE_PATTERNS_V3_OFFLINE_PILOT.html"
REVS = (
    ROOT
    / "tasks/life-patterns-guided-eight-assessment-20261015/V3_2_COGNITIVE_QUESTION_CANDIDATES.json"
)
OUT = HERE / "LIFE_PATTERNS_V32_OFFLINE_PILOT.html"

SECTION = """
<section aria-labelledby="v32-title" id="v32-section">
<h2 id="v32-title">V3.2 — revised questions (experimental)</h2>
<p>Six prompts seek specific behavior rather than general principles. The two optional items M05 and M03 remain <strong>excluded from chart scoring</strong> pending better evidence. You can skip any question.</p>
<p><strong>Returning participant:</strong> the old V3 selections, conditions and real examples remain below for reference. They are not silently counted as new V3.2 responses. You do not need to repeat what you have already described.</p>
<p class="small">Development questionnaire only; fully offline; no birth-chart inference or automatic submission.</p>
<label for="v32-route">Revised question</label><select id="v32-route"></select>
<p id="v32-progress" class="small" role="status" aria-live="polite"></p>
<p id="v32-question" class="question-text"></p>
<p id="v32-purpose" class="small"></p>
<details><summary>See saved V3 answer and guided context</summary><div id="v32-old"></div></details>
<label for="v32-response">Answer the revised wording (optional)</label>
<textarea id="v32-response" rows="5" placeholder="What happened, what did you actually do, and which conditions mattered?"></textarea>
<div class="row">
<label class="example"><input type="checkbox" id="v32-no-event"> I cannot recall a relevant event</label>
<label class="example"><input type="checkbox" id="v32-skip"> Prefer to skip</label>
</div>
<p id="v32-abstain" class="small"></p>
<div class="row"><button type="button" id="v32-prev">Previous</button>
<button type="button" id="v32-next">Next question</button>
<button type="button" id="v32-export">Export V3.2 JSON</button></div>
<p id="v32-status" class="small" role="status" aria-live="polite"></p>
</section>
"""

SCRIPT = """
const v32Items=d.v32.items;
function v32Item(){return v32Items.find(q=>q.id===el('v32-route').value);}
function v32Answered(a){return !!(a&&(a.response.trim()||a.no_event||a.skip));}
function v32Progress(){
 const n=v32Items.filter(q=>v32Answered(state.v32[q.id])).length;
 el('v32-progress').textContent=n+' of 8 V3.2 prompts addressed (6 core, 2 optional).';
}
function v32Show(){
 const item=v32Item();if(!item)return;
 const saved=state.v32[item.id]||{response:'',no_event:false,skip:false};
 const optional=['TF1-M05','TF1-M03'].includes(item.id);
 el('v32-question').textContent=item.candidate_question;
 el('v32-purpose').textContent=(optional?'Optional question, scoring suspended. ':'Core cognitive pilot. ')+item.what_to_compare;
 el('v32-abstain').textContent='Do not interpret as a trait if: '+item.abstain_if;
 el('v32-response').value=saved.response||'';
 el('v32-no-event').checked=saved.no_event===true;
 el('v32-skip').checked=saved.skip===true;
 el('v32-status').textContent=state.answers[item.id]
   ?'Prior answers already available; no need to repeat them unless testing this wording.'
   :'No earlier answer imported for this route.';
 const target=el('v32-old');target.replaceChildren();
 const old=state.answers[item.id];
 if(!old){const p=document.createElement('p');p.textContent='No previous V3 record';target.append(p);}
 else for(const [label,value] of [
  ['Selected examples',(old.selected||[]).join(' / ')],
  ['Own words',old.other],['Conditional rule',old.context_rule],
  ['Real example',old.recent_case],['No stable default',old.no_stable_default?'Yes':''],
  ['Prior skip',old.context_skipped?'Yes':'']
 ]){if(!value)continue;const p=document.createElement('p'),b=document.createElement('strong');
 b.textContent=label+': ';p.append(b,document.createTextNode(value));target.append(p);}
 v32Progress();
}
function v32Remember(){
 const id=el('v32-route').value;if(!id)return;
 const val={response:el('v32-response').value,no_event:el('v32-no-event').checked,skip:el('v32-skip').checked};
 if(v32Answered(val))state.v32[id]=val;else delete state.v32[id];
 v32Progress();
}
for(const item of v32Items){
 const opt=document.createElement('option');opt.value=item.id;
 opt.textContent=item.id+(['TF1-M05','TF1-M03'].includes(item.id)?' · optional':' · revised');
 el('v32-route').append(opt);
}
el('v32-route').addEventListener('change',v32Show);
el('v32-response').addEventListener('input',v32Remember);
for(const id of ['v32-no-event','v32-skip'])el(id).addEventListener('change',()=>{
 if(el(id).checked){el(id==='v32-no-event'?'v32-skip':'v32-no-event').checked=false;
  if(id==='v32-skip')el('v32-response').value='';}
 v32Remember();
});
function v32Move(delta){
 v32Remember();let idx=v32Items.findIndex(q=>q.id===el('v32-route').value);
 el('v32-route').value=v32Items[(idx+delta+v32Items.length)%v32Items.length].id;
 v32Show();el('v32-route').focus();
}
el('v32-next').onclick=()=>v32Move(1);
el('v32-prev').onclick=()=>v32Move(-1);
el('v32-export').onclick=()=>el('export').click();
v32Show();
"""


def one(s, old, new):
    assert s.count(old) == 1, ("Missing/duplicate generator anchor", old[:100], s.count(old))
    return s.replace(old, new, 1)


def build():
    s = OLD.read_text()
    revisions = json.loads(REVS.read_text())
    assert revisions["status"] == "DEVELOPMENT_ONLY_NOT_LIVE_NOT_SCORED"
    assert len(revisions["items"]) == len({x["id"] for x in revisions["items"]}) == 8
    marker = '<script id="pilot-data" type="application/json">'
    i = s.index(marker) + len(marker)
    j = s.index("</script>", i)
    data = json.loads(s[i:j])
    assert len(data["questions"]) == 25
    assert set(x["id"] for x in revisions["items"]) <= set(x["id"] for x in data["questions"])
    data["v32"] = revisions
    encoded = (
        json.dumps(data, ensure_ascii=False)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )
    s = s[:i] + encoded + s[j:]
    s = one(
        s,
        "<title>Life Patterns — Guided response and unusual behaviors pilot</title>",
        "<title>Life Patterns — V3.2 experimental questionnaire</title>",
    )
    s = one(
        s,
        "<h1>Life Patterns — guided responses and distinctive habits</h1>",
        "<h1>Life Patterns — V3.2 experimental questionnaire</h1>",
    )
    s = one(
        s,
        '<section aria-labelledby="section-questions">',
        SECTION + '<section aria-labelledby="section-questions">',
    )
    s = one(
        s,
        "Question examples (25 proposed variants)",
        "Earlier V3 questions (25 preserved and editable)",
    )
    s = one(s, "const state={answers:{},unique:[]};", "const state={answers:{},unique:[],v32:{}};")
    s = one(
        s,
        "input.schema!==storedSchema",
        "![storedSchema,'local_life_patterns_v3_2_pilot_unsubmitted'].includes(input.schema)",
    )
    s = one(
        s,
        "return {answers,unique};",
        """const raw32=input.v3_2_answers||{};
 if(!raw32||typeof raw32!=='object'||Array.isArray(raw32))
  throw new Error('Invalid V3.2 responses field.');
 const permitted=new Set(d.v32.items.map(q=>q.id)),v32={};
 for(const [id,val] of Object.entries(raw32)){
  if(!permitted.has(id)||!val||typeof val!=='object'||Array.isArray(val)||
    (val.response!=null&&typeof val.response!=='string')||
    (val.no_event!=null&&typeof val.no_event!=='boolean')||
    (val.skip!=null&&typeof val.skip!=='boolean'))
   throw new Error('Invalid V3.2 item '+id);
  v32[id]={response:val.response||'',no_event:val.no_event===true,skip:val.skip===true};
 }
 return {answers,unique,v32};""",
    )
    s = one(
        s,
        "return Object.keys(state.answers).length>0 || state.unique.length>0 ||",
        "return Object.keys(state.answers).length>0 || Object.keys(state.v32).length>0 || state.unique.length>0 ||",
    )
    s = one(
        s,
        "JSON.stringify({schema:storedSchema,answers:state.answers,unique_behaviors:state.unique},null,2)",
        "JSON.stringify({schema:'local_life_patterns_v3_2_pilot_unsubmitted',answers:state.answers,unique_behaviors:state.unique,v3_2_answers:state.v32},null,2)",
    )
    s = one(
        s,
        "link.download='my-life-patterns-v3-local-pilot.json'",
        "link.download='my-life-patterns-v3-2-local-pilot.json'",
    )
    s = one(
        s,
        "state.answers={};state.unique=[];emptyEditor();",
        "state.answers={};state.unique=[];state.v32={};emptyEditor();v32Show();",
    )
    s = one(
        s,
        "state.answers=parsed.answers;state.unique=parsed.unique;",
        "state.answers=parsed.answers;state.unique=parsed.unique;state.v32=parsed.v32;v32Show();",
    )
    s = one(
        s,
        "state.answers=restored.answers;state.unique=restored.unique;",
        "state.answers=restored.answers;state.unique=restored.unique;state.v32=restored.v32;v32Show();",
    )
    s = one(s, "if(d.prefilled_export){", SCRIPT + "if(d.prefilled_export){")
    return s.encode("utf-8")


if __name__ == "__main__":
    import sys

    payload = build()
    if "--check" in sys.argv:
        assert OUT.is_file() and OUT.read_bytes() == payload, "Generated HTML drift"
        print("V32_MATCHES_SOURCE", len(payload))
    else:
        OUT.write_bytes(payload)
        print("V32_GENERATED", len(payload))
