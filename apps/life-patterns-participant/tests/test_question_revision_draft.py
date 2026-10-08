"""Conservative prospective rewrites, never retroactive mutation of frozen questions."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / "apps/life-patterns-participant/participant/static/tendency-first-v1.json"
NEW = ROOT / "tasks/question-feedback-loop-20261008/tendency-first-v2-development.json"


def test_prospective_revision_changes_nine_question_texts_without_losing_routes():
    previous = json.loads(OLD.read_text())
    proposed = json.loads(NEW.read_text())
    assert proposed["version"] != previous["version"]
    assert proposed["status"].startswith("prospective_wording_candidate_NOT_DEPLOYED")
    old_routes = {item["id"]: item for item in previous["questions"]}
    new_routes = {item["id"]: item for item in proposed["questions"]}
    assert set(old_routes) == set(new_routes)
    changed = {
        route
        for route in old_routes
        if old_routes[route]["question"] != new_routes[route]["question"]
    }
    assert changed == {
        "TF1-G10",
        "TF1-D0",
        "TF1-M11",
        "TF1-G15",
        "TF1-STATUS",
        "TF1-G04",
        "TF1-M03",
        "TF1-ROUTINE-CHANGE",
        "TF1-G17",
    }
    for route in changed:
        assert new_routes[route]["source_route_id"] == old_routes[route]["source_route_id"]
        assert new_routes[route]["interpretation_limit"].startswith(
            old_routes[route]["interpretation_limit"]
        )
        assert "development_revision_rationale" in new_routes[route]
        assert new_routes[route]["question"].endswith("?")
    assert set(previous["retired_from_new_elicitation"]).issubset(
        set(proposed["retired_from_new_elicitation"])
    )
    assert {"ROMANCE-FADE", "ROOM-EFFECT", "CORRECTION-REASON"} <= set(
        proposed["retired_from_new_elicitation"]
    )


def test_live_policy_remains_pinned_to_unchanged_v1_source():
    from participant.question_policy import VERSION, identity

    assert VERSION == "tendency-first-v1-20261006"
    assert identity()["version"] == VERSION
    assert "prospective" not in OLD.read_text().lower()
    assert "prospective_wording_candidate" in NEW.read_text()


def test_feedback_packaged_instructions_preserve_source_separate_from_traits():
    instructions = (ROOT / "reference/custom_gpt/life_patterns_voice_interviewer_v2.md").read_text()
    guide = (ROOT / "reference/custom_gpt/ACTION-HANDOFF-GUIDE-v1.md").read_text()
    assert "turn's `process_feedback`" in instructions
    assert "not as trait evidence" in instructions
    assert "no additional approval card" in guide or "no separate transmission" in guide
    assert "question-design objections" in guide.lower()
    assert "researcher admin" in guide
    assert "consent" in guide
    assert len(instructions) + instructions.count("\n") <= 8000
