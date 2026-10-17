#!/usr/bin/env python3
"""Archive William Lilly original 1647 competing wife-count methods as history."""

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


a = read("SOURCE_FIRST_AUTHORING_20261017.json")
m = read("COMPETING_WIFE_COUNT_HISTORICAL_METHODS_V1.json")
assert a["batch"] == "B06j" and a["printed_chapter"] == "CXXXII"
assert a["body_pdf_frames"] == [624, 625, 626]
assert a["following_printed"] == "CXXXIII"
assert len(a["groups"]) == 11
assert m["printed_chapter"] == "CXXXII"
assert len(m["methods"]) == 10
assert m["empirical_validations"] == m["runtime_promotions"] == 0
assert not m["actual_person_partner_claims_authorized"]

records, reverse = [], []
for n, group in enumerate(a["groups"], 1):
    sid = f"B06j-S{n:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {624, 625, 626}
    refs = []
    for claim in group["clauses"]:
        no = 8027 + len(records)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["original_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_only_meaning"]) >= 40
        assert not claim["independent_spouse_number_validated"]
        assert not claim["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "original_anchor_not_diplomatic": claim["original_anchor_not_diplomatic"],
                "meaning_historical_only": claim["historical_only_meaning"],
                "source_qualification": claim["qualification"],
                "historical_documentary_accepted": True,
                "independent_legal_spouse_count_validated": False,
                "independent_nonmarital_partner_count_validated": False,
                "marital_survival_order_validated": False,
                "original_ptolemy_text_independently_verified": False,
                "private_partner_or_sexual_claim_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        refs.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["group"],
            "mapped_record_ids": refs,
        }
    )
assert len(records) == 80
assert [x["record_number"] for x in records] == list(range(8027, 8107))
assert [x["id"] for x in records if x["role"] == "next_chapter_navigation"] == ["R8105", "R8106"]
assert len({x["id"] for x in records}) == 80

photos = {}
for f in range(624, 628):
    p = B / "evidence" / f"pdf_1647-{f}.jpg"
    raw = p.read_bytes()
    assert len(raw) > 150000 and raw[:2] == bytes.fromhex("ffd8")
    photos[str(f)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(p),
        "printed_folio": str(f - 34),
        "role": "wife_count_body" if f <= 626 else "following_spouse_origin_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06j",
        "source": "William Lilly Christian Astrology original 1647 Wellcome b30338724",
        "original_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [624, 625, 626],
        "following_printed_CXXXIII_heading_frame": 626,
        "images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06j",
        "source_groups": reverse,
        "source_group_count": 11,
        "record_count": 80,
        "substantive_historical_clauses": 78,
        "following_chapter_navigation": 2,
        "competing_historic_methods": len(m["methods"]),
        "methods_file": "COMPETING_WIFE_COUNT_HISTORICAL_METHODS_V1.json",
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06j",
        "issues": [
            (
                "Lilly's original number-of-wives rules allow "
                "legal spouses, repeated ceremonies, nonmarital "
                "sweethearts and concubines to count as different "
                "outcomes; they are not interchangeable data."
            ),
            (
                "Moon in the seventh is claimed to predict "
                "more than one Wife, yet author admits it "
                "did not always give two legal wives; "
                "the self-report shifts to female friends "
                "or concubines, preventing unambiguous scoring."
            ),
            (
                "The author's 'never knew the Native failed' "
                "report is retrospective with no denominator, "
                "complete cases or transparent misses."
            ),
            (
                "Moon conjoined exactly one planet is alleged "
                "to indicate one wife, a potentially conflicting "
                "count with the Moon-in-seventh rule."
            ),
            (
                "Relative Moon-versus-aspecting-planet strength "
                "is used to claim order of death of husband "
                "versus wife; it is unverified and not "
                "legitimate health, safety or lifespan advice."
            ),
            (
                "The number count based on Moon applying "
                "partile to eligible direct noncombust "
                "planets excludes Sun and requires "
                "application in the correct direction."
            ),
            (
                "When qualifying planets occupy fruitful signs, "
                "the source doubles their number: another "
                "flexible alternative with no predetermined "
                "priority against other rules."
            ),
            (
                "The one-form or bicorporeal Moon method is "
                "attributed to Ptolemy by Lilly; Ptolemy's "
                "original source text has not yet been "
                "collated here."
            ),
            (
                "Additional fallback counts depend on planets "
                "between Midheaven and Venus or partile "
                "aspects to Lord Seventh, with inconsistent "
                "retrogradation/combustion eligibility "
                "depending on dignity or method choice."
            ),
            (
                "Lilly claims his best experienced method "
                "counts Moon-sign applying planets, or "
                "alternatively dignity-bearing aspecting "
                "planets, with no auditable prospective test."
            ),
            (
                "Weak marriage significators are explicitly "
                "said to imply courtship, affairs and "
                "sweethearts instead of actual wives; this "
                "is an alternative target, not confirmation."
            ),
            (
                "Two- or three-wife rules from common, "
                "fruitful/bicorporeal Moon and planet signs "
                "can overlap multiple other counting methods."
            ),
            (
                "The author calls the compounded fruitful "
                "seventh-house three-wife result certain, "
                "but offers no independent marriage register "
                "or sample of people with or without it."
            ),
            (
                "No single deterministic algorithm, "
                "planet-count weights, historical aspect orb "
                "thresholds or birth-time uncertainty rule "
                "has been finalized."
            ),
            (
                "No independent legal-marriage certificates, "
                "personal relationship histories, partner "
                "data, calendar periods or matched controls "
                "were inspected for this source batch."
            ),
            (
                "The following printed CHAP CXXXIII on "
                "geographical origin/quarter of wife "
                "begins lower PDF626 and is not included."
            ),
            (
                "The packet is a selective qualified "
                "original-source paraphrase, not a complete "
                "early-modern diplomatic transcription."
            ),
        ],
        "independent_human_marital_outcome_validations": 0,
        "verified_ptolemy_original_comparison": False,
        "private_intimate_or_survival_forecasts_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06j",
        "status": "ORIGINAL_1647_WIFE_COUNT_COMPETING_METHODS_HISTORICAL_ONLY",
        "printed_chapter": "CXXXII",
        "editorial_chapter": "CXXXIII",
        "record_count": 80,
        "first_record": "R8027",
        "last_record": "R8106",
        "substantive_historical": 78,
        "following_navigation": 2,
        "source_groups": 11,
        "competing_counting_methods": 10,
        "original_body_frames": [624, 625, 626],
        "following_numbered_heading_frame": 626,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "legal_marriage_or_partner_counts_validated": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06j",
        "status": "FIRST_EDITION_HISTORIC_WIFE_COUNT_FROZEN_PENDING_REMOTE",
        "previous_lilly": 8026,
        "new_historical_annotations": 80,
        "lilly_if_published": 8106,
        "ptolemy_retained": 1066,
        "combined_if_published": 9172,
        "substantive": 78,
        "navigation": 2,
        "source_groups": 11,
        "numbered_chapters_added": 1,
        "next_printed_chapter": "CXXXIII",
        "next_original_pdf": 626,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "competing_methods_sha256": sha(B / "COMPETING_WIFE_COUNT_HISTORICAL_METHODS_V1.json"),
        "empirical_validations": 0,
        "real_marriage_or_spouse_count_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06j historic competing wife-number methods: 80 notes R8027-R8106")
