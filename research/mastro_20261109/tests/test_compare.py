import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "compare.py"
spec = importlib.util.spec_from_file_location("compare", MODULE)
compare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compare)


def fixture(root):
    charts, keys, responses = [], [], []
    for i, hemisphere in enumerate(("N", "N", "S", "S")):
        arms = {}
        for j, arm in enumerate(compare.ARMS):
            cid = f"C{i * 4 + j:03}"
            arms[arm] = cid
            # Deliberately constructed synthetic pattern, not a Mastro output.
            match = (arm == "standard" and hemisphere == "N") or (arm == "inverted" and hemisphere == "S")
            charts.append({"chart_id": cid, "keywords": [{"word": f"trait{i}", "weight": 4 if match else 1}]})
        keys.append({"response_id": f"R{i}", "hemisphere": hemisphere, "arms": arms})
        responses.append({"response_id": f"R{i}", "words": [f"trait{i}"]})
    for name, value in (("charts.json", charts), ("responses.json", responses)):
        (root / name).write_bytes(compare.canonical(value))
    config = {"seed": 20261109, "permutations": 999, "n_north": 2, "n_south": 2,
              "status": "engineering_only", "custody_attestation": "not_blind_synthetic_fixture",
              **{k: "0" * 64 for k in ("engine_sha256", "settings_sha256", "birth_inputs_sha256", "measurement_protocol_sha256")}}
    (root / "config.json").write_bytes(compare.canonical(config))
    return keys


class ComparisonTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.keys = fixture(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def freeze_and_score(self):
        r = self.root
        compare.freeze(r / "charts.json", r / "config.json", r / "freeze.json")
        compare.score(r / "freeze.json", r / "charts.json", r / "config.json", r / "responses.json", r / "matrix.json")
        compare.save_new(r / "seal.json", {"matrix_sha256": compare.sha(r / "matrix.json")})
        compare.save_new(r / "custodian.json", self.keys)

    def evaluate(self, output="evaluation.json"):
        r = self.root
        compare.evaluate(r / "freeze.json", r / "matrix.json", r / "seal.json", r / "custodian.json", MODULE.parents[2], r / output)

    def test_literal_denominator_and_duplicates(self):
        self.assertEqual(compare.literal_score(["Calm", "calm", " calm"], [
            {"word": "calm", "weight": 3}, {"word": "calm", "weight": 10},
            {"word": "bold", "weight": 2}]), 2)

    def test_full_pipeline_and_seed_replay(self):
        self.freeze_and_score()
        self.evaluate()
        self.evaluate("replay.json")
        a, b = compare.load(self.root / "evaluation.json"), compare.load(self.root / "replay.json")
        a.pop("created_at_utc"); b.pop("created_at_utc")
        self.assertEqual(a, b)
        self.assertEqual(a["primary_contrast"], 1)
        self.assertTrue(all(x["unique_top1"] for x in a["true_chart_ranks_secondary"]))
        self.assertEqual(a["status"], "engineering_only")

    def test_changed_charts_rejected(self):
        r = self.root
        compare.freeze(r / "charts.json", r / "config.json", r / "freeze.json")
        (r / "charts.json").write_text("[]")
        with self.assertRaisesRegex(ValueError, "changed"):
            compare.score(r / "freeze.json", r / "charts.json", r / "config.json", r / "responses.json", r / "matrix.json")

    def test_matrix_tampering_rejected_before_missing_key(self):
        self.freeze_and_score()
        (self.root / "matrix.json").write_text("{}")
        (self.root / "custodian.json").unlink()
        with self.assertRaisesRegex(ValueError, "seal mismatch"):
            self.evaluate()

    def test_key_inside_decoder_rejected(self):
        self.freeze_and_score()
        r = self.root
        with self.assertRaisesRegex(ValueError, "outside"):
            compare.evaluate(r / "freeze.json", r / "matrix.json", r / "seal.json", r / "custodian.json", r, r / "no.json")

    def test_duplicate_chart_assignment_rejected(self):
        self.freeze_and_score()
        self.keys[0]["arms"]["inverted"] = self.keys[0]["arms"]["standard"]
        (self.root / "custodian.json").write_bytes(compare.canonical(self.keys))
        with self.assertRaisesRegex(ValueError, "partition"):
            self.evaluate()

    def test_ties_are_retained(self):
        r = self.root
        charts = compare.load(r / "charts.json")
        for c in charts:
            c["keywords"] = [{"word": "shared", "weight": 1}]
        (r / "charts.json").write_bytes(compare.canonical(charts))
        self.freeze_and_score()
        self.evaluate()
        result = compare.load(r / "evaluation.json")
        self.assertEqual(result["primary_contrast"], 0)
        self.assertEqual(result["primary_upper_tail_p_plus_one"], 1)
        self.assertEqual(result["by_hemisphere"]["N"]["ties"], 2)
        self.assertEqual(result["true_chart_ranks_secondary"][0]["rank_worst"], 2)

    def test_freeze_does_not_overwrite(self):
        self.freeze_and_score()
        r = self.root
        with self.assertRaises(FileExistsError):
            compare.freeze(r / "charts.json", r / "config.json", r / "freeze.json")

    def test_human_custody_required(self):
        r = self.root
        config = compare.load(r / "config.json")
        config["status"] = "preregistered_human"
        (r / "config.json").write_bytes(compare.canonical(config))
        with self.assertRaisesRegex(ValueError, "custody"):
            compare.freeze(r / "charts.json", r / "config.json", r / "freeze.json")


if __name__ == "__main__":
    unittest.main()
