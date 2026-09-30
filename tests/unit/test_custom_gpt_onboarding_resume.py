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
    assert "Continue my existing interview from the answers I’m attaching." in text
    assert "A Custom GPT cannot send a message before the user sends or taps something." in text
    assert "research-use consent" in text


def test_instructions_orient_then_resume_without_restart() -> None:
    text = (CUSTOM / "life_patterns_voice_interviewer_v2.md").read_text(encoding="utf-8")
    normalized = " ".join(text.split())
    assert "immediately orient them before behavioral questions" in normalized
    assert "responses may be shared with Joel" in normalized
    assert "consent to research use" in normalized
    assert "without another “ready” step" in normalized
    assert "do not restart or re-ask resolved questions" in normalized
    assert "word-for-word as imported source material" in normalized
    assert "ask only useful unresolved distinctions" in normalized


def test_manifest_pins_builder_config_and_instruction_budget() -> None:
    manifest = json.loads((CUSTOM / "life_patterns_voice_gpt_manifest_v2.json").read_text())
    cfg = ROOT / manifest["builder_config"]["path"]
    instructions = ROOT / manifest["instructions"]["path"]
    assert hashlib.sha256(cfg.read_bytes()).hexdigest() == manifest["builder_config"]["sha256"]
    assert (
        hashlib.sha256(instructions.read_bytes()).hexdigest()
        == manifest["instructions"]["sha256"]
    )
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
        assert "Continue my existing interview" in config
        assert "do not restart or re-ask resolved questions" in instructions
