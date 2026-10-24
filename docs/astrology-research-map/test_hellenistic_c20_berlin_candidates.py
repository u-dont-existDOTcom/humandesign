"""C20 textual conditional-candidate tests, not predictive-human evaluation."""
import unittest

from berlin_c20_conditional_monomoiria import (
    record, egyptian_Libra_term, Moon_monomoiria_candidates, source_constrained_audit
)
from paulus_bysign_papyrus_c04 import sign_monomoiria


class TestBerlinC20ConditionalLongitude(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=record()
        cls.audit=source_constrained_audit()

    def test_source_object_and_editor_are_distinct(self):
        a=self.source["sources"]
        self.assertIn("P. Berol. 21347",a["Berlin"])
        self.assertIn("p296",a["editor"])
        self.assertIn("Loeb English p97",a["primary_terms"])
        self.assertTrue(self.source["editorial_state"]["Moon_name_partly_restored"])

    def test_all_four_values_exactly_match_editorial_possibilities(self):
        self.assertEqual(self.audit["all_source_compatible_completed_degrees"],[2,9,16,23])
        self.assertEqual([r["completed_degree"] for r in self.source["candidate_table"]],[2,9,16,23])

    def test_moon_ruler_and_ordinals_for_all_possible_values(self):
        c=Moon_monomoiria_candidates()
        self.assertEqual([v["ordinal_degree"] for v in c],[3,10,17,24])
        self.assertTrue(all(sign_monomoiria("Libra",v["completed_degree"],35)=="Moon" for v in c))

    def test_egyptian_Libra_terms_exact_boundaries(self):
        spec=self.source["Egyptian_terms_Libra"]
        self.assertEqual(spec["order"],["Saturn","Mercury","Jupiter","Venus","Mars"])
        self.assertEqual(spec["widths"],[6,8,7,7,2])
        self.assertEqual(sum(spec["widths"]),30)
        self.assertEqual(spec["cumulative_ends"],[6,14,21,28,30])
        expected={0:"Saturn",5:"Saturn",6:"Mercury",13:"Mercury",14:"Jupiter",20:"Jupiter",21:"Venus",27:"Venus",28:"Mars",29:"Mars"}
        for d,p in expected.items():
            self.assertEqual(egyptian_Libra_term(d,35),p)

    def test_canonical_candidates_have_four_distinct_terms(self):
        self.assertEqual([r["Egyptian_term"] for r in self.audit["four_mathematically_possible_rows"]],
                         ["Saturn","Mercury","Jupiter","Venus"])

    def test_Saturn_term_is_conditional_not_original_papyrus_fact(self):
        self.assertEqual(self.audit["hypothetical_Egyptian_Saturn_terms_only_candidates"],[2])
        self.assertEqual(self.audit["editors_conditional_favorite"],2)
        self.assertFalse(self.audit["original_papyrus_exact_degree_independently_certified"])
        self.assertFalse(self.audit["Egyptian_terms_assumption_proved_for_this_scribe"])
        self.assertFalse(self.audit["monomoiria_only_determines_unique_degree"])

    def test_off_by_one_ordinal_interpretation_does_not_fake_moon(self):
        # Confusing ordinal numbers 2/9/16/23 with completed-degree positions
        # yields Mercury, not Moon. A negative historical index check.
        for ordinal in [2,9,16,23]:
            self.assertEqual(sign_monomoiria("Libra",ordinal-1,35),"Mercury")

    def test_inputs_fail_closed_at_all_boundaries(self):
        for d in [-1,30,1.5,"2",True]:
            with self.assertRaises(ValueError):
                egyptian_Libra_term(d,35)
        for m in [-1,60,0.5,"35",True]:
            with self.assertRaises(ValueError):
                egyptian_Libra_term(2,m)

    def test_independent_outcomes_unchanged_and_no_production_scoring(self):
        q=self.source["boundaries"]
        self.assertEqual((q["P_Oxy_4277_historical_agreements"],q["P_Oxy_4277_historical_disagreements"]),(1,2))
        self.assertEqual(q["human_predictive_validations"],0)
        self.assertFalse(q["production_scoring_changed"])
        self.assertTrue(q["gansten_Kindle_not_extracted"])

    def test_source_not_falsely_marked_fully_read(self):
        self.assertIn("not fully rendered PDF",self.source["sources"]["editor"])
        self.assertTrue(self.source["editorial_state"]["degree_missing_in_papyrus"])
        self.assertTrue(self.source["editorial_state"]["preferred_is_conjectural"])


if __name__=="__main__":
    unittest.main()
