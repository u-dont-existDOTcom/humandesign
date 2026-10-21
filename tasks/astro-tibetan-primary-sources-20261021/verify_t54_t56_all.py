#!/usr/bin/env python3
"""Incremental Tibetan source/calculation acceptance receipt T54–T56.
All outcomes below are engineering/source parity, not validated astrology.
"""
from pathlib import Path
import json, subprocess

R=Path(__file__).resolve().parent
def read(path):
    return json.loads((R/path).read_text(encoding="utf-8"))
notes1=read("batches/T51/CORNU_JUNGTSI_KARTSI_WORKED_24_NOTES_V1.json")
notes2=read("batches/T52/JANSON_CALENDAR_17_SOURCE_NOTES_V1.json")
notes3=read("batches/T54/JANSON_TRUE_DATE_12_SOURCE_NOTES_V1.json")
historical=notes1["notes"]+notes2["source_notes"]+notes3["source_notes"]
assert [n["id"] for n in historical]==[f"TIB-R{n:04d}" for n in range(448,501)]
assert (notes1["source_note_count"],notes2["note_count"],notes3["new_historical_note_count"]) == (24,17,12)
assert notes3["new_historical_note_count"]==12 and notes3["last_id"]=="TIB-R0500"
assert len(notes3["source_notes"])==12
assert all(x["source_id"]=="TIB-JANSON-2014" and x["required_inputs"] for x in notes3["source_notes"])
assert all(x["validated_on_real_humans"] is False and x["model_promoted"] is False for x in notes3["source_notes"])
PY=read("batches/T54/DIFFERENTIAL_PYTHON_RECEIPT_V1.json")
JS=read("batches/T54/DIFFERENTIAL_JAVASCRIPT_RECEIPT_V1.json")
assert PY["mismatch_count"]==0 and PY["day_comparisons"]==4386
assert PY["reference_commit_sha"]=="01591b5bf03d038b864c4138fde3cc4285ca8001"
assert PY["human_predictive_claims"]==0 and PY["source_code_vendored"] is False
assert JS["disagreements"]==0 and JS["compared_day_count"]==2193
assert JS["git_commit"]=="7651b8b579c8332442198cc0d9ca14d0b0e8b3a8"
assert JS["human_predictive_tests"]==0 and JS["original_upstream_code_in_our_repository"] is False
BIRTH=read("batches/T55/EXPLICIT_BIRTH_MEAN_DAWN_POLICY_V1.json")
assert BIRTH["new_historical_annotation_count"]==0
assert BIRTH["input_contract"]["day_boundary_policy"]=="project_extension_05_LMT_dawn (explicit; never default)"
assert "not UTC or GMT" in BIRTH["Cornu_1950_source_based_example"]["local_mean_solar"]
assert BIRTH["empirical_tests"]["real_people_blind_predictions"]==0
S=read("batches/T56/ANOMALY_POLICY_SENSITIVITY_1987_2051.json")
assert S["source_note_increment"]==S["human_prediction_successes"]==0
assert S["systems"]["phugpa"]["tithi_ends_compared"]==24120
assert S["systems"]["tsurphu"]["tithi_ends_compared"]==24120
assert S["systems"]["phugpa"]["tithi_end_JDN_disagreements"]==6
assert S["systems"]["tsurphu"]["tithi_end_JDN_disagreements"]==5
assert S["systems"]["phugpa"]["Losar_disagreements"]==S["systems"]["tsurphu"]["Losar_disagreements"]==0
result=subprocess.run(["python3",str(R/"verify_t55_birth_policy.py")],
                      check=True,capture_output=True,text=True)
assert "T55 BIRTH-POLICY" in result.stdout
print("T54–T56 PASS: 500 contiguous Tibetan source annotations (prior447 + T51/52 41 + T54 12),")
print("  Janson Gregorian/Tibetan exact-rational engine, Cornu-1950 UTC pilot,")
print("  4386 pinned Python +2193 pinned JS zero-disagreement date checks,")
print("  two explicit rounded-vs-Dharmashri anomaly policy sensitivity tallies,")
print("  all previous accepted Tibetan suites green; real human predictive validations ZERO.")
