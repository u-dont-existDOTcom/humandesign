#!/usr/bin/env python3
"""Original Lilly CXLII theological and sectarian material: source records only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, obj):
    (B / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261018.json")
guard = j("RELIGION_SOURCE_CAUSAL_SCOPE_V1.json")
assert a["batch"] == "B06v"
assert a["printed_chapter"] == "CXLII"
assert a["body_pdf_frames"] == [645, 646, 647]
assert a["next_printed"] == "CXLIII"
assert a["next_heading_frame"] == 647
assert len(a["groups"]) == 7
assert guard["strict_source_scope"]["denies_stars_enforce_faith"]
assert guard["strict_source_scope"]["denies_stars_cause_religion_or_irreligion"]
assert guard["human_validation_count"] == guard["runtime_rules_promoted"] == 0

rows, mapped = [], []
for idx, g in enumerate(a["groups"], 1):
    sid = f"B06v-S{idx:03d}"
    assert g["source_span"] == sid
    assert set(g["original_pdf_frames"]) <= {645, 646, 647}
    ids = []
    for c in g["claims"]:
        number = 8936 + len(rows)
        rid = f"R{number}"
        assert c["id"] == rid
        assert len(c["original_anchor_not_diplomatic"]) >= 5
        assert len(c["historical_meaning_only"]) >= 42
        assert not c["individual_religion_prediction_validated"]
        assert not c["real_person_faith_character_classification_authorized"]
        assert not c["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": number,
                "batch": "B06v",
                "source_span": sid,
                "original_pdf_frames": g["original_pdf_frames"],
                "role": c["role"],
                "original_anchor_not_diplomatic": c["original_anchor_not_diplomatic"],
                "historical_meaning_only": c["historical_meaning_only"],
                "source_qualification": c["qualification"],
                "original_source_documented": True,
                "independent_real_faith_affiliation_accuracy_validated": False,
                "independent_real_conversion_stability_validated": False,
                "independent_charity_or_moral_validity_established": False,
                "real_person_sectarian_label_authorized": False,
                "real_person_prophecy_or_divination_claim_authorized": False,
                "celestial_causal_religion_mechanism_verified": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    mapped.append(
        {
            "source_span": sid,
            "original_pdf_frames": g["original_pdf_frames"],
            "source_group": g["source_group"],
            "mapped_record_ids": ids,
        }
    )
assert len(rows) == 104
assert [r["record_number"] for r in rows] == list(range(8936, 9040))
assert [r["id"] for r in rows if r["role"] == "next_chapter_navigation"] == ["R9038", "R9039"]
assert len({r["id"] for r in rows}) == 104

pics = {}
for frame in [645, 646, 647, 648, 649]:
    path = B / "evidence" / f"pdf_1647-{frame}.jpg"
    raw = path.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    pics[str(frame)] = {
        "file": str(path.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(path),
        "printed_folio": str(frame - 34),
        "source_role": (
            "religion_cxlii_body" if frame <= 647 else "following_dream_chapter_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06v",
        "source": (
            "William Lilly Christian Astrology original 1647 first edition Wellcome b30338724"
        ),
        "original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": [645, 646, 647],
        "next_printed_CXLIII_heading_frame": 647,
        "images": pics,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06v",
        "source_groups": mapped,
        "source_group_count": 7,
        "source_records": 104,
        "substantive": 102,
        "following_navigation": 2,
        "causal_scope_file": "RELIGION_SOURCE_CAUSAL_SCOPE_V1.json",
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06v",
        "issues": [
            (
                "Lilly expressly DENIES stars force or CAUSE religious "
                "affiliation, religious practice or lack of religion. "
                "He attributes piety to divine grace and separately "
                "claims only natural inclination/persistence "
                "are allegedly decipherable by celestial arrangements."
            ),
            (
                "The theology of divine grace and moral good/ill is "
                "author's 1647 Christian worldview, not an "
                "independently demonstrated causal mechanism."
            ),
            (
                "Labels good Christian, sectary, heresy, impiety, "
                "atheism, blasphemy, prophecy and divination "
                "reflect a seventeenth-century normative "
                "classification and are not universal "
                "psychological or human virtue measures."
            ),
            (
                "No actual person may be classified as "
                "religious, heretical, atheist, immoral or "
                "spiritually endowed using these source records."
            ),
            (
                "Saturn in its own essential dignities in ninth "
                "is positively linked to charity and faith "
                "despite negative Saturn ninth stereotype "
                "earlier in the same chapter; preserve both "
                "with their qualifiers, never choose afterward."
            ),
            (
                "Saturn or Mars direct in ninth/third, "
                "receiving benefic aspects from planets "
                "in fixed signs, may be called pious "
                "even though the same malefics are "
                "ascribed negative labels elsewhere."
            ),
            (
                "Unnumbered piety and impiety aphorisms "
                "are BOTH substantive parts of printed "
                "CHAP CXLII, not separate numbered chapters."
            ),
            (
                "Several 1647 glyphs in Jupiter/Venus/"
                "North/South Node, Spica Virgo, Part Fortune, "
                "Cazimi, Moon and Lord Ascendant relations "
                "are not all professionally collated."
            ),
            (
                "Even if all original horoscope operators "
                "were identified, no birth-verified cohort, "
                "actual religious-history labels, practice "
                "measure, controlled prospective conversion "
                "test or nonastrological baseline is present."
            ),
            (
                "Religion membership, adherence to childhood "
                "faith, moral rhetoric, charity, social "
                "recognition, change of conviction, "
                "interest in divination, prophetic "
                "ability and stable values are distinct "
                "human constructs without a single score."
            ),
            (
                "The original author marks moderate or "
                "mixed testimonials from Sun/Moon/Mercury/"
                "Part Fortune, and several cases require "
                "essential dignity, reception, angularity "
                "and benefic versus malefic aspects."
            ),
            (
                "The next separately printed CHAP CXLIII "
                "on DREAMS begins after divider later "
                "original PDF647/printed613 and is "
                "not included in this religion source."
            ),
            (
                "This packet preserves short historic "
                "anchors and qualified paraphrases "
                "but is NOT complete diplomatic "
                "seventeenth-century transcription."
            ),
        ],
        "religion_caused_by_stars_according_to_original": False,
        "all_original_astrological_glyphs_collated": False,
        "personal_religion_or_morality_inferences_authorized": False,
        "independently_validated_real_religion_predictions": 0,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06v",
        "status": "ORIGINAL_1647_RELIGION_SOURCE_DENIES_CELESTIAL_CAUSATION",
        "printed_chapter": "CXLII",
        "editorial_chapter": "CXLIII",
        "record_count": 104,
        "first_record": "R8936",
        "last_record": "R9039",
        "substantive": 102,
        "following_navigation": 2,
        "source_groups": 7,
        "original_body_pdf_frames": [645, 646, 647],
        "next_printed_chapter": "CXLIII",
        "following_heading_pdf_frame": 647,
        "causal_guard_reference": "RELIGION_SOURCE_CAUSAL_SCOPE_V1.json",
        "original_author_denies_stars_cause_religion": True,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "actual_human_religion_character_accuracy_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06v",
        "status": "FIRST_EDITION_ORIGINAL_RELIGION_DOCUMENTARY_LOCALLY_FROZEN",
        "prior_lilly": 8935,
        "new_historical_annotations": 104,
        "lilly_if_published": 9039,
        "ptolemy_retained": 1066,
        "combined_if_published": 10105,
        "substantive": 102,
        "navigation": 2,
        "source_groups": 7,
        "numbered_chapters_added": 1,
        "next_printed_chapter": "CXLIII",
        "next_original_pdf": 647,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "causal_guard_sha256": sha(B / "RELIGION_SOURCE_CAUSAL_SCOPE_V1.json"),
        "empirical_validations": 0,
        "individual_religion_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original 1647 CXLII religion 104 historic clauses R8936–R9039; stars do not cause religion.")
