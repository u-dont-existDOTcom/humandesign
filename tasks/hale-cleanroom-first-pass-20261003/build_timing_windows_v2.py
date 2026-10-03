from __future__ import annotations
import json
from pathlib import Path

BASE=Path(__file__).resolve().parent
T=json.loads((BASE/"PROJECT_TIMING_2020_2041.json").read_text())["record"]
C=json.loads((BASE/"CALCULATIONS.json").read_text())
N=C["numerology"]

WINDOWS=[
 ("W1","2020-01-01","2024-12-31","retrospective_blind"),
 ("W2R","2026-01-01","2026-10-02","retrospective_blind"),
 ("W2P","2026-10-03","2027-12-31","prospective_from_freeze"),
 ("W3","2028-01-01","2030-12-31","prospective_from_freeze"),
 ("W4","2031-01-01","2033-12-31","prospective_from_freeze"),
 ("W5","2035-01-01","2037-12-31","prospective_from_freeze"),
 ("W6","2040-01-01","2041-12-31","prospective_from_freeze"),
]

def date(e):
    return e["utc"][:10]

def condense(events,start,end):
    groups={}
    for e in events:
        if not (start <= date(e) <= end):
            continue
        key=(e.get("moving"),e["aspect"],e["target"])
        g=groups.setdefault(key,[])
        g.append(e)
    out=[]
    for (moving,aspect,target),rows in sorted(groups.items(), key=lambda kv: kv[1][0]["utc"]):
        out.append({
          "moving":moving,"aspect":aspect,"target":target,
          "first_exact_utc":rows[0]["utc"],"last_exact_utc":rows[-1]["utc"],
          "exact_hit_count":len(rows),
          "birth_time_sensitive":target in {"ASC","MC"},
        })
    return out

pys={x["year"]:x["number"] for x in N["personal_years"]}
ess={1994+x["age"]:x["essence"] for x in N["birth_name_transits_essences"]}

report={
 "schema":"hale-cleanroom-timing-windows-v2",
 "freeze_date":"2026-10-03",
 "astrology_source":"PROJECT_TIMING_2020_2041.json generated from current scripts/partner_future_pilot.py",
 "selection_rule":{
   "status":"outcome_blind",
   "rule":"Select multi-year clusters with slow-planet transit and/or secondary-progression density plus a numerology phase marker. Retrograde repeats of one moving/aspect/target family are collapsed. Jupiter alone cannot define a window. Angle-target events are flagged conditional on the supplied birth time.",
   "unselected_comparison_periods":["2025","2034","2038-2039"],
 },
 "windows":[]
}

for wid,start,end,status in WINDOWS:
    years=range(int(start[:4]),int(end[:4])+1)
    row={
      "id":wid,"start":start,"end":end,"evaluation_status":status,
      "transit_families":condense([e for e in T["transit_events"] if e["moving"]!="Jupiter"],start,end),
      "progression_families":condense(T["progression_events"],start,end),
      "personal_years":{str(y):pys.get(y) for y in years},
      "essences":{str(y):ess.get(y) for y in years if y in ess},
    }
    report["windows"].append(row)

(BASE/"TIMING_WINDOWS_V2.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
print(BASE/"TIMING_WINDOWS_V2.json")
for w in report["windows"]:
    print(w["id"],w["evaluation_status"],len(w["transit_families"]),len(w["progression_families"]))
