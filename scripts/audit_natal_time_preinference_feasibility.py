"""Build synthetic-only pre-inference feasibility and disclosure artifacts.

The calculations in this module are sensitivity illustrations. They are not a
power analysis for an expected Human Design effect, a cohort-size selection, or
an inferential implementation.
"""

from __future__ import annotations

import argparse
import math
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.util import canonical_json_bytes, sha256_json

CREATED_AT = datetime(2026, 8, 30, 4, 15, tzinfo=UTC)
NOMINAL_TWO_SIDED_TAIL_AREA = 0.05
NORMAL_QUANTILE = 1.959963984540054
SAMPLE_SIZES = (50, 100, 200, 400, 800)


def _round(value: float) -> float:
    return round(value, 6)


def wilson_interval(sample_size: int, assumed_rate: float) -> dict[str, float]:
    """Return an illustrative Wilson interval for a hypothetical binary rate."""

    z2 = NORMAL_QUANTILE**2
    denominator = 1 + z2 / sample_size
    center = (assumed_rate + z2 / (2 * sample_size)) / denominator
    half_width = (
        NORMAL_QUANTILE
        * math.sqrt(assumed_rate * (1 - assumed_rate) / sample_size + z2 / (4 * sample_size**2))
        / denominator
    )
    return {
        "lower": _round(max(0.0, center - half_width)),
        "upper": _round(min(1.0, center + half_width)),
        "half_width": _round(half_width),
    }


def hoeffding_half_width(sample_size: int) -> float:
    """Distribution-free illustration for a mean of participant-level [0, 1] values."""

    return _round(math.sqrt(math.log(2 / NOMINAL_TWO_SIDED_TAIL_AREA) / (2 * sample_size)))


def paired_required_sample_size(net_difference: float, discordant_rate: float) -> int:
    """Approximate paired sample needed for a Wald interval to exclude zero.

    The hypothetical paired difference is encoded as -1, 0, or +1,
    ``discordant_rate`` is P(|difference| = 1), and ``net_difference`` is the
    absolute assumed E[difference]. This is a precision illustration, not a
    selected test, power calculation, or sample-size recommendation.
    """

    if not 0 < net_difference <= discordant_rate <= 1:
        raise ValueError("require 0 < net_difference <= discordant_rate <= 1")
    variance = discordant_rate - net_difference**2
    return math.ceil((NORMAL_QUANTILE**2 * variance) / net_difference**2)


def calibration_error_interval(
    sample_size: int,
    hypothetical_predicted_rate: float,
    hypothetical_signed_deviation: float,
) -> dict[str, float]:
    """Return a hypothetical signed calibration-error uncertainty interval.

    Error is defined only for this synthetic surface as observed event rate
    minus hypothetical predicted rate. The function does not select a
    calibrator, probability target, binning scheme, or operating point.
    """

    assumed_observed_rate = hypothetical_predicted_rate + hypothetical_signed_deviation
    if not 0 <= hypothetical_predicted_rate <= 1:
        raise ValueError("hypothetical_predicted_rate must be in [0, 1]")
    if not 0 <= assumed_observed_rate <= 1:
        raise ValueError("predicted rate plus signed deviation must be in [0, 1]")
    observed_interval = wilson_interval(sample_size, assumed_observed_rate)
    return {
        "assumed_observed_rate": _round(assumed_observed_rate),
        "signed_error_lower": _round(observed_interval["lower"] - hypothetical_predicted_rate),
        "signed_error_upper": _round(observed_interval["upper"] - hypothetical_predicted_rate),
        "sampling_half_width": observed_interval["half_width"],
    }


def _self_hash(payload: dict[str, Any], field: str) -> dict[str, Any]:
    payload[field] = sha256_json(payload)
    return payload


