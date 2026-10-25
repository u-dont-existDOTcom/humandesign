"""C34 standalone SYNTHETIC-ONLY freeze → outcomes → blinded-score rehearsal.

This is *not* a real participant intake, preregistration, locked external
timestamp or measured astrology effect. It never accepts real DOB/place or
marital histories. No changes to participant-session-v1 or production.

Source Ptolemy IV.5 male-text Moon bicorporeal *subclause only*.
An unindicated sign is a comparator, never a source prediction of one marriage.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import random
from typing import Any

SOURCE_NAME = "PTOLEMY_IV_5_MEN_MOON_BICORPOREAL_SUBCLAUSE_ONLY"
SOURCE_SHA256 = "4e9f8a27fa1c284ab9b9b6a24cdc0834c5e3bacc757c8435c921fdc42c2c45d4"
SOURCE_COMMIT = "ef8b143a9e30545118db72479a5cf3974f8b3c08"
B = 1999
PERM_SEED = 20261025
MOCK_SEED = "C34_SYNTHETIC_INDEPENDENT_OUTCOMES_NO_REAL_PERSON_20261025"
QUESTION = (
    "By your 50th birthday, how many distinct legally recognized marriages "
    "had you entered? 0 / 1 / 2 / 3 or more / Unsure / Prefer not to answer"
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf8")


def digest(value: Any) -> str:
    return sha256(canonical(value)).hexdigest()


def wrap(body: dict) -> dict:
    return {"body": body, "sha256": digest(body)}


def verify(packet: dict, *, expected_schema: str) -> dict:
    if not isinstance(packet, dict) or set(packet) != {"body", "sha256"}:
        raise ValueError("invalid frozen packet envelope")
    body = packet["body"]
    if not isinstance(body, dict) or body.get("schema") != expected_schema:
        raise ValueError("unexpected packet schema")
    if packet["sha256"] != digest(body):
        raise ValueError("SHA256 integrity check failed; packet changed")
    if body.get("synthetic_only") is not True:
        raise ValueError("real-person data is not supported by this rehearsal")
    return body


def file_read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf8"))


def new_file(path: Path, data: dict) -> None:
    """Exclusive creation; never silently replace the original freeze."""
    with path.open("x", encoding="utf8") as f:
        f.write(json.dumps(data, indent=2, sort_keys=True,
                           ensure_ascii=False) + "\n")


def freeze_from_c33(source_path: Path) -> dict:
    """Pure source-to-predictions mapping; NEVER reads outcome answers."""
    if sha256(source_path.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("C33 synthetic source has changed")
    source = file_read(source_path)
    if source.get("all_dates_are_SYNTHETIC_not_people") is not True:
        raise ValueError("source is not synthetic-only")
    if source.get("no_real_births_or_outcomes") is not True:
        raise ValueError("source contains human records or outcomes")
    if source.get("sampled_days") != 366 or len(source["rows"]) != 366:
        raise ValueError("unexpected source universe")
    prediction_rows = []
    dates = set()
    for index, row in enumerate(source["rows"], 1):
        day = row["utc_civil_date"]
        if day in dates or not day.startswith("2020-"):
            raise ValueError("duplicate/unexpected synthetic date")
        dates.add(day)
        cls = row["source_class"]
        if cls not in ("MANY_INDICATED_CONDITIONALLY",
                       "NO_INDICATION_CONDITIONALLY", "TIME_INDETERMINATE"):
            raise ValueError("unrecognized source-class value")
        positive = (True if cls == "MANY_INDICATED_CONDITIONALLY" else
                    False if cls == "NO_INDICATION_CONDITIONALLY" else None)
        prediction_rows.append({
            "synthetic_id": f"MOCK-C34-{index:03d}",
            "synthetic_utc_calendar_day": day,
            "birth_month_stratum": day[:7],
            "indicated_source_subclause": positive,
            "source_class": cls,
            "possible_source_signs": row["possible_signs"],
        })
    if len(dates) != 366:
        raise ValueError("incomplete frozen synthetic calendar")
    return wrap({
        "schema": "C34_SYNTHETIC_PREANSWER_PREDICTIONS_V1",
        "synthetic_only": True,
        "real_person_births_used": False,
        "real_human_outcomes_available": False,
        "rehearsal_not_a_trusted_timestamped_preregistration": True,
        "source_commit": SOURCE_COMMIT,
        "source_case": SOURCE_NAME,
        "source_snapshot_sha256": SOURCE_SHA256,
        "research_only_sign_method_speed_bound_unverified": True,
        "ancient_positive_clause": "multiple marriages when bicorporeal",
        "nonpositive_sign_is_not_a_source_prediction_of_one_marriage": True,
        "modern_endpoint_analyst_choice_not_in_Greek":
            "two_or_more_lawful_marriages_by_attained_age_50",
        "unadministered_concealed_question": QUESTION,
        "analysis_contract": {
            "primary": "one-sided within-birth-month stratified risk difference",
            "analyst_inference_not_literal_Ptolemy":
                "compare positive source sign vs all other stable signs",
            "null": "exchangeability of binary outcomes within fixed month strata",
            "unknowns": "remove from scored denominator, retain count",
            "no_source_sign_from_birth_time_indeterminate": True,
            "permutation_count": B,
            "permutation_seed": PERM_SEED,
            "minimum_exposure_and_control_per_stratum": 1,
            "no_unblinded_revision_after_any_outcome": True,
        },
        "cohort_size": len(prediction_rows),
        "participant_set_sha256": digest([x["synthetic_id"] for x in prediction_rows]),
        "frozen_cohort": prediction_rows,
    })


def verify_source_locked_freeze(freeze_packet: dict) -> dict:
    """A recomputed but modified chart-label packet must ALSO fail.

    SHA256 equality with one's *own rehashed edits* is not trustworthy
    preregistration. In this synthetic dry run compare against the
    original exact C33 source bytes and code-derived permitted rows.
    A real test must additionally commit externally before outcomes.
    """
    body = verify(
        freeze_packet,
        expected_schema="C34_SYNTHETIC_PREANSWER_PREDICTIONS_V1",
    )
    canonical_source = Path(__file__).with_name(
        "HELLENISTIC_C33_UTC_2020_SYNTHETIC_CLASSIFIER_V1.json"
    )
    expected = freeze_from_c33(canonical_source)
    if freeze_packet != expected:
        raise ValueError("validly rehashed but source-altered prediction freeze")
    return body


def mock_outcome_from_synthetic_id(synthetic_id: str, month: str) -> str:
    """Mock outcome independent of any astrological chart/exposure field."""
    if not synthetic_id.startswith("MOCK-C34-"):
        raise ValueError("must be a synthetic ID")
    if not month.startswith("2020-"):
        raise ValueError("synthetic 2020 month required")
    numeric_month = int(month[-2:])
    if not 1 <= numeric_month <= 12:
        raise ValueError("synthetic month out of range")
    prob = 0.15 + 0.002 * (numeric_month - 1)
    raw = sha256(f"{MOCK_SEED}:{synthetic_id}:outcome".encode()).digest()
    u = int.from_bytes(raw[:8], "big") / 2**64
    return "two_plus" if u < prob else "less_than_two"


def deterministic_mock_outcomes(freeze_packet: dict) -> dict:
    """Derive mock answers from id + seed ONLY, independent of source sign.

    This is intentionally *not* real marriage-history evidence. Responses
    are mock labels, and no participant consent or record is implied.
    """
    freeze = verify_source_locked_freeze(freeze_packet)
    answers = []
    for row in freeze["frozen_cohort"]:
        key = row["synthetic_id"]
        answers.append({
            "synthetic_id": key,
            "simulated_binary_marriage_outcome": mock_outcome_from_synthetic_id(
                key, row["birth_month_stratum"]),
            "this_is_not_a_real_marriage_history": True,
        })
    return wrap({
        "schema": "C34_SYNTHETIC_MOCK_OUTCOMES_V1",
        "synthetic_only": True,
        "generated_after_frozen_prediction_packet": True,
        "freeze_sha256": freeze_packet["sha256"],
        "source_of_mock_data": "ID_ONLY_DETERMINISTIC_NULL_BY_BIRTH_MONTH",
        "outcomes_independent_of_source_sign_by_construction": True,
        "observations": answers,
    })


def _statistic(rows: list[dict], y: dict[str, int]) -> tuple[float, list[dict]]:
    """Declared weighted month-stratified risk difference, no cherry picking."""
    strata: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        if r["indicated_source_subclause"] is not None and r["synthetic_id"] in y:
            strata[r["birth_month_stratum"]].append(r)
    usable = []
    for month, cohort in sorted(strata.items()):
        e = [y[r["synthetic_id"]] for r in cohort
             if r["indicated_source_subclause"] is True]
        c = [y[r["synthetic_id"]] for r in cohort
             if r["indicated_source_subclause"] is False]
        if e and c:
            usable.append((month, cohort, e, c))
    denom = sum(len(cohort) for _, cohort, _, _ in usable)
    if not denom:
        raise ValueError("no matched strata with both source conditions")
    stat = sum(len(cohort)/denom * (sum(e)/len(e) - sum(c)/len(c))
               for _, cohort, e, c in usable)
    details = [{
        "stratum": month, "scored": len(cohort),
        "source_positive_count": len(e), "source_comparator_count": len(c),
        "source_positive_mock_risk": sum(e)/len(e),
        "source_comparator_mock_risk": sum(c)/len(c),
    } for month, cohort, e, c in usable]
    return stat, details


def score_mock(frozen: dict, outcomes: dict) -> dict:
    """Read the sealed freeze BEFORE any mock outcomes, require same IDs."""
    f = verify_source_locked_freeze(frozen)
    o = verify(outcomes, expected_schema="C34_SYNTHETIC_MOCK_OUTCOMES_V1")
    if o.get("freeze_sha256") != frozen["sha256"]:
        raise ValueError("response file belongs to another frozen cohort")
    rows = f["frozen_cohort"]
    ids = [r["synthetic_id"] for r in rows]
    responses = o["observations"]
    supplied = [r["synthetic_id"] for r in responses]
    if len(set(supplied)) != len(supplied) or set(supplied) != set(ids):
        raise ValueError("duplicate or missing mock outcome IDs")
    y: dict[str, int] = {}
    for r in responses:
        if r.get("this_is_not_a_real_marriage_history") is not True:
            raise ValueError("only marked synthetic answers are admitted")
        value = r.get("simulated_binary_marriage_outcome")
        if value == "two_plus":
            y[r["synthetic_id"]] = 1
        elif value == "less_than_two":
            y[r["synthetic_id"]] = 0
        elif value != "unknown":
            raise ValueError("invalid mocked answer type")
    observed, strata_details = _statistic(rows, y)
    # Permutation within each birth-month. Fixed source positives and
    # controls; shuffle only mocked outcomes, preserving counts by month.
    eligible = [r for r in rows
                if r["indicated_source_subclause"] is not None
                and r["synthetic_id"] in y]
    bymonth: dict[str, list[str]] = defaultdict(list)
    for r in eligible:
        bymonth[r["birth_month_stratum"]].append(r["synthetic_id"])
    rng = random.Random(int(f["analysis_contract"]["permutation_seed"]))
    count_ge = 0
    for _ in range(int(f["analysis_contract"]["permutation_count"])):
        perm = dict(y)
        for ids_in_month in bymonth.values():
            labels = [y[k] for k in ids_in_month]
            rng.shuffle(labels)
            perm.update(zip(ids_in_month, labels))
        stat, _ = _statistic(rows, perm)
        if stat >= observed - 1e-12:
            count_ge += 1
    pvalue = (count_ge + 1) / (int(f["analysis_contract"]["permutation_count"]) + 1)
    abstain = sum(r["indicated_source_subclause"] is None for r in rows)
    unknowns = len(ids) - len(y)
    return wrap({
        "schema":"C34_SYNTHETIC_STATISTICAL_REHEARSAL_V1",
        "synthetic_only": True,
        "not_a_human_astrology_validation": True,
        "actual_human_predictions": 0,
        "any_source_effect_measured_in_real_population": False,
        "freeze_sha256": frozen["sha256"],
        "mock_response_sha256": outcomes["sha256"],
        "source_pre_answer_freeze_preceded_mock_outcome_generation": True,
        "no_trusted_external_preregistration_timestamp": True,
        "cohort_size": len(rows),
        "birth_sign_condition_indeterminate": abstain,
        "response_unknowns": unknowns,
        "scored_conditional_known": len(y) - sum(
            r["indicated_source_subclause"] is None and r["synthetic_id"] in y
            for r in rows),
        "month_stratified_risk_difference_mock": observed,
        "month_stratified_one_sided_permutation_p_MOCK_ONLY": pvalue,
        "predeclared_permutations": int(f["analysis_contract"]["permutation_count"]),
        "matched_month_strata": strata_details,
        "no_modifications_to_production_or_participant_session": True,
    })


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="action", required=True)
    a = sub.add_parser("freeze")
    a.add_argument("--source", type=Path, required=True)
    a.add_argument("--out", type=Path, required=True)
    a = sub.add_parser("mock-outcomes")
    a.add_argument("--freeze", type=Path, required=True)
    a.add_argument("--out", type=Path, required=True)
    a = sub.add_parser("score")
    a.add_argument("--freeze", type=Path, required=True)
    a.add_argument("--outcomes", type=Path, required=True)
    a.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.action == "freeze":
        packet = freeze_from_c33(args.source)
    elif args.action == "mock-outcomes":
        packet = deterministic_mock_outcomes(file_read(args.freeze))
    else:
        packet = score_mock(file_read(args.freeze), file_read(args.outcomes))
    new_file(args.out, packet)
    print("C34_SYNTHETIC_ONLY", args.action,
          "sha256", packet["sha256"], "file", args.out)


if __name__ == "__main__":
    main()
