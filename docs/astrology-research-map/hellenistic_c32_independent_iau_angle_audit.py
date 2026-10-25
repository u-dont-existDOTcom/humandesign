"""C32 independent IAU angle audit — strictly synthetic and research-only.

Two independent numerical engines:
  * ERFA/SOFA IAU 2006/2000A (GAST06A, OBL06, NUT06A) for sidereal
    time and true ecliptic obliquity, with an independent rising
    ecliptic / eastern-horizon intersection, not Swiss houses.
  * Swiss Ephemeris houses_ex for comparison only.

UT1-UTC defaults to *assumed zero*: actual EOP has not been supplied.
No participant, owner natal chart, DOB, military outcome or scoring input.
Does not certify a human prediction or all historical time conversions.
Optional `pyerfa` is loaded on invocation, not a project dependency.
"""
from __future__ import annotations

from datetime import UTC, datetime
from math import atan2, cos, degrees, pi, radians, sin
import importlib
import hashlib
import json
from pathlib import Path
import random
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


SYNTHETIC_SEED = 20261025
CASE_COUNT = 145
DEFAULT_DUT1_SECONDS = 0.0

# The five C31 *synthetic* tuples plus a deterministic cohort never
# built from the owner's personal data.
SEED_CASES = (
    (datetime(2000, 1, 1, 12, tzinfo=UTC), 0.0, 0.0),
    (datetime(2015, 3, 20, 12, tzinfo=UTC), 40.0, -75.0),
    (datetime(2026, 1, 1, tzinfo=UTC), 20.5, -70.0),
    (datetime(1999, 6, 15, 3, tzinfo=UTC), -33.0, 151.0),
    (datetime(2012, 12, 21, tzinfo=UTC), 55.0, 12.0),
)


def synthetic_cases():
    rng = random.Random(SYNTHETIC_SEED)
    yield from SEED_CASES
    for _ in range(CASE_COUNT - len(SEED_CASES)):
        y, mo = rng.randint(1960, 2026), rng.randint(1, 12)
        day, h = rng.randint(1, 28), rng.randint(0, 23)
        minute = rng.randint(0, 59)
        lat, lon = rng.uniform(-65, 65), rng.uniform(-179, 179)
        yield (datetime(y, mo, day, h, minute, tzinfo=UTC), lat, lon)


def circular_arcseconds(a: float, b: float) -> float:
    return abs(((a - b + 180) % 360) - 180) * 3600


def _require_input(utc: datetime, lat: float, lon: float) -> datetime:
    if utc.tzinfo is None or utc.utcoffset() is None:
        raise ValueError("a timezone-aware UTC instant is required")
    if not -66 < lat < 66 or not -180 <= lon <= 180:
        raise ValueError("only moderate-latitude geometric comparisons")
    normalized = utc.astimezone(UTC)
    if not 1960 <= normalized.year <= 2050:
        raise ValueError("outside declared modern IAU synthetic-test period")
    return normalized


def eastern_horizon_intersection(
    *, apparent_lst_radians: float, true_obliquity_radians: float,
    geographic_latitude_radians: float
) -> tuple[float, float, float]:
    """Return ASC, MC in degrees plus signed dot with local east vector.

    Equatorial ecliptic unit vector:
       (cos lambda, sin lambda*cos epsilon, sin lambda*sin epsilon).
    Local east unit vector:
       (-sin theta, cos theta, 0).
    At ASC the dot must be >0; opposite horizon root is western
    setting point, not the Ascendant. Uses a geometric construction
    independent from the Swiss Asc1 calculation.
    """
    theta, eps, phi = (apparent_lst_radians,
                        true_obliquity_radians,
                        geographic_latitude_radians)
    north = cos(phi) * cos(theta)
    east_north = sin(phi)*sin(eps) + cos(phi)*cos(eps)*sin(theta)
    root = atan2(-north, east_north)
    east_component = -sin(theta)*cos(root) + cos(theta)*cos(eps)*sin(root)
    if east_component < 0:
        root += pi
    east_component = -sin(theta)*cos(root) + cos(theta)*cos(eps)*sin(root)
    mc = atan2(sin(theta)/cos(eps), cos(theta)) % (2*pi)
    return degrees(root) % 360, degrees(mc), east_component


