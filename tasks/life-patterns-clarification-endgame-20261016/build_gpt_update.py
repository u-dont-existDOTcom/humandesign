"""Cumulative in-place Custom GPT update for honest clarification progress."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
REF = ROOT / "reference/custom_gpt"
BASE = REF / "releases/Life-Patterns-GPT-completed-interview-update-2026-10-15.zip"
OUT = REF / "releases/Life-Patterns-GPT-honest-review-progress-2026-10-16.zip"
ACTION = "ACTION-life-patterns-submission-openapi.yaml"
INSTR = "INSTRUCTIONS-life-patterns-voice-interviewer-v2.md"
GUIDE = "knowledge/ACTION-HANDOFF-GUIDE-v1.md"
ACTION_SOURCE = TASK / "frozen_source/action-openapi-v1.6.1.json"
GUIDE_SOURCE = TASK / "frozen_source/ACTION-HANDOFF-v1.6.1.md"


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def replace_once(text: str, before: str, after: str) -> str:
    if text.count(before) != 1:
        raise ValueError("Expected one existing GPT instruction anchor: " + before[:70])
    return text.replace(before, after, 1)


def build() -> dict[str, bytes]:
    with zipfile.ZipFile(BASE) as archive:
        previous = {key: archive.read(key) for key in archive.namelist()}
    manifest = json.loads(previous["UPDATE-MANIFEST.json"])
    if manifest["version"] != "2026-10-15.1-completed-historical-resume":
        raise ValueError("Incorrect cumulative GPT predecessor")
    if any(sha(previous[key]) != digest for key, digest in manifest["files"].items()):
        raise ValueError("Predecessor ZIP content differs from recorded hashes")
    files = {
        key: value
        for key, value in previous.items()
        if key not in ("UPDATE-MANIFEST.json", "UPDATE-EXISTING-GPT.md", "PARTICIPANT-CONTINUE.md")
    }
    contract = json.loads(ACTION_SOURCE.read_text())
    if contract["info"]["version"] != "1.6.1":
        raise ValueError("Latest additive progress schema not built")
    files[ACTION] = ACTION_SOURCE.read_bytes()
    files[GUIDE] = GUIDE_SOURCE.read_bytes()

    instructions = files[INSTR].decode()
    q = chr(96)
    before = (
        "Ask returned "
        + q
        + "question_text"
        + q
        + " verbatim; show "
        + q
        + "What this tests:"
        + q
        + " only when unclear. One at a time; "
        "no Action between questions."
    )
    after = (
        "Ask exact " + q + "question_text" + q + " singly. State "
        "'i/n IN THIS BATCH; global remaining UNKNOWN'. Never '1 of 1 remaining'. "
        "No Action between questions."
    )
    instructions = replace_once(instructions, before, after)
    strict_chars = len(instructions.replace("\n", "\r\n"))
    if strict_chars > 8000:
        raise ValueError(f"GPT instruction limit: {strict_chars}")
    if "No question-count cap or coverage-only asks." not in instructions:
        raise ValueError("Original nonredundancy and open-ended evidence rule lost")
    files[INSTR] = instructions.encode()
    files["UPDATE-EXISTING-GPT.md"] = (TASK / "UPDATE-EXISTING-GPT.md").read_bytes()
    files["HUMAN-QUICK-CORRECTION.md"] = (TASK / "HUMAN-QUICK-CORRECTION.md").read_bytes()
    knowledge_count = sum(k.startswith("knowledge/") for k in files)
    if knowledge_count != 8:
        raise ValueError("Other existing Knowledge has unexpectedly changed")
    metadata = {
        "version": "2026-10-16.1-honest-clarification-progress",
        "previous_version": manifest["version"],
        "previous_zip_sha256": sha(BASE.read_bytes()),
        "same_existing_gpt": True,
        "instruction_chars_strict_crlf": strict_chars,
        "knowledge_file_count": knowledge_count,
        "action_version": "1.6.1",
        "prior_actions_preserved": True,
        "schema_change": "Read-only clarification_progress; no new operations",
        "survey_bank_and_astrology_unchanged": True,
        "private_participant_data_or_credentials_present": False,
        "private_editor_applied": False,
        "files": {key: sha(value) for key, value in sorted(files.items())},
    }
    files["UPDATE-MANIFEST.json"] = (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode()
    return files


def serialize(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            item = zipfile.ZipInfo(name, date_time=(2026, 10, 16, 12, 0, 0))
            item.external_attr = 0o644 << 16
            item.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(item, data, compress_type=zipfile.ZIP_DEFLATED)
    return stream.getvalue()


def main() -> None:
    payload = serialize(build())
    if "--check" in sys.argv:
        if OUT.read_bytes() != payload:
            raise ValueError("Generated GPT ZIP drift")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    with zipfile.ZipFile(OUT) as archive:
        manifest = json.loads(archive.read("UPDATE-MANIFEST.json"))
        assert all(sha(archive.read(key)) == digest for key, digest in manifest["files"].items())
    print(
        json.dumps(
            {
                "result": "CHECKED" if "--check" in sys.argv else "BUILT",
                "instruction_chars": manifest["instruction_chars_strict_crlf"],
                "knowledge_files": manifest["knowledge_file_count"],
                "action_version": manifest["action_version"],
                "archive_bytes": len(payload),
            }
        )
    )


if __name__ == "__main__":
    main()
