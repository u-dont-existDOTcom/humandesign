"""Consumer-operation regressions for direct paraphrases and resolved repairs."""
from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from test_life_patterns_v2_owner_workflow import Model, op, session
from test_life_patterns_v2_owner_dialogue import RoutedModel, route
from hdmatch.api.life_patterns_v2_owner_conversation import ConversationMove
from hdmatch.api.life_patterns_v2_owner_dialogue import ParticipantInput, RepairFrontier
from hdmatch.api.life_patterns_v2_owner_persistent import _canonical_sha
from hdmatch.api.life_patterns_v2_owner_workflow_api import measurement_package


class SummaryModel(RoutedModel):
    summarize = False
    calls = 0

    def plan_turn(self, **kwargs: Any) -> ConversationMove:
        self.calls += 1
        if self.summarize:
            self.summarize = False
            return ConversationMove(reply="Does this connection fit?", move_type="surface_hypothesis",
                hypothesis_proposition="The participant walks on weekdays and cycles on weekends.",
                evidence_fact_ids=tuple(f.fact_id for f in kwargs["operative_facts"]))
        return ConversationMove(reply="What influences how far you travel?", move_type="follow_up")

    def review_pattern_candidate(self, **kwargs: Any) -> dict[str, Any]:
        return {"decision": "direct", "inference_added": "", "inference_quote": ""}


def make_summary() -> tuple[Any, SummaryModel, dict[str, Any]]:
    m = SummaryModel()
    s = session(m)
    s.execute(op(s, "answer", {"message": "I walk on weekdays."}))
    m.summarize = True
    result = s.execute(op(s, "answer", {"message": "I cycle on weekends."}, "second"))
    return s, m, result


def test_multiturn_direct_paraphrase_is_summary_not_inference_or_fabricated_acceptance() -> None:
    s, _, result = make_summary()
    assert result["reported_summary_recorded"]
    assert s.phase == "advancing" and s.continue_current_focus and not s._draft_move
    assert not s.core.record.pattern_proposals and not s.core.record.participant_adjudications
    assert len(s.core.record.episode_facts) == 2
    row = s.view()["patterns"][0]
    assert row["origin"] == "source_summary" and row["status"] == "reported"
    assert row["participant_adjudicated"] is False
    assert {r["text"] for r in row["sources"]} == {"I walk on weekdays.", "I cycle on weekends."}
    assert "connection" not in result["reply"]


def test_summary_continues_current_focus_without_fake_answer_or_more_evidence() -> None:
    s, m, _ = make_summary()
    before = s.core.record.model_dump(mode="json")
    count = len(m.extraction_messages)
    users = len([r for r in s.conversation if r["role"] == "user"])
    s.execute(op(s, "advance", identity="continue"))
    assert s.phase == "awaiting_answer" and s.conversation[-1]["text"] == "What influences how far you travel?"
    assert len(m.extraction_messages) == count and s.core.record.model_dump(mode="json") == before
    assert len([r for r in s.conversation if r["role"] == "user"]) == users


def test_summary_backup_retry_correction_and_research_export_remain_distinct() -> None:
    s, m, result = make_summary()
    r = session(m)
    r.restore_recovery_snapshot(result["snapshot"])
    assert r.view()["patterns"] == s.view()["patterns"]
    # Replay cannot append another source summary.
    retry = s.execute(op(s, "answer", {"message": "I cycle on weekends."}, "second").model_copy(update={"expected_revision": 1}))
    assert retry["replayed"] and len(s.reported_summaries) == 1
    note = op(r, "annotate", {"proposal_id": r.patterns()[0]["proposal_id"], "message": "Except during winter."}, "note")
    r.execute(note)
    package = measurement_package(r)
    assert package["completed_results"] == []
    assert package["reported_summaries"][0]["status"] == "disputed"
    assert package["reported_summaries"][0]["participant_adjudicated"] is False
    assert not r.core.record.participant_adjudications


