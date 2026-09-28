"""Pin the accuracy checks carried in the Custom GPT instruction blocks.

A published Custom GPT runs only on the text pasted into its builder, so each block
must carry its own accuracy checks and stay inside the builder's 8,000-character
instruction limit.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from hdmatch.relationship import llm_audit, phenotype_classifier

PROJECT_ROOT = Path(__file__).parents[2]
CUSTOM_GPT = PROJECT_ROOT / "reference/custom_gpt"

SHORT_INTERVIEWER = "participant_interviewer_instructions_under_8000_v1.md"
LONG_INTERVIEWER = "participant_interviewer_instructions_v1.md"
REVERSE_MATCHER = "custom_gpt_instructions_under_8000.md"

BUILDER_INSTRUCTION_LIMIT = 8000
DEPLOYABLE_BLOCKS = (SHORT_INTERVIEWER, REVERSE_MATCHER)

# Exact phrases, compared after collapsing whitespace, keyed by the claim-integrity
# check each one carries.
ANCHORS: dict[str, dict[str, str]] = {
    SHORT_INTERVIEWER: {
        "CI-01": (
            "Say what the participant said, did, felt, or wanted, including words like "
            "always, never, kept, stopped, willing, or forced, only when their words in "
            "this conversation support it."
        ),
        "CI-01 model claims": (
            "After reveal, state what AstroHD predicted only from the returned results."
        ),
        "CI-02": (
            "Put only their exact words in quotation marks, never a paraphrase or words "
            "joined from separate statements. Mark translations."
        ),
        "CI-03": (
            "Before saying they never mentioned something, check the whole conversation. "
            "The claim covers only what you checked; say so when that was less than all "
            "of it."
        ),
        "CI-07": (
            "If they correct how you reflected them, return to their words: neither "
            "defend your reading nor adopt one they did not say. If they dispute a "
            "result, recheck the Action response before agreeing or defending."
        ),
        "CI-10": (
            "Before sending, compare with what you already said on the topic; correct any "
            "conflict and say so. Label estimates, and give derived numbers no more "
            "precisely than their inputs."
        ),
    },
    LONG_INTERVIEWER: {
        "CI-01": (
            "Every sentence that says what the participant said, did, felt, wanted, or "
            "described must rest on their own words in this conversation."
        ),
        "CI-02": (
            "Put only the participant's exact words inside quotation marks. Mark "
            "translations as translations."
        ),
        "CI-03": (
            "Before saying the participant never mentioned something, check the whole "
            "conversation for counterexamples."
        ),
        "CI-04": (
            "After reveal, describe what the frozen model predicted only from the returned "
            "prediction comparisons and behavioral statements."
        ),
        "CI-04 stated expertise": (
            "If the participant says they know Human Design well, do not correct their use "
            "of its terms from general knowledge alone"
        ),
        "CI-06": (
            "When you call a prediction supported, matched, or contradicted, name the "
            "prediction and the answer it was compared with."
        ),
        "CI-07": (
            "When the participant corrects how you reflected what they said, go back to "
            "their words: do not defend your reading, and do not adopt a new one they did "
            "not say."
        ),
        "CI-10": (
            "Before sending, compare what you are about to say with what you already said "
            "on the same topic. If they conflict, correct one and say so."
        ),
    },
    REVERSE_MATCHER: {
        "CI-01": (
            "Describe the person only from their words, including always/never; label "
            "inferences; add no unstated motive/history."
        ),
        "CI-02": "Quote only exact words; mark translations.",
        "CI-03": "Check the whole chat before claiming they never said something.",
        "CI-04": (
            "Base HD claims on uploaded files or say “from memory”; check them before "
            "disputing their HD usage."
        ),
        "CI-06": "“Verified” names what was compared.",
        "CI-07": (
            "If corrected, reread their words; adopt no reading they didn't give. Recheck "
            "data before conceding or defending."
        ),
        "CI-10": "Before sending, fix conflicts with earlier replies openly. Label estimates.",
    },
}


def _read(file_name: str) -> str:
    return (CUSTOM_GPT / file_name).read_text(encoding="utf-8")


def _collapse_whitespace(text: str) -> str:
    return " ".join(text.split())


ANCHOR_CASES = [
    pytest.param(file_name, anchor, id=f"{file_name}:{check_id}")
    for file_name, checks in ANCHORS.items()
    for check_id, anchor in checks.items()
]


@pytest.mark.parametrize(("file_name", "anchor"), ANCHOR_CASES)
def test_instruction_block_carries_accuracy_check(file_name: str, anchor: str) -> None:
    assert _collapse_whitespace(anchor) in _collapse_whitespace(_read(file_name))


@pytest.mark.parametrize("file_name", DEPLOYABLE_BLOCKS)
def test_deployable_block_fits_custom_gpt_instruction_limit(file_name: str) -> None:
    text = _read(file_name)
    # The builder's exact counting rule is not documented, so apply two conservative
    # counts. UTF-16 code units are what a browser counts; adding one per line break
    # covers a counter that sees CRLF endings. UTF-8 bytes cover a byte-based limit.
    utf16_units = len(text.encode("utf-16-le")) // 2
    assert utf16_units + text.count("\n") <= BUILDER_INSTRUCTION_LIMIT
    assert len(text.encode("utf-8")) <= BUILDER_INSTRUCTION_LIMIT


# The accuracy checks live only in the conversational instruction blocks above. The
# relationship study's LLM auditor and phenotype classifier are versioned instruments
# in a running study, so their instructions stay as they are; any change needs a new
# instrument version. (The Survey-v2 classifier and adjudicator prompts are already
# pinned by test_survey_v2_human_measurement_freeze.py.)
RELATIONSHIP_CLASSIFIER_PROTOCOL = (
    "reference/relationship/relationship_blind_classifier_protocol_v1.json"
)


def test_relationship_llm_instruments_are_unchanged() -> None:
    digests = {
        "field_auditor": hashlib.sha256(llm_audit._FIELD_SYSTEM.encode()).hexdigest(),
        "session_auditor": hashlib.sha256(llm_audit._SESSION_SYSTEM.encode()).hexdigest(),
        "phenotype_classifier": hashlib.sha256(phenotype_classifier._SYSTEM.encode()).hexdigest(),
        "classifier_protocol": hashlib.sha256(
            (PROJECT_ROOT / RELATIONSHIP_CLASSIFIER_PROTOCOL).read_bytes()
        ).hexdigest(),
    }
    assert llm_audit.LLM_AUDIT_VERSION == "relationship-llm-auditor-v1"
    assert digests == {
        "field_auditor": "752288f4282ef6f6023f6023a22899654da48b683593cf2118e1466602cc2ae6",
        "session_auditor": "cf42f028b336aaa0f77d8f93eb775e17336ac12f885b9a2000debf38e6a397a0",
        "phenotype_classifier": (
            "15b47e7d811938d0563e60718ce2c8e123b5f100c896d6210dac327183f311d1"
        ),
        "classifier_protocol": ("b6971d715eb602a9ed8e9cb134cf166d688dd4d710a7ce3c0a0c604142dedb36"),
    }
