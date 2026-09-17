from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from threading import Event
from typing import Any

import pytest

from hdmatch.api.life_patterns_v2_owner_conversation import (
    ConversationMove,
    HiddenFactCandidate,
    TurnExtraction,
)
from hdmatch.api.life_patterns_v2_owner_workflow import (
    InterviewOperation,
    WorkflowConflict,
    WorkflowSession,
)


class Model:
    configured = True
    direct = False
    stop = False
    fail = False

    def extract_turn(self, **kwargs: Any) -> TurnExtraction:
        if self.fail:
            raise RuntimeError("synthetic failure")
        return TurnExtraction(
            episode_summary="Synthetic context",
            facts=(
                HiddenFactCandidate(
                    assertion_type="reported_appraisal_or_belief", proposition=kwargs["message"]
                ),
            ),
            corrections=(),
        )

    def plan_turn(self, **kwargs: Any) -> ConversationMove:
        if self.direct:
            return ConversationMove(
                reply="Recorded from your words.",
                move_type="surface_hypothesis",
                hypothesis_proposition=kwargs["recent_conversation"][-1]["text"],
                evidence_fact_ids=(kwargs["operative_facts"][-1].fact_id,),
            )
        return ConversationMove(reply="Which part remains unclear?", move_type="follow_up")

    def plan_continuation_question(self, **kwargs: Any) -> dict[str, Any]:
        return {
            "opening": None if self.stop else "What changed after that?",
            "primary_domain_id": None if self.stop else kwargs["open_domains"][0].domain_id,
            "no_useful_question": self.stop,
            "question_admission": {"decision": "stop" if self.stop else "admit"},
        }


def session(model: Model | None = None) -> WorkflowSession:
    result = WorkflowSession(session_id="OWNER-TEST", model=model or Model())  # type: ignore[arg-type]
    result.pattern_focus_established = True
    return result


def op(
    s: WorkflowSession,
    kind: str,
    payload: dict[str, Any] | None = None,
    identity: str = "operation-1",
) -> InterviewOperation:
    return InterviewOperation(
        operation_id=identity, expected_revision=s.revision, kind=kind, payload=payload or {}
    )  # type: ignore[arg-type]


def test_exact_retry_is_once_and_changed_reuse_conflicts() -> None:
    s = session()
    request = op(s, "answer", {"message": "A synthetic answer."})
    first = s.execute(request)
    second = s.execute(request)
    assert first["view"]["revision"] == second["view"]["revision"] == 1
    assert len([r for r in s.conversation if r["role"] == "user"]) == 1
    with pytest.raises(WorkflowConflict):
        s.execute(request.model_copy(update={"payload": {"message": "Different"}}))


def test_failed_turn_rolls_back_and_can_be_retried() -> None:
    model = Model()
    s = session(model)
    request = op(s, "answer", {"message": "Preserve this answer."})
    before = s.recovery_snapshot()
    model.fail = True
    with pytest.raises(RuntimeError):
        s.execute(request)
    assert s.revision == 0 and s.conversation == before["conversation"]
    model.fail = False
    assert s.execute(request)["view"]["revision"] == 1


def test_phase_after_old_acceptance_tracks_new_question_and_survives_restore() -> None:
    model = Model()
    model.direct = True
    s = session(model)
    s.execute(op(s, "answer", {"message": "I leave group work to think alone first."}))
    assert s.phase == "advancing"
    s.execute(op(s, "advance", identity="operation-2"))
    assert s.phase == "awaiting_answer"
    restored = session()
    restored.restore_recovery_snapshot(s.recovery_snapshot())
    assert restored.phase == "awaiting_answer"
    assert restored.view()["patterns"][0]["origin"] == "direct_report"


def test_pause_blocks_answers_and_resume_preserves_pending_phase() -> None:
    s = session()
    s.execute(op(s, "pause"))
    snap = s.recovery_snapshot()
    restored = session()
    restored.restore_recovery_snapshot(snap)
    assert restored.phase == "paused"
    with pytest.raises(WorkflowConflict):
        restored.execute(op(restored, "answer", {"message": "Not allowed"}, "operation-2"))
    restored.execute(op(restored, "resume", identity="operation-3"))
    assert restored.phase == "awaiting_answer"


