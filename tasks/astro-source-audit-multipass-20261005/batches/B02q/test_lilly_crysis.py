"""Focused documentary/conditional regressions for the original 1647 Chapter XLVII.

A PASS means source packet and declared extraction invariants are coherent,
NOT that historical prognostic or medical claims are true.
"""
from pathlib import Path
import unittest,hashlib,json,re
B=Path(__file__).resolve().parent
def rd(name): return json.loads((B/name).read_text())
D=rd("RULES.json");RULES=D["rules"]
R={int(x["id"].split(".R")[-1]):x for x in RULES}
I=rd("RETAINED_LILLY_INDEX_BEFORE.json")
S=rd("SOURCE_IDENTITY.json")
IMG=rd("SOURCE_IMAGE_MANIFEST.json")
C=rd("COUNTS.json")
SEC=rd("SECTION_COVERAGE.json")
T=rd("TABLE_GEOMETRY.json")
ERR=rd("ERRATA_COLLATION.json")
U=rd("UNRESOLVED.json")
REPORT=(B/"AUDIT_REPORT.md").read_text()
def text(n):return " ".join([R[n]["source_statement"]]+R[n]["preconditions"]+R[n]["exceptions_and_evidence_limits"])
def hm(s):return hashlib.sha256(s).hexdigest()

