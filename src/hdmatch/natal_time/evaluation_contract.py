"""Synthetic-only verifier for the frozen natal-time evaluation contract.

This module validates preconstructed test vectors.  It never constructs, ranks,
prunes, or recommends an ``S_i`` output and contains no Human Design, questionnaire,
participant, relationship, or inferential model semantics.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from fractions import Fraction
from pathlib import Path
from typing import Final, NoReturn, TypeAlias, cast
from weakref import WeakKeyDictionary

from hdmatch.util import sha256_file, sha256_json

JsonObject: TypeAlias = dict[str, object]

V1_CONTRACT_SHA256: Final = "c721dcdd5ed9e144ca4795523420e226bc13dc8a739669991c365c1bb4d3f6c9"
V2_CONTRACT_SHA256: Final = "067417a49c158fd7d7d1d31c3b21a584c1d1259aa85d60a30e9a6d3f39976f5e"
V3_CONTRACT_SHA256: Final = "75a1629203724715054e2a1d7ea1b6ead7dc0ffd6cf5f4df2756c3e622b5f1fe"
MODULE_PATH: Final = "src/hdmatch/natal_time/evaluation_contract.py"
BUILDER_PATH: Final = "scripts/build_natal_time_synthetic_evaluation_verifier.py"
_REFERENCE_CAPABILITY_ISSUER: Final = object()
_OPENED_REFERENCE_ISSUER: Final = object()

_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_SYNTHETIC_ID_RE = re.compile(r"SYNTH-[A-Z0-9]+(?:-[A-Z0-9]+)*")
_INTERVAL_ID_RE = re.compile(r"SYNTH-INTERVAL-[A-Z0-9]+(?:-[A-Z0-9]+)*")
_SOURCE_ID_RE = re.compile(r"SYNTH-SOURCE-[A-Z0-9]+(?:-[A-Z0-9]+)*")
_LINEAGE_ID_RE = re.compile(r"SYNTH-LINEAGE-[A-Z0-9]+(?:-[A-Z0-9]+)*")
_CUSTODY_ID_RE = re.compile(r"SYNTH-CUSTODY-[A-Z0-9]+(?:-[A-Z0-9]+)*")
_DATE_RE = re.compile(r"2099-\d{2}-\d{2}")

FORBIDDEN_FIELD_FRAGMENTS: Final = (
    "participant",
    "relationship",
    "partner",
    "household",
    "contact",
    "consent",
    "recovery",
    "birth",
    "question",
    "response",
    "free_text",
    "narrative",
    "email",
    "phone",
    "address",
    "name",
)
PROHIBITED_OUTPUT_FRAGMENTS: Final = (
    "rank",
    "best",
    "score",
    "weight",
    "probability",
    "confidence",
    "utility",
    "threshold",
    "recommendation",
)

BASELINE_IDS: Final = (
    "complete-unordered-candidate-set",
    "no-pruning-after-responses",
    "random-subset-temporal-width-matched",
    "random-subset-state-count-matched",
    "calendar-only",
    "season-only",
    "birthplace-only",
    "timezone-only",
    "cohort-only",
    "source-quality-only",
    "response-style-only",
    "participant-chart-label-permutation",
    "plausible-mismatched-chart",
    "blinded-matching",
    "strongest-ordinary-non-hd",
)
MEASUREMENT_REQUIREMENT_IDS: Final = (
    "test-retest-reliability",
    "inter-rater-reliability",
    "missingness",
    "acquiescence-and-response-style",
    "social-desirability",
    "forer-barnum-susceptibility",
    "item-transparency-and-chart-cueing",
    "construct-overlap",
    "language-and-population-invariance",
    "blinded-authorship-and-evaluation",
    "item-generation-label-separation",
)
DATA_ROLE_IDS: Final = (
    "development",
    "calibration",
    "locked_validation",
)
ACTOR_ACCESS_IDS: Final = (
    "candidate_constructor",
    "measurement_developer",
    "inference_procedure",
    "reference_custodian",
    "independent_calibration_evaluator",
    "independent_validation_evaluator",
)
SOURCE_ELIGIBILITY_RULE_IDS: Final = (
    "documentary-not-memory-only",
    "record-independent-of-study-inference",
    "auditable-source-and-custody-lineage",
    "recoverable-interval-precision-and-rounding",
    "not-derived-from-prohibited-inference-evidence",
)
ELIGIBLE_SOURCE_CLASS_IDS: Final = (
    "auditable-civil-or-clinical-record",
    "auditable-certified-extract-or-archive-transcription",
)
INELIGIBLE_SOURCE_CLASS_IDS: Final = (
    "memory-only-time-or-date",
    "unsupported-assertion",
    "unsupported-family-recollection",
    "rectified-time",
    "relationship-history-or-testimony",
    "reference-leaked-before-authorized-comparison",
)
SOURCE_PRECISION_RULE_IDS: Final = (
    "preserve-source-supported-interval",
    "known-rounding-cell",
    "unknown-rounding-envelope",
    "bounded-record-interval",
    "coarse-precision-remains-coarse",
    "memory-only-never-ground-truth",
)
CONNECTED_COMPONENT_EDGE_IDS: Final = (
    "same-or-repeated-identity",
    "relationship-pair",
    "shared-household",
    "relationship-chain",
    "shared-label-transmitting-record-source-or-custodian",
)
LEAKAGE_CONTAMINATION_RULE_IDS: Final = (
    "clean-disjoint-components",
    "same-participant-cross-role",
    "alias-cross-role",
    "partners-cross-role",
    "household-cross-role",
    "relationship-chain-cross-role",
    "shared-record-source-cross-role",
    "reference-enters-candidate-construction",
    "reference-enters-measurement-development",
    "reference-enters-fitting",
    "reference-enters-stopping",
    "calibration-becomes-adaptive",
    "validation-peek-changes-method",
    "relationship-evidence-assisted-inference",
)
METRIC_COMPONENT_IDS: Final = (
    "reference_intersection",
    "temporal_width_retained",
    "canonical_interval_count_retained",
    "unique_state_identity_count_retained",
    "date_coverage",
    "documentary_reference_width",
    "abstention",
)
METRIC_APPLICABILITY_STATUSES: Final = frozenset(
    {
        "applicable",
        "not_applicable_abstention",
        "not_applicable_no_eligible_reference",
        "not_applicable_conflicting_eligible_sources",
        "not_applicable_reference_canonicalization_failed",
        "not_applicable_reference_domain_incompatible",
        "not_applicable_reference_domain_partially_incompatible",
    }
)
DISCLOSURE_THREAT_IDS: Final = (
    "exact-birth-linkage",
    "sparse-state-fingerprints",
    "membership-inference",
    "rare-candidate-sets",
    "repeated-release-differencing",
    "relationship-network-linkage",
    "deterministic-personal-data-hashes",
    "small-cells",
    "free-text",
    "withdrawal-and-deletion",
    "versioned-corrections",
)
DISCLOSURE_CONTROL_IDS: Final = (
    "correction_and_withdrawal_policy",
    "privacy_budget_if_any",
    "release_cadence",
    "small_cell_suppression_threshold",
)
PROHIBITED_PUBLIC_FIELD_IDS: Final = (
    "participant_level_rows",
    "natal_chart_intervals",
    "exact_birth_dates",
    "birth_places",
    "source_documents",
    "relationship_identifiers",
    "personal_data_hashes",
    "free_text",
)
DISCLOSURE_SURFACE_DECLARATION_IDS: Final = (
    "cohort-aggregate-only",
    "release-disabled",
    "threat-review-required-before-release",
    "threat-model-artifact-not-anonymity-evidence",
)
PREREGISTRATION_IDENTIFIER_SETS: Final[dict[str, tuple[str, ...]]] = {
    "baseline_ids": BASELINE_IDS,
    "measurement_requirement_ids": MEASUREMENT_REQUIREMENT_IDS,
    "data_role_ids": DATA_ROLE_IDS,
    "actor_access_ids": ACTOR_ACCESS_IDS,
    "source_eligibility_rule_ids": SOURCE_ELIGIBILITY_RULE_IDS,
    "eligible_source_class_ids": ELIGIBLE_SOURCE_CLASS_IDS,
    "ineligible_source_class_ids": INELIGIBLE_SOURCE_CLASS_IDS,
    "source_precision_rule_ids": SOURCE_PRECISION_RULE_IDS,
    "connected_component_edge_ids": CONNECTED_COMPONENT_EDGE_IDS,
    "leakage_contamination_rule_ids": LEAKAGE_CONTAMINATION_RULE_IDS,
    "metric_component_ids": METRIC_COMPONENT_IDS,
    "disclosure_threat_ids": DISCLOSURE_THREAT_IDS,
    "disclosure_control_ids": DISCLOSURE_CONTROL_IDS,
    "prohibited_public_field_ids": PROHIBITED_PUBLIC_FIELD_IDS,
    "disclosure_surface_declaration_ids": DISCLOSURE_SURFACE_DECLARATION_IDS,
}
PREREGISTRATION_REQUIRED_SINGLETONS: Final = (
    "candidate_reference_output_definitions",
    "metric_applicability_and_separate_reporting",
    "freeze_access_contamination_and_deviation_policy",
    "proof_no_measurement_content_written",
)
ALLOWED_VIOLATION_CODES: Final = frozenset(
    {
        "abstention_must_not_select_intervals",
        "candidate_domain_gap_or_overlap",
        "candidate_domain_missing",
        "candidate_freeze_out_of_order",
        "candidate_manifest_mismatch",
        "candidate_set_digest_mismatch",
        "canonical_reference_requires_source",
        "conflicting_same_lineage_extracts",
        "contaminated_connected_component",
        "contract_digest_mismatch",
        "cross_role_connected_component",
        "declared_date_without_candidate_interval",
        "duplicate_candidate_interval",
        "duplicate_declared_date",
        "duplicate_reference_source_id",
        "duplicate_selected_interval",
        "duplicate_synthetic_observation",
        "empty_candidate_domain",
        "empty_component_assignments",
        "fixture_not_conspicuously_synthetic",
        "foreign_or_manufactured_interval",
        "inapplicable_reference_must_not_include_source",
        "interval_outside_declared_dates",
        "invalid_candidate_intervals",
        "invalid_candidate_manifest_digest",
        "invalid_candidate_set_digest",
        "invalid_candidate_set_fields",
        "invalid_candidate_set_object",
        "invalid_canonical_utc_instant",
        "invalid_component_assignment_fields",
        "invalid_component_assignment_object",
        "invalid_component_assignments",
        "invalid_data_role",
        "invalid_declared_dates",
        "invalid_fixture_fields",
        "invalid_fixture_id",
        "invalid_fixture_object",
        "invalid_fixture_schema_version",
        "inference_visible_fixture_digest_mismatch",
        "invalid_inference_visible_fixture_digest",
        "invalid_reference_custody_digest",
        "invalid_reference_custody_fields",
        "invalid_reference_custody_object",
        "invalid_reference_custody_schema_version",
        "invalid_reference_custody_classification",
        "invalid_reference_documentary_classification",
        "invalid_reference_precision_classification",
        "invalid_synthetic_custody_id",
        "invalid_evaluator_version_digest",
        "invalid_interval_fields",
        "invalid_interval_id",
        "invalid_interval_object",
        "invalid_method_digest",
        "invalid_method_specification_fields",
        "invalid_method_specification_object",
        "invalid_output_fields",
        "invalid_output_empty_non_abstention",
        "invalid_output_kind",
        "invalid_output_object",
        "invalid_reference_bundle_object",
        "invalid_reference_canonicalization_status",
        "invalid_reference_fields",
        "invalid_reference_object",
        "invalid_reference_source_fields",
        "invalid_reference_source_object",
        "invalid_reference_sources",
        "invalid_selected_intervals",
        "invalid_state_digest",
        "invalid_synthetic_component_id",
        "invalid_synthetic_date",
        "invalid_synthetic_lineage_id",
        "invalid_synthetic_observation_id",
        "invalid_synthetic_source_id",
        "invalid_v1_contract_digest",
        "invalid_v2_contract_digest",
        "invalid_v3_contract_digest",
        "method_freeze_out_of_order",
        "method_specification_digest_mismatch",
        "manufactured_interval_not_allowed",
        "metric_receipt_before_t_i_access",
        "metric_receipt_missing",
        "non_string_field_name",
        "noncanonical_utc_instant",
        "nonpositive_interval_width",
        "nonpositive_reference_width",
        "output_not_preconstructed",
        "partial_interval_not_allowed",
        "preconstructed_output_flag_required",
        "prohibited_inferential_or_scalar_output_field",
        "prohibited_personal_or_free_text_field",
        "reference_not_exposed",
        "s_i_commitment_out_of_order",
        "s_i_modified_after_t_i_exposure",
        "selection_procedure_prohibited",
        "early_reference_raw_byte_access",
        "early_reference_digest_access",
        "early_reference_metadata_access",
        "early_reference_alternate_loader_access",
        "invalid_reference_access_capability",
        "t_i_mutated_after_evaluator_access",
        "t_i_access_before_s_i_commitment",
        "unknown_execution_event",
    }
)

_INFERENCE_FIXTURE_KEYS: Final = {
    "schema_version",
    "fixture_id",
    "synthetic_only",
    "preconstructed_s_i",
    "candidate_set",
    "method_specification",
    "preconstructed_output",
    "component_assignments",
    "contamination_status",
    "execution_plan",
    "inference_visible_fixture_digest",
}
_EXECUTION_EVENTS: Final = {
    "candidate_domain_freeze",
    "study_method_specification_freeze",
    "preconstructed_s_i_commitment",
    "evaluator_only_t_i_access",
    "early_reference_raw_byte_access_attempt",
    "early_reference_digest_access_attempt",
    "early_reference_metadata_access_attempt",
    "early_reference_alternate_loader_access_attempt",
    "post_reference_s_i_mutation_attempt",
    "post_reference_t_i_mutation_attempt",
    "metric_receipt",
}

REFERENCE_OPERATION_CODES: Final = (
    "raw_byte",
    "open",
    "read",
    "stat",
    "path",
    "size",
    "parse",
    "serialization",
    "hash",
    "listing",
    "addressability",
)

_EARLY_REFERENCE_ATTEMPT_CODES: Final[dict[str, str]] = {
    "raw_byte": "early_reference_raw_byte_access",
    "digest": "early_reference_digest_access",
    "metadata": "early_reference_metadata_access",
    "alternate_loader": "early_reference_alternate_loader_access",
}

_REFERENCE_CUSTODY_KEYS: Final = {
    "schema_version",
    "custody_id",
    "synthetic_only",
    "documentary_source_classification",
    "precision_classification",
    "custody_classification",
    "reference",
    "mutation_test_mode",
    "reference_custody_sha256",
}


class VerificationError(ValueError):
    """A stable fail-closed verifier error."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class DataRole(StrEnum):
    DEVELOPMENT = "development"
    CALIBRATION = "calibration"
    LOCKED_VALIDATION = "locked_validation"


