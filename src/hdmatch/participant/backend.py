"""Concrete AstroHD backend for participant prediction, ranking, and question selection."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_file
from hdmatch.questionnaire import Question, load_question_bank
from hdmatch.runtime.chart_adapter import ExactChartAdapter
from hdmatch.runtime.symbolic_adapter import FrozenSymbolicModel, candidate_prevalence
from hdmatch.runtime.universe_cache import (
    MonthRequest,
    cache_path,
    ensure_month_caches,
    load_cached_universe,
)
from hdmatch.schemas import BehavioralResponse, CandidateState, ScoredState
from hdmatch.search import (
    AggregationMode,
    QuestionUtility,
    aggregate_dates,
    local_month_utc_bounds,
    select_next_question,
)

from .models import (
    PredictionDimension,
    PredictionFreeze,
    RankScope,
    RankingSnapshot,
    ResolvedBirth,
    SessionMode,
)


class UnsupportedRankScopeError(RuntimeError):
    """Raised when a requested candidate universe has no reusable production backend."""


class FrozenRuntimeMismatchError(RuntimeError):
    """Raised when an in-progress session meets a different runtime bundle."""


@dataclass(frozen=True, slots=True)
class DiscriminationDiagnostics:
    candidate_state_count: int
    top_state_tie_count: int
    top_margin_rubric_bits: float


@dataclass(frozen=True, slots=True)
class SelectedQuestion:
    question: Question
    utility: QuestionUtility


@dataclass(frozen=True, slots=True)
class _RankedState:
    state: CandidateState
    score: ScoredState
    rank: float


class AstroHDParticipantBackend:
    """Bridge the frozen symbolic model to exact candidate-state ranking."""

    def __init__(
        self,
        *,
        ephemeris_path: str,
        mapping_path: str,
        question_bank_path: str,
        candidate_cache_dir: str | None = None,
        code_commit: str = "unknown",
    ) -> None:
        self.ephemeris_path = ephemeris_path
        self.candidate_cache_dir = candidate_cache_dir
        self.chart_engine = ExactChartAdapter(ephemeris_path)
        self.model = FrozenSymbolicModel(mapping_path)
        self.question_bank = load_question_bank(question_bank_path)
        self.code_commit = code_commit
        question_hash = sha256_file(question_bank_path)
        if question_hash != self.model.question_bank_sha256:
            raise ValueError("question bank bytes do not match the frozen mapping library")
        self.model.library.validate_against_question_bank(self.question_bank)
        self._universe_cache: dict[tuple[int, int, str], tuple[CandidateState, ...]] = {}
        self._prevalence_cache: dict[tuple[int, str, str], dict[str, float]] = {}
        self._universe_digest_cache: dict[tuple[int, RankScope, str], str] = {}

    @property
    def scoreable_question_ids(self) -> frozenset[str]:
        return frozenset(
            question_id
            for mapping in self.model.library.frozen_mappings
            for question_id in mapping.question_ids
        )

    def build_prediction_freeze(
        self,
        *,
        session_id: str,
        birth: ResolvedBirth,
        ranking_scope: RankScope,
        created_at_utc: datetime,
    ) -> PredictionFreeze:
        self._require_supported_scope(ranking_scope)
        states = self._states_for_birth(birth)
        chart = self.chart_engine.calculate(birth.birth_utc)
        oracle = {
            response.question_id: response
            for response in self.model.oracle_responses(chart)
            if response.answer != "unknown"
        }
        dimensions: list[PredictionDimension] = []
        for question_id in sorted(oracle):
            response = oracle[question_id]
            mappings = self.model.library.matching_mappings(chart, question_id=question_id)
            support: set[str] = set()
            contradictions: set[str] = set()
            statements: set[str] = set()
            mapping_ids: set[str] = set()
            for mapping in mappings:
                mapping_ids.add(mapping.mapping_id)
                statements.add(mapping.behavioral_statement)
                assert mapping.predicted_response is not None
                support.update(mapping.predicted_response.support_answer_tokens)
                if mapping.contradiction_rule is not None:
                    contradictions.update(mapping.contradiction_rule.answer_tokens)
            dimensions.append(
                PredictionDimension(
                    question_id=question_id,
                    cluster_id=response.cluster_id,
                    canonical_answer=response.answer,
                    support_answers=tuple(sorted(support | {response.answer})),
                    contradiction_answers=tuple(sorted(contradictions)),
                    behavioral_statements=tuple(sorted(statements)),
                    mapping_ids=tuple(sorted(mapping_ids)),
                )
            )
        universe_hash = self._candidate_universe_digest(
            states,
            ranking_scope=ranking_scope,
            timezone_name=birth.iana_timezone,
        )
        return PredictionFreeze(
            session_id=session_id,
            created_at_utc=created_at_utc.astimezone(UTC),
            birth=birth,
            chart=chart,
            dimensions=tuple(dimensions),
            code_commit=self.code_commit,
            engine_fingerprint=self.chart_engine.fingerprint,
            model_version=self.model.library.model_version,
            model_sha256=self.model.model_sha256,
            mapping_sha256=self.model.mapping_sha256,
            question_bank_version=self.question_bank.version,
            question_bank_sha256=self.model.question_bank_sha256,
            ranking_scope=ranking_scope,
            candidate_universe_sha256=universe_hash,
            candidate_universe_state_count=len(states),
            candidate_universe_utc_start=states[0].start_utc,
            candidate_universe_utc_end_exclusive=states[-1].end_utc,
            candidate_universe_timezone=birth.iana_timezone,
        )

    def rank(
        self,
        *,
        session_id: str,
        freeze: PredictionFreeze,
        responses: Sequence[BehavioralResponse],
        mode: SessionMode,
        analysis_kind: str,
    ) -> RankingSnapshot:
        self.assert_freeze_compatible(freeze)
        self._require_supported_scope(freeze.ranking_scope)
        states = self._states_for_birth(freeze.birth)
        self._assert_frozen_universe(freeze, states)
        prevalence = self._prevalence_for_states(states)
        scores = self._score_states(states, responses, prevalence)
        ranked_states = self._rank_states(states, scores)
        actual = next(
            (
                item
                for item in ranked_states
                if item.state.start_utc <= freeze.birth.birth_utc < item.state.end_utc
            ),
            None,
        )
        if actual is None:
            raise RuntimeError("true birth instant is outside its declared candidate universe")
        ranked_dates = aggregate_dates(
            states,
            scores,
            AggregationMode.DURATION_WEIGHTED_EVIDENCE,
            0.0,
        )
        true_local_date = freeze.birth.supplied_local.date()
        actual_date = next(
            (item for item in ranked_dates if item.local_date == true_local_date),
            None,
        )
        if actual_date is None:
            raise RuntimeError("true local birth date is outside its declared candidate universe")
        top_state_ties = sum(math.isclose(item.rank, ranked_states[0].rank) for item in ranked_states)
        top_date_score = ranked_dates[0].date_score
        top_date_ties = sum(
            math.isclose(
                item.date_score,
                top_date_score,
                rel_tol=1e-12,
                abs_tol=1e-12,
            )
            for item in ranked_dates
        )
        margin = self._top_net_margin(ranked_states)
        if analysis_kind == "posthoc_final_profile":
            scientific_status = "posthoc_exploratory_not_independent"
            caveat = (
                "Post-hoc exploratory ranking after chart reveal/profile refinement; "
                "do not count it as independent evidence."
            )
        elif mode is SessionMode.SCIENTIFIC_BLIND:
            scientific_status = "confirmatory_blind"
            caveat = (
                "Confirmatory rank uses only pre-reveal trait/behavior evidence. "
                "Outcome, timing, environment, and conventional covariates are excluded."
            )
        else:
            scientific_status = "precommitted_self_discovery"
            caveat = (
                "Predictions were frozen before answers, but the interview model may have "
                "seen the birth tuple; treat this as precommitted exploration, not full blinding."
            )
        return RankingSnapshot(
            session_id=session_id,
            analysis_kind=analysis_kind,  # type: ignore[arg-type]
            ranking_scope=freeze.ranking_scope,
            created_at_utc=datetime.now(UTC),
            candidate_state_count=len(ranked_states),
            candidate_date_count=len(ranked_dates),
            true_state_rank=actual.rank,
            true_state_percentile=_percentile(actual.rank, len(ranked_states)),
            true_date_rank=actual_date.date_rank,
            true_date_percentile=_percentile(actual_date.date_rank, len(ranked_dates)),
            top_state_tie_count=top_state_ties,
            top_date_tie_count=top_date_ties,
            top_margin_rubric_bits=margin,
            actual_state_score=actual.score,
            scientific_status=scientific_status,  # type: ignore[arg-type]
            caveat=caveat,
        )

    def discrimination(
        self,
        *,
        freeze: PredictionFreeze,
        responses: Sequence[BehavioralResponse],
    ) -> DiscriminationDiagnostics:
        """Return only non-answer-key diagnostics safe to show before reveal."""

        self.assert_freeze_compatible(freeze)
        self._require_supported_scope(freeze.ranking_scope)
        states = self._states_for_birth(freeze.birth)
        self._assert_frozen_universe(freeze, states)
        prevalence = self._prevalence_for_states(states)
        scores = self._score_states(states, responses, prevalence)
        ranked = self._rank_states(states, scores)
        return DiscriminationDiagnostics(
            candidate_state_count=len(ranked),
            top_state_tie_count=sum(math.isclose(item.rank, ranked[0].rank) for item in ranked),
            top_margin_rubric_bits=self._top_net_margin(ranked),
        )

    def select_question(
        self,
        *,
        freeze: PredictionFreeze,
        responses: Sequence[BehavioralResponse],
        answered_question_ids: frozenset[str],
    ) -> SelectedQuestion | None:
        """Choose a neutral answer-blind question using candidate discrimination."""

        self.assert_freeze_compatible(freeze)
        self._require_supported_scope(freeze.ranking_scope)
        remaining = self.scoreable_question_ids - answered_question_ids
        if not remaining:
            return None
        states = self._states_for_birth(freeze.birth)
        self._assert_frozen_universe(freeze, states)
        prevalence = self._prevalence_for_states(states)
        score_by_id = self._score_states(states, responses, prevalence)
        scores = [score_by_id[state.state_id] for state in states]
        max_net = max(score.net_rubric_bits for score in scores)
        weights = [
            max(1.0, (state.end_utc - state.start_utc).total_seconds())
            * 2.0 ** max(-30.0, score.net_rubric_bits - max_net)
            for state, score in zip(states, scores, strict=True)
        ]
        canonical_cache: dict[tuple[str, str, str, str, tuple[str, ...]], dict[str, str]] = {}
        canonical_by_state: list[dict[str, str]] = []
        for state in states:
            signature = self.model.scoring_signature(state.chart_features)
            canonical = canonical_cache.get(signature)
            if canonical is None:
                canonical = self.model.library.canonical_answers(state.chart_features)
                canonical_cache[signature] = canonical
            canonical_by_state.append(canonical)
        answer_spaces = self.model.answer_spaces()
        likelihoods: dict[str, list[dict[str, float]]] = {}
        reliability: dict[str, float] = {}
        burden: dict[str, float] = {}
        for question_id in sorted(remaining):
            if question_id not in self.question_bank.question_ids:
                continue
            alphabet = tuple(answer_spaces.get(question_id, ("unknown",)))
            if "unknown" not in alphabet:
                alphabet = (*alphabet, "unknown")
            rows: list[dict[str, float]] = []
            for canonical in canonical_by_state:
                expected = canonical.get(question_id, "unknown")
                rows.append(_likelihood_row(alphabet, expected, match_probability=0.80))
            likelihoods[question_id] = rows
            question = self.question_bank.by_id(question_id)
            reliability[question_id] = 0.75 if question.body_access_sensitive else 1.0
            burden[question_id] = 0.05 * max(0, len(question.followups) - 1)
        utility = select_next_question(weights, likelihoods, reliability, burden)
        if utility is None:
            return None
        return SelectedQuestion(
            question=self.question_bank.by_id(utility.question_id),
            utility=utility,
        )

    def assert_freeze_compatible(self, freeze: PredictionFreeze) -> None:
        """Fail closed if an in-progress session meets a different runtime bundle."""

        expected = {
            "source commit": self.code_commit,
            "chart engine": self.chart_engine.fingerprint,
            "model version": self.model.library.model_version,
            "model bytes": self.model.model_sha256,
            "mapping bytes": self.model.mapping_sha256,
            "question bank version": self.question_bank.version,
            "question bank bytes": self.model.question_bank_sha256,
        }
        frozen = {
            "source commit": freeze.code_commit,
            "chart engine": freeze.engine_fingerprint,
            "model version": freeze.model_version,
            "model bytes": freeze.model_sha256,
            "mapping bytes": freeze.mapping_sha256,
            "question bank version": freeze.question_bank_version,
            "question bank bytes": freeze.question_bank_sha256,
        }
        mismatches = tuple(name for name, value in expected.items() if frozen[name] != value)
        if mismatches:
            raise FrozenRuntimeMismatchError(
                "active participant runtime differs from the frozen session bundle: "
                + ", ".join(mismatches)
            )

    def _states_for_birth(self, birth: ResolvedBirth) -> tuple[CandidateState, ...]:
        key = (
            birth.supplied_local.year,
            birth.supplied_local.month,
            birth.iana_timezone,
        )
        cached = self._universe_cache.get(key)
        if cached is not None:
            return cached
        if self.candidate_cache_dir is not None:
            request = MonthRequest(key[0], key[1], key[2])
            ensure_month_caches(
                (request,),
                ephemeris_path=self.ephemeris_path,
                cache_dir=self.candidate_cache_dir,
                workers=1,
            )
            cached_universe = load_cached_universe(
                cache_path(
                    self.candidate_cache_dir,
                    request,
                    self.chart_engine.fingerprint,
                ),
                request=request,
                engine_fingerprint=self.chart_engine.fingerprint,
            )
            states = cached_universe.states
        else:
            start, end = local_month_utc_bounds(key[0], key[1], key[2])
            states = self.chart_engine.candidate_states(start, end, birth.iana_timezone)
        if not states:
            raise RuntimeError("candidate universe is empty")
        self._universe_cache[key] = states
        return states

    def _prevalence_for_states(
        self,
        states: Sequence[CandidateState],
    ) -> dict[str, float]:
        key = _universe_cache_key(states)
        cached = self._prevalence_cache.get(key)
        if cached is None:
            cached = candidate_prevalence(states, self.model.library)
            self._prevalence_cache[key] = cached
        return cached

    def _score_states(
        self,
        states: Sequence[CandidateState],
        responses: Sequence[BehavioralResponse],
        prevalence: dict[str, float],
    ) -> dict[str, ScoredState]:
        """Score once per model-visible chart signature, preserving state IDs."""

        if not responses:
            return {
                state.state_id: ScoredState(
                    state_id=state.state_id,
                    net_rubric_bits=0.0,
                    evidence_rubric_bits=0.0,
                    contradiction_rubric_bits=0.0,
                    detailed_support=0.0,
                    core_fit=0.0,
                    meaningful_contradictions=0,
                )
                for state in states
            }
        by_signature: dict[
            tuple[str, str, str, str, tuple[str, ...]], ScoredState
        ] = {}
        result: dict[str, ScoredState] = {}
        for state in states:
            signature = self.model.scoring_signature(state.chart_features)
            score = by_signature.get(signature)
            if score is None:
                score = self.model.score(state, responses, prevalence)
                by_signature[signature] = score
            result[state.state_id] = (
                score
                if score.state_id == state.state_id
                else score.model_copy(update={"state_id": state.state_id})
            )
        return result

    def _candidate_universe_digest(
        self,
        states: Sequence[CandidateState],
        *,
        ranking_scope: RankScope,
        timezone_name: str,
    ) -> str:
        # CandidateState and the containing tuples are immutable.  Caching by tuple
        # identity avoids re-hashing ~289k rows on every adaptive interview turn.
        key = (id(states), ranking_scope, timezone_name)
        cached = self._universe_digest_cache.get(key)
        if cached is None:
            cached = _candidate_universe_sha256(
                states,
                ranking_scope=ranking_scope,
                engine_fingerprint=self.chart_engine.fingerprint,
                timezone_name=timezone_name,
            )
            self._universe_digest_cache[key] = cached
        return cached

    def _assert_frozen_universe(
        self,
        freeze: PredictionFreeze,
        states: Sequence[CandidateState],
    ) -> None:
        observed = self._candidate_universe_digest(
            states,
            ranking_scope=freeze.ranking_scope,
            timezone_name=freeze.birth.iana_timezone,
        )
        if observed != freeze.candidate_universe_sha256:
            raise RuntimeError(
                "candidate universe changed after the pre-answer prediction freeze"
            )
        if len(states) != freeze.candidate_universe_state_count:
            raise RuntimeError("candidate universe state count changed after freeze")
        if states[0].start_utc != freeze.candidate_universe_utc_start:
            raise RuntimeError("candidate universe start changed after freeze")
        if states[-1].end_utc != freeze.candidate_universe_utc_end_exclusive:
            raise RuntimeError("candidate universe end changed after freeze")

    def _rank_states(
        self,
        states: Sequence[CandidateState],
        scores: dict[str, ScoredState],
    ) -> tuple[_RankedState, ...]:
        """Rank by evidence score; duration only gives deterministic display order.

        State duration must never turn an evidence-equivalent set into distinct
        scientific ranks.  In particular, with zero behavioral evidence every
        candidate state receives the same midrank and the top tie count equals the
        full universe.
        """

        ordered = sorted(
            states,
            key=lambda state: (
                -scores[state.state_id].net_rubric_bits,
                scores[state.state_id].meaningful_contradictions,
                -scores[state.state_id].detailed_support,
                -scores[state.state_id].core_fit,
                -(state.end_utc - state.start_utc).total_seconds(),
                state.start_utc,
            ),
        )
        result: list[_RankedState] = []
        position = 0
        while position < len(ordered):
            state = ordered[position]
            key = _evidence_tie_key(scores[state.state_id])
            end = position + 1
            while end < len(ordered) and _evidence_tie_key(
                scores[ordered[end].state_id]
            ) == key:
                end += 1
            midrank = (position + 1 + end) / 2.0
            result.extend(
                _RankedState(item, scores[item.state_id], midrank)
                for item in ordered[position:end]
            )
            position = end
        return tuple(result)

    @staticmethod
    def _top_net_margin(ranked: Sequence[_RankedState]) -> float:
        if len(ranked) < 2:
            return 0.0
        top = ranked[0].score.net_rubric_bits
        for item in ranked[1:]:
            if not math.isclose(
                item.score.net_rubric_bits,
                top,
                rel_tol=1e-12,
                abs_tol=1e-12,
            ):
                return top - item.score.net_rubric_bits
        return 0.0

    @staticmethod
    def _require_supported_scope(scope: RankScope) -> None:
        if scope is RankScope.CENTURY_GLOBAL:
            raise UnsupportedRankScopeError(
                "century_global requires the reusable generic 100-year candidate-state cache; "
                "the completed 100-year audit is target-specific and is not reused as if it "
                "were a production participant universe"
            )


def _universe_cache_key(states: Sequence[CandidateState]) -> tuple[int, str, str]:
    if not states:
        raise ValueError("candidate universe must not be empty")
    return len(states), states[0].state_id, states[-1].state_id


def _candidate_universe_sha256(
    states: Sequence[CandidateState],
    *,
    ranking_scope: RankScope,
    engine_fingerprint: str,
    timezone_name: str,
) -> str:
    if not states:
        raise ValueError("candidate universe must not be empty")
    digest = sha256()
    digest.update(
        canonical_json_bytes(
            {
                "schema_version": "participant-candidate-universe-binding-v1",
                "ranking_scope": ranking_scope.value,
                "engine_fingerprint": engine_fingerprint,
                "timezone_name": timezone_name,
            }
        )
        + b"\n"
    )
    for state in states:
        digest.update(
            canonical_json_bytes(
                {
                    "state_id": state.state_id,
                    "start_utc": state.start_utc,
                    "end_utc": state.end_utc,
                    "chart_features_hash": state.chart_features_hash,
                }
            )
            + b"\n"
        )
    return digest.hexdigest()


def _evidence_tie_key(score: ScoredState) -> tuple[float | int, ...]:
    return (
        round(score.net_rubric_bits, 12),
        score.meaningful_contradictions,
        round(score.detailed_support, 12),
        round(score.core_fit, 12),
    )


def _percentile(rank: float, total: int) -> float:
    return 100.0 * (total - rank + 1.0) / total


def _likelihood_row(
    alphabet: Sequence[str],
    expected: str,
    *,
    match_probability: float,
) -> dict[str, float]:
    unique = tuple(dict.fromkeys(alphabet))
    if expected not in unique:
        unique = (*unique, expected)
    if len(unique) == 1:
        return {unique[0]: 1.0}
    mismatch = (1.0 - match_probability) / (len(unique) - 1)
    return {
        token: match_probability if token == expected else mismatch
        for token in unique
    }
