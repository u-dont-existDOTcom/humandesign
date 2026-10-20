"""Synthetic four-star source and scoring tests, never any real participant data."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

import synthetic_seal_and_score as smoke

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
MAP = B / "SOURCE_TO_BEHAVIOR_CANDIDATES_V1.json"
PKG = B / "SYNTHETIC_PRE_RESPONSE_SEAL_V1.json"
CHARTS = B / "SYNTHETIC_CHART_TOKENS_V1.json"


def sha(b):
    return sha256(b).hexdigest()


def r(p):
    return json.loads(p.read_text(encoding="utf-8"))


def load_resp(key):
    return r(B / f"SYNTHETIC_RESPONSES_{key.upper()}_CONTROL_V1.json")


class SourceVerifiedSyntheticFourAnchorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map = r(MAP)
        cls.seal = r(PKG)
        cls.charts = r(CHARTS)

    def test_01_source_index_and_source_raw_sha_exact(self):
        self.assertEqual(
            self.map["accepted_V14_index_SHA256"],
            "c3a85dd972e010398b671730d86b2eea671db3da313494807bcb42e2c209c770",
        )
        self.assertEqual(
            sha((ROOT / self.map["accepted_V14_index_path"]).read_bytes()),
            self.map["accepted_V14_index_SHA256"],
        )
        self.assertEqual(
            sha((ROOT / self.map["original_Wikitext_source_path"]).read_bytes()),
            self.map["original_Wikitext_raw_SHA256"],
        )
        self.assertEqual(self.map["original_Wikitext_oldid"], 1963110)
        self.assertEqual(self.map["human_predictive_validation_count"], 0)

    def test_02_all_four_source_quote_phrases_exact_sha_and_utf8_offset(self):
        raw = (ROOT / self.map["original_Wikitext_source_path"]).read_bytes()
        full = raw.decode("utf-8")
        sources = ["ZWD-R0287", "ZWD-R0330", "ZWD-R0464", "ZWD-R0505"]
        self.assertEqual([x["source_note_id"] for x in self.map["candidates"]], sources)
        for item in self.map["candidates"]:
            source = ROOT / item["source_line_file"]
            self.assertEqual(sha(source.read_bytes()), item["source_line_file_sha256"])
            line = next(row for row in r(source)["records"] if row["id"] == item["source_note_id"])
            anchor = item["source_original_Chinese_fragment"]
            cpos = item["source_original_fragment_codepoint_offset"]
            bpos = item["source_original_fragment_UTF8_byte_offset"]
            self.assertEqual(full[cpos : cpos + len(anchor)], anchor)
            self.assertEqual(raw[bpos : bpos + len(anchor.encode("utf-8"))], anchor.encode("utf-8"))
            self.assertEqual(sha(anchor.encode("utf-8")), item["source_original_fragment_SHA256"])
            self.assertEqual(line["source_quote_sha256_UTF8"], item["source_full_line_SHA256"])
            self.assertFalse(item["source_phrase_expert_translation_verified"])

    def test_03_concealed_behavioral_items_are_provisional_not_stars(self):
        source_terms = ("武曲", "廉贞", "天梁", "破军", "astrology", "chart", "star")
        questions = [
            item["draft_concealed_behavior_first_question"] for item in self.map["candidates"]
        ]
        self.assertEqual(len(questions), 4)
        self.assertTrue(
            all(
                not any(term.lower() in question.lower() for term in source_terms)
                for question in questions
            )
        )
        self.assertTrue(all("during the past" in text.lower() for text in questions))
        self.assertFalse(self.map["study_has_been_preregistered"])
        self.assertFalse(self.map["score_probabilities_calibrated"])
        self.assertFalse(self.map["scored_real_human_recruitment_authorized"])

    def test_04_fixture_contains_no_person_birth_data(self):
        self.assertTrue(self.charts["there_are_no_birth_dates_times_places_or_real_individuals"])
        self.assertTrue(
            all(
                set(row) == {"chart_id", "life_palace_main_star_mock", "synthetic"}
                for row in self.charts["charts"]
            )
        )
        self.assertEqual(len(self.charts["charts"]), 4)

    def test_05_seal_hash_source_and_code_shas(self):
        payload = smoke.verify_seal(self.seal)
        self.assertEqual(self.seal["sealed_payload_sha256"], smoke.digest(smoke.canon(payload)))
        self.assertEqual(payload["source_mapping_SHA256"], sha(MAP.read_bytes()))
        self.assertEqual(payload["mock_chart_fixture_SHA256"], sha(CHARTS.read_bytes()))
        self.assertEqual(payload["code_dependency_SHA256"], smoke.code_dependency_sha())
        self.assertEqual(payload["participant_birth_records_included"], 0)
        self.assertFalse(payload["source_to_human_questionnaire_mapping_is_frozen"])

    def test_06_seal_has_no_responses_or_true_birth_chart_labels(self):
        data = json.dumps(self.seal, ensure_ascii=False)
        self.assertNotIn('"mock_responses"', data)
        self.assertNotIn('"true_chart_id"', data)
        self.assertNotIn('"case_id"', data)
        self.assertNotIn('"date_of_birth"', data)
        self.assertEqual(
            self.seal["sealed_payload"]["mock_chart_ids"],
            [f"SYNTH-CHART-0{i}" for i in range(1, 5)],
        )

    def test_07_positive_toy_case_diagonal_and_reuse_metrics(self):
        out = smoke.evaluate_mock(self.seal, load_resp("aligned_positive"))
        self.assertEqual(out["human_predictive_validations"], 0)
        self.assertEqual(out["mean_diagonal_minus_no_chart_row_mean"], 0.75)
        self.assertEqual(out["HD_existing_rank_metrics_reused"]["top_1"], 1.0)
        self.assertEqual(out["HD_existing_rank_metrics_reused"]["mean_percentile"], 1.0)
        self.assertEqual(len(out["toy_response_to_chart_score_matrix"]), 4)
        self.assertFalse(out["ordinal_support_is_calibrated_probability"])

    def test_08_constant_toy_responses_yield_ties_and_no_advantage(self):
        out = smoke.evaluate_mock(self.seal, load_resp("constant_null"))
        self.assertEqual(out["mean_diagonal_minus_no_chart_row_mean"], 0.0)
        self.assertEqual(out["HD_existing_rank_metrics_reused"]["top_1"], 0.25)
        self.assertEqual(out["HD_existing_rank_metrics_reused"]["mean_percentile"], 0.5)
        self.assertEqual(out["HD_existing_seeded_label_permutation_reused"]["p_value"], 1.0)

    def test_09_adversarial_toy_answers_show_negative_control(self):
        out = smoke.evaluate_mock(self.seal, load_resp("deliberately_opposite"))
        self.assertEqual(out["mean_diagonal_minus_no_chart_row_mean"], -0.25)
        self.assertEqual(out["HD_existing_rank_metrics_reused"]["top_1"], 0.0)
        self.assertLess(out["HD_existing_rank_metrics_reused"]["mean_percentile"], 0.5)
        self.assertEqual(out["HD_existing_seeded_label_permutation_reused"]["p_value"], 1.0)

    def test_10_evaluate_results_deterministic_from_same_mock_inputs(self):
        results = [smoke.evaluate_mock(self.seal, load_resp("aligned_positive")) for _ in range(2)]
        self.assertEqual(results[0], results[1])
        self.assertEqual(results[0]["HD_existing_seeded_label_permutation_reused"]["seed"], 190526)

    def test_11_sealed_payload_mutation_rejected(self):
        edited = copy.deepcopy(self.seal)
        edited["sealed_payload"]["score_policy"] = "INVENTED_CALIBRATION"
        with self.assertRaisesRegex(ValueError, "payload SHA"):
            smoke.verify_seal(edited)

    def test_12_wrong_mapping_sha_rejected_even_if_seal_self_rehashed(self):
        changed = copy.deepcopy(self.seal)
        changed["sealed_payload"]["source_mapping_SHA256"] = "0" * 64
        changed["sealed_payload_sha256"] = smoke.digest(smoke.canon(changed["sealed_payload"]))
        with self.assertRaisesRegex(ValueError, "source mapping"):
            smoke.verify_seal(changed)

    def test_13_source_question_wording_change_after_seal_rejected(self):
        tampered = copy.deepcopy(self.map)
        tampered["candidates"][0]["draft_concealed_behavior_first_question"] = "Changed"
        with tempfile.TemporaryDirectory() as temp:
            fake = Path(temp) / "source_map.json"
            fake.write_text(json.dumps(tampered, ensure_ascii=False) + "\n")
            with (
                patch.object(smoke, "MAP", fake),
                self.assertRaisesRegex(ValueError, "source mapping"),
            ):
                smoke.verify_seal(self.seal)

    def test_14_fake_chart_cannot_contain_real_birth_attributes(self):
        invalid = copy.deepcopy(self.charts)
        invalid["charts"][0]["dob"] = "1980-01-01"
        with tempfile.TemporaryDirectory() as temp:
            fp = Path(temp) / "mock.json"
            fp.write_text(json.dumps(invalid, ensure_ascii=False) + "\n")
            with (
                patch.object(smoke, "CHARTS", fp),
                self.assertRaisesRegex(ValueError, "invalid fake chart"),
            ):
                smoke.synthetic_charts()

    def test_15_mock_response_cannot_include_person_birth_attributes(self):
        data = load_resp("aligned_positive")
        data["cases"][0]["birth_place"] = "Any city"
        with self.assertRaisesRegex(ValueError, "case unexpectedly"):
            smoke.evaluate_mock(self.seal, data)

    def test_16_missing_or_extra_response_rejected_not_imputed(self):
        data = load_resp("aligned_positive")
        data["cases"][0]["mock_responses"].pop("Q_DECISIVE")
        with self.assertRaisesRegex(ValueError, "mock response missing"):
            smoke.evaluate_mock(self.seal, data)

    def test_17_float_or_out_of_range_response_rejected(self):
        for fake_val in (2.0, 5, -1, "2", True):
            data = load_resp("aligned_positive")
            data["cases"][0]["mock_responses"]["Q_DECISIVE"] = fake_val
            with (
                self.subTest(value=str(fake_val)),
                self.assertRaisesRegex(ValueError, "mock response missing"),
            ):
                smoke.evaluate_mock(self.seal, data)

    def test_18_duplicate_true_chart_or_duplicate_case_rejected(self):
        first = load_resp("aligned_positive")
        first["cases"][0]["true_chart_id"] = first["cases"][1]["true_chart_id"]
        with self.assertRaisesRegex(ValueError, "nonunique fake case"):
            smoke.evaluate_mock(self.seal, first)
        second = load_resp("aligned_positive")
        second["cases"][0]["case_id"] = second["cases"][1]["case_id"]
        with self.assertRaisesRegex(ValueError, "nonunique fake case"):
            smoke.evaluate_mock(self.seal, second)

    def test_19_non_synthetic_case_or_source_status_fails_closed(self):
        bad = load_resp("aligned_positive")
        bad["cases"][0]["synthetic_case"] = False
        with self.assertRaisesRegex(ValueError, "nonunique fake case"):
            smoke.evaluate_mock(self.seal, bad)
        bad2 = copy.deepcopy(self.map)
        bad2["scored_real_human_recruitment_authorized"] = True
        with tempfile.TemporaryDirectory() as temp:
            f = Path(temp) / "bad.json"
            f.write_text(json.dumps(bad2, ensure_ascii=False) + "\n")
            with (
                patch.object(smoke, "MAP", f),
                self.assertRaisesRegex(ValueError, "source map must be provisional"),
            ):
                smoke.source_mapping()

    def test_20_readiness_gates_remain_blocked_after_synthetic_simulation(self):
        p = ROOT / "tasks/astro-blind-readiness-20261020/READINESS_GATES_V1.json"
        d = r(p)
        self.assertEqual(len(d["candidate_pilot_gates"]), 10)
        self.assertTrue(all(g["blocking"] for g in d["candidate_pilot_gates"]))
        self.assertFalse(d["pilot_eligibility"]["candidate_pilot_ready"])
        for scenario in ("POSITIVE", "NULL", "OPPOSITE"):
            out = r(B / f"SYNTHETIC_RESULT_{scenario}_CONTROL_V1.json")
            self.assertFalse(out["source_model_candidate_is_frozen_for_humans"])
            self.assertFalse(out["nonastrological_external_baseline_tested"])
            self.assertEqual(out["human_predictive_validations"], 0)


if __name__ == "__main__":
    unittest.main()
