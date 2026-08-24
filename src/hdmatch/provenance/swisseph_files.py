"""Fail-closed provenance for the canonical local Swiss Ephemeris files.

The committed source manifest is the trust root for locally provisioned binary
inputs.  A successful verification record contains no machine-specific paths, so
it can be bound directly into run and cache manifests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hdmatch.util import sha256_file, sha256_json

SHA256_PATTERN = r"^[a-f0-9]{64}$"
PINNED_UPSTREAM_REPOSITORY = "https://github.com/aloistr/swisseph"
PINNED_UPSTREAM_COMMIT = "3fd0f956d73898b91cc4f67cf18b21af656d1342"
REQUIRED_EPHEMERIS_FILES = ("sepl_18.se1", "semo_18.se1")


class EphemerisManifestError(ValueError):
    """The committed source manifest is malformed or no longer pinned."""


class EphemerisFileVerificationError(ValueError):
    """Local ephemeris bytes do not match the committed source manifest."""


class EphemerisFilePin(BaseModel):
    """Expected identity of one upstream file."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    name: str = Field(min_length=1)
    bytes: int = Field(gt=0)
    sha256: str = Field(pattern=SHA256_PATTERN)


class EphemerisSourceManifest(BaseModel):
    """Repository-controlled trust root for the production ephemeris files."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    schema_version: Literal["ephemeris-file-manifest-v1"]
    provider: Literal["Swiss Ephemeris"]
    upstream_repository: str
    upstream_commit: str
    files: tuple[EphemerisFilePin, ...]
    tested_range: str = Field(min_length=1)
    license: str = Field(min_length=1)

    @model_validator(mode="after")
    def require_frozen_upstream_and_file_set(self) -> EphemerisSourceManifest:
        if self.upstream_repository != PINNED_UPSTREAM_REPOSITORY:
            raise ValueError("Swiss Ephemeris upstream repository is not the frozen source")
        if self.upstream_commit != PINNED_UPSTREAM_COMMIT:
            raise ValueError("Swiss Ephemeris upstream commit is not the frozen immutable commit")
        names = tuple(record.name for record in self.files)
        if len(set(names)) != len(names):
            raise ValueError("Swiss Ephemeris source manifest contains duplicate file names")
        if set(names) != set(REQUIRED_EPHEMERIS_FILES):
            raise ValueError(
                "Swiss Ephemeris source manifest must declare exactly "
                f"{', '.join(REQUIRED_EPHEMERIS_FILES)}"
            )
        return self

    def pin_for(self, name: str) -> EphemerisFilePin:
        for record in self.files:
            if record.name == name:
                return record
        raise KeyError(name)


class VerifiedEphemerisFile(BaseModel):
    """Observed local identity after byte-for-byte verification."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    name: str = Field(min_length=1)
    bytes: int = Field(gt=0)
    sha256: str = Field(pattern=SHA256_PATTERN)


class VerifiedEphemerisProvenance(BaseModel):
    """Portable binding for verified local files and their immutable source."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    schema_version: Literal["ephemeris-provisioning-receipt-v1"] = (
        "ephemeris-provisioning-receipt-v1"
    )
    source_repository: str
    source_commit: str
    source_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    files: tuple[VerifiedEphemerisFile, ...]
    ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    verification_status: Literal["pass"] = "pass"

    @model_validator(mode="after")
    def require_consistent_binding(self) -> VerifiedEphemerisProvenance:
        if self.source_repository != PINNED_UPSTREAM_REPOSITORY:
            raise ValueError("verified ephemeris receipt has an unexpected source repository")
        if self.source_commit != PINNED_UPSTREAM_COMMIT:
            raise ValueError("verified ephemeris receipt has an unexpected source commit")
        names = tuple(record.name for record in self.files)
        if names != REQUIRED_EPHEMERIS_FILES:
            raise ValueError("verified ephemeris receipt has an unexpected or reordered file set")
        expected_file_set_hash = sha256_json(
            [record.model_dump(mode="json") for record in self.files]
        )
        if self.ephemeris_file_set_sha256 != expected_file_set_hash:
            raise ValueError("verified ephemeris file-set hash is inconsistent")
        return self

    def manifest_binding(self) -> dict[str, object]:
        """Return the path-free fields required in a run/cache manifest."""

        return self.model_dump(mode="json")


def load_ephemeris_source_manifest(path: str | Path) -> EphemerisSourceManifest:
    """Load and strictly validate the repository-controlled source manifest."""

    manifest_path = Path(path)
    try:
        payload = manifest_path.read_bytes()
        json.loads(payload)
        return EphemerisSourceManifest.model_validate_json(payload, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise EphemerisManifestError(
            f"invalid pinned Swiss Ephemeris source manifest: {manifest_path}"
        ) from exc


def verify_ephemeris_directory(
    *,
    source_manifest_path: str | Path,
    ephemeris_directory: str | Path,
    reject_unlisted_se1: bool = True,
) -> VerifiedEphemerisProvenance:
    """Verify every canonical file and return a portable immutable binding.

    No receipt is accepted as proof of local content.  This function always
    re-hashes the actual ``.se1`` bytes before returning ``verification_status=pass``.
    """

    source_path = Path(source_manifest_path)
    manifest = load_ephemeris_source_manifest(source_path)
    directory = Path(ephemeris_directory)
    if not directory.is_dir():
        raise EphemerisFileVerificationError(
            f"Swiss Ephemeris directory is missing: {directory}"
        )

    if reject_unlisted_se1:
        observed_names = {path.name for path in directory.glob("*.se1") if path.is_file()}
        unexpected_names = sorted(observed_names - set(REQUIRED_EPHEMERIS_FILES))
        if unexpected_names:
            raise EphemerisFileVerificationError(
                "unlisted Swiss Ephemeris files are present: " + ", ".join(unexpected_names)
            )

    verified_files: list[VerifiedEphemerisFile] = []
    for name in REQUIRED_EPHEMERIS_FILES:
        expected = manifest.pin_for(name)
        local_path = directory / name
        if not local_path.is_file():
            raise EphemerisFileVerificationError(f"required ephemeris file is missing: {name}")
        observed_bytes = local_path.stat().st_size
        if observed_bytes != expected.bytes:
            raise EphemerisFileVerificationError(
                f"ephemeris byte-size mismatch for {name}: "
                f"expected {expected.bytes}, observed {observed_bytes}"
            )
        observed_sha256 = sha256_file(local_path)
        if observed_sha256 != expected.sha256:
            raise EphemerisFileVerificationError(
                f"ephemeris SHA-256 mismatch for {name}: "
                f"expected {expected.sha256}, observed {observed_sha256}"
            )
        verified_files.append(
            VerifiedEphemerisFile(
                name=name,
                bytes=observed_bytes,
                sha256=observed_sha256,
            )
        )

    file_set_sha256 = sha256_json(
        [record.model_dump(mode="json") for record in verified_files]
    )
    return VerifiedEphemerisProvenance(
        source_repository=manifest.upstream_repository,
        source_commit=manifest.upstream_commit,
        source_manifest_sha256=sha256_file(source_path),
        files=tuple(verified_files),
        ephemeris_file_set_sha256=file_set_sha256,
    )
