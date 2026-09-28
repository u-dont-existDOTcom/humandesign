"""Mechanical freeze, multiplicity, and cohort-isolation gates for v1b."""

from __future__ import annotations

import math
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime

SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")

FREEZE_MANIFEST_REQUIRED_FIELDS = frozenset(
    {
        "decision_sha256",
        "reviewed_evidence_commit",
        "protocol_version",
        "software_commit",
        "ethics_consent_data_access_basis",
        "cohort_opening_utc",
        "cohort_closing_utc",
        "candidate_network_manifest_sha256",
        "selected_network_manifest_sha256",
        "lineage_exclusion_log_sha256",
        "participant_allocation_sha256",
        "relationship_component_registry_sha256",
        "birth_input_provenance_sha256",
        "covariate_registry_sha256",
        "pair_registry_sha256",
        "questionnaire_text_sha256",
        "questionnaire_instructions_sha256",
        "scoring_key_sha256",
        "questionnaire_package_sha256",
        "outcomes_inaccessible_attestation",
        "blind_custodian_id",
        "model_matrix_specification_sha256",
        "power_null_calibration_report_sha256",
        "software_dependency_manifest_sha256",
        "random_seed_manifest_sha256",
        "freeze_timestamp_utc",
    }
)

HASH_FIELDS = frozenset(
    field for field in FREEZE_MANIFEST_REQUIRED_FIELDS if field.endswith("sha256")
)


class FreezeManifestError(ValueError):
    """Raised when a pre-outcome freeze manifest is incomplete or malformed."""


def validate_freeze_manifest(manifest: Mapping[str, object]) -> None:
    """Validate required operational placeholders before any launch-capable state.

    Passing this structural validator does not authorize recruitment or collection.
    """

    missing = sorted(FREEZE_MANIFEST_REQUIRED_FIELDS - set(manifest))
    extra = sorted(set(manifest) - FREEZE_MANIFEST_REQUIRED_FIELDS)
    if missing or extra:
        raise FreezeManifestError(
            f"freeze manifest fields differ; missing={missing}, extra={extra}"
        )
    for field in HASH_FIELDS:
        value = manifest[field]
        if not isinstance(value, str) or SHA256_PATTERN.fullmatch(value) is None:
            raise FreezeManifestError(f"{field} must be a lowercase hexadecimal SHA256")
    for field in (
        "reviewed_evidence_commit",
        "software_commit",
    ):
        value = manifest[field]
        if not isinstance(value, str) or SHA256_PATTERN.fullmatch(value) is None:
            raise FreezeManifestError(f"{field} must be a lowercase hexadecimal commit SHA")
    for field in (
        "protocol_version",
        "ethics_consent_data_access_basis",
        "outcomes_inaccessible_attestation",
        "blind_custodian_id",
    ):
        value = manifest[field]
        if not isinstance(value, str) or not value.strip():
            raise FreezeManifestError(f"{field} must be a nonempty string")
    for field in ("cohort_opening_utc", "cohort_closing_utc", "freeze_timestamp_utc"):
        value = manifest[field]
        if not isinstance(value, str):
            raise FreezeManifestError(f"{field} must be an ISO-8601 UTC string")
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise FreezeManifestError(f"{field} is not valid ISO-8601") from exc
        offset = parsed.utcoffset()
        if offset is None or offset.total_seconds() != 0.0:
            raise FreezeManifestError(f"{field} must resolve to UTC")
    opening = datetime.fromisoformat(str(manifest["cohort_opening_utc"]).replace("Z", "+00:00"))
    closing = datetime.fromisoformat(str(manifest["cohort_closing_utc"]).replace("Z", "+00:00"))
    frozen = datetime.fromisoformat(str(manifest["freeze_timestamp_utc"]).replace("Z", "+00:00"))
    if not frozen < opening < closing:
        raise FreezeManifestError(
            "freeze_timestamp_utc must precede opening, which must precede closing"
        )
    if (closing - opening).total_seconds() != 30 * 86400:
        raise FreezeManifestError("the response window must be exactly 30*86400 seconds")


@dataclass(frozen=True, slots=True)
class CohortEntities:
    participant_ids: frozenset[str]
    relationship_component_ids: frozenset[str]
    hospital_ids: frozenset[str]
    network_ids: frozenset[str]


def ensure_disjoint_cohorts(left: CohortEntities, right: CohortEntities) -> None:
    """Fail on any person, relationship, hospital, or network overlap."""

    for field in (
        "participant_ids",
        "relationship_component_ids",
        "hospital_ids",
        "network_ids",
    ):
        overlap = getattr(left, field) & getattr(right, field)
        if overlap:
            raise ValueError(f"cross-cohort overlap in {field}: {sorted(overlap)}")


@dataclass(frozen=True, slots=True)
class HolmResult:
    original_index: int
    p_value: float
    adjusted_p_value: float
    rejected: bool


def holm_family(p_values: Sequence[float], *, alpha: float = 0.05) -> tuple[HolmResult, ...]:
    """Apply Holm correction to one fixed family without dropping failed tests."""

    if not p_values:
        raise ValueError("Holm family cannot be empty")
    if not math.isfinite(alpha) or not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be finite and in (0,1)")
    checked: list[tuple[int, float]] = []
    for index, raw in enumerate(p_values):
        value = float(raw)
        if not math.isfinite(value) or not 0.0 <= value <= 1.0:
            raise ValueError("every p-value must be finite and in [0,1]")
        checked.append((index, value))
    ordered = sorted(checked, key=lambda item: (item[1], item[0]))
    running_adjusted = 0.0
    rejection_open = True
    by_index: dict[int, HolmResult] = {}
    family_size = len(ordered)
    for rank, (index, value) in enumerate(ordered):
        multiplier = family_size - rank
        adjusted = min(1.0, max(running_adjusted, multiplier * value))
        running_adjusted = adjusted
        threshold = alpha / multiplier
        rejected = rejection_open and value <= threshold
        if not rejected:
            rejection_open = False
        by_index[index] = HolmResult(index, value, adjusted, rejected)
    return tuple(by_index[index] for index in range(family_size))


def require_exact_diagnostic_family(p_values: Iterable[float]) -> tuple[HolmResult, ...]:
    """Correct exactly twenty random-feature and one maternal-age diagnostic."""

    values = tuple(p_values)
    if len(values) != 21:
        raise ValueError("the frozen diagnostic family contains exactly 21 tests")
    return holm_family(values, alpha=0.05)
