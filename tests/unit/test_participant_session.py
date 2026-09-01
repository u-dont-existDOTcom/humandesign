from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.api.natal_pilot_app import NatalPilotConfig, _interviewer_reveal
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_bytes, sha256_file
from hdmatch.participant.backend import (
    DiscriminationDiagnostics,
    FrozenRuntimeMismatchError,
    SelectedQuestion,
)
from hdmatch.participant.models import (
    BirthIntake,
    CompletionPolicySnapshot,
    CompletionPolicyStatus,
    ConfirmatoryLock,
    EvidenceConsistency,
    EvidenceDomain,
    EvidenceInput,
    EvidenceRecord,
    ParticipantModelReceipt,
    PredictionDimension,
    PredictionFreeze,
    RankingSnapshot,
    RankScope,
    ResolvedBirth,
    RevealReport,
    SessionMode,
    StoredEvidenceInput,
)
from hdmatch.participant.service import (
    ParticipantProtocolError,
    ParticipantSessionService,
)
from hdmatch.participant.store import ParticipantSessionStore, SessionStorageError
from hdmatch.questionnaire import Question
from hdmatch.schemas import BehavioralResponse, ChartFeatures, ScoredState
from hdmatch.search import QuestionUtility


class FakeParticipantBackend:
    scoreable_question_ids = frozenset({"Q1", "Q2"})
    mapped_scoreable_question_ids = frozenset({"Q1", "Q2"})

    def assert_freeze_compatible(self, freeze: PredictionFreeze) -> None:
        del freeze

    def build_prediction_freeze(
        self,
        *,
        session_id: str,
        birth: ResolvedBirth,
        ranking_scope: RankScope,
        created_at_utc: datetime,
    ) -> PredictionFreeze:
        chart = ChartFeatures(
            personality_utc=birth.birth_utc,
            design_utc=birth.birth_utc - timedelta(days=88),
            type="Generator",
            strategy="Respond",
            authority="Sacral",
            profile="1/3",
            definition="Single",
            defined_centers=("Sacral",),
            channels=(),
            activations={},
            engine_metadata={"test": True},
        )
        return PredictionFreeze(
            session_id=session_id,
            created_at_utc=created_at_utc,
            birth=birth,
            chart=chart,
            dimensions=(
                PredictionDimension(
                    question_id="Q1",
                    cluster_id="DECISION",
                    canonical_answer="yes",
                    support_answers=("yes",),
                    contradiction_answers=("no",),
                    behavioral_statements=("Usually follows the predicted decision pattern.",),
                    mapping_ids=("MAP-TEST-Q1",),
                ),
                PredictionDimension(
                    question_id="Q2",
                    cluster_id="LEARNING",
                    canonical_answer="yes",
                    support_answers=("yes",),
                    contradiction_answers=("no",),
                    behavioral_statements=("Usually follows the predicted learning pattern.",),
                    mapping_ids=("MAP-TEST-Q2",),
                ),
            ),
            code_commit="test-commit",
            engine_fingerprint="engine-test",
            model_version="test-model",
            model_sha256="a" * 64,
            mapping_sha256="b" * 64,
            question_bank_version="test-bank",
            question_bank_sha256="c" * 64,
            ranking_scope=ranking_scope,
            candidate_universe_sha256="d" * 64,
            candidate_universe_state_count=12,
            candidate_universe_utc_start=birth.birth_utc - timedelta(days=15),
            candidate_universe_utc_end_exclusive=birth.birth_utc + timedelta(days=16),
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
        answers = {response.question_id: response.answer for response in responses}
        state_rank = 1.0 if answers.get("Q1") == "yes" else 7.0
        if analysis_kind == "posthoc_final_profile":
            status = "posthoc_exploratory_not_independent"
        elif mode is SessionMode.SCIENTIFIC_BLIND:
            status = "confirmatory_blind"
        else:
            status = "precommitted_self_discovery"
        return RankingSnapshot(
            session_id=session_id,
            analysis_kind=analysis_kind,  # type: ignore[arg-type]
            ranking_scope=freeze.ranking_scope,
            created_at_utc=datetime.now(UTC),
            candidate_state_count=12,
            candidate_date_count=31,
            true_state_rank=state_rank,
            true_state_percentile=100.0 * (13.0 - state_rank) / 12.0,
            true_date_rank=2.0,
            true_date_percentile=100.0 * 30.0 / 31.0,
            top_state_tie_count=1,
            top_date_tie_count=1,
            top_margin_rubric_bits=2.5,
            actual_state_score=ScoredState(
                state_id="STATE-TEST",
                net_rubric_bits=3.0,
                evidence_rubric_bits=3.5,
                contradiction_rubric_bits=0.5,
                detailed_support=80.0,
                core_fit=75.0,
                meaningful_contradictions=0,
            ),
            scientific_status=status,  # type: ignore[arg-type]
            caveat="test caveat",
        )

    def discrimination(
        self,
        *,
        freeze: PredictionFreeze,
        responses: Sequence[BehavioralResponse],
    ) -> DiscriminationDiagnostics:
        return DiscriminationDiagnostics(
            candidate_state_count=12,
            top_state_tie_count=max(1, 5 - len(responses)),
            top_margin_rubric_bits=0.5 * len(responses),
        )

    def select_question(
        self,
        *,
        freeze: PredictionFreeze,
        responses: Sequence[BehavioralResponse],
        answered_question_ids: frozenset[str],
    ) -> SelectedQuestion | None:
        if "Q1" in answered_question_ids:
            return None
        return SelectedQuestion(
            question=Question(
                id="Q1",
                phase="core",
                domain="decision",
                prompt="Which decision pattern is more typical for you?",
                response_format="yes / no",
                followups=("Was this already true in childhood?",),
                body_access_sensitive=False,
                minimum_evidence="one pattern plus context",
                behavioral_constructs=("decision pattern",),
                scoring_notes="test",
            ),
            utility=QuestionUtility(
                question_id="Q1",
                expected_information_gain=0.8,
                adjusted_utility=0.8,
                expected_reliability=1.0,
                burden=0.0,
            ),
        )


class PhasedParticipantBackend(FakeParticipantBackend):
    scoreable_question_ids = frozenset({"Q1", "Q2", "V03"})
    mapped_scoreable_question_ids = frozenset({"Q1", "Q2"})

    def build_prediction_freeze(
        self,
        *,
        session_id: str,
        birth: ResolvedBirth,
        ranking_scope: RankScope,
        created_at_utc: datetime,
    ) -> PredictionFreeze:
        freeze = super().build_prediction_freeze(
            session_id=session_id,
            birth=birth,
            ranking_scope=ranking_scope,
            created_at_utc=created_at_utc,
        )
        validation_prediction = PredictionDimension(
            question_id="V03",
            cluster_id="PROSPECTIVE_VALIDATION",
            canonical_answer="yes",
            support_answers=("yes",),
            contradiction_answers=("no",),
            behavioral_statements=("Prospective validation observation.",),
            mapping_ids=("MAP-TEST-V03",),
        )
        return freeze.model_copy(update={"dimensions": (*freeze.dimensions, validation_prediction)})


def _service(tmp_path: Path) -> ParticipantSessionService:
    return ParticipantSessionService(
        store=ParticipantSessionStore(tmp_path / "sessions"),
        backend=FakeParticipantBackend(),
    )


def _new_session(service: ParticipantSessionService) -> str:
    record = service.create_session(
        BirthIntake(
            local_datetime=datetime(1994, 1, 28, 0, 35),
            birthplace="Istanbul",
            iana_timezone="UTC",
            mode=SessionMode.SCIENTIFIC_BLIND,
        )
    )
    return record.session_id


def _behavior(
    question_id: str,
    answer: str | None,
    *,
    narrative: str,
) -> EvidenceInput:
    return EvidenceInput(
        domain=EvidenceDomain.BEHAVIOR,
        question_id=question_id,
        answer=answer,
        behavioral_confidence=0.9,
        measurement_reliability=0.9,
        narrative=narrative,
        minimum_evidence_passed=True,
        consistency_status=EvidenceConsistency.CONSISTENT,
        quality_rationale="The response meets the frozen test minimum and fits prior evidence.",
    )


def _seed_historical_lock(
    service: ParticipantSessionService,
    session_id: str,
) -> tuple[ConfirmatoryLock, RankingSnapshot]:
    """Create a pre-repair diagnostic lock without authorizing repaired-protocol lock."""

    records = tuple(
        record
        for record in service.store.load_evidence(session_id)
        if record.phase == "confirmatory_blind"
    )
    responses = service._latest_scoreable_responses(records)
    lock = ConfirmatoryLock(
        schema_version="participant-confirmatory-lock-v2",
        session_id=session_id,
        locked_at_utc=datetime.now(UTC),
        evidence_ids=tuple(record.evidence_id for record in records),
        scoring_responses=responses,
        scoring_responses_sha256=sha256_bytes(canonical_json_bytes(responses)),
        excluded_non_natal_evidence_count=sum(
            not record.evidence.domain.natal_ranking_eligible for record in records
        ),
    )
    ranking = service._calculate_ranking(session_id, responses, analysis_kind="pre_reveal")
    service.store.write_confirmatory_lock(lock)
    service.store.write_confirmatory_ranking(ranking)
    return lock, ranking


def _seed_historical_result(
    service: ParticipantSessionService,
    session_id: str,
) -> RevealReport:
    """Persist an already-created historical diagnostic result for compatibility tests."""

    _, ranking = _seed_historical_lock(service, session_id)
    freeze = service.store.load_freeze(session_id)
    session = service.store.load_session(session_id)
    report = RevealReport(
        session_id=session_id,
        revealed_at_utc=datetime.now(UTC),
        birth=freeze.birth,
        chart=freeze.chart,
        confirmatory_ranking=ranking,
        prediction_comparisons=service._prediction_comparisons(
            freeze,
            service.store.load_evidence(session_id),
        ),
        model_receipt=ParticipantModelReceipt(
            prediction_freeze_sha256=session.prediction_freeze_sha256,
            code_commit=freeze.code_commit,
            engine_fingerprint=freeze.engine_fingerprint,
            model_version=freeze.model_version,
            model_sha256=freeze.model_sha256,
            mapping_sha256=freeze.mapping_sha256,
            question_bank_version=freeze.question_bank_version,
            question_bank_sha256=freeze.question_bank_sha256,
            ranking_scope=freeze.ranking_scope,
            candidate_universe_sha256=freeze.candidate_universe_sha256,
            candidate_universe_state_count=freeze.candidate_universe_state_count,
        ),
    )
    service.store.write_reveal(report)
    return report


def test_prediction_is_frozen_before_answers_and_progress_conceals_true_rank(
    tmp_path: Path,
) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    freeze_path = tmp_path / "sessions" / session_id / "prediction.freeze.json"
    before = sha256_file(freeze_path)

    opening = service.next_question(session_id)
    assert opening.question_id is None
    service.append_evidence(session_id, _behavior("Q1", "no", narrative="Usually no."))
    progress = service.public_progress(session_id)

    assert progress.true_birth_rank_concealed is True
    assert "true_state_rank" not in progress.model_dump()
    assert "true_date_rank" not in progress.model_dump()
    assert progress.mapped_scoreable_coverage == 0.5
    assert progress.mapped_scoreable_question_count == 2
    assert progress.adequately_assessed_mapped_question_count == 1
    assert progress.completion_policy_status == "UNRESOLVED_OWNER_AUTHORITY"
    assert progress.completion_policy_id is None
    assert progress.completion_required_question_count is None
    assert progress.completion_coverage is None
    assert progress.completion_authority_source_ref is None
    assert sha256_file(freeze_path) == before


def test_mapped_counts_are_descriptive_not_required(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "yes", narrative="Adequate Q1."))
    payload = service.public_progress(session_id).model_dump(mode="json")

    assert payload["mapped_scoreable_question_count"] == 2
    assert payload["adequately_assessed_mapped_question_count"] == 1
    assert payload["mapped_scoreable_coverage"] == 0.5
    assert "required_confirmatory_question_count" not in payload
    assert "adequately_assessed_coverage" not in payload
    assert "unresolved_question_count" not in payload


