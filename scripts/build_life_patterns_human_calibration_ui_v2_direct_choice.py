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
    build_final_auditor_ui_v2,
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
        (
            "<style>\n.fallbackchoices{display:grid;grid-template-colu"
            "mns:repeat(2,minmax(0,1fr));gap:10px;margin-top:14px}\n.f"
            "allbackchoice{display:flex;gap:8px;align-items:flex-star"
            "t;padding:11px 12px;border:1px solid #d4ddd8;border-radi"
            "us:9px;background:#fafcfb}\n.fallbackchoice b{display:blo"
            "ck;margin-bottom:3px}\n@media(max-width:700px){.fallbackc"
            "hoices{grid-template-columns:1fr}}\n</style>\n</head>"
        ),
        1,
    )

    html = _replace_function(
        html,
        "renderStates",
        (
            "function renderStates(u,r){const subMap=new Map((u.resol"
            "ved?.subcodes||[]).map(s=>[s.subcode_id,s]));const selec"
            "ted=new Set(r.coded_values||[]);const values=u.obs.allow"
            'ed_values||[];const fallback=r.state==="insufficient"?"i'
            'nsufficient":r.state==="not_applicable"?"not_applicable"'
            ':null;$("stateGrid").innerHTML=`<div style="grid-column:'
            '1/-1"><h3 style="margin:0 0 5px">Which behavior or behav'
            'iors does the exact source clearly show?</h3><p class="h'
            'int" style="margin:0 0 10px">Select every behavior that '
            "is clearly supported. If you cannot select one, use one "
            'of the two choices underneath.</p><div class="values">${'
            "values.map(v=>{const s=subMap.get(v);const non=u.ext.non"
            '_action_values.includes(v);return`<label class="value"><'
            'input type="checkbox" data-value="${esc(v)}" ${selected.'
            'has(v)?"checked":""}><div><span class="wording">${esc(pl'
            "ainBehavior(s?.wording,v))}</span></div>${non?'<span cla"
            'ss="tag">extra check required</span>\':""}</label>`}).joi'
            'n("")}</div><div class="fallbackchoices"><label class="f'
            'allbackchoice"><input type="radio" name="stateFallback" '
            'value="not_applicable" ${fallback==="not_applicable"?"ch'
            'ecked":""}><span><b>Doesn\'t apply to this story</b><span'
            ' class="hint">The situation required by the question is '
            'clearly absent.</span></span></label><label class="fallb'
            'ackchoice"><input type="radio" name="stateFallback" valu'
            'e="insufficient" ${fallback==="insufficient"?"checked":"'
            '"}><span><b>Not enough information</b><span class="hint"'
            ">Some pieces may fit, but the exact source is too incomp"
            "lete or unclear to choose a behavior reliably.</span></s"
            "pan></label></div></div>`;updateStateSemantics(u,r.state"
            ");$(\"stateGrid\").querySelectorAll('[data-value]').forEac"
            'h(x=>x.addEventListener("change",()=>{if(selectedValues('
            ").length)document.querySelectorAll('input[name=\"stateFal"
            "lback\"]').forEach(el=>el.checked=false);const next=readF"
            "orm(u);renderSources(u,next);renderObserved(u,next);upda"
            'teStateSemantics(u,next.state)}));$("stateGrid").querySe'
            "lectorAll('input[name=\"stateFallback\"]').forEach(x=>x.ad"
            'dEventListener("change",()=>{document.querySelectorAll(\''
            "[data-value]').forEach(el=>el.checked=false);orderOverri"
            "des.delete(u.key);const next=readForm(u);renderSources(u"
            ",next);renderObserved(u,next);updateStateSemantics(u,nex"
            "t.state)}))}"
        ),
    )

    html = _replace_function(
        html,
        "updateStateSemantics",
        (
            'function updateStateSemantics(u,state){$("stateSemantics'
            '").textContent=state==="observed"?"The behavior choices '
            'you selected will be coded for this unit.":state==="not_'
            'applicable"?"No behavior is coded because the required s'
            'ituation is absent.":state==="insufficient"?"No behavior'
            " is coded because the exact source does not support a re"
            'liable choice.":""}'
        ),
    )

    html = _replace_function(
        html,
        "renderObserved",
        (
            'function renderObserved(u,r){const host=$("observedField'
            's");const selected=new Set(r.coded_values||selectedValue'
            's());if(!selected.size){host.innerHTML="";return}const r'
            'elation=r.value_relation||(selected.size===1?"single":""'
            ');let html="";if(selected.size>1){html+=`<div class="sec'
            'tion"><h3>You selected more than one behavior. Does the '
            "story say they happened in a particular order?</h3><div "
            'class="relationchoice"><label><input type="radio" name="'
            'valueRelationHuman" value="ordered_sequence" ${relation='
            '=="ordered_sequence"?"checked":""}> <span><b>Yes — the s'
            'tory gives an order</b><br><span class="hint">I can put '
            'them in order.</span></span></label><label><input type="'
            'radio" name="valueRelationHuman" value="unordered_multip'
            'le" ${relation==="unordered_multiple"?"checked":""}> <sp'
            "an><b>No — the order is not established</b><br><span cla"
            'ss="hint">The source supports more than one behavior, bu'
            "t not their sequence.</span></span></label></div>${relat"
            'ion==="ordered_sequence"?\'<div class="orderbox"><h4>Put '
            "the selected behaviors in the order they happened:</h4><"
            'div id="orderedValues"></div></div>\':""}</div>`}if(u.kin'
            'd==="series")html+=seriesFields(r);if(selected.has(u.ext'
            '.other_specified_value))html+=`<div class="section"><div'
            ' class="field"><label for="osDescription">Describe the b'
            'ehavior that is not listed above</label><textarea id="os'
            'Description">${esc(r.other_specified_description||"")}</'
            "textarea></div></div>`;if([...selected].some(v=>u.ext.no"
            'n_action_values.includes(v)))html+=`<div class="section"'
            "><h3>Extra check for the “did not act” behavior you sele"
            'cted</h3><p class="hint">This option only counts when al'
            "l four answers are Yes. If any answer is No or Can't tel"
            "l, choose another behavior or choose Not enough informat"
            'ion for the unit.</p><div class="gate">${["awareness","o'
            'pportunity","feasibility","established_non_action"].map('
            'k=>gateSelect(k,r.non_action_gate?.[k])).join("")}</div>'
            "</div>`;host.innerHTML=html;host.querySelectorAll('input"
            '[name="valueRelationHuman"]\').forEach(x=>x.addEventListe'
            'ner("change",()=>{if(x.value==="ordered_sequence"&&!orde'
            "rOverrides.has(u.key))orderOverrides.set(u.key,selectedV"
            'alues());renderObserved(u,readForm(u))}));$("recurrenceS'
            'trength")?.addEventListener("change",()=>renderObserved('
            'u,readForm(u)));$("exceptionStatus")?.addEventListener("'
            'change",()=>renderObserved(u,readForm(u)));if(relation=='
            '="ordered_sequence")renderOrdered()}'
        ),
    )

    html = _replace_function(
        html,
        "readForm",
        (
            "function readForm(u){const base=draftFromFormSeed(u);let"
            " vals=selectedValues();const fallback=document.querySele"
            "ctor('input[name=\"stateFallback\"]:checked')?.value||null"
            ';base.state=vals.length?"observed":fallback;base.support'
            'ing_source_segment_ids=sourceSelections("support");base.'
            "counterevidence_source_segment_ids=[];base.context_quali"
            "fiers=[];base.missingness_flags=[];base.life_phase_quali"
            'fier=null;base.annotation_note=null;if(u.kind==="episode'
            '"){base.language=null;base.influence_relation="none_repo'
            'rted";base.influence_source_segment_ids=[]}if(base.state'
            '!=="observed")return base;const rel=vals.length===1?"sin'
            'gle":document.querySelector(\'input[name="valueRelationHu'
            'man"]:checked\')?.value||null;if(rel==="ordered_sequence"'
            "){const over=orderOverrides.get(u.key)||[];const set=new"
            " Set(vals);if(over.length===vals.length&&over.every(x=>s"
            "et.has(x)))vals=[...over]}base.coded_values=vals;base.va"
            "lue_relation=rel;base.asserts_non_action=vals.some(v=>u."
            "ext.non_action_values.includes(v));if(base.asserts_non_a"
            "ction){base.non_action_gate={};document.querySelectorAll"
            "('[data-gate]').forEach(x=>base.non_action_gate[x.datase"
            "t.gate]=x.value||null)}if(vals.includes(u.ext.other_spec"
            'ified_value))base.other_specified_description=$("osDescr'
            'iption")?.value.trim()||null;if(u.kind==="series"){base.'
            'reported_recurrence_strength=$("recurrenceStrength")?.va'
            'lue||null;base.exception_status=$("exceptionStatus")?.va'
            "lue||null;base.exception_frequency=base.exception_status"
            '==="exceptions_explicitly_denied"?"none_reported":base.e'
            'xception_status==="exceptions_reported"?($("exceptionFre'
            'quency")?.value||"unknown"):null;base.frequency_evidence'
            '_basis=base.reported_recurrence_strength==="bounded_rate'
            '_or_count"?"bounded_rate_or_count_self_report":"generali'
            'zed_self_report";base.minimum_reported_occurrences=null;'
            "base.bounded_rate_or_count_description=base.reported_rec"
            'urrence_strength==="bounded_rate_or_count"?($("boundedDe'
            'scription")?.value.trim()||null):null;base.recurrence_sc'
            "ope_description=null}return base}"
        ),
    )

    html = _replace_function(
        html,
        "validate",
        (
            "function validate(u,r){const e=[];const sourceIds=new Se"
            "t(u.task.exact_source_segments.map(s=>s.segment_id));for"
            "(const arr of [r.supporting_source_segment_ids||[],r.cou"
            "nterevidence_source_segment_ids||[],r.influence_source_s"
            "egment_ids||[]])for(const id of arr)if(!sourceIds.has(id"
            '))return["This saved response no longer matches this uni'
            't. Stop and report the technical problem."];if(!["observ'
            'ed","insufficient","not_applicable"].includes(r.state))e'
            ".push(\"Select at least one behavior, or choose Doesn't a"
            'pply to this story / Not enough information.");if(r.stat'
            'e==="observed"){if(!r.coded_values.length)e.push("Select'
            " at least one behavior that the exact source clearly sho"
            'ws.");if(r.coded_values.length===1&&r.value_relation!=="'
            'single")e.push("The page could not save your one selecte'
            'd behavior correctly. Reload the file and try again.");i'
            "f(r.coded_values.length>1&&!['ordered_sequence','unorder"
            "ed_multiple'].includes(r.value_relation))e.push(\"You sel"
            "ected more than one behavior. Say whether the story give"
            's a clear order.");if(!r.supporting_source_segment_ids.l'
            'ength)e.push(u.task.exact_source_segments.length>1?"Choo'
            "se the quote(s) you relied on for the selected behavior("
            's).":"The page could not attach the exact quote to your '
            'selection. Reload the file and try again.");const expect'
            "edNon=r.coded_values.some(v=>u.ext.non_action_values.inc"
            "ludes(v));if(expectedNon&&(!r.non_action_gate||Object.va"
            'lues(r.non_action_gate).some(x=>x!=="established")))e.pu'
            'sh("For the selected ‘did not act’ behavior, all four ex'
            "tra checks must be Yes. If any one is No or Can't tell, "
            "choose another behavior or choose Not enough information"
            ' for the unit.");if(r.coded_values.includes(u.ext.other_'
            "specified_value)&&!r.other_specified_description)e.push("
            '"Describe the behavior that was not listed.");if(u.kind='
            '=="series"){if(!r.reported_recurrence_strength)e.push("C'
            'hoose how often the narrator says this behavior recurs."'
            ');if(!r.exception_status)e.push("Choose whether the narr'
            'ator reports exceptions or limits.");if(r.reported_recur'
            'rence_strength==="bounded_rate_or_count"&&!r.bounded_rat'
            'e_or_count_description)e.push("Enter the count or rate t'
            'hat the narrator actually states.")}}return e}'
        ),
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
        base_receipt = build_final_auditor_ui_v2(handoff_zip, previous)
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
