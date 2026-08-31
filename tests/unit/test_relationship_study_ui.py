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
    assert "Resume a saved study by email" in HTML
    assert "/api/study/recovery/request" in HTML
    assert "/api/study/recovery/verify" in HTML
    assert "single-use magic link and six-digit code" in HTML
    assert "onclick=\"begin()\"" not in HTML
    assert "OpenRouter" not in HTML


def test_birth_time_uses_explicit_numeric_fields_instead_of_native_time_control() -> None:
    assert 'type="time"' not in HTML
    for role in ("a", "b"):
        assert f'id="{role}BirthHour" type="text" inputmode="numeric"' in HTML
        assert f'id="{role}BirthMinute" type="text" inputmode="numeric"' in HTML
        assert f'id="{role}BirthTimeError"' in HTML
    assert "return String(hour).padStart(2,'0')+':'+String(minute).padStart(2,'0')+':00'" in HTML


def test_birth_time_validation_is_role_specific_and_accessible() -> None:
    assert "role==='a'?'your':\"the other person's\"" in HTML
    assert "birth hour and minute, or mark the time unknown" in HTML
    assert "birth hour from 00 to 23" in HTML
    assert "birth minute from 00 to 59" in HTML
    assert "error.classList.remove('hidden')" in HTML
    assert "document.getElementById(role+suffix).focus()" in HTML
    assert 'role="alert" aria-live="polite"' in HTML


def test_unknown_time_disables_both_numeric_time_fields_without_erasing_them() -> None:
    assert "document.getElementById(role+'BirthHour').disabled=unknown" in HTML
    assert "document.getElementById(role+'BirthMinute').disabled=unknown" in HTML
    assert "document.getElementById(role+'BirthHour').value=" not in HTML
    assert "document.getElementById(role+'BirthMinute').value=" not in HTML
