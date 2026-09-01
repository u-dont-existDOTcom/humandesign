"""Participant-session orchestration with strict confirmatory/post-hoc separation."""

from __future__ import annotations

import secrets
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Protocol

from hdmatch.chart.timezone import resolve_local_datetime
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_bytes
from hdmatch.schemas import BehavioralResponse

from .backend import DiscriminationDiagnostics, SelectedQuestion
from .models import (
    BirthIntake,
    CompletionPolicySnapshot,
    CompletionPolicyStatus,
    ConfirmatoryLock,
    EvidenceInput,
    EvidenceRecord,
    ExploratoryRankingReport,
    FinalParticipantReport,
    FrozenDimensionBinding,
    NextInterviewQuestion,
    PredictionComparison,
    PredictionFreeze,
    PredictionFreezeRef,
    PublicProgress,
    RankingSnapshot,
    RankScope,
    ResolvedBirth,
    RevealReport,
    SessionMode,
    SessionPhase,
    SessionRecord,
    StoredEvidenceInput,
)
from .store import ParticipantSessionStore


class ParticipantBackend(Protocol):
    @property
    def scoreable_question_ids(self) -> frozenset[str]: ...

    @property
    def mapped_scoreable_question_ids(self) -> frozenset[str]: ...

    def build_prediction_freeze(
        self,
        *,
        session_id: str,
        birth: ResolvedBirth,
        ranking_scope: RankScope,
        created_at_utc: datetime,
    ) -> PredictionFreeze: ...

    def assert_freeze_compatible(self, freeze: PredictionFreeze) -> None: ...

    def rank(
        self,
        *,
        session_id: str,
        freeze: PredictionFreeze,
        responses: Sequence[BehavioralResponse],
        mode: SessionMode,
        analysis_kind: str,
    ) -> RankingSnapshot: ...

    def discrimination(
        self,
        *,
        freeze: PredictionFreeze,
        responses: Sequence[BehavioralResponse],
    ) -> DiscriminationDiagnostics: ...

    def select_question(
        self,
        *,
        freeze: PredictionFreeze,
        responses: Sequence[BehavioralResponse],
        answered_question_ids: frozenset[str],
    ) -> SelectedQuestion | None: ...


class ParticipantStateError(RuntimeError):
    """Raised when an operation is invalid in the current session phase."""


