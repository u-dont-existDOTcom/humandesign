"""Synthetic only; validates lineage dependence and opposite-outcome handling."""
import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "scripts" / "audit_astrology_cross_system_consensus_v1.py"
spec = importlib.util.spec_from_file_location("astro_audit", PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def row(ident, system, preference, facts, sources):
    return {"testimony_id": ident, "system_id": system, "preferred_outcome": preference,
            "source_locator": f"example::{ident}", "signal_keys": facts,
            "source_lineage_keys": sources}


def packet(*rows):
    return {"schema":mod.SCHEMA,"study_id":"synthetic-fixture-20261020",
            "claims":[{"claim_id":"Q1", "outcomes":["A","B"],"testimonies":list(rows)}]}


class ConsensusTests(unittest.TestCase):
    def test_three_books_same_tradition_only_one_vote(self):
        p=packet(row("1","Jyotish","A",["mercury-position"],["BPHS"]),
                 row("2","Jyotish","A",["venus-position"],["Saravali"]),
                 row("3","Jyotish","A",["moon-position"],["JatakaParijata"]))
        r=mod.audit(p)["claims"][0]
        self.assertEqual(r["symbolic_consensus_strength"], 1)
        self.assertEqual(r["raw_testimony_count"], 3)

    def test_same_underlying_planet_not_three_independent_votes(self):
        p=packet(row("1","Lilly","A",["planet-mercury"],["A"]),
                 row("2","Jyotish","A",["planet-mercury"],["B"]),
                 row("3","Hellenistic","A",["planet-mercury"],["C"]))
        r=mod.audit(p)["claims"][0]
        self.assertEqual(r["symbolic_consensus_strength"], 1)
        self.assertEqual(len(r["lineage_distinct_groups"]), 1)

    def test_two_different_signals_across_traditions_can_converge(self):
        p=packet(row("1","Western","A",["mars-geometry"],["Lilly"]),
                 row("2","BaZi","A",["different-day-master"],["DiTianSui"]))
        r=mod.audit(p)["claims"][0]
        self.assertEqual(r["symbolic_consensus_strength"], 2)
        self.assertIsNone(r["empirical_probability_or_validated_weight"])

    def test_same_source_lineage_does_not_duplicate(self):
        p=packet(row("1","Lilly","A",["mars"],["borrowed-tradition-passage"]),
                 row("2","Jyotish","A",["earthly-cycle"],["borrowed-tradition-passage"]))
        self.assertEqual(mod.audit(p)["claims"][0]["symbolic_consensus_strength"], 1)

    def test_opposite_alternatives_within_one_system_abstain(self):
        p=packet(row("1","Western","A",["mars"],["x"]),
                 row("2","Western","B",["saturn"],["y"]))
        r=mod.audit(p)["claims"][0]
        self.assertEqual(r["system_votes"][0]["status"], "CONFLICTED")
        self.assertIsNone(r["symbolic_consensus_option"])

    def test_opposite_traditions_cannot_be_selected_after_outcome(self):
        p=packet(row("1","Western","A",["venus"],["x"]),
                 row("2","BaZi","B",["stem"],["y"]))
        r=mod.audit(p)["claims"][0]
        self.assertIsNone(r["symbolic_consensus_option"])
        self.assertEqual(r["lineage_distinct_support_by_outcome"],{"A":1,"B":1})

    def test_dependency_conflict_is_explicit_and_not_retrodicted(self):
        p=packet(row("1","Western","A",["venus"],["x"]),
                 row("2","Jyotish","B",["venus"],["y"]),
                 row("3","BaZi","A",["stem"],["z"]))
        r=mod.audit(p)["claims"][0]
        self.assertEqual(r["conflicted_lineage_groups"], 1)
        self.assertIsNone(r["symbolic_consensus_option"])

    def test_missing_lineage_rejected(self):
        p=packet(row("1","Western","A",["venus"],["x"]))
        p["claims"][0]["testimonies"][0]["source_lineage_keys"] = []
        with self.assertRaisesRegex(ValueError,"lineage"):
            mod.audit(p)

    def test_neutral_does_not_vote(self):
        p=packet(row("1","Western",None,["venus"],["x"]))
        r=mod.audit(p)["claims"][0]
        self.assertEqual(r["system_votes"][0]["status"], "ABSTAIN")
        self.assertEqual(r["symbolic_consensus_strength"],0)

    def test_fake_probability_never_returned(self):
        p=packet(row("1","Western","A",["venus"],["x"]))
        r=mod.audit(p)
        self.assertIsNone(r["independent_human_predictive_success"])
        self.assertIsNone(r["claims"][0]["empirical_probability_or_validated_weight"])


if __name__ == "__main__":
    unittest.main()