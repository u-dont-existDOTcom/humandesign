"""Research-only Papme variants reconstructed from Cornu and Erlewine.
Not an independently validated Tibetan natal calendar or human prediction engine.
Input natal mewa/year polarity/person sex must be independently computed/frozen.
"""
from __future__ import annotations

BASE_LO_SHU=((4,9,2),(3,5,7),(8,1,6))
MALE_ROUTE=((1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,1),(0,0))
FEMALE_ROUTE=((1,0),(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(2,0))
VALID_POLARITIES=frozenset(("masculine","feminine"))
VALID_SUBJECT_SEX=frozenset(("male","female"))


def square_for_mewa(natal_mewa: int) -> tuple[tuple[int,...],...]:
    if isinstance(natal_mewa, bool) or type(natal_mewa) is not int or not 1<=natal_mewa<=9:
        raise ValueError("natal mewa must be integer 1–9; natal mewa 5 remains valid Papme")
    return tuple(tuple((n-1 + natal_mewa-5)%9+1 for n in row) for row in BASE_LO_SHU)


def papme(*, natal_mewa: int, age_tibetan_inclusive: int,
          policy: str, natal_year_polarity: str | None = None,
          subject_sex: str | None = None) -> int:
    if type(age_tibetan_inclusive) is not int or age_tibetan_inclusive<1:
        raise ValueError("Tibetan inclusive age required, positive integer")
    if policy=="cornu_natal_year_polarity":
        if natal_year_polarity not in VALID_POLARITIES:
            raise ValueError("Cornu requires masculine/feminine natal-year polarity")
        route=MALE_ROUTE if natal_year_polarity=="masculine" else FEMALE_ROUTE
    elif policy=="erlewine_subject_sex":
        if subject_sex not in VALID_SUBJECT_SEX:
            raise ValueError("Erlewine requires explicitly supplied male/female subject sex")
        route=MALE_ROUTE if subject_sex=="male" else FEMALE_ROUTE
    else:
        raise ValueError("unknown Papme policy")
    square=square_for_mewa(natal_mewa)
    k=(age_tibetan_inclusive-1)%9
    if k==0:
        return natal_mewa
    i,j=route[k-1]
    return square[i][j]


def four_years(natal_mewa: int, policy: str, **known_inputs: str) -> list[int]:
    return [papme(natal_mewa=natal_mewa,age_tibetan_inclusive=age,
                  policy=policy,**known_inputs) for age in range(1,5)]
