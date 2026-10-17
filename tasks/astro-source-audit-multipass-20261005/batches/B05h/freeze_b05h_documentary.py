#!/usr/bin/env python3
"""Deterministic source-first historical source freeze for Lilly CHAP CIX, 1647.

Anchors are not full diplomatic transcription. No natal cognitive or health validation.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def write(name, data):
    (B / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_CLAIMS_AUTHORING.json")
assert a["batch"] == "B05h" and len(a["source_passages"]) == 12
assert a["pages"]["body"] == [577, 578, 579, 580]
ids = []
rule_rows = []
reverse = []
all_refs = []
for j, s in enumerate(a["source_passages"], start=1):
    sid = f"B05h-S{j:03d}"
    assert s["id"] == sid
    assert set(s["pdf_pages"]) <= {577, 578, 579, 580, 581}
    this = []
    for c in s["claims"]:
        rid = f"R{6592 + len(ids)}"
        assert c["proposed_record"] == rid, f"Record order mismatch {c['proposed_record']} != {rid}"
        assert len(c["anchor_not_diplomatic"]) > 12 and len(c["meaning_historical_only"]) > 40
        assert c["role"] in {
            "heading",
            "historical_mechanism",
            "positive_condition",
            "negative_condition",
            "mixed_condition",
            "graded_condition",
            "override",
            "qualification",
            "next_chapter_navigation",
        }
        assert not any(
            sensitive in c["meaning_historical_only"].lower()
            for sensitive in [
                "astrologically proven",
                "predicts actual intelligence",
                "empirically validated",
            ]
        )
        row = {
            "id": rid,
            "record_number": 6592 + len(ids),
            "batch": "B05h",
            "printed_chapter": "CIX"
            if c["role"] != "next_chapter_navigation"
            else "CX_OR_CXI_NAVIGATION_ONLY",
            "editorial_chapter": "CX"
            if c["role"] != "next_chapter_navigation"
            else "CXI_OR_CXII_NAVIGATION_ONLY",
            "source_span": sid,
            "original_pdf_pages": s["pdf_pages"],
            "role": c["role"],
            "anchor_not_diplomatic": c["anchor_not_diplomatic"],
            "meaning_historical_only": c["meaning_historical_only"],
            "historical_documentary_accepted": True,
            "validated_human_intelligence": False,
            "validated_cognitive_disability_classification": False,
            "validated_personality_prediction": False,
            "runtime_model_promoted": False,
            "source_limitation": (
                "Historical source assertion from 1647, not independent clinical, cognitive "
                "or social prediction."
            ),
        }
        rule_rows.append(row)
        ids.append(rid)
        this.append(rid)
        all_refs.append((sid, rid))
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_pages": s["pdf_pages"],
            "original_source_group": s["printed_source_group"],
            "mapped_record_ids": this,
        }
    )
assert len(ids) == 53 and ids == [f"R{n}" for n in range(6592, 6645)]
nav = [r for r in rule_rows if r["role"] == "next_chapter_navigation"]
assert len(nav) == 3 and len(rule_rows) - len(nav) == 50
assert len(set(x["source_span"] for x in rule_rows)) == 12
assert rule_rows[0]["anchor_not_diplomatic"].startswith("CHAP CIX")
assert "Mercury and his configuration with the Moon" in rule_rows[1]["anchor_not_diplomatic"]
assert all(
    not (
        x["validated_human_intelligence"]
        or x["validated_cognitive_disability_classification"]
        or x["runtime_model_promoted"]
    )
    for x in rule_rows
)

evidence = {}
for n in range(577, 582):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    bb = p.read_bytes()
    assert len(bb) > 100_000 and bb.startswith(bytes.fromhex("ffd8")), (
        f"Not original JPEG witness: {p}"
    )
    evidence[str(n)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(bb),
        "sha256": sha(p),
        "observed_printed_page": {577: "543", 578: "544", 579: "545", 580: "538", 581: "539"}[n],
    }
write(
    "SOURCE_IMAGE_WITNESSES.json",
    {
        "batch": "B05h",
        "image_origin": "Wellcome Collection IIIF b30338724, original 1647 edition",
        "status": "PAGE_ORDER_VISUALLY_CHECKED_FROM_ORIGINAL",
        "pdf_to_printed_note": (
            "PDF580 printed538 follows PDF579 printed545 without a text break; PDF581 "
            "printed539 follows. Apparent typographical pagination regression; do not "
            "reorder images by printed folio."
        ),
        "pages": evidence,
        "original_pdf_sha256": "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
    },
)
write(
    "SOURCE_TO_RECORD_REVERSE_MAP.json",
    {"batch": "B05h", "source_passages": reverse, "source_passage_count": 12, "record_count": 53},
)
write(
    "RULES.json",
    {
        "batch": "B05h",
        "status": "ORIGINAL_1647_HISTORICAL_DOCUMENTARY_ADMITTED",
        "printed_chapter": "CIX",
        "editorial_chapter": "CX",
        "record_count": 53,
        "first_record": "R6592",
        "last_record": "R6644",
        "source_passages": 12,
        "substantive_historical_records": 50,
        "following_chapter_navigation": 3,
        "original_pdf_body": [577, 578, 579, 580],
        "context_pdf_page": 581,
        "full_diplomatic_transcription": False,
        "clinical_or_intelligence_predictive_validation": 0,
        "empirical_validations": 0,
        "runtime_promotions": 0,
        "rules": rule_rows,
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05h",
        "not_authorized_for_personality_or_medical_claims": True,
        "issues": [
            (
                "Original print PDF580 folio is visibly 538 after printed545; PDF581 folio "
                "is 539. Scan/text order remains continuous. Modern transcription normalizes "
                "folio as 546/547; original ambiguity preserved."
            ),
            (
                "Modern retype is used only as secondary reading support; primary evidence "
                "and glyphs are the original 1647 scans."
            ),
            (
                "No full diplomatic first-edition transcription, exact Latin-cross-source "
                "reconciliation, or expert 17th-century paleographic review completed."
            ),
            (
                "All cognitive, intellectual-disability, speech-impairment and "
                "moral-character attributions are historical stereotypes with no "
                "demonstrated clinical or predictive validity."
            ),
            (
                "Mercury–Moon favorable conjunction and adverse instability mixture refer to "
                "different conditional contexts and must not be merged into one "
                "unconditional claim."
            ),
            (
                "The source's phrase 'any Signe but Pisces and Scorpio' follows "
                "own-domicile/angle conditions; operator-level logical parsing may require a "
                "separate expert reading before computational implementation."
            ),
            (
                "Humoral temperament stereotypes are not measurements or reliable predictors "
                "of learning or inventiveness."
            ),
            (
                "No human birth times or life histories were used to select, fit, or "
                "validate these annotations; no runtime scoring rule promoted."
            ),
        ],
    },
)
accepted = {
    "batch": "B05h",
    "status": "LOCALLY_FROZEN_SOURCE_DOCUMENTARY_NOT_EMPIRICAL_VALIDATION",
    "prior_lilly": 6591,
    "historical_source_annotations_added": 53,
    "lilly_if_published": 6644,
    "ptolemy_retained": 1066,
    "combined_if_published": 7710,
    "original_pdf_pages": [577, 578, 579, 580, 581],
    "source_groups": 12,
    "substantive_claims": 50,
    "next_chapter_navigation": 3,
    "next_printed_chapter": "CX",
    "next_editorial_chapter": "CXI",
    "next_original_pdf_page": 580,
    "next_printed_page_as_seen": "538 (expected 546; apparent misprint)",
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "independent_personality_validations": 0,
    "independent_intelligence_validations": 0,
    "medical_or_disability_validations": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "limitations_file": "UNRESOLVED_SOURCE_LIMITS.json",
    "published_to_remote": False,
}
write("ACCEPTANCE.json", accepted)
print(json.dumps(accepted, indent=2))
