"""Deterministic mount-boundary probe; not a scientific recovery or benchmark."""

from __future__ import annotations

import argparse
import hashlib
import os
from collections.abc import Sequence
from pathlib import Path

from hdmatch.experiments.canonical import write_new_canonical_json


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hdmatch-keyless-isolation-probe")
    parser.add_argument("--public-input", required=True, type=Path)
    parser.add_argument("--denied-host-path", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    public_bytes = args.public_input.read_bytes()
    try:
        args.denied_host_path.read_bytes()
    except (FileNotFoundError, PermissionError, OSError):
        secret_accessible = False
    else:
        secret_accessible = True
    if secret_accessible:
        return 3
    write_new_canonical_json(
        args.output,
        {
            "schema_version": "keyless-isolation-harness-v1",
            "public_input_accessible": True,
            "public_input_sha256": hashlib.sha256(public_bytes).hexdigest(),
            "evaluator_secret_location_accessible": False,
            "sandbox_uid": os.getuid(),
            "sandbox_gid": os.getgid(),
            "claim_boundary": (
                "OS mount-boundary harness only; no ephemeris, chart computation, scoring, "
                "or scientific recovery was performed"
            ),
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
