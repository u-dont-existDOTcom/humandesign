# ruff: noqa: E501  # HTML/CSS/JS template owns its own source line lengths.
"""Generate a standalone, no-network, unsaved-by-default survey-design pilot.

The HTML is generated from a separately versioned, unscored question bank.
Only an explicit export saves participant-entered responses to a local file.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "EXPERIENCE-MEANING-PILOT-v1.json"
OUTPUT = HERE / "EXPERIENCE-MEANING-PILOT-v1.html"

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Life Patterns — Experience and Meaning (optional pilot)</title>
<style>
:root{font:16px/1.55 system-ui,-apple-system,sans-serif;color:#22303c;background:#f7f9fa}
*{box-sizing:border-box}
body{margin:0}main{width:min(760px,100%);margin:auto;padding:clamp(1rem,3vw,2rem) 1rem 5rem}
h1{font-size:clamp(1.45rem,3vw,2.05rem);line-height:1.2;letter-spacing:-.03em}
h2{font-size:1.3rem;line-height:1.3}p{margin:.6rem 0 1rem}
.panel{border:1px solid #d7e0e6;border-radius:12px;padding:clamp(1rem,3vw,1.6rem);margin:1rem 0;background:white}
header{border-bottom:1px solid #ccd6dd;padding-bottom:.75rem;margin-bottom:1.2rem}
.eyebrow{font-size:.82rem;letter-spacing:.08em;text-transform:uppercase;color:#536b7c;font-weight:700}
.note{padding:.75rem 1rem;border-left:3px solid #69839a;background:#eef3f6}
.small{font-size:.87rem;color:#526474}.row{display:flex;gap:.65rem;flex-wrap:wrap;align-items:center;margin:.9rem 0}
button,input,select,textarea{font:inherit}button{border:1px solid #74889a;background:#eef3f7;color:#172b3e;padding:.6rem 1rem;border-radius:7px;cursor:pointer;min-height:42px}
button.primary{background:#204e70;color:white;border-color:#204e70}
button:disabled{opacity:.45;cursor:not-allowed}button:hover:not(:disabled){filter:brightness(.96)}
label{display:block;font-weight:650;margin:1rem 0 .3rem}
select,textarea,input[type=text],input[type=file]{display:block;width:100%;max-width:100%;padding:.65rem;border:1px solid #8b9baa;border-radius:7px;background:#fff;color:inherit}
textarea{min-height:90px;resize:vertical}
button:focus-visible,select:focus-visible,textarea:focus-visible,input:focus-visible{outline:3px solid #246da4;outline-offset:2px}
.choice{display:flex;align-items:flex-start;gap:.65rem;font-weight:400;padding:.35rem 0}.choice input{margin-top:.35rem}
#notice{min-height:1.6rem;color:#903d22;font-weight:600}
#progress{font-size:.88rem;color:#526474;font-variant-numeric:tabular-nums}
#prompt{font-size:1.12rem;font-weight:650;line-height:1.5}
details{border-top:1px solid #e1e8ec;margin:1rem 0;padding:.8rem 0}
summary{cursor:pointer;font-weight:650}
ul{padding-left:1.4rem}li{margin:.4rem 0} .subtle{color:#5d6d7a;font-size:.9rem}
[hidden]{display:none!important}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
</style>
</head>
<body>
<main>
<header><p class="eyebrow">Development instrument · Separate opt-in</p><h1>Experience and meaning</h1>
<p>A small optional interview about surprise, awe, sudden insights and the meaning of life, with extra topics only if you choose them.</p></header>
<section id="start" class="panel">
<h2>Before you begin</h2>
<p id="introduction"></p>
<p class="note">This file runs entirely on your device. Nothing is uploaded or automatically saved. Export your answers if you want to keep them. Closing the page without exporting loses unsaved changes.</p>
<p>You may choose “never,” “not sure,” or skip. Real-life examples are optional. The survey does not assume anything supernatural caused your experiences.</p>
<div class="row"><button id="begin" type="button" class="primary">I choose to try the optional pilot</button></div>
<label for="import">Or import an earlier export from this pilot</label><input id="import" type="file" accept=".json,application/json">
<p class="small" id="import-message" role="status" aria-live="polite"></p>
</section>
<section class="panel" id="question-panel" hidden>
<p class="eyebrow" id="progress"></p>
<h2 id="topic-title"></h2><p id="purpose" class="small"></p><p id="prompt"></p>
<div id="response-fields"></div>
<details id="context-panel"><summary>Optional context — only if useful</summary><p id="context-prompt"></p>
<label for="extra">Anything about the circumstances, earlier life or exceptions? (optional)</label>
<textarea id="extra" placeholder="An example is never required."></textarea></details>
<details><summary>Already answered this in an earlier interview?</summary>
<p class="small">Only mark this covered if you know the earlier answer directly addressed this exact experience. A nearby hypothetical does not count. In a live interview the reviewer should check automatically.</p>
<label for="earlier-source">Source or question reference</label><input type="text" id="earlier-source" placeholder="For example: interview Q42, exact relevant passage">
<button type="button" id="mark-covered">Mark already covered</button>
</details>
<p id="notice" role="alert" aria-live="polite"></p>
<div class="row"><button type="button" id="back">Back</button>
<button type="button" id="skip">Skip this question</button>
<button type="button" id="unknown">I cannot say</button>
<button type="button" class="primary" id="save">Save answer &amp; continue</button></div>
</section>
<section class="panel" id="topics" hidden>
<p class="eyebrow">Optional coverage check</p><h2>Would you like any further topics?</h2>
<p>None is required. Choosing a topic says nothing about how often you experience it.</p>
<div id="topic-options"></div>
<div class="row"><button type="button" id="topics-back">Back to previous answer</button>
<button type="button" id="topics-done" class="primary">Continue / finish</button></div>
</section>
<section class="panel" id="complete" hidden>
<p class="eyebrow">Pilot export</p><h2>Your answers are ready to export</h2>
<p id="summary" role="status" aria-live="polite"></p>
<p>Not-asked, skipped, unknown, “never” and previously covered stay separate in the export. Nothing was sent to the live survey.</p>
<div class="row"><button type="button" id="export" class="primary">Export answers as JSON</button></div>
<label for="review-select">Review or edit a question</label><select id="review-select"></select>
<button type="button" id="edit">Edit selected question</button>
</section>
<footer><p class="subtle">Life Patterns experience/meaning v1 · development only · no astrology or Human Design scoring.</p></footer>
</main>
<script>
"use strict";
const BANK = __PILOT_DATA__;
const itemById = Object.fromEntries(BANK.items.map(function(item){return [item.id,item];}));
const byId = function(id){return document.getElementById(id);};
const records = {};
let phase = "start", cursor = 0, requested = [], editMode = false;
const startOrder = BANK.prompt_order.slice();

byId("introduction").textContent = BANK.participant_header;
function visible(id) {
  ["start","question-panel","topics","complete"].forEach(function(key){
    byId(key).hidden = key !== id;
  });
}
function flash(message) {byId("notice").textContent = message;}
function makeChoice(id, label, options, selected) {
  const wrapper = document.createElement("div");
  const lab = document.createElement("label");
  lab.htmlFor = id; lab.textContent = label;
  const input = document.createElement("select");
  input.id = id;
  const blank = document.createElement("option");
  blank.value = ""; blank.textContent = "Choose an answer (or skip)";
  input.appendChild(blank);
  options.forEach(function(row){
    const opt = document.createElement("option");
    opt.value = row[0]; opt.textContent = row[1];
    input.appendChild(opt);
  });
  input.value = selected || "";
  wrapper.append(lab, input);
  return wrapper;
}
function questionIds() {
  return phase === "optional" ? requested : startOrder;
}
function activeId() {return questionIds()[cursor];}
function showQuestion() {
  visible("question-panel");
  flash("");
  const ids = questionIds();
  const item = itemById[activeId()];
  const r = records[item.id] || {};
  byId("progress").textContent = (phase === "core" ? "Core topics" : "Additional topics") + " · " + (cursor+1) + " of " + ids.length;
  byId("topic-title").textContent = item.construct.replaceAll("_"," ").replace(/^./,function(ch){return ch.toUpperCase();});
  byId("purpose").textContent = item.purpose;
  byId("prompt").textContent = item.question;
  byId("context-prompt").textContent = item.optional_followup;
  byId("earlier-source").value = r.source_ref || "";
  byId("extra").value = r.note || "";
  const fields = byId("response-fields");
  fields.replaceChildren();
  if (item.mode === "dual_meaning") {
    item.prompt_fields.forEach(function(field){
      fields.appendChild(makeChoice(field.key,field.label,BANK.meaning_options, r.values && r.values[field.key]));
    });
  } else {
    const options = item.mode === "predictability" ? BANK.predictability_options : BANK.frequency_options;
    fields.appendChild(makeChoice("primary-answer",item.mode === "predictability" ? "How predictable?" : "How often?",options,r.value || (r.state==="NEVER"?"never":r.state==="UNKNOWN"?"unknown":r.state==="SKIPPED"?"skip":"")));
    if (item.mode === "frequency") {
      const s = makeChoice("intensity",item.optional_intensity,BANK.intensity_options,r.intensity);
      s.id = "intensity-wrap";
      fields.appendChild(s);
      byId("primary-answer").addEventListener("change",adjustContext);
    }
  }
  adjustContext();
  byId("back").disabled = editMode ? false : (phase==="core" && cursor===0);
  byId("save").textContent = editMode ? "Save edit" : "Save answer & continue";
  byId("prompt").scrollIntoView({block:"nearest"});
}
function adjustContext() {
  const item = itemById[activeId()];
  let show = true;
  if (item.mode === "frequency") {
    const v = byId("primary-answer").value;
    show = !["","never","unknown","skip"].includes(v);
    byId("intensity-wrap").hidden = !show;
    if (!show) byId("intensity").value = "";
  }
  if (item.mode === "predictability") {
    show = !["","unknown","skip"].includes(byId("primary-answer").value);
  }
  byId("context-panel").hidden = !show;
}
function resolve(state) {
  const item = itemById[activeId()];
  records[item.id] = {question_id:item.id,state:state};
  advance();
}
function readAnswer() {
  const item = itemById[activeId()];
  const note = byId("extra").value.trim();
  if (item.mode === "dual_meaning") {
    const a = byId("personal_meaning").value, b = byId("perceived_contribution").value;
    if (!a && !b) return null;
    return {question_id:item.id,state:"ANSWERED",values:{personal_meaning:a||"not_answered",perceived_contribution:b||"not_answered"},note:note};
  }
  const answer = byId("primary-answer").value;
  if (!answer) return null;
  if (answer==="never") return {question_id:item.id,state:"NEVER"};
  if (answer==="unknown") return {question_id:item.id,state:"UNKNOWN"};
  if (answer==="skip") return {question_id:item.id,state:"SKIPPED"};
  const r = {question_id:item.id,state:"ANSWERED",value:answer};
  if (item.mode==="frequency" && byId("intensity").value) r.intensity=byId("intensity").value;
  if (note) r.note=note;
  return r;
}
function advance() {
  if (editMode) { editMode=false; showComplete(); return; }
  cursor++;
  if (cursor < questionIds().length) {showQuestion();return;}
  if (phase === "core") {showTopics();return;}
  showComplete();
}
function showTopics() {
  phase="topics"; visible("topics");
  const holder=byId("topic-options"); holder.replaceChildren();
  BANK.other_prompt_order.forEach(function(id){
    const label=document.createElement("label");label.className="choice";
    const checkbox=document.createElement("input");
    checkbox.type="checkbox";checkbox.value=id;checkbox.checked=requested.includes(id);
    const name=document.createElement("span");
    name.textContent=BANK.topic_selection.labels[id];
    label.append(checkbox,name);holder.appendChild(label);
  });
}
function showComplete() {
  phase="done"; visible("complete");
  const answered=Object.values(records).filter(function(x){return x.state==="ANSWERED"||x.state==="NEVER";}).length;
  const skipped=Object.values(records).filter(function(x){return x.state==="SKIPPED";}).length;
  const unknown=Object.values(records).filter(function(x){return x.state==="UNKNOWN";}).length;
  const covered=Object.values(records).filter(function(x){return x.state==="ALREADY_COVERED";}).length;
  byId("summary").textContent = answered+" substantive answers, "+skipped+" skipped, "+unknown+" uncertain, "+covered+" already covered. "+(BANK.items.length-Object.keys(records).length)+" not asked.";
  const select=byId("review-select");select.replaceChildren();
  BANK.items.forEach(function(item) {
    const option=document.createElement("option");option.value=item.id;
    option.textContent=item.id+" — "+item.construct.replaceAll("_"," ");
    select.appendChild(option);
  });
}
byId("begin").addEventListener("click",function(){phase="core";cursor=0;showQuestion();});
byId("save").addEventListener("click",function(){
  const r=readAnswer();
  if(!r) {flash("Choose an answer, or select Skip or I cannot say.");return;}
  records[r.question_id]=r;advance();
});
byId("skip").addEventListener("click",function(){resolve("SKIPPED");});
byId("unknown").addEventListener("click",function(){resolve("UNKNOWN");});
byId("mark-covered").addEventListener("click",function(){
  const ref=byId("earlier-source").value.trim();
  if(!ref){flash("Provide the exact earlier response or source reference first.");return;}
  records[activeId()]={question_id:activeId(),state:"ALREADY_COVERED",source_ref:ref};
  advance();
});
byId("back").addEventListener("click",function(){
  if(editMode){editMode=false;showComplete();return;}
  if(cursor>0){cursor--;showQuestion();return;}
  if(phase==="optional"){showTopics();return;}
});
byId("topics-back").addEventListener("click",function(){phase="core";cursor=startOrder.length-1;showQuestion();});
byId("topics-done").addEventListener("click",function(){
  requested=Array.from(byId("topic-options").querySelectorAll("input:checked")).map(function(x){return x.value;});
  if(requested.length){phase="optional";cursor=0;showQuestion();}else{showComplete();}
});
function exportData() {
  return {schema:"life-patterns-experience-pilot-answers-v1",instrument:BANK.version,recorded_at:new Date().toISOString(),no_birth_or_chart_data:true,no_scoring:true,topics_selected:requested.slice(),responses:BANK.items.map(function(x){
    return records[x.id] || {question_id:x.id,state:"NOT_ASKED"};
  })};
}
byId("export").addEventListener("click",function(){
  const raw=JSON.stringify(exportData(),null,2);
  const url=URL.createObjectURL(new Blob([raw],{type:"application/json"}));
  const anchor=document.createElement("a");anchor.href=url;anchor.download="Life-Patterns-Experience-Pilot-v1-answers.json";
  anchor.click();setTimeout(function(){URL.revokeObjectURL(url);},1000);
});
byId("edit").addEventListener("click",function(){
  const id=byId("review-select").value;
  if(!itemById[id])return;
  editMode=true;
  if(startOrder.includes(id)){phase="core";cursor=startOrder.indexOf(id);}
  else {if(!requested.includes(id))requested.push(id);phase="optional";cursor=requested.indexOf(id);}
  showQuestion();
});
byId("import").addEventListener("change",async function(){
  const file=byId("import").files && byId("import").files[0];
  if(!file)return;
  try {
    const data=JSON.parse(await file.text());
    if(data.schema!=="life-patterns-experience-pilot-answers-v1"||data.instrument!==BANK.version||!Array.isArray(data.responses))throw Error("Not an export of this pilot version.");
    const allowed=["ANSWERED","NEVER","SKIPPED","UNKNOWN","ALREADY_COVERED","NOT_ASKED"];
    const next={};
    data.responses.forEach(function(r){
      if(!r||!itemById[r.question_id]||!allowed.includes(r.state)||next[r.question_id])throw Error("Invalid response structure");
      if(r.state==="ALREADY_COVERED" && !(typeof r.source_ref==="string" && r.source_ref.trim()))throw Error("Covered item missing source reference");
      if(r.state!=="NOT_ASKED")next[r.question_id]=r;
    });
    const opt=new Set(BANK.other_prompt_order);
    if(!Array.isArray(data.topics_selected)||data.topics_selected.some(function(id){return !opt.has(id);}))throw Error("Invalid optional topics");
    Object.keys(records).forEach(function(id){delete records[id];});
    Object.assign(records,next);
    requested=Array.from(new Set(data.topics_selected));
    byId("import-message").textContent="Imported successfully. You can review and edit.";
    showComplete();
  } catch(e) {byId("import-message").textContent="Import failed: "+e.message;}
});
visible("start");
</script>
</body></html>
'''

def build() -> Path:
    bank = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert bank["status"] == "DEVELOPMENT_OPTIONAL_NOT_LIVE_NOT_SCORED"
    assert len(bank["items"]) == 8
    rendered = HTML.replace(
        "__PILOT_DATA__",
        json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c"),
    )
    assert "__PILOT_DATA__" not in rendered
    OUTPUT.write_text(rendered, encoding="utf-8")
    return OUTPUT

if __name__ == "__main__":
    print(build())
