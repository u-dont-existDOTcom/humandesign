#!/usr/bin/env python3
"""Freeze Lilly original unnumbered eleventh-house friendship source, never person labels."""

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
guard = read("FRIENDSHIP_HISTORICAL_TARGET_GUARD_V1.json")
assert a["batch"] == "B07d"
assert a["printed_chapter"] is None
assert a["section"] == "UNNUMBERED_ELEVENTH_HOUSE_FRIENDS"
assert a["body_original_pdf_frames"] == [668, 669, 670]
assert a["following_printed"] == "CL"
assert a["following_printed_heading_frame"] == 670
assert len(a["groups"]) == 7
assert len(guard["target_variables"]) == 8
assert guard["no_human_predictions_validated"] == 0
assert guard["no_runtime_model_promotions"]

records, mapdata = [], []
for n, group in enumerate(a["groups"], 1):
    sid = f"B07d-S{n:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {668, 669, 670}
    group_ids = []
    for claim in group["claims"]:
        number = 9778 + len(records)
        rid = f"R{number}"
        assert claim["id"] == rid
        assert len(claim["source_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning_only"]) >= 41
        assert claim["source_only"]
        assert not claim["real_human_friendship_accuracy_validated"]
        assert not claim["person_moral_character_inference_authorized"]
        assert not claim["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": number,
                "batch": "B07d",
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "original_anchor_not_diplomatic": claim["source_anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_meaning_only"],
                "qualification": claim["qualification"],
                "source_documentary_accepted": True,
                "independent_real_friendship_count_validated": False,
                "independent_real_relationship_reliability_validated": False,
                "independent_real_support_or_social_influence_validated": False,
                "independent_actual_enemy_count_validated": False,
                "no_real_person_morality_or_faith_label_authorized": True,
                "actual_source_planet_glyphs_and_calculations_verified": False,
                "runtime_model_promoted": False,
            }
        )
        group_ids.append(rid)
    mapdata.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": group_ids,
        }
    )
assert len(records) == 85
assert [x["record_number"] for x in records] == list(range(9778, 9863))
assert [x["id"] for x in records if x["role"] == "next_numbered_navigation"] == ["R9861", "R9862"]
assert len({x["id"] for x in records}) == 85

