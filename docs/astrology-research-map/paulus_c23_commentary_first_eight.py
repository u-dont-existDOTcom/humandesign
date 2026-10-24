"""C23 provisional photographed commentary canon, bounded to actually read rows.

This is a source-fidelity comparison of 14th-century handwriting, not a
human astrology validation, not Boer 1958/1962 printed apparatus, and not
a verified blind palaeographic transcription. No d9–30 interpolation.
"""
import json
from pathlib import Path

from paulus_trigon_narrative_c05 import narrative_degree_ruler
from paulus_monomoiria_source_c04 import edited_day_degree_ruler
from paulus_c15_three_manuscript_comparison import vatican_source

SOURCE=Path(__file__).with_name("PAULUS_C23_FLORENCE_COMMENTARY_204V_FIRST_EIGHT_V1.json")
SIGNS={"fire":"Aries","earth":"Taurus","air":"Gemini","water":"Cancer"}

def witness():
    return json.loads(SOURCE.read_text(encoding="utf-8"))

def source_slot(trigon,ordinal,slot="first"):
    w=witness()
    if trigon not in SIGNS:
        raise ValueError("not a manuscript triplicity")
    if type(ordinal) is not int or not (1<=ordinal<=30):
        raise ValueError("ordinal degree must be an integer between 1 and 30")
    if slot=="first":
        if ordinal>8:
            raise ValueError("first-slot manuscript degree 9–30 not yet individually read")
        return w["first_slot_first_eight_observed_by_trigon"][trigon][ordinal-1]
    if slot=="second":
        if ordinal!=1:
            raise ValueError("second-slot manuscript degree 2–30 not yet individually read")
        return w["second_slot_degree_one_observed_by_trigon"][trigon]
    raise ValueError("slot must be first or second")

def first_eight_source_comparison():
    old=vatican_source()["independent_source_observed_planetary_degree_1_to_30"]
    rows=[]
    for tri,sign in SIGNS.items():
        for degree in range(1,9):
            photographed=source_slot(tri,degree)
            narrative=narrative_degree_ruler(sign,degree,sect="day")
            printed=edited_day_degree_ruler(sign,degree,sect="day")
            oldms=old[tri][degree-1]
            rows.append(dict(
                trigon=tri,ordinal_degree=degree,
                new_commentary_first_slot=photographed,
                narrative_day=narrative,
                printed_Greenbaum_day=printed,
                old_Paulus_ms_candidate=oldms,
                matches_narrative=(photographed==narrative),
                matches_printed=(photographed==printed),
                matches_old_ms=(photographed==oldms),
                preexisting_C04_C05_disputed=(narrative!=printed),
                first_slot_as_day_is_provisional=True,
            ))
    disputed=[r for r in rows if r["preexisting_C04_C05_disputed"]]
    return dict(
        source_scope="ONLY_32_DIRECT_FIRST_SLOT_HANDWRITTEN_PHOTO_GLYPHS",
        total_directly_sampled_positions=len(rows),
        agrees_C05_day_narrative=sum(r["matches_narrative"] for r in rows),
        agrees_C04_printed_day=sum(r["matches_printed"] for r in rows),
        agrees_old_Paulus_ms_family=sum(r["matches_old_ms"] for r in rows),
        previously_disputed_subset=len(disputed),
        disputed_align_C05_only=sum(r["matches_narrative"] and not r["matches_printed"] for r in disputed),
        disputed_align_C04_only=sum(r["matches_printed"] and not r["matches_narrative"] for r in disputed),
        disputed_align_neither=sum(not r["matches_narrative"] and not r["matches_printed"] for r in disputed),
        night_opening_pairs_match_C05_night=sum(
            source_slot(tri,1,"second")==narrative_degree_ruler(sign,1,sect="night")
            for tri,sign in SIGNS.items()
        ),
        manuscript_day_night_abbreviations_independently_verified=False,
        remaining_22_degrees_x4_untranscribed=True,
        human_predictive_validations=0,
        promoted_production_rule=False,
        rows=rows
    )

if __name__=="__main__":
    print(json.dumps(first_eight_source_comparison(),indent=2))
