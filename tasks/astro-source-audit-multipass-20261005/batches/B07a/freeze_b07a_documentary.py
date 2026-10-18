#!/usr/bin/env python3
"""Freeze Lilly first-edition CXLVII continuity of honors as historical source."""

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
assert a["batch"] == "B07a"
assert a["printed_chapter"] == "CXLVII"
assert a["body_original_frames"] == [656, 657, 658]
assert a["next_printed"] == "CXLVIII"
assert a["following_heading_frame"] == 658
assert len(a["groups"]) == 6

rows, mapping = [], []
for i, group in enumerate(a["groups"], 1):
    sid = f"B07a-S{i:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {656, 657, 658}
    ids = []
    for claim in group["claims"]:
        num = 9368 + len(rows)
        rid = f"R{num}"
        assert claim["id"] == rid
        assert len(claim["source_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning_only"]) >= 42
        assert claim["source_only"]
        assert not claim["human_honor_duration_accuracy_validated"]
        assert not claim["real_person_reputation_danger_claim_authorized"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": num,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "original_anchor_not_diplomatic": claim["source_anchor_not_diplomatic"],
                "historical_source_meaning_only": claim["historical_meaning_only"],
                "qualification": claim["qualification"],
                "documentary_source_accepted": True,
                "real_person_honor_persistence_validated": False,
                "real_person_promotion_or_loss_age_validated": False,
                "actual_reputation_or_moral_trait_validated": False,
                "fixed_star_natal_parity_verified": False,
                "joint_nation_individual_chart_method_verified": False,
                "real_person_social_danger_or_prognosis_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    mapping.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rows) == 77
assert [r["record_number"] for r in rows] == list(range(9368, 9445))
assert [r["id"] for r in rows if r["role"] == "next_chapter_navigation"] == ["R9443", "R9444"]

images = {}
for n in range(656, 661):
    file = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(file.relative_to(B)),
        "sha256": sha(file),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "role": (
            "CXLVII_honor_continuity_original_body"
            if n <= 658
            else "following_profession_chapter_context_only"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07a",
        "source": "William Lilly Christian Astrology 1647 first edition Wellcome b30338724",
        "original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": [656, 657, 658],
        "following_printed_CXLVIII_heading_pdf": 658,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07a",
        "source_groups": mapping,
        "source_group_count": 6,
        "record_count": 77,
        "substantive": 75,
        "next_numbered_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07a",
        "issues": [
            (
                "CXLVII concerns CONTINUITY of honor, not whether "
                "a person receives honor or the source/type of it. "
                "Continual increase, temporary increase then decline, "
                "interruption, total loss, later recovery and "
                "social infamy are distinct historical endpoints."
            ),
            (
                "Eligible indicator planets must closely aspect "
                "the luminaries with priority to the strongest; "
                "a source glyph in the very first line "
                "requires future diplomatic collation."
            ),
            (
                "Strong Jupiter/Venus and weak/moderate Jupiter/Venus "
                "give opposing temporal outcomes; similarly "
                "strong Saturn/Mars can permit continuation "
                "despite supposed threat, not simply malefic=loss."
            ),
            (
                "Mercury may indicate rapid increase and "
                "later difficulty, with an exceptional claim "
                "that person's understanding averts full ruin. "
                "This admits nonchart protective activity "
                "rather than a deterministic natal forecast."
            ),
            (
                "When no planet aspects either luminary "
                "the source falls back to the strongest "
                "tenth-house occupant, then (if empty) "
                "tenth ruler, its sign and friendly aspects."
            ),
            (
                "Tenth ruler and tenth sign BOTH fixed "
                "and friendly Sun/Moon/Jupiter/Venus "
                "aspects to tenth cusp OR tenth ruler "
                "form a composite continuation source."
            ),
            (
                "The unnumbered special aphorisms on "
                "PDF657–658 belong WITHIN printed CXLVII, "
                "not to a separate missing chapter."
            ),
            (
                "Original names Hyades, Hercules, Cor Scorpii, "
                "Lanx Australis are fixed-star source labels. "
                "No modern star identity, period longitude, "
                "direction to year or nativity chart parity."
            ),
            (
                "The solar sign glyphs before good/ill directions "
                "and one original lunar MC sign are unclear. "
                "These source conditions remain NONEXECUTABLE."
            ),
            (
                "An apparent ancient King's just rule "
                "depends on comparison with a nation/people's "
                "nativities and cannot be inferred from "
                "one individual birth chart."
            ),
            (
                "Old stigmatizing terms 'infamous', "
                "unfortunate and lifelong moral labels "
                "are unverified rhetoric and no real "
                "person inference or treatment advice."
            ),
            (
                "The original provides no time windows, "
                "starting rank, duration thresholds, "
                "employment records, wealth baseline "
                "or chart-outcome calibrated probability."
            ),
            (
                "Printed CXLVIII Magistery/Profession begins "
                "on original PDF658 after distinct divider. "
                "Its definition and count of professional "
                "decisions are only navigational here."
            ),
            (
                "This packet is short original-page anchored "
                "historical paraphrase, not a full "
                "diplomatic seventeenth-century transcription."
            ),
        ],
        "original_solar_and_lunar_glyphs_fully_deciphered": False,
        "original_fixed_star_placement_verified_in_modern_ephemeris": False,
        "source_status_duration_model_executable": False,
        "independently_tested_human_honor_duration_accuracy": 0,
        "actual_person_moral_status_or_travel_safety_claim_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07a",
        "status": "ORIGINAL_1647_CXLVII_DURATION_OF_HONOR_HISTORICAL_ONLY",
        "printed_chapter": "CXLVII",
        "record_count": 77,
        "first_record": "R9368",
        "last_record": "R9444",
        "substantive": 75,
        "following_navigation": 2,
        "source_groups": 6,
        "body_original_pdf_frames": [656, 657, 658],
        "following_printed_chapter": "CXLVIII",
        "following_heading_pdf": 658,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "human_honor_status_duration_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07a",
        "status": "ORIGINAL_CXLVII_HONOR_DURATION_LOCALLY_FROZEN",
        "previous_lilly": 9367,
        "new_historical_annotations": 77,
        "lilly_if_published": 9444,
        "ptolemy_retained": 1066,
        "combined_if_published": 10510,
        "substantive": 75,
        "navigation": 2,
        "source_groups": 6,
        "new_numbered_chapters": 1,
        "following_printed_chapter": "CXLVIII",
        "following_heading_pdf": 658,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "real_human_honor_duration_accuracy_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Lilly original CXLVII dignity continuity: 77 historic R9368–R9444")
