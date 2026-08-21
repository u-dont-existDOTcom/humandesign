"""Blind recovery over exact candidate intervals with restoration traces."""

from __future__ import annotations

import calendar
import random
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import date
from hashlib import sha256
from pathlib import Path
from typing import Any

from hdmatch.evaluation.leakage import assert_no_blind_leakage, assert_no_prediction_leakage
from hdmatch.experiments.canonical import load_json_bytes, sha256_file
from hdmatch.model.mapping_library import MappingStatus
from hdmatch.schemas import BehavioralResponse, BlindCase, CandidateState, ScoredState
from hdmatch.search import AggregationMode, aggregate_dates, select_next_question

from .chart_adapter import ExactChartAdapter
from .symbolic_adapter import RuntimeSymbolicModel, candidate_prevalence
from .universe_cache import (
    MonthRequest,
    cache_path,
    ensure_month_caches,
    load_cached_universe,
)


@dataclass(frozen=True, slots=True)
class RecoverySettings:
    aggregation: AggregationMode
    threshold_rubric_bits: float
    workers: int = 1


def _score_states(
    states: Sequence[CandidateState],
    responses: Sequence[BehavioralResponse],
    model: RuntimeSymbolicModel,
    prevalence: Mapping[str, float],
) -> dict[str, ScoredState]:
    by_signature: dict[tuple[Any, ...], ScoredState] = {}
    scores: dict[str, ScoredState] = {}
    for state in states:
        signature = model.score_signature(state.chart_features)
        base = by_signature.get(signature)
        if base is None:
            base = model.score(state, responses, prevalence)
            by_signature[signature] = base
        scores[state.state_id] = base.model_copy(update={"state_id": state.state_id})
    return scores


def _ranked_payload(
    states: Sequence[CandidateState],
    responses: Sequence[BehavioralResponse],
    model: RuntimeSymbolicModel,
    prevalence: Mapping[str, float],
    settings: RecoverySettings,
    *,
    detailed: bool,
) -> list[dict[str, Any]]:
    scores = _score_states(states, responses, model, prevalence)
    ranked = aggregate_dates(
        states,
        scores,
        settings.aggregation,
        settings.threshold_rubric_bits,
    )
    state_by_id = {state.state_id: state for state in states}
    output: list[dict[str, Any]] = []
    for item in ranked:
        record: dict[str, Any] = {
            "local_date": item.local_date.isoformat(),
            "date_score": item.date_score,
            "date_rank": item.date_rank,
            "tied": item.tied,
        }
        if detailed:
            state = state_by_id[item.best_state.state_id]
            record.update(
                {
                    "duration_weighted_support": item.duration_weighted_support,
                    "best_state": {
                        **item.best_state.model_dump(mode="json"),
                        "start_utc": state.start_utc.isoformat().replace("+00:00", "Z"),
                        "end_utc": state.end_utc.isoformat().replace("+00:00", "Z"),
                        "interval_width_seconds": (state.end_utc - state.start_utc).total_seconds(),
                        "chart_features_hash": state.chart_features_hash,
                        "cross_engine_status": state.cross_engine_status,
                    },
                }
            )
        output.append(record)
    return output


def _group_responses(
    responses: Sequence[BehavioralResponse],
) -> dict[str, tuple[BehavioralResponse, ...]]:
    grouped: dict[str, list[BehavioralResponse]] = {}
    for response in responses:
        grouped.setdefault(response.cluster_id, []).append(response)
    return {
        cluster: tuple(sorted(items, key=lambda item: item.question_id))
        for cluster, items in sorted(grouped.items())
    }


def _response_label(responses: Iterable[BehavioralResponse]) -> str:
    return "|".join(
        f"{response.question_id}={response.answer}"
        for response in sorted(responses, key=lambda item: item.question_id)
    )


def _predicted_cluster_labels(
    states: Sequence[CandidateState],
    model: RuntimeSymbolicModel,
) -> dict[str, tuple[str, ...]]:
    result: dict[str, list[str]] = {}
    for state in states:
        predicted = _group_responses(tuple(model.oracle_responses(state.chart_features)))
        for cluster, responses in predicted.items():
            result.setdefault(cluster, []).append(_response_label(responses))
    return {cluster: tuple(labels) for cluster, labels in result.items()}


