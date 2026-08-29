from __future__ import annotations

import json
from collections.abc import Mapping

from hdmatch.api.relationship_llm_jsonmode_app import JsonModeOpenRouterRelationshipAuditor
from hdmatch.relationship.llm_audit import FieldAuditInput


def test_jsonmode_auditor_uses_json_object_response_format() -> None:
    captured: dict[str, object] = {}

    def transport(url: str, body: bytes, headers: Mapping[str, str], timeout: float) -> bytes:
        captured["url"] = url
        captured["body"] = json.loads(body.decode())
        captured["headers"] = dict(headers)
        captured["timeout"] = timeout
        content = json.dumps(
            {
                "score": 4,
                "feedback": "This is off-topic and does not provide the relationship timeline.",
                "needs_clarification": True,
                "reason_code": "off_topic",
            }
        )
        return json.dumps({"choices": [{"message": {"content": content}}]}).encode()

    auditor = JsonModeOpenRouterRelationshipAuditor(
        api_key="test-key",
        model="openai/gpt-test",
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
    assert isinstance(request_body, dict)
    assert request_body["response_format"] == {"type": "json_object"}
    assert "json_schema" not in request_body["response_format"]
    assert result.quality.score == 4
    assert result.quality.needs_clarification is True
