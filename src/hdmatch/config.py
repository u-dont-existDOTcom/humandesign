"""Strict experiment configuration loading."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field


class SyntheticConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    experiment_id: str
    # Generation seeds are secret until reveal. Public repository configs leave
    # this null; the CLI creates or reads the seed outside the decoder root.
    seed: int | None = None
    case_count: int = Field(default=1000, ge=1)
    tier: Literal["oracle", "low", "medium", "adversarial"] = "oracle"
    universe: Literal["known_month", "known_date"] = "known_month"
    year_start: int = 1950
    year_end: int = 2020
    timezone: str = "UTC"
    birthplace: str = "Synthetic UTC"
    aggregation: Literal["best_state", "duration_weighted_mean", "duration_weighted_evidence"] = (
        "duration_weighted_evidence"
    )
    threshold_rubric_bits: float = 0.0
    ephemeris_path: str | None = None


def load_synthetic_config(path: str | Path) -> SyntheticConfig:
    config_path = Path(path)
    if config_path.suffix.lower() == ".json":
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    else:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("configuration root must be an object")
    return SyntheticConfig.model_validate(raw)
