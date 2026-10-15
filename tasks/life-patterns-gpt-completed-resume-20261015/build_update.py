"""Build cumulative owner-applied update for existing Life Patterns Custom GPT."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]
REF = ROOT / "reference/custom_gpt"
BASE = REF / "releases/Life-Patterns-GPT-exact-recovery-update-2026-10-09.zip"
BASE_KNOWLEDGE = REF / "releases/life-patterns-voice-gpt-2026-09-30/knowledge"
OUT = REF / "releases/Life-Patterns-GPT-completed-interview-update-2026-10-15.zip"
ORIGINAL_FILES = (
    "INTERVIEW-PROTOCOL-v6.md",
    "interviewer-bank-v7.json",
    "EVIDENCE-GUIDE-v7.json",
    "RECOVERY-GUIDE-v2.md",
)
REPLACED_FILES = (
    "ACTION-HANDOFF-GUIDE-v1.md",
    "TENDENCY-FIRST-GUIDE-v1.json",
    "cf003_secondary_question_module_v0.json",
)
INSTRUCTIONS = "INSTRUCTIONS-life-patterns-voice-interviewer-v2.md"
ACTION = "ACTION-life-patterns-submission-openapi.yaml"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exactly(s: str, source: str, destination: str) -> str:
    if s.count(source) != 1:
        raise ValueError("Unexpected instruction source anchor: " + source[:65])
    return s.replace(source, destination, 1)


def components() -> dict[str, bytes]:
    with zipfile.ZipFile(BASE) as archive:
        old = {filename: archive.read(filename) for filename in archive.namelist()}
    manifest = json.loads(old["UPDATE-MANIFEST.json"])
    if manifest["version"] != "2026-10-09.1-recovery-access-autonomy":
        raise ValueError("Unexpected inherited GPT version")
    if any(sha(old[k]) != v for k, v in manifest["files"].items()):
        raise ValueError("Prior GPT update has changed; abort rather than combine stale content")

    instructions = old[INSTRUCTIONS].decode("utf-8")
    instructions = exactly(
        instructions,
        "Resume only from sources allowed by " + chr(96) + "RECOVERY-GUIDE-v2.md" + chr(96) + ".",
        "Resume under "
        + chr(96)
        + "RECOVERY-GUIDE-v2.md"
        + chr(96)
        + " and "
        + chr(96)
        + "COMPLETED-INTERVIEW-CONTINUATION-v1.md"
        + chr(96)
        + ".",
    )
    instructions = exactly(
        instructions,
        "Never claim a source you did not actually retrieve. ",
        "",
    )
    strict_len = len(instructions.replace("\n", "\r\n"))
    if not 6500 <= strict_len <= 8000:
        raise ValueError("Strict GPT editor 8000-character limit exceeded")
    if (
        "startLifePatternsReview" not in instructions
        or "Retired scenes cannot be new questions" not in instructions
    ):
        raise ValueError("Accidentally erased a key interview or Action workflow")

    files = {INSTRUCTIONS: instructions.encode("utf-8"), ACTION: old[ACTION]}
    for name in ORIGINAL_FILES:
        files["knowledge/" + name] = (BASE_KNOWLEDGE / name).read_bytes()
    for name in REPLACED_FILES:
        files["knowledge/" + name] = old["knowledge/" + name]
        if sha(files["knowledge/" + name]) != manifest["files"]["knowledge/" + name]:
            raise ValueError("Knowledge hash not retained from October 9")
    guide = TASK / "COMPLETED-INTERVIEW-CONTINUATION-v1.md"
    files["knowledge/" + guide.name] = guide.read_bytes()
    files["UPDATE-EXISTING-GPT.md"] = (TASK / "UPDATE-EXISTING-GPT.md").read_bytes()
    files["PARTICIPANT-CONTINUE.md"] = (TASK / "PARTICIPANT-CONTINUE.md").read_bytes()

    if len([n for n in files if n.startswith("knowledge/")]) != 8:
        raise ValueError("Wrong GPT Knowledge file count")
    new_manifest = {
        "version": "2026-10-15.1-completed-historical-resume",
        "previous_update_version": manifest["version"],
        "previous_update_zip_sha256": sha(BASE.read_bytes()),
        "instructions_strict_linebreak_count": strict_len,
        "knowledge_file_count": 8,
        "action_schema_version": "1.6.0",
        "model_or_review_backend_changed": False,
        "prior_questionnaire_and_frozen_bank_unchanged": True,
        "same_gpt_same_action_and_credential": True,
        "added_knowledge": guide.name,
        "participant_text_or_credentials_in_package": False,
        "files": {name: sha(data) for name, data in sorted(files.items())},
    }
    files["UPDATE-MANIFEST.json"] = (
        json.dumps(new_manifest, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    return files


def archive_bytes(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as out:
        for name, payload in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 15, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            out.writestr(info, payload, compress_type=zipfile.ZIP_DEFLATED)
    return stream.getvalue()


def main() -> None:
    blob = archive_bytes(components())
    if "--check" in sys.argv:
        if not OUT.is_file() or OUT.read_bytes() != blob:
            raise ValueError("GPT package generation is not reproducible")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(blob)
    with zipfile.ZipFile(OUT) as archive:
        manifest = json.loads(archive.read("UPDATE-MANIFEST.json"))
        if any(sha(archive.read(k)) != v for k, v in manifest["files"].items()):
            raise ValueError("GPT update ZIP readback failed")
    print(
        json.dumps(
            {
                "build": "CHECKED" if "--check" in sys.argv else "CREATED",
                "strict_chars": manifest["instructions_strict_linebreak_count"],
                "knowledge_files": manifest["knowledge_file_count"],
                "zip_bytes": len(blob),
                "private_records": 0,
            }
        )
    )


if __name__ == "__main__":
    main()
