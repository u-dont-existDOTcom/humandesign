"""Verify narrow religion/dream source witness and V7 keyword coverage.

Uses an already-archived *public* 1647 Internet Archive OCR stream. We do
not pretend that OCR recovers historical planet glyphs; the original page
facsimile and critical transcription remain a separate source fidelity task.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]
BANK = ROOT / "tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json"
CLAIMS = TASK / "LILLY-BOOK3-RELIGION-DREAMS-CLAIMS-v1.json"
OUT = TASK / "WITNESS-AND-V7-CHECK-v1.json"
EXPECTED = "7c08b55359c41049c5d43901b8da869a326f8eb852e4a30603a4b698533626aa"


def evidence(archive_ocr: Path) -> dict:
    raw = archive_ocr.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED:
        raise ValueError("Original 1647 OCR witness bytes differ; inspect before continuing.")
    text = " ".join(raw.decode("utf-8", errors="replace").casefold().split())
    # These short checks use the original OCR's historical spellings, and avoid
    # the many astronomical glyphs corrupted during the source OCR process.
    locations = {
        "religion_chapter_heading": ("chap. cxl1i.", "religion of the native"),
        "theological_non_compulsion": ("grace of god", "starres onely"),
        "religious_conversion_claim": ("converts the native from one religion to another",),
        "dream_chapter": ("of dreame", "dream"),
        "dream_quality_sections": ("significator", "sepulchers", "waters"),
        "ninth_house_content": ("ninth", "dreames"),
    }
    checks = {label: [item in text for item in needles] for label, needles in locations.items()}
    # The heading and manuscript word forms can vary by edition and OCR: record
    # false values and do not backfill results from the retyped witness.
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    questions = bank["questions"]
    if len(questions) != 79:
        raise ValueError("Unexpected V7 bank cardinality")
    words = {
        "religion_religious": r"\breligi(?:on|ous|osity)\b",
        "faith": r"\bfaith\b",
        "dreams": r"\bdreams?\b",
        "visions": r"\bvisions?\b",
        "prophecy": r"\bprophe(?:cy|s[yi]e|tic)\b",
        "divination": r"\bdivination\b",
        "awe": r"\bawe\b",
        "wonder": r"\bwonder\b",
        "synchronicities": r"\bsynchronicit(?:y|ies)\b",
        "revelation": r"\brevelations?\b",
        "spirituality": r"\bspiritual(?:ity|ly)?\b",
    }
    direct_lexical = {}
    for label, pattern in words.items():
        direct_lexical[label] = [
            question["id"]
            for question in questions
            if re.search(pattern, question["question"], re.IGNORECASE)
        ]
    claims = json.loads(CLAIMS.read_text(encoding="utf-8"))
    if claims["count"] != len(claims["records"]):
        raise ValueError("Claim source record count is stale")
    return {
        "schema": "lilly-book3-original-ocr-and-v7-audit-v1",
        "status": "HISTORICAL_TEXTUAL_CORROBORATION_NOT_ORIGINAL_FACSIMILE_GLYPH_CHECK",
        "original_1647_item": "b30338724",
        "original_1647_ocr_bytes": len(raw),
        "original_1647_ocr_sha256": digest,
        "original_ocr_phrase_checks": checks,
        "textual_check_pass_count": sum(hit for values in checks.values() for hit in values),
        "textual_check_total": sum(len(values) for values in checks.values()),
        "retyped_witness": (
            "Web-indexed retyped source with original printed pagination; "
            "laptop direct fetch returned HTTP 403."
        ),
        "original_page_facsimile_glyph_check_completed": False,
        "v7_bank_version": bank["version"],
        "v7_question_count": len(questions),
        "v7_direct_question_word_hits": direct_lexical,
        "lexical_absence_is_not_semantic_absence": True,
        "source_conditional_clauses": claims["count"],
        "historical_chart_rules_validated_on_humans": False,
        "current_participant_data_accessed": False,
        "no_live_scorer_or_questionnaire_change": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--original-ocr", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = json.dumps(evidence(args.original_ocr), indent=2, sort_keys=True) + "\n"
    if args.check:
        if OUT.read_text() != result:
            raise ValueError("Source-witness verification receipt changed.")
    else:
        OUT.write_text(result)
    print(
        json.dumps(
            {
                "result": "CHECKED" if args.check else "BUILT",
                "source_cases": json.loads(result)["source_conditional_clauses"],
                "ocr_checks": json.loads(result)["textual_check_pass_count"],
                "questions": json.loads(result)["v7_question_count"],
                "persistence": str(OUT),
            }
        )
    )


if __name__ == "__main__":
    main()