class SessionPhase(StrEnum):
    NEW = "new"
    CANDIDATE_FROZEN = "candidate_domain_frozen"
    METHOD_FROZEN = "study_method_frozen"
    OUTPUT_COMMITTED = "s_i_committed"
    REFERENCE_EXPOSED = "evaluator_t_i_exposed"
    INVALIDATED = "invalidated"
    RECEIPT_ISSUED = "receipt_issued"


class OutputKind(StrEnum):
    CANDIDATE_SUBSET = "candidate_subset"
    ABSTENTION = "abstention"


@dataclass(frozen=True, slots=True)
class CanonicalInterval:
    candidate_manifest_sha256: str
    candidate_set_sha256: str
    interval_id: str
    start_utc: datetime
    end_utc: datetime
    full_state_sha256: str
    civil_date: str

    @property
    def width_microseconds(self) -> int:
        return _timedelta_microseconds(self.start_utc, self.end_utc)

    def to_json(self) -> JsonObject:
        return {
            "candidate_manifest_sha256": self.candidate_manifest_sha256,
            "candidate_set_sha256": self.candidate_set_sha256,
            "interval_id": self.interval_id,
            "start_utc": _format_utc(self.start_utc),
            "end_utc": _format_utc(self.end_utc),
            "full_state_sha256": self.full_state_sha256,
            "civil_date": self.civil_date,
        }


@dataclass(frozen=True, slots=True)
class CandidateSet:
    candidate_manifest_sha256: str
    candidate_set_sha256: str
    declared_dates: tuple[str, ...]
    intervals: tuple[CanonicalInterval, ...]

    def canonical_payload(self) -> JsonObject:
        return {
            "candidate_manifest_sha256": self.candidate_manifest_sha256,
            "candidate_set_sha256": self.candidate_set_sha256,
            "declared_dates": list(sorted(self.declared_dates)),
            "intervals": [item.to_json() for item in _sort_intervals(self.intervals)],
        }


@dataclass(frozen=True, slots=True)
class PreconstructedOutput:
    output_kind: OutputKind
    selected_intervals: tuple[CanonicalInterval, ...]

    def canonical_payload(self) -> JsonObject:
        return {
            "output_kind": self.output_kind.value,
            "selected_intervals": [
                item.to_json() for item in _sort_intervals(self.selected_intervals)
            ],
        }


@dataclass(frozen=True, slots=True)
class MethodSpecification:
    study_design_contract_sha256: str
    preserved_metric_semantics_v2_contract_sha256: str
    operative_metric_semantics_v3_contract_sha256: str
    s_i_origin: str
    selection_procedure_present: bool
    method_specification_sha256: str


@dataclass(frozen=True, slots=True)
class ComponentAssignment:
    synthetic_observation_id: str
    component_id: str
    role: DataRole


@dataclass(frozen=True, slots=True)
class ReferenceSource:
    source_id: str
    lineage_id: str
    start_utc: datetime
    end_utc: datetime

    def interval_key(self) -> tuple[datetime, datetime]:
        return (self.start_utc, self.end_utc)

    def to_json(self) -> JsonObject:
        return {
            "source_id": self.source_id,
            "lineage_id": self.lineage_id,
            "start_utc": _format_utc(self.start_utc),
            "end_utc": _format_utc(self.end_utc),
        }


@dataclass(frozen=True, slots=True)
class ReferenceBundle:
    canonicalization_status: str
    sources: tuple[ReferenceSource, ...]

    def canonical_payload(self) -> JsonObject:
        sources = sorted(self.sources, key=lambda item: (item.source_id, item.lineage_id))
        return {
            "canonicalization_status": self.canonicalization_status,
            "sources": [item.to_json() for item in sources],
        }


@dataclass(frozen=True, slots=True)
class EvaluatorReferenceRecord:
    """A parsed evaluator-only custody object opened after ``S_i`` commitment."""

    custody_id: str
    reference_custody_sha256: str
    reference: ReferenceBundle
    mutation_test_mode: str


@dataclass(frozen=True, slots=True, init=False)
class _ReferenceAccessCapability:
    """Opaque state-order token released only by a committed session."""

    _seal: object
    s_i_commitment_sha256: str
    _authorizer: Callable[[object, str], None]

    def __init__(
        self,
        issuer: object,
        seal: object,
        s_i_commitment_sha256: str,
        authorizer: Callable[[object, str], None],
    ) -> None:
        if issuer is not _REFERENCE_CAPABILITY_ISSUER:
            _fail("invalid_reference_access_capability")
        object.__setattr__(self, "_seal", seal)
        object.__setattr__(self, "s_i_commitment_sha256", s_i_commitment_sha256)
        object.__setattr__(self, "_authorizer", authorizer)

    def _authorize(self) -> None:
        self._authorizer(self._seal, self.s_i_commitment_sha256)


