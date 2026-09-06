#!/usr/bin/env python3
"""Prepare v8/v8.1 Life Patterns development artifacts without calling any model."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from hdmatch.evaluation.development_private_preparation import (
    DEFAULT_EPISODE_CALIBRATION_UNITS,
    DEFAULT_EPISODE_PER_OBSERVABLE_FLOOR,
    DEFAULT_SERIES_CALIBRATION_UNITS,
    DEFAULT_SERIES_PER_OBSERVABLE_FLOOR,
    prepare_v8_private_development_package,
    private_preparation_safe_summary,
    write_private_development_preparation,
)


def _load_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return cast(dict[str, Any], raw)


def _git_head(repo_root: Path) -> str:
    try:
        result = subprocess.run(  # noqa: S603
            ["git", "rev-parse", "HEAD"],  # noqa: S607
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError("could not resolve repository HEAD; pass --source-commit explicitly") from exc
    value = result.stdout.strip()
    if len(value) < 7:
        raise ValueError("resolved repository HEAD is invalid")
    return value


def _parse_time(value: str | None) -> datetime:
    if value is None:
        return datetime.now(UTC)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("--created-at-utc must include a timezone")
    return parsed.astimezone(UTC)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build private development-only Life Patterns corpus/tasks/calibration from the "
            "v8 transfer record and v8.1 repair supplement. No model is called."
        )
    )
    parser.add_argument("--v8-record", type=Path, required=True)
    parser.add_argument("--v8-1-supplement", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--source-commit")
    parser.add_argument("--created-at-utc")
    parser.add_argument(
        "--episode-calibration-units",
        type=int,
        default=DEFAULT_EPISODE_CALIBRATION_UNITS,
    )
    parser.add_argument(
        "--series-calibration-units",
        type=int,
        default=DEFAULT_SERIES_CALIBRATION_UNITS,
    )
    parser.add_argument(
        "--episode-per-observable-floor",
        type=int,
        default=DEFAULT_EPISODE_PER_OBSERVABLE_FLOOR,
    )
    parser.add_argument(
        "--series-per-observable-floor",
        type=int,
        default=DEFAULT_SERIES_PER_OBSERVABLE_FLOOR,
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    source_commit = args.source_commit or _git_head(repo_root)
    created_at = _parse_time(args.created_at_utc)
    preparation = prepare_v8_private_development_package(
        original=_load_object(args.v8_record),
        supplement=_load_object(args.v8_1_supplement),
        repo_root=repo_root,
        source_commit=source_commit,
        created_at_utc=created_at,
        episode_calibration_units=args.episode_calibration_units,
        series_calibration_units=args.series_calibration_units,
        episode_per_observable_floor=args.episode_per_observable_floor,
        series_per_observable_floor=args.series_per_observable_floor,
    )
    write_private_development_preparation(args.output_dir, preparation)
    print(json.dumps(private_preparation_safe_summary(preparation), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
