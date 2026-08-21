"""Questionnaire response records and deterministic answer-token normalization."""

from __future__ import annotations

import re
import unicodedata

from pydantic import BaseModel, ConfigDict, Field, field_validator

_NON_TOKEN = re.compile(r"[^a-z0-9]+")


def normalize_answer_token(label: str) -> str:
    """Convert a declared answer label into a stable ASCII identifier.

    The transformation is deliberately mechanical. It never interprets a response or
    adds an HD-favouring meaning.
    """

    ascii_label = unicodedata.normalize("NFKD", label).encode("ascii", "ignore").decode()
    return _NON_TOKEN.sub("_", ascii_label.casefold()).strip("_")


class NormalizedResponse(BaseModel):
    """One categorical response consumed by the symbolic scorer."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    question_id: str = Field(min_length=1)
    answer_token: str = Field(pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    behavioral_confidence: float = Field(ge=0.0, le=1.0)
    measurement_reliability: float = Field(ge=0.0, le=1.0)

    @field_validator("question_id")
    @classmethod
    def uppercase_question_id(cls, value: str) -> str:
        return value.strip().upper()

    @property
    def effective_confidence(self) -> float:
        """Reliability can only remove evidence; it can never create support."""

        return self.behavioral_confidence * self.measurement_reliability
