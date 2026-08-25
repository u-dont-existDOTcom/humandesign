from __future__ import annotations

import pytest

from hdmatch.schemas import BehavioralResponse


def test_behavioral_response_preserves_period_context_and_nuance() -> None:
    response = BehavioralResponse(
        question_id="social.pattern",
        cluster_id="social-style",
        answer="selective-currently",
        behavioral_confidence=0.8,
        measurement_reliability=0.75,
        period_answers={
            "childhood": "social-and-curious",
            "adolescence": "more-withdrawn",
            "current": "selective-currently",
        },
        context_answers={
            "trusted-private": "very-outgoing",
            "unfamiliar-group": "quiet-observer",
        },
        pattern_changed=True,
        change_period="adolescence",
        nuance_text="The shift depends strongly on whether the group feels safe.",
    )
    assert response.period_answers["childhood"] == "social-and-curious"
    assert response.context_answers["trusted-private"] == "very-outgoing"
    assert response.pattern_changed is True
    assert response.change_period == "adolescence"
    assert response.effective_confidence == pytest.approx(0.6)


def test_structured_behavioral_answers_reject_blank_keys_and_values() -> None:
    with pytest.raises(ValueError, match="cannot be blank"):
        BehavioralResponse(
            question_id="q",
            cluster_id="c",
            answer="a",
            behavioral_confidence=1.0,
            measurement_reliability=1.0,
            period_answers={"childhood": ""},
        )
