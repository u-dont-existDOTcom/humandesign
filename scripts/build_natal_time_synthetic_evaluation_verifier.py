"""Build separated synthetic inference and evaluator-custody verification artifacts."""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import cast

from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.natal_time.evaluation_contract import (
    ALLOWED_VIOLATION_CODES,
    BASELINE_IDS,
    FORBIDDEN_FIELD_FRAGMENTS,
    MEASUREMENT_REQUIREMENT_IDS,
    METRIC_COMPONENT_IDS,
    PREREGISTRATION_IDENTIFIER_SETS,
    PREREGISTRATION_REQUIRED_SINGLETONS,
    PROHIBITED_OUTPUT_FRAGMENTS,
    REFERENCE_OPERATION_CODES,
    V1_CONTRACT_SHA256,
    V2_CONTRACT_SHA256,
    V3_CONTRACT_SHA256,
    CanonicalInterval,
    EvaluatorReferenceCustody,
    candidate_set_digest,
    evaluator_version_packet,
    inference_visible_fixture_digest,
    reference_custody_digest,
    verify_separated_synthetic_fixture,
)
from hdmatch.util import canonical_json_bytes, sha256_bytes, sha256_json

JsonObject = dict[str, object]

INFERENCE_FIXTURE_SCHEMA_VERSION = "natal-time-synthetic-inference-visible-fixture-v2"
STATE_DIRECTORY = "state/NATAL-TIME-SYNTHETIC-EVALUATION-V1"


@dataclass(frozen=True, slots=True)
class FixturePair:
    inference_visible: JsonObject
    evaluator_reference: JsonObject


@dataclass(frozen=True, slots=True)
class GeneratedBundle:
    inference_schema: JsonObject
    evaluator_schema: JsonObject
    fixture_pairs: tuple[FixturePair, ...]
    receipts: tuple[JsonObject, ...]
    inference_manifest: JsonObject
    evaluator_manifest: JsonObject
    evaluation_manifest: JsonObject


def _utc(day: str, time: str) -> str:
    return f"{day}T{time}.000000Z"


def _state_digest(code: str) -> str:
    return sha256_json({"schema_version": "synthetic-state-code-v1", "code": code})


def _parse_builder_utc(value: str) -> datetime:
    return datetime.fromisoformat(value[:-1] + "+00:00")


def _build_candidate_set() -> JsonObject:
    manifest_sha256 = sha256_json(
        {
            "schema_version": "synthetic-candidate-manifest-v1",
            "domain_code": "SYNTH-DOMAIN-NONCONSECUTIVE-DATES",
        }
    )
    zero = "0" * 64
    specifications = (
        (
            "SYNTH-INTERVAL-A",
            _utc("2099-01-01", "00:00:00"),
            _utc("2099-01-01", "06:00:00"),
            "SYNTH-STATE-A",
            "2099-01-01",
        ),
        (
            "SYNTH-INTERVAL-B",
            _utc("2099-01-01", "06:00:00"),
            _utc("2099-01-01", "12:00:00"),
            "SYNTH-STATE-B",
            "2099-01-01",
        ),
        (
            "SYNTH-INTERVAL-C",
            _utc("2099-01-01", "12:00:00"),
            _utc("2099-01-01", "18:00:00"),
            "SYNTH-STATE-A",
            "2099-01-01",
        ),
        (
            "SYNTH-INTERVAL-F",
            _utc("2099-01-01", "18:00:00"),
            _utc("2099-01-02", "00:00:00"),
            "SYNTH-STATE-D",
            "2099-01-01",
        ),
        (
            "SYNTH-INTERVAL-D",
            _utc("2099-01-03", "00:00:00"),
            _utc("2099-01-03", "12:00:00"),
            "SYNTH-STATE-C",
            "2099-01-03",
        ),
        (
            "SYNTH-INTERVAL-E",
            _utc("2099-01-03", "12:00:00"),
            _utc("2099-01-04", "00:00:00"),
            "SYNTH-STATE-C",
            "2099-01-03",
        ),
    )
    provisional = tuple(
        CanonicalInterval(
            candidate_manifest_sha256=manifest_sha256,
            candidate_set_sha256=zero,
            interval_id=interval_id,
            start_utc=_parse_builder_utc(start),
            end_utc=_parse_builder_utc(end),
            full_state_sha256=_state_digest(state),
            civil_date=civil_date,
        )
        for interval_id, start, end, state, civil_date in specifications
    )
    declared_dates = ("2099-01-01", "2099-01-03")
    set_sha256 = candidate_set_digest(manifest_sha256, declared_dates, provisional)
    intervals: list[JsonObject] = []
    for item in provisional:
        raw = item.to_json()
        raw["candidate_set_sha256"] = set_sha256
        intervals.append(raw)
    return {
        "candidate_manifest_sha256": manifest_sha256,
        "candidate_set_sha256": set_sha256,
        "declared_dates": list(declared_dates),
        "intervals": intervals,
    }


