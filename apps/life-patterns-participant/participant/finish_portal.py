"""Narrow, one-time handoff from ready GPT review to final Railway browser.

No GPT service credential, DOB, source answer or review ID is placed in links.
Raw capability tokens are never persisted. Finish sessions cannot review or
change a queued review; they exist solely for a ready review's finalization.
"""

from __future__ import annotations

import copy
import secrets
import time
from dataclasses import dataclass

from .store import Conflict, Missing, Store, digest

LINK_TTL_SECONDS = 20 * 60
SESSION_TTL_SECONDS = 7 * 24 * 60 * 60
COOKIE_NAME = "lp_finish"


@dataclass(frozen=True)
class FinishCapability:
    session_hash: str
    review_id: str
    csrf_hash: str
    expires_at: float
    summary_shown: bool
    submission_id: str | None
    final_input_hash: str | None


class FinishSessions:
    def __init__(self, store: Store):
        self.store = store
        with store.connection() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS gpt_finish_links(
                  token_hash TEXT PRIMARY KEY,
                  review_id TEXT NOT NULL,
                  expires_at REAL NOT NULL,
                  used INTEGER NOT NULL DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS idx_gpt_finish_links_review
                  ON gpt_finish_links(review_id);
                CREATE TABLE IF NOT EXISTS gpt_finish_sessions(
                  session_hash TEXT PRIMARY KEY,
                  review_id TEXT NOT NULL,
                  csrf_hash TEXT NOT NULL,
                  expires_at REAL NOT NULL,
                  summary_shown INTEGER NOT NULL DEFAULT 0,
                  submission_id TEXT,
                  final_input_hash TEXT
                );
            """)

    def issue_link(self, review_id: str) -> tuple[str, int]:
        token = secrets.token_urlsafe(32)
        now = time.time()
        with self.store.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT status FROM gpt_review_jobs WHERE id=?", (review_id,)
            ).fetchone()
            if not row or row[0] not in {
                "queued",
                "processing",
                "clarification_needed",
                "ready",
                "paused",
                "error",
                "resource_limited",
            }:
                raise Conflict("Only an existing active or review-ready record can open Railway.")
            submitted = db.execute(
                "SELECT 1 FROM gpt_review_finalizations WHERE review_id=?", (review_id,)
            ).fetchone()
            if submitted:
                raise Conflict("This review was already submitted.")
            # Latest link supersedes prior unredeemed tokens; existing sessions
            # are retained, so reopening the GPT cannot destroy a participant's work.
            db.execute(
                "UPDATE gpt_finish_links SET expires_at=0 WHERE review_id=? AND used=0",
                (review_id,),
            )
            db.execute(
                "INSERT INTO gpt_finish_links(token_hash,review_id,expires_at,used) "
                "VALUES (?,?,?,0)",
                (digest(token), review_id, now + LINK_TTL_SECONDS),
            )
            db.commit()
        return token, LINK_TTL_SECONDS

    def redeem(self, token: str) -> tuple[str, str]:
        if not isinstance(token, str) or not 32 <= len(token) <= 128:
            raise Missing("Finish link unavailable or expired.")
        now = time.time()
        session = secrets.token_urlsafe(32)
        csrf = secrets.token_urlsafe(32)
        with self.store.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT review_id,expires_at,used FROM gpt_finish_links WHERE token_hash=?",
                (digest(token),),
            ).fetchone()
            if not row or row[2] or row[1] <= now:
                raise Missing("Finish link unavailable or expired.")
            review_id = row[0]
            ready = db.execute(
                "SELECT status FROM gpt_review_jobs WHERE id=?", (review_id,)
            ).fetchone()
            if not ready or ready[0] not in {
                "queued",
                "processing",
                "clarification_needed",
                "ready",
                "paused",
                "error",
                "resource_limited",
            }:
                raise Conflict("Review is no longer available; use the original conversation.")
            if db.execute(
                "SELECT 1 FROM gpt_review_finalizations WHERE review_id=?", (review_id,)
            ).fetchone():
                raise Conflict("This review is already submitted.")
            db.execute(
                "UPDATE gpt_finish_links SET used=1 WHERE token_hash=?",
                (digest(token),),
            )
            db.execute(
                "INSERT INTO gpt_finish_sessions "
                "(session_hash,review_id,csrf_hash,expires_at) VALUES (?,?,?,?)",
                (digest(session), review_id, digest(csrf), now + SESSION_TTL_SECONDS),
            )
            db.commit()
        return session, csrf

    def session(self, token: str) -> FinishCapability:
        if not isinstance(token, str) or not 32 <= len(token) <= 128:
            raise Missing("Private finish session required.")
        with self.store.connection() as db:
            row = db.execute(
                "SELECT review_id,csrf_hash,expires_at,summary_shown,"
                "submission_id,final_input_hash "
                "FROM gpt_finish_sessions WHERE session_hash=?",
                (digest(token),),
            ).fetchone()
        if not row or row[2] <= time.time():
            raise Missing("Private finish session expired.")
        return FinishCapability(digest(token), row[0], row[1], row[2], bool(row[3]), row[4], row[5])

    def require_csrf(self, session: FinishCapability, csrf: str) -> None:
        if not csrf or not secrets.compare_digest(session.csrf_hash, digest(csrf)):
            raise Conflict("Session confirmation token mismatch.")

    def mark_summary_shown(self, session: FinishCapability) -> None:
        with self.store.connection() as db:
            db.execute(
                "UPDATE gpt_finish_sessions SET summary_shown=1 "
                "WHERE session_hash=? AND expires_at>?",
                (session.session_hash, time.time()),
            )

    def rotate_csrf(self, session: FinishCapability) -> str:
        token = secrets.token_urlsafe(32)
        with self.store.connection() as db:
            db.execute(
                "UPDATE gpt_finish_sessions SET csrf_hash=? WHERE session_hash=? AND expires_at>?",
                (digest(token), session.session_hash, time.time()),
            )
        return token

    def submitted_receipt(self, session: FinishCapability) -> dict | None:
        if session.submission_id:
            saved = self.store.gpt_submission_read(session.submission_id)
            return {
                "submission_id": session.submission_id,
                "stored_encrypted": True,
                "independent_review_completed": True,
                "primary_record_sha256": saved["primary_record_sha256"],
                "cf003_record_sha256": saved["cf003_record_sha256"],
                "duplicate": True,
            }
        return None


def frozen_primary(job: dict, *, confirmed_at: str) -> dict:
    """Rebuild exact reviewed behavior only; no independent coding or relabeling."""
    if job.get("status") != "ready":
        raise Conflict("Independent review has not completed.")
    candidate = job.get("candidate_record")
    if not isinstance(candidate, dict):
        raise ValueError("The reviewed source record is missing.")
    primary = copy.deepcopy(candidate)
    original = primary.get("turns")
    if not isinstance(original, list):
        raise ValueError("The original source turns are unavailable.")
    for index, item in enumerate(job.get("clarification_history") or [], 1):
        skipped = item.get("answer_status") == "skipped"
        if not skipped and item.get("answer_status") != "answered":
            raise ValueError("A clarification lacks verified answer status.")
        if not item.get("question_text") or not item.get("route_id"):
            raise ValueError("A stored clarification lacks source identity.")
        if not skipped and not isinstance(item.get("answer_text"), str):
            raise ValueError("Clarification answer text missing.")
        original.append(
            {
                "turn_id": f"review-answer-{index:04d}",
                "question_text": item["question_text"],
                "answer_text": None if skipped else item["answer_text"],
                "canonical_question_id": item["route_id"],
                "turn_role": "behavioral",
                "correction_of": None,
                "conditions": [],
                "corrections": [],
                "process_feedback": [],
            }
        )
    primary["participant_review"] = {
        **(primary.get("participant_review") or {}),
        "summary_shown": True,
        "confirmed": True,
        "confirmed_at_utc": confirmed_at,
        "confirmation_channel": "railway_finish",
    }
    primary["freeze"] = {
        **(primary.get("freeze") or {}),
        "record_state": "final",
        "frozen_before_birth_or_chart_reveal": True,
        "birth_or_chart_data_in_this_export": False,
        "freeze_channel": "railway_finish",
    }
    return primary


def cf003_secondary(source_questions: list[dict], answers: list[dict], metadata: dict) -> dict:
    if len(source_questions) != 3 or len(answers) != 3:
        raise ValueError("All three source-fixed CF003 questions are required.")
    turns = []
    for i, (question, item) in enumerate(zip(source_questions, answers, strict=True)):
        if item.get("question_id") != question["question_id"]:
            raise ValueError(f"CF003 answer {i + 1} has the wrong question ID.")
        text = item.get("answer_text")
        if not isinstance(text, str) or not text.strip() or len(text) > 20000:
            raise ValueError(f"CF003 answer {i + 1} must be non-empty and bounded.")
        turns.append(
            {
                "question_id": question["question_id"],
                "question_text": question["question"],
                "answer_text": text,
                "turn_role": "behavioral",
            }
        )
    for key, wording in (
        ("rising_sign_previously_known", "Did you know your rising sign before the interview?"),
        (
            "previous_natal_chart_reading",
            "Had you received a natal-chart reading before the interview?",
        ),
        ("target_information_exposure", "Was birth/chart material visible during the interview?"),
    ):
        response = metadata.get(key)
        allowed = ("yes", "no", "unsure", "prefer_not_to_say")
        if response not in allowed:
            raise ValueError("Post-freeze chart-familiarity metadata is missing or invalid.")
        turns.append(
            {
                "turn_role": "collection_metadata",
                "question_id": "META-" + key,
                "question_text": wording,
                "answer_text": response,
            }
        )
    return {
        "schema_version": "life-patterns-cf003-secondary-v0",
        "collection_mode": "railway_finish",
        "turns": turns,
        "freeze": {"state": "final", "birth_or_chart_data_in_this_export": False},
    }
