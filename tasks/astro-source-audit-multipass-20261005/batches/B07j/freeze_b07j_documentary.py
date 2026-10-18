#!/usr/bin/env python3
"""Freeze 1647 Lilly CLV captivity and imprisonment only as historical text."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261018.json")
assert a["batch"] == "B07j"
assert a["printed_chapter"] == "CLV"
assert a["original_body_frames"] == [676, 677]
assert a["next_printed"] == "CLVI"
assert a["next_heading_pdf"] == 678
assert len(a["groups"]) == 8

rows, inverse = [], []
for k, group in enumerate(a["groups"], 1):
    sid = f"B07j-S{k:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {676, 677, 678}
    group_ids = []
    for c in group["claims"]:
        num = 10147 + len(rows)
        rid = f"R{num}"
        assert c["id"] == rid
        assert len(c["source_anchor_not_diplomatic"]) >= 5
        assert len(c["historical_meaning_only"]) >= 37
        assert c["source_only"]
        assert not c["independent_human_captivity_accuracy_validated"]
        assert not c["real_person_legal_danger_prediction_authorized"]
        assert not c["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": num,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": c["role"],
                "source_anchor_not_diplomatic": c["source_anchor_not_diplomatic"],
                "historical_meaning_only": c["historical_meaning_only"],
                "qualification": c["qualification"],
                "first_edition_documentary_accepted": True,
                "real_person_captivity_or_detention_accuracy_validated": False,
                "real_person_sentence_or_detention_duration_validated": False,
                "real_person_legal_risk_criminality_validated": False,
                "real_person_harm_mortality_or_health_validated": False,
                "original_astro_calculations_or_glyphs_fully_verified": False,
                "person_level_legal_medical_safety_forecast_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        group_ids.append(rid)
    inverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": group_ids,
        }
    )
assert len(rows) == 100
assert [x["record_number"] for x in rows] == list(range(10147, 10247))
assert [x["id"] for x in rows if x["role"] == "next_navigation"] == ["R10245", "R10246"]
assert len({x["id"] for x in rows}) == 100

photos = {}
for n in range(676, 680):
    f = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = f.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    photos[str(n)] = {
        "file": str(f.relative_to(B)),
        "sha256": sha(f),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "role": "CLV_body" if n <= 677 else "CLVI_death_chapter_following_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07j",
        "original_source": (
            "William Lilly Christian Astrology 1647 first edition Wellcome b30338724"
        ),
        "full_1647_source_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [676, 677],
        "following_printed_CLVI_heading_frame": 678,
        "images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07j",
        "source_groups": inverse,
        "source_group_count": 8,
        "source_annotations": 100,
        "substantive": 98,
        "navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07j",
        "issues": [
            (
                "Source printed CLV begins mid original PDF676/printed642 "
                "after CLIIII and ends bottom PDF677/printed643, before "
                "new separately numbered CLVI on violent/natural "
                "death at TOP PDF678."
            ),
            (
                "First ranking Sun and Moon, second Saturn and Mars, "
                "third seventh/twelfth houses and occupants is an "
                "original-source priority list, not a validated "
                "arrest-prison statistical model."
            ),
            (
                "Numerous elaborate alternative natal configurations "
                "are alleged to produce imprisonment, captivity, "
                "arrests, restraint of liberty, sorrow, many enemies "
                "or even death. These are different observable "
                "outcomes, not substitutable for a predictive hit."
            ),
            (
                "Original allows benevolent reception/dignities and "
                "benefic interruption of captivity predictions, "
                "including exceptions in the eighth-house "
                "luminary conjunction. Both literal no-event "
                "and event circumstances need frozen thresholds."
            ),
            (
                "Long versus short imprisonment is separately "
                "attributed to fortified opposing malefics in "
                "twelfth with no benefic relief vs beneficial "
                "aspects, but no duration units, starting age, "
                "conviction standard or country-specific laws "
                "are defined."
            ),
            (
                "The period source uses contradictory celestial "
                "combinations including ordinary conjunction, "
                "square, opposition, sextile, retrograde, "
                "combustion and essential dignity, with "
                "different fallback requirements and some "
                "printed zodiac glyphs uncertain."
            ),
            (
                "Historic service to Kings, imprisonment by rulers "
                "and alleged killing by them are source class "
                "stereotypes; they do not imply any person's "
                "actual criminality, legal status or danger."
            ),
            (
                "The following printed CLVI concerns violent "
                "vs natural mortality. Its detailed conditions "
                "are NOT included as CLV imprisonment records."
            ),
            (
                "No verified birth chart, prosecution/legal record, "
                "ground truth confinement date, sentence "
                "duration, geographic legal baseline, "
                "matched null or blind prospective participant "
                "was scored in this archival source study."
            ),
            (
                "The packet contains photographed short original "
                "source anchors and historically qualified "
                "paraphrases; it is not a complete diplomatic "
                "transcription or an executable safety model."
            ),
        ],
        "all_original_source_glyphs_and_orbs_verified": False,
        "fully_executable_captivity_risk_method": False,
        "independently_verified_human_detention_predictions": 0,
        "actual_person_criminality_captivity_medical_or_mortality_inference_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07j",
        "status": "FIRST_EDITION_CLV_CAPTIVITY_IMPRISONMENT_HISTORICAL_ONLY",
        "printed_chapter": "CLV",
        "record_count": 100,
        "first_record": "R10147",
        "last_record": "R10246",
        "substantive": 98,
        "following_navigation": 2,
        "source_groups": 8,
        "body_original_pdf_frames": [676, 677],
        "following_printed": "CLVI",
        "following_heading_pdf": 678,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "real_person_captivity_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07j",
        "status": "ORIGINAL_CLV_CAPTIVITY_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 10146,
        "new_historical_annotations": 100,
        "lilly_if_published": 10246,
        "ptolemy_retained": 1066,
        "combined_if_published": 11312,
        "substantive": 98,
        "navigation": 2,
        "source_groups": 8,
        "numbered_chapters_added": 1,
        "following_printed": "CLVI",
        "following_heading_pdf": 678,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "human_imprisonment_accuracy_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original CLV captivity source frozen: 100 historic R10147-R10246")
