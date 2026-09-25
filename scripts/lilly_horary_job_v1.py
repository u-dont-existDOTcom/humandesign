#!/usr/bin/env python3
"""Source-frozen Lilly Chapter LXXXII affirmative job classifier v1."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

POSITIVE_PERFECTIONS = frozenset(
    {"direct_perfection", "translation_of_light", "collection_of_light"}
)


def compose_v1_verdict(
    *, affirmative_clauses: dict[str, bool], perfection_state: str,
    indeterminate_positive_perfection: bool,
) -> str:
    if any(affirmative_clauses.values()):
        return "YES"
    if perfection_state != "composed" or indeterminate_positive_perfection:
        return "DEFER"
    return "NO"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _value(obj: Any) -> Any:
    return getattr(obj, "value", obj)


def score_case(case: dict[str, Any], *, engine: Any, kernel_sha256: str) -> dict[str, Any]:
    from moira.classical_perfection import (
        ClassicalBodyState,
        _current_relation,
        _reception_bases,
    )
    from moira.constants import Body, HouseSystem
    from moira.horary import (
        HoraryEvidenceState,
        HoraryHousePolicy,
        HoraryQuestionReceipt,
        HoraryQuestionTimeBasis,
        HoraryQuestionTimeReceipt,
        HorarySourceCalendar,
    )
    from moira.houses import house_of
    from moira.julian import jd_from_datetime, utc_to_ut1
    from moira.planets import planet_at

    dt = datetime.fromisoformat(case["utc"])
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
        terminal_topic_house=10,
    )
    profile = engine.horary_evidence_at(
        question,
        house_policy=HoraryHousePolicy(HouseSystem.REGIOMONTANUS),
        perfection_jd_end=jd_ut1 + 31.0,
    )

    traditional = (
        Body.SUN, Body.MOON, Body.MERCURY, Body.VENUS,
        Body.MARS, Body.JUPITER, Body.SATURN,
    )
    states: dict[str, ClassicalBodyState] = {}
    for body in traditional:
        p = planet_at(body, jd_ut1, reader=engine._reader)
        states[body] = ClassicalBodyState(
            body=body, longitude=p.longitude, speed=p.speed, sign=p.sign
        )

    sig = profile.significators
    l1 = sig.principal_querent.body
    l10 = sig.principal_quesited.body
    if l1 is None or l10 is None:
        clauses = {
            "PERFECTION": False,
            "RECEPTION": False,
            "L10_IN_1_FASTER": False,
            "L10_IN_1_BENEFIC_JOIN": False,
        }
        return {
            "case_id": case["case_id"], "prediction": "DEFER",
            "affirmative_clauses": clauses,
            "reason": "principal_significator_assignment_not_evaluable",
        }

    analysis = profile.perfection.analysis
    present = set()
    indeterminate = set()
    if analysis is not None:
        present = {_value(k) for k in analysis.present_kinds}
        indeterminate = {_value(k) for k in analysis.indeterminate_kinds}

    is_day = _value(profile.chart_sect.sect) == "day"
    reception_l1 = _reception_bases(l10, states[l1], is_day)
    reception_moon = _reception_bases(l10, states[Body.MOON], is_day)

    l10_house = house_of(states[l10].longitude, profile.house_geometry.house_cusps)
    l10_in_1 = l10_house == 1
    l10_faster = abs(states[l10].speed) > abs(states[l1].speed)

    benefic_join = False
    benefic_relations: dict[str, Any] = {}
    for benefic in (Body.JUPITER, Body.VENUS):
        if benefic == l10:
            benefic_relations[benefic] = {"same_body": True}
            continue
        rel = _current_relation(states[l10], states[benefic])
        benefic_relations[benefic] = {
            "aspect": rel[0], "distance_deg": rel[2],
            "motion": rel[3], "within_moiety": rel[4],
        }
        if rel[4]:
            benefic_join = True

    clauses = {
        "PERFECTION": bool(POSITIVE_PERFECTIONS.intersection(present)),
        "RECEPTION": bool(reception_l1 or reception_moon),
        "L10_IN_1_FASTER": bool(l10_in_1 and l10_faster),
        "L10_IN_1_BENEFIC_JOIN": bool(l10_in_1 and benefic_join),
    }
    verdict = compose_v1_verdict(
        affirmative_clauses=clauses,
        perfection_state=_value(profile.perfection.state),
        indeterminate_positive_perfection=bool(
            POSITIVE_PERFECTIONS.intersection(indeterminate)
        ),
    )
    return {
        "case_id": case["case_id"],
        "prediction": verdict,
        "outcome_exposed_before_prediction": bool(
            case.get("outcome_exposed_before_prediction", False)
        ),
        "affirmative_clauses": clauses,
        "l1": l1, "l10": l10,
        "l10_house": l10_house,
        "l10_speed": states[l10].speed,
        "l1_speed": states[l1].speed,
        "l10_receives_l1_by": list(reception_l1),
        "l10_receives_moon_by": list(reception_moon),
        "benefic_relations": benefic_relations,
        "perfection_state": _value(profile.perfection.state),
        "present_kinds": sorted(present),
        "indeterminate_kinds": sorted(indeterminate),
        "kernel_sha256": kernel_sha256,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--kernel", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    import moira
    cases = [json.loads(x) for x in args.inputs.read_text().splitlines() if x.strip()]
    kernel_sha = sha256_file(args.kernel)
    engine = moira.Moira(str(args.kernel))
    rows = [score_case(c, engine=engine, kernel_sha256=kernel_sha) for c in cases]
    envelope = {
        "schema": "lilly-horary-job-ch82-v1",
        "classification": "post-v0 development repair; source-frozen before v1 scoring",
        "freeze_sha256": sha256_file(args.freeze),
        "inputs_sha256": sha256_file(args.inputs),
        "kernel_sha256": kernel_sha,
        "moira_version": getattr(moira, "__version__", "unknown"),
        "predictions": rows,
    }
    args.output.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output_sha256": sha256_file(args.output),
        "yes": sum(x["prediction"] == "YES" for x in rows),
        "no": sum(x["prediction"] == "NO" for x in rows),
        "defer": sum(x["prediction"] == "DEFER" for x in rows),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
