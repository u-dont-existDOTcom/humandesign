#!/usr/bin/env python3
"""Compare pinned Swiss positions with an independent Astropy+jplephem DE440s path.

This audit is deliberately descriptive on its first run: it records angular
agreement and actual IAU constellation membership without choosing a tolerance
post hoc. A later certification can freeze thresholds after the first report is
archived.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

import astropy.units as u
from astropy.coordinates import GeocentricTrueEcliptic, get_body, get_constellation
from astropy.time import Time

from hdmatch.chart.ephemeris import CelestialBody, SwissEphemerisProvider

BODIES = (
    CelestialBody.SUN,
    CelestialBody.MOON,
    CelestialBody.MERCURY,
    CelestialBody.VENUS,
    CelestialBody.MARS,
    CelestialBody.JUPITER,
    CelestialBody.SATURN,
    CelestialBody.URANUS,
    CelestialBody.NEPTUNE,
)

SAMPLES = (
    datetime(1930, 1, 1, 0, 0, tzinfo=UTC),
    datetime(1950, 1, 1, 0, 0, tzinfo=UTC),
    datetime(1985, 1, 29, 10, 25, tzinfo=UTC),
    datetime(2000, 1, 1, 12, 0, tzinfo=UTC),
    datetime(2026, 8, 27, 0, 0, tzinfo=UTC),
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _angular_error_arcsec(a: float, b: float) -> float:
    delta = abs((a - b + 180.0) % 360.0 - 180.0)
    return delta * 3600.0


def _astropy_body_name(body: CelestialBody) -> str:
    return body.value.lower().replace(" ", "-")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--swiss-file",
        action="append",
        required=True,
        type=Path,
        help="Authorized Swiss .se1 file; repeat for planet and Moon files",
    )
    parser.add_argument("--de440s", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    kernel = args.de440s.resolve(strict=True)
    swiss_files = tuple(path.resolve(strict=True) for path in args.swiss_file)
    swiss = SwissEphemerisProvider(swiss_files)
    rows: list[dict[str, object]] = []
    maxima: dict[str, float] = {}

    for when in SAMPLES:
        time = Time(when)
        ecliptic_frame = GeocentricTrueEcliptic(equinox=time, obstime=time)
        for body in BODIES:
            swiss_lon = swiss.position(body, when).longitude
            gcrs = get_body(_astropy_body_name(body), time, ephemeris=str(kernel))
            ecliptic = gcrs.transform_to(ecliptic_frame)
            jpl_lon = float(ecliptic.lon.to_value(u.deg) % 360.0)
            error = _angular_error_arcsec(swiss_lon, jpl_lon)
            constellation = str(
                get_constellation(gcrs, short_name=True, constellation_list="iau")
            )
            maxima[body.value] = max(maxima.get(body.value, 0.0), error)
            rows.append(
                {
                    "observed_at_utc": when.isoformat().replace("+00:00", "Z"),
                    "body": body.value,
                    "swiss_tropical_longitude_deg": swiss_lon,
                    "de440s_tropical_longitude_deg": jpl_lon,
                    "absolute_angular_error_arcsec": error,
                    "iau_constellation": constellation,
                }
            )

    payload = {
        "schema_version": "de440s-astropy-swiss-audit-v1",
        "claim_boundary": (
            "Descriptive first-run numerical audit. No pass/fail tolerance was selected "
            "after observing these results."
        ),
        "de440s": {
            "filename": kernel.name,
            "sha256": _sha256(kernel),
            "size_bytes": kernel.stat().st_size,
            "source": "NASA/JPL NAIF generic_kernels/spk/planets/de440s.bsp",
        },
        "swiss": asdict(swiss.metadata),
        "sample_count": len(rows),
        "max_absolute_error_arcsec_by_body": maxima,
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print("de440s_sha256", payload["de440s"]["sha256"])
    print("max_absolute_error_arcsec_by_body", json.dumps(maxima, sort_keys=True))


if __name__ == "__main__":
    main()
