import unittest
from oxy4277_monomoiria_audit_c05 import P_OXY_4277, documentary_audit, incorrect_ordinal_variant, AncientWitness

class TestOxyrhynchus4277C05(unittest.TestCase):
    def test_source_rows(self):
        self.assertEqual([(v.object_name,v.sign,v.completed_degrees,v.arcminutes,v.written_monomoiria) for v in P_OXY_4277],[
            ("Mercury","Capricorn",6,22,"Venus"),
            ("Midheaven","Taurus",27,8,"Mercury"),
            ("Lower Midheaven","Scorpio",27,8,"Jupiter")])

    def test_disagreements_remain(self):
        r=documentary_audit()
        self.assertEqual(r["n"],3)
        self.assertEqual(r["true_ordinal_agreements"],1)
        self.assertEqual(r["mistaken_ordinal_agreements"],0)
        self.assertEqual([v["Paulus_by_sign_true_ordinal"] for v in r["records"]],["Moon","Sun","Jupiter"])
        self.assertEqual([v["Paulus_by_sign_mistaken_ordinal"] for v in r["records"]],["Mercury","Mars","Saturn"])
        self.assertEqual([v["object_name"] for v in r["records"] if not v["agrees_true_ordinal"]],["Mercury","Midheaven"])
        self.assertFalse(r["model_promotion"])

    def test_out_of_range_flawed_convention(self):
        with self.assertRaises(ValueError):
            incorrect_ordinal_variant(AncientWitness("demo","Aries",0,1,"Mars","synthetic"))

if __name__=="__main__":
    unittest.main()
