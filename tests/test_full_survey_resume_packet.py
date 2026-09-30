"""Source-preservation tests; no claim of semantic or scientific validity."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("resume_packet",ROOT/"scripts/build_full_survey_resume_packet.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PacketTests(unittest.TestCase):
    def test_authority_hashes_match(self):
        for rel,sha in mod.SOURCES:
            self.assertEqual(mod.git_blob_sha((ROOT/rel).read_bytes()),sha)
    def test_full_originals_embedded_exactly_once(self):
        packet=mod.build_packet(ROOT)
        for rel,_ in mod.SOURCES:
            original=(ROOT/rel).read_text()
            begin=f"<!-- BEGIN {rel} -->\n"
            end=f"<!-- END {rel} -->"
            self.assertEqual(packet.count(begin),1)
            embedded=packet.split(begin,1)[1].split(end,1)[0]
            self.assertEqual(embedded,original)
    def test_full_bank_preserved_not_short_pilot(self):
        b=json.loads((ROOT/mod.SURVEY/"interviewer-bank-v7.json").read_text())
        self.assertEqual(len(b["questions"]),79)
        self.assertEqual(len({q["id"] for q in b["questions"]}),79)
        self.assertIn('"id": "M03"',mod.build_packet(ROOT))
    def test_all_evidence_facets_preserved(self):
        g=json.loads((ROOT/mod.SURVEY/"EVIDENCE-GUIDE-v7.json").read_text())
        self.assertEqual(len({x['facet_id'] for x in g}),73)
    def test_hash_drift_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            p=root/mod.TASK/'IMPORT-AND-RESUME-PROTOCOL-v1.md'
            p.parent.mkdir(parents=True)
            p.write_text('test')
            for rel,_ in mod.SOURCES:
                p=root/rel
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes((ROOT/rel).read_bytes())
            (root/mod.SOURCES[0][0]).write_text('changed authority')
            with self.assertRaises(ValueError):
                mod.build_packet(root)
    def test_no_empty_or_duplicate_original_ids(self):
        b=json.loads((ROOT/mod.SURVEY/'interviewer-bank-v7.json').read_text())
        self.assertTrue(all(q['id'] and q['question'] for q in b['questions']))
    def test_review_repairs_are_carried_in_the_packet(self):
        packet=mod.build_packet(ROOT)
        self.assertIn("not verified evidence of the exact prompt originally shown",packet)
        self.assertIn("Do not show an interpreted profile before new questions",packet)
        self.assertIn("reviewed_for_development_fitting",packet)
    def test_rules_do_not_claim_mechanical_semantic_validation(self):
        p=(ROOT/mod.TASK/'IMPORT-AND-RESUME-PROTOCOL-v1.md').read_text()
        self.assertIn('must never set semantic_validated=true',p)
        self.assertIn('Exact wording is not a validity requirement',p)
        self.assertIn('Partial inputs can support',p)

if __name__=='__main__':
    unittest.main()
