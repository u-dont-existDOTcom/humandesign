"""Emit the complete synthetic evidence-transition matrix required by Pro checkpoint 2."""

from __future__ import annotations

import argparse
import tempfile
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.natal_time.evidence import assess_evidence
from hdmatch.natal_time.models import (
    CandidateDateSetEvidence,
    DateEvidence,
    DocumentaryVerification,
    EvidenceLineage,
    EvidenceSource,
    Weekday,
    WeekdayAnswerStatus,
    WeekdayEvidence,
)
from hdmatch.natal_time.store import NatalTimePrivateStore
from hdmatch.util import canonical_json_bytes, sha256_json

CREATED_AT = datetime(2026, 8, 30, 4, 0, tzinfo=UTC)
ORIGINAL_DATE = date(2000, 1, 3)  # Monday; conspicuously synthetic.
ALTERNATE_DATE = date(2000, 1, 4)  # Tuesday; conspicuously synthetic.


def _id(prefix: str, number: int) -> str:
    return f"{prefix}-{number:024X}"


def _date_evidence(
    number: int,
    asserted_date: date,
    source: EvidenceSource,
    verification: DocumentaryVerification,
    *,
    supersedes: str | None = None,
) -> DateEvidence:
    return DateEvidence(
        evidence_id=_id("NTE", number),
        asserted_date=asserted_date,
        source=source,
        documentary_verification=verification,
        entered_at_utc=CREATED_AT + timedelta(seconds=number),
        entered_how="conspicuously_synthetic_evidence_matrix",
        supersedes_evidence_id=supersedes,
    )


def _lineage(
    number: int,
    dates: tuple[DateEvidence, ...],
    *,
    weekday_status: WeekdayAnswerStatus,
    weekday: Weekday | None,
    version: int = 1,
    supersedes: str | None = None,
    candidate_dates: tuple[date, ...] | None = None,
) -> EvidenceLineage:
    candidate = None
    if candidate_dates is not None:
        candidate = CandidateDateSetEvidence(
            evidence_id=_id("NTE", number * 100 + 3),
            candidate_dates=candidate_dates,
            declared_date_evidence_ids=tuple(item.evidence_id for item in dates),
            confirmed_at_utc=CREATED_AT + timedelta(minutes=number),
            confirmed_how="conspicuously_synthetic_evidence_matrix",
        )
    return EvidenceLineage(
        lineage_id=_id("NTL", number),
        version=version,
        date_evidence=dates,
        weekday_evidence=WeekdayEvidence(
            evidence_id=_id("NTE", number * 100 + 2),
            answer_status=weekday_status,
            asserted_weekday=weekday,
            entered_at_utc=CREATED_AT,
            entered_how="conspicuously_synthetic_evidence_matrix",
            locked_at_utc=CREATED_AT,
            server_lock_sequence=number,
        ),
        candidate_date_set=candidate,
        supersedes_lineage_sha256=supersedes,
    )


def _accepted_row(case_id: str, lineage: EvidenceLineage, expected: str) -> dict[str, Any]:
    assessment = assess_evidence(lineage)
    return {
        "case_id": case_id,
        "expected_transition": expected,
        "attempt_accepted": True,
        "assessment_state": assessment.state.value,
        "enumeration_allowed": assessment.enumeration_allowed,
        "operative_dates": [value.isoformat() for value in assessment.operative_dates],
        "evidence_lineage_sha256": lineage.content_sha256,
        "supersedes_lineage_sha256": lineage.supersedes_lineage_sha256,
        "rejection_type": None,
        "attempted_payload_sha256": None,
    }


def _rejected_row(
    case_id: str,
    baseline: EvidenceLineage,
    expected: str,
    attempted_payload: object,
    error: Exception,
) -> dict[str, Any]:
    assessment = assess_evidence(baseline)
    return {
        "case_id": case_id,
        "expected_transition": expected,
        "attempt_accepted": False,
        "assessment_state": assessment.state.value,
        "enumeration_allowed": assessment.enumeration_allowed,
        "operative_dates": [value.isoformat() for value in assessment.operative_dates],
        "evidence_lineage_sha256": baseline.content_sha256,
        "supersedes_lineage_sha256": baseline.supersedes_lineage_sha256,
        "rejection_type": type(error).__name__,
        "attempted_payload_sha256": sha256_json(attempted_payload),
    }