def build_feasibility_report(repository_commit: str) -> dict[str, Any]:
    """Return the reproducible hypothetical feasibility sensitivity grid."""

    binary_rows: list[dict[str, Any]] = []
    for metric, rates in (
        ("coverage_intersection_binary_indicator", (0.5, 0.7, 0.9)),
        ("abstention_binary_indicator", (0.1, 0.3, 0.5)),
        ("date_coverage_binary_indicator", (0.5, 0.7, 0.9)),
    ):
        for assumed_rate in rates:
            for sample_size in SAMPLE_SIZES:
                binary_rows.append(
                    {
                        "metric": metric,
                        "sample_size": sample_size,
                        "assumed_rate": assumed_rate,
                        "illustrative_interval": wilson_interval(sample_size, assumed_rate),
                    }
                )

    bounded_mean_rows = [
        {
            "metric": metric,
            "sample_size": sample_size,
            "distribution_free_half_width": hoeffding_half_width(sample_size),
        }
        for metric in (
            "temporal_width_retained_ratio",
            "full_state_count_retained_ratio",
        )
        for sample_size in SAMPLE_SIZES
    ]

    paired_rows = [
        {
            "hypothetical_net_paired_difference": difference,
            "assumed_discordant_pair_rate": discordance,
            "approximate_sample_size": paired_required_sample_size(difference, discordance),
        }
        for difference in (0.02, 0.05, 0.1)
        for discordance in (0.1, 0.3, 0.5)
    ]

    calibration_error_rows: list[dict[str, Any]] = []
    for sample_size in (20, 50, 100, 200):
        for hypothetical_predicted_rate in (0.2, 0.5, 0.8):
            for hypothetical_signed_deviation in (-0.1, 0.0, 0.1):
                calibration_error_rows.append(
                    {
                        "hypothetical_calibration_cell_size": sample_size,
                        "hypothetical_predicted_rate": hypothetical_predicted_rate,
                        "hypothetical_signed_calibration_deviation": (
                            hypothetical_signed_deviation
                        ),
                        "illustrative_signed_error_interval": calibration_error_interval(
                            sample_size,
                            hypothetical_predicted_rate,
                            hypothetical_signed_deviation,
                        ),
                    }
                )

    subgroup_rows: list[dict[str, Any]] = []
    for total_sample_size in (100, 200, 400, 800):
        for assumed_prevalence in (0.1, 0.25, 0.5):
            expected_cell_size = max(1, math.floor(total_sample_size * assumed_prevalence))
            for assumed_outcome_rate in (0.5, 0.8):
                subgroup_rows.append(
                    {
                        "total_sample_size": total_sample_size,
                        "hypothetical_subgroup_or_source_quality_prevalence": assumed_prevalence,
                        "expected_cell_size": expected_cell_size,
                        "assumed_binary_outcome_rate": assumed_outcome_rate,
                        "illustrative_interval": wilson_interval(
                            expected_cell_size, assumed_outcome_rate
                        ),
                    }
                )

    payload: dict[str, Any] = {
        "schema_version": "natal-time-preinference-feasibility-v1",
        "repository_commit": repository_commit,
        "created_at_utc": CREATED_AT.isoformat().replace("+00:00", "Z"),
        "synthetic_only": True,
        "human_observations_used": 0,
        "status": "hypothetical_sensitivity_grid_not_a_study_choice",
        "non_selections": {
            "cohort_size_selected": False,
            "expected_hd_effect_claimed": False,
            "operating_point_selected": False,
            "estimator_selected": False,
            "calibration_method_selected": False,
            "subgroup_definition_selected": False,
            "recruitment_cost_or_burden_committed": False,
        },
        "global_assumptions": {
            "nominal_two_sided_tail_area": NOMINAL_TWO_SIDED_TAIL_AREA,
            "normal_quantile": NORMAL_QUANTILE,
            "participants_treated_as_independent_only_after_connected_component_split": True,
            "all_rates_and_effect_sizes_are_hypothetical": True,
            "synthetic_chart_oracle_is_not_a_human_effect_estimate": True,
        },
        "binary_rate_precision": {
            "formula": "Wilson score interval evaluated at an assumed binary rate",
            "purpose": "precision sensitivity only; denominator/estimand remains protocol-defined",
            "rows": binary_rows,
        },
        "width_and_state_count_precision": {
            "formula": "sqrt(log(2/alpha)/(2*n)) for a mean bounded in [0,1]",
            "purpose": "distribution-free sensitivity for the two separate retained-ratio metrics",
            "rows": bounded_mean_rows,
        },
        "paired_baseline_sensitivity": {
            "formula": "ceil(z^2*(discordant_rate-net_difference^2)/net_difference^2)",
            "purpose": (
                "approximate paired-participant sensitivity, not a power guarantee or "
                "expected effect"
            ),
            "assumptions": [
                "paired outcome difference is encoded as -1, 0, or +1",
                "discordant_rate is P(abs(paired_difference)=1)",
                "net_difference is abs(E[paired_difference])",
                "paired_difference variance is discordant_rate minus net_difference squared",
                "a two-sided Wald-normal interval uses the displayed fixed normal quantile",
                "connected components, not rows, are the independent units",
                (
                    "no target power, attrition allowance, multiplicity adjustment, or "
                    "finite-sample exact guarantee is selected"
                ),
            ],
            "requires_future_comparator_and_outcome_definition": True,
            "target_power_selected": False,
            "rows": paired_rows,
        },
        "potential_future_calibration_error_sensitivity": {
            "formula": (
                "Wilson interval for the assumed observed event rate, translated by "
                "subtracting the hypothetical predicted rate"
            ),
            "signed_error_definition": "observed event rate minus hypothetical predicted rate",
            "purpose": (
                "illustrate uncertainty around explicitly hypothetical signed calibration "
                "deviations; no predictive target, calibrator, binning scheme, or operating "
                "point is selected"
            ),
            "calibrated_outputs_do_not_exist": True,
            "all_predicted_rates_and_deviations_are_hypothetical": True,
            "limitations": [
                "the rows illustrate one synthetic calibration cell at a time",
                (
                    "they do not bound model error, selection bias, distribution shift, "
                    "or multiplicity"
                ),
                "they are not evidence that a probability-bearing natal output can be calibrated",
            ],
            "rows": calibration_error_rows,
        },
        "subgroup_and_source_quality_sensitivity": {
            "formula": "floor(total_n*assumed_prevalence), then Wilson outcome-rate interval",
            "purpose": (
                "show sparse-cell precision loss; no subgroup or source-quality comparison selected"
            ),
            "rows": subgroup_rows,
        },
        "limitations": [
            "No row is a cohort-size recommendation or recruitment authorization.",
            (
                "Nominal intervals omit design effects, attrition, missing reference intervals, "
                "model selection, multiplicity, and distribution shift."
            ),
            (
                "Coverage, temporal width, state count, abstention, and date coverage remain "
                "separate outcomes."
            ),
            (
                "Conditional-on-non-abstention and full-cohort denominators remain unresolved "
                "protocol choices."
            ),
            (
                "Synthetic state counts and synthetic oracle performance are not human sample "
                "sizes or human effect estimates."
            ),
            (
                "No Human Design validity, recoverability, calibration, or practical-use claim "
                "follows from this grid."
            ),
        ],
    }
    return _self_hash(payload, "artifact_sha256")


