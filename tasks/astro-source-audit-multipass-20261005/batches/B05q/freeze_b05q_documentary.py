#!/usr/bin/env python3
"""First-edition Lilly: wealth durability history; no real financial prediction."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def load(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def dump(name, content):
    (B / name).write_text(
        json.dumps(content, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


author = load("SOURCE_FIRST_AUTHORING_20261017.json")
assert author["batch"] == "B05q"
assert author["printed_chapter"] == "CXVII"
assert author["editorial_chapter"] == "CXVIII"
assert author["original_body_pdf_frames"] == [596, 597, 598]
assert len(author["source_groups"]) == 13
rules, reverse = [], []
for group_no, group in enumerate(author["source_groups"], 1):
    sid = f"B05q-S{group_no:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {596, 597, 598, 599}
    refs = []
    for claim in group["claims"]:
        no = 7052 + len(rules)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["anchor_not_diplomatic"]) >= 6
        assert len(claim["historical_only_meaning"]) >= 50
        assert not (claim["independent_financial_outcome_verified"] or claim["runtime_promoted"])
        row = {
            "id": rid,
            "record_number": no,
            "batch": "B05q",
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "role": claim["role"],
            "printed_chapter": (
                "CXVII" if claim["role"] != "next_section_navigation" else "THIRD_HOUSE_NAVIGATION"
            ),
            "original_anchor_not_diplomatic": claim["anchor_not_diplomatic"],
            "meaning_historical_only": claim["historical_only_meaning"],
            "qualification": claim["qualification"],
            "historical_documentary_accepted": True,
            "diplomatic_transcription_complete": False,
            "independent_human_financial_validation": False,
            "actual_wealth_timing_accuracy_verified": False,
            "real_person_moral_or_legal_inference_authorized": False,
            "runtime_model_promoted": False,
        }
        rules.append(row)
        refs.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["source_group"],
            "mapped_record_ids": refs,
        }
    )
assert len(rules) == 75
assert [r["record_number"] for r in rules] == list(range(7052, 7127))
assert len({r["id"] for r in rules}) == len(rules)
assert [r["id"] for r in rules if r["role"] == "next_section_navigation"] == [
    "R7124",
    "R7125",
    "R7126",
]
assert len(reverse) == 13
images = {}
for page in range(596, 601):
    p = B / "evidence" / f"pdf_1647-{page}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(page)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(p),
        "original_printed_page": str(page - 34),
        "role": "chapter_body" if page <= 598 else "next_source_context",
    }
dump(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05q",
        "source": "William Lilly 1647 first edition, Wellcome b30338724",
        "volume_pdf_sha256": ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"),
        "source_body_pages": [596, 597, 598],
        "first_following_unnumbered_heading_page": 598,
        "next_printed_chapter_CXVIII_heading_page": 598,
        "images": images,
    },
)
dump(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05q",
        "source_groups": reverse,
        "source_group_count": 13,
        "record_count": 75,
        "substantive_records": 72,
        "next_section_navigation": 3,
    },
)
limits = [
    "Original source assertions about preserving, losing, or obtaining wealth "
    "are not verified financial outcomes or practical financial guidance.",
    "Benevolence, power and essential dignity must be combined for Lilly's "
    "strong second-house occupant persistence claim.",
    "A weak second-house planet or even a strong Infortune may permit estate "
    "to continue with difficulties and episodic losses; positive and negative "
    "cases overlap and need preregistered rejection rules.",
    "The empty-second fallback names both Lord of Second and Dispositor "
    "of Part of Fortune, but the priority between them is not explicit.",
    "The source's third aspect symbol alongside sextile and trine is "
    "hard to distinguish visually; do not encode a claimed operator.",
    "The house-quadrant time estimates contain overlapping numerical age "
    "ranges and a discretionary adjustment for estimated lifespan.",
    "Oriental/occidental placements, swift/direct/retrograde conditions "
    "and optional directions permit multiple event-time candidates; "
    "no prospective tolerance or rejection windows are given.",
    "The alleged losses through confiscation and banishment do not "
    "validate any actual legal event or moral accusation.",
    "The additional original symbol after Saturn/Mars for bad "
    "second-house occupants remains unconfirmed.",
    "Original names Oculus Tauri, Cor Scorpionis, Caput Medusae require "
    "historically correct fixed-star identifications and geometry "
    "before any computation.",
    "The Saturn covetousness personality allegation is historical "
    "stereotyping and may never label actual people.",
    "The compound 'both retrograde, cadent, peregrine, contrary "
    "nature' clause has uncertain antecedents and conjunction scope.",
    "Family inheritance, maternal/paternal estate and occupation "
    "are non-astrological socioeconomic predictors and confounders.",
    "No human chart/outcome observations, objective financial series, "
    "time-window precision, or statistical controls appear here.",
    "Following unnumbered third-house introductory prose and "
    "printed CXVIII 'If have Brethren or Sisters' both begin "
    "on frame598 and were not extracted into this wealth batch.",
    "Original first-edition scans and selective source anchors are "
    "preserved but this is not full diplomatic transcription.",
]
dump(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05q",
        "issues": limits,
        "actual_human_prediction_validations": 0,
        "clinical_or_financial_actions_authorized": False,
        "runtime_promotions": 0,
    },
)
dump(
    "RULES.json",
    {
        "batch": "B05q",
        "status": "ORIGINAL_1647_HISTORICAL_DOCUMENTARY_LOCALLY_ADMITTED",
        "printed_chapter": "CXVII",
        "editorial_chapter": "CXVIII",
        "record_count": 75,
        "first_record": "R7052",
        "last_record": "R7126",
        "source_passage_groups": 13,
        "substantive_historical_clauses": 72,
        "next_section_navigation_records": 3,
        "original_body_pdf_frames": [596, 597, 598],
        "next_unnumbered_heading_pdf_frame": 598,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "real_financial_outcomes_validated": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
dump(
    "ACCEPTANCE.json",
    {
        "batch": "B05q",
        "status": "DOCUMENTARY_LOCALLY_ACCEPTED_PENDING_REMOTE",
        "previous_lilly": 7051,
        "new_records": 75,
        "lilly_if_published": 7126,
        "ptolemy_retained": 1066,
        "combined_historical_if_published": 8192,
        "substantive_records": 72,
        "next_section_navigation": 3,
        "source_groups": 13,
        "original_body_pdf_frames": [596, 597, 598],
        "source_context_pdf_frames": [599, 600],
        "next_section": "UNNUMBERED_THIRD_HOUSE_BRETHREN",
        "next_section_pdf_frame": 598,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "independent_wealth_timing_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B05q source freeze R7052–R7126, 75 records, empirical=0")
