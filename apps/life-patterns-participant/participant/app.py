"""Isolated participant HTTP surface: no astrology or owner-app imports."""

from __future__ import annotations

import json
import os
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel, ConfigDict, Field

from .domain import (
    VERSION,
    bank,
    export_record,
    import_record,
    load_instrument,
    new_state,
    normalize_state_route_ids,
    resolved_turn_route_id,
    strict_json,
    target_exposure,
    utc,
)
from .engine import PAYMENT_ERROR, Engine, ProviderError, Venice
from .fast_review import PROTOCOL, source_revision
from .review_timing import review_guidance
from .store import Conflict, Missing, Store, canonical, digest
from .validation_diagnostics import safe_validation_diagnostic

STATIC = Path(__file__).parent / "static"


@dataclass(frozen=True)
class Settings:
    database: Path
    encryption_key: str
    admin_token: str
    join_token: str
    authority: Path
    submission_token: str = ""
    review_worker_token: str = ""
    gateway_url: str = "https://venice-model-gateway-production.up.railway.app/v1"
    gateway_token: str = ""
    model: str = "openai-gpt-56-sol"
    effort: str = "xhigh"
    secure_cookies: bool = True
    maximum_sessions: int = 50
    maximum_calls: int = 12
    live_enabled: bool = False
    public_origin: str = ""
    fast_review_enabled: bool = False

    @classmethod
    def from_env(cls):
        required = ("PARTICIPANT_DATA_KEY", "PARTICIPANT_ADMIN_TOKEN", "PARTICIPANT_JOIN_TOKEN")
        if any(not os.environ.get(k) for k in required):
            raise RuntimeError("Participant storage and access secrets must be configured.")
        path = Path(os.environ.get("PARTICIPANT_DB", "/data/survey.sqlite3"))
        if os.environ.get("RAILWAY_ENVIRONMENT_ID"):
            volume_path = os.environ.get("RAILWAY_VOLUME_MOUNT_PATH")
            if not volume_path or not path.resolve().is_relative_to(Path(volume_path).resolve()):
                raise RuntimeError("A persistent Railway volume is required.")
        return cls(
            database=path,
            encryption_key=os.environ[required[0]],
            admin_token=os.environ[required[1]],
            join_token=os.environ[required[2]],
            authority=Path(os.environ.get("SURVEY_AUTHORITY_DIR", "/app/authority")),
            submission_token=os.environ.get("PARTICIPANT_GPT_SUBMISSION_TOKEN", ""),
            review_worker_token=os.environ.get("PARTICIPANT_REVIEW_WORKER_TOKEN", ""),
            gateway_url=os.environ.get(
                "UDA_MODEL_GATEWAY_URL", "https://venice-model-gateway-production.up.railway.app"
            ).rstrip("/")
            + "/v1",
            gateway_token=os.environ.get("UDA_MODEL_GATEWAY_TOKEN", ""),
            model=os.environ.get("PARTICIPANT_MODEL", "openai-gpt-56-sol"),
            effort=os.environ.get("PARTICIPANT_REASONING", "xhigh"),
            live_enabled=os.environ.get("PARTICIPANT_LIVE_ENABLED") == "1",
            fast_review_enabled=os.environ.get("PARTICIPANT_FAST_REVIEW_ENABLED") == "1",
            public_origin=os.environ.get("PARTICIPANT_PUBLIC_ORIGIN", "").rstrip("/"),
            maximum_sessions=int(os.environ.get("PARTICIPANT_MAX_SESSIONS", "50")),
            maximum_calls=int(os.environ.get("PARTICIPANT_MAX_MODEL_CALLS", "12")),
        )