PUBLIC_UNRESOLVED_CONTROL_CODES = (
    "correction_and_withdrawal_policy",
    "privacy_budget_if_any",
    "release_cadence",
    "small_cell_suppression_threshold",
)
PUBLIC_AGGREGATE_INVARIANTS = (
    "included_count_lte_eligible_count",
    "included_count_eq_abstention_plus_non_abstaining_evaluable",
    "coverage_intersection_count_lte_non_abstaining_evaluable_count",
    "date_coverage_eligible_count_lte_included_count",
    "date_coverage_evaluable_count_lte_date_coverage_eligible_count",
    "date_coverage_evaluable_count_lte_non_abstaining_evaluable_count",
    "date_coverage_intersection_count_lte_date_coverage_evaluable_count",
    "ratio_summary_counts_eq_non_abstaining_evaluable_count",
    "ratio_summary_values_null_iff_evaluable_count_is_zero",
)


def validate_public_aggregate_semantics(record: dict[str, Any]) -> tuple[str, ...]:
    """Return fail-closed cross-field violations for one candidate public record."""

    aggregate = record.get("cohort_aggregate")
    if not isinstance(aggregate, dict):
        return ("cohort_aggregate_missing_or_invalid",)

    errors: list[str] = []
    count_names = (
        "eligible_count",
        "included_count",
        "non_abstaining_evaluable_count",
        "coverage_intersection_count",
        "abstention_count",
        "date_coverage_eligible_count",
        "date_coverage_evaluable_count",
        "date_coverage_intersection_count",
    )
    counts: dict[str, int] = {}
    for name in count_names:
        value = aggregate.get(name)
        if type(value) is not int or value < 0:
            errors.append(f"{name}_must_be_nonnegative_integer")
        else:
            counts[name] = value

    summary_names = (
        "temporal_width_retained_ratio_summary",
        "full_state_count_retained_ratio_summary",
    )
    summary_counts: dict[str, int] = {}
    for name in summary_names:
        summary = aggregate.get(name)
        if not isinstance(summary, dict):
            errors.append(f"{name}_missing_or_invalid")
            continue
        eligible_count = summary.get("eligible_count")
        if type(eligible_count) is not int or eligible_count < 0:
            errors.append(f"{name}_eligible_count_must_be_nonnegative_integer")
            continue
        summary_counts[name] = eligible_count
        for statistic in ("mean", "median"):
            value = summary.get(statistic)
            if eligible_count == 0:
                if value is not None:
                    errors.append(f"{name}_{statistic}_must_be_null_when_count_is_zero")
            elif (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not 0 <= value <= 1
            ):
                errors.append(f"{name}_{statistic}_must_be_unit_interval_number")

    if {"eligible_count", "included_count"} <= counts.keys() and (
        counts["included_count"] > counts["eligible_count"]
    ):
        errors.append("included_count_exceeds_eligible_count")
    if {
        "included_count",
        "abstention_count",
        "non_abstaining_evaluable_count",
    } <= counts.keys() and counts["included_count"] != (
        counts["abstention_count"] + counts["non_abstaining_evaluable_count"]
    ):
        errors.append("included_count_not_abstention_plus_non_abstaining_evaluable")
    if {
        "coverage_intersection_count",
        "non_abstaining_evaluable_count",
    } <= counts.keys() and (
        counts["coverage_intersection_count"] > counts["non_abstaining_evaluable_count"]
    ):
        errors.append("coverage_intersection_count_exceeds_evaluable_count")
    if {"date_coverage_eligible_count", "included_count"} <= counts.keys() and (
        counts["date_coverage_eligible_count"] > counts["included_count"]
    ):
        errors.append("date_coverage_eligible_count_exceeds_included_count")
    if {
        "date_coverage_evaluable_count",
        "date_coverage_eligible_count",
    } <= counts.keys() and (
        counts["date_coverage_evaluable_count"] > counts["date_coverage_eligible_count"]
    ):
        errors.append("date_coverage_evaluable_count_exceeds_eligible_count")
    if {
        "date_coverage_evaluable_count",
        "non_abstaining_evaluable_count",
    } <= counts.keys() and (
        counts["date_coverage_evaluable_count"] > counts["non_abstaining_evaluable_count"]
    ):
        errors.append("date_coverage_evaluable_count_exceeds_non_abstaining_count")
    if {
        "date_coverage_intersection_count",
        "date_coverage_evaluable_count",
    } <= counts.keys() and (
        counts["date_coverage_intersection_count"] > counts["date_coverage_evaluable_count"]
    ):
        errors.append("date_coverage_intersection_count_exceeds_evaluable_count")

    non_abstaining = counts.get("non_abstaining_evaluable_count")
    if non_abstaining is not None:
        for name, summary_count in summary_counts.items():
            if summary_count != non_abstaining:
                errors.append(f"{name}_eligible_count_not_non_abstaining_evaluable_count")
    return tuple(errors)


