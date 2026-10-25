"""C33: Ptolemy Tetrabiblos IV.5: sign-only *subrule*, not a full reading.

Greek: men use Moon; women use Sun; natal bicorporeal signs appear as
ONE alternative sufficient branch associated with "many marriages".
Other disjuncts (multiform signs, planetary applications) are NOT silently
executed. The uncomputed clauses can conflict with the sign branch.

No participant marriage history, birth data or production predictions.
"""
from __future__ import annotations
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

SIGNS=("Aries","Taurus","Gemini","Cancer","Leo","Virgo",
       "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces")
BICORPOREAL=frozenset(("Gemini","Virgo","Sagittarius","Pisces"))
SOURCE_BRANCH_BODY={"men_moon":"moon","women_sun":"sun"}
SOURCE_STATUS="PTOL_IV_5_BICORPOREAL_SIGN_DISJUNCT_ONLY"
MARRIAGE_OUTCOME="TWO_OR_MORE_LAWFUL_MARRIAGES"


def _decimal(x: Any) -> Decimal:
    if isinstance(x,bool) or not isinstance(x,(int,float,str,Decimal)):
        raise ValueError("exact numeric ecliptic longitude or margin required")
    try:
        z=Decimal(str(x))
    except InvalidOperation as exc:
        raise ValueError("not a finite number") from exc
    if not z.is_finite():
        raise ValueError("NaN or Infinity is not a valid angular input")
    return z


def sign_at(longitude: int|float|str|Decimal) -> str:
    """Tropical twelve 30° sectors, strict physical longitude [0,360)."""
    d=_decimal(longitude)
    if not Decimal(0)<=d<Decimal(360):
        raise ValueError("angle must be in [0,360) degrees; no silent wrap")
    return SIGNS[int(d//30)]


def sign_only_source_subrule(
    *, historical_branch: str, longitude: int|float|str|Decimal,
) -> dict:
    """Expose one positive condition, NOT exclusive horoscope classification.

    'men_moon' and 'women_sun' are categories *in the ancient text*, not
    labels inferred about actual participants or modern legal definitions.
    """
    if historical_branch not in SOURCE_BRANCH_BODY:
        raise ValueError("exact ancient text branch required")
    sign=sign_at(longitude)
    signal=sign in BICORPOREAL
    return {
        "source":"PTOLEMY_TETRABIBLOS_IV_5_P2_P4",
        "historical_branch":historical_branch,
        "natal_body":SOURCE_BRANCH_BODY[historical_branch],
        "body_sign":sign,
        "bicorporeal_positive_condition":signal,
        "source_outcome_if_positive":(
            MARRIAGE_OUTCOME if signal else "NO_CLAIM_FROM_BICORPOREAL_SUBRULE"
        ),
        "negative_condition_does_not_predict_one_marriage":True,
        "unimplemented_alternative_multiform_signs":True,
        "unimplemented_applying_planet_conditions":True,
        "other_source_clauses_may_conflict":True,
        "not_a_complete_historical_marriage_delineation":True,
        "person_outcomes_tested":0,
        "research_only":True,
    }


def continuous_sign_enclosure(
    *, center_longitude: int|float|str|Decimal,
    max_absolute_motion_deg: int|float|str|Decimal,
) -> dict:
    """All sign bins inside a CLOSED unwrapped [-radius,+radius] envelope.

    The radius must independently enclose the whole birth-interval body
    trajectory. This returns a conditional feature, never certification
    that the bound or historical time conversion is correct.
    """
    center=_decimal(center_longitude)
    radius=_decimal(max_absolute_motion_deg)
    if not Decimal(0)<=center<Decimal(360) or radius<0:
        raise ValueError("bad center longitude or motion bound")
    lower=center-radius
    upper=center+radius
    if upper-lower>=Decimal(360):
        signs=set(SIGNS)
    else:
        k0=int(lower//30)
        k1=int(upper//30)
        signs={SIGNS[k%12] for k in range(k0,k1+1)}
    statuses={name in BICORPOREAL for name in signs}
    return {
        "possible_signs":sorted(signs),
        "possible_bicorporeal_values":sorted(statuses),
        "condition_stable_if_envelope_is_valid":len(statuses)==1,
        "strictly_same_sign_if_envelope_is_valid":len(signs)==1,
        "source_margin_deg":str(radius),
        "continuous_speed_bound_independently_certified":False,
        "time_zone_and_birth_date_source_verified":False,
        "eligible_for_untouched_human_predictions":False,
    }


def synthetic_body_from_verified_provider(
    provider:object, *, time_start:datetime, time_end:datetime,
    historical_branch:str,
) -> dict:
    """Require actual incumbent strict Swiss provider with file/flag checks.

    The project declares conservative speed bounds (Moon=16°, Sun=1.1°
    per day); without a separate completeness audit they remain
    SOURCE-DECLARED NOT INDEPENDENTLY PROVED. The output stays research-only.
    """
    from hdmatch.chart.ephemeris import SwissEphemerisProvider,CelestialBody
    if type(provider) is not SwissEphemerisProvider:
        raise ValueError("must use real fail-closed SwissEphemerisProvider")
    if historical_branch not in SOURCE_BRANCH_BODY:
        raise ValueError("branch name is required")
    if any(x.tzinfo is None or x.utcoffset() is None
           for x in (time_start,time_end)):
        raise ValueError("UTC-aware time interval required")
    t0,t1=time_start.astimezone(UTC),time_end.astimezone(UTC)
    seconds=(t1-t0).total_seconds()
    if not 0<=seconds<=48*3600:
        raise ValueError("interval must be ordered and within 48 hours")
    mid=t0+(t1-t0)/2
    body=(CelestialBody.MOON if historical_branch=="men_moon"
          else CelestialBody.SUN)
    longitude=provider.position(body,mid).longitude
    speed_bound=provider.max_abs_speed_degrees_per_day(body)
    radius=Decimal(str(speed_bound))*Decimal(str(seconds))/Decimal("172800")
    envelope=continuous_sign_enclosure(
        center_longitude=longitude,max_absolute_motion_deg=radius)
    signal=sign_only_source_subrule(
        historical_branch=historical_branch,longitude=longitude)
    observed_files=tuple(sorted(
        (Path(x.path).name,x.sha256) for x in provider.metadata.files))
    if len(observed_files)<2:
        raise ValueError("two declared solar/lunar Swiss ephemeris sources required")
    return {
        "utc_interval_start":t0.isoformat(),
        "utc_interval_end":t1.isoformat(),
        "source_body_midpoint":str(longitude),
        "source_midpoint_sign":signal["body_sign"],
        "natal_body":body.value,
        "source_family":"PTOLEMY_TETRABIBLOS_IV_5_BICORPOREAL_DISJUNCT",
        "source_files_sha256":observed_files,
        "historical_branch":historical_branch,
        "reported_speed_max_deg_per_day":str(speed_bound),
        "source_speed_not_independently_verified_for_full_cohort":True,
        "conditional_interval_enclosure":envelope,
        "study_ready":False,
        "actual_human_prediction_or_response_seen":False,
    }
