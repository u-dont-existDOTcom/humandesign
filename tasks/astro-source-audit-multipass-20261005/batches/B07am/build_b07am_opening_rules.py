#!/usr/bin/env python3
"""Prepare source-only opening to original Lilly CLXVII, PDF752–754."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parent


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def save(p, v):
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


notes = j(B / "CLXVII_OPENING_INTERPRETIVE_NOTES_V1.json")
idx = j(ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json")
china = j(ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json")
assert idx["records_count"] == 12611
assert idx["next"]["chapter"] == "CLXVII"
assert idx["next"]["pdf_page"] == 752
assert china["sum_source_annotations"] == 262
assert len(notes["records"]) == 14
groups = {752: "B07am-S001", 753: "B07am-S002", 754: "B07am-S003"}
evidence = {}
for frame in (752, 753, 754):
    f = (
        P / "B07al/evidence/1647_original_pdf-752.jpg"
        if frame == 752
        else B / "evidence" / f"original_1647_pdf-{frame}.jpg"
    )
    assert sha(f) == notes["original_source_photo_shas"][str(frame)]
    evidence[str(frame)] = {
        "path": str(f.relative_to(ROOT)),
        "sha256": sha(f),
        "bytes": f.stat().st_size,
        "printed_folio": frame - 34,
    }
rows = []
for i, n in enumerate(notes["records"]):
    assert n["record_number"] == 12612 + i
    assert n["photo_sha256"] == evidence[str(n["pdf_frame"])]["sha256"]
    rows.append(
        {
            "id": n["id"],
            "record_number": n["record_number"],
            "batch": "B07am",
            "source_span": groups[n["pdf_frame"]],
            "original_pdf_frames": [n["pdf_frame"]],
            "role": n["role"],
            "source_anchor_not_diplomatic": n["short_photo_anchor"],
            "historical_meaning_only": n["historical_interpretation"],
            "historical_source_documented": True,
            "full_source_chapter_complete": False,
            "empirical_forecast_verified": False,
            "runtime_model_promoted": False,
        }
    )
rules = {
    "batch": "B07am",
    "status": "FIRST_1647_CLXVII_OPENING_PARTIAL_SOURCE_ONLY",
    "record_count": 14,
    "first_record": "R12612",
    "last_record": "R12625",
    "body_pdf_frames": [752, 753, 754],
    "source_groups": 3,
    "photo_witnesses": evidence,
    "chapter_complete": False,
    "next_1647_printed_conversion_tables_not_accepted": True,
    "real_person_predictions_validated": 0,
    "runtime_promotions": 0,
    "rules": rows,
}
save(B / "RULES.json", rules)
accept = {
    "batch": "B07am",
    "prior_Lilly": 12611,
    "Ptolemy_retained": 1066,
    "Chinese_V5_retained": 262,
    "historical_source_annotations_added": 14,
    "Lilly_if_accepted": 12625,
    "Western_if_accepted": 13691,
    "next_R": "R12626",
    "next_PDF": 755,
    "next_printed_folio": 721,
    "chapter_complete": False,
    "notes_SHA256": sha(B / "CLXVII_OPENING_INTERPRETIVE_NOTES_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "real_person_predictions_validated": 0,
    "runtime_promotions": 0,
}
save(B / "ACCEPTANCE.json", accept)
print(
    json.dumps(
        {
            "rules": 14,
            "next": "R12626",
            "notes_sha": accept["notes_SHA256"],
            "rules_sha": accept["rules_SHA256"],
        },
        indent=2,
    )
)