def _method_specification() -> JsonObject:
    payload: JsonObject = {
        "study_design_contract_sha256": V1_CONTRACT_SHA256,
        "preserved_metric_semantics_v2_contract_sha256": V2_CONTRACT_SHA256,
        "operative_metric_semantics_v3_contract_sha256": V3_CONTRACT_SHA256,
        "s_i_origin": "preconstructed_test_vector",
        "selection_procedure_present": False,
    }
    payload["method_specification_sha256"] = sha256_json(payload)
    return payload


def _candidate_set_for_dates(candidate_set: JsonObject, dates: tuple[str, ...]) -> JsonObject:
    manifest = cast(str, candidate_set["candidate_manifest_sha256"])
    raw_intervals = [
        item
        for item in cast(list[JsonObject], candidate_set["intervals"])
        if item["civil_date"] in dates
    ]
    zero = "0" * 64
    provisional = tuple(
        CanonicalInterval(
            candidate_manifest_sha256=manifest,
            candidate_set_sha256=zero,
            interval_id=cast(str, item["interval_id"]),
            start_utc=_parse_builder_utc(cast(str, item["start_utc"])),
            end_utc=_parse_builder_utc(cast(str, item["end_utc"])),
            full_state_sha256=cast(str, item["full_state_sha256"]),
            civil_date=cast(str, item["civil_date"]),
        )
        for item in raw_intervals
    )
    set_sha256 = candidate_set_digest(manifest, dates, provisional)
    intervals: list[JsonObject] = []
    for item in provisional:
        raw = item.to_json()
        raw["candidate_set_sha256"] = set_sha256
        intervals.append(raw)
    return {
        "candidate_manifest_sha256": manifest,
        "candidate_set_sha256": set_sha256,
        "declared_dates": list(dates),
        "intervals": intervals,
    }


def _assignment(role: str = "locked_validation") -> list[JsonObject]:
    return [
        {
            "synthetic_observation_id": "SYNTH-OBSERVATION-A",
            "component_id": "SYNTH-COMPONENT-A",
            "role": role,
        }
    ]


def _reference(start: str, end: str) -> JsonObject:
    return {
        "canonicalization_status": "canonical_half_open_utc",
        "sources": [
            {
                "source_id": "SYNTH-SOURCE-A",
                "lineage_id": "SYNTH-LINEAGE-A",
                "start_utc": start,
                "end_utc": end,
            }
        ],
    }


def _standard_plan() -> list[str]:
    return [
        "candidate_domain_freeze",
        "study_method_specification_freeze",
        "preconstructed_s_i_commitment",
        "evaluator_only_t_i_access",
        "metric_receipt",
    ]


def _output(candidate_set: JsonObject, interval_ids: tuple[str, ...]) -> JsonObject:
    intervals = cast(list[JsonObject], candidate_set["intervals"])
    by_id = {cast(str, item["interval_id"]): item for item in intervals}
    return {
        "output_kind": "candidate_subset",
        "selected_intervals": [deepcopy(by_id[item]) for item in interval_ids],
    }


def _inference_fixture(
    fixture_id: str,
    candidate_set: JsonObject,
    output: JsonObject,
    *,
    assignments: list[JsonObject] | None = None,
    contamination_status: str = "clean",
    execution_plan: list[str] | None = None,
) -> JsonObject:
    payload: JsonObject = {
        "schema_version": INFERENCE_FIXTURE_SCHEMA_VERSION,
        "fixture_id": fixture_id,
        "synthetic_only": True,
        "preconstructed_s_i": True,
        "candidate_set": deepcopy(candidate_set),
        "method_specification": _method_specification(),
        "preconstructed_output": output,
        "component_assignments": assignments if assignments is not None else _assignment(),
        "contamination_status": contamination_status,
        "execution_plan": execution_plan if execution_plan is not None else _standard_plan(),
    }
    payload["inference_visible_fixture_digest"] = inference_visible_fixture_digest(payload)
    return payload


