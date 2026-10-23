"""C15 source-critical comparison of Vatican, Florence and Munich Paulus tables.

Visual source arrays remain independent data inputs. This compares historical
textual witnesses only; it never validates a horoscope or chooses a production rule.
"""
from __future__ import annotations
import json
from pathlib import Path

from paulus_florence_munich_comparison_c14 import florence_source
from paulus_munich_full_c13 import manuscript_source
from paulus_trigon_narrative_c05 import TRIGON_ORDER, narrative_degree_ruler
from paulus_monomoiria_source_c04 import edited_day_degree_ruler

ROOT=Path(__file__).resolve().parent
VAT_PATH=ROOT/"PAULUS_C15_VATICAN_120_POSITION_SOURCE_WITNESS_V1.json"


def vatican_source():
    return json.loads(VAT_PATH.read_text(encoding="utf-8"))


def three_manuscript_comparison():
    vat=vatican_source()
    flo=florence_source()
    mun=manuscript_source()
    rows=[]
    for tri in TRIGON_ORDER:
        sign=vat["trigon_signs"][tri][0]
        for degree in range(1,31):
            i=degree-1
            v=vat["independent_source_observed_planetary_degree_1_to_30"][tri][i]
            f=flo["observed_degrees_1_to_30"][tri][i]
            m=mun["observed_degrees_1_to_30"][tri][i]
            narrative=narrative_degree_ruler(sign,degree,sect="day")
            print_d=edited_day_degree_ruler(sign,degree,sect="day")
            by_eight=vat["independent_source_observed_planetary_degree_1_to_30"][tri][i%8]
            rows.append({
                "trigon":tri,"ordinal_degree":degree,
                "vatican_observed":v,"florence_observed":f,"munich_observed":m,
                "vatican_florence_match":v==f,
                "vatican_munich_match":None if m is None else v==m,
                "manuscript_eightfold_extrapolation_match":v==by_eight,
                "c04_greenbaum_sevenfold_day":print_d,
                "c05_narrative_sevenfold_day":narrative,
                "was_among_34_preexisting_disputed":narrative!=print_d
            })
    inspected_munich=[r for r in rows if r["munich_observed"] is not None]
    changed=[r for r in rows if not r["manuscript_eightfold_extrapolation_match"]]
    disputed=[r for r in rows if r["was_among_34_preexisting_disputed"]]
    source_only={
        "three_physical_manuscripts_consulted":3,
        "independent_manuscript_text_families_proved":0,
        "vatican_glyphs_read":len(rows),
        "florence_glyphs_read":len(rows),
        "munich_readable_glyphs":len(inspected_munich),
        "vatican_florence_agree":sum(r["vatican_florence_match"] for r in rows),
        "vatican_munich_agree":sum(r["vatican_munich_match"] for r in inspected_munich),
        "vatican_munich_disagree":[(r["trigon"],r["ordinal_degree"]) for r in inspected_munich if not r["vatican_munich_match"]],
        "munich_unread_but_vatican_fl_fully_agree":[(r["trigon"],r["ordinal_degree"],r["vatican_observed"]) for r in rows if r["munich_observed"] is None and r["vatican_florence_match"]],
        "octet_repetition_failure_by_trigon":{tri:[r["ordinal_degree"] for r in changed if r["trigon"]==tri] for tri in TRIGON_ORDER},
        "octet_repetition_failure_total":len(changed),
        "preexisting_source_disagreements":len(disputed),
        "vatican_on_c05_narrative_only":sum(r["vatican_observed"]==r["c05_narrative_sevenfold_day"] for r in disputed),
        "vatican_on_c04_greenbaum_only":sum(r["vatican_observed"]==r["c04_greenbaum_sevenfold_day"] for r in disputed),
        "vatican_matches_neither":sum(r["vatican_observed"] not in (r["c05_narrative_sevenfold_day"],r["c04_greenbaum_sevenfold_day"]) for r in disputed)
    }
    return {
        "comparison_type":"SOURCE_HISTORY_THREE_PHYSICAL_MANUSCRIPTS_NOT_HUMAN_VALIDATION",
        "counts":source_only,
        "unique_ancient_authorial_canon_determined":False,
        "genetically_independent_witnesses_established":False,
        "blinded_human_predictive_validations":0,
        "promoted_production_rule":False,
        "rows":rows
    }


if __name__=="__main__":
    print(json.dumps(three_manuscript_comparison(),indent=2))
