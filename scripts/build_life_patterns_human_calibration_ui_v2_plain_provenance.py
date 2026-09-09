#!/usr/bin/env python3
"""Build the plain Life Patterns v2 UI with nonredundant source-provenance controls.

This is a presentation-only transform applied after the verified plain-language UI is built.
It preserves the exact private handoff, selected units, response schemas, measurement semantics,
blinding, and offline boundary. The only change is how the existing supporting/counterevidence
source-segment fields are presented to a human auditor.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from build_life_patterns_human_calibration_ui_v2_plain import (
    build_plain_standalone_human_calibration_ui_v2,
)


def _replace_function(text: str, name: str, replacement: str) -> str:
    start = text.find(f"function {name}(")
    if start < 0:
        raise ValueError(f"provenance UI patch could not find function {name}")
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
        raise ValueError("provenance UI patch cannot locate embedded handoff payload")
    return html[start:end]


def patch_html_for_nonredundant_provenance(html: str) -> str:
    """Make provenance bookkeeping conditional without changing exported semantics."""

    embedded_before = _embedded_fragment(html)

    html = html.replace(
        "</head>",
        """<style>
.provenancebox{margin:12px 0 0;padding:12px 14px;border:1px solid #d8e2dc;border-radius:10px;background:#f8fbf9}
.provenancebox h3{margin:0 0 5px;font-size:15px}.provenancebox p{margin:0 0 8px}
.provenancenote{margin:10px 0 0;padding:9px 11px;border-radius:9px;background:#f3f7f5;color:#51605a;font-size:12px}
.provenancelist{display:grid;gap:7px}.provenancelist label{display:flex;gap:8px;align-items:flex-start}
</style>
</head>""",
        1,
    )

    html = _replace_function(
        html,
        "renderSources",
        '''function renderSources(u,r){const segments=u.task.exact_source_segments||[];const support=new Set(r.supporting_source_segment_ids||[]),counter=new Set(r.counterevidence_source_segment_ids||[]);const observed=r.state==="observed";const cards=segments.map(s=>`<article class="source"><div class="sourceid">${esc(s.segment_id)}</div><p>${esc(s.exact_text||s.exact_participant_text||"")}</p></article>`).join("");let provenance="";if(observed&&segments.length===1){const s=segments[0];provenance=`<div class="provenancenote"><input type="checkbox" hidden data-source="support" value="${esc(s.segment_id)}" checked>Because there is only one exact quote in this unit, it will be saved automatically as the source for your Yes answer. No extra citation decision is needed.</div>`}else if(observed&&segments.length>1){provenance=`<div class="provenancebox"><h3>Which quote(s) show the behavior you selected?</h3><p class="hint">This is only source bookkeeping. Select the exact quote(s) you actually relied on for your Yes answer.</p><div class="provenancelist">${segments.map(s=>`<label><input type="checkbox" data-source="support" value="${esc(s.segment_id)}" ${support.has(s.segment_id)?"checked":""}> <span><b>${esc(s.segment_id)}</b></span></label>`).join("")}</div></div>`}if(observed&&segments.length){provenance+=`<details class="details provenancebox"><summary>Optional: does any quote contain an exception or conflicting detail?</summary><p class="hint">Use this only when some exact text genuinely limits, qualifies, or conflicts with the behavior you selected. Most units need nothing here.</p><div class="provenancelist">${segments.map(s=>`<label><input type="checkbox" data-source="counter" value="${esc(s.segment_id)}" ${counter.has(s.segment_id)?"checked":""}> <span>${esc(s.segment_id)}</span></label>`).join("")}</div></details>`}$("sources").innerHTML=cards+provenance}''',
    )
    html = _replace_function(
        html,
        "updateStateSemantics",
        '''function updateStateSemantics(u,state){$("stateSemantics").textContent=state==="observed"?"If Yes, choose the behavior below. With one exact quote, source provenance is saved automatically; with several, choose only the quote(s) you relied on.":state==="not_applicable"?"No behavioral value or source citation is needed.":state==="insufficient"?"No behavioral value or source citation is needed; use an uncertainty flag or note only if it helps explain why.":""}''',
    )

    if _embedded_fragment(html) != embedded_before:
        raise ValueError("provenance UI patch altered embedded private handoff bytes")
    for obsolete in (
        "Use this quote as evidence for the behavior I selected",
        "This quote qualifies or goes against my selected behavior",
    ):
        if obsolete in html:
            raise ValueError(f"provenance UI patch left redundant source control: {obsolete}")
    if "Which quote(s) show the behavior you selected?" not in html:
        raise ValueError("provenance UI patch is missing multi-source provenance selector")
    if "No extra citation decision is needed" not in html:
        raise ValueError("provenance UI patch is missing single-source auto-binding explanation")
    return html


def build_plain_provenance_standalone_human_calibration_ui_v2(
    handoff_zip: str | Path,
    output_html: str | Path,
    *,
    overwrite: bool = False,
) -> dict[str, Any]:
    output = Path(output_html)
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")

    with tempfile.TemporaryDirectory(prefix="life-patterns-ui-v2-provenance-") as temporary:
        plain = Path(temporary) / "plain.html"
        base_receipt = build_plain_standalone_human_calibration_ui_v2(
            handoff_zip,
            plain,
        )
        before = plain.read_text(encoding="utf-8")
        after = patch_html_for_nonredundant_provenance(before)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(after, encoding="utf-8", newline="\n")
    raw = output.read_bytes()
    receipt = dict(base_receipt)
    receipt.update(
        schema_version="life-patterns-human-calibration-ui-plain-provenance-build-receipt-v2",
        output_html_sha256=hashlib.sha256(raw).hexdigest(),
        output_html_bytes=len(raw),
        single_source_support_auto_bound=True,
        multi_source_support_requires_explicit_selection=True,
        counterevidence_control_optional_and_secondary=True,
        embedded_private_handoff_unchanged=True,
        selected_calibration_units_changed=False,
        response_contract_changed=False,
        measurement_semantics_changed=False,
        target_model_information_used=False,
        automated_judgment_used=False,
        network_requests_required=False,
        supersedes_prior_plain_ui_for_human_collection=True,
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-zip", type=Path, required=True)
    parser.add_argument("--output-html", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    receipt = build_plain_provenance_standalone_human_calibration_ui_v2(
        args.handoff_zip,
        args.output_html,
        overwrite=args.overwrite,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
