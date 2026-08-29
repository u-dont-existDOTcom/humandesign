"""Chart-blind LLM auditor for participant relationship answers.

The auditor receives only questionnaire semantics plus participant responses. It must
never receive birth data, charts, candidate identities, AstroRRF predictions, or model
fit. OpenRouter is used through its OpenAI-compatible chat-completions endpoint with
strict JSON-schema output.
"""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Literal, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request as URLRequest
from urllib.request import urlopen

from pydantic import BaseModel, ConfigDict, Field

FieldStatus = Literal["clear", "mixed", "context_dependent", "unknown", "not_applicable"]
LLM_AUDIT_VERSION = "relationship-llm-auditor-v1"
DEFAULT_OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_OPENROUTER_MODEL = "openai/gpt-5.6-sol"


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class FieldAuditInput(_FrozenModel):
    question_id: str = Field(min_length=1)
    question_title: str = Field(min_length=1)
    field_id: str = Field(min_length=1)
    field_label: str = Field(min_length=1)
    field_hint: str = ""
    status: FieldStatus
    answer: str = ""
    clarification: str = ""


class LLMFieldQuality(_FrozenModel):
    score: int = Field(ge=0, le=100)
    feedback: str = Field(min_length=1, max_length=500)
    needs_clarification: bool
    reason_code: str = Field(min_length=1, max_length=80)


class LLMFieldQualityRecord(_FrozenModel):
    question_id: str = Field(min_length=1)
    field_id: str = Field(min_length=1)
    score: int = Field(ge=0, le=100)
    feedback: str = Field(min_length=1, max_length=500)
    needs_clarification: bool
    reason_code: str = Field(min_length=1, max_length=80)


class LLMClarificationDraft(_FrozenModel):
    source_question_id: str = Field(min_length=1)
    source_field_id: str = Field(min_length=1)
    reason: str = Field(min_length=1, max_length=500)
    prompt: str = Field(min_length=1, max_length=800)
    priority: int = Field(ge=1, le=100)


class LLMSessionAudit(_FrozenModel):
    field_quality: tuple[LLMFieldQualityRecord, ...]
    clarifications: tuple[LLMClarificationDraft, ...]


class LLMClarificationItem(_FrozenModel):
    id: str = Field(min_length=1)
    source_question_id: str = Field(min_length=1)
    source_field_id: str = Field(min_length=1)
    source_label: str = Field(min_length=1)
    source_answer_excerpt: str
    reason: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    priority: int = Field(ge=1, le=100)
    audit_version: str = LLM_AUDIT_VERSION


class LLMProviderReceipt(_FrozenModel):
    provider: str
    model: str
    endpoint: str
    audit_version: str = LLM_AUDIT_VERSION
    raw_response_sha256: str


class LLMFieldQualityResult(_FrozenModel):
    quality: LLMFieldQuality
    receipt: LLMProviderReceipt


class LLMSessionAuditResult(_FrozenModel):
    audit: LLMSessionAudit
    receipt: LLMProviderReceipt


class LLMAuditUnavailableError(RuntimeError):
    """Raised when no server-side LLM credential has been configured."""


class LLMAuditProviderError(RuntimeError):
    """Raised when the configured provider fails or returns invalid structured output."""


Transport = Callable[[str, bytes, Mapping[str, str], float], bytes]


_FIELD_SYSTEM = """You are a chart-blind relationship-research answer auditor.
You receive ONE exact questionnaire field and the participant's answer. You do NOT
receive astrology, Human Design, birth data, chart predictions, candidate identity, or
model fit. Never infer or optimize toward any chart.

Score answer QUALITY, not length, eloquence, positivity, or relationship quality.
- 0-15: off-topic, random, incoherent, evasive, or does not answer the field.
- 20-55: partly relevant but materially ambiguous or missing the requested distinction.
- 60-79: usable but could be more precise.
- 80-100: directly answers the exact construct with enough precision to classify.
A very short answer can score highly when the field only needs a simple degree/fact.
Random fluent-looking text must stay near zero. Do not reward word count.
For claims about the other person's internal state, distinguish direct evidence from
inference. Preserve unknown and context-dependent states. Keep love vs being in love,
physical attraction vs sexual chemistry, general libido vs desire for this partner,
communication quality vs amount, reasoning compatibility vs stimulation, drama vs
hostility, and sexual vs romantic-priority jealousy separate.
Return only the required JSON object."""