def _noise_match_probability(tier: str) -> float:
    return {
        "oracle": 1.0,
        "low": 0.94,
        "medium": 0.80,
        "adversarial": 0.60,
    }[tier]


def _likelihood_rows(labels: Sequence[str], match_probability: float) -> list[dict[str, float]]:
    alphabet = tuple(sorted(set(labels)))
    rows: list[dict[str, float]] = []
    for label in labels:
        if len(alphabet) == 1:
            rows.append({label: 1.0})
            continue
        mismatch = (1.0 - match_probability) / (len(alphabet) - 1)
        rows.append(
            {option: match_probability if option == label else mismatch for option in alphabet}
        )
    return rows


def _active_order(
    states: Sequence[CandidateState],
    grouped: Mapping[str, tuple[BehavioralResponse, ...]],
    model: RuntimeSymbolicModel,
    noise_tier: str,
) -> tuple[str, ...]:
    labels_by_cluster = _predicted_cluster_labels(states, model)
    remaining = set(grouped) & set(labels_by_cluster)
    weights = [max(0.0, (state.end_utc - state.start_utc).total_seconds()) for state in states]
    selected: list[str] = []
    match_probability = _noise_match_probability(noise_tier)
    while remaining:
        likelihoods = {
            cluster: _likelihood_rows(labels_by_cluster[cluster], match_probability)
            for cluster in remaining
        }
        utility = select_next_question(weights, likelihoods)
        if utility is None:
            break
        cluster = utility.question_id
        selected.append(cluster)
        remaining.remove(cluster)
        observed = _response_label(grouped[cluster])
        rows = likelihoods[cluster]
        updated = [
            weight * row.get(observed, 0.0) for weight, row in zip(weights, rows, strict=True)
        ]
        if sum(updated) > 0.0:
            weights = updated
    selected.extend(sorted(remaining))
    return tuple(selected)


def _restoration(
    order: Sequence[str],
    grouped: Mapping[str, tuple[BehavioralResponse, ...]],
    states: Sequence[CandidateState],
    model: RuntimeSymbolicModel,
    prevalence: Mapping[str, float],
    settings: RecoverySettings,
) -> list[dict[str, Any]]:
    restored: list[BehavioralResponse] = []
    curve: list[dict[str, Any]] = []
    for count, cluster in enumerate(order, start=1):
        restored.extend(grouped[cluster])
        curve.append(
            {
                "cluster_count": count,
                "cluster_id": cluster,
                "ranked_dates": _ranked_payload(
                    states,
                    restored,
                    model,
                    prevalence,
                    settings,
                    detailed=False,
                ),
            }
        )
    return curve


def _zero_date_ranking(year: int, month: int) -> list[dict[str, Any]]:
    day_count = calendar.monthrange(year, month)[1]
    midrank = (1 + day_count) / 2.0
    return [
        {
            "local_date": date(year, month, day).isoformat(),
            "date_score": 0.0,
            "date_rank": midrank,
            "tied": True,
        }
        for day in range(1, day_count + 1)
    ]


