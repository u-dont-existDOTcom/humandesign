from __future__ import annotations

import json
from collections.abc import Mapping

from hdmatch.api.relationship_openai_app import OpenAIResponsesRelationshipAuditor
from hdmatch.api.relationship_openai_ui import HTML
from hdmatch.relationship.llm_audit import FieldAuditInput


def test_openai_auditor_uses_responses_structured_outputs() -> None:
    captured: dict[str, object] = {}

    def transport(url: str, body: bytes, headers: Mapping[str, str], timeout: float) -> bytes:
        captured["url"] = url
        captured["body"] = json.loads(body.decode())
        captured["headers"] = dict(headers)
        captured["timeout"] = timeout
        output = json.dumps(
            {
                "score": 3,
                "feedback": "This is random/off-topic and does not provide a relationship timeline.",
                "needs_clarification": True,
                "reason_code": "off_topic",
            }
        )
        return json.dumps(
            {
                "id": "resp_test",
                "object": "response",
                "status": "completed",
                "output": [
                    {
                        "type": "message",
                        "content": [{"type": "output_text", "text": output}],
                    }
                ],
            }
        ).encode()

    auditor = OpenAIResponsesRelationshipAuditor(
        api_key="test-key",
        model="gpt-5.6-sol",
        endpoint="https://api.openai.com/v1/responses",
        transport=transport,
    )
    result = auditor.assess_field(
        FieldAuditInput(
            question_id="RRQ_TRAJECTORY_CONTEXT",
            question_title="Relationship timeline & context",
            field_id="relationship_timeline",
            field_label="What was the romantic timeline of the relationship?",
            field_hint="When it became romantic, roughly how long that lasted, and what it is now.",
            status="clear",
            answer="peas carrots farting ice cream nonsense",
            clarification="",
        )
    )

    request_body = captured["body"]
    headers = captured["headers"]
    assert isinstance(request_body, dict)
    assert isinstance(headers, dict)
    assert captured["url"] == "https://api.openai.com/v1/responses"
    assert request_body["model"] == "gpt-5.6-sol"
    assert request_body["store"] is False
    assert request_body["max_output_tokens"] == 350
    assert request_body["reasoning"] == {"effort": "low"}
    assert request_body["text"]["format"]["type"] == "json_schema"
    assert request_body["text"]["format"]["name"] == "relationship_field_quality"
    assert request_body["text"]["format"]["strict"] is True
    assert "response_format" not in request_body
    assert headers["Authorization"] == "Bearer test-key"
    assert result.receipt.provider == "OpenAI"
    assert result.quality.score == 3
    assert result.quality.needs_clarification is True


def test_openai_ui_explains_scientific_and_participant_payoff() -> None:
    assert "Relationship Pattern Lab" in HTML
    assert "blind astrology &amp; Human Design relationship study" in HTML
    assert "structured map of one real relationship" in HTML
    assert "what the blinded system predicted well, what it missed" in HTML
    assert "prospectively checking likely relationship dynamics" in HTML
    assert "testing that possibility, not assuming it" in HTML
    assert "OpenAI's API" in HTML
    assert "OpenRouter" not in HTML
