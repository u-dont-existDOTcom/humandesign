"""Encrypted durable state; raw capabilities are not stored in the database."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from collections.abc import Callable

from cryptography.fernet import Fernet


def canonical(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    )


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


class Conflict(ValueError):
    pass


class Missing(ValueError):
    pass


class Store:
    def __init__(self, path: Path, encryption_key: str) -> None:
        self.path = path
        self.cipher = Fernet(encryption_key.encode())
        path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript("""
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY, token_hash TEXT UNIQUE NOT NULL,
                    created REAL NOT NULL, revision INTEGER NOT NULL, payload BLOB NOT NULL
                );
                CREATE TABLE IF NOT EXISTS instruments (
                    version TEXT PRIMARY KEY, payload BLOB NOT NULL
                );
                CREATE TABLE IF NOT EXISTS gpt_submissions (
                    id TEXT PRIMARY KEY,
                    content_sha256 TEXT UNIQUE NOT NULL,
                    created REAL NOT NULL,
                    payload BLOB NOT NULL
                );
                CREATE TABLE IF NOT EXISTS gpt_review_jobs (
                    id TEXT PRIMARY KEY,
                    candidate_sha256 TEXT UNIQUE NOT NULL,
                    status TEXT NOT NULL,
                    created REAL NOT NULL,
                    updated REAL NOT NULL,
                    lease_until REAL,
                    payload BLOB NOT NULL
                );
                CREATE TABLE IF NOT EXISTS gpt_review_finalizations (
                    review_id TEXT PRIMARY KEY, submission_id TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_gpt_review_status
                    ON gpt_review_jobs(status, created);
            """)
        os.chmod(path, 0o600)

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        db.execute("PRAGMA busy_timeout=15000")
        db.execute("PRAGMA synchronous=FULL")
        try:
            yield db
        finally:
            db.close()

    def encode(self, value: Any) -> bytes:
        return self.cipher.encrypt(canonical(value).encode())

    def decode(self, raw: bytes) -> Any:
        return json.loads(self.cipher.decrypt(raw))

    def pin_instrument(self, instrument: dict) -> str:
        version = digest(canonical(instrument))
        with self.connection() as db:
            db.execute(
                "INSERT OR IGNORE INTO instruments VALUES (?,?)", (version, self.encode(instrument))
            )
        return version

    def instrument(self, version: str) -> dict:
        with self.connection() as db:
            row = db.execute(
                "SELECT payload FROM instruments WHERE version=?", (version,)
            ).fetchone()
        if not row:
            raise Missing("Pinned survey authority is unavailable; do not recreate it from memory.")
        return self.decode(row[0])

    def create(self, state: dict, maximum_sessions: int) -> tuple[str, dict]:
        token = secrets.token_urlsafe(32)
        state = dict(state, session_id=secrets.token_hex(16), revision=0)
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT count(*) FROM sessions").fetchone()[0] >= maximum_sessions:
                db.rollback()
                raise Conflict(
                    "The study is not accepting additional sessions. Ask the researcher."
                )
            db.execute(
                "INSERT INTO sessions VALUES (?,?,?,?,?)",
                (state["session_id"], digest(token), time.time(), 0, self.encode(state)),
            )
            db.commit()
        return token, state

    def read(self, token: str) -> dict:
        if not isinstance(token, str) or not 32 <= len(token) <= 128:
            raise Missing("Session access required.")
        with self.connection() as db:
            row = db.execute(
                "SELECT payload FROM sessions WHERE token_hash=?", (digest(token),)
            ).fetchone()
        if row is None:
            raise Missing("Session access required.")
        return self.decode(row[0])

    def change(self, token: str, operation: Callable[[dict], None]) -> dict:
        return self._change("token_hash", digest(token), operation)

    def admin_change(self, session_id: str, operation: Callable[[dict], None]) -> dict:
        return self._change("id", session_id, operation)

    def _change(self, column: str, value: str, operation: Callable[[dict], None]) -> dict:
        if column not in {"id", "token_hash"}:
            raise ValueError("Unsupported lookup")
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                f"SELECT revision,payload FROM sessions WHERE {column}=?", (value,)
            ).fetchone()
            if not row:
                raise Missing("Session access required.")
            state = self.decode(row[1])
            before = canonical(state)
            operation(state)
            if canonical(state) == before:
                db.commit()
                return state
            state["revision"] = row[0] + 1
            db.execute(
                f"UPDATE sessions SET revision=?,payload=? WHERE {column}=?",
                (state["revision"], self.encode(state), value),
            )
            db.commit()
        return state

    def overview(self) -> list[dict]:
        with self.connection() as db:
            rows = db.execute("SELECT payload FROM sessions ORDER BY created DESC").fetchall()
        return [
            {k: state[k] for k in ("session_id", "phase", "created_at", "revision")}
            | {
                "turn_count": len(state["turns"]),
                "error_code": state.get("error"),
                "collection_mode": state.get("collection_mode", "unknown"),
                "model_calls": sum(
                    1 for call in state.get("calls", []) if call.get("provider") == "venice"
                ),
                "prompt_tokens": sum(
                    int(call.get("prompt_tokens") or 0) for call in state.get("calls", [])
                ),
                "completion_tokens": sum(
                    int(call.get("completion_tokens") or 0) for call in state.get("calls", [])
                ),
                "request_chars": sum(
                    int(call.get("request_chars") or 0) for call in state.get("calls", [])
                ),
            }
            for row in rows
            for state in [self.decode(row[0])]
        ]

    def admin_read(self, session_id: str) -> dict:
        with self.connection() as db:
            row = db.execute("SELECT payload FROM sessions WHERE id=?", (session_id,)).fetchone()
        if not row:
            raise Missing("Unknown session.")
        return self.decode(row[0])

    def create_gpt_submission(
        self, payload: dict, content_sha256: str | None = None
    ) -> tuple[str, dict, bool]:
        content_sha256 = content_sha256 or digest(canonical(payload))
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT id,payload FROM gpt_submissions WHERE content_sha256=?",
                (content_sha256,),
            ).fetchone()
            if row:
                db.commit()
                return row[0], self.decode(row[1]), True
            review_id = payload.get("review_id")
            if review_id:
                if db.execute(
                    "SELECT submission_id FROM gpt_review_finalizations WHERE review_id=?",
                    (review_id,),
                ).fetchone():
                    raise Conflict(
                        "This review already has a frozen submission; only exact retries are allowed."
                    )
                state_row = db.execute(
                    "SELECT status FROM gpt_review_jobs WHERE id=?", (review_id,)
                ).fetchone()
                if not state_row or state_row[0] != "ready":
                    raise Conflict(
                        "The review was paused, stopped or withdrawn before final storage."
                    )
            submission_id = "GPT-" + secrets.token_hex(16)
            db.execute(
                "INSERT INTO gpt_submissions VALUES (?,?,?,?)",
                (submission_id, content_sha256, time.time(), self.encode(payload)),
            )
            if review_id:
                db.execute(
                    "INSERT INTO gpt_review_finalizations VALUES (?,?)", (review_id, submission_id)
                )
            db.commit()
        return submission_id, payload, False

    def gpt_submission_overview(self) -> list[dict]:
        with self.connection() as db:
            rows = db.execute(
                "SELECT id,created,payload FROM gpt_submissions ORDER BY created DESC"
            ).fetchall()
        result = []
        for submission_id, created, raw in rows:
            payload = self.decode(raw)
            primary = payload.get("primary_record") or {}
            secondary = payload.get("cf003_record") or {}
            result.append(
                {
                    "submission_id": submission_id,
                    "received_at_utc": payload.get("received_at_utc"),
                    "created_unix": created,
                    "collection_mode": primary.get("collection_mode", "unknown"),
                    "primary_turn_count": len(primary.get("turns") or []),
                    "cf003_turn_count": len(secondary.get("turns") or []),
                    "primary_record_sha256": payload.get("primary_record_sha256"),
                }
            )
        return result

    def gpt_submission_read(self, submission_id: str) -> dict:
        with self.connection() as db:
            row = db.execute(
                "SELECT payload FROM gpt_submissions WHERE id=?", (submission_id,)
            ).fetchone()
        if not row:
            raise Missing("Unknown GPT submission.")
        return self.decode(row[0])

    def create_gpt_review(
        self,
        candidate_record: dict,
        candidate_sha256: str,
        *,
        request_id: str,
        instrument_version: str,
        model: str,
        effort: str,
        maximum_jobs: int = 50,
    ) -> tuple[str, dict, bool]:
        # The legacy SQL column holds the idempotency-key digest. The actual
        # source digest remains in the encrypted payload. Equal answers from two
        # people must NOT disclose the same private review capability.
        request_key = digest(request_id)
        now = time.time()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT id,payload FROM gpt_review_jobs WHERE candidate_sha256=?",
                (request_key,),
            ).fetchone()
            if row:
                payload = self.decode(row[1])
                if payload["candidate_sha256"] != candidate_sha256:
                    raise Conflict("A review request ID was reused for different source data.")
                db.commit()
                return row[0], payload, True
            if db.execute("SELECT count(*) FROM gpt_review_jobs").fetchone()[0] >= maximum_jobs:
                raise Conflict("The pilot review limit has been reached; saved records are safe.")
            review_id = "R-" + secrets.token_hex(16)
            payload = {
                "schema": "life-patterns-gpt-review-job-v2",
                "review_id": review_id,
                "candidate_sha256": candidate_sha256,
                "candidate_record": candidate_record,
                "status": "queued",
                "instrument_version": instrument_version,
                "model": model,
                "effort": effort,
                "created_at_unix": now,
                "updated_at_unix": now,
                "round": 0,
                "claim_attempts": 0,
                "clarification_history": [],
                "worker_state": None,
                "worker_receipts": [],
                "completed_claims": {},
                "operations": {},
                "error": None,
            }
            db.execute(
                "INSERT INTO gpt_review_jobs VALUES (?,?,?,?,?,?,?)",
                (review_id, request_key, "queued", now, now, None, self.encode(payload)),
            )
            db.commit()
        return review_id, payload, False

    def gpt_review_read(self, review_id: str) -> dict:
        with self.connection() as db:
            row = db.execute(
                "SELECT payload FROM gpt_review_jobs WHERE id=?", (review_id,)
            ).fetchone()
        if not row:
            raise Missing("Unknown GPT review.")
        return self.decode(row[0])

    def _save_review(self, db, payload: dict, lease_until: float | None = None) -> None:
        db.execute(
            "UPDATE gpt_review_jobs SET status=?,updated=?,lease_until=?,payload=? WHERE id=?",
            (
                payload["status"],
                payload["updated_at_unix"],
                lease_until,
                self.encode(payload),
                payload["review_id"],
            ),
        )

    def claim_gpt_review(self, lease_seconds: int = 180) -> dict | None:
        now = time.time()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT id,payload FROM gpt_review_jobs WHERE status='queued' OR "
                "(status='processing' AND lease_until<?) ORDER BY created LIMIT 1",
                (now,),
            ).fetchone()
            if not row:
                db.commit()
                return None
            payload = self.decode(row[1])
            if payload["status"] == "processing":
                payload["worker_recovered_stale_lease"] = True
            payload.update(
                status="processing",
                claim_id="L-" + secrets.token_hex(16),
                updated_at_unix=now,
                worker_heartbeat_at_unix=now,
            )
            payload["claim_attempts"] = int(payload.get("claim_attempts", 0)) + 1
            payload["lease_until"] = now + lease_seconds
            self._save_review(db, payload, payload["lease_until"])
            db.commit()
        return payload

    def renew_gpt_review(self, review_id: str, claim_id: str, lease_seconds: int = 180) -> dict:
        now = time.time()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT payload FROM gpt_review_jobs WHERE id=?", (review_id,)
            ).fetchone()
            if not row:
                raise Missing("Unknown GPT review.")
            payload = self.decode(row[0])
            self._require_review_claim(payload, claim_id, now)
            payload.update(
                worker_heartbeat_at_unix=now, updated_at_unix=now, lease_until=now + lease_seconds
            )
            self._save_review(db, payload, payload["lease_until"])
            db.commit()
        return {"review_id": review_id, "status": "processing", "lease_seconds": lease_seconds}

    @staticmethod
    def _require_review_claim(payload: dict, claim_id: str, now: float) -> None:
        if (
            payload["status"] != "processing"
            or payload.get("claim_id") != claim_id
            or payload.get("lease_until", 0) <= now
        ):
            raise Conflict("Worker claim expired or was superseded; do not apply this result.")

    def complete_gpt_review(
        self,
        review_id: str,
        candidate_sha256: str,
        status: str,
        *,
        claim_id: str,
        worker_state: dict | None,
        receipt: dict,
        clarification: dict | None = None,
        error: str | None = None,
    ) -> dict:
        if status not in {
            "clarification_needed",
            "ready",
            "error",
            "paused",
            "stopped",
            "resource_limited",
        }:
            raise ValueError("Unknown GPT review result status.")
        result_hash = digest(
            canonical(
                {
                    "candidate": candidate_sha256,
                    "status": status,
                    "state": worker_state,
                    "receipt": receipt,
                    "clarification": clarification,
                    "error": error,
                }
            )
        )
        now = time.time()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT payload FROM gpt_review_jobs WHERE id=?", (review_id,)
            ).fetchone()
            if not row:
                raise Missing("Unknown GPT review.")
            payload = self.decode(row[0])
            completed = payload.setdefault("completed_claims", {})
            if claim_id in completed:
                if completed[claim_id] != result_hash:
                    raise Conflict("A completed worker claim was replayed with different results.")
                db.commit()
                return payload
            self._require_review_claim(payload, claim_id, now)
            if payload["candidate_sha256"] != candidate_sha256:
                raise Conflict("The worker result does not match the queued candidate.")
            payload.update(status=status, updated_at_unix=now, error=error, lease_until=None)
            if status == "error":
                # A failed delivery/analysis cannot destroy the last valid source
                # state. Retain any recorded attempt usage without admitting the
                # failed candidate's semantic state.
                previous = payload.get("worker_state")
                if previous and worker_state and worker_state.get("calls"):
                    previous["calls"] = worker_state["calls"]
            elif worker_state is not None:
                payload["worker_state"] = worker_state
            completed[claim_id] = result_hash
            payload.setdefault("worker_receipts", []).append(receipt)
            if status == "clarification_needed":
                if not clarification:
                    raise ValueError("A clarification result needs one admitted question.")
                payload["pending_clarification"] = dict(clarification) | {
                    "clarification_id": "Q-" + secrets.token_hex(16)
                }
            else:
                payload["pending_clarification"] = None
            self._save_review(db, payload)
            db.commit()
        return payload

    def add_gpt_review_answer(
        self,
        review_id: str,
        answer_text: str,
        *,
        clarification_id: str,
        operation_id: str,
        skipped: bool = False,
    ) -> dict:
        signature = digest(
            canonical({"question": clarification_id, "text": answer_text, "skipped": skipped})
        )
        now = time.time()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT payload FROM gpt_review_jobs WHERE id=?", (review_id,)
            ).fetchone()
            if not row:
                raise Missing("Unknown GPT review.")
            payload = self.decode(row[0])
            operations = payload.setdefault("operations", {})
            if operation_id in operations:
                if operations[operation_id] != signature:
                    raise Conflict(
                        "A clarification operation ID was reused with different content."
                    )
                db.commit()
                return payload
            question = payload.get("pending_clarification") or {}
            if (
                payload["status"] != "clarification_needed"
                or question.get("clarification_id") != clarification_id
            ):
                raise Conflict("This answer does not match the pending clarification.")
            payload["clarification_history"].append(
                dict(question)
                | {
                    "answer_text": None if skipped else answer_text,
                    "answer_status": "skipped" if skipped else "answered",
                    "answered_at_unix": now,
                }
            )
            operations[operation_id] = signature
            payload.update(
                pending_clarification=None,
                status="queued",
                updated_at_unix=now,
                error=None,
                round=len(payload["clarification_history"]),
            )
            self._save_review(db, payload)
            db.commit()
        return payload

    def control_gpt_review(self, review_id: str, action: str, operation_id: str) -> dict:
        now = time.time()
        signature = digest("control:" + action)
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT payload FROM gpt_review_jobs WHERE id=?", (review_id,)
            ).fetchone()
            if not row:
                raise Missing("Unknown GPT review.")
            payload = self.decode(row[0])
            operations = payload.setdefault("operations", {})
            if operation_id in operations:
                if operations[operation_id] != signature:
                    raise Conflict("Control operation ID reused for a different action.")
                db.commit()
                return payload
            current = payload["status"]
            if action in {"pause", "stop", "withdraw"}:
                if current in {"stopped", "withdrawn"} and action != "withdraw":
                    return payload
                if current == "paused" and action == "pause":
                    return payload
                if action == "withdraw":
                    if db.execute(
                        "SELECT 1 FROM gpt_review_finalizations WHERE review_id=?", (review_id,)
                    ).fetchone():
                        raise Conflict(
                            "This record was already submitted; request removal through the researcher."
                        )
                    payload.update(
                        status="withdrawn",
                        candidate_record={},
                        worker_state=None,
                        clarification_history=[],
                        worker_receipts=[],
                        completed_claims={},
                        pending_clarification=None,
                        claim_id=None,
                        lease_until=None,
                        updated_at_unix=now,
                        error=None,
                    )
                    operations[operation_id] = signature
                    self._save_review(db, payload)
                    db.commit()
                    return payload
                payload["resume_status"] = "queued" if current == "processing" else current
                payload["status"] = "paused" if action == "pause" else "stopped"
                payload["claim_id"] = None
                payload["lease_until"] = None
            elif action == "resume":
                if current != "paused":
                    raise Conflict("This review is not paused.")
                payload["status"] = payload.get("resume_status", "queued")
                if payload["status"] in {"paused", "processing"}:
                    payload["status"] = "queued"
            elif action == "retry":
                if current not in {"error", "resource_limited"}:
                    raise Conflict(
                        "Retry is only available after a recoverable worker "
                        "or resource-limit error."
                    )
                worker_state = payload.get("worker_state")
                if isinstance(worker_state, dict):
                    calls = worker_state.get("calls") or []
                    prior_model_calls = sum(
                        1
                        for call in calls
                        if isinstance(call, dict)
                        and call.get("stage") in {"Plan", "Admission"}
                        and call.get("provider") != "deterministic"
                    )
                    # The historical calls stay in the audit trail. A deliberate
                    # retry after an operator-side repair gets a fresh bounded call
                    # epoch instead of immediately exhausting the same review on
                    # attempts spent diagnosing the repaired infrastructure fault.
                    # A zero-call transport error needs no epoch metadata and stays
                    # byte-for-byte compatible with the prior resumable state.
                    try:
                        budget_epoch = max(
                            0, int(worker_state.get("model_call_budget_epoch", 0) or 0)
                        )
                    except (TypeError, ValueError):
                        budget_epoch = 0
                    if current == "resource_limited" and prior_model_calls and budget_epoch == 0:
                        worker_state["model_call_budget_baseline"] = prior_model_calls
                        worker_state["model_call_budget_epoch"] = 1
                        worker_state["model_call_budget_reset_reason"] = payload.get("error")
                    if current == "resource_limited" and worker_state.get(
                        "phase"
                    ) == "resource_limited":
                        worker_state["phase"] = "ready"
                        worker_state["error"] = None
                        worker_state["stop_reason"] = None
                        worker_state["lease"] = None
                        worker_state["processing"] = None
                payload.update(status="queued", error=None)
            else:
                raise ValueError("Unknown review control.")
            payload["updated_at_unix"] = now
            operations[operation_id] = signature
            self._save_review(db, payload)
            db.commit()
        return payload
