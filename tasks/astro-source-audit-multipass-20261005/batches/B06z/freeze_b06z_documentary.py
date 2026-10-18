#!/usr/bin/env python3
"""Freeze original printed CXLVI on causes of preferment, no human prediction."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, item):
    (B / name).write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261018.json")
assert a["batch"] == "B06z"
assert a["printed_chapter"] == "CXLVI"
assert a["body_pdf_frames"] == [655, 656]
assert a["next_printed"] == "CXLVII"
assert a["following_original_pdf_frame"] == 656
assert a["previous_printed_CXLV_missing_unchanged"]
assert len(a["groups"]) == 4

rules, mapping = [], []
for n, group in enumerate(a["groups"], 1):
    sid = f"B06z-S{n:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {655, 656}
    record_ids = []
    for x in group["claims"]:
        number = 9313 + len(rules)
        rid = f"R{number}"
        assert x["id"] == rid
        assert len(x["original_anchor_not_diplomatic"]) >= 5
        assert len(x["historical_source_meaning_only"]) >= 42
        assert x["source_only"] and not x["independent_real_status_cause_validated"]
        assert not x["runtime_promoted"]
        rules.append(
            {
                "id": rid,
                "record_number": number,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": x["role"],
                "original_anchor_not_diplomatic": x["original_anchor_not_diplomatic"],
                "historical_source_meaning_only": x["historical_source_meaning_only"],
                "qualification": x["qualification"],
                "documentary_source_accepted": True,
                "independent_human_profession_or_promotion_cause_validated": False,
                "independent_human_property_or_military_advancement_validated": False,
                "independent_human_wit_morality_or_industry_validated": False,
                "real_person_employment_or_social_class_inference_authorized": False,
                "source_causal_attribution_experimentally_verified": False,
                "runtime_model_promoted": False,
            }
        )
        record_ids.append(rid)
    mapping.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": record_ids,
        }
    )
assert len(rules) == 55
assert [x["record_number"] for x in rules] == list(range(9313, 9368))
assert [x["id"] for x in rules if x["role"] == "next_chapter_navigation"] == ["R9366", "R9367"]
assert len({x["id"] for x in rules}) == 55

images = {}
for frame in [655, 656, 657, 658]:
    file = B / "evidence" / f"pdf_1647-{frame}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(frame)] = {
        "file": str(file.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(file),
        "printed_folio": str(frame - 34),
        "source_role": (
            "CXLVI_original_body" if frame <= 656 else "following_CXLVII_and_CXLVIII_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06z",
        "original_source": (
            "William Lilly Christian Astrology 1647 original first edition Wellcome b30338724"
        ),
        "original_source_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": [655, 656],
        "following_printed_CXLVII_heading_pdf": 656,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06z",
        "source_groups": mapping,
        "source_group_count": 4,
        "record_count": 55,
        "substantive": 53,
        "following_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06z",
        "issues": [
            (
                "Source CXLVI addresses the alleged kind and causal source of "
                "status, NOT whether a person actually obtains rank; distinguish "
                "from preceding CXLIIII."
            ),
            (
                "The original printed CXLV numbering omission before CXLVI remains; "
                "no invented CXLV unit was added."
            ),
            (
                "An eligible primary planet must partile-aspect one of the "
                "luminaries, giving precedence to the most essentially dignified "
                "light; original orb and arbitration algorithms are not supplied "
                "here."
            ),
            (
                "The author gives numerous alternative alleged motives and people "
                "for each planet, not a deterministic occupational result."
            ),
            (
                "Saturn is not always a bad outcome: when strong and aspecting the "
                "light, it allegedly signifies inheritance, possessions, favor or "
                "help from elders."
            ),
            (
                "Jupiter/Venus's supposed honesty, gravity and virtue are period "
                "normative claims, not independently measured morality."
            ),
            (
                "Mars's military status, Mercury's intellect/scholarship and "
                "Saturn's possessions are old social categories, not literal modern "
                "job predictions."
            ),
            (
                "First house honors from personal industry and second house honors "
                "from wealth are separate alleged causes, not the same event as "
                "receiving a public appointment."
            ),
            (
                "Two staged explicit fallbacks are given: if no light-aspecting "
                "source planet select strongest tenth occupant; if no tenth "
                "occupant use tenth ruler and its occupied house."
            ),
            (
                "Lilly acknowledges an alternative reading from other astrologers "
                "considering a dispositor of luminary above earth or the most "
                "partile luminary/tenth-ruler connection; neither has an "
                "established priority for conflicts."
            ),
            (
                "No verified personal career path, social baseline, historical "
                "income, birth-time record, outcome denominator, decoy or "
                "prospective evaluation appears in the source."
            ),
            (
                "This is selective first-edition historical paraphrase and "
                "photographed provenance, not a diplomatic source edition or tested "
                "natal causal model."
            ),
            (
                "The separately printed CHAP CXLVII begins after a horizontal "
                "divider on original PDF656 and concerns HONORS CONTINUING; do not "
                "include it as CXLVI."
            ),
        ],
        "source_planet_essential_dignity_weights_complete": False,
        "printed_CXLV_text_observed": False,
        "real_human_status_cause_accuracy_validated": 0,
        "real_person_recommendation_or_moral_classification_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06z",
        "status": "ORIGINAL_1647_CXLVI_CAUSES_OF_PREFERMENT_SOURCE_ONLY",
        "printed_chapter": "CXLVI",
        "record_count": 55,
        "first_record": "R9313",
        "last_record": "R9367",
        "substantive": 53,
        "following_navigation": 2,
        "source_groups": 4,
        "body_original_pdf_frames": [655, 656],
        "following_printed": "CXLVII",
        "next_original_pdf": 656,
        "previous_printed_CXLV_present": False,
        "complete_diplomatic_transcription": False,
        "empirical_validations": 0,
        "source_causal_model_runtime_promotions": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06z",
        "status": "FIRST_EDITION_CXLVI_PREFERMENT_CAUSES_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 9312,
        "new_historical_annotations": 55,
        "lilly_if_published": 9367,
        "ptolemy_retained": 1066,
        "combined_if_published": 10433,
        "substantive": 53,
        "navigation": 2,
        "source_groups": 4,
        "new_numbered_chapters": 1,
        "following_printed_chapter": "CXLVII",
        "following_heading_pdf": 656,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "human_status_cause_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original 1647 CXLVI: 55 historical source notes R9313–R9367")
