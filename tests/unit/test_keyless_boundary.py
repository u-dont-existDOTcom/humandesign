from __future__ import annotations

import hashlib
import os
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from hdmatch.cli import _parser as hdmatch_parser
from hdmatch.cli import main as hdmatch_main
from hdmatch.experiments.canonical import load_json_bytes, write_new_canonical_json
from hdmatch.experiments.manifest import git_revision
from hdmatch.runtime.keyless_boundary import (
    IsolationRuntimeUnavailable,
    RecoveryBoundaryRequest,
    SourceProvenance,
    bubblewrap_capable,
    build_recovery_mount_plan,
    run_claim_grade_recovery,
    run_isolation_harness,
)
from hdmatch.runtime.keyless_boundary import _parser as keyless_parser
from hdmatch.runtime.recovery import recover_blind_file

ROOT = Path(__file__).resolve().parents[2]


def _parser_destinations(parser: object) -> set[str]:
    return {action.dest for action in parser._actions}  # type: ignore[attr-defined]


def test_recovery_interfaces_have_no_key_decrypt_or_reveal_parameter() -> None:
    root_parser = hdmatch_parser()
    command_action = next(
        action for action in root_parser._actions if action.dest == "command"  # type: ignore[attr-defined]
    )
    recover_parser = command_action.choices["recover"]  # type: ignore[attr-defined]
    recovery_arguments = _parser_destinations(recover_parser)
    wrapper_arguments = _parser_destinations(keyless_parser())
    runtime_arguments = set(recover_blind_file.__annotations__)

    for destinations in (recovery_arguments, wrapper_arguments, runtime_arguments):
        assert not any(
            marker in destination
            for destination in destinations
            for marker in ("key", "decrypt", "reveal", "envelope", "truth")
        )


def _public_request(tmp_path: Path) -> tuple[RecoveryBoundaryRequest, SourceProvenance]:
    source_root = tmp_path / "source"
    tracked = source_root / "src" / "hdmatch" / "__init__.py"
    tracked.parent.mkdir(parents=True)
    tracked.write_text("\n", encoding="utf-8")
    blind = tmp_path / "blind.json"
    write_new_canonical_json(
        blind,
        {
            "schema_version": "blind-synthetic-v1",
            "experiment_id": "BOUNDARY-CONSTRUCTION",
            "cases": [],
        },
    )
    questions = tmp_path / "questions.json"
    write_new_canonical_json(questions, {"schema_version": "question-bank-test-v1"})
    mapping = tmp_path / "mapping.json"
    write_new_canonical_json(
        mapping,
        {"question_bank_sha256": hashlib.sha256(questions.read_bytes()).hexdigest()},
    )
    ephemeris = tmp_path / "ephemeris"
    ephemeris.mkdir()
    (ephemeris / "public.se1").write_bytes(b"public-test-ephemeris")
    cache = tmp_path / "cache"
    cache.mkdir()
    write_new_canonical_json(
        cache / "month-2000-01-UTC-test.json",
        {"schema_version": "candidate-universe-cache-v1", "states": []},
    )
    output = tmp_path / "output"
    output.mkdir()
    request = RecoveryBoundaryRequest(
        blind_file=blind,
        output_dir=output,
        ephemeris_path=ephemeris,
        mapping_file=mapping,
        question_bank_file=questions,
        python_environment=Path(sys.prefix),
        candidate_cache=cache,
    )
    provenance = SourceProvenance(
        repository_root=source_root,
        commit="a" * 40,
        tree="b" * 40,
        tracked_decoder_files=(tracked,),
    )
    return request, provenance


def test_recovery_mount_plan_is_allowlisted_read_only_and_keyless(tmp_path: Path) -> None:
    request, provenance = _public_request(tmp_path)
    plan = build_recovery_mount_plan(request, provenance=provenance, bwrap="/usr/bin/bwrap")
    command = plan.command

    assert "--unshare-all" in command
    assert "--disable-userns" in command
    assert "--clearenv" in command
    assert command[command.index("--uid") : command.index("--uid") + 2] == ("--uid", "65534")
    assert command[command.index("--gid") : command.index("--gid") + 2] == ("--gid", "65534")
    writable_sources = [
        command[index + 1] for index, item in enumerate(command) if item == "--bind"
    ]
    assert writable_sources == [str(request.output_dir.resolve())]
    child_start = command.index("hdmatch.cli")
    child_arguments = command[child_start:]
    assert child_arguments[1] == "recover"
    assert not any(
        marker in argument.casefold()
        for argument in child_arguments
        for marker in ("key-file", "decrypt", "reveal", "envelope", "truth")
    )
    assert str(request.question_bank_file.resolve()) in command
    assert str(request.ephemeris_path.resolve() / "public.se1") in command
    assert str(request.candidate_cache.resolve() / "month-2000-01-UTC-test.json") in command
    assert not any(argument.startswith("HDMATCH_ISOLATED_SOURCE") for argument in command)


def test_ordinary_manifest_git_revision_ignores_isolation_spoof_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HDMATCH_ISOLATED_SOURCE_COMMIT", "f" * 40)
    monkeypatch.setenv("HDMATCH_ISOLATED_SOURCE_TREE", "e" * 40)
    monkeypatch.setenv("HDMATCH_ISOLATED_SOURCE_ROOT", str(ROOT))

    commit, _dirty = git_revision(ROOT)
    assert commit != "f" * 40