@dataclass(frozen=True, slots=True, init=False)
class _OpenedEvaluatorReference:
    """Post-commit handoff from evaluator custody to the metric evaluator."""

    record: EvaluatorReferenceRecord
    custody_access_state_sha256: str
    s_i_commitment_sha256: str
    preissue_integrity_rechecked: bool

    def __init__(
        self,
        issuer: object,
        record: EvaluatorReferenceRecord,
        custody_access_state_sha256: str,
        s_i_commitment_sha256: str,
        *,
        preissue_integrity_rechecked: bool,
    ) -> None:
        if issuer is not _OPENED_REFERENCE_ISSUER:
            _fail("invalid_reference_access_capability")
        object.__setattr__(self, "record", record)
        object.__setattr__(
            self,
            "custody_access_state_sha256",
            custody_access_state_sha256,
        )
        object.__setattr__(self, "s_i_commitment_sha256", s_i_commitment_sha256)
        object.__setattr__(
            self,
            "preissue_integrity_rechecked",
            preissue_integrity_rechecked,
        )


class ReferenceCustodyPhase(StrEnum):
    SEALED = "sealed"
    OPENED = "opened"
    INVALIDATED = "invalidated"


@dataclass(frozen=True, slots=True)
class PreregistrationValidation:
    valid: bool
    missing_sections: tuple[str, ...]
    duplicate_sections: tuple[str, ...]
    unexpected_sections: tuple[str, ...]


def _fail(code: str) -> NoReturn:
    raise VerificationError(code)


