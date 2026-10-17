#!/usr/bin/env python3
"""First-edition Lilly sibling count history, not medical/demographic prediction."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


def write(name, value):
    (B / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261017.json")
assert a["batch"] == "B05s"
assert a["printed_chapter"] == "CXVIII"
assert a["editorial_chapter"] == "CXIX"
assert a["body_original_pdf_frames"] == [598, 599, 600]
assert len(a["groups"]) == 10
rules, mapping = [], []
for n, group in enumerate(a["groups"], 1):
    sid = f"B05s-S{n:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_pages"]) <= {598, 599, 600, 601}
    refs = []
    for clause in group["claims"]:
        record_number = 7139 + len(rules)
        rid = f"R{record_number}"
        assert clause["id"] == rid
        assert len(clause["anchor_not_diplomatic"]) >= 11
        assert len(clause["historical_meaning"]) >= 45
        assert not (clause["human_sibling_prediction_validated"] or clause["runtime_promoted"])
        rules.append(
            {
                "id": rid,
                "record_number": record_number,
                "source_span": sid,
                "original_pdf_pages": group["original_pdf_pages"],
                "role": clause["role"],
                "printed_chapter": (
                    "CXVIII"
                    if clause["role"] != "next_chapter_navigation"
                    else "CXIX_NAVIGATION_ONLY"
                ),
                "original_anchor_not_diplomatic": clause["anchor_not_diplomatic"],
                "meaning_historical_only": clause["historical_meaning"],
                "qualification": clause["source_qualification"],
                "historical_documentary_accepted": True,
                "diplomatic_transcription_complete": False,
                "independent_sibling_number_validation": False,
                "human_sex_or_fertility_prediction_validated": False,
                "clinical_or_family_planning_advice_authorized": False,
                "runtime_rule_promoted": False,
            }
        )
        refs.append(rid)
    mapping.append(
        {
            "source_span": sid,
            "original_pdf_pages": group["original_pdf_pages"],
            "source_group": group["source_group"],
            "record_ids": refs,
        }
    )
assert len(rules) == 48
assert [x["record_number"] for x in rules] == list(range(7139, 7187))
assert sum(r["role"] == "sign_source" for r in rules) == 12
assert [x["id"] for x in rules if x["role"] == "next_chapter_navigation"] == ["R7185", "R7186"]
images = {}
for pdf in range(598, 603):
    p = B / "evidence" / f"pdf_1647-{pdf}.jpg"
    data = p.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 180000
    images[str(pdf)] = {
        "file": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(data),
        "printed_page": str(pdf - 34),
        "role": "chapter_body" if pdf <= 600 else "following_context",
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05s",
        "source": "William Lilly Christian Astrology 1647, Wellcome b30338724",
        "full_original_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [598, 599, 600],
        "next_chapter_CXIX_heading_pdf": 600,
        "next_next_chapter_CXX_heading_pdf": 601,
        "images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05s",
        "groups": mapping,
        "record_count": 48,
        "substantive": 46,
        "next_navigation": 2,
        "sign_specific_records": 12,
    },
)
limits = [
    "The source's third-house five-degree cusp boundaries must "
    "not be implemented without historically correct house "
    "computations and explicit end-point inequalities.",
    "The Mars/brothers, Moon/sisters division is a historical "
    "astrological stereotype, not an empirical sex predictor.",
    "The optional lunar node included among fruitful or barren "
    "planets has unclear glyph/operator proof in the first "
    "edition and must remain optional and unresolved.",
    "The claimed many/few/none and moderate sibling categories "
    "have no objective count thresholds or registered accuracy.",
    "Age at birth, family planning, fertility, infant mortality, "
    "marriage patterns, contraception, geography and socioeconomic "
    "conditions are strong non-astrological family-size factors.",
    "Fruitful planets/signs and barren planets/signs combine as "
    "conditional paired prerequisites; mixed combinations "
    "permit a third ambiguous result.",
    "Mercury is explicitly said to change according to its "
    "configuration with purported fruitful or barren planets.",
    "All twelve sign classifications and their periodic imagery "
    "are author assertions, not medical claims about fertility.",
    "The Scorpio exception (historically called fruitful despite "
    "Mars rulership) prevents a ruler-only fertility shortcut.",
    "An exact aspect priority chain, partile over platick, "
    "has no specified numerical tolerance on these pages.",
    "No real sibling birth record, independent chart information, "
    "prospective outcomes or blind statistical tests were checked.",
    "Printed CXIX on sibling condition begins below another "
    "divider PDF600 and is not admitted as sibling count evidence.",
    "The original source was visually inspected and clause-level "
    "paraphrases stored, but no full diplomatic transcription "
    "or independent astrological efficacy was established.",
]
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05s",
        "issues": limits,
        "independent_human_family_validations": 0,
        "clinical_family_planning_uses_authorized": False,
        "runtime_promotions": 0,
    },
)
write(
    "RULES.json",
    {
        "batch": "B05s",
        "status": "ORIGINAL_1647_SIBLING_NUMBER_HISTORICAL_LOCALLY_ADMITTED",
        "printed_chapter": "CXVIII",
        "editorial_chapter": "CXIX",
        "record_count": 48,
        "first_record": "R7139",
        "last_record": "R7186",
        "source_groups": 10,
        "substantive_historical_records": 46,
        "next_chapter_navigation": 2,
        "sign_record_count": 12,
        "original_body_pdf_frames": [598, 599, 600],
        "following_printed_chapter": "CXIX",
        "following_chapter_pdf": 600,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "independent_family_count_validations": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
write(
    "ACCEPTANCE.json",
    {
        "batch": "B05s",
        "previous_lilly": 7138,
        "new_historical_source_records": 48,
        "lilly_if_published": 7186,
        "ptolemy_retained": 1066,
        "combined_if_published": 8252,
        "substantive": 46,
        "navigation": 2,
        "zodiac_sign_items": 12,
        "source_group_count": 10,
        "following_printed_chapter": "CXIX",
        "next_original_pdf_frame": 600,
        "source_rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "human_fertility_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original sibling existence history R7139–R7186, 48 annotations")
