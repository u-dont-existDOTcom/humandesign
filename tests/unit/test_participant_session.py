from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from hdmatch.experiments.canonical import sha256_file
from hdmatch.participant.backend import DiscriminationDiagnostics, SelectedQuestion
from hdmatch.participant.models import (
    BirthIntake,
    EvidenceDomain,
    EvidenceInput,
    PredictionDimension,
    PredictionFreeze,
    RankScope,
    RankingSnapshot,
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
    assert sha256_file(freeze_path) == before


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
    assert [response.question_id for response in final.exploratory.final_profile_responses] == ["Q2"]
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
