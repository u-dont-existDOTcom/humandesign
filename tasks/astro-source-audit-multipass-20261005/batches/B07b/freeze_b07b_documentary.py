#!/usr/bin/env python3
"""Freeze 1647 Lilly CXLVIII vocational Magistery source-only annotations."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, value):
    (B / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261018.json")
assert a["batch"] == "B07b"
assert a["printed_chapter"] == "CXLVIII"
assert a["body_original_pdf_frames"] == [658, 659, 660]
assert a["next_printed"] == "CXLIX"
assert a["next_heading_frame"] == 660
assert len(a["groups"]) == 6

rules, reverses = [], []
for i, group in enumerate(a["groups"], 1):
    sid = f"B07b-S{i:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {658, 659, 660}
    ids = []
    for c in group["clauses"]:
        no = 9445 + len(rules)
        rid = f"R{no}"
        assert c["id"] == rid
        assert len(c["source_anchor_not_diplomatic"]) >= 5
        assert len(c["historical_meaning_only"]) >= 42
        assert c["source_only"] and not c["real_human_vocation_accuracy_validated"]
        assert not c["real_person_occupation_moral_inference_authorized"]
        assert not c["runtime_promoted"]
        rules.append(
            {
                "id": rid,
                "record_number": no,
                "batch": "B07b",
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": c["role"],
                "source_anchor_not_diplomatic": c["source_anchor_not_diplomatic"],
                "historical_meaning_only": c["historical_meaning_only"],
                "qualification": c["qualification"],
                "documentary_source_accepted": True,
                "independent_real_profession_occurrence_validated": False,
                "independent_real_occupation_category_validated": False,
                "independent_real_professional_fame_or_income_validated": False,
                "source_ptolemy_original_cross_collated": False,
                "person_level_employment_or_moral_forecast_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    reverses.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rules) == 82
assert [x["record_number"] for x in rules] == list(range(9445, 9527))
assert [x["id"] for x in rules if x["role"] == "next_chapter_navigation"] == ["R9525", "R9526"]
assert len({x["id"] for x in rules}) == 82

images = {}
for n in range(658, 663):
    file = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(file.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(file),
        "printed_folio": str(n - 34),
        "source_role": (
            "CXLVIII_profession_definition_and_selection"
            if n <= 660
            else "following_CXLIX_occupation_aphorisms_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07b",
        "original_source": (
            "William Lilly Christian Astrology first edition 1647 Wellcome Collection b30338724"
        ),
        "source_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": [658, 659, 660],
        "following_printed_CXLIX_heading_pdf": 660,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07b",
        "source_groups": reverses,
        "source_group_count": 6,
        "records_count": 82,
        "substantive": 80,
        "navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07b",
        "issues": [
            (
                "The author defines Magistery broadly as a principal "
                "lifetime pursuit, studied art, delight, action, "
                "livelihood or reputation source, not strictly "
                "paid employment. Modern occupation codes "
                "do not transparently implement this construct."
            ),
            (
                "Three explicitly different questions are whether "
                "any profession exists, which type of profession, "
                "and what success/fame follows. Success in "
                "one must not rescue a miss in another."
            ),
            (
                "Mars, Venus and Mercury each have different "
                "source associations with bodily stamina, "
                "delight and mind. Planet identity alone "
                "does not meet first-tier eligibility."
            ),
            (
                "First tier requires tenth/first/seventh position "
                "and essential dignity while excluding "
                "combustion and being under Sun beams."
            ),
            (
                "The fallback to one of the three candidates "
                "ruling Midheaven still requires essential "
                "dignity; peregrine or fall excludes it."
            ),
            (
                "Next selection uses partile Moon aspects, "
                "strongest planet, aspect quality, partility "
                "and explicit sinister-before-dexter "
                "priority, needing original aspect algorithms."
            ),
            (
                "The following Moon-orb fallback appears to "
                "refer again to none of the three planets "
                "aspecting Moon and then selects one aspecting "
                "Moon within half-orb; literal wording is "
                "self-ambiguous. Preserve rather than repair."
            ),
            (
                "Moon-orb method rejects malignant corporal "
                "conjunction, square or opposition; the source "
                "does not provide modern orb weights."
            ),
            (
                "The last source fallback selects from "
                "candidate planets anteceding the Sun according "
                "to the first mover; original astronomical "
                "operator/time ordering is not fully verified."
            ),
            (
                "Negative source says weaker fallback-selected "
                "planets may show ignoble profession, negligence "
                "or no art, which are different outcomes "
                "and reflect historic class stigma."
            ),
            (
                "Lilly also describes an autobiographical "
                "method using tenth sign, its ruler and "
                "the ruler's house, not an independently "
                "registered trial or proven method."
            ),
            (
                "Ptolemy-attributed Sun/morning-riser and "
                "Midheaven ruler/occupant two-way method "
                "with Moon aspect is historically distinct "
                "and has NOT been cross-collated with the "
                "original Ptolemaic passage."
            ),
            (
                "The Ptolemy-attributed fallback accepts "
                "a planet meeting only one of the two source "
                "roles, lowering specificity, without "
                "predeclared tie/failure policy."
            ),
            (
                "The next separately numbered CXLIX "
                "experimental profession aphorisms begins "
                "after divider on same PDF660; no CXLIX "
                "substantive content admitted in this packet."
            ),
            (
                "No reliable real human birth-time, vocation "
                "timeline, main activity, profession, objective "
                "income, comparison chart or control dataset "
                "was used to validate any career claim."
            ),
            (
                "The packet is short photographed first-edition "
                "anchor/paraphrase documentation, not a "
                "complete seventeenth-century diplomatic "
                "transcription or executable scoring rule."
            ),
        ],
        "original_profession_selection_algorithm_complete": False,
        "ptolemy_profession_rules_crosscollated": False,
        "real_person_occupation_or_fame_accuracy_validated": 0,
        "actual_person_professional_moral_labels_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07b",
        "status": "ORIGINAL_1647_CXLVIII_PROFESSION_DEFINITION_AND_SELECTION_SOURCE_ONLY",
        "printed_chapter": "CXLVIII",
        "record_count": 82,
        "first_record": "R9445",
        "last_record": "R9526",
        "substantive": 80,
        "following_navigation": 2,
        "source_groups": 6,
        "body_original_pdf_frames": [658, 659, 660],
        "next_printed_chapter": "CXLIX",
        "following_heading_pdf": 660,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "real_profession_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07b",
        "status": "FIRST_EDITION_CXLVIII_MAGISTERY_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 9444,
        "new_historical_annotations": 82,
        "lilly_if_published": 9526,
        "ptolemy_retained": 1066,
        "combined_if_published": 10592,
        "substantive": 80,
        "navigation": 2,
        "source_groups": 6,
        "new_numbered_chapters": 1,
        "next_printed_chapter": "CXLIX",
        "next_original_pdf": 660,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "real_human_vocation_accuracy_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original CXLVIII profession historical source 82 annotations R9445–R9526")