def test_resolved_withdrawal_has_executable_continuation_and_no_implicit_completion() -> None:
    m = RoutedModel()
    m.routing = route("repair", [], "That was a restatement, not a discovery. I have withdrawn it.", True)
    s = session(m)
    s.phase = "synthesis_review"
    s._draft_move = ConversationMove(reply="Connection?", move_type="surface_hypothesis",
        hypothesis_proposition="A redundant statement", evidence_fact_ids=("unused",))
    before = s.core.record.model_dump(mode="json")
    result = s.execute(op(s, "answer", {"message": "That is just what I already said."}))
    assert s.phase == "advancing" and s.continue_current_focus and not s.repair_pending
    assert result["process_only"] and not s._draft_move
    assert s.core.record.model_dump(mode="json") == before
    s.execute(op(s, "advance", identity="next"))
    assert s.phase == "awaiting_answer" and s.conversation[-1]["text"].endswith("?")
    assert not m.extraction_messages and not s.coverage_aggregate


def test_explained_question_is_actually_present_and_not_skipped() -> None:
    m = RoutedModel()
    m.routing = route("repair", [], "The distinction concerns timing rather than intensity.")
    s = session(m)
    result = s.execute(op(s, "answer", {"message": "What did you mean?"}))
    assert result["reply"].endswith(m.routing["repair_frontier"]["question"])
    assert s.phase == "awaiting_answer" and not s.continue_current_focus
    assert not s.core.record.episode_facts


def test_repair_wait_for_judgment_requires_live_draft() -> None:
    s = session()
    with pytest.raises(ValueError, match="absent inference"):
        s._set_repair_frontier(RepairFrontier(next_action="await_judgment", question=""))


@pytest.mark.parametrize("action,question", [("await_answer", ""), ("continue_interview", "An unanswered question?"), ("await_judgment", "Question?")])
def test_repair_frontier_rejects_contradictory_next_action(action: str, question: str) -> None:
    with pytest.raises(ValueError):
        RepairFrontier(next_action=action, question=question)


@pytest.mark.parametrize("frontier,expected", [
    ({"next_action": "continue_interview", "question": ""}, "advancing"),
    ({"next_action": "await_answer", "question": "What happened next?"}, "awaiting_answer")])
def test_legacy_repair_migration_recovers_next_action_not_personality(frontier: dict[str, str], expected: str) -> None:
    class RecoveryModel(Model):
        def recover_repair_frontier(self, **kwargs: Any) -> dict[str, str]:
            return frontier
    m = RecoveryModel()
    s = session(m)
    s.repair_pending = True
    s.conversation = [{"turn_id": "TEST-U", "role": "user", "text": "Please explain."},
                      {"turn_id": "TEST-A", "role": "assistant", "text": "A clarification. What happened next?"}]
    backup = s.recovery_snapshot()
    backup["workflow"]["semantic_policy_version"] = 3
    for key in ("repair_needs_review", "repair_frontier"):
        backup["workflow"].pop(key, None)
    backup.pop("recovery_sha256")
    backup["recovery_sha256"] = _canonical_sha(backup)
    original = deepcopy(backup)
    r = session(m)
    r.restore_recovery_snapshot(backup)
    assert r.repair_needs_review
    before = r.core.record.model_dump(mode="json")
    r.execute(op(r, "review_repair", identity="recover"))
    assert r.phase == expected and not r.repair_needs_review
    assert r.conversation == s.conversation and r.core.record.model_dump(mode="json") == before
    assert backup == original


def test_pause_preserves_automatic_continuation_until_explicit_resume() -> None:
    s, _, _ = make_summary()
    s.execute(op(s, "pause", identity="pause"))
    r = session()
    r.restore_recovery_snapshot(s.recovery_snapshot())
    assert r.phase == "paused" and r.continue_current_focus
    with pytest.raises(ValueError):
        r.execute(op(r, "advance", identity="blocked"))
    r.execute(op(r, "resume", identity="resume"))
    assert r.phase == "advancing"


def test_live_input_contract_requires_frontier_but_ordinary_answers_do_not() -> None:
    raw = route("repair", [], "Explained.")
    raw.pop("repair_frontier")
    with pytest.raises(ValueError, match="next conversational action"):
        ParticipantInput.model_validate(raw)
    assert ParticipantInput.model_validate(route("answer", ["Full answer."])).repair_frontier is None
