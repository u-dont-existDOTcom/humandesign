"""Versioned human-case import without exposing final-test labels to fitting code."""

from __future__ import annotations

import csv
import json
import math
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hdmatch.util import sha256_file


class HumanCase(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    participant_id: str
    cohort: Literal["development", "validation", "final_test", "unassigned"]
    responses: dict[str, str]
    response_reliability: dict[str, float] = Field(default_factory=dict)
    chart_features: dict[str, str | bool | int | float | list[str]]
    birth_year: int | None = None
    birth_month: int | None = Field(default=None, ge=1, le=12)
    birth_day: int | None = Field(default=None, ge=1, le=31)
    documented_time_precision_minutes: int | None = Field(default=None, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def valid_response_reliability(self) -> HumanCase:
        unknown = set(self.response_reliability) - set(self.responses)
        if unknown:
            raise ValueError(f"reliability supplied for unanswered questions: {sorted(unknown)}")
        invalid = sorted(
            question
            for question, value in self.response_reliability.items()
            if not math.isfinite(value) or not 0.0 <= value <= 1.0
        )
        if invalid:
            raise ValueError(f"response reliability must be within [0, 1]: {invalid}")
        return self


class HumanDataset(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-dataset-v1"] = "human-dataset-v1"
    questionnaire_version: str
    cases: tuple[HumanCase, ...]
    source_sha256: str | None = None

    @model_validator(mode="after")
    def unique_people(self) -> HumanDataset:
        identifiers = [case.participant_id for case in self.cases]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError(
                "participant_id must be unique; merge a person's answers before import"
            )
        return self


def _from_rows(rows: Iterable[dict[str, Any]], questionnaire_version: str) -> HumanDataset:
    return HumanDataset(
        questionnaire_version=questionnaire_version,
        cases=tuple(HumanCase.model_validate(row) for row in rows),
    )


def load_human_dataset(path: str | Path, questionnaire_version: str) -> HumanDataset:
    """Load JSON, JSONL, CSV, or Parquet records into the strict person-level schema."""

    source = Path(path)
    suffix = source.suffix.lower()
    if suffix == ".json":
        raw = json.loads(source.read_text(encoding="utf-8"))
        if isinstance(raw, dict) and "cases" in raw:
            dataset = HumanDataset.model_validate(raw)
        elif isinstance(raw, list):
            dataset = _from_rows(raw, questionnaire_version)
        else:
            raise ValueError("JSON human dataset must be a list or HumanDataset object")
    elif suffix == ".jsonl":
        rows = [
            json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line
        ]
        dataset = _from_rows(rows, questionnaire_version)
    elif suffix == ".csv":
        with source.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        decoded: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            for field in ("responses", "response_reliability", "chart_features", "metadata"):
                item[field] = json.loads(item[field]) if item.get(field) else {}
            integer_fields = (
                "birth_year",
                "birth_month",
                "birth_day",
                "documented_time_precision_minutes",
            )
            for field in integer_fields:
                item[field] = int(item[field]) if item.get(field) else None
            decoded.append(item)
        dataset = _from_rows(decoded, questionnaire_version)
    elif suffix in {".parquet", ".pq"}:
        try:
            import pandas as pd  # type: ignore[import-untyped]
        except ImportError as exc:  # pragma: no cover - optional dependency boundary
            raise RuntimeError("Parquet import requires the empirical extra") from exc
        rows = pd.read_parquet(source).to_dict(orient="records")
        dataset = _from_rows(rows, questionnaire_version)
    else:
        raise ValueError(f"unsupported human dataset format: {suffix}")
    return dataset.model_copy(update={"source_sha256": sha256_file(source)})
