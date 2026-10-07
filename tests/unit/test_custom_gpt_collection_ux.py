"""Delivery-boundary regressions for the owner's intro/progress/recovery correction."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CUSTOM = ROOT / "reference/custom_gpt"


def text(name):
    return (CUSTOM / name).read_text()


def test_one_consent_question_not_mode_or_retrospective_form():
    s = text("life_patterns_voice_interviewer_v2.md")
    assert "Ask together for (1)" not in s
    assert "You are welcome to type or talk." in s
    assert "Ask ONLY for consent" in s
    assert "study_default" in s
    assert "preserve\nexplicit opt-outs" in s
    assert "Do not ask mode or earlier-life setup questions" in s
    assert "otherwise `unknown`" in s


def test_remaining_effort_is_mandatory_in_the_active_instructions():
    s = text("life_patterns_voice_interviewer_v2.md")
    assert "estimated remaining questions AND answering minutes" in s
    assert "counts/topic alone are not progress" in s
    assert "by the second behavioral question" in s


def test_completed_source_routes_to_review_without_local_reinterview():
    s = text("life_patterns_voice_interviewer_v2.md")
    assert "completed/saturated interview goes directly to independent review" in s
    assert "0 new main-interview questions planned" in s


def test_recovery_compares_lineages_before_offering_choices():
    s = text("RECOVERY-GUIDE-v2.md")
    assert "ask which one to use before reading/importing their answers" not in s
    for phrase in (
        "Discover before selecting",
        "EACH of the three allowed schemas",
        "follow relevant returned pagination",
        "unique verified current successor",
        "new empty/partial checkpoint cannot displace",
        "latest status unconfirmed",
        "different substantive wording",
    ):
        assert phrase.casefold() in s.casefold()


def test_footer_has_plan_math_and_distinguishes_complete_and_recovery_states():
    s = text("ACTION-HANDOFF-GUIDE-v1.md")
    for phrase in (
        "D/(D+U)",
        "planning assumption",
        "count-only/topic-only footer is a failure",
        "remaining questions/time",
        "Recovery incomplete — interview paused",
        "0 new main-interview questions planned",
        "current-batch remaining",
    ):
        assert phrase in s


def test_every_behavioral_question_must_show_its_neutral_purpose():
    s = text("life_patterns_voice_interviewer_v2.md")
    assert "Before EVERY behavioral question: `What this tests: <neutral purpose>`" in s
    assert "Use `participant_purpose`; else name its target/family plainly" in s
    assert "Show each returned clarification as `What this tests: {participant_purpose}`" in s
    assert "then `question_text` verbatim" in s
    assert "No scoring/chart targets/diagnostic claims" in s
