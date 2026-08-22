#!/usr/bin/env python3
"""Generate or verify the canonical V3.6 mapping-library-v2 artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

from hdmatch.model.v4_3_profile_mapping import (
    verify_tracked_profile_mapping_artifacts,
    write_profile_mapping_artifacts_new,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--write",
        action="store_true",
        help="create the five canonical artifacts; refuse to overwrite any file",
    )
    action.add_argument(
        "--check",
        action="store_true",
        help="recompile in memory and verify exact tracked artifact bytes",
    )
    args = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[1]
    if args.write:
        paths = write_profile_mapping_artifacts_new(repository_root)
        for path in paths:
            print(path.relative_to(repository_root))
    else:
        verify_tracked_profile_mapping_artifacts(repository_root)
        print("canonical V3.6 mapping-library-v2 artifacts verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
