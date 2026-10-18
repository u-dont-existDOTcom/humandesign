#!/usr/bin/env python3
"""Freeze Lilly original unnumbered tenth-house honor source, historical only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, obj):
    (B / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261018.json")
assert a["batch"] == "B06x"
assert a["section"] == "UNNUMBERED_TENTH_HOUSE_HONOURS_DIGNITIES"
assert a["printed_chapter"] is None
assert a["body_pdf_frames"] == [649]
assert a["following_printed"] == "CXLIIII"
assert a["following_heading_pdf"] == 649
assert len(a["source_groups"]) == 3

rows, mapped = [], []
for number, g in enumerate(a["source_groups"], 1):
    sid = f"B06x-S{number:03d}"
    assert g["source_span"] == sid
    assert g["original_pdf_frames"] == [649]
    ids = []
    for c in g["claims"]:
        rid = f"R{9106 + len(rows)}"
        assert c["id"] == rid
        assert len(c["source_anchor_not_diplomatic"]) >= 5
        assert len(c["historical_source_meaning_only"]) >= 40
        assert not c["real_human_status_prediction_validated"]
        assert not c["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": 9106 + len(rows),
                "source_span": sid,
                "original_pdf_frames": [649],
                "role": c["role"],
                "source_anchor_not_diplomatic": c["source_anchor_not_diplomatic"],
                "historical_meaning_only": c["historical_source_meaning_only"],
                "qualification": c["qualification"],
                "source_documentary_accepted": True,
                "real_human_honour_status_accuracy_validated": False,
                "real_career_rank_or_esteem_accuracy_validated": False,
                "regal_star_natal_conjunction_calculated": False,
                "real_person_professional_advice_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    mapped.append(
        {
            "source_span": sid,
            "original_pdf_frames": [649],
            "source_group": g["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rows) == 19
assert [x["record_number"] for x in rows] == list(range(9106, 9125))
assert [x["id"] for x in rows if x["role"] == "next_numbered_navigation"] == ["R9123", "R9124"]

photos = {}
for n in (649, 650, 651):
    file = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    photos[str(n)] = {
        "file": str(file.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(file),
        "printed_folio": str(n - 34),
        "role": "unnumbered_tenth_intro" if n == 649 else "following_numbered_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06x",
        "source": (
            "William Lilly Christian Astrology original first edition 1647 Wellcome b30338724"
        ),
        "original_pdf_sha256": ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"),
        "unnumbered": True,
        "body_original_pdf_frames": [649],
        "following_printed_CXLIIII_heading_pdf": 649,
        "images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06x",
        "source_groups": mapped,
        "source_group_count": 3,
        "source_annotations": 19,
        "substantive": 17,
        "next_numbered_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06x",
        "issues": [
            (
                "This is a substantive UNNUMBERED tenth-house introduction and "
                "must not increment the numbered chapter count."
            ),
            (
                "Original printed CXLIIII on dignity/advancement starts LATER on "
                "the SAME original PDF649 and is not part of these 17 substantive "
                "annotations."
            ),
            (
                "Lilly gives an ordered priority of four classes of witnesses, "
                "with luminaries and the Sun primary, the midheaven ruler next, "
                "planets in midheaven third, and bright regal fixed stars fourth."
            ),
            (
                "The aspecting planets require the mediety of their orbs; without "
                "precise original orb tables and chart geometry this is not a "
                "runnable prediction."
            ),
            (
                "Regal fixed stars require first or second magnitude and position "
                "near tenth or first cusp; the first-edition source here supplies "
                "no numerical allowable cusp distance or complete star list."
            ),
            (
                "Honours, preferment, dignity and estimation are separately named "
                "source social outcomes without objective benchmarks or a "
                "probabilistic endpoint."
            ),
            (
                "The following numbered source includes class-relative caveats, "
                "which must not be silently treated as proven here until its "
                "original passages are separately admitted."
            ),
            (
                "No verified human profession, status, promotion, lifetime rank, "
                "reputation, socioeconomics or external judge supplied an "
                "independent blind test."
            ),
            (
                "The sources are short anchored historical paraphrases, not a "
                "complete original-page diplomatic edition."
            ),
        ],
        "original_fixed_star_orb_table_complete": False,
        "human_honour_or_status_predictions_validated": 0,
        "real_person_professional_rank_inference_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06x",
        "status": "ORIGINAL_UNNUMBERED_TENTH_HOUSE_SOURCE_ONLY",
        "section": "UNNUMBERED_TENTH_HOUSE_HONOURS_DIGNITIES",
        "record_count": 19,
        "first_record": "R9106",
        "last_record": "R9124",
        "substantive": 17,
        "following_numbered_navigation": 2,
        "source_groups": 3,
        "body_original_pdf_frames": [649],
        "following_printed_chapter": "CXLIIII",
        "following_heading_pdf": 649,
        "original_printed_chapter_number": None,
        "empirical_validations": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06x",
        "status": "ORIGINAL_UNNUMBERED_TENTH_HOUSE_LOCALLY_FROZEN",
        "prior_lilly": 9105,
        "new_historical_annotations": 19,
        "lilly_if_published": 9124,
        "ptolemy_retained": 1066,
        "combined_if_published": 10190,
        "substantive": 17,
        "navigation": 2,
        "source_groups": 3,
        "numbered_chapters_added": 0,
        "next_source": "CXLIIII",
        "next_original_pdf": 649,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "human_status_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Unnumbered original tenth-house: 19 source records R9106–R9124")
