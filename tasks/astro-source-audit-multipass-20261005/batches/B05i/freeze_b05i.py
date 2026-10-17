#!/usr/bin/env python3
"""Source-first historical-only freeze of 1647 original printed CHAP CX (stature)."""

import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def load(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def write(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


input_data = load("SOURCE_FIRST_AUTHORING.json")
assert input_data["batch"] == "B05i"
assert len(input_data["groups"]) == 9
assert input_data["original_pages"]["source_body"] == [580, 581]
rules = []
mapping = []
for group in input_data["groups"]:
    assert set(group["original_pdf_pages"]) <= {580, 581, 582}
    mapped = []
    for claim in group["claims"]:
        expected = 6645 + len(rules)
        assert claim["record"] == f"R{expected}"
        assert not claim["claimed_validation"]
        assert claim["role"] in {
            "heading",
            "selection",
            "selection_tiebreak",
            "oriental",
            "occidental",
            "override",
            "override_condition",
            "qualification",
            "proportions",
            "proportions_component",
            "next_chapter_navigation",
        }
        record = {
            "id": claim["record"],
            "record_number": expected,
            "batch": "B05i",
            "source_span": group["id"],
            "pdf_pages": group["original_pdf_pages"],
            "role": claim["role"],
            "original_anchor_not_diplomatic": claim["anchor_not_diplomatic"],
            "historical_only_meaning": claim["meaning_historical_only"],
            "historical_documentary_accepted": True,
            "independently_tested_height_prediction": False,
            "validated_medical_or_ancestry_prediction": False,
            "promoted_into_runtime": False,
        }
        rules.append(record)
        mapped.append(record["id"])
    mapping.append(
        {
            "source_span": group["id"],
            "pdf_pages": group["original_pdf_pages"],
            "source_group": group["source_group"],
            "mapped_record_ids": mapped,
        }
    )
assert len(rules) == 27
assert [r["record_number"] for r in rules] == list(range(6645, 6672))
nav = [r for r in rules if r["role"] == "next_chapter_navigation"]
assert len(nav) == 3 and all(r["record_number"] >= 6669 for r in nav)
assert len([r for r in rules if r["role"] in ("oriental", "occidental")]) == 10
assert [
    r["original_anchor_not_diplomatic"].split()[0]
    for r in rules
    if r["role"] in ("oriental", "occidental")
] == [
    "Saturn",
    "Saturn",
    "Jupiter",
    "Jupiter",
    "Mars",
    "Mars",
    "Venus",
    "Venus",
    "Mercury",
    "Mercury",
]
images = {}
for p in range(580, 583):
    path = BASE / "evidence" / f"pdf_1647-{p}.jpg"
    raw = path.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 200000
    images[str(p)] = {
        "file": str(path.relative_to(BASE)),
        "sha256": digest(path),
        "bytes": len(raw),
        "printed_folio_as_seen": {580: "538", 581: "539", 582: "548"}[p],
    }

write(
    "ORIGINAL_IMAGE_MANIFEST.json",
    {
        "batch": "B05i",
        "original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "source": "Wellcome b30338724 original first edition images",
        "pagination_note": (
            "PDF580 appears printed538 after PDF579/printed545; PDF581 printed539; "
            "PDF582 printed548. Text and chapter boundaries are continuous, not a "
            "reordered leaf."
        ),
        "images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05i",
        "groups": mapping,
        "source_group_count": 9,
        "record_count": 27,
    },
)
write(
    "RULES.json",
    {
        "batch": "B05i",
        "status": "HISTORICAL_1647_SOURCE_LOCALLY_ACCEPTED_ONLY",
        "printed_chapter": "CX",
        "editorial_chapter": "CXI",
        "record_count": 27,
        "first_record": "R6645",
        "last_record": "R6671",
        "source_group_count": 9,
        "substantive": 24,
        "next_navigation": 3,
        "original_pdf_frames": [580, 581, 582],
        "original_full_diplomatic_transcription": False,
        "independent_actual_height_predictive_tests": 0,
        "actual_human_or_medical_validations": 0,
        "empirical_validations": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
write(
    "UNRESOLVED.json",
    {
        "batch": "B05i",
        "notes": [
            "Historic relative stature adjectives are not numerical height thresholds.",
            (
                "Oriental/occidental orientations are modified by dispositor, house, "
                "sign and strongest-planet priority; no unfrozen fallback may be added "
                "after outcomes are seen."
            ),
            (
                "No independently documented human height comparisons, measurement "
                "units, age, sex or ancestry adjustments are provided by Lilly's source."
            ),
            (
                "Any future human test must preregister sign, aspect and ranking "
                "procedures and compare against height prediction from sex, age, cohort "
                "and geography."
            ),
            (
                "Physical form and facial colour claims are not grounds for race, "
                "ancestry, medical, or stigma classifications."
            ),
            (
                "The original PDF580 and PDF581 folios regress to 538 and 539 despite "
                "source continuity; PDF582 shows expected 548."
            ),
            (
                "This is a source-anchored paraphrase of original images, not full "
                "diplomatic transcription, numeric rule implementation or clinical "
                "evidence."
            ),
            (
                "Following CHAP CXI (sign and face/hair) remains a distinct source batch "
                "and is not admitted here."
            ),
        ],
    },
)
accepted = {
    "batch": "B05i",
    "previous_lilly": 6644,
    "new_historical_source_annotations": 27,
    "lilly_if_published": 6671,
    "retained_ptolemy": 1066,
    "historical_combined_if_published": 7737,
    "substantive_annotations": 24,
    "following_navigation": 3,
    "original_body_pdf_frames": [580, 581],
    "following_chapter_pdf_frame": 581,
    "following_context_frame": 582,
    "next_printed_chapter": "CXI",
    "next_editorial_chapter": "CXII",
    "new_intelligence_validations": 0,
    "new_height_validations": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "rules_sha256": digest(BASE / "RULES.json"),
    "remote_published": False,
}
write("ACCEPTANCE.json", accepted)
print(json.dumps(accepted, indent=2))
