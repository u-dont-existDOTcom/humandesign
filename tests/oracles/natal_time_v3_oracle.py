"""Independent V3 descriptive oracle for preconstructed synthetic natal-time cases.

This test-only module intentionally uses only the Python standard library.  It does not import
the production evaluator, its models, its canonicalization helpers, or its fixture builder.  It
validates and evaluates already-constructed synthetic ``S_i`` records; it never constructs,
ranks, optimizes, or chooses an output.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from typing import NoReturn, cast

JsonObject = dict[str, object]

V3_CONTRACT_SHA256 = "75a1629203724715054e2a1d7ea1b6ead7dc0ffd6cf5f4df2756c3e622b5f1fe"

_PERSONAL_FRAGMENTS = (
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
_INFERENTIAL_FRAGMENTS = (
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
_EARLY_EVENTS = {
    "early_reference_raw_byte_access_attempt": "early_reference_raw_byte_access",
    "early_reference_digest_access_attempt": "early_reference_digest_access",
    "early_reference_metadata_access_attempt": "early_reference_metadata_access",
    "early_reference_alternate_loader_access_attempt": (
        "early_reference_alternate_loader_access"
    ),
}


class OracleViolation(ValueError):
    """A controlled independent-oracle rejection."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class OracleEvaluation:
    fixture_id: str
    summary: JsonObject
    access_trace: JsonObject


def _reject(code: str) -> NoReturn:
    raise OracleViolation(code)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def independent_sha256_json(value: object) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _parse_utc(value: object) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        _reject("invalid_canonical_utc_instant")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        _reject("invalid_canonical_utc_instant")
    if parsed.tzinfo is None or parsed.utcoffset() != UTC.utcoffset(parsed):
        _reject("invalid_canonical_utc_instant")
    rendered = parsed.astimezone(UTC).isoformat(timespec="microseconds").replace(
        "+00:00", "Z"
    )
    if rendered != value:
        _reject("noncanonical_utc_instant")
    return parsed


def _microseconds(start: datetime, end: datetime) -> int:
    delta = end - start
    return delta.days * 86_400_000_000 + delta.seconds * 1_000_000 + delta.microseconds


