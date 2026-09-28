from __future__ import annotations

import hashlib
from dataclasses import replace
from datetime import date

import pytest

from hdmatch.empirical_astrology.analysis import (
    AnalysisRow,
    NotEstimable,
    fit_gap_bound_sensitivities,
    fit_maternal_age_negative_control,
    fit_primary_association,
    fit_random_feature_diagnostic,
    restricted_wild_cluster_bootstrap,
)
from hdmatch.empirical_astrology.features import PairFeatures


def _rows(*, constant_within_group_x: bool = False) -> list[AnalysisRow]:
    rows: list[AnalysisRow] = []
    for network_index in range(4):
        for row_index in range(10):
            x = 1.0 if constant_within_group_x else 0.1 + 0.25 * row_index
            residual = ((row_index % 3) - 1) * 0.004 * (network_index + 1)
            outcome = 0.25 + 0.04 * x + residual
            first = f"P{network_index}_{row_index}_A"
            second = f"P{network_index}_{row_index}_B"
            pair_id = hashlib.sha256(f"{first}\0{second}".encode()).hexdigest()
            pair = PairFeatures(
                pair_id=pair_id,
                participant_ids=(first, second),
                network_id=f"N{network_index}",
                hospital_id=f"H{network_index}",
                local_birth_date=date(2000, 1, network_index + 1),
                center_gap_hours=x,
                lower_gap_hours=max(0.0, x - 0.01),
                upper_gap_hours=x + 0.01,
                nuisance_values=(0.0,) * 14,
            )
            rows.append(AnalysisRow(pair=pair, outcome_distance=outcome))
    return rows


def test_primary_fit_recovers_positive_theory_neutral_slope() -> None:
    fit = fit_primary_association(_rows(), required_networks=4)
    assert fit.n_pairs == 40
    assert fit.n_networks == 4
    assert fit.degrees_of_freedom == 3
    assert fit.parameter_count == 5
    assert fit.beta == pytest.approx(0.04, abs=0.01)
    assert fit.retained_nuisance_columns == ()


def test_gap_sensitivities_retain_original_pairs() -> None:
    lower, upper = fit_gap_bound_sensitivities(_rows(), required_networks=4)
    assert lower.n_pairs == upper.n_pairs == 40
    assert lower.x_variant == "lower"
    assert upper.x_variant == "upper"


def test_rank_deficient_exposure_fails_closed() -> None:
    with pytest.raises(NotEstimable, match="zero or collinear"):
        fit_primary_association(_rows(constant_within_group_x=True), required_networks=4)


def test_restricted_bootstrap_is_seed_reproducible() -> None:
    first = restricted_wild_cluster_bootstrap(_rows(), draws=31, seed=20260929, required_networks=4)
    second = restricted_wild_cluster_bootstrap(
        _rows(), draws=31, seed=20260929, required_networks=4
    )
    assert first == second
    assert first.draws == 31
    assert 0.0 < first.p_value_one_sided <= 1.0


def test_random_and_maternal_age_diagnostics_use_frozen_substitutions() -> None:
    rows = _rows()
    random_fit = fit_random_feature_diagnostic(
        rows,
        1,
        protocol_version="same-hospital-personality-protocol-v1b-20260928",
        base_seed=20260928,
        required_networks=4,
    )
    assert random_fit.x_variant == "random_feature_1"

    maternal_rows: list[AnalysisRow] = []
    for index, row in enumerate(rows):
        nuisance = list(row.pair.nuisance_values)
        nuisance[8] = 30.0 + index / 100.0
        nuisance[9] = 2.0 + 0.3 * row.pair.center_gap_hours + (index % 3) * 0.01
        maternal_rows.append(replace(row, pair=replace(row.pair, nuisance_values=tuple(nuisance))))
    maternal_fit = fit_maternal_age_negative_control(maternal_rows, required_networks=4)
    assert maternal_fit.x_variant == "maternal_age_negative_control"
    assert not any("maternal_age" in name for name in maternal_fit.retained_nuisance_columns)
