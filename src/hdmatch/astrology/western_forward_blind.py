"""Engineering scaffolding for a SEPARATELY NAMED modern Western pilot.

This is not an authenticated complete Lilly/Argolus/Regiomontanus prediction
model and does not claim any human predictive validation. Source candidates
remain versioned, including those whose source conditions are unresolved.
The actual participant intake, eligible opportunity and event evidence must
be independently frozen before outcomes are scored.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from typing import Any

DIAGNOSTIC_NAME = "WESTERN_PRIMARY_DIRECTIONS_MODERN_DIAGNOSTIC_V0"
SOURCE_CANDIDATES = (
    "L1647-MC-JUP-BODY",
    "L1647-MC-SAT-BODY",
    "L1647-ASC-JUP-BODY",
    "L1647-ASC-MARS-BODY",
    "L1647-MC-JUP-SOFT",
    "L1647-MC-SAT-HARD",
    "L1647-ASC-JUP-SOFT",
    "L1647-ASC-MARS-HARD",
)
# Narrow observable modern hypotheses. These are researcher-inferred and
# require independently ascertained formal responsibility at risk/gained.
TENTATIVE_PILOT_PRIMARY = {
    "L1647-MC-JUP-BODY": "documented_formal_role_gain",
    "L1647-MC-SAT-BODY": "documented_involuntary_role_loss",
}
NOT_READY_REASONS = {
    "L1647-ASC-JUP-BODY": "material value threshold and alternatives unresolved",
    "L1647-ASC-MARS-BODY": "broad controversy alternatives to formal case unresolved",
    "L1647-MC-JUP-SOFT": "Lilly requires natal strong Jupiter; no full verdict",
    "L1647-MC-SAT-HARD": "separate aspects and eligible office context unresolved",
    "L1647-ASC-JUP-SOFT": "benefit outcome and materiality threshold unresolved",
    "L1647-ASC-MARS-HARD": "broad adversarial alternatives to filing unresolved",
}


@dataclass(frozen=True)
class Interval:
    start: float
    end: float

    def __post_init__(self) -> None:
        if not all(math.isfinite(x) for x in (self.start, self.end)):
            raise ValueError("interval endpoints must be finite")
        if not self.start < self.end:
            raise ValueError("half-open interval must have positive length")


@dataclass(frozen=True)
class Contact:
    key: str
    rule_id: str
    symbolic_age_years: float

    def __post_init__(self) -> None:
        if self.rule_id not in SOURCE_CANDIDATES:
            raise ValueError("unknown historical-source candidate identifier")
        if not self.key or not math.isfinite(self.symbolic_age_years):
            raise ValueError("contact identity and finite age required")


@dataclass(frozen=True)
class WindowEnvelope:
    contact_key: str
    source_rule_id: str
    timing: Interval | None
    possible_range_for_review: Interval | None
    sampled_birth_minute_offsets: tuple[int, ...]
    reason: str
    historical_model_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.timing is None:
            payload["timing"] = None
        return payload


def canonical(obj: object) -> bytes:
    return (
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    ).encode("utf-8")


def merged_intervals(raw: Sequence[Interval], domain: Interval) -> tuple[Interval, ...]:
    pieces = sorted((max(v.start, domain.start), min(v.end, domain.end)) for v in raw)
    result: list[list[float]] = []
    for a, b in pieces:
        if b <= a:
            continue
        if result and a <= result[-1][1]:
            result[-1][1] = max(b, result[-1][1])
        else:
            result.append([a, b])
    return tuple(Interval(a, b) for a, b in result)


def measure_intervals(windows: Sequence[Interval], domain: Interval) -> float:
    return sum(v.end - v.start for v in merged_intervals(windows, domain))


def contact_uncertainty_envelopes(
    minute_samples: dict[int, Sequence[Contact]],
    *,
    half_window_years: float = 0.5,
    domain: Interval | None = None,
) -> tuple[WindowEnvelope, ...]:
    """Report ALL contact identities; never select a favorable birth minute.

    Sampling every permitted integer minute produces a *discrete-grid* timing
    envelope, NOT a certified bound over a continuous uncertainty interval.
    If a contact disappears at a sampled minute, preserve it as unscoreable.
    """
    domain = domain or Interval(18.0, 65.0)
    if not minute_samples or 0 not in minute_samples:
        raise ValueError("birth-time uncertainty samples must include minute offset zero")
    offsets = tuple(sorted(minute_samples))
    if offsets != tuple(range(offsets[0], offsets[-1] + 1)):
        raise ValueError("use complete one-minute-offset grid; no cherry-picked times")
    if offsets[0] != -offsets[-1]:
        raise ValueError("birth-time grid must be symmetric around recorded time")
    if not math.isfinite(half_window_years) or half_window_years <= 0:
        raise ValueError("positive finite timing tolerance required")
    registry: dict[str, dict[int, Contact]] = {}
    for offset, contacts in minute_samples.items():
        keys_seen = set()
        for item in contacts:
            if item.key in keys_seen:
                raise ValueError("duplicate candidate at one birth-time offset")
            keys_seen.add(item.key)
            registry.setdefault(item.key, {})[offset] = item
    result = []
    for key, appearances in sorted(registry.items()):
        kinds = {v.rule_id for v in appearances.values()}
        if len(kinds) != 1:
            raise ValueError("same contact identity changed source rule across minutes")
        rule_id = next(iter(kinds))
        complete = len(appearances) == len(offsets)
        ages = [v.symbolic_age_years for v in appearances.values()]
        lo = max(domain.start, min(ages) - half_window_years)
        hi = min(domain.end, max(ages) + half_window_years)
        span = Interval(lo, hi) if hi > lo else None
        if not complete:
            reason = "CONTACT_DISAPPEARS_FOR_SOME_PLAUSIBLE_BIRTHTIMES"
        elif span is None:
            reason = "CONTACT_OUTSIDE_OBSERVATION_INTERVAL"
        elif rule_id not in TENTATIVE_PILOT_PRIMARY:
            reason = "UNSCORED_HISTORICAL_OR_MODERN_OUTCOME_CONDITION"
        else:
            reason = "TENTATIVE_MODERN_PILOT_CANDIDATE_NOT_HUMAN_MODEL_FROZEN"
        result.append(
            WindowEnvelope(
                contact_key=key,
                source_rule_id=rule_id,
                # Only a complete, tentative modern endpoint exposes a usable
                # timing window. Missing-offset/conditional rules are NOT scored.
                timing=span if complete and rule_id in TENTATIVE_PILOT_PRIMARY else None,
                possible_range_for_review=span,
                sampled_birth_minute_offsets=offsets,
                reason=reason,
            )
        )
    return tuple(result)


def interval_intersection(a: Sequence[Interval], b: Sequence[Interval]) -> tuple[Interval, ...]:
    """Intersect two unions of half-open interval sets with no duplication."""
    if not a or not b:
        return ()
    limit = Interval(
        min(v.start for v in (*a, *b)),
        max(v.end for v in (*a, *b)),
    )
    x = merged_intervals(a, limit)
    y = merged_intervals(b, limit)
    out: list[Interval] = []
    i = j = 0
    while i < len(x) and j < len(y):
        start, end = max(x[i].start, y[j].start), min(x[i].end, y[j].end)
        if start < end:
            out.append(Interval(start, end))
        if x[i].end <= y[j].end:
            i += 1
        else:
            j += 1
    return tuple(out)


def eligible_exposure(
    prediction: Sequence[Interval],
    opportunity: Sequence[Interval],
    independently_ascertained: Sequence[Interval],
    *,
    adult_domain: Interval | None = None,
) -> dict[str, float | str]:
    """Report separately eligible and predicted years, NOT calibrated probabilities.

    Occupational opportunity/ascertainment cannot be recovered from the
    direction alone; those blinded records must come from independent coding.
    """
    adult_domain = adult_domain or Interval(18.0, 65.0)
    opportunity_intervals = merged_intervals(opportunity, adult_domain)
    ascertainment = merged_intervals(independently_ascertained, adult_domain)
    assessed = interval_intersection(opportunity_intervals, ascertainment)
    eligible = measure_intervals(assessed, adult_domain)
    prediction_with_assessment = interval_intersection(
        merged_intervals(prediction, adult_domain),
        assessed,
    )
    covered = measure_intervals(prediction_with_assessment, adult_domain)
    return {
        "assessed_eligible_years": eligible,
        "direction_exposure_years": covered,
        "unexposed_eligible_years": eligible - covered,
        "fraction_of_eligible_years_exposed": (covered / eligible if eligible else 0.0),
        "status": "EXPOSURE_ONLY_NOT_EVENT_PROBABILITY" if eligible else "UNASCERTAINED",
    }


def label_permutation_null(
    chart_scores: Sequence[Sequence[float]],
    true_chart_indices: Sequence[int],
    *,
    seed: int = 20261025,
    monte_carlo_draws: int = 10_000,
) -> dict[str, Any]:
    """One-to-one chart-label null on an ALREADY frozen N×N score matrix.

    Scores are externally defined, and this algorithm CANNOT validate that
    they were frozen before outcomes. For n<=8 enumerate every permutation;
    for n>=9 use a published-seed randomized null with +1 Monte-Carlo rule.
    Exchangeability under the chosen participant strata must be justified.
    """
    n = len(chart_scores)
    if n < 2:
        raise ValueError("need >=2 independently held-out human/chart labels")
    if len(true_chart_indices) != n or sorted(true_chart_indices) != list(range(n)):
        raise ValueError("true labels must form a complete one-to-one permutation")
    for row in chart_scores:
        if len(row) != n or any(not math.isfinite(v) for v in row):
            raise ValueError("full finite participant-by-chart compatibility matrix required")
    if not isinstance(seed, int) or monte_carlo_draws < 100:
        raise ValueError("frozen integer seed and adequate Monte Carlo samples required")
    observed = sum(chart_scores[i][true_chart_indices[i]] for i in range(n))

    if n <= 8:
        null_stats = (
            sum(chart_scores[i][perm[i]] for i in range(n))
            for perm in itertools.permutations(range(n))
        )
        extreme = total = 0
        for statistic in null_stats:
            total += 1
            extreme += statistic >= observed - 1e-10
        p = extreme / total
        sampling = "EXACT_N_FACTORIAL_LABEL_PERMUTATION"
    else:
        rng = random.Random(seed)
        total = monte_carlo_draws
        extreme = 1
        for _ in range(total):
            order = list(range(n))
            rng.shuffle(order)
            statistic = sum(chart_scores[i][order[i]] for i in range(n))
            extreme += statistic >= observed - 1e-10
        p = extreme / (total + 1)
        sampling = "FIXED_SEED_MONTE_CARLO_WITH_ADD_ONE_CORRECTION"
    return {
        "observed_diagonal_sum": observed,
        "permutation_null_probability_greater_or_equal": p,
        "null_method": sampling,
        "null_assignments_examined": total,
        "matrix_size": n,
        "frozen_seed": seed,
        "warning": (
            "Null is valid only if exchangeability, source rules, scoring, "
            "and blinding were prospectively established"
        ),
    }


def sealed_prediction_receipt(
    *,
    pseudonymous_participant_id: str,
    birth_input_sha256: str,
    chart_features_sha256: str,
    calculation_code_sha256: str,
    rules_sha256: str,
    birth_time_quality: str,
    windows: Sequence[WindowEnvelope],
    comparison_design_sha256: str,
) -> dict[str, Any]:
    """Create a commitment without storing private birth inputs or outcomes.

    The tool returns bytes/hash material for an EXTERNAL, write-once
    authorized storage system. It neither freezes a human study automatically
    nor certifies independently sourced birth data.
    """
    if not pseudonymous_participant_id or len(pseudonymous_participant_id) > 80:
        raise ValueError("use nonblank short pseudonym only")
    if birth_time_quality not in (
        "certified_minute",
        "family_recalled",
        "documented_uncertain",
        "unknown_or_rectified",
    ):
        raise ValueError("undeclared birth time quality")
    proofs = (
        birth_input_sha256,
        chart_features_sha256,
        calculation_code_sha256,
        rules_sha256,
        comparison_design_sha256,
    )
    if any(len(v) != 64 or any(ch not in "0123456789abcdef" for ch in v) for v in proofs):
        raise ValueError("all commitments must be lowercase SHA-256 hex digests")
    if len({w.contact_key for w in windows}) != len(windows):
        raise ValueError("cannot duplicate exposure to manufacture predictions")
    package = {
        "schema": "WESTERN_DIRECTION_MODERN_DIAGNOSTIC_PREDICTION_RECEIPT_V0",
        "pilot_stage": "ENGINEERING_ARTIFACT_ONLY_NOT_HUMAN_TRIAL_FROZEN",
        "pseudonymous_participant_id": pseudonymous_participant_id,
        "birth_input_sha256": birth_input_sha256,
        "chart_features_sha256": chart_features_sha256,
        "calculation_code_sha256": calculation_code_sha256,
        "rules_sha256": rules_sha256,
        "comparison_design_sha256": comparison_design_sha256,
        "birth_time_quality": birth_time_quality,
        "all_eight_source_candidate_ids": SOURCE_CANDIDATES,
        "two_tentative_modern_domains": TENTATIVE_PILOT_PRIMARY,
        "other_source_candidate_statuses": NOT_READY_REASONS,
        "windows": [v.to_dict() for v in sorted(windows, key=lambda w: w.contact_key)],
        "human_outcomes": "NOT_COLLECTED_IN_THIS_RECEIPT",
        "historical_Argolus_or_Lilly_exactness": "UNRESOLVED",
        "human_predictive_accuracy": "UNTESTED",
    }
    package["commitment_sha256"] = hashlib.sha256(canonical(package)).hexdigest()
    return package
