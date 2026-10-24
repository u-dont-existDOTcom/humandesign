#!/usr/bin/env python3
"""Export a *literal* digitization from visually inspected 2003 retypesetting.

No correction of anomalous rows, and no conflation with the continuous key.
"""

import csv
import json
from pathlib import Path

from hdmatch.astrology.historical_naibod import (
    DEGREE_COMPONENTS,
    KNOWN_WITNESS_ISSUES,
    MINUTE_COMPONENTS,
    SOURCE_WITNESS,
    literal_naibod_lookup,
)
from hdmatch.astrology.timeline import TimeKey, degrees_per_symbolic_year

root = Path("docs/astrology-research-map/gansten-lilly-naibod-20261024")
root.mkdir(parents=True, exist_ok=True)
rows = []
for i, (days, hours) in enumerate(DEGREE_COMPONENTS):
    flags = []
    if i >= 69:
        flags.append("degree_69_to_90:carried_year_missing")
    if i == 80:
        flags.append("degree_80_hour_24:unnormalized_hours")
    rows.append(
        {
            "table": "degree_component",
            "source_printed_page": 713,
            "row_label": i,
            "printed_years": i,
            "printed_days": days,
            "printed_hours": hours,
            "status": "printed_row" if i else "added_zero_identity",
            "warnings": ";".join(flags),
        }
    )
for i in range(61):
    val = MINUTE_COMPONENTS.get(i)
    flags = []
    if i == 8:
        flags.append("minute_8:day_discontinuity")
    if i == 27:
        flags.append("minute_27:missing_label_and_values")
    if i in (28, 29, 30):
        flags.append("minute_28_to_30:possibly_shifted_labels")
    if i == 44:
        flags.append("minute_44:unusual_hours")
    if i == 60:
        flags.append("minute_60:disagrees_with_one_degree")
    rows.append(
        {
            "table": "minute_component",
            "source_printed_page": 714,
            "row_label": i,
            "printed_years": "",
            "printed_days": "" if val is None else val[0],
            "printed_hours": "" if val is None else val[1],
            "status": (
                "missing_in_witness"
                if val is None
                else "added_zero_identity"
                if i == 0
                else "printed_row"
            ),
            "warnings": ";".join(flags),
        }
    )
path = root / "LILLY_NAIBOD_2003_RETYPED_LITERAL_CELLS.csv"
with path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
assert len(rows) == 152, len(rows)

issues = []
for key, description in KNOWN_WITNESS_ISSUES.items():
    issues.append(
        {
            "id": key,
            "description": description,
            "transcription_status": "visually_seen_in_2003_retypesetting",
            "source_printed_pages": (
                [713] if key.startswith("degree") else [715] if key == "example_19_52" else [714]
            ),
            "authenticated_1647_original": "not_checked",
        }
    )
path = root / "LILLY_SOURCE_ANOMALIES.json"
path.write_text(json.dumps(issues, ensure_ascii=False, indent=2) + "\n")

worked = [literal_naibod_lookup(11, 55).to_dict(), literal_naibod_lookup(19, 52).to_dict()]
(root / "examples/lilly_printed_worked_examples.json").write_text(
    json.dumps(worked, ensure_ascii=False, indent=2) + "\n"
)
arc = 75.0
calcs = []
for key in TimeKey:
    rate = degrees_per_symbolic_year(key)
    calcs.append(
        {
            "arc_deg": arc,
            "diagnostic_key": key.value,
            "annual_rotation_deg": rate,
            "symbolic_years": arc / rate,
            "not_printed_table_replacement": True,
            "printed_book_original_not_independently_verified": True,
        }
    )
(root / "examples/75_degree_key_sensitivity.json").write_text(
    json.dumps(calcs, ensure_ascii=False, indent=2) + "\n"
)
assert len(issues) >= 7
print(
    json.dumps(
        {
            "source_witness": SOURCE_WITNESS,
            "literal_rows": len(rows),
            "minute27": "recorded missing",
            "warnings": len(issues),
            "example1": (
                worked[0]["resulting_years"],
                worked[0]["resulting_days"],
                worked[0]["resulting_hours"],
            ),
            "example2_arithmetic": (
                worked[1]["resulting_years"],
                worked[1]["resulting_days"],
                worked[1]["resulting_hours"],
            ),
            "keys": len(calcs),
            "outputs": [
                "LILLY_NAIBOD_2003_RETYPED_LITERAL_CELLS.csv",
                "LILLY_SOURCE_ANOMALIES.json",
                "examples/lilly_printed_worked_examples.json",
                "examples/75_degree_key_sensitivity.json",
            ],
        },
        indent=2,
    )
)
