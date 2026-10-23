"""First eight directly inspected glyph assignments in Munich MS Cod.graec.170.

A 16th-century manuscript comparison is NOT a human prediction test.
Only degrees 1..8 are admitted as visual source readings. The tempting
eightfold pattern is a diagnostic, not authority to extend to degrees 9..30.
"""
import json
from pathlib import Path

from paulus_monomoiria_source_c04 import (
    ZODIAC,
    edited_day_degree_ruler,
    triplicity_for_sign,
)
from paulus_trigon_narrative_c05 import (
    TRIGON_DAY_NIGHT,
    TRIGON_ORDER,
    narrative_degree_ruler,
)

SOURCE_FILE = Path(__file__).with_name(
    "PAULUS_C12_MUNICH_FIRST_OCTET_SOURCE_WITNESS_V1.json"
)


def witness():
    return json.loads(SOURCE_FILE.read_text(encoding="utf-8"))


def manuscript_first_octet(trigon: str, ordinal_degree: int) -> str:
    """Only directly-read MS degrees 1..8; reject extrapolation."""
    w = witness()
    if trigon not in TRIGON_ORDER:
        raise ValueError("unrecognized manuscript trigon")
    if type(ordinal_degree) is not int or not (1 <= ordinal_degree <= 8):
        raise ValueError("degrees >8 are not admitted from handwritten evidence")
    return w["eight_by_trigon"][trigon][ordinal_degree - 1]


def eight_slots_without_skipping(trigon: str):
    """Diagnostic: traverse four day-trigon pairs, retaining duplicate Venus."""
    if trigon not in TRIGON_ORDER:
        raise ValueError("unrecognized trigon")
    i = TRIGON_ORDER.index(trigon)
    return tuple(
        planet
        for offset in range(4)
        for planet in TRIGON_DAY_NIGHT[TRIGON_ORDER[(i+offset) % 4]]
    )


def direct_octet_comparison():
    """Compare only observed first 8 MS cells to both C05 source interpretations.

    This counts witness agreement, not superiority or model correctness.
    Full historical 34-cell adjudication is withheld because 25 positions
    were not individually read in this bounded comparison.
    """
    data=[]
    for tri in TRIGON_ORDER:
        sign=next(s for s in ZODIAC if triplicity_for_sign(s)==tri)
        for degree in range(1,9):
            ms=manuscript_first_octet(tri,degree)
            derived=narrative_degree_ruler(sign,degree,sect="day")
            edited=edited_day_degree_ruler(sign,degree,sect="day")
            disputed=derived!=edited
            data.append({
                "trigon":tri,"ordinal_degree":degree,
                "direct_manuscript_read":ms,
                "seven_unique_narrative":derived,
                "greenbaum_corrected_day":edited,
                "previous_34_disputed_subset":disputed,
                "agrees_narrative":ms==derived,
                "agrees_corrected_day":ms==edited,
            })
    contested=[r for r in data if r["previous_34_disputed_subset"]]
    return {
        "source_class":"FIRST_OCTET_HANDWRITTEN_EDITION_COMPARISON",
        "inspected_cells":len(data),
        "formerly_disputed_visible_cells":len(contested),
        "visible_disputed_match_narrative":sum(r["agrees_narrative"] for r in contested),
        "visible_disputed_match_corrected_day":sum(r["agrees_corrected_day"] for r in contested),
        "visible_disputed_match_neither":sum(
            not r["agrees_narrative"] and not r["agrees_corrected_day"]
            for r in contested
        ),
        "uninspected_of_previous_34":34-len(contested),
        "original_ms_120_decoded":False,
        "accepted_as_canonical_day_rule":False,
        "human_predictive_validations":0,
        "rows":data,
    }


if __name__ == "__main__":
    print(json.dumps(direct_octet_comparison(),indent=2))
