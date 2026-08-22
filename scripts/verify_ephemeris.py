#!/usr/bin/env python3
"""Verify local ephemeris files against the committed provenance manifest."""

from __future__ import annotations

import argparse
from pathlib import Path

from hdmatch.provenance.swisseph_files import (
    EphemerisFileVerificationError,
    EphemerisManifestError,
    verify_ephemeris_directory,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", required=True, type=Path, dest="ephemeris_dir")
    args = parser.parse_args()
    try:
        verified = verify_ephemeris_directory(
            source_manifest_path=ROOT / "data" / "ephemeris" / "manifest.json",
            ephemeris_directory=args.ephemeris_dir,
        )
    except (EphemerisManifestError, EphemerisFileVerificationError) as exc:
        print(f"EPHEMERIS_INVALID:{exc}")
        return 1
    print(f"EPHEMERIS_OK:{verified.source_commit}:{verified.ephemeris_file_set_sha256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
