from __future__ import annotations

import json
from typing import Any
import pytest

from test_life_patterns_v2_owner_workflow import Model, session, op
from hdmatch.api.life_patterns_v2_owner_context import interview_context
from hdmatch.api.life_patterns_v2_owner_continuous_flow import ContinuousFlowRecoverabilityOpenAIModel
from hdmatch.api.life_patterns_v2_owner_conversation import ConversationMove
from hdmatch.api.life_patterns_v2_owner_natural_flow import TopicCompleteMove


def route(kind: str, quotes: list[str], reply: str = "", withdraw: bool = False, historical: list[str] | None = None) -> dict[str, Any]:
    return {"kind": kind, "evidence_quotes": quotes, "repair_reply": reply,
            "withdraw_pending_inference": withdraw, "historical_process_turn_ids": historical or []}


class RoutedModel(Model):
    routing: dict[str, Any] | None = None
    extraction_messages: list[str]

    def __init__(self) -> None:
        self.extraction_messages = []

    def route_participant_turn(self, **kwargs: Any) -> dict[str, Any]:
        return self.routing or route("answer", [kwargs["message"]])

    def extract_turn(self, **kwargs: Any) -> Any:
        self.extraction_messages.append(kwargs["message"])
        return super().extract_turn(**kwargs)


@pytest.mark.parametrize("message", ["What is the difference?", "Fix that question.", "Why mix those issues?", "I cannot understand what you mean."])
def test_repair_has_no_extraction_or_coverage_or_synthesis(message: str) -> None:
    model = RoutedModel()
    model.routing = route("repair", [], "Those can happen together; my contrast was not justified.")
    s = session(model)
    s.active_domain_id = "correction_threshold"
    before = s.core.record.model_dump(mode="json")
    result = s.execute(op(s, "answer", {"message": message}))
    assert not model.extraction_messages
    assert s.core.record.model_dump(mode="json") == before
    assert not s.coverage_aggregate and not s.core.record.participant_adjudications
    assert result["view"]["phase"] == "awaiting_answer"
    assert result["move_type"] == "conversation_repair"
    restored = session(model)
    restored.restore_recovery_snapshot(result["snapshot"])
    assert restored.repair_pending and restored.active_domain_id == "correction_threshold"
    assert restored._participant_user_turn_count() == 0


def test_mixed_input_preserves_real_evidence_and_original_full_source() -> None:
    model = RoutedModel()
    message = "Your contrast is wrong. I usually wait a day before responding."
    quote = "I usually wait a day before responding."
    model.routing = route("mixed", [quote], "I should not have treated those as opposites.")
    s = session(model)
    result = s.execute(op(s, "answer", {"message": message}))
    assert model.extraction_messages == [quote]
    assert s.conversation[0]["text"] == message
    assert s.core.record.episode_facts[0].proposition == quote
    assert s.core.record.source_provenance[0].locator.endswith(s.conversation[0]["turn_id"])
    assert result["reply"].startswith("I should not")


@pytest.mark.parametrize("kind,quotes", [("repair", ["a fact"]), ("mixed", ["fabricated"]), ("answer", ["a part"])])
def test_invalid_routing_is_rolled_back(kind: str, quotes: list[str]) -> None:
    model = RoutedModel()
    model.routing = route(kind, quotes, "A clarification")
    s = session(model)
    before = s.recovery_snapshot()
    with pytest.raises(ValueError):
        s.execute(op(s, "answer", {"message": "A complete original message."}))
    assert s.recovery_snapshot() == before


def test_exact_recorded_pattern_is_not_reproposed_even_with_new_evidence() -> None:
    model = RoutedModel()
    model.direct = True
    s = session(model)
    message = "I think alone before unfamiliar group decisions."
    s.execute(op(s, "answer", {"message": message}))
    s.execute(op(s, "advance", identity="next"))
    result = s.execute(op(s, "answer", {"message": message}, "repeated"))
    assert result["formulation_suppressed"] == "duplicate"
    assert len(s.core.record.participant_adjudications) == 1
    assert not s._draft_move


