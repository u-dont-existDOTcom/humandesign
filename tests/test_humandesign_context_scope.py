"""Structural and exact-preservation tests; not a model-behavior evaluation."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/audits/2026-09-12-humandesign-context-scope.json"

def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

class InstructionScopeTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_all_non_authorized_source_bytes_are_preserved(self):
        for spec in self.record["edits"]:
            with self.subTest(path=spec["path"]):
                current = (ROOT / spec["path"]).read_bytes().decode("utf-8")
                for change in reversed(spec["changes"]):
                    self.assertEqual(current.count(change["new"]), 1)
                    current = current.replace(change["new"], change["old"], 1)
                self.assertEqual(blob(current.encode("utf-8")), spec["base_blob_sha1"])

    def test_semantic_scenarios_are_present_but_not_claimed_executed(self):
        cases = self.record["semantic_discriminators"]
        self.assertGreaterEqual(len(cases), 6)
        self.assertEqual(len(cases), len({c["id"] for c in cases}))
        self.assertFalse(self.record["live_semantic_evaluation_executed"])
        for case in cases:
            self.assertTrue(case["input"])
            self.assertTrue(case["expected"])

    def test_boundary_specific_contracts(self):
        for item in self.record["required_text"]:
            body = (ROOT / item["path"]).read_text(encoding="utf-8")
            for text in item["contains"]:
                with self.subTest(path=item["path"], required=text):
                    self.assertIn(text, body)
            for text in item.get("absent", []):
                with self.subTest(path=item["path"], forbidden=text):
                    self.assertNotIn(text, body)

if __name__ == "__main__":
    unittest.main()