def build_public_ledger_schema(repository_commit: str) -> dict[str, Any]:
    """Return a release-disabled candidate schema plus one synthetic aggregate example."""

    record_schema: dict[str, Any] = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "synthetic_only",
            "release_authorized",
            "cohort_aggregate",
            "nonpersonal_provenance",
            "disclosure_review",
        ],
        "properties": {
            "schema_version": {"const": "natal-time-public-ledger-cohort-aggregate-v0"},
            "synthetic_only": {"const": True},
            "release_authorized": {"const": False},
            "cohort_aggregate": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "eligible_count",
                    "included_count",
                    "non_abstaining_evaluable_count",
                    "coverage_intersection_count",
                    "abstention_count",
                    "date_coverage_eligible_count",
                    "date_coverage_evaluable_count",
                    "date_coverage_intersection_count",
                    "temporal_width_retained_ratio_summary",
                    "full_state_count_retained_ratio_summary",
                ],
                "properties": {
                    "eligible_count": {"type": "integer", "minimum": 0},
                    "included_count": {"type": "integer", "minimum": 0},
                    "non_abstaining_evaluable_count": {
                        "type": "integer",
                        "minimum": 0,
                    },
                    "coverage_intersection_count": {"type": "integer", "minimum": 0},
                    "abstention_count": {"type": "integer", "minimum": 0},
                    "date_coverage_eligible_count": {"type": "integer", "minimum": 0},
                    "date_coverage_evaluable_count": {"type": "integer", "minimum": 0},
                    "date_coverage_intersection_count": {"type": "integer", "minimum": 0},
                    "temporal_width_retained_ratio_summary": {"$ref": "#/$defs/ratio_summary"},
                    "full_state_count_retained_ratio_summary": {"$ref": "#/$defs/ratio_summary"},
                },
            },
            "nonpersonal_provenance": {
                "type": "object",
                "additionalProperties": False,
                "required": ["protocol_version", "method_version", "software_commit"],
                "properties": {
                    "protocol_version": {
                        "type": "string",
                        "pattern": "^NT-PROTOCOL-[0-9]{8}-V[0-9]+$",
                    },
                    "method_version": {
                        "type": "string",
                        "pattern": "^NT-METHOD-[A-Z0-9]+-V[0-9]+$",
                    },
                    "software_commit": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
                },
            },
            "disclosure_review": {
                "type": "object",
                "additionalProperties": False,
                "required": ["status", "unresolved_controls"],
                "properties": {
                    "status": {"const": "synthetic_not_reviewed_for_release"},
                    "unresolved_controls": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": list(PUBLIC_UNRESOLVED_CONTROL_CODES),
                        },
                        "minItems": 1,
                        "uniqueItems": True,
                    },
                },
            },
        },
        "$defs": {
            "ratio_summary": {
                "type": "object",
                "additionalProperties": False,
                "required": ["eligible_count", "mean", "median"],
                "properties": {
                    "eligible_count": {"type": "integer", "minimum": 0},
                    "mean": {
                        "oneOf": [
                            {"type": "number", "minimum": 0, "maximum": 1},
                            {"type": "null"},
                        ]
                    },
                    "median": {
                        "oneOf": [
                            {"type": "number", "minimum": 0, "maximum": 1},
                            {"type": "null"},
                        ]
                    },
                },
            },
        },
        "x-semantic-validator": {
            "required": True,
            "implementation": (
                "scripts.audit_natal_time_preinference_feasibility."
                "validate_public_aggregate_semantics"
            ),
            "invariant_codes": list(PUBLIC_AGGREGATE_INVARIANTS),
        },
    }
    synthetic_example = {
        "schema_version": "natal-time-public-ledger-cohort-aggregate-v0",
        "synthetic_only": True,
        "release_authorized": False,
        "cohort_aggregate": {
            "eligible_count": 200,
            "included_count": 180,
            "non_abstaining_evaluable_count": 135,
            "coverage_intersection_count": 94,
            "abstention_count": 45,
            "date_coverage_eligible_count": 40,
            "date_coverage_evaluable_count": 30,
            "date_coverage_intersection_count": 21,
            "temporal_width_retained_ratio_summary": {
                "eligible_count": 135,
                "mean": 0.5,
                "median": 0.5,
            },
            "full_state_count_retained_ratio_summary": {
                "eligible_count": 135,
                "mean": 0.5,
                "median": 0.5,
            },
        },
        "nonpersonal_provenance": {
            "protocol_version": "NT-PROTOCOL-00000000-V0",
            "method_version": "NT-METHOD-SYNTHETIC-V0",
            "software_commit": "0" * 40,
        },
        "disclosure_review": {
            "status": "synthetic_not_reviewed_for_release",
            "unresolved_controls": list(PUBLIC_UNRESOLVED_CONTROL_CODES),
        },
    }
    semantic_violations = validate_public_aggregate_semantics(synthetic_example)
    if semantic_violations:
        raise ValueError(
            "synthetic public aggregate violates semantic contract: "
            + ", ".join(semantic_violations)
        )
    payload: dict[str, Any] = {
        "schema_version": "natal-time-public-ledger-synthetic-schema-artifact-v1",
        "repository_commit": repository_commit,
        "created_at_utc": CREATED_AT.isoformat().replace("+00:00", "Z"),
        "synthetic_only": True,
        "status": "candidate_schema_not_a_release_policy",
        "public_release_authorized": False,
        "default_granularity": "cohort_aggregate_only",
        "semantic_validation": {
            "required_after_structural_schema_validation": True,
            "validator": "validate_public_aggregate_semantics",
            "synthetic_example_status": "passed",
            "invariant_codes": list(PUBLIC_AGGREGATE_INVARIANTS),
        },
        "record_schema": record_schema,
        "synthetic_example": synthetic_example,
        "prohibited_public_fields": [
            "participant_level_rows",
            "natal_chart_intervals",
            "exact_birth_dates",
            "birth_places",
            "source_documents",
            "relationship_identifiers",
            "personal_data_hashes",
            "free_text",
        ],
        "unresolved_release_controls": [
            "small_cell_suppression_threshold",
            "privacy_budget_or_alternative_disclosure_control",
            "release_cadence_and_repeated_release_review",
            "withdrawal_deletion_and_versioned_correction_policy",
            "whether_any_subgroup_aggregate_is_safe_and_useful",
        ],
    }
    return _self_hash(payload, "artifact_sha256")