class ParticipantProtocolError(ParticipantStateError):
    """Fail-closed protocol error with a stable API-facing code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class ParticipantSessionService:
    """Create, interview, lock, reveal, and refine one participant profile."""

    def __init__(
        self,
        *,
        store: ParticipantSessionStore,
        backend: ParticipantBackend,
    ) -> None:
        self.store = store
        self.backend = backend

    def create_session(self, intake: BirthIntake) -> SessionRecord:
        resolution = resolve_local_datetime(
            intake.local_datetime,
            intake.iana_timezone,
            fold=intake.fold,
        )
        instant = resolution.require_unique()
        birth = ResolvedBirth(
            supplied_local=intake.local_datetime,
            birthplace=intake.birthplace,
            iana_timezone=intake.iana_timezone,
            fold=instant.fold,
            birth_utc=instant.utc,
            utc_offset_seconds=int(instant.utc_offset.total_seconds()),
            tzdb_version=resolution.tzdb_version,
            pre_standard_time_uncertain=resolution.pre_standard_time_uncertain,
        )
        session_id = "HD-" + secrets.token_hex(16).upper()
        now = datetime.now(UTC)
        freeze = self.backend.build_prediction_freeze(
            session_id=session_id,
            birth=birth,
            ranking_scope=intake.ranking_scope,
            created_at_utc=now,
        )
        freeze_sha256 = sha256_bytes(canonical_json_bytes(freeze))
        record = SessionRecord(
            session_id=session_id,
            mode=intake.mode,
            ranking_scope=intake.ranking_scope,
            created_at_utc=now,
            prediction_freeze_sha256=freeze_sha256,
        )
        self.store.create(record, freeze, CompletionPolicySnapshot())
        return record

    def phase(self, session_id: str) -> SessionPhase:
        self.store.load_session(session_id)
        if self.store.load_final_report(session_id) is not None:
            return SessionPhase.FINALIZED
        reveal = self.store.load_reveal(session_id)
        if reveal is not None:
            posthoc = any(
                record.phase == "posthoc_exploratory"
                for record in self.store.load_evidence(session_id)
            )
            return SessionPhase.POSTHOC_EXPLORATORY if posthoc else SessionPhase.REVEALED
        if self.store.load_confirmatory_lock(session_id) is not None:
            return SessionPhase.CONFIRMATORY_LOCKED
        return SessionPhase.CONFIRMATORY_BLIND

    def _current_completion_policy(self, session_id: str) -> CompletionPolicySnapshot:
        """Load only the owner-authorized policy state implemented by this protocol."""

        policy = self.store.load_completion_policy(session_id) or CompletionPolicySnapshot()
        if policy.status is not CompletionPolicyStatus.UNRESOLVED_OWNER_AUTHORITY:
            raise ParticipantProtocolError(
                "SCIENTIFIC_COMPLETENESS_POLICY_UNRESOLVED",
                "stored completion-policy authority cannot be verified by this protocol",
            )
        return policy

    def append_evidence(
        self,
        session_id: str,
        evidence: EvidenceInput,
    ) -> EvidenceRecord:
        current = self.phase(session_id)
        if current is SessionPhase.CONFIRMATORY_BLIND:
            evidence_phase = "confirmatory_blind"
        elif current in {SessionPhase.REVEALED, SessionPhase.POSTHOC_EXPLORATORY}:
            evidence_phase = "posthoc_exploratory"
        elif current is SessionPhase.CONFIRMATORY_LOCKED:
            raise ParticipantStateError(
                "confirmatory evidence is locked; reveal before adding exploratory clarification"
            )
        else:
            raise ParticipantStateError("finalized sessions cannot accept more evidence")
        resolved_evidence = self._resolve_evidence(session_id, evidence)
        record = EvidenceRecord(
            evidence_id="EV-" + secrets.token_hex(12).upper(),
            session_id=session_id,
            phase=evidence_phase,  # type: ignore[arg-type]
            created_at_utc=datetime.now(UTC),
            evidence=resolved_evidence,
        )
        self.store.append_evidence(record)
        return record

    def _resolve_evidence(
        self,
        session_id: str,
        evidence: EvidenceInput,
    ) -> StoredEvidenceInput:
        """Bind client evidence to exactly one immutable server-side dimension."""

        values = evidence.model_dump(mode="python")
        if not evidence.domain.natal_ranking_eligible or evidence.question_id is None:
            return StoredEvidenceInput(**values)

        freeze = self.store.load_freeze(session_id)
        self.backend.assert_freeze_compatible(freeze)
        matches = [
            (index, dimension)
            for index, dimension in enumerate(freeze.dimensions)
            if dimension.question_id == evidence.question_id
        ]
        if not matches:
            raise ParticipantProtocolError(
                "FROZEN_QUESTION_BINDING_MISSING",
                f"question_id {evidence.question_id!r} is absent from the session freeze",
            )
        if len(matches) > 1:
            raise ParticipantProtocolError(
                "FROZEN_QUESTION_BINDING_AMBIGUOUS",
                f"question_id {evidence.question_id!r} has multiple frozen dimensions",
            )

        dimension_index, dimension = matches[0]
        session = self.store.load_session(session_id)
        binding = FrozenDimensionBinding(
            question_id=evidence.question_id,
            resolved_cluster_id=dimension.cluster_id,
            freeze_ref=PredictionFreezeRef(
                session_id=session_id,
                freeze_sha256=session.prediction_freeze_sha256,
            ),
            dimension_index=dimension_index,
            resolved_at_utc=datetime.now(UTC),
        )
        return StoredEvidenceInput(**values, frozen_dimension_binding=binding)

    def public_progress(self, session_id: str) -> PublicProgress:
        current = self.phase(session_id)
        records = self.store.load_evidence(session_id)
        confirmatory = tuple(record for record in records if record.phase == "confirmatory_blind")
        locked = self.store.load_confirmatory_lock(session_id)
        if locked is not None:
            responses = locked.scoring_responses
        else:
            responses = self._latest_scoreable_responses(confirmatory)
        scoreable_ids = {response.question_id for response in responses}
        non_natal = sum(
            not record.evidence.domain.natal_ranking_eligible for record in confirmatory
        )
        freeze = self.store.load_freeze(session_id)
        diagnostics = self.backend.discrimination(freeze=freeze, responses=responses)
        mapped_scoreable_ids = self.backend.mapped_scoreable_question_ids
        total_mapped = len(mapped_scoreable_ids)
        mapped_coverage = (
            len(scoreable_ids & mapped_scoreable_ids) / total_mapped if total_mapped else 0.0
        )
        adequately_assessed_ids = (
            self._latest_adequately_assessed_question_ids(confirmatory) & mapped_scoreable_ids
        )
        policy = self._current_completion_policy(session_id)
        return PublicProgress(
            session_id=session_id,
            phase=current,
            confirmatory_observation_count=len(confirmatory),
            scoreable_observation_count=len(scoreable_ids),
            non_natal_observation_count=non_natal,
            mapped_scoreable_question_count=total_mapped,
            mapped_scoreable_coverage=mapped_coverage,
            adequately_assessed_mapped_question_count=len(adequately_assessed_ids),
            completion_policy_status=policy.status,
            completion_policy_id=None,
            completion_required_question_count=None,
            completion_coverage=None,
            completion_authority_source_ref=None,
            candidate_state_count=diagnostics.candidate_state_count,
            top_state_tie_count=diagnostics.top_state_tie_count,
            top_margin_rubric_bits=diagnostics.top_margin_rubric_bits,
        )

    def next_question(self, session_id: str) -> NextInterviewQuestion:
        if self.phase(session_id) is not SessionPhase.CONFIRMATORY_BLIND:
            raise ParticipantStateError(
                "adaptive confirmatory questions stop when evidence is locked"
            )
        freeze = self.store.load_freeze(session_id)
        self.backend.assert_freeze_compatible(freeze)
        records = tuple(
            record
            for record in self.store.load_evidence(session_id)
            if record.phase == "confirmatory_blind"
        )
        if not records:
            return NextInterviewQuestion(
                session_id=session_id,
                question_id=None,
                prompt=(
                    "Start with the patterns that have followed you across your life. "
                    "How have you tended to make decisions, approach people and groups, "
                    "learn or master things, handle conflict and uncertainty, use energy, "
                    "and pursue autonomy or resources? Include what was already true in "
                    "childhood, what changed later, and important contexts or exceptions."
                ),
                response_format=(
                    "Open narrative; concrete patterns are more useful than isolated events."
                ),
                minimum_evidence=(
                    "Cover recurring patterns across the named domains with concrete examples, "
                    "exceptions or counterexamples, and childhood-to-adult continuity or change."
                ),
                followups=(
                    "Which of those patterns was already visible in childhood?",
                    "Where does the pattern reliably fail or reverse?",
                    "Give an example and a counterexample for the strongest pattern.",
                ),
            )
        responses = self._latest_scoreable_responses(records)
        noninterview_question_ids = (
            self.backend.scoreable_question_ids - self.backend.mapped_scoreable_question_ids
        )
        answered = (
            self._latest_adequately_assessed_question_ids(records) | noninterview_question_ids
        )
        selected = self.backend.select_question(
            freeze=freeze,
            responses=responses,
            answered_question_ids=answered,
        )
        if selected is None:
            return NextInterviewQuestion(
                session_id=session_id,
                question_id=None,
                prompt=(
                    "No further mapped question was selected. Ask about any remaining "
                    "important contradiction, context dependence, childhood-to-adult change, "
                    "or weakly evidenced part of the holistic profile before locking it."
                ),
                response_format="Open narrative.",
                minimum_evidence=(
                    "Resolve every consequential contradiction or explicitly leave the affected "
                    "dimension insufficient. Completion policy remains unresolved owner authority."
                ),
                followups=(
                    "What would make your current description misleading?",
                    "What is the strongest counterexample?",
                ),
            )
        question = selected.question
        return NextInterviewQuestion(
            session_id=session_id,
            question_id=question.id,
            prompt=question.prompt,
            response_format=question.response_format,
            minimum_evidence=question.minimum_evidence,
            followups=question.followups,
            expected_information_gain=selected.utility.expected_information_gain,
            adjusted_utility=selected.utility.adjusted_utility,
        )

    def lock_confirmatory(
        self,
        session_id: str,
    ) -> ConfirmatoryLock:
        self._current_completion_policy(session_id)
        raise ParticipantProtocolError(
            "SCIENTIFIC_COMPLETENESS_POLICY_UNRESOLVED",
            "scientific completeness policy is unresolved owner authority",
        )

    def reveal(self, session_id: str) -> RevealReport:
        self._current_completion_policy(session_id)
        raise ParticipantProtocolError(
            "SCIENTIFIC_COMPLETENESS_POLICY_UNRESOLVED",
            "new conforming reveal is unavailable without verified owner authority",
        )

    def load_historical_diagnostic_reveal(self, session_id: str) -> RevealReport:
        """Read an existing pre-repair reveal without relabeling or mutating it."""

        report = self.store.load_reveal(session_id)
        if report is None:
            raise ParticipantStateError("no historical diagnostic reveal exists")
        lock = self.store.load_confirmatory_lock(session_id)
        if lock is None or lock.schema_version == "participant-confirmatory-lock-v3":
            raise ParticipantStateError("stored result is not a pre-repair diagnostic reveal")
        return report

    def finalize_exploratory(self, session_id: str) -> FinalParticipantReport:
        existing = self.store.load_final_report(session_id)
        if existing is not None:
            return existing
        reveal = self.store.load_reveal(session_id)
        if reveal is None:
            raise ParticipantStateError(
                "reveal the confirmatory result before post-hoc finalization"
            )
        lock = self.store.load_confirmatory_lock(session_id)
        if lock is None:
            raise ParticipantStateError("confirmatory lock is missing")
        records = self.store.load_evidence(session_id)
        posthoc = tuple(record for record in records if record.phase == "posthoc_exploratory")
        final_responses = self._apply_posthoc_overrides(
            lock.scoring_responses,
            posthoc,
        )
        ranking = self._calculate_ranking(
            session_id,
            final_responses,
            analysis_kind="posthoc_final_profile",
        )
        baseline = {response.question_id: response for response in lock.scoring_responses}
        refined = {response.question_id: response for response in final_responses}
        changed = tuple(
            sorted(
                question_id
                for question_id in set(baseline) | set(refined)
                if baseline.get(question_id) != refined.get(question_id)
            )
        )
        exploratory = ExploratoryRankingReport(
            session_id=session_id,
            ranking=ranking,
            final_profile_responses=final_responses,
            changed_question_ids=changed,
        )
        final = FinalParticipantReport(
            session_id=session_id,
            mode=self.store.load_session(session_id).mode,
            confirmatory=reveal,
            exploratory=exploratory,
            retained_secondary_evidence=tuple(
                record for record in records if not record.evidence.domain.natal_ranking_eligible
            ),
        )
        self.store.write_exploratory(exploratory)
        self.store.write_final_report(final)
        return final

    def _calculate_ranking(
        self,
        session_id: str,
        responses: Sequence[BehavioralResponse],
        *,
        analysis_kind: str,
    ) -> RankingSnapshot:
        session = self.store.load_session(session_id)
        freeze = self.store.load_freeze(session_id)
        return self.backend.rank(
            session_id=session_id,
            freeze=freeze,
            responses=responses,
            mode=session.mode,
            analysis_kind=analysis_kind,
        )

    def _store_confirmatory_ranking(
        self,
        session_id: str,
        responses: Sequence[BehavioralResponse],
    ) -> RankingSnapshot:
        ranking = self._calculate_ranking(
            session_id,
            responses,
            analysis_kind="pre_reveal",
        )
        self.store.write_confirmatory_ranking(ranking)
        return ranking

    def _latest_scoreable_responses(
        self,
        records: Sequence[EvidenceRecord],
    ) -> tuple[BehavioralResponse, ...]:
        by_question: dict[str, BehavioralResponse] = {}
        for record in records:
            evidence = record.evidence
            question_id = evidence.question_id
            if (
                not evidence.domain.natal_ranking_eligible
                or question_id is None
                or question_id not in self.backend.mapped_scoreable_question_ids
            ):
                continue
            response = evidence.scoring_response()
            if response is None:
                # A later free-form/"other" clarification deliberately removes an
                # earlier forced-choice token rather than leaving stale evidence scored.
                by_question.pop(question_id, None)
            else:
                by_question[question_id] = response
        return tuple(by_question[key] for key in sorted(by_question))

    def _latest_adequately_assessed_question_ids(
        self,
        records: Sequence[EvidenceRecord],
    ) -> frozenset[str]:
        latest: dict[str, bool] = {}
        for record in records:
            evidence = record.evidence
            question_id = evidence.question_id
            if (
                not evidence.domain.natal_ranking_eligible
                or question_id is None
                or question_id not in self.backend.scoreable_question_ids
            ):
                continue
            latest[question_id] = (
                evidence.minimum_evidence_passed and evidence.consistency_status.adequate
            )
        return frozenset(question_id for question_id, passed in latest.items() if passed)

    def _apply_posthoc_overrides(
        self,
        baseline: Sequence[BehavioralResponse],
        posthoc: Sequence[EvidenceRecord],
    ) -> tuple[BehavioralResponse, ...]:
        by_question = {response.question_id: response for response in baseline}
        for record in posthoc:
            evidence = record.evidence
            question_id = evidence.question_id
            if (
                not evidence.domain.natal_ranking_eligible
                or question_id is None
                or question_id not in self.backend.mapped_scoreable_question_ids
            ):
                continue
            response = evidence.scoring_response()
            if response is None:
                by_question.pop(question_id, None)
            else:
                by_question[question_id] = response
        return tuple(by_question[key] for key in sorted(by_question))

    def _prediction_comparisons(
        self,
        freeze: PredictionFreeze,
        records: Sequence[EvidenceRecord],
    ) -> tuple[PredictionComparison, ...]:
        confirmatory = tuple(record for record in records if record.phase == "confirmatory_blind")
        active: dict[str, tuple[BehavioralResponse, str]] = {}
        for record in confirmatory:
            evidence = record.evidence
            question_id = evidence.question_id
            if (
                not evidence.domain.natal_ranking_eligible
                or question_id is None
                or question_id not in self.backend.mapped_scoreable_question_ids
            ):
                continue
            response = evidence.scoring_response()
            if response is None:
                active.pop(question_id, None)
            else:
                active[question_id] = (response, record.evidence_id)
        comparisons: list[PredictionComparison] = []
        for prediction in freeze.dimensions:
            observed_pair = active.get(prediction.question_id)
            observed = observed_pair[0].answer if observed_pair is not None else None
            evidence_id = observed_pair[1] if observed_pair is not None else None
            if observed is None:
                classification = "insufficient_evidence"
            elif observed == prediction.canonical_answer:
                classification = "supported"
            elif observed in prediction.support_answers:
                classification = "partially_supported"
            elif observed in prediction.contradiction_answers:
                classification = "contradicted"
            else:
                classification = "insufficient_evidence"
            comparisons.append(
                PredictionComparison(
                    question_id=prediction.question_id,
                    cluster_id=prediction.cluster_id,
                    predicted_answer=prediction.canonical_answer,
                    observed_answer=observed,
                    classification=classification,  # type: ignore[arg-type]
                    behavioral_statements=prediction.behavioral_statements,
                    evidence_id=evidence_id,
                )
            )
        return tuple(comparisons)
