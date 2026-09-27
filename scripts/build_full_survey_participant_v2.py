"""Build self-contained Full Life Patterns V2 participant packets."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TASK = Path("tasks/full-survey-participant-v2-20260927")
SURVEY = Path("tasks/scenario-survey-v7-redesign-20260922")
SOURCES = (
    (SURVEY / "INTERVIEW-PROTOCOL-v6.md", "5dc95763f65441d67c87b21116e00d7f2df04223"),
    (SURVEY / "interviewer-bank-v7.json", "cf6c60ec7206e07ee62b6148549e6d755bef8ac1"),
    (SURVEY / "EVIDENCE-GUIDE-v7.json", "29309f2341e2a8c91e578b683058e360ded8e420"),
)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _read_verified(root: Path, rel: Path, expected: str) -> str:
    raw = (root / rel).read_bytes()
    actual = git_blob_sha(raw)
    if actual != expected:
        raise ValueError(f"Authority changed: {rel}: expected {expected}, got {actual}")
    return raw.decode("utf-8")


def build_route_card(root: Path = BASE) -> str:
    bank = json.loads(_read_verified(root, SOURCES[1][0], SOURCES[1][1]))
    lines = [
        "## Generated route card — navigation aid only",
        "",
        "This card is generated directly from the embedded bank. It is for locating a route quickly; the full bank's admission/context/interpretation rules still govern.",
        "For context=prior_answer_required, source_options are possible qualifying prior routes, not a requirement that all listed routes be answered. Self-contained routes show source_options=- even when the full bank carries advisory context links.",
        "",
    ]
    for q in bank["questions"]:
        requirement = str(q.get("context_requirement", ""))
        self_contained = requirement.startswith("Self-contained")
        context_mode = "self_contained" if self_contained else "prior_answer_required"
        source_options = "-" if self_contained else (",".join(q.get("context_sources") or []) or "-")
        question = " ".join(str(q["question"]).split())
        lines.append(
            f"- {q['id']} | kind={q.get('kind','unknown')} | context={context_mode} | source_options={source_options} | question={question}"
        )
    for q in bank.get("exploratory_questions", []):
        question = " ".join(str(q["question"]).split())
        lines.append(
            f"- {q['id']} | kind=exploratory_after_canonical_stop_only | context=after_canonical_stop | source_options=- | question={question}"
        )
    return "\n".join(lines) + "\n"


def authority_sections(root: Path = BASE) -> str:
    out: list[str] = []
    for rel, expected in SOURCES:
        text = _read_verified(root, rel, expected)
        out.append(
            f"\n\n## Embedded authority: {rel}\n"
            f"Git blob: {expected}\n\n"
            f"<!-- BEGIN {rel} -->\n{text}<!-- END {rel} -->\n"
        )
    return "".join(out)


def controller_text(root: Path = BASE) -> str:
    return (root / TASK / "INTERVIEW-CONTROLLER-v2.md").read_text(encoding="utf-8")


def build_universal(root: Path = BASE) -> str:
    return (
        "# Full Life Patterns Survey V2 — self-contained participant file\n\n"
        "**Participant:** upload this one file to a normal ChatGPT chat. You do not need to read it yourself. "
        "If you already started the older survey, upload it in that same chat and ChatGPT must preserve your visible earlier answers rather than restart. "
        "If you lost the old chat but have an answer record, use a recovery packet generated from that record.\n\n"
        "**ChatGPT interviewer:** read the controller and route card first, then use the exact embedded authorities. "
        "Web/GitHub access is not required.\n\n"
        + controller_text(root)
        + "\n\n"
        + build_route_card(root)
        + authority_sections(root)
    )


def _fence_for(text: str) -> str:
    runs = [len(m.group(0)) for m in re.finditer(r"`+", text)]
    return "`" * max(4, (max(runs) + 1) if runs else 4)


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _assert_private_recovery_path(path: Path, role: str) -> None:
    resolved = path.expanduser().resolve()
    repo = BASE.resolve()
    if not _inside(resolved, repo):
        return
    allowed = (repo / "experiments" / "private").resolve()
    if not _inside(resolved, allowed):
        raise ValueError(
            f"{role} for a participant-specific recovery may not be inside the public repository "
            f"outside {allowed}"
        )


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def render_imported_record(
    response: dict,
    source_type: str,
    record_label: str = "Imported response record",
) -> str:
    if not isinstance(response, dict):
        raise ValueError("response JSON must be an object")
    turns = response.get("turns")
    if turns is not None:
        if not isinstance(turns, list):
            raise ValueError("turns, when present, must be a list")
        for i, turn in enumerate(turns, 1):
            if not isinstance(turn, dict):
                raise ValueError(f"turn {i} must be an object")
            if (
                "answer_text" in turn
                and turn["answer_text"] is not None
                and not isinstance(turn["answer_text"], str)
            ):
                raise ValueError(f"turn {i} answer_text must be text or null when present")
            # A question is intentionally not required: answer-only historical notes are preservable.
    serialized = json.dumps(response, ensure_ascii=False, indent=2) + "\n"
    fence = _fence_for(serialized)
    return (
        f"## {record_label}\n\n"
        f"Declared source type: {source_type}\n\n"
        "The JSON below is a canonical reserialization of the received record data. "
        "It is source evidence, not proof that edited question wording was originally shown.\n\n"
        "<!-- BEGIN IMPORTED RESPONSE JSON -->\n"
        f"{fence}json\n{serialized}{fence}\n"
        "<!-- END IMPORTED RESPONSE JSON -->\n"
    )


def build_recovery(
    response: dict,
    source_type: str,
    root: Path = BASE,
    record_label: str = "Imported response record",
) -> str:
    if not source_type or not source_type.strip():
        raise ValueError("source_type is required for recovery")
    return (
        "# Full Life Patterns V2 — recover and continue without the old chat\n\n"
        "This file contains the complete V2 controller/route card, the received prior record, and the exact survey authorities. "
        "The old chat is not required. Do not restart. Do not ask for birth data.\n\n"
        + controller_text(root)
        + "\n\n"
        + build_route_card(root)
        + "\n\n"
        + render_imported_record(response, source_type.strip(), record_label)
        + authority_sections(root)
    )


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--response-json", type=Path)
    p.add_argument("--source-type")
    p.add_argument("--record-label", default="Imported response record")
    args = p.parse_args()

    output = args.output.expanduser().resolve()
    if output.exists():
        p.error("output already exists; use a new versioned path")

    if args.response_json:
        if not args.source_type:
            p.error("--source-type is required with --response-json")
        source = args.response_json.expanduser().resolve()
        _assert_private_recovery_path(source, "input")
        _assert_private_recovery_path(output, "output")
        response = json.loads(
            source.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
        text = build_recovery(response, args.source_type, BASE, args.record_label)
    else:
        if args.source_type:
            p.error("--source-type is only used with --response-json")
        text = build_universal(BASE)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"Wrote {output} ({len(text.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
