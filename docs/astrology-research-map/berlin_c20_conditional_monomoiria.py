"""Source-critical recheck of conjectural Berlin horoscope Libra longitude.

Separate editor's conditional restoration, Egyptian bounds attested in
Ptolemy Tetrabiblos, and C04 by-sign monomoiria calculation.
No historical alternatives are selected for human biography fitting.
"""
from __future__ import annotations
import json
from pathlib import Path
from paulus_bysign_papyrus_c04 import sign_monomoiria

EVIDENCE=Path(__file__).with_name("BERLIN_C20_MOON_LIBRA_CANDIDATES_V1.json")


def record() -> dict:
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def egyptian_Libra_term(complete_degree: int, minutes: int) -> str:
    """Ancient *Egyptian* Libra terms; exact [0,30) intervals, not Ptolemaic."""
    if type(complete_degree) is not int or not (0<=complete_degree<30):
        raise ValueError("Libra completed degree outside 0..29")
    if type(minutes) is not int or not (0<=minutes<60):
        raise ValueError("Minutes outside 0..59")
    bounds=record()["Egyptian_terms_Libra"]
    for planet,endpoint in zip(bounds["order"],bounds["cumulative_ends"]):
        if complete_degree<endpoint:
            return planet
    raise AssertionError("Invalid Egyptian term table")


def Moon_monomoiria_candidates(minutes: int=35) -> list[dict]:
    """Enumerate all 0..29 positions, rather than choosing an editor's favorite."""
    return [
        {
            "completed_degree":degree,
            "ordinal_degree":degree+1,
            "arcminutes":minutes,
            "monomoiria":"Moon",
            "Egyptian_term":egyptian_Libra_term(degree,minutes)
        }
        for degree in range(30)
        if sign_monomoiria("Libra",degree,minutes)=="Moon"
    ]


def source_constrained_audit() -> dict:
    e=record()
    published=e["candidate_table"]
    computed=Moon_monomoiria_candidates(minutes=35)
    assert len(published)==len(computed)==4
    for a,b in zip(published,computed):
        for key in ("completed_degree","ordinal_degree"):
            assert a[key]==b[key]
        assert a["by_sign_ruler"]==b["monomoiria"]=="Moon"
        assert a["Egyptian_term"]==b["Egyptian_term"]
    saturn=[row["completed_degree"] for row in computed if row["Egyptian_term"]=="Saturn"]
    return {
        "scope":"EDITORIAL_RESTORATION_AND_ANCIENT_TABLE_COMPARISON_ONLY",
        "all_source_compatible_completed_degrees":[r["completed_degree"] for r in computed],
        "hypothetical_Egyptian_Saturn_terms_only_candidates":saturn,
        "editors_conditional_favorite":e["editorial_state"]["preferred_completed_degree"],
        "original_papyrus_exact_degree_independently_certified":False,
        "Egyptian_terms_assumption_proved_for_this_scribe":False,
        "monomoiria_only_determines_unique_degree":False,
        "four_mathematically_possible_rows":computed,
        "human_predictive_validations":0,
        "production_model_promoted":False
    }


if __name__=="__main__":
    print(json.dumps(source_constrained_audit(),indent=2))
