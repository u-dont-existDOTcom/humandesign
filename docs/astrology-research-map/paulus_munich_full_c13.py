"""C13: source-specific comparison of visually transcribed Munich MS positions.

119 glyph identifications + 1 unknown are input evidence; neither
an eightfold nor a sevenfold algorithm is used to fill the observed data.
Comparison to C04/C05 is source fidelity, NOT human predictive validation.
"""
from __future__ import annotations
import json
from pathlib import Path

from paulus_monomoiria_source_c04 import (
    ZODIAC, edited_day_degree_ruler, triplicity_for_sign
)
from paulus_trigon_narrative_c05 import (
    narrative_degree_ruler, TRIGON_ORDER
)

EVIDENCE=Path(__file__).with_name("PAULUS_C13_MUNICH_120_POSITION_IMAGE_TRANSCRIPTION_V1.json")


def manuscript_source():
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def observed_glyph_assignment(trigon: str, ordinal_degree: int):
    src=manuscript_source()
    if trigon not in TRIGON_ORDER:
        raise ValueError("unknown source trigon")
    if type(ordinal_degree) is not int or not (1<=ordinal_degree<=30):
        raise ValueError("ordinal degree must be integer from 1 through 30")
    return src["observed_degrees_1_to_30"][trigon][ordinal_degree-1]


def naive_eight_step_hypothesis(trigon: str, ordinal_degree: int):
    """Falsifiable periodicity diagnostic, never a substitution for observed glyphs."""
    src=manuscript_source()
    if trigon not in TRIGON_ORDER or type(ordinal_degree) is not int or not (1<=ordinal_degree<=30):
        raise ValueError("invalid trigon or ordinal")
    return src["observed_degrees_1_to_30"][trigon][(ordinal_degree-1)%8]


def manuscript_model_comparison():
    src=manuscript_source()
    rows=[]
    for tri in TRIGON_ORDER:
        sign=src["trigon_signs"][tri][0]
        assert sign in ZODIAC and triplicity_for_sign(sign)==tri
        for degree in range(1,31):
            observed=observed_glyph_assignment(tri,degree)
            n=narrative_degree_ruler(sign,degree,sect="day")
            p=edited_day_degree_ruler(sign,degree,sect="day")
            hypothesis=naive_eight_step_hypothesis(tri,degree)
            rows.append({
                "trigon":tri,"degree":degree,"first_sign":sign,
                "observed":observed,"narrative_seven_unique_day":n,
                "greenbaum_printed_corrected_day":p,
                "naive_eightfold_extrapolation":hypothesis,
                "prior_day_canon_disputed":n!=p,
                "observed_narrative_agreement":None if observed is None else observed==n,
                "observed_corrected_agreement":None if observed is None else observed==p,
                "observed_eightfold_agreement":None if observed is None else observed==hypothesis
            })
    by_tri={}
    for tri in TRIGON_ORDER:
        subset=[r for r in rows if r["trigon"]==tri]
        certain=[r for r in subset if r["observed"] is not None]
        by_tri[tri]={
            "total_positions":30,
            "read_positions":len(certain),
            "unresolved_positions":[r["degree"] for r in subset if r["observed"] is None],
            "eightfold_extrapolation_mismatch_degrees":[r["degree"] for r in certain if r["observed"]!=r["naive_eightfold_extrapolation"]],
            "narrative_agreements":sum(r["observed_narrative_agreement"] for r in certain),
            "greenbaum_agreements":sum(r["observed_corrected_agreement"] for r in certain)
        }
    disputed=[r for r in rows if r["prior_day_canon_disputed"]]
    certain_disputed=[r for r in disputed if r["observed"] is not None]
    direct={
        "previous_narrative_greenbaum_dispute_universe":len(disputed),
        "disputed_source_observations_read":len(certain_disputed),
        "disputed_with_unread_manuscript":[(r["trigon"],r["degree"]) for r in disputed if r["observed"] is None],
        "disputed_source_agrees_narrative_only":sum(r["observed"]==r["narrative_seven_unique_day"] for r in certain_disputed),
        "disputed_source_agrees_corrected_only":sum(r["observed"]==r["greenbaum_printed_corrected_day"] for r in certain_disputed),
        "disputed_source_agrees_neither":sum(r["observed"] not in (r["narrative_seven_unique_day"],r["greenbaum_printed_corrected_day"]) for r in certain_disputed)
    }
    return {
        "kind":"SOURCE_RECONSTRUCTION_DIVERSITY_NOT_BLINDED_HUMAN_VALIDATION",
        "ordinal_span":[1,30],"total_source_positions":len(rows),
        "read":sum(r["observed"] is not None for r in rows),
        "unread":sum(r["observed"] is None for r in rows),
        "by_trigon":by_tri,
        "previous_34_disputed":direct,
        "eightfold_hypothesis_is_admitted_canon":False,
        "production_scoring_changed":False,
        "human_predictive_validations":0,
        "rows":rows
    }


if __name__=="__main__":
    print(json.dumps(manuscript_model_comparison(),indent=2))
