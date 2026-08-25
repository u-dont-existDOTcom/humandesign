"""Convert rich ``HumanCase`` questionnaire records to holistic positive evidence.

The conversion preserves the project's questionnaire semantics:

- every answered question is an observed categorical positive, not a set of
  implicit negatives for all other answers;
- the question itself defines the observation opportunity because an answered
  question proves that construct/item was observed;
- ``BehavioralResponse.cluster_id`` defines dependency families so correlated
  questions cannot multiply evidence without limit;
- typed response confidence × measurement reliability is retained as the base
  evidence weight before dependency normalization;
- ``Other`` or nuanced free-text-compatible answer codes remain ordinary
  evidence unless the caller explicitly declares that exact answer unscored;
- unknown/context-dependent answers may be omitted explicitly rather than forced
  to either side.

This adapter is deliberately DEVELOPMENT-only because the source ``HumanCase``
contains the person's actual chart features. A validation workflow must keep the
true chart/answer key outside the blind scorer and use a frozen candidate set.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from .dataset import HumanCase
from .holistic import CandidateChart, PositiveEvidenceRecord
from .holistic_labels import cluster_normalized_evidence_weights


def encode_question_answer_label(question_id: str, answer: str) -> str:
    """Return a collision-safe, deterministic categorical observation label."""

    if not question_id.strip() or not answer.strip():
        raise ValueError("question_id and answer must be nonblank")
    return json.dumps(
        [question_id.strip(), answer.strip()],
        ensure_ascii=False,
        separators=(",", ":"),
    )


def decode_question_answer_label(label: str) -> tuple[str, str]:
    """Invert ``encode_question_answer_label`` with strict shape validation."""

    raw = json.loads(label)
    if (
        not isinstance(raw, list)
        or len(raw) != 2
        or not all(isinstance(item, str) and item.strip() for item in raw)
    ):
        raise ValueError("holistic questionnaire label must encode [question_id, answer]")
    return raw[0], raw[1]


def _excluded_answer_set(
    excluded_answers: Mapping[str, Sequence[str]] | None,
) -> dict[str, frozenset[str]]:
    return {
        str(question_id): frozenset(str(answer) for answer in answers)
        for question_id, answers in (excluded_answers or {}).items()
    }


def _metadata_token(value: Any) -> str:
    if value is None:
        return "__missing__"
    if isinstance(value, str):
        return value.strip() or "__blank__"
    return json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)


def _question_clusters(case: HumanCase) -> dict[str, str]:
    if not case.response_records:
        return {question_id: question_id for question_id in case.responses}
    return {
        response.question_id: response.cluster_id
        for response in case.response_records
    }


def _match_strata(
    case: HumanCase,
    *,
    include_birth_year: bool,
    metadata_match_fields: Sequence[str],
) -> dict[str, str]:
    strata: dict[str, str] = {}
    if include_birth_year:
        strata["birth_year"] = (
            str(case.birth_year) if case.birth_year is not None else "__missing__"
        )
    for field in metadata_match_fields:
        name = str(field).strip()
        if not name:
            raise ValueError("metadata_match_fields cannot contain blank names")
        if name in strata:
            raise ValueError(f"duplicate holistic match stratum: {name}")
        strata[name] = _metadata_token(case.metadata.get(name))
    return strata


def _case_observations(
    case: HumanCase,
    *,
    excluded_answers: Mapping[str, Sequence[str]] | None,
) -> tuple[
    tuple[str, ...],
    dict[str, str],
    dict[str, str],
    dict[str, float],
]:
    excluded = _excluded_answer_set(excluded_answers)
    clusters_by_question = _question_clusters(case)
    base_weights_by_question = case.evidence_weights

    labels: list[str] = []
    opportunities: dict[str, str] = {}
    label_clusters: dict[str, str] = {}
    base_weights: dict[str, float] = {}
    for question_id, answer in sorted(case.responses.items()):
        if answer in excluded.get(question_id, frozenset()):
            continue
        label = encode_question_answer_label(question_id, answer)
        labels.append(label)
        opportunities[label] = question_id
        label_clusters[label] = clusters_by_question.get(question_id, question_id)
        base_weights[label] = float(base_weights_by_question.get(question_id, 1.0))

    observed = tuple(labels)
    if not observed:
        return (), {}, {}, {}
    weights = cluster_normalized_evidence_weights(
        observed,
        label_clusters=label_clusters,
        reliability_weights=base_weights,
    )
    return observed, opportunities, label_clusters, weights


class HumanCaseHolisticConversion(BaseModel):
    """Auditable DEVELOPMENT conversion result for a multi-person rich cohort."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-case-holistic-conversion-v1"] = (
        "human-case-holistic-conversion-v1"
    )
    records: tuple[PositiveEvidenceRecord, ...]
    true_charts: tuple[CandidateChart, ...]
    label_opportunities: dict[str, str]
    label_dependency_clusters: dict[str, str]
    skipped_no_scorable_evidence: tuple[str, ...] = ()


