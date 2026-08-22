#!/usr/bin/env python3
"""Fetch the minimal Swiss Ephemeris files required for the 1926-2026 HD cache.

Files are downloaded from the official aloistr/swisseph GitHub repository at an
immutable commit. This script does not accept Moshier as a substitute.
"""

from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

UPSTREAM_COMMIT = "3fd0f956d73898b91cc4f67cf18b21af656d1342"
FILES = ("sepl_18.se1", "semo_18.se1")
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


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    output = repo_root / "data" / "ephemeris"
    output.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, object] = {
        "source_repository": "aloistr/swisseph",
        "source_commit": UPSTREAM_COMMIT,
        "files": {},
    }

    for name in FILES:
        destination = output / name
        url = f"{BASE_URL}/{name}"
        print(f"fetching {url}")
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                payload = response.read()
        except Exception as exc:  # pragma: no cover - network-dependent helper
            print(f"ERROR: could not download {name}: {exc}", file=sys.stderr)
            return 2
        if len(payload) < 100_000:
            print(f"ERROR: downloaded {name} is implausibly small", file=sys.stderr)
            return 3
        destination.write_bytes(payload)
        digest = sha256(destination)
        manifest["files"][name] = {
            "bytes": len(payload),
            "sha256": digest,
            "source_url": url,
        }
        print(f"wrote {destination} sha256={digest}")

    manifest_path = output / "swisseph_ephemeris_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"wrote {manifest_path}")
    print("Next: run `hdmatch validate-engine` and require returned ephemeris flags to be SWIEPH.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
