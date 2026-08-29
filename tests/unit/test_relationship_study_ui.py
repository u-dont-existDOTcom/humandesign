from __future__ import annotations

from hdmatch.api.relationship_study_ui_enhanced import HTML


def test_confirmatory_ui_requires_birth_intake_and_hides_hash_as_technical_receipt() -> None:
    assert "Seal prediction &amp; begin questionnaire" in HTML
    assert "/api/study/intake" in HTML
    assert "/api/study/places" in HTML
    assert "The questionnaire AI never sees the birth data or hidden prediction" in HTML
    assert "Technical audit receipt" in HTML
    assert "You do not need to save this hash" in HTML
    assert "Reveal the blinded Astro/HD prediction" in HTML
    assert "Start a new relationship" in HTML
    assert "existing private frozen record will not be deleted" in HTML
    assert "onclick=\"begin()\"" not in HTML
    assert "OpenRouter" not in HTML
