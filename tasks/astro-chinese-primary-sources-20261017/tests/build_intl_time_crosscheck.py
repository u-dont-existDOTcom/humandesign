#!/usr/bin/env python3
"""Freeze separate ECMAScript Intl and Python zoneinfo date/hour comparisons.

No real people and no live API. These two implementations may use related IANA
time zone records; cross-implementation agreement is engineering evidence,
not independent adjudication of historical true local time.
"""
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path(__file__).resolve()
TEST_CASES = [
    ("hko-1965-summer-early","1965-06-30T15:30:00Z","Asia/Hong_Kong"),
    ("hko-1965-summer-late","1965-07-01T15:30:00Z","Asia/Hong_Kong"),
    ("hko-2026-cny","2026-02-16T23:30:00Z","Asia/Hong_Kong"),
    ("hko-1979-autumn-dst","1979-10-21T00:00:00Z","Asia/Hong_Kong"),
    ("ny-2026-spring-before","2026-03-08T06:30:00Z","America/New_York"),
    ("ny-2026-spring-after","2026-03-08T07:30:00Z","America/New_York"),
    ("ny-2026-autumn-fold0","2026-11-01T05:30:00Z","America/New_York"),
    ("ny-2026-autumn-fold1","2026-11-01T06:30:00Z","America/New_York"),
    ("apia-2011-skipped-prev","2011-12-30T09:30:00Z","Pacific/Apia"),
    ("apia-2011-skipped-next","2011-12-30T10:30:00Z","Pacific/Apia"),
    ("dakar-2026","2026-02-16T21:30:00Z","Africa/Dakar"),
    ("ny-2026-summer","2026-07-01T17:30:00Z","America/New_York"),
]
cases=[dict(id=i,utc=u,zone=z) for i,u,z in TEST_CASES]
result=subprocess.run(
    ["node",str(P.with_name("node_intl_zone_oracle.cjs"))],
    input=json.dumps({"cases":cases}),capture_output=True,text=True,check=True,timeout=20
)
js=json.loads(result.stdout)
lookup={r["id"]:r for r in js["cases"]}
if len(lookup)!=len(TEST_CASES):
    raise ValueError("Missing external timezone projection results")
rows=[]
for id_, iso, zone in TEST_CASES:
    py=datetime.fromisoformat(iso.replace("Z","+00:00")).astimezone(ZoneInfo(zone))
    expected=py.strftime("%Y-%m-%dT%H:%M:%S")
    observed=lookup[id_]["local_clock"]
    row={
        "id":id_, "utc_instant":iso, "iana_zone":zone,
        "python_zoneinfo_local_clock":expected,
        "node_intl_local_clock":observed,
        "agree":expected==observed,
        "python_zoneinfo_offset_seconds":int(py.utcoffset().total_seconds()),
        "python_zoneinfo_fold":py.fold,
    }
    rows.append(row)
assert all(r["agree"] for r in rows)
full=json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode("utf-8")
report={
    "status":"synthetic timezone edge-case engineering cross-check only",
    "source_reference":"https://peps.python.org/pep-0495/",
    "HKO_summer_time_reference":"https://www.hko.gov.hk/en/gts/time/Summertime.htm",
    "python_timezone_implementation":"Python standard zoneinfo system tzdb",
    "second_implementation":js["javascript_engine"],
    "node_runtime_version":js["node_version"],
    "node_ICU_version":js["icu_version"],
    "node_tzdb_version":js["node_tzdb_version"],
    "sample_count":len(rows),
    "identical_civil_dates_and_hours":sum(r["agree"] for r in rows),
    "disagreement_count":sum(not r["agree"] for r in rows),
    "sample_rows_sha256_canonical":hashlib.sha256(full).hexdigest(),
    "cases":rows,
    "limitations":[
        "IANA/ICU may share historical timezone source input",
        "Pre-1970 records may change between tzdb releases",
        "HK DST clock is not synonymous with UTC+8 standard lunar reference",
        "No independent true solar time or human predictive outcome tested"
    ]
}
dest=P.parent.parent/"batches/ChineseAstro-13/NODE_INTL_PYTHON_ZONEINFO_12_SYNTHETIC_PARITY_V1.json"
dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
print("WROTE",dest,"CASES",len(rows),"AGREE",report["identical_civil_dates_and_hours"],"SHA",report["sample_rows_sha256_canonical"])
