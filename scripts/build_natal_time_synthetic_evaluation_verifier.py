"""Build fixed synthetic evaluation-contract fixtures and content-hashed receipts."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import cast

from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.natal_time.evaluation_contract import (
    ACTOR_ACCESS_IDS,
    ALLOWED_VIOLATION_CODES,
    BASELINE_IDS,
    CONNECTED_COMPONENT_EDGE_IDS,
    DATA_ROLE_IDS,
    DISCLOSURE_CONTROL_IDS,
    DISCLOSURE_SURFACE_DECLARATION_IDS,
    DISCLOSURE_THREAT_IDS,
    ELIGIBLE_SOURCE_CLASS_IDS,
    FORBIDDEN_FIELD_FRAGMENTS,
    INELIGIBLE_SOURCE_CLASS_IDS,
    LEAKAGE_CONTAMINATION_RULE_IDS,
    MEASUREMENT_REQUIREMENT_IDS,
    METRIC_COMPONENT_IDS,
    PREREGISTRATION_IDENTIFIER_SETS,
    PREREGISTRATION_REQUIRED_SINGLETONS,
    PROHIBITED_OUTPUT_FRAGMENTS,
    PROHIBITED_PUBLIC_FIELD_IDS,
    SOURCE_ELIGIBILITY_RULE_IDS,
    SOURCE_PRECISION_RULE_IDS,
    V1_CONTRACT_SHA256,
    V2_CONTRACT_SHA256,
    CanonicalInterval,
    candidate_set_digest,
    evaluator_version_packet,
    fixture_digest,
    verify_synthetic_fixture,
)
from hdmatch.util import canonical_json_bytes, sha256_bytes, sha256_json

JsonObject = dict[str, object]

FIXTURE_SCHEMA_VERSION = "natal-time-synthetic-evaluation-fixture-v1"
STATE_DIRECTORY = "state/NATAL-TIME-SYNTHETIC-EVALUATION-V1"


def _utc(day: str, time: str) -> str:
    return f"{day}T{time}.000000Z"


def _state_digest(code: str) -> str:
    return sha256_json({"schema_version": "synthetic-state-code-v1", "code": code})


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
            _utc("2099-01-01", "08:00:00"),
            "SYNTH-STATE-A",
            "2099-01-01",
        ),
        (
            "SYNTH-INTERVAL-B",
            _utc("2099-01-01", "08:00:00"),
            _utc("2099-01-01", "16:00:00"),
            "SYNTH-STATE-B",
            "2099-01-01",
        ),
        (
            "SYNTH-INTERVAL-C",
            _utc("2099-01-01", "16:00:00"),
            _utc("2099-01-02", "00:00:00"),
            "SYNTH-STATE-A",
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


def _parse_builder_utc(value: str) -> datetime:
    return datetime.fromisoformat(value[:-1] + "+00:00")


def _method_specification() -> JsonObject:
    payload: JsonObject = {
        "study_design_contract_sha256": V1_CONTRACT_SHA256,
        "metric_semantics_contract_sha256": V2_CONTRACT_SHA256,
        "s_i_origin": "preconstructed_test_vector",
        "selection_procedure_present": False,
    }
    payload["method_specification_sha256"] = sha256_json(payload)
    return payload


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
        "selected_intervals": [deepcopy(by_id[interval_id]) for interval_id in interval_ids],
    }


def _fixture(
    fixture_id: str,
    candidate_set: JsonObject,
    output: JsonObject,
    reference: JsonObject,
    *,
    assignments: list[JsonObject] | None = None,
    contamination_status: str = "clean",
    execution_plan: list[str] | None = None,
) -> JsonObject:
    payload: JsonObject = {
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "fixture_id": fixture_id,
        "synthetic_only": True,
        "preconstructed_s_i": True,
        "candidate_set": deepcopy(candidate_set),
        "method_specification": _method_specification(),
        "preconstructed_output": output,
        "component_assignments": assignments if assignments is not None else _assignment(),
        "contamination_status": contamination_status,
        "execution_plan": execution_plan if execution_plan is not None else _standard_plan(),
        "hidden_reference": reference,
    }
    payload["fixture_sha256"] = fixture_digest(payload)
    return payload


def build_fixtures() -> tuple[JsonObject, ...]:
    """Return fixed vectors covering every Phase-1 acceptance boundary."""

    candidate_set = _build_candidate_set()
    intervals = cast(list[JsonObject], candidate_set["intervals"])
    full_ids = tuple(cast(str, item["interval_id"]) for item in intervals)
    ordinary_reference = _reference(_utc("2099-01-01", "01:00:00"), _utc("2099-01-01", "02:00:00"))
    fixtures: list[JsonObject] = [
        _fixture(
            "SYNTH-FIXTURE-FULL-C",
            candidate_set,
            _output(candidate_set, full_ids),
            ordinary_reference,
        ),
        _fixture(
            "SYNTH-FIXTURE-ABSTENTION",
            candidate_set,
            {"output_kind": "abstention", "selected_intervals": []},
            ordinary_reference,
        ),
        _fixture(
            "SYNTH-FIXTURE-BOUNDARY-TOUCH",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            _reference(_utc("2099-01-01", "08:00:00"), _utc("2099-01-01", "09:00:00")),
        ),
        _fixture(
            "SYNTH-FIXTURE-REPEATED-STATE",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-A", "SYNTH-INTERVAL-C")),
            ordinary_reference,
        ),
        _fixture(
            "SYNTH-FIXTURE-MULTIPLE-DATES",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-B", "SYNTH-INTERVAL-D")),
            _reference(_utc("2099-01-03", "01:00:00"), _utc("2099-01-03", "02:00:00")),
        ),
        _fixture(
            "SYNTH-FIXTURE-WIDE-REFERENCE",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-A", "SYNTH-INTERVAL-B")),
            _reference(_utc("2099-01-01", "01:00:00"), _utc("2099-01-01", "23:00:00")),
        ),
        _fixture(
            "SYNTH-FIXTURE-PARTIAL-REFERENCE-ONE-MICROSECOND",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            _reference("2098-12-31T23:59:00.000000Z", "2099-01-01T00:00:00.000001Z"),
        ),
        _fixture(
            "SYNTH-FIXTURE-IDENTICAL-MULTIPLE-SOURCES",
            candidate_set,
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
        ),
        _fixture(
            "SYNTH-FIXTURE-SOURCE-CONFLICT",
            candidate_set,
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
        ),
        _fixture(
            "SYNTH-FIXTURE-DOMAIN-INCOMPATIBLE",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            _reference("2098-12-31T23:00:00.000000Z", "2099-01-01T00:00:00.000000Z"),
        ),
        _fixture(
            "SYNTH-FIXTURE-NO-ELIGIBLE-REFERENCE",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            {"canonicalization_status": "no_eligible_reference", "sources": []},
        ),
        _fixture(
            "SYNTH-FIXTURE-REFERENCE-CANONICALIZATION-FAILED",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            {"canonicalization_status": "reference_canonicalization_failed", "sources": []},
        ),
    ]

    fixtures.append(
        _fixture(
            "SYNTH-FIXTURE-EMPTY-NON-ABSTENTION",
            candidate_set,
            {"output_kind": "candidate_subset", "selected_intervals": []},
            ordinary_reference,
        )
    )
    partial = deepcopy(intervals[0])
    partial["end_utc"] = _utc("2099-01-01", "07:00:00")
    fixtures.append(
        _fixture(
            "SYNTH-FIXTURE-PARTIAL-INTERVAL",
            candidate_set,
            {"output_kind": "candidate_subset", "selected_intervals": [partial]},
            ordinary_reference,
        )
    )
    duplicate = deepcopy(intervals[0])
    fixtures.append(
        _fixture(
            "SYNTH-FIXTURE-DUPLICATE-INTERVAL",
            candidate_set,
            {"output_kind": "candidate_subset", "selected_intervals": [duplicate, duplicate]},
            ordinary_reference,
        )
    )
    reordered_duplication = [deepcopy(intervals[2]), deepcopy(intervals[0]), deepcopy(intervals[2])]
    fixtures.append(
        _fixture(
            "SYNTH-FIXTURE-REORDERED-WITH-DUPLICATION",
            candidate_set,
            {"output_kind": "candidate_subset", "selected_intervals": reordered_duplication},
            ordinary_reference,
        )
    )
    foreign = deepcopy(intervals[0])
    foreign["interval_id"] = "SYNTH-INTERVAL-FOREIGN"
    fixtures.append(
        _fixture(
            "SYNTH-FIXTURE-FOREIGN-INTERVAL",
            candidate_set,
            {"output_kind": "candidate_subset", "selected_intervals": [foreign]},
            ordinary_reference,
        )
    )
    manufactured = deepcopy(intervals[0])
    manufactured["interval_id"] = "SYNTH-INTERVAL-MANUFACTURED"
    manufactured["end_utc"] = cast(str, intervals[1]["end_utc"])
    fixtures.append(
        _fixture(
            "SYNTH-FIXTURE-MANUFACTURED-INTERVAL",
            candidate_set,
            {"output_kind": "candidate_subset", "selected_intervals": [manufactured]},
            ordinary_reference,
        )
    )
    fixtures.append(
        _fixture(
            "SYNTH-FIXTURE-EARLY-REFERENCE-ACCESS",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            ordinary_reference,
            execution_plan=[
                "candidate_domain_freeze",
                "study_method_specification_freeze",
                "evaluator_only_t_i_access",
                "preconstructed_s_i_commitment",
                "metric_receipt",
            ],
        )
    )
    fixtures.append(
        _fixture(
            "SYNTH-FIXTURE-POST-REFERENCE-OUTPUT-MUTATION",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            ordinary_reference,
            execution_plan=[
                "candidate_domain_freeze",
                "study_method_specification_freeze",
                "preconstructed_s_i_commitment",
                "evaluator_only_t_i_access",
                "post_reference_s_i_mutation_attempt",
                "metric_receipt",
            ],
        )
    )
    fixtures.append(
        _fixture(
            "SYNTH-FIXTURE-CROSS-ROLE-COMPONENT",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            ordinary_reference,
            assignments=[
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
            ],
        )
    )
    fixtures.append(
        _fixture(
            "SYNTH-FIXTURE-CONTAMINATED-COMPONENT",
            candidate_set,
            _output(candidate_set, ("SYNTH-INTERVAL-A",)),
            ordinary_reference,
            contamination_status="method_changed_after_outcome_access",
        )
    )
    return tuple(fixtures)


def build_schema(project_root: Path) -> JsonObject:
    version = evaluator_version_packet(project_root)
    payload: JsonObject = {
        "schema_version": "natal-time-synthetic-evaluation-verifier-schema-v1",
        "synthetic_only": True,
        "participant_work_authorized": False,
        "contract_bindings": {
            "preserved_v1_contract_sha256": V1_CONTRACT_SHA256,
            "metric_semantics_v2_contract_sha256": V2_CONTRACT_SHA256,
        },
        "evaluator_version": version,
        "fixture_contract": {
            "additional_fields_allowed": False,
            "exact_top_level_fields": [
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
                "hidden_reference",
                "fixture_sha256",
            ],
            "preconstructed_s_i_required": True,
            "selection_procedure_present_required_value": False,
            "hidden_reference_access_after_s_i_commitment_only": True,
        },
        "receipt_contract": {
            "additional_fields_allowed": False,
            "structural_validator": "hdmatch.natal_time.evaluation_contract.verify_receipt",
            "rehashing_unknown_fields_never_makes_them_valid": True,
            "valid_receipt_exact_fields": [
                "schema_version",
                "receipt_kind",
                "synthetic_only",
                "fixture_id",
                "evaluation_eligible",
                "contract_bindings",
                "fixture_sha256",
                "candidate_domain_freeze_sha256",
                "study_method_specification_sha256",
                "s_i_commitment_sha256",
                "hidden_reference_sha256",
                "access_state_sha256",
                "evaluator_version_sha256",
                "metrics",
                "metrics_sha256",
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
                "fixture_sha256",
                "access_state_sha256",
                "evaluator_version_sha256",
                "violation_codes",
                "metrics_present",
                "inference_or_selection_performed",
                "receipt_sha256",
            ],
            "component_metrics": [
                *METRIC_COMPONENT_IDS,
            ],
            "typed_not_applicable_values_are_null": True,
            "scalar_summary_present": False,
            "required_binding_digests": [
                "contract_bindings",
                "fixture_sha256",
                "access_state_sha256",
                "evaluator_version_sha256",
                "metrics_sha256",
            ],
        },
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
        "controlled_sets": {
            "data_role_ids": list(DATA_ROLE_IDS),
            "actor_access_ids": list(ACTOR_ACCESS_IDS),
            "source_eligibility_rule_ids": list(SOURCE_ELIGIBILITY_RULE_IDS),
            "eligible_source_class_ids": list(ELIGIBLE_SOURCE_CLASS_IDS),
            "ineligible_source_class_ids": list(INELIGIBLE_SOURCE_CLASS_IDS),
            "source_precision_rule_ids": list(SOURCE_PRECISION_RULE_IDS),
            "connected_component_edge_ids": list(CONNECTED_COMPONENT_EDGE_IDS),
            "leakage_contamination_rule_ids": list(LEAKAGE_CONTAMINATION_RULE_IDS),
            "metric_component_ids": list(METRIC_COMPONENT_IDS),
            "disclosure_threat_ids": list(DISCLOSURE_THREAT_IDS),
            "disclosure_control_ids": list(DISCLOSURE_CONTROL_IDS),
            "prohibited_public_field_ids": list(PROHIBITED_PUBLIC_FIELD_IDS),
            "disclosure_surface_declaration_ids": list(DISCLOSURE_SURFACE_DECLARATION_IDS),
            "allowed_violation_codes": sorted(ALLOWED_VIOLATION_CODES),
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
    payload["schema_sha256"] = sha256_json(payload)
    return payload


def build_bundle(
    project_root: Path,
) -> tuple[JsonObject, tuple[JsonObject, ...], tuple[JsonObject, ...], JsonObject]:
    schema = build_schema(project_root)
    evaluator_sha256 = cast(JsonObject, schema["evaluator_version"])["evaluator_version_sha256"]
    assert isinstance(evaluator_sha256, str)
    fixtures = build_fixtures()
    receipts = tuple(
        verify_synthetic_fixture(fixture, evaluator_version_sha256=evaluator_sha256)
        for fixture in fixtures
    )
    entries: list[JsonObject] = []
    for fixture, receipt in zip(fixtures, receipts, strict=True):
        fixture_id = cast(str, fixture["fixture_id"])
        entries.append(
            {
                "fixture_id": fixture_id,
                "fixture_path": f"{STATE_DIRECTORY}/fixtures/{fixture_id}.json",
                "fixture_sha256": fixture["fixture_sha256"],
                "fixture_file_sha256": sha256_bytes(canonical_json_bytes(fixture) + b"\n"),
                "receipt_path": f"{STATE_DIRECTORY}/receipts/{fixture_id}.json",
                "receipt_sha256": receipt["receipt_sha256"],
                "receipt_file_sha256": sha256_bytes(canonical_json_bytes(receipt) + b"\n"),
                "receipt_kind": receipt["receipt_kind"],
            }
        )
    manifest: JsonObject = {
        "schema_version": "natal-time-synthetic-evaluation-manifest-v1",
        "synthetic_only": True,
        "contract_sha256": V2_CONTRACT_SHA256,
        "schema_path": f"{STATE_DIRECTORY}/schema.json",
        "schema_sha256": schema["schema_sha256"],
        "schema_file_sha256": sha256_bytes(canonical_json_bytes(schema) + b"\n"),
        "evaluator_version_sha256": evaluator_sha256,
        "fixture_count": len(fixtures),
        "entries": entries,
    }
    manifest["manifest_sha256"] = sha256_json(manifest)
    return schema, fixtures, receipts, manifest


def _write_json(path: Path, value: JsonObject) -> None:
    write_new_bytes(path, canonical_json_bytes(value) + b"\n")


def write_bundle(project_root: Path, output_root: Path) -> None:
    schema, fixtures, receipts, manifest = build_bundle(project_root)
    _write_json(output_root / "schema.json", schema)
    for fixture, receipt in zip(fixtures, receipts, strict=True):
        fixture_id = cast(str, fixture["fixture_id"])
        _write_json(output_root / "fixtures" / f"{fixture_id}.json", fixture)
        _write_json(output_root / "receipts" / f"{fixture_id}.json", receipt)
    _write_json(output_root / "manifest.json", manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path(__file__).parents[1])
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path(__file__).parents[1] / STATE_DIRECTORY,
    )
    args = parser.parse_args()
    write_bundle(args.project_root.resolve(), args.output_root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
