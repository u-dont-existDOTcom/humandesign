#!/usr/bin/env python3
"""Verify source-anchored synthetic scoring artifacts and write final receipt.

This deliberately cannot certify an actual real-person astrology study,
calibrated questionnaire, properly matched decoys or real birth-chart engine.
"""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
OUTPUT = B / "PROTOTYPE_VERIFICATION_RECEIPT_20261020.json"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path):
    return sha256(path.read_bytes()).hexdigest()


def verify():
    mp = B / "SOURCE_TO_BEHAVIOR_CANDIDATES_V1.json"
    seal = B / "SYNTHETIC_PRE_RESPONSE_SEAL_V1.json"
    charts = B / "SYNTHETIC_CHART_TOKENS_V1.json"
    crosswalk = B / "INSTRUMENT_CROSSWALK_DRAFT_V1.json"
    m = read(mp)
    packet = read(seal)
    instrument = read(crosswalk)
    archive = read(B / "PORTABLE_ARCHIVE_RECEIPT_20261020.json")
    gates = read(ROOT / "tasks/astro-blind-readiness-20261020/READINESS_GATES_V1.json")
    if (
        len(m["candidates"]) != 4
        or len({x["source_note_id"] for x in m["candidates"]}) != 4
        or len(instrument["crosswalk"]) != 4
        or instrument["validated_multi_item_battery_selected"] is not False
        or instrument["real_human_scored_data_collected"] != 0
        or instrument["licensed_instrument_text_copied"] is not False
    ):
        raise ValueError("Candidate source/psychometric design not accurately marked draft")
    ids = {x["candidate_id"] for x in m["candidates"]}
    if {x["candidate_id"] for x in instrument["crosswalk"]} != ids:
        raise ValueError("Psychometric source-to-instrument map incomplete")
    if packet["sealed_payload"]["source_mapping_SHA256"] != digest(mp) or packet["sealed_payload"][
        "mock_chart_fixture_SHA256"
    ] != digest(charts):
        raise ValueError("Sealed synthetic source and chart fixtures no longer match")
    if (
        archive["independent_cold_extracted_toy_source_tests_green"] != 20
        or not archive["zip_CRC_verified"]
        or not archive["all_member_exact_SHA_and_size_verified"]
    ):
        raise ValueError("Portable cold source/scoring smoke tests not verified")
    archive_path = Path(archive["owner_local_archive_path"])
    if not archive_path.is_file() or digest(archive_path) != archive["zip_sha256"]:
        raise ValueError("Portable source archive bytes/SHA changed")
    results = {}
    requirements = {
        "POSITIVE": ("aligned_positive_control", 0.75, 1.0),
        "NULL": ("constant_null_control", 0.0, 0.5),
        "OPPOSITE": ("deliberately_opposite_control", -0.25, 1 / 3),
    }
    for label, (scenario, delta, percentile) in requirements.items():
        path = B / f"SYNTHETIC_RESULT_{label}_CONTROL_V1.json"
        result = read(path)
        if (
            result["scenario"] != scenario
            or result["sealed_payload_sha256"] != packet["sealed_payload_sha256"]
            or abs(result["mean_diagonal_minus_no_chart_row_mean"] - delta) > 1e-12
            or abs(result["HD_existing_rank_metrics_reused"]["mean_percentile"] - percentile)
            > 1e-12
            or result["human_predictive_validations"] != 0
            or result["source_model_candidate_is_frozen_for_humans"] is not False
            or result["ordinal_support_is_calibrated_probability"] is not False
            or result["nonastrological_external_baseline_tested"] is not False
        ):
            raise ValueError("Synthetic outcome/control mismatch or falsely labeled human result")
        results[label] = {
            "SHA256": digest(path),
            "diagonal_advantage_toy_only": delta,
            "mean_true_chart_percentile_toy_only": result["HD_existing_rank_metrics_reused"][
                "mean_percentile"
            ],
            "seeded_permutation_p_is_not_human_evidence": result[
                "HD_existing_seeded_label_permutation_reused"
            ]["p_value"],
        }
    if not (
        len(gates["candidate_pilot_gates"]) == 10
        and all(
            x["blocking"] and x["status"] in ("unresolved", "owner_gate")
            for x in gates["candidate_pilot_gates"]
        )
        and gates["pilot_eligibility"]["candidate_pilot_ready"] is False
    ):
        raise ValueError("Human readiness gates cannot have changed because of toy scores")
    if (
        sum(
            (
                gates["source_provenance"]["chinese_bazi_source_annotations"],
                gates["source_provenance"]["chinese_ziwei_source_annotations"],
                gates["source_provenance"]["western_lilly_source_annotations_in_other_branch"],
                gates["source_provenance"]["western_ptolemy_source_annotations_in_other_branch"],
            )
        )
        != 15098
    ):
        raise ValueError("Source annotation counts mistaken for participant outcomes")
    manifest = {
        "schema": "HUMANDESIGN_ASTROLOGY_FOUR_ANCHOR_SYNTHETIC_ONLY_CHECKPOINT_V1",
        "status": "SOURCE_AND_SYNTHETIC_ENGINEERING_PASSED_REAL_HUMAN_RESEARCH_OPEN",
        "original_source_excerpt_candidates": 4,
        "source_note_ids": sorted(x["source_note_id"] for x in m["candidates"]),
        "original_verified_source_map_sha256": digest(mp),
        "synthetic_chart_tokens_sha256": digest(charts),
        "synthetic_seal_sha256": digest(seal),
        "synthetic_seal_inner_payload_sha256": packet["sealed_payload_sha256"],
        "instrument_prior_art_crosswalk_sha256": digest(crosswalk),
        "portable_archive_sha256": archive["zip_sha256"],
        "portable_archive_member_count": archive["member_count"],
        "independent_cold_source_and_synthetic_tests_green": 20,
        "toy_scenarios": results,
        "real_human_readiness_gates_unmet": 10,
        "preregistration_completed": False,
        "mock_chart_is_an_authentic_birth_derived_ziwei_chart": False,
        "questionnaire_human_psychometric_validation_completed": False,
        "nonastrological_external_baseline_complete": False,
        "all_input_chart_time_and_conditional_source_rules_frozen": False,
        "real_human_participants_in_public_artifact": 0,
        "empirical_human_predictive_validations": 0,
        "runtime_astrological_rule_promotions": 0,
        "next_safe_work": (
            "Independently birth-calculate one limited source chart subset and "
            "verify original traditional time rules, then finalize validated "
            "question instruments and proper controls before consented "
            "untouched humans."
        ),
    }
    OUTPUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    m = verify()
    print(
        json.dumps(
            {
                "status": m["status"],
                "source_anchored_behaviors": m["original_source_excerpt_candidates"],
                "cold_source_and_synthetic_tests_green": m[
                    "independent_cold_source_and_synthetic_tests_green"
                ],
                "readiness_gates_unmet": m["real_human_readiness_gates_unmet"],
                "empirical_human_predictions": 0,
            },
            indent=2,
        )
    )
