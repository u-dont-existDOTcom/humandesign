#!/usr/bin/env python3
"""Build the current human-facing Life Patterns v2 calibration UI.

This presentation-only layer is applied after the verified plain/provenance UI. It keeps all
measurement-bearing data and response contracts unchanged while removing two remaining pieces of
machine-oriented UI friction:

1. internal source-segment IDs are hidden from the human and replaced by readable quote labels/text;
2. the value-relation control is shown only when the human has actually selected multiple
   behavioral values. A single selected value is encoded as ``single`` automatically.

No target-model information, automated judgment, resampling, or network behavior is introduced.
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
        raise ValueError(f"final UI patch could not find function {name}")
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
        raise ValueError("final UI patch cannot locate embedded handoff payload")
    return html[start:end]


def patch_html_for_final_human_ui(html: str) -> str:
    """Hide machine identifiers and make relation UI conditional, failing closed on drift."""

    embedded_before = _embedded_fragment(html)

    html = html.replace(
        "</head>",
        """<style>
.quotelabel{font-weight:700}
.quotesnippet{display:block;color:#46554f;margin-top:2px}
.value code{display:none!important}
</style>
</head>""",
        1,
    )

    html = _replace_function(
        html,
        "renderSources",
        r'''function renderSources(u,r){const segments=u.task.exact_source_segments||[];const support=new Set(r.supporting_source_segment_ids||[]),counter=new Set(r.counterevidence_source_segment_ids||[]);const observed=r.state==="observed";const quoteName=i=>segments.length===1?"Exact quote":`Exact quote ${i+1}`;const quoteText=s=>s.exact_text||s.exact_participant_text||"";const cards=segments.map((s,i)=>`<article class="source"><div class="sourceid">${esc(quoteName(i))}</div><p>${esc(quoteText(s))}</p></article>`).join("");let provenance="";if(observed&&segments.length===1){const s=segments[0];provenance=`<div class="provenancenote"><input type="checkbox" hidden data-source="support" value="${esc(s.segment_id)}" checked>Because there is only one exact quote in this unit, it will be saved automatically as the source for your Yes answer. No extra citation decision is needed.</div>`}else if(observed&&segments.length>1){provenance=`<div class="provenancebox"><h3>Which quote(s) show the behavior you selected?</h3><p class="hint">This is only source bookkeeping. Select the exact quote(s) you actually relied on for your Yes answer.</p><div class="provenancelist">${segments.map((s,i)=>`<label><input type="checkbox" data-source="support" value="${esc(s.segment_id)}" ${support.has(s.segment_id)?"checked":""}> <span><span class="quotelabel">${esc(quoteName(i))}</span><span class="quotesnippet">${esc(quoteText(s))}</span></span></label>`).join("")}</div></div>`}if(observed&&segments.length){provenance+=`<details class="details provenancebox"><summary>Optional: does any quote contain an exception or conflicting detail?</summary><p class="hint">Use this only when some exact text genuinely limits, qualifies, or conflicts with the behavior you selected. Most units need nothing here.</p><div class="provenancelist">${segments.map((s,i)=>`<label><input type="checkbox" data-source="counter" value="${esc(s.segment_id)}" ${counter.has(s.segment_id)?"checked":""}> <span><span class="quotelabel">${esc(quoteName(i))}</span><span class="quotesnippet">${esc(quoteText(s))}</span></span></label>`).join("")}</div></details>`}$("sources").innerHTML=cards+provenance}''',
    )
    html = _replace_function(
        html,
        "episodeInfluence",
        r'''function episodeInfluence(u,r){const rel=r.influence_relation||"none_reported";const inf=new Set(r.influence_source_segment_ids||[]);const segments=u.task.exact_source_segments||[];const quoteName=i=>segments.length===1?"Exact quote":`Exact quote ${i+1}`;const quoteText=s=>s.exact_text||s.exact_participant_text||"";return`<details class="section details"><summary>Optional: does the narrator explicitly say something influenced the behavior you selected?</summary><p class="hint">This is only about the behavior you coded above. Do not record a causal statement about some other action in the story.</p>${selectField("influenceRelation","Relation to the selected behavior",INFLUENCE,rel,false)}${rel!=="none_reported"?`<div class="field"><span class="labelish">Which exact quote states or establishes that relation?</span><div class="provenancelist">${segments.map((s,i)=>`<label><input type="checkbox" data-source="influence" value="${esc(s.segment_id)}" ${inf.has(s.segment_id)?"checked":""}> <span><span class="quotelabel">${esc(quoteName(i))}</span><span class="quotesnippet">${esc(quoteText(s))}</span></span></label>`).join("")}</div></div>`:""}</details>`}''',
    )
    html = _replace_function(
        html,
        "renderObserved",
        r'''function renderObserved(u,r){const host=$("observedFields");if(r.state!=="observed"){host.innerHTML='<div class="section"><p class="hint">No behavioral subcode is needed for this answer.</p></div>';return}const subMap=new Map((u.resolved?.subcodes||[]).map(s=>[s.subcode_id,s]));const selected=new Set(r.coded_values||[]);const values=u.obs.allowed_values||[];const relation=selected.size===1?"single":(r.value_relation||"");const relationHidden=selected.size<=1?" hidden":"";let html=`<div class="section"><h3>Which behavior does the exact source show?</h3><div class="values">${values.map(v=>{const s=subMap.get(v);const non=u.ext.non_action_values.includes(v);return`<label class="value"><input type="checkbox" data-value="${esc(v)}" ${selected.has(v)?"checked":""}><div><div><span class="wording">${esc(plainBehavior(s?.wording,v))}</span> <code>${esc(v)}</code></div></div>${non?'<span class="tag">requires extra evidence check</span>':""}</label>`}).join("")}</div><div class="relationrow${relationHidden}" id="relationRow"><span class="labelish">You selected more than one behavior. Did they happen in a known order?</span><select id="valueRelation"><option value="">Choose…</option><option value="single" hidden ${relation==="single"?"selected":""}>One behavior</option><option value="ordered_sequence" ${relation==="ordered_sequence"?"selected":""}>Yes — they happened in this order</option><option value="unordered_multiple" ${relation==="unordered_multiple"?"selected":""}>No / the order is not established</option></select></div><div class="ordered" id="orderedValues"></div></div>`;if(u.kind==="series")html+=seriesFields(r);else html+=episodeInfluence(u,r);html+=`<div class="section hidden" id="osField"><div class="field"><label for="osDescription">Describe the behavior that is not listed above</label><textarea id="osDescription">${esc(r.other_specified_description||"")}</textarea></div></div><div class="section hidden" id="nonActionField"><h3>Extra check required for a “did not act” code</h3><p class="hint">Only use a no-action value when all four questions below can be answered Yes from the supplied evidence. Otherwise choose a different behavior or Can't tell.</p><div class="gate">${["awareness","opportunity","feasibility","established_non_action"].map(k=>gateSelect(k,r.non_action_gate?.[k])).join("")}</div></div>`;host.innerHTML=html;host.querySelectorAll('[data-value]').forEach(x=>x.addEventListener("change",()=>{syncSpecial(u);const vals=selectedValues();const vr=$("valueRelation"),row=$("relationRow");if(vr&&row){if(vals.length===1){vr.value="single";row.classList.add("hidden")}else if(vals.length>1){if(vr.value==="single")vr.value="";row.classList.remove("hidden")}else{vr.value="";row.classList.add("hidden")}}renderOrdered()}));$("valueRelation")?.addEventListener("change",()=>renderOrdered());$("influenceRelation")?.addEventListener("change",()=>renderObserved(u,readForm(u)));if(r.value_relation==="ordered_sequence")orderOverrides.set(u.key,[...(r.coded_values||[])]);else orderOverrides.delete(u.key);syncSpecial(u);const initialVals=selectedValues(),vr=$("valueRelation"),row=$("relationRow");if(vr&&row){if(initialVals.length===1){vr.value="single";row.classList.add("hidden")}else if(initialVals.length>1){if(vr.value==="single")vr.value="";row.classList.remove("hidden")}else row.classList.add("hidden")}}''',
    )

    if _embedded_fragment(html) != embedded_before:
        raise ValueError("final UI patch altered embedded private handoff bytes")
    if "If more than one behavior is selected, how do they relate?" in html:
        raise ValueError("final UI patch left the always-visible relation prompt")
    if "EP-002-SEG-01" in html.split("const EMBEDDED = ", 1)[0]:
        raise ValueError("final UI patch exposes a source-segment identifier in static human UI")
    if 'option value="single" hidden' not in html:
        raise ValueError("final UI patch must preserve automatic single-value serialization")
    if 'id="relationRow"' not in html or 'vals.length>1' not in html:
        raise ValueError("final UI patch is missing conditional multi-value relation behavior")
    return html


def build_final_standalone_human_calibration_ui_v2(
    handoff_zip: str | Path,
    output_html: str | Path,
    *,
    overwrite: bool = False,
) -> dict[str, Any]:
    output = Path(output_html)
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")

    with tempfile.TemporaryDirectory(prefix="life-patterns-ui-v2-final-") as temporary:
        prior = Path(temporary) / "plain-provenance.html"
        base_receipt = build_plain_provenance_standalone_human_calibration_ui_v2(
            handoff_zip,
            prior,
        )
        before = prior.read_text(encoding="utf-8")
        after = patch_html_for_final_human_ui(before)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(after, encoding="utf-8", newline="\n")
    raw = output.read_bytes()
    receipt = dict(base_receipt)
    receipt.update(
        schema_version="life-patterns-human-calibration-ui-final-build-receipt-v2",
        output_html_sha256=hashlib.sha256(raw).hexdigest(),
        output_html_bytes=len(raw),
        internal_source_ids_hidden_from_human=True,
        single_value_relation_auto_encoded=True,
        multi_value_relation_control_conditional=True,
        embedded_private_handoff_unchanged=True,
        selected_calibration_units_changed=False,
        response_contract_changed=False,
        measurement_semantics_changed=False,
        target_model_information_used=False,
        automated_judgment_used=False,
        network_requests_required=False,
        supersedes_prior_human_ui_for_collection=True,
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-zip", type=Path, required=True)
    parser.add_argument("--output-html", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    receipt = build_final_standalone_human_calibration_ui_v2(
        args.handoff_zip,
        args.output_html,
        overwrite=args.overwrite,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
