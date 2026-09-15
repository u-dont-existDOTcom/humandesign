from hdmatch.api.life_patterns_interview_ui import HTML


def test_ui_is_pattern_first_and_pending_examples_are_not_called_evidence() -> None:
    assert "This interview is mainly about recurring patterns" in HTML
    assert "Describe the pattern in your own words" in HTML
    assert "awaiting your factual review before it can count as evidence" in HTML
    assert "added to your evidence map" not in HTML
    assert "Think of a consequential decision or turning point" not in HTML
