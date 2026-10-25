"""Event-only, outcome-blind retrospective research scorer for Western directions.

Purpose: test WHETHER predicted age windows concentrate on independently dated,
documented events more often for true charts than precommitted decoy charts.
This cannot estimate event sensitivity, specificity, probability, life-event
incidence, or population predictive validity when event lists are incomplete.

No names, natal inputs, births, locations, private source texts, or real
individuals belong in this module. Astro-Databank C research sample is one
possible future source, but its outcome records have NOT been opened here.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from .western_forward_blind import (
    SOURCE_CANDIDATES,
    TENTATIVE_PILOT_PRIMARY,
    Interval,
    interval_intersection,
    label_permutation_null,
    measure_intervals,
    merged_intervals,
)
from .western_private_natal_bridge import EXPECTED_EPHEMERIS, METHOD_SPEC, SOURCE_FILES

DOMAIN_RULES = dict(TENTATIVE_PILOT_PRIMARY)
SOURCE_RULES = frozenset(DOMAIN_RULES)
VALID_DOMAINS = frozenset(DOMAIN_RULES.values())
ADULT = Interval(18.0, 65.0)


@dataclass(frozen=True)
class PositiveEvent:
    """Independently dated positive event as an age uncertainty interval.

    A year-only event spans roughly one year and is NOT a precise-day event.
    Uniform weighting inside the documented interval is an explicit
    exploratory date-uncertainty convention, not a measured probability.
    """

    domain: str
    age: Interval
    evidence_hash: str

    def __post_init__(self) -> None:
        if self.domain not in VALID_DOMAINS:
            raise ValueError("unsupported tentative modern occupational domain")
        if not (ADULT.start <= self.age.start < self.age.end <= ADULT.end):
            raise ValueError("outcome ages must lie in the declared adult domain")
        if len(self.evidence_hash) != 64 or any(
            c not in "0123456789abcdef" for c in self.evidence_hash
        ):
            raise ValueError("independent assessor evidence requires a SHA-256 digest")


@dataclass(frozen=True)
class OutcomeRecord:
    pseudonymous_case: str
    events: tuple[PositiveEvent, ...]
    independently_assessed_status: str = "POSITIVE_EVENTS_ONLY_NO_CERTIFIED_NEGATIVES"

    def __post_init__(self) -> None:
        if not self.pseudonymous_case or len(self.pseudonymous_case) > 80:
            raise ValueError("pseudonymous case ID is required")
        if self.independently_assessed_status != "POSITIVE_EVENTS_ONLY_NO_CERTIFIED_NEGATIVES":
            raise ValueError("cannot silently import a negative-event/completeness claim")
        refs = [event.evidence_hash for event in self.events]
        if len(set(refs)) != len(refs):
            raise ValueError("duplicate independent event-evidence reference")


@dataclass(frozen=True)
class ChartPrediction:
    """An already-generated, provenance-checked private prediction receipt."""

    pseudonymous_chart: str
    windows_by_domain: tuple[tuple[str, tuple[Interval, ...]], ...]
    prediction_receipt_sha256: str

    def __post_init__(self) -> None:
        if not self.pseudonymous_chart or len(self.pseudonymous_chart) > 80:
            raise ValueError("chart pseudonym required")
        if len(self.prediction_receipt_sha256) != 64 or any(
            c not in "0123456789abcdef" for c in self.prediction_receipt_sha256
        ):
            raise ValueError("prediction reference must have a SHA-256 hash")
        labels = [name for name, _ in self.windows_by_domain]
        if len(labels) != len(set(labels)) or any(x not in VALID_DOMAINS for x in labels):
            raise ValueError("duplicate or unsupported forecast domains")
        for _name, periods in self.windows_by_domain:
            if tuple(merged_intervals(periods, ADULT)) != periods:
                raise ValueError("chart forecast windows must be sorted disjoint adult intervals")


def chart_from_sanitized_receipt(
    container: dict[str, Any],
    *,
    pseudonymous_chart: str,
) -> ChartPrediction:
    """Use only candidate windows; never treat unresolved contacts as scores.

    An in-memory 'sealed' package has not independently proved the historical
    time it was created, consent, or isolation of the event answers.
    """
    if container.get("schema") != "PRIVATE_SOURCE_BOUND_WESTERN_DIAGNOSTIC_RECEIPT_V0":
        raise ValueError("wrong source-bound natal computation schema")
    if container.get("private_input_digest_scheme") != (
        "HMAC-SHA256_WITH_EXTERNAL_32_BYTE_OR_LONGER_KEY"
    ):
        raise ValueError("plain birth-date hash is not a privacy-safe commitment")
    if container.get("human_predictive_accuracy") != "UNTESTED":
        raise ValueError("invalid human-validation claim in natal receipt")
    if container.get("method_contract") != METHOD_SPEC:
        raise ValueError("method contract does not match declared Regiomontanian diagnostic")
    if container.get("source_rule_files_sha256") != SOURCE_FILES:
        raise ValueError("historical-source registry hashes do not match")
    if container.get("ephemeris_source_sha256") != EXPECTED_EPHEMERIS:
        raise ValueError("verified Swiss ephemeris fingerprints are missing/mismatched")
    if container.get("ephemeris_requested_and_returned_mode") != (
        "SWIEPH verified for all seven classical bodies"
    ):
        raise ValueError("Swiss Ephemeris fallback must not enter the human-study pilot")
    data = container.get("sealed_diagnostic_receipt")
    if not isinstance(data, dict) or data.get("schema") != (
        "WESTERN_DIRECTION_MODERN_DIAGNOSTIC_PREDICTION_RECEIPT_V0"
    ):
        raise ValueError("expected unmodified Western diagnostic prediction package")
    if data.get("historical_Argolus_or_Lilly_exactness") != "UNRESOLVED":
        raise ValueError("source completeness status was promoted without evidence")
    if data.get("all_eight_source_candidate_ids") != SOURCE_CANDIDATES:
        raise ValueError("source candidate families must be preserved unchanged")
    allowed = {
        "TENTATIVE_MODERN_PILOT_CANDIDATE_NOT_HUMAN_MODEL_FROZEN",
    }
    source_windows: dict[str, list[Interval]] = {domain: [] for domain in VALID_DOMAINS}
    seen = set()
    for contact in data.get("windows", []):
        if not isinstance(contact, dict):
            raise ValueError("invalid contact record")
        ident = contact.get("contact_key")
        if not isinstance(ident, str) or not ident or ident in seen:
            raise ValueError("invalid or duplicate source-contact key")
        seen.add(ident)
        rule_id = contact.get("source_rule_id")
        if rule_id not in SOURCE_CANDIDATES:
            raise ValueError("unexpected source rule, even if it is unresolved")
        time = contact.get("timing")
        if time is None:
            continue
        if rule_id not in SOURCE_RULES or contact.get("reason") not in allowed:
            raise ValueError("conditional or unresolved source contact cannot score")
        if not isinstance(time, dict) or set(time) != {"start", "end"}:
            raise ValueError("scoreable event age window has wrong schema")
        interval = Interval(time["start"], time["end"])
        source_windows[DOMAIN_RULES[rule_id]].append(interval)
    windows = tuple(
        (domain, merged_intervals(periods, ADULT))
        for domain, periods in sorted(source_windows.items())
    )
    # Receipt digest is a provenance pointer, not evidence of when a real
    # participant or the event assessor's data was actually frozen.
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return ChartPrediction(
        pseudonymous_chart=pseudonymous_chart,
        windows_by_domain=windows,
        prediction_receipt_sha256=hashlib.sha256(payload).hexdigest(),
    )


def _overlap_fraction(event: Interval, forecast: Sequence[Interval]) -> float:
    intersect = interval_intersection((event,), forecast)
    # Treat calendar-year-only event dates as an interval. All candidate
    # forecasts use the exact SAME within-interval averaging convention.
    return min(1.0, max(0.0, measure_intervals(intersect, ADULT) / (event.end - event.start)))


def positive_event_alignment(case: OutcomeRecord, chart: ChartPrediction) -> dict[str, Any]:
    """Event-conditional timing alignment. Absence of events is NOT a miss."""
    windows = dict(chart.windows_by_domain)
    weighted = 0.0
    partly_overlapping = 0
    per_event = []
    for event in case.events:
        weight = _overlap_fraction(event.age, windows.get(event.domain, ()))
        weighted += weight
        partly_overlapping += int(0.0 < weight < 1.0)
        per_event.append(
            {
                "domain": event.domain,
                "fraction_of_dated_event_interval_covered": weight,
                "original_event_precision_inferred_from_age_interval": False,
            }
        )
    observed = len(case.events)
    if observed == 0:
        return {
            "status": "NO_DOCUMENTED_POSITIVE_EVENTS_DO_NOT_ASSUME_NO_EVENTS",
            "observed_positive_event_count": 0,
            "event_conditional_alignment": None,
            "partly_overlapping_uncertain_event_intervals": 0,
        }
    return {
        "status": "EVENT_POSITIVE_ONLY_NO_NEGATIVE_EVENT_INFERENCE",
        "observed_positive_event_count": observed,
        "event_conditional_alignment": weighted / observed,
        "partly_overlapping_uncertain_event_intervals": partly_overlapping,
        "per_event": per_event,
    }


def build_positive_event_matrix(
    observations: Sequence[OutcomeRecord],
    forecasts: Sequence[ChartPrediction],
) -> dict[str, Any]:
    """Construct fixed alignment scores for each event-case against all charts.

    No true-chart identities are needed. Any no-documented-event profile must
    be identified explicitly and cannot be passed off as an event nonoccurrence.
    """
    n = len(observations)
    if n < 2 or len(forecasts) != n:
        raise ValueError("matched chart and outcome cohorts need n>=2")
    ids = [x.pseudonymous_case for x in observations]
    labels = [x.pseudonymous_chart for x in forecasts]
    if len(set(ids)) != n or len(set(labels)) != n:
        raise ValueError("each case and chart must have a unique blinded pseudonym")
    eventless = [x.pseudonymous_case for x in observations if not x.events]
    if eventless:
        return {
            "schema": "WESTERN_POSITIVE_EVENT_ONLY_N_BY_N_ALIGNMENT_V0",
            "status": "NOT_SCOREABLE_EVENTLESS_RECORDS_MUST_BE_REPORTED",
            "cohort_cases": n,
            "positive_event_cases": n - len(eventless),
            "no_documented_event_cases": eventless,
            "matrix": None,
            "human_predictive_validity": "UNTESTED",
        }
    matrix = []
    for case in observations:
        row = []
        for chart in forecasts:
            result = positive_event_alignment(case, chart)
            score = result["event_conditional_alignment"]
            if not isinstance(score, float) or not math.isfinite(score):
                raise ValueError("event-only matrix cannot contain unknown or invalid scores")
            row.append(score)
        matrix.append(row)
    return {
        "schema": "WESTERN_POSITIVE_EVENT_ONLY_N_BY_N_ALIGNMENT_V0",
        "status": "EXPLORATORY_EVENT_CONDITIONAL_MATRIX_NOT_PROSPECTIVE_HUMAN_VALIDATION",
        "cohort_cases": n,
        "positive_event_cases": n,
        "no_documented_event_cases": [],
        "chart_pseudonyms": labels,
        "outcome_pseudonyms": ids,
        "event_counts_by_case": [len(case.events) for case in observations],
        "score_definition": "Mean_fractional_age_interval_overlap_of_positive_events",
        "matrix": matrix,
        "missing_event_ascertainment_not_credited_as_true_negative": True,
        "no_demographic_or_temporal_exchangeability_proven": True,
        "human_predictive_validity": "UNTESTED",
    }


def exploratory_label_permutation(
    matrix: dict[str, Any],
    *,
    externally_unblinded_true_chart_indices: Sequence[int],
    seed: int = 20261025,
    monte_carlo_draws: int = 10000,
) -> dict[str, Any]:
    """Research null only; no claim that actual model/outcome hash was frozen."""
    if matrix.get("status") != (
        "EXPLORATORY_EVENT_CONDITIONAL_MATRIX_NOT_PROSPECTIVE_HUMAN_VALIDATION"
    ):
        raise ValueError("incomplete or unascertained outcome matrix cannot score")
    scores = matrix.get("matrix")
    if not isinstance(scores, list):
        raise ValueError("not a complete participant-by-chart score matrix")
    result = label_permutation_null(
        scores,
        externally_unblinded_true_chart_indices,
        seed=seed,
        monte_carlo_draws=monte_carlo_draws,
    )
    return {
        "status": "ASSUMPTION_CONDITIONAL_DEVELOPMENT_RESULT_NOT_VALIDATED_ASTROLOGY",
        "event_only_conditional_on_documented_events": True,
        "absent_events_and_true_negatives_never_inferred": True,
        "cohort_match_exchangeability_unproven": True,
        "temporal_selection_and_occupational_base_rates_unadjusted": True,
        "test": result,
    }
