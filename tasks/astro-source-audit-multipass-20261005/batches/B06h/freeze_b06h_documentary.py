#!/usr/bin/env python3
"""Lilly original unnumbered seventh-house marriage study: history, not prediction."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def load(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, payload):
    (B / name).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


author = load("SOURCE_FIRST_AUTHORING_20261017.json")
assert author["batch"] == "B06h"
assert author["section"] == "UNNUMBERED_SEVENTH_HOUSE_MARRIAGE"
assert author["body_original_pdf_frames"] == [621, 622, 623]
assert author["following_printed_chapter"] == "CXXXI"
assert len(author["source_groups"]) == 8

rows, reverse = [], []
for group_number, group in enumerate(author["source_groups"], 1):
    sid = f"B06h-S{group_number:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {621, 622, 623}
    refs = []
    for claim in group["clauses"]:
        no = 7878 + len(rows)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["anchor_not_diplomatic"]) >= 8
        assert len(claim["historical_meaning_only"]) >= 43
        assert not claim["independent_marriage_outcome_validated"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": no,
                "batch": "B06h",
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "original_anchor_not_diplomatic": claim["anchor_not_diplomatic"],
                "historical_only_meaning": claim["historical_meaning_only"],
                "source_qualification": claim["qualification"],
                "historical_documentary_accepted": True,
                "independent_human_marriage_outcome_validated": False,
                "real_partner_character_or_sexual_behavior_validated": False,
                "person_level_moral_or_intimate_claim_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        refs.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["source_group"],
            "mapped_record_ids": refs,
        }
    )
assert len(rows) == 66
assert [x["record_number"] for x in rows] == list(range(7878, 7944))
assert [x["id"] for x in rows if x["role"] == "next_chapter_navigation"] == ["R7942", "R7943"]
assert len({x["id"] for x in rows}) == len(rows)

images = {}
for n in [621, 622, 623, 624, 625]:
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(p),
        "printed_folio": str(n - 34),
        "source_role": (
            "original_unnumbered_marriage_intro"
            if n <= 623
            else "following_numbered_chapter_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06h",
        "source": (
            "William Lilly Christian Astrology original 1647 first edition Wellcome b30338724"
        ),
        "volume_sha256": "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        "body_pdf_frames": [621, 622, 623],
        "following_printed_CXXXI_heading_frame": 623,
        "seventh_house_intro_is_unnumbered": True,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06h",
        "source_groups": reverse,
        "source_group_count": 8,
        "record_count": 66,
        "substantive": 64,
        "next_numbered_chapter_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06h",
        "issues": [
            (
                "All original 1647 claims of marriage, aversion to marriage, "
                "sexual desire, chastity or lust are historical stereotypes, not "
                "scientifically verified psychological or individual relationship "
                "facts."
            ),
            (
                "This unnumbered section on whether a man marries is different "
                "from printed CXXXI, which predicts the ease or difficulty of "
                "obtaining a wife. Do not conflate or merge outcomes."
            ),
            (
                "Venus and Moon are cited as source indicia of a man's marriage; "
                "this is a sex-coded seventeenth-century construction, not "
                "sex-neutral or generalizable physiology."
            ),
            (
                "Barren Virgo, Gemini and Leo and fertile signs are historical "
                "astrological classes, not actual human infertility or sexual "
                "function evidence."
            ),
            (
                "The author calls houses 6, 9, 12 cadent and also includes eighth "
                "expressly although it is not cadent, due to his claimed "
                "malignancy."
            ),
            (
                "A majority of corroborating marriage significators is required "
                "by several negative rules; the source provides no calibrated "
                "weight, threshold or prioritization when conditions conflict."
            ),
            (
                "Saturn must be very strong in the negative scenario: Lilly "
                "expressly says that if Venus and Moon outrank it in strength, "
                "the preceding no-marriage conclusion does not hold."
            ),
            (
                "The author asserts a Moon/Saturn square or opposition without "
                "many other supporting testimonies is insufficient to infer "
                "singleness, even when Venus is in a barren sign. This explicit "
                "negative exception is preserved."
            ),
            (
                "Original source rules conflate objective marriage history with "
                "private desire/aversion, and with reported sexual potency. They "
                "are separate outcomes requiring independent definitions and "
                "evidence."
            ),
            (
                "Claims about concubines, chastity, monkhood and sexual "
                "immorality are period moral judgments, not evidence of private "
                "conduct by identifiable people."
            ),
            (
                "Some original early modern sign symbols, angularity and "
                "reception relationships need specialist checking before "
                "executable numerical rule coding."
            ),
            (
                "The alleged Moon combust, Saturn sign and Venus/Saturn "
                "configurations overlap with numerous exceptions; no historical "
                "denominator, negative cases or prospective test."
            ),
            (
                "The seventh-house positive source includes a source assertion of "
                "sexual ability, an intimate private property never established "
                "from astrology."
            ),
            (
                "No birth-time verified cohort, actual marriage registries, "
                "single-life histories, sex/gender comparison panels, self-report "
                "outcomes or blind-decoy model comparison has been evaluated."
            ),
            (
                "The original first-edition body finishes at top PDF623 before "
                "numbered CHAP CXXXI; it is a substantive unnumbered "
                "seventh-house source and must NOT increment printed numbered "
                "chapter coverage."
            ),
            (
                "This packet is source-anchored selective paraphrase, not a full "
                "diplomatic original glyph-by-glyph transcription or "
                "demonstration of astrological performance."
            ),
        ],
        "independently_validated_real_marriage_predictions": 0,
        "sex_life_character_or_partner_claim_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06h",
        "status": "ORIGINAL_1647_UNNUMBERED_SEVENTH_HOUSE_MARRIAGE_HISTORICAL_ONLY",
        "section": "UNNUMBERED_SEVENTH_HOUSE_MARRIAGE",
        "record_count": 66,
        "first_record": "R7878",
        "last_record": "R7943",
        "source_groups": 8,
        "substantive_historical_clauses": 64,
        "next_chapter_navigation": 2,
        "original_body_pdf_frames": [621, 622, 623],
        "next_printed_heading_pdf_frame": 623,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "independent_human_marriage_predictions": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06h",
        "status": "FIRST_EDITION_ORIGINAL_SEVENTH_HOUSE_DOCUMENTARY_LOCALLY_FROZEN",
        "previous_lilly": 7877,
        "new_historical_records": 66,
        "lilly_if_published": 7943,
        "ptolemy_retained": 1066,
        "combined_if_published": 9009,
        "substantive": 64,
        "navigation": 2,
        "source_groups": 8,
        "new_numbered_chapters": 0,
        "next_printed_chapter": "CXXXI",
        "next_original_pdf_frame": 623,
        "rules_sha256": sha(B / "RULES.json"),
        "source_authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "real_world_marriage_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06h unnumbered seventh-house marriage: 66 source notes R7878–R7943")
