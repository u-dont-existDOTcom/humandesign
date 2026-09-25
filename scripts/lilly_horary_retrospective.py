#!/usr/bin/env python3
"""Frozen exploratory Lilly-horary retrospective batch scorer."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

POSITIVE_KINDS = frozenset(
    {"direct_perfection", "translation_of_light", "collection_of_light"}
)


def frozen_verdict(
    *,
    perfection_state: str,
    present_kinds: set[str] | frozenset[str],
    indeterminate_kinds: set[str] | frozenset[str],
) -> str:
    """Apply the pre-outcome v0 judgement law from METHOD-FREEZE.md."""
    if perfection_state != "composed":
        return "DEFER"
    if POSITIVE_KINDS.intersection(present_kinds):
        return "YES"
    if POSITIVE_KINDS.intersection(indeterminate_kinds):
        return "DEFER"
    return "NO"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _value(obj: Any) -> Any:
    return getattr(obj, "value", obj)


def score_case(case: dict[str, Any], *, engine: Any, kernel_sha256: str) -> dict[str, Any]:
    from moira.constants import HouseSystem
    from moira.horary import (
        HoraryEvidenceState,
        HoraryHousePolicy,
        HoraryQuestionReceipt,
        HoraryQuestionTimeBasis,
        HoraryQuestionTimeReceipt,
        HorarySourceCalendar,
    )
    from moira.julian import jd_from_datetime, utc_to_ut1

    dt = datetime.fromisoformat(case["utc"])
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError(f"{case['case_id']}: utc must be timezone-aware")
    jd_ut1 = utc_to_ut1(jd_from_datetime(dt))
    question = HoraryQuestionReceipt(
        question_id=case["case_id"],
        latitude_deg=float(case["lat"]),
        longitude_deg=float(case["lon"]),
        time=HoraryQuestionTimeReceipt(
            state=HoraryEvidenceState.EVALUATED,
            stated_basis=HoraryQuestionTimeBasis.QUESTION_PROPOSED_AND_FIGURE_ERECTED,
            stated_basis_source="archived opening-post question time",
            source_calendar=HorarySourceCalendar.GREGORIAN,
            source_instant_label=dt.isoformat(),
            normalized_instant=dt,
            normalized_jd_ut1=jd_ut1,
            conversion_policy_id="moira_6.2.0_jd_from_datetime_utc_to_ut1",
            reason=None,
        ),
        perspective_path=(),
        terminal_topic_house=int(case["topic_house"]),
    )
    profile = engine.horary_evidence_at(
        question,
        house_policy=HoraryHousePolicy(HouseSystem.REGIOMONTANUS),
        perfection_jd_end=jd_ut1 + 31.0,
    )
    perf_state = _value(profile.perfection.state)
    analysis = profile.perfection.analysis
    present = set()
    indeterminate = set()
    witnesses: list[dict[str, Any]] = []
    if analysis is not None:
        present = {_value(kind) for kind in analysis.present_kinds}
        indeterminate = {_value(kind) for kind in analysis.indeterminate_kinds}
        for witness in analysis.witnesses:
            witnesses.append(
                {
                    "kind": _value(witness.kind),
                    "state": _value(witness.state),
                    "actors": list(witness.actors),
                    "event_ids": list(witness.event_ids),
                    "reception_bases": list(witness.reception_bases),
                }
            )
    verdict = frozen_verdict(
        perfection_state=perf_state,
        present_kinds=present,
        indeterminate_kinds=indeterminate,
    )
    sig = profile.significators
    considerations = [
        {
            "state": _value(item.state),
            "rule": getattr(item, "rule_id", getattr(item, "name", None)),
        }
        for item in getattr(profile, "considerations", ())
    ]
    return {
        "case_id": case["case_id"],
        "prediction": verdict,
        "outcome_exposed_before_prediction": bool(
            case.get("outcome_exposed_before_prediction", False)
        ),
        "question_utc": case["utc"],
        "topic_house": case["topic_house"],
        "principal_querent": sig.principal_querent.body,
        "principal_quesited": sig.principal_quesited.body,
        "same_body_principals": sig.same_body_principals,
        "perfection_state": perf_state,
        "perfection_reason": profile.perfection.reason,
        "present_kinds": sorted(present),
        "indeterminate_kinds": sorted(indeterminate),
        "witnesses": witnesses,
        "hour_agreement": _value(profile.hour_agreement.state),
        "considerations": considerations,
        "kernel_sha256": kernel_sha256,
        "moira_profile": "lilly_1647_perfection_v1",
        "house_system": "Regiomontanus",
        "perfection_span_days": 31.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--method-freeze", required=True, type=Path)
    parser.add_argument("--kernel", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    import moira

    inputs_sha = sha256_file(args.inputs)
    method_sha = sha256_file(args.method_freeze)
    kernel_sha = sha256_file(args.kernel)
    engine = moira.Moira(str(args.kernel))

    cases = [json.loads(line) for line in args.inputs.read_text().splitlines() if line.strip()]
    rows = [
        score_case(case, engine=engine, kernel_sha256=kernel_sha)
        for case in cases
    ]
    envelope = {
        "schema": "lilly-horary-retrospective-predictions-v0",
        "classification": "frozen-before-outcome-reveal exploratory retrospective pilot",
        "moira_version": getattr(moira, "__version__", "unknown"),
        "inputs_sha256": inputs_sha,
        "method_freeze_sha256": method_sha,
        "kernel_sha256": kernel_sha,
        "predictions": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(envelope, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "output": str(args.output),
        "output_sha256": sha256_file(args.output),
        "count": len(rows),
        "yes": sum(r["prediction"] == "YES" for r in rows),
        "no": sum(r["prediction"] == "NO" for r in rows),
        "defer": sum(r["prediction"] == "DEFER" for r in rows),
        "strict_unexposed_count": sum(
            not r["outcome_exposed_before_prediction"] for r in rows
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
