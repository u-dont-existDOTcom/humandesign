"""Verified reusable structural-state cache for century-wide participant recovery."""

from __future__ import annotations

import gzip
import json
from collections import defaultdict
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_file,
    sha256_json,
    write_new_bytes,
    write_new_canonical_json,
)
from hdmatch.schemas import CandidateState, StructuralChartFeatures
from hdmatch.search import split_interval_by_local_date


BOUNDARY_POLICY_VERSION: Final[
    Literal["activation-gates-plus-sun-lines-forward-design-v2"]
] = "activation-gates-plus-sun-lines-forward-design-v2"
CENTURY_CACHE_SCHEMA_VERSION: Final[Literal["century-candidate-cache-v2"]] = (
    "century-candidate-cache-v2"
)
FEATURE_VECTOR_SCHEMA_VERSION: Final[Literal["structural-chart-features-v1"]] = (
    "structural-chart-features-v1"
)


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class GlobalCandidateState(_FrozenModel):
    """Timezone-neutral structural chart interval stored in the global cache.

    ``chart_features_hash`` hashes the compact structural feature record.  It is
    intentionally not the full all-lines chart-engine stable hash: non-Sun line
    changes are outside this century-universe resolution and must not split a
    candidate interval.
    """

    state_id: str
    start_utc: datetime
    end_utc: datetime
    chart_features_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    chart_features: StructuralChartFeatures
    boundary_events: tuple[str, ...] = ()

    @field_validator("start_utc", "end_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("century-cache timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def positive_interval_and_hash(self) -> GlobalCandidateState:
        if self.end_utc <= self.start_utc:
            raise ValueError("global candidate interval must have positive duration")
        if self.chart_features_hash != structural_features_sha256(self.chart_features):
            raise ValueError("global candidate structural feature hash mismatch")
        return self


class CenturyCacheShard(_FrozenModel):
    filename: str
    first_state_utc: datetime
    last_state_end_utc: datetime
    state_count: int = Field(ge=1)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    uncompressed_bytes: int = Field(ge=1)

    @field_validator("first_state_utc", "last_state_end_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("shard timestamps must be timezone-aware")
        return value.astimezone(UTC)


class CenturyCacheManifest(_FrozenModel):
    schema_version: Literal["century-candidate-cache-v2"] = CENTURY_CACHE_SCHEMA_VERSION
    cache_version: str
    feature_vector_schema_version: Literal["structural-chart-features-v1"] = (
        FEATURE_VECTOR_SCHEMA_VERSION
    )
    utc_start: datetime
    utc_end_exclusive: datetime
    interval_count: int = Field(ge=1)
    canonical_rows_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    engine_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    boundary_policy_version: Literal[
        "activation-gates-plus-sun-lines-forward-design-v2"
    ] = BOUNDARY_POLICY_VERSION
    design_root_tolerance_seconds: float = Field(gt=0.0)
    generation_commit: str
    created_at_utc: datetime
    verification_status: Literal["verified"] = "verified"
    shard_format: Literal["canonical-jsonl-gzip-v1"] = "canonical-jsonl-gzip-v1"
    shards: tuple[CenturyCacheShard, ...]

    @field_validator("utc_start", "utc_end_exclusive", "created_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("manifest timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def valid_range(self) -> CenturyCacheManifest:
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("century cache range must have positive duration")
        if not self.shards:
            raise ValueError("century cache must contain at least one shard")
        if sum(item.state_count for item in self.shards) != self.interval_count:
            raise ValueError("manifest shard counts do not equal interval_count")
        return self


class CenturyCacheVerificationError(RuntimeError):
    """Raised when a global cache cannot be trusted for participant ranking."""


def structural_features_sha256(features: StructuralChartFeatures) -> str:
    """Hash the exact discrete structural vector used by the century universe."""

    return sha256_json(features)


def write_verified_century_cache(
    output_dir: str | Path,
    states: tuple[GlobalCandidateState, ...],
    *,
    engine_fingerprint: str,
    generation_commit: str,
    created_at_utc: datetime,
    cache_version: str = "century-structural-exact-v2",
    design_root_tolerance_seconds: float = 0.01,
    shard_years: int = 10,
) -> CenturyCacheManifest:
    """Write an immutable deterministic structural cache and verify it immediately."""

    if shard_years <= 0:
        raise ValueError("shard_years must be positive")
    _audit_partition(states)
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise FileExistsError(f"century cache output directory is not empty: {root}")

    start_year = states[0].start_utc.year
    groups: dict[int, list[GlobalCandidateState]] = defaultdict(list)
    for state in states:
        bucket = max(0, (state.start_utc.year - start_year) // shard_years)
        groups[bucket].append(state)

    universe_digest = sha256()
    shards: list[CenturyCacheShard] = []
    for bucket in sorted(groups):
        rows = tuple(groups[bucket])
        first_year = start_year + bucket * shard_years
        last_year = first_year + shard_years - 1
        filename = f"states-{first_year:04d}-{last_year:04d}.jsonl.gz"
        raw = b"".join(_row_bytes(state) for state in rows)
        universe_digest.update(raw)
        compressed = gzip.compress(raw, compresslevel=9, mtime=0)
        destination = write_new_bytes(root / filename, compressed)
        shards.append(
            CenturyCacheShard(
                filename=filename,
                first_state_utc=rows[0].start_utc,
                last_state_end_utc=rows[-1].end_utc,
                state_count=len(rows),
                sha256=sha256_file(destination),
                uncompressed_bytes=len(raw),
            )
        )

    manifest = CenturyCacheManifest(
        cache_version=cache_version,
        utc_start=states[0].start_utc,
        utc_end_exclusive=states[-1].end_utc,
        interval_count=len(states),
        canonical_rows_sha256=universe_digest.hexdigest(),
        engine_fingerprint=engine_fingerprint,
        design_root_tolerance_seconds=design_root_tolerance_seconds,
        generation_commit=generation_commit,
        created_at_utc=_require_utc(created_at_utc),
        shards=tuple(shards),
    )
    write_new_canonical_json(root / "manifest.json", manifest)
    verify_century_cache(root, expected_engine_fingerprint=engine_fingerprint)
    return manifest


def verify_century_cache(
    cache_dir: str | Path,
    *,
    expected_engine_fingerprint: str | None = None,
) -> CenturyCacheManifest:
    """Verify manifest, exact bytes, canonical rows, hashes, and interval partition."""

    root = Path(cache_dir)
    try:
        value = load_json_bytes(root / "manifest.json", require_canonical=True)
        manifest = CenturyCacheManifest.model_validate(value)
    except (OSError, ValueError) as exc:
        raise CenturyCacheVerificationError("invalid century-cache manifest") from exc
    if (
        expected_engine_fingerprint is not None
        and manifest.engine_fingerprint != expected_engine_fingerprint
    ):
        raise CenturyCacheVerificationError(
            "century-cache engine fingerprint does not match the deployed chart engine"
        )

    states = _load_verified_global_states(root, manifest)
    _audit_partition(states)
    if states[0].start_utc != manifest.utc_start:
        raise CenturyCacheVerificationError("century cache starts outside its manifest range")
    if states[-1].end_utc != manifest.utc_end_exclusive:
        raise CenturyCacheVerificationError("century cache ends outside its manifest range")
    return manifest


def load_century_candidate_states(
    cache_dir: str | Path,
    *,
    timezone_name: str,
    expected_engine_fingerprint: str,
) -> tuple[CandidateState, ...]:
    """Load a verified global cache and attach participant-local date overlaps."""

    root = Path(cache_dir)
    manifest = verify_century_cache(
        root,
        expected_engine_fingerprint=expected_engine_fingerprint,
    )
    states = _load_verified_global_states(root, manifest)
    return tuple(
        CandidateState(
            state_id=state.state_id,
            start_utc=state.start_utc,
            end_utc=state.end_utc,
            chart_features_hash=state.chart_features_hash,
            chart_features=state.chart_features,
            local_date_overlaps=split_interval_by_local_date(
                state.start_utc,
                state.end_utc,
                timezone_name,
            ),
            boundary_events=state.boundary_events,
        )
        for state in states
    )


def _load_verified_global_states(
    root: Path,
    manifest: CenturyCacheManifest,
) -> tuple[GlobalCandidateState, ...]:
    digest = sha256()
    states: list[GlobalCandidateState] = []
    for shard in manifest.shards:
        path = root / shard.filename
        try:
            if sha256_file(path) != shard.sha256:
                raise CenturyCacheVerificationError(
                    f"century-cache shard hash mismatch: {shard.filename}"
                )
            raw = gzip.decompress(path.read_bytes())
        except (OSError, gzip.BadGzipFile) as exc:
            raise CenturyCacheVerificationError(
                f"cannot read century-cache shard: {shard.filename}"
            ) from exc
        if len(raw) != shard.uncompressed_bytes:
            raise CenturyCacheVerificationError(
                f"century-cache shard byte count mismatch: {shard.filename}"
            )
        digest.update(raw)
        parsed = _parse_canonical_rows(raw, shard.filename)
        if len(parsed) != shard.state_count:
            raise CenturyCacheVerificationError(
                f"century-cache shard state count mismatch: {shard.filename}"
            )
        if parsed[0].start_utc != shard.first_state_utc:
            raise CenturyCacheVerificationError(
                f"century-cache shard start mismatch: {shard.filename}"
            )
        if parsed[-1].end_utc != shard.last_state_end_utc:
            raise CenturyCacheVerificationError(
                f"century-cache shard end mismatch: {shard.filename}"
            )
        states.extend(parsed)
    if len(states) != manifest.interval_count:
        raise CenturyCacheVerificationError("century-cache interval count mismatch")
    if digest.hexdigest() != manifest.canonical_rows_sha256:
        raise CenturyCacheVerificationError("century-cache logical universe hash mismatch")
    return tuple(states)


def _parse_canonical_rows(raw: bytes, filename: str) -> tuple[GlobalCandidateState, ...]:
    result: list[GlobalCandidateState] = []
    for line_number, line in enumerate(raw.splitlines(), start=1):
        if not line:
            continue
        try:
            value = json.loads(line)
            if canonical_json_bytes(value) != line:
                raise ValueError("row is not canonical JSON")
            result.append(GlobalCandidateState.model_validate(value))
        except (ValueError, TypeError) as exc:
            raise CenturyCacheVerificationError(
                f"invalid century-cache row {filename}:{line_number}"
            ) from exc
    if not result:
        raise CenturyCacheVerificationError(f"empty century-cache shard: {filename}")
    return tuple(result)


def _row_bytes(state: GlobalCandidateState) -> bytes:
    return canonical_json_bytes(state) + b"\n"


def _audit_partition(states: tuple[GlobalCandidateState, ...]) -> None:
    if not states:
        raise CenturyCacheVerificationError("century cache contains no intervals")
    for state in states:
        if state.chart_features_hash != structural_features_sha256(state.chart_features):
            raise CenturyCacheVerificationError("century cache contains a structural hash mismatch")
    for previous, current in zip(states, states[1:], strict=False):
        if previous.end_utc != current.start_utc:
            raise CenturyCacheVerificationError("century cache has a gap or overlap")
        if previous.chart_features_hash == current.chart_features_hash:
            raise CenturyCacheVerificationError(
                "century cache contains identical adjacent stable intervals"
            )


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("created_at_utc must be timezone-aware")
    return value.astimezone(UTC)
