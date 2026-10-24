"""C24 complete provisional paired manuscript photo slots.

C24 Stage A preserves 40 unknowns and is immutable as an evidentiary
intermediate fixture. Stage B records subsequent visually inspected values,
but all 240 glyph classifications are unblinded *candidate* readings.
The pair-exchange diagnostic is checked, never used to impute the data.
"""
from pathlib import Path
import json

from paulus_c24_commentary_120_first_80_second import source as stage_a_source
from paulus_trigon_narrative_c05 import narrative_degree_ruler

SECOND=Path(__file__).with_name("PAULUS_C24_COMMENTARY_FULL_SECOND_120_V1.json")
SIGNS={"fire":"Aries","earth":"Taurus","air":"Gemini","water":"Cancer"}

def stage_b_source():
    return json.loads(SECOND.read_text(encoding="utf-8"))

def complete_provisional_240():
    a=stage_a_source()
    b=stage_b_source()
    first=a["source_first_slot_ordinals_1_to_30"]
    second=b["source_second_slot_ordinals_1_to_30"]
    rows=[]
    for tr,sign in SIGNS.items():
        f=first[tr]
        s=second[tr]
        assert len(f)==len(s)==30
        old=a["source_second_slot_ordinals_1_to_30_sparse"][tr]
        for d in range(1,31):
            firstvalue=f[d-1]
            secondvalue=s[d-1]
            assert old[d-1] is None or old[d-1]==secondvalue, (
                tr,d,old[d-1],secondvalue
            )
            hypothesis=f[d] if d%2==1 else f[d-2]
            other_night=narrative_degree_ruler(sign,d,sect="night")
            rows.append({
                "trigon":tr,"ordinal_degree":d,
                "first_slot":firstvalue,"second_slot":secondvalue,
                "pairwise_adjacent_exchange_diagnostic":hypothesis,
                "swap_matches_photo":secondvalue==hypothesis,
                "nighttime_C05_narrative":other_night,
                "second_matches_C05_night":secondvalue==other_night,
                "stage_A_second_previously_read":old[d-1] is not None,
                "stage_B_second_newly_read":old[d-1] is None,
                "source_status":"CANDIDATE_NONBLIND_ORIGINAL_PHOTO_GLYPH"
            })
    return {
        "provisional_first_slot_glyphs":len(rows),
        "provisional_second_slot_glyphs":len(rows),
        "earlier_stage_A_second_cells_preserved":sum(r["stage_A_second_previously_read"] for r in rows),
        "new_stage_B_second_cells_read":sum(r["stage_B_second_newly_read"] for r in rows),
        "pairwise_exchange_matches":sum(r["swap_matches_photo"] for r in rows),
        "C05_night_narrative_matches_second_slot":sum(r["second_matches_C05_night"] for r in rows),
        "per_trigon":{
            tr:{
                "pairwise_exchange_matches":sum(r["trigon"]==tr and r["swap_matches_photo"] for r in rows),
                "C05_night_matches":sum(r["trigon"]==tr and r["second_matches_C05_night"] for r in rows)
            }for tr in SIGNS
        },
        "unread_second_source_cells_from_stage_B":0,
        "unblinded_glyph_names_not_independent_expert_certification":True,
        "day_night_rubric_not_verified":True,
        "cannot_use_pairwise_swap_as_production_night_rule":True,
        "historical_papyrus_and_human_predictions_unchanged":True,
        "human_predictive_validations":0,
        "production_model_changed":False,
        "rows":rows
    }

if __name__=="__main__":
    print(json.dumps(complete_provisional_240(),indent=2))
