"""Independent first-source-review regressions; no empirical astrology validation."""
from pathlib import Path
import hashlib,json,unittest
B=Path(__file__).resolve().parent
def rd(n):return json.loads((B/n).read_text())
RULES={q["record_number"]:q for q in rd("RULES.json")["rules"]}
U=rd("UNRESOLVED.json")
U_BY={x["id"]:x["description"] for x in U["limits"]}
C=rd("SECTION_COVERAGE.json")
def text(n):
 q=RULES[n]
 return " ".join([q["source_statement"]]+q["preconditions"]+q["exceptions_and_evidence_limits"])

class IndependentCorrections(unittest.TestCase):
 def test_source_reviewer_original_verbatim_frozen(self):
  p=B/"independent_review/OPUS_INITIAL_DIAGNOSIS.md"
  self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),
    "76e1516b5ed919abde128f341f6286d13a5be56dc5a2c499c1f920278641bce0")
  self.assertIn("FINDS_ERROR",p.read_text())
 def test_corrected_aphorism31_warre_not_wane(self):
  s=text(1907)
  self.assertIn("WAR",s);self.assertIn("journey",s.lower())
  self.assertIn("marriage",s.lower())
  self.assertNotIn("waning"," ".join([RULES[1907]["source_statement"]]+RULES[1907]["preconditions"]).lower())
  self.assertIn("impeded",s.lower())
 def test_moon_reception_in_aphorism6(self):
  s=text(1882).lower()
  for w in ("moon","saturn","mars","mutual","reception"):self.assertIn(w,s)
  self.assertIn("not merely any",s)
 def test_aphorism40_unfortunate_not_natural_malefic(self):
  s=text(1916).lower()
  for w in ("unfortunate","afflicted","seventh","birth"):self.assertIn(w,s)
  self.assertIn("not necessarily",s)
 def test_page_join_or_vs_and_retained(self):
  s=text(1896)
  self.assertIn("catchword",s)
  self.assertIn("'or'",s)
  self.assertIn("and Angles",s)
  self.assertIn("unresolved",s.lower())
  self.assertIn("U18",U_BY)
 def test_angular_positive_negative_conflict_retained(self):
  a=text(1862).lower();b=text(1865).lower()
  self.assertIn("direct",a);self.assertIn("contradiction",a)
  self.assertIn("direct",b);self.assertIn("not to be delivered",b)
  self.assertIn("u36"," ".join(U_BY).lower())
 def test_aphorism16_source_not_deleted(self):
  s=text(1892).lower()
  self.assertIn("cast not any aspect",s)
  self.assertIn("not",s)
  self.assertIn("ellipt",s)
 def test_determinate_two_examples_same_scope(self):
  s=text(1860).lower()
  self.assertIn("both",s);self.assertIn("same",s)
  self.assertIn("determinate",s)
 def test_combustion_angles_uncertain(self):
  s=text(1869).lower()
  self.assertIn("entering",s)
  self.assertIn("unresolved",s)
  self.assertIn("angular",s)
 def test_both_planets_in_aphorism36(self):
  s=text(1912).lower()
  self.assertIn("both",s)
  for t in ("peregrine","retrograde","cadent","may then be doubted"):self.assertIn(t,s)
 def test_source_precision_not_emended(self):
  self.assertIn("sixteen minutes",text(1902).lower())
  self.assertIn("twelve degrees",text(1902).lower())
  self.assertIn("what signe it will",text(1902).lower())
  self.assertIn("it seldome failes",text(1919).lower())
  self.assertIn("hope well",text(1884).lower())
  self.assertIn("as good as freed",text(1857).lower())
 def test_moon_good_house_with_moon(self):
  s=text(1887).lower()
  self.assertIn("moon",s);self.assertIn("good house",s)
  self.assertIn("to a good planet",s)
 def test_joined_not_forced_only_conjunction(self):
  s=text(1900).lower()
  self.assertIn("broad",s)
  self.assertIn("joining",s)
 def test_all_nine_actual_source_images_exist(self):
  base=rd("SOURCE_IMAGE_MANIFEST.json")
  self.assertEqual(len(base["images"]),9)
  for f in base["images"]:
   q=B/f["path"]
   self.assertTrue(q.exists(),f["path"])
   self.assertEqual(hashlib.sha256(q.read_bytes()).hexdigest(),f["sha256"])
 def test_page_to_records_exact_vs_original(self):
  m={x["pdf_page"]:x for x in C["partitions"]}
  for p in range(330,337):
   actual=[r for r,q in RULES.items() if p in q["source_locator"]["pdf_pages"]]
   row=m[p]
   self.assertEqual(row["first_source_record"],f"R{min(actual)}")
   self.assertEqual(row["last_source_record"],f"R{max(actual)}")
   self.assertEqual(row["exact_source_record_count"],len(actual))
  self.assertEqual(m[337]["exact_source_record_count"],0)
 def test_uncertainties_retained_and_no_promotions(self):
  self.assertEqual(U["retained_count"],39)
  self.assertEqual(len(U_BY),39)
  self.assertTrue(all(not r["independently_verified_outcome"] and r["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for r in RULES.values()))
 def test_report_exact_claim_ledger(self):
  report=(B/"AUDIT_REPORT.md").read_bytes()
  led=rd("CLAIM_LEDGER.json")
  self.assertEqual(hashlib.sha256(report).hexdigest(),led["report_sha256"])
  self.assertEqual(led["unit_count"],len(led["units"]))
  self.assertEqual("\n\n".join(q["text"] for q in led["units"]),report.decode())
if __name__=="__main__":unittest.main()
