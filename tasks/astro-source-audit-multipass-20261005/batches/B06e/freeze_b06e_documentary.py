#!/usr/bin/env python3
"""Lilly original CXXVIII eye/speech/neurologic source, historical only."""

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
boundary = j("ORIGINAL_NUMBERED_CHAPTER_BOUNDARY_20261017.json")
assert a["batch"] == boundary["batch"] == "B06e"
assert a["printed_chapter"] == boundary["printed_chapter"] == "CXXVIII"
assert a["original_body_pdf_frames"] == list(range(615, 620))
assert boundary["following_heading_pdf_frame"] == 619
assert len(a["source_groups"]) == 11
records, reverse = [], []
for index, group in enumerate(a["source_groups"], 1):
    sid = f"B06e-S{index:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= set(range(615, 621))
    ids = []
    for claim in group["claims"]:
        number = 7696 + len(records)
        rid = f"R{number}"
        assert claim["id"] == rid
        assert len(claim["original_anchor_not_diplomatic"]) >= 6
        assert len(claim["meaning_historical_only"]) >= 40
        assert not claim["independent_human_medical_outcome_validated"]
        assert not claim["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": number,
                "batch": "B06e",
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "original_anchor_not_diplomatic": claim["original_anchor_not_diplomatic"],
                "meaning_historical_only": claim["meaning_historical_only"],
                "source_qualification": claim["qualification"],
                "historical_documentary_accepted": True,
                "independent_human_medical_result_validated": False,
                "modern_ophthalmic_neurological_diagnosis_validated": False,
                "reliable_falls_disability_or_lifespan_prediction": False,
                "person_level_moral_or_psychiatric_label_authorized": False,
                "clinical_or_medical_treatment_advice_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["group"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 113
assert [r["record_number"] for r in records] == list(range(7696, 7809))
assert [r["id"] for r in records if r["role"] == "next_chapter_navigation"] == ["R7807", "R7808"]
assert len({r["id"] for r in records}) == 113

images = {}
for n in range(615, 628):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    data = p.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 150000
    images[str(n)] = {
        "file": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(data),
        "printed_folio": str(n - 34),
        "role": (
            "eye_subsections_chapter_CXXVIII"
            if n <= 619
            else "following_separately_numbered_chapters_context_only"
        ),
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06e",
        "original_source": "William Lilly Christian Astrology 1647 Wellcome b30338724",
        "original_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": list(range(615, 620)),
        "next_printed_CHAP_CXXIX_heading_pdf": 619,
        "following_CHAP_CXXX_heading_pdf": 620,
        "images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06e",
        "source_groups": reverse,
        "source_group_count": 11,
        "record_count": 113,
        "substantive_source_clauses": 111,
        "following_numbered_navigation": 2,
        "main_named_topics": a["historical_topics"],
        "distinct_numbered_chapters_covered": 1,
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06e",
        "issues": [
            (
                "All original 1647 claims about eyesight, hearing, "
                "speech, teeth, seizures, psychiatric labels, "
                "urinary stones, gout and violent falls are unsupported "
                "period medical hypotheses, never clinical evidence."
            ),
            (
                "Several short original author-claimed rules say a "
                "person 'shall be blind', 'deaf' or epileptic; none "
                "can inform real-person diagnosis, safety or treatment."
            ),
            (
                "No actual patients, verified birth-time sources, "
                "medical records, appropriate comparison controls or "
                "longitudinal events are presented by the author."
            ),
            (
                "Named zodiac ranges for Milky Way, Pleiades, "
                "Praesepe, Coma Berenices, Cor Scorpio, "
                "Orion and cloudy fixed stars require historically "
                "correct star identities and epoch coordinates."
            ),
            (
                "Several planetary/zodiac glyphs, conjunction and "
                "opposition operators in the eye and neurological "
                "paragraphs remain unresolved pending diplomatic "
                "first-edition transcription and mathematical review."
            ),
            (
                "Sun-right/Moon-left eye laterality reflects "
                "period interpretation, not clinically validated "
                "human visual anatomy."
            ),
            (
                "The author's suggested cause of eye injury by "
                "Saturn catarrh or Mars trauma is speculative "
                "astrological attribution, not actual etiology."
            ),
            (
                "The eye section includes total blindness, "
                "one-eye injury and squint, and contradictory "
                "conditions with and without angular malefics."
            ),
            (
                "The hearing section offers several sixth, "
                "eighth, tenth, Ascendant, Saturn/Mercury alternatives "
                "and explicitly allows benefic mitigation. No "
                "validated diagnosis or outcome matching exists."
            ),
            (
                "The speech section treats stammering, muteness "
                "and disability through compound Mercury/mute-sign "
                "conditions; no clinical neurodevelopmental "
                "association is demonstrated."
            ),
            (
                "Dental pain, loss and alleged elemental causes "
                "are separate outcomes with contrary air/earth/fire "
                "branches; no real dental chart histories supplied."
            ),
            (
                "Falling-sickness, epilepsy, seizure, madness, "
                "foolery and intellectual disability are conflated "
                "under premodern stigmatizing categories. "
                "Do not use them as modern psychiatric "
                "or neurologic diagnoses."
            ),
            (
                "The four supposedly epileptic causes are "
                "attributed to Albubater, Cardanus and Pontanus, "
                "not validated external clinical findings."
            ),
            (
                "The four-sect combinations of Moon/Mercury/"
                "Saturn/Mars have ambiguous grammatical "
                "conjunction scope and sign labels."
            ),
            (
                "Stone/strangury and gout combinations are "
                "compound physical disease claims with many "
                "alternative planet, house, aspect and sign outcomes."
            ),
            (
                "Gout is claimed to follow youth sickness "
                "at unspecified later ages; no objective "
                "age interval, severity or case count."
            ),
            (
                "Violent fall predictions invoke fixed stars, "
                "horses or beasts and house-specific malefics, "
                "and Lilly cites his own unverifiable experiences."
            ),
            (
                "The subheadings for ears, tongue, tooth, "
                "falling sickness, stone, gout and falls "
                "are all within printed CXXVIII; they do not "
                "increment numbered-chapter coverage."
            ),
            (
                "Printed CHAP CXXIX on whether disease "
                "is curable begins lower original PDF619; "
                "printed CXXX on servants and small cattle "
                "begins original PDF620 and neither is "
                "substantive source accepted here."
            ),
            (
                "This corpus is an anchored selective "
                "semantic documentary extraction, not "
                "full diplomatic transcription or proof "
                "of predictive astrological performance."
            ),
        ],
        "independent_medical_validation_successes": 0,
        "clinical_medical_advice_authorized": False,
        "actual_person_psychological_labels_authorized": False,
        "runtime_promotions": 0,
    },
)
write(
    "RULES.json",
    {
        "batch": "B06e",
        "status": "FIRST_EDITION_CXXVIII_MEDICAL_HISTORY_ONLY_LOCALLY_FROZEN",
        "printed_chapter": "CXXVIII",
        "editorial_chapter": "CXXIX",
        "record_count": 113,
        "first_record": "R7696",
        "last_record": "R7808",
        "substantive_historical_conditions": 111,
        "next_numbered_navigation": 2,
        "source_groups": 11,
        "body_original_pdf_frames": [615, 616, 617, 618, 619],
        "next_printed_CXXIX_heading_pdf": 619,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "independent_medical_or_psychiatric_accuracy": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
write(
    "ACCEPTANCE.json",
    {
        "batch": "B06e",
        "status": "FIRST_EDITION_CXXVIII_SOURCE_LOCALLY_FROZEN_PENDING_GITHUB",
        "previous_lilly": 7695,
        "new_historical_annotations": 113,
        "lilly_if_published": 7808,
        "ptolemy_retained": 1066,
        "combined_if_published": 8874,
        "substantive": 111,
        "navigation": 2,
        "source_groups": 11,
        "next_printed_chapter": "CXXIX",
        "next_original_pdf": 619,
        "rules_sha256": sha(B / "RULES.json"),
        "boundary_sha256": sha(B / "ORIGINAL_NUMBERED_CHAPTER_BOUNDARY_20261017.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "actual_human_medical_results_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06e historic first edition R7696–R7808 113 records, medical zero")
