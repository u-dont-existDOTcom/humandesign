"""Server-enforced weekday locking and append-only evidence transitions."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, date, datetime
from secrets import token_hex

from hdmatch.natal_time.evidence import assess_evidence
from hdmatch.natal_time.models import (
    CandidateDateSetEvidence,
    DateEvidence,
    DocumentaryVerification,
    EvidenceAssessment,
    EvidenceLineage,
    EvidenceSource,
    NatalTimeModel,
    Weekday,
    WeekdayAnswerStatus,
    WeekdayEvidence,
)
from hdmatch.natal_time.store import NatalTimePrivateStore


class WeekdayLockReceipt(NatalTimeModel):
    schema_version: str = "natal-weekday-lock-receipt-v1"
    lineage_id: str
    lineage_version: int
    lineage_sha256: str
    weekday_locked: bool = True
    server_lock_sequence: int
    implied_weekday_revealed: bool = False


class NatalTimeIntakeService:
    def __init__(
        self,
        store: NatalTimePrivateStore,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.store = store
        self._clock = clock or (lambda: datetime.now(UTC))
        self._lock_sequence = 0

    def capture_initial_evidence(
        self,
        *,
        asserted_date: date,
        date_source: EvidenceSource,
        documentary_verification: DocumentaryVerification,
        weekday_answer_status: WeekdayAnswerStatus,
        asserted_weekday: Weekday | None,
        entered_how: str,
    ) -> WeekdayLockReceipt:
        """Lock date and independent weekday evidence without revealing calendar facts."""

        now = self._now()
        self._lock_sequence += 1
        lineage = EvidenceLineage(
            lineage_id=_id("NTL"),
            version=1,
            date_evidence=(
                DateEvidence(
                    evidence_id=_id("NTE"),
                    asserted_date=asserted_date,
                    source=date_source,
                    documentary_verification=documentary_verification,
                    entered_at_utc=now,
                    entered_how=entered_how,
                ),
            ),
            weekday_evidence=WeekdayEvidence(
                evidence_id=_id("NTE"),
                answer_status=weekday_answer_status,
                asserted_weekday=asserted_weekday,
                entered_at_utc=now,
                entered_how=entered_how,
                locked_at_utc=now,
                server_lock_sequence=self._lock_sequence,
            ),
        )
        self.store.append_lineage(lineage)
        return WeekdayLockReceipt(
            lineage_id=lineage.lineage_id,
            lineage_version=lineage.version,
            lineage_sha256=lineage.content_sha256,
            server_lock_sequence=self._lock_sequence,
        )

    def assess_locked_evidence(self, lineage_id: str) -> EvidenceAssessment:
        return assess_evidence(self.store.load_latest_lineage(lineage_id))

    def confirm_candidate_dates(
        self,
        lineage_id: str,
        *,
        candidate_dates: tuple[date, ...],
        confirmed_how: str,
    ) -> EvidenceLineage:
        previous = self.store.load_latest_lineage(lineage_id)
        assessment = assess_evidence(previous)
        if not assessment.requires_candidate_date_set:
            raise ValueError("this evidence state does not require a candidate-date set")
        now = self._now()
        updated = EvidenceLineage(
            lineage_id=previous.lineage_id,
            version=previous.version + 1,
            date_evidence=previous.date_evidence,
            weekday_evidence=previous.weekday_evidence,
            candidate_date_set=CandidateDateSetEvidence(
                evidence_id=_id("NTE"),
                candidate_dates=candidate_dates,
                declared_date_evidence_ids=tuple(
                    item.evidence_id for item in previous.date_evidence
                ),
                confirmed_at_utc=now,
                confirmed_how=confirmed_how,
            ),
            supersedes_lineage_sha256=previous.content_sha256,
        )
        # Run the state machine before persistence so an incomplete set cannot
        # create a new scientific lineage.
        assessment = assess_evidence(updated)
        if not assessment.enumeration_allowed:
            raise ValueError("confirmed candidate-date set remains non-enumerable")
        self.store.append_lineage(updated)
        return updated

    def supersede_declared_date(
        self,
        lineage_id: str,
        *,
        superseded_evidence_id: str,
        asserted_date: date,
        source: EvidenceSource,
        documentary_verification: DocumentaryVerification,
        entered_how: str,
    ) -> EvidenceLineage:
        previous = self.store.load_latest_lineage(lineage_id)
        existing_ids = {item.evidence_id for item in previous.date_evidence}
        if superseded_evidence_id not in existing_ids:
            raise ValueError("superseded date evidence does not exist")
        replacement = DateEvidence(
            evidence_id=_id("NTE"),
            asserted_date=asserted_date,
            source=source,
            documentary_verification=documentary_verification,
            entered_at_utc=self._now(),
            entered_how=entered_how,
            supersedes_evidence_id=superseded_evidence_id,
        )
        updated = EvidenceLineage(
            lineage_id=previous.lineage_id,
            version=previous.version + 1,
            date_evidence=(*previous.date_evidence, replacement),
            weekday_evidence=previous.weekday_evidence,
            supersedes_lineage_sha256=previous.content_sha256,
        )
        self.store.append_lineage(updated)
        return updated

    def _now(self) -> datetime:
        value = self._clock()
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("service clock must return a timezone-aware datetime")
        return value.astimezone(UTC)


def _id(prefix: str) -> str:
    return f"{prefix}-{token_hex(12).upper()}"
