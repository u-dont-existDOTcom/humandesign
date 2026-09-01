"""Direct-OpenAI chart-blind relationship phenotype classifier."""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request as URLRequest
from urllib.request import urlopen

from .phenotype import (
    VALIDATION_CONTRACT_SHA256,
    VALIDATION_CONTRACT_VERSION,
    AxisScope,
    PhenotypeProviderReceipt,
    RelationshipPhenotypeFreeze,
    RelationshipPhenotypeOutput,
    response_record_sha256,
    source_text_corpus,
    validate_phenotype_output,
)
from .study import file_sha256

DEFAULT_OPENAI_ENDPOINT = "https://api.openai.com/v1/responses"
DEFAULT_CLASSIFIER_MODEL = "gpt-5.6-sol"
MINIMUM_CONFIDENCE = 0.65

Transport = Callable[[str, bytes, Mapping[str, str], float], bytes]

_SYSTEM = """You are a chart-blind evidence classifier for a relationship research study.
You classify the participant's relationship narrative into ONLY the supplied frozen
phenotype axes. You receive no birth data, astrology, Human Design, synastry,
AstroRRF predictions, candidate identity, rank, or model fit. Never infer toward any
astrological result.

Obey the supplied classifier protocol and rubric literally. Keep actor directions and
constructs separate. Preserve mixed, insufficient-evidence, unclassifiable, unknown,
and context/state-dependent outcomes. Do not infer another person's internal state from
the respondent's assumption without direct statements or behavior. Do not infer libido
from constrained behavior. Do not merge attraction, sexual desire, chemistry, Eros,
love, commitment, intellectual compatibility, stimulation, communication amount,
drama, conflict, or the two jealousy types.

Evidence and counterevidence spans MUST be short exact verbatim substrings copied from
the supplied participant responses. Do not paraphrase evidence spans. A classified
ordinal result must meet the frozen minimum confidence. Otherwise return an unresolved
status instead of forcing a choice. For each question, return only its declared target
axes and use only directions permitted by each rubric scope: directional axes use
a_to_b/b_to_a, dyadic axes use dyadic, and person axes use person_a/person_b. Return
only the required JSON object."""


def _output_schema() -> dict[str, Any]:
    axis = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "axis_id",
            "direction",
            "status",
            "ordinal_value",
            "trajectory",
            "confidence",
            "evidence_spans",
            "counterevidence_spans",
            "context_conditions",
            "observability_limits",
            "forced_choice",
        ],
        "properties": {
            "axis_id": {"type": "string", "minLength": 1},
            "direction": {
                "type": "string",
                "enum": ["a_to_b", "b_to_a", "dyadic", "person_a", "person_b"],
            },
            "status": {
                "type": "string",
                "enum": [
                    "classified",
                    "mixed",
                    "other",
                    "insufficient_evidence",
                    "unclassifiable",
                    "not_applicable",
                ],
            },
            "ordinal_value": {
                "anyOf": [
                    {
                        "type": "string",
                        "enum": ["very_low", "low", "moderate", "high", "very_high"],
                    },
                    {"type": "null"},
                ]
            },
            "trajectory": {
                "anyOf": [
                    {
                        "type": "string",
                        "enum": [
                            "stable",
                            "gradual_increase",
                            "gradual_decrease",
                            "rapid_increase",
                            "rapid_decrease",
                            "cyclical",
                            "novelty_reset",
                            "state_conditional",
                            "unknown",
                        ],
                    },
                    {"type": "null"},
                ]
            },
            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "evidence_spans": {"type": "array", "items": {"type": "string"}},
            "counterevidence_spans": {"type": "array", "items": {"type": "string"}},
            "context_conditions": {"type": "array", "items": {"type": "string"}},
            "observability_limits": {"type": "array", "items": {"type": "string"}},
            "forced_choice": {"type": "boolean", "enum": [False]},
        },
    }
    question = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "question_id",
            "axis_results",
            "applicability_flags",
            "unresolved_axis_ids",
            "verbatim_preserved",
        ],
        "properties": {
            "question_id": {"type": "string", "minLength": 1},
            "axis_results": {"type": "array", "items": axis},
            "applicability_flags": {"type": "array", "items": {"type": "string"}},
            "unresolved_axis_ids": {"type": "array", "items": {"type": "string"}},
            "verbatim_preserved": {"type": "boolean", "enum": [True]},
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["question_results"],
        "properties": {"question_results": {"type": "array", "items": question}},
    }


