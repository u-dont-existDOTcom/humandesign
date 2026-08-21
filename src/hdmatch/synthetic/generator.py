"""Blind synthetic cases generated only from a declared frozen model."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.config import SyntheticConfig
from hdmatch.evaluation.behavioral_difference import VerifiedBehavioralDifferenceBinding
from hdmatch.schemas import BehavioralResponse, BlindCase, ChartFeatures
from hdmatch.synthetic.noise import NoiseTier, apply_noise, noise_parameters_payload
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

    @property
    def capability_metadata(self) -> Mapping[str, object]: ...

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
        if config.month is None:
            start = datetime(config.year_start, 1, 1, tzinfo=zone).astimezone(UTC)
            end = datetime(config.year_end + 1, 1, 1, tzinfo=zone).astimezone(UTC)
        else:
            start = datetime(config.year_start, config.month, 1, tzinfo=zone).astimezone(UTC)
            end_year = config.year_start + int(config.month == 12)
            end_month = 1 if config.month == 12 else config.month + 1
            end = datetime(end_year, end_month, 1, tzinfo=zone).astimezone(UTC)
        seconds = int((end - start).total_seconds())
        if seconds <= 0:
            raise ValueError("year_end must not precede year_start")
        rng = random.Random(config.seed)
        return tuple(
            start + timedelta(seconds=rng.randrange(seconds)) for _ in range(config.case_count)
        )

    def generate(
        self,
        config: SyntheticConfig,
        *,
        model_b_v2_difference_gate: VerifiedBehavioralDifferenceBinding | None = None,
    ) -> BlindSyntheticBundle:
        if config.seed is None:
            raise ValueError("synthetic generation requires a secret seed")
        is_v2 = self.response_model.model_id == "MODEL-B-DETAILED-V2-NEW"
        if is_v2 and model_b_v2_difference_gate is None:
            raise ValueError(
                "MODEL-B-DETAILED-V2-NEW generation requires a verified "
                "behavioral-difference gate"
            )
        if not is_v2 and model_b_v2_difference_gate is not None:
            raise ValueError("behavioral-difference gate is only valid for Model B V2")
        if model_b_v2_difference_gate is not None:
            self._validate_v2_difference_gate(config, model_b_v2_difference_gate)
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
            "model_capabilities": dict(self.response_model.capability_metadata),
            "noise_tier": tier.value,
            "noise_parameters": noise_parameters_payload(tier),
            "candidate_universe": config.universe,
            "cases": cases,
        }
        if model_b_v2_difference_gate is not None:
            blind_document["model_b_v2_difference_gate"] = (
                model_b_v2_difference_gate.model_dump(mode="json")
            )
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

    def _validate_v2_difference_gate(
        self,
        config: SyntheticConfig,
        binding: VerifiedBehavioralDifferenceBinding,
    ) -> None:
        """Reject a verified audit binding that is stale for this model or scope."""

        metadata = self.response_model.capability_metadata
        expected_fields: tuple[tuple[str, object, object], ...] = (
            ("model SHA", binding.model_b_sha256, self.response_model.model_sha256),
            (
                "compiled artifact SHA",
                binding.model_b_compiled_file_sha256,
                self.response_model.mapping_sha256,
            ),
            (
                "freeze receipt SHA",
                binding.model_b_freeze_receipt_file_sha256,
                metadata.get("freeze_receipt_sha256"),
            ),
            (
                "question-bank SHA",
                binding.question_bank_sha256,
                self.response_model.question_bank_sha256,
            ),
        )
        for label, recorded, current in expected_fields:
            if recorded != current:
                raise ValueError(f"V2 behavioral-difference gate {label} is mismatched")
        request = binding.candidate_universe_request
        if (
            config.year_start != request.year
            or config.year_end != request.year
            or config.month != request.month
            or config.timezone != request.timezone_name
        ):
            raise ValueError(
                "V2 synthetic generation must match the audited month/year/timezone"
            )