def build_methods_decision_ledger(repository_commit: str) -> dict[str, Any]:
    """Return classifications and evidence gates without selecting an estimator."""

    entries = [
        {
            "method_family": "interval_censored_reference_data",
            "classification": "adaptation",
            "reason": (
                "Preserves documentary interval precision but does not rank one person's "
                "candidates."
            ),
            "evidence_required_before_use": [
                "predeclared intersection and width estimands",
                "simulation under observed reference-precision patterns",
                "untouched participant validation",
            ],
        },
        {
            "method_family": "prior_sensitivity",
            "classification": "adaptation",
            "reason": (
                "Relevant only if a later supervised design independently selects a "
                "prior-bearing model."
            ),
            "evidence_required_before_use": [
                "external evidence for every prior family",
                "predeclared sensitivity range",
                "held-out stability analysis",
            ],
        },
        {
            "method_family": "probability_calibration",
            "classification": "adaptation",
            "reason": (
                "Raw ranks or support values cannot be relabeled as calibrated probabilities."
            ),
            "evidence_required_before_use": [
                "frozen predictive target and method",
                "untouched connected-component calibration cohort",
                "calibration and shift diagnostics",
            ],
        },
        {
            "method_family": "abstention_rejection",
            "classification": "adaptation",
            "reason": (
                "Abstention is compatible with set output, but its loss and threshold are "
                "not neutral."
            ),
            "evidence_required_before_use": [
                "owner-selected operating semantics",
                "frozen loss and threshold",
                "separate coverage width and abstention reporting",
            ],
        },
        {
            "method_family": "conformal_set_valued",
            "classification": "unresolved_experimental",
            "reason": (
                "Conceptually aligned with set output, but exchangeability and sample adequacy "
                "are unproved."
            ),
            "evidence_required_before_use": [
                "fixed target and nonconformity construction",
                "exchangeability audit",
                "untouched participant-level calibration data",
            ],
        },
        {
            "method_family": "measurement_reliability",
            "classification": "adaptation",
            "reason": (
                "Reliability methods require a specified construct, rater model, and "
                "repeated-measure design."
            ),
            "evidence_required_before_use": [
                "separate item-development checkpoint",
                "test-retest and inter-rater design",
                "missingness response-style and invariance analysis",
            ],
        },
        {
            "method_family": "participant_connected_component_splitting",
            "classification": "direct_reuse",
            "reason": (
                "Prevents identity, relationship, household, and shared-record-source leakage "
                "across roles."
            ),
            "evidence_required_before_use": [
                "frozen graph construction rules",
                "synthetic leakage tests",
                "split receipt proving component disjointness",
            ],
        },
        {
            "method_family": "nested_adaptation",
            "classification": "direct_reuse",
            "reason": (
                "Every adaptive choice belongs inside development; final evaluation stays "
                "untouched."
            ),
            "evidence_required_before_use": [
                "complete adaptive-choice registry",
                "role-based access controls",
                "reproducible outer evaluation receipt",
            ],
        },
        {
            "method_family": "permutation_and_negative_controls",
            "classification": "baseline_only",
            "reason": (
                "They test null and leakage behavior but do not supply a natal inference estimator."
            ),
            "evidence_required_before_use": [
                "participant or connected-component exchange unit",
                "frozen permutation plan",
                "matched random-width and random-state-count controls",
            ],
        },
        {
            "method_family": "selective_post_selection_inference",
            "classification": "adaptation",
            "reason": (
                "Selection invalidates ordinary inference unless accounted for or moved to a "
                "new cohort."
            ),
            "evidence_required_before_use": [
                "selection-event inventory",
                "multiplicity and post-selection analysis plan",
                "new untouched cohort after methodology changes",
            ],
        },
        {
            "method_family": "disclosure_control",
            "classification": "adaptation",
            "reason": (
                "Aggregate-only governance transfers, while the mechanism and release "
                "parameters remain open."
            ),
            "evidence_required_before_use": [
                "release-specific threat review",
                "owner decision on suppression privacy budget and cadence",
                "differencing membership and linkage tests",
            ],
        },
        {
            "method_family": "traditional_birth_time_rectification",
            "classification": "incompatible",
            "reason": (
                "Located lore lacks blinded out-of-sample evidence and cannot be encoded as "
                "truth or a prior."
            ),
            "evidence_required_before_use": [
                "independent preregistered blinded human evidence over strong ordinary baselines"
            ],
        },
        {
            "method_family": "ordinary_non_hd_prediction",
            "classification": "baseline_only",
            "reason": (
                "A future HD method must add out-of-sample value over the strongest admissible "
                "ordinary model."
            ),
            "evidence_required_before_use": [
                "same admissible inputs and tuning opportunity",
                "frozen comparator specification",
                "paired untouched validation",
            ],
        },
    ]
    payload: dict[str, Any] = {
        "schema_version": "natal-time-methods-decision-ledger-v1",
        "repository_commit": repository_commit,
        "created_at_utc": CREATED_AT.isoformat().replace("+00:00", "Z"),
        "status": "method_families_classified_no_estimator_selected",
        "allowed_classifications": [
            "direct_reuse",
            "adaptation",
            "baseline_only",
            "incompatible",
            "unresolved_experimental",
        ],
        "estimator_selected": False,
        "entries": entries,
        "evidence_basis": [
            "docs/NATAL_TIME_METHODS_SCAN_20260830.md",
            "docs/PRO_SUPERVISION_CHECKPOINT_3_20260830.md",
        ],
    }
    return _self_hash(payload, "ledger_sha256")


