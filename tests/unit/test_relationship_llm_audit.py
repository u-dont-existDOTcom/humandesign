from __future__ import annotations

import json
from collections.abc import Mapping

import pytest

from hdmatch.relationship.llm_audit import (
    FieldAuditInput,
    LLMAuditProviderError,
    LLMAuditUnavailableError,
    OpenRouterRelationshipAuditor,
)


def _envelope(content: dict[str, object]) -> bytes:
    return json.dumps({"choices": [{"message": {"content": json.dumps(content)}}]}).encode()


def test_field_auditor_uses_structured_llm_output_and_chart_blind_prompt() -> None:
    captured: dict[str, object] = {}

    def transport(
        url: str,
        body: bytes,
        headers: Mapping[str, str],
        timeout: float,
    ) -> bytes:
        request = json.loads(body)
        captured["url"] = url
        captured["headers"] = dict(headers)
        captured["request"] = request
        captured["timeout"] = timeout
        return _envelope(
            {
                "score": 4,
                "feedback": "This is fluent text but it does not answer the relationship timeline question.",
                "needs_clarification": True,
                "reason_code": "off_topic",
            }
        )

    auditor = OpenRouterRelationshipAuditor(api_key="secret", transport=transport)
    result = auditor.assess_field(
        FieldAuditInput(
            question_id="RRQ_TRAJECTORY_CONTEXT",
            question_title="Relationship timeline & context",
            field_id="relationship_timeline",
            field_label="What was the romantic timeline of the relationship?",
            field_hint="When it became romantic, how long that lasted, and what it is now.",
            status="clear",
            answer="I farted on her and we ate ice cream with peas and carrots.",
        )
    )

    assert result.quality.score == 4
    assert result.quality.needs_clarification is True
    request = captured["request"]
    assert isinstance(request, dict)
    messages = request["messages"]
    assert isinstance(messages, list)
    system = messages[0]["content"]
    assert "Random fluent-looking text must stay near zero" in system
    assert "birth data" in system
    assert request["response_format"]["type"] == "json_schema"


def test_explicit_unknown_is_complete_without_provider_call() -> None:
    def should_not_run(
        url: str,
        body: bytes,
        headers: Mapping[str, str],
        timeout: float,
    ) -> bytes:
        raise AssertionError("provider must not be called for explicit unknown")

    auditor = OpenRouterRelationshipAuditor(api_key=None, transport=should_not_run)
    result = auditor.assess_field(
        FieldAuditInput(
            question_id="Q",
            question_title="Question",
            field_id="F",
            field_label="What did they feel?",
            status="unknown",
        )
    )
    assert result.quality.score == 100
    assert result.quality.reason_code == "explicit_unknown"


def test_missing_key_fails_closed_for_real_llm_audit() -> None:
    auditor = OpenRouterRelationshipAuditor(api_key=None)
    with pytest.raises(LLMAuditUnavailableError):
        auditor.assess_field(
            FieldAuditInput(
                question_id="Q",
                question_title="Question",
                field_id="F",
                field_label="How attracted were you?",
                status="clear",
                answer="Very high.",
            )
        )


def test_session_audit_rejects_fabricated_field_identity() -> None:
    def transport(
        url: str,
        body: bytes,
        headers: Mapping[str, str],
        timeout: float,
    ) -> bytes:
        return _envelope(
            {
                "field_quality": [
                    {
                        "question_id": "Q",
                        "field_id": "invented",
                        "score": 80,
                        "feedback": "Looks usable.",
                        "needs_clarification": False,
                        "reason_code": "usable",
                    }
                ],
                "clarifications": [],
            }
        )

    auditor = OpenRouterRelationshipAuditor(api_key="secret", transport=transport)
    with pytest.raises(LLMAuditProviderError):
        auditor.audit_session(
            (
                FieldAuditInput(
                    question_id="Q",
                    question_title="Question",
                    field_id="real",
                    field_label="How attracted were you?",
                    status="clear",
                    answer="Very high.",
                ),
            ),
            max_clarifications=6,
        )


def test_session_audit_preserves_specific_clarification() -> None:
    def transport(
        url: str,
        body: bytes,
        headers: Mapping[str, str],
        timeout: float,
    ) -> bytes:
        return _envelope(
            {
                "field_quality": [
                    {
                        "question_id": "Q",
                        "field_id": "eros",
                        "score": 45,
                        "feedback": "Love is described, but romantic in-love state is not distinguished.",
                        "needs_clarification": True,
                        "reason_code": "love_vs_eros",
                    }
                ],
                "clarifications": [
                    {
                        "source_question_id": "Q",
                        "source_field_id": "eros",
                        "reason": "The answer describes caring but does not establish romantic in-love experience.",
                        "prompt": "Separately from caring about them, were you romantically in love with them?",
                        "priority": 1,
                    }
                ],
            }
        )

    auditor = OpenRouterRelationshipAuditor(api_key="secret", transport=transport)
    result = auditor.audit_session(
        (
            FieldAuditInput(
                question_id="Q",
                question_title="Love",
                field_id="eros",
                field_label="Were you romantically in love?",
                status="clear",
                answer="I loved her a lot.",
            ),
        ),
        max_clarifications=6,
    )
    assert result.audit.clarifications[0].source_field_id == "eros"
    assert "romantically in love" in result.audit.clarifications[0].prompt
