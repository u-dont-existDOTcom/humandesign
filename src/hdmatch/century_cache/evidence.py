"""Re-verifiable proof artifacts required by the canonical century cache."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_bytes
from hdmatch.provenance.swisseph_files import VerifiedEphemerisProvenance

from .models import (
    GIT_COMMIT_PATTERN,
    SHA256_PATTERN,
    CenturyCacheBuildSpec,
    CenturyCacheEvidenceArtifact,
    CenturyCacheManifest,
    ExactStateUniverseProvenance,
)

ENGINE_EVIDENCE_FILENAME = "evidence/engine-validation.json"
PARITY_EVIDENCE_FILENAME = "evidence/parity-report.json"
BOUNDARY_AUDIT_EVIDENCE_FILENAME = "evidence/boundary-audit-report.json"
PARITY_REFERENCE_FILENAME = "evidence/parity-reference-source.json"
RECONCILIATION_EVIDENCE_FILENAME = "evidence/reconciliation-aggregate.json"


class CenturyCacheEvidenceError(ValueError):
    """A proof artifact is missing, malformed, substituted, or semantically invalid."""


class _EvidenceModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class _EngineFile(_EvidenceModel):
    name: str = Field(min_length=1)
    sha256: str = Field(pattern=SHA256_PATTERN)
    size_bytes: int = Field(gt=0)


class _CalculationProbe(_EvidenceModel):
    at_utc: datetime
    body: str = Field(min_length=1)
    longitude: float
    speed_degrees_per_day: float
    gate: int = Field(ge=1, le=64)
    line: int = Field(ge=1, le=6)
    requested_mode: Literal["SWIEPH"]
    returned_mode: Literal["SWIEPH"]
    requested_flags: int = Field(gt=0)
    returned_flags: int = Field(gt=0)
    ephemeris_mask: int = Field(gt=0)
    used_file_name: str = Field(min_length=1)
    used_file_sha256: str = Field(pattern=SHA256_PATTERN)

    @field_validator("at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("engine calculation-probe timestamp must be timezone-aware")
        return value.astimezone(UTC)


class _DesignRootProbe(_EvidenceModel):
    personality_utc: datetime
    design_utc: datetime
    target_arc_degrees: float
    solved_arc_degrees: float
    residual_degrees: float
    time_tolerance_seconds: float = Field(gt=0.0)
    arc_tolerance_degrees: float = Field(gt=0.0)

    @field_validator("personality_utc", "design_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Design-root probe timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_converged_root(self) -> _DesignRootProbe:
        if self.design_utc >= self.personality_utc:
            raise ValueError("Design-root probe does not precede Personality")
        if abs(self.residual_degrees) > self.arc_tolerance_degrees:
            raise ValueError("Design-root probe residual exceeds its declared tolerance")
        if not math.isclose(
            self.solved_arc_degrees - self.target_arc_degrees,
            self.residual_degrees,
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise ValueError("Design-root residual is inconsistent with the solved arc")
        return self


class _EngineValidation(_EvidenceModel):
    schema_version: Literal["production-engine-validation-v1"]
    validation_status: Literal["pass"]
    provider: Literal["swiss_ephemeris_local_files"]
    library_version: str = Field(min_length=1)
    ephemeris_requested: Literal["SWIEPH"]
    ephemeris_returned: Literal["SWIEPH"]
    requested_flags: int = Field(gt=0)
    ephemeris_mask: int = Field(gt=0)
    files: tuple[_EngineFile, ...] = Field(min_length=2)
    calculation_probes: tuple[_CalculationProbe, ...] = Field(min_length=2)
    design_root_probes: tuple[_DesignRootProbe, ...] = Field(min_length=1)
    gate_line_deterministic: Literal[True]
    design_root_converged: Literal[True]
    node_convention: Literal["true"]

    @model_validator(mode="after")
    def require_unique_files(self) -> _EngineValidation:
        names = tuple(item.name for item in self.files)
        if len(names) != len(set(names)):
            raise ValueError("engine validation contains duplicate file records")
        return self


class EngineValidationReceipt(_EvidenceModel):
    """Path-free Phase-0 receipt consumed as cache-generation evidence."""

    schema_version: Literal["production-engine-validation-receipt-v1"]
    validation_status: Literal["pass"]
    software_commit: str = Field(pattern=GIT_COMMIT_PATTERN)
    software_dirty: Literal[False]
    software_environment: dict[str, JsonValue]
    ephemeris_mode_argument: Literal["SWIEPH"]
    ephemeris_provenance: VerifiedEphemerisProvenance
    engine_validation: _EngineValidation
    claim_boundary: Literal[
        "astronomy-engine-phase-0-only-not-a-v4-3-cache-or-behavioral-result"
    ]


class CenturyCacheParityReport(_EvidenceModel):
    """Frozen independent engine-parity evidence for a cache universe."""

    schema_version: Literal["century-cache-parity-report-v1"]
    validation_status: Literal["pass"]
    engine_validation_sha256: str = Field(pattern=SHA256_PATTERN)
    ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_vector_schema_version: str = Field(min_length=1)
    utc_start: datetime
    utc_end_exclusive: datetime
    reference_source_locator: str = Field(min_length=1)
    reference_source_sha256: str = Field(pattern=SHA256_PATTERN)
    comparison_count: int = Field(gt=0)
    mismatch_count: Literal[0]
    tolerance_degrees: float = Field(gt=0.0)
    max_abs_longitude_error_degrees: float = Field(ge=0.0)

    @field_validator("utc_start", "utc_end_exclusive")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("parity-report timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_passing_parity(self) -> CenturyCacheParityReport:
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("parity-report range must be positive")
        if self.max_abs_longitude_error_degrees > self.tolerance_degrees:
            raise ValueError("parity error exceeds the declared tolerance")
        return self


class CenturyCacheBoundaryAuditReport(_EvidenceModel):
    """Frozen exact-coverage/maximality audit for the logical cache universe."""

    schema_version: Literal["century-cache-boundary-audit-report-v1"]
    validation_status: Literal["pass"]
    engine_validation_sha256: str = Field(pattern=SHA256_PATTERN)
    logical_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    bodygraph_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_policy_version: str = Field(min_length=1)
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)
    utc_start: datetime
    utc_end_exclusive: datetime
    interval_count: int = Field(gt=0)
    audited_boundary_event_count: int = Field(ge=0)
    missing_boundary_count: Literal[0]
    gap_count: Literal[0]
    overlap_count: Literal[0]
    maximality_violation_count: Literal[0]

    @field_validator("utc_start", "utc_end_exclusive")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("boundary-audit timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_positive_range(self) -> CenturyCacheBoundaryAuditReport:
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("boundary-audit range must be positive")
        return self


@dataclass(frozen=True, slots=True)
class CenturyCacheEvidenceInputs:
    """External proof and ephemeris inputs required by the explicit writer."""

    engine_validation_path: Path
    parity_report_path: Path
    boundary_audit_report_path: Path
    reconciliation_aggregate_path: Path | None
    parity_reference_source_path: Path
    ephemeris_source_manifest_path: Path
    ephemeris_directory: Path


@dataclass(frozen=True, slots=True)
class ValidatedCenturyCacheEvidence:
    """Canonical bytes and manifest bindings after semantic validation."""

    artifacts: tuple[CenturyCacheEvidenceArtifact, ...]
    bundled_bytes: tuple[tuple[str, bytes], ...]


def _read_canonical_json(path: Path, *, label: str) -> tuple[bytes, object]:
    if path.is_symlink():
        raise CenturyCacheEvidenceError(f"{label} must not be a symbolic link")
    try:
        raw = path.read_bytes()
        parsed = json.loads(raw)
        if canonical_json_bytes(parsed) != raw:
            raise ValueError("artifact is not canonically encoded")
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise CenturyCacheEvidenceError(f"invalid {label} artifact") from exc
    return raw, parsed


def _read_reference_bytes(path: Path) -> bytes:
    if path.is_symlink():
        raise CenturyCacheEvidenceError(
            "parity reference source must not be a symbolic link"
        )
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise CenturyCacheEvidenceError("invalid parity reference-source artifact") from exc
    if not raw:
        raise CenturyCacheEvidenceError("parity reference-source artifact is empty")
    return raw


def _validate_engine_receipt(
    raw: bytes,
    spec: CenturyCacheBuildSpec | CenturyCacheManifest,
) -> EngineValidationReceipt:
    try:
        receipt = EngineValidationReceipt.model_validate_json(raw, strict=True)
    except ValueError as exc:
        raise CenturyCacheEvidenceError("invalid engine-validation evidence") from exc
    if receipt.ephemeris_provenance != spec.engine.ephemeris_provenance:
        raise CenturyCacheEvidenceError(
            "engine-validation ephemeris provenance differs from the cache contract"
        )
    validation = receipt.engine_validation
    expected_engine = spec.engine
    scalar_bindings = {
        "provider": (validation.provider, expected_engine.provider),
        "library version": (
            validation.library_version,
            expected_engine.swiss_library_version,
        ),
        "requested flags": (validation.requested_flags, expected_engine.requested_flags),
        "ephemeris mask": (validation.ephemeris_mask, expected_engine.ephemeris_mask),
        "node convention": (validation.node_convention, spec.node_convention),
    }
    for label, (actual, expected) in scalar_bindings.items():
        if actual != expected:
            raise CenturyCacheEvidenceError(
                f"engine-validation {label} differs from the cache contract"
            )
    provenance_files = {
        item.name: (item.bytes, item.sha256)
        for item in expected_engine.ephemeris_provenance.files
    }
    validation_files = {
        item.name: (item.size_bytes, item.sha256) for item in validation.files
    }
    if validation_files != provenance_files:
        raise CenturyCacheEvidenceError(
            "engine-validation file identities differ from verified ephemeris provenance"
        )
    observed_flags = tuple(
        sorted({probe.returned_flags for probe in validation.calculation_probes})
    )
    if observed_flags != expected_engine.returned_flags_observed:
        raise CenturyCacheEvidenceError(
            "engine-validation returned flags differ from the cache contract"
        )
    used_files: set[str] = set()
    for probe in validation.calculation_probes:
        if probe.requested_flags != expected_engine.requested_flags:
            raise CenturyCacheEvidenceError("engine probe requested unexpected flags")
        if probe.ephemeris_mask != expected_engine.ephemeris_mask:
            raise CenturyCacheEvidenceError("engine probe used an unexpected ephemeris mask")
        if probe.returned_flags & expected_engine.ephemeris_mask != (
            expected_engine.swieph_flag
        ):
            raise CenturyCacheEvidenceError("engine probe did not return SWIEPH")
        expected_file = provenance_files.get(probe.used_file_name)
        if expected_file is None or probe.used_file_sha256 != expected_file[1]:
            raise CenturyCacheEvidenceError(
                "engine probe used a file outside verified ephemeris provenance"
            )
        used_files.add(probe.used_file_name)
    if used_files != set(provenance_files):
        raise CenturyCacheEvidenceError(
            "engine-validation probes do not exercise the complete ephemeris file set"
        )
    for root in validation.design_root_probes:
        if root.time_tolerance_seconds != spec.design_root_time_tolerance_seconds:
            raise CenturyCacheEvidenceError(
                "engine-validation Design-root time tolerance mismatch"
            )
        if root.arc_tolerance_degrees != spec.design_root_arc_tolerance_degrees:
            raise CenturyCacheEvidenceError(
                "engine-validation Design-root arc tolerance mismatch"
            )
    return receipt


def _validate_parity_report(
    raw: bytes,
    spec: CenturyCacheBuildSpec | CenturyCacheManifest,
) -> CenturyCacheParityReport:
    try:
        report = CenturyCacheParityReport.model_validate_json(raw, strict=True)
    except ValueError as exc:
        raise CenturyCacheEvidenceError("invalid parity evidence") from exc
    expected = {
        "engine-validation hash": (
            report.engine_validation_sha256,
            spec.engine.engine_validation_sha256,
        ),
        "ephemeris file-set hash": (
            report.ephemeris_file_set_sha256,
            spec.engine.ephemeris_provenance.ephemeris_file_set_sha256,
        ),
        "feature-vector schema": (
            report.feature_vector_schema_version,
            spec.feature_vector_schema_version,
        ),
        "UTC start": (report.utc_start, spec.utc_start),
        "UTC end": (report.utc_end_exclusive, spec.utc_end_exclusive),
        "reference-source locator": (
            report.reference_source_locator,
            spec.parity_reference_source_locator,
        ),
        "reference-source hash": (
            report.reference_source_sha256,
            spec.parity_reference_source_sha256,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise CenturyCacheEvidenceError(f"parity-report {label} mismatch")
    return report


def _validate_boundary_audit_report(
    raw: bytes,
    spec: CenturyCacheBuildSpec | CenturyCacheManifest,
    *,
    logical_universe_sha256: str,
    interval_count: int,
    boundary_event_count: int,
) -> CenturyCacheBoundaryAuditReport:
    try:
        report = CenturyCacheBoundaryAuditReport.model_validate_json(raw, strict=True)
    except ValueError as exc:
        raise CenturyCacheEvidenceError("invalid boundary-audit evidence") from exc
    expected = {
        "engine-validation hash": (
            report.engine_validation_sha256,
            spec.engine.engine_validation_sha256,
        ),
        "logical-universe hash": (
            report.logical_universe_sha256,
            logical_universe_sha256,
        ),
        "semantic feature-registry hash": (
            report.semantic_feature_registry_sha256,
            spec.semantic_feature_registry_sha256,
        ),
        "feature-registry hash": (
            report.feature_registry_sha256,
            spec.feature_registry_sha256,
        ),
        "Mandala mapping hash": (
            report.mandala_mapping_sha256,
            spec.mandala_mapping_sha256,
        ),
        "Bodygraph mapping hash": (
            report.bodygraph_mapping_sha256,
            spec.bodygraph_mapping_sha256,
        ),
        "boundary policy": (
            report.boundary_policy_version,
            spec.boundary_policy_version,
        ),
        "Design-root time tolerance": (
            report.design_root_time_tolerance_seconds,
            spec.design_root_time_tolerance_seconds,
        ),
        "Design-root arc tolerance": (
            report.design_root_arc_tolerance_degrees,
            spec.design_root_arc_tolerance_degrees,
        ),
        "UTC start": (report.utc_start, spec.utc_start),
        "UTC end": (report.utc_end_exclusive, spec.utc_end_exclusive),
        "interval count": (report.interval_count, interval_count),
        "boundary-event count": (
            report.audited_boundary_event_count,
            boundary_event_count,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise CenturyCacheEvidenceError(f"boundary-audit {label} mismatch")
    return report


def _validate_evidence(
    *,
    engine_path: Path,
    parity_path: Path,
    boundary_path: Path,
    reconciliation_path: Path | None,
    parity_reference_path: Path,
    spec: CenturyCacheBuildSpec | CenturyCacheManifest,
    logical_universe_sha256: str,
    interval_count: int,
    boundary_event_count: int,
    exact_state_provenance: ExactStateUniverseProvenance,
) -> ValidatedCenturyCacheEvidence:
    engine_raw, _ = _read_canonical_json(engine_path, label="engine-validation")
    parity_raw, _ = _read_canonical_json(parity_path, label="parity")
    boundary_raw, _ = _read_canonical_json(boundary_path, label="boundary-audit")
    parity_reference_raw = _read_reference_bytes(parity_reference_path)
    expected_hashes = {
        "engine-validation": (
            sha256_bytes(engine_raw),
            spec.engine.engine_validation_sha256,
        ),
        "parity": (sha256_bytes(parity_raw), spec.parity_report_sha256),
        "boundary-audit": (
            sha256_bytes(boundary_raw),
            spec.boundary_audit_report_sha256,
        ),
    }
    for label, (actual, expected) in expected_hashes.items():
        if actual != expected:
            raise CenturyCacheEvidenceError(f"{label} artifact SHA-256 mismatch")
    if sha256_bytes(parity_reference_raw) != spec.parity_reference_source_sha256:
        raise CenturyCacheEvidenceError("parity reference-source artifact SHA-256 mismatch")
    engine = _validate_engine_receipt(engine_raw, spec)
    parity = _validate_parity_report(parity_raw, spec)
    boundary = _validate_boundary_audit_report(
        boundary_raw,
        spec,
        logical_universe_sha256=logical_universe_sha256,
        interval_count=interval_count,
        boundary_event_count=boundary_event_count,
    )
    artifacts_list = [
        CenturyCacheEvidenceArtifact(
            kind="engine_validation",
            filename=ENGINE_EVIDENCE_FILENAME,
            sha256=expected_hashes["engine-validation"][0],
            schema_version=engine.schema_version,
            validation_status=engine.validation_status,
        ),
        CenturyCacheEvidenceArtifact(
            kind="parity",
            filename=PARITY_EVIDENCE_FILENAME,
            sha256=expected_hashes["parity"][0],
            schema_version=parity.schema_version,
            validation_status=parity.validation_status,
        ),
        CenturyCacheEvidenceArtifact(
            kind="boundary_audit",
            filename=BOUNDARY_AUDIT_EVIDENCE_FILENAME,
            sha256=expected_hashes["boundary-audit"][0],
            schema_version=boundary.schema_version,
            validation_status=boundary.validation_status,
        ),
    ]
    bundled_list = [
        (ENGINE_EVIDENCE_FILENAME, engine_raw),
        (PARITY_EVIDENCE_FILENAME, parity_raw),
        (BOUNDARY_AUDIT_EVIDENCE_FILENAME, boundary_raw),
        (PARITY_REFERENCE_FILENAME, parity_reference_raw),
    ]
    if spec.reconciliation_aggregate_sha256 is None:
        if reconciliation_path is not None:
            raise CenturyCacheEvidenceError(
                "reconciliation artifact was supplied without a declared binding"
            )
    else:
        if reconciliation_path is None:
            raise CenturyCacheEvidenceError(
                "declared reconciliation aggregate artifact is missing"
            )
        reconciliation_raw, reconciliation_payload = _read_canonical_json(
            reconciliation_path,
            label="reconciliation-aggregate",
        )
        if sha256_bytes(reconciliation_raw) != spec.reconciliation_aggregate_sha256:
            raise CenturyCacheEvidenceError(
                "reconciliation-aggregate artifact SHA-256 mismatch"
            )
        if not isinstance(reconciliation_payload, dict):
            raise CenturyCacheEvidenceError(
                "reconciliation-aggregate payload must be an object"
            )
        if reconciliation_payload.get("schema_version") != (
            "exact-state-reconciliation-aggregate-v1"
        ) or reconciliation_payload.get("status") != "pass":
            raise CenturyCacheEvidenceError(
                "reconciliation-aggregate schema/status is invalid"
            )
        required_reconciliation_fields = {
            "reconciliation_policy_version",
            "boundary_event_catalog_sha256",
            "ordered_sources",
            "ordered_core_reconciliation_receipt_sha256s",
            "ordered_output_chunk_provenance_sha256s",
            "exact_state_universe_provenance",
        }
        missing_reconciliation_fields = sorted(
            required_reconciliation_fields - set(reconciliation_payload)
        )
        if missing_reconciliation_fields:
            raise CenturyCacheEvidenceError(
                "reconciliation-aggregate is missing required provenance fields: "
                f"{missing_reconciliation_fields}"
            )
        if not {
            "reconciliation_calculation_audit",
            "reconciliation_calculation_audit_sha256",
        } & set(reconciliation_payload):
            raise CenturyCacheEvidenceError(
                "reconciliation-aggregate lacks calculation-audit provenance"
            )
        try:
            embedded_exact = ExactStateUniverseProvenance.model_validate_json(
                canonical_json_bytes(
                    reconciliation_payload.get("exact_state_universe_provenance")
                ),
                strict=True,
            )
        except ValueError as exc:
            raise CenturyCacheEvidenceError(
                "reconciliation-aggregate exact-state provenance is invalid"
            ) from exc
        if embedded_exact != exact_state_provenance:
            raise CenturyCacheEvidenceError(
                "reconciliation-aggregate exact-state provenance mismatch"
            )
        artifacts_list.append(
            CenturyCacheEvidenceArtifact(
                kind="reconciliation",
                filename=RECONCILIATION_EVIDENCE_FILENAME,
                sha256=sha256_bytes(reconciliation_raw),
                schema_version="exact-state-reconciliation-aggregate-v1",
                validation_status="pass",
            )
        )
        bundled_list.append((RECONCILIATION_EVIDENCE_FILENAME, reconciliation_raw))
    artifacts = tuple(sorted(artifacts_list, key=lambda item: item.kind))
    bundled = tuple(sorted(bundled_list))
    return ValidatedCenturyCacheEvidence(artifacts=artifacts, bundled_bytes=bundled)


def validate_external_cache_evidence(
    inputs: CenturyCacheEvidenceInputs,
    *,
    spec: CenturyCacheBuildSpec,
    logical_universe_sha256: str,
    interval_count: int,
    boundary_event_count: int,
    exact_state_provenance: ExactStateUniverseProvenance,
) -> ValidatedCenturyCacheEvidence:
    """Open, hash, parse, and semantically validate external proof inputs."""

    return _validate_evidence(
        engine_path=inputs.engine_validation_path,
        parity_path=inputs.parity_report_path,
        boundary_path=inputs.boundary_audit_report_path,
        reconciliation_path=inputs.reconciliation_aggregate_path,
        parity_reference_path=inputs.parity_reference_source_path,
        spec=spec,
        logical_universe_sha256=logical_universe_sha256,
        interval_count=interval_count,
        boundary_event_count=boundary_event_count,
        exact_state_provenance=exact_state_provenance,
    )


def validate_engine_validation_evidence(
    path: str | Path,
    *,
    spec: CenturyCacheBuildSpec | CenturyCacheManifest,
) -> EngineValidationReceipt:
    """Validate a Phase-0 receipt's exact bytes and semantic cache bindings."""

    receipt_path = Path(path)
    raw, _ = _read_canonical_json(receipt_path, label="engine-validation")
    if sha256_bytes(raw) != spec.engine.engine_validation_sha256:
        raise CenturyCacheEvidenceError("engine-validation artifact SHA-256 mismatch")
    return _validate_engine_receipt(raw, spec)


def validate_bundled_cache_evidence(
    cache_directory: Path,
    *,
    manifest: CenturyCacheManifest,
) -> ValidatedCenturyCacheEvidence:
    """Re-open all bundled proof artifacts during ordinary cache verification."""

    artifacts = {item.kind: item for item in manifest.evidence_artifacts}
    validated = _validate_evidence(
        engine_path=cache_directory / artifacts["engine_validation"].filename,
        parity_path=cache_directory / artifacts["parity"].filename,
        boundary_path=cache_directory / artifacts["boundary_audit"].filename,
        reconciliation_path=(
            cache_directory / artifacts["reconciliation"].filename
            if "reconciliation" in artifacts
            else None
        ),
        parity_reference_path=cache_directory / PARITY_REFERENCE_FILENAME,
        spec=manifest,
        logical_universe_sha256=manifest.logical_universe_sha256,
        interval_count=manifest.interval_count,
        boundary_event_count=(
            manifest.exact_state_provenance.boundary_event_count
        ),
        exact_state_provenance=manifest.exact_state_provenance,
    )
    if validated.artifacts != manifest.evidence_artifacts:
        raise CenturyCacheEvidenceError(
            "bundled proof metadata differs from the cache manifest"
        )
    return validated
