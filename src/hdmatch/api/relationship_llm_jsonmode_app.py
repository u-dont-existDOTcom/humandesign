"""OpenRouter JSON-mode compatibility wrapper for the relationship LLM pilot.

The core chart-blind auditor remains unchanged. This wrapper swaps only the
provider response-format transport from strict JSON Schema to JSON object mode,
then relies on the existing Pydantic validation and identity checks.
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Mapping, Sequence
from typing import Any, cast

from fastapi import FastAPI

import hdmatch.api.relationship_adaptive_app as adaptive_app
from hdmatch.relationship.llm_audit import (
    LLMAuditProviderError,
    LLMAuditUnavailableError,
    LLMProviderReceipt,
    OpenRouterRelationshipAuditor,
)

_LOG = logging.getLogger(__name__)


class JsonModeOpenRouterRelationshipAuditor(OpenRouterRelationshipAuditor):
    """OpenRouter auditor using broadly compatible JSON-object response mode."""

    def _call_json(
        self,
        *,
        schema_name: str,
        schema: Mapping[str, Any],
        messages: Sequence[Mapping[str, str]],
        max_tokens: int,
    ) -> tuple[dict[str, Any], LLMProviderReceipt]:
        del schema_name, schema
        if not self.api_key:
            raise LLMAuditUnavailableError(
                "LLM auditor is not configured; add OPENROUTER_API_KEY on the server"
            )
        body_obj = {
            "model": self.model,
            "messages": [dict(message) for message in messages],
            "max_tokens": max_tokens,
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "Relationship X-Ray",
        }
        body = json.dumps(body_obj, ensure_ascii=False, separators=(",", ":")).encode()
        try:
            raw = self._transport(self.endpoint, body, headers, self.timeout_seconds)
        except LLMAuditProviderError as exc:
            _LOG.error("OpenRouter relationship audit failed: %s", str(exc)[:1000])
            raise
        raw_hash = hashlib.sha256(raw).hexdigest()
        try:
            envelope_raw: Any = json.loads(raw.decode())
            envelope = cast(dict[str, Any], envelope_raw)
            choices = cast(list[dict[str, Any]], envelope["choices"])
            message = cast(dict[str, Any], choices[0]["message"])
            content_raw = message["content"]
            if isinstance(content_raw, str):
                content = content_raw
            elif isinstance(content_raw, list):
                parts = cast(list[dict[str, Any]], content_raw)
                content = "".join(str(part.get("text", "")) for part in parts)
            else:
                raise TypeError("unexpected message content type")
            parsed_raw: Any = json.loads(content)
            parsed = cast(dict[str, Any], parsed_raw)
        except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise LLMAuditProviderError("LLM provider returned invalid JSON output") from exc
        receipt = LLMProviderReceipt(
            provider="OpenRouter",
            model=self.model,
            endpoint=self.endpoint,
            raw_response_sha256=raw_hash,
        )
        return parsed, receipt


def create_relationship_llm_jsonmode_app_from_env() -> FastAPI:
    """Build the relationship app with JSON-mode OpenRouter transport."""
    setattr(
        adaptive_app,
        "OpenRouterRelationshipAuditor",
        JsonModeOpenRouterRelationshipAuditor,
    )
    return adaptive_app.create_relationship_adaptive_app_from_env()
