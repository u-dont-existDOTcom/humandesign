"""C14 manuscript-to-manuscript comparison, never a natal rule or human test.

Florence labels are stored as source observations independent of computation;
Munich remains null at earth 28. Agreement of two codices does not by itself
establish that their manuscript traditions are genealogically independent.
"""
from __future__ import annotations
import json
from pathlib import Path

from paulus_munich_full_c13 import manuscript_source
from paulus_monomoiria_source_c04 import edited_day_degree_ruler
from paulus_trigon_narrative_c05 import narrative_degree_ruler, TRIGON_ORDER

HERE=Path(__file__).resolve().parent
FLORENCE=HERE/"PAULUS_C14_FLORENCE_120_POSITION_ORIGINAL_WITNESS_V1.json"


def florence_source()->dict:
    return json.loads(FLORENCE.read_text(encoding="utf-8"))


def cross_codex_matrix()->dict:
    flor=florence_source()
    mun=manuscript_source()
    rows=[]
    for tri in TRIGON_ORDER:
        sign=flor["four_trigons_signs"][tri][0]
        for d in range(1,31):
            i=d-1
            fl=flor["observed_degrees_1_to_30"][tri][i]
            mu=mun["observed_degrees_1_to_30"][tri][i]
            n=narrative_degree_ruler(sign,d,sect="day")
            p=edited_day_degree_ruler(sign,d,sect="day")
            f8=flor["observed_degrees_1_to_30"][tri][i%8]
            rows.append({
                "trigon":tri,"degree":d,
                "florence":fl,"munich":mu,
                "two_codices_comparable":mu is not None,
                "matches_munich":None if mu is None else mu==fl,
                "florence_eightfold_first_octet_diagnostic_matches":f8==fl,
                "narrative_sevenfold_day":n,
                "greenbaum_corrected_day":p,
                "previous_34_disputed":n!=p,
                "florence_matches_narrative":fl==n,
                "florence_matches_corrected":fl==p,
            })
    comparable=[r for r in rows if r["two_codices_comparable"]]
    disputed=[r for r in rows if r["previous_34_disputed"]]
    anomalies={t:[r["degree"] for r in rows if r["trigon"]==t and not r["florence_eightfold_first_octet_diagnostic_matches"]] for t in TRIGON_ORDER}
    return {
        "scope":"RELATED_GREEK_MANUSCRIPT_WITNESSES_NOT_PROSPECTIVE_HUMAN_VALIDATION",
        "florence_total_read":len(rows),
        "munich_read":len(comparable),
        "cross_codex_cell_agreements":sum(r["matches_munich"] for r in comparable),
        "cross_codex_cell_disagreements":[(r["trigon"],r["degree"]) for r in comparable if not r["matches_munich"]],
        "munich_unresolved_even_after_other_witness":[(r["trigon"],r["degree"],r["florence"]) for r in rows if not r["two_codices_comparable"]],
        "florence_not_naive_eightfold":anomalies,
        "eightfold_difference_count":sum(len(x) for x in anomalies.values()),
        "preexisting_disputed_cells":len(disputed),
        "florence_matches_narrative_only":sum(r["florence_matches_narrative"] for r in disputed),
        "florence_matches_corrected_only":sum(r["florence_matches_corrected"] for r in disputed),
        "florence_matches_neither":sum(not r["florence_matches_corrected"] and not r["florence_matches_narrative"] for r in disputed),
        "ancient_author_preferred_algorithm_confirmed":False,
        "manuscript_genealogy_independence_confirmed":False,
        "production_model_promoted":False,
        "human_predictive_validations":0,
        "rows":rows,
    }


if __name__=="__main__":
    print(json.dumps(cross_codex_matrix(),indent=2))
