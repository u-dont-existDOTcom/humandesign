"""Global-vs-batch progress and unknown-future regression tests."""

from __future__ import annotations

import json
from pathlib import Path

from participant.review_timing import clarification_progress, review_guidance

ROOT = Path(__file__).resolve().parents[3]
ACTION = ROOT / "apps/life-patterns-participant/participant/static/action-openapi.yaml"


def case(status: str, *, pending: int = 0, answered: int = 0) -> dict:
    return {
        "status": status,
        "review_protocol": "fast-batch-v1",
        "review_stage": "reconciliation" if answered else "initial_triage",
        "pending_clarifications": [{"route_id": f"Q{i}"} for i in range(pending)],
        "clarification_history": [
            {"answer_status": "skipped" if i % 2 else "answered"} for i in range(answered)
        ],
        "round": answered,
    }


def test_one_of_one_batch_cannot_claim_one_more_question_total():
    payload = case("clarification_needed", pending=1, answered=7)
    progress = review_guidance(payload)
    status = progress["clarification_progress"]
    assert status["current_batch_question_count"] == 1
    assert status["clarifications_answered_or_skipped_total"] == 7
    assert status["current_batch_only"] is True
    assert status["overall_remaining_known"] is False
    assert status["overall_clarifications_remaining"] is None
    assert status["full_evidence_review_ready"] is False
    assert status["stage"] == "reviewer_clarification"
    assert "current batch only" in status["participant_message"]
    assert "overall" in progress["wait_guidance"].lower()
    assert progress["recommended_check_after_seconds"] == 0


def test_after_batch_future_questions_are_unknown_until_ready():
    pending = case("queued", answered=8)
    progress = clarification_progress(pending)
    assert progress["current_batch_question_count"] == 0
    assert progress["clarifications_answered_or_skipped_total"] == 8
    assert progress["overall_clarifications_remaining"] is None
    assert not progress["overall_remaining_known"]
    assert "another useful clarification" in progress["participant_message"]
    for status in ("processing", "paused", "error", "resource_limited", "stopped"):
        report = clarification_progress({**pending, "status": status})
        assert report["overall_clarifications_remaining"] is None
        assert report["full_evidence_review_ready"] is False


def test_only_ready_yields_zero_more_review_questions_and_declared_final_steps():
    ready = clarification_progress(case("ready", answered=8))
    assert ready["stage"] == "independent_review_complete"
    assert ready["overall_remaining_known"]
    assert ready["overall_clarifications_remaining"] == 0
    assert ready["remaining_after_ready"] == [
        "participant_review_and_confirmation",
        "CF003_three_secondary_questions",
        "encrypted_final_submission",
    ]


def test_legacy_single_question_shape_is_handled_without_fictitious_total():
    progress = clarification_progress(
        {
            "status": "clarification_needed",
            "pending_clarification": {"route_id": "Q-single"},
            "clarification_history": [],
        }
    )
    assert progress["current_batch_question_count"] == 1
    assert not progress["overall_remaining_known"]


def test_current_action_schema_declares_readonly_progress():
    contract = json.loads(ACTION.read_text())
    assert contract["info"]["version"] == "1.6.1"
    status = contract["components"]["schemas"]["ReviewStatus"]
    entry = status["properties"]["clarification_progress"]
    assert "clarification_progress" not in status["required"]
    assert "overall_clarifications_remaining" in entry["required"]
    assert entry["properties"]["overall_clarifications_remaining"]["type"] == ["integer", "null"]


def test_cumulative_gpt_update_preserves_prior_science_and_bans_false_count():
    import importlib.util
    import zipfile

    task = ROOT / "tasks/life-patterns-clarification-endgame-20261016"
    src = task / "build_gpt_update.py"
    spec = importlib.util.spec_from_file_location("gpt_progress_build", src)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    built = module.build()
    source = built[module.INSTR].decode("utf-8")
    assert len(source.replace("\n", "\r\n")) <= 8000
    assert "Never '1 of 1 remaining'" in source
    assert "global remaining UNKNOWN" in source
    assert "No question-count cap or coverage-only asks." in source
    manifest = json.loads(built["UPDATE-MANIFEST.json"])
    assert manifest["knowledge_file_count"] == 8
    assert manifest["action_version"] == "1.6.1"
    assert not manifest["private_participant_data_or_credentials_present"]
    with zipfile.ZipFile(module.BASE) as base:
        for key in built:
            if key.startswith("knowledge/") and key != module.GUIDE:
                assert built[key] == base.read(key)
        assert (
            json.loads(built[module.ACTION])["paths"]
            == json.loads(base.read(module.ACTION))["paths"]
        )
    assert module.OUT.read_bytes() == module.serialize(built)
    assert all(module.sha(built[k]) == v for k, v in manifest["files"].items())
    guide = built[module.GUIDE].decode("utf-8")
    assert "batch-local" in guide.lower()
    assert "overall remaining clarifications" in guide.lower()
    assert "This batch is complete" in guide
