"""Build cumulative original-GPT update for early Railway continuation."""

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
BASE = REF / "releases/Life-Patterns-GPT-Railway-Finish-2026-10-16.zip"
OUT = REF / "releases/Life-Patterns-GPT-Early-Review-2026-10-17.zip"
INSTR = "INSTRUCTIONS-life-patterns-voice-interviewer-v2.md"
ACTION = "ACTION-life-patterns-submission-openapi.yaml"
GUIDE = "knowledge/ACTION-HANDOFF-GUIDE-v1.md"


def sha(x: bytes) -> str:
    return hashlib.sha256(x).hexdigest()


def swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, "Incompatible original GPT instruction"
    return text.replace(old, new, 1)


def contents() -> dict[str, bytes]:
    with zipfile.ZipFile(BASE) as z:
        prior = {name: z.read(name) for name in z.namelist()}
    old = json.loads(prior["UPDATE-MANIFEST.json"])
    assert old["version"] == "2026-10-16.2-ready-railway-finish"
    assert all(sha(prior[k]) == v for k, v in old["files"].items())
    files = {
        k: v
        for k, v in prior.items()
        if k
        not in (
            "UPDATE-MANIFEST.json",
            "UPDATE-EXISTING-GPT.md",
            "TEST-RAILWAY-FINISH.md",
        )
    }
    text = files[INSTR].decode()
    text = swap(
        text,
        "Only `ready` permits finish. Offer GPT or Railway finish. If participant "
        "chooses Railway, call `issueLifePatternsFinishLink` for saved review "
        "(one Allow); do NOT also freeze/CF003/submit in GPT. Otherwise finish "
        "here. Honor pause/stop/withdraw and same-review retries.",
        "After `startLifePatternsReview` saves review ID, offer Railway immediately "
        "(even queued) via `issueLifePatternsFinishLink` on participant approval. "
        "Railway handles every admitted batch, auto-checks while open, allows "
        "declining further questions (unknowns kept), then after ready handles "
        "confirmation/CF003/storage. No GPT duplicate work after handoff; "
        "otherwise use the existing GPT review loop.",
    )
    text = swap(
        text,
        "Before batch submission, explain: **2 external calls remain in this round**—"
        "save answers now, retrieve the updated review later—and another Allow "
        "card may appear. Send once via `submitLifePatternsClarificationBatch` with "
        "fresh `operation_id`; reuse exact body on retry. If queued/processing, "
        "show check-back guidance and END THE TURN—never launch the later "
        "retrieval or leave a surprise card.",
        "If remaining in GPT, saving the batch and checking later are separate "
        "Actions; both may need Allow. Use fresh `operation_id` and reuse the "
        "exact same body on retry. If queued, give check-back instructions "
        "and END TURN; do not start a second Action immediately.",
    )
    strict = len(text.replace("\n", "\r\n"))
    if strict > 8000:
        raise ValueError(f"GPT editor Instructions exceed 8000 characters: {strict}")
    files[INSTR] = text.encode()
    files[ACTION] = (
        ROOT / "apps/life-patterns-participant/participant/static/action-openapi.yaml"
    ).read_bytes()
    assert json.loads(files[ACTION])["info"]["version"] == "1.8.0"
    files[GUIDE] = (REF / "ACTION-HANDOFF-GUIDE-v1.md").read_bytes()
    files["UPDATE-EXISTING-GPT.md"] = (TASK / "UPDATE-EXISTING-GPT.md").read_bytes()
    assert len([k for k in files if k.startswith("knowledge/")]) == 8
    manifest = {
        "version": "2026-10-17.1-early-railway-review",
        "prior_zip_sha256": sha(BASE.read_bytes()),
        "instructions_strict_characters": strict,
        "knowledge_files": 8,
        "action_version": "1.8.0",
        "same_existing_gpt_and_bearer": True,
        "private_data_in_package": False,
        "editor_applied": False,
        "files": {k: sha(v) for k, v in sorted(files.items())},
    }
    files["UPDATE-MANIFEST.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    return files


def serialize(files: dict[str, bytes]) -> bytes:
    f = io.BytesIO()
    with zipfile.ZipFile(f, "w") as z:
        for k, v in sorted(files.items()):
            info = zipfile.ZipInfo(k, date_time=(2026, 10, 17, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, v)
    return f.getvalue()


if __name__ == "__main__":
    content = serialize(contents())
    if "--check" in sys.argv:
        assert OUT.read_bytes() == content
    else:
        OUT.write_bytes(content)
    with zipfile.ZipFile(OUT) as z:
        info = json.loads(z.read("UPDATE-MANIFEST.json"))
        assert all(sha(z.read(k)) == v for k, v in info["files"].items())
    print(
        json.dumps(
            {
                "result": "CHECKED" if "--check" in sys.argv else "BUILT",
                "strict_chars": info["instructions_strict_characters"],
                "knowledge_files": info["knowledge_files"],
            }
        )
    )
