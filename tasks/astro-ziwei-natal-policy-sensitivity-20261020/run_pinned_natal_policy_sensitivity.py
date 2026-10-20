#!/usr/bin/env python3
"""Build accepted-source pinned engine in temp and test four synthetic clocks.

No external live API, no real birth records, no applicant screening, no actual
human predictions. The optional reference libraries are deliberately NOT
vendored or distributed here. Exact versions 1.4.8 and 2.0.7 are required.
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
MANIFEST = B / "PINNED_ENGINE_FILE_MANIFEST_V1.json"
WORKER = B / "worker_compute_synthetic_policy_variants.py"
OUTPUT = B / "PINNED_ENGINE_SYNTHETIC_NATAL_POLICY_SENSITIVITY_V1.json"
PREVIOUS = (
    ROOT / "tasks/astro-hour-stability-20261020/FOUR_ANCHOR_SOURCE_FEATURE_HOUR_SENSITIVITY_V1.json"
)
ENGINE_COMMIT = "fb6b30b1ca67ff62fecc0c4ea7f3e4d0553640d4"
PREVIOUS_AUDIT_SHA = "1303731a6ae0c1906dd439509c28951f15fa1ec2df6b17d04fc8a44c5b365d11"
EXPECTED_LIBRARY_TREE_SHA = {
    "lunar_python": "7123d898cbe2e8afff663e57a7e25c9d4f080e383b98fcc33485d502772a2303",
    "sxtwl": "b4c1b25f0453489e10c6d25c5407e904a31e7fca1dc72615fda5db169f143d14",
}
DEFAULT_CALENDAR_PACKAGE_SITE = Path("/tmp/hd-calendar-parity-20261020")
ROOT_SOURCE = "tasks/astro-chinese-primary-sources-20261017"
ENGINE_ZIWEI_DIR = ROOT_SOURCE + "/ziwei"


def digest(b: bytes) -> str:
    return sha256(b).hexdigest()


def fail(msg: str) -> None:
    raise ValueError("Pinned synthetic natal engine policy audit rejected: " + msg)


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verified_sources(from_archive_only: bool = False) -> dict[str, bytes]:
    manifest = read(MANIFEST)
    if (
        manifest.get("schema") != "PINNED_20261020_ORIGINAL_ZIWEI_NATAL_TIME_ENGINE_SOURCE_FILES_V1"
        or manifest.get("source_engine_parent_commit") != ENGINE_COMMIT
    ):
        fail("independent accepted source engine Git commit/version changed")
    if manifest.get("source_real_human_predictive_validations") != 0:
        fail("historical source must not assert actual human astrology accuracy")
    expected = manifest.get("source_engine_original_files_sha_and_bytes", {})
    if len(expected) != 22:
        fail("pinned engine source and original HKO witness member count incorrect")
    blobs = {}
    for name, meta in expected.items():
        p = ROOT / name
        if p.is_file() and (
            p.stat().st_size == meta["bytes"] and digest(p.read_bytes()) == meta["sha256"]
        ):
            b = p.read_bytes()
        else:
            if from_archive_only:
                fail("original accepted engine file not present in cold offline package: " + name)
            cp = subprocess.run(
                ["git", "show", f"{ENGINE_COMMIT}:{name}"],
                cwd=ROOT,
                capture_output=True,
                check=True,
            )
            b = cp.stdout
        if len(b) != meta["bytes"] or digest(b) != meta["sha256"]:
            fail("original engine code/source SHA mismatch " + name)
        blobs[name] = b
    return blobs


def verify_calendar_packages(site: Path) -> dict:
    # This is a local testing dependency, not authorization to download or
    # install packages. Without exact installed versions, fail closed.
    if not site.is_dir():
        fail("optional two independent lunar calendar libraries unavailable at pinned path")
    cmd = [
        sys.executable,
        "-c",
        "import json;from importlib.metadata import version;"
        "print(json.dumps({'lunar_python':version('lunar_python'),"
        "'sxtwl':version('sxtwl')}))",
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(site)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=15)
    if r.returncode:
        fail("both pinned external calendar packages unavailable")
    versions = json.loads(r.stdout)
    if versions != {"lunar_python": "1.4.8", "sxtwl": "2.0.7"}:
        fail("external lunar calendar package versions not original pinned versions")
    for package, expected in EXPECTED_LIBRARY_TREE_SHA.items():
        matching = []
        for p in site.rglob("*"):
            if not p.is_file() or "__pycache__" in p.parts:
                continue
            relative = p.relative_to(site)
            root_name = relative.parts[0]
            if root_name.startswith(package) or root_name.startswith("_" + package):
                matching.append((str(relative), len(p.read_bytes()), digest(p.read_bytes())))
        canonical = "\n".join(f"{name} {count} {h}" for name, count, h in sorted(matching)).encode(
            "utf-8"
        )
        if digest(canonical) != expected:
            fail(
                "pinned optional lunar calendar package source/binary "
                "fingerprint changed: " + package
            )
    return versions


def build(*, from_archive_only: bool = False, calendar_site: Path | None = None) -> dict:
    cal = calendar_site or Path(
        os.environ.get("ZIWEI_PINNED_CALENDAR_SITE", str(DEFAULT_CALENDAR_PACKAGE_SITE))
    )
    versions = verify_calendar_packages(cal)
    source = verified_sources(from_archive_only=from_archive_only)
    if digest(PREVIOUS.read_bytes()) != PREVIOUS_AUDIT_SHA:
        fail("accepted parent synthetic hour sensitivity provenance SHA changed")
    prior = read(PREVIOUS)
    if (
        prior["unique_synthetic_source_states"] != 120
        or prior["strict_methodological_abstentions_from_120_synthetic_states"] != 110
        or prior["real_human_forward_or_reverse_predictions_validated"] != 0
    ):
        fail("prior source-chart conditional applicability/abstention audit changed")
    with tempfile.TemporaryDirectory(prefix="pinned_ziwei_natal_policy_") as tmp:
        dir = Path(tmp)
        for name, raw in source.items():
            p = dir / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
        engine_dir = dir / ENGINE_ZIWEI_DIR
        env = os.environ.copy()
        env["PYTHONPATH"] = str(engine_dir) + os.pathsep + str(cal)
        result = subprocess.run(
            [sys.executable, str(WORKER)],
            cwd=dir,
            env=env,
            capture_output=True,
            text=True,
            timeout=90,
        )
        if result.returncode:
            raise RuntimeError(
                "Pinned source engine synthetic-only failed, no fallback model permitted:\n"
                + result.stderr[-2600:]
            )
        worker = json.loads(result.stdout)
    cases = worker.get("cases", [])
    if (
        len(cases) != 4
        or any(len(x.get("policy_cases", [])) != 12 for x in cases)
        or len(worker.get("unsupported_conditions_fail_closed", [])) != 7
    ):
        fail("source engine case/policy/fail-closed count deviated from selected scope")
    if worker.get("actual_human_natal_test_count") != 0:
        fail("source-only study cannot claim actual human prediction")
    if not all(x["actual_failed_closed"] for x in worker["unsupported_conditions_fail_closed"]):
        fail("unsupported actual-birth policies were silently resolved")
    all_cases = [r for case in cases for r in case["policy_cases"]]
    if any(
        x["is_actual_ordinary_human_behavioral_prediction"] is not False
        or x["is_complete_Zi_Wei_chart"] is not False
        for x in all_cases
    ):
        fail("original mechanical chart wrongly described as complete or human outcome")
    witness_counts = {
        "original_HKO_and_pinned_dual_calendar": sum(
            r["calendar_witness_quality"]
            == "INDEPENDENT_HKO_SOURCE_JSON_SHA_PLUS_TWO_SOFTWARE_CALENDARS"
            for r in all_cases
        ),
        "dual_calendar_software_only": sum(
            r["calendar_witness_quality"] == "DUAL_SOFTWARE_CALENDARS_ONLY_NO_PINNED_HKO_SOURCE"
            for r in all_cases
        ),
    }
    if sum(witness_counts.values()) != 48:
        fail("HKO original versus other dual-software witness scope inconsistent")
    envelope = {
        "schema": "HUMANDESIGN_PINNED_SOURCE_ZIWEI_SYNTHETIC_NATAL_POLICY_SENSITIVITY_V1",
        "status": (
            "EXPLICIT_SOURCE_PINNED_CIVIL_CLOCK_AND_CHINESE_CALENDAR_"
            "POLICIES_ONLY_NOT_HUMAN_PREDICTION"
        ),
        "original_accepted_engine_git_commit": ENGINE_COMMIT,
        "exact_original_engine_file_manifest_sha256": digest(MANIFEST.read_bytes()),
        "exact_original_engine_member_count": len(source),
        "source_engine_pinned_original_file_SHA256": {x: digest(b) for x, b in source.items()},
        "calendar_optional_libraries_external_and_unbundled": True,
        "calendar_optional_library_versions": versions,
        "calendar_optional_library_installed_tree_sha256": EXPECTED_LIBRARY_TREE_SHA.copy(),
        "original_prior_source_hour_sensitivity_audit_SHA256": PREVIOUS_AUDIT_SHA,
        "calendar_site_runtime_path_specific_to_owner_machine_not_archive_input": True,
        "source_lunar_calendar_BaZi_LiChun_year_policy_unimplemented": True,
        "source_fourteen_principal_stars_not_all_ancillary_astrology_stars": True,
        "ancient_original_Ming_woodblock_authenticated": False,
        "source_civil_clock_dst_and_zoneinfo_inputs_are_explicit": True,
        "original_HKO_calendar_witness_counts": witness_counts,
        "synthetic_birth_clocks_and_assumption_variants": worker,
        "actual_human_consent_or_birth_data": 0,
        "real_human_forward_reverse_predictive_validations": 0,
        "production_astrological_rule_promotions": 0,
    }
    OUTPUT.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return envelope


if __name__ == "__main__":
    x = build()
    results = x["synthetic_birth_clocks_and_assumption_variants"]
    print(
        json.dumps(
            {
                "synthetic_local_clocks": results["fictitious_independent_test_clocks"],
                "policy_variants": sum(c["policy_count"] for c in results["cases"]),
                "source_as_next_distinct_life_configurations": {
                    c["case_id"]: c[
                        "source_original_leap_grid_distinct_life_plus_clock_configurations"
                    ]
                    for c in results["cases"]
                },
                "raw_HKO_witness_counts": x["original_HKO_calendar_witness_counts"],
                "unsupported_policies_failed_closed": len(
                    results["unsupported_conditions_fail_closed"]
                ),
                "real_human_predictions": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
