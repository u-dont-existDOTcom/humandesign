"""Audit domain-level partner rankings against user-reported relationship phenotypes.

This development audit intentionally scores pairwise ordinal claims rather than a
single compatibility scalar. Unknown observed comparisons are omitted. Predicted
ties receive 0.5 credit only when the observed criterion also declares a tie;
otherwise a tie does not satisfy a directional observed claim.

The current three-pair files are development data. This script is reusable for
future frozen prediction snapshots and independently collected phenotype files.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rank_map(tiers: list[list[str]]) -> dict[str, int]:
    ranks: dict[str, int] = {}
    for rank, tier in enumerate(tiers):
        for case_id in tier:
            if case_id in ranks:
                raise ValueError(f"duplicate case in prediction tiers: {case_id}")
            ranks[case_id] = rank
    return ranks


def audit(phenotype: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
    constraints = phenotype["observed_pairwise_constraints"]
    prediction_tiers = prediction["prediction_tiers"]
    by_domain: dict[str, dict[str, float | int]] = defaultdict(
        lambda: {"correct": 0, "incorrect": 0, "ties_against_direction": 0, "total": 0}
    )
    details: list[dict[str, Any]] = []

    for item in constraints:
        domain = item["domain"]
        higher = item["higher"]
        lower = item["lower"]
        if domain not in prediction_tiers:
            details.append(
                {
                    "domain": domain,
                    "higher": higher,
                    "lower": lower,
                    "result": "unscored_missing_prediction",
                }
            )
            continue

        ranks = _rank_map(prediction_tiers[domain])
        if higher not in ranks or lower not in ranks:
            details.append(
                {
                    "domain": domain,
                    "higher": higher,
                    "lower": lower,
                    "result": "unscored_missing_case",
                }
            )
            continue

        by_domain[domain]["total"] += 1
        if ranks[higher] < ranks[lower]:
            by_domain[domain]["correct"] += 1
            result = "correct"
        elif ranks[higher] > ranks[lower]:
            by_domain[domain]["incorrect"] += 1
            result = "incorrect"
        else:
            by_domain[domain]["ties_against_direction"] += 1
            result = "predicted_tie_observed_direction"

        details.append(
            {
                "domain": domain,
                "higher": higher,
                "lower": lower,
                "observed_confidence": item.get("confidence"),
                "predicted_rank_higher": ranks[higher],
                "predicted_rank_lower": ranks[lower],
                "result": result,
            }
        )

    total = sum(int(v["total"]) for v in by_domain.values())
    correct = sum(int(v["correct"]) for v in by_domain.values())
    incorrect = sum(int(v["incorrect"]) for v in by_domain.values())
    ties = sum(int(v["ties_against_direction"]) for v in by_domain.values())

    summary_domains: dict[str, Any] = {}
    for domain, counts in sorted(by_domain.items()):
        n = int(counts["total"])
        c = int(counts["correct"])
        summary_domains[domain] = {
            **counts,
            "accuracy": c / n if n else None,
        }

    return {
        "audit_version": "relationship-pairwise-audit-v1",
        "criterion_version": phenotype.get("version"),
        "prediction_version": prediction.get("version"),
        "status": "development_descriptive_not_validation",
        "overall": {
            "correct": correct,
            "incorrect": incorrect,
            "ties_against_direction": ties,
            "total": total,
            "pairwise_accuracy": correct / total if total else None,
            "binary_ordering_reference": 0.5,
            "interpretation": (
                "Descriptive only. Small-N comparisons are not an inferential test; "
                "the 0.5 reference is the chance expectation for a forced binary ordering."
            ),
        },
        "by_domain": summary_domains,
        "details": details,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phenotype", type=Path)
    parser.add_argument("prediction", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = audit(_load(args.phenotype), _load(args.prediction))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
