from __future__ import annotations

import pytest

from hdmatch.api.life_patterns_v2_owner_app import PatternAdjudicationRequest
from hdmatch.api.life_patterns_v2_owner_dynamic_ui import DYNAMIC_RECOVERABILITY_HTML
from hdmatch.api.life_patterns_v2_owner_recoverability import RecoverabilityCoverageSession
from hdmatch.api.life_patterns_v2_owner_scope import (
    TransactionalRecoverabilityCoverageSession,
    create_life_patterns_v2_owner_scope_app,
)


class MinimalModel:
    configured = True


def test_finalization_rolls_back_if_post_decision_work_fails(monkeypatch) -> None:
    session = TransactionalRecoverabilityCoverageSession(
        session_id="OWNER-TEST",
        model=MinimalModel(),  # type: ignore[arg-type]
    )
    session.core.active_proposal_id = "PROP-ORIGINAL"
    original_record = session.core.record

    def fail_after_mutation(self, request):
        del request
        self.core.record = self.core.record.model_copy(
            update={"source_archive_sha256": "1" * 64}
        )
        self.core.active_proposal_id = "PROP-HALF-COMMITTED"
        raise RuntimeError("coverage assessment failed after decision")

    monkeypatch.setattr(RecoverabilityCoverageSession, "adjudicate", fail_after_mutation)

    with pytest.raises(RuntimeError, match="coverage assessment failed"):
        session.adjudicate(PatternAdjudicationRequest(decision="accept"))

    assert session.core.record == original_record
    assert session.core.active_proposal_id == "PROP-ORIGINAL"


def test_successful_finalization_closes_active_proposal(monkeypatch) -> None:
    session = TransactionalRecoverabilityCoverageSession(
        session_id="OWNER-TEST",
        model=MinimalModel(),  # type: ignore[arg-type]
    )
    session.core.active_proposal_id = "PROP-ORIGINAL"

    def succeed(self, request):
        del self, request
        return {"status": "accepted", "wording": "A settled pattern."}

    monkeypatch.setattr(RecoverabilityCoverageSession, "adjudicate", succeed)

    result = session.adjudicate(PatternAdjudicationRequest(decision="accept"))

    assert result["status"] == "accepted"
    assert session.core.active_proposal_id is None


def test_scope_app_uses_transactional_sessions() -> None:
    app = create_life_patterns_v2_owner_scope_app()
    runtime = app.state.recoverability_runtime

    session = runtime.create_session()

    assert isinstance(session, TransactionalRecoverabilityCoverageSession)
    assert app.state.transactional_pattern_finalization is True


def test_synthesis_choices_have_one_clear_investigation_path() -> None:
    html = DYNAMIC_RECOVERABILITY_HTML

    assert '>Keep investigating</button>' in html
    assert 'id="reject" class="danger hidden"' in html
    assert "If you already know what is wrong or missing, type it in the chat box below." in html
    assert "bubble('user','Keep investigating.');" in html
    assert "window.__patternDecisionPending" in html


def test_post_acceptance_flow_defaults_to_finite_continue_interview() -> None:
    html = DYNAMIC_RECOVERABILITY_HTML

    assert '<button id="continueCoverage">Continue interview</button>' in html
    assert 'id="exploreAnother" class="hidden"' in html
    assert "rather than opening an unlimited sequence of extra pattern threads" in html
