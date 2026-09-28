"""Frozen weighted association estimator and null diagnostics.

This module is an optional empirical-analysis component and requires NumPy and
SciPy.  It estimates the theory-neutral association only; it has no astrology
feature path.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, replace

import numpy as np
from scipy.stats import t as student_t

from .features import NUISANCE_COLUMN_NAMES, PairFeatures, deterministic_random_feature

RANK_TOLERANCE = 1e-10


class NotEstimable(ValueError):
    """Raised when the exact frozen analysis cannot be estimated."""


@dataclass(frozen=True, slots=True)
class AnalysisRow:
    """One complete, frozen pair and its normalized IPIP profile distance."""

    pair: PairFeatures
    outcome_distance: float

    def __post_init__(self) -> None:
        value = float(self.outcome_distance)
        if not math.isfinite(value) or not 0.0 <= value <= 1.0:
            raise ValueError("outcome_distance must be finite and in [0,1]")


@dataclass(frozen=True, slots=True)
class PrimaryFit:
    beta: float
    standard_error: float
    confidence_interval_95: tuple[float, float]
    t_statistic: float
    p_value_two_sided: float
    n_pairs: int
    n_networks: int
    degrees_of_freedom: int
    parameter_count: int
    retained_nuisance_columns: tuple[str, ...]
    weighted_residual_sum_squares: float
    x_variant: str


@dataclass(frozen=True, slots=True)
class WildBootstrapResult:
    observed: PrimaryFit
    draws: int
    exceedances: int
    p_value_one_sided: float
    seed: int


@dataclass(frozen=True, slots=True)
class _PreparedDesign:
    rows: tuple[AnalysisRow, ...]
    y: np.ndarray
    y_centered: np.ndarray
    nuisance_centered: np.ndarray
    x_centered: np.ndarray
    weights: np.ndarray
    networks: np.ndarray
    groups: np.ndarray
    retained_indices: tuple[int, ...]
    design: np.ndarray
    parameter_count: int


def _x_for_pair(pair: PairFeatures, variant: str) -> float:
    if variant == "center":
        return pair.center_gap_hours
    if variant == "lower":
        return pair.lower_gap_hours
    if variant == "upper":
        return pair.upper_gap_hours
    raise ValueError("x_variant must be center, lower, or upper")


def _within_center(
    values: np.ndarray,
    groups: np.ndarray,
    weights: np.ndarray,
) -> np.ndarray:
    centered = values.astype(np.float64, copy=True)
    for group in sorted(set(groups.tolist())):
        selected = groups == group
        group_weights = weights[selected]
        if values.ndim == 1:
            mean = np.average(values[selected], weights=group_weights)
        else:
            mean = np.average(values[selected, :], weights=group_weights, axis=0)
        centered[selected] -= mean
    return centered


def _retained_columns(values: np.ndarray, weights: np.ndarray) -> tuple[int, ...]:
    sqrt_weights = np.sqrt(weights)
    basis: list[np.ndarray] = []
    retained: list[int] = []
    for index in range(values.shape[1]):
        original = sqrt_weights * values[:, index]
        original_norm = float(np.linalg.norm(original))
        if not math.isfinite(original_norm) or original_norm == 0.0:
            continue
        residual = original.copy()
        for vector in basis:
            residual -= vector * float(vector @ residual)
        residual_norm = float(np.linalg.norm(residual))
        if residual_norm / original_norm <= RANK_TOLERANCE:
            continue
        basis.append(residual / residual_norm)
        retained.append(index)
    return tuple(retained)


def _prepare(
    rows: Sequence[AnalysisRow],
    *,
    x_variant: str,
    required_networks: int | None,
    outcome_values: Sequence[float] | None = None,
    x_values: Sequence[float] | None = None,
    nuisance_indices: tuple[int, ...] = tuple(range(len(NUISANCE_COLUMN_NAMES))),
) -> _PreparedDesign:
    if not rows:
        raise NotEstimable("no complete pairs")
    frozen = tuple(rows)
    pair_ids = [row.pair.pair_id for row in frozen]
    if len(pair_ids) != len(set(pair_ids)):
        raise NotEstimable("duplicate pair IDs")
    participant_ids = [participant for row in frozen for participant in row.pair.participant_ids]
    if len(participant_ids) != len(set(participant_ids)):
        raise NotEstimable("a participant appears in more than one pair")
    for row in frozen:
        if len(row.pair.nuisance_values) != len(NUISANCE_COLUMN_NAMES):
            raise NotEstimable("nuisance vector does not match the frozen column list")

    if len(set(nuisance_indices)) != len(nuisance_indices) or any(
        not 0 <= index < len(NUISANCE_COLUMN_NAMES) for index in nuisance_indices
    ):
        raise ValueError("nuisance_indices must be unique valid frozen-column indices")
    y_source = (
        [row.outcome_distance for row in frozen] if outcome_values is None else list(outcome_values)
    )
    x_source = (
        [_x_for_pair(row.pair, x_variant) for row in frozen] if x_values is None else list(x_values)
    )
    if len(y_source) != len(frozen) or len(x_source) != len(frozen):
        raise ValueError("custom outcome and exposure arrays must match the pair count")
    y = np.asarray(y_source, dtype=np.float64)
    all_nuisance = np.asarray([row.pair.nuisance_values for row in frozen], dtype=np.float64)
    nuisance = all_nuisance[:, nuisance_indices]
    x = np.asarray(x_source, dtype=np.float64)
    if (
        not np.all(np.isfinite(y))
        or not np.all(np.isfinite(nuisance))
        or not np.all(np.isfinite(x))
    ):
        raise NotEstimable("nonfinite model input")
    networks = np.asarray([row.pair.network_id for row in frozen], dtype=object)
    groups = np.asarray(
        [f"{row.pair.hospital_id}\0{row.pair.local_birth_date.isoformat()}" for row in frozen],
        dtype=object,
    )
    network_counts = Counter(networks.tolist())
    weights = np.asarray([1.0 / network_counts[value] for value in networks], dtype=np.float64)
    n_networks = len(network_counts)
    if required_networks is not None and n_networks != required_networks:
        raise NotEstimable(
            f"network count is {n_networks}; frozen full-cohort requirement is {required_networks}"
        )
    if n_networks < 2:
        raise NotEstimable("cluster inference requires at least two networks")

    y_centered = _within_center(y, groups, weights)
    nuisance_centered = _within_center(nuisance, groups, weights)
    x_centered = _within_center(x, groups, weights)
    retained_local = _retained_columns(nuisance_centered, weights)
    retained = tuple(nuisance_indices[index] for index in retained_local)
    nuisance_design = nuisance_centered[:, retained_local]
    if nuisance_design.ndim != 2:
        nuisance_design = nuisance_design.reshape(len(frozen), 0)

    combined = np.column_stack((nuisance_design, x_centered))
    retained_with_x = _retained_columns(combined, weights)
    if not retained_with_x or retained_with_x[-1] != combined.shape[1] - 1:
        raise NotEstimable("TN-001 is zero or collinear after frozen controls")
    if retained_with_x != tuple(range(combined.shape[1])):
        raise NotEstimable("internal rank selection changed after TN-001 was appended")

    n_groups = len(set(groups.tolist()))
    parameter_count = n_groups + len(retained) + 1
    if len(frozen) <= parameter_count:
        raise NotEstimable(
            f"N={len(frozen)} must exceed k={parameter_count} under the frozen model"
        )
    return _PreparedDesign(
        rows=frozen,
        y=y,
        y_centered=y_centered,
        nuisance_centered=nuisance_centered,
        x_centered=x_centered,
        weights=weights,
        networks=networks,
        groups=groups,
        retained_indices=retained,
        design=combined,
        parameter_count=parameter_count,
    )


def _fit_prepared(prepared: _PreparedDesign, y: np.ndarray, *, x_variant: str) -> PrimaryFit:
    y_centered = _within_center(y, prepared.groups, prepared.weights)
    design = prepared.design
    sqrt_weights = np.sqrt(prepared.weights)
    weighted_design = design * sqrt_weights[:, None]
    weighted_y = y_centered * sqrt_weights
    gram = weighted_design.T @ weighted_design
    try:
        gram_inverse = np.linalg.inv(gram)
        coefficients = gram_inverse @ (weighted_design.T @ weighted_y)
    except np.linalg.LinAlgError as exc:
        raise NotEstimable("weighted model matrix is numerically singular") from exc
    residuals = y_centered - design @ coefficients
    if not np.all(np.isfinite(coefficients)) or not np.all(np.isfinite(residuals)):
        raise NotEstimable("model fit is nonfinite")

    meat = np.zeros_like(gram)
    unique_networks = sorted(set(prepared.networks.tolist()))
    for network in unique_networks:
        selected = prepared.networks == network
        score = design[selected, :].T @ (prepared.weights[selected] * residuals[selected])
        meat += np.outer(score, score)
    n = len(prepared.rows)
    g = len(unique_networks)
    k = prepared.parameter_count
    cr1 = g / (g - 1) * (n - 1) / (n - k)
    covariance = cr1 * gram_inverse @ meat @ gram_inverse
    variance = float(covariance[-1, -1])
    if not math.isfinite(variance) or variance <= 0.0:
        raise NotEstimable("TN-001 cluster-robust variance is nonpositive or nonfinite")
    beta = float(coefficients[-1])
    standard_error = math.sqrt(variance)
    t_statistic = beta / standard_error
    df = g - 1
    critical = float(student_t.ppf(0.975, df))
    p_value = float(2.0 * student_t.sf(abs(t_statistic), df))
    if not all(
        math.isfinite(value) for value in (beta, standard_error, t_statistic, critical, p_value)
    ):
        raise NotEstimable("TN-001 inference is nonfinite")
    return PrimaryFit(
        beta=beta,
        standard_error=standard_error,
        confidence_interval_95=(beta - critical * standard_error, beta + critical * standard_error),
        t_statistic=t_statistic,
        p_value_two_sided=p_value,
        n_pairs=n,
        n_networks=g,
        degrees_of_freedom=df,
        parameter_count=k,
        retained_nuisance_columns=tuple(
            NUISANCE_COLUMN_NAMES[index] for index in prepared.retained_indices
        ),
        weighted_residual_sum_squares=float(np.sum(prepared.weights * residuals**2)),
        x_variant=x_variant,
    )


def fit_primary_association(
    rows: Sequence[AnalysisRow],
    *,
    x_variant: str = "center",
    required_networks: int | None = 20,
) -> PrimaryFit:
    """Fit the exact theory-neutral WLS slope with network-cluster CR1 inference."""

    prepared = _prepare(rows, x_variant=x_variant, required_networks=required_networks)
    return _fit_prepared(prepared, prepared.y, x_variant=x_variant)


def _restricted_fit(prepared: _PreparedDesign) -> tuple[np.ndarray, np.ndarray]:
    nuisance = prepared.design[:, :-1]
    if nuisance.shape[1] == 0:
        residual_centered = prepared.y_centered.copy()
        fitted_centered = np.zeros_like(prepared.y_centered)
    else:
        sqrt_weights = np.sqrt(prepared.weights)
        weighted = nuisance * sqrt_weights[:, None]
        try:
            coefficients = np.linalg.solve(
                weighted.T @ weighted,
                weighted.T @ (prepared.y_centered * sqrt_weights),
            )
        except np.linalg.LinAlgError as exc:
            raise NotEstimable("restricted model matrix is singular") from exc
        fitted_centered = nuisance @ coefficients
        residual_centered = prepared.y_centered - fitted_centered
    fitted = np.empty_like(prepared.y)
    for group in sorted(set(prepared.groups.tolist())):
        selected = prepared.groups == group
        group_mean = np.average(prepared.y[selected], weights=prepared.weights[selected])
        fitted[selected] = group_mean + fitted_centered[selected]
    if not np.all(np.isfinite(fitted)) or not np.all(np.isfinite(residual_centered)):
        raise NotEstimable("restricted fit is nonfinite")
    return fitted, residual_centered


def restricted_wild_cluster_bootstrap(
    rows: Sequence[AnalysisRow],
    *,
    draws: int = 99999,
    seed: int,
    required_networks: int | None = 20,
) -> WildBootstrapResult:
    """Run the frozen one-sided restricted wild cluster bootstrap-t."""

    if isinstance(draws, bool) or not isinstance(draws, int) or draws <= 0:
        raise ValueError("draws must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("seed must be a non-negative integer")
    prepared = _prepare(rows, x_variant="center", required_networks=required_networks)
    observed = _fit_prepared(prepared, prepared.y, x_variant="center")
    restricted_fitted, restricted_residuals = _restricted_fit(prepared)
    rng = np.random.Generator(np.random.PCG64(seed))
    networks = sorted(set(prepared.networks.tolist()))
    exceedances = 0
    for _ in range(draws):
        signs = {network: (-1.0 if int(rng.integers(0, 2)) == 0 else 1.0) for network in networks}
        pseudo = (
            restricted_fitted
            + np.asarray([signs[network] for network in prepared.networks], dtype=np.float64)
            * restricted_residuals
        )
        fit = _fit_prepared(prepared, pseudo, x_variant="center")
        if fit.t_statistic >= observed.t_statistic:
            exceedances += 1
    return WildBootstrapResult(
        observed=observed,
        draws=draws,
        exceedances=exceedances,
        p_value_one_sided=(1 + exceedances) / (draws + 1),
        seed=seed,
    )


def fit_gap_bound_sensitivities(
    rows: Sequence[AnalysisRow],
    *,
    required_networks: int | None = 20,
) -> tuple[PrimaryFit, PrimaryFit]:
    """Fit lower and upper uncertainty bounds on the original frozen pairs."""

    lower = fit_primary_association(
        rows,
        x_variant="lower",
        required_networks=required_networks,
    )
    upper = fit_primary_association(
        rows,
        x_variant="upper",
        required_networks=required_networks,
    )
    return lower, upper


def fit_random_feature_diagnostic(
    rows: Sequence[AnalysisRow],
    diagnostic_index: int,
    *,
    protocol_version: str,
    base_seed: int,
    required_networks: int | None = 20,
) -> PrimaryFit:
    """Replace TN-001 with one exact hash-defined random diagnostic feature."""

    x_values = [
        deterministic_random_feature(
            row.pair.pair_id,
            diagnostic_index,
            protocol_version=protocol_version,
            base_seed=base_seed,
        )
        for row in rows
    ]
    label = f"random_feature_{diagnostic_index}"
    prepared = _prepare(
        rows,
        x_variant=label,
        required_networks=required_networks,
        x_values=x_values,
    )
    return _fit_prepared(prepared, prepared.y, x_variant=label)


def fit_maternal_age_negative_control(
    rows: Sequence[AnalysisRow],
    *,
    required_networks: int | None = 20,
) -> PrimaryFit:
    """Use maternal-age difference as outcome and remove both maternal-age controls."""

    outcome_values = [row.pair.nuisance_values[9] for row in rows]
    nuisance_indices = tuple(
        index for index in range(len(NUISANCE_COLUMN_NAMES)) if index not in {8, 9}
    )
    label = "maternal_age_negative_control"
    prepared = _prepare(
        rows,
        x_variant=label,
        required_networks=required_networks,
        outcome_values=outcome_values,
        x_values=[row.pair.center_gap_hours for row in rows],
        nuisance_indices=nuisance_indices,
    )
    return _fit_prepared(prepared, prepared.y, x_variant=label)


def leave_one_network_out(
    rows: Sequence[AnalysisRow],
) -> tuple[PrimaryFit, ...]:
    """Return every fixed leave-one-network-out fit; never select a favorable subset."""

    networks = sorted({row.pair.network_id for row in rows})
    if len(networks) != 20:
        raise NotEstimable("the frozen LOO family requires exactly 20 source networks")
    results: list[PrimaryFit] = []
    for omitted in networks:
        subset = [row for row in rows if row.pair.network_id != omitted]
        fit = fit_primary_association(subset, required_networks=19)
        results.append(replace(fit, x_variant=f"center_leave_out_{omitted}"))
    return tuple(results)
