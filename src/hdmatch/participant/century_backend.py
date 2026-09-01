"""Participant backend that adds fail-closed verified century-wide recovery."""

from __future__ import annotations

from collections.abc import Sequence
from contextvars import ContextVar
from datetime import datetime

from hdmatch.runtime.century_cache import (
    CenturyCacheVerificationError,
    load_century_candidate_states,
    load_pinned_century_candidate_states_for_range,
    verify_century_cache,
    verify_pinned_century_cache,
)
from hdmatch.schemas import BehavioralResponse, CandidateState
from hdmatch.search import local_month_utc_bounds

from .backend import (
    AstroHDParticipantBackend,
    DiscriminationDiagnostics,
    SelectedQuestion,
    UnsupportedRankScopeError,
)
from .models import (
    PredictionFreeze,
    RankingSnapshot,
    RankScope,
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
        century_manifest_sha256: str | None = None,
        century_canonical_rows_sha256: str | None = None,
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
        self.century_manifest_sha256 = century_manifest_sha256
        self.century_canonical_rows_sha256 = century_canonical_rows_sha256
        self._active_scope: ContextVar[RankScope] = ContextVar(
            "hdmatch_participant_rank_scope",
            default=RankScope.KNOWN_BIRTH_MONTH,
        )
        self._century_verified = False
        self._century_universe_cache: dict[str, tuple[CandidateState, ...]] = {}

    @staticmethod
    def _require_supported_scope(scope: RankScope) -> None:
        """Base guard is replaced; instance-level verification happens during load."""

    def build_prediction_freeze(
        self,
        *,
        session_id: str,
        birth: ResolvedBirth,
        ranking_scope: RankScope,
        created_at_utc: datetime,
    ) -> PredictionFreeze:
        token = self._active_scope.set(ranking_scope)
        try:
            return super().build_prediction_freeze(
                session_id=session_id,
                birth=birth,
                ranking_scope=ranking_scope,
                created_at_utc=created_at_utc,
            )
        finally:
            self._active_scope.reset(token)

    def rank(
        self,
        *,
        session_id: str,
        freeze: PredictionFreeze,
        responses: Sequence[BehavioralResponse],
        mode: SessionMode,
        analysis_kind: str,
    ) -> RankingSnapshot:
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
        scope = self._active_scope.get()
        if scope is RankScope.KNOWN_BIRTH_MONTH and self._pinned_century_ready:
            key = (
                birth.supplied_local.year,
                birth.supplied_local.month,
                birth.iana_timezone,
            )
            cached_month = self._universe_cache.get(key)
            if cached_month is not None:
                return cached_month
            start, end = local_month_utc_bounds(key[0], key[1], key[2])
            assert self.century_cache_dir is not None
            assert self.century_manifest_sha256 is not None
            assert self.century_canonical_rows_sha256 is not None
            try:
                states = load_pinned_century_candidate_states_for_range(
                    self.century_cache_dir,
                    timezone_name=birth.iana_timezone,
                    expected_engine_fingerprint=self.chart_engine.fingerprint,
                    expected_manifest_sha256=self.century_manifest_sha256,
                    expected_canonical_rows_sha256=self.century_canonical_rows_sha256,
                    range_start_utc=start,
                    range_end_utc=end,
                )
            except CenturyCacheVerificationError as exc:
                raise UnsupportedRankScopeError(
                    f"known_birth_month pinned cache verification failed: {exc}"
                ) from exc
            self._universe_cache[key] = states
            return states
        if scope is not RankScope.CENTURY_GLOBAL:
            return super()._states_for_birth(birth)
        cached = self._century_universe_cache.get(birth.iana_timezone)
        if cached is not None:
            return cached
        if self.century_cache_dir is None:
            raise UnsupportedRankScopeError(
                "century_global requires HDMATCH_CENTURY_CACHE pointing to a verified exact cache"
            )
        try:
            # load_century_candidate_states verifies manifest, files, canonical rows,
            # partition and engine fingerprint in the same pass that constructs the
            # immutable timezone-localized CandidateState tuple.
            states = load_century_candidate_states(
                self.century_cache_dir,
                timezone_name=birth.iana_timezone,
                expected_engine_fingerprint=self.chart_engine.fingerprint,
            )
        except CenturyCacheVerificationError as exc:
            raise UnsupportedRankScopeError(
                f"century_global cache verification failed: {exc}"
            ) from exc
        if not any(state.start_utc <= birth.birth_utc < state.end_utc for state in states):
            raise UnsupportedRankScopeError(
                "the participant birth instant is outside the verified century-cache horizon"
            )
        self._century_verified = True
        self._century_universe_cache[birth.iana_timezone] = states
        return states

    def _verify_century_ready(self) -> str:
        """Explicit verifier for deployment health checks outside a loaded session."""

        if self.century_cache_dir is None:
            raise UnsupportedRankScopeError(
                "century_global requires HDMATCH_CENTURY_CACHE pointing to a verified exact cache"
            )
        if self._century_verified:
            return self.century_cache_dir
        try:
            verify_century_cache(
                self.century_cache_dir,
                expected_engine_fingerprint=self.chart_engine.fingerprint,
            )
        except CenturyCacheVerificationError as exc:
            raise UnsupportedRankScopeError(
                f"century_global cache verification failed: {exc}"
            ) from exc
        self._century_verified = True
        return self.century_cache_dir

    @property
    def _pinned_century_ready(self) -> bool:
        return (
            self.century_cache_dir is not None
            and self.century_manifest_sha256 is not None
            and self.century_canonical_rows_sha256 is not None
        )

    def verify_pinned_month_cache_ready(self) -> str:
        """Fail closed unless the exact released artifact is ready for month slicing."""

        if not self._pinned_century_ready:
            raise UnsupportedRankScopeError(
                "known_birth_month fast path requires the century cache and both release hashes"
            )
        assert self.century_cache_dir is not None
        assert self.century_manifest_sha256 is not None
        assert self.century_canonical_rows_sha256 is not None
        try:
            verify_pinned_century_cache(
                self.century_cache_dir,
                expected_engine_fingerprint=self.chart_engine.fingerprint,
                expected_manifest_sha256=self.century_manifest_sha256,
                expected_canonical_rows_sha256=self.century_canonical_rows_sha256,
            )
        except CenturyCacheVerificationError as exc:
            raise UnsupportedRankScopeError(
                f"known_birth_month pinned cache verification failed: {exc}"
            ) from exc
        return self.century_cache_dir