def _evaluator_reference(
    custody_id: str,
    reference: JsonObject,
    *,
    mutation_test_mode: str = "none",
) -> JsonObject:
    payload: JsonObject = {
        "schema_version": "natal-time-synthetic-evaluator-reference-custody-v1",
        "custody_id": custody_id,
        "synthetic_only": True,
        "documentary_source_classification": "synthetic_auditable_record",
        "precision_classification": "canonical_half_open_utc_microsecond",
        "custody_classification": "evaluator_only_sealed_reference",
        "reference": reference,
        "mutation_test_mode": mutation_test_mode,
    }
    payload["reference_custody_sha256"] = reference_custody_digest(payload)
    return payload


def _pair(
    sequence: int,
    fixture_id: str,
    candidate_set: JsonObject,
    output: JsonObject,
    reference: JsonObject,
    **options: object,
) -> FixturePair:
    return FixturePair(
        _inference_fixture(
            fixture_id,
            candidate_set,
            output,
            assignments=cast(list[JsonObject] | None, options.get("assignments")),
            contamination_status=cast(str, options.get("contamination_status", "clean")),
            execution_plan=cast(list[str] | None, options.get("execution_plan")),
        ),
        _evaluator_reference(
            f"SYNTH-CUSTODY-{sequence:03d}",
            reference,
            mutation_test_mode=cast(str, options.get("mutation_test_mode", "none")),
        ),
    )


