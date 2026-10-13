"""Deterministic source-bound checks of B02r, not empirical validation.

Each of 43 numbered 1647 general horary aphorisms gets an independent test ID.
Source images and source-sha are also checked, with page and clause qualifiers.
"""
import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
def rd(name):return json.loads((B/name).read_text())
D=rd("RULES.json");R=D["rules"];BY={x["record_number"]:x for x in R}
COUNT=rd("COUNTS.json");SRC=rd("SOURCE_IDENTITY.json");SEC=rd("SECTION_COVERAGE.json")
IMAGES=rd("SOURCE_IMAGE_MANIFEST.json");ERR=rd("ERRATA_COLLATION.json")
U=rd("UNRESOLVED.json");INDEX=rd("RETAINED_LILLY_INDEX_BEFORE.json")
def txt(n):return (BY[n]["source_statement"]+" "+" ".join(BY[n]["preconditions"]+BY[n]["exceptions_and_evidence_limits"])).lower()
def nh(s):return hashlib.sha256(s).hexdigest()
class Identity(unittest.TestCase):
    def test_contiguous_records(self):
        self.assertEqual([v["record_number"] for v in R],list(range(1852,1921)))
        self.assertEqual([v["id"].split(".R")[-1] for v in R],list(map(str,range(1852,1921))))
    def test_units_sum(self):
        self.assertEqual((D["record_count"],D["chapter_xlviii_own_units"],D["seventh_house_bridge_units"],D["general_horary_aphorism_units"],D["next_heading_boundary_units"]),(69,19,6,43,1))
    def test_cumulative_counts(self):
        self.assertEqual((COUNT["lilly_before"],COUNT["new_documentary_records"],COUNT["lilly_after_if_accepted"],COUNT["ptolemy_retained"],COUNT["combined_if_accepted"]),(1851,69,1920,1066,2986))
    def test_previous_index_not_advanced(self):
        self.assertEqual(INDEX["records_count"],1851)
        self.assertEqual(INDEX["batches"][-1]["id"],"B02q")
        self.assertEqual(INDEX["next"]["chapter"],"XLVIII")
        self.assertEqual(sum(v["records_count"] for v in INDEX["batches"]),1851)
    def test_source_full_original_sha(self):
        self.assertEqual(SRC["source_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
        self.assertEqual(SRC["full_pdf_pages"],894)
    def test_source_images_hash(self):
        self.assertEqual(len(IMAGES["images"]),9)
        self.assertEqual({v["pdf_page"] for v in IMAGES["images"]},set(range(330,338))|{888})
        for v in IMAGES["images"]:
            p=B/v["path"]
            self.assertTrue(p.is_file(),p)
            self.assertEqual(p.stat().st_size,v["bytes"])
            self.assertEqual(nh(p.read_bytes()),v["sha256"])
    def test_source_record_page_consistency(self):
        for v in R:
            loc=v["source_locator"]
            self.assertEqual(loc["printed_pages"],[x-34 for x in loc["pdf_pages"]])
            self.assertTrue(all(x in range(330,337) for x in loc["pdf_pages"]))
            self.assertTrue(all((B/x).is_file() for x in loc["page_images"]))
            self.assertFalse(loc["source_statement_is_verbatim"])
    def test_no_outcome_evidence_or_runtime_promotions(self):
        self.assertEqual((COUNT["new_original_horoscopes"],COUNT["new_historical_cases"],COUNT["independently_verified_outcomes"],COUNT["blinded_predictions"]),(0,0,0,0))
        self.assertFalse(COUNT["clinical_or_predictive_validation"])
        self.assertTrue(all(not v["case_evidence_countable"] and not v["independently_verified_outcome"] and not v["prospective_blinded_prediction"] and not v["clinical_efficacy_verified"] for v in R))
        self.assertTrue(all(v["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for v in R))
    def test_precise_boundaries_and_errata(self):
        self.assertEqual(SEC["numbered_aphorisms_source_range"],[1,43])
        self.assertTrue(SEC["chapter_xlviii_complete"] and SEC["seventh_intro_complete"] and SEC["horary_43_complete"])
        self.assertTrue(SEC["xlix_body_excluded"] and SEC["earlier_physician_43_is_distinct"])
        self.assertEqual(ERR["matching_entries"],[])
        self.assertIn("selective",ERR["absence_scope"])
    def test_record_qualifiers_and_paraphrase(self):
        self.assertTrue(all(v["preconditions"] and v["exceptions_and_evidence_limits"] for v in R))
        self.assertTrue(all(v["source_statement_type"]=="NORMALIZED_PARAPHRASE_NOT_DIPLOMATIC_QUOTE" for v in R))
    def test_all_43_numbers_no_gaps(self):
        aph=[v for v in R if "aphorism_number" in v]
        self.assertEqual(len(aph),43)
        self.assertEqual([v["aphorism_number"] for v in aph],list(range(1,44)))
        self.assertEqual([v["record_number"] for v in aph],list(range(1877,1920)))
    def test_aphorism_pages_exact(self):
        for i in range(1,44):
            expected=[332] if i<=8 else [333] if i<=19 else [333,334] if i==20 else [334] if i<=28 else [334,335] if i==29 else [335] if i<=39 else [336]
            self.assertEqual(BY[1876+i]["source_locator"]["pdf_pages"],expected,i)
    def test_intro_distinct_from_numbered(self):
        for n in range(1871,1877):
            self.assertNotIn("aphorism_number",BY[n])
        self.assertIn("forty-three",txt(1875))
        self.assertIn("any horary question",txt(1876))
        self.assertIn("forty-three",txt(1875))
    def test_previous_43_physician_distinguished(self):
        self.assertTrue(D["not_the_previous_physician_43"])
        self.assertTrue(COUNT["previous_physician_aphorisms_already_in_index"]==43)
        self.assertTrue(all("XLVIII-SEVENTH-HORARY" in v["id"] for v in R))
    def test_next_chapter_not_admitted(self):
        self.assertIn("xlix",txt(1920))
        self.assertIn("below",txt(1920))
        self.assertEqual(BY[1920]["source_locator"]["pdf_pages"],[336])
        self.assertIn("1921",(B/"CONTINUE_HANDOFF.md").read_text())
    def test_unresolved_count(self):
        self.assertEqual(U["retained_count"],len(U["limits"]))
        self.assertGreaterEqual(len(U["limits"]),30)
        self.assertEqual(len(set(v["id"] for v in U["limits"])),len(U["limits"]))
    def test_report_and_ledger(self):
        report=(B/"AUDIT_REPORT.md").read_bytes()
        ledger=rd("CLAIM_LEDGER.json")
        self.assertEqual(nh(report),ledger["report_sha256"])
        self.assertEqual(len(ledger["units"]),ledger["unit_count"])
        self.assertEqual("\n\n".join(x["text"] for x in ledger["units"]),report.decode())
        for u in ledger["units"]:
            self.assertEqual(nh(u["text"].encode()),u["sha256"])
class ChapterXLVIII(unittest.TestCase):
    def test_principal_house_assignments(self):
        for x in ("first house","moon"):self.assertIn(x,txt(1853))
        self.assertIn("tenth",txt(1854))
        self.assertIn("master",txt(1854))
    def test_exact_and_separating_conjunction(self):
        self.assertIn("degree and minute",txt(1856))
        self.assertIn("few minutes",txt(1857))
        self.assertIn("already",txt(1857))
    def test_fallback_order(self):
        self.assertIn("moon",txt(1858))
        self.assertIn("sun",txt(1859))
        self.assertIn("absent",txt(1858))
    def test_query_specificity(self):
        self.assertIn("determinate",txt(1860))
        self.assertIn("current particular master",txt(1860))
    def test_cadent_and_third_ninth(self):
        self.assertIn("cadent",txt(1861))
        for x in ("third","ninth"):self.assertIn(x,txt(1863))
        self.assertIn("moon",txt(1864))
    def test_angular_direct_vs_retrograde(self):
        s=txt(1865)
        for w in ("ascendant","tenth","seventh","fourth","direct"):self.assertIn(w,s)
        t=txt(1866)
        self.assertIn("retrograde",t)
        self.assertIn("slowness",t)
    def test_malefic_and_combustion(self):
        self.assertIn("conjunction",txt(1867))
        for w in ("square","opposition"):self.assertIn(w,txt(1868))
        self.assertIn("entering",txt(1869))
        self.assertIn("combustion",txt(1869))
    def test_seventh_bridge_after_sixth(self):
        self.assertIn("sixth-house",txt(1870))
        self.assertIn("seventh",txt(1871))
        for w in ("marriage","contracts","fugitives","thefts"):self.assertIn(w,txt(1872))
    def test_astrological_context_not_social_guidance(self):
        self.assertTrue(all("clinical_efficacy_verified" in x and not x["clinical_efficacy_verified"] for x in R[:19]))
class NumberedSourceAphorisms(unittest.TestCase):pass
# One distinct regression for EACH numbered record and its required conditional text.
anchors={
 1:("nature","triplicity"),2:("early","late"),3:("tenth","saturn","mars"),4:("trivial","question"),
 5:("moon","virtue"),6:("saturn","mars","moon","reception"),7:("jupiter","venus","dignity"),8:("fortunes","infortunes"),
 9:("void","cancer","taurus","sagittarius","pisces"),10:("separates","already"),11:("application","present"),
 12:("moon","fall"),13:("retrograde","first station"),14:("evil","good","solicitation"),
 15:("slow","delay"),16:("infortunes","not any aspect","fortunes"),17:("cadent","reception"),
 18:("reception","infortune"),19:("peregrine","essential"),20:("saturn","mars","triplicity","angles","or"),
 21:("fortune","dignity"),22:("weak","defer"),23:("combust","opposition"),24:("joined","infortunes"),
 25:("ascendant lord","cadent"),26:("twelve degrees","sixteen minutes","cazimi"),
 27:("saturn","jupiter","mars","venus","mercury","reverse"),28:("fixed","common","movable"),
 29:("head","tail","dragon"),30:("eclipse","ascendant"),31:("impeded","war"),
 32:("opposite","mercury","sagittarius","pisces"),33:("obstructing","house"),
 34:("angle","succedent","cadent"),35:("moon","sun","combustion"),
 36:("infortune","both","peregrine","retrograde"),37:("conjunct","nature"),
 38:("frustration","prohibition","before"),39:("fortune","house"),
 40:("seventh","birth","unfortunate"),41:("eighth","woman","debt"),42:("jupiter","venus","third","fourth","fifth"),
 43:("tail","scandal","house")
}
assert len(anchors)==43
def make_aph_test(i, words):
    def test(self):
        v=BY[1876+i]
        self.assertEqual(v["aphorism_number"],i)
        sentence=txt(1876+i)
        for w in words:self.assertIn(w,sentence,f"Aphorism{i} missing anchor {w}")
        self.assertTrue(v["exceptions_and_evidence_limits"],i)
    test.__name__=f"test_aphorism_{i:02d}_conditional_source"
    return test
for n,need in anchors.items():
    setattr(NumberedSourceAphorisms,f"test_aphorism_{n:02d}_conditional_source",make_aph_test(n,need))
if __name__=="__main__":unittest.main()
