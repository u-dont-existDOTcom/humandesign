"""Build the checkpoint-5 machine-readable acceptance matrix.

The matrix is a post-custody evidence index.  It reads only committed Git
objects from an exact source commit and deliberately excludes hidden-reference
bytes, canonical ``T_i`` digests, direct per-fixture reference-custody digests,
and reference paths. Finalization fails closed until the separated custody
bundle and all of its receipts are committed.
"""

# The normalized requirement catalog intentionally keeps each source summary
# as one auditable string literal.
# ruff: noqa: E501

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.util import canonical_json_bytes, sha256_json

PROJECT_ROOT = Path(__file__).parents[1]
OUTPUT_PATH = Path("state/NATAL-TIME-CHECKPOINT5-ACCEPTANCE-MATRIX.json")
BUNDLE_ROOT = Path("state/NATAL-TIME-SYNTHETIC-EVALUATION-V1")
INFERENCE_SCHEMA_PATH = BUNDLE_ROOT / "inference/schema.json"
EVALUATOR_SCHEMA_PATH = BUNDLE_ROOT / "evaluator/schema.json"
INFERENCE_MANIFEST_PATH = BUNDLE_ROOT / "inference/manifest.json"
EVALUATOR_MANIFEST_PATH = BUNDLE_ROOT / "evaluator/manifest.json"
EVALUATION_MANIFEST_PATH = BUNDLE_ROOT / "evaluation-manifest.json"

CONTRACT_PATHS = {
    "v1": Path("state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json"),
    "v2": Path("state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V2.json"),
    "v3": Path("state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V3.json"),
}
EXPECTED_CONTRACT_DIGESTS = {
    "v1": "c721dcdd5ed9e144ca4795523420e226bc13dc8a739669991c365c1bb4d3f6c9",
    "v2": "067417a49c158fd7d7d1d31c3b21a584c1d1259aa85d60a30e9a6d3f39976f5e",
    "v3": "75a1629203724715054e2a1d7ea1b6ead7dc0ffd6cf5f4df2756c3e622b5f1fe",
}
CHECKPOINT_PATHS = {
    checkpoint: Path(f"docs/PRO_SUPERVISION_CHECKPOINT_{checkpoint}_20260830.md")
    for checkpoint in range(1, 6)
}

FOUNDATION_TEST = Path("tests/unit/test_natal_time_foundation.py")
CONFORMANCE_TEST = Path("tests/unit/test_natal_time_real_engine_conformance.py")
EVIDENCE_TEST = Path("tests/unit/test_audit_natal_time_evidence_matrix_runner.py")
DESIGN_TEST = Path("tests/unit/test_natal_time_preinference_design_contract.py")
FEASIBILITY_TEST = Path("tests/unit/test_natal_time_preinference_feasibility_and_disclosure.py")
PHASE0_TEST = Path("tests/unit/test_natal_time_checkpoint4_phase0.py")
RESUME_TEST = Path("tests/integration/test_natal_time_replay_interruption.py")
METRIC_V2_TEST = Path("tests/unit/test_natal_time_metric_semantics_contract_v2.py")
METRIC_V3_TEST = Path("tests/unit/test_natal_time_metric_semantics_contract_v3.py")
EVALUATOR_TEST = Path("tests/unit/test_natal_time_synthetic_evaluation_contract.py")
REPLAY_DELTA_TEST = Path("tests/unit/test_natal_time_checkpoint5_replay_delta.py")
OPERATIONAL_TEST = Path("tests/unit/test_natal_time_checkpoint4_operational_evidence.py")

