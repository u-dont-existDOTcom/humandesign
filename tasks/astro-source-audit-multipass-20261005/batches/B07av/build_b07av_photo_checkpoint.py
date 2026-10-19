#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve exact original-source bibliographic identifiers.
"""Checkpoint exact physical source images for Lilly original CLXXIII before extraction."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = "tasks/astro-source-audit-multipass-20261005"
OLD = ROOT / T / "batches/B07au/evidence"
PHOTO = {
    "first_edition_1647": {
        738: OLD / "1647_original-772.jpg",
        739: OLD / "1647_original-773.jpg",
        740: B / "evidence/original_1647_CLXXIII_CLXXIV-774.jpg",
        741: B / "evidence/1647_original_775-775.jpg",
    },
    "independently_typeset_1659": {
        738: OLD / "1659_original_djvu_767.jpg",
        739: OLD / "1659_original_djvu_768.jpg",
        740: B / "evidence/independent_1659_CLXXIII_CLXXIV_djvu769.jpg",
        741: B / "evidence/independent_1659_djvu770.jpg",
    },
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


out = {}
for label, by_page in PHOTO.items():
    out[label] = []
    for printed, f in by_page.items():
        assert f.is_file(), f
        assert f.stat().st_size > 250_000, f
        b = f.read_bytes()
        assert b[:2] == bytes.fromhex("ffd8"), f
        out[label].append(
            {
                "printed_folio": printed,
                "PDF_or_DjVu_frame": printed + (34 if "1647" in label else 29),
                "repo_relative_file": str(f.relative_to(ROOT)),
                "sha256": hashlib.sha256(b).hexdigest(),
                "bytes": len(b),
                "first_reader_source_only": True,
            }
        )
assert [x["printed_folio"] for x in out["first_edition_1647"]] == [738, 739, 740, 741]
assert len(out["independently_typeset_1659"]) == 4
data = {
    "schema": "LILLY_CLXXIII_FIRST_AND_SECOND_EDITION_SOURCE_PREPARATION_V1",
    "batch": "B07av",
    "status": "PHOTO_SOURCE_CHECKPOINT_ONLY_NOT_CANONICALLY_ACCEPTED",
    "root_research_goal": "OPEN",
    "full_1647_first_edition_pdf_sha256": "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
    "source_title": "Of the Returne of the Planets to their owne Places, and to the places of other Planets in the Radix",
    "source_chapter_printed_number": "CLXXIII",
    "source_physically_begins_at": {"PDF_frame": 772, "printed_folio": 738},
    "source_physically_ends_at": {"PDF_frame": 775, "printed_folio": 741},
    "next_distinct_source_printed": "CLXXIV — Of the Transit of the Planets",
    "next_source_chapter_starts_below_divider_PDF775": True,
    "prior_accepted_historical_Lilly_records": 12803,
    "next_prospective_historical_source_record": "R12804",
    "previous_B07au_photo_files_reused_without_edits": True,
    "source_original_visual_evidence": out,
    "historical_source_stars_in_section": ["Saturn", "Jupiter", "Mars", "Venus", "Mercury", "Moon"],
    "source_critical_second_human_review_completed": False,
    "primary_original_1647_printed_rulebook_full_study_completed": False,
    "real_human_predictions_validated": 0,
    "runtime_model_promotions": 0,
}
f = B / "SOURCE_PHOTO_CHECKPOINT_V1.json"
f.write_text(json.dumps(data, indent=2) + "\n")
print(
    json.dumps(
        {
            "chapter": "CLXXIII",
            "printed_folios": [738, 739, 740, 741],
            "first_and_second_source_images": sum(len(v) for v in out.values()),
            "sha256": sha(f),
            "next": "R12804",
            "status": "checkpoint, not accepted rule",
        },
        indent=2,
    )
)
