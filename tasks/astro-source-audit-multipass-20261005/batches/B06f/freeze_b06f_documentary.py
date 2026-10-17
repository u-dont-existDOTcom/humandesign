#!/usr/bin/env python3
"""Archive original Lilly 1647 curability as historical, not treatment prediction."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


author = j("SOURCE_FIRST_AUTHORING_20261017.json")
assert author["batch"] == "B06f"
assert author["printed_chapter"] == "CXXIX"
assert author["original_body_pdf_frames"] == [619, 620]
assert len(author["groups"]) == 6
rules, map_source = [], []
for i, group in enumerate(author["groups"], 1):
    span = f"B06f-S{i:03d}"
    assert group["source_span"] == span
    assert set(group["original_pdf_frames"]) <= {619, 620}
    ids = []
    for claim in group["claims"]:
        no = 7809 + len(rules)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["source_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_only_meaning"]) >= 40
        assert not claim["independent_human_clinical_accuracy_validated"]
        assert not claim["runtime_promoted"]
        rules.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": span,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "anchor_not_diplomatic": claim["source_anchor_not_diplomatic"],
                "meaning_historical_only": claim["historical_only_meaning"],
                "qualification": claim["qualification"],
                "historical_documentary_accepted": True,
                "independent_disease_recovery_forecast_validated": False,
                "real_patient_diagnosis_or_prognosis_validated": False,
                "medicine_or_magic_treatment_authorized": False,
                "runtime_rule_promoted": False,
            }
        )
        ids.append(rid)
    map_source.append(
        {
            "source_span": span,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["source_group"],
            "mapped_record_ids": ids,
        }
    )
assert len(rules) == 27
assert [r["record_number"] for r in rules] == list(range(7809, 7836))
assert [r["id"] for r in rules if r["role"] == "next_chapter_navigation"] == ["R7834", "R7835"]

images = {}
for n in (619, 620, 621):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "role": "curability_body" if n <= 620 else "following_servants_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06f",
        "source": "William Lilly Christian Astrology original 1647 Wellcome b30338724",
        "complete_original_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": [619, 620],
        "following_CXXX_heading_pdf": 620,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06f",
        "source_groups": map_source,
        "source_group_count": 6,
        "record_count": 27,
        "substantive_historical_clauses": 25,
        "following_chapter_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06f",
        "issues": [
            (
                "An astrologically alleged incurable or long-lasting "
                "disease is NOT an evidence-based prognosis, and "
                "the source cannot inform any treatment decision."
            ),
            (
                "Benevolent sextile/trine to disease signifiers "
                "plus moveable signs is a compound historical "
                "criterion, not independent observed patient recovery."
            ),
            (
                "Fixed signs with absence of benefic support form "
                "the contrary branch, permitting long illness or "
                "near-incurability without operationalized thresholds."
            ),
            (
                "Near and partile aspects are used to grade "
                "speed/ease of cure, but no time units, angular "
                "orb tolerances or real clinical results are supplied."
            ),
            (
                "Lilly assigns Jupiter money/counsel, Mercury medicine, "
                "Venus magic/divine/chance aid: these are untested "
                "premodern classifications, not care options."
            ),
            (
                "The source's positive cure claims also require "
                "well-fortified helping planets and beneficial "
                "sextile or trine to disease significators."
            ),
            (
                "The claimed opposite rule for disease signifiers "
                "in their own domicile or exaltation offers very "
                "little hope of remedy, potentially contradicting "
                "earlier favorable testimonies."
            ),
            (
                "No real disease diagnoses, persons, recovery "
                "outcomes, medical controls, chart timing evidence, "
                "or independently observed failures were included."
            ),
            (
                "Printed CXXIX ends upper original PDF620; "
                "following printed CXXX on servants and small "
                "cattle begins on same page and is separate."
            ),
            (
                "Only selectively anchored historical paraphrases "
                "and original images are preserved, not a full "
                "diplomatic transcription or empirical medical proof."
            ),
        ],
        "human_clinical_utility_validated": False,
        "medical_or_treatment_advice_authorized": False,
        "independently_validated_disease_prognoses": 0,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06f",
        "status": "FIRST_EDITION_MEDICAL_CURABILITY_HISTORY_ONLY",
        "printed_chapter": "CXXIX",
        "editorial_chapter": "CXXX",
        "record_count": 27,
        "first_record": "R7809",
        "last_record": "R7835",
        "source_groups": 6,
        "substantive_historical_clauses": 25,
        "following_numbered_navigation": 2,
        "original_body_frames": [619, 620],
        "next_heading_frame": 620,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "human_prognosis_outcomes_validated": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06f",
        "status": "FIRST_EDITION_CURABILITY_DOCUMENTARY_LOCALLY_FROZEN_PENDING_REMOTE",
        "previous_lilly": 7808,
        "new_source_annotations": 27,
        "lilly_if_published": 7835,
        "ptolemy_retained": 1066,
        "combined_if_published": 8901,
        "substantive": 25,
        "navigation": 2,
        "source_groups": 6,
        "next_original_pdf": 620,
        "next_printed_chapter": "CXXX",
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "medical_recovery_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06f first-edition historical curability R7809–R7835, zero clinical validation")
