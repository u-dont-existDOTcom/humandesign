#!/usr/bin/env python3
"""Final owner-review build surface for the Life Patterns V5 human calibration UI.

This narrow presentation layer exists because V5 distinguishes an affirmatively absent
prerequisite from insufficient evidence. It replaces the inherited V2 No/Can't-tell labels with
the controlling V5 wording while preserving the exact V5 measurement/export layer and embedded
private handoff bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from build_life_patterns_human_calibration_ui_v2_auditor_final import (
    _embedded_fragment,
    _replace_function,
)
from build_life_patterns_human_calibration_ui_v5 import build_human_calibration_ui_v5


def patch_html_for_v5_final_fallbacks(html: str) -> str:
    embedded_before = _embedded_fragment(html)
    html = _replace_function(
        html,
        "renderStates",
        r'''function renderStates(u,r){const opts=[["observed","Yes — clearly shown","The exact source clearly shows at least one substantive behavior or affirmative component below."],["not_applicable","Doesn't apply to this story","The required situation is affirmatively absent. Do not reinterpret the story to make it fit."],["insufficient","Not enough information","The situation may apply, but the exact source is not sufficient to support a substantive value reliably."]];$("stateGrid").innerHTML=`<h3 style="grid-column:1/-1;margin:0">Does the exact source answer the question above?</h3>`+opts.map(([v,l,d])=>`<label class="state"><b><input type="radio" name="state" value="${v}" ${r.state===v?"checked":""}>${l}</b><span>${d}</span></label>`).join("");updateStateSemantics(u,r.state);document.querySelectorAll('input[name="state"]').forEach(el=>el.addEventListener("change",()=>{const next={...readForm(u),state:el.value};updateStateSemantics(u,el.value);renderSources(u,next);renderObserved(u,next)}))}''',
    )
    html = _replace_function(
        html,
        "updateStateSemantics",
        r'''function updateStateSemantics(u,state){$("stateSemantics").textContent=state==="observed"?"If Yes, select the substantive fact(s) below. Machine graph bookkeeping is automatic.":state==="not_applicable"?"Use this only when the required situation is affirmatively absent from the story; non-mention is not enough.":state==="insufficient"?"Use this when the situation may apply but the exact source does not support a substantive fact reliably.":""}''',
    )
    html = html.replace(
        "Choose No when the prerequisite is absent; choose Can't tell when the source is too unclear.",
        "Choose Doesn't apply to this story when the prerequisite is affirmatively absent; choose Not enough information when the exact source is insufficient.",
    )
    if _embedded_fragment(html) != embedded_before:
        raise ValueError("V5 final fallback patch altered embedded private handoff bytes")
    outside = html.replace(_embedded_fragment(html), "")
    for required in (
        "Doesn't apply to this story",
        "Not enough information",
        "non-mention is not enough",
        "Final V5 response export",
    ):
        if required not in outside:
            raise ValueError(f"V5 final UI missing required fallback wording: {required}")
    for obsolete in (
        "No — does not fit",
        ">Can't tell<",
        "Choose No when the prerequisite is absent",
    ):
        if obsolete in outside:
            raise ValueError(f"V5 final UI retains obsolete fallback wording: {obsolete}")
    return html


def build_final_human_calibration_ui_v5(
    handoff_zip: str | Path,
    output_html: str | Path,
    *,
    overwrite: bool = False,
) -> dict[str, Any]:
    output = Path(output_html)
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")
    with tempfile.TemporaryDirectory(prefix="life-patterns-ui-v5-final-") as temporary:
        previous = Path(temporary) / "v5.html"
        base_receipt = build_human_calibration_ui_v5(handoff_zip, previous)
        after = patch_html_for_v5_final_fallbacks(previous.read_text(encoding="utf-8"))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(after, encoding="utf-8", newline="\n")
    raw = output.read_bytes()
    receipt = dict(base_receipt)
    receipt.update(
        schema_version="life-patterns-human-calibration-ui-final-build-receipt-v5",
        output_html_sha256=hashlib.sha256(raw).hexdigest(),
        output_html_bytes=len(raw),
        not_applicable_label="Doesn't apply to this story",
        insufficient_label="Not enough information",
        nonmention_never_maps_to_not_applicable=True,
        embedded_private_handoff_unchanged=True,
        owner_usability_review_required_before_collection=True,
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-zip", type=Path, required=True)
    parser.add_argument("--output-html", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    receipt = build_final_human_calibration_ui_v5(
        args.handoff_zip,
        args.output_html,
        overwrite=args.overwrite,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
