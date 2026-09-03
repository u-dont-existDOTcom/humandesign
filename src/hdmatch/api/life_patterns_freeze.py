"""Participant-reviewed immutable behavioral-profile freezes for Life Patterns.

The live Life Patterns profile remains mutable. A behavioral freeze is a separate,
content-addressed private artifact that preserves the exact chart-blind evidence state,
original synthesis, participant review events, and final participant-endorsed claims.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import UTC, datetime
from typing import Any, Literal, cast

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json, write_new_bytes

from .life_patterns_app import LifePatternsFileStore, LifePatternsMap, PatternStatus

ClaimReviewAction = Literal["approve", "edit", "reject", "uncertain"]


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class FreezeCandidateRequest(BaseModel):
    token: str = Field(min_length=16)


class FreezeClaimReviewRequest(BaseModel):
    token: str = Field(min_length=16)
    action: ClaimReviewAction
    title: str | None = Field(default=None, max_length=160)
    summary: str | None = Field(default=None, max_length=12000)
    status: PatternStatus | None = None
    note: str | None = Field(default=None, max_length=4000)

    @model_validator(mode="after")
    def edited_claim_requires_summary(self) -> FreezeClaimReviewRequest:
        if self.action == "edit" and (self.summary is None or not self.summary.strip()):
            raise ValueError("an edited claim requires corrected summary wording")
        return self


class FinalizeFreezeRequest(BaseModel):
    token: str = Field(min_length=16)
    attest_profile_reviewed: bool
    attest_snapshot_immutable: bool


class FreezeReceipt(_FrozenModel):
    freeze_id: str
    freeze_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    candidate_id: str
    frozen_at_utc: str
    artifact_relpath: str


def _canonical_json(value: Any) -> bytes:
    """Use the repository-wide canonical JSON representation."""

    return canonical_json_bytes(value)


def _sha256_json(value: Any) -> str:
    """Use the repository-wide canonical JSON hash primitive."""

    return sha256_json(value)


def _approved_episodes(payload: dict[str, Any]) -> list[dict[str, Any]]:
    episodes = cast(list[dict[str, Any]], payload.get("episodes", []))
    return [row for row in episodes if row.get("review_status") == "approved"]


def _source_turns(
    payload: dict[str, Any],
    approved: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    wanted = {
        str(turn_id)
        for episode in approved
        for turn_id in cast(list[Any], episode.get("source_turn_ids", []))
        if isinstance(turn_id, str)
    }
    turns = cast(list[dict[str, Any]], payload.get("conversation_turns", []))
    return [
        row
        for row in turns
        if row.get("role") == "user"
        and isinstance(row.get("turn_id"), str)
        and row["turn_id"] in wanted
    ]


def _required_source_turn_ids(approved: list[dict[str, Any]]) -> set[str]:
    return {
        turn_id
        for episode in approved
        for turn_id in cast(list[Any], episode.get("source_turn_ids", []))
        if isinstance(turn_id, str)
    }


def _coverage_snapshot(approved: list[dict[str, Any]]) -> dict[str, Any]:
    domains = (
        "decisions",
        "work_projects",
        "relationships",
        "self_initiated_actions",
        "learning_adaptation",
        "conflict_stress",
        "life_transitions",
    )
    counts = {domain: 0 for domain in domains}
    for episode in approved:
        domain = episode.get("domain")
        if domain in counts:
            counts[cast(str, domain)] += 1
    return {
        "semantics": "descriptive_evidence_coverage_not_completion_denominator",
        "approved_episode_count": len(approved),
        "domain_episode_counts": counts,
    }


def _pattern_claims(life_map: LifePatternsMap) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": pattern.pattern_id,
            "title": pattern.title,
            "summary": pattern.summary,
            "status": pattern.status,
            "synthesis_confidence": pattern.confidence,
            "supporting_episode_ids": list(pattern.supporting_episode_ids),
            "counterexample_episode_ids": list(pattern.counterexample_episode_ids),
            "contexts": list(pattern.contexts),
            "limits": list(pattern.limits),
        }
        for pattern in life_map.patterns
    ]


def _build_candidate_source(payload: dict[str, Any]) -> dict[str, Any]:
    raw_map = payload.get("life_patterns_map")
    if not isinstance(raw_map, dict):
        raise HTTPException(status_code=409, detail="build your current Life Patterns Map first")
    approved = _approved_episodes(payload)
    approved_ids_raw = [row.get("episode_id") for row in approved]
    if not approved_ids_raw or not all(isinstance(value, str) and value for value in approved_ids_raw):
        raise HTTPException(status_code=409, detail="approved episode identities are missing or invalid")
    approved_ids = cast(list[str], approved_ids_raw)
    if len(approved_ids) != len(set(approved_ids)):
        raise HTTPException(status_code=409, detail="approved episode identities are not unique")
    mapped_ids_raw = payload.get("map_approved_episode_ids")
    mapped_ids = (
        cast(list[str], mapped_ids_raw)
        if isinstance(mapped_ids_raw, list)
        and all(isinstance(value, str) for value in mapped_ids_raw)
        else []
    )
    if mapped_ids != approved_ids:
        raise HTTPException(
            status_code=409,
            detail="your Life Patterns Map is older than the approved evidence; rebuild it before review",
        )
    try:
        life_map = LifePatternsMap.model_validate(raw_map)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail="the current Life Patterns Map is invalid") from exc
    claim_ids = [pattern.pattern_id for pattern in life_map.patterns]
    if len(claim_ids) != len(set(claim_ids)):
        raise HTTPException(status_code=409, detail="the current Life Patterns Map repeats a claim id")
    referenced_episode_ids = {
        episode_id
        for pattern in life_map.patterns
        for episode_id in (*pattern.supporting_episode_ids, *pattern.counterexample_episode_ids)
    }
    unknown_episode_ids = referenced_episode_ids - set(approved_ids)
    if unknown_episode_ids:
        raise HTTPException(
            status_code=409,
            detail="the current Life Patterns Map cites evidence outside the approved episode set",
        )
    turns = _source_turns(payload, approved)
    source_turn_ids = [row.get("turn_id") for row in turns]
    if len(source_turn_ids) != len(set(source_turn_ids)):
        raise HTTPException(status_code=409, detail="participant source-turn identities are not unique")
    if set(cast(list[str], source_turn_ids)) != _required_source_turn_ids(approved):
        raise HTTPException(
            status_code=409,
            detail="one or more approved episodes no longer resolve to participant source turns",
        )
    episode_hashes = {
        str(row["episode_id"]): _sha256_json(row)
        for row in approved
        if isinstance(row.get("episode_id"), str)
    }
    turn_hashes = {
        str(row["turn_id"]): _sha256_json(row)
        for row in turns
        if isinstance(row.get("turn_id"), str)
    }
    provider_receipt = payload.get("map_provider_receipt")
    if not isinstance(provider_receipt, dict):
        raise HTTPException(status_code=409, detail="the current map provider receipt is missing")
    return {
        "schema_version": "life-patterns-behavioral-freeze-candidate-source-v1",
        "session_id": str(payload["session_id"]),
        "session_schema_version": payload.get("schema_version"),
        "interview_schema_version": payload.get("interview_schema_version"),
        "approved_episodes": approved,
        "approved_episode_sha256": episode_hashes,
        "participant_source_turns": turns,
        "participant_source_turn_sha256": turn_hashes,
        "source_map_sha256": _sha256_json(raw_map),
        "source_map_provider_receipt": provider_receipt,
        "claims": _pattern_claims(life_map),
        "important_unknowns": list(life_map.important_unknowns),
        "evidence_coverage": _coverage_snapshot(approved),
        "research_exclusions": [
            "strengths",
            "friction_points",
            "transfer_opportunities",
            "reversible_experiments",
            "coaching_messages",
            "inner_signal_material",
            "birth_or_chart_model_outputs",
        ],
        "theory_blindness_boundary": {
            "interview_and_synthesis_receive_hidden_birth_or_chart_data": False,
            "interview_and_synthesis_receive_candidate_prediction_rank_or_model_fit": False,
            "participant_source_text_remains_participant_authored_and_may_contain_unprompted_content": True,
        },
    }


def _candidate_id(source: dict[str, Any]) -> tuple[str, str]:
    digest = _sha256_json(source)
    return f"BFC-{digest[:20].upper()}", digest


def _candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    value = payload.setdefault("behavioral_freeze_candidates", [])
    if not isinstance(value, list):
        raise HTTPException(status_code=500, detail="stored behavioral freeze candidates are invalid")
    return cast(list[dict[str, Any]], value)


def _find_candidate(payload: dict[str, Any], candidate_id: str) -> dict[str, Any]:
    for candidate in _candidates(payload):
        if candidate.get("candidate_id") == candidate_id:
            return _validate_candidate(candidate)
    raise HTTPException(status_code=404, detail="behavioral freeze candidate not found")


def _validate_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    source = candidate.get("source")
    if not isinstance(source, dict):
        raise HTTPException(status_code=500, detail="stored behavioral freeze candidate is invalid")
    digest = _sha256_json(source)
    expected_id = f"BFC-{digest[:20].upper()}"
    if candidate.get("candidate_sha256") != digest or candidate.get("candidate_id") != expected_id:
        raise HTTPException(status_code=500, detail="stored behavioral freeze candidate failed integrity verification")
    return candidate


def _latest_reviews(candidate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    events = candidate.get("review_events", [])
    if not isinstance(events, list):
        raise HTTPException(status_code=500, detail="stored behavioral review events are invalid")
    latest: dict[str, dict[str, Any]] = {}
    for event in cast(list[dict[str, Any]], events):
        claim_id = event.get("claim_id")
        if isinstance(claim_id, str):
            latest[claim_id] = event
    return latest


def _public_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    source = cast(dict[str, Any], candidate["source"])
    claims = cast(list[dict[str, Any]], source.get("claims", []))
    latest = _latest_reviews(candidate)
    rows = []
    for claim in claims:
        claim_id = str(claim["claim_id"])
        rows.append({**claim, "latest_review": latest.get(claim_id)})
    receipt = candidate.get("finalized_freeze_receipt")
    return {
        "candidate_id": candidate["candidate_id"],
        "candidate_sha256": candidate["candidate_sha256"],
        "created_at_utc": candidate["created_at_utc"],
        "claims": rows,
        "important_unknowns": source.get("important_unknowns", []),
        "claim_count": len(claims),
        "reviewed_claim_count": sum(str(row["claim_id"]) in latest for row in claims),
        "review_complete": all(str(row["claim_id"]) in latest for row in claims),
        "finalized_freeze_receipt": receipt,
        "live_profile_remains_editable_after_freeze": True,
        "model_comparison_authorized_by_freeze": False,
    }


def _effective_claims(candidate: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    source = cast(dict[str, Any], candidate["source"])
    claims = cast(list[dict[str, Any]], source.get("claims", []))
    latest = _latest_reviews(candidate)
    effective: list[dict[str, Any]] = []
    admissible: list[str] = []
    for original in claims:
        claim_id = str(original["claim_id"])
        review = latest.get(claim_id)
        if review is None:
            raise HTTPException(status_code=409, detail="review every claim before freezing")
        action = str(review["action"])
        final_claim: dict[str, Any] | None = None
        if action == "approve":
            final_claim = {
                "claim_id": claim_id,
                "title": original["title"],
                "summary": original["summary"],
                "status": original["status"],
                "supporting_episode_ids": original.get("supporting_episode_ids", []),
                "counterexample_episode_ids": original.get("counterexample_episode_ids", []),
                "contexts": original.get("contexts", []),
                "limits": original.get("limits", []),
                "participant_revision": False,
            }
            admissible.append(claim_id)
        elif action == "edit":
            revision = review.get("participant_revision")
            if not isinstance(revision, dict) or not isinstance(revision.get("summary"), str):
                raise HTTPException(status_code=500, detail="stored participant claim revision is invalid")
            final_claim = {
                "claim_id": claim_id,
                "title": revision.get("title") or original["title"],
                "summary": revision["summary"],
                "status": revision.get("status") or original["status"],
                "supporting_episode_ids": original.get("supporting_episode_ids", []),
                "counterexample_episode_ids": original.get("counterexample_episode_ids", []),
                "contexts": original.get("contexts", []),
                "limits": original.get("limits", []),
                "participant_revision": True,
                "new_data_during_review": True,
            }
            admissible.append(claim_id)
        effective.append(
            {
                "claim_id": claim_id,
                "original_synthesis": original,
                "effective_review": review,
                "final_participant_claim": final_claim,
                "admitted_as_participant_endorsed_claim": action in {"approve", "edit"},
            }
        )
    return effective, admissible


def _write_immutable_freeze(
    store: LifePatternsFileStore,
    *,
    artifact: dict[str, Any],
    freeze_id: str,
) -> str:
    directory = store.root / "freezes"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(directory, 0o700)
    path = directory / f"{freeze_id}.json"
    serialized = _canonical_json(artifact) + b"\n"
    if path.exists():
        if path.read_bytes() != serialized:
            raise RuntimeError("behavioral freeze hash collision or artifact tampering detected")
        return str(path.relative_to(store.root))
    try:
        write_new_bytes(path, serialized, mode=0o400)
    except FileExistsError:
        if path.read_bytes() != serialized:
            raise RuntimeError(
                "behavioral freeze hash collision or artifact tampering detected"
            ) from None
    return str(path.relative_to(store.root))


def _load_immutable_freeze(
    store: LifePatternsFileStore,
    *,
    session_id: str,
    receipt: dict[str, Any],
) -> dict[str, Any]:
    freeze_id = receipt.get("freeze_id")
    digest = receipt.get("freeze_sha256")
    relpath = receipt.get("artifact_relpath")
    expected_relpath = f"freezes/{freeze_id}.json"
    if (
        not isinstance(freeze_id, str)
        or not freeze_id.startswith("BPF-")
        or not isinstance(digest, str)
        or len(digest) != 64
        or relpath != expected_relpath
    ):
        raise HTTPException(status_code=500, detail="stored behavioral freeze receipt is invalid")
    path = store.root / expected_relpath
    try:
        raw = path.read_bytes()
        artifact_raw: Any = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=500, detail="behavioral freeze artifact is unreadable") from exc
    if not isinstance(artifact_raw, dict):
        raise HTTPException(status_code=500, detail="behavioral freeze artifact is invalid")
    artifact = cast(dict[str, Any], artifact_raw)
    payload = artifact.get("payload")
    if not isinstance(payload, dict):
        raise HTTPException(status_code=500, detail="behavioral freeze payload is invalid")
    actual_digest = _sha256_json(payload)
    expected_id = f"BPF-{actual_digest[:20].upper()}"
    if (
        artifact.get("schema_version") != "life-patterns-behavioral-freeze-artifact-v1"
        or artifact.get("freeze_id") != expected_id
        or artifact.get("freeze_sha256") != actual_digest
        or freeze_id != expected_id
        or digest != actual_digest
        or payload.get("session_id") != session_id
    ):
        raise HTTPException(status_code=500, detail="behavioral freeze artifact failed integrity verification")
    if raw != _canonical_json(artifact) + b"\n":
        raise HTTPException(status_code=500, detail="behavioral freeze artifact is not canonical")
    return artifact


def _current_candidate_digest(payload: dict[str, Any]) -> str:
    return _sha256_json(_build_candidate_source(payload))


def register_life_patterns_freeze_routes(
    app: FastAPI,
    *,
    store: LifePatternsFileStore,
) -> None:
    @app.post("/api/life-patterns/interview/sessions/{session_id}/freeze-candidate")
    def create_freeze_candidate(
        session_id: str,
        request: FreezeCandidateRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        source = _build_candidate_source(payload)
        candidate_id, digest = _candidate_id(source)
        for candidate in _candidates(payload):
            if candidate.get("candidate_id") == candidate_id:
                return _public_candidate(_validate_candidate(candidate))
        candidate = {
            "schema_version": "life-patterns-behavioral-freeze-candidate-v1",
            "candidate_id": candidate_id,
            "candidate_sha256": digest,
            "created_at_utc": datetime.now(UTC).isoformat(),
            "source": source,
            "review_events": [],
            "finalized_freeze_receipt": None,
        }
        _candidates(payload).append(candidate)
        store.save(payload)
        return _public_candidate(candidate)

    @app.post(
        "/api/life-patterns/interview/sessions/{session_id}/freeze-candidates/"
        "{candidate_id}/claims/{claim_id}/review"
    )
    def review_freeze_claim(
        session_id: str,
        candidate_id: str,
        claim_id: str,
        request: FreezeClaimReviewRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        candidate = _find_candidate(payload, candidate_id)
        if candidate.get("finalized_freeze_receipt") is not None:
            raise HTTPException(status_code=409, detail="this behavioral freeze is already final")
        source = cast(dict[str, Any], candidate["source"])
        claims = cast(list[dict[str, Any]], source.get("claims", []))
        original = next((row for row in claims if row.get("claim_id") == claim_id), None)
        if original is None:
            raise HTTPException(status_code=404, detail="behavioral claim not found")
        revision: dict[str, Any] | None = None
        if request.action == "edit":
            assert request.summary is not None
            revision = {
                "title": (
                    request.title.strip()
                    if request.title and request.title.strip()
                    else original["title"]
                ),
                "summary": request.summary.strip(),
                "status": request.status or original["status"],
            }
        event = {
            "review_event_id": f"BFR-{uuid.uuid4().hex[:16].upper()}",
            "candidate_id": candidate_id,
            "claim_id": claim_id,
            "action": request.action,
            "participant_revision": revision,
            "new_data_during_review": request.action == "edit",
            "note": request.note.strip() if request.note and request.note.strip() else None,
            "reviewed_at_utc": datetime.now(UTC).isoformat(),
        }
        events = candidate.setdefault("review_events", [])
        if not isinstance(events, list):
            raise HTTPException(status_code=500, detail="stored behavioral review events are invalid")
        cast(list[dict[str, Any]], events).append(event)
        store.save(payload)
        return _public_candidate(candidate)

    @app.post(
        "/api/life-patterns/interview/sessions/{session_id}/freeze-candidates/{candidate_id}/finalize"
    )
    def finalize_freeze(
        session_id: str,
        candidate_id: str,
        request: FinalizeFreezeRequest,
    ) -> dict[str, Any]:
        if not request.attest_profile_reviewed or not request.attest_snapshot_immutable:
            raise HTTPException(
                status_code=400,
                detail="explicit participant review and immutable-snapshot acknowledgment are required",
            )
        payload = store.read(session_id, request.token)
        candidate = _find_candidate(payload, candidate_id)
        existing = candidate.get("finalized_freeze_receipt")
        if isinstance(existing, dict):
            _load_immutable_freeze(store, session_id=session_id, receipt=existing)
            return {"freeze_receipt": existing, "candidate": _public_candidate(candidate)}
        if _current_candidate_digest(payload) != candidate.get("candidate_sha256"):
            raise HTTPException(
                status_code=409,
                detail=(
                    "the live evidence changed after this review candidate was created; "
                    "rebuild the current map and review a new candidate"
                ),
            )
        effective_claims, admissible = _effective_claims(candidate)
        source = cast(dict[str, Any], candidate["source"])
        frozen_at = datetime.now(UTC).isoformat()
        review_events = cast(list[dict[str, Any]], candidate.get("review_events", []))
        freeze_payload = {
            "schema_version": "life-patterns-behavioral-freeze-payload-v1",
            "session_id": session_id,
            "candidate_id": candidate_id,
            "candidate_sha256": candidate["candidate_sha256"],
            "frozen_at_utc": frozen_at,
            "behavioral_source": source,
            "participant_review": {
                "review_events": review_events,
                "effective_claims": effective_claims,
                "admissible_claim_ids": admissible,
                "attestation": {
                    "profile_reviewed": True,
                    "snapshot_immutable_acknowledged": True,
                    "model_comparison_authorized": False,
                },
            },
            "provenance": {
                "alignment": "W3C PROV-DM conceptual alignment",
                "prov_terms_used": [
                    "prov:Entity",
                    "prov:Activity",
                    "prov:wasDerivedFrom",
                    "prov:wasGeneratedBy",
                    "prov:wasAttributedTo",
                    "prov:Revision",
                ],
                "entities": {
                    "participant_source_turn_ids": list(
                        cast(
                            dict[str, str],
                            source.get("participant_source_turn_sha256", {}),
                        ).keys()
                    ),
                    "approved_episode_ids": list(
                        cast(dict[str, str], source.get("approved_episode_sha256", {})).keys()
                    ),
                    "source_map_sha256": source["source_map_sha256"],
                    "candidate_sha256": candidate["candidate_sha256"],
                },
                "activities": [
                    "chart_blind_map_generation",
                    "participant_member_check",
                    "behavioral_freeze_finalization",
                ],
                "relations": [
                    "map wasDerivedFrom approved episodes",
                    "reviewed claims wereDerivedFrom map claims plus participant review events",
                    "freeze wasGeneratedBy behavioral freeze finalization",
                ],
            },
            "future_model_binding": {
                "require_exact_freeze_sha256_on_every_model_result": True,
                "separate_model_analysis_authorization_required": True,
                "later_profile_changes_must_not_mutate_this_payload": True,
            },
        }
        digest = _sha256_json(freeze_payload)
        freeze_id = f"BPF-{digest[:20].upper()}"
        artifact = {
            "schema_version": "life-patterns-behavioral-freeze-artifact-v1",
            "freeze_id": freeze_id,
            "freeze_sha256": digest,
            "payload": freeze_payload,
        }
        try:
            relpath = _write_immutable_freeze(store, artifact=artifact, freeze_id=freeze_id)
        except (OSError, UnicodeError, RuntimeError) as exc:
            raise HTTPException(
                status_code=500,
                detail="behavioral freeze artifact could not be finalized",
            ) from exc
        receipt = FreezeReceipt(
            freeze_id=freeze_id,
            freeze_sha256=digest,
            candidate_id=candidate_id,
            frozen_at_utc=frozen_at,
            artifact_relpath=relpath,
        ).model_dump(mode="json")
        candidate["finalized_freeze_receipt"] = receipt
        receipts = payload.setdefault("behavioral_freeze_receipts", [])
        if not isinstance(receipts, list):
            raise HTTPException(status_code=500, detail="stored behavioral freeze receipts are invalid")
        cast(list[dict[str, Any]], receipts).append(receipt)
        store.save(payload)
        return {"freeze_receipt": receipt, "candidate": _public_candidate(candidate)}

    @app.get("/api/life-patterns/interview/sessions/{session_id}/freezes/{freeze_id}")
    def get_freeze(session_id: str, freeze_id: str, token: str) -> dict[str, Any]:
        payload = store.read(session_id, token)
        receipts_raw = payload.get("behavioral_freeze_receipts", [])
        if not isinstance(receipts_raw, list):
            raise HTTPException(status_code=500, detail="stored behavioral freeze receipts are invalid")
        receipt = next(
            (
                row
                for row in cast(list[dict[str, Any]], receipts_raw)
                if row.get("freeze_id") == freeze_id
            ),
            None,
        )
        if receipt is None:
            raise HTTPException(status_code=404, detail="behavioral freeze not found")
        artifact = _load_immutable_freeze(store, session_id=session_id, receipt=receipt)
        return {"freeze_receipt": receipt, "artifact": artifact, "integrity_verified": True}