def build_fixture_pairs() -> tuple[FixturePair, ...]:
    """Return fixed vectors covering Phase-1 plus the separated-custody boundary."""

    candidate_set = _build_candidate_set()
    intervals = cast(list[JsonObject], candidate_set["intervals"])
    full_ids = tuple(cast(str, item["interval_id"]) for item in intervals)
    ordinary = _reference(_utc("2099-01-01", "01:00:00"), _utc("2099-01-01", "02:00:00"))
    specs: list[tuple[str, JsonObject, JsonObject, dict[str, object]]] = [
        ("SYNTH-FIXTURE-FULL-C", _output(candidate_set, full_ids), ordinary, {}),
        (
            "SYNTH-FIXTURE-ABSTENTION",
            {"output_kind": "abstention", "selected_intervals": []},
            ordinary,
            {},
        ),
        (
            "SYNTH-FIXTURE-BOUNDARY-TOUCH",
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            _reference(_utc("2099-01-01", "06:00:00"), _utc("2099-01-01", "07:00:00")),
            {},
        ),
        (
            "SYNTH-FIXTURE-REPEATED-STATE",
            _output(candidate_set, ("SYNTH-INTERVAL-A", "SYNTH-INTERVAL-C")),
            ordinary,
            {},
        ),
        (
            "SYNTH-FIXTURE-MULTIPLE-DATES",
            _output(candidate_set, ("SYNTH-INTERVAL-B", "SYNTH-INTERVAL-D")),
            _reference(_utc("2099-01-03", "01:00:00"), _utc("2099-01-03", "02:00:00")),
            {},
        ),
        (
            "SYNTH-FIXTURE-WIDE-REFERENCE",
            _output(candidate_set, ("SYNTH-INTERVAL-A", "SYNTH-INTERVAL-B")),
            _reference(_utc("2099-01-01", "01:00:00"), _utc("2099-01-01", "23:00:00")),
            {},
        ),
        (
            "SYNTH-FIXTURE-PARTIAL-REFERENCE-ONE-MICROSECOND",
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            _reference("2098-12-31T23:59:00.000000Z", "2099-01-01T00:00:00.000001Z"),
            {},
        ),
        (
            "SYNTH-FIXTURE-REFERENCE-CONTAINED-ACROSS-ADJACENT",
            _output(candidate_set, ("SYNTH-INTERVAL-A", "SYNTH-INTERVAL-B")),
            _reference(_utc("2099-01-01", "05:00:00"), _utc("2099-01-01", "07:00:00")),
            {},
        ),
        (
            "SYNTH-FIXTURE-REFERENCE-EXTENDS-AFTER-DOMAIN",
            _output(candidate_set, ("SYNTH-INTERVAL-F",)),
            _reference(_utc("2099-01-01", "23:00:00"), _utc("2099-01-02", "01:00:00")),
            {},
        ),
        (
            "SYNTH-FIXTURE-REFERENCE-EXTENDS-BOTH-DOMAIN-ENDS",
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            _reference(_utc("2098-12-31", "23:00:00"), _utc("2099-01-02", "01:00:00")),
            {},
        ),
        (
            "SYNTH-FIXTURE-MULTIDATE-INCLUDED-DATE",
            _output(candidate_set, ("SYNTH-INTERVAL-D",)),
            _reference(_utc("2099-01-03", "03:00:00"), _utc("2099-01-03", "04:00:00")),
            {},
        ),
        (
            "SYNTH-FIXTURE-MULTIDATE-EXCLUDED-DATE",
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            _reference(_utc("2099-01-02", "03:00:00"), _utc("2099-01-02", "04:00:00")),
            {},
        ),
        (
            "SYNTH-FIXTURE-IDENTICAL-MULTIPLE-SOURCES",
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            {
                "canonicalization_status": "canonical_half_open_utc",
                "sources": [
                    {
                        "source_id": "SYNTH-SOURCE-A",
                        "lineage_id": "SYNTH-LINEAGE-A",
                        "start_utc": _utc("2099-01-01", "01:00:00"),
                        "end_utc": _utc("2099-01-01", "02:00:00"),
                    },
                    {
                        "source_id": "SYNTH-SOURCE-B",
                        "lineage_id": "SYNTH-LINEAGE-B",
                        "start_utc": _utc("2099-01-01", "01:00:00"),
                        "end_utc": _utc("2099-01-01", "02:00:00"),
                    },
                ],
            },
            {},
        ),
        (
            "SYNTH-FIXTURE-SOURCE-CONFLICT",
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            {
                "canonicalization_status": "canonical_half_open_utc",
                "sources": [
                    {
                        "source_id": "SYNTH-SOURCE-A",
                        "lineage_id": "SYNTH-LINEAGE-A",
                        "start_utc": _utc("2099-01-01", "01:00:00"),
                        "end_utc": _utc("2099-01-01", "02:00:00"),
                    },
                    {
                        "source_id": "SYNTH-SOURCE-B",
                        "lineage_id": "SYNTH-LINEAGE-B",
                        "start_utc": _utc("2099-01-01", "01:30:00"),
                        "end_utc": _utc("2099-01-01", "02:30:00"),
                    },
                ],
            },
            {},
        ),
        (
            "SYNTH-FIXTURE-DOMAIN-INCOMPATIBLE",
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            _reference("2098-12-31T23:00:00.000000Z", "2099-01-01T00:00:00.000000Z"),
            {},
        ),
        (
            "SYNTH-FIXTURE-NO-ELIGIBLE-REFERENCE",
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            {"canonicalization_status": "no_eligible_reference", "sources": []},
            {},
        ),
        (
            "SYNTH-FIXTURE-REFERENCE-CANONICALIZATION-FAILED",
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            {"canonicalization_status": "reference_canonicalization_failed", "sources": []},
            {},
        ),
        (
            "SYNTH-FIXTURE-EMPTY-NON-ABSTENTION",
            {"output_kind": "candidate_subset", "selected_intervals": []},
            ordinary,
            {},
        ),
    ]
    partial = deepcopy(intervals[0])
    partial["end_utc"] = _utc("2099-01-01", "05:00:00")
    duplicate = deepcopy(intervals[0])
    foreign = deepcopy(intervals[0])
    foreign["interval_id"] = "SYNTH-INTERVAL-FOREIGN"
    manufactured = deepcopy(intervals[0])
    manufactured["interval_id"] = "SYNTH-INTERVAL-MANUFACTURED"
    manufactured["end_utc"] = cast(str, intervals[2]["end_utc"])
    specs.extend(
        [
            (
                "SYNTH-FIXTURE-PARTIAL-INTERVAL",
                {"output_kind": "candidate_subset", "selected_intervals": [partial]},
                ordinary,
                {},
            ),
            (
                "SYNTH-FIXTURE-DUPLICATE-INTERVAL",
                {"output_kind": "candidate_subset", "selected_intervals": [duplicate, duplicate]},
                ordinary,
                {},
            ),
            (
                "SYNTH-FIXTURE-REORDERED-WITH-DUPLICATION",
                {
                    "output_kind": "candidate_subset",
                    "selected_intervals": [
                        deepcopy(intervals[2]),
                        deepcopy(intervals[0]),
                        deepcopy(intervals[2]),
                    ],
                },
                ordinary,
                {},
            ),
            (
                "SYNTH-FIXTURE-FOREIGN-INTERVAL",
                {"output_kind": "candidate_subset", "selected_intervals": [foreign]},
                ordinary,
                {},
            ),
            (
                "SYNTH-FIXTURE-MANUFACTURED-INTERVAL",
                {"output_kind": "candidate_subset", "selected_intervals": [manufactured]},
                ordinary,
                {},
            ),
            (
                "SYNTH-FIXTURE-EARLY-REFERENCE-ACCESS",
                _output(candidate_set, ("SYNTH-INTERVAL-A",)),
                ordinary,
                {
                    "execution_plan": [
                        "candidate_domain_freeze",
                        "study_method_specification_freeze",
                        "evaluator_only_t_i_access",
                        "preconstructed_s_i_commitment",
                        "metric_receipt",
                    ]
                },
            ),
            (
                "SYNTH-FIXTURE-EARLY-REFERENCE-RAW-BYTE",
                _output(candidate_set, ("SYNTH-INTERVAL-A",)),
                ordinary,
                {
                    "execution_plan": [
                        "candidate_domain_freeze",
                        "study_method_specification_freeze",
                        "early_reference_raw_byte_access_attempt",
                        "preconstructed_s_i_commitment",
                        "metric_receipt",
                    ]
                },
            ),
            (
                "SYNTH-FIXTURE-EARLY-REFERENCE-DIGEST",
                _output(candidate_set, ("SYNTH-INTERVAL-A",)),
                ordinary,
                {
                    "execution_plan": [
                        "candidate_domain_freeze",
                        "study_method_specification_freeze",
                        "early_reference_digest_access_attempt",
                        "preconstructed_s_i_commitment",
                        "metric_receipt",
                    ]
                },
            ),
            (
                "SYNTH-FIXTURE-EARLY-REFERENCE-METADATA",
                _output(candidate_set, ("SYNTH-INTERVAL-A",)),
                ordinary,
                {
                    "execution_plan": [
                        "candidate_domain_freeze",
                        "study_method_specification_freeze",
                        "early_reference_metadata_access_attempt",
                        "preconstructed_s_i_commitment",
                        "metric_receipt",
                    ]
                },
            ),
            (
                "SYNTH-FIXTURE-EARLY-REFERENCE-ALTERNATE-LOADER",
                _output(candidate_set, ("SYNTH-INTERVAL-A",)),
                ordinary,
                {
                    "execution_plan": [
                        "candidate_domain_freeze",
                        "study_method_specification_freeze",
                        "early_reference_alternate_loader_access_attempt",
                        "preconstructed_s_i_commitment",
                        "metric_receipt",
                    ]
                },
            ),
            (
                "SYNTH-FIXTURE-POST-REFERENCE-OUTPUT-MUTATION",
                _output(candidate_set, ("SYNTH-INTERVAL-A",)),
                ordinary,
                {
                    "execution_plan": [
                        "candidate_domain_freeze",
                        "study_method_specification_freeze",
                        "preconstructed_s_i_commitment",
                        "evaluator_only_t_i_access",
                        "post_reference_s_i_mutation_attempt",
                        "metric_receipt",
                    ]
                },
            ),
            (
                "SYNTH-FIXTURE-POST-REFERENCE-T-MUTATION",
                _output(candidate_set, ("SYNTH-INTERVAL-A",)),
                ordinary,
                {
                    "execution_plan": [
                        "candidate_domain_freeze",
                        "study_method_specification_freeze",
                        "preconstructed_s_i_commitment",
                        "evaluator_only_t_i_access",
                        "post_reference_t_i_mutation_attempt",
                        "metric_receipt",
                    ],
                    "mutation_test_mode": "mutate_after_authorized_open",
                },
            ),
            (
                "SYNTH-FIXTURE-CROSS-ROLE-COMPONENT",
                _output(candidate_set, ("SYNTH-INTERVAL-A",)),
                ordinary,
                {
                    "assignments": [
                        {
                            "synthetic_observation_id": "SYNTH-OBSERVATION-A",
                            "component_id": "SYNTH-COMPONENT-A",
                            "role": "development",
                        },
                        {
                            "synthetic_observation_id": "SYNTH-OBSERVATION-B",
                            "component_id": "SYNTH-COMPONENT-A",
                            "role": "locked_validation",
                        },
                    ]
                },
            ),
            (
                "SYNTH-FIXTURE-CONTAMINATED-COMPONENT",
                _output(candidate_set, ("SYNTH-INTERVAL-A",)),
                ordinary,
                {"contamination_status": "method_changed_after_outcome_access"},
            ),
        ]
    )
    pairs = [
        _pair(index, fixture_id, candidate_set, output, reference, **options)
        for index, (fixture_id, output, reference, options) in enumerate(specs, 1)
    ]
    single_date = _candidate_set_for_dates(candidate_set, ("2099-01-01",))
    start = len(pairs) + 1
    pairs.extend(
        [
            _pair(
                start,
                "SYNTH-FIXTURE-DISCONNECTED-SAME-DATE",
                single_date,
                _output(single_date, ("SYNTH-INTERVAL-A", "SYNTH-INTERVAL-C")),
                ordinary,
            ),
            _pair(
                start + 1,
                "SYNTH-FIXTURE-DISCONNECTED-REORDERED",
                single_date,
                _output(single_date, ("SYNTH-INTERVAL-C", "SYNTH-INTERVAL-A")),
                ordinary,
            ),
            _pair(
                start + 2,
                "SYNTH-FIXTURE-DISCONNECTED-DUPLICATE",
                single_date,
                {
                    "output_kind": "candidate_subset",
                    "selected_intervals": [
                        deepcopy(cast(list[JsonObject], single_date["intervals"])[0]),
                        deepcopy(cast(list[JsonObject], single_date["intervals"])[2]),
                        deepcopy(cast(list[JsonObject], single_date["intervals"])[0]),
                    ],
                },
                ordinary,
            ),
        ]
    )
    return tuple(pairs)