_SESSION_SYSTEM = """You are the final chart-blind evidence auditor for a relationship
research questionnaire. You receive questionnaire field definitions and the
participant's frozen pre-chart answers. You receive NO birth data, astrology, Human
Design, candidate identity, AstroRRF prediction, or model-fit information. Never infer
or optimize toward any chart.

Your job is to find answer-quality failures that would force a human analyst to guess.
Do not reward verbosity. Random/off-topic/incoherent content must receive very low
quality scores even if long. Concise direct answers are valid. Preserve genuine
unknowns. For partner-internal states, require direct statements/behavior or label the
inference limitation. Keep the frozen construct distinctions separate.

Return one quality record for EVERY supplied field, using the exact supplied
question_id and field_id. Then propose at most the requested number of clarifications.
Ask a clarification only when it materially improves interpretability. Each
clarification must be standalone and specific: say what is unclear and ask exactly what
distinction/evidence is needed. Never use a generic prompt such as 'add an example'
without naming what the example must establish. Do not ask the respondent to change an
answer; only to clarify it. Return only the required JSON object."""


def _field_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["score", "feedback", "needs_clarification", "reason_code"],
        "properties": {
            "score": {"type": "integer", "minimum": 0, "maximum": 100},
            "feedback": {"type": "string", "minLength": 1, "maxLength": 500},
            "needs_clarification": {"type": "boolean"},
            "reason_code": {"type": "string", "minLength": 1, "maxLength": 80},
        },
    }


def _session_schema() -> dict[str, Any]:
    quality_item = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "question_id",
            "field_id",
            "score",
            "feedback",
            "needs_clarification",
            "reason_code",
        ],
        "properties": {
            "question_id": {"type": "string", "minLength": 1},
            "field_id": {"type": "string", "minLength": 1},
            "score": {"type": "integer", "minimum": 0, "maximum": 100},
            "feedback": {"type": "string", "minLength": 1, "maxLength": 500},
            "needs_clarification": {"type": "boolean"},
            "reason_code": {"type": "string", "minLength": 1, "maxLength": 80},
        },
    }
    clarification_item = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "source_question_id",
            "source_field_id",
            "reason",
            "prompt",
            "priority",
        ],
        "properties": {
            "source_question_id": {"type": "string", "minLength": 1},
            "source_field_id": {"type": "string", "minLength": 1},
            "reason": {"type": "string", "minLength": 1, "maxLength": 500},
            "prompt": {"type": "string", "minLength": 1, "maxLength": 800},
            "priority": {"type": "integer", "minimum": 1, "maximum": 100},
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["field_quality", "clarifications"],
        "properties": {
            "field_quality": {"type": "array", "items": quality_item},
            "clarifications": {"type": "array", "items": clarification_item},
        },
    }


