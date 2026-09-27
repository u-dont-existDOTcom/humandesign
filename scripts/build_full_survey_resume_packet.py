"""Build a self-contained, birth-free full-survey continuation authority packet."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TASK = "tasks/full-survey-import-repair-20260927"
SURVEY = "tasks/scenario-survey-v7-redesign-20260922"
SOURCES = (
    (f"{SURVEY}/INTERVIEW-PROTOCOL-v6.md", "5dc95763f65441d67c87b21116e00d7f2df04223"),
    (f"{SURVEY}/interviewer-bank-v7.json", "cf6c60ec7206e07ee62b6148549e6d755bef8ac1"),
    (f"{SURVEY}/EVIDENCE-GUIDE-v7.json", "29309f2341e2a8c91e578b683058e360ded8e420"),
)

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def build_packet(root: Path = BASE) -> str:
    intro = """# Full Life Patterns interview: recover and continue

Instructions for the interview-only assistant. Read this whole packet and the privately attached response record before asking a question. The original survey authorities are embedded below; external links or repository access are not prerequisites.

Preserve the existing answers. This is not a restart or a requirement to complete every route. Do not use birth data, chart predictions or ranks. Do not give an astrology reading. If those appear in this interview context, record the exposure and route neutral interviewing to a clean context instead of claiming restored blindness.

First reconcile missing research permission and only source ambiguities needed for continuation. Do not show an interpreted profile before new questions. Continue with only useful unanswered distinctions under the full protocol, then perform the neutral source-anchored evidence review at the end. Never infer missing evidence as a negative trait. Off-bank answers can be usable with documented equivalence or narrower-scope review.

At completion, return a source-preserving reviewed JSON export, including exact imported/new questions and answers, corrections, conditions, provenance and unknowns. Do not claim semantic or predictive validation from formatting success. The research team handles later model mapping and comparison separately.

"""
    parts = [intro, "## Import and continuation rules\n\n", (root / TASK / "IMPORT-AND-RESUME-PROTOCOL-v1.md").read_text()]
    for rel, expected in SOURCES:
        raw = (root / rel).read_bytes()
        actual = git_blob_sha(raw)
        if actual != expected:
            raise ValueError(f"Authority changed: {rel}: expected {expected}, got {actual}")
        text = raw.decode("utf-8")
        parts.append(f"\n\n## Embedded original authority: {rel}\nGit blob: {actual}\n\n<!-- BEGIN {rel} -->\n{text}<!-- END {rel} -->\n")
    return "".join(parts)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output.exists():
        parser.error("Output already exists; choose a new version instead of overwriting.")
    output.parent.mkdir(parents=True, exist_ok=True)
    packet = build_packet()
    output.write_text(packet, encoding="utf-8")
    print(f"Wrote {output} ({len(packet.encode())} bytes)")

if __name__ == "__main__":
    main()
