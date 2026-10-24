"""C24 source-only comparison of literal but nonblind Florence ms table candidates.

Read only values manually recorded from photographed manuscript. The 120
first-slot glyph names and 80 selected second-slot names are NOT authoritative
palaeography, a complete diurnal/nocturnal canon, or validation on humans.
No extrapolation of source second-slot unknowns is permitted.
"""
from __future__ import annotations

import json
from pathlib import Path

from paulus_c23_commentary_first_eight import witness as c23_first8
from paulus_c15_three_manuscript_comparison import vatican_source
from paulus_monomoiria_source_c04 import edited_day_degree_ruler
from paulus_trigon_narrative_c05 import narrative_degree_ruler

EVIDENCE=Path(__file__).with_name("PAULUS_C24_COMMENTARY_120_FIRST_80_SECOND_SOURCE_V1.json")
SIGNS={"fire":"Aries","earth":"Taurus","air":"Gemini","water":"Cancer"}


def source():
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def observed_slot(trigon: str, ordinal_degree: int, slot: str="first"):
    doc=source()
    if trigon not in SIGNS:
        raise ValueError("Invalid trigon")
    if type(ordinal_degree) is not int or not (1<=ordinal_degree<=30):
        raise ValueError("Ordinal degree must be integer in 1..30")
    if slot=="first":
        return doc["source_first_slot_ordinals_1_to_30"][trigon][ordinal_degree-1]
    if slot=="second":
        val=doc["source_second_slot_ordinals_1_to_30_sparse"][trigon][ordinal_degree-1]
        if val is None:
            raise ValueError("That second-slot source glyph has not been individually read")
        return val
    raise ValueError("Slot must be 'first' or 'second'")


def research_comparison():
    doc=source()
    oldms=vatican_source()["independent_source_observed_planetary_degree_1_to_30"]
    first8=c23_first8()
    rows=[]
    for tr,sign in SIGNS.items():
        vals=doc["source_first_slot_ordinals_1_to_30"][tr]
        second=doc["source_second_slot_ordinals_1_to_30_sparse"][tr]
        assert len(vals)==len(second)==30
        assert vals[:8]==first8["first_slot_first_eight_observed_by_trigon"][tr]
        assert second[0]==first8["second_slot_degree_one_observed_by_trigon"][tr]
        for d in range(1,31):
            first=observed_slot(tr,d)
            secondval=second[d-1]
            dayn=narrative_degree_ruler(sign,d,sect="day")
            dayp=edited_day_degree_ruler(sign,d,sect="day")
            night=narrative_degree_ruler(sign,d,sect="night")
            paired_adjacent=vals[d] if d%2==1 else vals[d-2]
            # Paired exchange is DIAGNOSTIC; not used to fill null manuscript cells.
            rows.append({
                "trigon":tr,"degree":d,"source_first":first,
                "source_second":secondval,
                "second_pair_exchange_hypothesis":paired_adjacent,
                "source_second_pair_exchange_agrees":None if secondval is None else secondval==paired_adjacent,
                "day_narrative":dayn,"day_Greenbaum_printed":dayp,
                "night_narrative_diagnostic":night,
                "older_Paulus_manuscript":oldms[tr][d-1],
                "source_first_matches_day_narrative":first==dayn,
                "source_first_matches_printed_day":first==dayp,
                "source_first_matches_older_ms":first==oldms[tr][d-1],
                "source_second_matches_night_narrative":None if secondval is None else secondval==night,
                "source_first_matches_neither_day_method":first not in (dayn,dayp),
                "C04_C05_day_disagree":dayn!=dayp,
                "source_certainty":"PROVISIONAL_PHOTO_GLYPH_NONBLIND"
            })
    observed=[r for r in rows if r["source_second"] is not None]
    disputed=[r for r in rows if r["C04_C05_day_disagree"]]
    def sums(tr,key):return sum(r[key] for r in rows if r["trigon"]==tr)
    return {
        "scope":"SOURCE_EVIDENCE_NOT_ASTROLOGY_PREDICTIVE_PERFORMANCE",
        "first_slot_source_cells_provisionally_read":len(rows),
        "second_slot_source_cells_provisionally_read":len(observed),
        "second_slot_source_cells_still_unread":len(rows)-len(observed),
        "first_slot_day_C05_narrative_agreements":sum(r["source_first_matches_day_narrative"] for r in rows),
        "first_slot_day_C04_printed_agreements":sum(r["source_first_matches_printed_day"] for r in rows),
        "first_slot_old_Paulus_ms_family_agreements":sum(r["source_first_matches_older_ms"] for r in rows),
        "first_slot_matching_neither_day_rule":sum(r["source_first_matches_neither_day_method"] for r in rows),
        "second_slot_pair_exchange_matches":sum(r["source_second_pair_exchange_agrees"] for r in observed),
        "second_slot_matches_independent_C05_night":sum(r["source_second_matches_night_narrative"] for r in observed),
        "previous_C04_C05_day_disagreement_cells":len(disputed),
        "source_first_in_disputed_cells_align_narrative_only":sum(r["source_first_matches_day_narrative"] and not r["source_first_matches_printed_day"] for r in disputed),
        "source_first_in_disputed_cells_align_C04_only":sum(r["source_first_matches_printed_day"] and not r["source_first_matches_day_narrative"] for r in disputed),
        "source_first_in_disputed_cells_align_neither":sum(r["source_first_matches_neither_day_method"] for r in disputed),
        "per_trigon":{tr:{
            "first_C05":sums(tr,"source_first_matches_day_narrative"),
            "first_C04":sums(tr,"source_first_matches_printed_day"),
            "first_old_ms":sums(tr,"source_first_matches_older_ms"),
            "second_read":sum(r["trigon"]==tr and r["source_second"] is not None for r in rows),
            "second_pair_exchange_matches":sum(r["trigon"]==tr and r["source_second_pair_exchange_agrees"] is True for r in rows),
            "second_C05_night_matches":sum(r["trigon"]==tr and r["source_second_matches_night_narrative"] is True for r in rows)
        } for tr in SIGNS},
        "second_slot_night_sect_palaeographically_verified":False,
        "first_slot_day_sect_palaeographically_verified":False,
        "Boer_1958_1962_printed_critical_apparatus_examined":False,
        "human_predictive_validations":0,
        "production_model_modified":False,
        "rows":rows
    }


if __name__=="__main__":
    print(json.dumps(research_comparison(),indent=2))