def recover_blind_file(
    blind_path: str | Path,
    *,
    model: RuntimeSymbolicModel,
    ephemeris_path: str | Path,
    cache_dir: str | Path,
    settings: RecoverySettings,
) -> dict[str, Any]:
    """Recover cases without accepting or discovering any answer-key path."""

    assert_no_blind_leakage(blind_path)
    raw = load_json_bytes(blind_path, require_canonical=True)
    if not isinstance(raw, dict) or raw.get("schema_version") != "blind-synthetic-v1":
        raise ValueError("unsupported blind input schema")
    raw_cases = raw.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise ValueError("blind input contains no cases")
    cases = tuple(BlindCase.model_validate(item) for item in raw_cases)
    bindings = {
        "model_sha256": model.model_sha256,
        "question_bank_sha256": model.question_bank_sha256,
        "mapping_sha256": model.mapping_sha256,
    }
    blind_model_id = raw.get("model_id", "MODEL-A-CORE-V1")
    if blind_model_id != model.model_id:
        raise ValueError("blind input model_id does not match decoder model")
    for field, expected in bindings.items():
        if raw.get(field) != expected:
            raise ValueError(f"blind input {field} does not match decoder artifact")
    blind_capabilities = raw.get("model_capabilities")
    if blind_capabilities is not None and blind_capabilities != dict(model.capability_metadata):
        raise ValueError("blind input model capabilities do not match decoder model")
    engine = ExactChartAdapter(ephemeris_path)
    requests = tuple(
        MonthRequest(case.known_birth_year, case.known_birth_month, case.iana_timezone)
        for case in cases
    )
    ensure_month_caches(
        requests,
        ephemeris_path=ephemeris_path,
        cache_dir=cache_dir,
        workers=settings.workers,
    )
    universes: dict[MonthRequest, tuple[CandidateState, ...]] = {}
    cache_hashes: dict[str, str] = {}
    for request in sorted(set(requests)):
        path = cache_path(cache_dir, request, engine.fingerprint)
        cached = load_cached_universe(path, request=request, engine_fingerprint=engine.fingerprint)
        universes[request] = cached.states
        cache_hashes[path.name] = cached.sha256

    blind_hash = sha256_file(blind_path)
    predictions: list[dict[str, Any]] = []
    noise_tier = str(raw.get("noise_tier"))
    for case, request in zip(cases, requests, strict=True):
        states = universes[request]
        if case.candidate_universe == "known_date":
            raise ValueError(
                "known-date exact clipping is not yet enabled; use the dedicated "
                "rectification command"
            )
        prevalence = candidate_prevalence(states, model.library)
        grouped = _group_responses(case.responses)
        clusters = list(grouped)
        public_seed = int.from_bytes(
            sha256(f"{blind_hash}:{case.case_id}:random-restoration".encode()).digest()[:8],
            "big",
        )
        random.Random(public_seed).shuffle(clusters)
        active = _active_order(states, grouped, model, noise_tier)
        final_ranking = _ranked_payload(
            states,
            case.responses,
            model,
            prevalence,
            settings,
            detailed=True,
        )
        aggregation_variants = {
            mode.value: {
                "ranked_dates": _ranked_payload(
                    states,
                    case.responses,
                    model,
                    prevalence,
                    replace(settings, aggregation=mode),
                    detailed=False,
                )
            }
            for mode in AggregationMode
            if mode is not settings.aggregation
        }
        leave_one_out = [
            {
                "cluster_id": cluster,
                "ranked_dates": _ranked_payload(
                    states,
                    tuple(
                        response
                        for name, responses in grouped.items()
                        if name != cluster
                        for response in responses
                    ),
                    model,
                    prevalence,
                    settings,
                    detailed=False,
                ),
            }
            for cluster in grouped
        ]
        predictions.append(
            {
                "case_id": case.case_id,
                "recovery_status": "completed",
                "ranked_dates": final_ranking,
                "aggregation_variants": aggregation_variants,
                "zero_cluster": {
                    "ranked_dates": _zero_date_ranking(
                        case.known_birth_year, case.known_birth_month
                    )
                },
                "random_restoration": _restoration(
                    clusters, grouped, states, model, prevalence, settings
                ),
                "active_restoration": _restoration(
                    active, grouped, states, model, prevalence, settings
                ),
                "leave_one_cluster_out": leave_one_out,
                "unresolved_mapping_ids": [
                    mapping.mapping_id
                    for mapping in model.library.mappings
                    if mapping.status is MappingStatus.UNRESOLVED
                    and any(
                        question_id in {r.question_id for r in case.responses}
                        for question_id in mapping.question_ids
                    )
                ],
                "prevalence_source": "duration-weighted declared candidate universe",
            }
        )
    result = {
        "schema_version": "predictions-v1",
        "experiment_id": raw["experiment_id"],
        "model_id": model.model_id,
        "blind_input_sha256": blind_hash,
        **bindings,
        "aggregation_rule": settings.aggregation.value,
        "score_semantics": "rubric-bits-not-probabilities",
        "model_capabilities": dict(model.capability_metadata),
        "candidate_cache_sha256": dict(sorted(cache_hashes.items())),
        "predictions": predictions,
    }
    assert_no_prediction_leakage(result)
    return result
