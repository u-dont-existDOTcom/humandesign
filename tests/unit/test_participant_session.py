from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from hdmatch.api.natal_pilot_app import NatalPilotConfig, _interviewer_reveal
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_file
from hdmatch.participant.backend import DiscriminationDiagnostics, SelectedQuestion
from hdmatch.participant.models import (
    BirthIntake,
    EvidenceConsistency,
    EvidenceDomain,
    EvidenceInput,
    PredictionDimension,
    PredictionFreeze,
    RankingSnapshot,
    RankScope,
    ResolvedBirth,
    SessionMode,
)
from hdmatch.participant.service import ParticipantSessionService, ParticipantStateError
from hdmatch.participant.store import ParticipantSessionStore, SessionStorageError
from hdmatch.questionnaire import Question
from hdmatch.schemas import BehavioralResponse, ChartFeatures, ScoredState
from hdmatch.search import QuestionUtility


class FakeParticipantBackend:
    scoreable_question_ids = frozenset({"Q1", "Q2"})
    required_confirmatory_question_ids = frozenset({"Q1", "Q2"})

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
    required_confirmatory_question_ids = frozenset({"Q1", "Q2"})

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
        return freeze.model_copy(
            update={"dimensions": (*freeze.dimensions, validation_prediction)}
        )


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
        cluster_id="DECISION",
        answer=answer,
        behavioral_confidence=0.9,
        measurement_reliability=0.9,
        narrative=narrative,
        minimum_evidence_passed=True,
        consistency_status=EvidenceConsistency.CONSISTENT,
        quality_rationale="The response meets the frozen test minimum and fits prior evidence.",
    )


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
    assert progress.scoreable_coverage == 0.5
    assert progress.required_confirmatory_question_count == 2
    assert progress.adequately_assessed_coverage == 0.5
    assert progress.unresolved_question_count == 1
    assert sha256_file(freeze_path) == before


def test_unreceipted_legacy_answer_remains_readable_but_is_not_scoreable() -> None:
    evidence = EvidenceInput(
        domain=EvidenceDomain.BEHAVIOR,
        question_id="Q1",
        cluster_id="DECISION",
        answer="yes",
        narrative="A legacy answer remains readable.",
    )

    assert evidence.scoring_response() is None


def test_owner_quality_gate_refuses_incomplete_profile_then_accepts_full_coverage(
    tmp_path: Path,
) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "no", narrative="Q1 evidence."))

    with pytest.raises(ParticipantStateError, match="1 frozen dimensions"):
        service.lock_confirmatory(session_id, require_complete_profile=True)

    service.append_evidence(session_id, _behavior("Q2", None, narrative="No option fits Q2."))
    progress = service.public_progress(session_id)
    assert progress.adequately_assessed_coverage == 1.0
    assert progress.scoreable_coverage == 0.5
    assert progress.unresolved_question_count == 0

    lock = service.lock_confirmatory(session_id, require_complete_profile=True)
    assert [response.question_id for response in lock.scoring_responses] == ["Q1"]
    assert lock.schema_version == "participant-confirmatory-lock-v2"
    assert lock.complete_profile_required is True
    assert lock.adequately_assessed_question_count == 2
    assert lock.required_question_count == 2
    assert lock.evidence_quality_contract_version == "astrohd-natal-evidence-quality-v1"


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
    assert progress.scoreable_question_count == 2
    assert progress.scoreable_coverage == 1.0
    assert progress.adequately_assessed_coverage == 1.0

    lock = service.lock_confirmatory(session_id, require_complete_profile=True)
    assert [response.question_id for response in lock.scoring_responses] == ["Q1", "Q2"]

    reveal = service.reveal(session_id)
    validation_comparison = next(
        item for item in reveal.prediction_comparisons if item.question_id == "V03"
    )
    assert validation_comparison.observed_answer is None
    assert validation_comparison.evidence_id is None
    assert validation_comparison.classification == "insufficient_evidence"

    service.append_evidence(
        session_id,
        _behavior("V03", "no", narrative="Post-reveal validation observation."),
    )
    final = service.finalize_exploratory(session_id)
    assert [response.question_id for response in final.exploratory.final_profile_responses] == [
        "Q1",
        "Q2",
    ]


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

    lock = service.lock_confirmatory(session_id)
    assert [response.question_id for response in lock.scoring_responses] == ["Q1"]
    assert lock.excluded_non_natal_evidence_count == 1
    with pytest.raises(ParticipantStateError):
        service.append_evidence(session_id, _behavior("Q2", "yes", narrative="Too late."))

    service.reveal(session_id)
    final = service.finalize_exploratory(session_id)
    assert len(final.retained_secondary_evidence) == 1
    assert final.retained_secondary_evidence[0].evidence.domain is EvidenceDomain.OUTCOME


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

    lock = service.lock_confirmatory(session_id)
    assert [response.question_id for response in lock.scoring_responses] == ["Q2"]


def test_posthoc_profile_gets_separate_exploratory_rank_without_rewriting_blind_rank(
    tmp_path: Path,
) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "no", narrative="Initial self-report."))
    service.lock_confirmatory(session_id)
    reveal = service.reveal(session_id)
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
    service.lock_confirmatory(session_id)
    sensitive = service.reveal(session_id)

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


def test_legacy_v1_reveal_remains_readable_without_rewriting_it(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "yes", narrative="Legacy."))
    service.lock_confirmatory(session_id)
    created = service.reveal(session_id)
    path = tmp_path / "sessions" / session_id / "reveal.json"
    legacy = created.model_dump(mode="json")
    legacy["schema_version"] = "participant-reveal-v1"
    legacy.pop("model_receipt")
    path.write_bytes(canonical_json_bytes(legacy))

    loaded = service.store.load_reveal(session_id)

    assert loaded is not None
    assert loaded.schema_version == "participant-reveal-v1"
    assert loaded.model_receipt is None
    assert path.read_bytes() == canonical_json_bytes(legacy)


def test_participant_store_uses_private_permissions(tmp_path: Path) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "yes", narrative="Private."))
    service.lock_confirmatory(session_id)
    directory = tmp_path / "sessions" / session_id

    assert directory.stat().st_mode & 0o777 == 0o700
    for name in (
        "session.json",
        "prediction.freeze.json",
        "evidence.events.jsonl",
        ".evidence.lock",
        "confirmatory.lock.json",
        "confirmatory.ranking.json",
    ):
        assert (directory / name).stat().st_mode & 0o777 == 0o600


def test_posthoc_other_can_remove_a_confirmatory_dimension_from_final_profile(
    tmp_path: Path,
) -> None:
    service = _service(tmp_path)
    session_id = _new_session(service)
    service.append_evidence(session_id, _behavior("Q1", "no", narrative="Initial answer."))
    service.append_evidence(session_id, _behavior("Q2", "yes", narrative="Stable Q2."))
    service.lock_confirmatory(session_id)
    service.reveal(session_id)
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
