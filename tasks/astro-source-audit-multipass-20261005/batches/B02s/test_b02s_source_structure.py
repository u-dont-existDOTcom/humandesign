"""Documentary integrity: validates source packet, not astrological predictions."""
import unittest,hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
def rd(n):return json.loads((B/n).read_text())
D=rd("RULES.json")
R=D["rules"]
LOOK={r["record_number"]:r for r in R}
M=rd("SOURCE_IMAGE_MANIFEST.json")
C=rd("COUNTS.json")
I=rd("RETAINED_LILLY_INDEX_BEFORE.json")
U=rd("UNRESOLVED.json")
E=rd("ERRATA_COLLATION.json")
ORDER=rd("RULES_SOURCE_ORDER.json")["ids"]
SRC="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
class OriginalSourceStructure(unittest.TestCase):
 def test_contiguous_ids_and_counts(self):
  self.assertEqual(D["record_count"],len(R))
  self.assertEqual(list(LOOK),list(range(1921,1921+len(R))))
  self.assertEqual(D["first_record"],"R1921")
  self.assertEqual(D["last_record"],f"R{1920+len(R)}")
 def test_previous_canonical_index_unchanged(self):
  self.assertEqual(I["records_count"],1920)
  self.assertEqual(I["batches"][-1]["id"],"B02r")
  self.assertEqual(I["next"]["chapter"],"XLIX")
 def test_candidate_arithmetic(self):
  self.assertEqual(C["lilly_before"],1920)
  self.assertEqual(C["records"],len(R))
  self.assertEqual(C["lilly_if_accepted"],1920+len(R))
  self.assertEqual(C["combined_if_accepted"],2986+len(R))
  self.assertEqual(C["verified_couple_outcomes"],0)
  self.assertFalse(C["empirical_validation"])
 def test_original_source_identity(self):
  self.assertEqual(M["original_sha256"],SRC)
  self.assertEqual(M["content_pages"],list(range(336,354)))
 def test_original_evidence_images_hashes(self):
  self.assertEqual(len(M["images"]),19)
  self.assertEqual({v["pdf_page"] for v in M["images"]},set(range(336,354))|{888})
  for x in M["images"]:
   p=B/x["path"]
   self.assertTrue(p.is_file(),x["path"])
   self.assertEqual(p.stat().st_size,x["bytes"])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x["sha256"])
 def test_page_locators_in_scope(self):
  for r in R:
   p=r["source_locator"]["pdf_pages"]
   self.assertTrue(p and all(336<=x<=353 for x in p))
   self.assertEqual(r["source_locator"]["printed_pages"],[x-34 for x in p])
   self.assertEqual(r["source_locator"]["page_images"],[f"evidence/pdf-{x}.png" for x in p])
   self.assertFalse(r["source_locator"]["source_statement_is_verbatim"])
 def test_no_runtime_claims(self):
  for r in R:
   self.assertEqual(r["runtime_status"],"REFERENCE_ONLY_NOT_PROMOTED")
   self.assertFalse(r["independently_verified_outcome"])
   self.assertFalse(r["prospective_frozen_forecast"])
   self.assertFalse(r["case_evidence_countable"])
 def test_read_order_preserves_all_ids(self):
  self.assertEqual(len(ORDER),len(R))
  self.assertEqual(set(ORDER),set(LOOK))
  self.assertEqual(len(ORDER),len(set(ORDER)))
  pages=[min(LOOK[n]["source_locator"]["pdf_pages"]) for n in ORDER]
  self.assertEqual(pages,sorted(pages))
 def test_original_187_plus_source_additions(self):
  self.assertEqual(D["initial_draft_record_count"],187)
  self.assertEqual(D["added_missed_original_units"],len(R)-187)
  self.assertTrue(all(n<=2107 for n in LOOK if not LOOK[n].get("source_review_inserted")))
  self.assertTrue(all(LOOK[n]["source_review_inserted"] for n in LOOK if n>=2108))
 def test_source_errata_six_directions(self):
  self.assertEqual(E["count"],6)
  self.assertEqual([x["printed_page"] for x in E["entries"]],[305,306,307,312,315,315])
  self.assertTrue(E["original_body_unchanged"])
 def test_34_plus_30_retained_limits(self):
  self.assertEqual(U["retained_count"],len(U["limits"]))
  self.assertEqual(U["retained_count"],64)
  self.assertEqual(len({v["id"] for v in U["limits"]}),64)
 def test_each_page_covered(self):
  S=rd("SECTION_COVERAGE.json")
  self.assertEqual([x["pdf_page"] for x in S["pages"]],list(range(336,354)))
  for v in S["pages"]:
   self.assertTrue(v["records"])
 def test_claim_ledger_matches_report(self):
  ledger=rd("CLAIM_LEDGER.json")
  report=(B/"AUDIT_REPORT.md").read_bytes()
  self.assertEqual(ledger["report_sha256"],hashlib.sha256(report).hexdigest())
  self.assertEqual("\n\n".join(x["text"] for x in ledger["units"]),report.decode())
  for v in ledger["units"]:
   self.assertEqual(hashlib.sha256(v["text"].encode()).hexdigest(),v["sha256"])
class EachSourceRecord(unittest.TestCase):pass
def make(n):
 def test(self):
  v=LOOK[n]
  self.assertTrue(v["source_statement"] and len(v["source_statement"])>35)
  self.assertTrue(v["preconditions"] and v["exceptions_and_evidence_limits"])
  self.assertIn("PARAPHRASE",v["source_statement_type"])
  self.assertEqual(v["record_number"],n)
 test.__name__=f"test_record_R{n}_documentary_schema"
 return test
for n in LOOK:setattr(EachSourceRecord,f"test_record_R{n}_documentary_schema",make(n))
if __name__=="__main__":unittest.main()
