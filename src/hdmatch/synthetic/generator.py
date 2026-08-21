"""Blind synthetic cases generated only from a declared frozen model."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.config import SyntheticConfig
from hdmatch.schemas import BehavioralResponse, BlindCase, ChartFeatures
from hdmatch.synthetic.noise import NoiseTier, apply_noise
from hdmatch.util import canonical_json_bytes, sha256_bytes, sha256_json


class ChartCalculator(Protocol):
    def calculate(self, utc_moment: datetime) -> ChartFeatures: ...


class FrozenResponseModel(Protocol):
    @property
    def model_id(self) -> str: ...

    @property
    def model_sha256(self) -> str: ...

    @property
    def mapping_sha256(self) -> str: ...

    @property
    def question_bank_sha256(self) -> str: ...

    def oracle_responses(self, chart: ChartFeatures) -> Sequence[BehavioralResponse]: ...

    def answer_spaces(self) -> Mapping[str, Sequence[str]]: ...


class BlindSyntheticBundle(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    blind_document: dict[str, Any]
    answer_key: dict[str, Any]
    blind_input_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class SyntheticGenerator:
    def __init__(
        self, chart_calculator: ChartCalculator, response_model: FrozenResponseModel
    ) -> None:
        self.chart_calculator = chart_calculator
        self.response_model = response_model

    @staticmethod
    def _sample_utc_moments(config: SyntheticConfig) -> tuple[datetime, ...]:
        if config.seed is None:
            raise ValueError("synthetic generation requires a secret seed")
        zone = ZoneInfo(config.timezone)
        start = datetime(config.year_start, 1, 1, tzinfo=zone).astimezone(UTC)
        end = datetime(config.year_end + 1, 1, 1, tzinfo=zone).astimezone(UTC)
        seconds = int((end - start).total_seconds())
        if seconds <= 0:
            raise ValueError("year_end must not precede year_start")
        rng = random.Random(config.seed)
        return tuple(
            start + timedelta(seconds=rng.randrange(seconds)) for _ in range(config.case_count)
        )

    def generate(self, config: SyntheticConfig) -> BlindSyntheticBundle:
        if config.seed is None:
            raise ValueError("synthetic generation requires a secret seed")
        generation_seed = config.seed
        tier = NoiseTier(config.tier)
        zone = ZoneInfo(config.timezone)
        cases: list[dict[str, Any]] = []
        keys: list[dict[str, Any]] = []
        answer_spaces = self.response_model.answer_spaces()
        for index, utc_moment in enumerate(self._sample_utc_moments(config), start=1):
            case_id = f"CASE-{index:04d}"
            chart = self.chart_calculator.calculate(utc_moment)
            stable_hash = chart.engine_metadata.get("stable_feature_sha256")
            chart_hash = stable_hash if isinstance(stable_hash, str) else sha256_json(chart)
            local = utc_moment.astimezone(zone)
            canonical = tuple(self.response_model.oracle_responses(chart))
            responses = apply_noise(
                canonical,
                answer_spaces=answer_spaces,
                seed=generation_seed * 1_000_003 + index,
                tier=tier,
            )
            case = BlindCase(
                case_id=case_id,
                known_birth_year=local.year,
                known_birth_month=local.month,
                known_birth_day=local.day if config.universe == "known_date" else None,
                birthplace=config.birthplace,
                iana_timezone=config.timezone,
                responses=responses,
                candidate_universe=config.universe,
            )
            cases.append(case.model_dump(mode="json", exclude_none=True))
            keys.append(
                {
                    "case_id": case_id,
                    "true_local_datetime": local.isoformat(),
                    "true_utc": utc_moment.astimezone(UTC).isoformat().replace("+00:00", "Z"),
                    "true_local_date": local.date().isoformat(),
                    "true_state_id": f"TRUE-{chart_hash[:16].upper()}",
                    "true_chart_features_hash": chart_hash,
                }
            )
        blind_document = {
            "schema_version": "blind-synthetic-v1",
            "experiment_id": config.experiment_id,
            "generator": "frozen-chart-to-response-model",
            "model_id": self.response_model.model_id,
            "model_sha256": self.response_model.model_sha256,
            "question_bank_sha256": self.response_model.question_bank_sha256,
            "mapping_sha256": self.response_model.mapping_sha256,
            "noise_tier": tier.value,
            "candidate_universe": config.universe,
            "cases": cases,
        }
        blind_hash = sha256_bytes(canonical_json_bytes(blind_document))
        answer_key = {
            "schema_version": "answer-key-v1",
            "experiment_id": config.experiment_id,
            "blind_input_sha256": blind_hash,
            "generation_seed": generation_seed,
            "cases": keys,
        }
        return BlindSyntheticBundle(
            blind_document=blind_document,
            answer_key=answer_key,
            blind_input_sha256=blind_hash,
        )
