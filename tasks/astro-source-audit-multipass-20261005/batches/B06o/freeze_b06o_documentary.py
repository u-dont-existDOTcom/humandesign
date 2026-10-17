#!/usr/bin/env python3
"""Lilly 1647 printed CXXXVII on women's marriage, historical source only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def write(name, item):
    (B / name).write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261017.json")
assert a["batch"] == "B06o"
assert a["printed_chapter"] == "CXXXVII"
assert a["body_original_pdf_frames"] == [634, 635, 636]
assert a["following_section"] == "UNNUMBERED_FIFTH_HOUSE_CHILDREN"
assert a["following_section_pdf_frame"] == 636
assert a["following_next_printed_chapter"] == "CXXXVIII"
assert a["following_next_printed_frame"] == 638
assert len(a["groups"]) == 7

rows, reverses = [], []
for section_no, g in enumerate(a["groups"], 1):
    sid = f"B06o-S{section_no:03d}"
    assert g["source_span"] == sid
    assert set(g["original_pdf_frames"]) <= {634, 635, 636}
    refs = []
    for c in g["clauses"]:
        number = 8398 + len(rows)
        rid = f"R{number}"
        assert c["id"] == rid
        assert len(c["original_anchor_not_diplomatic"]) >= 5
        assert len(c["historical_only_meaning"]) >= 40
        assert c["source_only"]
        assert not c["actual_human_marriage_outcome_validated"]
        assert not c["person_level_partner_morality_or_sexual_claim_authorized"]
        assert not c["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": number,
                "source_span": sid,
                "original_pdf_frames": g["original_pdf_frames"],
                "role": c["role"],
                "original_anchor_not_diplomatic": c["original_anchor_not_diplomatic"],
                "historical_source_meaning_only": c["historical_only_meaning"],
                "source_qualification": c["qualification"],
                "documentary_source_accepted": True,
                "independent_legal_marriage_occurrence_validated": False,
                "independent_marriage_ages_or_number_validated": False,
                "independent_husband_origin_wealth_traits_validated": False,
                "independent_marital_concord_validated": False,
                "real_partner_identity_gender_sexual_conduct_claim_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        refs.append(rid)
    reverses.append(
        {
            "source_span": sid,
            "original_pdf_frames": g["original_pdf_frames"],
            "source_group": g["topic"],
            "mapped_record_ids": refs,
        }
    )
assert len(rows) == 99
assert [x["record_number"] for x in rows] == list(range(8398, 8497))
assert [x["id"] for x in rows if x["role"] == "next_section_navigation"] == ["R8495", "R8496"]
assert len({x["id"] for x in rows}) == 99

images = {}
for p in range(634, 639):
    path = B / "evidence" / f"pdf_1647-{p}.jpg"
    raw = path.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(p)] = {
        "file": str(path.relative_to(B)),
        "sha256": sha(path),
        "bytes": len(raw),
        "printed_folio": str(p - 34),
        "role": (
            "womens_marriage_body" if p <= 636 else "unnumbered_fifth_house_following_context"
        ),
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06o",
        "source": (
            "William Lilly Christian Astrology original 1647 first edition Wellcome b30338724"
        ),
        "original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": [634, 635, 636],
        "following_unnumbered_fifth_house_start_frame": 636,
        "following_printed_CXXXVIII_heading_frame": 638,
        "images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06o",
        "source_groups": reverses,
        "source_group_count": 7,
        "historical_records": 99,
        "substantive": 97,
        "following_unnumbered_navigation": 2,
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06o",
        "issues": [
            (
                "The chapter explicitly applies historical sex-coded Sun/Mars "
                "primary indicators for women and transfers most but not all "
                "male marriage rules from Venus/Moon, with contextual exceptions."
            ),
            (
                "The source subsequently uses Sun AND Moon in masculine-sign "
                "claims and Venus in seventh / Venus common-sign claims; "
                "do NOT systematically substitute Mars for all Venus lines."
            ),
            (
                "Historical words Virago, refractory wife, venereal preference "
                "are stigmatizing period judgments, not a real person's "
                "gender identity, sexuality, psychology or partnership."
            ),
            (
                "Signs of being fruitful/barren, house fortune/misfortune "
                "and aspect quality are ambiguous qualitative conditions "
                "with no frozen numerical weight or prospective denominator."
            ),
            (
                "Actual marriage occurrence, desire to marry, ease obtaining "
                "marriage, age at marriage, husband's age, spouse count, "
                "birthplace, appearance, wealth and concord are "
                "different outcomes that must not be pooled to rescue misses."
            ),
            (
                "The oriental-Sun timing rule permits either early marriage "
                "with any-age husband or mature-age marriage with young "
                "husband, a broad alternative that lacks a year cutoff."
            ),
            (
                "Midheaven or Sun directions for specific marriage "
                "calendar timing require a missing arc-to-years astronomical "
                "algorithm, exact historical primary directions, and rules "
                "for multiple competing triggers."
            ),
            (
                "A single-form zodiac Sun OR one matutine-planet aspect "
                "and multiple-form OR many matutine aspects are alternative "
                "wife-number/husband-number assertions, not measured counts."
            ),
            (
                "Different sign and planet-count methods for two/many "
                "husbands overlap and conflict; neither a unique "
                "ranking nor prospective failure policy is supplied."
            ),
            (
                "Moon-like counting method now uses Sun corporal same-sign "
                "company, partile/platick contacts, and failing that "
                "Sun applying to dignity-holder planets rather than reverse."
            ),
            (
                "One spouse-origin symbol in the third could be Part of "
                "Fortune; original glyph is not firmly validated and "
                "must not become an executable geographic predictor."
            ),
            (
                "Husband appearance/conditions, planet-defined character "
                "and social rank are author stereotypes without "
                "documented identities or independent measurements."
            ),
            (
                "For husband's wealth Lilly expressly rejects his "
                "earlier authors' rules in favor of eighth house and its "
                "ruler and occupants; alleged observer confidence "
                "is not independent replication."
            ),
            (
                "Strong eighth and absence of malefic aspects and ruler "
                "domicile/angular are different wealth qualifiers, "
                "with no money amounts or benchmark comparison."
            ),
            (
                "Mutual reception, sextile/trine and benefic aspects "
                "are proposed as marital concord alternatives, and "
                "negative sixth/eighth/twelfth house positions are "
                "not relationship safety or actual partner conflict evidence."
            ),
            (
                "Substantive unnumbered fifth-house/children section "
                "begins after a double divider PDF636 while next numbered "
                "CHAP CXXXVIII does not begin until PDF638. "
                "Do not incorrectly increment numbered chapter twice."
            ),
            (
                "The source provides no human cohort, chart parity, "
                "blind scoring, birth-time source quality, or "
                "calibrated probability of any spouse event."
            ),
            (
                "The packet is an anchored historical paraphrase with "
                "original photographs, NOT a full diplomatic "
                "line-by-line seventeenth-century transcription."
            ),
        ],
        "original_source_glyphs_fully_resolved": False,
        "sex_gender_partner_morality_predictions_authorized": False,
        "independently_validated_human_marriage_outcomes": 0,
        "runtime_promotions": 0,
    },
)
write(
    "RULES.json",
    {
        "batch": "B06o",
        "status": "ORIGINAL_1647_WOMENS_MARRIAGE_HISTORICAL_ONLY",
        "printed_chapter": "CXXXVII",
        "editorial_chapter": "CXXXVIII",
        "record_count": 99,
        "first_record": "R8398",
        "last_record": "R8496",
        "substantive": 97,
        "following_unnumbered_navigation": 2,
        "source_groups": 7,
        "body_original_frames": [634, 635, 636],
        "next_unnumbered_fifth_house_frame": 636,
        "next_numbered_chapter_heading_frame": 638,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "real_human_marital_prediction_validations": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
write(
    "ACCEPTANCE.json",
    {
        "batch": "B06o",
        "status": "ORIGINAL_1647_WOMENS_MARRIAGE_LOCALLY_FROZEN",
        "prior_lilly": 8397,
        "new_historical_annotations": 99,
        "lilly_if_published": 8496,
        "ptolemy_retained": 1066,
        "combined_if_published": 9562,
        "substantive": 97,
        "navigation": 2,
        "source_groups": 7,
        "new_numbered_chapters": 1,
        "next_source_section": "UNNUMBERED_FIFTH_HOUSE_CHILDREN",
        "next_source_pdf": 636,
        "next_printed": "CXXXVIII",
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "human_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original 1647 printed CXXXVII women's marriage R8398–R8496: 99 source notes")
