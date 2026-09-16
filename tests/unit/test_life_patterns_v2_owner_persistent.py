from __future__ import annotations

import pytest

from hdmatch.api.life_patterns_v2_owner_conversation import (
    ConversationMove,
    HiddenFactCandidate,
    TurnExtraction,
)
from hdmatch.api.life_patterns_v2_owner_persistent import (
    PersistentRecoverabilityCoverageSession,
)
from hdmatch.api.life_patterns_v2_owner_persistent_ui import PERSISTENT_RECOVERABILITY_HTML


class MinimalModel:
    configured = True


def _session() -> PersistentRecoverabilityCoverageSession:
    return PersistentRecoverabilityCoverageSession(
        session_id="OWNER-RECOVERY-TEST",
        model=MinimalModel(),  # type: ignore[arg-type]
    )


def test_exact_hidden_ledger_recovery_round_trip_preserves_draft_and_fact_ids() -> None:
    session = _session()
    session.pattern_focus_established = True
    session.conversation.append(
        {"turn_id": "TURN-1", "role": "user", "text": "I focus intensely on things that matter."}
    )
    session._apply_extraction(
        extraction=TurnExtraction(
            episode_summary="focus",
            facts=(
                HiddenFactCandidate(
                    assertion_type="reported_appraisal_or_belief",
                    proposition="The participant reports intense focus on things that matter.",
                ),
            ),
            corrections=(),
        ),
        turn_id="TURN-1",
        message="I focus intensely on things that matter.",
        start_new_episode=True,
    )
    fact_id = session.core.operative_facts()[0].fact_id
    session._create_pattern(
        ConversationMove(
            reply="A tentative pattern is that your attention becomes intense around what matters.",
            move_type="surface_hypothesis",
            hypothesis_proposition="The participant's attention becomes intense around what matters.",
            evidence_fact_ids=(fact_id,),
        )
    )
    session._last_progress_report = {
        "blueprint_version": "test",
        "assessments": [],
        "required_domain_count": 23,
        "complete_domain_count": 2,
    }

    snapshot = session.recovery_snapshot()
    restored = _session()
    restored.restore_recovery_snapshot(snapshot)

    assert restored.conversation == session.conversation
    assert restored.core.operative_facts()[0].fact_id == fact_id
    assert restored.core.operative_facts()[0].proposition == (
        "The participant reports intense focus on things that matter."
    )
    assert restored._draft_move is not None
    assert restored._draft_move.evidence_fact_ids == (fact_id,)
    assert restored._last_progress_report == session._last_progress_report
    assert restored.recovery_quality == "exact_hidden_ledger"


def test_recovery_checksum_rejects_modified_hidden_state() -> None:
    session = _session()
    snapshot = session.recovery_snapshot()
    snapshot["conversation"] = [{"turn_id": "X", "role": "user", "text": "tampered"}]

    with pytest.raises(ValueError, match="checksum"):
        _session().restore_recovery_snapshot(snapshot)


def test_visible_legacy_import_remains_explicitly_non_scientific() -> None:
    session = _session()
    session.visible_recovery_seed(
        [
            {"role": "assistant", "text": "Opening"},
            {"role": "user", "text": "A recovered answer"},
        ]
    )
    snapshot = session.recovery_snapshot()
    restored = _session()
    restored.restore_recovery_snapshot(snapshot)

    assert restored.recovery_quality == "visible_transcript_only"
    assert restored.recovery_status()["scientific_freeze_eligible"] is False
    assert restored.conversation[-1]["text"] == "A recovered answer"


def test_persistent_ui_has_exact_import_area_labels_and_action_scrolling() -> None:
    html = PERSISTENT_RECOVERABILITY_HTML
    assert "Import recovery JSON" in html
    assert "lifePatternsExactRecoveryV2" in html
    assert "/sessions/restore-visible" in html
    assert "/sessions/${encodeURIComponent(sessionId)}/recovery" in html
    assert "measurement areas still open" in html
    assert "questions left" not in html
    assert "These are measurement areas, not a question count." in html
    assert "overflow-y:scroll" in html
    assert "scrollToNextAction" in html
    assert "resumeOrStart();" in html
    assert "window.__lifePatternsTranscriptOnlyRecovery" in html
