"""Critical-source reconciliation: 1647 original vs 2003 Lilly/Naibod witness.

Original 1647 first-edition *page photographs* are now available and
independently VIEWED (Wikimedia Commons, CA_William_Lilly_.pdf,
PDF pages 735–737 / printed pages 713–715). Earlier 2003 re-typesetting:
WorldAstrology CA-III.pdf, printed pages 713–715 / PDF 226–228.

DO NOT overwrite either source: the 2003 transcription mistakenly labels
printed YEARS for degrees 69–90 with the degree number, whereas in the 1647
original those YEARS increment by one (69°->70y, 90°->91y). The 1647
narrative conclusion of the 19°52' worked example says TWENTY years,
not TWENTY-TWO as the 2003 retype prints.

Other minute-table anomalies, including absent 27', are visibly present
in the 1647 first-edition scan; beware inferring an editorial correction
for them. This is still a DIAGNOSTIC witness comparison, NOT a continuous
historical time-key for fractions/seconds.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .historical_naibod import (
    DEGREE_COMPONENTS,
    MINUTE_COMPONENTS,
    literal_naibod_lookup,
)

ORIGINAL_1647_WITNESS = (
    "William Lilly Christian Astrology 1647 facsimile, public domain; "
    "Wikimedia Commons File:Christian Astrology (IA ca-william-lilly).pdf; "
    "PDF pages 735–737 (1-based), printed pages 713–715; "
    "critical degree-year column, specific table anomalies, and both "
    "worked conclusions independently viewed"
)

YEAR_COLUMN_1647: tuple[int, ...] = tuple(
    (degree if degree <= 68 else degree + 1) for degree in range(91)
)
assert len(YEAR_COLUMN_1647) == 91


@dataclass(frozen=True, slots=True)
class ComparedNaibod1647:
    arc_degrees: int
    arc_minutes: int
    first_edition_degree_years: int
    literal_days_from_degree: int
    literal_hours_from_degree: int
    literal_days_from_minutes: int
    literal_hours_from_minutes: int
    resulting_years: int
    resulting_days: int
    resulting_hours: int
    differences_from_2003: tuple[str, ...]
    source_limits: str = (
        "First-edition year column at degrees 69–90 and 19°52' conclusion "
        "visually verified; other day/hour cells reused from the 2003 "
        "witness with selected checks against the 1647 photograph, "
        "NOT an exhaustive cell-by-cell photographic collation."
    )
    witness: str = ORIGINAL_1647_WITNESS

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["candidate_status"] = "source_compared_not_full_original_collation"
        result["not_continuous_timeline_key"] = True
        return result


def original_1647_critical_comparison(degrees: int, minutes: int) -> ComparedNaibod1647:
    """Compare 1647 printed-year column with the separate 2003 literal rows.

    Full printed years after 68° are independently checked against the
    first-edition degree table. Other numerical digits are REUSED from the
    2003 witness, not claimed to have been exhaustively transcribed twice.
    """
    retyped = literal_naibod_lookup(degrees, minutes)
    day_deg, hour_deg = DEGREE_COMPONENTS[degrees]
    day_min, hour_min = MINUTE_COMPONENTS[minutes]
    year = YEAR_COLUMN_1647[degrees]
    total_hours = hour_deg + hour_min
    total_days = day_deg + day_min + total_hours // 24
    years = year + total_days // 365
    days = total_days % 365
    hour = total_hours % 24
    difference: list[str] = []
    if degrees >= 69:
        difference.append(
            f"original_1647_year_column:{degrees}°={year}y; 2003_retype:{degrees}°={degrees}y"
        )
    if (degrees, minutes) == (19, 52):
        difference.append(
            "original_1647_worked_conclusion:twenty_years; "
            "2003_retype_worked_conclusion:twenty_two_years"
        )
    for issue in retyped.warnings:
        if degrees >= 69 and "degree-table DAYS resets" in issue:
            # The 1647 ORIGINAL explicitly carries the year in the YEARS
            # column; the 2003 retypesetting lost this carry. It is a
            # retype-only anomaly, not an anomaly shared with Lilly's scan.
            continue
        if (degrees, minutes) == (19, 52) and "22y57d21h" in issue:
            # The "22" is only in the modern retype. The original's
            # correctly stated result remains distinguished above.
            continue
        difference.append("shared_or_unresolved_source_anomaly:" + issue)
    return ComparedNaibod1647(
        arc_degrees=degrees,
        arc_minutes=minutes,
        first_edition_degree_years=year,
        literal_days_from_degree=day_deg,
        literal_hours_from_degree=hour_deg,
        literal_days_from_minutes=day_min,
        literal_hours_from_minutes=hour_min,
        resulting_years=years,
        resulting_days=days,
        resulting_hours=hour,
        differences_from_2003=tuple(difference),
    )


def main(argv: list[str] | None = None) -> int:
    """Print the selectively collated original-witness diagnostic as JSON."""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description=(
            "Compare visibly verified 1647 Lilly Naibod year-column cells "
            "against 2003 retype. Other day/hour values are reused, not "
            "fully independently collated."
        )
    )
    parser.add_argument("--degrees", type=int, required=True)
    parser.add_argument("--minutes", type=int, required=True)
    args = parser.parse_args(argv)
    try:
        result = original_1647_critical_comparison(
            degrees=args.degrees,
            minutes=args.minutes,
        )
    except (ValueError, TypeError) as exc:
        parser.exit(status=2, message=f"unavailable witness cell: {exc}\n")
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