class Body(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Access(Body):
    token: str = Field(min_length=32, max_length=128)


class QuestionFeedbackDisposition(Body):
    status: Literal["new", "triaging", "revision_proposed", "resolved", "dismissed"]
    revision_id: str = Field(default="", max_length=120, pattern=r"^[a-zA-Z0-9._/-]*$")


class Operation(Body):
    revision: int = Field(ge=0)
    operation_id: str = Field(min_length=12, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    action: Literal[
        "consent",
        "decline",
        "answer",
        "skip",
        "pause",
        "resume",
        "stop",
        "confirm",
        "correct",
        "review_correction",
        "review_seen",
        "set_retrospective_preference",
    ]
    text: str = Field(default="", max_length=20000)
    target: str | None = Field(default=None, max_length=100)
    retrospective_questions_welcome: bool | None = None


class Import(Body):
    source_type: Literal[
        "edited_response_record", "raw_transcript", "prior_json", "answer_only_notes"
    ] = "edited_response_record"
    source_mode: Literal["railway_text", "chatgpt_voice", "chatgpt_text", "mixed", "unknown"] = (
        "unknown"
    )
    record: dict | None = None
    record_text: str | None = Field(default=None, max_length=1_500_000)

    def parsed_record(self):
        if self.record is not None and self.record_text is not None:
            raise ValueError("Provide one source record representation, not two.")
        return strict_json(self.record_text) if self.record_text is not None else self.record


class ProviderRecovery(Body):
    billing_issue_resolved: Literal[True]


class GptReviewStart(Body):
    research_use_consented: Literal[True]
    request_id: str = Field(min_length=16, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    candidate_record: dict
    review_protocol: Literal["legacy-v1", "fast-batch-v1"] = "legacy-v1"


class GptReviewAnswer(Body):
    answer_text: str = Field(default="", max_length=20000)
    clarification_id: str = Field(pattern=r"^Q-[a-f0-9]{32}$")
    operation_id: str = Field(min_length=16, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    skipped: bool = False


class BatchAnswer(Body):
    clarification_id: str = Field(pattern=r"^Q-[a-f0-9]{32}$")
    answer_text: str = Field(default="", max_length=20000)
    skipped: bool = False


class GptBatchAnswers(Body):
    batch_id: str = Field(pattern=r"^B-[a-f0-9]{32}$")
    operation_id: str = Field(min_length=16, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    answers: list[BatchAnswer] = Field(min_length=1, max_length=3)


class GptReviewControl(Body):
    action: Literal["pause", "resume", "stop", "withdraw", "retry"]
    operation_id: str = Field(min_length=16, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")


class WorkerHeartbeat(Body):
    claim_id: str = Field(pattern=r"^L-[a-f0-9]{32}$")
    review_stage: str | None = Field(default=None, max_length=40)


class WorkerClarification(Body):
    route_id: str = Field(min_length=1, max_length=100)
    route_type: Literal["canonical", "context_repair", "missing_piece_followup"]
    question_text: str = Field(min_length=1, max_length=3000)
    participant_purpose: str | None = Field(default=None, min_length=1, max_length=700)
    antecedent_turn_ids: list[str] = Field(default_factory=list, max_length=100)


class WorkerReviewResult(Body):
    claim_id: str = Field(pattern=r"^L-[a-f0-9]{32}$")
    candidate_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    status: Literal[
        "queued", "clarification_needed", "ready", "error", "paused", "stopped", "resource_limited"
    ]
    worker_state: dict | None = None
    receipt: dict
    clarification: WorkerClarification | None = None
    clarifications: list[WorkerClarification] | None = Field(default=None, min_length=1, max_length=3)
    error: str | None = Field(default=None, max_length=1000)


class GptSubmission(Body):
    research_use_consented: Literal[True]
    review_id: str | None = Field(default=None, pattern=r"^R-[a-f0-9]{32}$")
    # Object fields remain backward-compatible for internal clients. The Custom GPT
    # Action uses JSON strings because free-form object parameters were not exposed.
    primary_record: dict | None = None
    cf003_record: dict | None = None
    primary_record_json: str | None = Field(default=None, min_length=2, max_length=1_500_000)
    cf003_record_json: str | None = Field(default=None, min_length=2, max_length=500_000)


class GptReviewedSubmission(GptSubmission):
    # Optional only for exact-source recovery against one existing ready review.
    # This endpoint never accepts an unreviewed final submission.
    pass


class BodyLimit:
    def __init__(self, app, limit=2_000_000):
        self.app, self.limit = app, limit

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        messages, size = [], 0
        while True:
            message = await receive()
            messages.append(message)
            if message["type"] == "http.disconnect":
                return
            size += len(message.get("body", b""))
            if size > self.limit:
                return await JSONResponse({"detail": "Request too large."}, status_code=413)(
                    scope, receive, send
                )
            if not message.get("more_body"):
                break
        position = 0

        async def replay():
            nonlocal position
            if position < len(messages):
                message = messages[position]
                position += 1
                return message
            return await receive()

        await self.app(scope, replay, send)


def create_app(settings: Settings, provider=None, instrument=None) -> FastAPI:
    if min(len(settings.admin_token), len(settings.join_token)) < 32:
        raise RuntimeError("Strong participant access secrets are required.")
    if any(
        token and len(token) < 32
        for token in (settings.submission_token, settings.review_worker_token)
    ):
        raise RuntimeError("Strong submission and review-worker keys are required.")
    store = Store(settings.database, settings.encryption_key)
    instrument = instrument or load_instrument(settings.authority)
    version = store.pin_instrument(instrument)
    from .question_policy import (
        activate,
        lineage_participant_purpose,
        participant_purpose,
    )

    migration_state = new_state(version, settings.model, settings.effort)
    activate(migration_state)
    migration_routes = {
        str(route["id"]): route for route in bank(instrument, migration_state)["questions"]
    }
    migration_route_ids = set(migration_routes)
    evidence_guide_by_facet = {
        str(row.get("facet_id")): row
        for row in json.loads(instrument["EVIDENCE-GUIDE-v7.json"])
        if row.get("facet_id")
    }

    def public_review_entry(entry: dict, worker_state: dict) -> dict:
        turns_by_id = {
            str(turn.get("turn_id")): turn for turn in worker_state.get("turns", [])
        }
        source_measurements = []
        labels = []
        for quote in entry.get("source_quotes", []):
            turn_id = str(quote.get("turn_id") or "")
            turn = turns_by_id.get(turn_id, {})
            route_id = resolved_turn_route_id(
                turn, migration_route_ids, allow_historical_turn_id=True
            )
            label = lineage_participant_purpose(route_id, migration_routes)
            if label:
                source_measurements.append(
                    {"turn_id": turn_id, "measurement_label": label}
                )
                if label not in labels:
                    labels.append(label)
        if not labels:
            for facet_id in entry.get("candidate_facet_ids", []):
                facet = evidence_guide_by_facet.get(str(facet_id), {})
                for route_id in facet.get("question_routes", []):
                    label = lineage_participant_purpose(str(route_id), migration_routes)
                    if label and label not in labels:
                        labels.append(label)
        supported_scope = str(entry.get("supported_scope") or "").strip()
        if not labels and supported_scope:
            labels.append(supported_scope)
        if not labels:
            labels.append("the specific recurring pattern supported by these quoted answers.")
        return {
            key: entry.get(key)
            for key in (
                "evidence_id",
                "observation",
                "conditions",
                "time_frame",
                "relationship_context",
                "source_quotes",
            )
        } | {
            "measured_distinction": supported_scope or labels[0],
            "measurement_labels": labels,
            "source_measurements": source_measurements,
            "split_for_display": (
                len(labels) > 1
                and "D19.status_ownership" in entry.get("candidate_facet_ids", [])
            ),
        }
    retired_routes = {
        route_id
        for route_id, route in migration_routes.items()
        if route.get("elicitation_retired")
    }

    def with_participant_purpose(question: dict | None) -> dict | None:
        if not isinstance(question, dict):
            return question
        result = dict(question)
        route = migration_routes.get(str(result.get("route_id") or ""))
        if route is not None:
            # Recompute from canonical route authority so stale saved questions gain the
            # explanation on read without replacing the review or changing question_text.
            result["participant_purpose"] = participant_purpose(route)
        elif not str(result.get("participant_purpose") or "").strip():
            result["participant_purpose"] = (
                "the specific recurring response or preference this clarification is resolving."
            )
        return result
    def stale_canonical_question(payload: dict, pending: list[dict]) -> bool:
        canonical_ids = {
            str(question.get("route_id"))
            for question in pending
            if isinstance(question, dict) and question.get("route_type") == "canonical"
        }
        if not canonical_ids:
            return False
        candidate = payload.get("candidate_record")
        if not isinstance(candidate, dict):
            return False
        check_state = new_state(
            version,
            str(payload.get("model") or settings.model),
            str(payload.get("effort") or settings.effort),
        )
        activate(check_state)
        import_record(
            check_state,
            candidate,
            "prior_json",
            instrument,
            candidate.get("collection_mode", "unknown"),
        )
        normalize_state_route_ids(check_state, instrument)
        from .inference_context import presented_route_ids

        return bool(canonical_ids.intersection(presented_route_ids(check_state, instrument)))

    app_policy_refresh_count = store.requeue_stale_gpt_review_questions(
        retired_routes, stale_question=stale_canonical_question
    )
    provider = provider or Venice(settings.gateway_url, settings.gateway_token)
    engine = Engine(store, provider, settings.maximum_calls)
    app = FastAPI(
        title="Life Patterns", version=VERSION, docs_url=None, redoc_url=None, openapi_url=None
    )
    app.state.store, app.state.engine = store, engine
    app.state.policy_refresh_count = app_policy_refresh_count
    app.add_middleware(BodyLimit)

    def ready():
        if not settings.live_enabled or not provider.configured:
            raise ProviderError("venice_not_activated")

    def token(request):
        value = request.cookies.get("lp_session", "")
        current = store.read(value)
        header_id = request.headers.get("x-life-patterns-session")
        query_id = request.query_params.get("session_id")
        if header_id and query_id and header_id != query_id:
            raise Conflict("Conflicting session identifiers.")
        expected = header_id or query_id
        if (
            request.method not in {"GET", "HEAD"} or request.url.path == "/api/export"
        ) and not expected:
            raise Conflict("A session-bound request is required. Reload your private resume link.")
        if expected and expected != current["session_id"]:
            raise Conflict(
                "Another session is open in this browser. Reload this tab's private resume link."
            )
        return value

    def admin(request):
        header = request.headers.get("authorization", "")
        value = header[7:] if header.startswith("Bearer ") else ""
        if not secrets.compare_digest(value, settings.admin_token):
            raise HTTPException(401, "Researcher access required.")

    def gpt_submitter(request):
        if not settings.submission_token:
            raise HTTPException(503, "GPT submission is not configured.")
        header = request.headers.get("authorization", "")
        value = header[7:] if header.startswith("Bearer ") else ""
        if not secrets.compare_digest(value, settings.submission_token):
            raise HTTPException(401, "GPT submission access required.")

    def review_worker(request):
        if not settings.review_worker_token:
            raise HTTPException(503, "GPT review worker is not configured.")
        header = request.headers.get("authorization", "")
        value = header[7:] if header.startswith("Bearer ") else ""
        if not secrets.compare_digest(value, settings.review_worker_token):
            raise HTTPException(401, "GPT review worker access required.")

    def reject_target_fields(record):
        forbidden = {
            "birth_date",
            "birth_time",
            "birthplace",
            "date_of_birth",
            "dob",
            "birth_location",
            "birth_chart",
            "human_design_type",
            "natal_chart",
            "chart",
            "rankings",
            "target_predictions",
        }

        def walk(value):
            if isinstance(value, dict):
                if forbidden.intersection(str(key).lower() for key in value):
                    raise ValueError("Remove birth/chart/ranking fields before submission.")
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(record)

    def behavioral_content(record):
        turns = record.get("turns")
        if not isinstance(turns, list):
            raise ValueError("A Life Patterns record needs a turns list.")
        result = []
        for turn in turns:
            if not isinstance(turn, dict):
                raise ValueError("Every Life Patterns turn must be an object.")
            if turn.get("turn_role", "behavioral") != "behavioral":
                continue
            result.append(
                {
                    "question_text": turn.get("question_text"),
                    "answer_text": turn.get("answer_text"),
                    "canonical_question_id": turn.get(
                        "canonical_question_id", turn.get("question_id")
                    ),
                    "correction_of": turn.get("correction_of"),
                    "conditions": turn.get("conditions") or [],
                    "corrections": turn.get("corrections") or [],
                    "process_feedback": turn.get("process_feedback") or [],
                }
            )
        return result

    def review_material(record):
        return {
            "turns": record.get("turns"),
            "collection_mode": record.get("collection_mode"),
            "retrospective_questions_welcome": record.get("retrospective_questions_welcome"),
            "collection_preferences": record.get("collection_preferences"),
            "source_type": record.get("source_type"),
            "source_fidelity": record.get("source_fidelity"),
            "evidence_authority": record.get("evidence_authority"),
        }

    def validate_review_candidate(record):
        if record.get("schema") != "life-patterns-full-survey-participant-export-v2":
            raise ValueError("Review candidate schema is not the current Life Patterns export.")
        if (
            not isinstance(record.get("consent"), dict)
            or record["consent"].get("research_use_consented") is not True
        ):
            raise ValueError("Research-use consent must be recorded before independent review.")
        freeze = record.get("freeze") or {}
        if not isinstance(freeze, dict):
            raise ValueError("Candidate freeze metadata must be an object.")
        if freeze.get("frozen_before_birth_or_chart_reveal") is True:
            raise ValueError("Independent review must happen before the primary record is frozen.")
        turns = record.get("turns")
        if not isinstance(turns, list) or len(turns) > 1000:
            raise ValueError("A candidate needs at most 1000 source turns.")
        for turn in turns:
            if not isinstance(turn, dict):
                raise ValueError("Every source turn must be an object.")
            for name in ("question_text", "answer_text"):
                if turn.get(name) is not None and not isinstance(turn[name], str):
                    raise ValueError("Source questions and answers must be text or null.")
            if target_exposure(
                (turn.get("question_text") or "") + "\n" + (turn.get("answer_text") or "")
            ):
                raise ValueError("Remove volunteered birth/chart information before review.")
        if not any((row.get("answer_text") or "").strip() for row in behavioral_content(record)):
            raise ValueError("Independent review needs at least one behavioral answer.")
        reject_target_fields(record)

    def review_public(payload):
        clarification = with_participant_purpose(payload.get("pending_clarification"))
        raw_clarifications = payload.get("pending_clarifications") or []
        clarifications = [with_participant_purpose(item) for item in raw_clarifications]
        status = payload["status"]
        return {
            "schema": "life-patterns-gpt-review-status-v1",
            "review_id": payload["review_id"],
            "status": status,
            "round": payload.get("round", 0),
            "duplicate": bool(payload.get("duplicate", False)),
            **review_guidance(payload),
            "review_protocol": payload.get("review_protocol", "legacy-v1"),
            "batch_id": payload.get("pending_batch_id") if status == "clarification_needed" else None,
            "clarifications": (
                clarifications if status == "clarification_needed" and clarifications else None
            ),
            "final_review_completed": status == "ready",

            "clarification": clarification
            if payload.get("status") == "clarification_needed"
            else None,
            "error": payload.get("error")
            if payload.get("status") in {"error", "resource_limited"}
            else None,
            "review_summary": [
                public_review_entry(entry, payload.get("worker_state") or {})
                for entry in (payload.get("worker_state") or {}).get("evidence", [])
                if entry.get("review_status") == "independent_semantic_admission_passed"
            ]
            if payload.get("status") == "ready"
            else None,
            "source_review_status": "independent_semantic_admission"
            if payload.get("status") == "ready"
            else "pending",
        }

    def expected_review_behavioral(payload):
        expected = behavioral_content(payload["candidate_record"])
        for item in payload.get("clarification_history", []):
            expected.append(
                {
                    "question_text": item.get("question_text"),
                    "answer_text": item.get("answer_text"),
                    "canonical_question_id": item.get("route_id"),
                    "correction_of": None,
                    "conditions": [],
                    "corrections": [],
                    "process_feedback": [],
                }
            )
        return expected

    def reviewed_turn_mismatches(primary: dict, review: dict) -> list[tuple[int, list[str]]]:
        """Exact behavior authority; additive clarification process notes are not traits."""
        actual_turns = behavioral_content(primary)
        expected_turns = expected_review_behavioral(review)
        if len(actual_turns) != len(expected_turns):
            return [(0, ["turn_count"]) ]
        original_count = len(behavioral_content(review["candidate_record"]))
        disagreements = []
        for index, (actual, expected) in enumerate(
            zip(actual_turns, expected_turns, strict=True), 1
        ):
            changed = [key for key in expected if actual.get(key) != expected.get(key)]
            if index > original_count and changed == ["process_feedback"]:
                notes = actual.get("process_feedback")
                if (
                    expected.get("process_feedback") == []
                    and isinstance(notes, list)
                    and all(isinstance(note, str) and 0 < len(note) <= 4000 for note in notes)
                ):
                    changed = []
            if changed:
                disagreements.append((index, changed))
        return disagreements

    def recover_ready_review_id(primary: dict) -> str:
        """Proof of full source possession; never search by biography or route alone."""
        if (
            primary.get("schema") != "life-patterns-full-survey-participant-export-v2"
            or (primary.get("consent") or {}).get("research_use_consented") is not True
            or (primary.get("freeze") or {}).get("frozen_before_birth_or_chart_reveal") is not True
        ):
            raise ValueError("Review recovery requires an exact, frozen, consented primary record.")
        reject_target_fields(primary)
        candidates = [
            row["review_id"]
            for row in store.ready_gpt_review_candidates()
            if (row.get("candidate_record") or {}).get("consent", {}).get("research_use_consented")
            and not reviewed_turn_mismatches(primary, row)
        ]
        if len(candidates) != 1:
            raise ValueError(
                "Cannot uniquely match this frozen primary to an existing ready review. "
                "Provide the original review handle; do not reconstruct or start a new review."
            )
        return candidates[0]

    def validate_gpt_submission(body):
        def exact_record(object_value, json_value, label, json_field):
            try:
                parsed = strict_json(json_value) if json_value is not None else None
            except ValueError as exc:
                code = (
                    "dict_type"
                    if str(exc) == "JSON must contain one object"
                    else "json_invalid"
                )
                raise RequestValidationError(
                    [
                        {
                            "type": code,
                            "loc": ("body", json_field),
                            "msg": "Invalid JSON record transport.",
                            "input": None,
                        }
                    ]
                ) from exc
            if object_value is None and parsed is None:
                raise RequestValidationError(
                    [
                        {
                            "type": "missing",
                            "loc": ("body", json_field),
                            "msg": f"{label} is required.",
                            "input": None,
                        }
                    ]
                )
            if object_value is not None and parsed is not None:
                if canonical(object_value) != canonical(parsed):
                    raise ValueError(f"{label} object and JSON string do not match.")
                return object_value
            return object_value if object_value is not None else parsed

        primary = exact_record(
            body.primary_record, body.primary_record_json, "Primary record", "primary_record_json"
        )
        secondary = exact_record(
            body.cf003_record, body.cf003_record_json, "CF-003 record", "cf003_record_json"
        )
        if primary.get("schema") != "life-patterns-full-survey-participant-export-v2":
            raise ValueError("Primary record schema is not the current Life Patterns export.")
        if (primary.get("consent") or {}).get("research_use_consented") is not True:
            raise ValueError("Research-use consent must be frozen in the primary record.")
        freeze = primary.get("freeze") or {}
        if freeze.get("frozen_before_birth_or_chart_reveal") is not True:
            raise ValueError("Primary record must be frozen before any birth/chart reveal.")
        if not isinstance(primary.get("turns"), list) or not isinstance(
            secondary.get("turns"), list
        ):
            raise ValueError("Both submitted records need a turns list.")
        if body.review_id is not None:
            review = store.gpt_review_read(body.review_id)
            if review.get("status") != "ready":
                raise ValueError("The independent Railway review is not ready.")
            disagreements = reviewed_turn_mismatches(primary, review)
            if disagreements:
                index, changed = disagreements[0]
                if index == 0:
                    raise ValueError(
                        "Final primary turn count does not match the independently reviewed record."
                    )
                raise ValueError(
                    "Final primary does not match the independently reviewed record at "
                    f"behavioral turn {index}: " + ", ".join(changed)
                )
            checked = primary.get("participant_review") or {}
            if checked.get("summary_shown") is not True or checked.get("confirmed") is not True:
                raise ValueError(
                    "Show the independent neutral review and record participant confirmation before freeze."
                )
        required = {"CF003-ID-01", "CF003-CENTRAL-01", "CF003-PERIPH-01"}
        present = {
            turn.get("question_id") or turn.get("canonical_question_id")
            for turn in secondary["turns"]
            if isinstance(turn, dict) and turn.get("turn_role", "behavioral") == "behavioral"
        }
        if not required.issubset(present):
            raise ValueError("CF-003 record must contain all three required behavioral questions.")
        reject_target_fields(primary)
        reject_target_fields(secondary)
        primary_sha256 = digest(canonical(primary))
        declared = secondary.get("primary_record_sha256")
        if declared not in {None, primary_sha256}:
            raise ValueError(
                "CF-003 primary_record_sha256 does not match the submitted primary record."
            )
        linked_secondary = dict(secondary)
        linked_secondary["primary_record_sha256"] = primary_sha256
        return primary, linked_secondary, primary_sha256

    def public(state):
        return {
            "session_id": state["session_id"],
            "revision": state["revision"],
            "phase": state["phase"],
            "server_time": utc(),
            "error_code": state.get("error"),
            "error": "The AI service needs API credit. Your saved answers are safe; the study organizer must resolve this before retrying."
            if state.get("error") == PAYMENT_ERROR
            else state["error"],
            "provider_issue": {
                "code": "payment_required",
                "http_status": 402,
                "title": "Interview paused — AI service needs credit",
                "detail": "Venice returned a payment-required response. This is a study service issue, not a problem with your answers. Please return after the organizer checks the API balance. Retrying now will not help.",
                "automatic_retry": False,
                "requires_organizer": True,
            }
            if state.get("error") == PAYMENT_ERROR
            else None,
            "question": {k: state["pending_question"].get(k) for k in ("text", "question_id")}
            if state["pending_question"]
            else None,
            "review": state["review"],
            "collection_preferences": state.get("collection_preferences", {}),
            "processing": state.get("processing") if state["phase"] == "planning" else None,
            "turns": [
                {
                    k: t.get(k)
                    for k in (
                        "turn_id",
                        "question_text",
                        "answer_text",
                        "turn_source",
                        "correction_of",
                    )
                }
                for t in state["turns"]
            ],
            "evidence": state["evidence"]
            if state["phase"] in {"review", "complete", "stopped"}
            else [],
            "processed_turn_count": len(state["dispositions"]),
            "ready": settings.live_enabled and provider.configured,
        }

    def with_cookie(state, value, disclose=False):
        response = JSONResponse(public(state) | ({"resume_token": value} if disclose else {}))
        response.set_cookie(
            "lp_session",
            value,
            secure=settings.secure_cookies,
            httponly=True,
            samesite="strict",
            max_age=180 * 24 * 3600,
            path="/",
        )
        return response

    @app.middleware("http")
    async def privacy_headers(request, call_next):
        origin = request.headers.get("origin")
        if (
            request.method not in {"GET", "HEAD"}
            and not request.url.path.startswith("/api/gpt/")
            and not request.url.path.startswith("/api/review-worker/")
            and origin
            and origin.rstrip("/") != (settings.public_origin or str(request.base_url).rstrip("/"))
        ):
            return JSONResponse({"detail": "Cross-origin writes are not allowed."}, status_code=403)
        response = await call_next(request)
        response.headers.update(
            {
                "Cache-Control": "no-store",
                "Referrer-Policy": "no-referrer",
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
            }
        )
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        if request.url.path.startswith("/api/gpt/"):
            return JSONResponse(safe_validation_diagnostic(exc.errors()), status_code=422)
        return JSONResponse(
            {"detail": "Invalid fields. Your saved record has not been replaced."}, status_code=422
        )

    @app.exception_handler(Conflict)
    async def conflict_error(request, exc):
        return JSONResponse({"detail": str(exc)}, status_code=409)

    @app.exception_handler(Missing)
    async def missing_error(request, exc):
        return JSONResponse({"detail": "Session access required."}, status_code=401)

    @app.exception_handler(ProviderError)
    async def provider_error(request, exc):
        return JSONResponse(
            {
                "detail": "Venice is unavailable or not activated. Saved answers remain available.",
                "code": str(exc),
            },
            status_code=503,
        )

    @app.exception_handler(ValueError)
    async def value_error(request, exc):
        return JSONResponse({"detail": str(exc)}, status_code=422)

    @app.get("/healthz")
    def health():
        from .question_policy import identity
        return {
            "status": "ok",
            "question_policy": identity(),
            "version": VERSION,
            "provider": "venice",
            "provider_configured": provider.configured,
            "participant_enabled": settings.live_enabled,
            "gpt_submission_enabled": bool(settings.submission_token),
            "gpt_review_queue_enabled": bool(
                settings.submission_token and settings.review_worker_token
            ),
            "fast_review_enabled": settings.fast_review_enabled,
            "review_protocols": ["legacy-v1"] + ([PROTOCOL] if settings.fast_review_enabled else []),
            "review_worker_configured": bool(settings.review_worker_token),
            "persistence": "encrypted_sqlite",
            "instrument_version": version,
        }

    @app.get("/")
    def home():
        return FileResponse(STATIC / "index.html")

    @app.get("/admin")
    def admin_home():
        return FileResponse(STATIC / "admin.html")

    @app.get("/privacy")
    def privacy():
        return FileResponse(STATIC / "privacy.html")

    @app.get("/action-openapi.yaml")
    def action_openapi():
        return FileResponse(STATIC / "action-openapi.yaml", media_type="application/yaml")

    @app.get("/assets/{name}")
    def assets(name: str):
        if name not in {"app.js", "style.css", "admin.js"}:
            raise HTTPException(404)
        return FileResponse(STATIC / name)

    @app.post("/api/join")
    def join(body: Access):
        if not secrets.compare_digest(body.token, settings.join_token):
            raise HTTPException(401, "Study invitation required.")
        ready()
        value, state = store.create(
            new_state(version, settings.model, settings.effort), settings.maximum_sessions
        )
        return with_cookie(state, value, True)

    @app.post("/api/resume")
    def resume(body: Access):
        return with_cookie(store.read(body.token), body.token)

    @app.get("/api/session")
    def session(request: Request):
        value = token(request)
        return public(engine.recover_interrupted(value))

    @app.post("/api/operations")
    def operation(request: Request, body: Operation):
        value = token(request)
        if body.action == "consent":
            ready()
        if body.action == "review_seen":

            def mark(s):
                if body.operation_id in s["operations"]:
                    return
                Engine._revision(s, body.revision)
                if s["phase"] != "review":
                    raise Conflict("No review is being shown.")
                s["review"].update(summary_shown=True, shown_at=utc())
                s["operations"][body.operation_id] = {"action": "review_seen", "at": utc()}

            return public(store.change(value, mark))
        return public(
            engine.command(
                value,
                body.revision,
                body.operation_id,
                body.action,
                body.text,
                body.target,
                body.retrospective_questions_welcome,
            )
        )

    @app.post("/api/next")
    def next_question(request: Request):
        ready()
        return public(engine.launch_advance(token(request)))

    def download_response(state):
        if state["consent"] is not True:
            raise HTTPException(403, "Research consent is not recorded.")
        text = state["final_export"] or canonical(
            export_record(state, store.instrument(state["instrument_version"]))
        )
        return Response(
            text,
            media_type="application/json",
            headers={
                "Content-Disposition": 'attachment; filename="life-patterns-participant-export.json"'
            },
        )

    @app.get("/api/export")
    def download(request: Request):
        return download_response(store.read(token(request)))

    @app.post("/api/import")
    def participant_import(request: Request, body: Import):
        value = token(request)
        record = body.parsed_record()
        if record is None:
            raise ValueError("Select a source record.")

        def apply(s):
            import_record(
                s,
                record,
                body.source_type,
                store.instrument(s["instrument_version"]),
                body.source_mode,
            )

        return public(store.change(value, apply))

    @app.post("/api/gpt/reviews")
    def gpt_review_start(request: Request, body: GptReviewStart):
        gpt_submitter(request)
        candidate = body.candidate_record
        if body.review_protocol == PROTOCOL and not settings.fast_review_enabled:
            raise HTTPException(409, "Fast review is not enabled; retain the source and try later.")
        validate_review_candidate(candidate)
        candidate_sha256 = digest(canonical(candidate))
        review_id, payload, duplicate = store.create_gpt_review(
            candidate,
            candidate_sha256,
            request_id=body.request_id,
            instrument_version=version,
            model=settings.model,
            effort=settings.effort,
            maximum_jobs=settings.maximum_sessions,
            review_protocol=body.review_protocol,
        )
        view = dict(payload)
        view["duplicate"] = duplicate
        return review_public(view)

    @app.get("/api/gpt/reviews/{review_id}")
    def gpt_review_status(request: Request, review_id: str):
        gpt_submitter(request)
        return review_public(store.gpt_review_read(review_id))

    @app.post("/api/gpt/reviews/{review_id}/clarifications")
    def gpt_review_answer(request: Request, review_id: str, body: GptReviewAnswer):
        gpt_submitter(request)
        if not body.skipped and not body.answer_text.strip():
            raise ValueError("An answer is required unless the participant explicitly skips.")
        if target_exposure(body.answer_text):
            raise ValueError("Omit birth/chart information from this clarification.")
        return review_public(
            store.add_gpt_review_answer(
                review_id,
                body.answer_text,
                clarification_id=body.clarification_id,
                operation_id=body.operation_id,
                skipped=body.skipped,
            )
        )

    @app.post("/api/gpt/reviews/{review_id}/clarification-batches")
    def gpt_review_batch(request: Request, review_id: str, body: GptBatchAnswers):
        gpt_submitter(request)
        for answer in body.answers:
            if target_exposure(answer.answer_text):
                raise ValueError("Omit birth/chart information from clarification answers.")
        return review_public(store.add_gpt_review_batch_answers(
            review_id, body.batch_id, [answer.model_dump() for answer in body.answers], body.operation_id
        ))

    @app.post("/api/gpt/reviews/{review_id}/control")
    def gpt_review_control(request: Request, review_id: str, body: GptReviewControl):
        gpt_submitter(request)
        return review_public(store.control_gpt_review(review_id, body.action, body.operation_id))

    @app.get("/api/review-worker/jobs/next")
    def review_worker_next(request: Request):
        review_worker(request)
        payload = store.claim_gpt_review()
        if payload is None:
            return Response(status_code=204)
        return {
            "schema": "life-patterns-review-worker-job-v1",
            "review_protocol": payload.get("review_protocol", "legacy-v1"),
            "review_stage": payload.get("review_stage"),
            "review_id": payload["review_id"],
            "candidate_sha256": payload["candidate_sha256"],
            "candidate_record": payload["candidate_record"],
            "worker_state": payload.get("worker_state"),
            "clarification_history": payload.get("clarification_history", []),
            "round": payload.get("round", 0),
            "model": payload.get("model", settings.model),
            "effort": payload.get("effort", settings.effort),
            "claim_id": payload["claim_id"],
            "instrument_version": payload.get("instrument_version", version),
            "instrument": store.instrument(payload.get("instrument_version", version)),
        }

    @app.post("/api/review-worker/jobs/{review_id}/heartbeat")
    def review_worker_heartbeat(request: Request, review_id: str, body: WorkerHeartbeat):
        review_worker(request)
        return store.renew_gpt_review(review_id, body.claim_id, review_stage=body.review_stage)

    @app.post("/api/review-worker/jobs/{review_id}/result")
    def review_worker_result(request: Request, review_id: str, body: WorkerReviewResult):
        review_worker(request)
        queued = store.gpt_review_read(review_id)
        if body.receipt.get("instrument_version") != queued.get("instrument_version", version):
            raise ValueError("The worker reviewed a different instrument version.")
        clarification = body.clarification.model_dump() if body.clarification else None
        clarifications = [q.model_dump() for q in body.clarifications] if body.clarifications else None
        fast = queued.get("review_protocol") == PROTOCOL
        if fast and body.receipt.get("source_revision") != source_revision(
            queued["candidate_sha256"], queued.get("clarification_history", [])
        ):
            raise HTTPException(409, "The worker result refers to a stale source revision.")
        if body.status == "clarification_needed":
            if not clarification:
                raise ValueError("Clarification-needed results require one question.")
            questions = clarifications or [clarification]
            if questions[0] != clarification or (not fast and len(questions) > 1):
                raise ValueError("The batch does not match the review protocol.")
            pinned = store.instrument(queued.get("instrument_version", version))
            from .question_policy import selectable
            routes = {row["id"]: row for row in bank(pinned, body.worker_state)["questions"]}
            from .question_policy import participant_purpose
            for question in questions:
                route = routes.get(question["route_id"])
                if route is None:
                    raise ValueError("Worker returned an unknown survey route.")
                if not selectable(route, body.worker_state or {}):
                    raise ValueError("Worker returned a retired or skipped elicitation route.")
                if not str(question.get("participant_purpose") or "").strip():
                    question["participant_purpose"] = participant_purpose(route)
                if (
                    question["route_type"] == "canonical"
                    and question["question_text"] != route["question"]
                ):
                    raise ValueError("Canonical worker question does not match the frozen bank.")
                if target_exposure(question["question_text"]):
                    raise ValueError("Birth/chart questions are not permitted.")
            clarification = questions[0]
            clarifications = questions if body.clarifications else None
            if not body.worker_state or body.worker_state.get("phase") != "awaiting_answer":
                raise ValueError("Clarification results require the saved awaiting-answer state.")
            if fast:
                private = (body.worker_state.get("fast_review") or {}).get("pending_questions")
                if private:
                    from .fast_review import public_question
                    if [public_question(q) for q in private] != questions:
                        raise ValueError("Public batch differs from the saved approved questions.")
        elif clarification is not None or clarifications:
            raise ValueError("Only clarification-needed results may include a question.")
        if body.status == "ready":
            if not body.worker_state or body.worker_state.get("phase") != "review":
                raise ValueError("Ready results require a worker state at independent neutral review.")
            if fast and not (
                body.receipt.get("final_review_completed") is True
                and (body.worker_state.get("fast_review") or {}).get("final_review_completed") is True
                and body.worker_state.get("gpt_review_answers_processed") == len(queued.get("clarification_history", []))
            ):
                raise ValueError("Fast triage alone cannot complete a full review.")
        if body.status == "queued" and not (
            fast and body.worker_state and body.worker_state.get("phase") == "ready"
            and (body.worker_state.get("fast_review") or {}).get("stage") == "final_synthesis"
            and body.receipt.get("next_stage") == "final_synthesis"
        ):
            raise ValueError("Invalid saved stage transition.")
        payload = store.complete_gpt_review(
            review_id,
            body.candidate_sha256,
            body.status,
            claim_id=body.claim_id,
            worker_state=body.worker_state,
            receipt=body.receipt,
            clarification=clarification,
            clarifications=clarifications,
            error=body.error,
        )
        return {"review_id": review_id, "status": payload["status"]}

    @app.post("/api/gpt/submissions")
    def gpt_submission(request: Request, body: GptSubmission):
        gpt_submitter(request)
        primary, secondary, primary_sha256 = validate_gpt_submission(body)
        cf003_sha256 = digest(canonical(secondary))
        submission_sha256 = digest(
            canonical(
                {
                    "review_id": body.review_id,
                    "primary_record": primary,
                    "cf003_record": secondary,
                }
            )
        )
        payload = {
            "schema": "life-patterns-gpt-submission-v1",
            "received_at_utc": utc(),
            "review_id": body.review_id,
            "independent_review": {
                "receipts": store.gpt_review_read(body.review_id).get("worker_receipts", []),
                "worker_state_sha256": digest(
                    canonical(store.gpt_review_read(body.review_id).get("worker_state"))
                ),
                "evidence": (store.gpt_review_read(body.review_id).get("worker_state") or {}).get(
                    "evidence", []
                ),
            }
            if body.review_id
            else None,
            "submission_sha256": submission_sha256,
            "primary_record_sha256": primary_sha256,
            "cf003_record_sha256": cf003_sha256,
            "primary_record": primary,
            "cf003_record": secondary,
        }
        submission_id, stored, duplicate = store.create_gpt_submission(payload, submission_sha256)
        return {
            "schema": "life-patterns-gpt-submission-receipt-v1",
            "submission_id": submission_id,
            "received_at_utc": stored["received_at_utc"],
            "duplicate": duplicate,
            "review_id": stored["review_id"],
            "primary_record_sha256": stored["primary_record_sha256"],
            "cf003_record_sha256": stored["cf003_record_sha256"],
            "stored_encrypted": True,
            "independent_review_completed": body.review_id is not None,
            "inference_started": False,
        }

    @app.post("/api/gpt/reviewed-submissions")
    def gpt_reviewed_submission(request: Request, body: GptReviewedSubmission):
        # This endpoint always binds a ready independent review. A lost opaque
        # handle may be recovered only by matching the entire exact frozen source.
        gpt_submitter(request)
        if body.review_id is None:
            if (
                body.primary_record is not None
                and body.primary_record_json is not None
                and canonical(body.primary_record) != canonical(strict_json(body.primary_record_json))
            ):
                raise ValueError("Primary object and JSON transport disagree.")
            primary = (
                strict_json(body.primary_record_json)
                if body.primary_record_json is not None
                else body.primary_record
            )
            if not isinstance(primary, dict):
                raise ValueError("Exact complete primary record is required for review recovery.")
            body = body.model_copy(update={"review_id": recover_ready_review_id(primary)})
        return gpt_submission(request, body)

    @app.get("/api/admin/sessions")
    def sessions(request: Request):
        admin(request)
        return {"sessions": store.overview()}

    @app.get("/api/admin/gpt-submissions")
    def gpt_submissions(request: Request):
        admin(request)
        return {"submissions": store.gpt_submission_overview()}

    @app.get("/api/admin/question-feedback")
    def question_feedback(request: Request):
        admin(request)
        from .question_feedback import researcher_feedback_overview

        return researcher_feedback_overview(store)

    @app.post("/api/admin/question-feedback/{feedback_id}/disposition")
    def set_feedback_disposition(
        request: Request, feedback_id: str, body: QuestionFeedbackDisposition
    ):
        admin(request)
        if body.status == "revision_proposed" and not body.revision_id:
            raise ValueError("Proposed question revisions require a version identifier.")
        from .question_feedback import researcher_feedback_overview

        current = researcher_feedback_overview(store)["feedback"]
        if feedback_id not in {item["feedback_id"] for item in current}:
            raise HTTPException(status_code=404, detail="Question feedback item unavailable.")
        return store.set_question_feedback_disposition(
            feedback_id, body.status, body.revision_id
        )

    @app.get("/api/admin/gpt-submissions/{submission_id}/primary")
    def gpt_submission_primary(request: Request, submission_id: str):
        admin(request)
        payload = store.gpt_submission_read(submission_id)
        return Response(
            canonical(payload["primary_record"]),
            media_type="application/json",
            headers={
                "Content-Disposition": 'attachment; filename="life-patterns-participant-export.json"'
            },
        )

    @app.get("/api/admin/gpt-submissions/{submission_id}/cf003")
    def gpt_submission_cf003(request: Request, submission_id: str):
        admin(request)
        payload = store.gpt_submission_read(submission_id)
        return Response(
            canonical(payload["cf003_record"]),
            media_type="application/json",
            headers={
                "Content-Disposition": 'attachment; filename="life-patterns-cf003-secondary-v0.json"'
            },
        )

    @app.post("/api/admin/invitations")
    def invitation(request: Request, body: Import):
        admin(request)
        state = new_state(version, settings.model, settings.effort)
        record = body.parsed_record()
        if record is not None:
            import_record(state, record, body.source_type, instrument, body.source_mode)
        value, state = store.create(state, settings.maximum_sessions)
        return {
            "session_id": state["session_id"],
            "resume_path": "/#resume=" + value,
            "turn_count": len(state["turns"]),
            "consent_required": True,
        }

    @app.post("/api/admin/sessions/{session_id}/resume-provider")
    def resume_provider(request: Request, session_id: str, body: ProviderRecovery):
        admin(request)

        def unblock(state):
            if state.get("error") != PAYMENT_ERROR or state["phase"] not in {
                "error",
                "provider_blocked",
            }:
                raise Conflict("This session is not blocked by the provider payment response.")
            state.setdefault("provider_recovery", []).append(
                {"at": utc(), "action": "organizer_acknowledged_billing_repair"}
            )
            state["phase"], state["error"], state["stop_reason"] = "ready", None, None
            state["processing"], state["lease"] = None, None
            state["generation"] += 1

        changed = store.admin_change(session_id, unblock)
        return {"session_id": session_id, "phase": changed["phase"], "inference_started": False}

    @app.get("/api/admin/exports/{session_id}")
    def researcher_export(request: Request, session_id: str):
        admin(request)
        return download_response(store.admin_read(session_id))

    return app


def factory():
    app = create_app(Settings.from_env())
    if not isinstance(app.state.engine.provider, Venice):
        raise RuntimeError("Production participant inference must use the Venice provider.")
    return app
