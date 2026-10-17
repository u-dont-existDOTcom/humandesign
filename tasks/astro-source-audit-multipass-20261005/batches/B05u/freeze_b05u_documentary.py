#!/usr/bin/env python3
"""Freeze original 1647 sibling concord as historical source, not human prediction."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def load(name):
    return json.loads((B / name).read_text())


def save(name, value):
    (B / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = load("SOURCE_FIRST_AUTHORING_20261017.json")
assert a["batch"] == "B05u"
assert a["printed_chapter"] == "CXX"
assert a["body_original_pdf_frames"] == [601]
assert len(a["groups"]) == 8
rows, reverse = [], []
for index, group in enumerate(a["groups"], 1):
    sid = f"B05u-S{index:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {601, 602}
    group_ids = []
    for clause in group["claims"]:
        no = 7209 + len(rows)
        rid = f"R{no}"
        assert clause["id"] == rid
        assert len(clause["anchor_not_diplomatic"]) >= 7
        assert len(clause["historical_meaning"]) > 45
        assert not clause["actual_family_concord_validated"]
        assert not clause["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": sid,
                "original_pdf_pages": group["original_pdf_frames"],
                "role": clause["role"],
                "source_anchor_not_diplomatic": clause["anchor_not_diplomatic"],
                "historical_only_meaning": clause["historical_meaning"],
                "source_qualification": clause["qualification"],
                "source_documentation_accepted": True,
                "verified_family_relationship_prediction": False,
                "validated_financial_or_legal_claim": False,
                "clinical_or_personal_accusation_authorized": False,
                "runtime_rule_promoted": False,
            }
        )
        group_ids.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "pdf_pages": group["original_pdf_frames"],
            "passage_group": group["group"],
            "mapped_ids": group_ids,
        }
    )
assert len(rows) == 44
assert [r["record_number"] for r in rows] == list(range(7209, 7253))
assert [r["id"] for r in rows if r["role"] == "next_chapter_navigation"] == ["R7251", "R7252"]
assert len({r["id"] for r in rows}) == len(rows)
images = {}
for page in (601, 602):
    path = B / "evidence" / f"pdf_1647-{page}.jpg"
    raw = path.read_bytes()
    assert len(raw) > 150000 and raw[:2] == bytes.fromhex("ffd8")
    images[str(page)] = {
        "file": str(path.relative_to(B)),
        "sha256": sha(path),
        "bytes": len(raw),
        "printed_folio": {601: "567", 602: "568"}[page],
        "role": "body" if page == 601 else "next_heading_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05u",
        "source": "William Lilly Christian Astrology original 1647 Wellcome b30338724",
        "original_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "source_body_frame": 601,
        "next_chapter_heading_frame": 602,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05u",
        "source_groups": reverse,
        "record_count": 44,
        "source_group_count": 8,
        "substantive": 42,
        "next_chapter_navigation": 2,
    },
)
limits = [
    "The assertions concern actual family affection and conflict, but "
    "the source does not include independent observations or prediction failures.",
    "Author statement of never recalling failure is anecdotal and "
    "not a verified sample with a known denominator.",
    "The Moon/Mars/South Node family-conflict allegories are "
    "separate alternatives and not a proof of anyone's character.",
    "The same first-third house contact must preserve the "
    "square/opposition/no-aspect distinctions and contrary reception exceptions.",
    "An apparent favorable relation of native-to-sibling can "
    "coexist with disagreement among siblings themselves; "
    "these are separate dyads, not one outcome.",
    "Third-lord conjunction with Part of Fortune or its Lord "
    "and a good place of heaven is a compound historical condition.",
    "An alleged financial harm from siblings uses South Node "
    "in the third and combust second ruler together.",
    "Original sign groups Aries/Libra, Cancer/Scorpio, "
    "Leo/Aquarius are individual 17th-century stereotypes, "
    "not real-life diagnoses of relatives or neighbors.",
    "The extension to kindred and neighbors widens the set of "
    "possible post hoc matches; no prospective outcome coding exists.",
    "No exact aspect/house/Reception astronomy, calibrated threshold "
    "or human family outcome statistics are presented.",
    "Full diplomatic transcription has not been independently "
    "completed; source anchors are selective and qualified.",
    "Printed CHAP CXXI starts in PDF602 and is separate sibling "
    "number source work; do not merge it into this chapter.",
]
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05u",
        "issues": limits,
        "human_relationship_predictions_validated": 0,
        "moral_or_criminality_classifications_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B05u",
        "status": "ORIGINAL_1647_SIBLING_CONCORD_HISTORICAL_LOCALLY_ACCEPTED",
        "printed_chapter": "CXX",
        "editorial_chapter": "CXXI",
        "record_count": 44,
        "first_record": "R7209",
        "last_record": "R7252",
        "source_groups": 8,
        "substantive_historical_records": 42,
        "next_navigation": 2,
        "body_pdf_frame": 601,
        "next_heading_pdf_frame": 602,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "sibling_harmony_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B05u",
        "previous_lilly": 7208,
        "new_records": 44,
        "lilly_if_published": 7252,
        "ptolemy_retained": 1066,
        "combined_if_published": 8318,
        "substantive": 42,
        "navigation": 2,
        "source_group_count": 8,
        "next_printed_chapter": "CXXI",
        "next_pdf_page": 602,
        "rules_sha256": sha(B / "RULES.json"),
        "empirical_validations": 0,
        "human_family_relationship_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B05u original source frozen: R7209–R7252 (44 claims), human validations 0")
