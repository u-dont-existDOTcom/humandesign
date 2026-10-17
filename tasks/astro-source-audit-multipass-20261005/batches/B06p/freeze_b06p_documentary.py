#!/usr/bin/env python3
"""Original Lilly unnumbered fifth-house children: historic source only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, payload):
    (B / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261017.json")
assert a["batch"] == "B06p"
assert a["section"] == "UNNUMBERED_FIFTH_HOUSE_CHILDREN"
assert a["printed_chapter"] is None
assert a["body_original_pdf_frames"] == [636, 637, 638]
assert a["following_numbered_printed_chapter"] == "CXXXVIII"
assert a["following_heading_frame"] == 638
assert len(a["groups"]) == 8

rows, reverse = [], []
for n, group in enumerate(a["groups"], 1):
    sid = f"B06p-S{n:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {636, 637, 638}
    refs = []
    for claim in group["clauses"]:
        no = 8497 + len(rows)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["anchor_not_diplomatic"]) >= 5
        assert len(claim["meaning_historical_only"]) >= 40
        assert not claim["independent_reproductive_or_child_mortality_validated"]
        assert not claim["clinical_or_child_moral_prediction_authorized"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": no,
                "batch": "B06p",
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "source_anchor_not_diplomatic": claim["anchor_not_diplomatic"],
                "meaning_historical_only": claim["meaning_historical_only"],
                "source_qualification": claim["qualification"],
                "documentary_source_accepted": True,
                "independent_human_fertility_accuracy_validated": False,
                "independent_human_child_count_validated": False,
                "independent_real_child_health_or_death_validated": False,
                "human_parent_child_morality_claim_authorized": False,
                "person_level_medical_fertility_advice_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        refs.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "passage_group": group["topic"],
            "mapped_record_ids": refs,
        }
    )
assert len(rows) == 106
assert [r["record_number"] for r in rows] == list(range(8497, 8603))
assert [r["id"] for r in rows if r["role"] == "next_chapter_navigation"] == ["R8601", "R8602"]
assert len({r["id"] for r in rows}) == 106

photos = {}
for n in [636, 637, 638, 639]:
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    photos[str(n)] = {
        "path": str(p.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(p),
        "printed_folio": str(n - 34),
        "original_role": (
            "unnumbered_children_intro" if n <= 638 else "following_numbered_children_count_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06p",
        "source": ("William Lilly Christian Astrology 1647 first edition Wellcome b30338724"),
        "original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [636, 637, 638],
        "following_printed_CXXXVIII_heading_frame": 638,
        "unnumbered": True,
        "images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06p",
        "source_groups": reverse,
        "source_groups_count": 8,
        "source_records": 106,
        "substantive_historical": 104,
        "following_numbered_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06p",
        "issues": [
            (
                "Original fifth-house/children introduction is substantive "
                "but UNNUMBERED; do not increment the printed chapter "
                "counter. Subsequent printed CXXXVIII count starts "
                "late original PDF638."
            ),
            (
                "All original source claims about pregnancy, infertility, "
                "abortion, miscarriage, child birth, child health "
                "and child death are unsupported historical hypotheses "
                "and must not inform care or prognosis."
            ),
            (
                "Fifth house is expressly prioritized over contrary "
                "eleventh testimony in both favorable and adverse cases. "
                "Do not interpret eleventh as equivalent source weight."
            ),
            (
                "When fifth and eleventh are empty, author falls back "
                "to Lord fifth, and when several sources disagree "
                "he urges a nonnumeric majority of testimonies."
            ),
            (
                "Jupiter Venus Moon and North Node are source fruitful "
                "labels, Saturn Mars Sun and South Node barren; these "
                "are NOT scientific reproductive indicators."
            ),
            (
                "Mercury is explicitly neutral/convertible depending "
                "on aspects, conjunction, essential dignity and "
                "oriental/occidental status, preventing a simple "
                "Mercury=fertility or Mercury=infertility rule."
            ),
            (
                "Planet strength and sign fruitfulness interact, "
                "and mixed fertile/barren arrangements are said "
                "to be mediocrity or require other testimonies, "
                "not unqualified positive or negative outcomes."
            ),
            (
                "The original printed fifth-lord negative passage "
                "can mean no children, few children and possibly "
                "uncertain survival; syntactic wording about living "
                "children is ambiguous and not repaired."
            ),
            (
                "Planetary and zodiac glyphs and mutual terms "
                "on original PDF638 are not fully transcribed, "
                "and cannot enter executable reproductive rules."
            ),
            (
                "Original source attributes multiple further aphorisms "
                "to Alubater, Schoner and Origanus page 640; "
                "original author-to-author collation not done."
            ),
            (
                "Period statements about children's temperament "
                "or welfare are not evidence of a real child's "
                "personality, disability or health."
            ),
            (
                "Several high-stakes branches switch freely from "
                "few children to no children, infertility, "
                "infant death, or even death of the native; "
                "outcomes are scientifically noninterchangeable."
            ),
            (
                "Lilly's personally observed Jupiter retrograde "
                "in fifth but no children is a single retrospective "
                "anecdote, not replicated prospective evidence."
            ),
            (
                "No verified birth certificates, repeated parent/child "
                "records, obstetric data, denominators, controls "
                "or blinded predictions were used in this lane."
            ),
            (
                "Even if original planet placements are eventually "
                "computed, actuarial/clinical fertility and death "
                "probabilities cannot be inferred without "
                "independent validated data and appropriate safeguards."
            ),
            (
                "The packet is selective original-source anchoring "
                "and qualified paraphrase rather than original "
                "diplomatic glyph-by-glyph printed edition."
            ),
        ],
        "original_glyphs_fully_resolved": False,
        "original_named_author_attributions_verified": False,
        "independent_human_reproductive_predictions_validated": 0,
        "medical_or_child_death_predictions_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06p",
        "status": "ORIGINAL_1647_UNNUMBERED_FIFTH_HOUSE_HISTORICAL_ONLY",
        "section": "UNNUMBERED_FIFTH_HOUSE_CHILDREN",
        "record_count": 106,
        "first_record": "R8497",
        "last_record": "R8602",
        "substantive": 104,
        "following_navigation": 2,
        "source_groups": 8,
        "body_original_pdf_frames": [636, 637, 638],
        "next_printed_chapter": "CXXXVIII",
        "next_numbered_heading_pdf": 638,
        "first_ed_printed_chapter_number": None,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "real_human_fertility_or_child_outcomes_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06p",
        "status": "ORIGINAL_1647_CHILDREN_INTRO_HISTORICAL_LOCAL_FREEZE",
        "prior_lilly": 8496,
        "new_historical_annotations": 106,
        "lilly_if_published": 8602,
        "ptolemy_retained": 1066,
        "combined_if_published": 9668,
        "substantive": 104,
        "navigation": 2,
        "source_groups": 8,
        "new_numbered_chapters": 0,
        "next_printed_chapter": "CXXXVIII",
        "next_source_pdf": 638,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "human_fertility_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original Lilly unnumbered fifth house children: 106 historic R8497–R8602")
