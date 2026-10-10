"""Execute the focused suite and retain its actual result and test identities."""

import hashlib
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).parent


def identities(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from identities(item)
        else:
            yield item.id()


def main():
    suite = unittest.defaultTestLoader.discover(str(ROOT), pattern="test_lilly_sixth_opening.py")
    names = list(identities(suite))
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    log = output.getvalue()
    (ROOT / "TEST_B02k.txt").write_text(log, encoding="utf-8")
    evidence_files = ["test_lilly_sixth_opening.py", "lilly_sixth_opening_reference.py",
                      "RULES.json", "REFERENCE_TABLES.json", "SECTION_COVERAGE.json"]
    summary = {"batch": "B02k", "command": "python run_verification.py",
        "discovered_test_ids": names, "distinct_test_count": len(set(names)),
        "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "skipped": len(result.skipped), "successful": result.wasSuccessful(),
        "test_files": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in evidence_files},
        "log_sha256": hashlib.sha256(log.encode()).hexdigest(),
        "scope": "Source data, exact declared arithmetic, source-table routing and caller-qualified predicates.",
        "clinical_or_predictive_validation": False,
        "duplicate_execution_policy": "An independent or extracted-packet repeat does not add new test identities."}
    (ROOT / "TEST_RUN_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(log, end="")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
