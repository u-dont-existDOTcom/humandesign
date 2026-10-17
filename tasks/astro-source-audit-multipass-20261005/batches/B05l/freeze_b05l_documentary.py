#!/usr/bin/env python3
"""Source-only freeze of Lilly's 1647 general fortune chapter (not a prediction test)."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


def save(name, value):
    (B / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def h(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


author = j("SOURCE_FIRST_AUTHORING_20261017.json")
assert author["batch"] == "B05l"
assert author["printed_chapter"] == "CXIII"
assert author["body_pages"] == [585, 586]
assert len(author["groups"]) == 10
records = []
mapping = []
for i, group in enumerate(author["groups"], start=1):
    sid = f"B05l-S{i:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_pages"]) <= {585, 586, 587}
    mapped = []
    for c in group["claims"]:
        no = 6765 + len(records)
        rid = f"R{no}"
        assert rid == c["id"], (rid, c["id"])
        assert len(c["anchor_not_diplomatic"]) >= 12
        assert len(c["meaning_historical_only"]) > 40
        assert not (c["validated_actual_prediction"] or c["runtime_promoted"])
        row = {
            "id": rid,
            "record_number": no,
            "batch": "B05l",
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_pages"],
            "role": c["role"],
            "printed_chapter": (
                "CXIII"
                if c["role"] != "next_chapter_navigation"
                else "SECOND_HOUSE_WEALTH_OR_CXIIII_NAVIGATION"
            ),
            "anchor_not_diplomatic": c["anchor_not_diplomatic"],
            "historical_only_meaning": c["meaning_historical_only"],
            "source_condition_type": c["qualification"],
            "historical_documentary_accepted": True,
            "verified_human_life_outcome_prediction": False,
            "prospective_blind_validation": False,
            "validated_medical_or_financial_forecast": False,
            "runtime_rule_promoted": False,
        }
        records.append(row)
        mapped.append(rid)
    mapping.append(
        {
            "source_span": sid,
            "pdf_pages": group["original_pdf_pages"],
            "source_group": group["source_group"],
            "record_ids": mapped,
        }
    )
assert len(records) == 44
assert [r["record_number"] for r in records] == list(range(6765, 6809))
assert sum(r["role"] == "next_chapter_navigation" for r in records) == 3
assert [r["id"] for r in records[-3:]] == ["R6806", "R6807", "R6808"]

images = {}
for n in range(585, 589):
    file = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = file.read_bytes()
    assert len(raw) > 200000 and raw[:2] == bytes.fromhex("ffd8")
    images[str(n)] = {
        "path": str(file.relative_to(B)),
        "sha256": h(file),
        "bytes": len(raw),
        "original_printed_folio": {
            585: "543",
            586: "552",
            587: "553",
            588: "554",
        }[n],
        "role": "general_fortune_body" if n in (585, 586) else "wealth_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05l",
        "original_full_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "origin": "Wellcome Collection b30338724, original first edition 1647",
        "source_body_frames": [585, 586],
        "unnumbered_wealth_heading_frame": 586,
        "next_printed_numbered_chapter_frame": 587,
        "pagination_note": (
            "Original PDF585 printed folio543 follows PDF584 folio542, "
            "then PDF586–588 folios552,553,554. Original physical text is "
            "continuous; do not reorder or infer a missing chapter."
        ),
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05l",
        "group_count": 10,
        "record_count": 44,
        "groups": mapping,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05l",
        "issues": [
            (
                "General fortune and misery are broad categories with no measured "
                "outcomes, independent observations, base rates, decision thresholds or "
                "calibration in the source."
            ),
            (
                "The phrase 3–4 dignified planets needs a frozen exact "
                "essential-dignity scheme and a defined chart/house algorithm before "
                "any meaningful test."
            ),
            (
                "Mutual reception and debilitated house rules contain alternatives; "
                "avoid unregistered and retrospective selection of the most flattering "
                "chart configuration."
            ),
            (
                "The author says positive natal configurations can be delayed; this can "
                "rescue failed timeless forecasts unless acceptable time windows and "
                "rejection rules are registered."
            ),
            (
                "Directions of five Hylegical places and promittor contacts require "
                "precisely predeclared computations and historical-calendar "
                "assumptions; no explicit quantitative forecasting precision is "
                "demonstrated by this passage."
            ),
            (
                "Use an independent cohort, exact event-date sources, blind targets, "
                "untouched held-out cases and meaningful non-astrological "
                "age/region/social controls to evaluate any future claims."
            ),
            (
                "Happiness, esteem, 'misery', social class, calamity and status are "
                "different constructs; do not code them as one undifferentiated success "
                "score."
            ),
            (
                "The Saturn/Mars/South Node/Mercury signification glyph grouping and "
                "conjunction/operator scope on page552 require another first-edition "
                "specialist audit before deterministic implementation."
            ),
            (
                "The author's attribution of calamity cause from malefic house and time "
                "from directions is not proof of an independently foretold cause/date."
            ),
            (
                "The unnumbered second-house wealth section begins mid original PDF586, "
                "followed by printed CXIIII wealth chapter on PDF587; do not skip "
                "either by following only Roman numbered chapters."
            ),
            (
                "Original 1647 pages are preserved as image witnesses and clauses "
                "paraphrased; no full diplomatic transcription is claimed."
            ),
            (
                "Historical astrology cannot be the basis for medical, legal, financial "
                "or personal safety judgments from these untested claims."
            ),
        ],
        "no_independent_predictions": True,
        "runtime_admission_forbidden": True,
    },
)
save(
    "RULES.json",
    {
        "batch": "B05l",
        "status": "ORIGINAL_1647_HISTORICAL_DOCUMENTARY_LOCALLY_ADMITTED",
        "printed_chapter": "CXIII",
        "editorial_chapter": "CXIV",
        "record_count": 44,
        "first_record": "R6765",
        "last_record": "R6808",
        "source_passages": 10,
        "substantive_history_records": 41,
        "following_section_navigation": 3,
        "body_pages": [585, 586],
        "further_context_pages": [587, 588],
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "independently_correct_life_forecasts": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
receipt = {
    "batch": "B05l",
    "status": "LOCALLY_VERIFIED_HISTORICAL_SOURCE_PENDING_REMOTE",
    "prior_lilly": 6764,
    "historical_records_added": 44,
    "lilly_if_published": 6808,
    "ptolemy_retained": 1066,
    "combined_historical_if_published": 7874,
    "source_body_frames": [585, 586],
    "next_source_frame": 586,
    "next_section": "Unnumbered second house of riches, followed by CXIIII",
    "substantive": 41,
    "following_navigation": 3,
    "original_source_passages": 10,
    "rules_sha256": h(B / "RULES.json"),
    "authoring_sha256": h(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
    "empirical_validations": 0,
    "independent_life_predictions": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
save("ACCEPTANCE.json", receipt)
print(json.dumps(receipt, indent=2))
