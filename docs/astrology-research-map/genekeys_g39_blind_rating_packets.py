"""G39 offline, respondent-blinded manipulation-check pack generator.

This prepares optional consenting RATER materials. It NEVER contacts anyone
or reads actual birth charts/participant outcomes. The packet shows prompts
and category names, but neither their intended category nor Gene Keys/HD
coordinates; researcher answer key is a SEPARATE artifact not in rater ZIP.
No network or third-party runtime dependencies.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import random
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BANK=ROOT/"GENEKEYS_G38_SIX_LINE_MESSAGE_BANK_DRAFT_V1.json"
SOURCE=ROOT/"GENEKEYS_G37_SIX_LINE_SOURCE_TESTABILITY_V1.json"
CONTRACT=ROOT/"GENEKEYS_G38_LINE_STYLE_STUDY_CONTRACT_DRAFT_V1.json"
SHA_BANK="fd3c880aa2cb84cd1f9c50eff0905f744d3b4d9bc22bf63f8ff825520976ecad"
SHA_SOURCE="2e53d6013037aeb40884df1da96390a27b7fbeb15828bb0a84342ddabd660b82"
SHA_CONTRACT="3ff656246104e58700b2fd49f122fcb97077ccfc50bd1549b0d2e537c0358559"
N_RATERS=6
N_ITEMS=24
CANDIDATE_SEED="G39_PUBLIC_NEUTRAL_STYLE_RATER_PACKETS_2026-10-25"

def sha_bytes(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def digest(x:object)->str:
    return sha_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,
                                separators=(",",":"),allow_nan=False).encode("utf8"))

def load_pin(p:Path,expect:str)->dict:
    if sha_bytes(p.read_bytes())!=expect:
        raise ValueError("accepted parent input has changed: "+p.name)
    return json.loads(p.read_text(encoding="utf8"))

def source_stimuli()->tuple[list[dict],list[str]]:
    from genekeys_g38_synthetic_line_preference import messages_from_bank
    bank=load_pin(BANK,SHA_BANK)
    source=load_pin(SOURCE,SHA_SOURCE)
    _=load_pin(CONTRACT,SHA_CONTRACT)
    src={v["line"]:v["brief_official_responds_best_to"]
         for v in source["verified_six_line_interpersonal_styles"]}
    if set(src)!=set(range(1,7)):
        raise ValueError("source six original lines absent")
    expected=messages_from_bank(bank)
    if len(expected)!=4 or any(len(v["messages"])!=6 for v in expected.values()):
        raise ValueError("missing scenario or communication style")
    rows=[]
    for item in bank["scenarios"]:
        scenario=item["id"]
        for style in range(1,7):
            contents=expected[scenario]["messages"][style]
            # Blind code intentionally reveals neither Line nor scenario ID.
            item_code="M-"+sha_bytes(
                (CANDIDATE_SEED+"|"+scenario+"|"+str(style)).encode())[:11].upper()
            for fact in item["facts"]:
                if contents.count(fact)!=1:
                    raise ValueError("factual core is not equal")
            rows.append({
                "item_code":item_code,
                "scenario":scenario,
                "source_line":style,
                "source_short_description":src[style],
                "facts":list(item["facts"]),
                "message":contents,
                "word_count":len(contents.split()),
                "message_sha256":sha_bytes(contents.encode("utf8"))
            })
    if len(rows)!=24 or len({r["item_code"] for r in rows})!=24:
        raise ValueError("invalid blinded item universe")
    return rows,[src[i] for i in range(1,7)]

def rotated_sequence(items:list,offset:int)->list:
    k=offset%len(items)
    return items[k:]+items[:k]

def html_render(rater_id:str,items:list[dict],cats:list[dict])->str:
    # The JSON visible to raters has NO source truth: no source_line key, no
    # numeric output, no gene-key name or natal data.
    shown=[
        {"code":r["item_code"],
         "text":r["message"],
         "facts":r["facts"]}
        for r in items
    ]
    cats_json=json.dumps(cats,ensure_ascii=False).replace("<","\\u003c")
    shown_json=json.dumps(shown,ensure_ascii=False).replace("<","\\u003c")
    template=r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Message style rating — anonymous optional review</title>
<style>
:root {color-scheme:light dark; font-family:system-ui,sans-serif;line-height:1.5}
body {margin:auto; max-width:760px; padding:18px}
h1 {font-size:1.35rem}
.note {opacity:.84;font-size:.92rem}
.message {border:1px solid #8886;border-radius:10px;padding:16px;white-space:pre-wrap;margin:16px 0;font-size:1.07rem}
fieldset {border:1px solid #8886;border-radius:10px;padding:12px;margin:12px 0}
legend {font-weight:600}
label {display:block;padding:5px 0}
button {cursor:pointer;padding:10px 16px;border:1px solid;border-radius:9px;font-size:1rem}
button:disabled {cursor:not-allowed;opacity:.4}
footer {padding-top:18px;font-size:.86rem}
#step {font-weight:600}
</style>
</head>
<body>
<h1>Message style rating — optional anonymous review</h1>
<p class="note">These are fictional workshop invitations, not actual events. Review one message at a time. Pick the single description that best fits the <strong>communication style</strong>, not which message you personally prefer. “None / unclear” is allowed. Every example is anonymous and is independent of any birth chart.</p>
<p class="note"><strong>Privacy:</strong> Do not enter names or identifying details. This page runs locally in your browser, does not connect to a website, and stores answers only in page memory until you choose to export a JSON file. You may close it without submitting anything. Share that file only if you voluntarily agree.</p>
<p id="step" aria-live="polite"></p>
<div id="card" class="message"></div>
<p class="note" id="facts"></p>
<form id="rate">
 <fieldset>
  <legend>Which description best captures the message's style?</legend>
  <div id="choices"></div>
 </fieldset>
 <fieldset><legend>How confident are you in your classification?</legend>
  <label><input type="radio" name="confidence" value="1" required> 1 — Very uncertain</label>
  <label><input type="radio" name="confidence" value="2"> 2 — Uncertain</label>
  <label><input type="radio" name="confidence" value="3"> 3 — Moderately confident</label>
  <label><input type="radio" name="confidence" value="4"> 4 — Confident</label>
  <label><input type="radio" name="confidence" value="5"> 5 — Very confident</label>
 </fieldset>
 <fieldset><legend>Does the message accurately preserve all three event facts listed above?</legend>
  <label><input type="radio" name="facts" value="yes" required> Yes</label>
  <label><input type="radio" name="facts" value="no"> No</label>
  <label><input type="radio" name="facts" value="unsure"> Unsure</label>
 </fieldset>
 <fieldset><legend>How natural would this message sound if you received it from a real person?</legend>
  <label><input type="radio" name="naturalness" value="1" required> 1 — Very unnatural</label>
  <label><input type="radio" name="naturalness" value="2"> 2 — Unnatural</label>
  <label><input type="radio" name="naturalness" value="3"> 3 — Neutral</label>
  <label><input type="radio" name="naturalness" value="4"> 4 — Natural</label>
  <label><input type="radio" name="naturalness" value="5"> 5 — Very natural</label>
 </fieldset>
 <fieldset><legend>How much interpersonal pressure does this message create?</legend>
  <label><input type="radio" name="perceived_pressure" value="1" required> 1 — None</label>
  <label><input type="radio" name="perceived_pressure" value="2"> 2 — Very little</label>
  <label><input type="radio" name="perceived_pressure" value="3"> 3 — Some</label>
  <label><input type="radio" name="perceived_pressure" value="4"> 4 — Considerable</label>
  <label><input type="radio" name="perceived_pressure" value="5"> 5 — Very high</label>
 </fieldset>
 <button id="next" type="submit">Save this rating and continue</button>
</form>
<div id="completed" hidden>
 <h2>Review complete</h2>
 <p>All 24 message ratings are ready. Nothing has been uploaded. Click below to save a JSON file and send it only if you choose.</p>
 <button type="button" id="export">Export anonymous ratings (.json)</button>
</div>
<footer>Packet: @@RATER@@. This evaluates message wording only; it does not test a medical treatment, genetic claim, personality, or astrology prediction. No payment or account required.</footer>
<script>
"use strict";
const packet="@@RATER@@";
const items=@@ITEMS_JSON@@;
const categories=@@CATEGORIES_JSON@@;
let current=0;
const responses=[];
const form=document.getElementById("rate");
const step=document.getElementById("step");
const card=document.getElementById("card");
const facts=document.getElementById("facts");
const choices=document.getElementById("choices");
function showItem(){
 const x=items[current];
 step.textContent="Message "+(current+1)+" of "+items.length+" • "+x.code;
 card.textContent=x.text;
 facts.textContent="Check these factual claims: "+x.facts.join(" ");
 choices.textContent="";
 for(const cat of categories.concat([{code:"U",name:"None / unclear"}])){
  const label=document.createElement("label");
  const input=document.createElement("input");
  input.type="radio";input.name="category";input.value=cat.code;input.required=true;
  label.appendChild(input);
  label.appendChild(document.createTextNode(" "+cat.name));
  choices.appendChild(label);
 }
 form.reset();
 document.getElementById("next").textContent=
   current===items.length-1?"Finish and prepare local export":"Save this rating and continue";
}
form.addEventListener("submit",function(event){
 event.preventDefault();
 if(!form.reportValidity())return;
 const x=items[current];
 const data=new FormData(form);
 responses.push({item_code:x.code,category_code:data.get("category"),
                 confidence:Number(data.get("confidence")),facts_check:data.get("facts"),
                 naturalness:Number(data.get("naturalness")),
                 perceived_pressure:Number(data.get("perceived_pressure"))});
 current++;
 if(current<items.length){showItem();}
 else {
  form.hidden=true;
  step.textContent="All "+items.length+" items rated.";
  card.hidden=true;facts.hidden=true;
  document.getElementById("completed").hidden=false;
 }
});
document.getElementById("export").addEventListener("click",function(){
 if(responses.length!==items.length)return;
 const result={schema:"G39_ANONYMOUS_OPTIONAL_BLIND_MESSAGE_RATER_V1",
  packet_id:packet,synthetic_messages_only:true,respondent_bio_data_collected:false,
  independent_of_respondent_birth_chart:true,ratings:responses};
 const blob=new Blob([JSON.stringify(result,null,2)+"\n"],{type:"application/json"});
 const url=URL.createObjectURL(blob);
 const a=document.createElement("a");
 a.href=url;a.download="G39_"+packet+"_optional_ratings.json";
 document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(url);},1000);
});
showItem();
</script>
</body>
</html>
"""
    result=template.replace("@@RATER@@",html.escape(rater_id,quote=True))
    result=result.replace("@@ITEMS_JSON@@",shown_json)
    result=result.replace("@@CATEGORIES_JSON@@",cats_json)
    # Study source truth must never appear, even in client-readable JS.
    for bad in ("source_line","target_line","Gene Keys","Human Design","intended_category"):
        if bad in result:
            raise AssertionError("rater packet leaks experimental source: "+bad)
    if "<script src=" in result or "http://" in result or "https://" in result:
        raise AssertionError("rater page must be fully offline")
    return result


