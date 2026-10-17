#!/usr/bin/env python3
"""First-edition Lilly historical sibling fortunes, never real-person predictions."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


def dump(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


author = j("SOURCE_FIRST_AUTHORING_20261017.json")
assert author["batch"] == "B05t"
assert author["printed_chapter"] == "CXIX"
assert author["body_original_pdf_frames"] == [600]
assert len(author["groups"]) == 6
rows, cross = [], []
for i, group in enumerate(author["groups"], 1):
    sid = f"B05t-S{i:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_pages"]) <= {600, 601}
    ids = []
    for claim in group["claims"]:
        no = 7187 + len(rows)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["original_anchor_not_diplomatic"]) >= 9
        assert len(claim["meaning_historical_only"]) >= 40
        assert not claim["actual_human_sibling_outcome_validated"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_pages"],
                "role": claim["role"],
                "source_anchor_not_diplomatic": claim["original_anchor_not_diplomatic"],
                "meaning_historical_only": claim["meaning_historical_only"],
                "source_qualification": claim["qualification"],
                "historical_documentary_accepted": True,
                "actual_human_sibling_outcome_validated": False,
                "sibling_longevity_validated": False,
                "clinical_or_social_advice_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    cross.append(
        {
            "source_span": sid,
            "pdf_frames": group["original_pdf_pages"],
            "source_group": group["source_group"],
            "record_ids": ids,
        }
    )
assert len(rows) == 22
assert [r["record_number"] for r in rows] == list(range(7187, 7209))
assert [x["id"] for x in rows if x["role"] == "next_chapter_navigation"] == ["R7207", "R7208"]
img = {}
for n in (600, 601, 602):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    data = p.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 150000
    img[str(n)] = {
        "file": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(data),
        "printed_folio": str(n - 34),
        "role": "chapter_body" if n == 600 else "context",
    }
dump(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05t",
        "source": "William Lilly 1647 original first edition Wellcome b30338724",
        "original_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frame": 600,
        "next_printed_chapter_CXX_frame": 601,
        "next_next_printed_CXXI_frame": 602,
        "images": img,
    },
)
dump(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05t",
        "source_groups": cross,
        "record_count": 22,
        "substantive": 20,
        "navigation": 2,
    },
)
limits = [
    "Lilly's sibling happiness, wealth, long life and preferment "
    "claims have no independent person-level evidence.",
    "All or majority favorable sibling significators is a "
    "different condition than all or majority weak ones.",
    "Mixed strong/weak configurations allegedly allow "
    "different fortunes for different siblings; the source "
    "does not specify individual birth order identification.",
    "The author divides Mars and Moon testimonies into "
    "male/female sibling comparative fortunes, a historical "
    "gender stereotype rather than a reliable sex or social forecast.",
    "The sibling-relative favor rule additionally requires "
    "overall strong testimony and opposite strength of Moon "
    "versus Mars; isolate all conditions.",
    "No preregistered lifespan, income, social position, "
    "education, health or age window is given for the outcomes.",
    "Actual sibling differences are heavily confounded by "
    "birth order, parental wealth, geography, sex inequality "
    "and access to resources.",
    "Printed CXIX is confined to lower original PDF600; "
    "following printed CXX on PDF601 concerns concord and "
    "is not included in this batch.",
    "This is source-based paraphrase, not full diplomatic "
    "transcription or any scientific demonstration of astrology.",
]
dump(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05t",
        "issues": limits,
        "human_family_outcomes_validated": 0,
        "runtime_promotions": 0,
    },
)
dump(
    "RULES.json",
    {
        "batch": "B05t",
        "status": "FIRST_EDITION_SIBLING_FORTUNE_HISTORICAL_SOURCE_LOCALLY_ACCEPTED",
        "printed_chapter": "CXIX",
        "editorial_chapter": "CXX",
        "record_count": 22,
        "first_record": "R7187",
        "last_record": "R7208",
        "source_groups": 6,
        "substantive_historical_records": 20,
        "following_chapter_navigation": 2,
        "original_body_pdf_frame": 600,
        "next_heading_pdf_frame": 601,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "independent_sibling_fortune_validations": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
dump(
    "ACCEPTANCE.json",
    {
        "batch": "B05t",
        "previous_lilly": 7186,
        "new_source_records": 22,
        "lilly_if_published": 7208,
        "retained_ptolemy": 1066,
        "combined_if_published": 8274,
        "substantive": 20,
        "navigation": 2,
        "source_group_count": 6,
        "next_printed_chapter": "CXX",
        "next_original_pdf_page": 601,
        "rules_sha256": sha(B / "RULES.json"),
        "empirical_validations": 0,
        "human_social_fortune_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B05t R7187–R7208: 22 historical notes, no human predictions")
