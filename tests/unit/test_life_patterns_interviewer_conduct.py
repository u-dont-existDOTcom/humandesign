from __future__ import annotations

from hdmatch.api.life_patterns_interview_app import (
    _INTERVIEW_SYSTEM,
    _PARTICIPANT_HISTORY_MAX_CHARS_PER_TURN,
    _PARTICIPANT_HISTORY_MAX_TURNS,
    _RECENT_TURN_WINDOW,
    _participant_statement_index,
)


def test_interviewer_policy_is_pattern_first_neutral_and_selective() -> None:
    prompt = _INTERVIEW_SYSTEM
    folded = prompt.casefold()
    assert "pattern-first, evidence-anchored" in folded
    assert "follow-up gate" in folded
    assert "interaction mismatch / self-correction" in folded
    assert "never use motivational interviewing to evoke change talk" in folded
    assert "do not force a dated incident" in folded
    assert "do not ask the participant to restate information already supplied" in folded
    assert "prioritize a material unresolved ambiguity" in folded
    assert 'use "none_material"' in folded
    assert "prefer concrete episodes over global personality claims" not in folded


def test_participant_statement_index_keeps_older_user_answers_visible() -> None:
    turns: list[dict[str, object]] = []
    for index in range(_RECENT_TURN_WINDOW + 8):
        turns.append(
            {
                "turn_id": f"U-{index:03d}",
                "role": "user",
                "text": f"participant statement {index}",
            }
        )
        turns.append(
            {
                "turn_id": f"A-{index:03d}",
                "role": "assistant",
                "text": f"assistant response {index}",
            }
        )

    history = _participant_statement_index(turns)
    assert len(history) == _RECENT_TURN_WINDOW + 8
    assert history[0]["turn_id"] == "U-000"
    assert history[-1]["turn_id"] == f"U-{_RECENT_TURN_WINDOW + 7:03d}"
    assert all(str(row["turn_id"]).startswith("U-") for row in history)


def test_participant_statement_index_bounds_size_and_marks_truncation() -> None:
    turns = [
        {
            "turn_id": f"U-{index:03d}",
            "role": "user",
            "text": "x" * (_PARTICIPANT_HISTORY_MAX_CHARS_PER_TURN + 50),
        }
        for index in range(_PARTICIPANT_HISTORY_MAX_TURNS + 5)
    ]

    history = _participant_statement_index(turns)
    assert len(history) == _PARTICIPANT_HISTORY_MAX_TURNS
    assert history[0]["turn_id"] == "U-005"
    assert len(str(history[0]["text"])) == _PARTICIPANT_HISTORY_MAX_CHARS_PER_TURN
    assert all(row["text_truncated"] is True for row in history)