def build_schemas(project_root: Path) -> tuple[JsonObject, JsonObject]:
    version = evaluator_version_packet(project_root)
    bindings = {
        "preserved_v1_contract_sha256": V1_CONTRACT_SHA256,
        "preserved_v2_contract_sha256": V2_CONTRACT_SHA256,
        "operative_v3_contract_sha256": V3_CONTRACT_SHA256,
    }
    inference: JsonObject = {
        "schema_version": "natal-time-synthetic-inference-visible-schema-v2",
        "synthetic_only": True,
        "contract_bindings": bindings,
        "exact_fixture_fields": [
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
        ],
        "evaluator_reference_addressable": False,
        "reference_dependent_fields_allowed": False,
        "candidate_domain_contiguous_per_declared_date": True,
        "s_i_adjacency_required": False,
        "reference_operation_codes_required_zero_before_s_i_commitment": list(
            REFERENCE_OPERATION_CODES
        ),
        "preregistration_contract": {
            "schema_version": "natal-time-preregistration-structure-v1",
            "required_singletons": list(PREREGISTRATION_REQUIRED_SINGLETONS),
            "identifier_sets": {
                key: list(values) for key, values in PREREGISTRATION_IDENTIFIER_SETS.items()
            },
            "baseline_id_count": len(BASELINE_IDS),
            "measurement_requirement_id_count": len(MEASUREMENT_REQUIREMENT_IDS),
            "content_fields_accepted": False,
        },
        "privacy_and_semantic_prohibitions": {
            "forbidden_field_fragments": list(FORBIDDEN_FIELD_FRAGMENTS),
            "prohibited_output_fragments": list(PROHIBITED_OUTPUT_FRAGMENTS),
            "free_text_accepted": False,
            "relationship_fields_accepted": False,
            "real_person_fields_accepted": False,
            "inference_or_candidate_selection_present": False,
        },
    }
    inference["schema_sha256"] = sha256_json(inference)
    evaluator: JsonObject = {
        "schema_version": "natal-time-synthetic-evaluator-custody-schema-v1",
        "synthetic_only": True,
        "contract_bindings": bindings,
        "evaluator_version": version,
        "exact_reference_fields": [
            "schema_version",
            "custody_id",
            "synthetic_only",
            "documentary_source_classification",
            "precision_classification",
            "custody_classification",
            "reference",
            "mutation_test_mode",
            "reference_custody_sha256",
        ],
        "custody_access_phase_order": ["sealed", "opened", "invalidated"],
        "authorized_open_requires_s_i_capability": True,
        "early_access_attempts_fail_closed": ["raw_byte", "digest", "metadata", "alternate_loader"],
        "post_access_t_i_mutation_invalidates_custody": True,
        "receipt_component_metrics": list(METRIC_COMPONENT_IDS),
        "artifact_contract": {
            "structural_validator": "hdmatch.natal_time.evaluation_contract.verify_receipt",
            "rehashing_unknown_fields_never_makes_them_valid": True,
            "valid_metric_receipt_exact_fields": [
                "schema_version",
                "receipt_kind",
                "synthetic_only",
                "fixture_id",
                "evaluation_eligible",
                "contract_bindings",
                "inference_visible_fixture_digest",
                "candidate_domain_freeze_sha256",
                "study_method_specification_sha256",
                "s_i_commitment_sha256",
                "canonical_t_i_sha256",
                "reference_custody_sha256",
                "reference_custody_access_state_sha256",
                "access_state_sha256",
                "evaluator_version_sha256",
                "metrics",
                "metrics_sha256",
                "inference_or_selection_performed",
                "receipt_sha256",
            ],
            "domain_diagnostic_exact_fields": [
                "schema_version",
                "receipt_kind",
                "synthetic_only",
                "fixture_id",
                "valid_reference_evaluation_receipt",
                "contract_bindings",
                "inference_visible_fixture_digest",
                "candidate_domain_freeze_sha256",
                "study_method_specification_sha256",
                "s_i_commitment_sha256",
                "canonical_t_i_sha256",
                "reference_custody_sha256",
                "reference_custody_access_state_sha256",
                "access_state_sha256",
                "evaluator_version_sha256",
                "reference_domain_status",
                "reference_intersection",
                "documentary_reference_width",
                "inference_or_selection_performed",
                "receipt_sha256",
            ],
            "rejection_exact_fields": [
                "schema_version",
                "receipt_kind",
                "synthetic_only",
                "fixture_id",
                "valid_evaluation_receipt",
                "contract_bindings",
                "inference_visible_fixture_digest",
                "access_state_sha256",
                "evaluator_version_sha256",
                "violation_codes",
                "metrics_present",
                "inference_or_selection_performed",
                "receipt_sha256",
            ],
        },
        "allowed_violation_codes": sorted(ALLOWED_VIOLATION_CODES),
    }
    evaluator["schema_sha256"] = sha256_json(evaluator)
    return inference, evaluator


