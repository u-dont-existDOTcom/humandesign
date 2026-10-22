"""B51/B52 combined source-fidelity tests. Not a predictive astrology model."""
import unittest

BJ = ('अर्थाप्तिः पितृपितृपत्निशत्रुमित्रभ्रातृस्त्रीभृतकजनाद्दिवाकराद्यैः '
      'होरेन्द्वोर्दशमगतैर्विकल्पनीया भेन्द्वर्कास्पदपतिगांशनाथवृत्त्या')
JP = ('अर्थाप्तिः पितृजननीसपत्नमित्रभ्रातृतकजनाहिवाकराद्यैः '
      'होरेन्द्वोर्दशमगतैविकल्पनीया भेन्द्वर्कास्पदपतिगांशनाथवृत्त्या')
FOOT = 'भेन्द्वर्कास्पदपतिगांशनाथवृत्त्या'

def adverse_trios(tenth_lord):
    en = {'Mercury','Jupiter',tenth_lord}
    sa = {'Mercury','Jupiter','Venus'}
    return en,sa

def orders(sun_tenth,mars_conjunct,lord_angular):
    return (sun_tenth and mars_conjunct and lord_angular,
            (sun_tenth or mars_conjunct) and lord_angular)

def reputation_witnesses(adverse=True):
    return {'printed':('NEGATIVE' if adverse else 'UNTRIGGERED'),
            'electronic':('POSITIVE' if adverse else 'UNTRIGGERED'),
            'canonical':None, 'score_allowed':False}

def eleventh_v2_v10(malefic_in_11th):
    return {'gain_v2':bool(malefic_in_11th),'loss_v10':bool(malefic_in_11th),
            'v9_resolves_collision':False,'score_allowed':False}

def textual_parallel(a,b):
    return (a.startswith('अर्थाप्तिः') and b.startswith('अर्थाप्तिः')
            and FOOT in a and FOOT in b)

class SourceIntegrity(unittest.TestCase):
    def test_v3_different_planets_tenth_lord_saturn(self):
        self.assertNotEqual(*adverse_trios('Saturn'))
    def test_v3_same_planets_if_venus_is_tenth_lord(self):
        self.assertEqual(*adverse_trios('Venus'))
    def test_v3_replacement_tenth_lord_not_sanskrit_original(self):
        self.assertNotIn('Saturn',adverse_trios('Saturn')[1])
    def test_v16_disjoint_sun_only(self):
        self.assertEqual(orders(True,False,True),(False,True))
    def test_v16_disjoint_mars_only(self):
        self.assertEqual(orders(False,True,True),(False,True))
    def test_v16_both_and_no_lord(self):
        self.assertEqual(orders(True,True,True),(True,True))
        self.assertEqual(orders(True,True,False),(False,False))
    def test_v24_polarity_opposes_and_abstains(self):
        r=reputation_witnesses();self.assertNotEqual(r['printed'],r['electronic'])
        self.assertIsNone(r['canonical']);self.assertFalse(r['score_allowed'])
    def test_v24_untriggered_not_prediction(self):
        self.assertEqual(reputation_witnesses(False)['printed'],'UNTRIGGERED')
    def test_eleventh_overlap_no_priority(self):
        r=eleventh_v2_v10(True)
        self.assertTrue(r['gain_v2'] and r['loss_v10'])
        self.assertFalse(r['v9_resolves_collision'] or r['score_allowed'])
    def test_bj_jp_near_verbatim_not_identical(self):
        self.assertTrue(textual_parallel(BJ,JP));self.assertNotEqual(BJ,JP)
    def test_garbled_suffix_not_independent_parallel(self):
        self.assertFalse(textual_parallel(BJ,JP.replace(FOOT,'')))
    def test_generic_arthapti_word_not_enough(self):
        self.assertFalse(textual_parallel('अर्थाप्तिः','अर्थाप्तिः इति'))

if __name__=='__main__': unittest.main()
