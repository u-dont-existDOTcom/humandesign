#!/usr/bin/env python3
"""Freeze unnumbered second-house riches from original Lilly 1647, historical only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


def save(name, value):
    (B / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def h(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


author = j("SOURCE_FIRST_AUTHORING_20261017.json")
w = j("SOURCE_WINDOW_20261017.json")
assert author["batch"] == w["batch"] == "B05m"
assert w["accepted_lilly_before_extraction"] == 6808
assert author["original_pdf_body"] == [586, 587]
assert len(author["source_groups"]) == 6
records, reverse = [], []
for i, group in enumerate(author["source_groups"], 1):
    sid = f"B05m-S{i:03d}"
    assert group["id"] == sid
    assert set(group["original_pdf_pages"]) <= {586, 587}
    refs = []
    for item in group["claims"]:
        no = 6809 + len(records)
        rid = f"R{no}"
        assert item["id"] == rid
        assert len(item["source_meaning_historical_only"]) >= 45
        assert not item["independent_financial_accuracy_validation"]
        assert not item["runtime_promoted"]
        row = {
            "id": rid,
            "record_number": no,
            "batch": "B05m",
            "source_span": sid,
            "original_pdf_pages": group["original_pdf_pages"],
            "role": item["role"],
            "original_anchor_not_diplomatic": item["anchor_not_diplomatic"],
            "historical_only_paraphrase": item["source_meaning_historical_only"],
            "qualification": item["qualification"],
            "accepted_historical_documentation": True,
            "independent_human_economic_prediction": False,
            "actual_inheritance_prediction_validated": False,
            "source_attribution_verified_against_ptolemy": False,
            "runtime_scoring_rule_promoted": False,
        }
        records.append(row)
        refs.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_pages": group["original_pdf_pages"],
            "original_source_group": group["source_group"],
            "mapped_records": refs,
        }
    )

assert len(records) == 45
assert [r["record_number"] for r in records] == list(range(6809, 6854))
assert sum(r["role"] == "next_chapter_navigation" for r in records) == 2
assert records[-2]["id"] == "R6852" and records[-1]["id"] == "R6853"
assert len({r["id"] for r in records}) == len(records)
assert len(reverse) == 6
pages = {}
for p in (586, 587, 588):
    file = B / w["images"][str(p)]["file"]
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 200000
    assert h(file) == w["images"][str(p)]["sha256"]
    pages[str(p)] = {
        "pdf_frame": p,
        "file": str(file.relative_to(B)),
        "bytes": len(raw),
        "sha256": h(file),
        "printed_folio": w["images"][str(p)]["printed_folio_original"],
        "role": "source_body" if p in (586, 587) else "next_chapter_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05m",
        "original_full_pdf_sha256": w["original_pdf_sha256"],
        "source": w["primary_source"],
        "body_pdf_frames": [586, 587],
        "following_heading_pdf_frame": 587,
        "printed_chapter_after_unnumbered": "CXIIII",
        "pages": pages,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05m",
        "source_groups": reverse,
        "group_count": 6,
        "record_count": 45,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05m",
        "issues": [
            (
                "Ptolemy lib.4 cap.1 is Lilly's historical attribution and must be "
                "separately verified against actual Ptolemy text before claiming "
                "quote-level agreement."
            ),
            (
                "The second-house cusp range from five degrees before second cusp to "
                "within five degrees of the third must retain exactly the original "
                "inclusion language before formal angle inequalities are encoded."
            ),
            (
                "Interceptions and house systems change the sign set and require frozen "
                "computational and longitude provenance for any rule comparison."
            ),
            (
                "Astrological Part of Fortune calculation depends on sect and "
                "traditional definitions; do not silently select a formula."
            ),
            (
                "A stronger planet nearer the second cusp is unquantified, with no "
                "weighting function or testable continuous gradient supplied."
            ),
            (
                "The alternative inheritance discussion's 'or she afflicting' has "
                "unresolved Moon pronoun and operator scope."
            ),
            (
                "Superior angles, bycorporeal signs, western angle, partile good "
                "aspect, and planet dominium require source-precise definitions before "
                "executable implementation."
            ),
            (
                "Cause-specific Saturn/Jupiter/Mars/Venus/Mercury wealth routes are "
                "stereotypes about 17th-century vocations and gender, not real-world "
                "contemporary financial predictions."
            ),
            (
                "Estate retention/destruction and planetary access to angles are not "
                "independently tested and have no registered timing tolerances."
            ),
            (
                "The source explicitly transitions from Ptolemy to Leovitius/Origanus; "
                "later elaborations cannot be misattributed to a unitary historical "
                "Ptolemy theory."
            ),
            (
                "Full source image order is correct, but this unit is not a full "
                "diplomatic transcription or independent human validation."
            ),
            (
                "The following numbered CHAP CXIIII begins in the same PDF587 and its "
                "substantive claims must not be absorbed into the unnumbered passage."
            ),
        ],
        "real_human_economic_validations": 0,
        "medical_financial_advice_authorized": False,
        "runtime_rules_promoted": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B05m",
        "status": "ORIGINAL_1647_UNNUMBERED_SECOND_HOUSE_HISTORICAL_DOCUMENTARY_ADMITTED_LOCAL",
        "source_section": "UNNUMBERED_SECOND_HOUSE_RICHES",
        "record_count": 45,
        "first_record": "R6809",
        "last_record": "R6853",
        "source_passages": 6,
        "substantive_historical_records": 43,
        "following_numbered_navigation": 2,
        "original_pdf_body": [586, 587],
        "next_heading_original_pdf": 587,
        "original_diplomatic_transcription_complete": False,
        "independent_wealth_outcomes_validated": 0,
        "empirical_validations": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
accept = {
    "batch": "B05m",
    "status": "SOURCE_ADMISSION_PREPARED_PENDING_REMOTE",
    "previous_lilly": 6808,
    "new_historical_records": 45,
    "lilly_if_published": 6853,
    "ptolemy_retained": 1066,
    "combined_if_published": 7919,
    "substantive_historical_records": 43,
    "navigation_records": 2,
    "source_image_frames": [586, 587, 588],
    "next_chapter_printed": "CXIIII",
    "next_chapter_editorial": "CXV",
    "next_pdf_frame": 587,
    "rules_sha256": h(B / "RULES.json"),
    "authoring_sha256": h(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
    "empirical_validations": 0,
    "independent_human_economic_prediction": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
save("ACCEPTANCE.json", accept)
print(json.dumps(accept, indent=2))