def test_semantic_duplicate_can_be_suppressed_without_exact_wording_match() -> None:
    class DuplicateModel(RoutedModel):
        direct = True
        def review_pattern_candidate(self, **kwargs: Any) -> dict[str, Any]:
            existing = kwargs["evidence_context"]["patterns"]
            return ({"decision": "duplicate", "related_proposal_id": existing[0]["proposal_id"]}
                    if existing else {"decision": "direct"})
    s = session(DuplicateModel())
    s.execute(op(s, "answer", {"message": "I think alone before unfamiliar group decisions."}))
    s.execute(op(s, "advance", identity="next"))
    result = s.execute(op(s, "answer", {"message": "I first reflect privately with new groups."}, "repeated"))
    assert result["formulation_suppressed"] == "duplicate"
    assert len(s.core.record.participant_adjudications) == 1


def test_same_sources_can_support_genuinely_different_inference() -> None:
    s = session()
    s.execute(op(s, "answer", {"message": "I decide privately, but explain my choice in public."}))
    ids = tuple(f.fact_id for f in s.core.operative_facts())
    s._create_pattern(ConversationMove(reply="A?", move_type="surface_hypothesis",
        hypothesis_proposition="Private decision and public explanation are distinct stages.", evidence_fact_ids=ids))
    from hdmatch.api.life_patterns_v2_owner_app import PatternAdjudicationRequest
    s.adjudicate(PatternAdjudicationRequest(decision="accept"))
    s._create_pattern(ConversationMove(reply="B?", move_type="surface_hypothesis",
        hypothesis_proposition="The participant may prepare before speaking to a group.", evidence_fact_ids=ids))
    assert s._draft_move is not None


def test_repair_can_retire_unjudged_duplicate_without_rewriting_accepted_record() -> None:
    model = RoutedModel()
    s = session(model)
    s._draft_move = ConversationMove(reply="An old idea", move_type="surface_hypothesis",
                                    hypothesis_proposition="An unjudged idea", evidence_fact_ids=("old",))
    s.phase = "synthesis_review"
    before = s.core.record.model_dump(mode="json")
    model.routing = route("repair", [], "That was not a new interpretation; I have withdrawn it.", True)
    result = s.execute(op(s, "answer", {"message": "You already said that."}))
    assert result["view"]["phase"] == "awaiting_answer"
    assert len(s.retired_drafts) == 1 and not s.retired_drafts[0]["adjudicated"]
    assert s.core.record.model_dump(mode="json") == before


def test_explanation_does_not_discard_valid_unjudged_inference() -> None:
    m = RoutedModel()
    m.routing = route("repair", [], "I was distinguishing timing, not strength.")
    s = session(m)
    s.phase = "synthesis_review"
    s._draft_move = ConversationMove(reply="A connection", move_type="surface_hypothesis",
                                    hypothesis_proposition="A tentative connection", evidence_fact_ids=("fact",))
    s.execute(op(s, "answer", {"message": "What does that mean?"}))
    assert s.phase == "synthesis_review" and s._draft_move


def test_legacy_process_facts_are_quarantined_not_erased() -> None:
    m = RoutedModel()
    s = session(m)
    s.execute(op(s, "answer", {"message": "An old interview complaint stored by the old version."}))
    old_record = s.core.record.model_dump(mode="json")
    old_turn = s.conversation[0]["turn_id"]
    m.routing = route("repair", [], "I misunderstood the question you were asking me.", historical=[old_turn])
    s.execute(op(s, "answer", {"message": "That was a complaint about the question."}, "repair"))
    assert not s._planning_facts()
    assert s.core.record.model_dump(mode="json") == old_record
    assert old_turn in s.recovery_snapshot()["workflow"]["process_turn_ids"]


