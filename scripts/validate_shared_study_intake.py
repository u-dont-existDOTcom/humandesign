#!/usr/bin/env python3
"""Validate a private shared-study metadata record and optionally write a new copy."""

from __future__ import annotations

import argparse
import json
import sys
from hashlib import sha256
from pathlib import Path

from pydantic import ValidationError

from hdmatch.participant.shared_intake_metadata import (
    canonical_shared_intake_bytes,
    parse_shared_study_intake_metadata,
    write_shared_intake_metadata,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Private source JSON; it is never modified")
    parser.add_argument(
        "--output", type=Path,
        help="Optional new private canonical JSON file; existing files are never replaced",
    )
    args = parser.parse_args(argv)
    try:
        record = parse_shared_study_intake_metadata(args.input.read_bytes())
        raw = canonical_shared_intake_bytes(record)
    except ValidationError as error:
        # Do not echo submitted values, full records, participant IDs or birth hashes.
        issues = [
            {"field": ".".join(str(part) for part in item["loc"]), "type": item["type"]}
            for item in error.errors(include_url=False, include_input=False)
        ]
        print(json.dumps({"valid": False, "issues": issues}, sort_keys=True), file=sys.stderr)
        return 2
    except (OSError, ValueError, UnicodeError):
        print(
            json.dumps({"valid": False, "error": "input unreadable or not strict valid JSON"}),
            file=sys.stderr,
        )
        return 2
    if args.output is not None:
        try:
            write_shared_intake_metadata(args.output, record)
        except (OSError, ValueError):
            print(
                json.dumps({
                    "valid": True, "written": False,
                    "error": "output must be a new file in an existing writable private directory",
                }),
                file=sys.stderr,
            )
            return 2
    print(json.dumps({
        "valid": True,
        "schema_version": record.schema_version,
        "canonical_sha256": sha256(raw).hexdigest(),
        "written": args.output is not None,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
