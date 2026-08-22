from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.century_cache import (
    CANONICAL_CENTURY_PLAN_TRUST_LOCK_SHA256,
    load_century_build_plan_trust_lock,
    write_century_build_plan_trust_lock_new,
)
from hdmatch.century_cache import plan_lock as plan_lock_module
from hdmatch.experiments.canonical import sha256_file

_ROOT = Path(__file__).resolve().parents[2]
_CANONICAL_LOCK = _ROOT / "data/century_cache/v1.plan-trust-lock.json"


def test_tracked_canonical_plan_trust_lock_has_reviewed_exact_identity() -> None:
    assert sha256_file(_CANONICAL_LOCK) == (
        CANONICAL_CENTURY_PLAN_TRUST_LOCK_SHA256
    )

    lock = load_century_build_plan_trust_lock(_CANONICAL_LOCK)

    assert lock.plan_locator == "data/century_cache/build-v1/plan.json"
    assert lock.plan_sha256 == (
        "8d0133ddce8b161019a8d126098386ca5b593abe7561036ebb8be766dac362f6"
    )
    assert lock.generation_commit == (
        "9eafe5344740cdf24c4796dbcbad8fb4514045ec"
    )
    assert lock.utc_start == datetime(1926, 8, 22, tzinfo=UTC)
    assert lock.utc_end_exclusive == datetime(2026, 8, 23, tzinfo=UTC)
    assert lock.job_count == 101
    assert lock.engine_identity_sha256 == (
        "5ac974da2e385bd09f3c15e457a70f58d05e288c5d36927102d7bd2efc5b3d8a"
    )


def test_plan_trust_lock_write_new_fsyncs_its_parent_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lock = load_century_build_plan_trust_lock(_CANONICAL_LOCK)
    destination = tmp_path / "plan-trust-lock.json"
    durable_paths: list[Path] = []
    monkeypatch.setattr(
        plan_lock_module,
        "_fsync_parent_directory",
        durable_paths.append,
    )

    assert write_century_build_plan_trust_lock_new(destination, lock) == destination
    assert durable_paths == [destination]
    with pytest.raises(FileExistsError, match="immutable artifact already exists"):
        write_century_build_plan_trust_lock_new(destination, lock)
