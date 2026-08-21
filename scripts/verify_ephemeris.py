#!/usr/bin/env python3
"""Verify local ephemeris files against the committed provenance manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hdmatch.util import sha256_file

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", required=True, type=Path, dest="ephemeris_dir")
    args = parser.parse_args()
    manifest = json.loads(
        (ROOT / "data" / "ephemeris" / "manifest.json").read_text(encoding="utf-8")
    )
    errors = 0
    for record in manifest["files"]:
        path = args.ephemeris_dir / record["name"]
        if not path.is_file():
            print(f"EPHEMERIS_FILE_MISSING:{path}")
            errors += 1
            continue
        if path.stat().st_size != record["bytes"]:
            print(f"EPHEMERIS_SIZE_MISMATCH:{path}")
            errors += 1
        if sha256_file(path) != record["sha256"]:
            print(f"EPHEMERIS_HASH_MISMATCH:{path}")
            errors += 1
    if errors:
        return 1
    print(f"EPHEMERIS_OK:{manifest['upstream_commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
