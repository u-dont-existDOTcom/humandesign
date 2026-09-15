from __future__ import annotations

from hdmatch.api.life_patterns_v2_owner_recoverability import (
    create_life_patterns_v2_owner_recoverability_app,
)
from hdmatch.api.life_patterns_v2_owner_recoverability_ui import RECOVERABILITY_HTML


class RecoverabilityUIModel:
    configured = True


def test_recoverability_ui_exports_frozen_measurement_locally() -> None:
    assert "Freeze/export measurement" in RECOVERABILITY_HTML
    assert "life-patterns-owner-measurement-bundle-v1" in RECOVERABILITY_HTML
    assert "crypto.subtle.digest('SHA-256'" in RECOVERABILITY_HTML
    assert "measurement_bundle_sha256" in RECOVERABILITY_HTML
    assert "life-patterns-measurement-${digest.slice(0,12)}.json" in RECOVERABILITY_HTML
    assert "freeze_payload_sha256:p.freeze_payload_sha256" in RECOVERABILITY_HTML


def test_synthesis_review_keeps_free_form_chat_available() -> None:
    assert "The buttons are shortcuts; if none says what you mean, type it in the chat box below." in RECOVERABILITY_HTML
    assert "Close — I’ll explain what needs changing" in RECOVERABILITY_HTML
    assert "Edit exact wording myself" in RECOVERABILITY_HTML
    assert "Or explain what fits, what does not, or what the buttons miss…" in RECOVERABILITY_HTML
    assert "if(refiningPattern){show('composer')}else{hide('composer')}" not in RECOVERABILITY_HTML


def test_exact_wording_revision_is_explicit_and_reversible() -> None:
    assert "← Back to synthesis choices" in RECOVERABILITY_HTML
    assert "Use this editor only if you want to write the exact replacement pattern yourself." in RECOVERABILITY_HTML
    assert "What exact replacement wording should be recorded?" in RECOVERABILITY_HTML
    assert "Does the evidence already discussed in this thread support that exact wording?" in RECOVERABILITY_HTML
    assert "You are about to record the exact wording above. What status should it have?" in RECOVERABILITY_HTML
    assert "Accept this wording" in RECOVERABILITY_HTML
    assert "Leave this wording unresolved" in RECOVERABILITY_HTML
    assert "$('backFromRevise').onclick" in RECOVERABILITY_HTML


def test_free_form_feedback_closes_stale_exact_wording_form() -> None:
    assert "hide('reviseBox');hide('finalChoice');groundingChoice=null" in RECOVERABILITY_HTML
    assert "document.querySelectorAll('.grounding').forEach(b=>b.disabled=false)" in RECOVERABILITY_HTML


def test_health_declares_client_side_measurement_freeze() -> None:
    app = create_life_patterns_v2_owner_recoverability_app(
        model=RecoverabilityUIModel()  # type: ignore[arg-type]
    )
    health_route = next(route for route in app.routes if getattr(route, "path", None) == "/healthz")
    payload = health_route.endpoint()

    assert payload["client_side_measurement_freeze"] is True
    assert payload["target_theory_blind"] is True
