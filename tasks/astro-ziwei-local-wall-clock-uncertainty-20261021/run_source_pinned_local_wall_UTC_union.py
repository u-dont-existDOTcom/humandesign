#!/usr/bin/env python3
"""Pinned original Zi Wei source local wall-clock uncertainty synthetic harness.

The parent UTC interval evaluator and Chinese original source are exact Git
provenance and SHA verified. Input is hardcoded imaginary civil-clock cases,
not a person's birth record, and does not permit historical source prediction.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from hashlib import sha256
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
PARENT = ROOT / "tasks/astro-ziwei-finite-utc-uncertainty-20261020"
PARENT_RUNNER = PARENT / "run_source_pinned_utc_intervals.py"
PARENT_WORKER = PARENT / "worker_synthetic_utc_interval_states.py"
PARENT_REPORT = PARENT / "FINITE_UTC_SECOND_SYNTHETIC_ORIGINAL_SOURCE_CHART_SETS_V1.json"
OUT = B / "PINNED_SOURCE_SYNTHETIC_WALL_CLOCK_UTC_FOLD_UNION_V1.json"
WORKER = B / "worker_synthetic_local_wall_clock_to_UTC_set.py"
PARENT_COMMIT = "dae5ebe7a519405b0f0572d6cc79db4d41d17f5d"
PARENT_RUNNER_SHA = "75f33c16e98f9fc09e6d00318465a9741a32f09c9b0155f43add99d77166f92d"
PARENT_WORKER_SHA = "8fdcea04b516770df41ce2bff48ccbcb9ef5c8491dcbc09f67abf737caba84d4"
PARENT_REPORT_SHA = "717ebb5a1020aa275e495b6f42ac534229346b52607eb142d293556aec1b118f"
ORIGINAL_COMMIT = "fb6b30b1ca67ff62fecc0c4ea7f3e4d0553640d4"
LIBRARY_SITE = Path("/tmp/hd-calendar-parity-20261020")


def hash_file(p: Path) -> str:
    return sha256(p.read_bytes()).hexdigest()


def fail(msg):
    raise ValueError("Original source synthetic local wall-clock fold union rejected: " + msg)


def read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def verify_parent():
    for path, sha in (
        (PARENT_RUNNER, PARENT_RUNNER_SHA),
        (PARENT_WORKER, PARENT_WORKER_SHA),
        (PARENT_REPORT, PARENT_REPORT_SHA),
    ):
        if not path.is_file() or hash_file(path) != sha:
            fail(
                "original independently accepted UTC interval checker/receipt changed " + str(path)
            )
    old = read(PARENT_REPORT)
    if (
        old.get("source_engine_git_commit") != ORIGINAL_COMMIT
        or old.get("real_blind_predictive_outcomes") != 0
        or old.get("actual_human_chart_subjects") != 0
    ):
        fail("original source parent not mechanically validated or contains humans")
    return old


def build(*, archive_only: bool = False, calendar_site: Path | None = None) -> dict:
    verify_parent()
    sys.path.insert(0, str(PARENT))
    try:
        import run_source_pinned_utc_intervals as old
    finally:
        sys.path.pop(0)
    if old.ENGINE_COMMIT != ORIGINAL_COMMIT:
        fail("original pinned source engine commit drift")
    orig, source = old.get_original_source(archive_only=archive_only)
    site = calendar_site or Path(os.environ.get("ZIWEI_PINNED_CALENDAR_SITE", str(LIBRARY_SITE)))
    pinned_versions = orig.verify_calendar_packages(site)
    if pinned_versions != {"lunar_python": "1.4.8", "sxtwl": "2.0.7"}:
        fail("accepted original independent Chinese calendar library versions differ")
    with tempfile.TemporaryDirectory(prefix="ZiWei_PINNED_wall_clock_folds_") as d:
        root = Path(d)
        for name, blob in source.items():
            p = root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(blob)
        parent_worker = (
            root
            / "tasks"
            / "astro-ziwei-finite-utc-uncertainty-20261020"
            / "worker_synthetic_utc_interval_states.py"
        )
        parent_worker.parent.mkdir(parents=True, exist_ok=True)
        parent_worker.write_bytes(PARENT_WORKER.read_bytes())
        env = os.environ.copy()
        env["PYTHONPATH"] = os.pathsep.join(
            (
                str(parent_worker.parent),
                str(root / "tasks/astro-chinese-primary-sources-20261017/ziwei"),
                str(site),
            )
        )
        proc = subprocess.run(
            [sys.executable, str(WORKER)],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            timeout=100,
        )
        if proc.returncode:
            print(proc.stderr[-2500:])
            raise RuntimeError(
                "Pinned original finite synthetic wall-clock UTC candidate scan failed"
            )
        data = json.loads(proc.stdout)
    if (
        data.get("schema")
        != "HUMANDESIGN_ORIGINAL_ZIWEI_SYNTHETIC_LOCAL_WALL_CLOCK_TO_UTC_UNION_V1"
        or len(data.get("cases", [])) != 6
        or data.get("real_human_chart_outcomes_or_predictions_validated") != 0
        or data.get("real_person_birth_records") != 0
        or data.get("production_astro_human_traits_promoted") != 0
        or not data.get("entirely_rejected_2057_source_date", {}).get("refused")
    ):
        fail("six synthetic clocks or refused 2057 source date absent, or real-person claim")
    if any(
        r["source_summary_is_a_real_behavioral_prediction"] is not False
        or r["actual_personal_birth_instant_recovered"] is not False
        for r in data["cases"]
    ):
        fail("a fictional wall clock was claimed to validate human astrology")
    receipt = {
        "schema": "HUMANDESIGN_ORIGINAL_ZIWEI_SHA_PINNED_SYNTHETIC_WALL_CLOCK_UNCERTAINTY_V1",
        "status": "LOCAL_WALL_CLOCK_FOLD_AND_GAP_EXPLICIT_SOURCE_CHART_UNION_ONLY_NOT_HUMAN",
        "original_accepted_UTC_interval_parent_commit": PARENT_COMMIT,
        "original_parent_runner_sha256": PARENT_RUNNER_SHA,
        "original_parent_worker_sha256": PARENT_WORKER_SHA,
        "original_parent_result_sha256": PARENT_REPORT_SHA,
        "original_Chinese_natal_source_engine_git_commit": ORIGINAL_COMMIT,
        "pinned_chinese_engine_original_module_sha256": {
            name: sha256(blob).hexdigest() for name, blob in source.items()
        },
        "external_lunar_package_source_and_binary_tree_pinned_unbundled": (
            orig.EXPECTED_LIBRARY_TREE_SHA.copy()
        ),
        "pinned_external_package_versions": pinned_versions,
        "source_input_cases_explicitly_fictional": True,
        "source_ASTRO_complete_real_birthplace_hour_uncertainty_covered": False,
        "local_fold_branches_cannot_be_chosen_after_person_survey": True,
        "nonexistent_local_clocks_never_silently_shifted": True,
        "source_traditional_23h_Zi_day_apparent_solar_unimplemented": True,
        "astrological_source_a_real_person_trait_predictor": False,
        "mock_local_wall_clock_set_results": data,
        "actual_human_birth_records": 0,
        "real_human_blind_chart_outcome_validations": 0,
        "astrological_runtime_rule_promotions": 0,
    }
    OUT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    obj = build()
    d = obj["mock_local_wall_clock_set_results"]
    print(
        json.dumps(
            {
                "fictional_local_wall_cases": d["number_of_entirely_fictional_wall_clock_cases"],
                "wall_clock_second_total": d[
                    "sum_of_independent_artificial_local_wall_seconds_across_cases"
                ],
                "all_real_UTC_candidates_including_DST_folds": d[
                    "sum_of_UTC_candidates_including_two_fold_branches"
                ],
                "by_case": {
                    c["case_id"]: {
                        "valid_UTC_instants": c[
                            "valid_UTC_candidate_instants_including_both_DST_folds"
                        ],
                        "nonexistent_wall_seconds": c["nonexistent_local_clock_second_count"],
                        "ambiguous_wall_seconds": c["ambiguous_local_clock_second_count"],
                        "UTC_components": c["number_of_separate_UTC_components"],
                        "source_chart_state_count": c[
                            "original_source_unique_chart_states_across_all_UTC_and_calendar_hour_policies"
                        ],
                        "status": c["status"],
                    }
                    for c in d["cases"]
                },
                "actual_blind_human_chart_predictions": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