def test_unresolved_policy_has_null_required_count_and_coverage(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    progress = service.public_progress(session_id)

    assert progress.completion_policy_status == "UNRESOLVED_OWNER_AUTHORITY"
    assert progress.completion_policy_id is None
    assert progress.completion_required_question_count is None
    assert progress.completion_coverage is None
    assert progress.completion_authority_source_ref is None


def test_client_model_rejects_cluster_id() -> None:
    with pytest.raises(ValidationError, match="cluster_id"):
        EvidenceInput.model_validate(
            {
                "domain": "behavior",
                "narrative": "Client data cannot choose a hidden binding.",
                "cluster_id": "INJECTED",
            }
        )


@pytest.mark.parametrize(
    "field",
    ["resolved_cluster_id", "frozen_cluster_id", "frozen_dimension_ref"],
)
def test_client_model_rejects_resolved_cluster_aliases(field: str) -> None:
    with pytest.raises(ValidationError, match=field):
        EvidenceInput.model_validate(
            {
                "domain": "behavior",
                "narrative": "Client data cannot choose a hidden binding.",
                field: "INJECTED",
            }
        )


def test_unbound_narrative_remains_readable_and_nonscoreable(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)

    record = service.append_evidence(
        session_id,
        EvidenceInput(
            domain=EvidenceDomain.BEHAVIOR,
            narrative="A recurring pattern described before a mapped question is selected.",
        ),
    )

    assert record.evidence.narrative.startswith("A recurring pattern")
    assert record.evidence.frozen_dimension_binding is None
    assert record.evidence.scoring_response() is None


def test_unreceipted_legacy_answer_remains_readable_but_is_not_scoreable() -> None:
    evidence = StoredEvidenceInput(
        domain=EvidenceDomain.BEHAVIOR,
        question_id="Q1",
        cluster_id="DECISION",
        answer="yes",
        narrative="A legacy answer remains readable.",
    )

    assert evidence.scoring_response() is None


def test_server_resolves_cluster_from_session_freeze(
    tmp_path: Path,
) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    record = service.append_evidence(
        session_id,
        _behavior("Q2", "yes", narrative="Q2 evidence."),
    )

    binding = record.evidence.frozen_dimension_binding
    assert binding is not None
    assert binding.question_id == "Q2"
    assert binding.resolved_cluster_id == "LEARNING"
    assert binding.dimension_index == 1


def test_server_binding_records_exact_freeze_identity(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    record = service.append_evidence(
        session_id,
        _behavior("Q2", "yes", narrative="Q2 evidence."),
    )
    binding = record.evidence.frozen_dimension_binding

    assert binding is not None
    assert binding.freeze_ref.session_id == session_id
    assert binding.freeze_ref.freeze_sha256 == (
        service.store.load_session(session_id).prediction_freeze_sha256
    )


def test_persisted_scoreable_evidence_uses_server_resolved_cluster(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(
        session_id,
        _behavior("Q2", "yes", narrative="Q2 evidence."),
    )
    persisted = service.store.load_evidence(session_id)[0]
    response = persisted.evidence.scoring_response()
    assert response is not None
    assert response.cluster_id == "LEARNING"


def test_null_answer_can_be_adequately_assessed_without_becoming_scoreable(
    tmp_path: Path,
) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    record = service.append_evidence(
        session_id,
        _behavior("Q2", None, narrative="No frozen answer fits Q2."),
    )
    progress = service.public_progress(session_id)

    assert record.evidence.frozen_dimension_binding is not None
    assert record.evidence.scoring_response() is None
    assert progress.adequately_assessed_mapped_question_count == 1
    assert progress.scoreable_observation_count == 0
    assert progress.mapped_scoreable_coverage == 0.0


class AmbiguousParticipantBackend(FakeParticipantBackend):
    def build_prediction_freeze(
        self,
        *,
        session_id: str,
        birth: ResolvedBirth,
        ranking_scope: RankScope,
        created_at_utc: datetime,
    ) -> PredictionFreeze:
        freeze = super().build_prediction_freeze(
            session_id=session_id,
            birth=birth,
            ranking_scope=ranking_scope,
            created_at_utc=created_at_utc,
        )
        return freeze.model_copy(update={"dimensions": (*freeze.dimensions, freeze.dimensions[0])})


class MismatchedParticipantBackend(FakeParticipantBackend):
    def assert_freeze_compatible(self, freeze: PredictionFreeze) -> None:
        raise FrozenRuntimeMismatchError(
            f"session {freeze.session_id} was frozen by a different runtime bundle"
        )


def test_missing_frozen_question_binding_fails_closed(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)

    with pytest.raises(ParticipantProtocolError) as captured:
        service.append_evidence(
            session_id,
            _behavior("Q-MISSING", "yes", narrative="Unknown frozen question."),
        )

    assert captured.value.code == "FROZEN_QUESTION_BINDING_MISSING"
    assert service.store.load_evidence(session_id) == ()


def test_ambiguous_frozen_question_binding_fails_closed(tmp_path: Path) -> None:
    service = ParticipantSessionService(
        store=ParticipantSessionStore(tmp_path / "sessions"),
        backend=AmbiguousParticipantBackend(),
    )
    session_id = _new_session(service)

    with pytest.raises(ParticipantProtocolError) as captured:
        service.append_evidence(session_id, _behavior("Q1", "yes", narrative="Ambiguous."))

    assert captured.value.code == "FROZEN_QUESTION_BINDING_AMBIGUOUS"
    assert service.store.load_evidence(session_id) == ()


def test_lock_fails_when_completion_policy_is_unresolved(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "yes", narrative="Adequate Q1."))
    service.append_evidence(session_id, _behavior("Q2", None, narrative="Adequate Q2."))

    with pytest.raises(ParticipantProtocolError) as lock_error:
        service.lock_confirmatory(session_id)
    assert lock_error.value.code == "SCIENTIFIC_COMPLETENESS_POLICY_UNRESOLVED"


def test_reveal_cannot_bypass_unresolved_completion_policy(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "yes", narrative="Adequate Q1."))
    _seed_historical_lock(service, session_id)
    with pytest.raises(ParticipantProtocolError) as reveal_error:
        service.reveal(session_id)
    assert reveal_error.value.code == "SCIENTIFIC_COMPLETENESS_POLICY_UNRESOLVED"


def test_neither_23_nor_76_populates_completion_policy(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    policy = service.store.load_completion_policy(session_id)

    assert policy is not None
    assert policy.status == "UNRESOLVED_OWNER_AUTHORITY"
    assert policy.required_question_ids is None
    assert policy.policy_id is None
    assert policy.authority_source_ref is None
    assert policy.policy_digest is None


def test_source_or_protocol_mismatch_blocks_conforming_reuse(tmp_path: Path) -> None:
    service = ParticipantSessionService(
        store=ParticipantSessionStore(tmp_path / "sessions"),
        backend=MismatchedParticipantBackend(),
    )
    session_id = _new_session(service)

    with pytest.raises(FrozenRuntimeMismatchError, match="different runtime bundle"):
        service.append_evidence(
            session_id,
            _behavior("Q1", "yes", narrative="Must not reuse a mismatched freeze."),
        )

    assert service.store.load_evidence(session_id) == ()


def test_fabricated_authorized_policy_cannot_manufacture_completion(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    path = tmp_path / "sessions" / session_id / "completion.policy.json"
    fabricated = CompletionPolicySnapshot(
        status=CompletionPolicyStatus.AUTHORIZED,
        policy_id="FABRICATED",
        authority_source_ref="self-asserted-owner",
        required_question_ids=("Q1",),
        policy_digest="a" * 64,
    )
    path.write_bytes(canonical_json_bytes(fabricated))

    with pytest.raises(ParticipantProtocolError, match="cannot be verified") as progress_error:
        service.public_progress(session_id)
    assert progress_error.value.code == "SCIENTIFIC_COMPLETENESS_POLICY_UNRESOLVED"
    with pytest.raises(ParticipantProtocolError) as lock_error:
        service.lock_confirmatory(session_id)
    assert lock_error.value.code == "SCIENTIFIC_COMPLETENESS_POLICY_UNRESOLVED"


def test_validation_phase_evidence_cannot_enter_initial_rank_or_comparison(
    tmp_path: Path,
) -> None:
    service = ParticipantSessionService(
        store=ParticipantSessionStore(tmp_path / "sessions"),
        backend=PhasedParticipantBackend(),
    )
    session_id = _new_session(service)
    service.append_evidence(
        session_id,
        _behavior("V03", "yes", narrative="Premature prospective validation evidence."),
    )
    service.append_evidence(session_id, _behavior("Q1", "yes", narrative="Q1 evidence."))
    service.append_evidence(session_id, _behavior("Q2", "yes", narrative="Q2 evidence."))

    progress = service.public_progress(session_id)
    assert progress.scoreable_observation_count == 2
    assert progress.mapped_scoreable_coverage == 1.0
    assert progress.adequately_assessed_mapped_question_count == 2

    lock, _ = _seed_historical_lock(service, session_id)
    assert [response.question_id for response in lock.scoring_responses] == ["Q1", "Q2"]
    freeze = service.store.load_freeze(session_id)
    comparisons = service._prediction_comparisons(
        freeze,
        service.store.load_evidence(session_id),
    )
    validation_comparison = next(item for item in comparisons if item.question_id == "V03")
    assert validation_comparison.observed_answer is None
    assert validation_comparison.evidence_id is None
    assert validation_comparison.classification == "insufficient_evidence"


def test_outcomes_are_retained_but_excluded_from_natal_confirmatory_rank(
    tmp_path: Path,
) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "no", narrative="Stable pattern."))
    service.append_evidence(
        session_id,
        EvidenceInput(
            domain=EvidenceDomain.OUTCOME,
            narrative="I changed careers three times.",
        ),
    )

    lock, _ = _seed_historical_lock(service, session_id)
    assert [response.question_id for response in lock.scoring_responses] == ["Q1"]
    assert lock.excluded_non_natal_evidence_count == 1


def test_later_other_neutralizes_an_earlier_forced_choice_before_lock(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "no", narrative="First approximation."))
    service.append_evidence(
        session_id,
        _behavior(
            "Q1",
            None,
            narrative="Neither option fits; it reverses by context.",
        ),
    )
    service.append_evidence(session_id, _behavior("Q2", "yes", narrative="Q2 remains clear."))

    responses = service._latest_scoreable_responses(service.store.load_evidence(session_id))
    assert [response.question_id for response in responses] == ["Q2"]


