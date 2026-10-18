#!/usr/bin/env python3
"""Original Lilly 1647 printed CL friend types/constancy: historic source, not person inference."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, value):
    (B / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261018.json")
assert a["batch"] == "B07e"
assert a["printed_chapter"] == "CL"
assert a["body_original_pdf_frames"] == [670, 671]
assert a["next_printed"] == "CLI"
assert a["next_heading_pdf"] == 671
assert len(a["groups"]) == 6

rules, inverse = [], []
for i, group in enumerate(a["groups"], 1):
    sid = f"B07e-S{i:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {670, 671}
    ids = []
    for claim in group["claims"]:
        no = 9863 + len(rules)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["original_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning_only"]) >= 36
        assert claim["source_only"] and not claim["real_human_friend_type_accuracy_validated"]
        assert not claim["person_morality_relationship_prediction_authorized"]
        assert not claim["runtime_promoted"]
        rules.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "source_anchor_not_diplomatic": claim["original_anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_meaning_only"],
                "qualification": claim["qualification"],
                "source_documentary_accepted": True,
                "independent_real_friend_occupation_accuracy_validated": False,
                "independent_real_friend_status_or_appearance_validated": False,
                "independent_real_friend_constancy_validated": False,
                "real_person_loyalty_or_morality_inference_authorized": False,
                "separate_relationship_synastry_rule_validated": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    inverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": (
                "source priorities / planetary friendship types"
                if i == 1
                else "Saturn and Jupiter friend categories"
                if i == 2
                else "Mars and Sun social roles"
                if i == 3
                else "Venus Mercury Moon alternatives"
                if i == 4
                else "friendship constancy from cusp and significators"
                if i == 5
                else "following CLI two-nativity boundary"
            ),
            "mapped_record_ids": ids,
        }
    )
assert len(rules) == 64
assert [x["record_number"] for x in rules] == list(range(9863, 9927))
assert [x["id"] for x in rules if x["role"] == "next_chapter_navigation"] == ["R9925", "R9926"]
assert len({x["id"] for x in rules}) == 64

pictures = {}
for frame in range(670, 674):
    file = B / "evidence" / f"pdf_1647-{frame}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    pictures[str(frame)] = {
        "file": str(file.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(file),
        "printed_folio": str(frame - 34),
        "role": "CL_friend_type_body" if frame <= 671 else "following_CLI_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07e",
        "source": (
            "William Lilly Christian Astrology 1647 original first edition Wellcome b30338724"
        ),
        "original_first_edition_source_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [670, 671],
        "following_printed_CLI_heading_pdf": 671,
        "images": pictures,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07e",
        "source_groups": inverse,
        "source_group_count": 6,
        "source_records": 64,
        "substantive": 62,
        "following_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07e",
        "issues": [
            (
                "The first-edition printed CHAP CL starts middle of original "
                "PDF670/printed636 after separately accepted unnumbered "
                "11th-house friendship introduction, and ends upper "
                "PDF671/printed637 before CHAP CLI on pairwise concord."
            ),
            (
                "CL covers the SOURCE-ASSIGNED quality/social classes "
                "of associates, as distinct from preceding friend count, "
                "actual loyalty, practical support, and later mutual "
                "relationship compatibility."
            ),
            (
                "Initial source chooses planets occupying first or eleventh "
                "if any, else the rulers of either and potentially an "
                "intercepted zodiac sign; no formal arbitration weights "
                "for multiple occupied houses or intercepts."
            ),
            (
                "Saturn Jupiter Mars Sun Venus Mercury and Moon each yield "
                "very broad lists of alternative friends' historical "
                "occupations, classes, appearances, gender and traits; "
                "these have no unique calibrated predictive probability."
            ),
            (
                "Saturn categories include poor/trade/stigmatized "
                "social occupations, Jupiter legal/clerical/noble, "
                "Mars military/surgical and physical-appearance, "
                "Sun royal/governmental, Venus art/women/gaming, "
                "Mercury scholarly/commercial, Moon matrons/"
                "diplomats/water/common people and wavering; "
                "none is evidence about actual individuals."
            ),
            (
                "Original says fixed sign at eleventh cusp signals "
                "fixed friends, movable a changeable relation and common "
                "intermediate constancy, but no time threshold, "
                "relationship length or comparator are supplied."
            ),
            (
                "Constancy may also allegedly depend on signs in which "
                "significators are placed. One final condition considers "
                "eleventh ruler not aspecting its own house OR Venus "
                "in her own house. Original conjunction/or scope "
                "is preserved without mathematical repair."
            ),
            (
                "The ensuing CHAP CLI on concord is a separate "
                "TWO-NATIVITY comparative method. Do not count "
                "either birth chart or alleged dyadic harmony "
                "from this single-person friend-type chapter."
            ),
            (
                "The source uses period class, gender and moral "
                "stereotypes, including allegations of covetousness, "
                "pride and inconstancy. No real person sex/gender, "
                "honesty, trustworthiness, profession, social "
                "status or appearance inference is authorized."
            ),
            (
                "No independent human chart, social network data, "
                "occupation labels of friends, matched demographic "
                "baseline or prospective test was used. "
                "Source statements are NOT human accuracy."
            ),
            (
                "Source method is short photo-anchored historical "
                "paraphrase, not glyph-by-glyph diplomatic "
                "transcription or full executable chart scorer."
            ),
        ],
        "friendship_quality_original_operator_complete": False,
        "real_human_friend_type_or_constancy_predictions_validated": 0,
        "real_person_trustworthiness_or_demographic_inference_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07e",
        "status": "ORIGINAL_1647_CL_QUALITY_OF_FRIENDS_HISTORIC_SOURCE_ONLY",
        "printed_chapter": "CL",
        "record_count": 64,
        "first_record": "R9863",
        "last_record": "R9926",
        "substantive": 62,
        "following_navigation": 2,
        "source_groups": 6,
        "body_original_pdf_frames": [670, 671],
        "following_printed_chapter": "CLI",
        "following_heading_pdf": 671,
        "empirical_validations": 0,
        "actual_human_friendship_quality_validated": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07e",
        "status": "ORIGINAL_PRINTED_CL_FRIEND_TYPE_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 9862,
        "new_historical_annotations": 64,
        "lilly_if_published": 9926,
        "ptolemy_retained": 1066,
        "combined_if_published": 10992,
        "substantive": 62,
        "navigation": 2,
        "source_groups": 6,
        "numbered_chapters_added": 1,
        "next_printed_chapter": "CLI",
        "next_original_pdf": 671,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "real_friend_character_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B07e printed CL source: 64 historic records R9863–R9926, next CLI.")
