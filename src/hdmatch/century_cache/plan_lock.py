"""Independent reviewed trust root for an immutable century build plan."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)

from .models import GIT_COMMIT_PATTERN, SHA256_PATTERN, FrozenModel
from .staging import (
    CenturyBuildPlanV1,
    century_build_plan_sha256,
    load_century_build_plan,
)

DEFAULT_CENTURY_PLAN_TRUST_LOCK = Path(
    "data/century_cache/v1.plan-trust-lock.json"
)
CANONICAL_CENTURY_PLAN_TRUST_LOCK_SHA256 = (
    "45e647cf11210864f8f0fe3005db1f339dfb9822a5a06cd335a6e0a8b08926e8"
)


def _fsync_parent_directory(path: Path) -> None:
    descriptor = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


class CenturyBuildPlanTrustLockV1(FrozenModel):
    """Separately reviewed identity for one exact immutable build plan."""

    schema_version: Literal["century-build-plan-trust-lock-v1"] = (
        "century-build-plan-trust-lock-v1"
    )
    plan_locator: str = Field(min_length=1)
    plan_sha256: str = Field(pattern=SHA256_PATTERN)
    generation_commit: str = Field(pattern=GIT_COMMIT_PATTERN)
    utc_start: datetime
    utc_end_exclusive: datetime
    job_count: int = Field(gt=0)
    engine_identity_sha256: str = Field(pattern=SHA256_PATTERN)

    @field_validator("utc_start", "utc_end_exclusive")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("plan trust-lock timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_safe_locator_and_range(self) -> CenturyBuildPlanTrustLockV1:
        locator = Path(self.plan_locator)
        if locator.is_absolute() or ".." in locator.parts:
            raise ValueError("plan trust-lock locator must be repository-relative")
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("plan trust-lock range must be positive")
        return self


@dataclass(frozen=True, slots=True)
class VerifiedCenturyBuildPlanTrust:
    plan: CenturyBuildPlanV1
    trust_lock: CenturyBuildPlanTrustLockV1
    plan_path: Path
    trust_lock_path: Path
    plan_sha256: str
    trust_lock_sha256: str


def century_build_plan_trust_lock_from_plan(
    plan: CenturyBuildPlanV1,
    *,
    plan_locator: str,
) -> CenturyBuildPlanTrustLockV1:
    """Create reviewable trust-root bytes from a validated immutable plan."""

    checked = CenturyBuildPlanV1.model_validate(
        plan.model_dump(mode="python"),
        strict=True,
    )
    return CenturyBuildPlanTrustLockV1(
        plan_locator=plan_locator,
        plan_sha256=century_build_plan_sha256(checked),
        generation_commit=checked.source_commit,
        utc_start=checked.utc_start,
        utc_end_exclusive=checked.utc_end_exclusive,
        job_count=len(checked.jobs),
        engine_identity_sha256=sha256_json(
            checked.engine.model_dump(mode="json")
        ),
    )


def write_century_build_plan_trust_lock_new(
    path: str | Path,
    lock: CenturyBuildPlanTrustLockV1,
) -> Path:
    """Persist canonical plan-lock bytes without replacing a reviewed root."""

    destination = Path(path)
    write_new_canonical_json(destination, lock)
    _fsync_parent_directory(destination)
    return destination


def load_century_build_plan_trust_lock(
    path: str | Path,
) -> CenturyBuildPlanTrustLockV1:
    """Load exact canonical plan-lock bytes and reject links/substitutions."""

    source = Path(path)
    if source.is_symlink():
        raise ValueError("century build-plan trust lock must not be a symbolic link")
    try:
        raw = source.read_bytes()
        payload = json.loads(raw)
        if canonical_json_bytes(payload) != raw:
            raise ValueError("plan trust lock is not canonical JSON")
        return CenturyBuildPlanTrustLockV1.model_validate_json(raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError("invalid century build-plan trust lock") from exc


def verify_century_build_plan_against_trust_lock(
    plan_path: str | Path,
    *,
    trust_lock_path: str | Path,
    expected_trust_lock_sha256: str,
    repository_root: str | Path,
) -> VerifiedCenturyBuildPlanTrust:
    """Verify plan bytes against an independently supplied reviewed lock hash."""

    if len(expected_trust_lock_sha256) != 64 or any(
        character not in "0123456789abcdef"
        for character in expected_trust_lock_sha256
    ):
        raise ValueError("expected plan trust-lock SHA-256 is invalid")
    lock_path = Path(trust_lock_path)
    lock_sha256 = sha256_file(lock_path)
    if lock_sha256 != expected_trust_lock_sha256:
        raise ValueError(
            "century build-plan trust-lock bytes differ from the independent root"
        )
    lock = load_century_build_plan_trust_lock(lock_path)
    source = Path(plan_path)
    root = Path(repository_root).resolve(strict=True)
    expected_source = root / lock.plan_locator
    try:
        expected_resolved = expected_source.resolve(strict=True)
        expected_resolved.relative_to(root)
        source_resolved = source.resolve(strict=True)
    except (OSError, ValueError) as exc:
        raise ValueError(
            "century build-plan locator does not resolve inside the trusted repository"
        ) from exc
    if source_resolved != expected_resolved:
        raise ValueError(
            "century build-plan path differs from its independently locked locator"
        )
    plan = load_century_build_plan(source)
    plan_sha256 = sha256_file(source)
    if plan_sha256 != century_build_plan_sha256(plan):
        raise ValueError("century build-plan bytes differ from the validated plan")
    expected = {
        "plan SHA-256": (plan_sha256, lock.plan_sha256),
        "generation commit": (plan.source_commit, lock.generation_commit),
        "UTC start": (plan.utc_start, lock.utc_start),
        "UTC end": (plan.utc_end_exclusive, lock.utc_end_exclusive),
        "job count": (len(plan.jobs), lock.job_count),
        "engine identity": (
            sha256_json(plan.engine.model_dump(mode="json")),
            lock.engine_identity_sha256,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise ValueError(f"century build-plan {label} differs from its trust lock")
    return VerifiedCenturyBuildPlanTrust(
        plan=plan,
        trust_lock=lock,
        plan_path=source,
        trust_lock_path=lock_path,
        plan_sha256=plan_sha256,
        trust_lock_sha256=lock_sha256,
    )
