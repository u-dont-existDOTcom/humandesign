#!/usr/bin/env python3
"""Freeze Lilly's alleged wealth-acquisition conduct as historic text, never real ethics."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def write(name, obj):
    (B / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


author = j("SOURCE_FIRST_AUTHORING_20261017.json")
assert author["batch"] == "B05p"
assert author["printed_chapter"] == "CXVI"
assert author["editorial_chapter"] == "CXVII"
assert author["body_pdf_frames"] == [594, 595, 596]
assert len(author["groups"]) == 10
records, reverse = [], []
for group_no, group in enumerate(author["groups"], 1):
    sid = f"B05p-S{group_no:03d}"
    assert group["source_span"] == sid
    assert set(group["source_pdf_frames"]) <= {594, 595, 596}
    group_records = []
    for claim in group["clauses"]:
        no = 6995 + len(records)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["source_anchor_not_diplomatic"]) >= 7
        assert len(claim["meaning_historical_only"]) >= 55
        assert not claim["verified_actual_legality_of_person"]
        assert not claim["runtime_model_promoted"]
        record = {
            "id": rid,
            "record_number": no,
            "batch": "B05p",
            "source_span": sid,
            "original_pdf_pages": group["source_pdf_frames"],
            "printed_chapter": (
                "CXVI" if claim["role"] != "next_chapter_navigation" else "CXVII_NAVIGATION_ONLY"
            ),
            "editorial_chapter": (
                "CXVII" if claim["role"] != "next_chapter_navigation" else "CXVIII_NAVIGATION_ONLY"
            ),
            "role": claim["role"],
            "original_anchor_not_diplomatic": claim["source_anchor_not_diplomatic"],
            "historical_only_paraphrase": claim["meaning_historical_only"],
            "qualifier_class": claim["qualification"],
            "historical_documentary_accepted": True,
            "diplomatic_source_transcription": False,
            "independent_human_financial_accuracy_validated": False,
            "actual_criminal_or_ethical_classification_validated": False,
            "real_person_legal_allegation_authorized": False,
            "runtime_rule_promoted": False,
        }
        records.append(record)
        group_records.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "pdf_pages": group["source_pdf_frames"],
            "passage_group": group["group"],
            "mapped_record_ids": group_records,
        }
    )
assert len(records) == 57
assert [r["record_number"] for r in records] == list(range(6995, 7052))
assert len(reverse) == 10
assert [r["id"] for r in records if r["role"] == "next_chapter_navigation"] == ["R7050", "R7051"]
assert all(not r["real_person_legal_allegation_authorized"] for r in records)

images = {}
for n in range(594, 599):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 180000
    images[str(n)] = {
        "path": str(p.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(p),
        "printed_folio_verified": {594: "561", 595: "561", 596: "562"}.get(n),
        "source_role": "chapter_body" if n <= 596 else "later_context",
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05p",
        "source": "William Lilly first edition 1647, Wellcome b30338724",
        "full_original_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "source_body_original_frames": [594, 595, 596],
        "next_numbered_heading_frame": 596,
        "original_pagination_note": (
            "Source PDF594 and PDF595 both visibly print folio 561, "
            "followed by PDF596 printed562. Physical source order and "
            "body texts remain continuous; the duplicate is original."
        ),
        "images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05p",
        "groups": reverse,
        "source_group_count": 10,
        "record_count": 57,
        "substantive": 55,
        "following_navigation": 2,
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05p",
        "issues": [
            (
                "The source asserts lawful versus unlawful modes of gaining wealth "
                "from natal planetary status; this is not evidence of real human "
                "ethics, crimes or innocence and must never be used as a person-level "
                "accusation."
            ),
            (
                "Naturally benefic/malefic planetary labels are modified by sign "
                "dignity, aspects, combustion and retrograde motion; these cannot be "
                "simplified into inherent human moral character."
            ),
            (
                "Lilly's 'mixing according to discretion' and majority-of-testimonies "
                "rules lack frozen weights, tie handling, probability estimates, or a "
                "registered rejection criterion."
            ),
            (
                "Direct or lawful and indirect or unlawful methods are explicitly "
                "allowed to coexist in the same natal case; a forced single legal "
                "outcome would misrepresent this source."
            ),
            (
                "The phrase 'lawful versus unlawfull means' reflects early modern "
                "historical wording, not present-day criminal legislation or standards "
                "of proof."
            ),
            (
                "The worked Jupiter–Saturn case is hypothetical in the original and is "
                "not an independently verified case of theft or misconduct by "
                "relatives, servants or livestock traders."
            ),
            (
                "The phrase about the father's kindred, servants and small cattle is "
                "period house/planet taxonomy; no evidence about an actual absent "
                "family member is supplied."
            ),
            (
                "Direction to terms, square/opposition, converse/direct Fortune, "
                "Ascendant direction and revolution are alternative flexible "
                "event-time methods; any future test must fix them before results."
            ),
            (
                "The accepted time may be 'or near' the directional contact, with no "
                "specific tolerance; retrospective window choice would permit severe "
                "overfitting."
            ),
            (
                "Astrological Part of Fortune formula, house system, Saturn aspects, "
                "combustion and retrograde astronomy require reproducible calculation "
                "with documented exact source conventions."
            ),
            (
                "Benefic/malefic planets in contrary dignities and their combustion or "
                "retrogradation produce layered override rules; no original human "
                "validation isolates their separate effects."
            ),
            (
                "No independent records of legally proven means, income amounts, "
                "property transfers, person-level financial performance or court "
                "adjudication were inspected."
            ),
            (
                "The original source is preserved as images and selective clause-level "
                "paraphrases; no full diplomatic first-edition transcription or "
                "independent paleography is claimed."
            ),
            (
                "PDF594 and PDF595 printed folio561 is a source numbering anomaly, not "
                "two copies of the same page or cause to reorder."
            ),
            (
                "The next numbered CHAP CXVII on wealth durability starts in PDF596; "
                "its substantive wealth-continuation procedure is outside the current "
                "accepted source."
            ),
        ],
        "predictive_legality_or_financial_validations": 0,
        "person_level_moral_predictions_authorized": False,
        "runtime_promotions": 0,
    },
)
write(
    "RULES.json",
    {
        "batch": "B05p",
        "status": "ORIGINAL_1647_ETHICAL_ACQUISITION_HISTORICAL_ONLY_LOCALLY_ACCEPTED",
        "printed_chapter": "CXVI",
        "editorial_chapter": "CXVII",
        "record_count": 57,
        "first_record": "R6995",
        "last_record": "R7051",
        "source_group_count": 10,
        "substantive_historical_annotations": 55,
        "following_navigation_records": 2,
        "source_body_pdf_frames": [594, 595, 596],
        "following_chapter_start_pdf_frame": 596,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "verified_criminality_or_lawfulness_predictions": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
accepted = {
    "batch": "B05p",
    "status": "LOCALLY_VERIFIED_ORIGINAL_HISTORICAL_SOURCE_PENDING_GITHUB",
    "prior_lilly": 6994,
    "new_historical_annotations": 57,
    "lilly_if_published": 7051,
    "ptolemy_retained": 1066,
    "combined_if_published": 8117,
    "substantive": 55,
    "following_navigation": 2,
    "source_group_count": 10,
    "body_original_pdf_frames": [594, 595, 596],
    "following_printed_chapter": "CXVII",
    "following_editorial_chapter": "CXVIII",
    "next_pdf_frame": 596,
    "rules_sha256": sha(B / "RULES.json"),
    "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
    "empirical_validations": 0,
    "actual_ethical_or_criminal_outcomes_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
write("ACCEPTANCE.json", accepted)
print(json.dumps(accepted, indent=2))