photos = {}
for n in range(668, 673):
    file = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    photos[str(n)] = {
        "file": str(file.relative_to(B)),
        "sha256": sha(file),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "source_role": (
            "unnumbered_eleventh_house_friends_intro"
            if n <= 670
            else "following_numbered_CL_CLI_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07d",
        "original_source": (
            "William Lilly Christian Astrology 1647 original first edition Wellcome b30338724"
        ),
        "first_edition_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "unnumbered": True,
        "body_original_pdf_frames": [668, 669, 670],
        "next_printed_CL_heading_frame": 670,
        "images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07d",
        "source_groups": mapdata,
        "source_group_count": 7,
        "record_count": 85,
        "substantive": 83,
        "following_numbered_navigation": 2,
        "future_human_target_guard": "FRIENDSHIP_HISTORICAL_TARGET_GUARD_V1.json",
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07d",
        "issues": [
            (
                "The source is UNNUMBERED and starts after printed "
                "CXLIX in PDF668; internal Speciall Rules concerning "
                "Friends continue through TOP PDF670 before separate "
                "printed CHAP CL Quality of Friends on same PDF670. "
                "Do not increment numbered chapter count."
            ),
            (
                "The author explicitly selects eleventh occupants/"
                "aspects first, first-house planets second, and "
                "eleventh ruler/aspects last. Multiple witnesses "
                "and empty-house fallbacks cannot be flattened "
                "into a single equal-weight vote."
            ),
            (
                "Jupiter/Venus strong can allegedly yield a high "
                "number of good/helpful friends and sincere "
                "affection, while weak benefics allow moderate "
                "friendship, low expected aid, or mixed sincerity."
            ),
            (
                "Saturn/Mars even well dignified allegedly "
                "yield MANY friends who are insincere; "
                "WEAK malefics instead signal FEW and "
                "unfaithful friends. Number, relationship "
                "quality and support are separate outcomes."
            ),
            (
                "Original text lists North/South lunar-node signs "
                "and categorizes Sun/Moon/Mercury as intermediate; "
                "one source glyph near neutral planet list "
                "is not independently identified. "
                "Do not invent node or planet operators."
            ),
            (
                "Several strongest supposedly good friends may "
                "be determined from the strongest planet "
                "in first/eleventh if mixed, a subjective "
                "post-hoc choice without formal tie rules."
            ),
            (
                "The astrologer offers a personal anecdote "
                "about peregrine infortunes in movable or "
                "common sign predicting adulterate friends, "
                "without actual source case/denominator."
            ),
            (
                "The Speciall Rules include six benefic "
                "source houses for FRIEND counts, "
                "malefics in twelfth or angles for ENEMY "
                "counts, Cancer rising friendship difficulty, "
                "Moon Aquarius/Pisces lack of royal favor, "
                "and 11th/1st or 10th/1st lord separation."
            ),
            (
                "Astrological signs said to mark powerful "
                "friends, gender-associated friends, "
                "and perceived friendship faithfulness "
                "are period stereotypes, not actual "
                "personal trustworthiness or moral traits."
            ),
            (
                "The original deliberately distinguishes "
                "Moon at eleventh making a person KNOWN "
                "to many while yielding FEW true friends, "
                "so general sociability cannot rescue "
                "a prediction of real close friendship."
            ),
            (
                "No independent human natal source, actual "
                "friend counts, time series, ground-truth "
                "reliability/loyalty measures, objectively "
                "rated friend help, enemies or class-matched "
                "null models are supplied."
            ),
            (
                "The following separate printed CL begins "
                "after divider PDF670; its list of friends "
                "according to Saturn/Jupiter/Mars/Sun/Venus/"
                "Mercury/Moon and sign constancy must NOT "
                "be admitted into this unnumbered section."
            ),
            (
                "Source is short original historical "
                "anchors with photographs and parity, "
                "not complete diplomatic transcription "
                "or a genuine interpersonal forecast."
            ),
        ],
        "all_original_lunar_node_glyphs_verified": False,
        "friendship_count_and_quality_scoring_engine": False,
        "real_human_friendship_prediction_accuracy_validated": 0,
        "actual_person_trustworthiness_and_moral_classification_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07d",
        "status": "ORIGINAL_1647_UNNUMBERED_ELEVENTH_HOUSE_FRIENDSHIP_HISTORY_ONLY",
        "section": "UNNUMBERED_ELEVENTH_HOUSE_FRIENDS",
        "original_printed_chapter_number": None,
        "record_count": 85,
        "first_record": "R9778",
        "last_record": "R9862",
        "substantive": 83,
        "following_numbered_navigation": 2,
        "source_groups": 7,
        "body_original_pdf_frames": [668, 669, 670],
        "following_printed": "CL",
        "following_heading_frame": 670,
        "empirical_validations": 0,
        "human_friendship_accuracy_validated": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07d",
        "status": "ORIGINAL_UNNUMBERED_ELEVENTH_HOUSE_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 9777,
        "new_historical_annotations": 85,
        "lilly_if_published": 9862,
        "ptolemy_retained": 1066,
        "combined_if_published": 10928,
        "substantive": 83,
        "navigation": 2,
        "source_groups": 7,
        "numbered_chapters_added": 0,
        "next_printed_chapter": "CL",
        "next_original_pdf": 670,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "friendship_guard_sha256": sha(B / "FRIENDSHIP_HISTORICAL_TARGET_GUARD_V1.json"),
        "empirical_validations": 0,
        "human_friendship_accuracy_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B07d UNNUMBERED friends: 85 original historical notes R9778–R9862.")