def test_legacy_knowledge_is_planning_only_not_fabricated_coverage() -> None:
    s = session()
    s.legacy_patterns = [{"wording": "An older pattern", "coverage": {"assessments": [
        {"domain_id": "complex_structure", "status": "sufficient", "reason": "Old unavailable evidence"}]}}]
    ctx = s.evidence_context()
    assert ctx["legacy_coverage_planning_only"][0]["source_available"] is False
    assert not s.coverage_aggregate and not s.core.record.episode_facts


def test_review_explanation_must_anchor_in_actual_candidate() -> None:
    class ReviewModel(RoutedModel):
        direct = True
        def review_pattern_candidate(self, **kwargs: Any) -> dict[str, Any]:
            return {"decision": "inference", "inference_added": "More persistence.",
                    "inference_quote": "words absent from candidate"}
    s = session(ReviewModel())
    result = s.execute(op(s, "answer", {"message": "I often revisit an unresolved decision."}))
    assert result["formulation_suppressed"] == "review_does_not_match_candidate"
    assert not s._draft_move and not s.core.record.participant_adjudications


def test_inference_reply_does_not_announce_completion() -> None:
    class InferenceModel(RoutedModel):
        def plan_turn(self, **kwargs: Any) -> ConversationMove:
            return ConversationMove(reply="We have enough information; we are done.", move_type="surface_hypothesis",
                hypothesis_proposition="This may be a context-dependent distinction.",
                evidence_fact_ids=(kwargs["operative_facts"][-1].fact_id,))
    s = session(InferenceModel())
    result = s.execute(op(s, "answer", {"message": "I respond differently in familiar groups."}))
    assert result["view"]["phase"] == "synthesis_review"
    assert "enough" not in result["reply"] and "done" not in result["reply"]


@pytest.mark.parametrize("schema,expected,effort", [
    ("life_patterns_hidden_ledger_turn_v1", "gpt-5.6-sol", "xhigh"),
    ("life_patterns_participant_input_v1", "gpt-5.6-sol", "xhigh"),
    ("life_patterns_conversation_move_v1", "gpt-5.6-sol", "xhigh"),
    ("life_patterns_refinement_move_v1", "gpt-5.6-sol", "xhigh"),
    ("life_patterns_question_admission_v1", "gpt-5.6-sol", "xhigh"),
    ("life_patterns_formulation_fidelity_v2", "gpt-5.6-sol", "xhigh"),
    ("life_patterns_continuation_question_admission_v1", "gpt-5.6-sol", "xhigh"),
])
def test_actual_request_body_uses_role_model_and_reasoning(monkeypatch: Any, schema: str, expected: str, effort: str) -> None:
    import hdmatch.api.life_patterns_v2_owner_conversation as transport
    requests = []
    class Response:
        def __enter__(self) -> Response:
            return self
        def __exit__(self, *args: Any) -> None:
            pass
        def read(self) -> bytes:
            return json.dumps({"status": "completed", "model": expected,
                               "output_text": "{}", "usage": {"output_tokens": 300}}).encode()
    def call(request: Any, **kwargs: Any) -> Response:
        requests.append(json.loads(request.data))
        return Response()
    monkeypatch.setattr(transport, "urlopen", call)
    m = ContinuousFlowRecoverabilityOpenAIModel(api_key="test-not-real")
    sink: list[dict[str, Any]] = []
    with interview_context(lambda: {"conversation": [], "evidence_conversation": [], "operative_facts": [], "model_call_sink": sink}):
        m._conversation_call_json(instructions="test", payload={}, schema={"type": "object"},
                                  effort="low", max_output_tokens=900, schema_name=schema)
    assert requests[0]["model"] == expected and requests[0]["reasoning"]["effort"] == effort
    assert requests[0]["max_output_tokens"] >= (25000 if effort == "xhigh" else 2500)
    assert m.model == "gpt-5.6-sol"  # No shared object mutation for extraction.
    assert sink[0]["returned_model"] == expected and "output_text" not in sink[0]


