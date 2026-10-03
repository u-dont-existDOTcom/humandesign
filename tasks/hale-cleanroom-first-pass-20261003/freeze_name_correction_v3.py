import hashlib, json
from pathlib import Path
BASE=Path(__file__).resolve().parent
def sha(name): return hashlib.sha256((BASE/name).read_bytes()).hexdigest()
record={
 "schema":"hale-first-pass-authority-v3",
 "status":"CURRENT_INPUT_CORRECTED_PRE_PERSONALITY_OUTCOME",
 "date_utc":"2026-10-03",
 "base_v2":{"branch":"research/hale-cleanroom-20261003","commit":"e653ca002ef9b49a9ff681e09a1809aa4c8da609"},
 "new_input":{
   "type":"name-history correction",
   "supplied_sequence":[
     "Hatice Hale Baysan until 2016",
     "Hatice Hale Aru from marriage in 2016",
     "Hatice Hale Baysan Aru in 2019",
     "Hatice Hale Baysan after divorce in 2021",
     "Hale Denizden later in 2021"
   ],
   "other_personality_survey_history_inspected":False,
   "revealed_event_warning":"Marriage/divorce/name-change chronology is now known and cannot be used as independent event-timing validation."
 },
 "current_authority":{
   "astrology":"V2 remains current and unchanged",
   "birth_date_numerology":"V2 remains current and unchanged",
   "birth_name_core":"NAME_INPUT_CORRECTION_V3",
   "birth_name_transits_essences":"NAME_INPUT_CORRECTION_V3",
   "changed_name_overlays":"NAME_INPUT_CORRECTION_V3",
   "fusion_name_dependent_claims":"NAME_INPUT_CORRECTION_V3",
   "astrology_timing":"V2 remains current",
   "personal_year_pinnacle_period_challenge_timing":"V2 remains current",
   "fused_timing_where_essence_matters":"NAME_INPUT_CORRECTION_V3"
 },
 "superseded_scope":{
   "v2_birth_name":"Hatice Baysan",
   "v2_name_numbers":["Expression 9","Soul Urge 8","Personality 10/1","Maturity 16/7"],
   "v2_birth_name_transit_rule":"no-middle-name fallback duplicating Baysan",
   "v2_name_dependent_fusion":"superseded wherever it depends on the above",
   "not_superseded":["astrology","Life Path 7","Birthday 28/1","Attitude 29/11/2->2","Pinnacles 2/6/8/6","Challenges 0/4/4/4","Periods 1/1/5","Personal Years"]
 },
 "corrected_core":{"birth_name":"Hatice Hale Baysan","expression":"17/8","soul_urge":"14/5","personality":"21/3","maturity":"15/6"},
 "artifacts":{
   "calculate_corrected_name_numerology.py":sha("calculate_corrected_name_numerology.py"),
   "NAME_INPUT_CORRECTION_V3.json":sha("NAME_INPUT_CORRECTION_V3.json"),
   "NAME_INPUT_CORRECTION_V3.md":sha("NAME_INPUT_CORRECTION_V3.md")
 }
}
(BASE/"CURRENT_HALE_FIRST_PASS_AUTHORITY_V3.json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
print(sha("CURRENT_HALE_FIRST_PASS_AUTHORITY_V3.json"))
