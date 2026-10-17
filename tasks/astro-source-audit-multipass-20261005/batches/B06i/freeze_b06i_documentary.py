#!/usr/bin/env python3
"""Archive Lilly 1647 CXXXI marriage ease and directions as history only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def write(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261017.json")
procedure = j("MARRIAGE_PRIMARY_DIRECTIONS_HISTORICAL_METHOD_V1.json")
assert a["batch"] == "B06i" and a["printed_chapter"] == "CXXXI"
assert a["source_body_pdf_frames"] == [623, 624]
assert len(a["groups"]) == 11
assert procedure["printed_chapter"] == "CXXXI"
assert procedure["procedure_status"] == ("HISTORICAL_SOURCE_STRUCTURED_NOT_EXECUTABLE_OR_VALIDATED")
assert len(procedure["steps"]) == 14
assert procedure["empirical_status"]["dates_predicted"] is False
assert procedure["empirical_status"]["runtime_promotions"] == 0

rules, mapping = [], []
for index, group in enumerate(a["groups"], 1):
    sid = f"B06i-S{index:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {623, 624}
    ids = []
    for claim in group["claims"]:
        num = 7944 + len(rules)
        rid = f"R{num}"
        assert claim["id"] == rid
        assert len(claim["original_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning"]) >= 40
        assert not claim["independent_marriage_timing_accuracy_validated"]
        assert not claim["runtime_promoted"]
        rules.append(
            {
                "id": rid,
                "record_number": num,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "original_anchor_not_diplomatic": claim["original_anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_meaning"],
                "source_qualification": claim["qualification"],
                "documentary_source_accepted": True,
                "independent_human_marriage_difficulty_validated": False,
                "independent_marriage_calendar_date_validated": False,
                "actual_partner_age_or_personal_behavior_validated": False,
                "source_direction_computation_executable": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    mapping.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "passage_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rules) == 83
assert [r["record_number"] for r in rules] == list(range(7944, 8027))
assert [r["id"] for r in rules if r["role"] == "next_chapter_navigation"] == ["R8025", "R8026"]
assert len({r["id"] for r in rules}) == 83

images = {}
for page in range(623, 628):
    p = B / "evidence" / f"pdf_1647-{page}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(page)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(p),
        "printed_folio": str(page - 34),
        "source_role": (
            "ease_and_directions_body" if page <= 624 else "following_numbered_chapters_context"
        ),
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06i",
        "source": (
            "William Lilly Christian Astrology original first edition 1647 Wellcome b30338724"
        ),
        "volume_original_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_frames": [623, 624],
        "next_printed_CXXXII_heading_frame": 624,
        "marriage_time_heading_within_CXXXI": True,
        "images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06i",
        "source_groups": mapping,
        "source_group_count": 11,
        "historical_records": 83,
        "substantive_historical": 81,
        "following_navigation": 2,
        "historical_direction_steps": len(procedure["steps"]),
        "source_method_file": "MARRIAGE_PRIMARY_DIRECTIONS_HISTORICAL_METHOD_V1.json",
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06i",
        "issues": [
            (
                "The original seventeenth-century text alleges "
                "marriage difficulty and marriage timing, but "
                "no birth certificates, verified marriages, "
                "nonmatches or prospective controls are given."
            ),
            (
                "Earlier unnumbered seventh-house introduction "
                "addresses whether marriage occurs; this "
                "numbered CXXXI concerns obtaining marriage "
                "with ease and timing. They are different targets."
            ),
            (
                "An earlier or later marriage and the age of "
                "the spouse at marriage are explicit alternative "
                "outcomes in the source, not interchangeable tests."
            ),
            (
                "The source's age classes Youth, maturer years "
                "and very aged spouse have no specified cutoffs."
            ),
            (
                "The east/Oriental and west/Occidental quarters "
                "use source-defined six-house lists that need "
                "historical astronomical geometry checks."
            ),
            (
                "Moon Orientall of Sun versus general "
                "significators occidentall has different grammatical "
                "scope and prerequisites, not a simple house rule."
            ),
            (
                "Direct/swift and retrograde/slow/stationary "
                "planetary states may contradict each other across "
                "multiple indicators, without deterministic weights."
            ),
            (
                "When testimonies disagree, Lilly prioritizes "
                "indicator alignment with Moon then Venus, "
                "but provides no mathematical thresholds."
            ),
            (
                "Lilly's personal anecdote of four adverse marriage "
                "placements does not report denominator, "
                "counterexamples, or observable full histories."
            ),
            (
                "The source's sexual desire and lasciviousness "
                "claims are historically stigmatizing stereotypes, "
                "not facts about actual persons."
            ),
            (
                "Sun/MC/Moon directions to Moon/Venus and "
                "seventh lord/benefic offer many overlapping "
                "potential event matches without selection policy."
            ),
            (
                "Precise original direct/converse primary "
                "directions, Regiomontanus house geometry, "
                "aspect calculation, term/bounds table and "
                "arc-to-age conversion are NOT supplied."
            ),
            (
                "Squares/oppositions to Sun/Mars are used "
                "with a Terms-of-a-Fortune caveat, "
                "not independently reproducible in this batch."
            ),
            (
                "Qualitative marriage and partner-age claims, "
                "primary directions and source interpretation "
                "are preserved without runtime implementation."
            ),
            (
                "Printed CXXXII on number of wives begins "
                "lower original PDF624 and belongs to "
                "a separate future source batch."
            ),
            (
                "No woman/wife personal characterization, "
                "intimate behavior, birth date or future "
                "marriage prediction may be inferred from "
                "this source as established fact."
            ),
            (
                "The packet is an anchored selective "
                "source paraphrase, not a complete "
                "diplomatic first-edition transcription."
            ),
        ],
        "historic_primary_directions_executable": False,
        "marriage_ages_or_dates_validated": 0,
        "intimate_behavior_predictions_authorized": False,
        "runtime_promotions": 0,
    },
)
write(
    "RULES.json",
    {
        "batch": "B06i",
        "status": "ORIGINAL_1647_MARRIAGE_EASE_DIRECTIONS_HISTORICAL_ONLY",
        "printed_chapter": "CXXXI",
        "editorial_chapter": "CXXXII",
        "record_count": 83,
        "first_record": "R7944",
        "last_record": "R8026",
        "substantive": 81,
        "next_chapter_navigation": 2,
        "source_groups": 11,
        "original_source_frames": [623, 624],
        "next_numbered_frame": 624,
        "historic_direction_method_steps": 14,
        "direction_algorithm_complete": False,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "independent_human_marriage_timing_validations": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
write(
    "ACCEPTANCE.json",
    {
        "batch": "B06i",
        "status": "SOURCE_HISTORICAL_LOCALLY_FROZEN_PENDING_GITHUB",
        "prior_lilly": 7943,
        "new_historical_annotations": 83,
        "lilly_if_published": 8026,
        "ptolemy_retained": 1066,
        "combined_if_published": 9092,
        "substantive": 81,
        "navigation": 2,
        "source_groups": 11,
        "numbered_chapters_added": 1,
        "next_printed_chapter": "CXXXII",
        "next_original_pdf": 624,
        "rules_sha256": sha(B / "RULES.json"),
        "source_authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "marriage_method_sha256": sha(B / "MARRIAGE_PRIMARY_DIRECTIONS_HISTORICAL_METHOD_V1.json"),
        "empirical_validations": 0,
        "real_marriage_date_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06i printed CXXXI R7944–R8026: 83 historical notes; 14 steps, 0 forecasts")
