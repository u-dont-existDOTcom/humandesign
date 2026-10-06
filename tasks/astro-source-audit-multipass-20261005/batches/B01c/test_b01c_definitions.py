import importlib.util
import json
import math
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("b01c_defs", B / "b01c_definitions.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
EG = "EGYPTIAN_ROBBINS_ADOPTED"
PT = "PTOLEMY_ROBBINS_ADOPTED"


class BookOneDefinitions(unittest.TestCase):
    def test_all_twelve_domiciles(self):
        self.assertEqual([m.domicile_owner(s) for s in m.SIGNS], ["MARS", "VENUS", "MERCURY", "MOON", "SUN", "MERCURY", "VENUS", "MARS", "JUPITER", "SATURN", "SATURN", "JUPITER"])

    def test_unknown_domicile(self):
        self.assertIsNone(m.domicile_owner(None))

    def test_bad_sign_rejected(self):
        with self.assertRaises(ValueError):
            m.domicile_owner("Ophiuchus")

    def test_exaltations_opposite_depressions(self):
        for p, row in m.DIGNITIES["exaltation_and_depression"].items():
            self.assertEqual(m.exaltation_state(p, row["exaltation"]), "EXALTATION")
            self.assertEqual(m.exaltation_state(p, row["depression"]), "DEPRESSION")
            self.assertEqual((m.SIGNS.index(row["exaltation"]) - m.SIGNS.index(row["depression"])) % 12, 6)

    def test_no_imported_exaltation_degrees(self):
        self.assertIsNone(m.DIGNITIES["exaltation_degrees"])

    def test_unsupported_planet(self):
        with self.assertRaises(ValueError):
            m.exaltation_state("NEPTUNE", "PISCES")

    def test_unknown_exaltation(self):
        self.assertIsNone(m.exaltation_state(None, "ARIES"))

    def test_triangles_cover_exactly_twelve_signs(self):
        signs = [s for r in m.DIGNITIES["triangles"] for s in r["signs"]]
        self.assertEqual(set(signs), set(m.SIGNS))
        self.assertEqual(len(signs), 12)

    def test_fire_sect_rulers(self):
        self.assertEqual(m.triangle_governors("ARIES", "DAY"), {"principal": "SUN", "co_ruler": None})
        self.assertEqual(m.triangle_governors("LEO", "NIGHT")["principal"], "JUPITER")

    def test_earth_air_sect_rulers(self):
        for s, day, night in [("TAURUS", "VENUS", "MOON"), ("GEMINI", "SATURN", "MERCURY")]:
            self.assertEqual(m.triangle_governors(s, "DAY")["principal"], day)
            self.assertEqual(m.triangle_governors(s, "NIGHT")["principal"], night)

    def test_water_retains_mars_and_coruler(self):
        self.assertEqual(m.triangle_governors("CANCER", "DAY"), {"principal": "MARS", "co_ruler": "VENUS"})
        self.assertEqual(m.triangle_governors("PISCES", "NIGHT"), {"principal": "MARS", "co_ruler": "MOON"})

    def test_triangle_unknown_sect(self):
        self.assertIsNone(m.triangle_governors("ARIES", None))

    def test_triangle_bad_sect(self):
        with self.assertRaises(ValueError):
            m.triangle_governors("ARIES", "TWILIGHT")

    def test_adopted_term_rows_complete(self):
        for scheme in (EG, PT):
            for sign in m.SIGNS:
                rows = m.term_rows(sign, scheme)
                self.assertEqual(len(rows), 5)
                self.assertEqual({r["planet"] for r in rows}, {"SATURN", "JUPITER", "MARS", "VENUS", "MERCURY"})
                self.assertEqual(sum(r["length_degrees"] for r in rows), 30)

    def test_all_table_boundaries(self):
        for scheme, sect in [(EG, None), (PT, None), ("CHALDEAN", "DAY"), ("CHALDEAN", "NIGHT")]:
            for sign in m.SIGNS:
                for row in m.term_rows(sign, scheme, sect):
                    lo, hi = row["computed_start"], row["computed_end"]
                    self.assertEqual(m.term_owner(sign, lo, scheme, sect), row["planet"])
                    self.assertEqual(m.term_owner(sign, math.nextafter(float(hi), -math.inf), scheme, sect), row["planet"])

    def test_two_tables_same_totals_not_same_rules(self):
        self.assertEqual(m.scheme_totals(EG), m.scheme_totals(PT))
        self.assertEqual(m.scheme_totals(EG), {"SATURN": 57, "JUPITER": 79, "MARS": 66, "VENUS": 82, "MERCURY": 76})
        self.assertNotEqual(m.term_owner("ARIES", 13, EG), m.term_owner("ARIES", 13, PT))

    def test_egyptian_capricorn_source_row(self):
        self.assertEqual([(r["planet"], r["length_degrees"]) for r in m.term_rows("CAPRICORN", EG)], [("MERCURY", 7), ("JUPITER", 7), ("VENUS", 8), ("SATURN", 4), ("MARS", 4)])

    def test_ptolemy_leo_starts_jupiter_not_repaired_from_prose(self):
        self.assertEqual(m.term_rows("LEO", PT)[0]["planet"], "JUPITER")

    def test_chaldean_day_totals(self):
        self.assertEqual(m.scheme_totals("CHALDEAN", "DAY"), m.TERMS["chaldean_construction"]["source_totals"]["DAY"])

    def test_chaldean_night_totals(self):
        self.assertEqual(m.scheme_totals("CHALDEAN", "NIGHT"), m.TERMS["chaldean_construction"]["source_totals"]["NIGHT"])

    def test_chaldean_group_pair_not_split(self):
        for sect in ("DAY", "NIGHT"):
            for sign in m.SIGNS:
                names = [r["planet"] for r in m.chaldean_rows(sign, sect)]
                self.assertEqual(abs(names.index("MERCURY") - names.index("SATURN")), 1)

    def test_chaldean_same_triangle_same_rows(self):
        for sect in ("DAY", "NIGHT"):
            for start in range(4):
                self.assertEqual(m.chaldean_rows(m.SIGNS[start], sect), m.chaldean_rows(m.SIGNS[start + 4], sect))
                self.assertEqual(m.chaldean_rows(m.SIGNS[start], sect), m.chaldean_rows(m.SIGNS[start + 8], sect))

    def test_chaldean_air_pair_first(self):
        self.assertEqual([r["planet"] for r in m.chaldean_rows("GEMINI", "NIGHT")], ["MERCURY", "SATURN", "MARS", "JUPITER", "VENUS"])

    def test_unknown_term_inputs(self):
        self.assertIsNone(m.term_owner(None, 3, EG))
        self.assertIsNone(m.term_owner("ARIES", None, EG))
        self.assertIsNone(m.term_owner("ARIES", 1, "CHALDEAN"))

    def test_invalid_term_numbers(self):
        for x in [-0.1, 30, 360, True, math.nan, math.inf, "3"]:
            with self.assertRaises(ValueError):
                m.term_owner("ARIES", x, PT)

    def test_no_unspecified_term_scheme(self):
        with self.assertRaises(ValueError):
            m.term_owner("ARIES", 1, "BEST_FITTING")

    def test_chariot_threshold(self):
        self.assertTrue(m.chariot_qualifies({"domicile": True, "triangle": True}))
        self.assertFalse(m.chariot_qualifies({"domicile": True, "triangle": False}))

    def test_chariot_unknown_not_false(self):
        self.assertIsNone(m.chariot_qualifies({"domicile": True, "triangle": None}))
        self.assertTrue(m.chariot_qualifies({"domicile": True, "triangle": True, "exaltation": None}))

    def test_chariot_nonboolean_rejected(self):
        with self.assertRaises(ValueError):
            m.chariot_qualifies({"domicile": 1})

    def test_latitude_side_fixture(self):
        self.assertTrue(m.same_ecliptic_side(1, 4))
        self.assertTrue(m.same_ecliptic_side(-1, -4))
        self.assertFalse(m.same_ecliptic_side(1, -1))

    def test_latitude_equality_not_implied(self):
        self.assertTrue(m.same_ecliptic_side(1, 4))
        self.assertNotEqual(1, 4)

    def test_latitude_unknown_equator(self):
        self.assertIsNone(m.same_ecliptic_side(None, 1))
        self.assertIsNone(m.same_ecliptic_side(0, 1))

    def test_bad_latitude_rejected(self):
        with self.assertRaises(ValueError):
            m.same_ecliptic_side(91, 1)

    def test_exact_table_disagreement_is_bounded(self):
        d = m.term_table_disagreement()
        self.assertEqual(d["different_degrees"], sum(d["per_sign"].values()))
        self.assertTrue(0 < d["different_degrees"] < 360)

    def test_source_record_coverage(self):
        d = json.loads((B / "RULES.json").read_text())
        self.assertEqual(d["records_count"], 53)
        self.assertEqual(len({r["id"] for r in d["records"]}), 53)
        self.assertEqual({r["source_locator"]["chapter_or_verse"] for r in d["records"]}, {f"I.{n}" for n in range(17, 25)})
        self.assertEqual(d["independent_predictions_count"], 0)
        self.assertTrue(all(r["admission"].startswith("SOURCE_AUDIT_ONLY") for r in d["records"]))

    def test_nonadoption_and_commentary_preserved(self):
        d = json.loads((B / "RULES.json").read_text())
        self.assertTrue(any(r["output_type"] == "EXPLICIT_SOURCE_NON_ADOPTION" for r in d["records"]))
        orb = next(r for r in d["records"] if r["title"].startswith("Numerical orb"))
        self.assertEqual(orb["source_locator"]["attribution_layer"], "ROBBINS_NOTE")
        self.assertEqual(orb["consequent"]["anonymous_commentator_max_deg"], 15)


if __name__ == "__main__":
    unittest.main()
