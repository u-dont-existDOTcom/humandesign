"""One-shot independent probes; these are not candidate unittest identities."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import hashlib
import importlib.util
import json
import sys

ROOT = Path(__file__).parent
PRIVATE = ROOT / "private_run"
SPEC = importlib.util.spec_from_file_location("private_reference", PRIVATE / "lilly_sixth_opening_reference.py")
ref = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ref
SPEC.loader.exec_module(ref)

groups = {}
failures = []


def check(group, label, observed, expected):
    groups[group] = groups.get(group, 0) + 1
    if observed != expected:
        failures.append({"group": group, "label": label, "observed": repr(observed), "expected": repr(expected)})


def error_kind(fn):
    try:
        fn()
    except Exception as exc:
        return type(exc).__name__
    return "NO_EXCEPTION"


for flags in product((True, False, None), repeat=5):
    evidence = {key: ref.TimeEvidence(flag, "same-token" if flag else None)
                for key, flag in zip(ref.TIME_KEYS, flags)}
    observed = ref.select_source_time(evidence)
    if flags[0] is not False:
        expected = ("UNKNOWN" if flags[0] is None else "SELECTED", 1)
    elif flags[1] is not False:
        expected = ("UNKNOWN" if flags[1] is None else "SELECTED", 2)
    else:
        final = flags[2:]
        expected = ("UNKNOWN" if None in final else "SELECTED" if True in final else "UNAVAILABLE", 3)
        expected_candidates = [{"event": key, "token": "same-token"}
                               for key, flag in zip(ref.TIME_KEYS[2:], final) if flag is True]
        check("time_candidates", repr(flags), observed["candidates"], expected_candidates)
    check("time_state_matrix", repr(flags), (observed["status"], observed["stage"]), expected)

for flags in product((True, False, None), repeat=4):
    expected = "CONTRADICTED" if False in flags else "UNKNOWN" if None in flags else "SATISFIED"
    check("conjunction_matrix", repr(flags), ref.all_facts(*flags), expected)
    transformed = flags[:3] + ((None if flags[3] is None else not flags[3]),)
    guarded = "CONTRADICTED" if False in transformed else "UNKNOWN" if None in transformed else "SATISFIED"
    check("benevolent_matrix", repr(flags), ref.benevolent_sixth_predicate(
        benevolent=flags[0], well_fortified=flags[1], in_sixth=flags[2], author_of_disease=flags[3]), guarded)
    check("saturn_matrix", repr(flags), ref.declining_moon_saturn_predicate(
        light_decreasing=flags[0], motion_decreasing=flags[1],
        moon_applying_conjunction_square_or_opposition_to_saturn=flags[2],
        disease_decreasing_and_leaving=flags[3]), guarded)

for value in (0, 1, "unknown", "false", [], {}):
    check("boolean_validation", repr(value), error_kind(lambda: ref.all_facts(value)), "TypeError")
    check("time_validation", repr(value), error_kind(lambda: ref.TimeEvidence(value)), "TypeError")
for available, token in [(True, None), (True, ""), (True, " "), (True, 1), (False, "x"), (None, "x")]:
    check("time_validation", repr((available, token)), error_kind(lambda: ref.TimeEvidence(available, token)), "ValueError")
check("time_validation", "wrong evidence value", error_kind(lambda: ref.select_source_time({ref.TIME_KEYS[0]: True})), "TypeError")
check("time_validation", "unknown event", error_kind(lambda: ref.select_source_time({"other": ref.TimeEvidence(False)})), "ValueError")

for speed in (0, Fraction(1, 2), Fraction(94799, 2), 47400, Fraction(94801, 2), 47418, Fraction(94871, 2), 47436, Fraction(94873, 2), 1296000):
    check("lunar_exact_arithmetic", str(speed), ref.moon_speed_comparisons(speed),
          {"below_stated_mean": speed < 13 * 3600 + 10 * 60 + 36,
           "under_retrograde_analogy_threshold": speed < 13 * 3600 + 10 * 60})
check("lunar_exact_arithmetic", "unknown", ref.moon_speed_comparisons(None),
      {"below_stated_mean": None, "under_retrograde_analogy_threshold": None})
for value in (True, False, 13.17, "47400"):
    check("lunar_validation", repr(value), error_kind(lambda: ref.moon_speed_comparisons(value)), "TypeError")
for value in (-1, Fraction(-1, 2)):
    check("lunar_validation", str(value), error_kind(lambda: ref.moon_speed_comparisons(value)), "ValueError")

for position in [(0, 0, 0), (29, 30, 0), (29, 59, 59), (Fraction(59, 2), 0, 0), (29, Fraction(1, 2), Fraction(1, 2)), (0, 0, Fraction(1, 2))]:
    expected = Fraction(30) - Fraction(position[0]) - Fraction(position[1], 60) - Fraction(position[2], 3600)
    check("remaining_exact_arithmetic", repr(position), ref.remaining_degrees_in_sign(*position), {"remaining_degrees": expected, "time_unit": None})
for position in [(None, 0, 0), (29, None, 0), (29, 0, None), (None, None, None)]:
    check("remaining_missing", repr(position), ref.remaining_degrees_in_sign(*position), {"remaining_degrees": None, "time_unit": None})
for position in [(30, 0, 0), (-1, 0, 0), (29, -1, 0), (29, 0, -1), (29, 60, 0), (29, 0, 60), (Fraction(59, 2), 30, 0), (Fraction(59, 2), 59, 0)]:
    check("remaining_validation", repr(position), error_kind(lambda: ref.remaining_degrees_in_sign(*position)), "ValueError")
for position in [(True, 0, 0), (29, False, 0), (29, 0, True), (29.0, 0, 0), (29, "0", 0)]:
    check("remaining_validation", repr(position), error_kind(lambda: ref.remaining_degrees_in_sign(*position)), "TypeError")

tables = json.loads((PRIVATE / "REFERENCE_TABLES.json").read_text())
signs = {"Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"}
check("lookup_catalogues", "sign identities", set(tables["namespaces"]["sign"]), signs)
check("lookup_catalogues", "house identities", set(tables["namespaces"]["house"]), {str(i) for i in range(1, 13)})
check("lookup_catalogues", "planet identities", set(tables["namespaces"]["planet"]), {"Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"})
for namespace, rows in tables["namespaces"].items():
    for key, row in rows.items():
        check("all_lookup_routing", namespace + "/" + key, ref.source_lookup(namespace, key), row)
for key, row in tables["namespaces"]["historical_fixed_star"].items():
    check("star_precision", key, [row[k] for k in ["minutes", "seconds", "modern_epoch_longitude", "ordinal_to_continuous_degree_convention", "nearness_threshold"]], [None] * 5)
for namespace, key in [("missing", "1"), ("house", "Cancer"), ("sign", "cancer"), ("sign", "Cancer "), ("sign", "1"), ("retained_planet_sign", "Mars|Cancer")]:
    check("lookup_rejection", namespace + "/" + key, error_kind(lambda: ref.source_lookup(namespace, key)), "KeyError")
check("lookup_catalogues", "integer house key", ref.source_lookup("house", 1), tables["namespaces"]["house"]["1"])
check("lookup_catalogues", "explicit path", ref.source_lookup("sign", "Cancer", path=PRIVATE / "REFERENCE_TABLES.json"), tables["namespaces"]["sign"]["Cancer"])
original = (PRIVATE / "REFERENCE_TABLES.json").read_bytes()
changed = ref.source_lookup("sign", "Cancer")
changed["source_items"].clear()
changed["source_locator"]["pdf_pages"].clear()
check("lookup_detachment", "nested returned mutation", ref.source_lookup("sign", "Cancer"), tables["namespaces"]["sign"]["Cancer"])
check("lookup_detachment", "file not changed", (PRIVATE / "REFERENCE_TABLES.json").read_bytes(), original)

rules_document = json.loads((PRIVATE / "RULES.json").read_text())
rules = rules_document["rules"]
coverage = json.loads((PRIVATE / "SECTION_COVERAGE.json").read_text())
check("mechanical_record_structure", "192 records", len(rules), 192)
check("mechanical_record_structure", "192 unique full IDs", len({r["id"] for r in rules}), 192)
check("mechanical_record_structure", "nonempty page arrays", all(r["source_locator"]["pdf_pages"] for r in rules), True)
check("mechanical_record_structure", "parallel locator arrays", all(len(r["source_locator"]["pdf_pages"]) == len(r["source_locator"]["visible_printed_labels"]) == len(r["source_locator"]["printed_sequence_expected"]) for r in rules), True)

result = {"probe_groups": groups, "check_count": sum(groups.values()), "failures": failures,
          "all_observed_checks_passed": not failures,
          "candidate_unittest_identities_added": 0,
          "historical_source_fidelity_assessed": False,
          "clinical_or_predictive_validation": False,
          "scope": "One finite descriptive API, exact arithmetic, routing and structural boundary pass on private copies; no repair loop."}
(ROOT / "BOUNDED_PROBES.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
raise SystemExit(1 if failures else 0)
