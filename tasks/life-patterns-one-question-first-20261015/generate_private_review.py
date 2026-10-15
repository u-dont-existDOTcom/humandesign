"""Render an owner-private source report without publishing participant responses."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path


def write_private(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        out.write(value)
    path.chmod(0o600)


def build(source: Path, primary: Path, secondary: Path) -> tuple[str, dict]:
    raw = json.loads(source.read_text())
    role = raw["role_entry_review"]
    assert raw["schema"] == "local_life_patterns_v3_3_pilot_unsubmitted"
    assert len(raw["answers"]) == 25 and len(role["episodes"]) == 3
    assert isinstance(role.get("pattern"), str)
    fingerprint = hashlib.sha256(source.read_bytes()).hexdigest()
    results = [json.loads(p.read_text()) for p in (primary, secondary)]
    for file, result in zip((primary, secondary), results, strict=True):
        freeze = json.loads((file.parent / "FROZEN-BEFORE-SCORE.json").read_text())
        if freeze["source_sha256"] != fingerprint:
            raise ValueError("Frozen run source mismatch")
        if result["participant_confirmed_five_domain_profile"] is not False:
            raise ValueError("Cannot recast researcher draft as participant-confirmed")
    neutral_role = "mixed" if role["pattern"] == "context_dependent" else "unresolved"
    lines = [
        "# Private Life Patterns source and development results",
        "",
        "**Your completed role-entry response is retained. No additional answer is required.**",
        "",
        "The revised questionnaire accepts a brief conditional response, allows no-role examples,",
        "and leaves deeper follow-ups optional. Your previous responses were not modified.",
        "",
        "## Original source (not independently corroborated)",
        "",
    ]
    for i, event in enumerate(role["episodes"], 1):
        lines.extend(
            [
                "### Recorded occasion " + str(i),
                "",
                "Selected example type: " + str(event["origin"]),
                "",
                event["example"],
                "",
            ]
        )
    lines.extend(
        [
            "## Participant's overall selection",
            "",
            "Source-selected category: " + role["pattern"],
            "Neutral role-entry coder recommendation: " + neutral_role,
            "Neither a positive nor a negative natal clause is inferred from a mixed answer.",
            "",
            "## Previously frozen model, same-person development check",
            "",
            "The five-domain profile is researcher-drafted, not separately participant-confirmed.",
            "The astronomical conditions were selected using the known development birth.",
            "Model and signed bridge were unchanged; six votes are not independent traits.",
            "",
        ]
    )
    for label, result in zip(("999-decoy primary", "9999-decoy secondary"), results, strict=True):
        lines.append(
            "{}: target score {}, rank {}-{}, other tied candidates {}.".format(
                label, result["score"], result["rank_best"], result["rank_worst"],
                result["tied_other_candidates"]
            )
        )
    lines.extend(
        [
            "",
            "These are not a new full-century scan or an independent birth-time validation.",
            "The previously fitted six-rule century result remains the development reference.",
        ]
    )
    return "\n".join(lines) + "\n", {
        "prior_answers": len(raw["answers"]),
        "role_episodes": len(role["episodes"]),
        "role_evidence_state": neutral_role,
        "first_in_primary": results[0]["rank_best"] == 1,
        "first_in_secondary": results[1]["rank_best"] == 1,
        "additional_owner_input_needed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    for argument in ("source", "primary", "secondary", "output"):
        parser.add_argument("--" + argument, type=Path, required=True)
    args = parser.parse_args()
    text, aggregate = build(args.source, args.primary, args.secondary)
    write_private(args.output / "ROLE-REVIEW-PRIVATE.md", text)
    page = (
        "<!doctype html><html lang='en'><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Private Role Review</title>"
        "<style>body{font:16px/1.6 system-ui;max-width:850px;margin:auto;padding:1rem}"
        "pre{white-space:pre-wrap;overflow-wrap:anywhere}</style><pre>"
        + html.escape(text)
        + "</pre></html>"
    )
    write_private(args.output / "ROLE-REVIEW-PRIVATE.html", page)
    print(json.dumps(aggregate))


if __name__ == "__main__":
    main()