def test_posthoc_profile_gets_separate_exploratory_rank_without_rewriting_blind_rank(
    tmp_path: Path,
) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "no", narrative="Initial self-report."))
    reveal = _seed_historical_result(service, session_id)
    assert reveal.confirmatory_ranking.true_state_rank == 7.0
    assert reveal.confirmatory_ranking.scientific_status == "confirmatory_blind"
    assert reveal.schema_version == "participant-reveal-v2"
    assert reveal.model_receipt is not None
    assert reveal.model_receipt.prediction_freeze_sha256 == (
        service.store.load_session(session_id).prediction_freeze_sha256
    )
    assert reveal.model_receipt.model_version == "test-model"
    assert reveal.model_receipt.candidate_universe_state_count == 12

    service.append_evidence(
        session_id,
        _behavior(
            "Q1",
            "yes",
            narrative="After examining contexts, yes is the better holistic description.",
        ),
    )
    final = service.finalize_exploratory(session_id)

    assert final.confirmatory.confirmatory_ranking.true_state_rank == 7.0
    assert final.exploratory.ranking.true_state_rank == 1.0
    assert final.exploratory.ranking.scientific_status == "posthoc_exploratory_not_independent"
    assert final.exploratory.changed_question_ids == ("Q1",)
    assert "not independent" in final.exploratory.disclaimer