def erfa_iau06_angles(
    utc: datetime, *, latitude: float, longitude: float,
    dut1_seconds: float = DEFAULT_DUT1_SECONDS,
) -> dict:
    """SOFA/ERFA true-equinox geometry; DUT1=0 is a declared approximation."""
    from math import isfinite
    at = _require_input(utc, latitude, longitude)
    if not isfinite(dut1_seconds) or abs(dut1_seconds) > 1:
        raise ValueError("DUT1 perturbation must be finite in +/- 1 second")
    erfa = importlib.import_module("erfa")
    utc1, utc2 = erfa.dtf2d("UTC", at.year, at.month, at.day,
                             at.hour, at.minute,
                             at.second + at.microsecond/1e6)
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    ut11, ut12 = erfa.utcut1(utc1, utc2, dut1_seconds)
    gast = erfa.gst06a(ut11, ut12, tt1, tt2)
    epsilon = erfa.obl06(tt1, tt2) + erfa.nut06a(tt1, tt2)[1]
    asc, mc, east = eastern_horizon_intersection(
        apparent_lst_radians=(float(gast)+radians(longitude))%(2*pi),
        true_obliquity_radians=float(epsilon),
        geographic_latitude_radians=radians(latitude),
    )
    return {
        "asc":asc,"mc":mc,"east_dot":east,
        "dut1_seconds_ASSUMED_NOT_MEASURED":dut1_seconds,
        "model":"IAU_2006_2000A_ERFA_TRUE_EQUINOX",
        "full_EOP_nutation_timezone_certified":False,
    }


def swiss_angle_reference(
    utc: datetime, *, latitude: float, longitude: float,
    house_system: bytes=b"P",
) -> tuple[float, float]:
    """Swiss is a comparison target, not a source for ERFA's formula."""
    at = _require_input(utc, latitude, longitude)
    swe = importlib.import_module("swisseph")
    hour = (at.hour + at.minute/60.0 + at.second/3600.0
            + at.microsecond/3.6e9)
    jd = swe.julday(at.year, at.month, at.day, hour, swe.GREG_CAL)
    _, ascmc = swe.houses_ex(jd, latitude, longitude, house_system, 0)
    return float(ascmc[0]), float(ascmc[1])


def resolve_civil_time_without_guessing(
    local_naive: datetime, *, iana_timezone: str
) -> dict:
    """Return every UTC candidate for IANA fall fold; never guess.

    Spring-forward nonexistent local times yield zero candidates.
    Normal wall times yield one; ambiguous wall times yield two.
    This does not prove a historical birthplace or its correct zone.
    """
    if local_naive.tzinfo is not None:
        raise ValueError("local input must be timezone-naive")
    try:
        tz = ZoneInfo(iana_timezone)
    except ZoneInfoNotFoundError as exc:
        raise ValueError("IANA zone unavailable") from exc
    options = set()
    for fold in (0, 1):
        aware = local_naive.replace(tzinfo=tz, fold=fold)
        utc = aware.astimezone(UTC)
        back = utc.astimezone(tz)
        if back.replace(tzinfo=None) == local_naive:
            options.add(utc.isoformat())
    ordered = sorted(options)
    return {
        "civil_time_status": (
            "GAP_NONEXISTENT" if not ordered else
            "FOLD_AMBIGUOUS" if len(ordered)==2 else "UNIQUE"
        ),
        "utc_candidates":ordered,
        "birthplace_time_zone_authenticated":False,
        "automatic_fold_choice_made":False,
        "eligible_for_human_prediction":False,
    }


