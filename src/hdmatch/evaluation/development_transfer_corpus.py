"""Development-only bridge from the pattern-first v8/v8.1 transfer records to coding units.

The completed owner interview predates the source-complete in-app freeze pipeline.  Its v8
transfer record contains participant-supplied exact text fragments plus interviewer summaries,
and the v8.1 repair supplement recovers some additional exact turns.  That is useful development
material, but it must not be silently promoted to the semantics of a source-complete BPF
behavioral freeze.

This module therefore creates a separate, content-addressed development corpus.  It preserves
original episodes, post-review evidence, repeated-series reports, review scope, source
limitations, and participant theory-exposure status.  Raw autobiographical records are intended
to remain under experiments/private/ (already gitignored); this module contains no participant
content.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_json,
    write_new_bytes,
)

from .neutral_measurement import TheoryExposureState

_SHA256_PATTERN = r"^[0-9a-f]{64}$"

CollectionPhase = Literal["v8_original", "v8.1_repair"]
EpisodeReviewScope = Literal[
    "pattern_reviewed_transfer_summary",
    "post_review_participant_approved",
]
EpisodeSourceCompleteness = Literal[
    "partial_exact_segments_plus_transfer_summary",
    "exact_repair_response_plus_transfer_summary",
]
SeriesSourceCompleteness = Literal[
    "transfer_summary_only",
    "partial_exact_recovered_turns",
]


class DevelopmentTransferModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class DevelopmentSourceSegment(DevelopmentTransferModel):
    segment_id: str = Field(min_length=1)
    exact_text: str = Field(min_length=1)
    provenance_refs: tuple[str, ...] = Field(min_length=1)
    exact_participant_text: Literal[True] = True


class DevelopmentTransferEpisode(DevelopmentTransferModel):
    episode_id: str = Field(min_length=1)
    origin_id: str = Field(min_length=1)
    collection_phase: CollectionPhase
    domain_id: str | None = None
    approximate_age_life_phase: str = Field(min_length=1)
    age_estimation_basis: str | None = None
    source_review_scope: EpisodeReviewScope
    source_completeness: EpisodeSourceCompleteness
    bounded_situation: str = Field(min_length=1)
    contemporaneous_knowledge: str | None = None
    relevant_options_constraints: str | None = None
    actions_in_temporal_order: tuple[str, ...] = Field(min_length=1)
    outcome_when_known: str | None = None
    participant_stated_explanation: str | None = None
    memory_uncertainty: str | None = None
    original_source_turn_ids: tuple[str, ...] = ()
    exact_source_segments: tuple[DevelopmentSourceSegment, ...] = Field(min_length=1)
    transfer_summary: str = Field(min_length=1)
    transfer_summary_is_not_primary_source: Literal[True] = True

    @field_validator("actions_in_temporal_order")
    @classmethod
    def actions_are_nonempty(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if any(not row.strip() for row in value):
            raise ValueError("development episode contains an empty action")
        return value


class DevelopmentTransferSeriesReport(DevelopmentTransferModel):
    series_id: str = Field(min_length=1)
    origin_id: str = Field(min_length=1)
    collection_phase: CollectionPhase
    domain_id: str | None = None
    bounded_period_context: str = Field(min_length=1)
    approximate_age_life_phase: str = Field(min_length=1)
    recurrence_language: str = Field(min_length=1)
    rough_opportunity_count: str | None = None
    behavior_reportedly_recurred: str = Field(min_length=1)
    explicit_exceptions_or_limits: str | None = None
    memory_source_uncertainty: str | None = None
    original_source_turn_ids: tuple[str, ...] = ()
    exact_source_segments: tuple[DevelopmentSourceSegment, ...] = ()
    source_completeness: SeriesSourceCompleteness
    primary_episode_code_from_series_forbidden: Literal[True] = True


class DevelopmentAuxiliaryEvidence(DevelopmentTransferModel):
    evidence_id: str = Field(min_length=1)
    evidence_type: str = Field(min_length=1)
    target_pattern_id: str = Field(min_length=1)
    collection_phase: Literal["v8.1_repair"] = "v8.1_repair"
    payload: dict[str, Any]
    primary_episode_code_from_auxiliary_evidence_forbidden: Literal[True] = True


class DevelopmentTransferCorpusPayload(DevelopmentTransferModel):
    schema_version: Literal["life-patterns-development-transfer-corpus-v1"] = (
        "life-patterns-development-transfer-corpus-v1"
    )
    source_record_schema_version: str = Field(min_length=1)
    source_record_sha256: str = Field(pattern=_SHA256_PATTERN)
    supplement_schema_version: str = Field(min_length=1)
    supplement_sha256: str = Field(pattern=_SHA256_PATTERN)
    participant_theory_exposure: TheoryExposureState
    source_record_status: str = Field(min_length=1)
    supplement_status: str = Field(min_length=1)
    episodes: tuple[DevelopmentTransferEpisode, ...] = Field(min_length=1)
    series_reports: tuple[DevelopmentTransferSeriesReport, ...]
    pattern_claims: tuple[dict[str, Any], ...]
    auxiliary_post_review_evidence: tuple[DevelopmentAuxiliaryEvidence, ...]
    source_transcript_completeness: Literal["partial_exact_segments_only"] = (
        "partial_exact_segments_only"
    )
    episode_review_scope: Literal[
        "pattern_claims_reviewed_not_every_episode_individually"
    ] = "pattern_claims_reviewed_not_every_episode_individually"
    canonical_behavioral_freeze_eligible: Literal[False] = False
    development_coding_eligible: Literal[True] = True
    validation_use_forbidden: Literal[True] = True
    target_model_information_available: Literal[False] = False
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("development transfer corpus timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def identifiers_are_unique(self) -> DevelopmentTransferCorpusPayload:
        episode_ids = [row.episode_id for row in self.episodes]
        if len(episode_ids) != len(set(episode_ids)):
            raise ValueError("development transfer corpus repeats an episode identity")
        series_ids = [row.series_id for row in self.series_reports]
        if len(series_ids) != len(set(series_ids)):
            raise ValueError("development transfer corpus repeats a series identity")
        return self


class DevelopmentTransferCorpusArtifact(DevelopmentTransferModel):
    schema_version: Literal["life-patterns-development-transfer-corpus-artifact-v1"] = (
        "life-patterns-development-transfer-corpus-artifact-v1"
    )
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: DevelopmentTransferCorpusPayload


class DevelopmentEpisodeCodingTask(DevelopmentTransferModel):
    schema_version: Literal["life-patterns-development-episode-coding-task-v1"] = (
        "life-patterns-development-episode-coding-task-v1"
    )
    task_id: str = Field(pattern=r"^LPDT-[0-9A-F]{20}$")
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_id: str = Field(min_length=1)
    domain_id: str | None = None
    approximate_age_life_phase: str = Field(min_length=1)
    episode_narrative: str = Field(min_length=1)
    exact_source_segments: tuple[DevelopmentSourceSegment, ...] = Field(min_length=1)
    source_completeness: EpisodeSourceCompleteness
    observable_ids: tuple[str, ...] = Field(min_length=1)
    participant_theory_exposure: TheoryExposureState
    transfer_summary_is_not_primary_source: Literal[True] = True
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True
    birth_chart_model_blind: Literal[True] = True

    @field_validator("observable_ids")
    @classmethod
    def observable_ids_are_unique(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("development coding task repeats an observable identity")
        return value


class DevelopmentTaskSetManifestPayload(DevelopmentTransferModel):
    schema_version: Literal["life-patterns-development-task-set-manifest-v1"] = (
        "life-patterns-development-task-set-manifest-v1"
    )
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    task_set_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_task_count: int = Field(ge=1)
    observable_count: int = Field(ge=1)
    expected_episode_observable_unit_count: int = Field(ge=1)
    series_report_count: int = Field(ge=0)
    series_reports_are_not_pseudo_episodes: Literal[True] = True
    canonical_freeze_required_before_validation: Literal[True] = True
    target_model_information_available: Literal[False] = False
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("development task manifest timestamp must be timezone-aware")
        return value.astimezone(UTC)


class DevelopmentTaskSetManifestArtifact(DevelopmentTransferModel):
    schema_version: Literal["life-patterns-development-task-set-manifest-artifact-v1"] = (
        "life-patterns-development-task-set-manifest-artifact-v1"
    )
    manifest_id: str = Field(pattern=r"^LPDM-[0-9A-F]{20}$")
    manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: DevelopmentTaskSetManifestPayload


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return cast(dict[str, Any], value)


def _require_list(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise ValueError(f"{label} must be a list of JSON objects")
    return cast(list[dict[str, Any]], value)


def _unique_ids(rows: list[dict[str, Any]], key: str, label: str) -> set[str]:
    values = [row.get(key) for row in rows]
    if not all(isinstance(value, str) and value for value in values):
        raise ValueError(f"{label} contains a missing or invalid {key}")
    typed = cast(list[str], values)
    if len(typed) != len(set(typed)):
        raise ValueError(f"{label} repeats {key}")
    return set(typed)


def _episode_summary(row: dict[str, Any]) -> str:
    parts = [f"Situation: {str(row['bounded_situation']).strip()}"]
    knowledge = row.get("contemporaneous_knowledge_when_relevant")
    if isinstance(knowledge, str) and knowledge.strip():
        parts.append(f"Contemporaneous knowledge: {knowledge.strip()}")
    options = row.get("relevant_opportunities_options_constraints")
    if isinstance(options, str) and options.strip():
        parts.append(f"Options/constraints: {options.strip()}")
    actions = row.get("actions_in_temporal_order")
    if isinstance(actions, list):
        cleaned = [str(action).strip() for action in actions if str(action).strip()]
        if cleaned:
            parts.append("Actions in order: " + " -> ".join(cleaned))
    outcome = row.get("outcome_when_known")
    if isinstance(outcome, str) and outcome.strip():
        parts.append(f"Outcome: {outcome.strip()}")
    explanation = row.get("participant_stated_explanation_if_supplied")
    if isinstance(explanation, str) and explanation.strip():
        parts.append(f"Participant-stated explanation: {explanation.strip()}")
    uncertainty = row.get("memory_uncertainty")
    if isinstance(uncertainty, str) and uncertainty.strip():
        parts.append(f"Memory uncertainty: {uncertainty.strip()}")
    return "\n".join(parts)


def _repair_episode_summary(row: dict[str, Any]) -> str:
    parts = [f"Situation: {str(row['bounded_situation']).strip()}"]
    actions = row.get("actions_in_temporal_order")
    if isinstance(actions, list):
        cleaned = [str(action).strip() for action in actions if str(action).strip()]
        if cleaned:
            parts.append("Actions in order: " + " -> ".join(cleaned))
    outcome = row.get("outcome_when_known")
    if isinstance(outcome, str) and outcome.strip():
        parts.append(f"Outcome: {outcome.strip()}")
    explanation = row.get("participant_stated_explanation")
    if isinstance(explanation, str) and explanation.strip():
        parts.append(f"Participant-stated explanation: {explanation.strip()}")
    return "\n".join(parts)


def _recovered_exact_turns(supplement: dict[str, Any]) -> dict[str, str]:
    output: dict[str, str] = {}
    for row in _require_list(supplement.get("recovered_transcript_turns", []), "recovered turns"):
        original_id = row.get("original_local_id")
        role = row.get("role")
        text = row.get("exact_text")
        if (
            isinstance(original_id, str)
            and original_id
            and isinstance(role, str)
            and role.startswith("participant_")
            and isinstance(text, str)
            and text.strip()
        ):
            output[original_id] = text.strip()
    return output


def _validate_transfer_links(original: dict[str, Any], supplement: dict[str, Any]) -> None:
    if original.get("schema_version") != "life-patterns-pattern-first-longitudinal-interview-v8":
        raise ValueError("unsupported original Life Patterns transfer schema")
    if supplement.get("schema_version") != "life-patterns-v8-repair-supplement-v8.1":
        raise ValueError("unsupported Life Patterns repair supplement schema")
    if supplement.get("original_schema_version") != original.get("schema_version"):
        raise ValueError("repair supplement does not bind original transfer schema")
    if original.get("record_status") != "complete_after_pattern_review":
        raise ValueError("original transfer record is not complete after pattern review")
    if supplement.get("review_status") != (
        "participant_approved_changed_account; technical_audit_findings_logged_without_overwriting_original"
    ):
        raise ValueError("repair supplement lacks the expected participant-approved review state")

    patterns = _require_list(original.get("pattern_claims"), "pattern_claims")
    episodes = _require_list(original.get("episodes"), "episodes")
    series = _require_list(original.get("series_reports"), "series_reports")
    pattern_ids = _unique_ids(patterns, "pattern_id", "pattern_claims")
    episode_ids = _unique_ids(episodes, "episode_id", "episodes")
    series_ids = _unique_ids(series, "series_id", "series_reports")

    provenance = _require_mapping(original.get("transcript_source_provenance"), "transcript provenance")
    source_turn_index = _require_mapping(provenance.get("source_turn_index"), "source_turn_index")
    known_turn_ids = set(source_turn_index)

    for pattern in patterns:
        for key, known in (
            ("supporting_episode_ids", episode_ids),
            ("counterexample_episode_ids", episode_ids),
            ("supporting_series_report_ids", series_ids),
        ):
            raw = pattern.get(key, [])
            if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
                raise ValueError(f"pattern {pattern['pattern_id']} has invalid {key}")
            unknown = set(cast(list[str], raw)) - known
            if unknown:
                raise ValueError(
                    f"pattern {pattern['pattern_id']} references unknown {key}: {sorted(unknown)}"
                )
        raw_turn_ids = pattern.get("source_turn_ids", [])
        if isinstance(raw_turn_ids, list):
            unknown_turns = {str(item) for item in raw_turn_ids} - known_turn_ids
            if unknown_turns:
                raise ValueError(
                    f"pattern {pattern['pattern_id']} references unknown source turns: {sorted(unknown_turns)}"
                )

    for episode in episodes:
        raw_turn_ids = episode.get("source_turn_ids", [])
        if not isinstance(raw_turn_ids, list) or not all(isinstance(item, str) for item in raw_turn_ids):
            raise ValueError(f"episode {episode['episode_id']} has invalid source_turn_ids")
        unknown_turns = set(cast(list[str], raw_turn_ids)) - known_turn_ids
        if unknown_turns:
            raise ValueError(
                f"episode {episode['episode_id']} references unknown source turns: {sorted(unknown_turns)}"
            )
        segments = episode.get("exact_participant_source_segments")
        if not isinstance(segments, list) or not segments or not all(
            isinstance(item, str) and item.strip() for item in segments
        ):
            raise ValueError(
                f"episode {episode['episode_id']} lacks exact participant source fragments"
            )

    responses = _require_list(supplement.get("repair_responses"), "repair_responses")
    response_ids = _unique_ids(responses, "response_id", "repair_responses")
    review_record = _require_mapping(supplement.get("review_record"), "review_record")
    approval_ref = review_record.get("participant_response_reference")
    if approval_ref not in response_ids:
        raise ValueError("repair review approval reference does not resolve")
    response_by_id = {str(row["response_id"]): row for row in responses}
    approval = response_by_id[str(approval_ref)].get("exact_text")
    if not isinstance(approval, str) or approval.strip().casefold() not in {"yes", "approve", "approved"}:
        raise ValueError("repair supplement does not contain an affirmative participant approval")

    additions = _require_list(supplement.get("post_review_added_evidence"), "post_review_added_evidence")
    _unique_ids(additions, "added_evidence_id", "post_review_added_evidence")
    for addition in additions:
        if addition.get("target_pattern_id") not in pattern_ids:
            raise ValueError("post-review evidence references an unknown pattern")
        source_ref = addition.get("source_reference")
        if not isinstance(source_ref, str) or source_ref not in response_ids:
            raise ValueError("post-review evidence source reference does not resolve")


def build_v8_v8_1_development_corpus(
    original: dict[str, Any],
    supplement: dict[str, Any],
    *,
    participant_theory_exposure: TheoryExposureState,
    created_at_utc: datetime,
) -> DevelopmentTransferCorpusArtifact:
    """Build a development-only corpus without rewriting either source record."""

    _validate_transfer_links(original, supplement)
    episodes_raw = _require_list(original["episodes"], "episodes")
    patterns_raw = _require_list(original["pattern_claims"], "pattern_claims")
    series_raw = _require_list(original["series_reports"], "series_reports")
    recovered_turns = _recovered_exact_turns(supplement)
    pattern_domain = {
        str(row["pattern_id"]): str(row["domain_id"])
        for row in patterns_raw
        if isinstance(row.get("pattern_id"), str) and isinstance(row.get("domain_id"), str)
    }

    episodes: list[DevelopmentTransferEpisode] = []
    for row in episodes_raw:
        episode_id = str(row["episode_id"])
        turn_ids = tuple(str(value) for value in cast(list[Any], row.get("source_turn_ids", [])))
        raw_segments = cast(list[str], row["exact_participant_source_segments"])
        segments = tuple(
            DevelopmentSourceSegment(
                segment_id=f"{episode_id}-SEG-{index:02d}",
                exact_text=text.strip(),
                provenance_refs=turn_ids or (episode_id,),
            )
            for index, text in enumerate(raw_segments, start=1)
        )
        raw_actions = row.get("actions_in_temporal_order", [])
        actions = tuple(str(value).strip() for value in cast(list[Any], raw_actions) if str(value).strip())
        episodes.append(
            DevelopmentTransferEpisode(
                episode_id=episode_id,
                origin_id=episode_id,
                collection_phase="v8_original",
                domain_id=(str(row["domain_id"]) if isinstance(row.get("domain_id"), str) else None),
                approximate_age_life_phase=str(row.get("approximate_age_age_range") or "unknown"),
                age_estimation_basis=(
                    str(row["age_estimation_basis"])
                    if isinstance(row.get("age_estimation_basis"), str)
                    else None
                ),
                source_review_scope="pattern_reviewed_transfer_summary",
                source_completeness="partial_exact_segments_plus_transfer_summary",
                bounded_situation=str(row["bounded_situation"]),
                contemporaneous_knowledge=(
                    str(row["contemporaneous_knowledge_when_relevant"])
                    if isinstance(row.get("contemporaneous_knowledge_when_relevant"), str)
                    else None
                ),
                relevant_options_constraints=(
                    str(row["relevant_opportunities_options_constraints"])
                    if isinstance(row.get("relevant_opportunities_options_constraints"), str)
                    else None
                ),
                actions_in_temporal_order=actions,
                outcome_when_known=(
                    str(row["outcome_when_known"])
                    if isinstance(row.get("outcome_when_known"), str)
                    else None
                ),
                participant_stated_explanation=(
                    str(row["participant_stated_explanation_if_supplied"])
                    if isinstance(row.get("participant_stated_explanation_if_supplied"), str)
                    else None
                ),
                memory_uncertainty=(
                    str(row["memory_uncertainty"])
                    if isinstance(row.get("memory_uncertainty"), str)
                    else None
                ),
                original_source_turn_ids=turn_ids,
                exact_source_segments=segments,
                transfer_summary=_episode_summary(row),
            )
        )

    repair_responses = {
        str(row["response_id"]): row
        for row in _require_list(supplement["repair_responses"], "repair_responses")
    }
    auxiliary: list[DevelopmentAuxiliaryEvidence] = []
    for addition in _require_list(supplement["post_review_added_evidence"], "post_review_added_evidence"):
        evidence_type = str(addition.get("evidence_type", ""))
        addition_id = str(addition["added_evidence_id"])
        target_pattern_id = str(addition["target_pattern_id"])
        if evidence_type == "concrete_episode":
            response = repair_responses[str(addition["source_reference"])]
            text = str(response["exact_text"]).strip()
            raw_actions = addition.get("actions_in_temporal_order", [])
            actions = tuple(
                str(value).strip() for value in cast(list[Any], raw_actions) if str(value).strip()
            )
            episodes.append(
                DevelopmentTransferEpisode(
                    episode_id=addition_id,
                    origin_id=addition_id,
                    collection_phase="v8.1_repair",
                    domain_id=pattern_domain.get(target_pattern_id),
                    approximate_age_life_phase=str(
                        addition.get("approximate_age_life_phase") or "unknown"
                    ),
                    age_estimation_basis="participant-supplied in v8.1 repair response",
                    source_review_scope="post_review_participant_approved",
                    source_completeness="exact_repair_response_plus_transfer_summary",
                    bounded_situation=str(addition["bounded_situation"]),
                    actions_in_temporal_order=actions,
                    outcome_when_known=(
                        str(addition["outcome_when_known"])
                        if isinstance(addition.get("outcome_when_known"), str)
                        else None
                    ),
                    participant_stated_explanation=(
                        str(addition["participant_stated_explanation"])
                        if isinstance(addition.get("participant_stated_explanation"), str)
                        else None
                    ),
                    exact_source_segments=(
                        DevelopmentSourceSegment(
                            segment_id=f"{addition_id}-SEG-01",
                            exact_text=text,
                            provenance_refs=(str(addition["source_reference"]),),
                        ),
                    ),
                    transfer_summary=_repair_episode_summary(addition),
                )
            )
        else:
            auxiliary.append(
                DevelopmentAuxiliaryEvidence(
                    evidence_id=addition_id,
                    evidence_type=evidence_type or "unspecified",
                    target_pattern_id=target_pattern_id,
                    payload=addition,
                )
            )

    series_reports: list[DevelopmentTransferSeriesReport] = []
    for row in series_raw:
        series_id = str(row["series_id"])
        turn_ids = tuple(str(value) for value in cast(list[Any], row.get("source_turn_ids", [])))
        exact_segments = tuple(
            DevelopmentSourceSegment(
                segment_id=f"{series_id}-SEG-{index:02d}",
                exact_text=recovered_turns[turn_id],
                provenance_refs=(turn_id,),
            )
            for index, turn_id in enumerate(turn_ids, start=1)
            if turn_id in recovered_turns
        )
        rough = row.get("rough_opportunity_count")
        series_reports.append(
            DevelopmentTransferSeriesReport(
                series_id=series_id,
                origin_id=series_id,
                collection_phase="v8_original",
                domain_id=(str(row["domain_id"]) if isinstance(row.get("domain_id"), str) else None),
                bounded_period_context=str(row["bounded_period_context"]),
                approximate_age_life_phase=str(row["approximate_age_life_phase"]),
                recurrence_language=str(row["participant_recurrence_language"]),
                rough_opportunity_count=(str(rough) if rough is not None else None),
                behavior_reportedly_recurred=str(row["behavior_reportedly_recurred"]),
                explicit_exceptions_or_limits=(
                    str(row["explicit_exceptions"])
                    if isinstance(row.get("explicit_exceptions"), str)
                    else None
                ),
                memory_source_uncertainty=(
                    str(row["memory_source_uncertainty"])
                    if isinstance(row.get("memory_source_uncertainty"), str)
                    else None
                ),
                original_source_turn_ids=turn_ids,
                exact_source_segments=exact_segments,
                source_completeness=(
                    "partial_exact_recovered_turns" if exact_segments else "transfer_summary_only"
                ),
            )
        )

    for evidence in auxiliary:
        if evidence.evidence_type != "repeated_series_report":
            continue
        row = evidence.payload
        response = repair_responses[str(row["source_reference"])]
        text = str(response["exact_text"]).strip()
        series_reports.append(
            DevelopmentTransferSeriesReport(
                series_id=evidence.evidence_id,
                origin_id=evidence.evidence_id,
                collection_phase="v8.1_repair",
                domain_id=pattern_domain.get(evidence.target_pattern_id),
                bounded_period_context=str(row["bounded_period_context"]),
                approximate_age_life_phase=str(row["approximate_age_life_phase"]),
                recurrence_language=str(row["participant_recurrence_language"]),
                rough_opportunity_count=(
                    str(row["rough_opportunity_count"])
                    if row.get("rough_opportunity_count") is not None
                    else None
                ),
                behavior_reportedly_recurred=str(row["behavior_reportedly_recurred"]),
                explicit_exceptions_or_limits=(
                    str(row["explicit_exceptions_or_limits"])
                    if isinstance(row.get("explicit_exceptions_or_limits"), str)
                    else None
                ),
                memory_source_uncertainty=(
                    str(row["memory_source_uncertainty"])
                    if isinstance(row.get("memory_source_uncertainty"), str)
                    else None
                ),
                exact_source_segments=(
                    DevelopmentSourceSegment(
                        segment_id=f"{evidence.evidence_id}-SEG-01",
                        exact_text=text,
                        provenance_refs=(str(row["source_reference"]),),
                    ),
                ),
                source_completeness="partial_exact_recovered_turns",
            )
        )

    payload = DevelopmentTransferCorpusPayload(
        source_record_schema_version=str(original["schema_version"]),
        source_record_sha256=sha256_json(original),
        supplement_schema_version=str(supplement["schema_version"]),
        supplement_sha256=sha256_json(supplement),
        participant_theory_exposure=participant_theory_exposure,
        source_record_status=str(original["record_status"]),
        supplement_status=str(supplement["supplement_status"]),
        episodes=tuple(episodes),
        series_reports=tuple(series_reports),
        pattern_claims=tuple(patterns_raw),
        auxiliary_post_review_evidence=tuple(auxiliary),
        created_at_utc=created_at_utc,
    )
    digest = sha256_json(payload)
    return DevelopmentTransferCorpusArtifact(
        corpus_id=f"LPDC-{digest[:20].upper()}",
        corpus_sha256=digest,
        payload=payload,
    )


def development_transfer_corpus_integrity_errors(
    artifact: DevelopmentTransferCorpusArtifact,
) -> tuple[str, ...]:
    digest = sha256_json(artifact.payload)
    if artifact.corpus_sha256 != digest or artifact.corpus_id != f"LPDC-{digest[:20].upper()}":
        return ("development transfer corpus failed content-address verification",)
    if artifact.payload.canonical_behavioral_freeze_eligible:
        return ("development transfer corpus must not claim canonical freeze eligibility",)
    if not artifact.payload.validation_use_forbidden:
        return ("development transfer corpus must remain blocked from validation use",)
    return ()


def build_development_episode_tasks(
    artifact: DevelopmentTransferCorpusArtifact,
    *,
    observable_ids: tuple[str, ...],
) -> tuple[DevelopmentEpisodeCodingTask, ...]:
    errors = development_transfer_corpus_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid development transfer corpus: " + "; ".join(errors))
    if not observable_ids or len(observable_ids) != len(set(observable_ids)):
        raise ValueError("development task observable IDs must be nonempty and unique")

    tasks: list[DevelopmentEpisodeCodingTask] = []
    for episode in artifact.payload.episodes:
        task_payload = {
            "corpus_id": artifact.corpus_id,
            "corpus_sha256": artifact.corpus_sha256,
            "episode_id": episode.episode_id,
            "domain_id": episode.domain_id,
            "approximate_age_life_phase": episode.approximate_age_life_phase,
            "episode_narrative": episode.transfer_summary,
            "exact_source_segments": episode.exact_source_segments,
            "source_completeness": episode.source_completeness,
            "observable_ids": observable_ids,
            "participant_theory_exposure": artifact.payload.participant_theory_exposure,
        }
        digest = sha256_json(task_payload)
        tasks.append(
            DevelopmentEpisodeCodingTask(
                task_id=f"LPDT-{digest[:20].upper()}",
                **task_payload,
            )
        )
    return tuple(tasks)


def build_development_task_manifest(
    artifact: DevelopmentTransferCorpusArtifact,
    *,
    tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    created_at_utc: datetime,
) -> DevelopmentTaskSetManifestArtifact:
    if not tasks:
        raise ValueError("development task set cannot be empty")
    for task in tasks:
        if task.corpus_id != artifact.corpus_id or task.corpus_sha256 != artifact.corpus_sha256:
            raise ValueError("development task does not bind supplied corpus")
    task_set_sha256 = sha256_json(tasks)
    observable_ids = tasks[0].observable_ids
    if any(task.observable_ids != observable_ids for task in tasks):
        raise ValueError("development task set has inconsistent observable universes")
    payload = DevelopmentTaskSetManifestPayload(
        corpus_id=artifact.corpus_id,
        corpus_sha256=artifact.corpus_sha256,
        task_set_sha256=task_set_sha256,
        episode_task_count=len(tasks),
        observable_count=len(observable_ids),
        expected_episode_observable_unit_count=len(tasks) * len(observable_ids),
        series_report_count=len(artifact.payload.series_reports),
        created_at_utc=created_at_utc,
    )
    digest = sha256_json(payload)
    return DevelopmentTaskSetManifestArtifact(
        manifest_id=f"LPDM-{digest[:20].upper()}",
        manifest_sha256=digest,
        payload=payload,
    )


def write_development_transfer_corpus(
    path: str | Path,
    artifact: DevelopmentTransferCorpusArtifact,
) -> Path:
    errors = development_transfer_corpus_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid development transfer corpus: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_development_transfer_corpus(path: str | Path) -> DevelopmentTransferCorpusArtifact:
    raw = load_json_bytes(path, require_canonical=True)
    artifact = DevelopmentTransferCorpusArtifact.model_validate(raw)
    errors = development_transfer_corpus_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid development transfer corpus: " + "; ".join(errors))
    return artifact
