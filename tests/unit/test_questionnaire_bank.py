from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.questionnaire.bank import QuestionBank, load_question_bank
from hdmatch.questionnaire.response import NormalizedResponse, normalize_answer_token

ROOT = Path(__file__).parents[2]


def test_normative_question_bank_is_complete_and_unique() -> None:
    bank = load_question_bank(ROOT / "reference/core/question_bank_v1.json")

    assert bank.version == "1.0.0"
    assert len(bank.questions) == 81
    assert len(bank.question_ids) == 81
    assert bank.by_id("D01").body_access_sensitive is True
    assert bank.by_id("T01").body_access_sensitive is False
    assert bank.by_id("R02").response_format_options == (
        "never",
        "rarely",
        "sometimes",
        "often",
        "very often",
    )


def test_question_bank_rejects_duplicate_ids() -> None:
    bank = load_question_bank(ROOT / "reference/core/question_bank_v1.json")
    payload = bank.model_dump(mode="json")
    payload["questions"].append(payload["questions"][0])

    with pytest.raises(ValidationError, match="duplicate question IDs"):
        QuestionBank.model_validate(payload)


def test_answer_token_normalization_is_mechanical() -> None:
    assert normalize_answer_token("A gut-like yes/no energy") == "a_gut_like_yes_no_energy"
    response = NormalizedResponse(
        question_id="d01",
        answer_token="an_immediate_quiet_sense",
        behavioral_confidence=0.75,
        measurement_reliability=0.5,
    )

    assert response.question_id == "D01"
    assert response.effective_confidence == pytest.approx(0.375)
