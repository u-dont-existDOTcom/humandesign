"""Exact-match, chart-blind theory-language exposure research scaffold."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Sequence
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class LexicalSpecificity(StrEnum):
    THEORY_SPECIFIC = "theory_specific"
    CONTEXT_DEPENDENT = "context_dependent"
    ORDINARY_LANGUAGE_EXCLUDED = "ordinary_language_excluded"


class OccurrenceProvenance(StrEnum):
    PARTICIPANT_SPONTANEOUS = "participant_spontaneous"
    PARTICIPANT_AFTER_INTERVIEWER_SAME_TERM = "participant_after_interviewer_same_term"
    QUOTED_OR_REPORTED_SOURCE = "quoted_or_reported_source"
    PROVENANCE_UNKNOWN = "provenance_unknown"


class ParticipantStance(StrEnum):
    AFFIRMED = "affirmed"
    NEUTRAL_OR_QUOTED = "neutral_or_quoted"
    REJECTED = "rejected"
    STANCE_UNKNOWN = "stance_unknown"


class LanguageAssessability(StrEnum):
    ASSESSABLE = "assessable"
    NOT_ASSESSABLE = "not_assessable"
    LANGUAGE_UNKNOWN = "language_unknown"


class TheoryLanguageEntry(FrozenModel):
    entry_id: str = Field(pattern=r"^[A-Z][A-Z0-9_-]*$")
    exact_phrase: str = Field(min_length=1)
    language_code: str = Field(min_length=1)
    lexical_specificity: LexicalSpecificity
    rationale_or_provenance_note: str | None = None
    version: str = Field(min_length=1)
    freeze_identifier: str = Field(min_length=1)

    @field_validator("exact_phrase", "language_code", "version", "freeze_identifier")
    @classmethod
    def required_strings_are_not_whitespace(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("required codebook strings cannot be whitespace")
        return value


class TheoryLanguageCodebook(FrozenModel):
    schema_version: Literal["astrohd-theory-language-codebook-template-v1"]
    status: Literal["draft_synthetic_template_non_authority"]
    version: str = Field(min_length=1)
    freeze_identifier: str = Field(min_length=1)
    entries: tuple[TheoryLanguageEntry, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def identifiers_and_exact_phrases_are_unique(self) -> TheoryLanguageCodebook:
        identifiers = [entry.entry_id for entry in self.entries]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("theory-language entry IDs must be unique")

        phrase_keys: set[tuple[str, str]] = set()
        for entry in self.entries:
            if entry.version != self.version:
                raise ValueError("entry version must match codebook version")
            if entry.freeze_identifier != self.freeze_identifier:
                raise ValueError("entry freeze identifier must match the codebook")
            key = (entry.language_code, normalize_for_exact_matching(entry.exact_phrase))
            if key in phrase_keys:
                raise ValueError("exact phrases must be unique per language")
            phrase_keys.add(key)
        return self

    @property
    def language_codes(self) -> frozenset[str]:
        return frozenset(entry.language_code for entry in self.entries)


class TranscriptTurn(FrozenModel):
    turn_id: str = Field(pattern=r"^TURN-[A-Za-z0-9_-]+$")
    speaker: Literal["interviewer", "participant"]
    text: str = Field(min_length=1)
    response_language: str | None = None
    stance_annotation: ParticipantStance = ParticipantStance.STANCE_UNKNOWN
    provenance_annotation: (
        Literal[
            OccurrenceProvenance.QUOTED_OR_REPORTED_SOURCE,
            OccurrenceProvenance.PROVENANCE_UNKNOWN,
        ]
        | None
    ) = None

    @field_validator("response_language")
    @classmethod
    def language_is_not_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("response language cannot be blank")
        return value


class TheoryLanguageOccurrence(FrozenModel):
    turn_id: str
    entry_id: str
    normalized_exact_phrase: str
    language_code: str
    lexical_specificity: LexicalSpecificity
    provenance: OccurrenceProvenance
    stance: ParticipantStance


class TheoryLanguageExposureAssessment(FrozenModel):
    schema_version: Literal["astrohd-theory-language-exposure-assessment-v1"] = (
        "astrohd-theory-language-exposure-assessment-v1"
    )
    status: Literal["draft_non_authority_no_runtime_effect"] = (
        "draft_non_authority_no_runtime_effect"
    )
    matching_policy: Literal["frozen_exact_phrase_only"] = "frozen_exact_phrase_only"
    language_assessability: LanguageAssessability
    occurrences: tuple[TheoryLanguageOccurrence, ...]
    theory_specific_exposure_evidence_present: bool
    codebook_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    target_chart_and_prediction_inputs_absent: Literal[True] = True
    participant_effects: Literal["none_diagnostic_metadata_only"] = "none_diagnostic_metadata_only"


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
    """Return exact lexical occurrences without chart, prediction, or outcome inputs."""

    participant_turns = tuple(turn for turn in transcript if turn.speaker == "participant")
    language_assessability = _language_assessability(participant_turns, codebook)
    if language_assessability is not LanguageAssessability.ASSESSABLE:
        return TheoryLanguageExposureAssessment(
            language_assessability=language_assessability,
            occurrences=(),
            theory_specific_exposure_evidence_present=False,
            codebook_sha256=codebook_sha256,
        )

    entries_by_language: dict[str, tuple[TheoryLanguageEntry, ...]] = {
        language_code: tuple(
            entry for entry in codebook.entries if entry.language_code == language_code
        )
        for language_code in codebook.language_codes
    }
    interviewer_phrases_seen: set[tuple[str, str]] = set()
    occurrences: list[TheoryLanguageOccurrence] = []
    for turn in transcript:
        if turn.response_language is None:
            continue
        for entry in entries_by_language.get(turn.response_language, ()):
            normalized_phrase = normalize_for_exact_matching(entry.exact_phrase)
            if not _contains_exact_phrase(turn.text, normalized_phrase):
                continue
            phrase_key = (turn.response_language, normalized_phrase)
            if turn.speaker == "interviewer":
                interviewer_phrases_seen.add(phrase_key)
                continue
            provenance = _participant_provenance(
                turn,
                phrase_key=phrase_key,
                interviewer_phrases_seen=interviewer_phrases_seen,
            )
            occurrences.append(
                TheoryLanguageOccurrence(
                    turn_id=turn.turn_id,
                    entry_id=entry.entry_id,
                    normalized_exact_phrase=normalized_phrase,
                    language_code=entry.language_code,
                    lexical_specificity=entry.lexical_specificity,
                    provenance=provenance,
                    stance=turn.stance_annotation,
                )
            )

    return TheoryLanguageExposureAssessment(
        language_assessability=language_assessability,
        occurrences=tuple(occurrences),
        theory_specific_exposure_evidence_present=any(
            occurrence.lexical_specificity is LexicalSpecificity.THEORY_SPECIFIC
            for occurrence in occurrences
        ),
        codebook_sha256=codebook_sha256,
    )


def normalize_for_exact_matching(text: str) -> str:
    """Apply only NFKC, case folding, and whitespace normalization."""

    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def _language_assessability(
    participant_turns: Sequence[TranscriptTurn], codebook: TheoryLanguageCodebook
) -> LanguageAssessability:
    if not participant_turns or any(turn.response_language is None for turn in participant_turns):
        return LanguageAssessability.LANGUAGE_UNKNOWN
    if any(turn.response_language not in codebook.language_codes for turn in participant_turns):
        return LanguageAssessability.NOT_ASSESSABLE
    return LanguageAssessability.ASSESSABLE


def _contains_exact_phrase(text: str, normalized_phrase: str) -> bool:
    normalized_text = normalize_for_exact_matching(text)
    escaped_phrase = re.escape(normalized_phrase).replace(r"\ ", r"\s+")
    return re.search(rf"(?<!\w){escaped_phrase}(?!\w)", normalized_text) is not None


def _participant_provenance(
    turn: TranscriptTurn,
    *,
    phrase_key: tuple[str, str],
    interviewer_phrases_seen: set[tuple[str, str]],
) -> OccurrenceProvenance:
    if phrase_key in interviewer_phrases_seen:
        return OccurrenceProvenance.PARTICIPANT_AFTER_INTERVIEWER_SAME_TERM
    if turn.provenance_annotation is not None:
        return OccurrenceProvenance(turn.provenance_annotation)
    return OccurrenceProvenance.PARTICIPANT_SPONTANEOUS
