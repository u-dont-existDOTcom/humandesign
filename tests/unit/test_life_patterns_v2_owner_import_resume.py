from __future__ import annotations

from hdmatch.api.life_patterns_v2_owner_app import PatternAdjudicationRequest
from hdmatch.api.life_patterns_v2_owner_conversation import ConversationMove
from hdmatch.api.life_patterns_v2_owner_import_resume import (
    _rebuild_visible_transcript_working_ledger,
    create_life_patterns_v2_owner_import_resume_app,
)
from hdmatch.api.life_patterns_v2_owner_import_resume_ui import IMPORT_RESUME_RECOVERABILITY_HTML
from hdmatch.api.life_patterns_v2_owner_persistent import PersistentRecoverabilityCoverageSession


class MinimalModel:
    configured = True

    def plan_turn(self, **kwargs):
        facts = kwargs["operative_facts"]
        assert len(facts) >= 2
        return ConversationMove(
            reply=(
                "A recovered tentative pattern is that your attention can become strongly invested "
                "in whatever currently matters, while you still report being able to shift away."
            ),
            move_type="surface_hypothesis",
            hypothesis_proposition=(
                "The participant reports becoming strongly invested in what currently matters while "
                "also reporting an ability to shift away when circumstances change."
            ),
            evidence_fact_ids=(facts[0].fact_id, facts[1].fact_id),
        )


def _turns() -> list[dict[str, str]]:
    return [
        {"role": "assistant", "text": "What happens when something matters a lot to you?"},
        {"role": "user", "text": "I can get very absorbed in work or meditation."},
        {"role": "assistant", "text": "Can you shift away when circumstances change?"},
        {"role": "user", "text": "Yes, usually I can."},
    ]


def test_transcript_reconstruction_creates_explicitly_non_scientific_working_ledger() -> None:
    session = PersistentRecoverabilityCoverageSession(
        session_id="OWNER-IMPORT-TEST",
        model=MinimalModel(),  # type: ignore[arg-type]
    )
    session.visible_recovery_seed(_turns())

    result = _rebuild_visible_transcript_working_ledger(session)

    assert result["pattern_active"] is True
    assert result["reconstructed_from_visible_transcript"] is True
    assert result["scientific_freeze_eligible"] is False
    assert result["working_ledger_validation_status"] == "reconstructed_unvalidated"
    assert session.recovery_quality == "reconstructed_visible_transcript"
    assert len(session.core.record.episodes) == 2
    assert len(session.core.record.episode_facts) == 2
    assert session._draft_move is not None
    assert session.recovery_status()["workflow_phase"] == "synthesis_review"


def test_recovery_status_preserves_post_adjudication_workflow_phase() -> None:
    session = PersistentRecoverabilityCoverageSession(
        session_id="OWNER-IMPORT-SETTLED",
        model=MinimalModel(),  # type: ignore[arg-type]
    )
    session.visible_recovery_seed(_turns())
    _rebuild_visible_transcript_working_ledger(session)

    session.adjudicate(PatternAdjudicationRequest(decision="accept"))
    status = session.recovery_status()

    assert status["pattern_active"] is False
    assert status["workflow_phase"] == "post_adjudication"
    assert status["latest_adjudication_decision"] == "accept"
    assert status["latest_adjudication_wording"]


def test_import_resume_app_exposes_reconstruction_and_quality_preserving_restore_routes() -> None:
    app = create_life_patterns_v2_owner_import_resume_app()
    paths = [getattr(route, "path", None) for route in app.router.routes]
    assert "/api/owner-v2/conversation/sessions/{session_id}/reconstruct-visible" in paths
    assert paths.count("/api/owner-v2/conversation/sessions/restore") == 1
    assert app.state.transcript_only_import_has_explicit_continuation is True
    assert app.state.transcript_reconstruction_is_non_scientific is True
    assert app.state.reconstructed_recovery_quality_survives_reload is True


def test_import_ui_restores_actionable_workflow_phase_instead_of_blank_composer() -> None:
    html = IMPORT_RESUME_RECOVERABILITY_HTML
    assert "Recovered transcript" in html
    assert "Continue from this recovered interview" in html
    assert "Start a clean scientific interview" in html
    assert "/reconstruct-visible" in html
    assert "showRecoveredTranscriptActions" in html
    assert "reconstructed development ledger" in html
    assert "cannot become the clean scientific freeze" in html
    assert "p.recovery_quality==='visible_transcript_only'" in html
    assert "p.recovery_quality!=='exact_hidden_ledger')showRecoveredTranscriptActions" not in html
    assert "Recovered reconstructed development ledger · non-scientific" in html
    assert "renderRecoveredWorkflow(p)" in html
    assert "p&&p.workflow_phase==='post_adjudication'" in html
    assert "show('result');show('continuation')" in html
    assert "This settled state was restored from the saved interview checkpoint." in html
