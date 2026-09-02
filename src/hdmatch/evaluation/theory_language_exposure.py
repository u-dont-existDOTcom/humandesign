"""Chart-blind diagnostic for observable astrology/HD language exposure signals."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Sequence
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class LanguageSpecificity(StrEnum):
    THEORY_SPECIFIC = "theory_specific"
    CONTEXT_DEPENDENT = "context_dependent"
    ORDINARY_LANGUAGE_EXCLUSION = "ordinary_language_exclusion"


class ParticipantStance(StrEnum):
    AFFIRMATIVE = "affirmative"
    NEUTRAL_QUOTE = "neutral_quote"
    EXPLICIT_REJECTION = "explicit_rejection"
    PREVIOUS_EXPOSURE_MENTION = "previous_exposure_mention"
    UNRESOLVED = "unresolved"


class MatchSource(StrEnum):
    PARTICIPANT_SPONTANEOUS = "participant_spontaneous"
    INTERVIEWER_INTRODUCED_OR_ECHOED = "interviewer_introduced_or_echoed"
    PARTICIPANT_QUOTED_OR_REPORTED = "participant_quoted_or_reported"


class LanguageAssessability(StrEnum):
    FULLY_ASSESSABLE = "fully_assessable"
    PARTIALLY_ASSESSABLE = "partially_assessable"
    NOT_ADEQUATELY_ASSESSABLE = "not_adequately_assessable"


class ExposureSignalLevel(StrEnum):
    THEORY_SPECIFIC_EXPOSURE_SIGNAL_PRESENT = "theory_specific_exposure_signal_present"
    INTERVIEWER_ECHO_ONLY = "interviewer_echo_only"
    CONTEXT_DEPENDENT_LANGUAGE_ONLY = "context_dependent_language_only"
    NO_USABLE_THEORY_LANGUAGE_SIGNAL = "no_usable_theory_language_signal"
    NOT_ASSESSED = "not_assessed"


class TheoryLanguageEntry(FrozenModel):
    entry_id: str = Field(pattern=r"^TL-[A-Z0-9-]+$")
    theory: Literal["astrology", "human_design", "cross_theory"]
    specificity: LanguageSpecificity
    language: str = Field(pattern=r"^[a-z]{2,3}(?:-[A-Za-z0-9]+)*$")
    expressions: tuple[str, ...] = Field(min_length=1)
    rationale: str = Field(min_length=1)
    validation_status: Literal["draft_not_validated"] = "draft_not_validated"

    @field_validator("expressions")
    @classmethod
    def expressions_are_nonblank(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if any(not expression.strip() for expression in value):
            raise ValueError("codebook expressions cannot be blank")
        return value


class TheoryLanguageCodebook(FrozenModel):
    schema_version: Literal["astrohd-theory-language-codebook-v0.1"]
    status: Literal["draft_evaluation_only_not_validated"]
    supported_languages: tuple[str, ...] = Field(min_length=1)
    entries: tuple[TheoryLanguageEntry, ...] = Field(min_length=1)
    forbidden_uses: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def identifiers_and_expressions_are_unique(self) -> TheoryLanguageCodebook:
        ids = [entry.entry_id for entry in self.entries]
        if len(ids) != len(set(ids)):
            raise ValueError("theory-language entry IDs must be unique")
        seen: set[tuple[str, str]] = set()
        for entry in self.entries:
            if entry.language not in self.supported_languages:
                raise ValueError("entry language must be declared supported")
            for expression in entry.expressions:
                key = (entry.language, _normalize(expression))
                if key in seen:
                    raise ValueError("codebook expressions must be unique per language")
                seen.add(key)
        return self


class TranscriptTurn(FrozenModel):
    turn_id: str = Field(pattern=r"^TURN-[A-Za-z0-9_-]+$")
    speaker: Literal["interviewer", "participant"]
    text: str = Field(min_length=1)
    language: str = Field(pattern=r"^[a-z]{2,3}(?:-[A-Za-z0-9]+)*$")
    stance_annotation: ParticipantStance = ParticipantStance.UNRESOLVED


class TheoryLanguageMatch(FrozenModel):
    turn_id: str
    entry_id: str
    theory: Literal["astrology", "human_design", "cross_theory"]
    specificity: LanguageSpecificity
    matched_expression: str
    source: MatchSource
    stance: ParticipantStance


class ExposureConsequences(FrozenModel):
    diagnostic_or_stratification_only: Literal[True] = True
    eligibility_unchanged: Literal[True] = True
    questionnaire_flow_unchanged: Literal[True] = True
    scoring_unchanged: Literal[True] = True
    primary_analysis_unchanged: Literal[True] = True


class TheoryLanguageExposureAssessment(FrozenModel):
    schema_version: Literal["astrohd-theory-language-exposure-assessment-v0.1"] = (
        "astrohd-theory-language-exposure-assessment-v0.1"
    )
    signal_level: ExposureSignalLevel
    language_assessability: LanguageAssessability
    assessed_languages: tuple[str, ...]
    unassessed_languages: tuple[str, ...]
    matches: tuple[TheoryLanguageMatch, ...]
    codebook_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    chart_and_prediction_inputs_absent: Literal[True] = True
    causal_contamination_inference_permitted: Literal[False] = False
    consequences: ExposureConsequences = Field(default_factory=ExposureConsequences)


def load_theory_language_codebook(
    path: str | Path,
) -> tuple[TheoryLanguageCodebook, str]:
    source = Path(path)
    raw = source.read_bytes()
    codebook = TheoryLanguageCodebook.model_validate(json.loads(raw))
    return codebook, hashlib.sha256(raw).hexdigest()


def assess_theory_language_exposure(
    transcript: Sequence[TranscriptTurn],
    *,
    codebook: TheoryLanguageCodebook,
    codebook_sha256: str,
) -> TheoryLanguageExposureAssessment:
    """Assess observable wording without access to charts, predictions, scores, or results."""

    assessed_languages = sorted(
        {turn.language for turn in transcript if turn.language in codebook.supported_languages}
    )
    unassessed_languages = sorted(
        {turn.language for turn in transcript if turn.language not in codebook.supported_languages}
    )
    if assessed_languages and unassessed_languages:
        assessability = LanguageAssessability.PARTIALLY_ASSESSABLE
    elif assessed_languages:
        assessability = LanguageAssessability.FULLY_ASSESSABLE
    else:
        assessability = LanguageAssessability.NOT_ADEQUATELY_ASSESSABLE

    entries_by_language: dict[str, tuple[TheoryLanguageEntry, ...]] = {
        language: tuple(entry for entry in codebook.entries if entry.language == language)
        for language in codebook.supported_languages
    }
    interviewer_seen: set[str] = set()
    matches: list[TheoryLanguageMatch] = []
    for turn in transcript:
        if turn.language not in codebook.supported_languages:
            continue
        for entry, expression in _turn_matches(turn.text, entries_by_language[turn.language]):
            if turn.speaker == "interviewer":
                interviewer_seen.add(entry.entry_id)
                continue
            if entry.entry_id in interviewer_seen:
                source = MatchSource.INTERVIEWER_INTRODUCED_OR_ECHOED
            elif turn.stance_annotation in {
                ParticipantStance.NEUTRAL_QUOTE,
                ParticipantStance.EXPLICIT_REJECTION,
                ParticipantStance.PREVIOUS_EXPOSURE_MENTION,
            }:
                source = MatchSource.PARTICIPANT_QUOTED_OR_REPORTED
            else:
                source = MatchSource.PARTICIPANT_SPONTANEOUS
            matches.append(
                TheoryLanguageMatch(
                    turn_id=turn.turn_id,
                    entry_id=entry.entry_id,
                    theory=entry.theory,
                    specificity=entry.specificity,
                    matched_expression=expression,
                    source=source,
                    stance=turn.stance_annotation,
                )
            )

    signal_level = _signal_level(matches, assessability)
    return TheoryLanguageExposureAssessment(
        signal_level=signal_level,
        language_assessability=assessability,
        assessed_languages=tuple(assessed_languages),
        unassessed_languages=tuple(unassessed_languages),
        matches=tuple(matches),
        codebook_sha256=codebook_sha256,
    )


def _signal_level(
    matches: Sequence[TheoryLanguageMatch],
    assessability: LanguageAssessability,
) -> ExposureSignalLevel:
    if assessability is LanguageAssessability.NOT_ADEQUATELY_ASSESSABLE:
        return ExposureSignalLevel.NOT_ASSESSED
    theory_specific = [
        match for match in matches if match.specificity is LanguageSpecificity.THEORY_SPECIFIC
    ]
    if any(
        match.source is not MatchSource.INTERVIEWER_INTRODUCED_OR_ECHOED
        for match in theory_specific
    ):
        return ExposureSignalLevel.THEORY_SPECIFIC_EXPOSURE_SIGNAL_PRESENT
    if theory_specific:
        return ExposureSignalLevel.INTERVIEWER_ECHO_ONLY
    if any(match.specificity is LanguageSpecificity.CONTEXT_DEPENDENT for match in matches):
        return ExposureSignalLevel.CONTEXT_DEPENDENT_LANGUAGE_ONLY
    return ExposureSignalLevel.NO_USABLE_THEORY_LANGUAGE_SIGNAL


def _normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def _first_match(text: str, expressions: Sequence[str]) -> str | None:
    match = _first_match_with_span(text, expressions)
    return None if match is None else match[0]


def _first_match_with_span(
    text: str, expressions: Sequence[str]
) -> tuple[str, tuple[int, int]] | None:
    normalized = _normalize(text)
    for expression in expressions:
        candidate = _normalize(expression)
        escaped_candidate = re.escape(candidate).replace(r"\ ", r"\s+")
        pattern = rf"(?<!\w){escaped_candidate}(?!\w)"
        if match := re.search(pattern, normalized):
            return expression, match.span()
    return None


def _turn_matches(
    text: str, entries: Sequence[TheoryLanguageEntry]
) -> tuple[tuple[TheoryLanguageEntry, str], ...]:
    raw: list[tuple[TheoryLanguageEntry, str, tuple[int, int]]] = []
    for entry in entries:
        if match := _first_match_with_span(text, entry.expressions):
            expression, span = match
            raw.append((entry, expression, span))

    specificity_rank = {
        LanguageSpecificity.CONTEXT_DEPENDENT: 1,
        LanguageSpecificity.ORDINARY_LANGUAGE_EXCLUSION: 2,
        LanguageSpecificity.THEORY_SPECIFIC: 3,
    }
    retained = []
    for entry, expression, span in raw:
        contained_by_more_specific = any(
            other_span[0] <= span[0]
            and other_span[1] >= span[1]
            and specificity_rank[other_entry.specificity] > specificity_rank[entry.specificity]
            for other_entry, _, other_span in raw
        )
        if not contained_by_more_specific:
            retained.append((entry, expression))
    return tuple(retained)
