#!/usr/bin/env python3
"""Freeze original Lilly 1647 mature-body-size claims without validating them."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(path):
    return json.loads((B / path).read_text())


def write(name, payload):
    (B / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def h(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261017.json")
assert a["batch"] == "B05k"
assert a["printed_chapter"] == "CXII"
assert len(a["source_groups"]) == 13
records = []
mapping = []
for i, g in enumerate(a["source_groups"], start=1):
    sid = f"B05k-S{i:03d}"
    assert g["source_span"] == sid
    assert set(g["original_pdf_frames"]) <= {583, 584, 585}
    group_ids = []
    for claim in g["claims"]:
        no = 6734 + len(records)
        rid = f"R{no}"
        assert claim["id"] == rid, (rid, claim["id"])
        assert len(claim["historical_meaning"]) >= 35
        assert len(claim["anchor_not_diplomatic"]) >= 12
        assert not (
            claim["verified_human_prediction"]
            or claim["medical_prediction_validated"]
            or claim["runtime_promoted"]
        )
        records.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": sid,
                "original_pdf_pages": g["original_pdf_frames"],
                "role": claim["role"],
                "printed_chapter": (
                    "CXII"
                    if claim["role"] != "next_chapter_navigation"
                    else "CXIII_NAVIGATION_ONLY"
                ),
                "editorial_chapter": (
                    "CXIII"
                    if claim["role"] != "next_chapter_navigation"
                    else "CXIV_NAVIGATION_ONLY"
                ),
                "anchor_not_diplomatic": claim["anchor_not_diplomatic"],
                "meaning_historical_only": claim["historical_meaning"],
                "confidence_class": claim["qualification"],
                "historical_documentary_accepted": True,
                "independent_human_size_validation": False,
                "medical_or_metabolic_validation": False,
                "ancestry_or_stigma_classification_validated": False,
                "runtime_rule_promoted": False,
            }
        )
        group_ids.append(rid)
    mapping.append(
        {
            "source_span": sid,
            "pdf_pages": g["original_pdf_frames"],
            "passage_group": g["source_group"],
            "record_ids": group_ids,
        }
    )
assert len(records) == 31
assert [r["record_number"] for r in records] == list(range(6734, 6765))
assert sum(r["role"] == "next_chapter_navigation" for r in records) == 2
assert len({r["id"] for r in records}) == 31
assert len({g["source_span"] for g in mapping}) == 13

original_pages = {}
for n in range(583, 587):
    path = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = path.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8")
    assert len(raw) > 150000
    original_pages[str(n)] = {
        "path": str(path.relative_to(B)),
        "bytes": len(raw),
        "sha256": h(path),
        "original_printed_folio": {583: "549", 584: "542", 585: "543", 586: "552"}[n],
        "role": ("chapter_body" if n in (583, 584) else "following_chapter_context"),
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05k",
        "source": "William Lilly 1647 original first edition, Wellcome b30338724",
        "complete_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [583, 584],
        "following_chapter_pdf_frame": 585,
        "folio_note": (
            "Source PDF583 folio549, PDF584 folio542, PDF585 folio543, "
            "PDF586 folio552: printed numerals regress but physical chapter "
            "content continues; do not rearrange by printed folio."
        ),
        "images": original_pages,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05k",
        "source_groups": mapping,
        "group_count": len(mapping),
        "record_count": 31,
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05k",
        "issues": [
            (
                "Lilly's 'first part'/'latter part' sign divisions are categorical and "
                "are not assigned exact degree cutoffs in these two original source "
                "pages; do not invent numerical thresholds."
            ),
            (
                "Height, body mass, weight and body adiposity are distinct variables; "
                "this text supplies no objective units or documented human anthropometry."
            ),
            (
                "The Almuten 'that mediety of the Signe ... doth not occupie' passage is "
                "unexpectedly worded and needs another expert first-edition reading "
                "before programmatic application."
            ),
            (
                "The source employs partile aspects, orb moieties, Mars absence, "
                "multiple testimonies, agreement and equal-dominion tie-breaking; do not "
                "retrospectively select convenient branches."
            ),
            (
                "The author specifically excludes a period category he calls 'Monsters'; "
                "preserve that historical refusal but never use it as present-day "
                "disability or other stigmatizing classification."
            ),
            (
                "The source invokes an earlier book's planetary descriptions and is not "
                "independent replication of its own predictions."
            ),
            (
                "Approximate thirty-year/mature-age constraint is a qualification, not a "
                "measured change-at-thirty prediction or a source of treatment advice."
            ),
            (
                "The printed folio 549,542,543,552 regressions are typography artifacts "
                "rather than evidence of missing body-form text."
            ),
            (
                "No sex, cohort, age-adjusted, region, diet or health comparison "
                "baseline or independently blinded human trial occurs here."
            ),
            (
                "Original first-edition source images and selective brief anchors "
                "preserved, but no full diplomatic transcription or detailed symbolic "
                "sign-glyph parity audit conducted."
            ),
        ],
        "no_clinical_or_personal_disability_inference": True,
        "diplomatic_transcription_complete": False,
    },
)
write(
    "RULES.json",
    {
        "batch": "B05k",
        "status": "ORIGINAL_HISTORICAL_DOCUMENTARY_LOCALLY_ADMITTED",
        "printed_chapter": "CXII",
        "editorial_chapter": "CXIII",
        "record_count": 31,
        "first_record": "R6734",
        "last_record": "R6764",
        "source_groups": 13,
        "substantive_historical_annotations": 29,
        "following_navigation_annotations": 2,
        "source_body_frames": [583, 584],
        "following_heading_frame": 585,
        "original_diplomatic_transcription": False,
        "empirical_validations": 0,
        "real_human_body_size_validation": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
accept = {
    "batch": "B05k",
    "status": "LOCALLY_VERIFIED_DOCUMENTARY_PENDING_GITHUB",
    "previous_lilly": 6733,
    "new_records": 31,
    "lilly_if_published": 6764,
    "retained_ptolemy": 1066,
    "total_historical_if_published": 7830,
    "substantive": 29,
    "following_navigation": 2,
    "source_group_count": 13,
    "source_witness_original_frames": [583, 584, 585, 586],
    "original_following_printed_chapter": "CXIII",
    "original_following_pdf_frame": 585,
    "rules_sha256": h(B / "RULES.json"),
    "source_authoring_sha256": h(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
    "new_human_weight_validations": 0,
    "new_medical_validations": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
write("ACCEPTANCE.json", accept)
print(json.dumps(accept, indent=2))
