#!/usr/bin/env python3
"""Build the minimal-burden human-facing Life Patterns v2 calibration UI.

Only judgments that can change the planned human calibration are shown. Machine identifiers and
schema bookkeeping remain in exports but are not presented as human tasks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from build_life_patterns_human_calibration_ui_v2_plain_provenance import (
    build_plain_provenance_standalone_human_calibration_ui_v2,
)


def _replace_function(text: str, name: str, replacement: str) -> str:
    start = text.find(f"function {name}(")
    if start < 0:
        raise ValueError(f"auditor UI patch could not find function {name}")
    candidates = [
        text.find("\nfunction ", start + 1),
        text.find("\nconst attestQs=", start + 1),
        text.find("\n</script>", start + 1),
    ]
    end = min(value for value in candidates if value >= 0)
    return text[:start] + replacement + text[end:]


def _embedded_fragment(html: str) -> str:
    start = html.find("const EMBEDDED = ")
    end = html.find("\nconst OUTER = ", start)
    if start < 0 or end < 0:
        raise ValueError("auditor UI patch cannot locate embedded handoff payload")
    return html[start:end]


def patch_html_for_auditor(html: str) -> str:
    embedded_before = _embedded_fragment(html)
    html = html.replace(
        "</head>",
        """<style>
#advancedContext{display:none!important}
.value code{display:none!important}
.machineonly{display:none!important}
.quotelabel{font-weight:700}.quotesnippet{display:block;color:#46554f;margin-top:2px;line-height:1.35}
.relationchoice{display:grid;gap:8px;margin-top:9px}.relationchoice label{display:flex;gap:8px;align-items:flex-start;padding:10px 11px;border:1px solid #d4ddd8;border-radius:9px;background:#fff}
.orderbox{margin-top:10px;padding:11px 12px;border:1px solid #d8e2dc;border-radius:9px;background:#f8fbf9}.orderbox h4{margin:0 0 8px}
.ordereditem{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 0;border-top:1px solid #e5ece8}.ordereditem:first-of-type{border-top:0}.ordereditem .orderlabel{font-weight:650}.ordereditem button{min-width:34px}
.humanerror{margin:7px 0}
</style>
</head>""",
        1,
    )

    html = _replace_function(
        html,
        "renderSources",
        r'''function renderSources(u,r){const segments=u.task.exact_source_segments||[];const support=new Set(r.supporting_source_segment_ids||[]);const observed=r.state==="observed";const quoteName=i=>segments.length===1?"Exact quote":`Exact quote ${i+1}`;const quoteText=s=>s.exact_text||s.exact_participant_text||"";const cards=segments.map((s,i)=>`<article class="source"><div class="sourceid">${esc(quoteName(i))}</div><p>${esc(quoteText(s))}</p></article>`).join("");let provenance="";if(observed&&segments.length===1){const s=segments[0];provenance=`<input class="machineonly" type="checkbox" data-source="support" value="${esc(s.segment_id)}" checked>`}else if(observed&&segments.length>1){provenance=`<div class="provenancebox"><h3>Which quote(s) did you use for this Yes answer?</h3><p class="hint">Choose only the quote(s) that actually show the behavior you selected.</p><div class="provenancelist">${segments.map((s,i)=>`<label><input type="checkbox" data-source="support" value="${esc(s.segment_id)}" ${support.has(s.segment_id)?"checked":""}> <span><span class="quotelabel">${esc(quoteName(i))}</span><span class="quotesnippet">${esc(quoteText(s))}</span></span></label>`).join("")}</div></div>`}$("sources").innerHTML=cards+provenance}''',
    )

    html = _replace_function(
        html,
        "seriesFields",
        r'''function seriesFields(r){const status=r.exception_status||"";const strength=r.reported_recurrence_strength||"";const exceptionPart=status==="exceptions_reported"?selectField("exceptionFrequency","How often does the narrator say the exceptions happen?",["unknown","almost_never","sometimes","often","context_dependent","rough_rate_or_count"],r.exception_frequency||"unknown"):"";const countPart=strength==="bounded_rate_or_count"?`<div class="field"><label for="boundedDescription">What count or rate does the narrator actually state?</label><textarea id="boundedDescription">${esc(r.bounded_rate_or_count_description||"")}</textarea><div class="hint">Use only what the exact source actually gives. Do not estimate.</div></div>`:"";return`<div class="section"><h3>How often does the narrator say this behavior happens?</h3><p class="hint">This is about what the narrator reports, not an externally verified frequency.</p>${selectField("recurrenceStrength","How often?",RECURRENCE_STRENGTH,strength)}${selectField("exceptionStatus","Does the narrator report exceptions or limits?",EXCEPTION_STATUS,status)}${exceptionPart}${countPart}</div>`}''',
    )

    html = _replace_function(
        html,
        "renderObserved",
        r'''function renderObserved(u,r){const host=$("observedFields");if(r.state!=="observed"){host.innerHTML='<div class="section"><p class="hint">Nothing else is required for this answer.</p></div>';return}const subMap=new Map((u.resolved?.subcodes||[]).map(s=>[s.subcode_id,s]));const selected=new Set(r.coded_values||[]);const values=u.obs.allowed_values||[];const relation=r.value_relation||(selected.size===1?"single":"");let html=`<div class="section"><h3>Which behavior does the exact source show?</h3><div class="values">${values.map(v=>{const s=subMap.get(v);const non=u.ext.non_action_values.includes(v);return`<label class="value"><input type="checkbox" data-value="${esc(v)}" ${selected.has(v)?"checked":""}><div><span class="wording">${esc(plainBehavior(s?.wording,v))}</span></div>${non?'<span class="tag">extra check required</span>':""}</label>`}).join("")}</div></div>`;if(selected.size>1){html+=`<div class="section"><h3>You selected more than one behavior. Does the story say they happened in a particular order?</h3><div class="relationchoice"><label><input type="radio" name="valueRelationHuman" value="ordered_sequence" ${relation==="ordered_sequence"?"checked":""}> <span><b>Yes — the story gives an order</b><br><span class="hint">I can put them in order.</span></span></label><label><input type="radio" name="valueRelationHuman" value="unordered_multiple" ${relation==="unordered_multiple"?"checked":""}> <span><b>No — the order is not established</b><br><span class="hint">The source supports more than one behavior, but not their sequence.</span></span></label></div>${relation==="ordered_sequence"?'<div class="orderbox"><h4>Put the selected behaviors in the order they happened:</h4><div id="orderedValues"></div></div>':""}</div>`}if(u.kind==="series")html+=seriesFields(r);if(selected.has(u.ext.other_specified_value))html+=`<div class="section"><div class="field"><label for="osDescription">Describe the behavior that is not listed above</label><textarea id="osDescription">${esc(r.other_specified_description||"")}</textarea></div></div>`;if([...selected].some(v=>u.ext.non_action_values.includes(v)))html+=`<div class="section"><h3>Extra check for the “did not act” behavior you selected</h3><p class="hint">This option only counts when all four answers are Yes. If any answer is No or Can't tell, choose another behavior or Can't tell for the unit.</p><div class="gate">${["awareness","opportunity","feasibility","established_non_action"].map(k=>gateSelect(k,r.non_action_gate?.[k])).join("")}</div></div>`;host.innerHTML=html;host.querySelectorAll('[data-value]').forEach(x=>x.addEventListener("change",()=>renderObserved(u,readForm(u))));host.querySelectorAll('input[name="valueRelationHuman"]').forEach(x=>x.addEventListener("change",()=>{if(x.value==="ordered_sequence"&&!orderOverrides.has(u.key))orderOverrides.set(u.key,selectedValues());renderObserved(u,readForm(u))}));$("recurrenceStrength")?.addEventListener("change",()=>renderObserved(u,readForm(u)));$("exceptionStatus")?.addEventListener("change",()=>renderObserved(u,readForm(u)));if(relation==="ordered_sequence")renderOrdered()}''',
    )

    html = _replace_function(
        html,
        "renderOrdered",
        r'''function renderOrdered(){const host=$("orderedValues");if(!host)return;const u=units[current];const subMap=new Map((u.resolved?.subcodes||[]).map(s=>[s.subcode_id,s]));let vals=[...(orderOverrides.get(u.key)||selectedValues())];const selected=new Set(selectedValues());vals=vals.filter(v=>selected.has(v));for(const v of selected)if(!vals.includes(v))vals.push(v);orderOverrides.set(u.key,vals);host.innerHTML=vals.map((v,i)=>`<div class="ordereditem"><span class="orderlabel">${i+1}. ${esc(plainBehavior(subMap.get(v)?.wording,v))}</span><span>${i?`<button type="button" aria-label="Move up" data-move="up" data-v="${esc(v)}">↑</button>`:""}${i<vals.length-1?`<button type="button" aria-label="Move down" data-move="down" data-v="${esc(v)}">↓</button>`:""}</span></div>`).join("");host.querySelectorAll('[data-move]').forEach(b=>b.addEventListener("click",()=>moveValue(b.dataset.v,b.dataset.move)))}''',
    )

    html = _replace_function(
        html,
        "moveValue",
        r'''function moveValue(v,dir){const u=units[current];const vals=[...(orderOverrides.get(u.key)||selectedValues())];const i=vals.indexOf(v),j=dir==="up"?i-1:i+1;if(i<0||j<0||j>=vals.length)return;[vals[i],vals[j]]=[vals[j],vals[i]];orderOverrides.set(u.key,vals);renderOrdered()}''',
    )

    html = _replace_function(
        html,
        "renderCommon",
        r'''function renderCommon(u,r){$("missingFlags").innerHTML="";$("contextQualifiers").value="";$("lifePhase").value="";$("language").value="";$("note").value=""}''',
    )

    html = _replace_function(
        html,
        "readForm",
        r'''function readForm(u){const base=draftFromFormSeed(u);base.state=document.querySelector('input[name="state"]:checked')?.value||null;base.supporting_source_segment_ids=sourceSelections("support");base.counterevidence_source_segment_ids=[];base.context_qualifiers=[];base.missingness_flags=[];base.life_phase_qualifier=null;base.annotation_note=null;if(u.kind==="episode"){base.language=null;base.influence_relation="none_reported";base.influence_source_segment_ids=[]}if(base.state!=="observed")return base;let vals=selectedValues();const rel=vals.length===1?"single":document.querySelector('input[name="valueRelationHuman"]:checked')?.value||null;if(rel==="ordered_sequence"){const over=orderOverrides.get(u.key)||[];const set=new Set(vals);if(over.length===vals.length&&over.every(x=>set.has(x)))vals=[...over]}base.coded_values=vals;base.value_relation=rel;base.asserts_non_action=vals.some(v=>u.ext.non_action_values.includes(v));if(base.asserts_non_action){base.non_action_gate={};document.querySelectorAll('[data-gate]').forEach(x=>base.non_action_gate[x.dataset.gate]=x.value||null)}if(vals.includes(u.ext.other_specified_value))base.other_specified_description=$("osDescription")?.value.trim()||null;if(u.kind==="series"){base.reported_recurrence_strength=$("recurrenceStrength")?.value||null;base.exception_status=$("exceptionStatus")?.value||null;base.exception_frequency=base.exception_status==="exceptions_explicitly_denied"?"none_reported":base.exception_status==="exceptions_reported"?($("exceptionFrequency")?.value||"unknown"):null;base.frequency_evidence_basis=base.reported_recurrence_strength==="bounded_rate_or_count"?"bounded_rate_or_count_self_report":"generalized_self_report";base.minimum_reported_occurrences=null;base.bounded_rate_or_count_description=base.reported_recurrence_strength==="bounded_rate_or_count"?($("boundedDescription")?.value.trim()||null):null;base.recurrence_scope_description=null}return base}''',
    )

    html = _replace_function(
        html,
        "validate",
        r'''function validate(u,r){const e=[];const sourceIds=new Set(u.task.exact_source_segments.map(s=>s.segment_id));for(const arr of [r.supporting_source_segment_ids||[],r.counterevidence_source_segment_ids||[],r.influence_source_segment_ids||[]])for(const id of arr)if(!sourceIds.has(id))return["This saved response no longer matches this unit. Stop and report the technical problem."];if(!["observed","insufficient","not_applicable"].includes(r.state))e.push("Choose Yes, No, or Can't tell.");if(r.state==="observed"){if(!r.coded_values.length)e.push("Choose at least one behavior from the list.");if(r.coded_values.length===1&&r.value_relation!=="single")e.push("The page could not save your one selected behavior correctly. Reload the file and try again.");if(r.coded_values.length>1&&!['ordered_sequence','unordered_multiple'].includes(r.value_relation))e.push("You selected more than one behavior. Say whether the story gives a clear order.");if(!r.supporting_source_segment_ids.length)e.push(u.task.exact_source_segments.length>1?"Choose the quote(s) you relied on for this Yes answer.":"The page could not attach the exact quote to your Yes answer. Reload the file and try again.");const expectedNon=r.coded_values.some(v=>u.ext.non_action_values.includes(v));if(expectedNon&&(!r.non_action_gate||Object.values(r.non_action_gate).some(x=>x!=="established")))e.push("For the selected ‘did not act’ behavior, all four extra checks must be Yes. If any one is No or Can't tell, choose another behavior or Can't tell for the unit.");if(r.coded_values.includes(u.ext.other_specified_value)&&!r.other_specified_description)e.push("Describe the behavior that was not listed.");if(u.kind==="series"){if(!r.reported_recurrence_strength)e.push("Choose how often the narrator says this behavior recurs.");if(!r.exception_status)e.push("Choose whether the narrator reports exceptions or limits.");if(r.reported_recurrence_strength==="bounded_rate_or_count"&&!r.bounded_rate_or_count_description)e.push("Enter the count or rate that the narrator actually states.")}}return e}''',
    )

    html = _replace_function(
        html,
        "saveUnit",
        r'''function saveUnit(move){const u=units[current],r=readForm(u),errors=validate(u,r);if(errors.length){$("unitErrors").innerHTML=`<b>${errors.length===1?"One thing needs fixing before this can be saved:":"A few things need fixing before this can be saved:"}</b><ul>${errors.map(x=>`<li class="humanerror">${esc(x)}</li>`).join("")}</ul>`;$("unitErrors").classList.remove("hidden");return false}responses.set(u.key,r);$("unitErrors").classList.add("hidden");$("saveState").textContent="Saved on this page. Download progress if you want a durable backup.";updateProgress();if(move&&current<units.length-1){current++;render()}else render();return true}''',
    )

    if _embedded_fragment(html) != embedded_before:
        raise ValueError("auditor UI patch altered embedded private handoff bytes")
    outside = html.replace(_embedded_fragment(html), "")
    for obsolete in (
        "Use this quote as evidence for the behavior I selected",
        "This quote qualifies or goes against my selected behavior",
        "If more than one behavior is selected, how do they relate?",
        "Observed requires a value relation",
    ):
        if obsolete in outside:
            raise ValueError(f"auditor UI still exposes obsolete human-facing text: {obsolete}")
    return html


def build_auditor_standalone_human_calibration_ui_v2(
    handoff_zip: str | Path,
    output_html: str | Path,
    *,
    overwrite: bool = False,
) -> dict[str, Any]:
    output = Path(output_html)
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")
    with tempfile.TemporaryDirectory(prefix="life-patterns-ui-v2-auditor-") as temporary:
        previous = Path(temporary) / "previous.html"
        base_receipt = build_plain_provenance_standalone_human_calibration_ui_v2(
            handoff_zip,
            previous,
        )
        after = patch_html_for_auditor(previous.read_text(encoding="utf-8"))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(after, encoding="utf-8", newline="\n")
    raw = output.read_bytes()
    receipt = dict(base_receipt)
    receipt.update(
        schema_version="life-patterns-human-calibration-ui-auditor-build-receipt-v2",
        output_html_sha256=hashlib.sha256(raw).hexdigest(),
        output_html_bytes=len(raw),
        human_optional_auxiliary_fields_shown=False,
        single_value_relation_automatic=True,
        multi_value_relation_conditional=True,
        ordered_sequence_labels_human_readable=True,
        source_ids_human_visible=False,
        code_ids_human_visible=False,
        single_source_support_auto_bound=True,
        counterevidence_metadata_collected_from_human=False,
        influence_metadata_collected_from_human=False,
        validation_errors_humanized=True,
        embedded_private_handoff_unchanged=True,
        selected_calibration_units_changed=False,
        response_contract_changed=False,
        measurement_semantics_changed=False,
        target_model_information_used=False,
        automated_judgment_used=False,
        network_requests_required=False,
        supersedes_prior_auditor_ui_for_human_collection=True,
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-zip", type=Path, required=True)
    parser.add_argument("--output-html", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    receipt = build_auditor_standalone_human_calibration_ui_v2(
        args.handoff_zip,
        args.output_html,
        overwrite=args.overwrite,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
