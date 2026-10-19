"""Naibod original 1647 tables: recorded readings, ambiguities, immutable parents."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
P = B.parent
ROOT = B.parents[3]


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class NaibodSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = j(P / "B07x/NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json")
        cls.cmp = j(P / "B07x/NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json")
        cls.data = j(B / "ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.deg = {
            r["source_equatorial_degrees"]: r for r in cls.data["rows"] if r["kind"] == "degree"
        }
        cls.minute = {
            r["source_equatorial_arcminutes_printed_label"]: r
            for r in cls.data["rows"]
            if r["kind"] == "minute"
        }

    def test_four_original_edition_photo_sha_bytes(self):
        for rec in self.data["source_image_witnesses_first_and_second_editions"].values():
            p = ROOT / rec["path"]
            self.assertEqual(sha(p), rec["sha256"])
            self.assertEqual(p.stat().st_size, rec["bytes"])

    def test_rows_cover_actual_printed_labels_only(self):
        self.assertEqual(set(self.deg), set(range(1, 91)))
        self.assertEqual(set(self.minute), set(range(1, 61)) - {27})
        self.assertEqual(len(self.data["rows"]), 149)

    def test_printed_rollover_preserved(self):
        self.assertEqual(
            [
                self.deg[69]["literal_1647_one_reader_years"],
                self.deg[69]["literal_1647_one_reader_days"],
                self.deg[69]["literal_1647_one_reader_hours"],
            ],
            [70, 4, 3],
        )
        self.assertEqual(self.deg[80]["literal_1647_one_reader_hours"], 24)
        self.assertEqual(self.deg[90]["literal_1647_one_reader_years"], 91)

    def test_minute_one_1647_uncertain(self):
        self.assertIsNone(self.minute[1]["literal_1647_one_reader_days"])
        self.assertEqual(self.minute[1]["1647_first_minute_day_glyph_options"], [5, 6])

    def test_distinct_edition_minute44(self):
        self.assertEqual(self.minute[44]["literal_1647_one_reader_hours"], 8)
        c = [r for r in self.cmp["comparisons"] if r["kind"] == "minute" and r["row"] == 44]
        self.assertEqual(c[0]["1659"], [271, 18])

    def test_printed_minute8_and_60(self):
        self.assertEqual(
            [
                self.minute[8]["literal_1647_one_reader_days"],
                self.minute[8]["literal_1647_one_reader_hours"],
            ],
            [44, 10],
        )
        self.assertEqual(
            [
                self.minute[60]["literal_1647_one_reader_days"],
                self.minute[60]["literal_1647_one_reader_hours"],
            ],
            [374, 14],
        )

    def test_original_naibod_worked_lookup(self):
        self.assertEqual(
            [
                self.deg[11]["literal_1647_one_reader_years"],
                self.deg[11]["literal_1647_one_reader_days"],
                self.deg[11]["literal_1647_one_reader_hours"],
            ],
            [11, 58, 21],
        )
        self.assertEqual(
            [
                self.minute[55]["literal_1647_one_reader_days"],
                self.minute[55]["literal_1647_one_reader_hours"],
            ],
            [339, 17],
        )

    def test_prior_b07x_source_hash_preserved(self):
        self.assertEqual(
            self.data["previous_1647_source_table_SHA256"],
            sha(P / "B07x/NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json"),
        )
        self.assertEqual(
            self.data["previous_1647_1659_comparison_SHA256"],
            sha(P / "B07x/NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json"),
        )

    def test_exact_nonduplicative_21_source_rules(self):
        self.assertEqual(
            [x["record_number"] for x in self.rules["rules"]], list(range(12547, 12568))
        )
        self.assertFalse(self.rules["full_first_CLXVI_source_chapter_complete"])

    def test_chinese_western_counts_still_old(self):
        self.assertEqual(
            j(
                ROOT
                / "tasks/astro-source-audit-multipass-20261005"
                / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
            )["records_count"],
            12546,
        )
        self.assertEqual(
            j(
                ROOT
                / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
            )["sum_source_annotations"],
            262,
        )

    def test_not_approved_timing_engine(self):
        self.assertFalse(self.data["original_natal_time_calculator_approved"])
        self.assertFalse(self.data["second_edition_all_149_source_cells_expert_collated"])
        self.assertEqual(self.data["human_prediction_validations"], 0)
        self.assertEqual(self.data["runtime_promotions"], 0)


def degree_test(i):
    def test(self):
        a = self.deg[i]
        b = self.src["degree_rows"][i - 1]
        self.assertEqual(
            [
                a["literal_1647_one_reader_years"],
                a["literal_1647_one_reader_days"],
                a["literal_1647_one_reader_hours"],
            ],
            [b["printed_1647_years"], b["printed_1647_days"], b["printed_1647_hours"]],
        )
        self.assertFalse(a["runtime_promoted"])

    return test


def minute_test(i):
    def test(self):
        a = self.minute[i]
        b = next(r for r in self.src["minute_rows"] if r["equatorial_arcminutes_as_printed"] == i)
        self.assertEqual(a["literal_1647_one_reader_days"], None if i == 1 else b["secondary_days"])
        self.assertEqual(a["literal_1647_one_reader_hours"], b["secondary_hours"])
        self.assertEqual(
            a["1647_first_minute_day_glyph_options"], b["original_photo_day_ambiguity"]
        )
        self.assertFalse(a["runtime_promoted"])

    return test


for i in range(1, 91):
    setattr(NaibodSource, f"test_degree_{i:02d}", degree_test(i))
for i in range(1, 61):
    if i != 27:
        setattr(NaibodSource, f"test_minute_{i:02d}", minute_test(i))


if __name__ == "__main__":
    unittest.main()
