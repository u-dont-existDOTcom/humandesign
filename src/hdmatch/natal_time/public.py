"""Synthetic-only allowlist serializer for public-safe foundation receipts."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from hdmatch.natal_time.models import NatalTimeModel
from hdmatch.natal_time.records import (
    FixtureClassification,
    MechanicStatus,
    NatalTimeManifest,
    NatalTimeResult,
)


class SyntheticPublicNatalTimeArtifact(NatalTimeModel):
    schema_version: Literal["synthetic-public-natal-time-foundation-v1"] = (
        "synthetic-public-natal-time-foundation-v1"
    )
    public_id: str = Field(pattern=r"^NTP-[A-F0-9]{24}$")
    synthetic: Literal[True] = True
    manifest_schema_version: Literal["natal-time-manifest-v1"]
    result_schema_version: Literal["natal-time-result-v1"]
    candidate_date_count: int = Field(gt=0)
    interval_count: int = Field(gt=0)
    stable_field_paths: tuple[str, ...]
    variable_field_paths: tuple[str, ...]
    unresolved_field_paths: tuple[str, ...]
    coverage_complete: Literal[True] = True
    contains_participant_level_record: Literal[False] = False
    contains_exact_birth_data: Literal[False] = False
    contains_relationship_evidence: Literal[False] = False
    contains_private_linkage_hash: Literal[False] = False


def serialize_synthetic_public_artifact(
    manifest: NatalTimeManifest,
    result: NatalTimeResult,
    *,
    independent_public_id: str,
) -> SyntheticPublicNatalTimeArtifact:
    """Allow only aggregate field-path facts from conspicuously synthetic runs."""

    if manifest.fixture_classification is not FixtureClassification.SYNTHETIC:
        raise ValueError("real participant natal-time export is disabled before checkpoint 2")
    if result.manifest_sha256 != manifest.content_sha256:
        raise ValueError("result does not bind the supplied synthetic manifest")
    return SyntheticPublicNatalTimeArtifact(
        public_id=independent_public_id,
        manifest_schema_version=manifest.schema_version,
        result_schema_version=result.schema_version,
        candidate_date_count=len(manifest.candidate_dates),
        interval_count=len(result.intervals),
        stable_field_paths=tuple(
            item.path for item in result.mechanic_facts if item.status is MechanicStatus.STABLE
        ),
        variable_field_paths=tuple(
            item.path for item in result.mechanic_facts if item.status is MechanicStatus.VARIABLE
        ),
        unresolved_field_paths=tuple(
            item.path for item in result.mechanic_facts if item.status is MechanicStatus.UNRESOLVED
        ),
    )
