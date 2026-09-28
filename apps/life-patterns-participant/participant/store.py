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
