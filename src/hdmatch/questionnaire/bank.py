"""Typed access to the normative candidate-blind question bank."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class FrozenModel(BaseModel):
    """Strict immutable questionnaire record."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class Question(FrozenModel):
    """One question exactly as declared in ``question_bank_v1.json``."""

    id: str = Field(min_length=1)
    phase: str = Field(min_length=1)
    domain: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    response_format: str = Field(min_length=1)
    followups: tuple[str, ...]
    body_access_sensitive: bool
    minimum_evidence: str = Field(min_length=1)
    behavioral_constructs: tuple[str, ...] = Field(min_length=1)
    scoring_notes: str

    @field_validator("id")
    @classmethod
    def normalize_id(cls, value: str) -> str:
        normalized = value.strip().upper()
        if normalized != value:
            raise ValueError("question IDs must already be uppercase and whitespace-free")
        return normalized

    @field_validator("followups", "behavioral_constructs")
    @classmethod
    def reject_blank_items(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if any(not item.strip() for item in value):
            raise ValueError("question lists cannot contain blank values")
        return value

    @property
    def response_format_options(self) -> tuple[str, ...]:
        """Return literal slash-delimited response options when the bank declares them."""

        if "/" not in self.response_format:
            return ()
        return tuple(part.strip() for part in self.response_format.split("/") if part.strip())


class QuestionBank(FrozenModel):
    """The complete versioned question bank."""

    version: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    rules: tuple[str, ...] = Field(min_length=1)
    questions: tuple[Question, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_question_ids(self) -> QuestionBank:
        ids = [question.id for question in self.questions]
        if len(ids) != len(set(ids)):
            duplicates = sorted({question_id for question_id in ids if ids.count(question_id) > 1})
            raise ValueError(f"duplicate question IDs: {', '.join(duplicates)}")
        return self

    def by_id(self, question_id: str) -> Question:
        """Return a question by its frozen ID."""

        for question in self.questions:
            if question.id == question_id:
                return question
        raise KeyError(question_id)

    @property
    def question_ids(self) -> frozenset[str]:
        return frozenset(question.id for question in self.questions)


def load_question_bank(path: str | Path) -> QuestionBank:
    """Read and strictly validate a normative question-bank JSON file."""

    source = Path(path)
    return QuestionBank.model_validate(json.loads(source.read_text(encoding="utf-8")))
