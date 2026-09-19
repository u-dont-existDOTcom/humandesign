#!/usr/bin/env python3
"""Export unchanged frozen human packets with unfilled response templates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hdmatch.evaluation.development_human_handoff import (
    export_development_human_calibration_bundle,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        receipt = export_development_human_calibration_bundle(args.prepared_dir, args.output_dir)
    except (ValueError, OSError):
        parser.exit(1, "Human handoff export failed; inspect the private inputs locally.\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
