"""Build the same-GPT question-purpose update packet."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
CUSTOM = ROOT / "reference/custom_gpt"
VERSION = "2026-10-07.1-question-purpose"
ARCHIVE = CUSTOM / "releases" / "Life-Patterns-GPT-question-purpose-update-2026-10-07.zip"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


sources = {
    "INSTRUCTIONS-life-patterns-voice-interviewer-v2.md": (
        CUSTOM / "life_patterns_voice_interviewer_v2.md"
    ),
    "knowledge/TENDENCY-FIRST-GUIDE-v1.json": CUSTOM / "TENDENCY-FIRST-GUIDE-v1.json",
    "ACTION-life-patterns-submission-openapi.yaml": (
        ROOT / "apps/life-patterns-participant/participant/static/action-openapi.yaml"
    ),
    "UPDATE-EXISTING-GPT.md": TASK / "UPDATE-EXISTING-GPT.md",
}
contents = {name: path.read_bytes() for name, path in sources.items()}
instructions = contents["INSTRUCTIONS-life-patterns-voice-interviewer-v2.md"].decode()
strict = len(instructions) + instructions.count("\n")
assert strict < 8000, strict
assert b"participant_purpose" in contents["ACTION-life-patterns-submission-openapi.yaml"]
assert b"participant_purpose" in contents["knowledge/TENDENCY-FIRST-GUIDE-v1.json"]
assert b"What this tests" in contents["INSTRUCTIONS-life-patterns-voice-interviewer-v2.md"]
manifest = {
    "version": VERSION,
    "same_existing_gpt": True,
    "same_existing_review": True,
    "knowledge_replacements": ["TENDENCY-FIRST-GUIDE-v1.json"],
    "action_schema_changed": True,
    "existing_bearer_key_changes": False,
    "private_data_in_package": False,
    "instructions_strict_linebreak_count": strict,
    "files": {name: sha(data) for name, data in contents.items()},
}
contents["UPDATE-MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as z:
    for name, data in sorted(contents.items()):
        info = zipfile.ZipInfo(name, (2026, 10, 7, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, data)
with zipfile.ZipFile(ARCHIVE) as z:
    assert z.testzip() is None
    assert {name: z.read(name) for name in z.namelist()} == contents
receipt = {
    **manifest,
    "archive": ARCHIVE.name,
    "archive_sha256": sha(ARCHIVE.read_bytes()),
    "archive_bytes": ARCHIVE.stat().st_size,
}
(TASK / "PACKAGE-RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
