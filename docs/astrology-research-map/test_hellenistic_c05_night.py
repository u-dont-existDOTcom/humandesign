"""Archaeological/textual semantics tests; never human prediction claims."""
import unittest

from paulus_trigon_narrative_c05 import (
    TRIGON_ORDER, TRIGON_DAY_NIGHT, narrative_one_cycle,
    narrative_degree_ruler, printed_diurnal_difference_summary,
)
from paulus_monomoiria_source_c04 import edited_day_degree_ruler


class TestPaulusGreekNarrativeC05(unittest.TestCase):
    def test_primary_sect_pairs_from_greek_chapter_2(self):
        self.assertEqual(TRIGON_DAY_NIGHT, {
            "fire":("Sun","Jupiter"),
            "earth":("Venus","Moon"),
            "air":("Saturn","Mercury"),
            "water":("Venus","Mars"),
        })

    def test_night_fire_beginning_explicitly_in_chapter_32(self):
        self.assertEqual(narrative_one_cycle("fire","night")[:2],
                         ("Jupiter","Sun"))
        self.assertEqual(narrative_degree_ruler("Aries",1,sect="night"),"Jupiter")
        self.assertEqual(narrative_degree_ruler("Aries",2,sect="night"),"Sun")

    def test_seven_star_cycle_and_repetition_for_both_sects(self):
        all_planets={"Sun","Jupiter","Venus","Moon","Saturn","Mercury","Mars"}
        for t in TRIGON_ORDER:
            for sect in ("day","night"):
                seq=narrative_one_cycle(t,sect)
                self.assertEqual(len(seq),7)
                self.assertEqual(set(seq),all_planets)
                sign={"fire":"Aries","earth":"Taurus","air":"Gemini","water":"Cancer"}[t]
                for degree in range(1,24):
                    self.assertEqual(narrative_degree_ruler(sign,degree,sect=sect),
                                     narrative_degree_ruler(sign,degree+7,sect=sect))

    def test_expected_day_and_night_water_orders(self):
        # Six apart from initial seven are derived from paired-sect
        # priority + skip-duplicates. NOT a Greek manuscript table.
        self.assertEqual(narrative_one_cycle("water","day"),
                         ("Venus","Mars","Sun","Jupiter","Moon","Saturn","Mercury"))
        self.assertEqual(narrative_one_cycle("water","night"),
                         ("Mars","Venus","Jupiter","Sun","Moon","Mercury","Saturn"))

    def test_disagreement_from_printed_diurnal_canon_is_preserved(self):
        result=printed_diurnal_difference_summary()
        self.assertEqual(result["difference_count"],
                         {"fire":0,"earth":0,"air":16,"water":18})
        self.assertEqual(result["total_differing_cells"],34)
        self.assertEqual(result["total_cells"],120)
        self.assertEqual(result["scientific_status"],"SOURCE_DISAGREEMENT_ONLY")
        self.assertEqual(narrative_degree_ruler("Cancer",8,sect="day"),"Venus")
        self.assertEqual(edited_day_degree_ruler("Cancer",8,sect="day"),"Mars")
        self.assertEqual(narrative_degree_ruler("Gemini",3,sect="day"),"Venus")
        self.assertEqual(edited_day_degree_ruler("Gemini",3,sect="day"),"Mars")

    def test_invalid_sources_not_forced_to_known(self):
        for t,sect in [("air","dawn"),("unknown","night"),
                       ("water",None)]:
            with self.assertRaises(ValueError):
                narrative_one_cycle(t,sect)
        for sign,degree,sect in [("Gemini",0,"day"),("Cancer",31,"night"),
                                 ("Cancer",2.4,"day"),("Cancer",True,"day"),
                                 ("Ophiuchus",1,"night"),("Cancer",5,"unknown")]:
            with self.assertRaises(ValueError):
                narrative_degree_ruler(sign,degree,sect=sect)


if __name__=="__main__":
    unittest.main()
