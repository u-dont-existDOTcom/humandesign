#!/usr/bin/env python3
"""Known-answer synthetic execution test; explicitly NOT blinded human evidence."""
import argparse
import importlib.util
from pathlib import Path
import tempfile

import compare


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = args.out.resolve()
    root.mkdir(parents=True, exist_ok=False)
    spec = importlib.util.spec_from_file_location("fixtures", Path(__file__).parent / "tests/test_compare.py")
    fixtures = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixtures)
    keys = fixtures.fixture(root)
    compare.freeze(root / "charts.json", root / "config.json", root / "freeze.json")
    compare.score(root / "freeze.json", root / "charts.json", root / "config.json", root / "responses.json", root / "matrix.json")
    compare.save_new(root / "matrix-seal.json", {"matrix_sha256": compare.sha(root / "matrix.json")})
    # Synthetic evaluator key is held outside the repository and removed afterward.
    # This operator knows the fixture; no access-isolation/blinding claim is made.
    with tempfile.TemporaryDirectory(prefix="mastro-engineering-custodian-") as temp:
        key = Path(temp) / "synthetic-key.json"
        compare.save_new(key, keys)
        compare.evaluate(root / "freeze.json", root / "matrix.json", root / "matrix-seal.json", key,
                         Path(__file__).resolve().parents[2], root / "evaluation.json")
    result = compare.load(root / "evaluation.json")
    assert result["status"] == "engineering_only"
    assert result["primary_contrast"] == 1.0
    assert all(r["unique_top1"] for r in result["true_chart_ranks_secondary"])
    print("PASS: 4 constructed cases x 16 artificial chart vectors, 999 seeded permutations.")
    print("Engineering only. No Mastro-derived behavioral or human-validity claim.")


if __name__ == "__main__":
    main()