def test_interviewer_reveal_redacts_birth_and_raw_chart(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "yes", narrative="Stable."))
    sensitive = _seed_historical_result(service, session_id)

    config = NatalPilotConfig(
        invite_token_sha256="a" * 64,
        invite_state_root=tmp_path / "invites",
        health_probe_root=tmp_path / "health",
        public_base_url="https://example.test",
        interviewer_url="https://chatgpt.com/g/test",
        interviewer_model_receipt="custom-gpt-test:gpt-5.6",
        action_schema_template="openapi: 3.1.0",
        runtime_receipt={
            "interviewer_instructions_sha256": "b" * 64,
            "interviewer_action_schema_sha256": "c" * 64,
        },
    )
    public = _interviewer_reveal(sensitive, config)
    payload = public.model_dump(mode="json")

    assert "birth" not in payload
    assert "chart" not in payload
    assert payload["trusted_result_url"] == "https://example.test/astrohd/result"
    assert payload["interviewer_model_receipt"] == "custom-gpt-test:gpt-5.6"
    assert payload["prediction_comparisons"]


def test_legacy_session_remains_readable_and_diagnostic(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "yes", narrative="Legacy."))
    created = _seed_historical_result(service, session_id)
    path = tmp_path / "sessions" / session_id / "reveal.json"
    legacy = created.model_dump(mode="json")
    legacy["schema_version"] = "participant-reveal-v1"
    legacy.pop("model_receipt")
    path.write_bytes(canonical_json_bytes(legacy))
    (tmp_path / "sessions" / session_id / "completion.policy.json").unlink()
    before = path.read_bytes()

    with pytest.raises(ParticipantProtocolError) as ordinary_reveal:
        service.reveal(session_id)
    assert ordinary_reveal.value.code == "SCIENTIFIC_COMPLETENESS_POLICY_UNRESOLVED"

    loaded = service.load_historical_diagnostic_reveal(session_id)

    assert loaded is not None
    assert loaded.schema_version == "participant-reveal-v1"
    assert loaded.model_receipt is None
    assert path.read_bytes() == before


