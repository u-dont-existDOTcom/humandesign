"""Source-only regression and synthetic reviewer counterexamples; no owner fit."""
from copy import deepcopy
from datetime import date
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ref = module("source_reference", "scripts/numerology_book_reference.py")
protocol = module("protocol_checks", "scripts/numerology_audit_protocol_checks.py")
CONTRACT = json.loads((ROOT / protocol.BASE / "empirical_admission_contract.json").read_text())


class SourceErrata(unittest.TestCase):
    def test_doyle_pinnacle_is_not_adjacent_reality(self):
        self.assertEqual([v["root"] for v in ref.pinnacles(3, 6, 1932, ref.JORDAN)], [9, 3, 3, 9])
        self.assertEqual(ref.challenges(3, 6, 1932, ref.JORDAN), [3, 0, 3, 3])
        self.assertEqual(ref.root(5 + 6), 2)
        self.assertNotEqual(ref.pinnacles(3, 6, 1932, ref.JORDAN)[3]["root"], ref.root(5 + 6))

    def test_campbell_eva_ordinal_branch_not_global_tape_shift(self):
        a = ref.tape(["EVA", "AMY", "DOWNS"], 18, ref.CAMPBELL)
        b = ref.tape(["EVA", "AMY", "DOWNS"], 19, ref.CAMPBELL)
        self.assertEqual(a["active"], ["V", "Y", "N"])
        self.assertEqual(a["essence"]["root"], 7)
        self.assertEqual(b["active"], ["A", "Y", "N"])
        self.assertEqual(b["essence"]["root"], 4)

    def test_race_consciousness_has_five_odd_then_four_even(self):
        for start in (0, 18, 27, 54):
            values = [ref.jordan_race_consciousness(i) for i in range(start, start + 9)]
            self.assertEqual([v % 2 for v in values], [1] * 5 + [0] * 4)

    def test_jordan_boundary_example_separates_1961_from_1962(self):
        self.assertEqual(ref.calendar_number(3, 7, 1961, ref.JORDAN)["root"], 9)
        self.assertEqual(ref.calendar_number(3, 7, 1962, ref.JORDAN)["root"], 1)
        self.assertEqual(ref.pinnacle_marks(5, ref.JORDAN), [31, 40, 49])

    def test_cayce_power_number_is_not_power_phase_square(self):
        self.assertEqual(45 + 44, 89)
        self.assertEqual(ref.digit_sum(89), 17)
        self.assertEqual(ref.root(89), 8)
        self.assertEqual(sorted([45 + ref.root(42), 54 - ref.root(42)]), [48, 51])
        # The blueprint's odd/even minor/major rules are already tested in the
        # frozen Cayce fixtures. Do not infer its age rule from a square label.
        self.assertNotEqual(ref.root(89), ref.root(42))

    def test_mandatory_effective_erratum_binding(self):
        self.assertEqual(protocol.validate_effective_overlay(ROOT), [])


class ReviewedDesignCounterexamples(unittest.TestCase):
    def cell(self, key, y, pred, complete=True):
        return {"key": key, "outcome": y, "decision": pred, "observation_complete": complete}

    def test_equal_cost_not_two_to_one_miss_reward(self):
        positive = [self.cell(str(i), int(i < 4), 1) for i in range(10)]
        negative = [self.cell(str(i), int(i < 4), 0) for i in range(10)]
        a, b = protocol.compare_primary_cells(positive, negative)
        self.assertEqual((a["error"], b["error"]), (0.6, 0.4))
        self.assertEqual((a["utility"], b["utility"]), (-6, -4))
        self.assertGreater(b["symmetric_score"], a["symmetric_score"])

    def test_each_fp_and_each_fn_has_identical_cost(self):
        fp = protocol.primary_cell_score([self.cell("a", 0, 1)])
        fn = protocol.primary_cell_score([self.cell("a", 1, 0)])
        self.assertEqual((fp["error"], fp["utility"]), (fn["error"], fn["utility"]))

    def test_recalled_events_in_incomplete_windows_are_not_free_hits(self):
        rows = [self.cell(str(i), 1 if i < 2 else None, 1, False) for i in range(12)]
        with self.assertRaises(ValueError):
            protocol.primary_cell_score(rows)
        rows += [self.cell("complete", 0, 1)]
        result = protocol.primary_cell_score(rows)
        self.assertEqual((result["TP"], result["FP"], result["N_eligible"]), (0, 1, 1))
        self.assertEqual(result["unassessed_cells"], 12)

    def test_all_abstain_is_not_zero_error(self):
        with self.assertRaises(ValueError):
            protocol.primary_cell_score([self.cell("a", 1, None)])

    def test_silence_is_not_implicitly_negative(self):
        row = self.cell("a", 0, 0)
        del row["decision"]
        with self.assertRaises(ValueError):
            protocol.primary_cell_score([row])

    def test_equal_percentage_on_different_cells_is_not_matched_coverage(self):
        with self.assertRaises(ValueError):
            protocol.compare_primary_cells([self.cell("a", 1, 1)], [self.cell("b", 1, 1)])

    def test_one_favorable_anchor_is_insufficient(self):
        self.assertFalse(protocol.both_timing_anchors_pass(True, False))
        self.assertFalse(protocol.both_timing_anchors_pass(False, True))
        self.assertTrue(protocol.both_timing_anchors_pass(True, True))

    def test_grid_boundary_artifact_is_exposed_not_silently_selected(self):
        # Equal-duration calendar and birthday intervals can touch different
        # counts of calendar cells; this is why both anchors are required.
        calendar = (date(1975, 1, 1), date(1976, 1, 1))
        birthday = (date(1975, 11, 12), date(1976, 11, 12))
        from datetime import timedelta
        count = lambda interval: (interval[1] - timedelta(days=1)).year - interval[0].year + 1
        self.assertEqual(count(calendar), 1)
        self.assertEqual(count(birthday), 2)
        self.assertFalse(protocol.both_timing_anchors_pass(count(calendar) < count(birthday), False))

    def test_duplicate_endpoint_credit_rejected(self):
        with self.assertRaises(ValueError):
            protocol.primary_cell_score([self.cell("a", 1, 1), self.cell("a", 1, 1)])

    def test_actual_reconciled_contract(self):
        self.assertEqual(protocol.validate_reconciled_contract(CONTRACT), [])

    def test_asymmetric_hybrid_scope_rejected(self):
        mutated = deepcopy(CONTRACT)
        mutated["constraints"]["horoscope_adapter_required_for"] = ["CAMPBELL_YOUR_DAYS_V1"]
        self.assertTrue(protocol.validate_reconciled_contract(mutated))

    def test_owner_aware_report_cannot_enter_reader_packet(self):
        mutated = deepcopy(CONTRACT)
        mutated["constraints"]["owner_aware_audit_documents_allowed_in_reader_context"] = True
        self.assertTrue(protocol.validate_reconciled_contract(mutated))


if __name__ == "__main__":
    unittest.main()
