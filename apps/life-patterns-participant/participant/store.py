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
from typing import Any, Callable

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
            submission_id = "GPT-" + secrets.token_hex(16)
            db.execute(
                "INSERT INTO gpt_submissions VALUES (?,?,?,?)",
                (submission_id, content_sha256, time.time(), self.encode(payload)),
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
        self, candidate_record: dict, candidate_sha256: str
    ) -> tuple[str, dict, bool]:
        now = time.time()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT id,payload FROM gpt_review_jobs WHERE candidate_sha256=?",
                (candidate_sha256,),
            ).fetchone()
            if row:
                payload = self.decode(row[1])
                if payload.get("status") == "error":
                    payload["status"] = "queued"
                    payload["error"] = None
                    payload["updated_at_unix"] = now
                    db.execute(
                        "UPDATE gpt_review_jobs SET status='queued',updated=?,lease_until=NULL,payload=? "
                        "WHERE id=?",
                        (now, self.encode(payload), row[0]),
                    )
                db.commit()
                return row[0], payload, True
            review_id = "R-" + secrets.token_hex(16)
            payload = {
                "schema": "life-patterns-gpt-review-job-v1",
                "review_id": review_id,
                "candidate_sha256": candidate_sha256,
                "candidate_record": candidate_record,
                "status": "queued",
                "created_at_unix": now,
                "updated_at_unix": now,
                "round": 0,
                "clarification_history": [],
                "worker_state": None,
                "worker_receipts": [],
                "error": None,
            }
            db.execute(
                "INSERT INTO gpt_review_jobs VALUES (?,?,?,?,?,?,?)",
                (
                    review_id,
                    candidate_sha256,
                    "queued",
                    now,
                    now,
                    None,
                    self.encode(payload),
                ),
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

    def claim_gpt_review(self, lease_seconds: int = 1800) -> dict | None:
        now = time.time()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            stale = db.execute(
                "SELECT id,payload FROM gpt_review_jobs "
                "WHERE status='processing' AND lease_until IS NOT NULL AND lease_until<?",
                (now,),
            ).fetchall()
            for review_id, raw in stale:
                payload = self.decode(raw)
                payload["status"] = "queued"
                payload["updated_at_unix"] = now
                payload["worker_recovered_stale_lease"] = True
                db.execute(
                    "UPDATE gpt_review_jobs SET status='queued',updated=?,lease_until=NULL,payload=? "
                    "WHERE id=?",
                    (now, self.encode(payload), review_id),
                )
            row = db.execute(
                "SELECT id,payload FROM gpt_review_jobs "
                "WHERE status='queued' ORDER BY created LIMIT 1"
            ).fetchone()
            if not row:
                db.commit()
                return None
            review_id, raw = row
            payload = self.decode(raw)
            payload["status"] = "processing"
            payload["round"] = int(payload.get("round") or 0) + 1
            payload["updated_at_unix"] = now
            lease_until = now + lease_seconds
            db.execute(
                "UPDATE gpt_review_jobs SET status='processing',updated=?,lease_until=?,payload=? "
                "WHERE id=?",
                (now, lease_until, self.encode(payload), review_id),
            )
            db.commit()
        return payload

    def complete_gpt_review(
        self,
        review_id: str,
        candidate_sha256: str,
        status: str,
        *,
        worker_state: dict | None,
        receipt: dict,
        clarification: dict | None = None,
        error: str | None = None,
    ) -> dict:
        if status not in {"clarification_needed", "ready", "error"}:
            raise ValueError("Unknown GPT review result status.")
        now = time.time()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT status,payload FROM gpt_review_jobs WHERE id=?", (review_id,)
            ).fetchone()
            if not row:
                raise Missing("Unknown GPT review.")
            if row[0] != "processing":
                raise Conflict("This GPT review is not currently claimed by a worker.")
            payload = self.decode(row[1])
            if payload.get("candidate_sha256") != candidate_sha256:
                raise Conflict("The worker result does not match the queued candidate.")
            payload["status"] = status
            payload["updated_at_unix"] = now
            payload["worker_state"] = worker_state
            payload.setdefault("worker_receipts", []).append(receipt)
            payload["error"] = error
            if status == "clarification_needed":
                if not clarification:
                    raise ValueError("A clarification result needs one admitted question.")
                payload["pending_clarification"] = clarification
            else:
                payload["pending_clarification"] = None
            db.execute(
                "UPDATE gpt_review_jobs SET status=?,updated=?,lease_until=NULL,payload=? WHERE id=?",
                (status, now, self.encode(payload), review_id),
            )
            db.commit()
        return payload

    def add_gpt_review_answer(self, review_id: str, answer_text: str) -> dict:
        now = time.time()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT status,payload FROM gpt_review_jobs WHERE id=?", (review_id,)
            ).fetchone()
            if not row:
                raise Missing("Unknown GPT review.")
            if row[0] != "clarification_needed":
                raise Conflict("This review is not waiting for a clarification answer.")
            payload = self.decode(row[1])
            clarification = payload.get("pending_clarification")
            if not isinstance(clarification, dict):
                raise Conflict("The saved clarification question is unavailable.")
            payload.setdefault("clarification_history", []).append(
                {
                    "route_id": clarification.get("route_id"),
                    "question_text": clarification.get("question_text"),
                    "antecedent_turn_ids": clarification.get("antecedent_turn_ids") or [],
                    "answer_text": answer_text,
                    "answered_at_unix": now,
                }
            )
            payload["pending_clarification"] = None
            payload["status"] = "queued"
            payload["updated_at_unix"] = now
            payload["error"] = None
            db.execute(
                "UPDATE gpt_review_jobs SET status='queued',updated=?,lease_until=NULL,payload=? "
                "WHERE id=?",
                (now, self.encode(payload), review_id),
            )
            db.commit()
        return payload
