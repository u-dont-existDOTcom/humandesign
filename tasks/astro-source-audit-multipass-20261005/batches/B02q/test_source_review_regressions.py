"""B02q source-review regressions; documentary fidelity, not clinical validation."""
import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
def j(name):
    return json.loads((B/name).read_text())

R = {int(r["id"].split(".R")[-1]): r for r in j("RULES.json")["rules"]}
T = j("TABLE_GEOMETRY.json")
P = j("TABLE_PRINT_EXCEPTIONS.json")

class SourceReview(unittest.TestCase):
    def test_unnamed_objection(self):
        x = R[1806]
        self.assertEqual(x["claim_class"], "REPORTED_UNNAMED_OBJECTION")
        for word in ("except pestilential", "many times", "unnamed", "recovery"):
            self.assertIn(word, str(x).lower())

    def test_avicenna_is_not_galen(self):
        self.assertIn("est velox motus morbi", R[1807]["source_statement"])
        self.assertIn("not ascribe", str(R[1807]["preconditions"]))

    def test_table_exception_accounting(self):
        self.assertEqual(P["different_printed_positions"], 64)
        self.assertEqual(P["systematic_apparent_plus_one_degree"]["total_cells"], 60)
        self.assertEqual(P["systematic_apparent_plus_one_degree"]["columns_1based"], [3,7,11,15])
        self.assertEqual(len(P["other_printed_anomalies"]), 4)
        self.assertEqual(T["printed_exception_authority"], "TABLE_PRINT_EXCEPTIONS.json")
        self.assertIn("NOT_DIPLOMATIC", T["reconstruction_status"])

    def test_historical_ambiguities(self):
        self.assertIn("all one", R[1798]["source_statement"])
        self.assertIn("eighth", T["chart_input"])
        self.assertIn("unresolved", str(R[1838]).lower())
        self.assertEqual(j("UNRESOLVED.json")["retained_count"], 32)
        e = j("ERRATA_COLLATION.json")["entries"]
        self.assertFalse(e[0]["body_target_line_matched"])
        self.assertTrue(e[1]["body_target_line_matched"])

    def test_report_exact_claim_ledger(self):
        b = (B/"AUDIT_REPORT.md").read_bytes()
        ledger = j("CLAIM_LEDGER.json")
        self.assertEqual(hashlib.sha256(b).hexdigest(),ledger["report_sha256"])
        self.assertEqual(ledger["unit_count"],len(ledger["units"]))
        for q in ledger["units"]:
            self.assertEqual(hashlib.sha256(q["text"].encode()).hexdigest(),q["sha256"])

if __name__ == "__main__":
    unittest.main()