class PacketIntegrity(unittest.TestCase):
    def test_ids_contiguous_and_boundary(self):
        self.assertEqual(list(R),list(range(1794,1852)))
        self.assertEqual((D["first_record"],D["last_record"],len(R)),(1794,1851,58))
    def test_previous_accepted_index_unchanged(self):
        self.assertEqual(I["records_count"],1793)
        self.assertEqual(I["batches"][-1]["id"],"B02p")
        self.assertEqual(I["next"]["chapter"],"XLVII")
        self.assertEqual(sum(x["records_count"] for x in I["batches"]),1793)
    def test_arithmetic_and_source_units(self):
        self.assertEqual((C["lilly_before"],C["new_documentary_records"],C["lilly_after_if_accepted"],C["retained_ptolemy"],C["combined_if_accepted"]),(1793,58,1851,1066,2917))
        self.assertEqual((C["new_historical_patient_cases"],C["new_original_patient_charts"],C["independently_verified_patient_outcomes"]),(0,0,0))
    def test_pdf_full_source_sha(self):
        self.assertEqual(S["source_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
        self.assertEqual(IMG["source_pdf_sha256"],S["source_full_pdf_sha256"])
        self.assertEqual(S["page_count"],894)
    def test_exact_source_page_boundaries(self):
        self.assertEqual(S["admitted_pdf_pages"],list(range(324,331)))
        self.assertEqual(SEC["exact_start"],"below horizontal divider PDF324")
        self.assertEqual(SEC["exact_end"],"above horizontal divider PDF330")
        self.assertEqual(R[1794]["source_locator"]["pdf_pages"],[324])
        self.assertEqual(R[1851]["source_locator"]["pdf_pages"],[330])
    def test_source_images_exact_hash(self):
        self.assertEqual(len(IMG["included"]),8)
        for row in IMG["included"]:
            p=B/row["path"];self.assertTrue(p.is_file(),p)
            self.assertEqual(p.stat().st_size,row["bytes"])
            self.assertEqual(hm(p.read_bytes()),row["sha256"])
        self.assertEqual({x["pdf_page"] for x in IMG["included"]},set(range(324,331))|{888})
    def test_all_source_locators_carry_physical_images(self):
        for r in RULES:
            loc=r["source_locator"]
            self.assertEqual(loc["printed_pages"],[p-34 for p in loc["pdf_pages"]])
            self.assertEqual(len(loc["page_images"]),len(loc["pdf_pages"]))
            self.assertTrue(all((B/p).is_file() for p in loc["page_images"]))
            self.assertFalse(loc["source_statement_is_verbatim"])
    def test_no_imported_clinical_or_predictive_evidence(self):
        self.assertTrue(all(not r["case_evidence_countable"] and not r["chart_countable"] and not r["blinded_prospective_prediction"] and not r["clinical_efficacy_verified"] and not r["independently_verified_patient_outcome"] for r in RULES))
        self.assertTrue(all(r["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for r in RULES))
        self.assertFalse(C["clinical_or_predictive_validation"])
    def test_all_conditions_and_limits_explicit(self):
        self.assertTrue(all(r["preconditions"] and r["exceptions_and_evidence_limits"] and r["dependency_group"] for r in RULES))
        self.assertTrue(all(r["source_statement_type"]=="NORMALIZED_PARAPHRASE_NOT_DIPLOMATIC_TRANSCRIPTION" for r in RULES))
    def test_no_missing_section_page(self):
        self.assertTrue(SEC["all_seven_original_pages_in_packet"])
        self.assertTrue(all(p in {q["pdf_page"] for q in SEC["sections"]} for p in range(324,331)))
        self.assertGreaterEqual(len(SEC["sections"]),19)
    def test_errata_p291_and_p295(self):
        e=ERR["entries"]
        self.assertEqual([(x["target_printed_page"],x["read_token"]) for x in e],[(291,"do"),(295,"atram")])
        self.assertTrue(all(x["body_target_line_matched"] is False for x in e))
        self.assertTrue(ERR["source_body_not_overwritten"])
    def test_unresolved_count_matches(self):
        self.assertEqual(U["retained_count"],len(U["limits"]))
        self.assertGreaterEqual(len(U["limits"]),30)
        self.assertEqual(len({x["id"] for x in U["limits"]}),len(U["limits"]))

class ConditionalSourceReading(unittest.TestCase):
    def test_crisis_does_not_mean_only_death(self):
        self.assertIn("further disease",text(1797))
        self.assertIn("nature",text(1795).lower())
        self.assertIn("sickness prevails",text(1796).lower())
    def test_onset_first(self):
        self.assertIn("illness first began",text(1799).lower())
        self.assertIn("onset",text(1800).lower())
        self.assertIn("less certain",text(1800).lower())
    def test_urine_then_first_requested_conversation(self):
        self.assertIn("first brought",text(1800).lower())
        self.assertIn("no urine",text(1801).lower())
        self.assertIn("asks for judgment",text(1801).lower())
    def test_ancient_attributions_not_collated(self):
        self.assertIn("Galen",text(1802))
        self.assertIn("Hippocrat",text(1805))
        self.assertIn("Avicenna",text(1807))
        for n in (1802,1805,1807):
            self.assertEqual(R[n]["claim_class"],"ATTRIBUTED_ANCIENT_AUTHORITY")
    def test_malignant_exception_retained(self):
        self.assertIn("malignant",text(1806).lower())
        self.assertIn("exception",text(1806).lower())
    def test_inferior_cause_rival(self):
        self.assertIn("inferior causes",text(1808).lower())
        self.assertIn("continued",text(1809).lower())
    def test_moon_theory_not_verified(self):
        self.assertIn("Moon",text(1810))
        self.assertIn("empirical",text(1810).lower())
    def test_anchor_radix_not_natal_chart(self):
        self.assertTrue(any(k in text(1811).lower() for k in ("onset","first moment of illness")))
        self.assertIn("natal chart",text(1811).lower())
        self.assertIn("first",text(1812).lower())
    def test_crisis_aspect_categories(self):
        s=text(1814).lower()
        for key in ("indicative","semiquadrate","opposition"):self.assertIn(key,s)
        self.assertTrue(any(k in s for k in ("quartile","quadrature")))
        self.assertIn("full crisis",s)
    def test_example_prior_figure_is_hypothetical(self):
        self.assertIn("16 July 1645",text(1815))
        self.assertIn("hypothetical",text(1815).lower())
        self.assertTrue(C["reuses_unvalidated_previous_july_horoscope_as_hypothetical"])
    def test_rounding_not_exact(self):
        for x in ("15 degrees 42 minutes","16 degrees","18 arcminutes"):self.assertIn(x,text(1816))
        self.assertTrue(any("15°43" in x["description"] for x in U["limits"]))
    def test_first_indicative_and_semi(self):
        self.assertIn("8 degrees 30",text(1817))
        self.assertIn("Libra",text(1817))
        self.assertIn("Scorpio 1",text(1819))
        self.assertIn("half crisis",text(1819).lower())
    def test_second_indicative_then_true_quartile(self):
        self.assertIn("Scorpio 23 degrees 30",text(1820))
        self.assertIn("Sagittarius 16",text(1821))
        self.assertIn("quadrature",text(1821))
    def test_aspects_attached_to_event(self):
        self.assertIn("planet",text(1818).lower())
        self.assertIn("planet",text(1822).lower())
        self.assertIn("better or worse",text(1822).lower())
    def test_continue_all_positions(self):
        self.assertTrue(any(k in text(1823).lower() for k in ("remaining","further","repeating")))
    def test_house_cusps_not_natal(self):
        for k in ("sixth","seventh","eighth"):self.assertIn(k,text(1824).lower())
    def test_benefic_requires_survival_qualification(self):
        self.assertIn("ordained for life",text(1827))
        self.assertIn("survival",text(1827).lower())
    def test_treatment_not_advice(self):
        for n in (1828,1836,1837,1838):
            self.assertEqual(R[n]["claim_class"],"HISTORICAL_MEDICAL_DOCTRINE")
            self.assertTrue(any(k in " ".join(R[n]["exceptions_and_evidence_limits"]).lower() for k in ("historical","not", "avoid", "unvalidated")))
    def test_7_14_21_not_exact_dates(self):
        self.assertIn("seven",text(1830).lower())
        self.assertIn("fourteen",text(1830).lower())
        self.assertIn("twenty-one",text(1830).lower())
        self.assertIn("variable",text(1831).lower())
    def test_moon_sign_temperament_four_way(self):
        self.assertEqual([R[n]["dependency_group"] for n in range(1832,1836)],["humoral_temperament"]*4)
        for n,keys in [(1832,("Aries","Leo","Sagittarius","phlegmatic")),(1833,("Taurus","Virgo","Capricorn","sanguine")),(1834,("Gemini","Libra","Aquarius","melancholic")),(1835,("Cancer","Scorpio","Pisces","choleric"))]:
            x=text(n).lower()
            for k in keys:self.assertIn(k.lower(),x)
    def test_three_purging_planets_are_conditional(self):
        for n,k in [(1836,"Jupiter"),(1837,"Venus"),(1838,"Mars")]:
            s=text(n)
            self.assertIn("Cancer/Scorpio/Pisces",s)
            self.assertIn("sextile/trine",s)
            self.assertIn(k,s)
        self.assertIn("Sun",text(1838))
    def test_seven_planet_faculty_items(self):
        got=[R[n]["source_record_kind"] for n in range(1839,1846)]
        self.assertEqual(got,["saturn_retentive","jupiter_faculty","mars_faculty","sun_faculty","venus_faculty","mercury_faculty","moon_faculty"])
    def test_four_elements_distinct_from_sign_faculties(self):
        for n,k in [(1846,"red choler"),(1847,"black melancholy"),(1848,"blood"),(1849,"phlegm")]:
            self.assertIn(k,text(n).lower())
            self.assertEqual(R[n]["dependency_group"],"elemental_humours")
    def test_booker_and_next_headed_chapter(self):
        self.assertIn("Booker",text(1850))
        self.assertIn("XLVIII",text(1851))
        self.assertIn("below",text(1851).lower())
        self.assertIn("1852",(B/"CONTINUE_HANDOFF.md").read_text())

class DerivedTableNotObservedPatients(unittest.TestCase):
    def test_grid_shape(self):
        self.assertEqual((T["printed_rows"],T["printed_columns"],T["derived_coordinate_cells"]),(30,16,480))
        self.assertEqual((len(T["table_data"]),len(T["table_data"][0])),(30,16))
        self.assertTrue(all(len(r)==16 for r in T["table_data"]))
        self.assertEqual(T["columns_step_from_previous_arcminutes"],1350)
    def test_480_computed_cells_arithmetic(self):
        signs=["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
        for row in range(30):
            for col in range(16):
                val=T["table_data"][row][col]
                arc=(30+60*row+1350*col)%21600
                self.assertEqual(val["longitude_arcminutes"],arc)
                self.assertEqual((val["sign"],val["degree"],val["minutes"]),
                                 (signs[arc//1800],(arc%1800)//60,arc%60))
    def test_first_source_row_cells(self):
        got=T["table_data"][0]
        self.assertEqual([(p["sign"],p["degree"],p["minutes"]) for p in got[:3]],[("Aries",0,30),("Aries",23,0),("Taurus",15,30)])
    def test_source_example_same_row_across_five_columns(self):
        row=T["table_data"][8]
        self.assertEqual([(p["sign"],p["degree"],p["minutes"]) for p in row[7:12]],
                         [("Virgo",16,0),("Libra",8,30),("Scorpio",1,0),("Scorpio",23,30),("Sagittarius",16,0)])
    def test_explicit_not_a_full_original_diplomatic_replay(self):
        self.assertIn("EDITORIAL",T["reconstruction_status"])
        self.assertTrue(any(k in T["original_source_cell_verification_scope"].lower() for k in ("unverified","not individually")))
        self.assertTrue(T["not_calendar_days"])
        self.assertEqual(R[1825]["source_locator"]["pdf_pages"],[328])
        self.assertEqual(R[1826]["source_locator"]["pdf_pages"],[328])
    def test_one_printed_table_not_480_observed_successes(self):
        self.assertEqual(C["printed_table_count"],1)
        self.assertEqual(C["derived_table_cells_not_observed_cases"],480)
        self.assertEqual(C["new_historical_patient_cases"],0)

if __name__=="__main__":unittest.main()
