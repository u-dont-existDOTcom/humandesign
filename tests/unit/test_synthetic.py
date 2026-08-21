from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from hdmatch.config import SyntheticConfig
from hdmatch.evaluation import (
    BehavioralDifferenceMonthRequest,
    VerifiedBehavioralDifferenceBinding,
)
from hdmatch.schemas import Activation, BehavioralResponse, ChartFeatures
from hdmatch.synthetic import (
    NoiseTier,
    SyntheticGenerator,
    apply_noise,
    noise_parameters_payload,
)


class FakeChartCalculator:
    def calculate(self, utc_moment: datetime) -> ChartFeatures:
        activation = Activation(body="sun", side="personality", longitude=0, gate=25, line=1)
        return ChartFeatures(
            personality_utc=utc_moment,
            design_utc=utc_moment - timedelta(days=88),
            type="Projector",
            strategy="Wait for the Invitation",
            authority="Splenic",
            profile="1/3",
            definition="single",
            activations={"personality.sun": activation},
        )


class FakeModel:
    model_id = "MODEL-FAKE-V1"
    model_sha256 = "1" * 64
    mapping_sha256 = "2" * 64
    question_bank_sha256 = "3" * 64
    capability_metadata = {"behavioral_scoring": "fake"}

    def oracle_responses(self, chart: ChartFeatures) -> tuple[BehavioralResponse, ...]:
        return (
            BehavioralResponse(
                question_id="Q1",
                cluster_id="TYPE",
                answer=chart.type,
                behavioral_confidence=1,
                measurement_reliability=1,
            ),
        )

    def answer_spaces(self) -> dict[str, tuple[str, ...]]:
        return {"Q1": ("Projector", "Generator")}


class FakeModelBV2(FakeModel):
    model_id = "MODEL-B-DETAILED-V2-NEW"
    model_sha256 = "6" * 64
    mapping_sha256 = "4" * 64
    question_bank_sha256 = "7" * 64
    capability_metadata = {
        "behavioral_scoring": "fake-v2",
        "freeze_receipt_sha256": "5" * 64,
    }


def _difference_binding() -> VerifiedBehavioralDifferenceBinding:
    return VerifiedBehavioralDifferenceBinding(
        audit_file_sha256="1" * 64,
        audited_at_utc=datetime(2026, 1, 2, tzinfo=UTC),
        model_a_sha256="2" * 64,
        model_a_mapping_sha256="3" * 64,
        model_b_compiled_file_sha256="4" * 64,
        model_b_freeze_receipt_file_sha256="5" * 64,
        model_b_sha256="6" * 64,
        question_bank_sha256="7" * 64,
        candidate_cache_file_sha256="8" * 64,
        candidate_engine_fingerprint="9" * 64,
        candidate_universe_request=BehavioralDifferenceMonthRequest(
            year=2000,
            month=1,
            timezone_name="UTC",
        ),
        candidate_universe_sha256="a" * 64,
        candidate_state_count=2,
    )


def test_oracle_noise_is_identity() -> None:
    response = FakeModel().oracle_responses(FakeChartCalculator().calculate(datetime.now(UTC)))
    assert (
        apply_noise(
            response,
            answer_spaces=FakeModel().answer_spaces(),
            seed=7,
            tier=NoiseTier.ORACLE,
        )
        == response
    )


def test_generator_is_reproducible_and_blind() -> None:
    config = SyntheticConfig(
        experiment_id="test",
        seed=7,
        case_count=3,
        year_start=2000,
        year_end=2000,
    )
    generator = SyntheticGenerator(FakeChartCalculator(), FakeModel())
    first = generator.generate(config)
    second = generator.generate(config)
    assert first == second
    assert first.blind_input_sha256 == second.blind_input_sha256
    encoded = str(first.blind_document)
    assert "true_local_date" not in encoded
    assert "generation_seed" not in encoded
    assert all("known_birth_day" not in case for case in first.blind_document["cases"])
    assert first.blind_document["noise_parameters"] == noise_parameters_payload(NoiseTier.ORACLE)


def test_fixed_month_sampling_stays_inside_one_declared_month() -> None:
    config = SyntheticConfig(
        experiment_id="fixed-month",
        seed=11,
        case_count=100,
        year_start=2000,
        year_end=2000,
        month=2,
    )

    moments = SyntheticGenerator._sample_utc_moments(config)

    assert {moment.year for moment in moments} == {2000}
    assert {moment.month for moment in moments} == {2}


def test_fixed_month_rejects_multi_year_window() -> None:
    with pytest.raises(ValidationError, match="fixed synthetic month"):
        SyntheticConfig(
            experiment_id="invalid-fixed-month",
            seed=11,
            year_start=2000,
            year_end=2001,
            month=1,
        )


def test_v2_generator_requires_and_embeds_verified_difference_gate() -> None:
    config = SyntheticConfig(
        experiment_id="v2-gated",
        seed=7,
        case_count=1,
        year_start=2000,
        year_end=2000,
        month=1,
    )
    generator = SyntheticGenerator(FakeChartCalculator(), FakeModelBV2())

    with pytest.raises(ValueError, match="verified behavioral-difference gate"):
        generator.generate(config)

    binding = _difference_binding()
    bundle = generator.generate(config, model_b_v2_difference_gate=binding)

    assert bundle.blind_document["model_b_v2_difference_gate"] == binding.model_dump(
        mode="json"
    )


def test_v2_generator_rejects_stale_binding_before_chart_calculation() -> None:
    config = SyntheticConfig(
        experiment_id="v2-stale-gate",
        seed=7,
        case_count=1,
        year_start=2000,
        year_end=2000,
        month=1,
    )
    generator = SyntheticGenerator(FakeChartCalculator(), FakeModelBV2())
    stale = VerifiedBehavioralDifferenceBinding.model_validate(
        {
            **_difference_binding().model_dump(mode="json"),
            "model_b_sha256": "f" * 64,
        }
    )

    with pytest.raises(ValueError, match="model SHA is mismatched"):
        generator.generate(config, model_b_v2_difference_gate=stale)
