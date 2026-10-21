#!/usr/bin/env python3
"""Hash-pin original chart engine and run finite synthetic UTC-second intervals.

This does not modify the accepted original natal engine or authorize real
uncertain human birth-clock inputs. The interval is an explicit UTC-instant
set with exact integer-second resolution, NOT an interval of civil wall clocks.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from hashlib import sha256
from pathlib import Path

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]
PARENT = ROOT / "tasks/astro-ziwei-natal-policy-sensitivity-20261020"
PARENT_RUNNER = PARENT / "run_pinned_natal_policy_sensitivity.py"
PARENT_MANIFEST = PARENT / "PINNED_ENGINE_FILE_MANIFEST_V1.json"
PARENT_REPORT = PARENT / "PINNED_ENGINE_SYNTHETIC_NATAL_POLICY_SENSITIVITY_V1.json"
OUTPUT = TASK / "FINITE_UTC_SECOND_SYNTHETIC_ORIGINAL_SOURCE_CHART_SETS_V1.json"
WORKER = TASK / "worker_synthetic_utc_interval_states.py"

ENGINE_COMMIT = "fb6b30b1ca67ff62fecc0c4ea7f3e4d0553640d4"
PARENT_COMMIT = "abbae2c9661de0b06a23a891d971fc4fb61598fc"
PARENT_MANIFEST_SHA = "aac1e39c563829a1ea07c95875260ee278928bb5f2becdbca7c2375a986c8afd"
PARENT_ENGINE_RUNNER_SHA = "b7ccf7cef9f32364b15bbeac21103b99d40e8e74207cceb43e19385023198074"
PARENT_REPORT_SHA = "12b8ebc0a4a8a91c02f418ebf2e7787d382c750ef6bccc19afb8623d3fe731be"
CALENDAR_RUNTIME_DEFAULT = Path("/tmp/hd-calendar-parity-20261020")


def sha(b: bytes) -> str:
    return sha256(b).hexdigest()


def fail(reason: str):
    raise ValueError("Finite UTC second synthetic source oracle rejected: " + reason)


def read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def assert_pinned_original_parent():
    expected = [
        (PARENT_MANIFEST, PARENT_MANIFEST_SHA),
        (PARENT_REPORT, PARENT_REPORT_SHA),
        (PARENT_RUNNER, PARENT_ENGINE_RUNNER_SHA),
    ]
    for file, checksum in expected:
        if not file.is_file() or sha(file.read_bytes()) != checksum:
            fail(
                "accepted original parent source receipt/code/report "
                "SHA not found or drifted: " + str(file)
            )
    receipt = read(PARENT_REPORT)
    if (
        receipt["original_accepted_engine_git_commit"] != ENGINE_COMMIT
        or receipt["real_human_forward_reverse_predictive_validations"] != 0
    ):
        fail("parent source engine version or absence of human predictions changed")
    index = read(PARENT_MANIFEST)
    if len(index["source_engine_original_files_sha_and_bytes"]) != 22:
        fail("original 22 source engine modules/official HKO witnesses no longer present")
    return expected


def get_original_source(*, archive_only: bool = False):
    # Import the accepted parent runner as an unmodified versioned path,
    # only after verifying the original SHA/commit/manifest.
    assert_pinned_original_parent()
    sys.path.insert(0, str(PARENT))
    try:
        import run_pinned_natal_policy_sensitivity as original
    finally:
        sys.path.pop(0)
    if (
        original.ENGINE_COMMIT != ENGINE_COMMIT
        or original.digest(PARENT_MANIFEST.read_bytes()) != PARENT_MANIFEST_SHA
    ):
        fail("imported original source module is not declared accepted source")
    source = original.verified_sources(from_archive_only=archive_only)
    return original, source


def build(*, archive_only: bool = False, calendar_site: Path | None = None) -> dict:
    original, files = get_original_source(archive_only=archive_only)
    package_site = calendar_site or Path(
        os.environ.get("ZIWEI_PINNED_CALENDAR_SITE", str(CALENDAR_RUNTIME_DEFAULT))
    )
    package_versions = original.verify_calendar_packages(package_site)
    if package_versions != {"lunar_python": "1.4.8", "sxtwl": "2.0.7"}:
        fail("calendar library source binary versions differ from accepted")
    with tempfile.TemporaryDirectory(prefix="source_pinned_ziwei_UTC_uncertainty_") as d:
        root = Path(d)
        for filename, content in files.items():
            path = root / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        env = os.environ.copy()
        env["PYTHONPATH"] = (
            str(root / "tasks/astro-chinese-primary-sources-20261017/ziwei")
            + os.pathsep
            + str(package_site)
        )
        proc = subprocess.run(
            [sys.executable, str(WORKER)],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            timeout=100,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                "Original pinned engine source synthetic interval computation failed: "
                + proc.stderr[-2500:]
            )
        data = json.loads(proc.stdout)
    cases = data.get("case_results", [])
    if (
        data.get("schema")
        != ("HUMANDESIGN_ZIWEI_EXPLICIT_FINITE_UTC_SECOND_SYNTHETIC_INTERVAL_SOURCE_V1")
        or len(cases) != 6
        or data.get("fictional_UTC_intervals") != 6
        or len({x["case_id"] for x in cases}) != 6
        or data.get("real_human_predictive_validations") != 0
        or data.get("human_personal_birth_records_or_survey_responses") != 0
        or data.get("runtime_astrological_promotions") != 0
        or data["disputed_original_calendar_interval_rejection"][
            "entire_uncertain_interval_rejected"
        ]
        is not True
    ):
        fail(
            "uncertain interval source results incomplete or falsely presented as human validation"
        )
    if any(
        len(c["four_calendar_hour_policy_runs"]) != 4
        or not c["all_four_reference_day_hour_policies_enumerated"]
        for c in cases
    ):
        fail("not all four separately named day/hour policies covered")
    for case in cases:
        n = case["total_original_UTC_integer_second_inclusive_samples"]
        for policy in case["four_calendar_hour_policy_runs"]:
            if n != policy["interval_integer_second_samples"] or (
                n != sum(x["integer_second_samples"] for x in policy["source_chart_segment_states"])
            ):
                fail("incomplete UTC interval states or discarded instants")
        if case["robust_behavioral_prediction_from_source"] is not False:
            fail("original synthetic mechanical source claimed human prediction")
    out = {
        "schema": "HUMANDESIGN_ORIGINAL_ZIWEI_SOURCE_SHA_PINNED_SYNTHETIC_FINITE_UTC_INTERVAL_V1",
        "status": "SYNTHETIC_INSTANT_INTERVAL_SOURCE_CHART_SET_NOT_HUMAN_ASTROLOGY",
        "source_engine_git_commit": ENGINE_COMMIT,
        "source_22_original_engine_files_sha256": {k: sha(b) for k, b in files.items()},
        "source_original_manifest_SHA256": PARENT_MANIFEST_SHA,
        "source_previous_policy_oracle_report_SHA256": PARENT_REPORT_SHA,
        "source_original_calculation_runner_SHA256": PARENT_ENGINE_RUNNER_SHA,
        "pinned_external_calendar_binary_source_tree_sha256": (
            original.EXPECTED_LIBRARY_TREE_SHA.copy()
        ),
        "pinned_external_calendar_package_versions": package_versions,
        "external_calendar_package_binaries_included_in_repository": False,
        "original_Ming_printed_source_verified": False,
        "validated_full_ZiWei_natal_chart": False,
        "real_birth_clock_uncertainty_to_possible_UTC_instants_implemented": False,
        "real_birthplace_and_astronomical_apparent_solar_calibration_implemented": False,
        "finite_declared_integer_second_UTC_interval_enumeration_complete": True,
        "synthetic_UTC_integer_second_interval_output": data,
        "actual_human_chart_subjects": 0,
        "real_blind_predictive_outcomes": 0,
        "astrological_runtime_rule_promotions": 0,
    }
    OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    result = build()
    core = result["synthetic_UTC_integer_second_interval_output"]
    print(
        json.dumps(
            {
                "invented_UTC_intervals": core["fictional_UTC_intervals"],
                "unique_integer_second_UTC_samples": core[
                    "total_fake_integer_second_instants_unique_by_case"
                ],
                "four_policy_runs_per_case": core[
                    "number_of_declared_calendar_hour_policies_per_case"
                ],
                "source_chart_states_per_interval": {
                    c["case_id"]: c[
                        "distinct_source_calendar_hour_life_full14_states_across_all_seconds_policies"
                    ]
                    for c in core["case_results"]
                },
                "intervals_with_all_policy_invariant_14_stars": sum(
                    c["source_all_policy_invariant_14star_state"] for c in core["case_results"]
                ),
                "independent_human_predictions": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
