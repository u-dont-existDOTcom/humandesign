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


def test_health_declares_client_side_measurement_freeze() -> None:
    app = create_life_patterns_v2_owner_recoverability_app(
        model=RecoverabilityUIModel()  # type: ignore[arg-type]
    )
    health_route = next(route for route in app.routes if getattr(route, "path", None) == "/healthz")
    payload = health_route.endpoint()

    assert payload["client_side_measurement_freeze"] is True
    assert payload["target_theory_blind"] is True
