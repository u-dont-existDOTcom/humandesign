#!/usr/bin/env python3
"""Original Lilly second sibling-number method; documentary only, not demographic fact."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


author = j("SOURCE_FIRST_AUTHORING_20261017.json")
assert author["batch"] == "B05v"
assert author["printed_chapter"] == "CXXI"
assert author["source_body_pdf_frame"] == 602
assert len(author["groups"]) == 8
records, reverse = [], []
for index, group in enumerate(author["groups"], 1):
    sid = f"B05v-S{index:03d}"
    assert sid == group["source_span"]
    assert set(group["original_pdf_frames"]) <= {602, 603}
    ids = []
    for claim in group["clauses"]:
        no = 7253 + len(records)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["anchor_not_diplomatic"]) >= 9
        assert len(claim["meaning_historical_only"]) >= 50
        assert not claim["independent_sibling_count_validated"]
        assert not claim["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "anchor_not_diplomatic": claim["anchor_not_diplomatic"],
                "historical_only_meaning": claim["meaning_historical_only"],
                "source_qualification": claim["qualification"],
                "source_documentation_accepted": True,
                "independent_sibling_birth_count_validated": False,
                "human_fertility_or_sex_prediction_validated": False,
                "human_longevity_or_death_prediction_validated": False,
                "original_ptolemy_text_independently_verified": False,
                "clinical_or_personal_actions_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["scope"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 43
assert [r["record_number"] for r in records] == list(range(7253, 7296))
assert [r["id"] for r in records if r["role"] == "next_section_navigation"] == ["R7294", "R7295"]
assert len({r["id"] for r in records}) == 43
witness = {}
for n in (602, 603, 604, 605):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    data = p.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 180000
    witness[str(n)] = {
        "path": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(data),
        "original_printed_page": str(n - 34),
        "role": "chapter_body" if n == 602 else "later_fourth_house_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05v",
        "source": (
            "William Lilly Christian Astrology original first edition 1647, Wellcome b30338724"
        ),
        "complete_pdf_sha256": ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"),
        "body_pdf_page": 602,
        "following_unnumbered_fourth_house_pdf_page": 603,
        "following_printed_CXXII_pdf_page": 604,
        "images": witness,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05v",
        "source_groups": reverse,
        "record_count": 43,
        "substantive": 41,
        "next_section_navigation": 2,
        "source_passages": 8,
    },
)
limitations = [
    "The alternative sibling-number CXXI and earlier CXVIII are distinct "
    "historic methods; their overlap does not create independent experimental replication.",
    "The male/female zodiac-sign attribution to actual brothers and sisters "
    "is a historical classification, not scientific sex prediction.",
    "Aspected planets are said to indicate sibling number, but the original "
    "does not define the orb/exact eligibility and duplicate counting policies.",
    "Harmful claims of younger-sibling mortality or shortened life are "
    "unverified, high-stakes assertions and cannot be applied to actual families.",
    "The third-lord/Sun-Jupiter opposition phrase has ambiguous grammatical "
    "antecedents and must not become a deterministic prediction without review.",
    "Birth-order versus best-living-sibling is an explicit either/or "
    "alternative, increasing post-hoc opportunities to rescue a failed forecast.",
    "Lilly's purported Ptolemy method is an attribution by Lilly and "
    "must be reconciled against original Ptolemy texts separately.",
    "The author's suggestion that Ptolemy's approach may work for "
    "siblings from the same mother is a new scope qualification, not a verified observation.",
    "The claim that Ptolemy lacked Greek, Jewish, Arabic and Latin support "
    "is a historical authority dispute and not independent validation.",
    "The Latin maxim at the end of the chapter has not been subject "
    "to a complete specialist 17th-century diplomatic transcription.",
    "No complete natal datasets, true sibling counts, survival histories, "
    "birth-time checks, fertility/infant mortality or prospective control cohorts are provided.",
    "Next original PDF603 starts an unnumbered fourth-house parent/patrimony "
    "intro; its clauses belong to a separate archival batch, not CXXI.",
]
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05v",
        "issues": limitations,
        "actual_person_predictions_validated": 0,
        "medical_fertility_or_mortality_claims_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B05v",
        "status": "ORIGINAL_1647_PTOLEMY_SIBLING_METHOD_CONTRAST_HISTORICAL_ONLY",
        "printed_chapter": "CXXI",
        "editorial_chapter": "CXXII",
        "record_count": 43,
        "first_record": "R7253",
        "last_record": "R7295",
        "source_group_count": 8,
        "substantive_historical_claims": 41,
        "following_source_navigation": 2,
        "source_body_pdf": 602,
        "next_unnumbered_pdf": 603,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "actual_sibling_births_or_deaths_validated": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B05v",
        "previous_lilly": 7252,
        "new_historical_annotations": 43,
        "lilly_if_published": 7295,
        "ptolemy_retained": 1066,
        "combined_if_published": 8361,
        "substantive": 41,
        "navigation": 2,
        "source_groups": 8,
        "next_source": "UNNUMBERED_FOURTH_HOUSE_PARENTS_PATRIMONY",
        "next_original_pdf": 603,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "independent_ptolemy_original_crosscheck": False,
        "empirical_validations": 0,
        "independent_human_demographic_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B05v original historic sibling contrast R7253–R7295, no tested human predictions")
