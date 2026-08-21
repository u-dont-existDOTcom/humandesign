from datetime import UTC, datetime, timedelta

from hdmatch.config import SyntheticConfig
from hdmatch.schemas import Activation, BehavioralResponse, ChartFeatures
from hdmatch.synthetic import NoiseTier, SyntheticGenerator, apply_noise


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
    model_sha256 = "1" * 64
    mapping_sha256 = "2" * 64
    question_bank_sha256 = "3" * 64

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
