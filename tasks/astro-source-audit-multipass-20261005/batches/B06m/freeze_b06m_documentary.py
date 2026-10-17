#!/usr/bin/env python3
"""Freeze 1647 Lilly relationship concord source, not personal predictions."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, value):
    (B / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261017.json")
assert a["batch"] == "B06m" and a["printed_chapter"] == "CXXXV"
assert a["body_original_pdf_frames"] == [631, 632, 633]
assert a["following_printed_chapter"] == "CXXXVI"
assert len(a["groups"]) == 7

rows, mapping = [], []
for group_no, group in enumerate(a["groups"], 1):
    span = f"B06m-S{group_no:03d}"
    assert group["source_span"] == span
    assert set(group["original_pdf_frames"]) <= {631, 632, 633}
    ids = []
    for clause in group["clauses"]:
        n = 8273 + len(rows)
        rid = f"R{n}"
        assert clause["id"] == rid
        assert len(clause["anchor_not_diplomatic"]) >= 8
        assert len(clause["historical_only_meaning"]) >= 50
        assert not clause["independent_marital_relational_quality_validated"]
        assert not clause["real_partner_intimate_moral_claim_authorized"]
        assert not clause["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": n,
                "batch": "B06m",
                "source_span": span,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": clause["role"],
                "anchor_not_diplomatic": clause["anchor_not_diplomatic"],
                "historical_meaning_only": clause["historical_only_meaning"],
                "source_qualification": clause["source_qualification"],
                "independent_human_marital_concord_validated": False,
                "independent_real_couple_pair_chart_accuracy_validated": False,
                "real_partner_fidelity_morality_jealousy_claim_authorized": False,
                "private_safety_or_intimate_inference_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    mapping.append(
        {
            "source_span": span,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["source_group"],
            "mapped_record_ids": ids,
        }
    )
assert len(rows) == 71
assert [x["record_number"] for x in rows] == list(range(8273, 8344))
assert [x["id"] for x in rows if x["role"] == "next_chapter_navigation"] == ["R8342", "R8343"]

images = {}
for page in range(631, 635):
    path = B / "evidence" / f"pdf_1647-{page}.jpg"
    data = path.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 150000
    images[str(page)] = {
        "file": str(path.relative_to(B)),
        "bytes": len(data),
        "sha256": sha(path),
        "printed_folio": str(page - 34),
        "source_role": "marital_concord_body"
        if page <= 633
        else "following_death_and_women_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06m",
        "source": "William Lilly Christian Astrology original first edition Wellcome b30338724",
        "original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [631, 632, 633],
        "following_printed_CXXXVI_heading_pdf": 633,
        "photos": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06m",
        "source_groups": mapping,
        "source_group_count": len(mapping),
        "record_count": len(rows),
        "substantive": 69,
        "following_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06m",
        "issues": [
            (
                "Seventeenth-century gender-coded marital concord models do not "
                "establish actual present couples' psychological health, conduct, "
                "fidelity or longevity."
            ),
            (
                "Original favorable versus adverse aspects depend jointly on "
                "benefic/malefic planetary nature; malefic-friendly aspects may still "
                "supposedly indicate disagreement and benefic-hard may still indicate "
                "moderate agreement."
            ),
            (
                "The first group of aspect heuristics explicitly applies only to Lord "
                "of Seventh and Moon, not to every marriage significator; later "
                "aphorisms introduce others. Preserve contextual scope."
            ),
            (
                "Lilly calls comparison of BOTH separately calculated genitures most "
                "assured; missing one birth time or natal chart does not authorize "
                "choosing favorable narrative."
            ),
            (
                "Wife Sun at same zodiac sign AND degree of husband's Moon, or wife's "
                "Moon at man's Sun, are separate directional relationship geometry "
                "routes; vague zodiac-sign similarity is not sufficient."
            ),
            (
                "All personal natal chart birth times, places, independently confirmed "
                "relationship events, partner questionnaires and comparator samples "
                "absent."
            ),
            (
                "Author offers vague unity, perpetual affection, disagreement and "
                "contentment endpoints with no calibrated time, repeated measure or "
                "objective scale."
            ),
            (
                "Venus with Saturn aspecting Mars original glyph syntax is not "
                "resolved as a three-way conjunction; do not encode until diplomatic "
                "specialists verify."
            ),
            (
                "Claims about jealousy, infidelity, desire for other partners or "
                "behavior in a spouse are period stereotypes, never established actual "
                "psychological/moral facts."
            ),
            (
                "Common versus movable signs are original zodiac taxonomy and interact "
                "with benefit/affliction conditions; avoid post-hoc rule selection."
            ),
            (
                "The paragraph crossing PDF632-633 has Moon beholding Sun in favorable "
                "aspect, both in humane signs AND fortune aspecting one or both as "
                "compound condition, not separate independent supports."
            ),
            (
                "Original malefic/square/opposition plus bad Sun-Moon contacts has "
                "multiple compound conditions, not a free-standing universal hostile "
                "relationship verdict."
            ),
            (
                "A Moon ruled-seventh, waning and in eighth source claim is about "
                "subjective marital satisfaction and not direct mortality in this "
                "chapter."
            ),
            (
                "Next printed CHAP CXXXVI on husband-versus-wife death order starts "
                "middle original PDF633; no mortality source rules ingested here."
            ),
            (
                "This first edition selective source paraphrase does NOT constitute "
                "full diplomatic transcription, independent Ptolemy collation, numeric "
                "geometry or validated partner predictions."
            ),
        ],
        "couple_pair_actual_predictions_validated": 0,
        "intimate_or_moral_real_partner_claims_authorized": False,
        "complete_pair_geometry_engine_verified": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06m",
        "status": "ORIGINAL_1647_MUTUAL_MARITAL_CONCORD_HISTORICAL_ONLY",
        "printed_chapter": "CXXXV",
        "editorial_chapter": "CXXXVI",
        "record_count": 71,
        "first_record": "R8273",
        "last_record": "R8343",
        "substantive": 69,
        "next_chapter_navigation": 2,
        "source_groups": 7,
        "source_pdf_frames": [631, 632, 633],
        "following_printed_heading_pdf": 633,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "actual_couple_predictive_validations": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06m",
        "status": "FIRST_EDITION_MARITAL_CONCORD_FROZEN_LOCAL_PENDING_REMOTE",
        "previous_lilly": 8272,
        "new_historical_annotations": 71,
        "lilly_if_published": 8343,
        "ptolemy_retained": 1066,
        "combined_if_published": 9409,
        "substantive": 69,
        "navigation": 2,
        "source_groups": 7,
        "new_numbered_chapters": 1,
        "next_printed_chapter": "CXXXVI",
        "next_source_pdf": 633,
        "rules_sha256": sha(B / "RULES.json"),
        "source_authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "actual_marriage_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06m historical marriage concord: 71 first-edition notes R8273–R8343")
