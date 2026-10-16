"""Cumulative ready-only Railway finishing addition for the existing GPT."""

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
BASE = REF / "releases/Life-Patterns-GPT-honest-review-progress-2026-10-16.zip"
OUT = REF / "releases/Life-Patterns-GPT-Railway-Finish-2026-10-16.zip"
INSTR = "INSTRUCTIONS-life-patterns-voice-interviewer-v2.md"
ACTION = "ACTION-life-patterns-submission-openapi.yaml"
GUIDE = "knowledge/ACTION-HANDOFF-GUIDE-v1.md"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def once(s: str, old: str, new: str) -> str:
    if s.count(old) != 1:
        raise ValueError("Missing or ambiguous inherited instruction: " + old[:65])
    return s.replace(old, new, 1)


def build() -> dict[str, bytes]:
    with zipfile.ZipFile(BASE) as archive:
        previous = {name: archive.read(name) for name in archive.namelist()}
    manifest = json.loads(previous["UPDATE-MANIFEST.json"])
    if manifest["version"] != "2026-10-16.1-honest-clarification-progress":
        raise ValueError("The predecessor is not the latest progress update")
    if any(sha(previous[k]) != v for k, v in manifest["files"].items()):
        raise ValueError("Predecessor GPT update hashes do not match")
    files = {
        name: data
        for name, data in previous.items()
        if name
        not in ("UPDATE-MANIFEST.json", "UPDATE-EXISTING-GPT.md", "HUMAN-QUICK-CORRECTION.md")
    }
    old = (
        "Only `ready` permits final review. Honor pause/stop/withdraw through "
        "the control Action. After error/resource repair, retry that review when "
        "asked; blocked is not complete. No replacement job."
    )
    new = (
        "Only `ready` permits finish. Offer GPT or Railway finish. If participant "
        "chooses Railway, call `issueLifePatternsFinishLink` for saved review "
        "(one Allow); do NOT also freeze/CF003/submit in GPT. Otherwise finish "
        "here. Honor pause/stop/withdraw and same-review retries."
    )
    text = once(files[INSTR].decode("utf-8"), old, new)
    text = once(
        text,
        "For queued/processing, report stage/range/`recommended_check_after_seconds` "
        "and `wait_guidance`; be accurate about delays or blocked status. They may "
        "leave. On return call `getLifePatternsReview` once; no polling/promised notification.",
        "For queued/processing show stage, check-back interval and honest uncertainty. "
        "On return call `getLifePatternsReview` once; no polling or notifications.",
    )
    strict_chars = len(text.replace("\n", "\r\n"))
    if strict_chars > 8000:
        raise ValueError(f"GPT instructions exceed editor limit: {strict_chars}")
    for constraint in (
        "fast-batch-v1",
        "No question-count cap or coverage-only asks.",
        "COMPLETED-INTERVIEW-CONTINUATION-v1.md",
        "startLifePatternsReview",
    ):
        if constraint not in text:
            raise ValueError("A frozen interview/review constraint disappeared")
    files[INSTR] = text.encode("utf-8")
    files[ACTION] = (
        ROOT / "apps/life-patterns-participant/participant/static/action-openapi.yaml"
    ).read_bytes()
    contract = json.loads(files[ACTION])
    if contract["info"]["version"] != "1.7.0":
        raise ValueError("New Action contract version missing")
    files[GUIDE] = (REF / "ACTION-HANDOFF-GUIDE-v1.md").read_bytes()
    files["UPDATE-EXISTING-GPT.md"] = (TASK / "UPDATE-EXISTING-GPT.md").read_bytes()
    files["TEST-RAILWAY-FINISH.md"] = (TASK / "TEST-RAILWAY-FINISH.md").read_bytes()
    count = sum(name.startswith("knowledge/") for name in files)
    if count != 8:
        raise ValueError("Existing GPT Knowledge was not preserved")
    metadata = {
        "version": "2026-10-16.2-ready-railway-finish",
        "predecessor_zip_sha256": sha(BASE.read_bytes()),
        "same_existing_gpt": True,
        "strict_instructions_characters": strict_chars,
        "knowledge_files": count,
        "action_version": "1.7.0",
        "new_action_operation": "issueLifePatternsFinishLink",
        "previous_six_actions_unchanged": True,
        "participant_data_or_credentials_in_package": False,
        "private_gpt_editor_updated": False,
        "files": {key: sha(value) for key, value in sorted(files.items())},
    }
    files["UPDATE-MANIFEST.json"] = (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode()
    return files


def serialize(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(2026, 10, 16, 12, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            archive.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED)
    return stream.getvalue()


def main() -> None:
    data = serialize(build())
    if "--check" in sys.argv:
        if OUT.read_bytes() != data:
            raise ValueError("Final GPT ZIP does not match source")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(data)
    with zipfile.ZipFile(OUT) as archive:
        manifest = json.loads(archive.read("UPDATE-MANIFEST.json"))
        if any(sha(archive.read(k)) != v for k, v in manifest["files"].items()):
            raise ValueError("Final GPT release failed exact hash readback")
    print(
        json.dumps(
            {
                "status": "CHECKED" if "--check" in sys.argv else "BUILT",
                "strict_chars": manifest["strict_instructions_characters"],
                "knowledge_files": manifest["knowledge_files"],
                "action_version": manifest["action_version"],
                "zip_bytes": len(data),
            }
        )
    )


if __name__ == "__main__":
    main()
