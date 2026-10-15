"""Synthetic structural regression for Life Patterns guided-context exports."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tasks/life-patterns-guided-eight-assessment-20261015/verify_private_context_export.py"
spec = importlib.util.spec_from_file_location("review_context_export", SOURCE)
assert spec and spec.loader
reviewer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reviewer)


def test_synthetic_roundtrip():
    targets = reviewer.TARGET_ROUTES
    routes = list(targets) + [f"EXTRA{i}" for i in range(17)]
    previous = {
        "schema": "local_life_patterns_v3_pilot_unsubmitted",
        "answers": {
            route: {
                "selected": ["Sample one"],
                "other": "Synthetic response not for publication",
                "unsure": False,
                "skip": False,
            }
            for route in routes
        },
        "unique_behaviors": [{"behavior": "Synthetic anonymous habit"}],
    }
    updated = {
        "schema": previous["schema"],
        "answers": {k: dict(v) for k, v in previous["answers"].items()},
        "unique_behaviors": [dict(x) for x in previous["unique_behaviors"]],
    }
    for route in targets:
        updated["answers"][route]["context_rule"] = "If there is time, research before testing."
        updated["answers"][route]["recent_case"] = "A synthetic example."
        updated["answers"][route]["no_stable_default"] = False
        updated["answers"][route]["context_skipped"] = False
    result = reviewer.review(previous, updated)
    assert result["question_routes_preserved"] == 25
    assert result["completed_target_count"] == 8
    assert result["conditional_rule_count"] == 8
    assert result["concrete_example_count"] == 8
    assert result["private_content_in_output"] is False
    assert result["birth_chart_predictions_tested"] == 0
    assert "Synthetic response not for publication" not in str(result)
