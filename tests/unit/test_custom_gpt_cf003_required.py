"""Regression checks that CF-003 is required in the shipped voice-GPT bundle."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CUSTOM = ROOT / "reference" / "custom_gpt"
RELEASE = CUSTOM / "releases" / "life-patterns-voice-gpt-2026-09-30"
ZIP = CUSTOM / "releases" / "life-patterns-voice-gpt-2026-09-30.zip"


def _text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_cf003_is_required_not_conditional() -> None:
    instructions = _text(CUSTOM / "life_patterns_voice_interviewer_v2.md")
    setup = _text(CUSTOM / "LIFE-PATTERNS-VOICE-GPT-SETUP.md")
    readme = _text(RELEASE / "README-FIRST.md")
    assert "ask all three CF-003 questions before chart reveal" in instructions
    assert "Then ask all three CF-003 secondary questions" in setup
    assert "CF-003 is **required in this bundle**" in readme
    forbidden = ("If CF-003", "CF-003 development module is enabled", "if the CF-003")
    for phrase in forbidden:
        assert phrase not in instructions
        assert phrase not in setup
        assert phrase not in readme


def test_manifest_requires_cf003_and_matches_instructions() -> None:
    manifest = json.loads((CUSTOM / "life_patterns_voice_gpt_manifest_v2.json").read_text())
    cf003 = manifest["secondary_modules"]["cf003"]
    assert cf003["required_in_this_bundle"] is True
    assert cf003["activation"].startswith("required after primary behavioral record freeze")
    p = ROOT / manifest["instructions"]["path"]
    text = p.read_text(encoding="utf-8")
    assert manifest["instructions"]["sha256"] == hashlib.sha256(p.read_bytes()).hexdigest()
    assert manifest["instructions"]["characters"] == len(text)
    assert manifest["instructions"]["strict_linebreak_count"] == len(text) + text.count("\n")
    assert manifest["instructions"]["strict_linebreak_count"] <= 8000


def test_release_zip_contains_required_cf003_bundle() -> None:
    with zipfile.ZipFile(ZIP) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert any(
            name.endswith("/knowledge/cf003_secondary_question_module_v0.json")
            for name in names
        )
        instructions_name = next(
            name
            for name in names
            if name.endswith("/INSTRUCTIONS-life-patterns-voice-interviewer-v2.md")
        )
        manifest_name = next(name for name in names if name.endswith("/MANIFEST.json"))
        instructions = " ".join(archive.read(instructions_name).decode().split())
        manifest = json.loads(archive.read(manifest_name))
        assert "ask all three CF-003 questions before chart reveal" in instructions
        assert manifest["secondary_modules"]["cf003"]["required_in_this_bundle"] is True


def test_cf003_metadata_records_actual_exposure_not_memory_setting():
    module_path = (
        ROOT / "reference/empirical_astrology/cf003_secondary_question_module_v0.json"
    )
    module = json.loads(module_path.read_text())
    metadata = module["post_freeze_metadata"]
    joined = " ".join(metadata["fields"] + [metadata.get("memory_note", "")])
    assert all("ChatGPT Memory" not in field for field in metadata["fields"])
    assert "actually visible" in joined
    assert "Memory status is not collected" in joined
