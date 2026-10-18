#!/usr/bin/env python3
"""Original William Lilly CXL travel causes and Haly aphorisms — source only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, value):
    (B / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261018.json")
assert a["batch"] == "B06t"
assert a["printed_chapter"] == "CXL"
assert a["original_body_pdf_frames"] == [643, 644]
assert a["next_printed"] == "CXLI"
assert a["next_heading_pdf"] == 644
assert len(a["groups"]) == 6

records, reverse = [], []
for group_number, g in enumerate(a["groups"], 1):
    sid = f"B06t-S{group_number:03d}"
    assert g["source_span"] == sid
    assert set(g["original_pdf_frames"]) <= {643, 644}
    ids = []
    for c in g["claims"]:
        number = 8807 + len(records)
        rid = f"R{number}"
        assert c["id"] == rid
        assert len(c["source_anchor_not_diplomatic"]) >= 5
        assert len(c["historical_meaning_only"]) >= 40
        assert not c["independent_human_travel_outcome_validated"]
        assert not c["person_level_inference_authorized"]
        assert not c["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": number,
                "batch": "B06t",
                "source_span": sid,
                "original_pdf_frames": g["original_pdf_frames"],
                "role": c["role"],
                "source_anchor_not_diplomatic": c["source_anchor_not_diplomatic"],
                "historical_meaning_only": c["historical_meaning_only"],
                "qualification": c["qualification"],
                "documentary_source_accepted": True,
                "independent_person_travel_causes_validated": False,
                "independent_trade_or_law_motive_validated": False,
                "independent_people_or_estate_event_validated": False,
                "independent_animal_or_parent_illness_validated": False,
                "independent_travel_death_validated": False,
                "historical_haly_original_independently_verified": False,
                "private_religious_moral_health_inference_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": g["original_pdf_frames"],
            "source_group": g["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 53
assert [x["record_number"] for x in records] == list(range(8807, 8860))
assert [x["id"] for x in records if x["role"] == "next_chapter_navigation"] == ["R8858", "R8859"]
assert len({x["id"] for x in records}) == 53

images = {}
for n in [643, 644, 645, 646]:
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(p),
        "printed_folio": str(n - 34),
        "role": (
            "causes_of_travel_and_haly_body"
            if n <= 644
            else "following_success_and_religion_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06t",
        "source": (
            "William Lilly Christian Astrology original 1647 first edition Wellcome b30338724"
        ),
        "volume_sha256": ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"),
        "body_pdf_frames": [643, 644],
        "following_printed_CXLI_heading_pdf": 644,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06t",
        "source_groups": reverse,
        "source_group_count": 6,
        "records_count": 53,
        "substantive": 51,
        "following_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06t",
        "issues": [
            (
                "Planetary nature and planetary house occupancy "
                "are separately considered for a travel cause; "
                "the author does not give calibrated weights or "
                "a deterministic selection among competing motives."
            ),
            (
                "Saturn-related claims have three alternative "
                "preconditions: travel significator conjoined "
                "Saturn, occupying Saturn's essential dignity, "
                "or Saturn acting directly as significator."
            ),
            (
                "Searching for mines, recovery of inheritance, "
                "transactions in Saturnine commodities, "
                "meetings with older men and merchants are "
                "separate proposed causes, not equivalent "
                "observations of a successful prediction."
            ),
            (
                "Jupiter-like causes include religion, "
                "honour, law, ecclesiastical preferment "
                "and meetings with associated people; "
                "these are historical institutional roles, "
                "not facts about anyone's faith or politics."
            ),
            (
                "The text references other planetary "
                "topics from Lilly's second-house doctrine "
                "rather than specifying all those alternative "
                "planetary classes in this travel chapter."
            ),
            (
                "First-house travel significator suggests "
                "curiosity; second suggests trade and potential "
                "wealth. Intentions, actual journeys, business "
                "transactions and financial results are "
                "different measurable target variables."
            ),
            (
                "The author attributes a house-by-house "
                "series of aphorisms to HALY, but Haly's "
                "original manuscript and identity/translation "
                "have not been independently collated."
            ),
            (
                "Haly ninth-ruler in first through eighth "
                "house claims are different alleged outcomes; "
                "the excerpt STOPS at eighth, so do not "
                "invent ninth-to-twelfth corresponding rules."
            ),
            (
                "Several Haly branches permit harmful "
                "or high-stakes outcomes including hidden "
                "parental illness and death while traveling. "
                "They have no valid clinical or safety use."
            ),
            (
                "Historically the sixth-house branch alleges "
                "gain through enslaved people/servants and "
                "illness of cattle, which are period economic "
                "and veterinary claims, not modern advice."
            ),
            (
                "Third and seventh Haly aphorisms use "
                "period sexual/gender stereotypes involving "
                "women and wifely obedience; no actual "
                "individual intimate, moral or suitability "
                "inference is authorized."
            ),
            (
                "No source outcome has a fixed forecast "
                "window, unambiguous motivation category, "
                "objective socioeconomic baseline, confirmed "
                "journey or biographical denominator."
            ),
            (
                "The NEXT numbered CHAP CXLI success in "
                "travels begins after horizontal divider "
                "mid PDF644. Its favorable benefic, "
                "dangers and fatal outcomes MUST NOT "
                "be admitted with current causes chapter."
            ),
            (
                "This source packet is anchored historical "
                "paraphrase, not a complete diplomatic "
                "glyph-by-glyph original first edition."
            ),
        ],
        "haly_original_text_crosscollated": False,
        "complete_travel_motive_scoring_engine": False,
        "parental_illness_mortality_predictions_validated": 0,
        "human_travel_motivation_predictions_validated": 0,
        "real_person_motive_faith_health_or_intimate_inference_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06t",
        "status": "ORIGINAL_1647_CXL_TRAVEL_CAUSES_HALY_SOURCE_ONLY",
        "printed_chapter": "CXL",
        "editorial_chapter": "CXLI",
        "record_count": 53,
        "first_record": "R8807",
        "last_record": "R8859",
        "substantive": 51,
        "following_navigation": 2,
        "source_groups": 6,
        "body_original_pdf_frames": [643, 644],
        "next_printed_chapter": "CXLI",
        "following_heading_original_pdf": 644,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "real_human_travel_motives_and_dangers_validated": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06t",
        "status": "ORIGINAL_TRAVEL_CAUSE_HALY_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 8806,
        "new_historical_annotations": 53,
        "lilly_if_published": 8859,
        "ptolemy_retained": 1066,
        "combined_if_published": 9925,
        "substantive": 51,
        "navigation": 2,
        "source_groups": 6,
        "numbered_chapters_added": 1,
        "next_printed_chapter": "CXLI",
        "next_original_pdf": 644,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "human_travel_motive_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original CXL Causes of Travels: 53 historic records R8807–R8859")
