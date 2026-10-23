"""P.Oxy. LXI 4277: second papyrus, documentary monomoiria comparison.

This program checks three surviving *source attributions* from the
astrological papyrus (late 2nd / early 3rd century CE) as tabulated in:
Cristian Tolsa, "'New' Zodiacal Divisions in P.Oxy. LXI 4277,"
Zeitschrift für Papyrologie und Epigraphik 203 (2017), pp. 192–198,
especially p. 197, 'Single degree' column.

Unlike the 319 CE P.Berl. 9825 in C04, the surviving labels do NOT all
agree with the Paulus/Valens by-sign method. There is no license to tune
the method to make every ancient scribe agree. Preserve each negative.

The original author discusses a third "mixed" reconstruction and warns
that numerical methods in this text are inconsistent. That speculative
mixed method is NOT implemented here.

NOTE: Manuscript position Capricorn 6°22' means ordinal degree seven,
not "degree six". We compare the correct and an explicitly labelled
mistaken ordinal convention as a source-critical diagnostic only.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

from paulus_bysign_papyrus_c04 import sign_monomoiria


@dataclass(frozen=True)
class AncientWitness:
    object_name: str
    sign: str
    completed_degrees: int
    arcminutes: int
    written_monomoiria: str
    source_locator: str


P_OXY_4277 = (
    AncientWitness("Mercury","Capricorn",6,22,"Venus",
                   "Tolsa (2017), p197, P.Oxy. LXI 4277 i.5-9"),
    AncientWitness("Midheaven","Taurus",27,8,"Mercury",
                   "Tolsa (2017), p197, P.Oxy. LXI 4277, cardinal point"),
    AncientWitness("Lower Midheaven","Scorpio",27,8,"Jupiter",
                   "Tolsa (2017), p197, P.Oxy. LXI 4277, cardinal point"),
)


def incorrect_ordinal_variant(row: AncientWitness) -> str:
    """A documented comparison of an off-by-one *error* convention.

    For this corpus every reported completed-degree integer is >=1.
    This function should not become a new accepted historical chart
    calculator: 0° cannot be mapped under its flawed convention.
    """
    if row.completed_degrees <= 0:
        raise ValueError("flawed ordinal convention is undefined at 0°")
    return sign_monomoiria(row.sign,row.completed_degrees-1,row.arcminutes)


def documentary_audit() -> dict:
    data=[]
    for r in P_OXY_4277:
        corrected=sign_monomoiria(r.sign,r.completed_degrees,r.arcminutes)
        one_lesser=incorrect_ordinal_variant(r)
        data.append({
            **asdict(r),
            "Paulus_by_sign_true_ordinal":corrected,
            "Paulus_by_sign_mistaken_ordinal":one_lesser,
            "agrees_true_ordinal":corrected==r.written_monomoiria,
            "agrees_mistaken_ordinal":one_lesser==r.written_monomoiria,
        })
    return {
        "kind":"INDEPENDENT_PAPYRUS_DOCUMENTARY_CALCULATION_FIDELITY_NOT_HUMAN_VALIDATION",
        "historical_witness":"P.Oxy. LXI 4277",
        "edition":"Tolsa 2017 pp192-198, derivative analysis of Jones 1999 original",
        "source_status":"SCHOLARLY_SECONDARY_TEXT_READ; MANUSCRIPT_IMAGE_NOT_RECHECKED",
        "n":len(data),
        "true_ordinal_agreements":sum(v["agrees_true_ordinal"] for v in data),
        "mistaken_ordinal_agreements":sum(v["agrees_mistaken_ordinal"] for v in data),
        "records":data,
        "model_promotion":False,
    }


if __name__=="__main__":
    import json
    print(json.dumps(documentary_audit(),indent=2))
