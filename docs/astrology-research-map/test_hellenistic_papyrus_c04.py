"""Mechanical tests for Paulus by-sign monomoiria and the 319 CE papyrus.

These are historical-reconstruction tests, *not* forward human validation.
"""
import unittest
from paulus_bysign_papyrus_c04 import (
    CHALDEAN_SEQUENCE, SIGN_DOMICILE, PAPYRUS_ROWS,
    sign_monomoiria, documented_papyrus_check,
)


class TestDocumentaryMonomoiriaC04(unittest.TestCase):
    def test_twelve_signs_and_seven_rulers(self):
        self.assertEqual(len(SIGN_DOMICILE),12)
        self.assertEqual(len(CHALDEAN_SEQUENCE),7)
        self.assertEqual(len(set(CHALDEAN_SEQUENCE)),7)
        self.assertTrue(set(SIGN_DOMICILE.values()).issubset(CHALDEAN_SEQUENCE))
        for s,r in SIGN_DOMICILE.items():
            self.assertEqual(sign_monomoiria(s,0,0),r)
            self.assertEqual(sign_monomoiria(s,7,59),r)

    def test_papyrus_preserves_negative_result(self):
        observed=documented_papyrus_check()
        self.assertEqual(observed["checked_rows"],7)
        self.assertEqual(observed["disagreements"],1)
        mismatches=[x for x in observed["records"] if not x["agrees"]]
        self.assertEqual(mismatches,[{
            "body":"Mercury", "ruler_in_text":"Mars",
            "calculated_ruler":"Saturn", "agrees":False,
            "textual_status":"SOURCE_REPORTED_ERROR",
        }])
        self.assertIn("not_human_validation",observed["kind"])

    def test_first_and_late_degrees_off_by_one(self):
        self.assertEqual(sign_monomoiria("Aries",3,43),"Mercury")
        self.assertEqual(sign_monomoiria("Scorpio",22,32),"Sun")
        self.assertEqual(sign_monomoiria("Libra",29,18),"Mercury")
        self.assertEqual(sign_monomoiria("Sagittarius",13,53),"Saturn")
        self.assertEqual(sign_monomoiria("Taurus",9,40),"Moon")
        self.assertEqual(sign_monomoiria("Taurus",20,30),"Sun")
        self.assertNotEqual(sign_monomoiria("Aries",2,43), "Mercury")

    def test_minutes_do_not_change_degree_index(self):
        for sign in SIGN_DOMICILE:
            for deg in range(30):
                self.assertEqual(sign_monomoiria(sign,deg,0),
                                 sign_monomoiria(sign,deg,59))

    def test_fail_closed_on_non_integers_out_of_range(self):
        for sign,d,m in [("Ophiuchus",0,0),("Aries",-1,0),("Aries",30,0),
                         ("Aries",5,60),("Aries",4,-1),("Aries",True,0),
                         ("Aries",0,True),("Aries",2.5,0),("Aries",2,"35")]:
            with self.assertRaises(ValueError):
                sign_monomoiria(sign,d,m)

    def test_disallow_unverified_jupiter_label(self):
        self.assertNotIn("Jupiter", {r.body for r in PAPYRUS_ROWS})
        self.assertEqual(sign_monomoiria("Virgo",7,40),"Mercury")


if __name__=="__main__":
    unittest.main()
