"""Bounded post-freeze probes for source-A's helper review; no table/suite run."""
from fractions import Fraction
from pathlib import Path
import hashlib
import inspect
import json
import sys
import types

sys.dont_write_bytecode = True
helper = Path("/workspace/scratch/43f75264c32e/humandesign-b02k/tasks/astro-source-audit-multipass-20261005/batches/B02k/lilly_sixth_opening_reference.py")
expected_hash = "972076c053dc8ad340d6369ecdbf3893f3b1d1354231a087d0ade88b2a1f180f"
raw = helper.read_bytes()
actual_hash = hashlib.sha256(raw).hexdigest()
if actual_hash != expected_hash:
    raise SystemExit("Reviewed helper changed before probes: " + actual_hash)
ref = types.ModuleType("source_a_reviewed_helper")
ref.__file__ = str(helper)
sys.modules[ref.__name__] = ref
exec(compile(raw, str(helper), "exec"), ref.__dict__)

records = []
def retain(name, result, expected, meaning):
    assert result == expected, (name, result, expected)
    records.append({"probe": name, "observed": result, "expected": expected, "passed": True, "meaning": meaning})

def unavailable():
    return {key: ref.TimeEvidence(False) for key in ref.TIME_KEYS}

data = unavailable()
data["enforced_bed_or_rest"] = ref.TimeEvidence(None)
data["first_urine_inquiry"] = ref.TimeEvidence(True, "later")
result = ref.select_source_time(data)
retain("earlier_unknown_blocks_fallback", (result["status"], result["stage"], result["candidates"]),
       ("UNKNOWN", 1, []), "Availability unknown does not authorize fallback.")

data = unavailable()
data["first_urine_inquiry"] = ref.TimeEvidence(None)
data["physician_first_access"] = ref.TimeEvidence(True, "access")
result = ref.select_source_time(data)
retain("second_stage_unknown_blocks_third", (result["status"], result["stage"]),
       ("UNKNOWN", 2), "Ordered fallback also preserves unknown at stage 2.")

data = unavailable()
data["physician_first_speaking"] = ref.TimeEvidence(True, "a")
data["physician_first_access"] = ref.TimeEvidence(True, "b")
data["physician_first_urine_receipt"] = ref.TimeEvidence(None)
result = ref.select_source_time(data)
retain("third_stage_retains_candidates_and_unknown",
       (result["status"], [x["token"] for x in result["candidates"]], result["unresolved_alternatives"]),
       ("UNKNOWN", ["a", "b"], ["physician_first_urine_receipt"]),
       "The conservative UNKNOWN status retains both known, unranked candidates.")

data["physician_first_urine_receipt"] = ref.TimeEvidence(False)
retain("third_stage_distinct_known_times",
       ref.select_source_time(data)["status"], "CHOICE_UNRESOLVED",
       "No preferred physician alternative is invented.")

for speed, expected in [
    (Fraction(94799, 2), (True, True)),
    (47400, (True, False)),
    (47418, (True, False)),
    (47436, (False, False)),
    (None, (None, None)),
]:
    result = ref.moon_speed_comparisons(speed)
    retain("lunar_motion_" + str(speed),
           (result["below_stated_mean"], result["under_retrograde_analogy_threshold"]),
           expected, "Distinct strict thresholds and missing speed.")

retain("coordinate_missing_seconds", ref.remaining_degrees_in_sign(29, 0),
       {"remaining_degrees": None, "time_unit": None},
       "Missing seconds are not replaced with zero.")
retain("exact_arc_unknown_time_unit", ref.remaining_degrees_in_sign(29, 30, 0),
       {"remaining_degrees": Fraction(1, 2), "time_unit": None},
       "Arc arithmetic does not select months, weeks or days.")
retain("H-A01_negative_remainder_reproduced",
       ref.remaining_degrees_in_sign(Fraction(59, 2), 59, 0),
       {"remaining_degrees": Fraction(-29, 60), "time_unit": None},
       "Confirmed defect: admitted components sum beyond the within-sign domain. This probe passes by reproducing the defect, not by approving it.")

for author, expected in [(False, "SATISFIED"), (True, "CONTRADICTED"), (None, "UNKNOWN")]:
    retain("benevolent_author_" + str(author),
           ref.benevolent_sixth_predicate(benevolent=True, well_fortified=True, in_sixth=True, author_of_disease=author),
           expected, "Explicit non-author exclusion preserves all three states.")

for decreasing, expected in [(True, "CONTRADICTED"), (None, "UNKNOWN")]:
    retain("H-A02_current_exception_" + str(decreasing),
           ref.declining_moon_saturn_predicate(light_decreasing=True, motion_decreasing=True,
               applying_conjunction_square_or_opposition=True, disease_already_decreasing=decreasing),
           expected, "Current API can establish the exception from decreasing alone; leaving has no separately named or composite-defined input.")

output = {
    "record_type": "bounded_post_freeze_probe_results",
    "review_id": "B02k-source-a-helper-review-01",
    "diagnosis_frozen_before_test_inspection": True,
    "diagnosis_hashes": {
        "HELPER_DIAGNOSIS.md": "5f51b532971dd3221777c1ff774dcb0b7352785e77773c56e257eed5fb851a89",
        "HELPER_DIAGNOSIS.json": "574fcfc8d6e602ff81b06706177af0136727604854483250341b7f15ede5f14d"
    },
    "helper_sha256": actual_hash,
    "producer_tests_inspected_after_freeze": True,
    "producer_tests_executed": False,
    "whole_suite_executed": False,
    "reference_tables_or_rules_loaded": False,
    "repository_writes": False,
    "bytecode_writes_disabled": True,
    "telemetry": "Not applicable: one tiny pure-function process, no concurrency or broad suite.",
    "probe_count": len(records),
    "probes": records,
    "current_saturn_predicate_signature": str(inspect.signature(ref.declining_moon_saturn_predicate)),
    "producer_test_findings": [
        "Existing RemainingArc invalid-coordinate test checks individually invalid components, but no aggregate Fraction overflow case.",
        "Existing declining-exception test uses disease_already_decreasing alone and therefore repeats the same incomplete source phrase.",
        "SourceLookups and SourceRecordIntegrity were read but not run; their data dependencies are outside this pure-function probe."
    ],
    "diagnosis_reconciliation": "No initial finding was withdrawn or materially changed. H-A01 is dynamically reproduced; H-A02 remains a source/input-contract finding."
}
def encode(value):
    if isinstance(value, Fraction):
        return {"fraction": str(value), "numerator": value.numerator, "denominator": value.denominator}
    raise TypeError(type(value).__name__)
destination = Path("/workspace/scratch/43f75264c32e/b02k-workers/source-a/HELPER_PROBES.json")
destination.write_text(json.dumps(output, indent=2, ensure_ascii=False, default=encode) + "\n", encoding="utf-8")
print(json.dumps({"probe_count": len(records), "status": "completed", "H-A01": "negative remainder reproduced", "H-A02": "incomplete exception contract confirmed", "output": str(destination)}))