def test_legacy_evidence_is_not_silently_migrated(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    legacy = EvidenceRecord(
        schema_version="participant-evidence-v2",
        evidence_id="EV-LEGACY",
        session_id=session_id,
        phase="confirmatory_blind",
        created_at_utc=datetime.now(UTC),
        evidence=StoredEvidenceInput(
            domain=EvidenceDomain.BEHAVIOR,
            question_id="Q1",
            cluster_id="DECISION",
            answer="yes",
            narrative="Historical client-authored cluster remains diagnostic only.",
        ),
    )
    service.store.append_evidence(legacy)
    log_path = tmp_path / "sessions" / session_id / "evidence.events.jsonl"
    before = log_path.read_bytes()

    loaded = service.store.load_evidence(session_id)[0]

    assert loaded.evidence.cluster_id == "DECISION"
    assert loaded.evidence.frozen_dimension_binding is None
    assert loaded.evidence.scoring_response() is None
    assert log_path.read_bytes() == before


def test_participant_store_uses_private_permissions(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "yes", narrative="Private."))
    directory = tmp_path / "sessions" / session_id

    assert directory.stat().st_mode & 0o777 == 0o700
    for name in (
        "session.json",
        "prediction.freeze.json",
        "completion.policy.json",
        "evidence.events.jsonl",
        ".evidence.lock",
    ):
        assert (directory / name).stat().st_mode & 0o777 == 0o600


def test_posthoc_other_can_remove_a_confirmatory_dimension_from_final_profile(
    tmp_path: Path,
) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "no", narrative="Initial answer."))
    service.append_evidence(session_id, _behavior("Q2", "yes", narrative="Stable Q2."))
    _seed_historical_result(service, session_id)
    service.append_evidence(
        session_id,
        _behavior(
            "Q1",
            None,
            narrative="Post-reveal review: neither answer captures this dimension.",
        ),
    )

    final = service.finalize_exploratory(session_id)
    assert [response.question_id for response in final.exploratory.final_profile_responses] == [
        "Q2"
    ]
    assert final.exploratory.changed_question_ids == ("Q1",)


def test_evidence_log_hash_chain_detects_tampering(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "no", narrative="Original."))
    log_path = tmp_path / "sessions" / session_id / "evidence.events.jsonl"
    raw = log_path.read_text(encoding="utf-8")
    log_path.write_text(raw.replace("Original.", "Tampered."), encoding="utf-8")

    with pytest.raises(SessionStorageError, match="digest"):
        service.store.load_evidence(session_id)