def build_matrix(repository_commit: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    number = 0

    def single(
        source: EvidenceSource,
        verification: DocumentaryVerification,
        status: WeekdayAnswerStatus,
        weekday: Weekday | None,
    ) -> EvidenceLineage:
        nonlocal number
        number += 1
        return _lineage(
            number,
            (_date_evidence(number * 100 + 1, ORIGINAL_DATE, source, verification),),
            weekday_status=status,
            weekday=weekday,
        )

    ordinary_cases = (
        (
            "documentary_weekday_unavailable",
            single(
                EvidenceSource.DOCUMENTARY,
                DocumentaryVerification.INDEPENDENTLY_VERIFIED,
                WeekdayAnswerStatus.NOT_REMEMBERED,
                None,
            ),
        ),
        (
            "documentary_weekday_concordant",
            single(
                EvidenceSource.DOCUMENTARY,
                DocumentaryVerification.INDEPENDENTLY_VERIFIED,
                WeekdayAnswerStatus.REMEMBERED,
                Weekday.MONDAY,
            ),
        ),
        (
            "documentary_weekday_conflict",
            single(
                EvidenceSource.DOCUMENTARY,
                DocumentaryVerification.INDEPENDENTLY_VERIFIED,
                WeekdayAnswerStatus.REMEMBERED,
                Weekday.TUESDAY,
            ),
        ),
        (
            "memory_weekday_unavailable",
            single(
                EvidenceSource.MEMORY,
                DocumentaryVerification.NOT_APPLICABLE,
                WeekdayAnswerStatus.UNKNOWN,
                None,
            ),
        ),
        (
            "memory_weekday_concordant",
            single(
                EvidenceSource.MEMORY,
                DocumentaryVerification.NOT_APPLICABLE,
                WeekdayAnswerStatus.REMEMBERED,
                Weekday.MONDAY,
            ),
        ),
        (
            "memory_weekday_conflict",
            single(
                EvidenceSource.MEMORY,
                DocumentaryVerification.NOT_APPLICABLE,
                WeekdayAnswerStatus.REMEMBERED,
                Weekday.TUESDAY,
            ),
        ),
    )
    rows.extend(
        _accepted_row(case_id, lineage, "assess_without_date_repair")
        for case_id, lineage in ordinary_cases
    )

    number += 1
    conflict_dates = (
        _date_evidence(
            number * 100 + 1,
            ORIGINAL_DATE,
            EvidenceSource.DOCUMENTARY,
            DocumentaryVerification.INDEPENDENTLY_VERIFIED,
        ),
        _date_evidence(
            number * 100 + 4,
            ALTERNATE_DATE,
            EvidenceSource.DOCUMENTARY,
            DocumentaryVerification.PARTICIPANT_REPORTED,
        ),
    )
    documentary_conflict = _lineage(
        number,
        conflict_dates,
        weekday_status=WeekdayAnswerStatus.REMEMBERED,
        weekday=Weekday.MONDAY,
    )
    rows.append(
        _accepted_row(
            "conflicting_documentary_sources",
            documentary_conflict,
            "fail_closed_pending_explicit_full_candidate_set",
        )
    )

    number += 1
    explicit_initial = _lineage(
        number,
        (
            _date_evidence(
                number * 100 + 1,
                ORIGINAL_DATE,
                EvidenceSource.MEMORY,
                DocumentaryVerification.NOT_APPLICABLE,
            ),
        ),
        weekday_status=WeekdayAnswerStatus.REMEMBERED,
        weekday=Weekday.TUESDAY,
    )
    explicit_confirmed = _lineage(
        number,
        explicit_initial.date_evidence,
        weekday_status=WeekdayAnswerStatus.REMEMBERED,
        weekday=Weekday.TUESDAY,
        version=2,
        supersedes=explicit_initial.content_sha256,
        candidate_dates=(ORIGINAL_DATE, ALTERNATE_DATE),
    )
    rows.append(
        _accepted_row(
            "explicit_unordered_candidate_set",
            explicit_confirmed,
            "enumerate_every_confirmed_date_without_order_or_prior",
        )
    )

    number += 1
    correction_initial = _lineage(
        number,
        (
            _date_evidence(
                number * 100 + 1,
                ORIGINAL_DATE,
                EvidenceSource.MEMORY,
                DocumentaryVerification.NOT_APPLICABLE,
            ),
        ),
        weekday_status=WeekdayAnswerStatus.REMEMBERED,
        weekday=Weekday.MONDAY,
    )
    correction = _date_evidence(
        number * 100 + 4,
        ALTERNATE_DATE,
        EvidenceSource.DOCUMENTARY,
        DocumentaryVerification.PARTICIPANT_REPORTED,
        supersedes=correction_initial.date_evidence[0].evidence_id,
    )
    corrected = EvidenceLineage(
        lineage_id=correction_initial.lineage_id,
        version=2,
        date_evidence=(*correction_initial.date_evidence, correction),
        weekday_evidence=correction_initial.weekday_evidence,
        supersedes_lineage_sha256=correction_initial.content_sha256,
    )
    correction_row = _accepted_row(
        "correction_supersession",
        corrected,
        "append_new_evidence_and_bind_predecessor_digest",
    )
    correction_row["original_lineage_sha256"] = correction_initial.content_sha256
    rows.append(correction_row)

    attempted_omission = {
        **explicit_initial.model_dump(mode="json"),
        "version": 2,
        "supersedes_lineage_sha256": explicit_initial.content_sha256,
        "candidate_date_set": CandidateDateSetEvidence(
            evidence_id=_id("NTE", 999_001),
            candidate_dates=(ALTERNATE_DATE,),
            declared_date_evidence_ids=(explicit_initial.date_evidence[0].evidence_id,),
            confirmed_at_utc=CREATED_AT,
            confirmed_how="conspicuously_synthetic_omission_attempt",
        ).model_dump(mode="json"),
    }
    omitted = EvidenceLineage.model_validate(attempted_omission)
    try:
        assess_evidence(omitted)
    except ValueError as exc:
        rows.append(
            _rejected_row(
                "attempted_original_date_omission",
                explicit_initial,
                "reject_before_enumeration",
                attempted_omission,
                exc,
            )
        )
    else:  # pragma: no cover - fail-closed assertion
        raise RuntimeError("original-date omission was unexpectedly accepted")

    relationship_attempt = {
        **explicit_initial.model_dump(mode="json"),
        "relationship_evidence": {"synthetic_relationship_id": "FORBIDDEN"},
    }
    try:
        EvidenceLineage.model_validate(relationship_attempt)
    except ValidationError as exc:
        rows.append(
            _rejected_row(
                "attempted_relationship_evidence_injection",
                explicit_initial,
                "schema_rejects_relationship_fields",
                relationship_attempt,
                exc,
            )
        )
    else:  # pragma: no cover - fail-closed assertion
        raise RuntimeError("relationship evidence injection was unexpectedly accepted")

    with tempfile.TemporaryDirectory(prefix="astrohd-evidence-matrix-") as directory:
        store = NatalTimePrivateStore(Path(directory))
        store.append_lineage(explicit_initial)
        try:
            store.append_lineage(explicit_initial)
        except FileExistsError as exc:
            rows.append(
                _rejected_row(
                    "attempted_in_place_mutation",
                    explicit_initial,
                    "append_only_store_refuses_existing_version",
                    explicit_initial.model_dump(mode="json"),
                    exc,
                )
            )
        else:  # pragma: no cover - fail-closed assertion
            raise RuntimeError("in-place lineage overwrite was unexpectedly accepted")

    payload: dict[str, Any] = {
        "schema_version": "natal-time-evidence-transition-matrix-v1",
        "repository_commit": repository_commit,
        "created_at_utc": CREATED_AT.isoformat().replace("+00:00", "Z"),
        "synthetic_only": True,
        "case_count": len(rows),
        "cases": rows,
        "forbidden_semantics": {
            "ranking": False,
            "weights": False,
            "probability": False,
            "relationship_evidence": False,
        },
    }
    payload["matrix_sha256"] = sha256_json(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-commit", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = canonical_json_bytes(build_matrix(args.repository_commit)) + b"\n"
    if args.output is None:
        print(encoded.decode(), end="")
    else:
        write_new_bytes(args.output, encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
