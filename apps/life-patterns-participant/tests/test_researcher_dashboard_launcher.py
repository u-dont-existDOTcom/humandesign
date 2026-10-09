"""Owner-local researcher dashboard, credential hygiene and usable feedback."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from life_patterns_local_dashboard import (
    private_write,
    render_private_feedback,
)


def test_private_report_escapes_user_text_and_does_not_embed_credential(tmp_path):
    fake = [
        {
            "route_id": "G10",
            "issue_hint": "unclear",
            "status": "new",
            "question_text": "<b>Question?</b>",
            "feedback_text": '<script>alert("bad")</script>',
        }
    ]
    markup = render_private_feedback(fake)
    assert "1 feedback entries" in markup
    assert "&lt;script&gt;" in markup
    assert "<script>alert" not in markup
    assert "<b>Question?" not in markup
    assert "Authorization" not in markup
    output = tmp_path / "feedback.html"
    private_write(output, markup)
    assert (output.stat().st_mode & 0o777) == 0o600
    assert output.read_text() == markup


def test_private_browser_handoff(tmp_path, monkeypatch):
    import life_patterns_local_dashboard as viewer

    monkeypatch.setenv("XDG_RUNTIME_DIR", str(tmp_path))
    sample_key = "synthetic_nonproduction_key_0123456789"
    bridge = viewer.make_handoff(
        {"dashboard_url": "https://example.invalid"}, sample_key
    )
    try:
        assert bridge.stat().st_mode & 0o777 == 0o600
        assert bridge.parent.stat().st_mode & 0o777 == 0o700
        assert sample_key not in bridge.as_uri()
        assert sample_key in bridge.read_text()
    finally:
        bridge.unlink(missing_ok=True)
