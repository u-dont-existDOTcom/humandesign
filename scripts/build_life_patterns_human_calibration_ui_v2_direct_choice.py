#!/usr/bin/env python3
"""Build the Life Patterns v2 human auditor UI with direct behavior choice.

The auditor should never have to answer a meta-question such as whether there is "enough
information to code" before seeing what they are being asked to code. This presentation-only
layer puts the actual behavior choices first and derives the existing observed / insufficient /
not_applicable machine state from the human's direct choice.

The embedded handoff, selected units, response schemas, measurement semantics, blinding, and
offline boundary remain unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from build_life_patterns_human_calibration_ui_v2_auditor_final import (
    build_final_auditor_human_calibration_ui_v2,
)


def _replace_function(text: str, name: str, replacement: str) -> str:
    start = text.find(f"function {name}(")
    if start < 0:
        raise ValueError(f"direct-choice UI patch could not find function {name}")
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
        raise ValueError("direct-choice UI patch cannot locate embedded handoff payload")
    return html[start:end]


def patch_html_for_direct_behavior_choice(html: str) -> str:
    """Ask the behavioral question directly; machine applicability state is derived."""

    embedded_before = _embedded_fragment(html)
    html = html.replace(
        "</head>",
        """<style>
.fallbackchoices{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:14px}
.fallbackchoice{display:flex;gap:8px;align-items:flex-start;padding:11px 12px;border:1px solid #d4ddd8;border-radius:9px;background:#fafcfb}
.fallbackchoice b{display:block;margin-bottom:3px}
@media(max-width:700px){.fallbackchoices{grid-template-columns:1fr}}
</style>
</head>""",
        1,
    )

    html = _replace_function(
        html,
        "renderStates",
        r'''function renderStates(u,r){const subMap=new Map((u.resolved?.subcodes||[]).map(s=>[s.subcode_id,s]));const selected=new Set(r.coded_values||[]);const values=u.obs.allowed_values||[];const fallback=r.state==="insufficient"?"insufficient":r.state==="not_applicable"?"not_applicable":null;$("stateGrid").innerHTML=`<div style="grid-column:1/-1"><h3 style="margin:0 0 5px">Which behavior or behaviors does the exact source clearly show?</h3><p class="hint" style="margin:0 0 10px">Select every behavior that is clearly supported. If you cannot select one, use one of the two choices underneath.</p><div class="values">${values.map(v=>{const s=subMap.get(v);const non=u.ext.non_action_values.includes(v);return`<label class="value"><input type="checkbox" data-value="${esc(v)}" ${selected.has(v)?"checked":""}><div><span class="wording">${esc(plainBehavior(s?.wording,v))}</span></div>${non?'<span class="tag">extra check required</span>':""}</label>`}).join("")}</div><div class="fallbackchoices"><label class="fallbackchoice"><input type="radio" name="stateFallback" value="not_applicable" ${fallback==="not_applicable"?"checked":""}><span><b>Doesn't apply to this story</b><span class="hint">The situation required by the question is clearly absent.</span></span></label><label class="fallbackchoice"><input type="radio" name="stateFallback" value="insufficient" ${fallback==="insufficient"?"checked":""}><span><b>Not enough information</b><span class="hint">Some pieces may fit, but the exact source is too incomplete or unclear to choose a behavior reliably.</span></span></label></div></div>`;updateStateSemantics(u,r.state);$("stateGrid").querySelectorAll('[data-value]').forEach(x=>x.addEventListener("change",()=>{if(selectedValues().length)document.querySelectorAll('input[name="stateFallback"]').forEach(el=>el.checked=false);const next=readForm(u);renderSources(u,next);renderObserved(u,next);updateStateSemantics(u,next.state)}));$("stateGrid").querySelectorAll('input[name="stateFallback"]').forEach(x=>x.addEventListener("change",()=>{document.querySelectorAll('[data-value]').forEach(el=>el.checked=false);orderOverrides.delete(u.key);const next=readForm(u);renderSources(u,next);renderObserved(u,next);updateStateSemantics(u,next.state)}))}''',
    )

    html = _replace_function(
        html,
        "updateStateSemantics",
        r'''function updateStateSemantics(u,state){$("stateSemantics").textContent=state==="observed"?"The behavior choices you selected will be coded for this unit.":state==="not_applicable"?"No behavior is coded because the required situation is absent.":state==="insufficient"?"No behavior is coded because the exact source does not support a reliable choice.":""}''',
    )

    html = _replace_function(
        html,
        "renderObserved",
        r'''function renderObserved(u,r){const host=$("observedFields");const selected=new Set(r.coded_values||selectedValues());if(!selected.size){host.innerHTML="";return}const relation=r.value_relation||(selected.size===1?"single":"");let html="";if(selected.size>1){html+=`<div class="section"><h3>You selected more than one behavior. Does the story say they happened in a particular order?</h3><div class="relationchoice"><label><input type="radio" name="valueRelationHuman" value="ordered_sequence" ${relation==="ordered_sequence"?"checked":""}> <span><b>Yes — the story gives an order</b><br><span class="hint">I can put them in order.</span></span></label><label><input type="radio" name="valueRelationHuman" value="unordered_multiple" ${relation==="unordered_multiple"?"checked":""}> <span><b>No — the order is not established</b><br><span class="hint">The source supports more than one behavior, but not their sequence.</span></span></label></div>${relation==="ordered_sequence"?'<div class="orderbox"><h4>Put the selected behaviors in the order they happened:</h4><div id="orderedValues"></div></div>':""}</div>`}if(u.kind==="series")html+=seriesFields(r);if(selected.has(u.ext.other_specified_value))html+=`<div class="section"><div class="field"><label for="osDescription">Describe the behavior that is not listed above</label><textarea id="osDescription">${esc(r.other_specified_description||"")}</textarea></div></div>`;if([...selected].some(v=>u.ext.non_action_values.includes(v)))html+=`<div class="section"><h3>Extra check for the “did not act” behavior you selected</h3><p class="hint">This option only counts when all four answers are Yes. If any answer is No or Can't tell, choose another behavior or choose Not enough information for the unit.</p><div class="gate">${["awareness","opportunity","feasibility","established_non_action"].map(k=>gateSelect(k,r.non_action_gate?.[k])).join("")}</div></div>`;host.innerHTML=html;host.querySelectorAll('input[name="valueRelationHuman"]').forEach(x=>x.addEventListener("change",()=>{if(x.value==="ordered_sequence"&&!orderOverrides.has(u.key))orderOverrides.set(u.key,selectedValues());renderObserved(u,readForm(u))}));$("recurrenceStrength")?.addEventListener("change",()=>renderObserved(u,readForm(u)));$("exceptionStatus")?.addEventListener("change",()=>renderObserved(u,readForm(u)));if(relation==="ordered_sequence")renderOrdered()}''',
    )

    html = _replace_function(
        html,
        "readForm",
        r'''function readForm(u){const base=draftFromFormSeed(u);let vals=selectedValues();const fallback=document.querySelector('input[name="stateFallback"]:checked')?.value||null;base.state=vals.length?"observed":fallback;base.supporting_source_segment_ids=sourceSelections("support");base.counterevidence_source_segment_ids=[];base.context_qualifiers=[];base.missingness_flags=[];base.life_phase_qualifier=null;base.annotation_note=null;if(u.kind==="episode"){base.language=null;base.influence_relation="none_reported";base.influence_source_segment_ids=[]}if(base.state!=="observed")return base;const rel=vals.length===1?"single":document.querySelector('input[name="valueRelationHuman"]:checked')?.value||null;if(rel==="ordered_sequence"){const over=orderOverrides.get(u.key)||[];const set=new Set(vals);if(over.length===vals.length&&over.every(x=>set.has(x)))vals=[...over]}base.coded_values=vals;base.value_relation=rel;base.asserts_non_action=vals.some(v=>u.ext.non_action_values.includes(v));if(base.asserts_non_action){base.non_action_gate={};document.querySelectorAll('[data-gate]').forEach(x=>base.non_action_gate[x.dataset.gate]=x.value||null)}if(vals.includes(u.ext.other_specified_value))base.other_specified_description=$("osDescription")?.value.trim()||null;if(u.kind==="series"){base.reported_recurrence_strength=$("recurrenceStrength")?.value||null;base.exception_status=$("exceptionStatus")?.value||null;base.exception_frequency=base.exception_status==="exceptions_explicitly_denied"?"none_reported":base.exception_status==="exceptions_reported"?($("exceptionFrequency")?.value||"unknown"):null;base.frequency_evidence_basis=base.reported_recurrence_strength==="bounded_rate_or_count"?"bounded_rate_or_count_self_report":"generalized_self_report";base.minimum_reported_occurrences=null;base.bounded_rate_or_count_description=base.reported_recurrence_strength==="bounded_rate_or_count"?($("boundedDescription")?.value.trim()||null):null;base.recurrence_scope_description=null}return base}''',
    )

    html = _replace_function(
        html,
        "validate",
        r'''function validate(u,r){const e=[];const sourceIds=new Set(u.task.exact_source_segments.map(s=>s.segment_id));for(const arr of [r.supporting_source_segment_ids||[],r.counterevidence_source_segment_ids||[],r.influence_source_segment_ids||[]])for(const id of arr)if(!sourceIds.has(id))return["This saved response no longer matches this unit. Stop and report the technical problem."];if(!["observed","insufficient","not_applicable"].includes(r.state))e.push("Select at least one behavior, or choose Doesn't apply to this story / Not enough information.");if(r.state==="observed"){if(!r.coded_values.length)e.push("Select at least one behavior that the exact source clearly shows.");if(r.coded_values.length===1&&r.value_relation!=="single")e.push("The page could not save your one selected behavior correctly. Reload the file and try again.");if(r.coded_values.length>1&&!['ordered_sequence','unordered_multiple'].includes(r.value_relation))e.push("You selected more than one behavior. Say whether the story gives a clear order.");if(!r.supporting_source_segment_ids.length)e.push(u.task.exact_source_segments.length>1?"Choose the quote(s) you relied on for the selected behavior(s).":"The page could not attach the exact quote to your selection. Reload the file and try again.");const expectedNon=r.coded_values.some(v=>u.ext.non_action_values.includes(v));if(expectedNon&&(!r.non_action_gate||Object.values(r.non_action_gate).some(x=>x!=="established")))e.push("For the selected ‘did not act’ behavior, all four extra checks must be Yes. If any one is No or Can't tell, choose another behavior or choose Not enough information for the unit.");if(r.coded_values.includes(u.ext.other_specified_value)&&!r.other_specified_description)e.push("Describe the behavior that was not listed.");if(u.kind==="series"){if(!r.reported_recurrence_strength)e.push("Choose how often the narrator says this behavior recurs.");if(!r.exception_status)e.push("Choose whether the narrator reports exceptions or limits.");if(r.reported_recurrence_strength==="bounded_rate_or_count"&&!r.bounded_rate_or_count_description)e.push("Enter the count or rate that the narrator actually states.")}}return e}''',
    )

    if _embedded_fragment(html) != embedded_before:
        raise ValueError("direct-choice UI patch altered embedded private handoff bytes")
    outside = html.replace(_embedded_fragment(html), "")
    for obsolete in (
        "Enough information to code",
        "Can this unit be coded for the question above?",
        "This is not a fit scale",
    ):
        if obsolete in outside:
            raise ValueError(f"direct-choice UI still exposes meta-coding prompt: {obsolete}")
    for required in (
        "Which behavior or behaviors does the exact source clearly show?",
        "Doesn't apply to this story",
        "Not enough information",
        'base.state=vals.length?"observed":fallback',
    ):
        if required not in outside:
            raise ValueError(f"direct-choice UI is missing required human task: {required}")
    return html


def build_direct_choice_human_calibration_ui_v2(
    handoff_zip: str | Path,
    output_html: str | Path,
    *,
    overwrite: bool = False,
) -> dict[str, Any]:
    output = Path(output_html)
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")

    with tempfile.TemporaryDirectory(prefix="life-patterns-ui-v2-direct-choice-") as temporary:
        previous = Path(temporary) / "auditor.html"
        base_receipt = build_final_auditor_human_calibration_ui_v2(handoff_zip, previous)
        before = previous.read_text(encoding="utf-8")
        after = patch_html_for_direct_behavior_choice(before)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(after, encoding="utf-8", newline="\n")
    raw = output.read_bytes()
    receipt = dict(base_receipt)
    receipt.update(
        schema_version="life-patterns-human-calibration-ui-direct-choice-build-receipt-v2",
        output_html_sha256=hashlib.sha256(raw).hexdigest(),
        output_html_bytes=len(raw),
        human_primary_choice="behavior_values_directly",
        machine_state_derived_from_human_choice=True,
        generic_partial_state_added=False,
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
    receipt = build_direct_choice_human_calibration_ui_v2(
        args.handoff_zip,
        args.output_html,
        overwrite=args.overwrite,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
