from pathlib import Path

from hdmatch.config import load_synthetic_config

ROOT = Path(__file__).parents[2]


def test_noise_smoke_configs_define_one_matched_public_cohort() -> None:
    paths = {
        "oracle": ROOT / "configs/synth_month_oracle_noise_smoke.yaml",
        "low": ROOT / "configs/synth_month_low_smoke.yaml",
        "medium": ROOT / "configs/synth_month_medium_smoke.yaml",
        "adversarial": ROOT / "configs/synth_month_adversarial_smoke.yaml",
    }
    configs = {tier: load_synthetic_config(path) for tier, path in paths.items()}

    for tier, config in configs.items():
        assert config.tier == tier
        assert config.seed is None
        assert config.case_count == 25

    cohort_fields = (
        "case_count",
        "universe",
        "year_start",
        "year_end",
        "timezone",
        "birthplace",
        "aggregation",
        "threshold_rubric_bits",
    )
    oracle = configs["oracle"]
    for config in configs.values():
        assert tuple(getattr(config, field) for field in cohort_fields) == tuple(
            getattr(oracle, field) for field in cohort_fields
        )
