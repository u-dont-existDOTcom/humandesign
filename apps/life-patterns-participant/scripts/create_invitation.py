#!/usr/bin/env python3
"""Create one private participant invitation from a local prior JSON record.

The admin token is read from a file and never printed. Birth/chart/ranking fields are
rejected before upload. The output contains the private resume link and must be kept private.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import urllib.error
import urllib.request

FORBIDDEN_KEYS = {
    "birth_date",
    "birth_time",
    "birthplace",
    "date_of_birth",
    "dob",
    "birth_location",
    "birth_chart",
    "natal_chart",
    "chart",
    "rankings",
    "target_predictions",
    "human_design_type",
}
SOURCE_TYPES = {"edited_response_record", "raw_transcript", "prior_json", "answer_only_notes"}
SOURCE_MODES = {"railway_text", "chatgpt_voice", "chatgpt_text", "mixed", "unknown"}


def reject_target_fields(value, path="root"):
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_KEYS:
                raise ValueError(f"Remove birth/chart/ranking field before upload: {path}.{key}")
            reject_target_fields(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_target_fields(child, f"{path}[{index}]")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", required=True, type=pathlib.Path)
    parser.add_argument("--admin-token-file", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    parser.add_argument(
        "--source-type", default="edited_response_record", choices=sorted(SOURCE_TYPES)
    )
    parser.add_argument("--source-mode", default="unknown", choices=sorted(SOURCE_MODES))
    parser.add_argument(
        "--origin", default="https://life-patterns-participant-production.up.railway.app"
    )
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    record = json.loads(args.record.expanduser().read_text())
    if not isinstance(record, dict):
        raise SystemExit("Record JSON must contain one object.")
    turns = record.get("turns")
    if not isinstance(turns, list):
        raise SystemExit("Record must contain a turns list.")
    reject_target_fields(record)
    source_mode = args.source_mode
    if source_mode == "unknown" and record.get("collection_mode") in SOURCE_MODES:
        source_mode = str(record["collection_mode"])
    if args.validate_only:
        print(f"VALID: {len(turns)} turns, no forbidden birth/chart/ranking keys detected.")
        return 0

    token = args.admin_token_file.expanduser().read_text().strip()
    if len(token) < 32:
        raise SystemExit("Admin token file is missing or invalid.")
    origin = args.origin.rstrip("/")
    payload = {
        "source_type": args.source_type,
        "source_mode": source_mode,
        "record": record,
    }
    request = urllib.request.Request(
        origin + "/api/admin/invitations",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Origin": origin,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            invitation = json.load(response)
    except urllib.error.HTTPError as exc:
        try:
            detail = json.loads(exc.read()).get("detail")
        except Exception:
            detail = None
        suffix = f": {detail}" if detail else ""
        raise SystemExit(f"Invitation creation failed HTTP {exc.code}{suffix}") from None

    link = origin + invitation["resume_path"]
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "session_id": invitation["session_id"],
        "turn_count": invitation["turn_count"],
        "consent_required": invitation["consent_required"],
        "resume_link": link,
        "source_type": args.source_type,
        "source_mode": source_mode,
    }
    output.write_text(json.dumps(result, indent=2) + "\n")
    os.chmod(output, 0o600)
    print(f"Invitation created for {invitation['turn_count']} preloaded turns.")
    print(f"Private invitation saved to: {output}")
    print("The link itself was not printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
