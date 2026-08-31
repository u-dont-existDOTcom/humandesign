"""Pure builders for manifest and pre-enumeration freeze records."""

from __future__ import annotations

from datetime import UTC, datetime
from secrets import token_hex

from hdmatch.natal_time.models import EvidenceAssessment, EvidenceLineage
from hdmatch.natal_time.provenance import EngineProvenance, StateIdentitySpecification
from hdmatch.natal_time.records import (
    FixtureClassification,
    NatalTimeFreeze,
    NatalTimeManifest,
    TimezoneResolution,
    deterministic_computation_sha256,
)


def create_manifest(
    lineage: EvidenceLineage,
    assessment: EvidenceAssessment,
    *,
    timezone_resolution: TimezoneResolution,
    engine_provenance: EngineProvenance,
    state_identity: StateIdentitySpecification,
    fixture_classification: FixtureClassification,
    created_at_utc: datetime | None = None,
    supersedes_manifest_sha256: str | None = None,
) -> NatalTimeManifest:
    if assessment.lineage_sha256 != lineage.content_sha256:
        raise ValueError("assessment does not bind the supplied evidence lineage")
    if not assessment.enumeration_allowed:
        raise ValueError("fail-closed evidence state cannot create an enumerable manifest")
    if not assessment.operative_dates:
        raise ValueError("manifest requires an explicit candidate-date set")
    return NatalTimeManifest(
        manifest_id="NTM-" + token_hex(12).upper(),
        created_at_utc=created_at_utc or datetime.now(UTC),
        evidence_lineage_sha256=lineage.content_sha256,
        candidate_dates=assessment.operative_dates,
        timezone_resolution=timezone_resolution,
        engine_provenance=engine_provenance,
        state_identity_specification=state_identity,
        state_identity_sha256=state_identity.content_sha256,
        fixture_classification=fixture_classification,
        supersedes_manifest_sha256=supersedes_manifest_sha256,
    )


def create_freeze(
    manifest: NatalTimeManifest,
    *,
    created_at_utc: datetime | None = None,
    supersedes_freeze_sha256: str | None = None,
) -> NatalTimeFreeze:
    return NatalTimeFreeze(
        freeze_id="NTF-" + token_hex(12).upper(),
        created_at_utc=created_at_utc or datetime.now(UTC),
        manifest_sha256=manifest.content_sha256,
        deterministic_computation_sha256=deterministic_computation_sha256(manifest),
        repository_commit=manifest.engine_provenance.repository_commit,
        engine_provenance_sha256=manifest.engine_provenance.content_sha256,
        state_identity_sha256=manifest.state_identity_sha256,
        supersedes_freeze_sha256=supersedes_freeze_sha256,
    )
