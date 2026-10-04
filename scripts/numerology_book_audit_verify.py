#!/usr/bin/env python3
"""Task-local evidence gate. Structural checks do not certify source interpretation."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "research/six-rule-life-timing-20261001"
BASELINE = {
    "reference/research/NUMEROLOGY_METHODOLOGY_AUDIT_V1_20261003.md": "e09a0201eab09078ee8df34204b9a02d90cb45a0",
    "reference/research/numerology_method_registry_v1_20261003.json": "9cf4a28bab2f8c9714c1c01fb503e918b3e29734",
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    errors = []
    branch = subprocess.check_output(["git", "-C", str(ROOT), "branch", "--show-current"], text=True).strip()
    lock = json.loads((ROOT / "tasks/ACTIVE-TASK.json").read_text())
    if branch != BRANCH or lock.get("requiredBranch") != BRANCH or lock.get("taskId") != "NUMEROLOGY-BOOK-AUDIT-20261004":
        errors.append("TASK_BRANCH_IDENTITY_MISMATCH")
    for path, expected in BASELINE.items():
        actual = subprocess.check_output(["git", "hash-object", str(ROOT / path)], text=True).strip()
        if actual != expected:
            errors.append("IMMUTABLE_V1_CHANGED: " + path)
    if not args.preflight:
        required = [
            "reference/research/NUMEROLOGY_BOOK_AUDIT_V2_20261004.md",
            "reference/research/numerology_method_registry_v2_20261004.json",
            "reference/research/numerology_v2_20261004/source_coverage.json",
            "reference/research/numerology_v2_20261004/formula_fixtures.json",
            "reference/research/numerology_v2_20261004/ambiguities.json",
            "reference/research/numerology_v2_20261004/freeze_manifest.json",
            "reference/research/numerology_v2_20261004/independent_review.md",
            "reference/research/numerology_v2_20261004/EMPIRICAL_COMPARISON_DESIGN.md",
        ]
        for path in required:
            if not (ROOT / path).is_file():
                errors.append("REQUIRED_ARTIFACT_MISSING: " + path)
        # Full registry/coverage/fixture validation is added with the audited schema.
        errors.append("SOURCE_COMPLETENESS_GATE_NOT_YET_IMPLEMENTED")
    print(json.dumps({"mode": "preflight" if args.preflight else "acceptance", "status": "FAIL" if errors else "PASS", "findings": errors}, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
