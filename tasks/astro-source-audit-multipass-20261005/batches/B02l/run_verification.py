"""Standalone standard-library verification entry for the extracted B02l packet."""
import hashlib
import json
import sys
import unittest
from pathlib import Path


def iter_tests(suite):
    for child in suite:
        if isinstance(child, unittest.TestSuite):
            yield from iter_tests(child)
        else:
            yield child


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    suite = unittest.defaultTestLoader.discover(str(here), pattern="test_lilly_dariot.py")
    ids = [t.id() for t in iter_tests(suite)]
    files = ["lilly_dariot_reference.py", "test_lilly_dariot.py", "RULES.json", "SECTION_COVERAGE.json", "UNRESOLVED.json", "REFERENCE_TABLES.json", "LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json", "RETAINED_LILLY_INDEX_BEFORE.json"]
    manifest = [{"path": n, "sha256": hashlib.sha256((here / n).read_bytes()).hexdigest()} for n in files]
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    summary = {"tests_run": result.testsRun, "discovered_test_ids": ids, "distinct_test_count": len(set(ids)), "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped), "successful": result.wasSuccessful(), "test_files": manifest, "predictive_validation": False}
    (here / "TEST_RUN_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    raise SystemExit(0 if result.wasSuccessful() else 1)
