"""Append an independently sourced personal-answer questionnaire to the owner's prior survey.

Privacy: source answer contents and merged output are *private local files*.
Do not execute with third-party respondent data. This transformer never joins
anonymous/other-person interview files and never changes a frozen primary answer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

OLD_SCHEMA = "life-patterns-owner-results-with-experience-addendum-v1"
NEW_SCHEMA = "life-patterns-private-personal-survey-source-stack-v2"
ADD_SCHEMA = "life-patterns-20261021-external-questionnaire-personal-answer-import-v1"
PENDING = "FUTURE_OUTCOME_PENDING_NO_ANSWER"
MISSING = "EXPLICIT_MISSING_UNCLEAR_OR_DECLINED"
MARKED = "MARKED_RESPONSE"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> tuple[bytes, dict[str, Any]]:
    raw = path.read_bytes()
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise ValueError(f"Expected JSON object: {path.name}")
    return raw, obj


def audit_original_sources(master: dict[str, Any]) -> None:
    if master.get("schema") != OLD_SCHEMA:
        raise ValueError("Unknown personal baseline survey schema.")
    sources = master.get("historical_original_sources")
    if not isinstance(sources, list) or len(sources) != 3:
        raise ValueError("Personal baseline must retain all three original source files.")
    expected_source_names = {
        "my-life-patterns-v3-3-role-entry.json",
        "Life-Patterns-FINAL-Primary-84-Turns-2026-10-09.json",
        "Life-Patterns-FINAL-CF003-3-Turns-2026-10-09.json",
    }
    if {s.get("filename") for s in sources} != expected_source_names:
        raise ValueError("Unrecognized original survey source identities.")
    for source in sources:
        if sha(source["text"].encode("utf-8")) != source["sha256"]:
            raise ValueError("Historical source hash mismatch.")
        assert isinstance(json.loads(source["text"]), dict)
    em = master.get("experience_addendum")
    if (
        not isinstance(em, dict)
        or em.get("schema") != "life-patterns-experience-pilot-answers-v1"
        or len(em.get("responses", [])) != 8
    ):
        raise ValueError("Baseline's eight experience answers are missing.")


def check_external_addendum(record: dict[str, Any], expected_source_sha: str) -> Counter:
    if record.get("schema") != ADD_SCHEMA:
        raise ValueError("Wrong external answer import schema.")
    if record.get("source_odg_sha256") != expected_source_sha:
        raise ValueError("Uploaded source identity mismatch.")
    if record.get("question_count") != 31:
        raise ValueError("Question count changed from original submitted form.")
    answers = record.get("responses")
    if not isinstance(answers, list):
        raise ValueError("Missing external questionnaire answers.")
    if [x.get("id") for x in answers] != [f"Q{i:02}" for i in range(1, 32)]:
        raise ValueError("Missing, reordered or duplicated external questions.")
    counts: Counter[str] = Counter()
    for index, item in enumerate(answers, 1):
        status = item.get("state")
        counts[status] += 1
        if (
            not isinstance(item.get("question"), str)
            or not item["question"].startswith(item["id"])
            or not isinstance(item.get("reference_window"), str)
            or not item["reference_window"].startswith("Reference window:")
            or not isinstance(item.get("verbatim_user_evidence_field"), str)
            or not item["verbatim_user_evidence_field"].startswith("Evidence or clarification")
        ):
            raise ValueError(f"Source question/response text missing: {index}.")
        if status == PENDING:
            if index <= 26 or item.get("marked_choice") is not None:
                raise ValueError("Future unanswered item is not an observed negative.")
        elif status == MISSING:
            if "Missing / unclear" not in (item.get("marked_choice") or ""):
                raise ValueError("Ambiguous/missing response was silently recoded.")
        elif status == MARKED:
            if not item.get("marked_choice"):
                raise ValueError("Observed item has no actual marked option.")
        else:
            raise ValueError(f"Unsupported external response state: {status!r}")
    if counts != Counter({MARKED: 21, MISSING: 5, PENDING: 5}):
        raise ValueError(f"Source marks changed: {dict(counts)}")
    prior = record.get("state_counts") or {}
    if (
        prior.get("marked_responses") != 26
        or prior.get("marked_other_than_missing") != 21
        or prior.get("marked_missing_or_unclear") != 5
        or prior.get("future_unmarked") != 5
    ):
        raise ValueError("Extraction manifest contradicts exact recorded answers.")
    return counts


def build(baseline: Path, added: Path, out: Path, *, expected_source_sha: str) -> dict[str, Any]:
    baseline_raw, older = load(baseline)
    addendum_raw, new = load(added)
    audit_original_sources(older)
    counts = check_external_addendum(new, expected_source_sha)
    if out.exists():
        raise FileExistsError(out)
    result = {
        "schema": NEW_SCHEMA,
        "research_status": "OWNER_PRIVATE_POST_HOC_DEVELOPMENT_NOT_FROZEN_ASTROLOGY_SCORE",
        "preceding_complete_survey_sha256": sha(baseline_raw),
        "new_questionnaire_extract_sha256": sha(addendum_raw),
        "source_original_odg_sha256": expected_source_sha,
        "baseline_original_schema": OLD_SCHEMA,
        "baseline": older,
        "external_blinded_questionnaire_addendum": new,
        "preservation": {
            "baseline_surveys_kept_unchanged": True,
            "v33_original_answer_source": True,
            "primary_84_original_source": True,
            "separate_cf003_3_original_source": True,
            "experience_em8_unchanged": True,
            "external_marked_observations": 26,
            "source_explicit_missing_unclear": 5,
            "future_items_unobserved_and_not_negative": 5,
            "excludes_other_participant_records": True,
            "no_double_count_claim": (
                "Earlier survey sources overlap and external questionnaire topics "
                "can repeat them; counts are source records, not independent personality traits."
            ),
        },
        "future_boundaries": {
            "source_claim_of_frozen_prediction_not_verified": True,
            "new_answers_not_used_to_revise_original_chart_forecasts": True,
            "future_question_ids": [f"Q{i:02}" for i in range(27, 32)],
        },
    }
    raw = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode()
    out.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(out, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(raw)
    readback = json.loads(out.read_bytes())
    if readback["baseline"] != older or readback["external_blinded_questionnaire_addendum"] != new:
        out.unlink()
        raise AssertionError("Lossless merge readback mismatch.")
    if sha(baseline.read_bytes()) != sha(baseline_raw):
        raise AssertionError("Original master was changed.")
    return {
        "status": "private_master_created",
        "old_sha256": sha(baseline_raw),
        "new_source_sha256": expected_source_sha,
        "new_answer_extract_sha256": sha(addendum_raw),
        "merged_sha256": sha(raw),
        "bytes": len(raw),
        "counts": dict(counts),
        "previous_original_sources": 3,
        "previous_experience_answers": 8,
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--baseline", type=Path, required=True)
    p.add_argument("--addendum", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--odg-sha256", required=True)
    args = p.parse_args()
    print(
        json.dumps(
            build(
                args.baseline,
                args.addendum,
                args.output,
                expected_source_sha=args.odg_sha256,
            ),
            sort_keys=True,
        )
    )