def _default_transport(
    url: str,
    body: bytes,
    headers: Mapping[str, str],
    timeout: float,
) -> bytes:
    request = URLRequest(url, data=body, headers=dict(headers), method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed HTTPS API
            return cast(bytes, response.read())
    except HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:1000]
        raise RuntimeError(f"OpenAI phenotype classifier HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"OpenAI phenotype classifier network error: {exc.reason}") from exc


class OpenAIRelationshipPhenotypeClassifier:
    def __init__(
        self,
        *,
        api_key: str | None,
        model: str = DEFAULT_CLASSIFIER_MODEL,
        endpoint: str = DEFAULT_OPENAI_ENDPOINT,
        timeout_seconds: float = 90.0,
        transport: Transport | None = None,
    ) -> None:
        self.api_key = api_key.strip() if api_key else None
        self.model = model
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds
        self._transport = transport or _default_transport

    @classmethod
    def from_env(cls) -> OpenAIRelationshipPhenotypeClassifier:
        return cls(
            api_key=os.environ.get("HDMATCH_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY"),
            model=os.environ.get("HDMATCH_PHENOTYPE_MODEL", DEFAULT_CLASSIFIER_MODEL).strip(),
            endpoint=os.environ.get("HDMATCH_LLM_API_URL", DEFAULT_OPENAI_ENDPOINT).strip(),
            timeout_seconds=float(os.environ.get("HDMATCH_PHENOTYPE_TIMEOUT_SECONDS", "90")),
        )

    def classify_and_freeze(
        self,
        *,
        session_id: str,
        answers: list[dict[str, Any]],
        semantic_audit: dict[str, Any],
        questionnaire_path: Path,
        rubric_path: Path,
        protocol_path: Path,
    ) -> RelationshipPhenotypeFreeze:
        if not self.api_key:
            raise RuntimeError("OpenAI phenotype classifier is not configured")
        questionnaire = _load_json_object(questionnaire_path)
        rubric = _load_json_object(rubric_path)
        protocol = _load_json_object(protocol_path)
        submitted_question_rows = [row.get("question_id") for row in answers]
        if not submitted_question_rows or not all(
            isinstance(question_id, str) and question_id for question_id in submitted_question_rows
        ):
            raise ValueError("participant answers require nonempty question ids")
        submitted_question_ids = set(cast(list[str], submitted_question_rows))
        if len(submitted_question_ids) != len(submitted_question_rows):
            raise ValueError("participant answers contain duplicate question ids")
        axis_scopes = _axis_scope_registry(rubric)
        allowed_axis_ids = set(axis_scopes)
        question_target_axis_ids = _question_target_registry(
            questionnaire,
            allowed_axis_ids=allowed_axis_ids,
        )
        if not submitted_question_ids <= set(question_target_axis_ids):
            raise ValueError("participant answers contain an unknown question id")
        classifier_payload = {
            "minimum_confidence": MINIMUM_CONFIDENCE,
            "classifier_protocol": protocol,
            "outcome_rubric": rubric,
            "questionnaire": {
                "schema_version": questionnaire.get("schema_version"),
                "questions": questionnaire.get("questions", []),
            },
            "participant_response_record": {
                "answers": answers,
                "semantic_clarification_queue": semantic_audit.get("queue", []),
                "semantic_clarification_answers": semantic_audit.get("answers", []),
            },
        }
        raw = self._call(classifier_payload)
        raw_hash = hashlib.sha256(raw).hexdigest()
        parsed = _parse_openai_json(raw)
        output = RelationshipPhenotypeOutput.model_validate(parsed)
        validated = validate_phenotype_output(
            output,
            submitted_question_ids=submitted_question_ids,
            allowed_axis_ids=allowed_axis_ids,
            question_target_axis_ids=question_target_axis_ids,
            axis_scopes=axis_scopes,
            source_texts_by_question=source_text_corpus(answers, semantic_audit),
            minimum_confidence=MINIMUM_CONFIDENCE,
        )
        return RelationshipPhenotypeFreeze(
            validation_contract_version=VALIDATION_CONTRACT_VERSION,
            validation_contract_sha256=VALIDATION_CONTRACT_SHA256,
            session_id=session_id,
            created_at_utc=datetime.now(UTC),
            response_record_sha256=response_record_sha256(answers, semantic_audit),
            questionnaire_sha256=file_sha256(questionnaire_path),
            rubric_sha256=file_sha256(rubric_path),
            classifier_protocol_sha256=file_sha256(protocol_path),
            classifier_model=self.model,
            minimum_confidence=MINIMUM_CONFIDENCE,
            provider_receipt=PhenotypeProviderReceipt(
                model=self.model,
                endpoint=self.endpoint,
                raw_response_sha256=raw_hash,
            ),
            output=validated,
        )

    def _call(self, payload: dict[str, Any]) -> bytes:
        body_obj = {
            "model": self.model,
            "instructions": _SYSTEM,
            "input": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            "store": False,
            "reasoning": {"effort": "low"},
            "max_output_tokens": 12000,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "relationship_phenotype_v1",
                    "strict": True,
                    "schema": _output_schema(),
                }
            },
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        return self._transport(
            self.endpoint,
            json.dumps(body_obj, ensure_ascii=False, separators=(",", ":")).encode(),
            headers,
            self.timeout_seconds,
        )


