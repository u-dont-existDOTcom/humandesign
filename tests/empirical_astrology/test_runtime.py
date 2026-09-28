from __future__ import annotations

import pytest

from hdmatch.empirical_astrology import (
    RuntimeEnvironmentError,
    require_deterministic_numerical_runtime,
)


def test_runtime_records_single_thread_float64_environment() -> None:
    report = require_deterministic_numerical_runtime()
    assert report["float_dtype"] == "float64"
    assert report["float_itemsize"] == 8
    assert report["numpy_version"]
    assert report["scipy_version"]
    assert report["blas"]
    assert all(pool["num_threads"] == 1 for pool in report["blas"])


def test_runtime_rejects_missing_single_thread_declaration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENBLAS_NUM_THREADS", raising=False)
    with pytest.raises(RuntimeEnvironmentError, match="OPENBLAS_NUM_THREADS"):
        require_deterministic_numerical_runtime()
