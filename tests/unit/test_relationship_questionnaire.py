from pathlib import Path

import pytest

from hdmatch.relationship.questionnaire import (
    load_relationship_questionnaire,
    select_next_capture_question,
    select_next_validation_question,
)


QUESTIONNAIRE_PATH = Path("reference/relationship/relationship_dynamic_questionnaire_v1.json")


def test_relationship_questionnaire_loads_and_core_order_is_frozen() -> None:
    spec = load_relationship_questionnaire(QUESTIONNAIRE_PATH)
    assert spec.core_question_ids == (
        "RRQ_TRAJECTORY_CONTEXT",
        "RRQ_LOVE_EROS_DIRECTION",
        "RRQ_SEXUAL_SYSTEM",
        "RRQ_MIND_COMMUNICATION",
        "RRQ_EMOTIONAL_AUTONOMY",
        "RRQ_PRACTICAL_FUTURE",
    )
    first = select_next_capture_question(spec)
    assert first is not None
    assert first.id == "RRQ_TRAJECTORY_CONTEXT"


def test_capture_mode_asks_only_relevant_followup_after_core() -> None:
    spec = load_relationship_questionnaire(QUESTIONNAIRE_PATH)
    next_question = select_next_capture_question(
        spec,
        answered_question_ids=spec.core_question_ids,
        unresolved_axis_ids=("intellectual_stimulation_self_expansion",),
    )
    assert next_question is not None
    assert next_question.id == "RRQ_COGNITIVE_DECOMPOSITION"


def test_capture_mode_can_route_from_non_scored_applicability_flag() -> None:
    spec = load_relationship_questionnaire(QUESTIONNAIRE_PATH)
    next_question = select_next_capture_question(
        spec,
        answered_question_ids=spec.core_question_ids,
        applicability_flags=("sexual_boredom_reported",),
    )
    assert next_question is not None
    assert next_question.id == "RRQ_SEX_HABITUATION"


def test_validation_mode_reuses_adjusted_expected_information_gain() -> None:
    spec = load_relationship_questionnaire(QUESTIONNAIRE_PATH)
    selected = select_next_validation_question(
        spec,
        candidate_weights=(1.0, 1.0),
        likelihoods_by_question={
            "RRQ_TRAJECTORY_CONTEXT": (
                {"same": 1.0},
                {"same": 1.0},
            ),
            "RRQ_LOVE_EROS_DIRECTION": (
                {"left": 1.0},
                {"right": 1.0},
            ),
        },
    )
    assert selected is not None
    assert selected.question_id == "RRQ_LOVE_EROS_DIRECTION"
    assert selected.expected_information_gain == pytest.approx(1.0)


def test_validation_mode_does_not_ask_inapplicable_followup() -> None:
    spec = load_relationship_questionnaire(QUESTIONNAIRE_PATH)
    selected = select_next_validation_question(
        spec,
        candidate_weights=(1.0, 1.0),
        likelihoods_by_question={
            "RRQ_SEX_HABITUATION": (
                {"stable": 1.0},
                {"decline": 1.0},
            )
        },
    )
    assert selected is None


def test_unknown_answered_question_id_fails_closed() -> None:
    spec = load_relationship_questionnaire(QUESTIONNAIRE_PATH)
    with pytest.raises(KeyError):
        select_next_capture_question(spec, answered_question_ids=("NOT_A_REAL_QUESTION",))
