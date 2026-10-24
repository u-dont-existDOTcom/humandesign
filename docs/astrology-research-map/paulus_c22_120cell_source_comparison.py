"""C22: full 120-cell source-fidelity comparison; absolutely no natal scoring.

Disparate evidence layers are held separate:
- candidate glyph identifications from C15 Vatican manuscript photos,
- a printed corrected diurnal table interpreted in C04 from Greenbaum,
- the C05 interpretive no-duplicate Greek prose algorithm.
The counts below are not independent human/behavioral tests and do not prove
the Vatican/Florence/Munich glyph transcriptions are independently correct.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import json

from paulus_c15_three_manuscript_comparison import three_manuscript_comparison
from paulus_trigon_narrative_c05 import narrative_degree_ruler, TRIGON_ORDER
from paulus_monomoiria_source_c04 import edited_day_degree_ruler

EVIDENCE=Path(__file__).with_name(
    "PAULUS_C22_COMPLETE_120_SOURCE_COMPARISON_PROVENANCE_V1.json"
)
FIRST_SIGN={"fire":"Aries","earth":"Taurus","air":"Gemini","water":"Cancer"}
CATEGORIES=("both","narrative_only","greenbaum_only","neither")


def provenance():
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def compare_all_120():
    source=provenance()
    prior=three_manuscript_comparison()
    rows=[]
    for x in prior["rows"]:
        trigon=x["trigon"]
        degree=x["ordinal_degree"]
        ms=x["vatican_observed"]
        sign=FIRST_SIGN[trigon]
        narrative=narrative_degree_ruler(sign,degree,sect="day")
        printed=edited_day_degree_ruler(sign,degree,sect="day")
        nighttime=narrative_degree_ruler(sign,degree,sect="night")
        assert narrative==x["c05_narrative_sevenfold_day"]
        assert printed==x["c04_greenbaum_sevenfold_day"]
        cat=("both" if ms==narrative==printed
             else "narrative_only" if ms==narrative
             else "greenbaum_only" if ms==printed
             else "neither")
        rows.append({
            "trigon":trigon,"ordinal_degree":degree,
            "manuscript_label":ms,
            "narrative_day":narrative,
            "greenbaum_printed_day":printed,
            "narrative_night_diagnostic":nighttime,
            "category":cat,
            "two_sevenfold_day_sources_disagree":narrative!=printed,
            "manuscript_matches_narrative_night":ms==nighttime,
            "manuscript_Munich_label":x["munich_observed"],
            "manuscript_Florence_label":x["florence_observed"],
            "source_certification_level":"PROVISIONAL_MANUSCRIPT_GLYPH",
        })
    assert len(rows)==120
    total=Counter(r["category"] for r in rows)
    per_trigon={
        tri:{cat:sum(r["trigon"]==tri and r["category"]==cat for r in rows)
             for cat in CATEGORIES}
        for tri in TRIGON_ORDER
    }
    old_dispute=[r for r in rows if r["two_sevenfold_day_sources_disagree"]]
    undisputed=[r for r in rows if not r["two_sevenfold_day_sources_disagree"]]
    assert len(old_dispute)==34 and len(undisputed)==86
    return {
        "audit_type":"FULL_SOURCE_CANDIDATE_TABLE_NOT_HUMAN_PREDICTION",
        "physical_photo_candidate_positions":len(rows),
        "category_counts":{cat:total[cat] for cat in CATEGORIES},
        "category_per_trigon":per_trigon,
        "manuscript_vs_narrative_day_matches":sum(
            r["manuscript_label"]==r["narrative_day"] for r in rows
        ),
        "manuscript_vs_greenbaum_day_matches":sum(
            r["manuscript_label"]==r["greenbaum_printed_day"] for r in rows
        ),
        "manuscript_vs_narrative_night_matches":sum(
            r["manuscript_matches_narrative_night"] for r in rows
        ),
        "previously_disputed_34":{
            "total":len(old_dispute),
            "narrative_only":sum(r["category"]=="narrative_only" for r in old_dispute),
            "greenbaum_only":sum(r["category"]=="greenbaum_only" for r in old_dispute),
            "neither":sum(r["category"]=="neither" for r in old_dispute)
        },
        "previously_agreed_day_sources_86":{
            "total":len(undisputed),
            "manuscript_agrees_both":sum(r["category"]=="both" for r in undisputed),
            "manuscript_disagrees_both":sum(r["category"]=="neither" for r in undisputed),
        },
        "Munich_readable_compared":sum(r["manuscript_Munich_label"] is not None for r in rows),
        "source_status":"NO_BLINDED_PALEOGRAPHY_OR_INDEPENDENT_TEXTUAL_FAMILY_PROVEN",
        "manuscript_explicit_day_night_rubric_certified":False,
        "Boer_1958_Greek_critical_table_apparatus_inspected":False,
        "production_rule_promoted":False,
        "human_predictive_validations":0,
        "rows":rows,
    }


if __name__=="__main__":
    print(json.dumps(compare_all_120(),ensure_ascii=False,indent=2))
