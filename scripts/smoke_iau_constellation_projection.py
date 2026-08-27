#!/usr/bin/env python3
"""Exercise the actual-sky IAU constellation projection on pinned Swiss states."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import swisseph as swe

from hdmatch.chart.astronomy_reference import (
    AstronomyProvenance,
    AstropyIauConstellationResolver,
    EphemerisFileProvenance,
    ObserverOrigin,
    ReferenceFrame,
    SwissAstronomyReferenceProvider,
    iau_constellation,
)

SAMPLES = (
    (datetime(2026, 1, 1, 12, tzinfo=UTC), "Sagittarius", "Sgr"),
    (datetime(2026, 4, 1, 12, tzinfo=UTC), "Pisces", "Psc"),
    (datetime(2026, 7, 1, 12, tzinfo=UTC), "Gemini", "Gem"),
    (datetime(2026, 10, 1, 12, tzinfo=UTC), "Virgo", "Vir"),
    # A direct demonstration that actual IAU zodiac membership includes the
    # thirteenth ecliptic constellation rather than twelve equal signs.
    (datetime(2026, 12, 5, 12, tzinfo=UTC), "Ophiuchus", "Oph"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ephemeris", required=True, type=Path)
    parser.add_argument("--astropy-version", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _julian_day(moment: datetime) -> float:
    hour = moment.hour + moment.minute / 60.0 + moment.second / 3600.0
    return swe.julday(moment.year, moment.month, moment.day, hour, swe.GREG_CAL)


def main() -> None:
    args = parse_args()
    files = tuple(sorted(args.ephemeris.glob("*.se1")))
    if not files:
        raise SystemExit("no Swiss .se1 files found")
    swe.set_ephe_path(str(args.ephemeris.resolve()))
    provenance = AstronomyProvenance(
        provider="Swiss Ephemeris",
        provider_version=str(swe.version),
        package="pyswisseph",
        input_time_scale="UT",
        origin=ObserverOrigin.GEOCENTRIC,
        native_frame=ReferenceFrame.ECLIPTIC_OF_DATE,
        calculation_flags=("FLG_SWIEPH", "FLG_SPEED", "apparent/of-date"),
        source_files=tuple(
            EphemerisFileProvenance(name=path.name, sha256=_sha(path)) for path in files
        ),
        notes=(
            "IAU resolver interprets Swiss apparent state as geocentric true ecliptic of date.",
        ),
    )
    provider = SwissAstronomyReferenceProvider(engine=swe, provenance=provenance)
    resolver = AstropyIauConstellationResolver(
        expected_astropy_version=args.astropy_version
    )

    rows: list[dict[str, object]] = []
    for moment, expected_name, expected_abbreviation in SAMPLES:
        state = provider.state(
            jd_ut=_julian_day(moment),
            observed_at_utc=moment,
            body_name="Sun",
            body_id=swe.SUN,
        )
        projection = iau_constellation(state, resolver=resolver)
        if projection.name != expected_name or projection.abbreviation != expected_abbreviation:
            raise RuntimeError(
                f"unexpected Sun constellation at {moment.isoformat()}: "
                f"{projection.name} ({projection.abbreviation}), expected "
                f"{expected_name} ({expected_abbreviation})"
            )
        rows.append(
            {
                "observed_at_utc": moment.isoformat(),
                "tropical_ecliptic_longitude_deg": state.ecliptic_longitude_deg,
                "ecliptic_latitude_deg": state.ecliptic_latitude_deg,
                "iau_constellation": projection.name,
                "iau_abbreviation": projection.abbreviation,
                "resolver": projection.resolver,
                "resolver_version": projection.resolver_version,
                "boundary_reference": projection.boundary_reference,
            }
        )

    report = {
        "schema_version": "iau-constellation-smoke-v1",
        "astropy_version": resolver.version,
        "boundary_reference": "IAU-88-Delporte-B1875-Roman1987",
        "coordinate_input": "Swiss geocentric true/apparent ecliptic of date",
        "samples": rows,
    }
    rendered = json.dumps(report, sort_keys=True, indent=2)
    print(rendered, flush=True)
    args.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
