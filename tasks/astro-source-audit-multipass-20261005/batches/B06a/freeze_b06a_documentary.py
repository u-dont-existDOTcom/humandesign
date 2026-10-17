#!/usr/bin/env python3
"""Source-only William Lilly 1647 parent-parent harmony; no modern characterization."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def load(name):
    return json.loads((B / name).read_text())


def write(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


s = load("SOURCE_FIRST_AUTHORING_20261017.json")
assert s["batch"] == "B06a"
assert s["printed_chapter"] == "CXXV"
assert s["original_body_pdf_frames"] == [607]
assert len(s["source_groups"]) == 9
records, reverse = [], []
for group_no, group in enumerate(s["source_groups"], 1):
    sid = f"B06a-S{group_no:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {607, 608}
    ids = []
    for claim in group["claims"]:
        no = 7474 + len(records)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["source_anchor_not_diplomatic"]) >= 6
        assert len(claim["historical_meaning"]) >= 48
        assert not claim["validated_parental_relationship"]
        assert not claim["runtime_promoted"]
        row = {
            "id": rid,
            "record_number": no,
            "batch": "B06a",
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "role": claim["role"],
            "anchor_not_diplomatic": claim["source_anchor_not_diplomatic"],
            "meaning_historical_only": claim["historical_meaning"],
            "qualification": claim["source_qualification"],
            "historical_documentary_accepted": True,
            "actual_parental_marriage_harmony_validated": False,
            "verified_personal_ethics_or_behavior": False,
            "clinical_or_family_actions_authorized": False,
            "promoted_to_runtime": False,
        }
        records.append(row)
        ids.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "topic": group["source_group"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 29
assert [r["record_number"] for r in records] == list(range(7474, 7503))
assert [r["id"] for r in records if r["role"] == "next_chapter_navigation"] == ["R7501", "R7502"]
images = {}
for n in (607, 608, 609):
    file = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(file.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(file),
        "original_printed_folio": str(n - 34),
        "role": "parents_agreement_body" if n == 607 else "next_chapter_context",
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06a",
        "source": "Lilly Christian Astrology 1647 original first edition Wellcome b30338724",
        "original_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_frame": 607,
        "following_chapter_CXXVI_frame": 608,
        "images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06a",
        "source_groups": reverse,
        "source_group_count": 9,
        "record_count": 29,
        "substantive_historical": 27,
        "navigation": 2,
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06a",
        "issues": [
            (
                "Lilly's Sun/Venus by day and Saturn/Moon by night are alternate "
                "sex-coded historical astrological source configurations, not "
                "empirically valid relationships."
            ),
            (
                "The author infers women's marital obedience or rebelliousness from "
                "Venus strength and phase; this is a discriminatory historical "
                "gender stereotype, not a real-person character assessment."
            ),
            (
                "The Venus-to-Sun combustion application branch requires a "
                "historical timing calculation that has not been independently "
                "verified here."
            ),
            (
                "The converse Venus retrograde/peregrine/unfortunate/separating from "
                "Sun branch contains multiple preconditions, not a single "
                "Venus-retrograde verdict."
            ),
            (
                "Beneficial aspects, mutual reception, opposition and square are "
                "distinct conditional tests and must not be retrospectively selected "
                "according to remembered marriage history."
            ),
            (
                "A malefic in the mother's tenth versus father's fourth house is "
                "used as an alleged blame assignment, not evidence about a parent's "
                "guilt or causation of arguments."
            ),
            (
                "This source presents no actual parent-parent couple data, "
                "prospective forecasts, subjective relationship measurements, "
                "genuine outcome negatives or non-astrological controls."
            ),
            (
                "The following printed chapter CXXVI starts original PDF608, and its "
                "Regiomontanus father-birth-time method is a separate computational "
                "source not extracted here."
            ),
            (
                "Original first-edition page scanned, source anchors selectively "
                "paraphrased; complete historical astronomical glyph transcription "
                "and blind prediction validity remain open."
            ),
        ],
        "independent_human_couple_validations": 0,
        "moral_or_criminality_classification_authorized": False,
        "runtime_promotions": 0,
    },
)
write(
    "RULES.json",
    {
        "batch": "B06a",
        "status": "ORIGINAL_1647_PARENTAL_CONCORD_DOCUMENTARY_ONLY",
        "printed_chapter": "CXXV",
        "editorial_chapter": "CXXVI",
        "record_count": 29,
        "first_record": "R7474",
        "last_record": "R7502",
        "source_passage_groups": 9,
        "substantive_historical_clauses": 27,
        "following_chapter_navigation": 2,
        "body_pdf_frame": 607,
        "next_heading_original_frame": 608,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "independent_parental_relationship_validations": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
write(
    "ACCEPTANCE.json",
    {
        "batch": "B06a",
        "status": "SOURCE_ONLY_LOCALLY_FROZEN_PENDING_REMOTE",
        "previous_lilly": 7473,
        "new_historical_records": 29,
        "lilly_if_published": 7502,
        "ptolemy_retained": 1066,
        "combined_historical_if_published": 8568,
        "substantive": 27,
        "navigation": 2,
        "source_group_count": 9,
        "next_printed": "CXXVI",
        "next_original_pdf": 608,
        "rules_sha256": sha(B / "RULES.json"),
        "source_authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "human_relationship_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06a parental-concord original historic source frozen R7474-R7502, N=29")
