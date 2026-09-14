#!/usr/bin/env python3
"""Build the minimal-burden human-facing Life Patterns v2 calibration UI.

The human sees only judgments that can change the planned calibration. Machine identifiers,
transport defaults, and auxiliary metadata remain in the export contract but are not presented as
human work.
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
        raise ValueError(f"final auditor UI patch could not find function {name}")
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
        raise ValueError("final auditor UI patch cannot locate embedded handoff payload")
    return html[start:end]


def patch_html_for_final_auditor(html: str) -> str:
    embedded_before = _embedded_fragment(html)
    html = html.replace(
        "</head>",
        (
            "<style>\n#advancedContext{display:none!important}.value c"
            "ode{display:none!important}.machineonly{display:none!imp"
            "ortant}\n.quotelabel{font-weight:700}.quotesnippet{displa"
            "y:block;color:#46554f;margin-top:2px;line-height:1.35}\n."
            "relationchoice{display:grid;gap:8px;margin-top:9px}.rela"
            "tionchoice label{display:flex;gap:8px;align-items:flex-s"
            "tart;padding:10px 11px;border:1px solid #d4ddd8;border-r"
            "adius:9px;background:#fff}\n.orderbox{margin-top:10px;pad"
            "ding:11px 12px;border:1px solid #d8e2dc;border-radius:9p"
            "x;background:#f8fbf9}.orderbox h4{margin:0 0 8px}\n.order"
            "editem{display:flex;align-items:center;justify-content:s"
            "pace-between;gap:12px;padding:8px 0;border-top:1px solid"
            " #e5ece8}.ordereditem:first-of-type{border-top:0}.ordere"
            "ditem .orderlabel{font-weight:650}.ordereditem button{mi"
            "n-width:34px}.humanerror{margin:7px 0}\n</style>\n</head>"
        ),
        1,
    )
    html = _replace_function(
        html,
        "renderSources",
        (
            "function renderSources(u,r){const segments=u.task.exact_"
            "source_segments||[];const support=new Set(r.supporting_s"
            'ource_segment_ids||[]);const observed=r.state==="observe'
            'd";const quoteName=i=>segments.length===1?"Exact quote":'
            "`Exact quote ${i+1}`;const quoteText=s=>s.exact_text||s."
            'exact_participant_text||"";const cards=segments.map((s,i'
            ')=>`<article class="source"><div class="sourceid">${esc('
            "quoteName(i))}</div><p>${esc(quoteText(s))}</p></article"
            '>`).join("");let provenance="";if(observed&&segments.len'
            'gth===1){const s=segments[0];provenance=`<input class="m'
            'achineonly" type="checkbox" data-source="support" value='
            '"${esc(s.segment_id)}" checked>`}else if(observed&&segme'
            'nts.length>1){provenance=`<div class="provenancebox"><h3'
            ">Which quote(s) did you use for this Yes answer?</h3><p "
            'class="hint">Choose only the quote(s) that actually show'
            ' the behavior you selected.</p><div class="provenancelis'
            't">${segments.map((s,i)=>`<label><input type="checkbox" '
            'data-source="support" value="${esc(s.segment_id)}" ${sup'
            'port.has(s.segment_id)?"checked":""}> <span><span class='
            '"quotelabel">${esc(quoteName(i))}</span><span class="quo'
            'tesnippet">${esc(quoteText(s))}</span></span></label>`).'
            'join("")}</div></div>`}$("sources").innerHTML=cards+prov'
            "enance}"
        ),
    )
    html = _replace_function(
        html,
        "seriesFields",
        (
            "function seriesFields(r){const status=r.exception_status"
            '||"";const strength=r.reported_recurrence_strength||"";c'
            'onst exceptionPart=status==="exceptions_reported"?select'
            'Field("exceptionFrequency","How often does the narrator '
            'say the exceptions happen?",["unknown","almost_never","s'
            'ometimes","often","context_dependent","rough_rate_or_cou'
            'nt"],r.exception_frequency||"unknown"):"";const countPar'
            't=strength==="bounded_rate_or_count"?`<div class="field"'
            '><label for="boundedDescription">What count or rate does'
            ' the narrator actually state?</label><textarea id="bound'
            'edDescription">${esc(r.bounded_rate_or_count_description'
            '||"")}</textarea><div class="hint">Use only what the exa'
            "ct source actually gives. Do not estimate.</div></div>`:"
            '"";return`<div class="section"><h3>How often does the na'
            'rrator say this behavior happens?</h3><p class="hint">Th'
            "is is about what the narrator reports, not an externally"
            ' verified frequency.</p>${selectField("recurrenceStrengt'
            'h","How often?",RECURRENCE_STRENGTH,strength)}${selectFi'
            'eld("exceptionStatus","Does the narrator report exceptio'
            'ns or limits?",EXCEPTION_STATUS,status)}${exceptionPart}'
            "${countPart}</div>`}"
        ),
    )
    html = _replace_function(
        html,
        "renderObserved",
        (
            'function renderObserved(u,r){const host=$("observedField'
            's");if(r.state!=="observed"){host.innerHTML=\'<div class='
            '"section"><p class="hint">Nothing else is required for t'
            "his answer.</p></div>';return}const subMap=new Map((u.re"
            "solved?.subcodes||[]).map(s=>[s.subcode_id,s]));const se"
            "lected=new Set(r.coded_values||[]);const values=u.obs.al"
            "lowed_values||[];const relation=r.value_relation||(selec"
            'ted.size===1?"single":"");let html=`<div class="section"'
            "><h3>Which behavior does the exact source show?</h3><div"
            ' class="values">${values.map(v=>{const s=subMap.get(v);c'
            "onst non=u.ext.non_action_values.includes(v);return`<lab"
            'el class="value"><input type="checkbox" data-value="${es'
            'c(v)}" ${selected.has(v)?"checked":""}><div><span class='
            '"wording">${esc(plainBehavior(s?.wording,v))}</span></di'
            "v>${non?'<span class=\"tag\">extra check required</span>':"
            '""}</label>`}).join("")}</div></div>`;if(selected.size>1'
            '){html+=`<div class="section"><h3>You selected more than'
            " one behavior. Does the story say they happened in a par"
            'ticular order?</h3><div class="relationchoice"><label><i'
            'nput type="radio" name="valueRelationHuman" value="order'
            'ed_sequence" ${relation==="ordered_sequence"?"checked":"'
            '"}> <span><b>Yes — the story gives an order</b><br><span'
            ' class="hint">I can put them in order.</span></span></la'
            'bel><label><input type="radio" name="valueRelationHuman"'
            ' value="unordered_multiple" ${relation==="unordered_mult'
            'iple"?"checked":""}> <span><b>No — the order is not esta'
            'blished</b><br><span class="hint">The source supports mo'
            "re than one behavior, but not their sequence.</span></sp"
            'an></label></div>${relation==="ordered_sequence"?\'<div c'
            'lass="orderbox"><h4>Put the selected behaviors in the or'
            'der they happened:</h4><div id="orderedValues"></div></d'
            'iv>\':""}</div>`}if(u.kind==="series")html+=seriesFields('
            "r);if(selected.has(u.ext.other_specified_value))html+=`<"
            'div class="section"><div class="field"><label for="osDes'
            'cription">Describe the behavior that is not listed above'
            '</label><textarea id="osDescription">${esc(r.other_speci'
            'fied_description||"")}</textarea></div></div>`;if([...se'
            "lected].some(v=>u.ext.non_action_values.includes(v)))htm"
            'l+=`<div class="section"><h3>Extra check for the “did no'
            't act” behavior you selected</h3><p class="hint">This op'
            "tion only counts when all four answers are Yes. If any a"
            "nswer is No or Can't tell, choose another behavior or Ca"
            'n\'t tell for the unit.</p><div class="gate">${["awarenes'
            's","opportunity","feasibility","established_non_action"]'
            '.map(k=>gateSelect(k,r.non_action_gate?.[k])).join("")}<'
            "/div></div>`;host.innerHTML=html;host.querySelectorAll('"
            '[data-value]\').forEach(x=>x.addEventListener("change",()'
            "=>renderObserved(u,readForm(u))));host.querySelectorAll("
            "'input[name=\"valueRelationHuman\"]').forEach(x=>x.addEven"
            'tListener("change",()=>{if(x.value==="ordered_sequence"&'
            "&!orderOverrides.has(u.key))orderOverrides.set(u.key,sel"
            'ectedValues());renderObserved(u,readForm(u))}));$("recur'
            'renceStrength")?.addEventListener("change",()=>renderObs'
            'erved(u,readForm(u)));$("exceptionStatus")?.addEventList'
            'ener("change",()=>renderObserved(u,readForm(u)));if(rela'
            'tion==="ordered_sequence")renderOrdered()}'
        ),
    )
    html = _replace_function(
        html,
        "renderOrdered",
        (
            'function renderOrdered(){const host=$("orderedValues");i'
            "f(!host)return;const u=units[current];const subMap=new M"
            "ap((u.resolved?.subcodes||[]).map(s=>[s.subcode_id,s]));"
            "let vals=[...(orderOverrides.get(u.key)||selectedValues("
            "))];const selected=new Set(selectedValues());vals=vals.f"
            "ilter(v=>selected.has(v));for(const v of selected)if(!va"
            "ls.includes(v))vals.push(v);orderOverrides.set(u.key,val"
            's);host.innerHTML=vals.map((v,i)=>`<div class="orderedit'
            'em"><span class="orderlabel">${i+1}. ${esc(plainBehavior'
            "(subMap.get(v)?.wording,v))}</span><span>${i?`<button ty"
            'pe="button" aria-label="Move up" data-move="up" data-v="'
            '${esc(v)}">↑</button>`:""}${i<vals.length-1?`<button typ'
            'e="button" aria-label="Move down" data-move="down" data-'
            'v="${esc(v)}">↓</button>`:""}</span></div>`).join("");ho'
            "st.querySelectorAll('[data-move]').forEach(b=>b.addEvent"
            'Listener("click",()=>moveValue(b.dataset.v,b.dataset.mov'
            "e)))}\nlet orderOverrides=new Map();function moveValue(v,"
            "dir){const u=units[current];const vals=[...(orderOverrid"
            "es.get(u.key)||selectedValues())];const i=vals.indexOf(v"
            '),j=dir==="up"?i-1:i+1;if(i<0||j<0||j>=vals.length)retur'
            "n;[vals[i],vals[j]]=[vals[j],vals[i]];orderOverrides.set"
            "(u.key,vals);renderOrdered()}"
        ),
    )
    html = _replace_function(
        html,
        "renderCommon",
        (
            'function renderCommon(u,r){$("missingFlags").innerHTML="'
            '";$("contextQualifiers").value="";$("lifePhase").value="'
            '";$("language").value="";$("note").value=""}'
        ),
    )
    html = _replace_function(
        html,
        "readForm",
        (
            "function readForm(u){const base=draftFromFormSeed(u);bas"
            'e.state=document.querySelector(\'input[name="state"]:chec'
            "ked')?.value||null;base.supporting_source_segment_ids=so"
            'urceSelections("support");base.counterevidence_source_se'
            "gment_ids=[];base.context_qualifiers=[];base.missingness"
            "_flags=[];base.life_phase_qualifier=null;base.annotation"
            '_note=null;if(u.kind==="episode"){base.language=null;bas'
            'e.influence_relation="none_reported";base.influence_sour'
            'ce_segment_ids=[]}if(base.state!=="observed")return base'
            ';let vals=selectedValues();const rel=vals.length===1?"si'
            'ngle":document.querySelector(\'input[name="valueRelationH'
            'uman"]:checked\')?.value||null;if(rel==="ordered_sequence'
            '"){const over=orderOverrides.get(u.key)||[];const set=ne'
            "w Set(vals);if(over.length===vals.length&&over.every(x=>"
            "set.has(x)))vals=[...over]}base.coded_values=vals;base.v"
            "alue_relation=rel;base.asserts_non_action=vals.some(v=>u"
            ".ext.non_action_values.includes(v));if(base.asserts_non_"
            "action){base.non_action_gate={};document.querySelectorAl"
            "l('[data-gate]').forEach(x=>base.non_action_gate[x.datas"
            "et.gate]=x.value||null)}if(vals.includes(u.ext.other_spe"
            'cified_value))base.other_specified_description=$("osDesc'
            'ription")?.value.trim()||null;if(u.kind==="series"){base'
            '.reported_recurrence_strength=$("recurrenceStrength")?.v'
            'alue||null;base.exception_status=$("exceptionStatus")?.v'
            "alue||null;base.exception_frequency=base.exception_statu"
            's==="exceptions_explicitly_denied"?"none_reported":base.'
            'exception_status==="exceptions_reported"?($("exceptionFr'
            'equency")?.value||"unknown"):null;base.frequency_evidenc'
            'e_basis=base.reported_recurrence_strength==="bounded_rat'
            'e_or_count"?"bounded_rate_or_count_self_report":"general'
            'ized_self_report";base.minimum_reported_occurrences=null'
            ";base.bounded_rate_or_count_description=base.reported_re"
            'currence_strength==="bounded_rate_or_count"?($("boundedD'
            'escription")?.value.trim()||null):null;base.recurrence_s'
            "cope_description=null}return base}"
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
            '.push("Choose Yes, No, or Can\'t tell.");if(r.state==="ob'
            'served"){if(!r.coded_values.length)e.push("Choose at lea'
            'st one behavior from the list.");if(r.coded_values.lengt'
            'h===1&&r.value_relation!=="single")e.push("The page coul'
            "d not save your one selected behavior correctly. Reload "
            'the file and try again.");if(r.coded_values.length>1&&!['
            "'ordered_sequence','unordered_multiple'].includes(r.valu"
            'e_relation))e.push("You selected more than one behavior.'
            ' Say whether the story gives a clear order.");if(!r.supp'
            "orting_source_segment_ids.length)e.push(u.task.exact_sou"
            'rce_segments.length>1?"Choose the quote(s) you relied on'
            ' for this Yes answer.":"The page could not attach the ex'
            "act quote to your Yes answer. Reload the file and try ag"
            'ain.");const expectedNon=r.coded_values.some(v=>u.ext.no'
            "n_action_values.includes(v));if(expectedNon&&(!r.non_act"
            'ion_gate||Object.values(r.non_action_gate).some(x=>x!=="'
            'established")))e.push("For the selected ‘did not act’ be'
            "havior, all four extra checks must be Yes. If any one is"
            " No or Can't tell, choose another behavior or Can't tell"
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
    html = _replace_function(
        html,
        "saveUnit",
        (
            "function saveUnit(move){const u=units[current],r=readFor"
            'm(u),errors=validate(u,r);if(errors.length){$("unitError'
            's").innerHTML=`<b>${errors.length===1?"One thing needs f'
            'ixing before this can be saved:":"A few things need fixi'
            'ng before this can be saved:"}</b><ul>${errors.map(x=>`<'
            'li class="humanerror">${esc(x)}</li>`).join("")}</ul>`;$'
            '("unitErrors").classList.remove("hidden");return false}r'
            'esponses.set(u.key,r);$("unitErrors").classList.add("hid'
            'den");$("saveState").textContent="Saved on this page. Do'
            'wnload progress if you want a durable backup.";updatePro'
            "gress();if(move&&current<units.length-1){current++;rende"
            "r()}else render();return true}"
        ),
    )
    if _embedded_fragment(html) != embedded_before:
        raise ValueError("final auditor UI patch altered embedded private handoff bytes")
    outside = html.replace(_embedded_fragment(html), "")
    for obsolete in (
        "Use this quote as evidence for the behavior I selected",
        "This quote qualifies or goes against my selected behavior",
        "If more than one behavior is selected, how do they relate?",
        "Observed requires a value relation",
    ):
        if obsolete in outside:
            raise ValueError(f"final auditor UI still exposes obsolete text: {obsolete}")
    return html


def build_final_auditor_ui_v2(
    handoff_zip: str | Path,
    output_html: str | Path,
    *,
    overwrite: bool = False,
) -> dict[str, Any]:
    output = Path(output_html)
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")
    with tempfile.TemporaryDirectory(prefix="life-patterns-final-auditor-") as temporary:
        previous = Path(temporary) / "previous.html"
        base_receipt = build_plain_provenance_standalone_human_calibration_ui_v2(
            handoff_zip,
            previous,
        )
        after = patch_html_for_final_auditor(previous.read_text(encoding="utf-8"))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(after, encoding="utf-8", newline="\n")
    raw = output.read_bytes()
    receipt = dict(base_receipt)
    receipt.update(
        schema_version="life-patterns-human-calibration-ui-final-auditor-build-receipt-v2",
        output_html_sha256=hashlib.sha256(raw).hexdigest(),
        output_html_bytes=len(raw),
        optional_auxiliary_fields_shown=False,
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
    receipt = build_final_auditor_ui_v2(
        args.handoff_zip,
        args.output_html,
        overwrite=args.overwrite,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
