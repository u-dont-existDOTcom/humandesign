"""C29: source-only Hellenistic monomoiria candidate registry and contrasts.

NO natal biography, timing forecast, empirical score, or production promotion.
All matrices are documentary reconstructions with source-specific status.
A reproducible matrix is NOT an empirical validation or a frozen prediction.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from paulus_bysign_papyrus_c04 import sign_monomoiria
from paulus_monomoiria_source_c04 import (
    ZODIAC, edited_day_degree_ruler, triplicity_for_sign,
)
from paulus_trigon_narrative_c05 import narrative_degree_ruler, TRIGON_ORDER
from paulus_c24_complete_240_source_comparison import complete_provisional_240
from paulus_c22_120cell_source_comparison import compare_all_120

ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT / "HELLENISTIC_C29_DOCUMENTARY_VARIANT_MATRIX_V1.json"

FIRST_SIGN = {"fire": "Aries", "earth": "Taurus",
              "air": "Gemini", "water": "Cancer"}
SOURCE_PATHS = (
    "paulus_bysign_papyrus_c04.py",
    "paulus_monomoiria_source_c04.py",
    "paulus_trigon_narrative_c05.py",
    "paulus_c24_complete_240_source_comparison.py",
    "paulus_c22_120cell_source_comparison.py",
    "PAULUS_C24_COMMENTARY_120_FIRST_80_SECOND_SOURCE_V1.json",
    "PAULUS_C24_COMMENTARY_FULL_SECOND_120_V1.json",
    "PAULUS_C22_COMPLETE_120_SOURCE_COMPARISON_PROVENANCE_V1.json",
    "PAULUS_C21_GREEK_SECT_LIGHT_CLAUSES_V1.json",
    "HELIODORUS_C28_KROLL_CODEX_IDENTITY_V1.json",
)

# A candidate's output domain matters at least as much as its planet names.
# Do not infer day/night column semantics from a figure's *shape*.
CANDIDATES = (
    {
        "id": "CH5_BY_SIGN_CHALDEAN",
        "domain": "each zodiac sign and physical completed degree 0..29",
        "source_layer": "Paulus ch5 Greek prose and C04 papyrus comparison",
        "role": "computable documentary method",
        "sect": "not a day/night table",
        "row_count": 360,
        "source_support": "Greek prose with historically observed negative Mercury case",
        "eligible_as_verified_human_outcome_model": False,
    },
    {
        "id": "CH32_GREEK_NARRATIVE_DAY",
        "domain": "four trigons, thirty ordinal degrees of the DAY light of sect",
        "source_layer": "C21 Paulus Greek ch32 plus C05 no-duplicate reconstruction",
        "role": "interpreted computational candidate",
        "sect": "day",
        "row_count": 120,
        "source_support": "prose reconstruction, not certified original table",
        "eligible_as_verified_human_outcome_model": False,
    },
    {
        "id": "CH32_GREEK_NARRATIVE_NIGHT",
        "domain": "four trigons, thirty ordinal degrees of the NIGHT light of sect",
        "source_layer": "C21 Paulus Greek ch32 plus C05 reversed trigon order",
        "role": "interpreted computational candidate",
        "sect": "night",
        "row_count": 120,
        "source_support": "nighttime prose reconstruction, NOT Florence second slot",
        "eligible_as_verified_human_outcome_model": False,
    },
    {
        "id": "CH32_GREENBAUM_EDITED_DAY",
        "domain": "four trigons, thirty ordinal degrees of the DAY light of sect",
        "source_layer": "C04 Greenbaum corrected printed table, p67",
        "role": "editorial computational candidate",
        "sect": "day",
        "row_count": 120,
        "source_support": "modern editorial correction, not ancient autograph",
        "eligible_as_verified_human_outcome_model": False,
    },
    {
        "id": "FLORENCE_COMMENTARY_FIRST_SLOT",
        "domain": "four trigons, thirty ordinal degrees, FIRST figure glyph slot",
        "source_layer": "C24 Florence Plut.28.14 f204v original-photo candidates",
        "role": "nonblind manuscript-glyph record, NOT algorithm",
        "sect": "UNKNOWN",
        "row_count": 120,
        "source_support": "provisional single-reader glyph normalization",
        "eligible_as_verified_human_outcome_model": False,
    },
    {
        "id": "FLORENCE_COMMENTARY_SECOND_SLOT",
        "domain": "four trigons, thirty ordinal degrees, SECOND figure glyph slot",
        "source_layer": "C24 Florence Plut.28.14 f204v original-photo candidates",
        "role": "nonblind manuscript-glyph record, NOT nighttime algorithm",
        "sect": "UNKNOWN",
        "row_count": 120,
        "source_support": "pair-swap pattern diagnostic not paleographic validation",
        "eligible_as_verified_human_outcome_model": False,
    },
    {
        "id": "OLDER_PAULUS_VATICAN_PHOTO",
        "domain": "four trigons, thirty ordinal degrees, C15 source candidate",
        "source_layer": "C15/C22 photographed Paulus manuscript family",
        "role": "nonblind manuscript-glyph record, NOT algorithm",
        "sect": "UNKNOWN",
        "row_count": 120,
        "source_support": "source family dependence and 96/120 neither-day retained",
        "eligible_as_verified_human_outcome_model": False,
    },
    {
        "id": "VIENNA_115_STRUCTURAL_ONLY",
        "domain": "Vienna Cod. phil. gr.115 f205v figure",
        "source_layer": "C25/C26/C27 table photographed; 15+15 provisional numbers",
        "role": "table identity/layout only, no certified glyph values",
        "sect": "UNKNOWN",
        "row_count": 0,
        "source_support": "no independent planet glyph collation or day/night rubric",
        "eligible_as_verified_human_outcome_model": False,
    },
    {
        "id": "VIENNA_108_CATALOGUE_ONLY",
        "domain": "Vienna Cod. phil. gr.108 f159v",
        "source_layer": "C28-corrected Kroll CCAG VI printed pp1-2",
        "role": "catalogued witness only, not a table reconstruction",
        "sect": "UNKNOWN",
        "row_count": 0,
        "source_support": "original folio image not examined; C27 codex error superseded",
        "eligible_as_verified_human_outcome_model": False,
    },
)

def _digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True,
                   separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def build_documentary_matrix() -> dict:
    """Materialize source contrasts; never select a 'winning' historical rule."""
    photo = complete_provisional_240()
    older = compare_all_120()
    a = {(r["trigon"], r["ordinal_degree"]): r for r in photo["rows"]}
    b = {(r["trigon"], r["ordinal_degree"]): r for r in older["rows"]}
    if len(a) != 120 or len(b) != 120:
        raise AssertionError("expected 120 independently stored rows per source")

    rows = []
    for trigon in TRIGON_ORDER:
        sign = FIRST_SIGN[trigon]
        for degree in range(1, 31):
            x = a[(trigon, degree)]
            y = b[(trigon, degree)]
            narrative_day = narrative_degree_ruler(sign, degree, sect="day")
            edited_day = edited_day_degree_ruler(sign, degree, sect="day")
            narrative_night = narrative_degree_ruler(sign, degree, sect="night")
            if (narrative_day != y["narrative_day"]
                or edited_day != y["greenbaum_printed_day"]
                or narrative_night != y["narrative_night_diagnostic"]):
                raise AssertionError("prior source calculations changed")
            rows.append({
                "trigon": trigon,
                "ordinal_degree": degree,
                "representative_sign": sign,
                "CH32_GREEK_NARRATIVE_DAY": narrative_day,
                "CH32_GREEK_NARRATIVE_NIGHT": narrative_night,
                "CH32_GREENBAUM_EDITED_DAY": edited_day,
                "FLORENCE_COMMENTARY_FIRST_SLOT": x["first_slot"],
                "FLORENCE_COMMENTARY_SECOND_SLOT": x["second_slot"],
                "OLDER_PAULUS_VATICAN_PHOTO": y["manuscript_label"],
            })

    by_sign = [
        {
            "sign": sign,
            "completed_degrees": completed_degree,
            "ordinal_degree": completed_degree + 1,
            "CH5_BY_SIGN_CHALDEAN": sign_monomoiria(
                sign, completed_degree, 0),
        }
        for sign in ZODIAC for completed_degree in range(30)
    ]

    summary = {
        "trigon_rows": len(rows),
        "by_sign_rows": len(by_sign),
        "Greek_day_vs_Greenbaum_edited_day_disagreements": sum(
            r["CH32_GREEK_NARRATIVE_DAY"] != r["CH32_GREENBAUM_EDITED_DAY"]
            for r in rows),
        "Florence_first_vs_Greek_day_matches": sum(
            r["FLORENCE_COMMENTARY_FIRST_SLOT"] == r["CH32_GREEK_NARRATIVE_DAY"]
            for r in rows),
        "Florence_first_vs_Greenbaum_day_matches": sum(
            r["FLORENCE_COMMENTARY_FIRST_SLOT"] == r["CH32_GREENBAUM_EDITED_DAY"]
            for r in rows),
        "Florence_second_vs_Greek_night_matches": sum(
            r["FLORENCE_COMMENTARY_SECOND_SLOT"] == r["CH32_GREEK_NARRATIVE_NIGHT"]
            for r in rows),
        "Florence_second_adjacent_pair_swap_matches": sum(
            rows[i]["FLORENCE_COMMENTARY_SECOND_SLOT"] ==
            rows[i+1]["FLORENCE_COMMENTARY_FIRST_SLOT"] if
            rows[i]["ordinal_degree"] % 2 == 1 else
            rows[i]["FLORENCE_COMMENTARY_SECOND_SLOT"] ==
            rows[i-1]["FLORENCE_COMMENTARY_FIRST_SLOT"]
            for i in range(120)),
        "Older_Paulus_vatican_matches_neither_day": sum(
            r["OLDER_PAULUS_VATICAN_PHOTO"] not in (
                r["CH32_GREEK_NARRATIVE_DAY"],
                r["CH32_GREENBAUM_EDITED_DAY"]) for r in rows),
    }
    expected = (120, 360, 34, 104, 102, 48, 120, 96)
    if tuple(summary.values()) != expected:
        raise AssertionError(("C29 source mismatch", summary, expected))
    return {
        "schema": "HUMANDESIGN_C29_DOCUMENTARY_MONOMOIRIA_VARIANTS_V1",
        "root_goal_status": "OPEN",
        "scientific_role": "DOCUMENTARY_COMPUTATIONS_ONLY_NOT_HUMAN_PREDICTION",
        "parent_commit": "b784a5782af89b773deaa5ddd640e90ca237178a",
        "source_input_sha256": {
            filename: hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()
            for filename in SOURCE_PATHS
        },
        "variants": list(CANDIDATES),
        "summary": summary,
        "trigon_rows": rows,
        "by_sign_rows": by_sign,
        "unresolved_separate_timing_family": {
            "Hephaistio_II_periods": "literal 40 vs derived 140 vs main 150; 360/365/375 also source-divergent",
            "production_timing_prediction_available": False,
        },
        "gates": {
            "ruler_data_not_behavioral_outcome_mapping": True,
            "C21_ch32_restricted_to_sect_light": True,
            "unknown_photo_slot_sect_not_inferred": True,
            "C28_codex_108_115_distinction_preserved": True,
            "no_auto_selection_or_weighted_ensemble": True,
            "Boer_1962_apparatus_still_unread": True,
            "human_predictive_validations": 0,
            "production_scoring_modified": False,
            "input_dates_or_life_events_used": False,
            "next": "Identify person-specific outcome rules for this feature, freeze interpretations and measurement BEFORE collecting untouched participant answers.",
        },
    }


def frozen_source_snapshot() -> dict:
    body = build_documentary_matrix()
    return {**body, "documentary_matrix_sha256": _digest(body)}


if __name__ == "__main__":
    print(json.dumps(frozen_source_snapshot(), ensure_ascii=False,
                     sort_keys=True, indent=2))
