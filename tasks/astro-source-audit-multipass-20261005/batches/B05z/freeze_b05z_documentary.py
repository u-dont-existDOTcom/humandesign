#!/usr/bin/env python3
"""Original Lilly 1647 patrimony inheritance source only, no financial outcomes."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text())


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261017.json")
assert a["batch"] == "B05z"
assert a["printed_chapter"] == "CXXIIII"
assert a["body_original_pdf_frames"] == [606, 607]
assert len(a["groups"]) == 8
rows, mapping = [], []
for gi, group in enumerate(a["groups"], 1):
    sid = f"B05z-S{gi:03d}"
    assert group["source_span"] == sid
    assert set(group["pdf_frames"]) <= {606, 607}
    refs = []
    for c in group["claims"]:
        no = 7441 + len(rows)
        rid = f"R{no}"
        assert c["id"] == rid
        assert len(c["anchor_not_diplomatic"]) >= 7
        assert len(c["meaning_historical_only"]) >= 47
        assert not c["independent_inheritance_outcome_validated"]
        assert not c["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": sid,
                "original_pdf_frames": group["pdf_frames"],
                "role": c["role"],
                "anchor_not_diplomatic": c["anchor_not_diplomatic"],
                "meaning_historical_only": c["meaning_historical_only"],
                "qualification": c["qualification"],
                "historical_source_accepted": True,
                "independent_human_inheritance_validated": False,
                "family_finances_or_management_predicted": False,
                "legal_or_financial_advice_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        refs.append(rid)
    mapping.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["pdf_frames"],
            "source_group": group["passage"],
            "mapped_record_ids": refs,
        }
    )
assert len(rows) == 33
assert [r["record_number"] for r in rows] == list(range(7441, 7474))
assert [r["id"] for r in rows if r["role"] == "next_chapter_navigation"] == ["R7472", "R7473"]
images = {}
for n in (606, 607, 608, 609):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "role": "inheritance_body" if n in (606, 607) else "later_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05z",
        "source": (
            "William Lilly original Christian Astrology first edition 1647, Wellcome b30338724"
        ),
        "full_pdf_sha256": ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"),
        "body_original_frames": [606, 607],
        "next_printed_CXXV_heading_frame": 607,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05z",
        "source_groups": mapping,
        "source_group_count": 8,
        "record_count": 33,
        "substantive": 31,
        "following_navigation": 2,
    },
)
issues = [
    (
        "Historical estate-transfer claims lack independently verified "
        "probate cases, property valuation, family starting wealth, "
        "financial management records or non-astrology controls."
    ),
    (
        "Sun by day versus Saturn by night is a conditional sect "
        "distinction; collapsing it removes an essential source condition."
    ),
    (
        "Benefics in conjunction or favorable aspect are alternative "
        "supporting testimonies with distinct house placement and rulership "
        "clauses."
    ),
    (
        "Mars afflicting day Sun or night Saturn is combined with absence of "
        "intervening fortunate beneficial aspect in the negative branch."
    ),
    (
        "The nocturnal diminished/afflicted Moon, second ruler and fourth "
        "ruler/house clauses combine several potentially alternative "
        "requirements; grammatical scope needs further reading."
    ),
    (
        "The twelfth-house Saturn and fourth ruler must both be peregrine "
        "under one of several separately alleged patrimony-wasting paths."
    ),
    (
        "The Sun/Mars conjunct/peregrine and second-house-harm original "
        "sentence has unclear retrograde or peregrine referent; no "
        "deterministic rule warranted."
    ),
    (
        "The chapter's alleged destruction-of-patrimony branches may overlap "
        "and rescue failed positive cases; no registered prospective "
        "comparison or economic outcome window."
    ),
    (
        "Parent's own birth-chart findings from preceding section are "
        "preferred source for parent fortunes; child natal chart forecasts "
        "do not independently corroborate those claims."
    ),
    (
        "Statements about 'wasting' a deceased parent's inheritance are "
        "socially and financially sensitive historical stereotypes, not "
        "evidence of actual conduct."
    ),
    (
        "The following printed CXXV on parents' agreement begins lower "
        "original PDF607 and must be extracted separately."
    ),
    (
        "The original 1647 image order and source paraphrases are preserved "
        "but complete diplomatic glyph transcription and empirical validity "
        "remain open."
    ),
]
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05z",
        "issues": issues,
        "actual_human_inheritance_validations": 0,
        "legal_or_financial_action_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B05z",
        "status": "ORIGINAL_1647_PATERNITY_ESTATE_DOCUMENTARY_SOURCE_ONLY",
        "printed_chapter": "CXXIIII",
        "editorial_chapter": "CXXV",
        "record_count": 33,
        "first_record": "R7441",
        "last_record": "R7473",
        "substantive_historical": 31,
        "navigation": 2,
        "source_groups": 8,
        "body_original_frames": [606, 607],
        "next_printed_heading_frame": 607,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "economic_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B05z",
        "previous_lilly": 7440,
        "new_historical_records": 33,
        "lilly_if_published": 7473,
        "ptolemy_retained": 1066,
        "combined_if_published": 8539,
        "substantive": 31,
        "navigation": 2,
        "source_groups": 8,
        "next_printed": "CXXV",
        "next_original_pdf": 607,
        "rules_sha256": sha(B / "RULES.json"),
        "empirical_validations": 0,
        "human_family_financial_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B05z 33 source records R7441-R7473, zero actual economic validation")
