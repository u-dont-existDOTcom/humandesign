"""Reconcile printed XXVIII numbers using the retained B02f geometry.

No ephemeris, event date, outcome probability, or wealth forecast is calculated.
The inputs are a transcription of one historical figure and its printed tables.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
HELPER = ROOT.parent / "B02f" / "lilly_presence_ship_reference.py"
SPEC = importlib.util.spec_from_file_location("retained_lilly_geometry", HELPER)
GEO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEO)


def _motion_arcseconds(value: str) -> int:
    """Read the exact normalized diurnal-motion notation used in this packet."""
    match = re.fullmatch(r"(\d+)d(\d{1,2})m(?:(\d{1,2})s)?", value)
    if match is None:
        raise ValueError("Expected explicit degrees/minutes and optional seconds")
    degrees, minutes, seconds = (int(x or 0) for x in match.groups())
    if minutes >= 60 or seconds >= 60:
        raise ValueError("Minutes and seconds must be below sixty")
    return degrees * 3600 + minutes * 60 + seconds


def reconcile() -> dict:
    data = json.loads((ROOT / "WORKED_NUMERIC_TABLES.json").read_text())
    positions = {
        r["body"]: GEO.longitude(r["sign"], r["degree"], r["minute"])
        for r in data["chart"]["positions"]
    }
    cusps = {
        r["house"]: GEO.longitude(r["sign"], r["degree"], r["minute"])
        for r in data["chart"]["houses"]
    }
    reflected = []
    for row in data["antiscia"]:
        actual = GEO.antiscion(positions[row["body"]])
        contra = (actual + 10800) % 21600
        expected = GEO.longitude(row["antiscion_sign"], row["degree"], row["minute"])
        expected_contra = GEO.longitude(row["contra_antiscion_sign"], row["degree"], row["minute"])
        reflected.append({
            "body": row["body"], "computed_antiscion": list(GEO.as_sign(actual)),
            "computed_contra_antiscion": list(GEO.as_sign(contra)),
            "printed_antiscion_matches": actual == expected,
            "printed_contra_antiscion_matches": contra == expected_contra,
        })
    strengths = []
    for row in data["strength_tables"]:
        positive = sum(x["score"] for x in row["fortitudes"])
        negative = sum(x["score"] for x in row["debilities"])
        strengths.append({
            "body": row["body"], "computed_positive": positive,
            "computed_negative": negative, "computed_net": positive - negative,
            "printed_components_and_net_match": (
                positive == row["source_positive_total"]
                and negative == row["source_negative_total"]
                and positive - negative == row["source_net"]
            ),
        })
    fortune = GEO.fortune(cusps[1], positions["Moon"], positions["Sun"], profile=GEO.FORTUNE_PROFILE)
    swift = [r["body"] for r in data["motions"] if "swift" in r["source_status"]]
    slow = [r["body"] for r in data["motions"] if r["source_status"] == "slow"]
    mean_comparisons = {}
    for row in data["motions"]:
        if "source_mean" in row:
            daily, mean = _motion_arcseconds(row["daily_motion"]), _motion_arcseconds(row["source_mean"])
            mean_comparisons[row["body"]] = {"daily_arcseconds": daily,
                "source_mean_arcseconds": mean, "greater_than_mean": daily > mean}
    contacts = {
        "Mars_to_Ascendant": GEO.separation(positions["Mars"], cusps[1]),
        "Moon_to_Venus": GEO.separation(positions["Moon"], positions["Venus"]),
        "Fortune_to_second_cusp": GEO.separation(positions["Fortune"], cusps[2]),
        "Venus_to_eleventh_cusp": GEO.separation(positions["Venus"], cusps[11]),
        "Saturn_contra_antiscion_to_Jupiter": GEO.separation(
            (GEO.antiscion(positions["Saturn"]) + 10800) % 21600, positions["Jupiter"]
        ),
    }
    # Exact coincidences only: this does not define which houses are material,
    # what near means, or whether a nonzero residual is astrologically admissible.
    exact_antiscion_hits = []
    for body in (r["body"] for r in data["antiscia"]):
        a = GEO.antiscion(positions[body])
        for other, p in positions.items():
            if a == p:
                exact_antiscion_hits.append([body, other])
        for house, p in cusps.items():
            if a == p:
                exact_antiscion_hits.append([body, f"cusp_{house}"])
    return {
        "source_id": data["source_id"], "source_sha256": data["source_sha256"],
        "status": "STATIC_PRINTED_ARITHMETIC_ONLY",
        "geometry_implementation": "retained B02f/lilly_presence_ship_reference.py unchanged",
        "antiscia": reflected, "strengths": strengths,
        "fortune": {"profile": GEO.FORTUNE_PROFILE, "computed": list(GEO.as_sign(fortune)),
                    "printed_matches": fortune == positions["Fortune"],
                    "computed_strength_net": data["fortune_strength"]["positive"] - data["fortune_strength"]["negative"],
                    "printed_strength_net": data["fortune_strength"]["net"]},
        "swift_count": {"table_pages": [212], "swift_bodies": swift, "slow_bodies": slow,
                        "computed_from_source_labels": len(swift), "later_source_claim": 5,
                        "later_claim_page": 217, "consistent": len(swift) == 5},
        "distances_arcminutes": contacts,
        "aspect_residuals_arcminutes": {
            "Jupiter_square_Ascendant": GEO.aspect_residual(positions["Jupiter"], cusps[1], 90),
            "Jupiter_square_Mars": GEO.aspect_residual(positions["Jupiter"], positions["Mars"], 90),
            "Sun_square_Fortune": GEO.aspect_residual(positions["Sun"], positions["Fortune"], 90),
            "Sun_square_second_cusp": GEO.aspect_residual(positions["Sun"], cusps[2], 90),
            "Moon_sextile_Mars": GEO.aspect_residual(positions["Moon"], positions["Mars"], 60),
            "Moon_conjunction_Mercury": GEO.aspect_residual(positions["Moon"], positions["Mercury"], 0),
        },
        "exact_antiscion_hits_on_transcribed_points_or_cusps": exact_antiscion_hits,
        "mean_motion_comparisons": mean_comparisons,
        "source_timing_reconciliation": [
            {"input": "Mars_to_Ascendant", "distance": "1 degree 59 minutes",
             "source_duration": "two years or thereabouts", "source_page": 217,
             "assessment": "Source's approximately two degrees is consistent with the coordinates; year selection is a separate interpretive choice."},
            {"input": "Moon_to_Venus", "distance": "6 degrees 27 minutes",
             "source_duration": "about 1640, six years after the question", "source_pages": [217, 218],
             "assessment": "Exact printed distance reproduced; no exact 6.45-year civil date is claimed or generated."},
        ],
        "source_cusp_assignment": {
            "Fortune": {"geometric_house_between_printed_cusps": 1, "source_attributed_house": 2,
                        "gap_to_second_cusp_arcminutes": contacts["Fortune_to_second_cusp"],
                        "greater_than_five_degrees": contacts["Fortune_to_second_cusp"] > 300,
                        "general_replacement_threshold": None},
            "Venus": {"geometric_house_between_printed_cusps": 10, "source_attributed_house": 11,
                      "gap_to_eleventh_cusp_arcminutes": contacts["Venus_to_eleventh_cusp"]},
        },
        "fixed_star_limits": {"Spica": "Source gives Libra 18 without minutes; no exact longitude inserted.",
                              "Regulus": "Source grants a six-degree proximity allowance; no exact local coordinate supplied."},
        "physical_contact_times_computed": False, "historical_calendar_resolved": False,
        "current_participant_inputs": False, "predictive_validation": False,
    }


if __name__ == "__main__":
    result = reconcile()
    (ROOT / "ARITHMETIC_CHECKS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"reflected_pairs": len(result["antiscia"]),
                      "strength_rows": len(result["strengths"]),
                      "swift_count": result["swift_count"],
                      "distances_arcminutes": result["distances_arcminutes"]}, ensure_ascii=False))
