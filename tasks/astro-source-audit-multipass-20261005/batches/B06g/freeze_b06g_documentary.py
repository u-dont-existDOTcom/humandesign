#!/usr/bin/env python3
"""Archive original Lilly 1647 servant/cattle stereotypes as historical source only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def load(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, data):
    (B / name).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = load("SOURCE_FIRST_AUTHORING_20261017.json")
assert a["batch"] == "B06g"
assert a["printed_chapter"] == "CXXX"
assert a["body_original_pdf_frame"] == 620
assert len(a["groups"]) == 8
rows, reverse = [], []
for group_number, group in enumerate(a["groups"], 1):
    sid = f"B06g-S{group_number:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {620, 621}
    refs = []
    for claim in group["clauses"]:
        no = 7836 + len(rows)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["anchor_not_diplomatic"]) >= 7
        assert len(claim["historical_meaning"]) >= 48
        assert not claim["real_human_worker_reliability_validated"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "original_anchor_not_diplomatic": claim["anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_meaning"],
                "qualification": claim["source_qualification"],
                "historical_documentary_accepted": True,
                "independent_human_worker_ethics_accuracy_validated": False,
                "worker_criminality_or_dishonesty_allegation_authorized": False,
                "actual_livestock_economic_outcome_validated": False,
                "employment_or_financial_advice_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        refs.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": refs,
        }
    )
assert len(rows) == 42
assert [r["record_number"] for r in rows] == list(range(7836, 7878))
assert [r["id"] for r in rows if r["role"] == "next_section_navigation"] == ["R7876", "R7877"]
images = {}
for n in range(620, 628):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    data = p.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 150000
    images[str(n)] = {
        "path": str(p.relative_to(B)),
        "bytes": len(data),
        "sha256": sha(p),
        "printed_folio": str(n - 34),
        "source_role": ("servants_cattle_body" if n == 620 else "following_seventh_house_context"),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06g",
        "source": "William Lilly Christian Astrology original 1647 Wellcome b30338724",
        "original_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frame": 620,
        "unnumbered_seventh_house_start_pdf_frame": 621,
        "end_of_original_pdf_620_handover_word": "The",
        "following_pdf_621_heading": "The seventh House, and the Judgments appertaining unto it",
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06g",
        "source_groups": reverse,
        "source_group_count": 8,
        "record_count": 42,
        "substantive_source_annotations": 40,
        "following_unnumbered_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06g",
        "issues": [
            (
                "The original servant dishonesty and theft allegations are "
                "unsupported 1647 social stereotypes, NOT evidence of "
                "worker crime, loyalty, morality or occupational suitability."
            ),
            (
                "Servant and small-cattle predictions use similar sixth-house "
                "indicators but are different social and economic outcomes; "
                "they cannot be pooled as separate successes."
            ),
            (
                "Strong or benefic majority is a source qualifier "
                "without a calibrated number-of-servants threshold "
                "or independent household employment observations."
            ),
            (
                "Malefic essential dignity plus favorable aspect "
                "to Ascendant ruler is an explicit positive exception "
                "to the stereotype of intrinsically malefic planets."
            ),
            (
                "The sixth lord in tenth is alleged to promote servants, "
                "a different outcome from number or financial profit."
            ),
            (
                "The original applied-to glyph after Mercury's "
                "favorable tenth/first/sixth/twelfth house placement "
                "is not sufficiently verified to name the planet."
            ),
            (
                "Mercury retrograde OR combust and applying to malefics "
                "in fixed signs is a compound branch; not a valid "
                "character inference about human workers."
            ),
            (
                "The last branch groups Saturn peregrine, "
                "South Node or Mars in airy/fiery signs in sixth "
                "as alleged source of bad servants or zero profit."
            ),
            (
                "Period assumptions concerning servants, masters "
                "and cattle trade are not modern employment "
                "ethics, animal health or financial advice."
            ),
            (
                "No chart birth-time verification, workers, "
                "theft adjudications, payroll records, animal "
                "profit data, cohort, or negative cases are provided."
            ),
            (
                "The word 'The' at original PDF620 page bottom "
                "belongs to following unnumbered seventh-house "
                "intro whose separate heading starts PDF621."
            ),
            (
                "No complete diplomatic transcription or "
                "independent historical paleography is claimed; "
                "source JPEGs and qualified anchors are retained."
            ),
        ],
        "actual_human_worker_accuracy": 0,
        "criminality_classification_authorized": False,
        "animal_health_or_financial_advice_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06g",
        "status": "ORIGINAL_1647_SERVANT_CATTLE_HISTORICAL_ONLY_LOCAL_SOURCE",
        "printed_chapter": "CXXX",
        "editorial_chapter": "CXXXI",
        "record_count": 42,
        "first_record": "R7836",
        "last_record": "R7877",
        "substantive_source_annotations": 40,
        "following_unnumbered_navigation": 2,
        "source_groups": 8,
        "original_body_pdf_frame": 620,
        "following_unnumbered_pdf_frame": 621,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "real_workers_or_cattle_outcomes_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06g",
        "status": "ORIGINAL_FIRST_EDITION_DOCUMENTARY_LOCALLY_FROZEN",
        "prior_lilly": 7835,
        "new_historical_annotations": 42,
        "lilly_if_published": 7877,
        "ptolemy_retained": 1066,
        "combined_if_published": 8943,
        "substantive": 40,
        "navigation": 2,
        "source_groups": 8,
        "next_source": "UNNUMBERED_SEVENTH_HOUSE_MARRIAGE",
        "next_original_pdf_frame": 621,
        "numbered_chapters_added": 1,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "real_worker_or_livestock_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06g original printed CXXX servants R7836-R7877; 42 historical annotations")
