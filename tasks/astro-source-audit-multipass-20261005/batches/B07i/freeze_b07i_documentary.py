#!/usr/bin/env python3
"""Freeze original 1647 Lilly CLIIII adversary victory and injury claims as history only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(filename):
    return json.loads((B / filename).read_text(encoding="utf-8"))


def save(filename, value):
    (B / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


auth = read("SOURCE_FIRST_AUTHORING_20261018.json")
assert auth["batch"] == "B07i"
assert auth["printed_chapter"] == "CLIIII"
assert auth["body_original_pdf_frames"] == [675, 676]
assert auth["next_printed"] == "CLV"
assert auth["next_heading_pdf"] == 676
assert len(auth["groups"]) == 6

rows, mapping = [], []
for idx, group in enumerate(auth["groups"], 1):
    span = f"B07i-S{idx:03d}"
    assert group["source_span"] == span
    assert set(group["original_pdf_frames"]) <= {675, 676}
    ids = []
    for claim in group["claims"]:
        no = 10083 + len(rows)
        rid = f"R{no}"
        assert rid == claim["id"]
        assert len(claim["original_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning_only"]) >= 37
        assert claim["source_only"]
        assert not claim["real_enemy_conflict_or_safety_accuracy_validated"]
        assert not claim["actual_person_danger_diagnosis_authorized"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": span,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "source_anchor_not_diplomatic": claim["original_anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_meaning_only"],
                "qualification": claim["qualification"],
                "first_edition_documentary_source": True,
                "independently_validated_real_adversary_victory": False,
                "independently_validated_injury_mortality_or_illness": False,
                "independently_validated_imprisonment_or_horse_fall": False,
                "independently_validated_relationship_danger": False,
                "real_person_adversary_or_friend_risk_advice_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    mapping.append(
        {
            "source_span": span,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rows) == 64
assert [r["record_number"] for r in rows] == list(range(10083, 10147))
assert [r["id"] for r in rows if r["role"] == "next_navigation"] == ["R10145", "R10146"]
assert len({r["id"] for r in rows}) == 64

photos = {}
for n in range(675, 678):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    photos[str(n)] = {
        "file": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "role": "original_CLIIII_body" if n <= 676 else "next_printed_CLV_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07i",
        "source": ("William Lilly Christian Astrology first edition 1647 Wellcome b30338724"),
        "original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [675, 676],
        "following_printed_CLV_heading_frame": 676,
        "images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07i",
        "source_groups": mapping,
        "source_group_count": 6,
        "record_count": 64,
        "substantive": 62,
        "following_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07i",
        "issues": [
            (
                "Printed CLIIII source starts mid original PDF675/printed641 "
                "following CLIII on enemy quality, and ends original "
                "PDF676/printed642 upper before distinct printed CLV "
                "on captivity and imprisonment. Keep these separate."
            ),
            (
                "The historical question 'overcome or be overcome by "
                "enemies' is NOT an accurate personal safety or "
                "legal forecast, and should not invite suspicion "
                "toward actual friends or partners."
            ),
            (
                "Original alternatives include seventh/tenth or "
                "twelfth/tenth lord reciprocal placements, versus "
                "retrograde and debilitated twelfth lord in sixth."
            ),
            (
                "The selected luminary depends on daytime/nighttime "
                "birth and Mars's essential dignities or house "
                "reception, explicitly excluding eighth-house case."
            ),
            (
                "Strong Saturn AND Mars in twelfth allegedly "
                "predict others' death; weak planets reverse this "
                "and add physical disability. Real mortality "
                "and disability outcomes have zero validation."
            ),
            (
                "One malefic in twelfth and another in sixth yields "
                "three completely different alleged outcomes: "
                "death at others' hands, lifelong sickness or "
                "imprisonment. Do not treat any one as a "
                "correct unique hit without predeclared rules."
            ),
            (
                "Jupiter OR Venus as lord twelfth allegedly "
                "indicate escape from harms, NOT that the "
                "person has no enemies."
            ),
            (
                "Gemini, Sagittarius or Aquarius Ascendant is "
                "alleged to stir conflict; a malefic twelfth "
                "with Leo/Sagittarius twelfth alleges a "
                "fatal horse fall. Never issue actual-world "
                "moral or transport safety judgments."
            ),
            (
                "Internal section 'Whose Friendship the Native must "
                "avoyd' makes old warnings about someone else's "
                "Ascendant lord, the South Node, fixed stars and "
                "two chart disagreements. These are SOURCE warnings "
                "and not recommendations for actual relationships."
            ),
            (
                "The period source adds one party's luminary "
                "square or opposite a planet of another natal "
                "chart and proposes eternal enmity, with a "
                "final unweighted count of victory indicators. "
                "This requires TWO independent source charts."
            ),
            (
                "The next printed CLV concerns captivity and "
                "prison legal/safety claims, separate from CLIIII; "
                "do not import its original rules at this seam."
            ),
            (
                "No prospective real adversity outcome, police or "
                "court record, accident/illness baseline, verified "
                "birth chart, matched null or blinded independent "
                "human testing has been performed."
            ),
            (
                "Source glyphs/nodal star positions and ordinal "
                "strength scores remain incompletely collated. "
                "Packet is photo-anchored paraphrase, not "
                "a complete diplomatic original edition."
            ),
        ],
        "original_glyphs_fully_verified": False,
        "adversary_victory_decision_rule_executable": False,
        "any_real_person_enemy_or_safety_prediction_validated": False,
        "actual_person_risk_or_moral_inference_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07i",
        "status": "ORIGINAL_1647_CLIIII_ADVERSARY_CONFLICT_HIGH_STAKES_HISTORICAL_ONLY",
        "printed_chapter": "CLIIII",
        "record_count": 64,
        "first_record": "R10083",
        "last_record": "R10146",
        "substantive": 62,
        "following_navigation": 2,
        "source_groups": 6,
        "body_original_pdf_frames": [675, 676],
        "next_printed": "CLV",
        "following_heading_pdf": 676,
        "empirical_validations": 0,
        "real_person_adversary_or_safety_accuracy": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07i",
        "status": "FIRST_EDITION_CLIIII_ADVERSARY_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 10082,
        "new_historical_annotations": 64,
        "lilly_if_published": 10146,
        "ptolemy_retained": 1066,
        "combined_if_published": 11212,
        "substantive": 62,
        "navigation": 2,
        "source_groups": 6,
        "numbered_chapters_added": 1,
        "next_printed": "CLV",
        "next_original_pdf": 676,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "real_adversary_outcomes_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B07i CLIIII original source frozen: 64 records R10083–R10146")
