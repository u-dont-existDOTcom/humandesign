import unittest
from pada_source_scope_B59 import h,v12,v15,v27,v29,v22_transfer,v35_transfer,ParentRule

class SourceScope(unittest.TestCase):
    def test_house(self):
        self.assertEqual(h(11,0),2)
    def test_h_invalid(self):
        with self.assertRaises(ValueError):h(True,0)
    def test_27_AL(self):
        r=v27(0,6,1,True);self.assertEqual((r['SANSKRIT_AL_2'],r['PORTUGUESE_UL_2']),(True,False))
    def test_27_UL(self):
        r=v27(0,6,7,True);self.assertEqual((r['SANSKRIT_AL_2'],r['PORTUGUESE_UL_2']),(False,True))
    def test_27_same_reference(self):
        r=v27(4,4,5,True);self.assertTrue(r['SANSKRIT_AL_2'] and r['PORTUGUESE_UL_2'])
    def test_27_gate(self):
        with self.assertRaises(ValueError):v27(0,6,1)
    def test_12_sanskrit(self):
        self.assertTrue(v12(True,False,True)['SANSKRIT'])
    def test_12_portuguese_empty(self):
        for a in (True,False):
            for b in (True,False):
                self.assertFalse(v12(a,b,True)['PORTUGUESE_LITERAL'])
    def test_12_no_11_no_gain(self):
        self.assertFalse(v12(False,False,True)['SANSKRIT'])
    def test_12_12_aspect_no_gain(self):
        self.assertFalse(v12(True,True,True)['SANSKRIT'])
    def test_12_gate(self):
        with self.assertRaises(ValueError):v12(True,False)
    def test_15_source_disagreement(self):
        r=v15(True,False,True);self.assertFalse(r['SANSKRIT_NO_ASPECT']);self.assertTrue(r['PORTUGUESE_NO_MALEFIC_ASSOCIATION'])
    def test_15_no_aspect(self):
        self.assertTrue(v15(False,False,True)['SANSKRIT_NO_ASPECT'])
    def test_15_gate(self):
        with self.assertRaises(ValueError):v15(True,False)
    def test_29_kin_excluded(self):
        self.assertFalse(v29("child")['SANSKRIT_KARAKAMSHA_TRANSFER'])
    def test_29_omission_not_promotion(self):
        self.assertFalse(v29("wealth")['score_allowed'])
    def test_29_nonkin_source(self):
        self.assertTrue(v29("wealth")['SANSKRIT_KARAKAMSHA_TRANSFER'])
    def test_22_inheritance(self):
        r=v22_transfer(ParentRule('29.18',12,'expense'))
        self.assertEqual(r['derived_house'],11);self.assertFalse(r['independent_source'])
    def test_22_unrelated_not_inherited(self):
        with self.assertRaises(ValueError):v22_transfer(ParentRule('29.27',7,'expense'))
    def test_35_inheritance(self):
        r=v35_transfer('29.34','child')
        self.assertFalse(r['independent_source']);self.assertFalse(r['score_allowed'])
    def test_35_bad_target(self):
        with self.assertRaises(ValueError):v35_transfer('29.34','')
    def test_all_paths_non_scoring(self):
        results=[v27(0,6,1,True),v12(True,False,True),v15(False,False,True),v29('relative'),v22_transfer(ParentRule('29.16',12,'expense')),v35_transfer('29.34','child')]
        self.assertTrue(all(not r['score_allowed'] for r in results))

if __name__=='__main__':unittest.main()