def generate(*,out_dir:Path)->tuple[dict,list[Path]]:
    rows,styles=source_stimuli()
    base=rows.copy()
    random.Random(int(sha_bytes(CANDIDATE_SEED.encode())[:15],16)).shuffle(base)
    out_dir.mkdir(parents=True,exist_ok=True)
    packet_data=[]
    produced=[]
    for k in range(N_RATERS):
        rid=f"R{k+1:02d}"
        order=rotated_sequence(base,4*k)
        descriptions=[
            {"code":"C"+sha_bytes((CANDIDATE_SEED+"|"+rid+"|"+str(line)).encode())[:9].upper(),
             "name":styles[line-1]}
            for line in range(1,7)
        ]
        # Shuffle category display order independent of actual message targets
        rng=random.Random(int(sha_bytes((CANDIDATE_SEED+"|CAT|"+rid).encode())[:15],16))
        rng.shuffle(descriptions)
        path=out_dir/(f"G39_Anonymous_Message_Reviewer_{rid}.html")
        path.write_text(html_render(rid,order,descriptions),encoding="utf8")
        produced.append(path)
        packet_data.append({
            "packet_id":rid,
            "rater_html_basename":path.name,
            "rater_html_sha256":sha_bytes(path.read_bytes()),
            "item_order":[r["item_code"] for r in order],
            "public_category_code_to_original_source_line":{
                a["code"]:styles.index(a["name"])+1 for a in descriptions},
            "category_label_order":[x["code"] for x in descriptions],
        })
    answer_key={
        "schema":"G39_RESEARCHER_ONLY_SOURCE_STIMULUS_KEY_V1",
        "synthetic_stimuli_only":True,
        "research_only_do_NOT_distribute_this_key_with_rater_HTML":True,
        "original_G38_parent_git_commit":
             "40ac0e2aa07f992843180c51bf923d9baf05125d",
        "input_source_sha256":SHA_SOURCE,
        "input_bank_sha256":SHA_BANK,
        "input_contract_sha256":SHA_CONTRACT,
        "n_rater_packets":N_RATERS,
        "n_items_per_rater":N_ITEMS,
        "no_genuine_independent_rater_answers_collected":True,
        "no_human_natal_predictions":True,
        "no_active_participant_study_changes":True,
        "reviewer_rating_prompt_is_classification_not_own_preference":True,
        "target_style_defined_by_researcher_messages_not_original_Rudd_text":True,
        "actual_source_text_equivalence_rated_by_humans":False,
        "rater_packets":packet_data,
        "items":[{
            "item_code":r["item_code"],
            "source_scenario":r["scenario"],
            "researcher_intended_style_original_line":r["source_line"],
            "original_message_sha256":r["message_sha256"],
            "n_words":r["word_count"],
        } for r in rows],
    }
    answer_key["research_key_body_sha256"]=digest(answer_key)
    return answer_key,produced


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--html-dir",type=Path,required=True)
    p.add_argument("--research-key",type=Path,required=True)
    args=p.parse_args()
    key,files=generate(out_dir=args.html_dir)
    if args.research_key.exists():
        raise FileExistsError("researcher key exists: no overwrite")
    args.research_key.write_text(
        json.dumps(key,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf8")
    print("G39_BLIND_PACKET_BUILD",len(files),"packets x",
          key["n_items_per_rater"],"ratings",
          "research_key_SHA",key["research_key_body_sha256"])
    print("CANNOT_CLAIM_RATER_RESULTS",key["no_genuine_independent_rater_answers_collected"])


if __name__=="__main__":
    main()
