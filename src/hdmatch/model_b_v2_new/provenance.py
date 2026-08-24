"""Exact external-source provenance for the prospective Model B V2 amendment.

The repository stores hashes and source-specific retrieval metadata, never the
copyrighted response bodies.  The V2 compiler uses this module to prove that a
provenance amendment did not alter any frozen scoring semantics.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, date, datetime
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from .artifacts import (
    ArtifactBinding,
    FrozenModel,
    PreregistrationArtifact,
    PreregistrationArtifactV2,
    SourceCatalogEntry,
    canonical_bytes,
    reject_forbidden_provenance,
    validate_prospective_relative_path,
)

_SHA256_PATTERN = r"^[a-f0-9]{64}$"


class SnapshotStatus(StrEnum):
    CAPTURED_HASH_ONLY = "captured-hash-only-no-repository-snapshot"
    LICENSE_BLOCKED = "license-blocked-no-snapshot-or-content-hash"


class RetrievalMethod(FrozenModel):
    method_id: Literal["curl-http-get-compressed-v1"] = "curl-http-get-compressed-v1"
    tool: Literal["curl"] = "curl"
    tool_version: str = Field(min_length=1)
    request_profile: Literal[
        "HTTP GET with --compressed; response headers and decoded entity body captured ephemerally"
    ]
    raw_response_representation: Literal[
        "exact decoded HTTP entity-body bytes written by curl after content decoding"
    ]
    repository_body_storage: Literal["forbidden"] = "forbidden"


class RetrievalTerms(FrozenModel):
    terms_url: str = Field(min_length=1)
    checked_on: date
    capture_basis: str = Field(min_length=1)
    redistribution_allowed: Literal[False] = False
    repository_snapshot_allowed: Literal[False] = False
    constraints: str = Field(min_length=1)

    @field_validator("terms_url")
    @classmethod
    def validate_terms_url(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("terms URL must use HTTPS")
        reject_forbidden_provenance(value)
        return value


class ExternalSourceRetrieval(FrozenModel):
    retrieval_id: str = Field(pattern=r"^RETRIEVAL-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
    retrieval_method_id: Literal["curl-http-get-compressed-v1"] = "curl-http-get-compressed-v1"
    source_id: str = Field(pattern=r"^SRC-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
    exact_url: str = Field(min_length=1)
    locator: str = Field(min_length=1)
    proposition_ids: tuple[str, ...] = Field(min_length=1)
    accessed_at_utc: datetime
    http_status: int = Field(ge=100, le=599)
    response_mime_type: str = Field(min_length=1)
    response_content_encoding: str | None
    raw_response_byte_length: int | None = Field(default=None, gt=0)
    raw_response_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    etag: str | None
    snapshot_status: SnapshotStatus
    repository_snapshot_path: None = None
    terms: RetrievalTerms

    @field_validator("exact_url")
    @classmethod
    def validate_exact_url(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("external source URL must use HTTPS")
        reject_forbidden_provenance(value)
        return value

    @field_validator("accessed_at_utc")
    @classmethod
    def require_access_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("source access timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_snapshot_disposition(self) -> ExternalSourceRetrieval:
        if len(self.proposition_ids) != len(set(self.proposition_ids)):
            raise ValueError("retrieval proposition IDs must be unique")
        if self.http_status != 200:
            raise ValueError("a frozen source retrieval must have returned HTTP 200")
        if self.snapshot_status is SnapshotStatus.CAPTURED_HASH_ONLY:
            if self.raw_response_byte_length is None or self.raw_response_sha256 is None:
                raise ValueError("captured-hash-only records require exact body bytes and SHA-256")
        elif any(
            value is not None
            for value in (self.raw_response_byte_length, self.raw_response_sha256, self.etag)
        ):
            raise ValueError(
                "license-blocked records must omit body bytes, content hashes, and entity tags"
            )
        if self.repository_snapshot_path is not None:
            raise ValueError("external response bodies must never be stored in this repository")
        return self


class RetrievalManifest(FrozenModel):
    schema_version: Literal["model-b-v2-new-source-retrieval-manifest-v1"] = (
        "model-b-v2-new-source-retrieval-manifest-v1"
    )
    manifest_id: Literal["MODEL-B-DETAILED-V2-NEW-SOURCE-RETRIEVAL-V1"] = (
        "MODEL-B-DETAILED-V2-NEW-SOURCE-RETRIEVAL-V1"
    )
    model_id: Literal["MODEL-B-DETAILED-V2-NEW"] = "MODEL-B-DETAILED-V2-NEW"
    created_at_utc: datetime
    source_catalog_v1: ArtifactBinding
    retrieval_methods: tuple[RetrievalMethod, ...] = Field(min_length=1)
    sources: tuple[ExternalSourceRetrieval, ...] = Field(min_length=1)

    @field_validator("created_at_utc")
    @classmethod
    def require_created_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("retrieval-manifest timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_inventory(self) -> RetrievalManifest:
        if self.source_catalog_v1.role != "previous_source_catalog":
            raise ValueError("retrieval manifest must bind the V1 source catalog")
        method_ids = tuple(item.method_id for item in self.retrieval_methods)
        if len(method_ids) != len(set(method_ids)):
            raise ValueError("retrieval method IDs must be unique")
        retrieval_ids = tuple(item.retrieval_id for item in self.sources)
        if len(retrieval_ids) != len(set(retrieval_ids)):
            raise ValueError("retrieval IDs must be unique")
        urls = tuple(item.exact_url for item in self.sources)
        if len(urls) != len(set(urls)):
            raise ValueError("every exact external URL must have one retrieval record")
        unknown_methods = {item.retrieval_method_id for item in self.sources} - set(method_ids)
        if unknown_methods:
            raise ValueError(f"unknown retrieval methods: {sorted(unknown_methods)}")
        return self

    def canonical_bytes(self) -> bytes:
        return canonical_bytes(self)

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


class ExcludedInput(FrozenModel):
    path: str | None = None
    path_pattern: str | None = None
    reason: str = Field(min_length=1)

    @model_validator(mode="after")
    def exactly_one_locator(self) -> ExcludedInput:
        if (self.path is None) == (self.path_pattern is None):
            raise ValueError("excluded input requires exactly one path or path_pattern")
        return self


class LocalSourceRecord(FrozenModel):
    path: str = Field(min_length=1)
    role: str = Field(min_length=1)
    sha256: str = Field(pattern=_SHA256_PATTERN)

    @field_validator("path")
    @classmethod
    def validate_path(cls, value: str) -> str:
        return validate_prospective_relative_path(value)


class ProspectiveProvenanceClaim(FrozenModel):
    candidate_outcome_blind: Literal[True] = True
    claim: Literal["prospective-new-not-historical-reconstruction"] = (
        "prospective-new-not-historical-reconstruction"
    )
    historical_reproduction_claimed: Literal[False] = False
    legacy_results_used: Literal[False] = False
    method: str = Field(min_length=1)


class FrozenParaphrasedProposition(FrozenModel):
    proposition_id: str = Field(pattern=r"^P-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
    text: str = Field(min_length=1)


class ExternalSourceDefinition(FrozenModel):
    author: str = Field(min_length=1)
    frozen_paraphrased_propositions: tuple[FrozenParaphrasedProposition, ...] = Field(min_length=1)
    publisher: str = Field(min_length=1)
    source_id: str = Field(pattern=r"^SRC-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
    tier: str = Field(min_length=1)
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)

    @model_validator(mode="after")
    def unique_propositions_and_valid_urls(self) -> ExternalSourceDefinition:
        proposition_ids = tuple(
            item.proposition_id for item in self.frozen_paraphrased_propositions
        )
        if len(proposition_ids) != len(set(proposition_ids)):
            raise ValueError(f"duplicate proposition IDs in {self.source_id}")
        for url in self.url.split(" | "):
            if not url.startswith("https://"):
                raise ValueError("source URL must use HTTPS")
            reject_forbidden_provenance(url)
        return self


class ProvenanceAmendment(FrozenModel):
    amendment_scope: Literal[
        "external-source-retrieval-metadata-only; no behavioral or scoring changes"
    ]
    mapping_semantics_changed: Literal[False] = False
    previous_source_catalog: ArtifactBinding
    retrieval_manifest: ArtifactBinding


class SourceCatalogArtifactV2(FrozenModel):
    schema_version: Literal["model-b-detailed-v2-new-sources-v2"] = (
        "model-b-detailed-v2-new-sources-v2"
    )
    artifact_id: Literal["MODEL-B-DETAILED-V2-NEW-SOURCES-V2"] = (
        "MODEL-B-DETAILED-V2-NEW-SOURCES-V2"
    )
    model_id: Literal["MODEL-B-DETAILED-V2-NEW"] = "MODEL-B-DETAILED-V2-NEW"
    access_date: date
    excluded_inputs: tuple[ExcludedInput, ...] = Field(min_length=1)
    local_sources: tuple[LocalSourceRecord, ...] = Field(min_length=1)
    provenance: ProspectiveProvenanceClaim
    provenance_amendment: ProvenanceAmendment
    source_catalog: tuple[ExternalSourceDefinition, ...] = Field(min_length=1)
    source_hierarchy: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_inventory(self) -> SourceCatalogArtifactV2:
        source_ids = tuple(item.source_id for item in self.source_catalog)
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("source catalog IDs must be unique")
        if self.provenance_amendment.previous_source_catalog.role != ("previous_source_catalog"):
            raise ValueError("source amendment must bind the prior source catalog")
        if self.provenance_amendment.retrieval_manifest.role != ("source_retrieval_manifest"):
            raise ValueError("source amendment must bind the retrieval manifest")
        return self

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.model_dump(mode="json", exclude_none=True),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


def load_retrieval_manifest(path: str | Path) -> RetrievalManifest:
    return RetrievalManifest.model_validate_json(Path(path).read_text(encoding="utf-8"))


def load_source_catalog_v2(path: str | Path) -> SourceCatalogArtifactV2:
    return SourceCatalogArtifactV2.model_validate_json(Path(path).read_text(encoding="utf-8"))


def assert_source_catalog_provenance_only_equivalent(
    previous_source_path: str | Path,
    amended: SourceCatalogArtifactV2,
) -> None:
    """Require V2 to equal V1 after removing only amendment metadata."""

    previous = json.loads(Path(previous_source_path).read_text(encoding="utf-8"))
    if not isinstance(previous, dict):
        raise ValueError("V1 source catalog must be a JSON object")
    normalized = amended.model_dump(mode="json", exclude_none=True)
    normalized.pop("provenance_amendment")
    normalized["schema_version"] = "model-b-detailed-v2-new-sources-v1"
    normalized["artifact_id"] = "MODEL-B-DETAILED-V2-NEW-SOURCES-V1"
    if normalized != previous:
        differing = sorted(
            key
            for key in set(normalized) | set(previous)
            if normalized.get(key) != previous.get(key)
        )
        raise ValueError(
            "V2 source catalog changes non-provenance content: " + ", ".join(differing)
        )


def assert_preregistration_provenance_only_equivalent(
    previous: PreregistrationArtifact,
    amended: PreregistrationArtifactV2,
) -> None:
    """Fail if the V2 amendment changes any scientific or mapping semantics."""

    fields = (
        "model_id",
        "model_version",
        "base_model_id",
        "preregistered_at_utc",
        "behavioral_target",
        "question_bank",
        "model_a_base",
        "local_methods",
        "question_token_sets",
        "constants",
        "discovery_holdout_policy",
        "observations",
    )
    differing = [
        field
        for field in fields
        if _json_value(getattr(previous, field)) != _json_value(getattr(amended, field))
    ]
    if _source_reference_semantics(previous.source_catalog) != _source_reference_semantics(
        amended.source_catalog
    ):
        differing.append("source_catalog_semantics")
    if differing:
        raise ValueError(
            "V2 provenance amendment changes frozen preregistration semantics: "
            + ", ".join(differing)
        )


def validate_retrieval_manifest_against_source_catalog(
    manifest: RetrievalManifest,
    source_catalog_path: str | Path,
) -> None:
    """Bind each retrieved URL and proposition locator to the frozen V1 catalog."""

    raw = json.loads(Path(source_catalog_path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("source_catalog"), list):
        raise ValueError("source catalog has no external-source inventory")
    expected: dict[str, tuple[str, tuple[str, ...], str]] = {}
    for source in raw["source_catalog"]:
        if not isinstance(source, dict):
            raise ValueError("source catalog entries must be objects")
        source_id = source.get("source_id")
        raw_urls = source.get("url")
        propositions = source.get("frozen_paraphrased_propositions")
        if (
            not isinstance(source_id, str)
            or not isinstance(raw_urls, str)
            or not isinstance(propositions, list)
        ):
            raise ValueError("source catalog entry is malformed")
        proposition_ids = tuple(
            item["proposition_id"]
            for item in propositions
            if isinstance(item, dict) and isinstance(item.get("proposition_id"), str)
        )
        if len(proposition_ids) != len(propositions):
            raise ValueError(f"source proposition inventory is malformed: {source_id}")
        urls = tuple(raw_urls.split(" | "))
        for index, url in enumerate(urls, start=1):
            locator = source_id if len(urls) == 1 else f"{source_id}:url-{index}-of-{len(urls)}"
            expected[url] = (source_id, proposition_ids, locator)
    actual = {item.exact_url: item for item in manifest.sources}
    if set(actual) != set(expected):
        raise ValueError("retrieval manifest URL inventory differs from the V1 source catalog")
    for url, (source_id, proposition_ids, locator) in expected.items():
        record = actual[url]
        if (
            record.source_id != source_id
            or record.proposition_ids != proposition_ids
            or record.locator != locator
        ):
            raise ValueError(f"retrieval provenance differs from source catalog: {url}")


def _source_reference_semantics(
    entries: tuple[SourceCatalogEntry, ...],
) -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "source_id": item.source_id,
            "kind": item.kind.value,
            "title": item.title,
            "public_url": item.public_url,
            "locator": item.locator,
            "provenance_rationale": item.provenance_rationale,
        }
        for item in entries
    )


def _json_value(value: object) -> object:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json", exclude_none=False)
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, datetime):
        return value.isoformat().replace("+00:00", "Z")
    return value
