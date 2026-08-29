"""Post-survey phenotype freeze and reveal for the confirmatory relationship study."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from hdmatch.api.relationship_public_app import RelationshipFileStore
from hdmatch.api.relationship_study_app import create_relationship_study_app_from_env
from hdmatch.relationship.phenotype import RelationshipPhenotypeFreeze
from hdmatch.relationship.phenotype_classifier import OpenAIRelationshipPhenotypeClassifier
from hdmatch.relationship.reveal import conservative_prediction_reveal, relationship_fingerprint
from hdmatch.relationship.study import RelationshipPredictionFreeze


class StudyTokenRequest(BaseModel):
    token: str


def create_relationship_full_study_app_from_env() -> FastAPI:
    app = create_relationship_study_app_from_env()
    app.title = "Relationship Pattern Lab"
    app.version = "0.7.0"

    store_value = os.environ.get("HDMATCH_RELATIONSHIP_STORE", "").strip()
    if not store_value:
        raise RuntimeError("HDMATCH_RELATIONSHIP_STORE is required")
    store = RelationshipFileStore(Path(store_value))
    root = Path(os.environ.get("HDMATCH_REPO_ROOT", "/app"))
    questionnaire_path = root / "reference/relationship/relationship_dynamic_questionnaire_v1.json"
    rubric_path = root / "reference/relationship/relationship_outcome_rubrics_v1.json"
    protocol_path = root / "reference/relationship/relationship_blind_classifier_protocol_v1.json"
    classifier = OpenAIRelationshipPhenotypeClassifier.from_env()

    @app.post("/api/study/sessions/{session_id}/phenotype-freeze")
    def freeze_phenotype(session_id: str, request: StudyTokenRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        _require_confirmatory_study(payload)
        if payload.get("status") != "frozen":
            raise HTTPException(
                status_code=409,
                detail="questionnaire responses must be frozen before phenotype classification",
            )
        existing = payload.get("phenotype_freeze")
        if isinstance(existing, dict):
            frozen = RelationshipPhenotypeFreeze.model_validate(existing)
            return {
                "status": "frozen",
                "phenotype_freeze_sha256": frozen.freeze_sha256,
                "fingerprint_ready": True,
                "reveal_ready": True,
            }
        prediction_raw = payload.get("prediction_freeze")
        if not isinstance(prediction_raw, dict):
            raise HTTPException(status_code=409, detail="pre-answer prediction freeze is missing")
        prediction = RelationshipPredictionFreeze.model_validate(prediction_raw)
        if not prediction.confirmatory_ready:
            raise HTTPException(status_code=409, detail="pre-answer prediction freeze is incomplete")
        audit = payload.get("semantic_audit")
        if not isinstance(audit, dict):
            raise HTTPException(status_code=409, detail="LLM answer-quality audit is missing")
        if _audit_has_pending_clarifications(audit):
            raise HTTPException(status_code=409, detail="targeted clarifications are incomplete")
        answers = cast(list[dict[str, Any]], payload.get("answers", []))
        if not answers:
            raise HTTPException(status_code=409, detail="relationship answers are missing")
        try:
            phenotype = classifier.classify_and_freeze(
                session_id=session_id,
                answers=answers,
                semantic_audit=audit,
                questionnaire_path=questionnaire_path,
                rubric_path=rubric_path,
                protocol_path=protocol_path,
            )
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(
                status_code=502,
                detail="Chart-blind phenotype classification failed; no reveal was performed.",
            ) from exc
        payload["phenotype_freeze"] = phenotype.model_dump(mode="json")
        payload["phenotype_freeze_sha256"] = phenotype.freeze_sha256
        payload["phenotype_frozen_at"] = datetime.now(UTC).isoformat()
        store.save(payload)
        return {
            "status": "frozen",
            "phenotype_freeze_sha256": phenotype.freeze_sha256,
            "fingerprint_ready": True,
            "reveal_ready": True,
        }

    @app.get("/api/study/sessions/{session_id}/fingerprint")
    def get_fingerprint(session_id: str, token: str) -> dict[str, Any]:
        payload = store.read(session_id, token)
        phenotype = _phenotype_from_payload(payload)
        rubric = _load_json_object(rubric_path)
        return relationship_fingerprint(phenotype, rubric)

    @app.post("/api/study/sessions/{session_id}/reveal")
    def reveal(session_id: str, request: StudyTokenRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        _require_confirmatory_study(payload)
        phenotype = _phenotype_from_payload(payload)
        prediction_raw = payload.get("prediction_freeze")
        if not isinstance(prediction_raw, dict):
            raise HTTPException(status_code=409, detail="pre-answer prediction freeze is missing")
        prediction = RelationshipPredictionFreeze.model_validate(prediction_raw)
        if not prediction.confirmatory_ready:
            raise HTTPException(status_code=409, detail="pre-answer prediction freeze is incomplete")
        if payload.get("revealed_at") is None:
            payload["revealed_at"] = datetime.now(UTC).isoformat()
            payload["reveal_prediction_freeze_sha256"] = prediction.freeze_sha256
            payload["reveal_phenotype_freeze_sha256"] = phenotype.freeze_sha256
            store.save(payload)
        rubric = _load_json_object(rubric_path)
        return {
            "fingerprint": relationship_fingerprint(phenotype, rubric),
            "prediction_reveal": conservative_prediction_reveal(prediction, phenotype),
            "revealed_at": payload["revealed_at"],
        }

    return app


def _require_confirmatory_study(payload: dict[str, Any]) -> None:
    if payload.get("study_schema_version") != "relationship-study-v1":
        raise HTTPException(status_code=409, detail="not a confirmatory relationship study session")


def _phenotype_from_payload(payload: dict[str, Any]) -> RelationshipPhenotypeFreeze:
    raw = payload.get("phenotype_freeze")
    if not isinstance(raw, dict):
        raise HTTPException(status_code=409, detail="chart-blind phenotype is not frozen yet")
    return RelationshipPhenotypeFreeze.model_validate(raw)


def _audit_has_pending_clarifications(audit: dict[str, Any]) -> bool:
    queue = cast(list[dict[str, Any]], audit.get("queue", []))
    answers = cast(list[dict[str, Any]], audit.get("answers", []))
    answered = {str(row.get("clarification_id", "")) for row in answers}
    return any(str(item.get("id", "")) not in answered for item in queue)


def _load_json_object(path: Path) -> dict[str, Any]:
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return cast(dict[str, Any], raw)
