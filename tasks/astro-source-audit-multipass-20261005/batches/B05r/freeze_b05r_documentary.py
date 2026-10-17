#!/usr/bin/env python3
"""Original first-edition unnumbered sibling introduction: source only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def load(name):
    return json.loads((B / name).read_text())


def dump(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


source = load("SOURCE_FIRST_AUTHORING_20261017.json")
assert source["batch"] == "B05r"
assert source["section"] == "UNNUMBERED_THIRD_HOUSE_KINRED"
assert source["original_body_pdf_frames"] == [598]
assert len(source["groups"]) == 5
records, mapping = [], []
for index, group in enumerate(source["groups"], 1):
    sid = f"B05r-S{index:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {598, 599}
    ids = []
    for c in group["claims"]:
        no = 7127 + len(records)
        assert c["id"] == f"R{no}"
        assert len(c["anchor_not_diplomatic"]) >= 10
        assert len(c["historical_only_meaning"]) >= 50
        assert not c["human_family_prediction_validated"]
        assert not c["runtime_promoted"]
        records.append(
            {
                "id": f"R{no}",
                "record_number": no,
                "source_span": sid,
                "original_pdf_pages": group["original_pdf_frames"],
                "role": c["role"],
                "anchor_not_diplomatic": c["anchor_not_diplomatic"],
                "historical_source_meaning": c["historical_only_meaning"],
                "source_qualification": c["source_qualification"],
                "accepted_historical_documentation": True,
                "validated_actual_sibling_number": False,
                "validated_sibling_relationship_quality": False,
                "medical_or_family_advice_authorized": False,
                "promoted_to_runtime_model": False,
            }
        )
        ids.append(c["id"])
    mapping.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["description"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 12
assert [x["record_number"] for x in records] == list(range(7127, 7139))
assert [x["id"] for x in records if x["role"] == "next_chapter_navigation"] == ["R7137", "R7138"]
images = {}
for page in [598, 599, 600]:
    p = B / "evidence" / f"pdf_1647-{page}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(page)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(p),
        "printed_folio": str(page - 34),
        "role": "intro" if page == 598 else "context",
    }
dump(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05r",
        "original_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "source": "Lilly 1647 original first edition Wellcome b30338724",
        "intro_pdf_frame": 598,
        "numbered_CXVIII_heading_pdf_frame": 598,
        "following_CXIX_heading_pdf_frame": 600,
        "source_images": images,
    },
)
dump(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05r",
        "source_groups": mapping,
        "record_count": 12,
        "substantive": 10,
        "next_heading_navigation": 2,
    },
)
limitations = [
    "Historical assertion that first-born nativity can indicate the number "
    "of later siblings is not supported by independent birth records.",
    "The author limits the first-born count to subsequent siblings; "
    "do not interpret it as measuring people born before the firstborn.",
    "The fallback to a different native's chart when firstborn birth data "
    "are missing is acknowledged by the source and must not be erased.",
    "Whether there are siblings, their described condition, and familial "
    "amity/concord are three different outcomes, not one composite score.",
    "No birth time accuracy, sample, non-astrology family-size baseline, "
    "fertility-control variables, age cohorts or blinded tests appear.",
    "The unnumbered introduction is not the next printed chapter CXVIII; "
    "its separate numbered sibling source begins lower in PDF598.",
    "No actual person's siblings, relationship quality, health, "
    "fertility or genealogy can be inferred from this historical text.",
    "Source images and selective anchors are preserved; a complete "
    "diplomatic transcription and scientific assessment remain open.",
]
dump(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05r",
        "issues": limitations,
        "new_empirical_successes": 0,
        "runtime_promotions": 0,
    },
)
dump(
    "RULES.json",
    {
        "batch": "B05r",
        "status": "ORIGINAL_1647_UNNUMBERED_KINSHIP_HISTORICAL_ONLY",
        "section": "UNNUMBERED_THIRD_HOUSE_KINRED",
        "record_count": 12,
        "first_record": "R7127",
        "last_record": "R7138",
        "source_passage_groups": 5,
        "substantive_source_records": 10,
        "following_numbered_chapter_navigation": 2,
        "original_body_pdf_frames": [598],
        "following_CXVIII_pdf_frame": 598,
        "complete_diplomatic_transcription": False,
        "empirical_validations": 0,
        "human_sibling_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
dump(
    "ACCEPTANCE.json",
    {
        "batch": "B05r",
        "previous_lilly": 7126,
        "new_source_records": 12,
        "lilly_if_published": 7138,
        "retained_ptolemy": 1066,
        "combined_if_published": 8204,
        "substantive_records": 10,
        "navigation": 2,
        "first_numbered_chapter_after_intro": "CXVIII",
        "numbered_chapters_added": 0,
        "next_original_pdf_page": 598,
        "source_sha256": sha(B / "RULES.json"),
        "empirical_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B05r: 12 original historic annotations R7127–R7138; no science claims")
