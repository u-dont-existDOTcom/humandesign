#!/usr/bin/env python3
"""Lilly 1647 childbirth labour chapter: documentary text, not clinical prediction."""

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
assert source["batch"] == "B05y"
assert source["printed_chapter"] == "CXXIII"
assert source["body_original_pdf_frame"] == 606
assert len(source["groups"]) == 7
records, reverse = [], []
for i, group in enumerate(source["groups"], 1):
    sid = f"B05y-S{i:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {606, 607}
    ids = []
    for c in group["claims"]:
        number = 7411 + len(records)
        key = f"R{number}"
        assert c["id"] == key
        assert len(c["original_anchor_not_diplomatic"]) >= 7
        assert len(c["historical_source_meaning"]) >= 50
        assert not c["human_childbirth_outcome_validated"]
        assert not c["runtime_promoted"]
        records.append(
            {
                "id": key,
                "record_number": number,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": c["role"],
                "anchor_not_diplomatic": c["original_anchor_not_diplomatic"],
                "meaning_historical_only": c["historical_source_meaning"],
                "qualification": c["qualification"],
                "historical_source_accepted": True,
                "human_pregnancy_complication_validated": False,
                "human_maternal_mortality_predicted": False,
                "human_neonatal_outcome_predicted": False,
                "medical_advice_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(key)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "passage_group": group["source_group"],
            "mapped_ids": ids,
        }
    )
assert len(records) == 30
assert [x["record_number"] for x in records] == list(range(7411, 7441))
assert [x["id"] for x in records if x["role"] == "next_chapter_navigation"] == ["R7439", "R7440"]
images = {}
for n in (606, 607, 608):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    data = p.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 150000
    images[str(n)] = {
        "file": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(data),
        "printed_folio": str(n - 34),
        "role": "childbirth_chapter" if n == 606 else "next_chapter_context",
    }
dump(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05y",
        "source": "Lilly 1647 original first edition Wellcome b30338724",
        "volume_pdf_sha256": ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"),
        "childbirth_body_frame": 606,
        "following_printed_CXXIIII_heading_frame": 606,
        "images": images,
    },
)
dump(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05y",
        "source_groups": reverse,
        "record_count": 30,
        "source_groups_count": 7,
        "substantive": 28,
        "navigation": 2,
    },
)
limits = [
    (
        "Ancient astrology claims of birth complications, obstetric danger "
        "and maternal death are historically unvalidated and must never "
        "inform clinical or pregnancy decisions."
    ),
    (
        "The original oblique/long ascension sign glyphs and right-ascension "
        "family classifications require specialist verification before "
        "computerized chart rules."
    ),
    (
        "Dangerous childbirth is a compound oblique Ascendant plus "
        "affliction or node condition; it is not simply a sign-based birth "
        "risk."
    ),
    (
        "Favorable delivery is offered through several partially overlapping "
        "alternatives, allowing extensive retrospective choice of apparent "
        "successes."
    ),
    (
        "The manuscript uses different zodiac signs for men's and women's "
        "natal charts, period sex/gender categories and no actual birth "
        "records."
    ),
    (
        "Mars/Saturn condition in twelfth, slow/retrograde/stationary and "
        "Moon-in-oblique condition, tenth ruler in eighth are different "
        "source branches."
    ),
    (
        "No human pregnancy care records, duration of labor, birth outcome, "
        "mother-child survival, era-correct maternal death baseline or "
        "controls were supplied."
    ),
    (
        "The author 'may be doubted' maternal childbirth mortality claim is "
        "hedged, not a quantified prospective risk or direct prediction."
    ),
    (
        "No clinical use, pregnancy monitoring or medication/surgical "
        "interpretation is permitted from such source hypotheses."
    ),
    (
        "The subsequent printed CXXIIII on paternal inheritance begins later "
        "on the SAME frame606 and has separate substantive original source "
        "rules."
    ),
    (
        "Original source images and selective brief anchors are preserved; "
        "no full diplomatic glyph transcription or human-prospectively "
        "tested accuracy."
    ),
]
dump(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05y",
        "issues": limits,
        "independently_validated_birth_outcomes": 0,
        "medical_advice_authorized": False,
        "runtime_promotions": 0,
    },
)
dump(
    "RULES.json",
    {
        "batch": "B05y",
        "status": "FIRST_EDITION_ORIGINAL_MEDICAL_CLAIMS_HISTORICAL_ONLY",
        "printed_chapter": "CXXIII",
        "editorial_chapter": "CXXIV",
        "record_count": 30,
        "first_record": "R7411",
        "last_record": "R7440",
        "substantive": 28,
        "next_chapter_navigation": 2,
        "source_groups": 7,
        "original_body_frame": 606,
        "following_heading_frame": 606,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "clinical_validation_successes": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
dump(
    "ACCEPTANCE.json",
    {
        "batch": "B05y",
        "status": "SOURCE_ONLY_ARCHIVE_ACCEPTED_LOCALLY_PENDING_GITHUB",
        "previous_lilly": 7410,
        "new_records": 30,
        "lilly_if_published": 7440,
        "ptolemy_retained": 1066,
        "combined_if_published": 8506,
        "substantive": 28,
        "navigation": 2,
        "source_groups": 7,
        "next_printed_chapter": "CXXIIII",
        "next_original_pdf_page": 606,
        "rules_sha256": sha(B / "RULES.json"),
        "empirical_validations": 0,
        "human_mortality_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B05y original mother labor R7411-R7440, source 30, empirical 0")
