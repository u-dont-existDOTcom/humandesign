#!/usr/bin/env python3
"""Generate distinct, visibly sourced true-solar timeline examples and key comparison.

No personal or known life events are used. Do not fit a key to a real event.
"""

from __future__ import annotations

import csv
import json
import os
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.astrology.sky import snapshot_from_swiss_files
from hdmatch.astrology.solar_time_keys import SolarRAEngine, SolarTimeKey
from hdmatch.astrology.timeline import TimeKey, degrees_per_symbolic_year

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
EPHE = Path(
    os.environ.get(
        "HDMATCH_PRIMARY_DIR_EPHE_DIR",
        str(Path.home() / ".local/share/hdmatch/ephemeris/1800-2399"),
    )
)
cases = [
    ("synthetic_2000_january", datetime(2000, 1, 1, 12, tzinfo=UTC), 45.0, 0.0),
    ("synthetic_2000_july", datetime(2000, 7, 1, 18, tzinfo=UTC), -34.0, -70.0),
    ("synthetic_2026_march", datetime(2026, 3, 19, 6, tzinfo=UTC), 45.0, 24.0),
]
rows = []
for label, birth, lat, lon in cases:
    sky = snapshot_from_swiss_files(
        birth, latitude_deg=lat, longitude_east_deg=lon, ephemeris_directory=EPHE
    )
    solver = SolarRAEngine(sky, EPHE)
    rate, low, high = solver.birth_date_brahe_rate()
    for arc in (1.0, 25.0, 50.0, 75.0, 90.0):
        for method in (
            TimeKey.PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR.value,
            TimeKey.NAIBOD_59M08S_FIXED_DIAGNOSTIC.value,
            SolarTimeKey.BRAHE_TRUE_MIDNIGHT_BIRTH_DAY.value,
            SolarTimeKey.PLACIDUS_CUMULATIVE_TRUE_SOLAR_RA.value,
        ):
            if method == SolarTimeKey.BRAHE_TRUE_MIDNIGHT_BIRTH_DAY.value:
                years = arc / rate
            elif method == SolarTimeKey.PLACIDUS_CUMULATIVE_TRUE_SOLAR_RA.value:
                years = solver.placidus_age_for_arc(arc)
            else:
                years = arc / degrees_per_symbolic_year(TimeKey(method))
            rows.append(
                {
                    "case": label,
                    "birth_utc": birth.isoformat(),
                    "latitude_north_deg": lat,
                    "longitude_east_deg": lon,
                    "arc_deg": arc,
                    "method": method,
                    "age_model_years": years,
                    "birth_day_solar_rate_deg": rate,
                    "true_midnight_start_utc": low.isoformat(),
                    "true_midnight_end_utc": high.isoformat(),
                    "label": "ARITHMETIC_DIAGNOSTIC_ONLY_NO_EVENT_PREDICTIONS",
                }
            )
assert len(rows) == 3 * 5 * 4
outfile = HERE / "SOLAR_KEY_3_CHART_SENSITIVITY.csv"
with outfile.open("w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    wr.writeheader()
    wr.writerows(rows)

data = {
    "status": "MATHEMATICAL_RESEARCH_TEST_NOT_HISTORICAL_PROOF",
    "case_count": len(cases),
    "compared_arcs": [1, 25, 50, 75, 90],
    "profiles": [v.value for v in SolarTimeKey],
    "strict_ephemeris": "SWIEPH returned flags+verified file path+file SHA",
    "rows": len(rows),
    "rates": {
        key: [
            {
                k: x[k]
                for k in (
                    "birth_utc",
                    "latitude_north_deg",
                    "longitude_east_deg",
                    "birth_day_solar_rate_deg",
                    "true_midnight_start_utc",
                    "true_midnight_end_utc",
                )
            }
            for x in rows
            if x["case"] == key
            and x["arc_deg"] == 1
            and x["method"] == SolarTimeKey.BRAHE_TRUE_MIDNIGHT_BIRTH_DAY.value
        ]
        for key, _, _, _ in cases
    },
}
(HERE / "COMPARISON_METADATA.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n"
)
print(
    json.dumps(
        {
            "cases": len(cases),
            "rows": len(rows),
            "rates": {k: v[0]["birth_day_solar_rate_deg"] for k, v in data["rates"].items()},
        },
        indent=2,
    )
)