def test_gate_rejects_self_reported_invalid_logic(monkeypatch: Any) -> None:
    m = ContinuousFlowRecoverabilityOpenAIModel(api_key="test")
    monkeypatch.setattr(m, "_conversation_call_json", lambda **kwargs: {
        "decision": "admit", "premises_supported": True, "scope_preserved": True,
        "contrast_answerable": False})
    answer = m._admit_in_thread_question(candidate=ConversationMove(reply="Do you act or feel?", move_type="follow_up"),
                                          operative_facts=(), recent_conversation=())
    assert isinstance(answer, TopicCompleteMove)


def test_old_pending_draft_is_rechecked_before_repeated_approval() -> None:
    from hdmatch.api.life_patterns_v2_owner_persistent import _canonical_sha
    m = RoutedModel()
    m.direct = True
    s = session(m)
    message = "I think privately before a group discussion."
    s.execute(op(s, "answer", {"message": message}))
    s._draft_move = ConversationMove(reply="Already said?", move_type="surface_hypothesis",
                                    hypothesis_proposition=message,
                                    evidence_fact_ids=tuple(f.fact_id for f in s.core.operative_facts()))
    s.phase = "synthesis_review"
    snap = s.recovery_snapshot()
    snap["workflow"].pop("semantic_policy_version")
    snap.pop("recovery_sha256")
    snap["recovery_sha256"] = _canonical_sha(snap)
    restored = session(m)
    restored.restore_recovery_snapshot(snap)
    assert restored.view()["draft_needs_review"]
    result = restored.execute(op(restored, "review_draft", identity="check-draft"))
    assert result["view"]["phase"] == "advancing" and not restored._draft_move
    assert len(restored.core.record.participant_adjudications) == 1
    assert not restored.draft_needs_review


def test_explicit_pause_is_not_confused_with_clarification() -> None:
    m = RoutedModel()
    m.routing = route("pause", [])
    s = session(m)
    s.execute(op(s, "answer", {"message": "Pause this interview."}))
    assert s.phase == "paused" and not s.core.record.episode_facts
    s.execute(op(s, "resume", identity="resume"))
    assert s.phase == "awaiting_answer"


def test_direct_source_does_not_depend_on_extractor_assertion_label() -> None:
    from hdmatch.api.life_patterns_v2_owner_conversation import TurnExtraction, HiddenFactCandidate
    class LabelModel(RoutedModel):
        direct = True
        def extract_turn(self, **kwargs: Any) -> TurnExtraction:
            return TurnExtraction(episode_summary="A synthetic report", facts=(HiddenFactCandidate(
                assertion_type="positive_occurrence", proposition=kwargs["message"]),), corrections=())
        def review_pattern_candidate(self, **kwargs: Any) -> dict[str, Any]:
            return {"decision": "direct", "inference_added": "", "inference_quote": ""}
    s = session(LabelModel())
    result = s.execute(op(s, "answer", {"message": "I prepare less when I know the task well."}))
    assert result["direct_pattern_recorded"] and not s._draft_move
    assert len(s.core.record.participant_adjudications) == 1
    assert s.view()["patterns"][0]["origin"] == "direct_report"


def test_direct_label_independence_does_not_accept_other_turn_evidence() -> None:
    s = session()
    s.execute(op(s, "answer", {"message": "An earlier different source."}))
    ids = tuple(f.fact_id for f in s.core.operative_facts())
    s.execute(op(s, "answer", {"message": "I prepare less when I know the task well."}, "second"))
    move = ConversationMove(reply="Saved", move_type="surface_hypothesis",
                            hypothesis_proposition="I prepare less when I know the task well.", evidence_fact_ids=ids)
    assert s._direct_report_source(move) is None
