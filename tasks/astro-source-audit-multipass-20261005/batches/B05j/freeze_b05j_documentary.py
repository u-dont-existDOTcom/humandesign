#!/usr/bin/env python3
"""Freeze image-anchored 1647 Lilly sign/face/hair as historical assertions only."""

import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def load(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def save(name, obj):
    (BASE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


author = load("SOURCE_FIRST_AUTHORING_20261017.json")
window = load("SOURCE_WINDOW_20261017.json")
assert author["batch"] == window["batch"] == "B05j"
assert window["baseline_accepted_lilly"] == 6671
assert author["independent_validations"] == author["runtime_promotions"] == 0
assert len(author["source_groups"]) == 11
source_groups = []
records = []
for i, source in enumerate(author["source_groups"], start=1):
    sid = f"B05j-S{i:03d}"
    assert sid == source["source_span"]
    assert set(source["original_pdf_frames"]) <= {581, 582, 583}
    mapped = []
    for claim in source["claims"]:
        rid = f"R{6672 + len(records)}"
        assert claim["id"] == rid, (claim["id"], rid)
        assert len(claim["anchor_not_diplomatic"]) > 14
        assert len(claim["meaning_historical_only"]) > 50
        assert not claim["accepted_as_human_prediction"]
        assert claim["source_original_not_redistributed_as_legal_or_medical_finding"]
        record = {
            "id": rid,
            "record_number": 6672 + len(records),
            "batch": "B05j",
            "printed_chapter": (
                "CXI" if claim["role"] != "next_chapter_navigation" else "CXII_NAVIGATION_ONLY"
            ),
            "editorial_chapter": (
                "CXII" if claim["role"] != "next_chapter_navigation" else "CXIII_NAVIGATION_ONLY"
            ),
            "source_span": sid,
            "original_pdf_pages": source["original_pdf_frames"],
            "role": claim["role"],
            "anchor_not_diplomatic": claim["anchor_not_diplomatic"],
            "meaning_historical_only": claim["meaning_historical_only"],
            "qualification_class": claim["confidence_class"],
            "historical_documentary_accepted": True,
            "original_diplomatic_transcription": False,
            "independent_human_biometric_validation": False,
            "validated_ancestry_or_ethnicity_prediction": False,
            "validated_medical_or_disability_prediction": False,
            "runtime_model_promoted": False,
        }
        records.append(record)
        mapped.append(rid)
    source_groups.append(
        {
            "source_span": sid,
            "source_group": source["scope"],
            "original_pdf_pages": source["original_pdf_frames"],
            "mapped_record_ids": mapped,
        }
    )
assert len(records) == 62
assert [r["record_number"] for r in records] == list(range(6672, 6734))
assert sum(r["role"] == "next_chapter_navigation" for r in records) == 2
assert [r["role"] for r in records[-2:]] == ["next_chapter_navigation"] * 2
assert len({r["id"] for r in records}) == len(records)
assert len({s["source_span"] for s in source_groups}) == len(source_groups)
assert all(not r["independent_human_biometric_validation"] for r in records)
assert all(not r["validated_ancestry_or_ethnicity_prediction"] for r in records)
assert all(not r["validated_medical_or_disability_prediction"] for r in records)
assert all(not r["runtime_model_promoted"] for r in records)

# Verify the preserved six-image physical sequence but restrict this batch's
# substantive content to frames 581–583.
source_hashes = {}
for n in range(581, 587):
    page = window["original_scans"][str(n)]
    p = BASE / page["file"]
    raw = p.read_bytes()
    assert raw.startswith(bytes.fromhex("ffd8")) and len(raw) > 100000
    assert digest(p) == page["sha256"]
    assert len(raw) == page["bytes"]
    source_hashes[str(n)] = {
        "pdf_frame": n,
        "image_sha256": page["sha256"],
        "bytes": page["bytes"],
        "printed_folio": page["folio_as_seen"],
        "role": "body" if n in (581, 582, 583) else "later_chapter_context",
    }

save(
    "SOURCE_FIRST_REVERSE_MAP.json",
    {
        "batch": "B05j",
        "source_groups": source_groups,
        "source_group_count": 11,
        "bidirectional_mapping_claims": 62,
        "substantive_records": 60,
        "following_chapter_navigation": 2,
    },
)
save(
    "ORIGINAL_SOURCE_INTEGRITY.json",
    {
        "batch": "B05j",
        "original_1647_full_pdf_sha256": window["full_original_pdf_sha256"],
        "image_order_rule": (
            "Use original PDF frame order, never the inconsistent printed folio numbers"
        ),
        "source_body_original_pdf_frames": [581, 582, 583],
        "first_next_chapter_heading_pdf_frame": 583,
        "later_context_only": [584, 585, 586],
        "printed_folio_sequence": [source_hashes[str(n)]["printed_folio"] for n in range(581, 587)],
        "images": source_hashes,
    },
)
save(
    "UNRESOLVED_SOURCE_QUALIFICATIONS.json",
    {
        "batch": "B05j",
        "exact_diplomatic_transcription": False,
        "impression": "Original first edition images examined; selective anchors/paraphrases only",
        "unresolved": [
            (
                "The 'Septentrionall Signes' zodiac-glyph inventory is not independently "
                "glyph-verified; no sign-specific executable rule can be built from it."
            ),
            (
                "The visually dense 'Humane Signes' and alleged deformity sign lists have "
                "some ambiguous handwritten/printed glyphs and partial-sign qualifiers; "
                "do not promote unverified glyph sets."
            ),
            (
                "The complex 'both Lights impedited' and malefic-luminary/latitude "
                "passage contains ambiguous symbols; record only its broad original claim "
                "without resolving exact orbs or diagnosis conditions."
            ),
            (
                "The author's majority-of-testimonies and 'right mixture' procedure "
                "allows discretionary weighting, and cannot be scored as pre-calibrated "
                "probability or replicated without a frozen rule."
            ),
            (
                "The explicit Spaniard/Dane climate-country exception involves "
                "historically stereotyped appearance and demonstrates a confounding "
                "baseline; no contemporary ancestry, ethnicity or race inference is "
                "authorized."
            ),
            (
                "The source revisits partile Ascendant-lord, Mercury dispositor and "
                "stature rules from the preceding chapter; the historical annotations "
                "here do not constitute independent scientific corroboration."
            ),
            (
                "References to earlier Book I first-edition pages 57-83 and 93-99 are "
                "cross-references, not new independent authored experiments."
            ),
            (
                "All talk of deformity, bodily injury, scarring, eye harm and period "
                "disease is historically documented only and cannot support medical "
                "diagnosis, high-stakes or disability predictions."
            ),
            (
                "Full diplomatic transcription, independent paleographic annotation, "
                "biological outcomes, numerical stature thresholds and controlled blind "
                "tests remain undone."
            ),
            (
                "Printed folio discrepancies 539,548,549,542,543,552 must not cause "
                "reordering; original source scan is continuous."
            ),
        ],
    },
)
save(
    "RULES.json",
    {
        "batch": "B05j",
        "status": "FIRST_EDITION_HISTORICAL_DOCUMENTARY_LOCALLY_ADMITTED",
        "original_printed_chapter": "CXI",
        "editorial_chapter": "CXII",
        "record_count": 62,
        "first_record": "R6672",
        "last_record": "R6733",
        "source_groups": 11,
        "substantive_historical_units": 60,
        "next_chapter_navigation_units": 2,
        "original_pdf_body": [581, 582, 583],
        "next_heading_frame": 583,
        "original_diplomatic_transcription": False,
        "empirical_human_appearance_validation": 0,
        "empirical_validations": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
receipt = {
    "batch": "B05j",
    "source_authoring_sha256": digest(BASE / "SOURCE_FIRST_AUTHORING_20261017.json"),
    "records_sha256": digest(BASE / "RULES.json"),
    "previous_lilly": 6671,
    "new_historical_records": 62,
    "substantive_claim_annotations": 60,
    "following_chapter_navigation": 2,
    "lilly_if_published": 6733,
    "retained_ptolemy": 1066,
    "historical_corpus_if_published": 7799,
    "source_group_count": 11,
    "source_original_pdf_body": [581, 582, 583],
    "next_printed_chapter": "CXII",
    "next_editorial_chapter": "CXIII",
    "next_original_pdf_frame": 583,
    "original_pdf_folio": "549",
    "human_biometric_validations": 0,
    "medical_or_ancestry_validations": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
save("ACCEPTANCE.json", receipt)
print(json.dumps(receipt, indent=2))
