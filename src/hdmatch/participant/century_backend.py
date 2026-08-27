"""Participant backend that adds fail-closed verified century-wide recovery."""

from __future__ import annotations

from collections.abc import Sequence
from contextvars import ContextVar
from datetime import datetime

from hdmatch.runtime.century_cache import (
    CenturyCacheVerificationError,
    load_century_candidate_states,
    verify_century_cache,
)
from hdmatch.schemas import BehavioralResponse, CandidateState

from .backend import (
    AstroHDParticipantBackend,
    DiscriminationDiagnostics,
    SelectedQuestion,
    UnsupportedRankScopeError,
)
from .models import (
    PredictionFreeze,
    RankScope,
    RankingSnapshot,
    ResolvedBirth,
    SessionMode,
)


class CenturyCapableParticipantBackend(AstroHDParticipantBackend):
    """Extend the exact month backend with an immutable verified century cache."""

    def __init__(
        self,
        *,
        ephemeris_path: str,
        mapping_path: str,
        question_bank_path: str,
        candidate_cache_dir: str | None = None,
        century_cache_dir: str | None = None,
        code_commit: str = "unknown",
    ) -> None:
        super().__init__(
            ephemeris_path=ephemeris_path,
            mapping_path=mapping_path,
            question_bank_path=question_bank_path,
            candidate_cache_dir=candidate_cache_dir,
            code_commit=code_commit,
        )
        self.century_cache_dir = century_cache_dir
        self._active_scope: ContextVar[RankScope] = ContextVar(
            "hdmatch_participant_rank_scope",
            default=RankScope.KNOWN_BIRTH_MONTH,
        )
        self._century_universe_cache: dict[str, tuple[CandidateState, ...]] = {}

    @staticmethod
    def _require_supported_scope(scope: RankScope) -> None:
        """Base guard is replaced; instance-level verification happens before use."""

    def build_prediction_freeze(
        self,
        *,
        session_id: str,
        birth: ResolvedBirth,
        ranking_scope: RankScope,
        created_at_utc: datetime,
    ) -> PredictionFreeze:
        if ranking_scope is RankScope.CENTURY_GLOBAL:
            self._verify_century_ready()
        return super().build_prediction_freeze(
            session_id=session_id,
            birth=birth,
            ranking_scope=ranking_scope,
            created_at_utc=created_at_utc,
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
        if freeze.ranking_scope is RankScope.CENTURY_GLOBAL:
            self._verify_century_ready()
        token = self._active_scope.set(freeze.ranking_scope)
        try:
            return super().rank(
                session_id=session_id,
                freeze=freeze,
                responses=responses,
                mode=mode,
                analysis_kind=analysis_kind,
            )
        finally:
            self._active_scope.reset(token)

    def discrimination(
        self,
        *,
        freeze: PredictionFreeze,
        responses: Sequence[BehavioralResponse],
    ) -> DiscriminationDiagnostics:
        if freeze.ranking_scope is RankScope.CENTURY_GLOBAL:
            self._verify_century_ready()
        token = self._active_scope.set(freeze.ranking_scope)
        try:
            return super().discrimination(freeze=freeze, responses=responses)
        finally:
            self._active_scope.reset(token)

    def select_question(
        self,
        *,
        freeze: PredictionFreeze,
        responses: Sequence[BehavioralResponse],
        answered_question_ids: frozenset[str],
    ) -> SelectedQuestion | None:
        if freeze.ranking_scope is RankScope.CENTURY_GLOBAL:
            self._verify_century_ready()
        token = self._active_scope.set(freeze.ranking_scope)
        try:
            return super().select_question(
                freeze=freeze,
                responses=responses,
                answered_question_ids=answered_question_ids,
            )
        finally:
            self._active_scope.reset(token)

    def _states_for_birth(self, birth: ResolvedBirth) -> tuple[CandidateState, ...]:
        if self._active_scope.get() is not RankScope.CENTURY_GLOBAL:
            return super()._states_for_birth(birth)
        cached = self._century_universe_cache.get(birth.iana_timezone)
        if cached is not None:
            return cached
        cache_dir = self._verify_century_ready()
        states = load_century_candidate_states(
            cache_dir,
            timezone_name=birth.iana_timezone,
            expected_engine_fingerprint=self.chart_engine.fingerprint,
        )
        if not any(state.start_utc <= birth.birth_utc < state.end_utc for state in states):
            raise UnsupportedRankScopeError(
                "the participant birth instant is outside the verified century-cache horizon"
            )
        self._century_universe_cache[birth.iana_timezone] = states
        return states

    def _verify_century_ready(self) -> str:
        if self.century_cache_dir is None:
            raise UnsupportedRankScopeError(
                "century_global requires HDMATCH_CENTURY_CACHE pointing to a verified exact cache"
            )
        try:
            verify_century_cache(
                self.century_cache_dir,
                expected_engine_fingerprint=self.chart_engine.fingerprint,
            )
        except CenturyCacheVerificationError as exc:
            raise UnsupportedRankScopeError(
                f"century_global cache verification failed: {exc}"
            ) from exc
        return self.century_cache_dir
