"""Regressions for the second original-image source review; not efficacy tests."""
import json
import hashlib
import unittest
from pathlib import Path
from test_lilly_xlvi import B, rec, CHART, CASE, U, R

def t(n):
    r=rec(n)
    return " ".join([r["source_statement"]]+r["preconditions"]+r["exceptions_and_evidence_limits"])

class SecondReadback(unittest.TestCase):
    def test_original_cusp_not_assumed_ordinal(self):
        c=next(x for x in CHART["wheel_labels_provisional"] if x["sector"]=="sixth cusp")
        self.assertIn("13 32",c["printed"])
        self.assertIn("14. of ♒",c["confidence"])
        self.assertIn("no ordinal/rounding equivalence",c["confidence"])
        self.assertIn("ordinal",t(1792).lower())
        self.assertIn("possible",t(1792).lower())

    def test_mercury_then_sun_degree_then_saturn(self):
        u=next(x["description"] for x in U["limits"] if x["id"]=="U31")
        for s in ("Mercury", "Sun", "QUESTION", "Saturn", "distinct"):
            self.assertIn(s,u)
        self.assertIn("therein",t(1790))

    def test_prior_chapter_date_not_cited_to_july_page(self):
        r=(B/"AUDIT_REPORT.md").read_text()
        self.assertIn("B02o/CHAPTER_XLV_DATE_CORRECTION.md",r)
        self.assertIn("identical or different",r)
        self.assertNotIn("May 24 Chapter XLV",r)

    def test_full_rationale_conditions_preserved(self):
        r=(B/"AUDIT_REPORT.md").read_text()
        for x in ["both in fixed signs","accidentally almost","Mercury is the ascendant ruler"]:
            self.assertIn(x,r)
        self.assertIn("both in fixed signs",t(1784))
        self.assertIn("almost",t(1785))
        self.assertIn("Mercury",t(1787))

    def test_planetary_hour_copy_specific_h(self):
        self.assertIn("h-shaped",CHART["source_planetary_hour_glyph_qualification"])
        self.assertIn("medium-high",CHART["source_planetary_hour_glyph_qualification"])
        self.assertIn("7:22 AM:",CHART["source_clock_time"])

    def test_uncertain_july_date_propagated(self):
        self.assertTrue(any(w in t(1788).lower() for w in ("weak","imperfect")))
        self.assertIn("weak",t(1789).lower())
        self.assertIn("weak",CASE["source_death_date_legibility"].lower())
        self.assertFalse(CASE["independent_outcome_verification"])
        self.assertIn("provisionally read 28 July",(B/"AUDIT_REPORT.md").read_text())

    def test_that_day_unresolved_in_both_records(self):
        for n in [1791,1792]:
            self.assertIn("that day",t(n).lower())
            self.assertIn("preceding day",t(n).lower())
        self.assertTrue(any(x["id"]=="U37" for x in U["limits"]))

    def test_no_fabricated_chart_planet_signs(self):
        self.assertNotIn("planet signs",rec(1772)["source_statement"])
        v=CHART["wheel_body_readings_provisional"]
        self.assertGreaterEqual(len(v),4)
        self.assertTrue(all("visible_glyph" in x and "adjacent_degree_numerals" in x and "sign_reading" in x for x in v))
        self.assertTrue(all("UNRESOLVED" in x["sign_reading"] for x in v))
        self.assertFalse(CHART["independent_ephemeris_parity"])

    def test_verbatim_dyed_vs_normalized_died(self):
        self.assertIn("dyed",CASE["source_reported_death_text"])
        self.assertEqual(CASE["normalized_death_word"],"died")
        self.assertIn("normalized",CASE["normalization_note"])

    def test_calendar_convention_separate(self):
        self.assertNotIn("inferred_proleptic_gregorian_equivalent",CHART)
        self.assertEqual(CHART["computed_extended_gregorian_equivalent"],"1645-07-26")
        self.assertIn("proleptic",CHART["gregorian_calculation_convention"].lower())
        self.assertTrue(CHART["julian_not_explicit_in_print"])

    def test_multipage_images_and_editorial_class(self):
        for n in [1777,1789]:
            loc=rec(n)["source_locator"]
            self.assertEqual(loc["pdf_pages"],[323,324])
            self.assertEqual(loc["page_images"],["evidence/pdf-323.png","evidence/pdf-324.png"])
        self.assertTrue(rec(1789)["historical_evidence_class"].startswith("EDITORIAL"))
        self.assertTrue(rec(1793)["historical_evidence_class"].startswith("EDITORIAL"))
        self.assertFalse(rec(1789)["case_evidence_countable"])
        self.assertFalse(rec(1793)["case_evidence_countable"])

    def test_original_scope_and_words(self):
        report=(B/"AUDIT_REPORT.md").read_text()
        self.assertIn("CRYSIS",report)
        self.assertIn("most afflicted",report)
        self.assertIn("corporeal presence",report)
        self.assertIn("7:22 AM:",report)
        self.assertTrue(any(x["id"]=="U38" for x in U["limits"]))

    def test_claim_ledger_tracks_exact_report(self):
        content=(B/"AUDIT_REPORT.md").read_bytes()
        ledger=json.loads((B/"CLAIM_LEDGER.json").read_text())
        self.assertEqual(hashlib.sha256(content).hexdigest(),ledger["report_sha256"])
        self.assertEqual(len(ledger["units"]),26)
        for unit in ledger["units"]:
            self.assertEqual(hashlib.sha256(unit["text"].encode()).hexdigest(),unit["sha256"])
        self.assertEqual("\n\n".join(x["text"] for x in ledger["units"]),content.decode().rstrip("\n")+"\n")

if __name__=="__main__":
    unittest.main()