def test_wrapper_fails_closed_before_creating_output_without_isolation_runtime(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request, _ = _public_request(tmp_path)
    request.output_dir.rmdir()
    monkeypatch.setattr("hdmatch.runtime.keyless_boundary.shutil.which", lambda _name: None)

    with pytest.raises(IsolationRuntimeUnavailable, match="Bubblewrap"):
        run_claim_grade_recovery(request, repository_root=ROOT)
    assert not request.output_dir.exists()


def test_wrapper_rejects_child_environment_that_differs_from_manifest_runtime(
    tmp_path: Path,
) -> None:
    request, _ = _public_request(tmp_path)
    request.output_dir.rmdir()
    different_environment = tmp_path / "different-python-environment"
    different_environment.mkdir()

    with pytest.raises(
        RuntimeError,
        match="child Python environment must equal the wrapper environment",
    ):
        run_claim_grade_recovery(
            replace(request, python_environment=different_environment),
            repository_root=ROOT,
        )
    assert not request.output_dir.exists()


def test_cli_preflight_rejects_plaintext_key_in_run_dir_before_model_or_cache(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    write_new_canonical_json(
        run_dir / "ordinary.data",
        {
            "schema_version": "answer-key-v1",
            "experiment_id": "EXP",
            "blind_input_sha256": "a" * 64,
            "cases": [{"case_id": "C1", "true_local_date": "2000-01-01"}],
        },
    )
    missing_blind = tmp_path / "missing-blind.json"
    missing_ephemeris = tmp_path / "missing-ephemeris"

    with pytest.raises(SystemExit) as raised:
        hdmatch_main(
            (
                "recover",
                "--run-dir",
                str(run_dir),
                "--blind-file",
                str(missing_blind),
                "--ephemeris",
                str(missing_ephemeris),
            )
        )
    assert raised.value.code == 2
    stderr = capsys.readouterr().err
    assert "plaintext answer key file" in stderr
    assert str(run_dir) not in stderr


def test_real_bubblewrap_boundary_reads_public_input_writes_output_and_denies_secret(
    tmp_path: Path,
) -> None:
    if not bubblewrap_capable():
        pytest.skip("Bubblewrap cannot establish the required namespaces on this host")
    public_input = tmp_path / "public-input.bin"
    public_input.write_bytes(b"candidate-blind-public-input\n")
    secret = tmp_path / "evaluator" / "ordinary.data"
    secret.parent.mkdir()
    secret.write_bytes(b"never-mount-this-evaluator-secret\n")
    output = tmp_path / "output"

    receipt_path = run_isolation_harness(
        public_input=public_input,
        output_dir=output,
        denied_host_path=secret,
        python_environment=Path(sys.prefix),
        repository_root=ROOT,
    )
    receipt = load_json_bytes(receipt_path, require_canonical=True)
    assert receipt["public_input_accessible"] is True
    assert receipt["evaluator_secret_location_accessible"] is False
    assert receipt["sandbox_uid"] == 65534
    assert receipt["sandbox_gid"] == 65534
    assert secret.read_bytes() not in receipt_path.read_bytes()
    assert str(secret).encode() not in receipt_path.read_bytes()


@pytest.mark.skipif(
    os.environ.get("HDMATCH_RUN_EXACT_KEYLESS_E2E") != "1",
    reason="set HDMATCH_RUN_EXACT_KEYLESS_E2E=1 with retained public fixtures",
)
def test_optional_real_exact_recovery_completes_inside_keyless_boundary(
    tmp_path: Path,
) -> None:
    if not bubblewrap_capable():
        pytest.skip("Bubblewrap cannot establish the required namespaces on this host")
    ephemeris = Path("/tmp/hdmatch-ephe")
    retained_run = Path(
        "/tmp/hdmatch-integration/run_artifacts/known_month_oracle_1000"
    )
    blind_source = retained_run / "blind_cases.json"
    retained_cache = retained_run / "candidate_cache"
    if not blind_source.is_file() or not retained_cache.is_dir() or not ephemeris.is_dir():
        pytest.skip("retained public exact-recovery fixtures are unavailable")

    blind = load_json_bytes(blind_source, require_canonical=True)
    assert isinstance(blind, dict)
    cases = blind["cases"]
    assert isinstance(cases, list) and cases
    selected = cases[0]
    assert isinstance(selected, dict)
    blind["cases"] = [selected]
    blind_file = tmp_path / "one-public-blind-case.json"
    write_new_canonical_json(blind_file, blind)
    cache = tmp_path / "public-cache"
    cache.mkdir()
    zone = str(selected["iana_timezone"]).replace("/", "_")
    prefix = (
        f"month-{int(selected['known_birth_year']):04d}-"
        f"{int(selected['known_birth_month']):02d}-{zone}-"
    )
    matching = tuple(retained_cache.glob(f"{prefix}*.json"))
    assert len(matching) == 1
    (cache / matching[0].name).hardlink_to(matching[0])

    receipt_path = run_claim_grade_recovery(
        RecoveryBoundaryRequest(
            blind_file=blind_file,
            output_dir=tmp_path / "run-output",
            ephemeris_path=ephemeris,
            mapping_file=ROOT / "mappings" / "mapping_library_v1.json",
            question_bank_file=ROOT / "reference" / "core" / "question_bank_v1.json",
            python_environment=Path(sys.prefix),
            candidate_cache=cache,
        ),
        repository_root=ROOT,
    )
    receipt = load_json_bytes(receipt_path, require_canonical=True)
    predictions = load_json_bytes(
        tmp_path / "run-output" / "predictions.json", require_canonical=True
    )
    assert receipt["command_contract"]["exit_status"] == 0
    assert receipt["runtime_controls"]["evaluator_secret_mounts"] == "absent"
    assert isinstance(predictions, dict)
    assert len(predictions["predictions"]) == 1
