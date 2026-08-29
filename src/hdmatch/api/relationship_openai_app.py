"""Direct OpenAI Responses API wrapper for the relationship LLM pilot.

The underlying chart-blind prompts, Pydantic validation, field-identity checks, and
freeze semantics remain in ``relationship_adaptive_app`` / ``llm_audit``. This
module changes only the provider transport: participant questionnaire text is sent
directly to OpenAI's Responses API using Structured Outputs.
"""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Mapping, Sequence
from typing import Any, cast

from fastapi import FastAPI

import hdmatch.api.relationship_adaptive_app as adaptive_app
from hdmatch.api.relationship_openai_ui import HTML as OPENAI_HTML
from hdmatch.relationship.llm_audit import (
    LLM_AUDIT_VERSION,
    LLMAuditProviderError,
    LLMAuditUnavailableError,
    LLMProviderReceipt,
    OpenRouterRelationshipAuditor,
)

DEFAULT_OPENAI_ENDPOINT = "https://api.openai.com/v1/responses"
DEFAULT_OPENAI_MODEL = "gpt-5.6-sol"


class OpenAIResponsesRelationshipAuditor(OpenRouterRelationshipAuditor):
    """Chart-blind relationship auditor using OpenAI's Responses API directly."""

    @classmethod
    def from_env(cls) -> OpenAIResponsesRelationshipAuditor:
        key = os.environ.get("HDMATCH_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
        model = os.environ.get("HDMATCH_LLM_MODEL", DEFAULT_OPENAI_MODEL).strip()
        endpoint = os.environ.get("HDMATCH_LLM_API_URL", DEFAULT_OPENAI_ENDPOINT).strip()
        timeout_text = os.environ.get("HDMATCH_LLM_TIMEOUT_SECONDS", "60")
        try:
            timeout = float(timeout_text)
        except ValueError as exc:
            raise ValueError("HDMATCH_LLM_TIMEOUT_SECONDS must be numeric") from exc
        return cls(api_key=key, model=model, endpoint=endpoint, timeout_seconds=timeout)

    def public_configuration(self) -> dict[str, Any]:
        return {
            "configured": self.available,
            "provider": "OpenAI",
            "model": self.model,
            "audit_version": LLM_AUDIT_VERSION,
        }

    def _call_json(
        self,
        *,
        schema_name: str,
        schema: Mapping[str, Any],
        messages: Sequence[Mapping[str, str]],
        max_tokens: int,
    ) -> tuple[dict[str, Any], LLMProviderReceipt]:
        if not self.api_key:
            raise LLMAuditUnavailableError(
                "LLM auditor is not configured; add OPENAI_API_KEY on the server"
            )

        instructions = "\n\n".join(
            str(message["content"])
            for message in messages
            if message.get("role") in {"system", "developer"}
        )
        input_messages = [
            {"role": str(message.get("role", "user")), "content": str(message["content"])}
            for message in messages
            if message.get("role") not in {"system", "developer"}
        ]
        body_obj: dict[str, Any] = {
            "model": self.model,
            "input": input_messages,
            "max_output_tokens": max_tokens,
            "store": False,
            "reasoning": {"effort": "low"},
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "strict": True,
                    "schema": dict(schema),
                }
            },
        }
        if instructions:
            body_obj["instructions"] = instructions

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = json.dumps(body_obj, ensure_ascii=False, separators=(",", ":")).encode()
        raw = self._transport(self.endpoint, body, headers, self.timeout_seconds)
        raw_hash = hashlib.sha256(raw).hexdigest()

        try:
            envelope_raw: Any = json.loads(raw.decode())
            envelope = cast(dict[str, Any], envelope_raw)
            if envelope.get("error"):
                raise LLMAuditProviderError("OpenAI returned an error response")
            content = _response_output_text(envelope)
            parsed_raw: Any = json.loads(content)
            parsed = cast(dict[str, Any], parsed_raw)
        except LLMAuditProviderError:
            raise
        except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise LLMAuditProviderError("OpenAI returned invalid structured output") from exc

        receipt = LLMProviderReceipt(
            provider="OpenAI",
            model=self.model,
            endpoint=self.endpoint,
            raw_response_sha256=raw_hash,
        )
        return parsed, receipt


def _response_output_text(envelope: Mapping[str, Any]) -> str:
    direct = envelope.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct

    parts: list[str] = []
    for item_raw in cast(list[dict[str, Any]], envelope.get("output", [])):
        if item_raw.get("type") != "message":
            continue
        for content_raw in cast(list[dict[str, Any]], item_raw.get("content", [])):
            if content_raw.get("type") == "refusal":
                raise LLMAuditProviderError("OpenAI refused the relationship-audit request")
            if content_raw.get("type") == "output_text":
                text = content_raw.get("text")
                if isinstance(text, str):
                    parts.append(text)
    content = "".join(parts).strip()
    if not content:
        raise LLMAuditProviderError("OpenAI response contained no output text")
    return content


def create_relationship_openai_app_from_env() -> FastAPI:
    """Build the relationship app with direct OpenAI Responses API transport."""
    adaptive_app.OpenRouterRelationshipAuditor = OpenAIResponsesRelationshipAuditor
    adaptive_app.ADAPTIVE_HTML = OPENAI_HTML
    app = adaptive_app.create_relationship_adaptive_app_from_env()
    app.title = "Relationship Pattern Lab"
    app.version = "0.5.0"
    return app
