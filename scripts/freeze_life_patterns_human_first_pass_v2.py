#!/usr/bin/env python3
"""Validate and freeze a Life Patterns v2 independent human first pass."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.evaluation.development_human_first_pass_freeze_v2 import (
    write_human_first_pass_freeze_v2,
)


def _parse_time(value: str | None) -> datetime:
    if value is None:
        return datetime.now(UTC)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("--frozen-at-utc must include a timezone")
    return parsed.astimezone(UTC)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-zip", type=Path, required=True)
    parser.add_argument("--episode-responses", type=Path, required=True)
    parser.add_argument("--series-responses", type=Path, required=True)
    parser.add_argument("--attestation", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--frozen-at-utc")
    args = parser.parse_args()

    receipt = write_human_first_pass_freeze_v2(
        output_dir=args.output_dir,
        handoff_zip=args.handoff_zip,
        raw_episode_output=args.episode_responses.read_bytes(),
        raw_series_output=args.series_responses.read_bytes(),
        raw_attestation=args.attestation.read_bytes(),
        frozen_at_utc=_parse_time(args.frozen_at_utc),
    )
    print(json.dumps(receipt.model_dump(mode="json"), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
