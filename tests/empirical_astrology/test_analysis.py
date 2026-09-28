from __future__ import annotations

import hashlib
from dataclasses import replace
from datetime import date

import numpy as np
import pytest

import hdmatch.empirical_astrology.analysis as analysis_module
from hdmatch.empirical_astrology.analysis import (
    AnalysisRow,
    NotEstimable,
    PrimaryFit,
    fit_diagnostic_family,
    fit_gap_bound_sensitivities,
    fit_maternal_age_negative_control,
    fit_primary_association,
    fit_random_feature_diagnostic,
    restricted_wild_cluster_bootstrap,
)
from hdmatch.empirical_astrology.features import PairFeatures


def _rows(
    *,
    constant_within_group_x: bool = False,
    network_count: int = 4,
) -> list[AnalysisRow]:
    rows: list[AnalysisRow] = []
    for network_index in range(network_count):
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
    lower, upper = fit_gap_bound_sensitivities(_rows(), required_networks=4).require_all()
    assert lower.n_pairs == upper.n_pairs == 40
    assert lower.x_variant == "lower"
    assert upper.x_variant == "upper"


def test_gap_sensitivity_ledger_attempts_upper_after_lower_failure() -> None:
    rows = [replace(row, pair=replace(row.pair, lower_gap_hours=1.0)) for row in _rows()]
    ledger = fit_gap_bound_sensitivities(rows, required_networks=4)
    assert [attempt.label for attempt in ledger.attempts] == ["lower", "upper"]
    assert ledger.attempts[0].fit is None
    assert ledger.attempts[0].error is not None
    assert ledger.attempts[1].succeeded is True
    with pytest.raises(NotEstimable, match="lower"):
        ledger.require_all()


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


def test_diagnostic_ledger_retains_all_twenty_one_attempts() -> None:
    ledger = fit_diagnostic_family(
        _rows(),
        protocol_version="same-hospital-personality-protocol-v1b-20260928",
        base_seed=20260928,
        required_networks=4,
    )
    assert len(ledger.attempts) == 21
    assert [attempt.label for attempt in ledger.attempts[:2]] == [
        "random_feature_1",
        "random_feature_2",
    ]
    assert ledger.attempts[-1].label == "maternal_age_negative_control"


def _near_collinear_rows(epsilon: float) -> list[AnalysisRow]:
    rng = np.random.Generator(np.random.PCG64(1234))
    count = 20 * 20
    z = rng.standard_normal(count)
    noise = rng.standard_normal(count)
    values = np.tile(np.linspace(0.1, 2.9, 20), 20)
    rows: list[AnalysisRow] = []
    for index, x_value in enumerate(values):
        network_index = index // 20
        row_index = index % 20
        first = f"NC{network_index}_{row_index}_A"
        second = f"NC{network_index}_{row_index}_B"
        pair_id = hashlib.sha256(f"{first}\0{second}".encode()).hexdigest()
        nuisance = (float(x_value + epsilon * z[index]),) + (0.0,) * 13
        pair = PairFeatures(
            pair_id=pair_id,
            participant_ids=(first, second),
            network_id=f"N{network_index:02d}",
            hospital_id=f"H{network_index:02d}",
            local_birth_date=date(2000, 1, network_index + 1),
            center_gap_hours=float(x_value),
            lower_gap_hours=float(x_value),
            upper_gap_hours=float(x_value),
            nuisance_values=nuisance,
        )
        outcome = float(0.2 + 0.03 * x_value + 0.003 * epsilon * noise[index])
        rows.append(AnalysisRow(pair=pair, outcome_distance=outcome))
    return rows


def _explicit_fixed_effect_reference(rows: list[AnalysisRow]) -> tuple[float, float]:
    networks = sorted({row.pair.network_id for row in rows})
    groups = sorted({row.pair.hospital_date_group for row in rows})
    design = np.zeros((len(rows), len(groups) + 2), dtype=np.float64)
    outcomes = np.asarray([row.outcome_distance for row in rows], dtype=np.float64)
    weights = np.asarray(
        [
            1.0 / sum(candidate.pair.network_id == row.pair.network_id for candidate in rows)
            for row in rows
        ],
        dtype=np.float64,
    )
    for row_index, row in enumerate(rows):
        design[row_index, groups.index(row.pair.hospital_date_group)] = 1.0
        design[row_index, -2] = row.pair.nuisance_values[0]
        design[row_index, -1] = row.pair.center_gap_hours
    weighted = design * np.sqrt(weights)[:, None]
    weighted_y = outcomes * np.sqrt(weights)
    q_matrix, r_matrix = np.linalg.qr(weighted, mode="reduced")
    coefficients = np.linalg.solve(r_matrix, q_matrix.T @ weighted_y)
    residuals = outcomes - design @ coefficients
    covariance_core = np.zeros((design.shape[1], design.shape[1]))
    for network in networks:
        selected = np.asarray([row.pair.network_id == network for row in rows])
        score = design[selected].T @ (weights[selected] * residuals[selected])
        influence = np.linalg.solve(r_matrix, np.linalg.solve(r_matrix.T, score))
        covariance_core += np.outer(influence, influence)
    n_rows = len(rows)
    n_networks = len(networks)
    parameter_count = len(groups) + 2
    covariance = (
        n_networks / (n_networks - 1) * (n_rows - 1) / (n_rows - parameter_count) * covariance_core
    )
    return float(coefficients[-1]), float(np.sqrt(covariance[-1, -1]))


def test_near_collinear_fit_matches_explicit_fixed_effect_qr() -> None:
    rows = _near_collinear_rows(1e-7)
    fit = fit_primary_association(rows, required_networks=20)
    reference_beta, reference_se = _explicit_fixed_effect_reference(rows)
    assert fit.beta == pytest.approx(reference_beta, rel=1e-8, abs=1e-10)
    assert fit.standard_error == pytest.approx(reference_se, rel=1e-6, abs=1e-10)
    assert fit.weighted_residual_sum_squares < 1e-14


def test_leave_one_network_out_retains_all_attempts_after_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rows = _rows(network_count=20)
    original = analysis_module.fit_primary_association

    def fail_one(
        subset: list[AnalysisRow],
        *,
        x_variant: str = "center",
        required_networks: int | None = 20,
    ) -> PrimaryFit:
        networks = {row.pair.network_id for row in subset}
        if "N7" not in networks:
            raise NotEstimable("synthetic omitted-network failure")
        return original(
            subset,
            x_variant=x_variant,
            required_networks=required_networks,
        )

    monkeypatch.setattr(analysis_module, "fit_primary_association", fail_one)
    ledger = analysis_module.leave_one_network_out(rows)
    assert len(ledger.attempts) == 20
    assert sum(not attempt.succeeded for attempt in ledger.attempts) == 1
    assert ledger.attempts[-1].label == "center_leave_out_N9"
