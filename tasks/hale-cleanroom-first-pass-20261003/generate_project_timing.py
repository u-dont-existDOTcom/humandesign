from __future__ import annotations
import hashlib, importlib.util, json, os
from datetime import UTC, datetime
from pathlib import Path
import swisseph as swe

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/"scripts/partner_future_pilot.py"
OUT=Path(__file__).with_name("PROJECT_TIMING_2020_2041.json")
EPHE=Path(os.environ["EPHEMERIS_ROOT"])

spec=importlib.util.spec_from_file_location("partner_future_pilot_clean", SRC)
pilot=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(pilot)
pilot.EPHE=EPHE
pilot.START=datetime(2020,1,1,tzinfo=UTC)
pilot.END=datetime(2042,1,1,tzinfo=UTC)
swe.set_ephe_path(str(EPHE))

birth=datetime(1994,1,27,22,35,tzinfo=UTC)
record=pilot.subject_record(
    "hale-cleanroom",
    birth,
    41.0138429552247,
    28.9496612548828,
    True,
)
report={
    "schema":"hale-project-timing-v1",
    "source_script":"scripts/partner_future_pilot.py",
    "source_script_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),
    "ephemeris":{"sepl_18":pilot.sha256(EPHE/"sepl_18.se1"),"semo_18":pilot.sha256(EPHE/"semo_18.se1")},
    "horizon":[pilot.START.isoformat(),pilot.END.isoformat()],
    "record":record,
}
OUT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
print(OUT)
print("transits",len(record["transit_events"]),"progressions",len(record["progression_events"]))
print(hashlib.sha256(OUT.read_bytes()).hexdigest())
