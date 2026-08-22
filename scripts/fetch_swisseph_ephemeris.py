#!/usr/bin/env python3
"""Fetch the minimal Swiss Ephemeris files required for the 1926-2026 HD cache.

Files are downloaded from the official aloistr/swisseph GitHub repository at an
immutable commit. This script does not accept Moshier as a substitute.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import urllib.request
from collections.abc import Sequence
from pathlib import Path

from hdmatch.provenance.swisseph_files import (
    PINNED_UPSTREAM_COMMIT,
    REQUIRED_EPHEMERIS_FILES,
    EphemerisFilePin,
    EphemerisFileVerificationError,
    EphemerisManifestError,
    load_ephemeris_source_manifest,
    verify_ephemeris_directory,
)

UPSTREAM_COMMIT = PINNED_UPSTREAM_COMMIT
FILES = REQUIRED_EPHEMERIS_FILES
BASE_URL = (
    "https://raw.githubusercontent.com/aloistr/swisseph/"
    f"{UPSTREAM_COMMIT}/ephe"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _verify_payload(name: str, payload: bytes, expected: EphemerisFilePin) -> None:
    if len(payload) != expected.bytes:
        raise EphemerisFileVerificationError(
            f"downloaded byte-size mismatch for {name}: "
            f"expected {expected.bytes}, observed {len(payload)}"
        )
    digest = hashlib.sha256(payload).hexdigest()
    if digest != expected.sha256:
        raise EphemerisFileVerificationError(
            f"downloaded SHA-256 mismatch for {name}: "
            f"expected {expected.sha256}, observed {digest}"
        )


def _local_file_matches(path: Path, expected: EphemerisFilePin) -> bool:
    return (
        path.is_file()
        and path.stat().st_size == expected.bytes
        and sha256(path) == expected.sha256
    )


def main(argv: Sequence[str] | None = None) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repo_root / "data" / "ephemeris",
        help="directory for the locally provisioned .se1 files",
    )
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=repo_root / "data" / "ephemeris" / "manifest.json",
        help="repository-controlled pinned provenance manifest",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="verify existing local bytes without accessing the network",
    )
    args = parser.parse_args(argv)
    output: Path = args.output_dir
    source_manifest_path: Path = args.source_manifest
    output.mkdir(parents=True, exist_ok=True)
    receipt_path = output / "swisseph_ephemeris_manifest.json"
    receipt_path.unlink(missing_ok=True)

    try:
        source_manifest = load_ephemeris_source_manifest(source_manifest_path)
    except EphemerisManifestError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not args.verify_only:
        for name in FILES:
            destination = output / name
            expected = source_manifest.pin_for(name)
            if _local_file_matches(destination, expected):
                print(f"already verified {name} sha256={expected.sha256}")
                continue
            url = f"{BASE_URL}/{name}"
            print(f"fetching {url}")
            try:
                with urllib.request.urlopen(url, timeout=60) as response:
                    payload = response.read()
                _verify_payload(name, payload, expected)
                _atomic_write(destination, payload)
            except Exception as exc:  # pragma: no cover - network-dependent helper
                print(f"ERROR: could not provision verified {name}: {exc}", file=sys.stderr)
                return 3
            print(f"wrote verified {destination} sha256={expected.sha256}")

    try:
        verified = verify_ephemeris_directory(
            source_manifest_path=source_manifest_path,
            ephemeris_directory=output,
        )
    except (EphemerisManifestError, EphemerisFileVerificationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4

    receipt_bytes = (
        json.dumps(
            verified.model_dump(mode="json"),
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n"
    ).encode("utf-8")
    _atomic_write(receipt_path, receipt_bytes)

    for record in verified.files:
        print(f"verified {record.name} sha256={record.sha256}")
    print(f"source commit: {verified.source_commit}")
    print(f"file-set sha256: {verified.ephemeris_file_set_sha256}")
    print(f"wrote deterministic verification receipt {receipt_path}")
    print("Next: run `hdmatch validate-engine` and require returned ephemeris flags to be SWIEPH.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
