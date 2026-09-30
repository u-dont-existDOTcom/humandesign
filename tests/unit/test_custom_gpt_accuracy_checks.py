"""Regression checks for Custom GPT claim-integrity instructions."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from hdmatch.relationship import llm_audit, phenotype_classifier

ROOT = Path(__file__).resolve().parents[2]
CUSTOM_GPT = ROOT / "reference" / "custom_gpt"
SHORT = "participant_interviewer_instructions_under_8000_v1.md"
LONG = "participant_interviewer_instructions_v1.md"
REVERSE = "custom_gpt_instructions_under_8000.md"
LIMIT = 8000


def _read(name: str) -> str:
    return (CUSTOM_GPT / name).read_text(encoding="utf-8")


def _collapsed(name: str) -> str:
    return " ".join(_read(name).split())


ANCHORS = {
    SHORT: (
        "only when their words support it, in replies and evidence records",
        "Quote only exact contiguous participant words; mark translations.",
        "only after checking the whole conversation",
        "recheck the Action response before agreeing or defending",
        "state AstroHD predictions only from returned results",
    ),
    LONG: (
        "Anchor claims about the participant in their own words.",
        "Put only the participant's exact words inside quotation marks.",
        "check the whole conversation",
        "recheck the returned Action response before agreeing or defending",
        "describe the frozen model only from returned prediction comparisons",
        "Do not correct a participant's Human Design terminology from general knowledge alone",
    ),
    REVERSE: (
        "Describe the person only from their words",
        "Quote only exact words; mark translations.",
        "Check the whole chat before claiming they never said something.",
        "Recheck data before conceding or defending.",
        "“Verified” names what was compared.",
    ),
}


@pytest.mark.parametrize(
    ("name", "anchor"),
    [
        pytest.param(name, anchor, id=f"{name}:{index}")
        for name, anchors in ANCHORS.items()
        for index, anchor in enumerate(anchors, 1)
    ],
)
def test_custom_gpt_accuracy_anchor(name: str, anchor: str) -> None:
    assert " ".join(anchor.split()) in _collapsed(name)


@pytest.mark.parametrize("name", (SHORT, REVERSE))
def test_deployable_custom_gpt_block_stays_under_builder_limit(name: str) -> None:
    text = _read(name)
    utf16_units = len(text.encode("utf-16-le")) // 2
    assert utf16_units + text.count("\n") <= LIMIT
    assert len(text.encode("utf-8")) <= LIMIT


def test_frozen_relationship_llm_instruments_are_unchanged() -> None:
    protocol = ROOT / "reference/relationship/relationship_blind_classifier_protocol_v1.json"
    digests = {
        "field": hashlib.sha256(llm_audit._FIELD_SYSTEM.encode()).hexdigest(),
        "session": hashlib.sha256(llm_audit._SESSION_SYSTEM.encode()).hexdigest(),
        "phenotype": hashlib.sha256(phenotype_classifier._SYSTEM.encode()).hexdigest(),
        "protocol": hashlib.sha256(protocol.read_bytes()).hexdigest(),
    }
    assert llm_audit.LLM_AUDIT_VERSION == "relationship-llm-auditor-v1"
    assert digests == {
        "field": "752288f4282ef6f6023f6023a22899654da48b683593cf2118e1466602cc2ae6",
        "session": "cf42f028b336aaa0f77d8f93eb775e17336ac12f885b9a2000debf38e6a397a0",
        "phenotype": "15b47e7d811938d0563e60718ce2c8e123b5f100c896d6210dac327183f311d1",
        "protocol": "b6971d715eb602a9ed8e9cb134cf166d688dd4d710a7ce3c0a0c604142dedb36",
    }
