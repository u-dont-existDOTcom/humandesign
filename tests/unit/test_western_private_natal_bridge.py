"""Synthetic-only integration of strict Swiss natal skies to sealed modern directions.

Synthetic timestamp is a test fixture, not the owner or an actual participant.
No private HMAC keys, real birth details or outcome records are published.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

import pytest

from hdmatch.astrology import western_private_natal_bridge as bridge

ROOT = Path(__file__).resolve().parents[2]
SYNTHETIC = {
    "schema": bridge.PRIVATE_SCHEMA,
    "pseudonymous_participant_id": "SYNTHETIC_TEST_CASE_001",
    "birth_utc": "2000-01-01T12:00:00+00:00",
    "latitude_deg": 40.0,
    "longitude_east_deg": -75.0,
    "birth_time_uncertainty_minutes": 1,
    "birth_time_quality": "unknown_or_rectified",
}


@pytest.fixture(scope="module")
def computed_synthetic() -> tuple[bridge.PrivateNatalTuple, dict, bytes]:
    """One real Swiss calculation, still entirely fictional data."""
    pytest.importorskip("swisseph")
    ephemeris = os.environ.get("HDMATCH_PRIMARY_DIR_EPHE_DIR")
    if not ephemeris:
        pytest.skip("strict verified Swiss fixture requires explicit ephemeris folder")
    input_tuple = bridge.PrivateNatalTuple.from_json(dict(SYNTHETIC))
    synthetic_only_dummy_key = b"S" * 32
    result = bridge.build_sealed_direction_diagnostic(
        input_tuple,
        secret=synthetic_only_dummy_key,
        ephemeris_directory=Path(ephemeris),
    )
    return input_tuple, result, synthetic_only_dummy_key


def test_normalized_utc_only_and_rejects_extraneous_private_fields() -> None:
    assert bridge.PrivateNatalTuple.from_json(dict(SYNTHETIC)).birth_utc.isoformat() == (
        "2000-01-01T12:00:00+00:00"
    )
    for bad in (
        {**SYNTHETIC, "birth_utc": "2000-01-01T12:00:00"},
        {**SYNTHETIC, "birth_utc": "2000-01-01T12:00:00+02:00"},
        {**SYNTHETIC, "birth_time_uncertainty_minutes": 1.5},
        {**SYNTHETIC, "birth_time_uncertainty_minutes": 20},
        {**SYNTHETIC, "longitude_east_deg": "not-a-number"},
        {**SYNTHETIC, "latitude_deg": 70},
        {**SYNTHETIC, "full_legal_name": "SHOULD_NEVER_APPEAR"},
        {**SYNTHETIC, "birth_time_quality": "verified_by_astrology"},
    ):
        with pytest.raises(ValueError):
            bridge.PrivateNatalTuple.from_json(bad)


def test_original_source_registry_is_exact_and_must_match_sha256(monkeypatch) -> None:
    bodies, rays = bridge._read_fixed_rules()
    assert len(bodies) == len(rays) == 4
    actual = {*bodies.values(), *(x["id"] for x in rays.values())}
    assert actual == set(bridge.SOURCE_CANDIDATES)
    monkeypatch.setitem(
        bridge.SOURCE_FILES,
        "LILLY_1647_EVENT_CANDIDATES.json",
        "f" * 64,
    )
    with pytest.raises(ValueError, match="modified"):
        bridge._read_fixed_rules()


def test_swiss_natal_adapter_and_provenance_never_leak_birth_data(
    computed_synthetic,
) -> None:
    _input, result, _dummy_key = computed_synthetic
    assert result["schema"] == "PRIVATE_SOURCE_BOUND_WESTERN_DIAGNOSTIC_RECEIPT_V0"
    assert result["stage"] == "ENGINEERING_ONLY_NOT_A_HUMAN_MODEL_OR_OUTCOME_FREEZE"
    assert result["minute_samples_count"] == 3
    assert result["ephemeris_source_sha256"] == bridge.EXPECTED_EPHEMERIS
    assert result["source_rule_files_sha256"] == bridge.SOURCE_FILES
    assert result["method_contract"]["geometry"] == "regiomontanian_position_circle"
    assert result["method_contract"]["time_key"] == "ptolemy_one_degree_per_year"
    assert result["human_predictive_accuracy"] == "UNTESTED"
    assert result["real_birth_inputs_in_output"] is False
    payload = json.dumps(result, sort_keys=True)
    assert "2000-01-01" not in payload
    assert "12:00:00" not in payload
    assert '"birth_utc"' not in payload
    assert '"latitude_deg"' not in payload
    assert '"longitude_east_deg"' not in payload
    assert result["deduplicated_candidate_contacts"] == len(
        result["sealed_diagnostic_receipt"]["windows"]
    )


def test_hmac_private_commitment_cannot_be_guessed_from_plain_birth_hash(
    computed_synthetic,
) -> None:
    row, receipt, dummy_key = computed_synthetic
    record = receipt["sealed_diagnostic_receipt"]
    assert record["human_predictive_accuracy"] == "UNTESTED"
    digest = record["birth_input_sha256"]
    assert len(digest) == 64
    pure_data = {
        "schema": bridge.PRIVATE_SCHEMA,
        "pseudonymous_participant_id": row.pseudonymous_participant_id,
        "birth_utc": row.birth_utc.isoformat(),
        "latitude_deg": row.latitude_deg,
        "longitude_east_deg": row.longitude_east_deg,
        "birth_time_uncertainty_minutes": row.birth_time_uncertainty_minutes,
        "birth_time_quality": row.birth_time_quality,
    }
    assert digest == bridge._hmac_sha256(dummy_key, pure_data)
    assert digest != hashlib.sha256(bridge.canonical(pure_data)).hexdigest()
    assert digest != bridge._hmac_sha256(b"X" * 32, pure_data)
    with pytest.raises(ValueError, match="secret"):
        bridge._hmac_sha256(b"short", pure_data)


def test_only_tentative_modern_timing_and_unresolved_source_null(
    computed_synthetic,
) -> None:
    _, artifact, _ = computed_synthetic
    all_source_keys = set(bridge.SOURCE_CANDIDATES)
    scoring_rules = {"L1647-MC-JUP-BODY", "L1647-MC-SAT-BODY"}
    all_windows = artifact["sealed_diagnostic_receipt"]["windows"]
    assert all(w["source_rule_id"] in all_source_keys for w in all_windows)
    assert all(w["historical_model_ready"] is False for w in all_windows)
    assert all(
        w["timing"] is None
        for w in all_windows
        if w["source_rule_id"] not in scoring_rules
        or w["reason"] == "CONTACT_DISAPPEARS_FOR_SOME_PLAUSIBLE_BIRTHTIMES"
    )
    assert artifact["tentative_modern_timing_windows_for_future_freeze"] == sum(
        w["timing"] is not None for w in all_windows
    )
    assert artifact["sealed_diagnostic_receipt"]["historical_Argolus_or_Lilly_exactness"] == (
        "UNRESOLVED"
    )


def test_private_output_is_created_once_with_mode_0600_and_no_raw_birth(
    computed_synthetic,
    tmp_path,
) -> None:
    _, artifact, _ = computed_synthetic
    target = tmp_path / "sanitized_test_receipt.json"
    bridge.write_private_receipt_once(target, artifact)
    saved = json.loads(target.read_text())
    assert saved == json.loads(bridge.canonical(artifact))
    assert stat.S_IMODE(target.stat().st_mode) == 0o600
    assert "2000-01-01" not in target.read_text()
    assert '"birth_utc"' not in target.read_text()
    with pytest.raises(FileExistsError):
        bridge.write_private_receipt_once(target, artifact)


def test_private_key_input_rejects_world_readable_files_and_symlinks(tmp_path) -> None:
    key = tmp_path / "synthetic_secret_key"
    key.write_bytes(b"TEST-ONLY-NOT-A-REAL-SECRET--32BYTE")
    key.chmod(0o644)
    with pytest.raises(ValueError, match="owner-only permissions"):
        bridge._read_private_bytes(key)
    key.chmod(0o600)
    assert bridge._read_private_bytes(key).startswith(b"TEST-ONLY")
    link = tmp_path / "synthetic_link"
    link.symlink_to(key)
    with pytest.raises(ValueError, match="non-symlink"):
        bridge._read_private_bytes(link)


def test_refuse_private_input_or_output_path_inside_git_repo(computed_synthetic) -> None:
    _, artifact, _ = computed_synthetic
    source_file = ROOT / "src/hdmatch/astrology/western_private_natal_bridge.py"
    with pytest.raises(ValueError, match="outside the Git repository"):
        bridge._read_private_bytes(source_file)
    forbidden = ROOT / "tests/unit/DO_NOT_CREATE_PRIVATE_RECEIPT.json"
    with pytest.raises(ValueError, match="outside the Git repository"):
        bridge.write_private_receipt_once(forbidden, artifact)
    assert not forbidden.exists()


def test_runtime_will_not_allow_missing_swiss_ephemeris_sources(tmp_path) -> None:
    private = bridge.PrivateNatalTuple.from_json({**SYNTHETIC, "birth_time_uncertainty_minutes": 0})
    with pytest.raises((FileNotFoundError, ValueError, RuntimeError)):
        bridge.build_sealed_direction_diagnostic(
            private,
            secret=b"T" * 32,
            ephemeris_directory=tmp_path,
        )


def test_no_earlier_synthetic_development_occupancy_mislabel_as_this_model() -> None:
    name = bridge.METHOD.value
    prior = ROOT / (
        "docs/astrology-research-map/primary-direction-synthetic-panel-20261024/PANEL_PLAN.json"
    )
    data = json.loads(prior.read_text())
    assert data["geometry"] == "proportional_semi_arc"
    assert name == "regiomontanian_position_circle"
    assert data["geometry"] != name


def test_cli_synthetic_only_private_file_to_write_once_receipt(tmp_path) -> None:
    """Prove the actual command accepts owner-only files and never echoes birth."""
    import subprocess
    import sys

    ephemeris = os.environ.get("HDMATCH_PRIMARY_DIR_EPHE_DIR")
    if not ephemeris:
        pytest.skip("Swiss source path is required for integration")
    private_input = tmp_path / "fictional_private_record.json"
    private_input.write_text(json.dumps(SYNTHETIC), encoding="utf-8")
    private_input.chmod(0o600)
    key_file = tmp_path / "fictional_only_key.bin"
    key_file.write_bytes(b"F" * 32)
    key_file.chmod(0o600)
    receipt_file = tmp_path / "fictional_only_out.json"

    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    cmd = [
        sys.executable,
        "-m",
        "hdmatch.astrology.western_private_natal_bridge",
        "--private-input",
        str(private_input),
        "--secret-key-file",
        str(key_file),
        "--ephemeris-dir",
        ephemeris,
        "--external-receipt",
        str(receipt_file),
    ]
    completed = subprocess.run(
        cmd,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=90,
    )
    assert completed.returncode == 0, completed.stderr
    assert "RESEARCH_ONLY_SANITIZED_RECEIPT_WRITTEN" in completed.stdout
    assert "2000-01-01" not in completed.stdout
    assert "SYNTHETIC_TEST_CASE_001" not in completed.stdout
    assert "2000-01-01" not in completed.stderr
    saved = json.loads(receipt_file.read_text())
    assert saved["human_predictive_accuracy"] == "UNTESTED"
    assert saved["private_input_digest_scheme"].startswith("HMAC-SHA256")
    assert saved["real_birth_inputs_in_output"] is False
    assert stat.S_IMODE(receipt_file.stat().st_mode) == 0o600
    assert '"birth_utc"' not in receipt_file.read_text()


def test_unexpected_private_output_fields_are_rejected_before_disk(
    computed_synthetic,
    tmp_path,
) -> None:
    _, record, _ = computed_synthetic
    suspicious = dict(record)
    suspicious["birth_utc"] = "FICTIONAL_SENSITIVE_CANARY"
    target = tmp_path / "never_created.json"
    with pytest.raises(ValueError, match="raw private"):
        bridge.write_private_receipt_once(target, suspicious)
    assert not target.exists()


def test_source_code_and_protocol_manifest_match_current_research_checkout() -> None:
    import importlib.util

    folder = ROOT / "docs/astrology-research-map/western-private-natal-bridge-20261025"
    verification_file = folder / "build_verification.py"
    spec = importlib.util.spec_from_file_location(
        "private_bridge_source_manifest", verification_file
    )
    assert spec and spec.loader
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    stored = json.loads((folder / "VERIFICATION.json").read_text())
    assert verifier.manifest() == stored
    assert stored["human_predictive_validity"] == "UNTESTED"
    assert stored["private_input_exposure"] == "NO_REAL_BIRTH_RECORDS_USED"
    for path, proof in stored["file_sha256"].items():
        f = ROOT / path
        assert f.stat().st_size == proof["bytes"]
        assert hashlib.sha256(f.read_bytes()).hexdigest() == proof["sha256"]


def test_synthetic_natal_calculation_receipt_exactly_replays(computed_synthetic) -> None:
    input_tuple, original, dummy_key = computed_synthetic
    folder = os.environ["HDMATCH_PRIMARY_DIR_EPHE_DIR"]
    repeated = bridge.build_sealed_direction_diagnostic(
        input_tuple,
        secret=dummy_key,
        ephemeris_directory=Path(folder),
    )
    assert bridge.canonical(repeated) == bridge.canonical(original)
    assert (
        repeated["sealed_diagnostic_receipt"]["commitment_sha256"]
        == original["sealed_diagnostic_receipt"]["commitment_sha256"]
    )


def test_fails_closed_if_swiss_file_fingerprint_does_not_match(
    monkeypatch,
    computed_synthetic,
) -> None:
    input_tuple, _record, dummy_key = computed_synthetic
    changed = {**bridge.EXPECTED_EPHEMERIS, "sepl_18.se1": "0" * 64}
    monkeypatch.setattr(bridge, "EXPECTED_EPHEMERIS", changed)
    with pytest.raises(RuntimeError, match="hashes"):
        bridge.build_sealed_direction_diagnostic(
            input_tuple,
            secret=dummy_key,
            ephemeris_directory=Path(os.environ["HDMATCH_PRIMARY_DIR_EPHE_DIR"]),
        )
