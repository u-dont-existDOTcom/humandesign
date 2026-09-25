from __future__ import annotations

from hdmatch.api.life_patterns_v2_owner_liveness import create_life_patterns_v2_owner_liveness_app
from hdmatch.api.life_patterns_v2_owner_liveness_ui import LIVENESS_RECOVERABILITY_HTML


def test_recovery_loads_blueprint_before_rendering_restored_progress() -> None:
    html = LIVENESS_RECOVERABILITY_HTML
    assert "async function ensureCoverageBlueprint()" in html
    assert "await ensureCoverageBlueprint();\n  const snapshot=" in html
    assert "await ensureCoverageBlueprint();\n  const turns=" in html
    assert "Interview coverage blueprint did not load." in html
    assert "coverageBlueprint=b.domains||[]" in html


def test_long_operations_have_visible_liveness_feedback() -> None:
    html = LIVENESS_RECOVERABILITY_HTML
    assert 'id="operationStatus"' in html
    assert "Working on it…" in html
    assert "Saving that and updating interview progress…" in html
    assert "Rebuilding the recovered interview and preparing a synthesis…" in html
    assert "Choosing the next useful question…" in html
    assert "showWorking(" in html
    assert "hideWorking()" in html


def test_continue_interview_checks_real_blueprint_before_declaring_complete() -> None:
    html = LIVENESS_RECOVERABILITY_HTML
    marker = "$('continueCoverage').onclick=async()=>{"
    start = html.index(marker)
    end = html.index("};", start) + 2
    handler = html[start:end]
    assert "await ensureCoverageBlueprint();" in handler
    assert "const missing=incompleteCoverage();" in handler
    assert handler.index("await ensureCoverageBlueprint();") < handler.index(
        "const missing=incompleteCoverage();"
    )


def test_liveness_app_marks_participant_seam_guards() -> None:
    app = create_life_patterns_v2_owner_liveness_app()
    assert app.state.long_operation_feedback is True
    assert app.state.recovery_restores_coverage_blueprint is True
    assert app.state.progress_false_complete_guard is True
