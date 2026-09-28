"""Deterministic numerical-runtime gate for frozen empirical analyses."""

from __future__ import annotations

import os
import platform
import sys
from typing import Any

import numpy as np
import scipy  # type: ignore[import-untyped]
from threadpoolctl import threadpool_info  # type: ignore[import-untyped]

SINGLE_THREAD_ENVIRONMENT = (
    "OPENBLAS_NUM_THREADS",
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
)


class RuntimeEnvironmentError(RuntimeError):
    """Raised when a confirmatory numerical process is not deterministic."""


def require_deterministic_numerical_runtime() -> dict[str, Any]:
    """Require float64 plus an actually single-threaded BLAS runtime and report it."""

    thread_environment = {name: os.environ.get(name) for name in SINGLE_THREAD_ENVIRONMENT}
    invalid = sorted(name for name, value in thread_environment.items() if value != "1")
    if invalid:
        raise RuntimeEnvironmentError(
            "single-thread environment variables must equal 1 before process start: "
            + ", ".join(invalid)
        )
    if np.dtype(np.float64).itemsize != 8:
        raise RuntimeEnvironmentError("NumPy float64 is not an eight-byte IEEE-754 type")
    pools = threadpool_info()
    blas_pools = [pool for pool in pools if pool.get("user_api") == "blas"]
    if not blas_pools:
        raise RuntimeEnvironmentError("no loaded BLAS runtime could be audited")
    if any(pool.get("num_threads") != 1 for pool in blas_pools):
        raise RuntimeEnvironmentError("a loaded BLAS runtime is not single-threaded")
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable_basename": os.path.basename(sys.executable),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "float_dtype": "float64",
        "float_itemsize": np.dtype(np.float64).itemsize,
        "thread_environment": thread_environment,
        "blas": [
            {
                "internal_api": pool.get("internal_api"),
                "version": pool.get("version"),
                "num_threads": pool.get("num_threads"),
                "threading_layer": pool.get("threading_layer"),
                "architecture": pool.get("architecture"),
            }
            for pool in blas_pools
        ],
        "random_generator": "NumPy Generator(PCG64(seed))",
        "identifier_order": "unsigned UTF-8 byte order",
    }