def _self_hashed_manifest(payload: JsonObject) -> JsonObject:
    payload["manifest_sha256"] = sha256_json(payload)
    return payload


def _custody_from_reference(value: JsonObject) -> EvaluatorReferenceCustody:
    def load() -> object:
        return deepcopy(value)

    return EvaluatorReferenceCustody(load)


def build_bundle(project_root: Path) -> GeneratedBundle:
    inference_schema, evaluator_schema = build_schemas(project_root)
    evaluator_version = cast(JsonObject, evaluator_schema["evaluator_version"])
    evaluator_sha256 = cast(str, evaluator_version["evaluator_version_sha256"])
    pairs = build_fixture_pairs()
    receipts = tuple(
        verify_separated_synthetic_fixture(
            pair.inference_visible,
            _custody_from_reference(pair.evaluator_reference),
            evaluator_version_sha256=evaluator_sha256,
        )
        for pair in pairs
    )
    inference_entries: list[JsonObject] = []
    evaluator_entries: list[JsonObject] = []
    evaluation_entries: list[JsonObject] = []
    for pair, receipt in zip(pairs, receipts, strict=True):
        fixture = pair.inference_visible
        reference = pair.evaluator_reference
        fixture_id = cast(str, fixture["fixture_id"])
        custody_id = cast(str, reference["custody_id"])
        inference_entries.append(
            {
                "fixture_id": fixture_id,
                "fixture_path": f"{STATE_DIRECTORY}/inference/fixtures/{fixture_id}.json",
                "inference_visible_fixture_digest": fixture["inference_visible_fixture_digest"],
                "fixture_file_sha256": sha256_bytes(canonical_json_bytes(fixture) + b"\n"),
            }
        )
        evaluator_entries.append(
            {
                "fixture_id": fixture_id,
                "inference_visible_fixture_digest": fixture["inference_visible_fixture_digest"],
                "custody_id": custody_id,
                "reference_path": f"{STATE_DIRECTORY}/evaluator/references/{custody_id}.json",
                "reference_custody_sha256": reference["reference_custody_sha256"],
                "reference_file_sha256": sha256_bytes(canonical_json_bytes(reference) + b"\n"),
            }
        )
        evaluation_entries.append(
            {
                "fixture_id": fixture_id,
                "inference_visible_fixture_digest": fixture["inference_visible_fixture_digest"],
                "custody_id": custody_id,
                "receipt_path": f"{STATE_DIRECTORY}/receipts/{fixture_id}.json",
                "receipt_sha256": receipt["receipt_sha256"],
                "receipt_file_sha256": sha256_bytes(canonical_json_bytes(receipt) + b"\n"),
                "receipt_kind": receipt["receipt_kind"],
            }
        )
    inference_manifest = _self_hashed_manifest(
        {
            "schema_version": "natal-time-synthetic-inference-visible-manifest-v2",
            "synthetic_only": True,
            "schema_path": f"{STATE_DIRECTORY}/inference/schema.json",
            "schema_sha256": inference_schema["schema_sha256"],
            "schema_file_sha256": sha256_bytes(canonical_json_bytes(inference_schema) + b"\n"),
            "fixture_count": len(pairs),
            "entries": inference_entries,
        }
    )
    evaluator_manifest = _self_hashed_manifest(
        {
            "schema_version": "natal-time-synthetic-evaluator-custody-manifest-v1",
            "synthetic_only": True,
            "schema_path": f"{STATE_DIRECTORY}/evaluator/schema.json",
            "schema_sha256": evaluator_schema["schema_sha256"],
            "schema_file_sha256": sha256_bytes(canonical_json_bytes(evaluator_schema) + b"\n"),
            "custody_count": len(pairs),
            "entries": evaluator_entries,
        }
    )
    evaluation_manifest = _self_hashed_manifest(
        {
            "schema_version": "natal-time-synthetic-postcommit-evaluation-manifest-v3",
            "synthetic_only": True,
            "contract_sha256": V3_CONTRACT_SHA256,
            "evaluator_version_sha256": evaluator_sha256,
            "inference_manifest_sha256": inference_manifest["manifest_sha256"],
            "evaluator_manifest_sha256": evaluator_manifest["manifest_sha256"],
            "receipt_count": len(receipts),
            "entries": evaluation_entries,
        }
    )
    return GeneratedBundle(
        inference_schema,
        evaluator_schema,
        pairs,
        receipts,
        inference_manifest,
        evaluator_manifest,
        evaluation_manifest,
    )


