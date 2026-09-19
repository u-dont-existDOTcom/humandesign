#!/usr/bin/env python3
"""Export the verified recurrence-corrected Life Patterns human calibration bundle v2."""

from __future__ import annotations

import argparse
import json

from hdmatch.evaluation.development_human_handoff_v2 import (
    export_development_human_calibration_bundle_v2,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    receipt = export_development_human_calibration_bundle_v2(
        args.prepared_dir,
        args.output_dir,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
