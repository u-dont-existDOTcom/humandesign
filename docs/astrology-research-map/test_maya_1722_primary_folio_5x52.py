#!/usr/bin/env python3
"""Direct photographed Berendt calendar observations vs frozen math reference."""
from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
import json
from pathlib import Path
import unittest

from maya_1722_five_by_52_reference import (
    SOURCE_INTERVAL, GROUP_SIZE, GROUP_COUNT, CYCLE_DAYS,
    reference_1722_almanac_group, all_reference_1722_almanac_groups,
)
from maya_calendar_reference import (
    KICHE_DAY_NAMES_BY_YUCATEC, reference_calendar_for_date,
)

DATA=json.loads(
    Path(__file__).with_name("MAYA_1722_PRIMARY_FACSIMILE_HAND_READ_B04.json")
    .read_text(encoding="utf-8")
)

class Facsimile1722DirectWitnessTests(unittest.TestCase):
    def test_famsi_item58_images_are_separately_pinned_not_redistributed(self):
        manuscript=DATA["manuscript"]
        images=manuscript["visually_examined_image_sha256"]
        self.assertEqual(manuscript["reported_image_pages"],69)
        self.assertEqual(len(images),DATA["status"]["image_pages_hash_pinned"])
        self.assertEqual(len({i["id"] for i in images}),len(images))
        self.assertTrue(all(len(i["sha256"])==64 for i in images))
        self.assertFalse(manuscript["facsimile_pages_original_digitized_work_separately_copied_to_repo"])
        self.assertIn("1877",manuscript["physical_primary_surrogate"])

    def test_all_30_independently_transcribed_photo_dates_match_frozen_reference(self):
        rows=DATA["observed_1722_1723_date_rows"]
        self.assertEqual(len(rows),30)
        self.assertEqual(len(set(r["gregorian"] for r in rows)),len(rows))
        self.assertGreaterEqual(len(set(r["photo_id"] for r in rows)),9)
        for row in rows:
            with self.subTest(row=row["gregorian"],folio=row["photo_id"]):
                converted=reference_calendar_for_date(date.fromisoformat(row["gregorian"]))
                self.assertEqual(
                    (converted["tzolkin_number"],converted["kiche_label_from_practitioner_crosswalk_only"]),
                    (row["number"],row["normalized_kiche"])
                )

    def test_1722_may_3_primary_and_1723_may_3_yearbearer_change(self):
        a=reference_calendar_for_date(date(1722,5,3))
        b=reference_calendar_for_date(date(1723,5,3))
        self.assertEqual((a["tzolkin_number"],a["kiche_label_from_practitioner_crosswalk_only"]),(9,"KEJ"))
        self.assertEqual((b["tzolkin_number"],b["kiche_label_from_practitioner_crosswalk_only"]),(10,"E"))
        self.assertEqual((a["haab_day"],a["haab_month"]),(5,"K’AYAB"))
        self.assertEqual((b["haab_day"],b["haab_month"]),(5,"K’AYAB"))
        self.assertEqual((date(1723,5,3)-date(1722,5,3)).days,365)
        self.assertEqual(
            [(r["gregorian"],r["photo_id"]) for r in DATA["observed_1722_1723_date_rows"]
             if r["gregorian"] in ["1722-05-03","1723-05-03"]],
            [("1722-05-03","body0001"),("1723-05-03","body0018")]
        )

    def test_may_june_rollover_and_source_solar_month_not_relabelled(self):
        rows={r["gregorian"]:r for r in DATA["observed_1722_1723_date_rows"]}
        self.assertEqual((rows["1722-05-31"]["number"],rows["1722-05-31"]["normalized_kiche"]), (11,"TZ’IKIN"))
        self.assertEqual((rows["1722-06-01"]["number"],rows["1722-06-01"]["normalized_kiche"]), (12,"AJMAQ"))
        old=reference_calendar_for_date(date(1722,5,3))
        forty=reference_calendar_for_date(date(1722,5,3)+timedelta(days=40))
        self.assertEqual((old["haab_day"],old["haab_month"]),(5,"K’AYAB"))
        self.assertEqual((forty["haab_day"],forty["haab_month"]),(0,"POP"))
        self.assertEqual((forty["tzolkin_number"],forty["kiche_label_from_practitioner_crosswalk_only"]),(10,"KEJ"))

    def test_1722_editorial_table_20_name_variants_mapping_only(self):
        rows=DATA["transliteration_1722_from_publisher_table"]
        self.assertEqual(len(rows),20)
        self.assertEqual(len({r["modern_kiche"] for r in rows}),20)
        self.assertEqual([r["modern_kiche"] for r in rows],list(KICHE_DAY_NAMES_BY_YUCATEC))
        self.assertTrue(all(r["editorial_1722_variant"] for r in rows))
        src=DATA["publisher_preview"]
        self.assertEqual(src["authorized_intro_pdf_page_count"],18)
        self.assertIn("not 1722 chapter pp.64-135",src["available_material"])

    def test_source_photo_13_groups_match_independent_52_step_math(self):
        rows=DATA["independently_read_5x52_group_rows"]
        self.assertEqual(len(rows),13)
        self.assertEqual((SOURCE_INTERVAL,GROUP_SIZE,GROUP_COUNT,CYCLE_DAYS),(52,5,52,260))
        for entry in rows:
            with self.subTest(group=entry["group_serial"]):
                actual=reference_1722_almanac_group(entry["group_serial"])
                self.assertEqual(
                    [(g.number,g.kiche_name) for g in actual],
                    [(entry["coefficient"], name) for name in entry["names_in_photo_read_order"]]
                )
                self.assertEqual(len(actual),5)
                self.assertFalse(entry["not_5_independent_person_predictions"] is False)

    def test_all_52_groups_cover_260_distinct_numbered_days_once(self):
        allgroups=all_reference_1722_almanac_groups()
        self.assertEqual(len(allgroups),52)
        allitems=[(d.number,d.kiche_name) for group in allgroups for d in group]
        self.assertEqual(len(allitems),260)
        self.assertEqual(len(set(allitems)),260)
        self.assertEqual(set(d.reference_position_1_based for group in allgroups for d in group),set(range(1,261)))
        counts=Counter(d.number for group in allgroups for d in group)
        self.assertEqual(counts,{i:20 for i in range(1,14)})

    def test_52_day_distance_mutant_would_not_match_source_photo(self):
        groups=DATA["independently_read_5x52_group_rows"]
        first=groups[0]
        reference=reference_1722_almanac_group(1)
        self.assertEqual([x.reference_position_1_based for x in reference],[1,53,105,157,209])
        bad=[KICHE_DAY_NAMES_BY_YUCATEC[((i*51)%20)] for i in range(5)]
        self.assertNotEqual(bad,first["names_in_photo_read_order"])

    def test_group_limits_strict_reject_bad_index_and_bool(self):
        for bad in [0,53,True,False,1.0,"1",None]:
            with self.subTest(group=str(bad)):
                with self.assertRaises(ValueError):
                    reference_1722_almanac_group(bad)

    def test_original_folio_date_and_separate_hand_not_inferred_birth_trait(self):
        x={a["id"]:a for a in DATA["manuscript"]["primary_span_observations"]}
        self.assertEqual(x["B04_EXPLICIT_DATE"]["pages"],"body0036")
        self.assertIn("6 Diciembre",x["B04_EXPLICIT_DATE"]["handwritten_short_locus"])
        self.assertEqual(x["B04_DIFFERENT_HAND"]["handwritten_short_locus"],"De otra mano")
        self.assertFalse(DATA["structural_sensitivity"]["source_content_not_frozen_natal_rule"] is False)
        self.assertEqual(DATA["status"]["source_natal_rules_added"],0)
        self.assertEqual(DATA["status"]["blind_real_human_outcomes"],0)
        self.assertEqual(DATA["status"]["production_natal_promotions"],0)

if __name__=="__main__":
    unittest.main()