def build_unresolved_decision_register(repository_commit: str) -> dict[str, Any]:
    """Return choices that this slice deliberately leaves open."""

    decisions = [
        (
            "UDR-001",
            "inferential_target_and_method_family",
            "Scientific target and estimator selection changes what a recovery claim means.",
            ["falsification plan", "feasible role-separated sample", "Pro review"],
        ),
        (
            "UDR-002",
            "coverage_width_abstention_operating_point",
            "No frontier point is scientifically or product-neutral.",
            ["untouched frontier estimates", "loss and consequence analysis", "owner choice"],
        ),
        (
            "UDR-003",
            "human_cohort_size_burden_and_cost",
            "Synthetic precision grids do not authorize recruitment or expenditure.",
            ["recruitment feasibility", "attrition assumptions", "owner budget and burden choice"],
        ),
        (
            "UDR-004",
            "questionnaire_and_measurement_content",
            "No questions, choices, keys, or chart-linked interpretations are authorized.",
            ["new Pro checkpoint", "blinded item-development protocol", "reliability plan"],
        ),
        (
            "UDR-005",
            "candidate_ranking_pruning_or_exclusion",
            "Candidate-complete deterministic output has no authorized ordering semantics.",
            ["validated target", "strong-baseline comparison", "owner and Pro authorization"],
        ),
        (
            "UDR-006",
            "probabilistic_or_calibration_language",
            (
                "Ranks, widths, duration fractions, and support values are not calibrated "
                "probabilities."
            ),
            ["frozen method", "independent calibration cohort", "calibration diagnostics"],
        ),
        (
            "UDR-007",
            "subgroup_and_source_quality_analysis",
            "Definitions and multiplicity choices are adaptive and small cells may be unsafe.",
            ["development-only definition", "precision review", "disclosure review"],
        ),
        (
            "UDR-008",
            "public_ledger_suppression_privacy_budget_and_release_cadence",
            (
                "Disclosure risk depends on the actual cohort, releases, auxiliary data, "
                "and corrections."
            ),
            ["release-specific threat model", "membership and differencing tests", "owner choice"],
        ),
        (
            "UDR-009",
            "withdrawal_deletion_and_versioned_correction_policy",
            "Corrections must not create public personal linkage or repeated-release leakage.",
            ["retention obligations", "append-versus-replace analysis", "owner policy choice"],
        ),
        (
            "UDR-010",
            "public_ledger_deployment",
            "This slice designs a release-disabled synthetic aggregate schema only.",
            ["completed disclosure review", "approved release policy", "owner authorization"],
        ),
        (
            "UDR-011",
            "repository_push_merge_migration_or_deployment",
            "Local implementation authority does not authorize external state changes.",
            ["owner authorization"],
        ),
        (
            "UDR-012",
            "participant_facing_use_case_and_output",
            (
                "A participant-facing use case changes product purpose, claim exposure, safety, "
                "and the consequences of unresolved or abstaining output."
            ),
            [
                "explicit owner choice",
                "new Pro checkpoint",
                "participant-safety and claims review",
            ],
        ),
    ]
    entries = [
        {
            "decision_id": decision_id,
            "decision": decision,
            "status": "unresolved",
            "selected_value": None,
            "why_unresolved": why,
            "evidence_or_authority_required": requirements,
            "implementation_blocked": True,
        }
        for decision_id, decision, why, requirements in decisions
    ]
    payload: dict[str, Any] = {
        "schema_version": "natal-time-unresolved-decision-register-v1",
        "repository_commit": repository_commit,
        "created_at_utc": CREATED_AT.isoformat().replace("+00:00", "Z"),
        "owner_decision_required_now": False,
        "status": "preinference_slice_can_continue_without_resolving_these_choices",
        "decisions": entries,
    }
    return _self_hash(payload, "register_sha256")


BUILDERS: dict[str, Callable[[str], dict[str, Any]]] = {
    "feasibility": build_feasibility_report,
    "public-ledger-schema": build_public_ledger_schema,
    "methods-ledger": build_methods_decision_ledger,
    "unresolved-decisions": build_unresolved_decision_register,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-kind", choices=tuple(BUILDERS), default="feasibility")
    parser.add_argument("--repository-commit", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = canonical_json_bytes(BUILDERS[args.artifact_kind](args.repository_commit)) + b"\n"
    if args.output is None:
        print(encoded.decode(), end="")
    else:
        write_new_bytes(args.output, encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