DIMENSIONS = (
    "schema",
    "access_order",
    "metric_semantics",
    "provenance",
    "privacy",
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


class AcceptanceMatrixError(ValueError):
    """Raised when checkpoint-5 acceptance evidence is incomplete or invalid."""


@dataclass(frozen=True, slots=True)
class RequirementSpec:
    requirement_id: str
    checkpoint: int
    section: str
    ordinal: str
    requirement: str
    domain: str
    dimensions: tuple[str, ...]
    test_path: Path
    test_name: str
    artifact_path: Path
    fixture_ids: tuple[str, ...] = ()
    expected_receipt_kind: str | None = None
    expected_code: str | None = None
    invariants: tuple[str, ...] = ()
    contract_versions: tuple[str, ...] = ()
    code_bindings: tuple[tuple[Path, tuple[str, ...]], ...] = ()
    pro_minimum: bool = False


def _r(
    requirement_id: str,
    checkpoint: int,
    section: str,
    ordinal: str,
    requirement: str,
    domain: str,
    dimensions: tuple[str, ...],
    test_path: Path,
    test_name: str,
    artifact_path: Path,
    *,
    fixture_ids: tuple[str, ...] = (),
    expected_receipt_kind: str | None = None,
    expected_code: str | None = None,
    invariants: tuple[str, ...] = (),
    contract_versions: tuple[str, ...] = (),
    code_bindings: tuple[tuple[Path, tuple[str, ...]], ...] = (),
    pro_minimum: bool = False,
) -> RequirementSpec:
    return RequirementSpec(
        requirement_id,
        checkpoint,
        section,
        ordinal,
        requirement,
        domain,
        dimensions,
        test_path,
        test_name,
        artifact_path,
        fixture_ids,
        expected_receipt_kind,
        expected_code,
        invariants,
        contract_versions,
        code_bindings,
        pro_minimum,
    )


FOUNDATION_CODE = (
    (Path("src/hdmatch/natal_time/evidence.py"), ()),
    (Path("src/hdmatch/natal_time/enumerator.py"), ()),
    (Path("src/hdmatch/natal_time/records.py"), ()),
)
EVALUATOR_CODE = (
    (
        Path("src/hdmatch/natal_time/evaluation_contract.py"),
        ("verify_separated_synthetic_fixture", "verify_receipt"),
    ),
    (Path("scripts/build_natal_time_synthetic_evaluation_verifier.py"), ("build_bundle",)),
)


REQUIREMENTS: tuple[RequirementSpec, ...] = (
    # Checkpoint 1: foundation rule families.
    _r(
        "CP1-EVIDENCE-LINEAGE",
        1,
        "Evidence-state contract",
        "1",
        "Evidence records preserve source, entry, supplementation, and immutable supersession lineage.",
        "evidence_state",
        ("schema", "provenance"),
        FOUNDATION_TEST,
        "test_server_correction_appends_lineage_and_never_overwrites_evidence",
        Path("state/NATAL-TIME-EVIDENCE-TRANSITION-MATRIX.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-WEEKDAY-LOCK",
        1,
        "Evidence-state contract",
        "2",
        "Remembered weekday is server-locked before any date-implied weekday reveal.",
        "access_order",
        ("access_order", "privacy"),
        FOUNDATION_TEST,
        "test_api_locks_weekday_before_any_implied_weekday_reveal",
        Path("state/NATAL-TIME-WEEKDAY-LOCK-TRACE.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-EVIDENCE-TRANSITIONS",
        1,
        "Evidence-state contract",
        "3",
        "Every documentary, memory, conflict, candidate-set, and supersession transition is controlled.",
        "evidence_state",
        ("schema", "provenance"),
        EVIDENCE_TEST,
        "test_evidence_matrix_is_complete_synthetic_and_self_hashing",
        Path("state/NATAL-TIME-EVIDENCE-TRANSITION-MATRIX.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-CANDIDATE-DATE-CONFIRMATION",
        1,
        "Evidence-state contract",
        "4",
        "An explicit candidate-date set is fully confirmed, unordered, and retains the original declared date.",
        "evidence_state",
        ("schema", "metric_semantics"),
        FOUNDATION_TEST,
        "test_memory_conflict_requires_explicit_unordered_set_containing_original_date",
        Path("state/NATAL-TIME-EVIDENCE-TRANSITION-MATRIX.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-RELATIONSHIP-SEPARATION",
        1,
        "Evidence-state contract",
        "5",
        "Natal-time schemas reject relationship fields and client-asserted independence.",
        "schema_closure",
        ("schema", "privacy"),
        FOUNDATION_TEST,
        "test_api_rejects_relationship_or_client_independence_fields",
        Path("state/NATAL-TIME-FOUNDATION-AUDIT.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-CIVIL-DAY-DOMAIN",
        1,
        "Candidate-complete interval contract",
        "1",
        "The instant domain covers ordinary, leap, DST, historical-offset, and nonexistent civil dates exactly.",
        "candidate_domain",
        ("metric_semantics", "provenance"),
        FOUNDATION_TEST,
        "test_civil_date_domain_handles_leap_dst_and_historical_offsets",
        Path("state/NATAL-TIME-REAL-ENGINE-FIXTURES.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-INTERVAL-COVERAGE",
        1,
        "Candidate-complete interval contract",
        "2",
        "Candidate intervals form a complete maximal gap-free non-overlapping half-open partition.",
        "interval_construction",
        ("metric_semantics", "provenance"),
        FOUNDATION_TEST,
        "test_enumerator_produces_complete_maximal_unranked_receipt",
        Path("state/NATAL-TIME-REAL-ENGINE-FIXTURES.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-FULL-STATE-IDENTITY",
        1,
        "Candidate-complete interval contract",
        "3",
        "Full state identity includes every eligible discrete field and never collapses to a reduced signature.",
        "identity",
        ("schema", "provenance"),
        FOUNDATION_TEST,
        "test_same_reduced_signature_does_not_collapse_different_full_states",
        Path("state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-SET-FACTS-ONLY",
        1,
        "Candidate-complete interval contract",
        "4",
        "Results expose only deterministic stable/variable set facts and use duration only for coverage accounting.",
        "result_semantics",
        ("schema", "metric_semantics"),
        FOUNDATION_TEST,
        "test_enumerator_produces_complete_maximal_unranked_receipt",
        Path("state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json"),
        contract_versions=("v1",),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-PROVENANCE-PINNING",
        1,
        "Provenance and immutable records",
        "1",
        "Engine, dependency, runtime, ephemeris, timezone, canonicalizer, enumerator, resolution, and identity provenance are pinned.",
        "provenance",
        ("provenance",),
        FOUNDATION_TEST,
        "test_runtime_provenance_mismatch_fails_closed",
        Path("state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-IMMUTABLE-OBJECTS",
        1,
        "Provenance and immutable records",
        "2",
        "Manifest, freeze, and result are content-bound and scientific records cannot be overwritten in place.",
        "immutability",
        ("schema", "provenance"),
        FOUNDATION_TEST,
        "test_manifest_freeze_result_are_content_bound_and_extra_fields_are_rejected",
        Path("state/NATAL-TIME-FOUNDATION-AUDIT.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-FORBIDDEN-INFERENCE",
        1,
        "Provenance and immutable records",
        "3",
        "Schemas fail closed on rank, score, weight, probability, confidence, duration mass, recommendation, and relationship semantics.",
        "schema_closure",
        ("schema", "metric_semantics", "privacy"),
        DESIGN_TEST,
        "test_every_forbidden_semantic_is_fail_closed",
        Path("state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json"),
        contract_versions=("v1",),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-PUBLIC-ALLOWLIST",
        1,
        "Public-safe boundary",
        "1",
        "Public serialization is synthetic-only, allowlisted, and excludes private participant values.",
        "privacy",
        ("schema", "privacy"),
        FOUNDATION_TEST,
        "test_public_serializer_is_allowlisted_synthetic_only_and_contains_no_private_values",
        Path("state/NATAL-TIME-PUBLIC-LEDGER-SYNTHETIC-SCHEMA.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    _r(
        "CP1-PRIVACY-GATE",
        1,
        "Privacy and operations",
        "1",
        "Repository, build, history, secret, private-canary, and log-redaction privacy gates remain required.",
        "privacy",
        ("privacy", "provenance"),
        FOUNDATION_TEST,
        "test_public_serializer_is_allowlisted_synthetic_only_and_contains_no_private_values",
        Path("state/NATAL-TIME-FOUNDATION-AUDIT.json"),
        code_bindings=FOUNDATION_CODE,
    ),
    # Checkpoint 2: real-engine and evidence closure.
    _r(
        "CP2-CANONICAL-ENGINE",
        2,
        "Required real-engine identity packet",
        "1",
        "One fail-closed canonical chart engine and its exact local ephemeris identity are pinned.",
        "engine_identity",
        ("provenance",),
        CONFORMANCE_TEST,
        "test_field_inventory_covers_every_canonical_runtime_dataclass_field",
        Path("state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json"),
        code_bindings=((Path("src/hdmatch/runtime/chart_adapter.py"), ("ExactChartAdapter",)),),
    ),
    _r(
        "CP2-FIELD-INVENTORY",
        2,
        "Required real-engine identity packet",
        "2",
        "Every emitted or derivable engine field has an explicit identity, coordinate, diagnostic, provenance, unavailable, or excluded classification.",
        "engine_identity",
        ("schema", "provenance"),
        CONFORMANCE_TEST,
        "test_field_inventory_covers_every_canonical_runtime_dataclass_field",
        Path("state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json"),
    ),
    _r(
        "CP2-PRECISION-BOUNDARY",
        2,
        "Required real-engine identity packet",
        "3",
        "Exactness is bounded by demonstrated engine precision and does not make a scientific microsecond claim.",
        "precision",
        ("metric_semantics", "provenance"),
        CONFORMANCE_TEST,
        "test_actual_swiss_temporal_grid_is_measured_without_microsecond_claim",
        Path("state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json"),
    ),
    _r(
        "CP2-TRANSITION-EXHAUSTIVENESS",
        2,
        "Authorized bounded slice",
        "5",
        "Transition candidates cover direct, retrograde, repeated, stationary, design-side, near-coincident, and day-edge changes.",
        "interval_construction",
        ("metric_semantics", "provenance"),
        CONFORMANCE_TEST,
        "test_independent_design_transition_matches_production_on_engine_grid",
        Path("state/NATAL-TIME-REAL-ENGINE-FIXTURES.json"),
        code_bindings=(
            (Path("src/hdmatch/chart/boundaries.py"), ("build_chart_state_intervals",)),
        ),
    ),
    _r(
        "CP2-REAL-ENGINE-FIXTURES",
        2,
        "Authorized bounded slice",
        "6",
        "The real-engine fixture set covers every required civil-day and state-collision family.",
        "fixture_coverage",
        ("schema", "provenance"),
        CONFORMANCE_TEST,
        "test_independent_design_transition_matches_production_on_engine_grid",
        Path("state/NATAL-TIME-REAL-ENGINE-FIXTURES.json"),
    ),
    _r(
        "CP2-INDEPENDENT-CONFORMANCE",
        2,
        "Authorized bounded slice",
        "7",
        "An independent implementation verifies real-engine transition construction.",
        "independent_verification",
        ("provenance", "metric_semantics"),
        CONFORMANCE_TEST,
        "test_independent_design_transition_matches_production_on_engine_grid",
        Path("state/NATAL-TIME-REAL-ENGINE-FIXTURES.json"),
        code_bindings=(
            (
                Path("src/hdmatch/natal_time/conformance.py"),
                ("independently_enumerate_line_transitions",),
            ),
        ),
    ),
    _r(
        "CP2-EVIDENCE-MATRIX",
        2,
        "Required evidence-state matrix",
        "1",
        "The machine matrix covers all required evidence transitions, lineage mutations, omission, and relationship injection.",
        "evidence_state",
        ("schema", "provenance", "privacy"),
        EVIDENCE_TEST,
        "test_evidence_matrix_is_complete_synthetic_and_self_hashing",
        Path("state/NATAL-TIME-EVIDENCE-TRANSITION-MATRIX.json"),
    ),
    _r(
        "CP2-METHODS-SCAN",
        2,
        "Literature-scan boundary",
        "1",
        "Methods are classified as reusable, adaptable, incompatible, unresolved, or baseline-only without selecting an estimator or operating point.",
        "methods",
        ("metric_semantics", "provenance"),
        FEASIBILITY_TEST,
        "test_methods_ledger_covers_required_families_without_estimator_choice",
        Path("state/NATAL-TIME-METHODS-DECISION-LEDGER.json"),
    ),
    # Checkpoint 3: pre-inference design and replay rule families.
    _r(
        "CP3-REPLAY-HARDENING",
        3,
        "Aggregate replay ruling",
        "1-9",
        "Replay is fixture-granular, resumable, exact-source-bound, independently verified, aggregate-only, and fail closed on every invalid receipt class.",
        "replay",
        ("provenance",),
        RESUME_TEST,
        "test_aggregate_rejects_invalid_or_incomplete_receipt_sets",
        Path("state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/index.json"),
        code_bindings=(
            (Path("src/hdmatch/natal_time/replay.py"), ("run_replay", "build_aggregate_index")),
        ),
    ),
    _r(
        "CP3-C-T-S-SEPARATION",
        3,
        "Evaluation unit and reference standard",
        "1",
        "C_i, hidden documentary T_i, and future returned S_i remain distinct frozen objects.",
        "study_design",
        ("schema", "access_order", "metric_semantics"),
        DESIGN_TEST,
        "test_formal_objects_preserve_complete_candidates_hidden_reference_and_set_output",
        Path("state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json"),
        contract_versions=("v1",),
    ),
    _r(
        "CP3-REFERENCE-PRECISION",
        3,
        "Evaluation unit and reference standard",
        "2",
        "Documentary precision remains an interval and memory-only time is not accuracy ground truth.",
        "reference_standard",
        ("schema", "metric_semantics"),
        DESIGN_TEST,
        "test_documentary_reference_eligibility_preserves_coarse_precision",
        Path("state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json"),
        contract_versions=("v1",),
    ),
    _r(
        "CP3-NONSCALAR-ESTIMAND",
        3,
        "Non-scalar estimand",
        "1",
        "Coverage, temporal width, interval count, unique-state count, date coverage, reference width, and abstention stay separate.",
        "metric_semantics",
        ("schema", "metric_semantics"),
        DESIGN_TEST,
        "test_estimand_keeps_coverage_width_state_count_date_and_abstention_separate",
        Path("state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json"),
        contract_versions=("v1",),
    ),
    _r(
        "CP3-BASELINES",
        3,
        "Required baselines",
        "1",
        "All required null, falsification, random-matched, ordinary non-HD, and label-permutation baselines are preregistered but not executed.",
        "baselines",
        ("schema", "metric_semantics"),
        DESIGN_TEST,
        "test_baseline_falsification_matrix_is_complete_and_keeps_random_controls_distinct",
        Path("state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json"),
        contract_versions=("v1",),
    ),
    _r(
        "CP3-ROLE-ISOLATION",
        3,
        "Data roles and leakage",
        "1",
        "Development, calibration, and validation are disjoint by participant and connected component, and contamination fails closed.",
        "leakage",
        ("access_order", "privacy", "provenance"),
        DESIGN_TEST,
        "test_connected_component_rules_cover_identity_relationship_household_and_source",
        Path("state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json"),
        contract_versions=("v1",),
    ),
    _r(
        "CP3-MEASUREMENT-REQUIREMENTS",
        3,
        "Measurement-development requirements",
        "1",
        "Measurement controls are complete while questions, choices, keys, and interpretations remain absent.",
        "measurement",
        ("schema", "privacy"),
        DESIGN_TEST,
        "test_measurement_requirements_are_controls_only_and_prove_zero_item_content",
        Path("state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json"),
        contract_versions=("v1",),
    ),
    _r(
        "CP3-FEASIBILITY",
        3,
        "Feasibility analysis",
        "1",
        "Feasibility calculations are reproducible and hypothetical without choosing sample size, effect, cost, or recruitment.",
        "feasibility",
        ("metric_semantics", "provenance"),
        FEASIBILITY_TEST,
        "test_feasibility_report_is_synthetic_nonselecting_and_complete",
        Path("state/NATAL-TIME-PREINFERENCE-FEASIBILITY.json"),
    ),
    _r(
        "CP3-DISCLOSURE-LEDGER",
        3,
        "Aggregate public-ledger threat model",
        "1",
        "The aggregate schema remains release-disabled and covers linkage, membership, differencing, sparse cells, deletion, and correction threats.",
        "privacy",
        ("schema", "privacy"),
        FEASIBILITY_TEST,
        "test_public_ledger_schema_is_release_disabled_and_aggregate_only",
        Path("state/NATAL-TIME-PUBLIC-LEDGER-SYNTHETIC-SCHEMA.json"),
    ),
    _r(
        "CP3-METHOD-LEDGER",
        3,
        "Methods decision ledger",
        "1",
        "Every required method family has a controlled disposition without selecting an estimator.",
        "methods",
        ("metric_semantics", "provenance"),
        DESIGN_TEST,
        "test_method_ledger_is_complete_without_selecting_an_estimator",
        Path("state/NATAL-TIME-METHODS-DECISION-LEDGER.json"),
        contract_versions=("v1",),
    ),
    _r(
        "CP3-UNRESOLVED-REGISTER",
        3,
        "Checkpoint 4 package",
        "1",
        "Unresolved choices remain explicit and do not silently select an operating point or owner decision.",
        "governance",
        ("schema", "provenance"),
        FEASIBILITY_TEST,
        "test_unresolved_register_selects_nothing_and_preserves_owner_boundaries",
        Path("state/NATAL-TIME-UNRESOLVED-DECISIONS.json"),
    ),
    # Checkpoint 4: closure and executable evaluator rule families.
    _r(
        "CP4-LINEAGE-ATTESTATION",
        4,
        "Required correction 2.1",
        "1",
        "Reviewed, replay, operational, and evaluated commit lineage and protected-byte identity are content-attested.",
        "provenance",
        ("provenance",),
        PHASE0_TEST,
        "test_lineage_attestation_is_exact_content_hashed_and_unmerged",
        Path("state/NATAL-TIME-CHECKPOINT4-LINEAGE-ATTESTATION.json"),
    ),
    _r(
        "CP4-REPLAY-SOURCE-MANIFEST",
        4,
        "Required correction 2.2",
        "1",
        "Replay-affecting source identity and aggregate-only reproduction are fail-closed.",
        "replay",
        ("provenance",),
        PHASE0_TEST,
        "test_replay_source_manifest_is_fail_closed_and_current_aggregate_matches",
        Path("state/NATAL-TIME-REPLAY-SOURCE-MANIFEST-V1.json"),
    ),
    _r(
        "CP4-INTERRUPTION-RESUME",
        4,
        "Required correction 2.3",
        "1",
        "A deliberate interrupted run resumes without recomputing valid receipts and matches a clean run.",
        "replay",
        ("provenance",),
        RESUME_TEST,
        "test_interruption_resume_preserves_receipts_and_matches_clean_run",
        Path("state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/index.json"),
    ),
    _r(
        "CP4-METRIC-V2-EDGE-CLOSURE",
        4,
        "Required correction 2.4",
        "1",
        "Nonempty S_i, abstention, membership, canonical reference, documentary width, count separation, and no scalar summary are explicit.",
        "metric_semantics",
        ("schema", "metric_semantics"),
        METRIC_V2_TEST,
        "test_output_contract_rejects_empty_duplicate_partial_manufactured_and_foreign_members",
        Path("state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V2.json"),
        contract_versions=("v1", "v2"),
    ),
    _r(
        "CP4-ACCESS-ORDER",
        4,
        "Phase-1 acceptance tests",
        "1",
        "T_i access before frozen S_i commitment fails closed.",
        "access_order",
        ("access_order",),
        EVALUATOR_TEST,
        "test_precommit_boundary_performs_zero_reference_operations",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-EARLY-REFERENCE-ACCESS",),
        expected_receipt_kind="fail_closed_rejection",
        expected_code="t_i_access_before_s_i_commitment",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP4-POSTREFERENCE-S-MUTATION",
        4,
        "Phase-1 acceptance tests",
        "2",
        "Changing S_i after T_i exposure invalidates the component and emits no valid evaluation receipt.",
        "access_order",
        ("access_order", "provenance"),
        EVALUATOR_TEST,
        "test_full_candidate_set_has_unit_fractions_without_success_semantics",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-POST-REFERENCE-OUTPUT-MUTATION",),
        expected_receipt_kind="fail_closed_rejection",
        expected_code="s_i_modified_after_t_i_exposure",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP4-ROLE-CONTAMINATION",
        4,
        "Phase-1 acceptance tests",
        "3",
        "Cross-role connected components and contaminated components fail closed.",
        "leakage",
        ("access_order", "privacy"),
        EVALUATOR_TEST,
        "test_fixed_fixture_kinds_and_controlled_rejections",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-CROSS-ROLE-COMPONENT", "SYNTH-FIXTURE-CONTAMINATED-COMPONENT"),
        expected_receipt_kind="fail_closed_rejection",
        invariants=("controlled_violation_code_present",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP4-FULL-C",
        4,
        "Phase-1 acceptance tests",
        "4",
        "Full C_i yields unit width and count fractions without a success or inference claim.",
        "metric_semantics",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_fixed_fixture_kinds_and_controlled_rejections",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("full_c_unit_fractions", "no_inference_claim"),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
        pro_minimum=True,
    ),
    _r(
        "CP4-ABSTENTION-NA",
        4,
        "Phase-1 acceptance tests",
        "5",
        "Abstention leaves coverage and retention components typed non-applicable rather than zero.",
        "metric_semantics",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_reference_na_abstention_and_separate_metric_components",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-ABSTENTION",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("abstention_components_typed_na",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP4-EMPTY-NONABSTENTION",
        4,
        "Phase-1 acceptance tests",
        "6",
        "An empty non-abstaining S_i is rejected.",
        "metric_semantics",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_fixed_fixture_kinds_and_controlled_rejections",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-EMPTY-NON-ABSTENTION",),
        expected_receipt_kind="fail_closed_rejection",
        expected_code="invalid_output_empty_non_abstention",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP4-INVALID-INTERVAL-MEMBERSHIP",
        4,
        "Phase-1 acceptance tests",
        "7",
        "Partial, duplicate, foreign, and manufactured selected intervals fail closed.",
        "metric_semantics",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_fixed_fixture_kinds_and_controlled_rejections",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=(
            "SYNTH-FIXTURE-PARTIAL-INTERVAL",
            "SYNTH-FIXTURE-DUPLICATE-INTERVAL",
            "SYNTH-FIXTURE-FOREIGN-INTERVAL",
            "SYNTH-FIXTURE-MANUFACTURED-INTERVAL",
        ),
        expected_receipt_kind="fail_closed_rejection",
        invariants=("controlled_violation_code_present",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP4-CANONICAL-REORDER",
        4,
        "Phase-1 acceptance tests",
        "8",
        "Canonical reordering without semantic change preserves commitment and receipt bytes.",
        "canonicalization",
        ("schema", "metric_semantics", "provenance"),
        EVALUATOR_TEST,
        "test_disconnected_reordering_preserves_commitment_and_complete_receipt",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-DISCONNECTED-REORDERED",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("canonical_reorder_equivalent",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
        pro_minimum=True,
    ),
    _r(
        "CP4-BOUNDARY-ENDPOINT",
        4,
        "Phase-1 acceptance tests",
        "10",
        "Reference endpoint contact follows canonical half-open interval semantics.",
        "metric_semantics",
        ("metric_semantics",),
        EVALUATOR_TEST,
        "test_fixed_fixture_kinds_and_controlled_rejections",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-BOUNDARY-TOUCH",),
        expected_receipt_kind="descriptive_metric_receipt",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP4-REPEATED-STATE-COUNTS",
        4,
        "Phase-1 acceptance tests",
        "11",
        "Interval-count and unique-state-count fractions diverge when state identities repeat.",
        "metric_semantics",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_repeated_state_interval_and_unique_state_counts_diverge",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-REPEATED-STATE",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("interval_state_count_divergence",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
        pro_minimum=True,
    ),
    _r(
        "CP4-MULTIDATE-COVERAGE",
        4,
        "Phase-1 acceptance tests",
        "12",
        "Multiple-date coverage remains separate from retained temporal width.",
        "metric_semantics",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_fixed_fixture_kinds_and_controlled_rejections",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-MULTIPLE-DATES",),
        expected_receipt_kind="descriptive_metric_receipt",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP4-NO-PROHIBITED-OUTPUT",
        4,
        "Phase-1 acceptance tests",
        "13",
        "No receipt contains rank, best, score, weight, probability, confidence, utility, threshold, recommendation, or scalar summary semantics.",
        "schema_closure",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_reference_na_abstention_and_separate_metric_components",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("no_forbidden_semantics",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP4-NO-SELECTOR",
        4,
        "Phase-1 acceptance tests",
        "14",
        "The verifier consumes preconstructed S_i and implements no candidate selector or baseline execution.",
        "scope",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_inference_bundle_has_no_reference_address_or_dependency",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("no_inference_claim",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP4-PRIVATE-FIELD-REJECTION",
        4,
        "Phase-1 acceptance tests",
        "15",
        "Relationship, participant, birth-record, contact, consent, recovery, and free-text fields are rejected.",
        "privacy",
        ("schema", "privacy"),
        EVALUATOR_TEST,
        "test_recursive_prohibited_and_exact_membership_mutants_fail_closed",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("no_forbidden_semantics",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP4-RECEIPT-BINDINGS",
        4,
        "Phase-1 acceptance tests",
        "16",
        "Every valid receipt binds contract, inference-visible fixture, access state, and evaluator version digests.",
        "receipt_provenance",
        ("access_order", "provenance"),
        EVALUATOR_TEST,
        "test_valid_receipts_bind_s_t_custody_access_evaluator_and_v1_v2_v3",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("required_receipt_bindings",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    # Checkpoint 5: custody, subset, reference-domain, provenance, and matrix minima.
    _r(
        "CP5-T-ONLY-INVARIANCE",
        5,
        "Required correction 2.1",
        "1",
        "Changing only T_i leaves every inference-visible precommit byte and digest unchanged.",
        "custody",
        ("access_order", "privacy", "provenance"),
        EVALUATOR_TEST,
        "test_t_only_change_leaves_all_inference_visible_bytes_and_digests_unchanged",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("required_receipt_bindings",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-ZERO-PRECOMMIT-OPS",
        5,
        "Required correction 2.1",
        "2",
        "Precommit execution performs zero open, read, stat, parse, serialization, or hash operations on evaluator-only reference objects.",
        "custody",
        ("access_order", "privacy"),
        EVALUATOR_TEST,
        "test_precommit_boundary_performs_zero_reference_operations",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-EARLY-REFERENCE-ACCESS",),
        expected_receipt_kind="fail_closed_rejection",
        expected_code="t_i_access_before_s_i_commitment",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-REFERENCE-UNADDRESSABLE",
        5,
        "Required correction 2.1",
        "3",
        "The inference role cannot enumerate, fetch, list, or address evaluator reference objects.",
        "custody",
        ("schema", "access_order", "privacy"),
        EVALUATOR_TEST,
        "test_inference_bundle_has_no_reference_address_or_dependency",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("required_receipt_bindings",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-SPLIT-MANIFESTS",
        5,
        "Required correction 2.1",
        "4",
        "Inference-visible and evaluator-only bundles have separate schemas and manifests.",
        "custody",
        ("schema", "access_order", "privacy", "provenance"),
        EVALUATOR_TEST,
        "test_committed_split_bundle_matches_builder_and_hashes",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("required_receipt_bindings",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-NO-PRECOMMIT-T-DIGEST",
        5,
        "Required correction 2.1",
        "5",
        "No unkeyed T_i-dependent commitment or combined fixture digest is inference-visible before S_i commitment.",
        "custody",
        ("schema", "access_order", "privacy"),
        EVALUATOR_TEST,
        "test_inference_bundle_has_no_reference_address_or_dependency",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("inference_fixture_has_no_reference_dependency",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-EARLY-RAW-BYTE",
        5,
        "Required correction 2.1",
        "7a",
        "An early raw-byte reference access attempt fails closed.",
        "custody",
        ("access_order", "privacy"),
        EVALUATOR_TEST,
        "test_early_probe_modes_fail_without_loader_or_reference_operations",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-EARLY-REFERENCE-RAW-BYTE",),
        expected_receipt_kind="fail_closed_rejection",
        expected_code="early_reference_raw_byte_access",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-EARLY-DIGEST",
        5,
        "Required correction 2.1",
        "7b",
        "An early reference digest access attempt fails closed.",
        "custody",
        ("access_order", "privacy"),
        EVALUATOR_TEST,
        "test_early_probe_modes_fail_without_loader_or_reference_operations",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-EARLY-REFERENCE-DIGEST",),
        expected_receipt_kind="fail_closed_rejection",
        expected_code="early_reference_digest_access",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-EARLY-METADATA",
        5,
        "Required correction 2.1",
        "7c",
        "An early reference file-metadata access attempt fails closed.",
        "custody",
        ("access_order", "privacy"),
        EVALUATOR_TEST,
        "test_early_probe_modes_fail_without_loader_or_reference_operations",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-EARLY-REFERENCE-METADATA",),
        expected_receipt_kind="fail_closed_rejection",
        expected_code="early_reference_metadata_access",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-EARLY-ALTERNATE-LOADER",
        5,
        "Required correction 2.1",
        "7d",
        "An alternate-loader reference access attempt fails closed.",
        "custody",
        ("access_order", "privacy"),
        EVALUATOR_TEST,
        "test_early_probe_modes_fail_without_loader_or_reference_operations",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-EARLY-REFERENCE-ALTERNATE-LOADER",),
        expected_receipt_kind="fail_closed_rejection",
        expected_code="early_reference_alternate_loader_access",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-POSTACCESS-T-MUTATION",
        5,
        "Required correction 2.1",
        "8",
        "Changing T_i after evaluator access invalidates the reference custody chain.",
        "custody",
        ("access_order", "provenance", "privacy"),
        EVALUATOR_TEST,
        "test_post_access_t_mutation_fixture_invalidates_custody",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-POST-REFERENCE-T-MUTATION",),
        expected_receipt_kind="fail_closed_rejection",
        expected_code="t_i_mutated_after_evaluator_access",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-DISCONNECTED-SUBSET",
        5,
        "Required correction 2.2",
        "1",
        "A first-and-third disconnected same-date S_i is accepted without filling the gap.",
        "subset_semantics",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_disconnected_first_and_third_same_date_has_exact_components_and_no_gap_fill",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-DISCONNECTED-SAME-DATE",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("disconnected_subset_exact",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-DISCONNECTED-REORDER",
        5,
        "Required correction 2.2",
        "3",
        "Reordering a disconnected subset preserves its commitment and receipt.",
        "canonicalization",
        ("schema", "metric_semantics", "provenance"),
        EVALUATOR_TEST,
        "test_disconnected_reordering_preserves_commitment_and_complete_receipt",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-DISCONNECTED-REORDERED",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("canonical_reorder_equivalent",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-DISCONNECTED-DUPLICATE",
        5,
        "Required correction 2.2",
        "4",
        "Duplicating an interval in a disconnected subset is rejected.",
        "subset_semantics",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_fixed_fixture_kinds_and_controlled_rejections",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-DISCONNECTED-DUPLICATE",),
        expected_receipt_kind="fail_closed_rejection",
        expected_code="duplicate_selected_interval",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-MANUFACTURED-SPAN",
        5,
        "Required correction 2.2",
        "5",
        "A manufactured window spanning disconnected intervals is rejected.",
        "subset_semantics",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_fixed_fixture_kinds_and_controlled_rejections",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-MANUFACTURED-INTERVAL",),
        expected_receipt_kind="fail_closed_rejection",
        expected_code="manufactured_interval_not_allowed",
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-NO-CONTIGUOUS-BEST",
        5,
        "Required correction 2.2",
        "6",
        "Generic receipts contain no contiguous-window or best-window semantic.",
        "schema_closure",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_receipt_schema_is_closed_for_valid_diagnostic_and_rejection",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-DISCONNECTED-SAME-DATE",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("no_forbidden_semantics",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-REFERENCE-CONTAINED-ONE",
        5,
        "Required correction 2.3",
        "1",
        "T_i fully contained in one canonical interval is reference-domain compatible.",
        "reference_domain",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_fixed_fixture_kinds_and_controlled_rejections",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("reference_accuracy_applicable",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-REFERENCE-CONTAINED-ADJACENT",
        5,
        "Required correction 2.3",
        "2",
        "T_i fully contained across adjacent canonical intervals is reference-domain compatible.",
        "reference_domain",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_three_way_domain_union_and_diagnostic_only_artifacts",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-REFERENCE-CONTAINED-ACROSS-ADJACENT",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("reference_accuracy_applicable",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-REFERENCE-PARTIAL-BEFORE",
        5,
        "Required correction 2.3",
        "3",
        "T_i extending before D_i is partially incompatible and yields diagnostics only.",
        "reference_domain",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_three_way_domain_union_and_diagnostic_only_artifacts",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-PARTIAL-REFERENCE-ONE-MICROSECOND",),
        expected_receipt_kind="reference_domain_diagnostic",
        expected_code="reference_domain_partially_incompatible",
        invariants=("reference_accuracy_not_applicable",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-REFERENCE-PARTIAL-AFTER",
        5,
        "Required correction 2.3",
        "4",
        "T_i extending after D_i is partially incompatible and yields diagnostics only.",
        "reference_domain",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_three_way_domain_union_and_diagnostic_only_artifacts",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-REFERENCE-EXTENDS-AFTER-DOMAIN",),
        expected_receipt_kind="reference_domain_diagnostic",
        expected_code="reference_domain_partially_incompatible",
        invariants=("reference_accuracy_not_applicable",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-REFERENCE-PARTIAL-BOTH",
        5,
        "Required correction 2.3",
        "5",
        "T_i extending across both D_i ends is partially incompatible and yields diagnostics only.",
        "reference_domain",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_three_way_domain_union_and_diagnostic_only_artifacts",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-REFERENCE-EXTENDS-BOTH-DOMAIN-ENDS",),
        expected_receipt_kind="reference_domain_diagnostic",
        expected_code="reference_domain_partially_incompatible",
        invariants=("reference_accuracy_not_applicable",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-REFERENCE-OUTSIDE",
        5,
        "Required correction 2.3",
        "6",
        "T_i wholly outside D_i is incompatible and yields diagnostics only.",
        "reference_domain",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_three_way_domain_union_and_diagnostic_only_artifacts",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-DOMAIN-INCOMPATIBLE",),
        expected_receipt_kind="reference_domain_diagnostic",
        expected_code="reference_domain_incompatible",
        invariants=("reference_accuracy_not_applicable",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-REFERENCE-ENDPOINT-ONLY",
        5,
        "Required correction 2.3",
        "7",
        "Endpoint-only contact has zero width and is reference-domain incompatible.",
        "reference_domain",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_three_way_domain_union_and_diagnostic_only_artifacts",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-DOMAIN-INCOMPATIBLE",),
        expected_receipt_kind="reference_domain_diagnostic",
        expected_code="reference_domain_incompatible",
        invariants=("reference_accuracy_not_applicable",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-REFERENCE-MULTIDATE-INCLUDED",
        5,
        "Required correction 2.3",
        "8",
        "A reference on an included candidate date is compatible.",
        "reference_domain",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_three_way_domain_union_and_diagnostic_only_artifacts",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-MULTIDATE-INCLUDED-DATE",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("reference_accuracy_applicable",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-REFERENCE-MULTIDATE-EXCLUDED",
        5,
        "Required correction 2.3",
        "9",
        "A reference on an excluded date is incompatible and yields diagnostics only.",
        "reference_domain",
        ("schema", "metric_semantics"),
        EVALUATOR_TEST,
        "test_three_way_domain_union_and_diagnostic_only_artifacts",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-MULTIDATE-EXCLUDED-DATE",),
        expected_receipt_kind="reference_domain_diagnostic",
        expected_code="reference_domain_incompatible",
        invariants=("reference_accuracy_not_applicable",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
    ),
    _r(
        "CP5-REPLAY-ROUTE-A",
        5,
        "Required correction 2.4",
        "1",
        "Replay semantic inputs and receipt construction remain equivalent through the acceptance source, and all nine receipts reproduce exactly.",
        "replay",
        ("provenance",),
        REPLAY_DELTA_TEST,
        "test_acceptance_validator_reproduces_receipts_index_and_mutation_failure",
        Path("state/NATAL-TIME-CHECKPOINT5-REPLAY-DELTA-ATTESTATION.json"),
    ),
    _r(
        "CP5-ACCESS-BINDING-EVERY-VALID",
        5,
        "Required correction 2.5",
        "minimum-4",
        "Every valid evaluation receipt binds the exact access state.",
        "receipt_provenance",
        ("access_order", "provenance"),
        EVALUATOR_TEST,
        "test_every_postcommit_artifact_binds_access_state_and_evaluator",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("all_valid_receipts_bind_access",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
        pro_minimum=True,
    ),
    _r(
        "CP5-REHASHED-FORBIDDEN-FIELD",
        5,
        "Required correction 2.5",
        "minimum-5",
        "A rehash-added forbidden scalar or inferential field is rejected by the closed receipt and fixture schemas.",
        "schema_closure",
        ("schema", "metric_semantics", "privacy"),
        EVALUATOR_TEST,
        "test_rehash_added_forbidden_scalar_field_is_rejected",
        EVALUATION_MANIFEST_PATH,
        fixture_ids=("SYNTH-FIXTURE-FULL-C",),
        expected_receipt_kind="descriptive_metric_receipt",
        invariants=("closed_schema_rehash_mutation_test_bound",),
        contract_versions=("v1", "v2", "v3"),
        code_bindings=EVALUATOR_CODE,
        pro_minimum=True,
    ),
    _r(
        "CP5-OPERATING-V3",
        5,
        "Required corrections 2.2-2.3",
        "contract",
        "V3 preserves V1/V2 while removing S_i contiguity and establishing three-way reference-domain status.",
        "metric_contract",
        ("schema", "metric_semantics", "provenance"),
        METRIC_V3_TEST,
        "test_v3_is_the_operating_reference_without_overwriting_v1_or_v2",
        Path("state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V3.json"),
        contract_versions=("v1", "v2", "v3"),
    ),
    _r(
        "CP5-OPERATIONAL-EVIDENCE",
        5,
        "Non-blocking improvements",
        "1-4",
        "Replay timing remains explicitly operational, lint scope is Git-derived, legacy debt is separate, and release-disabled artifacts make no anonymity claim.",
        "operational_evidence",
        ("provenance", "privacy"),
        OPERATIONAL_TEST,
        "test_lint_scopes_are_git_derived_and_legacy_debt_is_separate",
        Path("state/NATAL-TIME-CHECKPOINT4-OPERATIONAL-EVIDENCE.json"),
    ),
)

PRO_MINIMUM_IDS = frozenset(spec.requirement_id for spec in REQUIREMENTS if spec.pro_minimum)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AcceptanceMatrixError(message)


def _git(root: Path, arguments: Sequence[str]) -> bytes:
    result = subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True)
    return result.stdout


def _git_text(root: Path, arguments: Sequence[str]) -> str:
    return _git(root, arguments).decode("utf-8").strip()


def _resolve_commit(root: Path, source_commit: str | None) -> str:
    resolved = _git_text(root, ["rev-parse", source_commit or "HEAD"])
    _require(COMMIT_RE.fullmatch(resolved) is not None, "source commit is not a full Git OID")
    return resolved


def _git_file(root: Path, commit: str, path: Path) -> bytes:
    try:
        return _git(root, ["show", f"{commit}:{path.as_posix()}"])
    except subprocess.CalledProcessError as exc:
        raise AcceptanceMatrixError(
            f"required committed custody/evidence file is missing: {path.as_posix()}"
        ) from exc


def _blob_oid(root: Path, commit: str, path: Path) -> str:
    oid = _git_text(root, ["rev-parse", f"{commit}:{path.as_posix()}"])
    _require(re.fullmatch(r"[0-9a-f]{40,64}", oid) is not None, f"invalid blob OID: {path}")
    return oid


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _load_json_bytes(value: bytes, label: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise AcceptanceMatrixError(f"invalid JSON object: {label}") from exc
    _require(isinstance(parsed, dict), f"JSON value is not an object: {label}")
    return cast(dict[str, Any], parsed)


def _git_json(root: Path, commit: str, path: Path) -> dict[str, Any]:
    return _load_json_bytes(_git_file(root, commit, path), path.as_posix())


def _verify_self_hash(value: Mapping[str, Any], field: str, label: str) -> str:
    payload = dict(value)
    embedded = payload.pop(field, None)
    _require(isinstance(embedded, str), f"missing {field}: {label}")
    _require(SHA256_RE.fullmatch(embedded) is not None, f"malformed {field}: {label}")
    _require(sha256_json(payload) == embedded, f"self-hash mismatch: {label}")
    return cast(str, embedded)


def _test_functions(source: bytes, path: Path) -> frozenset[str]:
    try:
        tree = ast.parse(source, filename=path.as_posix())
    except SyntaxError as exc:
        raise AcceptanceMatrixError(f"invalid committed Python source: {path}") from exc
    return frozenset(
        node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    )


def _verify_symbols(source: bytes, path: Path, symbols: Sequence[str]) -> None:
    if not symbols:
        return
    names = _test_functions(source, path)
    tree = ast.parse(source, filename=path.as_posix())
    names |= frozenset(node.name for node in tree.body if isinstance(node, ast.ClassDef))
    missing = sorted(set(symbols) - names)
    _require(not missing, f"committed code binding is missing symbols {missing}: {path}")


def _load_contract_catalog(root: Path, commit: str) -> dict[str, dict[str, str]]:
    catalog: dict[str, dict[str, str]] = {}
    for version, path in CONTRACT_PATHS.items():
        raw = _git_file(root, commit, path)
        contract = _load_json_bytes(raw, path.as_posix())
        digest = _verify_self_hash(contract, "contract_sha256", path.as_posix())
        _require(digest == EXPECTED_CONTRACT_DIGESTS[version], f"{version} digest changed")
        catalog[version] = {
            "path": path.as_posix(),
            "schema_version": cast(str, contract["schema_version"]),
            "contract_sha256": digest,
            "file_sha256": _sha256_bytes(raw),
            "git_blob_oid": _blob_oid(root, commit, path),
        }
    return catalog


@dataclass(frozen=True, slots=True)
class BundleEvidence:
    inference_schema: dict[str, Any]
    evaluator_schema: dict[str, Any]
    inference_manifest: dict[str, Any]
    evaluator_manifest: dict[str, Any]
    evaluation_manifest: dict[str, Any]
    inference_entries: dict[str, dict[str, Any]]
    evaluation_entries: dict[str, dict[str, Any]]
    receipts: dict[str, dict[str, Any]]
    fixtures: dict[str, dict[str, Any]]


def _indexed_entries(value: Mapping[str, Any], label: str) -> dict[str, dict[str, Any]]:
    entries = value.get("entries")
    _require(isinstance(entries, list), f"manifest entries are absent: {label}")
    entry_list = cast(list[Any], entries)
    result: dict[str, dict[str, Any]] = {}
    for raw in entry_list:
        _require(isinstance(raw, dict), f"manifest entry is not an object: {label}")
        item = cast(dict[str, Any], raw)
        fixture_id = item.get("fixture_id")
        _require(isinstance(fixture_id, str), f"manifest fixture_id is absent: {label}")
        fixture_id_string = cast(str, fixture_id)
        _require(
            fixture_id_string not in result,
            f"duplicate manifest fixture_id: {fixture_id_string}",
        )
        result[fixture_id_string] = item
    return result


def _load_bundle(root: Path, commit: str) -> BundleEvidence:
    inference_schema = _git_json(root, commit, INFERENCE_SCHEMA_PATH)
    evaluator_schema = _git_json(root, commit, EVALUATOR_SCHEMA_PATH)
    inference_manifest = _git_json(root, commit, INFERENCE_MANIFEST_PATH)
    evaluator_manifest = _git_json(root, commit, EVALUATOR_MANIFEST_PATH)
    evaluation_manifest = _git_json(root, commit, EVALUATION_MANIFEST_PATH)
    for value, field, label in (
        (inference_schema, "schema_sha256", INFERENCE_SCHEMA_PATH.as_posix()),
        (evaluator_schema, "schema_sha256", EVALUATOR_SCHEMA_PATH.as_posix()),
        (inference_manifest, "manifest_sha256", INFERENCE_MANIFEST_PATH.as_posix()),
        (evaluator_manifest, "manifest_sha256", EVALUATOR_MANIFEST_PATH.as_posix()),
        (evaluation_manifest, "manifest_sha256", EVALUATION_MANIFEST_PATH.as_posix()),
    ):
        _verify_self_hash(value, field, label)
    inference_surface = json.dumps(
        {"schema": inference_schema, "manifest": inference_manifest},
        sort_keys=True,
    )
    for forbidden in (
        '"evaluator_version"',
        '"source_files"',
        '"reference_path"',
        '"reference_custody_sha256"',
        '"canonical_t_i_sha256"',
        '"custody_id"',
    ):
        _require(
            forbidden not in inference_surface,
            f"inference-visible bundle contains evaluator/reference dependency: {forbidden}",
        )

    inference_entries = _indexed_entries(inference_manifest, "inference")
    evaluator_entries = _indexed_entries(evaluator_manifest, "evaluator")
    evaluation_entries = _indexed_entries(evaluation_manifest, "evaluation")
    _require(
        set(inference_entries) == set(evaluator_entries) == set(evaluation_entries),
        "split custody manifests have different fixture sets",
    )
    declared_count = evaluation_manifest.get("receipt_count")
    _require(declared_count == len(evaluation_entries), "evaluation receipt count mismatch")

    receipts: dict[str, dict[str, Any]] = {}
    fixtures: dict[str, dict[str, Any]] = {}
    for fixture_id in sorted(evaluation_entries):
        inference_entry = inference_entries[fixture_id]
        evaluator_entry = evaluator_entries[fixture_id]
        evaluation_entry = evaluation_entries[fixture_id]
        fixture_path = Path(cast(str, inference_entry["fixture_path"]))
        reference_path = Path(cast(str, evaluator_entry["reference_path"]))
        receipt_path = Path(cast(str, evaluation_entry["receipt_path"]))
        fixture_raw = _git_file(root, commit, fixture_path)
        reference_raw = _git_file(root, commit, reference_path)
        receipt_raw = _git_file(root, commit, receipt_path)
        fixture = _load_json_bytes(fixture_raw, fixture_path.as_posix())
        reference = _load_json_bytes(reference_raw, reference_path.as_posix())
        receipt = _load_json_bytes(receipt_raw, receipt_path.as_posix())
        fixture_digest = fixture.get("inference_visible_fixture_digest")
        _require(
            fixture_digest == inference_entry.get("inference_visible_fixture_digest"),
            f"fixture digest manifest mismatch: {fixture_id}",
        )
        _require(
            _sha256_bytes(fixture_raw) == inference_entry.get("fixture_file_sha256"),
            f"fixture file digest mismatch: {fixture_id}",
        )
        reference_digest = _verify_self_hash(
            reference,
            "reference_custody_sha256",
            reference_path.as_posix(),
        )
        _require(
            reference_digest == evaluator_entry.get("reference_custody_sha256"),
            f"reference custody manifest mismatch: {fixture_id}",
        )
        _require(
            _sha256_bytes(reference_raw) == evaluator_entry.get("reference_file_sha256"),
            f"reference custody file digest mismatch: {fixture_id}",
        )
        _require(
            fixture_digest == evaluator_entry.get("inference_visible_fixture_digest"),
            f"evaluator fixture binding mismatch: {fixture_id}",
        )
        receipt_digest = _verify_self_hash(receipt, "receipt_sha256", fixture_id)
        _require(
            receipt_digest == evaluation_entry.get("receipt_sha256"),
            f"receipt digest manifest mismatch: {fixture_id}",
        )
        _require(
            _sha256_bytes(receipt_raw) == evaluation_entry.get("receipt_file_sha256"),
            f"receipt file digest mismatch: {fixture_id}",
        )
        _require(
            fixture_digest == evaluation_entry.get("inference_visible_fixture_digest"),
            f"evaluation fixture binding mismatch: {fixture_id}",
        )
        _require(
            receipt.get("evaluator_version_sha256")
            == evaluation_manifest.get("evaluator_version_sha256"),
            f"receipt evaluator binding mismatch: {fixture_id}",
        )
        _require(
            receipt.get("inference_visible_fixture_digest") == fixture_digest,
            f"receipt inference binding mismatch: {fixture_id}",
        )
        expected_contract_bindings = {
            "preserved_v1_contract_sha256": EXPECTED_CONTRACT_DIGESTS["v1"],
            "preserved_v2_contract_sha256": EXPECTED_CONTRACT_DIGESTS["v2"],
            "operative_v3_contract_sha256": EXPECTED_CONTRACT_DIGESTS["v3"],
        }
        _require(
            receipt.get("contract_bindings") == expected_contract_bindings,
            f"receipt contract binding mismatch: {fixture_id}",
        )
        if receipt.get("receipt_kind") != "fail_closed_rejection":
            _require(
                receipt.get("reference_custody_sha256") == reference_digest,
                f"receipt custody binding mismatch: {fixture_id}",
            )
            output = fixture.get("preconstructed_output")
            _require(isinstance(output, dict), f"fixture output is absent: {fixture_id}")
            output_payload = dict(cast(dict[str, Any], output))
            selected = output_payload.get("selected_intervals")
            _require(isinstance(selected, list), f"fixture selection is absent: {fixture_id}")
            output_payload["selected_intervals"] = sorted(
                cast(list[dict[str, Any]], selected),
                key=lambda item: (
                    item["start_utc"],
                    item["end_utc"],
                    item["interval_id"],
                ),
            )
            _require(
                receipt.get("s_i_commitment_sha256") == sha256_json(output_payload),
                f"receipt S_i binding mismatch: {fixture_id}",
            )
        fixtures[fixture_id] = fixture
        receipts[fixture_id] = receipt
    return BundleEvidence(
        inference_schema,
        evaluator_schema,
        inference_manifest,
        evaluator_manifest,
        evaluation_manifest,
        inference_entries,
        evaluation_entries,
        receipts,
        fixtures,
    )


def _typed_digest(value: object) -> dict[str, str | None]:
    if value is None:
        return {"applicability": "not_applicable", "sha256": None}
    _require(isinstance(value, str) and SHA256_RE.fullmatch(value) is not None, "invalid digest")
    return {"applicability": "applicable", "sha256": cast(str, value)}


def _actual_code(receipt: Mapping[str, Any]) -> str | None:
    violations = receipt.get("violation_codes")
    if isinstance(violations, list) and violations:
        _require(all(isinstance(item, str) for item in violations), "invalid violation codes")
        return cast(str, violations[0])
    status = receipt.get("reference_domain_status")
    return status if isinstance(status, str) else None


def _fraction(metrics: Mapping[str, Any], name: str) -> str | None:
    value = metrics.get(name)
    if not isinstance(value, dict):
        return None
    fraction = value.get("fraction")
    return fraction if isinstance(fraction, str) else None


def _assert_invariants(
    invariants: Sequence[str],
    fixture: Mapping[str, Any],
    receipt: Mapping[str, Any],
    bundle: BundleEvidence,
) -> None:
    rendered = json.dumps(receipt, sort_keys=True).lower()
    metrics = receipt.get("metrics")
    metric_map = cast(Mapping[str, Any], metrics) if isinstance(metrics, dict) else {}
    for invariant in invariants:
        if invariant == "controlled_violation_code_present":
            _require(_actual_code(receipt) is not None, "controlled violation code is missing")
        elif invariant == "full_c_unit_fractions":
            for name in (
                "temporal_width_retained",
                "canonical_interval_count_retained",
                "unique_state_identity_count_retained",
                "date_coverage",
            ):
                _require(_fraction(metric_map, name) == "1/1", f"full-C {name} is not one")
        elif invariant == "no_inference_claim":
            _require(receipt.get("inference_or_selection_performed") is False, "inference claim")
        elif invariant == "abstention_components_typed_na":
            abstention = metric_map.get("abstention")
            _require(abstention == {"status": "applicable", "value": True}, "bad abstention")
            for name in (
                "reference_intersection",
                "temporal_width_retained",
                "canonical_interval_count_retained",
                "unique_state_identity_count_retained",
                "date_coverage",
            ):
                component = metric_map.get(name)
                _require(
                    isinstance(component, dict)
                    and cast(dict[str, Any], component).get("status")
                    == "not_applicable_abstention",
                    f"abstention component is not typed N/A: {name}",
                )
        elif invariant == "interval_state_count_divergence":
            _require(
                _fraction(metric_map, "canonical_interval_count_retained") == "1/3",
                "selected interval-count fraction changed",
            )
            _require(
                _fraction(metric_map, "unique_state_identity_count_retained") == "1/4",
                "selected unique-state fraction changed",
            )
        elif invariant == "disconnected_subset_exact":
            output = fixture.get("preconstructed_output")
            _require(isinstance(output, dict), "preconstructed output missing")
            selected = cast(dict[str, Any], output).get("selected_intervals")
            _require(isinstance(selected, list) and len(selected) == 2, "disconnected S_i changed")
            selected_list = cast(list[Any], selected)
            ids = [cast(dict[str, Any], item).get("interval_id") for item in selected_list]
            _require(ids == ["SYNTH-INTERVAL-A", "SYNTH-INTERVAL-C"], "wrong disconnected S_i")
            _require(_fraction(metric_map, "temporal_width_retained") == "1/2", "gap filled")
        elif invariant == "canonical_reorder_equivalent":
            base = bundle.receipts.get("SYNTH-FIXTURE-DISCONNECTED-SAME-DATE")
            _require(base is not None, "canonical reorder base receipt missing")
            base_receipt = cast(dict[str, Any], base)
            for field in (
                "s_i_commitment_sha256",
                "metrics_sha256",
            ):
                _require(receipt.get(field) == base_receipt.get(field), f"reorder changed {field}")
        elif invariant == "no_forbidden_semantics":
            for fragment in (
                '"rank"',
                '"best',
                '"score',
                '"weight',
                '"probability',
                '"confidence',
                '"utility',
                '"threshold',
                '"recommendation',
                '"contiguous_window',
            ):
                _require(fragment not in rendered, f"forbidden receipt semantic: {fragment}")
        elif invariant == "required_receipt_bindings":
            for field in (
                "inference_visible_fixture_digest",
                "s_i_commitment_sha256",
                "canonical_t_i_sha256",
                "reference_custody_sha256",
                "reference_custody_access_state_sha256",
                "access_state_sha256",
                "evaluator_version_sha256",
            ):
                _require(
                    isinstance(receipt.get(field), str)
                    and SHA256_RE.fullmatch(cast(str, receipt[field])) is not None,
                    f"valid receipt binding is absent: {field}",
                )
        elif invariant == "all_valid_receipts_bind_access":
            for fixture_id, candidate in bundle.receipts.items():
                if candidate.get("receipt_kind") == "fail_closed_rejection":
                    continue
                digest = candidate.get("access_state_sha256")
                _require(
                    isinstance(digest, str) and SHA256_RE.fullmatch(digest) is not None,
                    f"valid receipt lacks access binding: {fixture_id}",
                )
        elif invariant == "inference_fixture_has_no_reference_dependency":
            prohibited = {
                "hidden_reference",
                "reference_custody_sha256",
                "canonical_t_i_sha256",
                "reference_path",
                "reference_size",
                "custody_id",
            }
            _require(not (set(fixture) & prohibited), "inference fixture exposes reference")
        elif invariant == "reference_accuracy_applicable":
            component = metric_map.get("reference_intersection")
            _require(
                isinstance(component, dict)
                and cast(dict[str, Any], component).get("status") == "applicable",
                "reference accuracy is not applicable",
            )
        elif invariant == "reference_accuracy_not_applicable":
            _require(receipt.get("valid_reference_evaluation_receipt") is False, "valid accuracy")
            component = receipt.get("reference_intersection")
            _require(
                isinstance(component, dict)
                and str(cast(dict[str, Any], component).get("status", "")).startswith(
                    "not_applicable_reference_domain_"
                ),
                "incompatible reference lacks typed N/A",
            )
            _require("metrics" not in receipt, "incompatible reference has accuracy metrics")
        elif invariant == "closed_schema_rehash_mutation_test_bound":
            _require(receipt.get("receipt_kind") == "descriptive_metric_receipt", "bad base")
        else:
            raise AcceptanceMatrixError(f"unknown invariant: {invariant}")


def _artifact_binding(root: Path, commit: str, path: Path) -> dict[str, str]:
    raw = _git_file(root, commit, path)
    return {
        "path": path.as_posix(),
        "git_blob_oid": _blob_oid(root, commit, path),
        "file_sha256": _sha256_bytes(raw),
    }


def _code_binding(root: Path, commit: str, path: Path, symbols: Sequence[str]) -> dict[str, Any]:
    raw = _git_file(root, commit, path)
    _verify_symbols(raw, path, symbols)
    return {
        "path": path.as_posix(),
        "git_blob_oid": _blob_oid(root, commit, path),
        "file_sha256": _sha256_bytes(raw),
        "symbols": list(symbols),
    }


def _fixture_case(spec: RequirementSpec, fixture_id: str, bundle: BundleEvidence) -> dict[str, Any]:
    _require(fixture_id in bundle.receipts, f"required fixture is absent: {fixture_id}")
    fixture = bundle.fixtures[fixture_id]
    receipt = bundle.receipts[fixture_id]
    actual_kind = receipt.get("receipt_kind")
    actual_code = _actual_code(receipt)
    _require(
        actual_kind == spec.expected_receipt_kind,
        f"unexpected receipt kind for {fixture_id}: {actual_kind}",
    )
    if spec.expected_code is not None:
        _require(actual_code == spec.expected_code, f"unexpected controlled code: {fixture_id}")
    _assert_invariants(spec.invariants, fixture, receipt, bundle)
    inference_entry = bundle.inference_entries[fixture_id]
    evaluation_entry = bundle.evaluation_entries[fixture_id]
    return {
        "fixture_id": fixture_id,
        "controlled_status": actual_kind,
        "controlled_code": actual_code,
        "expectation_matched": True,
        "digest_evidence": {
            "inference_visible_fixture": _typed_digest(
                inference_entry.get("inference_visible_fixture_digest")
            ),
            "receipt": _typed_digest(evaluation_entry.get("receipt_sha256")),
            "access_state": _typed_digest(receipt.get("access_state_sha256")),
        },
    }


def _build_entry(
    root: Path,
    commit: str,
    tree_oid: str,
    spec: RequirementSpec,
    contract_catalog: Mapping[str, Mapping[str, str]],
    evaluator_sha256: str,
    requirement_sources: Mapping[int, Mapping[str, str]],
    bundle: BundleEvidence,
) -> dict[str, Any]:
    test_source = _git_file(root, commit, spec.test_path)
    _require(
        spec.test_name in _test_functions(test_source, spec.test_path),
        f"mapped test is missing at source commit: {spec.test_path}:{spec.test_name}",
    )
    cases = [_fixture_case(spec, fixture_id, bundle) for fixture_id in spec.fixture_ids]
    artifact = _artifact_binding(root, commit, spec.artifact_path)
    contract_bindings = [
        {
            "version": version,
            "contract_sha256": contract_catalog[version]["contract_sha256"],
        }
        for version in spec.contract_versions
    ]
    dimensions = {name: name in spec.dimensions for name in DIMENSIONS}
    requirement_sha256 = _sha256_bytes(spec.requirement.encode("utf-8"))
    evaluator_binding: dict[str, str | None]
    if spec.fixture_ids:
        evaluator_binding = {
            "applicability": "applicable",
            "evaluator_version_sha256": evaluator_sha256,
        }
    else:
        evaluator_binding = {
            "applicability": "not_applicable",
            "evaluator_version_sha256": None,
        }
    return {
        "requirement_id": spec.requirement_id,
        "origin": {
            "checkpoint": spec.checkpoint,
            "section": spec.section,
            "rule_ordinal": spec.ordinal,
            "source_path": CHECKPOINT_PATHS[spec.checkpoint].as_posix(),
            "source_document_sha256": requirement_sources[spec.checkpoint]["file_sha256"],
        },
        "requirement": spec.requirement,
        "requirement_sha256": requirement_sha256,
        "requirement_domain": spec.domain,
        "acceptance_dimensions": dimensions,
        "test_evidence": {
            "path": spec.test_path.as_posix(),
            "test_name": spec.test_name,
            "test_source_blob_oid": _blob_oid(root, commit, spec.test_path),
            "test_source_sha256": _sha256_bytes(test_source),
        },
        "fixture_ids": list(spec.fixture_ids),
        "expected_outcome": {
            "kind": spec.expected_receipt_kind or "committed_evidence_binding",
            "controlled_code": spec.expected_code,
            "invariants": list(spec.invariants),
        },
        "actual_outcome": {
            "verification_state": (
                "controlled_fixture_receipt_observed"
                if spec.fixture_ids
                else "committed_evidence_and_test_binding_observed"
            ),
            "cases": cases,
            "artifact": artifact,
        },
        "contract_bindings": contract_bindings,
        "evaluator_binding": evaluator_binding,
        "source_binding": {
            "exact_source_commit": commit,
            "exact_source_tree_oid": tree_oid,
        },
        "code_bindings": [
            _code_binding(root, commit, path, symbols) for path, symbols in spec.code_bindings
        ],
        "custody_dependency": {
            "required": bool(spec.fixture_ids),
            "pending_fields": [],
        },
        "pro_minimum": spec.pro_minimum,
    }


def build_acceptance_matrix(
    repository_root: Path = PROJECT_ROOT, source_commit: str | None = None
) -> dict[str, Any]:
    """Build a final matrix from exact committed post-custody evidence."""

    root = repository_root.resolve(strict=True)
    commit = _resolve_commit(root, source_commit)
    tree_oid = _git_text(root, ["rev-parse", f"{commit}^{{tree}}"])
    contract_catalog = _load_contract_catalog(root, commit)
    bundle = _load_bundle(root, commit)
    evaluator_version = bundle.evaluator_schema.get("evaluator_version")
    _require(isinstance(evaluator_version, dict), "evaluator schema lacks evaluator version")
    evaluator_sha256 = cast(dict[str, Any], evaluator_version).get("evaluator_version_sha256")
    _require(
        isinstance(evaluator_sha256, str) and SHA256_RE.fullmatch(evaluator_sha256) is not None,
        "invalid evaluator-version digest",
    )
    evaluator_digest = cast(str, evaluator_sha256)
    _require(
        bundle.evaluation_manifest.get("evaluator_version_sha256") == evaluator_digest,
        "evaluation manifest evaluator digest mismatch",
    )
    _require(
        bundle.evaluation_manifest.get("contract_sha256")
        == contract_catalog["v3"]["contract_sha256"],
        "evaluation manifest does not bind operative v3",
    )
    source_files = cast(dict[str, Any], evaluator_version).get("source_files")
    _require(isinstance(source_files, list) and bool(source_files), "evaluator source files absent")
    evaluator_source_files = cast(list[Any], source_files)
    evaluator_sources: list[dict[str, str]] = []
    for item in evaluator_source_files:
        _require(isinstance(item, dict), "invalid evaluator source-file binding")
        path = Path(cast(str, item.get("path")))
        raw = _git_file(root, commit, path)
        digest = _sha256_bytes(raw)
        _require(digest == item.get("sha256"), f"evaluator source digest mismatch: {path}")
        evaluator_sources.append(
            {
                "path": path.as_posix(),
                "git_blob_oid": _blob_oid(root, commit, path),
                "sha256": digest,
            }
        )

    requirement_sources = {
        checkpoint: {
            "path": path.as_posix(),
            "git_blob_oid": _blob_oid(root, commit, path),
            "file_sha256": _sha256_bytes(_git_file(root, commit, path)),
        }
        for checkpoint, path in CHECKPOINT_PATHS.items()
    }
    entries = [
        _build_entry(
            root,
            commit,
            tree_oid,
            spec,
            contract_catalog,
            evaluator_digest,
            requirement_sources,
            bundle,
        )
        for spec in REQUIREMENTS
    ]
    dimension_counts = {
        dimension: sum(
            bool(cast(dict[str, bool], entry["acceptance_dimensions"])[dimension])
            for entry in entries
        )
        for dimension in DIMENSIONS
    }
    checkpoint_counts = {
        str(checkpoint): count
        for checkpoint, count in sorted(Counter(spec.checkpoint for spec in REQUIREMENTS).items())
    }
    domain_counts = dict(sorted(Counter(spec.domain for spec in REQUIREMENTS).items()))
    payload: dict[str, Any] = {
        "schema_version": "natal-time-checkpoint5-acceptance-matrix-v1",
        "matrix_status": "finalized_post_custody_synthetic_only",
        "synthetic_only": True,
        "participant_records_accessed": 0,
        "exact_source": {"commit": commit, "tree_oid": tree_oid},
        "requirement_sources": [
            {"checkpoint": checkpoint, **requirement_sources[checkpoint]}
            for checkpoint in sorted(requirement_sources)
        ],
        "contract_catalog": contract_catalog,
        "evaluator_binding": {
            "evaluator_version_sha256": evaluator_digest,
            "source_files": evaluator_sources,
        },
        "bundle_bindings": {
            "inference_schema_sha256": bundle.inference_schema["schema_sha256"],
            "evaluator_schema_sha256": bundle.evaluator_schema["schema_sha256"],
            "inference_manifest_sha256": bundle.inference_manifest["manifest_sha256"],
            "evaluator_manifest_sha256": bundle.evaluator_manifest["manifest_sha256"],
            "evaluation_manifest_sha256": bundle.evaluation_manifest["manifest_sha256"],
            "fixture_count": len(bundle.fixtures),
            "receipt_count": len(bundle.receipts),
            "hidden_reference_content_included": False,
            "canonical_t_i_digest_included": False,
            "reference_custody_digest_included": False,
        },
        "entry_count": len(entries),
        "entries": entries,
        "coverage_summary": {
            "checkpoint_entry_counts": checkpoint_counts,
            "requirement_domain_counts": domain_counts,
            "acceptance_dimension_counts": dimension_counts,
            "pro_minimum_requirement_ids": sorted(PRO_MINIMUM_IDS),
            "pro_minimums_complete": True,
            "pending_field_count": 0,
        },
    }
    payload["matrix_sha256"] = sha256_json(payload)
    validate_matrix_structure(payload)
    return payload


def _validate_digest_object(value: object, label: str) -> None:
    _require(isinstance(value, dict), f"digest evidence is not an object: {label}")
    item = cast(dict[str, Any], value)
    _require(set(item) == {"applicability", "sha256"}, f"bad digest keys: {label}")
    if item["applicability"] == "applicable":
        _require(
            isinstance(item["sha256"], str) and SHA256_RE.fullmatch(item["sha256"]) is not None,
            f"applicable digest is malformed: {label}",
        )
    elif item["applicability"] == "not_applicable":
        _require(item["sha256"] is None, f"N/A digest has a value: {label}")
    else:
        raise AcceptanceMatrixError(f"unknown digest applicability: {label}")


def validate_matrix_structure(
    matrix: Mapping[str, Any], required_ids: frozenset[str] | None = None
) -> None:
    """Validate closed matrix structure without reading repository files."""

    expected_top = {
        "schema_version",
        "matrix_status",
        "synthetic_only",
        "participant_records_accessed",
        "exact_source",
        "requirement_sources",
        "contract_catalog",
        "evaluator_binding",
        "bundle_bindings",
        "entry_count",
        "entries",
        "coverage_summary",
        "matrix_sha256",
    }
    _require(set(matrix) == expected_top, "acceptance matrix top-level schema changed")
    _require(
        matrix.get("schema_version") == "natal-time-checkpoint5-acceptance-matrix-v1",
        "acceptance matrix schema version changed",
    )
    _require(
        matrix.get("matrix_status") == "finalized_post_custody_synthetic_only",
        "acceptance matrix is not finalized",
    )
    _require(matrix.get("synthetic_only") is True, "matrix is not synthetic-only")
    _require(matrix.get("participant_records_accessed") == 0, "participant access claimed")
    exact_source = matrix.get("exact_source")
    _require(isinstance(exact_source, dict), "exact source is absent")
    source = cast(dict[str, Any], exact_source)
    _require(COMMIT_RE.fullmatch(str(source.get("commit", ""))) is not None, "bad source OID")
    _require(
        re.fullmatch(r"[0-9a-f]{40,64}", str(source.get("tree_oid", ""))) is not None,
        "bad tree OID",
    )
    entries = matrix.get("entries")
    _require(isinstance(entries, list), "matrix entries are absent")
    entry_list = cast(list[Any], entries)
    _require(matrix.get("entry_count") == len(entry_list), "matrix entry count mismatch")
    ids: list[str] = []
    for raw in entry_list:
        _require(isinstance(raw, dict), "matrix entry is not an object")
        entry = cast(dict[str, Any], raw)
        requirement_id = entry.get("requirement_id")
        _require(isinstance(requirement_id, str), "matrix requirement ID is missing")
        requirement_id_string = cast(str, requirement_id)
        ids.append(requirement_id_string)
        _require(
            entry.get("requirement_sha256")
            == _sha256_bytes(cast(str, entry.get("requirement", "")).encode("utf-8")),
            f"requirement digest mismatch: {requirement_id_string}",
        )
        dimensions = entry.get("acceptance_dimensions")
        _require(isinstance(dimensions, dict), f"dimensions absent: {requirement_id}")
        dimension_map = cast(dict[str, Any], dimensions)
        _require(set(dimension_map) == set(DIMENSIONS), f"dimension set changed: {requirement_id}")
        _require(
            all(isinstance(value, bool) for value in dimension_map.values()), "nonboolean dimension"
        )
        _require(
            any(dimension_map.values()), f"entry has no acceptance dimension: {requirement_id}"
        )
        custody = entry.get("custody_dependency")
        _require(isinstance(custody, dict), f"custody dependency absent: {requirement_id}")
        _require(
            cast(dict[str, Any], custody).get("pending_fields") == [],
            f"pending fields: {requirement_id}",
        )
        actual = entry.get("actual_outcome")
        _require(isinstance(actual, dict), f"actual outcome absent: {requirement_id}")
        cases = cast(dict[str, Any], actual).get("cases")
        _require(isinstance(cases, list), f"actual cases absent: {requirement_id}")
        for case in cast(list[Any], cases):
            _require(isinstance(case, dict), "actual case is not an object")
            case_map = cast(dict[str, Any], case)
            _require(case_map.get("expectation_matched") is True, "fixture expectation failed")
            digests = case_map.get("digest_evidence")
            _require(isinstance(digests, dict), "fixture digest evidence absent")
            digest_map = cast(dict[str, Any], digests)
            _require(
                set(digest_map) == {"inference_visible_fixture", "receipt", "access_state"},
                "fixture digest evidence type set changed",
            )
            for name, digest in digest_map.items():
                _validate_digest_object(digest, f"{requirement_id}:{name}")
        evaluator = entry.get("evaluator_binding")
        _require(isinstance(evaluator, dict), f"evaluator binding absent: {requirement_id}")
        evaluator_map = cast(dict[str, Any], evaluator)
        if evaluator_map.get("applicability") == "applicable":
            _require(
                SHA256_RE.fullmatch(str(evaluator_map.get("evaluator_version_sha256", "")))
                is not None,
                f"bad evaluator digest: {requirement_id}",
            )
        else:
            _require(
                evaluator_map
                == {"applicability": "not_applicable", "evaluator_version_sha256": None},
                f"bad N/A evaluator binding: {requirement_id}",
            )
    _require(len(ids) == len(set(ids)), "duplicate requirement IDs")
    expected_ids = (
        required_ids
        if required_ids is not None
        else frozenset(spec.requirement_id for spec in REQUIREMENTS)
    )
    _require(set(ids) == expected_ids, "requirement inventory is incomplete or unexpected")
    if required_ids is None:
        _require(set(ids) >= PRO_MINIMUM_IDS, "one or more Pro minimum entries are missing")
    rendered = json.dumps(matrix, sort_keys=True).lower()
    for forbidden in (
        '"canonical_t_i_sha256"',
        '"reference_custody_sha256"',
        '"reference_path"',
        '"hidden_reference"',
    ):
        _require(
            forbidden not in rendered, f"matrix exposes forbidden custody material: {forbidden}"
        )
    payload = dict(matrix)
    embedded = payload.pop("matrix_sha256", None)
    _require(
        isinstance(embedded, str) and SHA256_RE.fullmatch(embedded) is not None, "bad matrix hash"
    )
    _require(sha256_json(payload) == embedded, "matrix self-hash mismatch")


def validate_acceptance_matrix(repository_root: Path, matrix: Mapping[str, Any]) -> None:
    """Reproduce a saved matrix from its exact source commit."""

    validate_matrix_structure(matrix)
    exact_source = cast(dict[str, Any], matrix["exact_source"])
    reproduced = build_acceptance_matrix(
        repository_root, source_commit=cast(str, exact_source["commit"])
    )
    _require(reproduced == matrix, "saved acceptance matrix does not reproduce exactly")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--source-commit")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / OUTPUT_PATH)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve(strict=True)
    output = args.output.resolve()
    if args.validate_only:
        saved = _load_json_bytes(output.read_bytes(), output.as_posix())
        validate_acceptance_matrix(root, saved)
        return 0
    matrix = build_acceptance_matrix(root, source_commit=args.source_commit)
    write_new_bytes(output, canonical_json_bytes(matrix) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
