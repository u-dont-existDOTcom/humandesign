"""Prefill a simplified offline Life Patterns pilot without changing past answers.

Sensitive respondent text is embedded only into owner-private local HTML (mode 0600).
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PILOT = (
    ROOT
    / "tasks/life-patterns-role-entry-repair-20261015"
    / "LIFE_PATTERNS_V33_ROLE_ENTRY_OFFLINE_PILOT.html"
)


def create_private(source: Path, output: Path) -> dict:
    raw = json.loads(source.read_text(encoding="utf-8"))
    if raw.get("schema") not in {
        "local_life_patterns_v3_pilot_unsubmitted",
        "local_life_patterns_v3_2_pilot_unsubmitted",
        "local_life_patterns_v3_3_pilot_unsubmitted",
    }:
        raise ValueError("Unexpected source schema")
    text = PILOT.read_text(encoding="utf-8")
    opening = '<script id="pilot-data" type="application/json">'
    a = text.index(opening) + len(opening)
    b = text.index("</script>", a)
    contents = json.loads(text[a:b])
    questions = contents["questions"]
    assert len(questions) == 25
    answers = raw.get("answers")
    if not isinstance(answers, dict) or len(answers) != 25:
        raise ValueError("Expected original 25 answers")
    banks = {q["id"]: set(q["example_answer_paths"]) for q in questions}
    if set(answers) != set(banks):
        raise ValueError("Old questionnaire route mismatch")
    for key, rec in answers.items():
        if not isinstance(rec, dict) or not isinstance(rec.get("selected"), list):
            raise ValueError("Malformed old answer")
        if any(x not in banks[key] for x in rec["selected"]):
            raise ValueError("Option does not match original V3 bank")
    if not isinstance(raw.get("unique_behaviors"), list):
        raise ValueError("No behavior inventory")
    if raw.get("role_entry_review") is not None:
        review = raw["role_entry_review"]
        if not isinstance(review, dict) or len(review.get("episodes", [])) != 3:
            raise ValueError("Malformed role history")
        origins = {x["id"] for x in contents["role_probe"]["allowed_origins"]}
        patterns = {x["id"] for x in contents["role_probe"]["pattern_choices"]}
        if review.get("pattern") not in patterns.union({""}):
            raise ValueError("Invalid role pattern")
        for item in review["episodes"]:
            if not isinstance(item, dict) or item.get("origin") not in origins.union({""}):
                raise ValueError("Invalid role history")
    contents["prefilled_export"] = raw
    safe = (
        json.dumps(contents, ensure_ascii=False)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )
    text = text[:a] + safe + text[b:]
    output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as file:
        file.write(text)
    output.chmod(0o600)
    return {
        "legacy_answers": len(answers),
        "unique_behaviors": len(raw["unique_behaviors"]),
        "past_role_response_preserved": bool(raw.get("role_entry_review")),
        "mode": "0600",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    p = parser.parse_args()
    print(json.dumps(create_private(p.source, p.output)))