def human_case_to_positive_evidence(
    case: HumanCase,
    *,
    excluded_answers: Mapping[str, Sequence[str]] | None = None,
    include_birth_year: bool = True,
    metadata_match_fields: Sequence[str] = (),
) -> tuple[
    PositiveEvidenceRecord,
    CandidateChart,
    dict[str, str],
    dict[str, str],
]:
    """Convert one DEVELOPMENT ``HumanCase`` and its true chart.

    Raises when every answer was explicitly excluded. Use the multi-case helper
    when empty-evidence people should be retained in an audit as skipped.
    """

    if case.cohort != "development":
        raise ValueError("HumanCase holistic conversion is DEVELOPMENT-only")
    labels, opportunities, clusters, weights = _case_observations(
        case,
        excluded_answers=excluded_answers,
    )
    if not labels:
        raise ValueError(f"participant {case.participant_id} has no scorable evidence")
    strata = _match_strata(
        case,
        include_birth_year=include_birth_year,
        metadata_match_fields=metadata_match_fields,
    )
    record = PositiveEvidenceRecord(
        participant_id=case.participant_id,
        cohort="development",
        observed_labels=labels,
        chart_features=case.chart_features,
        match_strata=strata,
        evidence_weights=weights,
    )
    chart = CandidateChart(
        chart_id=f"true:{case.participant_id}",
        owner_participant_id=case.participant_id,
        chart_features=case.chart_features,
        match_strata=strata,
    )
    return record, chart, opportunities, clusters


def human_cases_to_positive_evidence(
    cases: Sequence[HumanCase],
    *,
    excluded_answers: Mapping[str, Sequence[str]] | None = None,
    include_birth_year: bool = True,
    metadata_match_fields: Sequence[str] = (),
) -> HumanCaseHolisticConversion:
    """Convert a rich DEVELOPMENT cohort and preserve skipped-person provenance."""

    identifiers = [case.participant_id for case in cases]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("HumanCase participant_id values must be unique")
    records: list[PositiveEvidenceRecord] = []
    charts: list[CandidateChart] = []
    opportunities: dict[str, str] = {}
    dependency_clusters: dict[str, str] = {}
    skipped: list[str] = []

    for case in sorted(cases, key=lambda item: item.participant_id):
        if case.cohort != "development":
            raise ValueError("HumanCase holistic conversion is DEVELOPMENT-only")
        labels, case_opportunities, case_clusters, weights = _case_observations(
            case,
            excluded_answers=excluded_answers,
        )
        if not labels:
            skipped.append(case.participant_id)
            continue
        for label, opportunity in case_opportunities.items():
            prior = opportunities.get(label)
            if prior is not None and prior != opportunity:
                raise ValueError(f"inconsistent observation opportunity for {label}")
            opportunities[label] = opportunity
        for label, cluster in case_clusters.items():
            prior = dependency_clusters.get(label)
            if prior is not None and prior != cluster:
                raise ValueError(f"inconsistent dependency cluster for {label}")
            dependency_clusters[label] = cluster
        strata = _match_strata(
            case,
            include_birth_year=include_birth_year,
            metadata_match_fields=metadata_match_fields,
        )
        records.append(
            PositiveEvidenceRecord(
                participant_id=case.participant_id,
                cohort="development",
                observed_labels=labels,
                chart_features=case.chart_features,
                match_strata=strata,
                evidence_weights=weights,
            )
        )
        charts.append(
            CandidateChart(
                chart_id=f"true:{case.participant_id}",
                owner_participant_id=case.participant_id,
                chart_features=case.chart_features,
                match_strata=strata,
            )
        )

    return HumanCaseHolisticConversion(
        records=tuple(records),
        true_charts=tuple(charts),
        label_opportunities=dict(sorted(opportunities.items())),
        label_dependency_clusters=dict(sorted(dependency_clusters.items())),
        skipped_no_scorable_evidence=tuple(sorted(skipped)),
    )
