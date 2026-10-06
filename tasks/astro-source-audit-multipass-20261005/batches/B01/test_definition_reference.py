import importlib.util
import json
import math
import unittest
from pathlib import Path

B = Path(__file__).parent
spec = importlib.util.spec_from_file_location("ptolemy_definition_reference", B / "definition_reference.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class DefinitionsTest(unittest.TestCase):
    def test_sect_six_fixed_members(self):
        for p in ["SUN", "JUPITER", "SATURN"]:
            self.assertEqual(m.planet_classes(p)["sect"], "DIURNAL")
        for p in ["MOON", "VENUS", "MARS"]:
            self.assertEqual(m.planet_classes(p)["sect"], "NOCTURNAL")
    def test_mercury_depends_on_supplied_phase(self):
        self.assertEqual(m.planet_classes("MERCURY", mercury_phase="MORNING")["sect"], "DIURNAL")
        self.assertEqual(m.planet_classes("MERCURY", mercury_phase="EVENING")["sect"], "NOCTURNAL")
    def test_mercury_unknown_is_not_nocturnal_default(self):
        for phase in [None, "UNKNOWN", "BOUNDARY"]:
            self.assertEqual(m.planet_classes("MERCURY", mercury_phase=phase)["sect"], "UNRESOLVED")
    def test_invalid_phase_rejected(self):
        with self.assertRaises(ValueError): m.planet_classes("MERCURY", mercury_phase="RETROGRADE")
    def test_intrinsic_categories_not_sect(self):
        self.assertEqual(m.planet_classes("MARS")["historical_category"], "masculine")
        self.assertEqual(m.planet_classes("MARS")["sect"], "NOCTURNAL")
    def test_moon_is_beneficent_in_this_source(self):
        self.assertEqual(m.planet_classes("MOON")["benefic_class"], "beneficent")
    def test_sun_not_unconditional_benefic(self):
        self.assertEqual(m.planet_classes("SUN")["benefic_class"], "common")
    def test_outer_planets_not_imported_into_ptolemy(self):
        with self.assertRaises(ValueError): m.planet_classes("PLUTO")
    def test_no_personal_or_health_prediction(self):
        self.assertIsNone(m.planet_classes("SATURN")["person_outcome_claim"])
    def test_four_open_intervals(self):
        for p, q in [(45,"MOISTURE"),(135,"HEAT"),(225,"DRYNESS"),(315,"COLD")]:
            self.assertEqual(m.lunar_phase_quality(0,p)["quality"], q)
    def test_exact_boundaries_not_silently_assigned(self):
        for p in [0,90,180,270,360]:
            self.assertEqual(m.lunar_phase_quality(0,p)["quality"], "BOUNDARY_UNRESOLVED")
    def test_wraparound(self):
        self.assertEqual(m.lunar_phase_quality(350,20)["quality"], "MOISTURE")
        self.assertEqual(m.lunar_phase_quality(20,350)["quality"], "COLD")
    def test_boundary_neighbours(self):
        self.assertEqual(m.lunar_phase_quality(0,89.999)["quality"], "MOISTURE")
        self.assertEqual(m.lunar_phase_quality(0,90.001)["quality"], "HEAT")
    def test_nonfinite_and_nonnumeric_rejected(self):
        for v in [math.nan, math.inf, -math.inf, True, "45", None]:
            with self.assertRaises(ValueError): m.lunar_phase_quality(0,v)
    def test_records_unique_and_source_bound(self):
        d=json.loads((B/"RULES.json").read_text()); rows=d["records"]
        self.assertEqual(d["records_count"],24);self.assertEqual(len({r["id"] for r in rows}),24)
        for r in rows:
            self.assertEqual(r["source_locator"]["source_file_sha256"],"10b44f40e47409215aa3d6c4ec2863ebc3982b81d33b4d4e5e2a065761ab7fec")
            self.assertIn("project_guardrails",r);self.assertIn("source_exceptions",r)
            self.assertNotIn("exceptions",r)
            self.assertEqual(r["admission"],"SOURCE_AUDIT_ONLY_NOT_ADMITTED_TO_FROZEN_PREDICTION_MODELS")
    def test_all_eight_chapters_have_dispositions(self):
        d=json.loads((B.parents[1]/"SECTION_DISCOVERY.json").read_text())
        self.assertEqual(len(d["sections"]),61)
        read=[x for x in d["sections"] if x["status"]=="READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE"]
        self.assertEqual([x["chapter"] for x in read],list(range(1,9)))
        self.assertEqual(sum(x["status"]=="INDEXED_NOT_READ" for x in d["sections"]),53)
    def test_superior_phase_not_extended_to_mercury_venus(self):
        self.assertEqual(m.record("R22")["antecedents"]["planet"],["SATURN","JUPITER","MARS"])
    def test_same_quality_and_opposite_quality_rules_both_retained(self):
        self.assertIn("reinforces",m.record("R24")["title"])
        self.assertIn("moderates",m.record("R20")["title"])

if __name__ == "__main__": unittest.main()
