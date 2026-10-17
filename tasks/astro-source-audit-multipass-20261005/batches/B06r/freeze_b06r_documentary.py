#!/usr/bin/env python3
"""Archive original Lilly unnumbered ninth-house questions as history only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(n):
    return json.loads((B / n).read_text(encoding="utf-8"))


def save(n, obj):
    (B / n).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261017.json")
assert a["batch"] == "B06r"
assert a["source_section"] == "UNNUMBERED_NINTH_HOUSE_JOURNEYS_RELIGIONS"
assert a["printed_chapter"] is None
assert a["body_original_pdf_frames"] == [640]
assert a["following_printed_chapter"] == "CXXXIX"
assert a["following_heading_frame"] == 640
assert len(a["source_groups"]) == 5

records, reverses = [], []
for no, group in enumerate(a["source_groups"], 1):
    sid = f"B06r-S{no:03d}"
    assert group["source_span"] == sid
    assert group["original_pdf_frames"] == [640]
    ids = []
    for c in group["claims"]:
        num = 8681 + len(records)
        rid = f"R{num}"
        assert c["id"] == rid
        assert len(c["original_anchor_not_diplomatic"]) >= 6
        assert len(c["meaning_historical_only"]) >= 43
        assert not c["independent_human_travel_prediction_validated"]
        assert not c["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": num,
                "source_span": sid,
                "original_pdf_frame": 640,
                "role": c["role"],
                "original_anchor_not_diplomatic": c["original_anchor_not_diplomatic"],
                "historical_meaning_only": c["meaning_historical_only"],
                "source_qualification": c["source_qualification"],
                "historical_documentary_accepted": True,
                "independent_travel_occurrence_or_frequency_validated": False,
                "independent_travel_destination_or_cause_validated": False,
                "independent_travel_success_or_danger_validated": False,
                "real_person_faith_religion_or_safety_claim_authorized": False,
                "ptolemy_travel_attribution_independently_verified": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    reverses.append(
        {
            "source_span": sid,
            "original_pdf_frames": [640],
            "source_group": group["source_group"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 25
assert [r["record_number"] for r in records] == list(range(8681, 8706))
assert [r["id"] for r in records if r["role"] == "next_chapter_navigation"] == ["R8704", "R8705"]

images = {}
for n in [640, 641, 642]:
    f = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = f.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(f.relative_to(B)),
        "sha256": sha(f),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "role": "original_unnumbered_ninth_intro" if n == 640 else "following_travel_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06r",
        "source": "William Lilly Christian Astrology original 1647 Wellcome b30338724",
        "full_original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [640],
        "next_printed_CXXXIX_heading_pdf": 640,
        "unnumbered": True,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06r",
        "source_groups": reverses,
        "source_group_count": 5,
        "records_count": 25,
        "substantive": 23,
        "navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06r",
        "issues": [
            (
                "This is a substantive UNNUMBERED ninth-house introduction "
                "on original PDF640, not printed numbered CXXXIX. "
                "The printed chapter starts after the introduction "
                "on the SAME PDF640, so chapter numbering must not advance."
            ),
            (
                "Though heading says 'Journeys and Religions', "
                "the substantive passage introduces only travel; "
                "no religious behavior or conviction claims "
                "are established by this particular source."
            ),
            (
                "Lilly names ninth and its ruler, ninth occupants, "
                "Moon and Mercury, and attributes Mars addition "
                "to Ptolemy; exact original glyph and Ptolemy "
                "text have not been independently collated."
            ),
            (
                "Travel yes/no, once/multiple times, frequent, "
                "nearly lifelong transmarine residence and "
                "rare foreign journeys are overlapping outcomes "
                "without a count threshold or defined observation age."
            ),
            (
                "The author's destination question is conditional on "
                "already having decided travel will occur; "
                "it uses region relative to the natal country "
                "and allows several regions or a preferred one."
            ),
            (
                "Principal causes of travel, travel success and "
                "life-threatening hazard are distinct dependent "
                "variable questions, not independently verified "
                "positive astrological examples."
            ),
            (
                "The source provides no map projection, numeric "
                "bearing or physical distance, real-life case "
                "locations, journey registries, age horizons "
                "or comparable nonastrology baseline."
            ),
            (
                "Speculations on death, travel danger and faith "
                "could cause harm and cannot be used as "
                "a present-day safety, religion or life forecast."
            ),
            (
                "Historical source notes record what the "
                "1647 author asks an astrologer to examine, "
                "NOT demonstrated answers or forecast accuracy."
            ),
            (
                "The passage is source-anchored selective paraphrase "
                "and image provenance, not diplomatic "
                "seventeenth-century printed text edition."
            ),
        ],
        "original_ptolemy_mars_attribution_verified": False,
        "religious_personality_judgment_in_this_section": False,
        "independent_human_travel_predictions_validated": 0,
        "real_person_safety_or_faith_predictions_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06r",
        "status": "ORIGINAL_UNNUMBERED_NINTH_HOUSE_HISTORICAL_QUESTIONS_ONLY",
        "section": "UNNUMBERED_NINTH_HOUSE_JOURNEYS_RELIGIONS",
        "record_count": 25,
        "first_record": "R8681",
        "last_record": "R8705",
        "substantive": 23,
        "following_numbered_navigation": 2,
        "source_groups": 5,
        "original_body_pdf_frames": [640],
        "next_printed_chapter": "CXXXIX",
        "following_heading_original_pdf": 640,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "travel_or_life_danger_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06r",
        "status": "ORIGINAL_NINTH_HOUSE_HISTORICAL_LOCALLY_FROZEN",
        "previous_lilly": 8680,
        "new_historical_records": 25,
        "lilly_if_published": 8705,
        "ptolemy_retained": 1066,
        "combined_if_published": 9771,
        "substantive": 23,
        "navigation": 2,
        "source_groups": 5,
        "numbered_chapters_added": 0,
        "next_printed": "CXXXIX",
        "next_original_pdf_frame": 640,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "human_travel_accuracy_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06r original unnumbered ninth-house intro 25 historical source notes R8681–R8705.")