def test_busy_session_rejects_second_mutation_without_waiting() -> None:
    entered, release = Event(), Event()
    model = Model()
    original = model.extract_turn

    def blocked(**kwargs: Any) -> TurnExtraction:
        entered.set()
        assert release.wait(3)
        return original(**kwargs)

    model.extract_turn = blocked  # type: ignore[method-assign]
    s = session(model)
    with ThreadPoolExecutor(max_workers=2) as pool:
        future = pool.submit(s.execute, op(s, "answer", {"message": "First"}))
        assert entered.wait(1)
        try:
            with pytest.raises(WorkflowConflict):
                s.execute(op(s, "answer", {"message": "Second"}, "operation-2"))
        finally:
            release.set()
        future.result()
    assert s.revision == 1


def test_no_useful_next_question_preserves_incomplete_coverage() -> None:
    model = Model()
    model.stop = True
    s = session(model)
    s.phase = "advancing"
    result = s.execute(op(s, "advance"))
    assert result["view"]["phase"] == "bounded"
    assert result["complete"] is False
    assert result["no_useful_question"] is True


def test_stale_revision_cannot_apply_an_answer() -> None:
    s = session()
    s.execute(op(s, "answer", {"message": "First"}))
    with pytest.raises(WorkflowConflict):
        s.execute(
            InterviewOperation(
                operation_id="old", expected_revision=0, kind="answer", payload={"message": "Stale"}
            )
        )


def test_final_gate_also_catches_runtime_fallback_questions() -> None:
    from hdmatch.api.life_patterns_v2_owner_natural_flow import TopicCompleteMove

    class FallbackModel(Model):
        gate_calls = 0

        def plan_turn(self, **kwargs: Any) -> ConversationMove:
            return ConversationMove(
                reply="An invalid proposed connection.",
                move_type="surface_hypothesis",
                hypothesis_proposition="Unsupported",
                evidence_fact_ids=("MISSING",),
            )

        def _admit_in_thread_question(self, **kwargs: Any) -> TopicCompleteMove:
            self.gate_calls += 1
            assert kwargs["candidate"].move_type == "follow_up"
            return TopicCompleteMove(reply="Nothing useful to ask.")

    model = FallbackModel()
    s = session(model)
    result = s.execute(op(s, "answer", {"message": "A complete synthetic answer."}))
    assert model.gate_calls == 1
    assert result["no_useful_question"] is True
    assert s.phase == "advancing"
    assert not s.core.record.participant_adjudications


def test_stopping_refinement_preserves_unjudged_inference() -> None:
    from hdmatch.api.life_patterns_v2_owner_natural_flow import TopicCompleteMove

    class RefinementModel(Model):
        def plan_refinement_turn(self, **kwargs: Any) -> ConversationMove:
            return ConversationMove(reply="A redundant question?", move_type="follow_up")

        def _admit_in_thread_question(self, **kwargs: Any) -> TopicCompleteMove:
            return TopicCompleteMove(reply="No worthwhile further question.")

    s = session(RefinementModel())
    s._draft_move = ConversationMove(
        reply="Possible connection?",
        move_type="surface_hypothesis",
        hypothesis_proposition="A tentative idea",
        evidence_fact_ids=("unused",),
    )
    s.phase = "synthesis_review"
    result = s.execute(op(s, "investigate"))
    assert result["no_useful_question"] is True
    assert s.phase == "synthesis_review"
    assert s._draft_move is not None and not s.core.record.participant_adjudications


def test_context_reviewer_can_block_auto_recording_of_exact_but_unendorsed_text() -> None:
    class ContextModel(Model):
        direct = True

        def review_pattern_candidate(self, **kwargs: Any) -> dict[str, str]:
            assert "I no longer believe" in kwargs["evidence_context"]["conversation"][-1]["text"]
            return {"decision": "inference", "inference_added": "Endorsement is not established."}

    s = session(ContextModel())
    result = s.execute(
        op(s, "answer", {"message": "I no longer believe that quiet always helps me."})
    )
    assert not s.core.record.participant_adjudications
    assert result["view"]["phase"] == "synthesis_review"
