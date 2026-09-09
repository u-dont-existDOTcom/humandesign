#!/usr/bin/env python3
"""Patch the final auditor UI so primary states are not presented as a fit scale.

This is presentation-only. It preserves the embedded private handoff, selected units, response
contract and target-model blind. The human sees the actual decision represented by the frozen
observed / insufficient / not_applicable states.
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
        raise ValueError(f"auditor state-label patch could not find function {name}")
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
        raise ValueError("auditor state-label patch cannot locate embedded handoff payload")
    return html[start:end]


def patch_html_for_evidence_state_clarity(html: str) -> str:
    embedded_before = _embedded_fragment(html)

    html = _replace_function(
        html,
        "renderStates",
        r'''function renderStates(u,r){const opts=[["observed","Enough information to code","The exact source gives enough information to choose at least one behavior below."],["not_applicable","Doesn't apply","The situation required by this question is clearly not present."],["insufficient","Not enough information","Some pieces may fit, but the exact source is not clear or complete enough to choose a behavior reliably."]];$("stateGrid").innerHTML=`<h3 style="grid-column:1/-1;margin:0">Can this unit be coded for the question above?</h3><p class="hint" style="grid-column:1/-1;margin:0">This is not a fit scale. If it partly fits but you cannot confidently choose a behavior from the exact source, choose <b>Not enough information</b>.</p>`+opts.map(([v,l,d])=>`<label class="state"><b><input type="radio" name="state" value="${v}" ${r.state===v?"checked":""}>${l}</b><span>${d}</span></label>`).join("");updateStateSemantics(u,r.state);document.querySelectorAll('input[name="state"]').forEach(el=>el.addEventListener("change",()=>{const next={...readForm(u),state:el.value};updateStateSemantics(u,el.value);renderSources(u,next);renderObserved(u,next)}))}''',
    )
    html = _replace_function(
        html,
        "updateStateSemantics",
        r'''function updateStateSemantics(u,state){$("stateSemantics").textContent=state==="observed"?"Choose the behavior or behaviors that the exact source clearly supports.":state==="not_applicable"?"The required situation is absent, so no behavioral value is needed.":state==="insufficient"?"Use this when only part of the needed information is present, or the source is too unclear to choose a behavior reliably.":""}''',
    )

    old = 'if(!["observed","insufficient","not_applicable"].includes(r.state))e.push("Choose Yes, No, or Can\'t tell.");'
    new = 'if(!["observed","insufficient","not_applicable"].includes(r.state))e.push("Choose Enough information to code, Doesn\'t apply, or Not enough information.");'
    if old not in html:
        raise ValueError("auditor state-label patch could not find primary-state validation copy")
    html = html.replace(old, new, 1)

    if _embedded_fragment(html) != embedded_before:
        raise ValueError("auditor state-label patch altered embedded private handoff bytes")
    outside = html.replace(_embedded_fragment(html), "")
    for required in (
        "Enough information to code",
        "Doesn't apply",
        "Not enough information",
        "This is not a fit scale",
        "If it partly fits",
    ):
        if required not in outside:
            raise ValueError(f"auditor state-label patch is missing required human copy: {required}")
    return html


def build_state_clarified_auditor_ui_v2(
    handoff_zip: str | Path,
    output_html: str | Path,
    *,
    overwrite: bool = False,
) -> dict[str, Any]:
    output = Path(output_html)
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")
    with tempfile.TemporaryDirectory(prefix="life-patterns-ui-v2-state-labels-") as temporary:
        base = Path(temporary) / "auditor.html"
        base_receipt = build_final_auditor_human_calibration_ui_v2(handoff_zip, base)
        before = base.read_text(encoding="utf-8")
        after = patch_html_for_evidence_state_clarity(before)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(after, encoding="utf-8", newline="\n")
    raw = output.read_bytes()
    receipt = dict(base_receipt)
    receipt.update(
        schema_version="life-patterns-human-calibration-ui-auditor-state-labels-v2",
        output_html_sha256=hashlib.sha256(raw).hexdigest(),
        output_html_bytes=len(raw),
        primary_states_presented_as_fit_scale=False,
        partial_fit_maps_to_insufficient_when_not_codeable=True,
        response_contract_changed=False,
        embedded_private_handoff_unchanged=True,
        selected_calibration_units_changed=False,
        target_model_information_used=False,
        automated_judgment_used=False,
        network_requests_required=False,
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-zip", type=Path, required=True)
    parser.add_argument("--output-html", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    receipt = build_state_clarified_auditor_ui_v2(
        args.handoff_zip,
        args.output_html,
        overwrite=args.overwrite,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
