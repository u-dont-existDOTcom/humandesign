#!/usr/bin/env python3
"""Freeze Lilly original CXLIII dreams source-only archival clauses."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, obj):
    (B / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261018.json")
assert a["batch"] == "B06w"
assert a["printed_chapter"] == "CXLIII"
assert a["body_original_pdf_frames"] == [647, 648]
assert a["next_source"] == "UNNUMBERED_TENTH_HOUSE_HONOURS_DIGNITIES"
assert a["next_source_pdf_frame"] == 649
assert a["following_printed_chapter"] == "CXLIIII"
assert a["following_printed_frame"] == 649
assert len(a["groups"]) == 7

records, reverse = [], []
for index, group in enumerate(a["groups"], 1):
    sid = f"B06w-S{index:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {647, 648, 649}
    ids = []
    for claim in group["claims"]:
        number = 9040 + len(records)
        rid = f"R{number}"
        assert claim["id"] == rid
        assert len(claim["original_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning_only"]) >= 40
        assert claim["source_only"]
        assert not claim["independently_validated_human_dream_outcome"]
        assert not claim["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": number,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "source_anchor_not_diplomatic": claim["original_anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_meaning_only"],
                "source_qualification": claim["qualification"],
                "original_first_edition_documented": True,
                "independent_dream_content_prediction_validated": False,
                "independent_dream_prophecy_accuracy_validated": False,
                "independent_sleep_psychological_diagnosis_validated": False,
                "human_spiritual_or_nightmare_classification_authorized": False,
                "dream_to_real_event_causation_verified": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 66
assert [x["record_number"] for x in records] == list(range(9040, 9106))
assert [x["id"] for x in records if x["role"] == "next_section_navigation"] == ["R9104", "R9105"]
assert len({x["id"] for x in records}) == 66

images = {}
for page in [647, 648, 649, 650, 651]:
    file = B / "evidence" / f"pdf_1647-{page}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(page)] = {
        "file": str(file.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(file),
        "printed_folio": str(page - 34),
        "role": (
            "original_printed_dreams_body"
            if page <= 648
            else "following_tenth_house_honors_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06w",
        "source": (
            "William Lilly Christian Astrology original 1647 first edition Wellcome b30338724"
        ),
        "full_original_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": [647, 648],
        "following_unnumbered_tenth_house_pdf": 649,
        "following_printed_CXLIIII_heading_pdf": 649,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06w",
        "source_groups": reverse,
        "source_group_count": 7,
        "record_count": 66,
        "substantive": 64,
        "next_section_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06w",
        "issues": [
            (
                "Original dream rules consider both alleged "
                "truthfulness of dream outcomes and the dream's "
                "content/sensory themes. The two are different "
                "targets, not interchangeable confirmations."
            ),
            (
                "Jupiter or Venus in ninth, potent and not afflicted, "
                "allegedly give dreams corresponding to actual "
                "events; the source provides no forecast window, "
                "target event registry, hit denominator or controls."
            ),
            (
                "Malefics in ninth allegedly give dreams wholly "
                "deceitful; this is a retrospective and untested "
                "dream-to-event correspondence claim."
            ),
            (
                "Benefics in ninth but debilitated/afflicted "
                "permit ambiguous dreams both sometimes true "
                "and sometimes false, so matching one detail "
                "alone could not establish accurate prediction."
            ),
            (
                "When no planet occupies ninth the author "
                "uses ninth cusp sign and its ruler as fallback, "
                "rather than assuming no dreams occur."
            ),
            (
                "The content categories Saturn agriculture/caves/"
                "burial/fear, Jupiter gentry/church, Mars fights/"
                "war/animals/fires, Sun gold/status, Venus pleasure/"
                "clothes/smells, Mercury books/journeys/youth, "
                "Moon water/sea/flying, overlap significantly."
            ),
            (
                "Moon with Saturn is given as a conditional "
                "horrifying-dream exception; this is not "
                "a clinical nightmare or trauma diagnosis."
            ),
            (
                "Spirits, demons and prophecy language in "
                "the historical original concerns perceived "
                "dream content or claimed symbolism, not "
                "independently established supernatural facts."
            ),
            (
                "No real human dream reports, independent "
                "pre-registered dream dates, outcome verification, "
                "comparison subjects or blind testing occurred."
            ),
            (
                "Original chapter source ends bottom PDF648 "
                "but its trailing printed word 'The' is a "
                "catchword leading to the separate substantive "
                "UNNUMBERED tenth-house introduction PDF649."
            ),
            (
                "No royal rank, supernatural ability, clinical "
                "sleep or mental-health classification may "
                "be inferred from natal planets based on "
                "these unvalidated historical claims."
            ),
            (
                "The next separately numbered printed "
                "CHAP CXLIIII on honors begins later PDF649 "
                "after the unnumbered tenth-house introduction; "
                "must not skip the intervening material."
            ),
            (
                "Photographic provenance and record mapping "
                "tests establish historical-source integrity, "
                "not the truth of predictive astrology."
            ),
        ],
        "original_glyphs_and_aspect_orbs_fully_transcribed": False,
        "dream_prophecy_forecasts_independently_validated": 0,
        "actual_sleep_or_spiritual_diagnosis_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06w",
        "status": "ORIGINAL_FIRST_EDITION_DREAM_VERACITY_CONTENT_HISTORICAL_ONLY",
        "printed_chapter": "CXLIII",
        "editorial_chapter": "CXLIV",
        "record_count": 66,
        "first_record": "R9040",
        "last_record": "R9105",
        "substantive": 64,
        "following_navigation": 2,
        "source_groups": 7,
        "body_original_pdf_frames": [647, 648],
        "next_source": "UNNUMBERED_TENTH_HOUSE_HONOURS_DIGNITIES",
        "next_source_pdf": 649,
        "following_printed_chapter": "CXLIIII",
        "following_heading_pdf": 649,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "independent_human_dream_prediction_validations": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06w",
        "status": "FIRST_EDITION_DREAMS_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 9039,
        "new_historical_records": 66,
        "lilly_if_published": 9105,
        "ptolemy_retained": 1066,
        "combined_if_published": 10171,
        "substantive": 64,
        "navigation": 2,
        "source_groups": 7,
        "numbered_chapters_added": 1,
        "next_source": "UNNUMBERED_TENTH_HOUSE_HONOURS_DIGNITIES",
        "next_original_pdf": 649,
        "following_printed_chapter": "CXLIIII",
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "human_dream_prediction_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original 1647 CXLIII Dreams: 66 historical notes R9040–R9105; 0 true-human predictions")