def _format_utc(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _timedelta_microseconds(start: datetime, end: datetime) -> int:
    delta = end - start
    return delta.days * 86_400_000_000 + delta.seconds * 1_000_000 + delta.microseconds


def _parse_utc(value: object) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        _fail("invalid_canonical_utc_instant")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        _fail("invalid_canonical_utc_instant")
    if parsed.tzinfo is None or parsed.utcoffset() != UTC.utcoffset(parsed):
        _fail("invalid_canonical_utc_instant")
    if _format_utc(parsed) != value:
        _fail("noncanonical_utc_instant")
    return parsed


def _require_object(value: object, code: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        _fail(code)
    return cast(Mapping[str, object], value)


def _require_exact_keys(value: Mapping[str, object], keys: set[str], code: str) -> None:
    if set(value) != keys:
        _fail(code)


def _require_string(value: object, pattern: re.Pattern[str], code: str) -> str:
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        _fail(code)
    return value


def _require_digest(value: object, code: str) -> str:
    return _require_string(value, _SHA256_RE, code)


def _require_synthetic_date(value: object) -> str:
    rendered = _require_string(value, _DATE_RE, "invalid_synthetic_date")
    try:
        parsed = datetime.strptime(rendered, "%Y-%m-%d").date()
    except ValueError:
        _fail("invalid_synthetic_date")
    if parsed.year != 2099 or parsed.isoformat() != rendered:
        _fail("invalid_synthetic_date")
    return rendered


def _require_bool(value: object, expected: bool, code: str) -> None:
    if value is not expected:
        _fail(code)


def _require_sequence(value: object, code: str) -> Sequence[object]:
    if not isinstance(value, list):
        _fail(code)
    return value


def _sort_intervals(values: Sequence[CanonicalInterval]) -> tuple[CanonicalInterval, ...]:
    return tuple(
        sorted(
            values,
            key=lambda item: (
                item.start_utc,
                item.end_utc,
                item.interval_id,
                item.full_state_sha256,
            ),
        )
    )


def _interval_without_set_digest(interval: CanonicalInterval) -> JsonObject:
    value = interval.to_json()
    value.pop("candidate_set_sha256")
    return value


def candidate_set_digest(
    candidate_manifest_sha256: str,
    declared_dates: Sequence[str],
    intervals: Sequence[CanonicalInterval],
) -> str:
    """Digest a candidate set without creating a self-referential interval field."""

    return sha256_json(
        {
            "candidate_manifest_sha256": candidate_manifest_sha256,
            "declared_dates": sorted(declared_dates),
            "intervals": [
                _interval_without_set_digest(item) for item in _sort_intervals(intervals)
            ],
        }
    )


def parse_interval(value: object) -> CanonicalInterval:
    raw = _require_object(value, "invalid_interval_object")
    _require_exact_keys(
        raw,
        {
            "candidate_manifest_sha256",
            "candidate_set_sha256",
            "interval_id",
            "start_utc",
            "end_utc",
            "full_state_sha256",
            "civil_date",
        },
        "invalid_interval_fields",
    )
    interval = CanonicalInterval(
        candidate_manifest_sha256=_require_digest(
            raw["candidate_manifest_sha256"], "invalid_candidate_manifest_digest"
        ),
        candidate_set_sha256=_require_digest(
            raw["candidate_set_sha256"], "invalid_candidate_set_digest"
        ),
        interval_id=_require_string(raw["interval_id"], _INTERVAL_ID_RE, "invalid_interval_id"),
        start_utc=_parse_utc(raw["start_utc"]),
        end_utc=_parse_utc(raw["end_utc"]),
        full_state_sha256=_require_digest(raw["full_state_sha256"], "invalid_state_digest"),
        civil_date=_require_synthetic_date(raw["civil_date"]),
    )
    if interval.end_utc <= interval.start_utc:
        _fail("nonpositive_interval_width")
    return interval


def parse_candidate_set(value: object) -> CandidateSet:
    raw = _require_object(value, "invalid_candidate_set_object")
    _require_exact_keys(
        raw,
        {"candidate_manifest_sha256", "candidate_set_sha256", "declared_dates", "intervals"},
        "invalid_candidate_set_fields",
    )
    manifest_digest = _require_digest(
        raw["candidate_manifest_sha256"], "invalid_candidate_manifest_digest"
    )
    set_digest = _require_digest(raw["candidate_set_sha256"], "invalid_candidate_set_digest")
    date_values = _require_sequence(raw["declared_dates"], "invalid_declared_dates")
    dates = tuple(_require_synthetic_date(item) for item in date_values)
    interval_values = _require_sequence(raw["intervals"], "invalid_candidate_intervals")
    intervals = tuple(parse_interval(item) for item in interval_values)
    if not intervals or not dates:
        _fail("empty_candidate_domain")
    if len(dates) != len(set(dates)):
        _fail("duplicate_declared_date")
    if any(item.candidate_manifest_sha256 != manifest_digest for item in intervals):
        _fail("candidate_manifest_mismatch")
    if any(item.candidate_set_sha256 != set_digest for item in intervals):
        _fail("candidate_set_digest_mismatch")
    if any(item.civil_date not in dates for item in intervals):
        _fail("interval_outside_declared_dates")
    interval_ids = [item.interval_id for item in intervals]
    if len(interval_ids) != len(set(interval_ids)):
        _fail("duplicate_candidate_interval")
    for civil_date in dates:
        date_intervals = _sort_intervals(
            tuple(item for item in intervals if item.civil_date == civil_date)
        )
        if not date_intervals:
            _fail("declared_date_without_candidate_interval")
        adjacent_pairs = zip(date_intervals, date_intervals[1:], strict=False)
        if any(left.end_utc != right.start_utc for left, right in adjacent_pairs):
            _fail("candidate_domain_gap_or_overlap")
    globally_ordered = _sort_intervals(intervals)
    global_pairs = zip(globally_ordered, globally_ordered[1:], strict=False)
    if any(left.end_utc > right.start_utc for left, right in global_pairs):
        _fail("candidate_domain_gap_or_overlap")
    if candidate_set_digest(manifest_digest, dates, intervals) != set_digest:
        _fail("candidate_set_digest_mismatch")
    return CandidateSet(manifest_digest, set_digest, dates, intervals)


def parse_preconstructed_output(value: object) -> PreconstructedOutput:
    raw = _require_object(value, "invalid_output_object")
    _require_exact_keys(raw, {"output_kind", "selected_intervals"}, "invalid_output_fields")
    raw_kind = raw["output_kind"]
    if not isinstance(raw_kind, str):
        _fail("invalid_output_kind")
    try:
        kind = OutputKind(raw_kind)
    except (TypeError, ValueError):
        _fail("invalid_output_kind")
    selected_values = _require_sequence(raw["selected_intervals"], "invalid_selected_intervals")
    selected = tuple(parse_interval(item) for item in selected_values)
    return PreconstructedOutput(kind, selected)


def parse_method_specification(value: object) -> MethodSpecification:
    raw = _require_object(value, "invalid_method_specification_object")
    _require_exact_keys(
        raw,
        {
            "study_design_contract_sha256",
            "preserved_metric_semantics_v2_contract_sha256",
            "operative_metric_semantics_v3_contract_sha256",
            "s_i_origin",
            "selection_procedure_present",
            "method_specification_sha256",
        },
        "invalid_method_specification_fields",
    )
    v1 = _require_digest(raw["study_design_contract_sha256"], "invalid_v1_contract_digest")
    v2 = _require_digest(
        raw["preserved_metric_semantics_v2_contract_sha256"],
        "invalid_v2_contract_digest",
    )
    v3 = _require_digest(
        raw["operative_metric_semantics_v3_contract_sha256"],
        "invalid_v3_contract_digest",
    )
    if v1 != V1_CONTRACT_SHA256 or v2 != V2_CONTRACT_SHA256 or v3 != V3_CONTRACT_SHA256:
        _fail("contract_digest_mismatch")
    if raw["s_i_origin"] != "preconstructed_test_vector":
        _fail("output_not_preconstructed")
    _require_bool(raw["selection_procedure_present"], False, "selection_procedure_prohibited")
    embedded = _require_digest(raw["method_specification_sha256"], "invalid_method_digest")
    payload = dict(raw)
    payload.pop("method_specification_sha256")
    if sha256_json(payload) != embedded:
        _fail("method_specification_digest_mismatch")
    return MethodSpecification(v1, v2, v3, "preconstructed_test_vector", False, embedded)


def parse_component_assignments(value: object) -> tuple[ComponentAssignment, ...]:
    values = _require_sequence(value, "invalid_component_assignments")
    assignments: list[ComponentAssignment] = []
    for item in values:
        raw = _require_object(item, "invalid_component_assignment_object")
        _require_exact_keys(
            raw,
            {"synthetic_observation_id", "component_id", "role"},
            "invalid_component_assignment_fields",
        )
        observation_id = _require_string(
            raw["synthetic_observation_id"], _SYNTHETIC_ID_RE, "invalid_synthetic_observation_id"
        )
        component_id = _require_string(
            raw["component_id"], _SYNTHETIC_ID_RE, "invalid_synthetic_component_id"
        )
        raw_role = raw["role"]
        if not isinstance(raw_role, str):
            _fail("invalid_data_role")
        try:
            role = DataRole(raw_role)
        except (TypeError, ValueError):
            _fail("invalid_data_role")
        assignments.append(ComponentAssignment(observation_id, component_id, role))
    if not assignments:
        _fail("empty_component_assignments")
    observation_ids = [item.synthetic_observation_id for item in assignments]
    if len(observation_ids) != len(set(observation_ids)):
        _fail("duplicate_synthetic_observation")
    roles_by_component: dict[str, set[DataRole]] = {}
    for item in assignments:
        roles_by_component.setdefault(item.component_id, set()).add(item.role)
    if any(len(roles) > 1 for roles in roles_by_component.values()):
        _fail("cross_role_connected_component")
    return tuple(assignments)


def parse_reference_bundle(value: object) -> ReferenceBundle:
    raw = _require_object(value, "invalid_reference_bundle_object")
    _require_exact_keys(raw, {"canonicalization_status", "sources"}, "invalid_reference_fields")
    status = raw["canonicalization_status"]
    if status not in {
        "canonical_half_open_utc",
        "no_eligible_reference",
        "reference_canonicalization_failed",
    }:
        _fail("invalid_reference_canonicalization_status")
    source_values = _require_sequence(raw["sources"], "invalid_reference_sources")
    sources: list[ReferenceSource] = []
    for item in source_values:
        raw_source = _require_object(item, "invalid_reference_source_object")
        _require_exact_keys(
            raw_source,
            {"source_id", "lineage_id", "start_utc", "end_utc"},
            "invalid_reference_source_fields",
        )
        parsed = ReferenceSource(
            source_id=_require_string(
                raw_source["source_id"], _SOURCE_ID_RE, "invalid_synthetic_source_id"
            ),
            lineage_id=_require_string(
                raw_source["lineage_id"], _LINEAGE_ID_RE, "invalid_synthetic_lineage_id"
            ),
            start_utc=_parse_utc(raw_source["start_utc"]),
            end_utc=_parse_utc(raw_source["end_utc"]),
        )
        if parsed.end_utc <= parsed.start_utc:
            _fail("nonpositive_reference_width")
        sources.append(parsed)
    if status == "canonical_half_open_utc" and not sources:
        _fail("canonical_reference_requires_source")
    if status != "canonical_half_open_utc" and sources:
        _fail("inapplicable_reference_must_not_include_source")
    source_ids = [item.source_id for item in sources]
    if len(source_ids) != len(set(source_ids)):
        _fail("duplicate_reference_source_id")
    lineage_intervals: dict[str, tuple[datetime, datetime]] = {}
    for parsed_source in sources:
        existing = lineage_intervals.setdefault(
            parsed_source.lineage_id, parsed_source.interval_key()
        )
        if existing != parsed_source.interval_key():
            _fail("conflicting_same_lineage_extracts")
    return ReferenceBundle(status, tuple(sources))


def canonical_reference_custody_payload(value: Mapping[str, object]) -> JsonObject:
    payload = dict(value)
    payload.pop("reference_custody_sha256", None)
    return payload


def reference_custody_digest(value: Mapping[str, object]) -> str:
    return sha256_json(canonical_reference_custody_payload(value))


def parse_evaluator_reference_record(value: object) -> EvaluatorReferenceRecord:
    """Parse the closed evaluator-only schema after an authorized custody open."""

    raw = _require_object(value, "invalid_reference_custody_object")
    validate_no_prohibited_fields(raw)
    _require_exact_keys(raw, _REFERENCE_CUSTODY_KEYS, "invalid_reference_custody_fields")
    if raw["schema_version"] != "natal-time-synthetic-evaluator-reference-custody-v1":
        _fail("invalid_reference_custody_schema_version")
    custody_id = _require_string(raw["custody_id"], _CUSTODY_ID_RE, "invalid_synthetic_custody_id")
    _require_bool(raw["synthetic_only"], True, "fixture_not_conspicuously_synthetic")
    if raw["documentary_source_classification"] != "synthetic_auditable_record":
        _fail("invalid_reference_documentary_classification")
    if raw["precision_classification"] != "canonical_half_open_utc_microsecond":
        _fail("invalid_reference_precision_classification")
    if raw["custody_classification"] != "evaluator_only_sealed_reference":
        _fail("invalid_reference_custody_classification")
    mutation_mode = raw["mutation_test_mode"]
    if mutation_mode not in {"none", "mutate_after_authorized_open"}:
        _fail("invalid_reference_custody_classification")
    embedded = _require_digest(raw["reference_custody_sha256"], "invalid_reference_custody_digest")
    if reference_custody_digest(raw) != embedded:
        _fail("invalid_reference_custody_digest")
    return EvaluatorReferenceRecord(
        custody_id=custody_id,
        reference_custody_sha256=embedded,
        reference=parse_reference_bundle(raw["reference"]),
        mutation_test_mode=mutation_mode,
    )


_CUSTODY_LOADERS: Final[WeakKeyDictionary[object, Callable[[], object]]] = WeakKeyDictionary()


class EvaluatorReferenceCustody:
    """Evaluator-only loader with an observable, fail-closed access boundary.

    Construction stores only an opaque callable. It performs no reference operation and exposes
    no locator, byte count, digest, metadata, or enumeration surface. The callable is invoked
    only after a session-issued capability proves that ``S_i`` is committed.
    """

    __slots__ = (
        "_phase",
        "_operations",
        "_attempts",
        "_opened_raw",
        "_opened_record",
        "_opened_payload_digest",
        "_opened_s_i_commitment_sha256",
        "__weakref__",
    )

    def __init__(self, loader: Callable[[], object]) -> None:
        _CUSTODY_LOADERS[self] = loader
        self._phase = ReferenceCustodyPhase.SEALED
        self._operations: list[str] = []
        self._attempts: list[str] = []
        self._opened_raw: object | None = None
        self._opened_record: EvaluatorReferenceRecord | None = None
        self._opened_payload_digest: str | None = None
        self._opened_s_i_commitment_sha256: str | None = None

    @property
    def phase(self) -> ReferenceCustodyPhase:
        return self._phase

    @property
    def operation_counts(self) -> Mapping[str, int]:
        return {
            operation: self._operations.count(operation) for operation in REFERENCE_OPERATION_CODES
        }

    @property
    def access_state_digest(self) -> str:
        return sha256_json(
            {
                "phase": self._phase.value,
                "operations": [
                    {"sequence": index + 1, "operation": operation}
                    for index, operation in enumerate(self._operations)
                ],
                "rejected_attempts": [
                    {"sequence": index + 1, "attempt": attempt}
                    for index, attempt in enumerate(self._attempts)
                ],
            }
        )

    def reject_unauthorized_attempt(self, attempt: str) -> NoReturn:
        """Reject an early probe without touching the loader or reference object."""

        code = _EARLY_REFERENCE_ATTEMPT_CODES.get(attempt)
        if code is None:
            raise ValueError("uncontrolled evaluator-reference access attempt")
        self._attempts.append(attempt)
        _fail(code)

    def open(self, capability: object) -> _OpenedEvaluatorReference:
        if self._phase is not ReferenceCustodyPhase.SEALED:
            _fail("invalid_reference_access_capability")
        if not isinstance(capability, _ReferenceAccessCapability):
            _fail("invalid_reference_access_capability")
        capability._authorize()
        loader = _CUSTODY_LOADERS.get(self)
        if loader is None:
            _fail("invalid_reference_access_capability")
        self._operations.extend(("addressability", "open", "read"))
        try:
            raw = deepcopy(loader())
        finally:
            _CUSTODY_LOADERS.pop(self, None)
        self._operations.append("parse")
        try:
            record = parse_evaluator_reference_record(raw)
            self._operations.extend(("serialization", "hash"))
            self._operations.extend(("serialization", "hash"))
            exact_opened_digest = sha256_json(raw)
        except VerificationError:
            self._phase = ReferenceCustodyPhase.INVALIDATED
            raise
        self._opened_raw = raw
        self._opened_record = record
        self._opened_payload_digest = exact_opened_digest
        self._opened_s_i_commitment_sha256 = capability.s_i_commitment_sha256
        self._phase = ReferenceCustodyPhase.OPENED
        return _OpenedEvaluatorReference(
            _OPENED_REFERENCE_ISSUER,
            record,
            self.access_state_digest,
            capability.s_i_commitment_sha256,
            preissue_integrity_rechecked=False,
        )

    def verify_unchanged_after_access(self) -> _OpenedEvaluatorReference:
        """Invalidate custody if the exact evaluator-only payload changes after opening."""

        if self._phase is not ReferenceCustodyPhase.OPENED or self._opened_raw is None:
            _fail("invalid_reference_access_capability")
        self._operations.extend(("serialization", "hash"))
        try:
            cached = sha256_json(
                _require_object(self._opened_raw, "invalid_reference_custody_object")
            )
        except VerificationError:
            self._phase = ReferenceCustodyPhase.INVALIDATED
            _fail("t_i_mutated_after_evaluator_access")
        if cached != self._opened_payload_digest:
            self._phase = ReferenceCustodyPhase.INVALIDATED
            _fail("t_i_mutated_after_evaluator_access")
        if self._opened_record is None or self._opened_s_i_commitment_sha256 is None:
            self._phase = ReferenceCustodyPhase.INVALIDATED
            _fail("invalid_reference_access_capability")
        return _OpenedEvaluatorReference(
            _OPENED_REFERENCE_ISSUER,
            self._opened_record,
            self.access_state_digest,
            self._opened_s_i_commitment_sha256,
            preissue_integrity_rechecked=True,
        )

    def apply_synthetic_mutation_probe(self) -> NoReturn:
        """Mutate a fixed synthetic test vector, then prove custody detects it."""

        if self._phase is not ReferenceCustodyPhase.OPENED or self._opened_raw is None:
            _fail("invalid_reference_access_capability")
        if self._opened_record is None or (
            self._opened_record.mutation_test_mode != "mutate_after_authorized_open"
        ):
            raise ValueError("synthetic mutation probe not declared")
        raw = cast(JsonObject, self._opened_raw)
        reference = cast(JsonObject, raw["reference"])
        sources = cast(list[JsonObject], reference["sources"])
        if not sources:
            raise ValueError("synthetic mutation probe requires a source")
        sources[0]["end_utc"] = "2099-01-01T02:00:00.000001Z"
        self.verify_unchanged_after_access()
        raise AssertionError("synthetic T_i mutation was not detected")


def validate_preregistration_sections(value: Mapping[str, object]) -> PreregistrationValidation:
    """Require exact controlled IDs; headings, prose, and measurement content are rejected."""

    required_fields = {
        "schema_version",
        "required_singletons",
        *PREREGISTRATION_IDENTIFIER_SETS,
    }
    unexpected_fields = set(value) - required_fields
    missing_fields = required_fields - set(value)
    missing: set[str] = {f"field:{item}" for item in missing_fields}
    duplicates: set[str] = set()
    unexpected: set[str] = {f"field:{item}" for item in unexpected_fields}
    if value.get("schema_version") != "natal-time-preregistration-structure-v1":
        unexpected.add("schema_version:value")

    expected_sets = {
        "required_singletons": PREREGISTRATION_REQUIRED_SINGLETONS,
        **PREREGISTRATION_IDENTIFIER_SETS,
    }
    for field, expected in expected_sets.items():
        raw_values = value.get(field)
        if not isinstance(raw_values, list) or not all(
            isinstance(item, str) for item in raw_values
        ):
            missing.add(f"set:{field}")
            continue
        strings = cast(list[str], raw_values)
        seen: set[str] = set()
        for item in strings:
            if item in seen:
                duplicates.add(f"{field}:{item}")
            seen.add(item)
        expected_values = set(expected)
        missing.update(f"{field}:{item}" for item in expected_values - seen)
        unexpected.update(f"{field}:{item}" for item in seen - expected_values)
    return PreregistrationValidation(
        valid=not missing and not duplicates and not unexpected,
        missing_sections=tuple(sorted(missing)),
        duplicate_sections=tuple(sorted(duplicates)),
        unexpected_sections=tuple(sorted(unexpected)),
    )


def validate_no_prohibited_fields(value: object) -> None:
    """Reject personal/free-text/relationship fields and inferential/scalar output fields."""

    def visit(item: object) -> None:
        if isinstance(item, Mapping):
            for raw_key, child in item.items():
                if not isinstance(raw_key, str):
                    _fail("non_string_field_name")
                lowered = raw_key.lower()
                if any(fragment in lowered for fragment in FORBIDDEN_FIELD_FRAGMENTS):
                    _fail("prohibited_personal_or_free_text_field")
                if any(fragment in lowered for fragment in PROHIBITED_OUTPUT_FRAGMENTS):
                    _fail("prohibited_inferential_or_scalar_output_field")
                visit(child)
        elif isinstance(item, list):
            for child in item:
                visit(child)

    visit(value)


def canonical_inference_visible_fixture_payload(value: Mapping[str, object]) -> JsonObject:
    """Canonicalize an inference-visible fixture containing no reference material."""

    fixture = dict(value)
    fixture.pop("inference_visible_fixture_digest", None)
    candidate = dict(_require_object(fixture["candidate_set"], "invalid_candidate_set_object"))
    candidate["declared_dates"] = sorted(cast(list[object], candidate["declared_dates"]), key=str)
    candidate["intervals"] = sorted(
        cast(list[object], candidate["intervals"]),
        key=lambda raw: (
            cast(Mapping[str, object], raw)["start_utc"],
            cast(Mapping[str, object], raw)["end_utc"],
            cast(Mapping[str, object], raw)["interval_id"],
        ),
    )
    fixture["candidate_set"] = candidate
    output = dict(_require_object(fixture["preconstructed_output"], "invalid_output_object"))
    output["selected_intervals"] = sorted(
        cast(list[object], output["selected_intervals"]),
        key=lambda raw: (
            cast(Mapping[str, object], raw)["start_utc"],
            cast(Mapping[str, object], raw)["end_utc"],
            cast(Mapping[str, object], raw)["interval_id"],
        ),
    )
    fixture["preconstructed_output"] = output
    fixture["component_assignments"] = sorted(
        cast(list[object], fixture["component_assignments"]),
        key=lambda raw: (
            cast(Mapping[str, object], raw)["component_id"],
            cast(Mapping[str, object], raw)["synthetic_observation_id"],
        ),
    )
    return fixture


def inference_visible_fixture_digest(value: Mapping[str, object]) -> str:
    return sha256_json(canonical_inference_visible_fixture_payload(value))


def evaluator_version_packet(project_root: Path) -> JsonObject:
    """Bind evaluator identity to the exact local module and generator bytes."""

    files = [
        {"path": MODULE_PATH, "sha256": sha256_file(project_root / MODULE_PATH)},
        {"path": BUILDER_PATH, "sha256": sha256_file(project_root / BUILDER_PATH)},
    ]
    payload: JsonObject = {
        "schema_version": "natal-time-synthetic-evaluator-version-v1",
        "contract_bindings": {
            "preserved_v1_contract_sha256": V1_CONTRACT_SHA256,
            "preserved_v2_contract_sha256": V2_CONTRACT_SHA256,
            "operative_v3_contract_sha256": V3_CONTRACT_SHA256,
        },
        "source_files": files,
    }
    payload["evaluator_version_sha256"] = sha256_json(payload)
    return payload


def current_evaluator_version_sha256() -> str:
    project_root = Path(__file__).resolve().parents[3]
    packet = evaluator_version_packet(project_root)
    return cast(str, packet["evaluator_version_sha256"])


def _fraction_payload(numerator: int, denominator: int, unit: str) -> JsonObject:
    fraction = Fraction(numerator, denominator)
    return {
        "status": "applicable",
        f"selected_{unit}": numerator,
        f"candidate_{unit}": denominator,
        "fraction": f"{fraction.numerator}/{fraction.denominator}",
    }


def _boolean_not_applicable(status: str) -> JsonObject:
    return {"status": status, "value": None}


def _fraction_not_applicable(status: str, unit: str) -> JsonObject:
    return {
        "status": status,
        f"selected_{unit}": None,
        f"candidate_{unit}": None,
        "fraction": None,
    }


def _documentary_width_not_applicable(status: str) -> JsonObject:
    return {"status": status, "microseconds": None}


def _overlaps(
    left_start: datetime, left_end: datetime, right_start: datetime, right_end: datetime
) -> bool:
    return max(left_start, right_start) < min(left_end, right_end)


class EvaluationSession:
    """Ordered synthetic evaluation session with evaluator-only reference access."""

    def __init__(self) -> None:
        self.phase = SessionPhase.NEW
        self._candidate_set: CandidateSet | None = None
        self._method: MethodSpecification | None = None
        self._output: PreconstructedOutput | None = None
        self._opened_reference: _OpenedEvaluatorReference | None = None
        self._capability_seal = object()
        self._access_events: list[str] = []
        self._violations: list[str] = []

    @property
    def access_state_digest(self) -> str:
        return sha256_json(
            {
                "phase": self.phase.value,
                "events": [
                    {"sequence": index + 1, "event": event}
                    for index, event in enumerate(self._access_events)
                ],
                "violations": sorted(set(self._violations)),
            }
        )

    @property
    def violations(self) -> tuple[str, ...]:
        return tuple(sorted(set(self._violations)))

    def _invalidate(self, code: str) -> None:
        self._violations.append(code)
        self.phase = SessionPhase.INVALIDATED
        _fail(code)

    def freeze_candidate_domain(
        self,
        candidate_set: CandidateSet,
        assignments: tuple[ComponentAssignment, ...],
        contamination_status: str,
    ) -> None:
        if self.phase is not SessionPhase.NEW:
            self._invalidate("candidate_freeze_out_of_order")
        if contamination_status != "clean":
            self._invalidate("contaminated_connected_component")
        roles_by_component: dict[str, set[DataRole]] = {}
        for assignment in assignments:
            roles_by_component.setdefault(assignment.component_id, set()).add(assignment.role)
        if any(len(roles) > 1 for roles in roles_by_component.values()):
            self._invalidate("cross_role_connected_component")
        self._candidate_set = candidate_set
        self._access_events.append("candidate_domain_freeze")
        self.phase = SessionPhase.CANDIDATE_FROZEN

    def freeze_method_specification(self, method: MethodSpecification) -> None:
        if self.phase is not SessionPhase.CANDIDATE_FROZEN:
            self._invalidate("method_freeze_out_of_order")
        self._method = method
        self._access_events.append("study_method_specification_freeze")
        self.phase = SessionPhase.METHOD_FROZEN

    def commit_preconstructed_output(self, output: PreconstructedOutput) -> None:
        if self.phase is SessionPhase.REFERENCE_EXPOSED:
            self._invalidate("s_i_modified_after_t_i_exposure")
        if self.phase is not SessionPhase.METHOD_FROZEN:
            self._invalidate("s_i_commitment_out_of_order")
        candidate_set = self._candidate_set
        if candidate_set is None:
            self._invalidate("candidate_domain_missing")
        assert candidate_set is not None
        if output.output_kind is OutputKind.ABSTENTION:
            if output.selected_intervals:
                self._invalidate("abstention_must_not_select_intervals")
        else:
            if not output.selected_intervals:
                self._invalidate("invalid_output_empty_non_abstention")
            selected_payloads = [sha256_json(item.to_json()) for item in output.selected_intervals]
            if len(selected_payloads) != len(set(selected_payloads)):
                self._invalidate("duplicate_selected_interval")
            selected_ids = [item.interval_id for item in output.selected_intervals]
            if len(selected_ids) != len(set(selected_ids)):
                self._invalidate("duplicate_selected_interval")
            frozen_by_id = {item.interval_id: item for item in candidate_set.intervals}
            for selected in output.selected_intervals:
                frozen = frozen_by_id.get(selected.interval_id)
                if frozen is None:
                    enclosed = [
                        item
                        for item in candidate_set.intervals
                        if item.start_utc >= selected.start_utc and item.end_utc <= selected.end_utc
                    ]
                    if (
                        len(enclosed) > 1
                        and min(item.start_utc for item in enclosed) == selected.start_utc
                        and max(item.end_utc for item in enclosed) == selected.end_utc
                    ):
                        self._invalidate("manufactured_interval_not_allowed")
                    self._invalidate("foreign_or_manufactured_interval")
                assert frozen is not None
                if selected != frozen:
                    if (
                        selected.candidate_manifest_sha256 == frozen.candidate_manifest_sha256
                        and selected.candidate_set_sha256 == frozen.candidate_set_sha256
                        and selected.start_utc >= frozen.start_utc
                        and selected.end_utc <= frozen.end_utc
                        and (
                            selected.start_utc > frozen.start_utc
                            or selected.end_utc < frozen.end_utc
                        )
                    ):
                        self._invalidate("partial_interval_not_allowed")
                    self._invalidate("foreign_or_manufactured_interval")
        self._output = output
        self._access_events.append("preconstructed_s_i_commitment")
        self.phase = SessionPhase.OUTPUT_COMMITTED

    def release_reference_access_capability(self) -> _ReferenceAccessCapability:
        """Release the only evaluator-custody capability after exact ``S_i`` commitment."""

        if self.phase is not SessionPhase.OUTPUT_COMMITTED:
            self._invalidate("t_i_access_before_s_i_commitment")
        output = self._output
        assert output is not None
        return _ReferenceAccessCapability(
            _REFERENCE_CAPABILITY_ISSUER,
            self._capability_seal,
            sha256_json(output.canonical_payload()),
            self._authorize_reference_capability,
        )

    def _authorize_reference_capability(self, seal: object, commitment: str) -> None:
        output = self._output
        if (
            seal is not self._capability_seal
            or self.phase is not SessionPhase.OUTPUT_COMMITTED
            or output is None
            or commitment != sha256_json(output.canonical_payload())
        ):
            self._invalidate("invalid_reference_access_capability")

    def accept_opened_reference(self, opened: object) -> None:
        if self.phase is not SessionPhase.OUTPUT_COMMITTED:
            self._invalidate("invalid_reference_access_capability")
        output = self._output
        if (
            not isinstance(opened, _OpenedEvaluatorReference)
            or opened.preissue_integrity_rechecked
            or output is None
            or opened.s_i_commitment_sha256 != sha256_json(output.canonical_payload())
        ):
            self._invalidate("invalid_reference_access_capability")
        assert isinstance(opened, _OpenedEvaluatorReference)
        self._opened_reference = opened
        self._access_events.append("evaluator_only_t_i_access")
        self.phase = SessionPhase.REFERENCE_EXPOSED

    def accept_preissue_reference_integrity_recheck(self, opened: object) -> None:
        current = self._opened_reference
        if (
            self.phase is not SessionPhase.REFERENCE_EXPOSED
            or current is None
            or not isinstance(opened, _OpenedEvaluatorReference)
            or not opened.preissue_integrity_rechecked
            or opened.record != current.record
            or opened.s_i_commitment_sha256 != current.s_i_commitment_sha256
        ):
            self._invalidate("invalid_reference_access_capability")
        assert isinstance(opened, _OpenedEvaluatorReference)
        self._opened_reference = opened

    def attempt_output_recommit(self, output: PreconstructedOutput) -> None:
        """Represent a mutation attempt; post-reference attempts invalidate permanently."""

        if self.phase is SessionPhase.REFERENCE_EXPOSED:
            self._access_events.append("post_reference_s_i_mutation_attempt")
            self._invalidate("s_i_modified_after_t_i_exposure")
        self.commit_preconstructed_output(output)

    def _adjudicate_reference(self) -> tuple[str, ReferenceSource | None]:
        opened = self._opened_reference
        if opened is None:
            self._invalidate("reference_not_exposed")
        assert opened is not None
        reference = opened.record.reference
        if reference.canonicalization_status == "no_eligible_reference":
            return ("not_applicable_no_eligible_reference", None)
        if reference.canonicalization_status == "reference_canonicalization_failed":
            return ("not_applicable_reference_canonicalization_failed", None)
        distinct_intervals = {item.interval_key() for item in reference.sources}
        if len(distinct_intervals) != 1:
            return ("not_applicable_conflicting_eligible_sources", None)
        return ("applicable", reference.sources[0])

    def _reference_domain_status(self, reference: ReferenceSource) -> str:
        candidate_set = self._candidate_set
        assert candidate_set is not None
        overlap_width = 0
        for interval in candidate_set.intervals:
            overlap_start = max(interval.start_utc, reference.start_utc)
            overlap_end = min(interval.end_utc, reference.end_utc)
            if overlap_start < overlap_end:
                overlap_width += _timedelta_microseconds(overlap_start, overlap_end)
        reference_width = _timedelta_microseconds(reference.start_utc, reference.end_utc)
        if overlap_width == reference_width:
            return "reference_domain_compatible"
        if overlap_width > 0:
            return "reference_domain_partially_incompatible"
        return "reference_domain_incompatible"

    def compute_metrics(self) -> JsonObject:
        if self.phase is not SessionPhase.REFERENCE_EXPOSED:
            self._invalidate("metric_receipt_before_t_i_access")
        opened = self._opened_reference
        if opened is None or not opened.preissue_integrity_rechecked:
            self._invalidate("invalid_reference_access_capability")
        candidate_set = self._candidate_set
        output = self._output
        assert candidate_set is not None and output is not None
        reference_status, operative_reference = self._adjudicate_reference()
        if operative_reference is None:
            return self._reference_failure_metrics(reference_status, output)
        documentary_width = _timedelta_microseconds(
            operative_reference.start_utc, operative_reference.end_utc
        )
        domain_status = self._reference_domain_status(operative_reference)
        if domain_status != "reference_domain_compatible":
            return self._reference_failure_metrics(
                f"not_applicable_{domain_status}",
                output,
                documentary_width=documentary_width,
            )
        if output.output_kind is OutputKind.ABSTENTION:
            status = "not_applicable_abstention"
            return {
                "reference_intersection": _boolean_not_applicable(status),
                "temporal_width_retained": _fraction_not_applicable(status, "width_microseconds"),
                "canonical_interval_count_retained": _fraction_not_applicable(
                    status, "interval_count"
                ),
                "unique_state_identity_count_retained": _fraction_not_applicable(
                    status, "unique_state_identity_count"
                ),
                "date_coverage": _fraction_not_applicable(status, "date_count"),
                "documentary_reference_width": {
                    "status": "applicable",
                    "microseconds": documentary_width,
                },
                "abstention": {"status": "applicable", "value": True},
            }
        selected = output.selected_intervals
        candidate_width = sum(item.width_microseconds for item in candidate_set.intervals)
        selected_width = sum(item.width_microseconds for item in selected)
        candidate_states = {item.full_state_sha256 for item in candidate_set.intervals}
        selected_states = {item.full_state_sha256 for item in selected}
        selected_dates = {item.civil_date for item in selected}
        intersects = any(
            _overlaps(
                item.start_utc,
                item.end_utc,
                operative_reference.start_utc,
                operative_reference.end_utc,
            )
            for item in selected
        )
        return {
            "reference_intersection": {"status": "applicable", "value": intersects},
            "temporal_width_retained": _fraction_payload(
                selected_width, candidate_width, "width_microseconds"
            ),
            "canonical_interval_count_retained": _fraction_payload(
                len(selected), len(candidate_set.intervals), "interval_count"
            ),
            "unique_state_identity_count_retained": _fraction_payload(
                len(selected_states), len(candidate_states), "unique_state_identity_count"
            ),
            "date_coverage": _fraction_payload(
                len(selected_dates), len(candidate_set.declared_dates), "date_count"
            ),
            "documentary_reference_width": {
                "status": "applicable",
                "microseconds": documentary_width,
            },
            "abstention": {"status": "applicable", "value": False},
        }

    def _reference_failure_metrics(
        self,
        status: str,
        output: PreconstructedOutput,
        *,
        documentary_width: int | None = None,
    ) -> JsonObject:
        return {
            "reference_intersection": _boolean_not_applicable(status),
            "temporal_width_retained": _fraction_not_applicable(status, "width_microseconds"),
            "canonical_interval_count_retained": _fraction_not_applicable(status, "interval_count"),
            "unique_state_identity_count_retained": _fraction_not_applicable(
                status, "unique_state_identity_count"
            ),
            "date_coverage": _fraction_not_applicable(status, "date_count"),
            "documentary_reference_width": (
                _documentary_width_not_applicable(status)
                if documentary_width is None
                else {"status": "applicable", "microseconds": documentary_width}
            ),
            "abstention": {
                "status": "applicable",
                "value": output.output_kind is OutputKind.ABSTENTION,
            },
        }

    def issue_receipt(
        self,
        *,
        fixture_id: str,
        inference_visible_fixture_digest: str,
        evaluator_version_sha256: str,
    ) -> JsonObject:
        candidate_set = self._candidate_set
        method = self._method
        output = self._output
        opened = self._opened_reference
        assert candidate_set is not None and method is not None and output is not None
        assert opened is not None
        if not opened.preissue_integrity_rechecked:
            self._invalidate("invalid_reference_access_capability")
        metrics = self.compute_metrics()
        self._access_events.append("metric_receipt")
        self.phase = SessionPhase.RECEIPT_ISSUED
        statuses = {
            cast(str, item["status"]) for item in metrics.values() if isinstance(item, dict)
        }
        reference_failure = any(
            status.startswith("not_applicable_reference") for status in statuses
        )
        evaluation_eligible = (
            not reference_failure
            and "not_applicable_conflicting_eligible_sources" not in statuses
            and "not_applicable_no_eligible_reference" not in statuses
        )
        _, operative_reference = self._adjudicate_reference()
        canonical_t_i_sha256: str | None = None
        if operative_reference is not None:
            canonical_t_i_sha256 = sha256_json(
                {
                    "start_utc": _format_utc(operative_reference.start_utc),
                    "end_utc": _format_utc(operative_reference.end_utc),
                }
            )
        custody_access_digest = opened.custody_access_state_sha256
        combined_access_digest = sha256_json(
            {
                "evaluation_session_access_state_sha256": self.access_state_digest,
                "reference_custody_access_state_sha256": custody_access_digest,
            }
        )
        contract_bindings = {
            "preserved_v1_contract_sha256": V1_CONTRACT_SHA256,
            "preserved_v2_contract_sha256": V2_CONTRACT_SHA256,
            "operative_v3_contract_sha256": V3_CONTRACT_SHA256,
        }
        common: JsonObject = {
            "synthetic_only": True,
            "fixture_id": fixture_id,
            "contract_bindings": contract_bindings,
            "inference_visible_fixture_digest": inference_visible_fixture_digest,
            "candidate_domain_freeze_sha256": candidate_set.candidate_set_sha256,
            "study_method_specification_sha256": method.method_specification_sha256,
            "s_i_commitment_sha256": sha256_json(output.canonical_payload()),
            "canonical_t_i_sha256": canonical_t_i_sha256,
            "reference_custody_sha256": opened.record.reference_custody_sha256,
            "reference_custody_access_state_sha256": custody_access_digest,
            "access_state_sha256": combined_access_digest,
            "evaluator_version_sha256": evaluator_version_sha256,
            "inference_or_selection_performed": False,
        }
        if operative_reference is not None:
            domain_status = self._reference_domain_status(operative_reference)
            if domain_status != "reference_domain_compatible":
                diagnostic: JsonObject = {
                    "schema_version": "natal-time-synthetic-reference-domain-diagnostic-v1",
                    "receipt_kind": "reference_domain_diagnostic",
                    **common,
                    "valid_reference_evaluation_receipt": False,
                    "reference_domain_status": domain_status,
                    "reference_intersection": _boolean_not_applicable(
                        f"not_applicable_{domain_status}"
                    ),
                    "documentary_reference_width": {
                        "status": "applicable",
                        "microseconds": _timedelta_microseconds(
                            operative_reference.start_utc, operative_reference.end_utc
                        ),
                    },
                }
                validate_no_prohibited_fields(diagnostic)
                diagnostic["receipt_sha256"] = sha256_json(diagnostic)
                return diagnostic
        payload: JsonObject = {
            "schema_version": "natal-time-synthetic-evaluation-receipt-v3",
            "receipt_kind": "descriptive_metric_receipt",
            **common,
            "evaluation_eligible": evaluation_eligible,
            "metrics": metrics,
            "metrics_sha256": sha256_json(metrics),
        }
        validate_no_prohibited_fields(payload)
        payload["receipt_sha256"] = sha256_json(payload)
        return payload


def build_rejection_receipt(
    *,
    fixture_id: str,
    inference_visible_fixture_digest: str,
    evaluator_version_sha256: str,
    access_state_sha256: str,
    violation_codes: Sequence[str],
) -> JsonObject:
    """Build an audit rejection; this is explicitly not a valid evaluation receipt."""

    codes = sorted(set(violation_codes))
    if not codes or any(code not in ALLOWED_VIOLATION_CODES for code in codes):
        raise ValueError("uncontrolled rejection violation code")
    payload: JsonObject = {
        "schema_version": "natal-time-synthetic-evaluation-rejection-v3",
        "receipt_kind": "fail_closed_rejection",
        "synthetic_only": True,
        "fixture_id": fixture_id,
        "valid_evaluation_receipt": False,
        "contract_bindings": {
            "preserved_v1_contract_sha256": V1_CONTRACT_SHA256,
            "preserved_v2_contract_sha256": V2_CONTRACT_SHA256,
            "operative_v3_contract_sha256": V3_CONTRACT_SHA256,
        },
        "inference_visible_fixture_digest": inference_visible_fixture_digest,
        "access_state_sha256": access_state_sha256,
        "evaluator_version_sha256": evaluator_version_sha256,
        "violation_codes": codes,
        "metrics_present": False,
        "inference_or_selection_performed": False,
    }
    validate_no_prohibited_fields(payload)
    payload["receipt_sha256"] = sha256_json(payload)
    return payload


def verify_receipt_self_hash(receipt: Mapping[str, object]) -> bool:
    payload = dict(receipt)
    embedded = payload.pop("receipt_sha256", None)
    return isinstance(embedded, str) and embedded == sha256_json(payload)


def _valid_digest_field(value: object) -> bool:
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None


def _valid_fraction_component(
    value: object,
    *,
    selected_field: str,
    candidate_field: str,
) -> bool:
    if not isinstance(value, Mapping):
        return False
    if set(value) != {"status", selected_field, candidate_field, "fraction"}:
        return False
    status = value["status"]
    if status == "applicable":
        selected = value[selected_field]
        candidate = value[candidate_field]
        fraction = value["fraction"]
        if (
            not isinstance(selected, int)
            or isinstance(selected, bool)
            or not isinstance(candidate, int)
            or isinstance(candidate, bool)
            or candidate <= 0
            or selected < 0
            or selected > candidate
            or not isinstance(fraction, str)
        ):
            return False
        expected = Fraction(selected, candidate)
        return fraction == f"{expected.numerator}/{expected.denominator}"
    return (
        isinstance(status, str)
        and status in METRIC_APPLICABILITY_STATUSES - {"applicable"}
        and value[selected_field] is None
        and value[candidate_field] is None
        and value["fraction"] is None
    )


def _valid_boolean_component(value: object, *, abstention: bool = False) -> bool:
    if not isinstance(value, Mapping) or set(value) != {"status", "value"}:
        return False
    status = value["status"]
    component_value = value["value"]
    if status == "applicable":
        return isinstance(component_value, bool)
    return (
        not abstention
        and isinstance(status, str)
        and status in METRIC_APPLICABILITY_STATUSES - {"applicable"}
        and component_value is None
    )


def _valid_documentary_width_component(value: object) -> bool:
    if not isinstance(value, Mapping) or set(value) != {"status", "microseconds"}:
        return False
    status = value["status"]
    width = value["microseconds"]
    if status == "applicable":
        return isinstance(width, int) and not isinstance(width, bool) and width > 0
    return (
        isinstance(status, str)
        and status in METRIC_APPLICABILITY_STATUSES - {"applicable"}
        and width is None
    )


def _valid_applicable_documentary_width(value: object) -> bool:
    return (
        isinstance(value, Mapping)
        and set(value) == {"status", "microseconds"}
        and value["status"] == "applicable"
        and isinstance(value["microseconds"], int)
        and not isinstance(value["microseconds"], bool)
        and value["microseconds"] > 0
    )


def _valid_metrics(value: object) -> bool:
    if not isinstance(value, Mapping) or set(value) != set(METRIC_COMPONENT_IDS):
        return False
    return (
        _valid_boolean_component(value["reference_intersection"])
        and _valid_fraction_component(
            value["temporal_width_retained"],
            selected_field="selected_width_microseconds",
            candidate_field="candidate_width_microseconds",
        )
        and _valid_fraction_component(
            value["canonical_interval_count_retained"],
            selected_field="selected_interval_count",
            candidate_field="candidate_interval_count",
        )
        and _valid_fraction_component(
            value["unique_state_identity_count_retained"],
            selected_field="selected_unique_state_identity_count",
            candidate_field="candidate_unique_state_identity_count",
        )
        and _valid_fraction_component(
            value["date_coverage"],
            selected_field="selected_date_count",
            candidate_field="candidate_date_count",
        )
        and _valid_documentary_width_component(value["documentary_reference_width"])
        and _valid_boolean_component(value["abstention"], abstention=True)
    )


def _metrics_evaluation_eligible(value: object) -> bool | None:
    if not isinstance(value, Mapping):
        return None
    reference = value.get("reference_intersection")
    abstention = value.get("abstention")
    documentary = value.get("documentary_reference_width")
    if not isinstance(reference, Mapping) or not isinstance(abstention, Mapping):
        return None
    if not isinstance(documentary, Mapping):
        return None
    reference_status = reference.get("status")
    abstention_value = abstention.get("value")
    component_statuses: set[object] = set()
    for name in (
        "temporal_width_retained",
        "canonical_interval_count_retained",
        "unique_state_identity_count_retained",
        "date_coverage",
    ):
        component = value.get(name)
        if not isinstance(component, Mapping):
            return None
        component_statuses.add(component.get("status"))
    if reference_status == "applicable" and abstention_value is False:
        return component_statuses == {"applicable"} and documentary.get("status") == "applicable"
    if reference_status == "not_applicable_abstention" and abstention_value is True:
        return (
            component_statuses == {"not_applicable_abstention"}
            and documentary.get("status") == "applicable"
        )
    reference_failures = METRIC_APPLICABILITY_STATUSES - {
        "applicable",
        "not_applicable_abstention",
    }
    if reference_status in reference_failures and isinstance(abstention_value, bool):
        if (
            component_statuses == {reference_status}
            and documentary.get("status") == reference_status
        ):
            return False
        return None
    return None


def verify_receipt(
    receipt: Mapping[str, object],
    *,
    expected_evaluator_version_sha256: str | None = None,
    expected_binding_values: Mapping[str, object] | None = None,
) -> bool:
    """Validate a receipt's closed schema and any supplied external bindings."""

    try:
        validate_no_prohibited_fields(receipt)
    except VerificationError:
        return False
    if not verify_receipt_self_hash(receipt):
        return False
    common_keys = {
        "schema_version",
        "receipt_kind",
        "synthetic_only",
        "fixture_id",
        "contract_bindings",
        "inference_visible_fixture_digest",
        "access_state_sha256",
        "evaluator_version_sha256",
        "inference_or_selection_performed",
        "receipt_sha256",
    }
    if receipt.get("synthetic_only") is not True:
        return False
    if receipt.get("inference_or_selection_performed") is not False:
        return False
    fixture_id = receipt.get("fixture_id")
    if not isinstance(fixture_id, str) or _SYNTHETIC_ID_RE.fullmatch(fixture_id) is None:
        return False
    bindings = receipt.get("contract_bindings")
    if bindings != {
        "preserved_v1_contract_sha256": V1_CONTRACT_SHA256,
        "preserved_v2_contract_sha256": V2_CONTRACT_SHA256,
        "operative_v3_contract_sha256": V3_CONTRACT_SHA256,
    }:
        return False
    if any(
        not _valid_digest_field(receipt.get(field))
        for field in (
            "inference_visible_fixture_digest",
            "access_state_sha256",
            "evaluator_version_sha256",
        )
    ):
        return False
    if (
        expected_evaluator_version_sha256 is not None
        and receipt.get("evaluator_version_sha256") != expected_evaluator_version_sha256
    ):
        return False
    if expected_binding_values is not None and any(
        key not in receipt or receipt[key] != value
        for key, value in expected_binding_values.items()
    ):
        return False
    kind = receipt.get("receipt_kind")
    if kind == "descriptive_metric_receipt":
        expected_keys = common_keys | {
            "evaluation_eligible",
            "candidate_domain_freeze_sha256",
            "study_method_specification_sha256",
            "s_i_commitment_sha256",
            "canonical_t_i_sha256",
            "reference_custody_sha256",
            "reference_custody_access_state_sha256",
            "metrics",
            "metrics_sha256",
        }
        if set(receipt) != expected_keys:
            return False
        if receipt.get("schema_version") != "natal-time-synthetic-evaluation-receipt-v3":
            return False
        if not isinstance(receipt.get("evaluation_eligible"), bool):
            return False
        if any(
            not _valid_digest_field(receipt.get(field))
            for field in (
                "candidate_domain_freeze_sha256",
                "study_method_specification_sha256",
                "s_i_commitment_sha256",
                "reference_custody_sha256",
                "reference_custody_access_state_sha256",
                "metrics_sha256",
            )
        ):
            return False
        canonical_t_i_sha256 = receipt.get("canonical_t_i_sha256")
        if canonical_t_i_sha256 is not None and not _valid_digest_field(canonical_t_i_sha256):
            return False
        metrics = receipt.get("metrics")
        eligible = _metrics_evaluation_eligible(metrics)
        return (
            _valid_metrics(metrics)
            and receipt.get("metrics_sha256") == sha256_json(metrics)
            and eligible is not None
            and receipt.get("evaluation_eligible") is eligible
        )
    if kind == "reference_domain_diagnostic":
        expected_keys = common_keys | {
            "valid_reference_evaluation_receipt",
            "candidate_domain_freeze_sha256",
            "study_method_specification_sha256",
            "s_i_commitment_sha256",
            "canonical_t_i_sha256",
            "reference_custody_sha256",
            "reference_custody_access_state_sha256",
            "reference_domain_status",
            "reference_intersection",
            "documentary_reference_width",
        }
        if set(receipt) != expected_keys:
            return False
        if receipt.get("schema_version") != "natal-time-synthetic-reference-domain-diagnostic-v1":
            return False
        status = receipt.get("reference_domain_status")
        if status not in {
            "reference_domain_partially_incompatible",
            "reference_domain_incompatible",
        }:
            return False
        expected_na = f"not_applicable_{status}"
        return (
            receipt.get("valid_reference_evaluation_receipt") is False
            and all(
                _valid_digest_field(receipt.get(field))
                for field in (
                    "candidate_domain_freeze_sha256",
                    "study_method_specification_sha256",
                    "s_i_commitment_sha256",
                    "canonical_t_i_sha256",
                    "reference_custody_sha256",
                    "reference_custody_access_state_sha256",
                )
            )
            and receipt.get("reference_intersection") == {"status": expected_na, "value": None}
            and _valid_applicable_documentary_width(receipt.get("documentary_reference_width"))
        )
    if kind == "fail_closed_rejection":
        expected_keys = common_keys | {
            "valid_evaluation_receipt",
            "violation_codes",
            "metrics_present",
        }
        if set(receipt) != expected_keys:
            return False
        if receipt.get("schema_version") != "natal-time-synthetic-evaluation-rejection-v3":
            return False
        codes = receipt.get("violation_codes")
        return (
            receipt.get("valid_evaluation_receipt") is False
            and receipt.get("metrics_present") is False
            and isinstance(codes, list)
            and bool(codes)
            and all(isinstance(code, str) for code in codes)
            and codes == sorted(set(codes))
            and set(cast(list[str], codes)) <= ALLOWED_VIOLATION_CODES
        )
    return False


def verify_separated_synthetic_fixture(
    inference_visible_value: object,
    evaluator_custody: EvaluatorReferenceCustody,
    *,
    evaluator_version_sha256: str,
) -> JsonObject:
    """Evaluate separated synthetic bundles without giving inference actors custody access."""

    if (
        _SHA256_RE.fullmatch(evaluator_version_sha256) is None
        or evaluator_version_sha256 != current_evaluator_version_sha256()
    ):
        _fail("invalid_evaluator_version_digest")
    session = EvaluationSession()
    fallback_id = "SYNTH-FIXTURE-REJECTED-INPUT"
    fixture_id = fallback_id
    visible_digest = sha256_json({"fixture_id": fallback_id})
    try:
        raw = _require_object(inference_visible_value, "invalid_fixture_object")
        validate_no_prohibited_fields(raw)
        _require_exact_keys(raw, _INFERENCE_FIXTURE_KEYS, "invalid_fixture_fields")
        if raw["schema_version"] != "natal-time-synthetic-inference-visible-fixture-v2":
            _fail("invalid_fixture_schema_version")
        fixture_id = _require_string(raw["fixture_id"], _SYNTHETIC_ID_RE, "invalid_fixture_id")
        _require_bool(raw["synthetic_only"], True, "fixture_not_conspicuously_synthetic")
        _require_bool(raw["preconstructed_s_i"], True, "preconstructed_output_flag_required")
        embedded_visible_digest = _require_digest(
            raw["inference_visible_fixture_digest"],
            "invalid_inference_visible_fixture_digest",
        )
        visible_digest = inference_visible_fixture_digest(raw)
        if embedded_visible_digest != visible_digest:
            _fail("inference_visible_fixture_digest_mismatch")
        candidate_set = parse_candidate_set(raw["candidate_set"])
        method = parse_method_specification(raw["method_specification"])
        output = parse_preconstructed_output(raw["preconstructed_output"])
        assignments = parse_component_assignments(raw["component_assignments"])
        contamination_status = raw["contamination_status"]
        if contamination_status not in {"clean", "method_changed_after_outcome_access"}:
            _fail("contaminated_connected_component")
        raw_plan = _require_sequence(raw["execution_plan"], "unknown_execution_event")
        if not all(isinstance(event, str) and event in _EXECUTION_EVENTS for event in raw_plan):
            _fail("unknown_execution_event")
        plan = cast(list[str], raw_plan)

        for event in plan:
            if event == "candidate_domain_freeze":
                session.freeze_candidate_domain(candidate_set, assignments, contamination_status)
            elif event == "study_method_specification_freeze":
                session.freeze_method_specification(method)
            elif event == "preconstructed_s_i_commitment":
                session.commit_preconstructed_output(output)
            elif event == "evaluator_only_t_i_access":
                capability = session.release_reference_access_capability()
                opened = evaluator_custody.open(capability)
                session.accept_opened_reference(opened)
            elif event == "early_reference_raw_byte_access_attempt":
                evaluator_custody.reject_unauthorized_attempt("raw_byte")
            elif event == "early_reference_digest_access_attempt":
                evaluator_custody.reject_unauthorized_attempt("digest")
            elif event == "early_reference_metadata_access_attempt":
                evaluator_custody.reject_unauthorized_attempt("metadata")
            elif event == "early_reference_alternate_loader_access_attempt":
                evaluator_custody.reject_unauthorized_attempt("alternate_loader")
            elif event == "post_reference_s_i_mutation_attempt":
                session.attempt_output_recommit(output)
            elif event == "post_reference_t_i_mutation_attempt":
                evaluator_custody.apply_synthetic_mutation_probe()
            elif event == "metric_receipt":
                session.accept_preissue_reference_integrity_recheck(
                    evaluator_custody.verify_unchanged_after_access()
                )
                return session.issue_receipt(
                    fixture_id=fixture_id,
                    inference_visible_fixture_digest=visible_digest,
                    evaluator_version_sha256=evaluator_version_sha256,
                )
        _fail("metric_receipt_missing")
    except VerificationError as error:
        return build_rejection_receipt(
            fixture_id=fixture_id,
            inference_visible_fixture_digest=visible_digest,
            evaluator_version_sha256=evaluator_version_sha256,
            access_state_sha256=sha256_json(
                {
                    "evaluation_session_access_state_sha256": session.access_state_digest,
                    "reference_custody_access_state_sha256": (
                        evaluator_custody.access_state_digest
                    ),
                }
            ),
            violation_codes=(error.code, *session.violations),
        )
