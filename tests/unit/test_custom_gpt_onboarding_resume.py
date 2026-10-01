"""Regression checks for Custom GPT onboarding and resume behavior."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CUSTOM = ROOT / "reference" / "custom_gpt"
RELEASE = CUSTOM / "releases" / "life-patterns-voice-gpt-2026-09-30"
ZIP = CUSTOM / "releases" / "life-patterns-voice-gpt-2026-09-30.zip"


def test_builder_config_has_user_facing_start_paths() -> None:
    text = (CUSTOM / "GPT-BUILDER-CONFIG.md").read_text(encoding="utf-8")
    assert "Life Patterns Interview" in text
    assert "Start my Life Patterns interview." in text
    assert "Find my Life Patterns record in my Library and continue." in text
    assert "Continue my interview from this chat or a record I attach." in text
    assert "A Custom GPT cannot send a message before the user sends or taps something." in text
    assert "research-use consent" in text
    assert "Enable **Code Interpreter & Data Analysis**" in text
    assert "Authentication: **API key → Bearer**" in text
    assert "action-openapi.yaml" in text
    assert "/privacy" in text
    assert "action-capable non-Pro model" in text
    assert "Same-chat automatic resume (web)" in text
    assert "Library fallback" in text
    assert "canonical Life Patterns export/recovery schemas only" in text
    assert "generic continue request must not search Library" in text


def test_instructions_orient_then_resume_without_restart() -> None:
    text = (CUSTOM / "life_patterns_voice_interviewer_v2.md").read_text(encoding="utf-8")
    normalized = " ".join(text.split())
    assert "On the first message, orient them before behavioral questions" in normalized
    assert "responses may be shared with Joel" in normalized
    assert "consent to research use" in normalized
    assert "without another “ready” step" in normalized
    assert "Resume only from sources allowed by `RECOVERY-GUIDE-v2.md`" in normalized
    assert "generic “continue” request never authorizes account-level lookup" in normalized
    assert "Library search is allowed only when the participant explicitly asks" in normalized
    assert "Never claim a source you did not actually retrieve" in normalized
    assert "submitLifePatternsRecords" in text
    assert "call it exactly once" in text
    assert "submission ID" in text
    assert "life-patterns-participant-export.json" in text
    assert "life-patterns-cf003-secondary-v0.json" in text


def test_recovery_guide_keeps_hale_derived_safeguards() -> None:
    text = (CUSTOM / "RECOVERY-GUIDE-v2.md").read_text(encoding="utf-8")
    required = (
        "word-for-word from the received record",
        "question wording is the exact original prompt",
        "cannot by itself prove the participant saw that condition",
        "A missing hedge, exception, correction, or condition is not evidence",
        "Editor-written headings, summaries, labels, or third-person paraphrases",
        "cannot retroactively verify original question wording",
        "Do not require reconfirmation of every old answer",
        "Missing metadata stays unknown",
        "Explicit Library fallback",
        "life-patterns-full-survey-participant-export-v2",
        "life-patterns-full-survey-participant-export-v1",
        "life-patterns-railway-visible-conversation-recovery-v1",
        "Do not broaden the search to generic behavioral/personality/interview files",
        "If exactly one canonical Library candidate is found",
        "If multiple canonical candidates are found",
        "generic request such as “continue my interview” is not authorization to search Library",
        "Never claim that an interview source was found",
    )
    for phrase in required:
        assert phrase in text


def test_manifest_pins_builder_config_and_instruction_budget() -> None:
    manifest = json.loads((CUSTOM / "life_patterns_voice_gpt_manifest_v2.json").read_text())
    cfg = ROOT / manifest["builder_config"]["path"]
    instructions = ROOT / manifest["instructions"]["path"]
    recovery = next(
        item
        for item in manifest["knowledge_files"]
        if item["path"].endswith("RECOVERY-GUIDE-v2.md")
    )
    recovery_path = ROOT / recovery["path"]
    action = ROOT / manifest["action_schema"]["path"]
    assert manifest["runtime_actions_required"] is True
    assert manifest["action_schema"]["operation_id"] == "submitLifePatternsRecords"
    assert manifest["action_schema"]["authentication"] == "api_key_bearer"
    assert manifest["action_schema"]["schema_url"].endswith("/action-openapi.yaml")
    assert manifest["action_schema"]["privacy_policy_url"].endswith("/privacy")
    assert hashlib.sha256(action.read_bytes()).hexdigest() == manifest["action_schema"]["sha256"]
    assert hashlib.sha256(cfg.read_bytes()).hexdigest() == manifest["builder_config"]["sha256"]
    assert (
        hashlib.sha256(instructions.read_bytes()).hexdigest()
        == manifest["instructions"]["sha256"]
    )
    assert hashlib.sha256(recovery_path.read_bytes()).hexdigest() == recovery["sha256"]
    text = instructions.read_text(encoding="utf-8")
    assert manifest["instructions"]["characters"] == len(text)
    assert manifest["instructions"]["strict_linebreak_count"] == len(text) + text.count("\n")
    assert manifest["instructions"]["strict_linebreak_count"] <= 8000


def test_release_zip_contains_builder_config_and_resume_instructions() -> None:
    with zipfile.ZipFile(ZIP) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        config_name = next(name for name in names if name.endswith("/GPT-BUILDER-CONFIG.md"))
        instructions_name = next(
            name
            for name in names
            if name.endswith("/INSTRUCTIONS-life-patterns-voice-interviewer-v2.md")
        )
        config = archive.read(config_name).decode()
        instructions = " ".join(archive.read(instructions_name).decode().split())
        assert "Start my Life Patterns interview." in config
        assert "Find my Life Patterns record in my Library and continue." in config
        assert "Continue my interview from this chat or a record I attach." in config
        assert "Library search is allowed only when the participant explicitly asks" in instructions
        assert any(name.endswith("/knowledge/RECOVERY-GUIDE-v2.md") for name in names)
        assert any(name.endswith("/ACTION-life-patterns-submission-openapi.yaml") for name in names)
        assert "submitLifePatternsRecords" in archive.read(instructions_name).decode()