def audit_synthetic() -> dict:
    erfa = importlib.import_module("erfa")
    swe = importlib.import_module("swisseph")
    samples = []
    for at, lat, lon in synthetic_cases():
        iau = erfa_iau06_angles(at, latitude=lat, longitude=lon)
        sw = swiss_angle_reference(at, latitude=lat, longitude=lon)
        plus = erfa_iau06_angles(at, latitude=lat, longitude=lon,
                                dut1_seconds=0.9)
        minus = erfa_iau06_angles(at, latitude=lat, longitude=lon,
                                 dut1_seconds=-0.9)
        # Swiss house systems all have a common physical Ascendant/MC.
        alternative_houses = [
            swiss_angle_reference(at, latitude=lat, longitude=lon,
                                  house_system=name)
            for name in (b"W",b"E",b"O",b"R")
        ]
        row={
            "utc":at.isoformat(),"latitude":lat,"longitude":lon,
            "IAU_asc":iau["asc"],"IAU_mc":iau["mc"],
            "SWISS_asc":sw[0],"SWISS_mc":sw[1],
            "asc_error_arcsec":circular_arcseconds(iau["asc"],sw[0]),
            "mc_error_arcsec":circular_arcseconds(iau["mc"],sw[1]),
            "east_horizon_dot":iau["east_dot"],
            "western_intersection_deg":(iau["asc"]+180)%360,
            "western_east_dot":-iau["east_dot"],
            "DUT1_perturbation_asc_arcsec":max(
                circular_arcseconds(iau["asc"],plus["asc"]),
                circular_arcseconds(iau["asc"],minus["asc"])),
            "DUT1_perturbation_mc_arcsec":max(
                circular_arcseconds(iau["mc"],plus["mc"]),
                circular_arcseconds(iau["mc"],minus["mc"])),
            "max_swiss_house_system_asc_diff_arcsec":max(
                circular_arcseconds(sw[0],v[0]) for v in alternative_houses),
            "max_swiss_house_system_mc_diff_arcsec":max(
                circular_arcseconds(sw[1],v[1]) for v in alternative_houses),
        }
        samples.append(row)
    return {
        "schema":"HUMANDESIGN_C32_INDEPENDENT_IAU_ANGLE_PARITY_V1",
        "scope":"DETERMINISTIC_SYNTHETIC_ONLY_PRIVATE_CASE_NOT_INCLUDED",
        "seed":SYNTHETIC_SEED,
        "count":len(samples),
        "era":"1960_TO_2026_INCLUSIVE",
        "latitude_range":"-65_TO_+65",
        "Swiss_library_version":swe.version,
        "ERFA_version":erfa.__version__,
        "Swiss_python_binary_sha256":hashlib.sha256(Path(swe.__file__).read_bytes()).hexdigest(),
        "ERFA_C_binary_sha256":hashlib.sha256(Path(erfa.ufunc.__file__).read_bytes()).hexdigest(),
        "max_abs_asc_error_arcseconds":max(x["asc_error_arcsec"] for x in samples),
        "max_abs_mc_error_arcseconds":max(x["mc_error_arcsec"] for x in samples),
        "max_abs_DUT1_plusminus_0p9s_asc_shift_arcseconds":
            max(x["DUT1_perturbation_asc_arcsec"] for x in samples),
        "max_abs_DUT1_plusminus_0p9s_mc_shift_arcseconds":
            max(x["DUT1_perturbation_mc_arcsec"] for x in samples),
        "min_eastern_point_east_dot":min(x["east_horizon_dot"] for x in samples),
        "max_house_system_asc_disagreement_arcseconds":
            max(x["max_swiss_house_system_asc_diff_arcsec"] for x in samples),
        "max_house_system_mc_disagreement_arcseconds":
            max(x["max_swiss_house_system_mc_diff_arcsec"] for x in samples),
        "IAU_2006_2000A_source_independent_from_Swiss_house_calculator":True,
        "UT1_UTC_assumed_zero_not_actual_historical_EOP":True,
        "not_an_independent_birthplace_timezone_audit":True,
        "original_wrong_horizon_code_and_input_receipt_not_available":True,
        "incident_suggested_class":"EAST_WEST_HORIZON_ANTIPODE_180_DEG",
        "cannot_prove_original_program_defect_from_synthetic_parity":True,
        "human_predictive_validations":0,
        "production_runtime_modified":False,
        "human_personal_inputs_included":False,
        "samples":samples
    }


if __name__=="__main__":
    print(json.dumps(audit_synthetic(),sort_keys=True,indent=2))
