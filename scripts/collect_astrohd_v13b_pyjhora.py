#!/usr/bin/env python3
"""Collect frozen PyJHora Shadbala strengths for AstroHD V1.3b.

PyJHora is an external private-development oracle. This script imports it from
an exact checked-out source tree; no PyJHora code is copied into this project.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

EXPECTED_ENGINE_COMMIT = "48e57d29b47a3143519910a24866758116467485"
PYJHORA_PLANET_ORDER = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--pyjhora-src", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    freeze = json.loads(args.freeze.read_text())
    _verify_engine_commit(args.pyjhora_src)
    sys.path.insert(0, str(args.pyjhora_src))

    from jhora import utils  # type: ignore[import-not-found]
    from jhora.horoscope.chart import strength  # type: ignore[import-not-found]
    from jhora.panchanga import drik  # type: ignore[import-not-found]

    drik.set_ayanamsa_mode("LAHIRI")

    queries = freeze["direct_queries"]
    rows = [
        ("target", queries["target"]),
        ("persistent_competitor", queries["persistent_competitor"]),
        *[
            (f"same_date_{index}", value)
            for index, value in enumerate(queries["same_date_alternative_midpoints"])
        ],
    ]

    zone = ZoneInfo("America/New_York")
    results = []
    for label, raw in rows:
        utc = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        local = utc.astimezone(zone)
        offset_hours = local.utcoffset().total_seconds() / 3600.0
        place = drik.Place("Philadelphia", 39.9526, -75.1652, offset_hours)
        dob = (local.year, local.month, local.day)
        tob = (local.hour, local.minute, local.second + local.microsecond / 1_000_000.0)
        jd = utils.julian_day_number(dob, tob)
        shadbala = strength.shad_bala(jd, place)
        normalized = shadbala[8]
        if len(normalized) != 7:
            raise RuntimeError(f"unexpected Shadbala output length: {len(normalized)}")
        by_planet = {
            planet: float(normalized[index])
            for index, planet in enumerate(PYJHORA_PLANET_ORDER)
        }
        results.append(
            {
                "label": label,
                "timestamp_utc": utc.isoformat(),
                "local_datetime": local.isoformat(),
                "timezone_offset_hours": offset_hours,
                "normalized_shadbala_strength": by_planet,
            }
        )

    report = {
        "schema": "astrohd-v1.3b-pyjhora-shadbala-oracle-v1",
        "engine": "PyJHora strength.shad_bala",
        "engine_commit": EXPECTED_ENGINE_COMMIT,
        "ayanamsha": "LAHIRI",
        "location": {"name": "Philadelphia", "latitude": 39.9526, "longitude": -75.1652},
        "freeze_sha256": hashlib.sha256(args.freeze.read_bytes()).hexdigest(),
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(args.output)


def _verify_engine_commit(src: Path) -> None:
    root = src.parent if src.name == "src" else src
    actual = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    if actual != EXPECTED_ENGINE_COMMIT:
        raise RuntimeError(
            f"PyJHora commit mismatch: expected {EXPECTED_ENGINE_COMMIT}, got {actual}"
        )


if __name__ == "__main__":
    main()