def _default_transport(
    url: str,
    body: bytes,
    headers: Mapping[str, str],
    timeout: float,
) -> bytes:
    request = URLRequest(url, data=body, headers=dict(headers), method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - configured HTTPS API
            return cast(bytes, response.read())
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        raise LLMAuditProviderError(f"LLM provider HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise LLMAuditProviderError(f"LLM provider network error: {exc.reason}") from exc


class OpenRouterRelationshipAuditor:
    """Small OpenRouter client with strict chart-blind structured-output prompts."""

    def __init__(
        self,
        *,
        api_key: str | None,
        model: str = DEFAULT_OPENROUTER_MODEL,
        endpoint: str = DEFAULT_OPENROUTER_ENDPOINT,
        timeout_seconds: float = 45.0,
        transport: Transport | None = None,
    ) -> None:
        self.api_key = api_key.strip() if api_key else None
        self.model = model
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds
        self._transport = transport or _default_transport

    @classmethod
    def from_env(cls) -> OpenRouterRelationshipAuditor:
        key = os.environ.get("HDMATCH_LLM_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
        model = os.environ.get("HDMATCH_LLM_MODEL", DEFAULT_OPENROUTER_MODEL).strip()
        endpoint = os.environ.get("HDMATCH_LLM_API_URL", DEFAULT_OPENROUTER_ENDPOINT).strip()
        timeout_text = os.environ.get("HDMATCH_LLM_TIMEOUT_SECONDS", "45")
        try:
            timeout = float(timeout_text)
        except ValueError as exc:
            raise ValueError("HDMATCH_LLM_TIMEOUT_SECONDS must be numeric") from exc
        return cls(api_key=key, model=model, endpoint=endpoint, timeout_seconds=timeout)

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def public_configuration(self) -> dict[str, Any]:
        return {
            "configured": self.available,
            "provider": "OpenRouter",
            "model": self.model,
            "audit_version": LLM_AUDIT_VERSION,
        }

    def assess_field(self, field: FieldAuditInput) -> LLMFieldQualityResult:
        if field.status in {"unknown", "not_applicable"}:
            quality = LLMFieldQuality(
                score=100,
                feedback="Explicit unknown/not-applicable is a complete response when accurate.",
                needs_clarification=False,
                reason_code="explicit_unknown",
            )
            receipt = LLMProviderReceipt(
                provider="local-explicit-unknown",
                model="none",
                endpoint="none",
                raw_response_sha256=hashlib.sha256(b"explicit_unknown").hexdigest(),
            )
            return LLMFieldQualityResult(quality=quality, receipt=receipt)

        prompt = json.dumps(field.model_dump(), ensure_ascii=False, sort_keys=True)
        parsed, receipt = self._call_json(
            schema_name="relationship_field_quality",
            schema=_field_schema(),
            messages=[
                {"role": "system", "content": _FIELD_SYSTEM},
                {"role": "user", "content": prompt},
            ],
            max_tokens=350,
        )
        return LLMFieldQualityResult(
            quality=LLMFieldQuality.model_validate(parsed),
            receipt=receipt,
        )

    def audit_session(
        self,
        fields: Sequence[FieldAuditInput],
        *,
        max_clarifications: int,
        prior_clarifications: Sequence[Mapping[str, Any]] = (),
    ) -> LLMSessionAuditResult:
        if max_clarifications < 0:
            raise ValueError("max_clarifications must be non-negative")
        payload = {
            "max_clarifications": max_clarifications,
            "fields": [field.model_dump() for field in fields],
            "prior_clarifications": [dict(item) for item in prior_clarifications],
        }
        parsed, receipt = self._call_json(
            schema_name="relationship_session_audit",
            schema=_session_schema(),
            messages=[
                {"role": "system", "content": _SESSION_SYSTEM},
                {
                    "role": "user",
                    "content": json.dumps(payload, ensure_ascii=False, sort_keys=True),
                },
            ],
            max_tokens=5000,
        )
        audit = LLMSessionAudit.model_validate(parsed)
        supplied = {(field.question_id, field.field_id) for field in fields}
        returned = {(row.question_id, row.field_id) for row in audit.field_quality}
        if returned != supplied or len(audit.field_quality) != len(supplied):
            raise LLMAuditProviderError(
                "LLM field-quality output did not exactly cover the supplied field identities"
            )
        for item in audit.clarifications:
            if (item.source_question_id, item.source_field_id) not in supplied:
                raise LLMAuditProviderError("LLM clarification referenced an unknown field")
        if len(audit.clarifications) > max_clarifications:
            audit = audit.model_copy(update={"clarifications": audit.clarifications[:max_clarifications]})
        return LLMSessionAuditResult(audit=audit, receipt=receipt)

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
                "LLM auditor is not configured; add OPENROUTER_API_KEY on the server"
            )
        body_obj = {
            "model": self.model,
            "messages": [dict(message) for message in messages],
            "max_tokens": max_tokens,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": schema_name,
                    "strict": True,
                    "schema": dict(schema),
                },
            },
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "Relationship X-Ray",
        }
        body = json.dumps(body_obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        raw = self._transport(self.endpoint, body, headers, self.timeout_seconds)
        raw_hash = hashlib.sha256(raw).hexdigest()
        try:
            envelope_raw: Any = json.loads(raw.decode("utf-8"))
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
            raise LLMAuditProviderError("LLM provider returned invalid structured output") from exc
        receipt = LLMProviderReceipt(
            provider="OpenRouter",
            model=self.model,
            endpoint=self.endpoint,
            raw_response_sha256=raw_hash,
        )
        return parsed, receipt