def _mapping(value: object, code: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        _reject(code)
    return cast(Mapping[str, object], value)


def _sequence(value: object, code: str) -> Sequence[object]:
    if not isinstance(value, list):
        _reject(code)
    return value


def _scan_prohibited(value: object) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if not isinstance(key, str):
                _reject("non_string_field_name")
            lowered = key.lower()
            if any(fragment in lowered for fragment in _PERSONAL_FRAGMENTS):
                _reject("prohibited_personal_or_free_text_field")
            if any(fragment in lowered for fragment in _INFERENTIAL_FRAGMENTS):
                _reject("prohibited_inferential_or_scalar_output_field")
            _scan_prohibited(child)
    elif isinstance(value, list):
        for item in value:
            _scan_prohibited(item)


def _sort_intervals(values: Sequence[Mapping[str, object]]) -> list[Mapping[str, object]]:
    return sorted(
        values,
        key=lambda item: (
            cast(str, item["start_utc"]),
            cast(str, item["end_utc"]),
            cast(str, item["interval_id"]),
            cast(str, item["full_state_sha256"]),
        ),
    )


def _interval_identity(value: Mapping[str, object]) -> bytes:
    return _canonical_bytes(value)


def _validated_candidate_set(value: object) -> tuple[Mapping[str, object], ...]:
    raw = _mapping(value, "invalid_candidate_set_object")
    if set(raw) != {
        "candidate_manifest_sha256",
        "candidate_set_sha256",
        "declared_dates",
        "intervals",
    }:
        _reject("invalid_candidate_set_fields")
    declared = _sequence(raw["declared_dates"], "invalid_declared_dates")
    intervals_raw = _sequence(raw["intervals"], "invalid_candidate_intervals")
    if not declared or not intervals_raw:
        _reject("empty_candidate_domain")
    if len(declared) != len(set(declared)):
        _reject("duplicate_declared_date")
    intervals: list[Mapping[str, object]] = []
    ids: list[str] = []
    for value_item in intervals_raw:
        item = _mapping(value_item, "invalid_interval_object")
        if set(item) != {
            "candidate_manifest_sha256",
            "candidate_set_sha256",
            "interval_id",
            "start_utc",
            "end_utc",
            "full_state_sha256",
            "civil_date",
        }:
            _reject("invalid_interval_fields")
        start = _parse_utc(item["start_utc"])
        end = _parse_utc(item["end_utc"])
        if end <= start:
            _reject("nonpositive_interval_width")
        if item["civil_date"] not in declared:
            _reject("interval_outside_declared_dates")
        if item["candidate_manifest_sha256"] != raw["candidate_manifest_sha256"]:
            _reject("candidate_manifest_mismatch")
        if item["candidate_set_sha256"] != raw["candidate_set_sha256"]:
            _reject("candidate_set_digest_mismatch")
        ids.append(cast(str, item["interval_id"]))
        intervals.append(item)
    if len(ids) != len(set(ids)):
        _reject("duplicate_candidate_interval")
    for civil_date in declared:
        date_intervals = _sort_intervals(
            [item for item in intervals if item["civil_date"] == civil_date]
        )
        if not date_intervals:
            _reject("declared_date_without_candidate_interval")
        for left, right in zip(date_intervals, date_intervals[1:], strict=False):
            if left["end_utc"] != right["start_utc"]:
                _reject("candidate_domain_gap_or_overlap")
    global_intervals = _sort_intervals(intervals)
    for left, right in zip(global_intervals, global_intervals[1:], strict=False):
        if _parse_utc(left["end_utc"]) > _parse_utc(right["start_utc"]):
            _reject("candidate_domain_gap_or_overlap")
    return tuple(intervals)


def _validate_components(value: object, contamination_status: object) -> None:
    assignments = _sequence(value, "invalid_component_assignments")
    if not assignments:
        _reject("empty_component_assignments")
    roles: dict[str, set[str]] = {}
    observations: list[str] = []
    for raw_item in assignments:
        item = _mapping(raw_item, "invalid_component_assignment_object")
        if set(item) != {"synthetic_observation_id", "component_id", "role"}:
            _reject("invalid_component_assignment_fields")
        component = cast(str, item["component_id"])
        observations.append(cast(str, item["synthetic_observation_id"]))
        roles.setdefault(component, set()).add(cast(str, item["role"]))
    if len(observations) != len(set(observations)):
        _reject("duplicate_synthetic_observation")
    if any(len(values) > 1 for values in roles.values()):
        _reject("cross_role_connected_component")
    if contamination_status != "clean":
        _reject("contaminated_connected_component")


def _validate_output(
    value: object, candidates: tuple[Mapping[str, object], ...]
) -> tuple[str, tuple[Mapping[str, object], ...], str]:
    raw = _mapping(value, "invalid_output_object")
    if set(raw) != {"output_kind", "selected_intervals"}:
        _reject("invalid_output_fields")
    kind = raw["output_kind"]
    if kind not in {"candidate_subset", "abstention"}:
        _reject("invalid_output_kind")
    selected = tuple(
        _mapping(item, "invalid_interval_object")
        for item in _sequence(raw["selected_intervals"], "invalid_selected_intervals")
    )
    if kind == "abstention" and selected:
        _reject("abstention_must_not_select_intervals")
    if kind == "candidate_subset" and not selected:
        _reject("invalid_output_empty_non_abstention")
    identities = [_interval_identity(item) for item in selected]
    ids = [cast(str, item.get("interval_id")) for item in selected]
    if len(identities) != len(set(identities)) or len(ids) != len(set(ids)):
        _reject("duplicate_selected_interval")
    frozen_by_id = {cast(str, item["interval_id"]): item for item in candidates}
    for chosen in selected:
        chosen_id = cast(str, chosen.get("interval_id"))
        frozen = frozen_by_id.get(chosen_id)
        if frozen is None:
            chosen_start = _parse_utc(chosen.get("start_utc"))
            chosen_end = _parse_utc(chosen.get("end_utc"))
            enclosed = [
                item
                for item in candidates
                if _parse_utc(item["start_utc"]) >= chosen_start
                and _parse_utc(item["end_utc"]) <= chosen_end
            ]
            if (
                len(enclosed) > 1
                and min(_parse_utc(item["start_utc"]) for item in enclosed)
                == chosen_start
                and max(_parse_utc(item["end_utc"]) for item in enclosed) == chosen_end
            ):
                _reject("manufactured_interval_not_allowed")
            _reject("foreign_or_manufactured_interval")
        if chosen != frozen:
            chosen_start = _parse_utc(chosen.get("start_utc"))
            chosen_end = _parse_utc(chosen.get("end_utc"))
            frozen_start = _parse_utc(frozen["start_utc"])
            frozen_end = _parse_utc(frozen["end_utc"])
            if (
                chosen.get("candidate_manifest_sha256")
                == frozen["candidate_manifest_sha256"]
                and chosen.get("candidate_set_sha256") == frozen["candidate_set_sha256"]
                and chosen_start >= frozen_start
                and chosen_end <= frozen_end
                and (chosen_start > frozen_start or chosen_end < frozen_end)
            ):
                _reject("partial_interval_not_allowed")
            _reject("foreign_or_manufactured_interval")
    canonical_output = {
        "output_kind": kind,
        "selected_intervals": [dict(item) for item in _sort_intervals(selected)],
    }
    return kind, selected, independent_sha256_json(canonical_output)


def _fraction(numerator: int, denominator: int, unit: str) -> JsonObject:
    value = Fraction(numerator, denominator)
    return {
        "status": "applicable",
        f"selected_{unit}": numerator,
        f"candidate_{unit}": denominator,
        "fraction": f"{value.numerator}/{value.denominator}",
    }


def _not_applicable(status: str, unit: str) -> JsonObject:
    return {
        "status": status,
        f"selected_{unit}": None,
        f"candidate_{unit}": None,
        "fraction": None,
    }


def _reference_failure_metrics(
    status: str, *, abstention: bool, documentary_width: int | None = None
) -> JsonObject:
    return {
        "reference_intersection": {"status": status, "value": None},
        "temporal_width_retained": _not_applicable(status, "width_microseconds"),
        "canonical_interval_count_retained": _not_applicable(status, "interval_count"),
        "unique_state_identity_count_retained": _not_applicable(
            status, "unique_state_identity_count"
        ),
        "date_coverage": _not_applicable(status, "date_count"),
        "documentary_reference_width": (
            {"status": status, "microseconds": None}
            if documentary_width is None
            else {"status": "applicable", "microseconds": documentary_width}
        ),
        "abstention": {"status": "applicable", "value": abstention},
    }


def _reference_result(
    custody: Mapping[str, object],
    candidates: tuple[Mapping[str, object], ...],
    selected: tuple[Mapping[str, object], ...],
    kind: str,
) -> JsonObject:
    reference = _mapping(custody.get("reference"), "invalid_reference_bundle_object")
    status = reference.get("canonicalization_status")
    sources = [
        _mapping(item, "invalid_reference_source_object")
        for item in _sequence(reference.get("sources"), "invalid_reference_sources")
    ]
    if status == "no_eligible_reference":
        failure_metrics = _reference_failure_metrics(
            "not_applicable_no_eligible_reference", abstention=kind == "abstention"
        )
        return {
            "receipt_kind": "descriptive_metric_receipt",
            "evaluation_eligible": False,
            "metrics": failure_metrics,
        }
    if status == "reference_canonicalization_failed":
        failure_metrics = _reference_failure_metrics(
            "not_applicable_reference_canonicalization_failed",
            abstention=kind == "abstention",
        )
        return {
            "receipt_kind": "descriptive_metric_receipt",
            "evaluation_eligible": False,
            "metrics": failure_metrics,
        }
    if status != "canonical_half_open_utc" or not sources:
        _reject("invalid_reference_canonicalization_status")
    intervals = {
        (cast(str, item["start_utc"]), cast(str, item["end_utc"])) for item in sources
    }
    if len(intervals) != 1:
        failure_metrics = _reference_failure_metrics(
            "not_applicable_conflicting_eligible_sources",
            abstention=kind == "abstention",
        )
        return {
            "receipt_kind": "descriptive_metric_receipt",
            "evaluation_eligible": False,
            "metrics": failure_metrics,
        }
    reference_start_text, reference_end_text = next(iter(intervals))
    reference_start = _parse_utc(reference_start_text)
    reference_end = _parse_utc(reference_end_text)
    documentary_width = _microseconds(reference_start, reference_end)
    if documentary_width <= 0:
        _reject("nonpositive_reference_width")
    overlap_width = 0
    for item in candidates:
        start = max(_parse_utc(item["start_utc"]), reference_start)
        end = min(_parse_utc(item["end_utc"]), reference_end)
        if start < end:
            overlap_width += _microseconds(start, end)
    if overlap_width == documentary_width:
        domain_status = "reference_domain_compatible"
    elif overlap_width > 0:
        domain_status = "reference_domain_partially_incompatible"
    else:
        domain_status = "reference_domain_incompatible"
    if domain_status != "reference_domain_compatible":
        na_status = f"not_applicable_{domain_status}"
        return {
            "receipt_kind": "reference_domain_diagnostic",
            "valid_reference_evaluation_receipt": False,
            "reference_domain_status": domain_status,
            "reference_intersection": {"status": na_status, "value": None},
            "documentary_reference_width": {
                "status": "applicable",
                "microseconds": documentary_width,
            },
        }
    if kind == "abstention":
        failure_metrics = _reference_failure_metrics(
            "not_applicable_abstention",
            abstention=True,
            documentary_width=documentary_width,
        )
        return {
            "receipt_kind": "descriptive_metric_receipt",
            "evaluation_eligible": True,
            "metrics": failure_metrics,
        }
    candidate_width = sum(
        _microseconds(_parse_utc(item["start_utc"]), _parse_utc(item["end_utc"]))
        for item in candidates
    )
    selected_width = sum(
        _microseconds(_parse_utc(item["start_utc"]), _parse_utc(item["end_utc"]))
        for item in selected
    )
    candidate_states = {item["full_state_sha256"] for item in candidates}
    selected_states = {item["full_state_sha256"] for item in selected}
    candidate_dates = {item["civil_date"] for item in candidates}
    selected_dates = {item["civil_date"] for item in selected}
    intersects = any(
        max(_parse_utc(item["start_utc"]), reference_start)
        < min(_parse_utc(item["end_utc"]), reference_end)
        for item in selected
    )
    result_metrics: JsonObject = {
        "reference_intersection": {"status": "applicable", "value": intersects},
        "temporal_width_retained": _fraction(
            selected_width, candidate_width, "width_microseconds"
        ),
        "canonical_interval_count_retained": _fraction(
            len(selected), len(candidates), "interval_count"
        ),
        "unique_state_identity_count_retained": _fraction(
            len(selected_states), len(candidate_states), "unique_state_identity_count"
        ),
        "date_coverage": _fraction(len(selected_dates), len(candidate_dates), "date_count"),
        "documentary_reference_width": {
            "status": "applicable",
            "microseconds": documentary_width,
        },
        "abstention": {"status": "applicable", "value": False},
    }
    return {
        "receipt_kind": "descriptive_metric_receipt",
        "evaluation_eligible": True,
        "metrics": result_metrics,
    }


def evaluate_preconstructed_fixture(
    inference_fixture: Mapping[str, object],
    evaluator_reference_loader: Callable[[], Mapping[str, object]],
) -> OracleEvaluation:
    """Evaluate one fixed synthetic case without generating or choosing ``S_i``."""

    fixture_id = cast(str, inference_fixture.get("fixture_id", "SYNTH-FIXTURE-REJECTED"))
    phase = "new"
    reference_loads = 0
    loads_before_commit = 0
    selected: tuple[Mapping[str, object], ...] = ()
    candidates: tuple[Mapping[str, object], ...] = ()
    output_kind = "candidate_subset"
    s_i_commitment: str | None = None
    opened_reference: Mapping[str, object] | None = None
    trace: list[str] = []
    try:
        _scan_prohibited(inference_fixture)
        candidates = _validated_candidate_set(inference_fixture.get("candidate_set"))
        _validate_components(
            inference_fixture.get("component_assignments"),
            inference_fixture.get("contamination_status"),
        )
        output_kind, selected, s_i_commitment = _validate_output(
            inference_fixture.get("preconstructed_output"), candidates
        )
        plan = _sequence(inference_fixture.get("execution_plan"), "unknown_execution_event")
        for raw_event in plan:
            if not isinstance(raw_event, str):
                _reject("unknown_execution_event")
            event = raw_event
            trace.append(event)
            if event == "candidate_domain_freeze":
                if phase != "new":
                    _reject("candidate_freeze_out_of_order")
                phase = "candidate_frozen"
            elif event == "study_method_specification_freeze":
                if phase != "candidate_frozen":
                    _reject("method_freeze_out_of_order")
                phase = "method_frozen"
            elif event == "preconstructed_s_i_commitment":
                if phase != "method_frozen":
                    _reject("s_i_commitment_out_of_order")
                phase = "s_i_committed"
            elif event in _EARLY_EVENTS:
                _reject(_EARLY_EVENTS[event])
            elif event == "evaluator_only_t_i_access":
                if phase != "s_i_committed":
                    _reject("t_i_access_before_s_i_commitment")
                if phase != "s_i_committed":
                    loads_before_commit += 1
                opened_reference = deepcopy(dict(evaluator_reference_loader()))
                reference_loads += 1
                phase = "reference_exposed"
            elif event == "post_reference_s_i_mutation_attempt":
                if phase == "reference_exposed":
                    _reject("s_i_modified_after_t_i_exposure")
                _reject("s_i_commitment_out_of_order")
            elif event == "post_reference_t_i_mutation_attempt":
                _reject("t_i_mutated_after_evaluator_access")
            elif event == "metric_receipt":
                if phase != "reference_exposed" or opened_reference is None:
                    _reject("metric_receipt_before_t_i_access")
                result = _reference_result(
                    opened_reference, candidates, selected, output_kind
                )
                result["s_i_commitment_sha256"] = s_i_commitment
                result["inference_or_selection_performed"] = False
                return OracleEvaluation(
                    fixture_id,
                    result,
                    {
                        "events": trace,
                        "reference_load_count": reference_loads,
                        "reference_loads_before_s_i_commitment": loads_before_commit,
                    },
                )
            else:
                _reject("unknown_execution_event")
        _reject("metric_receipt_missing")
    except OracleViolation as exc:
        return OracleEvaluation(
            fixture_id,
            {
                "receipt_kind": "fail_closed_rejection",
                "violation_codes": [exc.code],
                "inference_or_selection_performed": False,
            },
            {
                "events": trace,
                "reference_load_count": reference_loads,
                "reference_loads_before_s_i_commitment": loads_before_commit,
            },
        )


def validate_receipt_guard(receipt: Mapping[str, object]) -> tuple[bool, str | None]:
    """Independently guard a postcommit artifact against rehashed forbidden fields."""

    try:
        _scan_prohibited(receipt)
        raw = dict(receipt)
        embedded = raw.pop("receipt_sha256", None)
        if not isinstance(embedded, str) or embedded != independent_sha256_json(raw):
            _reject("receipt_self_hash_mismatch")
    except OracleViolation as exc:
        return (False, exc.code)
    return (True, None)
