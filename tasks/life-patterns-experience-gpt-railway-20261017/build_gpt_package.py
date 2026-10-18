# ruff: noqa: E501  # Exact GPT Instruction paragraph template.
"""Build a cumulative in-place Custom GPT editor package after verified v1.8.

The original GPT editor requires an owner action; no existing bearer or GPT
identity is changed by producing this deterministic package.
"""
from __future__ import annotations

import hashlib
import io
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / "reference/custom_gpt"
BASE = REF / "releases/Life-Patterns-GPT-Early-Review-2026-10-17.zip"
OUT = REF / "releases/Life-Patterns-GPT-Experience-and-Railway-v1.9-2026-10-17.zip"
GUIDE = "knowledge/EXPERIENCE-MEANING-OPTIONAL-v2.md"
BANK = "knowledge/experience-meaning-v2.json"
INSTR = "INSTRUCTIONS-life-patterns-voice-interviewer-v2.md"
ACTION = "ACTION-life-patterns-submission-openapi.yaml"
LONG_START = "After primary freeze, ask all three CF-003 questions"
LONG_END = "\n\nNever recode from target information after freeze"
FINAL_TEXT = """Freeze primary, then ask three CF003 questions before chart reveal. Keep CF003 separate; capture chart-familiarity and exposure; never ask Memory status. Railway handoff handles CF003, optional experience and storage; do not duplicate in GPT.

If staying in GPT, offer optional unscored Experience & Meaning v2 after CF003 per Knowledge. Respect refusal, skip covered items, separate usual/peak intensity. On opt-in add exact experience_record_json to the same final Action; otherwise omit it.

Submit complete source-preserving primary_record_json and cf003_record_json; relink CF003 per handoff guide. Include verified review_id or use exact-source server recovery. Explain **1 final storage call / 1 expected Allow card**, then say the exact Allow sentence. Claim storage only with receipt ID; on failure give both JSONs and diagnostic, never account-data Export."""


def sha(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def contents() -> dict[str, bytes]:
    with zipfile.ZipFile(BASE) as z:
        previous = {key: z.read(key) for key in z.namelist()}
    manifest = json.loads(previous["UPDATE-MANIFEST.json"])
    assert manifest["version"] == "2026-10-17.1-early-railway-review"
    assert all(sha(previous[key]) == value for key, value in manifest["files"].items())
    files = {
        key: value for key, value in previous.items()
        if key not in {
            "UPDATE-MANIFEST.json", "UPDATE-EXISTING-GPT.md",
            "TEST-RAILWAY-FINISH.md"
        }
    }
    original = files[INSTR].decode()
    start, end = original.index(LONG_START), original.index(LONG_END)
    assert start < end
    adjusted = original[:start] + FINAL_TEXT + original[end:]
    strict = len(adjusted.replace("\n", "\r\n"))
    if strict > 8000:
        raise ValueError(f"GPT Instructions exceed 8000 characters: {strict}")
    files[INSTR] = adjusted.encode()
    files[ACTION] = (
        ROOT / "apps/life-patterns-participant/participant/static/action-openapi-v1.9.yaml"
    ).read_bytes()
    assert json.loads(files[ACTION])["info"]["version"] == "1.9.0"
    files[GUIDE] = (REF / "EXPERIENCE-MEANING-OPTIONAL-v2.md").read_bytes()
    files[BANK] = (
        ROOT / "apps/life-patterns-participant/participant/static/experience-meaning-v2.json"
    ).read_bytes()
    files["UPDATE-EXISTING-GPT.md"] = (
        ROOT / "tasks/life-patterns-experience-gpt-railway-20261017/UPDATE-EXISTING-GPT.md"
    ).read_bytes()
    count = len([key for key in files if key.startswith("knowledge/")])
    assert count == 10
    new_manifest = {
        "version": "2026-10-17.2-experience-and-railway",
        "prior_zip_sha256": sha(BASE.read_bytes()),
        "instructions_strict_characters": strict,
        "knowledge_files": count,
        "action_version": "1.9.0",
        "same_existing_gpt_and_bearer": True,
        "private_data_in_package": False,
        "editor_applied": False,
        "files": {key: sha(value) for key, value in sorted(files.items())}
    }
    files["UPDATE-MANIFEST.json"] = (
        json.dumps(new_manifest,indent=2,sort_keys=True)+"\n"
    ).encode()
    return files


def serialize(files: dict[str, bytes]) -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        for key, value in sorted(files.items()):
            entry = zipfile.ZipInfo(key, date_time=(2026, 10, 17, 21, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            z.writestr(entry, value)
    return out.getvalue()


if __name__ == "__main__":
    data = serialize(contents())
    OUT.write_bytes(data)
    with zipfile.ZipFile(OUT) as z:
        new = json.loads(z.read("UPDATE-MANIFEST.json"))
        assert all(sha(z.read(k)) == v for k,v in new["files"].items())
        print(json.dumps({
            "package_sha256": sha(data),
            "instructions_strict_chars": new["instructions_strict_characters"],
            "knowledge_files": new["knowledge_files"],
            "action_version": new["action_version"],
        }))
