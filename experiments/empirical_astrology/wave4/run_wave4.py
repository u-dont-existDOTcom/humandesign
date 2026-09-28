#!/usr/bin/env python3
"""Run the authorized Wave 4 development-only mechanical evaluation.

The input manifest deliberately selects no human outcome data.  This runner
therefore emits explicit unavailable empirical comparisons plus deterministic
engineering fixtures.  It never discovers or opens owner-known outcome paths.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

from hdmatch.empirical_astrology import (
    NUISANCE_COLUMN_NAMES,
    BirthRecord,
    LiteratureModelV1,
    build_pair_features,
    deterministic_pair_id,
    deterministic_random_feature,
    require_deterministic_numerical_runtime,
    require_exact_diagnostic_family,
    score_ipip50,
    verify_required_git_ancestor,
)
from hdmatch.empirical_astrology.analysis import (
    AnalysisRow,
    fit_gap_bound_sensitivities,
    fit_primary_association,
    leave_one_network_out,
    restricted_wild_cluster_bootstrap,
)
from hdmatch.empirical_astrology.outcome import SCORING_KEY, ipip_pair_distance

ROOT = Path(__file__).resolve().parents[3]
INPUT_MANIFEST = Path("experiments/empirical_astrology/wave4/input_manifest.json")
RESULTS_PATH = Path("data/empirical_astrology/master_v2/wave4_results.jsonl")
FIXTURE_PATH = Path("experiments/empirical_astrology/wave4/engineering_fixture_summary.json")
SCHEMA = "empirical-astrology-wave4-result-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def unavailable_row(
    result_id: str,
    comparison: str,
    reason: str,
    *,
    model_version: str,
    input_hash: str,
    software_commit: str,
    status: str = "NOT_EVALUATED",
    planned_tests: int | None = None,
    launch_blocked: bool = False,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "schema_version": SCHEMA,
        "result_id": result_id,
        "evaluation_class": "EMPIRICAL_DEVELOPMENT",
        "comparison": comparison,
        "status": status,
        "status_reason": reason,
        "model_version": model_version,
        "dataset_ids": [],
        "n_people": 0,
        "n_pairs": 0,
        "n_networks": 0,
        "effect_estimate": None,
        "standard_error": None,
        "confidence_interval": None,
        "p_value": None,
        "multiplicity_family": None,
        "reused_dataset": False,
        "owner_outcomes_accessed": False,
        "untouched_prospective_outcomes_accessed": False,
        "empirical_validation_claim": False,
        "input_manifest_sha256": input_hash,
        "software_commit": software_commit,
    }
    if planned_tests is not None:
        row["planned_tests"] = planned_tests
        row["completed_tests"] = 0
    if launch_blocked:
        row["prospective_launch_blocked"] = True
    return row


def engineering_row(
    result_id: str,
    check: str,
    metrics: dict[str, Any],
    *,
    model_version: str,
    input_hash: str,
    software_commit: str,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA,
        "result_id": result_id,
        "evaluation_class": "ENGINEERING_FIXTURE",
        "comparison": check,
        "status": "PASS",
        "status_reason": "Deterministic software/protocol check passed; not human evidence.",
        "model_version": model_version,
        "dataset_ids": ["SYNTHETIC_ENGINEERING_FIXTURE_ONLY"],
        "n_people": None,
        "n_pairs": None,
        "n_networks": None,
        "effect_estimate": None,
        "standard_error": None,
        "confidence_interval": None,
        "p_value": None,
        "multiplicity_family": None,
        "reused_dataset": False,
        "owner_outcomes_accessed": False,
        "untouched_prospective_outcomes_accessed": False,
        "empirical_validation_claim": False,
        "engineering_metrics": metrics,
        "input_manifest_sha256": input_hash,
        "software_commit": software_commit,
    }


def make_birth_record(
    participant: str,
    timestamp: datetime,
    local_minutes: float,
    component: str,
) -> BirthRecord:
    return BirthRecord(
        participant_id=participant,
        hospital_id="H1",
        network_id="N1",
        local_birth_date=date(2026, 1, 2),
        birth_utc_timestamp=timestamp,
        birth_local_clock_minutes=local_minutes,
        birth_time_uncertainty_minutes=1.0,
        record_precision_category="recorded_to_minute",
        sex_at_birth_category="female",
        delivery_mode_category="spontaneous_vaginal",
        maternal_age_at_birth_years=30.0,
        gestational_age_at_birth_weeks=39.0,
        birthweight_grams=3300.0,
        recruitment_source_category="hospital_registry_invitation",
        relationship_component_id=component,
    )


def keyed_responses(keyed_value: int) -> dict[int, int]:
    responses: dict[int, int] = {}
    for scale in SCORING_KEY.values():
        for item in scale["positive"]:
            responses[item] = keyed_value
        for item in scale["negative"]:
            responses[item] = 6 - keyed_value
    return responses


def synthetic_analysis_rows(model: LiteratureModelV1) -> list[AnalysisRow]:
    """Build a deterministic 20-network software fixture, not a human cohort."""

    from hdmatch.empirical_astrology.features import PairFeatures

    rows: list[AnalysisRow] = []
    for network_index in range(20):
        network = f"SYN_NET_{network_index:02d}"
        hospital = f"SYN_HOSP_{network_index:02d}"
        local_date = date(2000, 1, 1) + timedelta(days=network_index)
        for pair_index in range(10):
            left = f"SYN_P_{network_index:02d}_{pair_index:02d}_A"
            right = f"SYN_P_{network_index:02d}_{pair_index:02d}_B"
            x = 0.05 + 2.85 * pair_index / 9
            # The exact nuisance construction is exercised above from real
            # BirthRecord fixtures.  This numerical-rank fixture sets those
            # controls to zero so its sole purpose is an unambiguous TN-001,
            # CR1, gap-bound, LOO, and bootstrap code-path check.
            nuisance = (0.0,) * len(NUISANCE_COLUMN_NAMES)
            pair = PairFeatures(
                pair_id=deterministic_pair_id(
                    left,
                    right,
                    protocol_version=model.contract.protocol_version,
                    base_seed=model.contract.base_seed,
                ),
                participant_ids=(left, right),
                network_id=network,
                hospital_id=hospital,
                local_birth_date=local_date,
                center_gap_hours=x,
                lower_gap_hours=max(0.0, x - 0.02),
                upper_gap_hours=min(3.0, x + 0.02),
                nuisance_values=nuisance,
            )
            slope = 0.010 + (network_index - 9.5) * 0.00015
            noise = ((pair_index % 3) - 1) * 0.001 * (1 + network_index / 40)
            outcome = 0.20 + slope * x + noise
            rows.append(AnalysisRow(pair=pair, outcome_distance=outcome))
    return rows


def main() -> None:
    numerical_runtime = require_deterministic_numerical_runtime()
    manifest_path = ROOT / INPUT_MANIFEST
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["selected_human_development_files"] != []:
        raise RuntimeError("this runner is frozen to an empty human-data allowlist")
    if manifest["owner_known_outcomes_accessed"] is not False:
        raise RuntimeError("owner-known outcomes must remain inaccessible")
    if manifest["untouched_prospective_outcomes_accessed"] is not False:
        raise RuntimeError("prospective outcomes must remain inaccessible")

    model = LiteratureModelV1.load(ROOT)
    verify_required_git_ancestor(model.contract)
    model_version = model.model_version
    input_hash = sha256(manifest_path)
    software_commit = git_head()
    rows: list[dict[str, Any]] = []

    no_data_reason = (
        "No eligible raw non-owner same-hospital IPIP development dataset with the frozen "
        "participant covariates is available; aggregate literature records cannot substitute."
    )
    empirical_comparisons = [
        ("W4-EMP-FULL-V1B", "frozen_full_model"),
        ("W4-EMP-THEORY-NEUTRAL", "theory_neutral_birth_time_distance"),
        ("W4-EMP-BASELINE-INTERCEPT", "intercept_only"),
        ("W4-EMP-BASELINE-DATE", "date_only_local_calendar_date_fixed_effects"),
        ("W4-EMP-BASELINE-TIME", "time_only_eight_clock_columns"),
        ("W4-EMP-BASELINE-SITE", "location_site_only_hospital_fixed_effects"),
        ("W4-EMP-BASELINE-SEASON-COHORT", "season_cohort_birth_year_annual_phase"),
        ("W4-EMP-BASELINE-FULL-NULL", "full_conventional_null"),
        ("W4-EMP-BASELINE-TIME-DISTANCE", "time_distance_only"),
        ("W4-EMP-BASELINE-FULL-PLUS-X", "full_conventional_plus_tn001"),
        ("W4-EMP-MATERNAL-AGE-NC", "maternal_age_negative_control"),
        ("W4-EMP-GAP-LOWER", "lower_birth_gap_bound"),
        ("W4-EMP-GAP-UPPER", "upper_birth_gap_bound"),
        ("W4-EMP-STRICT-PRECISION", "strict_half_width_at_most_half_minute"),
        ("W4-EMP-BELIEF-STRATA", "belief_levels_0_through_4"),
        ("W4-EMP-SIGN-KNOWLEDGE-STRATA", "sign_name_knowledge_strata"),
    ]
    for result_id, comparison in empirical_comparisons:
        rows.append(
            unavailable_row(
                result_id,
                comparison,
                no_data_reason,
                model_version=model_version,
                input_hash=input_hash,
                software_commit=software_commit,
            )
        )
    rows.append(
        unavailable_row(
            "W4-EMP-RANDOM-FEATURE-DIAGNOSTICS",
            "twenty_random_feature_diagnostics",
            no_data_reason,
            model_version=model_version,
            input_hash=input_hash,
            software_commit=software_commit,
            planned_tests=20,
        )
    )
    rows.append(
        unavailable_row(
            "W4-EMP-LOO-NETWORK",
            "all_twenty_leave_one_network_out_fits",
            no_data_reason,
            model_version=model_version,
            input_hash=input_hash,
            software_commit=software_commit,
            planned_tests=20,
        )
    )
    for result_id, comparison in (
        ("W4-EMP-POWER-BETA-0", "development_residual_null_calibration_beta_0"),
        ("W4-EMP-POWER-BETA-001", "development_residual_power_beta_0_01"),
    ):
        rows.append(
            unavailable_row(
                result_id,
                comparison,
                "No declared hashed non-owner residual template with 20 networks and 100 "
                "same-instrument pairs per network exists; launch remains blocked.",
                model_version=model_version,
                input_hash=input_hash,
                software_commit=software_commit,
                planned_tests=5000,
                launch_blocked=True,
            )
        )

    ablation_reason = (
        "The frozen astrology surface is empty; removing an absent feature is not an effect test."
    )
    for candidate in range(1, 9):
        rows.append(
            unavailable_row(
                f"W4-ABL-CF-{candidate:03d}",
                f"remove_CF-{candidate:03d}",
                ablation_reason,
                model_version=model_version,
                input_hash=input_hash,
                software_commit=software_commit,
                status="NOT_APPLICABLE_NO_INCLUDED_FEATURE",
            )
        )
    rows.append(
        unavailable_row(
            "W4-ABL-ALL-ASTROLOGY",
            "remove_all_astrology_features",
            "Full v1b and the theory-neutral model are definitionally identical.",
            model_version=model_version,
            input_hash=input_hash,
            software_commit=software_commit,
            status="NOT_APPLICABLE_NO_INCLUDED_FEATURE",
        )
    )

    decision = model.contract.decision
    registry = model.contract.feature_registry
    executable_empty = (
        registry["executable_astrology_features"] == []
        and registry["aspect_to_trait_mappings"] == []
        and registry["executable_moderator_interactions"] == []
        and registry["astrology_weights"] == {}
        and registry["astrology_coefficient_vector_length"] == 0
    )
    if not executable_empty or model.executable_astrology_feature_ids != ():
        raise AssertionError("astrology surface is not empty")
    rows.append(
        engineering_row(
            "W4-ENG-CONTRACT",
            "artifact_hash_version_ancestry_and_authorization",
            {
                "decision_sha256": model.contract.decision_sha256,
                "feature_registry_sha256": model.contract.feature_registry_sha256,
                "model_sha256": model.contract.model_sha256,
                "review_base_commit": decision["review_base_commit"],
                "verdict": decision["verdict"],
            },
            model_version=model_version,
            input_hash=input_hash,
            software_commit=software_commit,
        )
    )
    rows.append(
        engineering_row(
            "W4-ENG-EMPTY-ASTROLOGY",
            "empty_astrology_surface_and_full_neutral_equivalence",
            {
                "executable_feature_ids": list(model.executable_feature_ids),
                "executable_astrology_feature_ids": [],
                "astrology_coefficient_vector_length": 0,
                "full_equals_theory_neutral": True,
            },
            model_version=model_version,
            input_hash=input_hash,
            software_commit=software_commit,
        )
    )

    low_scores = score_ipip50(keyed_responses(1))
    high_scores = score_ipip50(keyed_responses(5))
    if ipip_pair_distance(low_scores, low_scores) != 0.0:
        raise AssertionError("identical IPIP profiles must have distance zero")
    if ipip_pair_distance(low_scores, high_scores) != 1.0:
        raise AssertionError("opposite endpoint profiles must have distance one")
    rows.append(
        engineering_row(
            "W4-ENG-IPIP",
            "complete_ipip_scoring_and_distance_endpoints",
            {"identical_distance": 0.0, "opposite_endpoint_distance": 1.0},
            model_version=model_version,
            input_hash=input_hash,
            software_commit=software_commit,
        )
    )

    left = make_birth_record(
        "PAIR_A",
        datetime(2026, 1, 2, 12, 0, tzinfo=UTC),
        720.0,
        "REL_A",
    )
    right = make_birth_record(
        "PAIR_B",
        datetime(2026, 1, 2, 13, 0, tzinfo=UTC),
        780.0,
        "REL_B",
    )
    pair = build_pair_features(
        left,
        right,
        protocol_version=model.contract.protocol_version,
        base_seed=model.contract.base_seed,
    )
    if (pair.lower_gap_hours, pair.center_gap_hours, pair.upper_gap_hours) != (
        58 / 60,
        1.0,
        62 / 60,
    ):
        raise AssertionError("gap-bound fixture changed")
    reverse_id = deterministic_pair_id(
        "PAIR_B",
        "PAIR_A",
        protocol_version=model.contract.protocol_version,
        base_seed=model.contract.base_seed,
    )
    if pair.pair_id != reverse_id or len(pair.nuisance_values) != 14:
        raise AssertionError("pair invariance or nuisance order changed")
    random_features = [
        deterministic_random_feature(
            pair.pair_id,
            index,
            protocol_version=model.contract.protocol_version,
            base_seed=model.contract.base_seed,
        )
        for index in range(1, 21)
    ]
    if len(set(random_features)) != 20 or not all(0.0 < value < 3.0 for value in random_features):
        raise AssertionError("random-feature fixture changed")
    rows.append(
        engineering_row(
            "W4-ENG-PAIR-FEATURES",
            "gap_bounds_pair_hash_nuisance_order_and_random_features",
            {
                "gap_minutes": {"lower": 58.0, "center": 60.0, "upper": 62.0},
                "nuisance_column_count": len(NUISANCE_COLUMN_NAMES),
                "random_feature_count": 20,
                "random_feature_min": min(random_features),
                "random_feature_max": max(random_features),
            },
            model_version=model_version,
            input_hash=input_hash,
            software_commit=software_commit,
        )
    )

    synthetic = synthetic_analysis_rows(model)
    fit = fit_primary_association(synthetic, required_networks=20)
    lower, upper = fit_gap_bound_sensitivities(synthetic, required_networks=20).require_all()
    loo = leave_one_network_out(synthetic).require_all()
    bootstrap_a = restricted_wild_cluster_bootstrap(
        synthetic,
        draws=99,
        seed=model.contract.model["randomness_and_determinism"]["bootstrap_seed_A"],
        required_networks=20,
    )
    bootstrap_b = restricted_wild_cluster_bootstrap(
        synthetic,
        draws=99,
        seed=model.contract.model["randomness_and_determinism"]["bootstrap_seed_A"],
        required_networks=20,
    )
    if asdict(bootstrap_a) != asdict(bootstrap_b):
        raise AssertionError("bootstrap seed replay is not deterministic")
    if len(loo) != 20 or not all(result.n_networks == 19 for result in loo):
        raise AssertionError("leave-one-network-out fixture changed")
    rows.append(
        engineering_row(
            "W4-ENG-ANALYSIS",
            "wls_cr1_gap_loo_and_bootstrap_seed_replay",
            {
                "fixture_only_beta": fit.beta,
                "fixture_only_standard_error": fit.standard_error,
                "fixture_only_ci95": list(fit.confidence_interval_95),
                "lower_bound_beta": lower.beta,
                "upper_bound_beta": upper.beta,
                "loo_fit_count": len(loo),
                "bootstrap_fixture_draws": bootstrap_a.draws,
                "bootstrap_fixture_p": bootstrap_a.p_value_one_sided,
                "prospective_draw_requirement_not_run": 99999,
            },
            model_version=model_version,
            input_hash=input_hash,
            software_commit=software_commit,
        )
    )

    holm = require_exact_diagnostic_family([0.001] + [0.5] * 20)
    if len(holm) != 21:
        raise AssertionError("Holm diagnostic family changed")
    rows.append(
        engineering_row(
            "W4-ENG-MULTIPLICITY",
            "fixed_twenty_one_test_holm_family",
            {
                "family_size": len(holm),
                "first_adjusted_p": holm[0].adjusted_p_value,
                "rejection_count": sum(result.rejected for result in holm),
                "empirical_tests_run": 0,
            },
            model_version=model_version,
            input_hash=input_hash,
            software_commit=software_commit,
        )
    )

    if manifest["prospective_launch_blocked"] is not True:
        raise AssertionError("missing development reference must block prospective launch")
    rows.append(
        engineering_row(
            "W4-ENG-LEAKAGE-BOUNDARY",
            "empty_human_allowlist_and_outcome_access_boundary",
            {
                "selected_human_development_files": [],
                "owner_outcomes_accessed": False,
                "untouched_prospective_outcomes_accessed": False,
                "prospective_launch_blocked": True,
            },
            model_version=model_version,
            input_hash=input_hash,
            software_commit=software_commit,
        )
    )

    output = ROOT / RESULTS_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    fixture_summary = {
        "schema_version": "empirical-astrology-wave4-engineering-summary-v1",
        "run_date": "2026-09-28",
        "software_commit": software_commit,
        "model_version": model_version,
        "input_manifest_sha256": input_hash,
        "results_sha256": sha256(output),
        "result_row_count": len(rows),
        "empirical_human_test_count": 0,
        "engineering_fixture_rows": sum(
            row["evaluation_class"] == "ENGINEERING_FIXTURE" for row in rows
        ),
        "owner_outcomes_accessed": False,
        "untouched_prospective_outcomes_accessed": False,
        "prospective_launch_blocked": True,
        "numerical_runtime": numerical_runtime,
        "interpretation": (
            "Engineering fixtures validate deterministic code paths only; they are not "
            "empirical evidence, power evidence, or prospective validation."
        ),
    }
    fixture_path = ROOT / FIXTURE_PATH
    fixture_path.write_text(
        json.dumps(fixture_summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(fixture_summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
