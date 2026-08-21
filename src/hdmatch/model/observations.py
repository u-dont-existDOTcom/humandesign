"""Typed V4 behavioral observations, kept separate from chart interpretation."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class BehavioralObservation(BaseModel):
    """Candidate-blind atomic observation from the V4 profile-synthesis phase."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    observation_id: str = Field(min_length=1)
    behavioral_statement: str = Field(min_length=1)
    contexts_where_true: tuple[str, ...] = ()
    exceptions: tuple[str, ...] = ()
    examples: tuple[str, ...] = ()
    counterexamples: tuple[str, ...] = ()
    life_periods: tuple[str, ...] = ()
    source_types: tuple[
        Literal[
            "self_report",
            "contemporaneous_record",
            "independent_informant",
            "public_writing",
            "behavioral_record",
            "prospective_log",
        ],
        ...,
    ] = ()
    behavioral_confidence: float = Field(ge=0.0, le=1.0)
    measurement_reliability: float = Field(ge=0.0, le=1.0)
    dependency_cluster: str = Field(min_length=1)
    state_sensitive: bool = False
    body_access_sensitive: bool = False
    holdout_eligible: bool = True
    status: Literal["discovery", "holdout", "excluded"] = "discovery"

    @property
    def effective_confidence(self) -> float:
        return self.behavioral_confidence * self.measurement_reliability
