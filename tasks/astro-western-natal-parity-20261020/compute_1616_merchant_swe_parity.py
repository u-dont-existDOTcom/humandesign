#!/usr/bin/env python3
"""William Lilly 1616 merchant nativity: first-edition literal vs SWIEPH.

Source-only diagnostic comparing ORIGINAL printed seven natal longitudes against
a separately computed modern Swiss planetary ephemeris. The source merchant
was KNOWN TO LILLY; this is NOT a prospective or independently blinded
astrology human result.

Calendar hypothesis: source written 1616-09-19 Julian OR Gregorian, explicit.
Time hypothesis: printed '2 h. 24. 39 P.M.' treated ONLY FOR REFERENCE as
14:24:39 UT, not independently known original longitude/local-solar basis.
Sensitivity ±1h/±2h recorded, not optimized for best subjective fit.

Must have official 2026 DE441 Swiss .se1 files in external, locally supplied
directory, checksum exact; no fallback to Moshier regardless of API success.
The .se1 binaries are NOT committed or redistributed with the project.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
from hashlib import sha256
from pathlib import Path
from typing import Any

import swisseph as swe

ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = (
    ROOT
    / "tasks/astro-source-audit-multipass-20261005/batches/B07ax"
    / "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json"
)
SOURCE_PDF_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
EPHE_FILES = {
    "sepl_12.se1": "8dccace2557601a223d5f8a7cf64de4e6bbb8a82b9b130b95a54d49adfbe546d",
    "semo_12.se1": "1c65fdbb854f350d3de36afc3e4ac126a53f360ae4f6dcb57beed7c690e7eb61",
}
EPHE_SOURCE = "https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/"
PRINTED_BODIES = {
    "Saturn": swe.SATURN,
    "Jupiter": swe.JUPITER,
    "Mars": swe.MARS,
    "Sun": swe.SUN,
    "Venus": swe.VENUS,
    "Mercury": swe.MERCURY,
    "Moon": swe.MOON,
}
ZODIAC = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
REFERENCE_CLOCK_UT_HOURS_ASSUMED = 14 + 24 / 60 + 39 / 3600
SENSITIVITY_OFFSETS_HOURS = (-2, -1, 0, 1, 2)


def source_original() -> tuple[dict[str, float], str]:
    raw = SOURCE_PATH.read_bytes()
    manifest = json.loads(raw.decode("utf-8"))
    if manifest["1647_Wellcome_full_pdf_sha256"] != SOURCE_PDF_SHA:
        raise ValueError("Original full-book PDF fingerprint differs")
    rows = manifest["records"]
    if len(rows) != 7 or {r["source_body"] for r in rows} != set(PRINTED_BODIES):
        raise ValueError("Original source no longer contains the seven printed bodies")
    original: dict[str, float] = {}
    for row in rows:
        sign, deg, minute = row["original_first_1647_and_second_1659_printed_natal_longitude"]
        if sign not in ZODIAC or not all(type(x) is int for x in (deg, minute)):
            raise ValueError("Original planet zodiac glyph invalid")
        if not (0 <= deg < 30 and 0 <= minute < 60):
            raise ValueError("Original planet sign degree/minute invalid")
        original[row["source_body"]] = 30 * ZODIAC.index(sign) + deg + minute / 60
        if not row["source_physical_edition_single_reader_verified"]:
            raise ValueError("Original seven-text row lacks physical image provenance")
    if manifest["historical_source_natal_longitude_chart_recomputed"]:
        raise ValueError("Original source was expected to preserve unsolved ephemeris parity")
    return original, sha256(raw).hexdigest()


def validate_ephe_dir(ephe_dir: Path) -> dict[str, dict[str, Any]]:
    if not ephe_dir.is_dir() or not ephe_dir.is_absolute():
        raise ValueError("Require an explicit existing absolute ephemeris directory")
    if os.environ.get("SE_EPHE_PATH"):
        raise ValueError("Refuse hidden SE_EPHE_PATH overriding supplied verified files")
    witnesses: dict[str, dict[str, Any]] = {}
    for filename, expected_hash in EPHE_FILES.items():
        blob = (ephe_dir / filename).read_bytes()
        actual = sha256(blob).hexdigest()
        if actual != expected_hash:
            raise ValueError(f"Ephemeris file {filename} SHA256 mismatch")
        witnesses[filename] = {
            "original_upstream_url": EPHE_SOURCE + filename,
            "sha256": actual,
            "bytes": len(blob),
            "released_outside_repo_binary_copied_into_humandesign": False,
        }
    return witnesses


def strict_swieph_body(julian_day_ut: float, body: int) -> tuple[float, int]:
    result, returned_flags = swe.calc_ut(
        julian_day_ut, body, swe.FLG_SWIEPH | swe.FLG_SPEED
    )
    if not returned_flags & swe.FLG_SWIEPH or returned_flags & swe.FLG_MOSEPH:
        raise ValueError(
            f"SWIEPH requested but actual returned flags {returned_flags} "
            "indicate missing files / fallback. No astronomical parity admitted."
        )
    lon = result[0] % 360.0
    if not 0 <= lon < 360:
        raise ValueError("No finite tropical geocentric ecliptic longitude")
    return lon, returned_flags


def signed_arcminutes(predicted: float, printed: float) -> float:
    """Calculated minus historic printed degree, in signed circular arcmin."""
    return ((predicted - printed + 180) % 360 - 180) * 60


def time_grid_for_calendar(printed: dict[str, float], calendar: int) -> dict[str, Any]:
    ref_jd = swe.julday(1616, 9, 19, REFERENCE_CLOCK_UT_HOURS_ASSUMED, calendar)
    source_name = "Julian" if calendar == swe.JUL_CAL else "Gregorian"
    nsign = 0
    rows: list[dict[str, Any]] = []
    for body_name, pl in PRINTED_BODIES.items():
        printed_longitude = printed[body_name]
        positions = []
        for t in SENSITIVITY_OFFSETS_HOURS:
            lon, returned_flags = strict_swieph_body(ref_jd + t / 24.0, pl)
            positions.append({
                "reference_clock_offset_hours": t,
                "solar_tropical_geocentric_ecliptic_longitude_degrees": round(lon, 8),
                "difference_vs_1647_printed_arcminutes": round(
                    signed_arcminutes(lon, printed_longitude), 5
                ),
                "returned_flags": returned_flags,
                "actual_SWIEPH": bool(returned_flags & swe.FLG_SWIEPH),
                "actual_MOSEPH_fallback": bool(returned_flags & swe.FLG_MOSEPH),
            })
        central = next(p for p in positions if p["reference_clock_offset_hours"] == 0)
        calculated_sign = ZODIAC[
            int(central["solar_tropical_geocentric_ecliptic_longitude_degrees"] // 30)
        ]
        printed_sign = ZODIAC[int(printed_longitude // 30)]
        match = calculated_sign == printed_sign
        nsign += match
        rows.append({
            "source_body": body_name,
            "printed_original_first_second_edition_longitude_degrees": round(
                printed_longitude, 8
            ),
            "printed_zodiac": printed_sign,
            "computed_zodiac": calculated_sign,
            "sign_matches": match,
            "reference_UT_assumption_arcminute_difference": central[
                "difference_vs_1647_printed_arcminutes"
            ],
            "time_sensitivity_plus_minus_2h": positions,
        })
    arr = [abs(r["reference_UT_assumption_arcminute_difference"]) for r in rows]
    return {
        "hypothesis": source_name + " calendar date as 1616-09-19",
        "source_wrote_year_month_day": [1616, 9, 19],
        "calendar_mode": source_name,
        "modern_UT_clock_assumed_HHMMSS": "14:24:39",
        "original_clock_was_UT_independently_verified": False,
        "julian_day_UT_for_reference_assumption": round(ref_jd, 10),
        "matching_original_zodiac_signs": nsign,
        "total_printed_zodiac_signs": len(rows),
        "mean_abs_arcminute_longitude_residual_at_unverified_UT": round(
            statistics.mean(arr), 5
        ),
        "median_abs_arcminute_longitude_residual_at_unverified_UT": round(
            statistics.median(arr), 5
        ),
        "max_abs_arcminute_longitude_residual_at_unverified_UT": round(
            max(arr), 5
        ),
        "body_reports": rows,
    }


def compute(ephe_dir: Path) -> dict[str, Any]:
    witnesses = validate_ephe_dir(ephe_dir)
    original, original_sha = source_original()
    swe.close()
    swe.set_ephe_path(str(ephe_dir))
    julian = time_grid_for_calendar(original, swe.JUL_CAL)
    gregorian = time_grid_for_calendar(original, swe.GREG_CAL)
    conversion_jd = swe.julday(1616, 9, 19, 0, swe.JUL_CAL)
    converted = swe.revjul(conversion_jd, swe.GREG_CAL)
    if converted[:3] != (1616, 9, 29):
        raise ValueError("Swiss Julian/Gregorian historical 1616 date conversion failed")
    if not julian["matching_original_zodiac_signs"] > gregorian["matching_original_zodiac_signs"]:
        raise ValueError("Predeclared Julian calendar did not better match source zodiac signs")
    report = {
        "title": (
            "Lilly CLXXV merchant historical source-versus-modern-Swiss "
            "ephemeris, Julian/Gregorian hypotheses"
        ),
        "status": (
            "RESEARCH SOURCE CALENDAR-AND-ASTRONOMY DIAGNOSTIC, NOT VERIFIED "
            "HISTORIC ACTUAL NATAL CHART OR HUMAN FORECAST"
        ),
        "independent_source_original": (
            "1647 first + separately typeset 1659 second print, merchant Chapter CLXXV"
        ),
        "original_image_witness": str(SOURCE_PATH.relative_to(ROOT)),
        "original_source_witness_SHA256": original_sha,
        "original_Wellcome_whole_original_1647_pdf_SHA256": SOURCE_PDF_SHA,
        "source_printed_birth_year_month_day": [1616, 9, 19],
        "source_printed_birth_clock_text": "2 h. 24. 39 P.M.",
        "source_printed_latitude_degrees": 53,
        "source_birthplace_precise_longitude_independently_known": False,
        "source_birth_clock_UT_or_apparent_local_solar_independently_known": False,
        "source_old_new_style_calendar_externally_birth_registered": False,
        "source_author_already_knows_native": True,
        "independently_verified_human_prediction": False,
        "calc_library": "pyswisseph",
        "calc_library_version": swe.version,
        "swisseph_600_year_file_span": "1200-1799 CE",
        "external_official_2026_DE441_ephemeris_file_witnesses": witnesses,
        "underlying_ephemeris_source": (
            "Official Alois Treindl Swiss Ephemeris 2026 DE441-based .se1"
        ),
        "calc_requested_swieph": True,
        "calc_returned_swieph_for_all_70_positions": True,
        "calc_any_moshier_fallback": False,
        "zodiac_tropical_geocentric_ecliptic_apparent": True,
        "source_planet_positions_7": {k: round(v,8) for k,v in original.items()},
        "julian_date_written_1616_09_19_as_gregorian_reference": "1616-09-29",
        "assumption_sensitivity_hours": list(SENSITIVITY_OFFSETS_HOURS),
        "julian_original_calendar_hypothesis": julian,
        "gregorian_original_calendar_hypothesis": gregorian,
        "claimed_independent_original_birth_certificate": False,
        "independent_natal_house_geometry_reconstruction": False,
        "independent_historical_ephemeris_exact_natal_parity": False,
        "real_person_prospective_blind_prediction_count": 0,
        "runtime_astrological_promotions": 0,
        "historical_source_records_added": 0,
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ephe-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = compute(args.ephe_dir)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    for label in ("julian_original_calendar_hypothesis", "gregorian_original_calendar_hypothesis"):
        r = result[label]
        print("HYPOTHESIS", r["calendar_mode"], "signs",
              r["matching_original_zodiac_signs"], "/7", "median_abs_min",
              r["median_abs_arcminute_longitude_residual_at_unverified_UT"])
        for row in r["body_reports"]:
            print("BODY",row["source_body"],row["printed_zodiac"],
                  row["computed_zodiac"],"residual_arcmin",
                  row["reference_UT_assumption_arcminute_difference"])
    print("OUTPUT",args.output)


if __name__ == "__main__":
    main()
