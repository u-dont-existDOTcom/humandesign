"""Hash-bound on-disk cache for exact candidate interval universes."""

from __future__ import annotations

import re
from collections.abc import Iterable
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hdmatch.experiments.canonical import load_json_bytes, sha256_file, write_new_canonical_json
from hdmatch.schemas import CandidateState
from hdmatch.search import local_month_utc_bounds

from .chart_adapter import ExactChartAdapter


@dataclass(frozen=True, slots=True, order=True)
class MonthRequest:
    year: int
    month: int
    timezone_name: str


@dataclass(frozen=True, slots=True)
class CachedUniverse:
    request: MonthRequest
    path: Path
    sha256: str
    states: tuple[CandidateState, ...]


def cache_path(
    cache_dir: str | Path, request: MonthRequest, engine_fingerprint: str
) -> Path:
    safe_zone = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.timezone_name)
    return Path(cache_dir) / (
        f"month-{request.year:04d}-{request.month:02d}-{safe_zone}-"
        f"{engine_fingerprint[:16]}.json"
    )


def _cache_payload(
    request: MonthRequest,
    engine_fingerprint: str,
    states: tuple[CandidateState, ...],
) -> dict[str, Any]:
    start, end = local_month_utc_bounds(
        request.year, request.month, request.timezone_name
    )
    return {
        "schema_version": "candidate-universe-cache-v1",
        "year": request.year,
        "month": request.month,
        "timezone": request.timezone_name,
        "start_utc": start,
        "end_utc": end,
        "engine_fingerprint": engine_fingerprint,
        "state_count": len(states),
        "states": [state.model_dump(mode="json") for state in states],
    }


def _build_one(
    ephemeris_path: str,
    cache_dir: str,
    request: MonthRequest,
) -> str:
    engine = ExactChartAdapter(ephemeris_path)
    destination = cache_path(cache_dir, request, engine.fingerprint)
    if destination.is_file():
        # Validation happens when the integration owner loads the result.
        return str(destination)
    start, end = local_month_utc_bounds(
        request.year, request.month, request.timezone_name
    )
    states = engine.candidate_states(start, end, request.timezone_name)
    write_new_canonical_json(
        destination,
        _cache_payload(request, engine.fingerprint, states),
    )
    return str(destination)


def ensure_month_caches(
    requests: Iterable[MonthRequest],
    *,
    ephemeris_path: str | Path,
    cache_dir: str | Path,
    workers: int = 1,
) -> tuple[Path, ...]:
    """Build missing exact universes, optionally in independent processes."""

    unique = tuple(sorted(set(requests)))
    if not unique:
        return ()
    if workers < 1:
        raise ValueError("workers must be at least 1")
    directory = Path(cache_dir)
    directory.mkdir(parents=True, exist_ok=True)
    ephemeris = str(Path(ephemeris_path).resolve())
    if workers == 1:
        paths = tuple(Path(_build_one(ephemeris, str(directory), item)) for item in unique)
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            paths = tuple(
                Path(path)
                for path in pool.map(
                    _build_one,
                    (ephemeris for _ in unique),
                    (str(directory) for _ in unique),
                    unique,
                )
            )
    return tuple(sorted(paths))


def load_cached_universe(
    path: str | Path,
    *,
    request: MonthRequest,
    engine_fingerprint: str,
) -> CachedUniverse:
    source = Path(path)
    raw = load_json_bytes(source, require_canonical=True)
    if not isinstance(raw, dict):
        raise ValueError("candidate-universe cache must be an object")
    expected = {
        "schema_version": "candidate-universe-cache-v1",
        "year": request.year,
        "month": request.month,
        "timezone": request.timezone_name,
        "engine_fingerprint": engine_fingerprint,
    }
    for field, value in expected.items():
        if raw.get(field) != value:
            raise ValueError(f"candidate-universe cache {field} mismatch")
    stored_states = raw.get("states")
    if not isinstance(stored_states, list):
        raise ValueError("candidate-universe cache states must be a list")
    states = tuple(CandidateState.model_validate(item) for item in stored_states)
    if raw.get("state_count") != len(states):
        raise ValueError("candidate-universe cache state count mismatch")
    start, end = local_month_utc_bounds(
        request.year, request.month, request.timezone_name
    )
    if not states or states[0].start_utc != start or states[-1].end_utc != end:
        raise ValueError("candidate-universe cache does not cover the requested month")
    for previous, current in zip(states, states[1:], strict=False):
        if previous.end_utc != current.start_utc:
            raise ValueError("candidate-universe cache has a gap or overlap")
    return CachedUniverse(
        request=request,
        path=source,
        sha256=sha256_file(source),
        states=states,
    )
