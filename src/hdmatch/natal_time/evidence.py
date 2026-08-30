"""Fail-closed date/source/weekday evidence transition semantics."""

from __future__ import annotations

from datetime import date

from hdmatch.natal_time.models import (
    DateWeekdayFact,
    EvidenceAssessment,
    EvidenceLineage,
    EvidenceSource,
    EvidenceState,
    Weekday,
    WeekdayAnswerStatus,
    WeekdayRelation,
)


def assess_evidence(lineage: EvidenceLineage) -> EvidenceAssessment:
    """Assess immutable evidence without correcting or ranking any date."""

    declared_dates = {item.asserted_date for item in lineage.date_evidence}
    documentary_dates = {
        item.asserted_date
        for item in lineage.date_evidence
        if item.source is EvidenceSource.DOCUMENTARY
    }
    memory_dates = {
        item.asserted_date for item in lineage.date_evidence if item.source is EvidenceSource.MEMORY
    }

    candidate_set = lineage.candidate_date_set
    if candidate_set is not None:
        if set(candidate_set.declared_date_evidence_ids) != {
            item.evidence_id for item in lineage.date_evidence
        }:
            raise ValueError("candidate set must explicitly bind every declared date evidence item")
        if not declared_dates.issubset(candidate_set.candidate_dates):
            raise ValueError("candidate set cannot silently remove an originally declared date")
        dates = candidate_set.candidate_dates
        return _assessment(
            lineage,
            state=EvidenceState.CANDIDATE_DATE_SET_CONFIRMED,
            dates=dates,
            enumeration_allowed=True,
            requires_candidate_date_set=False,
        )

    if len(documentary_dates) > 1:
        return _assessment(
            lineage,
            state=EvidenceState.UNRESOLVED_DOCUMENTARY_CONFLICT,
            dates=tuple(sorted(documentary_dates)),
            enumeration_allowed=False,
            requires_candidate_date_set=True,
        )

    if documentary_dates:
        dates = tuple(documentary_dates)
        weekday = lineage.weekday_evidence
        if weekday.answer_status is not WeekdayAnswerStatus.REMEMBERED:
            state = EvidenceState.DOCUMENTARY_WEEKDAY_UNAVAILABLE
        elif Weekday.from_date(dates[0]) is weekday.asserted_weekday:
            state = EvidenceState.DOCUMENTARY_CONCORDANT
        else:
            state = EvidenceState.DOCUMENTARY_WEEKDAY_CONFLICT
        return _assessment(
            lineage,
            state=state,
            dates=dates,
            enumeration_allowed=True,
            requires_candidate_date_set=False,
        )

    if len(memory_dates) != 1:
        return _assessment(
            lineage,
            state=EvidenceState.BIRTH_DATE_UNCERTAIN,
            dates=tuple(sorted(memory_dates)),
            enumeration_allowed=False,
            requires_candidate_date_set=True,
        )

    dates = tuple(memory_dates)
    weekday = lineage.weekday_evidence
    if weekday.answer_status is not WeekdayAnswerStatus.REMEMBERED:
        state = EvidenceState.MEMORY_DATE_UNVERIFIED
        allowed = True
        required = False
    elif Weekday.from_date(dates[0]) is weekday.asserted_weekday:
        state = EvidenceState.MEMORY_CONCORDANT
        allowed = True
        required = False
    else:
        state = EvidenceState.BIRTH_DATE_UNCERTAIN
        allowed = False
        required = True
    return _assessment(
        lineage,
        state=state,
        dates=dates,
        enumeration_allowed=allowed,
        requires_candidate_date_set=required,
    )


def _assessment(
    lineage: EvidenceLineage,
    *,
    state: EvidenceState,
    dates: tuple[date, ...],
    enumeration_allowed: bool,
    requires_candidate_date_set: bool,
) -> EvidenceAssessment:
    remembered = lineage.weekday_evidence.asserted_weekday
    facts = tuple(
        DateWeekdayFact(
            candidate_date=candidate_date,
            implied_weekday=Weekday.from_date(candidate_date),
            remembered_weekday_matches=(
                None if remembered is None else Weekday.from_date(candidate_date) is remembered
            ),
        )
        for candidate_date in sorted(dates)
    )
    matches = {item.remembered_weekday_matches for item in facts}
    if matches == {None} or not facts:
        relation = WeekdayRelation.UNAVAILABLE
    elif matches == {True}:
        relation = WeekdayRelation.CONCORDANT
    elif matches == {False}:
        relation = WeekdayRelation.CONFLICT
    else:
        relation = WeekdayRelation.MIXED
    return EvidenceAssessment(
        lineage_sha256=lineage.content_sha256,
        state=state,
        weekday_relation=relation,
        operative_dates=tuple(item.candidate_date for item in facts),
        date_weekday_facts=facts,
        enumeration_allowed=enumeration_allowed,
        requires_candidate_date_set=requires_candidate_date_set,
    )
