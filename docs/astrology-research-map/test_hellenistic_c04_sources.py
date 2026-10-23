"""Source-note arithmetic tests only; no natal/behavioral accuracy claims."""
import json
import unittest
from pathlib import Path

from paulus_monomoiria_source_c04 import (
    PLANET_CYCLE,
    PRINTED_DIURNAL_FIRST,
    TRIPLICITIES,
    ZODIAC,
    CANON,
    EXAMPLE_VARIANT,
    edited_day_degree_ruler,
    source_specific_example,
    invariant_check,
    triplicity_for_sign,
)

BASE = Path(__file__).resolve().parent
WITNESS = BASE / "HEPHAISTIO_C04_GREEK_ENGLISH_NUMERIC_VARIANTS_V1.json"


class TestPaulusMonomoiriaC04(unittest.TestCase):
    def test_120_cells_7_planets_periodic(self):
        self.assertEqual(invariant_check()["cells_in_edition_diurnal_canon"], 120)
        self.assertEqual(invariant_check()["distinct_planets"], 7)
        for tri, members in TRIPLICITIES.items():
            names = [ZODIAC[i] for i in members]
            self.assertEqual([triplicity_for_sign(s) for s in names], [tri]*3)
            for sign in names:
                for degree in range(1,24):
                    self.assertEqual(
                        edited_day_degree_ruler(sign, degree, sect="day"),
                        edited_day_degree_ruler(sign, degree+7, sect="day")
                    )

    def test_direct_printed_gold_rows(self):
        # Four 30-row columns on visually inspected scanned PDF p83.
        self.assertEqual(
            [edited_day_degree_ruler(s,1,sect="day") for s in
             ("Leo","Taurus","Gemini","Cancer")],
            ["Sun","Venus","Saturn","Mars"]
        )
        self.assertEqual(
            [edited_day_degree_ruler(s,12,sect="day") for s in
             ("Aries","Virgo","Aquarius","Pisces")],
            ["Saturn","Mars","Jupiter","Moon"]
        )
        self.assertEqual(
            [edited_day_degree_ruler(s,30,sect="day") for s in
             ("Sagittarius","Capricorn","Libra","Scorpio")],
            ["Jupiter","Moon","Mercury","Sun"]
        )

    def test_example_paulus_vs_included_scholion_disagree(self):
        self.assertEqual(source_specific_example("Aries",12,CANON.name),"Saturn")
        self.assertEqual(source_specific_example("Cancer",8,CANON.name),"Mars")
        self.assertEqual(source_specific_example("Cancer",8,EXAMPLE_VARIANT.name),"Venus")
        self.assertEqual(invariant_check()["scholion_example_cancer_degree_8_disagrees"],1)
        with self.assertRaises(ValueError):
            source_specific_example("Cancer",9,EXAMPLE_VARIANT.name)

    def test_no_invented_nocturnal_or_unknown_rules(self):
        for s in ("night","unknown","Day",None):
            with self.assertRaises(ValueError):
                edited_day_degree_ruler("Aries",10,sect=s)
        for degree in (0,31,1.2,"8",True,-1):
            with self.assertRaises(ValueError):
                edited_day_degree_ruler("Aries",degree,sect="day")
        with self.assertRaises(ValueError):
            edited_day_degree_ruler("Ophiuchus",8,sect="day")


class TestGreekNumericalWitnessC04(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(WITNESS.read_text(encoding="utf-8"))

    def test_identified_snapshot_not_independent_manuscript(self):
        d=self.d
        self.assertTrue(d["source_greek"]["direct_text_verified"])
        self.assertTrue(d["source_greek"]["markdown_sha256"])
        self.assertIn("UNVERIFIED",d["source_greek"]["editorial_origin"])
        self.assertFalse(d["model_promotion"])
        self.assertEqual(d["human_validation_runs"],0)

    def test_english_greek_360_365_375_differ(self):
        d=self.d["section36"]
        self.assertEqual(sum(d["year_primary_periods"].values()),360)
        self.assertEqual(sum(d["greek_subperiod_headers"].values()),365)
        self.assertEqual(sum(d["english_subperiod_headers"].values()),375)
        self.assertEqual(sum(d["fine_subperiod_item_sums"].values()),365)
        self.assertEqual(d["greek_subperiod_headers"]["Moon"],71)
        self.assertEqual(d["english_subperiod_headers"]["Moon"],81)
        self.assertEqual(d["year_primary_periods"]["Mercury"],52)
        self.assertEqual(d["greek_subperiod_headers"]["Mercury"],57)
        self.assertEqual(d["fine_subperiod_item_sums"]["Saturn"],86)
        self.assertEqual(d["fine_subperiod_item_sums"]["Venus"],21)

    def test_section29_unresolved_150_vs_140(self):
        s=self.d["section29"]
        self.assertEqual(s["saturn_to_mercury_english"],150)
        self.assertEqual(s["saturn_to_mercury_greek_ρν"],150)
        self.assertEqual(s["later_valens_appendix_saturn_to_mercury"],140)
        self.assertNotEqual(s["saturn_to_mercury_greek_ρν"],s["later_valens_appendix_saturn_to_mercury"])


if __name__ == "__main__":
    unittest.main()
