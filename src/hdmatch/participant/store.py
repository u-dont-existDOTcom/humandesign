"""Append-only filesystem storage for participant sessions."""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_bytes,
    sha256_file,
    write_new_canonical_json,
)

from .models import (
    ConfirmatoryLock,
    EvidenceRecord,
    ExploratoryRankingReport,
    FinalParticipantReport,
    PredictionFreeze,
    RankingSnapshot,
    RevealReport,
    SessionRecord,
)

try:
    import fcntl
except ImportError:  # pragma: no cover - supported deployment target is POSIX
    fcntl = None  # type: ignore[assignment]


_SESSION_RE = re.compile(r"^HD-[A-F0-9]{32}$")
T = TypeVar("T", bound=BaseModel)


class SessionStorageError(RuntimeError):
    """Raised when persisted session state is missing, corrupt, or inconsistent."""


class ParticipantSessionStore:
    """Canonical append-only storage with a hash-chained evidence log."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def _directory(self, session_id: str) -> Path:
        if not _SESSION_RE.fullmatch(session_id):
            raise ValueError("invalid participant session ID")
        return self.root / session_id

    def create(self, record: SessionRecord, freeze: PredictionFreeze) -> None:
        directory = self._directory(record.session_id)
        if freeze.session_id != record.session_id:
            raise ValueError("session and prediction freeze IDs differ")
        try:
            directory.mkdir(parents=True, exist_ok=False)
            freeze_path = directory / "prediction.freeze.json"
            write_new_canonical_json(freeze_path, freeze)
            if sha256_file(freeze_path) != record.prediction_freeze_sha256:
                raise SessionStorageError("prediction freeze hash does not match session record")
            write_new_canonical_json(directory / "session.json", record)
        except BaseException:
            if not (directory / "session.json").exists():
                shutil.rmtree(directory, ignore_errors=True)
            raise

    def load_session(self, session_id: str) -> SessionRecord:
        directory = self._directory(session_id)
        try:
            record = SessionRecord.model_validate(
                load_json_bytes(directory / "session.json", require_canonical=True)
            )
        except (OSError, ValueError) as exc:
            raise SessionStorageError(f"invalid or missing session: {session_id}") from exc
        freeze_path = directory / "prediction.freeze.json"
        try:
            actual_hash = sha256_file(freeze_path)
        except OSError as exc:
            raise SessionStorageError("prediction freeze is missing") from exc
        if actual_hash != record.prediction_freeze_sha256:
            raise SessionStorageError("prediction freeze bytes changed after session creation")
        return record

    def load_freeze(self, session_id: str) -> PredictionFreeze:
        self.load_session(session_id)
        try:
            value = load_json_bytes(
                self._directory(session_id) / "prediction.freeze.json",
                require_canonical=True,
            )
            freeze = PredictionFreeze.model_validate(value)
        except (OSError, ValueError) as exc:
            raise SessionStorageError("invalid prediction freeze") from exc
        if freeze.session_id != session_id:
            raise SessionStorageError("prediction freeze belongs to a different session")
        return freeze

    def append_evidence(self, record: EvidenceRecord) -> None:
        self.load_session(record.session_id)
        directory = self._directory(record.session_id)
        event_path = directory / "evidence.events.jsonl"
        lock_path = directory / ".evidence.lock"
        lock_path.touch(exist_ok=True)
        with lock_path.open("rb") as lock_handle:
            if fcntl is not None:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            try:
                existing = self._read_event_envelopes(event_path)
                previous = existing[-1]["event_sha256"] if existing else None
                sequence = len(existing) + 1
                body = {
                    "sequence": sequence,
                    "previous_event_sha256": previous,
                    "payload": record.model_dump(mode="json"),
                }
                envelope = {**body, "event_sha256": sha256_bytes(canonical_json_bytes(body))}
                line = canonical_json_bytes(envelope) + b"\n"
                descriptor = os.open(event_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
                try:
                    os.write(descriptor, line)
                    os.fsync(descriptor)
                finally:
                    os.close(descriptor)
            finally:
                if fcntl is not None:
                    fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)

    def load_evidence(self, session_id: str) -> tuple[EvidenceRecord, ...]:
        self.load_session(session_id)
        path = self._directory(session_id) / "evidence.events.jsonl"
        envelopes = self._read_event_envelopes(path)
        records: list[EvidenceRecord] = []
        for envelope in envelopes:
            try:
                record = EvidenceRecord.model_validate(envelope["payload"])
            except ValueError as exc:
                raise SessionStorageError("invalid evidence event payload") from exc
            if record.session_id != session_id:
                raise SessionStorageError("evidence event belongs to a different session")
            records.append(record)
        return tuple(records)

    def _read_event_envelopes(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        try:
            raw_lines = path.read_bytes().splitlines()
        except OSError as exc:
            raise SessionStorageError("cannot read evidence event log") from exc
        previous: str | None = None
        envelopes: list[dict[str, Any]] = []
        for expected_sequence, raw in enumerate(raw_lines, start=1):
            try:
                envelope = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise SessionStorageError("evidence event log contains invalid JSON") from exc
            if not isinstance(envelope, dict):
                raise SessionStorageError("evidence event envelope must be an object")
            if envelope.get("sequence") != expected_sequence:
                raise SessionStorageError("evidence event sequence is not contiguous")
            if envelope.get("previous_event_sha256") != previous:
                raise SessionStorageError("evidence event hash chain is broken")
            event_hash = envelope.get("event_sha256")
            body = {
                "sequence": envelope.get("sequence"),
                "previous_event_sha256": envelope.get("previous_event_sha256"),
                "payload": envelope.get("payload"),
            }
            calculated = sha256_bytes(canonical_json_bytes(body))
            if event_hash != calculated:
                raise SessionStorageError("evidence event digest is invalid")
            previous = calculated
            envelopes.append(envelope)
        return envelopes

    def write_confirmatory_lock(self, value: ConfirmatoryLock) -> None:
        self._write_artifact(value.session_id, "confirmatory.lock.json", value)

    def load_confirmatory_lock(self, session_id: str) -> ConfirmatoryLock | None:
        return self._load_optional(
            session_id, "confirmatory.lock.json", ConfirmatoryLock
        )

    def write_confirmatory_ranking(self, value: RankingSnapshot) -> None:
        self._write_artifact(value.session_id, "confirmatory.ranking.json", value)

    def load_confirmatory_ranking(self, session_id: str) -> RankingSnapshot | None:
        return self._load_optional(
            session_id, "confirmatory.ranking.json", RankingSnapshot
        )

    def write_reveal(self, value: RevealReport) -> None:
        self._write_artifact(value.session_id, "reveal.json", value)

    def load_reveal(self, session_id: str) -> RevealReport | None:
        return self._load_optional(session_id, "reveal.json", RevealReport)

    def write_exploratory(self, value: ExploratoryRankingReport) -> None:
        self._write_artifact(value.session_id, "exploratory.ranking.json", value)

    def load_exploratory(self, session_id: str) -> ExploratoryRankingReport | None:
        return self._load_optional(
            session_id, "exploratory.ranking.json", ExploratoryRankingReport
        )

    def write_final_report(self, value: FinalParticipantReport) -> None:
        self._write_artifact(value.session_id, "final-report.json", value)

    def load_final_report(self, session_id: str) -> FinalParticipantReport | None:
        return self._load_optional(session_id, "final-report.json", FinalParticipantReport)

    def _write_artifact(self, session_id: str, filename: str, value: BaseModel) -> None:
        self.load_session(session_id)
        write_new_canonical_json(self._directory(session_id) / filename, value)

    def _load_optional(
        self,
        session_id: str,
        filename: str,
        model_type: type[T],
    ) -> T | None:
        self.load_session(session_id)
        path = self._directory(session_id) / filename
        if not path.exists():
            return None
        try:
            value = load_json_bytes(path, require_canonical=True)
            result = model_type.model_validate(value)
        except (OSError, ValueError) as exc:
            raise SessionStorageError(f"invalid {filename}") from exc
        if getattr(result, "session_id", session_id) != session_id:
            raise SessionStorageError(f"{filename} belongs to a different session")
        return result