def _load_json_object(path: Path) -> dict[str, Any]:
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"expected JSON object: {path}")
    return cast(dict[str, Any], raw)


def _axis_scope_registry(rubric: dict[str, Any]) -> dict[str, AxisScope]:
    rows = rubric.get("axes")
    if not isinstance(rows, list):
        raise ValueError("relationship outcome rubric axes must be a list")
    registry: dict[str, AxisScope] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("relationship outcome rubric axes must be objects")
        axis_id = row.get("id")
        scope = row.get("scope")
        if not isinstance(axis_id, str) or not axis_id:
            raise ValueError("relationship outcome rubric contains an invalid axis id")
        if scope not in {"directional", "dyadic", "person"}:
            raise ValueError("relationship outcome rubric contains an invalid axis scope")
        if axis_id in registry:
            raise ValueError("relationship outcome rubric contains duplicate axis ids")
        registry[axis_id] = cast(AxisScope, scope)
    return registry


def _question_target_registry(
    questionnaire: dict[str, Any],
    *,
    allowed_axis_ids: set[str],
) -> dict[str, set[str]]:
    rows = questionnaire.get("questions")
    if not isinstance(rows, list):
        raise ValueError("relationship questionnaire questions must be a list")
    registry: dict[str, set[str]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("relationship questionnaire questions must be objects")
        question_id = row.get("id")
        targets = row.get("target_axes")
        if not isinstance(question_id, str) or not question_id:
            raise ValueError("relationship questionnaire contains an invalid question id")
        if question_id in registry:
            raise ValueError("relationship questionnaire contains duplicate question ids")
        if not isinstance(targets, list) or not all(
            isinstance(axis_id, str) and axis_id for axis_id in targets
        ):
            raise ValueError("relationship questionnaire target_axes must be a string list")
        target_ids = cast(list[str], targets)
        if len(target_ids) != len(set(target_ids)):
            raise ValueError("relationship questionnaire contains duplicate target axes")
        unknown = set(target_ids) - allowed_axis_ids
        if unknown:
            raise ValueError(f"relationship questionnaire targets unknown axes: {sorted(unknown)}")
        registry[question_id] = set(target_ids)
    return registry


def _parse_openai_json(raw: bytes) -> dict[str, Any]:
    try:
        envelope_raw: Any = json.loads(raw.decode())
        envelope = cast(dict[str, Any], envelope_raw)
        output = cast(list[dict[str, Any]], envelope.get("output", []))
        texts: list[str] = []
        for item in output:
            if item.get("type") != "message":
                continue
            for content in cast(list[dict[str, Any]], item.get("content", [])):
                if content.get("type") == "refusal":
                    raise RuntimeError("OpenAI refused the phenotype classification request")
                if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                    texts.append(str(content["text"]))
        if not texts and isinstance(envelope.get("output_text"), str):
            texts.append(str(envelope["output_text"]))
        if not texts:
            raise ValueError("no OpenAI output text")
        parsed_raw: Any = json.loads("".join(texts))
        if not isinstance(parsed_raw, dict):
            raise ValueError("classifier output must be a JSON object")
        return cast(dict[str, Any], parsed_raw)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError("OpenAI returned invalid phenotype structured output") from exc