def _write_json(path: Path, value: JsonObject) -> None:
    write_new_bytes(path, canonical_json_bytes(value) + b"\n")


def write_bundle(project_root: Path, output_root: Path) -> None:
    bundle = build_bundle(project_root)
    _write_json(output_root / "inference" / "schema.json", bundle.inference_schema)
    _write_json(output_root / "evaluator" / "schema.json", bundle.evaluator_schema)
    for pair, receipt in zip(bundle.fixture_pairs, bundle.receipts, strict=True):
        fixture_id = cast(str, pair.inference_visible["fixture_id"])
        custody_id = cast(str, pair.evaluator_reference["custody_id"])
        _write_json(
            output_root / "inference" / "fixtures" / f"{fixture_id}.json", pair.inference_visible
        )
        _write_json(
            output_root / "evaluator" / "references" / f"{custody_id}.json",
            pair.evaluator_reference,
        )
        _write_json(output_root / "receipts" / f"{fixture_id}.json", receipt)
    _write_json(output_root / "inference" / "manifest.json", bundle.inference_manifest)
    _write_json(output_root / "evaluator" / "manifest.json", bundle.evaluator_manifest)
    _write_json(output_root / "evaluation-manifest.json", bundle.evaluation_manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path(__file__).parents[1])
    parser.add_argument(
        "--output-root", type=Path, default=Path(__file__).parents[1] / STATE_DIRECTORY
    )
    args = parser.parse_args()
    write_bundle(args.project_root.resolve(), args.output_root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
