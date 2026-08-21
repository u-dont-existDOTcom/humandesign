"""Claim-grade keyless recovery in a fail-closed Bubblewrap boundary.

The recovery process receives a deliberately small mount set. Evaluator keys,
plaintext truth, encrypted envelopes, parent directories, and the host network
namespace are never mounted or shared by this wrapper.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, Final

from hdmatch.evaluation.leakage import assert_no_blind_leakage
from hdmatch.experiments.canonical import sha256_file, write_new_canonical_json
from hdmatch.runtime.symbolic_adapter import MODEL_A_ID, MODEL_B_ID
from hdmatch.search import AggregationMode
from hdmatch.synthetic.sealing import assert_no_plaintext_answer_keys_in_paths

_SANDBOX_ROOT: Final[PurePosixPath] = PurePosixPath("/workspace")
_SANDBOX_SOURCE: Final[PurePosixPath] = _SANDBOX_ROOT / "src"
_SANDBOX_RUNTIME: Final[PurePosixPath] = PurePosixPath("/runtime")
_SANDBOX_PUBLIC: Final[PurePosixPath] = PurePosixPath("/public")
_SANDBOX_OUTPUT: Final[PurePosixPath] = PurePosixPath("/output")
_RECEIPT_NAME: Final[str] = "keyless-isolation.receipt.json"


class KeylessIsolationError(RuntimeError):
    """The requested run cannot satisfy the claim-grade isolation contract."""


class IsolationRuntimeUnavailable(KeylessIsolationError):
    """Bubblewrap is absent or cannot establish every required namespace."""


@dataclass(frozen=True, slots=True)
class SourceProvenance:
    repository_root: Path
    commit: str
    tree: str
    tracked_decoder_files: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class RecoveryBoundaryRequest:
    blind_file: Path
    output_dir: Path
    ephemeris_path: Path
    mapping_file: Path
    question_bank_file: Path
    python_environment: Path
    model_id: str = MODEL_A_ID
    model_b_artifact: Path | None = None
    candidate_cache: Path | None = None
    workers: int = 1
    aggregation: str = AggregationMode.DURATION_WEIGHTED_EVIDENCE.value
    threshold_rubric_bits: float = 0.0


@dataclass(frozen=True, slots=True)
class RecoveryMountPlan:
    command: tuple[str, ...]
    ephemeris_files: tuple[Path, ...]
    candidate_cache_files: tuple[Path, ...]


def _run_git(repository_root: Path, *arguments: str) -> str:
    try:
        result = subprocess.run(
            ("git", *arguments),
            cwd=repository_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise KeylessIsolationError("cannot verify the decoder source checkout") from exc
    return result.stdout.strip()


def _source_provenance(repository_root: Path) -> SourceProvenance:
    root = repository_root.expanduser().resolve(strict=True)
    if _run_git(root, "status", "--porcelain", "--untracked-files=all"):
        raise KeylessIsolationError("claim-grade recovery requires a clean source checkout")
    commit = _run_git(root, "rev-parse", "HEAD")
    tree = _run_git(root, "rev-parse", "HEAD^{tree}")
    relative_files = tuple(
        Path(line)
        for line in _run_git(root, "ls-files", "--", "src/hdmatch").splitlines()
        if line
    )
    tracked = tuple(root / relative for relative in relative_files)
    if not tracked or any(not path.is_file() for path in tracked):
        raise KeylessIsolationError("tracked decoder source inventory is incomplete")
    return SourceProvenance(
        repository_root=root,
        commit=commit,
        tree=tree,
        tracked_decoder_files=tracked,
    )


def _runtime_python(python_environment: Path) -> str:
    environment = python_environment.expanduser().resolve(strict=True)
    if environment == Path("/usr"):
        executable = Path("/usr/bin/python3")
        sandbox_executable = "/usr/bin/python3"
    else:
        executable = environment / "bin" / "python"
        sandbox_executable = str(_SANDBOX_RUNTIME / "bin" / "python")
    if not executable.is_file():
        raise KeylessIsolationError("the dedicated Python environment has no interpreter")
    return sandbox_executable


def _bwrap_base(bwrap: str) -> list[str]:
    command = [
        bwrap,
        "--unshare-user",
        "--unshare-all",
        "--disable-userns",
        "--assert-userns-disabled",
        "--die-with-parent",
        "--new-session",
        "--uid",
        "65534",
        "--gid",
        "65534",
        "--cap-drop",
        "ALL",
        "--clearenv",
        "--ro-bind",
        "/usr",
        "/usr",
    ]
    for name in ("bin", "lib", "lib64", "sbin"):
        host = Path("/") / name
        if host.is_symlink():
            command.extend(("--symlink", os.readlink(host), str(host)))
        elif host.exists():
            command.extend(("--ro-bind", str(host), str(host)))
    command.extend(
        (
            "--dev",
            "/dev",
            "--proc",
            "/proc",
            "--tmpfs",
            "/tmp",
            "--setenv",
            "HOME",
            "/tmp",
            "--setenv",
            "TMPDIR",
            "/tmp",
            "--setenv",
            "PYTHONDONTWRITEBYTECODE",
            "1",
            "--setenv",
            "PYTHONNOUSERSITE",
            "1",
            "--setenv",
            "PYTHONPATH",
            str(_SANDBOX_SOURCE),
            "--setenv",
            "PATH",
            f"{_SANDBOX_RUNTIME}/bin:/usr/bin",
            "--setenv",
            "LC_ALL",
            "C.UTF-8",
        )
    )
    return command


def bubblewrap_capable(bwrap: str | None = None) -> bool:
    """Return true only when every required namespace/control can be established."""

    executable = bwrap or shutil.which("bwrap")
    if executable is None:
        return False
    try:
        result = subprocess.run(
            (*_bwrap_base(executable), "/usr/bin/true"),
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return False
    return result.returncode == 0


def _require_bubblewrap() -> str:
    executable = shutil.which("bwrap")
    if executable is None or not bubblewrap_capable(executable):
        raise IsolationRuntimeUnavailable(
            "Bubblewrap is unavailable or cannot establish the required isolation boundary"
        )
    return executable


def _bubblewrap_identity(executable: str) -> dict[str, str]:
    try:
        version = subprocess.run(
            (executable, "--version"),
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise IsolationRuntimeUnavailable("cannot bind the Bubblewrap runtime identity") from exc
    return {
        "name": "bubblewrap",
        "version": version,
        "executable_sha256": sha256_file(executable),
    }


def _add_directories(command: list[str], directories: set[PurePosixPath]) -> None:
    for directory in sorted(directories, key=lambda item: (len(item.parts), str(item))):
        command.extend(("--dir", str(directory)))


def _mount_tracked_source(command: list[str], provenance: SourceProvenance) -> None:
    targets: list[tuple[Path, PurePosixPath]] = []
    directories = {_SANDBOX_ROOT, _SANDBOX_SOURCE}
    for source in provenance.tracked_decoder_files:
        relative = source.relative_to(provenance.repository_root)
        target = _SANDBOX_ROOT / relative.as_posix()
        targets.append((source, target))
        directories.update(parent for parent in target.parents if str(parent) != "/")
    _add_directories(command, directories)
    for source, target in targets:
        command.extend(("--ro-bind", str(source), str(target)))


def _ephemeris_files(path: Path) -> tuple[Path, ...]:
    resolved = path.expanduser().resolve(strict=True)
    files = (resolved,) if resolved.is_file() else tuple(sorted(resolved.glob("*.se1")))
    if not files or any(not item.is_file() or item.suffix != ".se1" for item in files):
        raise KeylessIsolationError("ephemeris input must contain declared .se1 files")
    names = [item.name for item in files]
    if len(names) != len(set(names)):
        raise KeylessIsolationError("ephemeris filenames must be unique")
    return files


def _candidate_cache_files(path: Path | None) -> tuple[Path, ...]:
    if path is None:
        return ()
    resolved = path.expanduser().resolve(strict=True)
    if not resolved.is_dir():
        raise KeylessIsolationError("candidate cache must be a directory")
    files = tuple(sorted(resolved.glob("month-*.json")))
    if not files:
        raise KeylessIsolationError("candidate cache contains no public month cache files")
    assert_no_plaintext_answer_keys_in_paths((resolved,))
    return files


def _verify_question_binding(mapping_file: Path, question_bank_file: Path) -> None:
    try:
        mapping = json.loads(mapping_file.read_bytes())
    except (OSError, json.JSONDecodeError) as exc:
        raise KeylessIsolationError("mapping artifact is not valid JSON") from exc
    if not isinstance(mapping, dict):
        raise KeylessIsolationError("mapping artifact must be an object")
    if mapping.get("question_bank_sha256") != sha256_file(question_bank_file):
        raise KeylessIsolationError("question bank does not match the frozen mapping artifact")


def _prepare_output(path: Path) -> Path:
    output = path.expanduser().resolve(strict=False)
    output.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not output.is_dir():
        raise KeylessIsolationError("run output is not a directory")
    if any(output.iterdir()):
        raise KeylessIsolationError("claim-grade recovery requires an empty run output directory")
    return output


def build_recovery_mount_plan(
    request: RecoveryBoundaryRequest,
    *,
    provenance: SourceProvenance,
    bwrap: str,
) -> RecoveryMountPlan:
    """Build the fixed recovery command; no secret/key/reveal parameter exists."""

    if request.model_id not in {MODEL_A_ID, MODEL_B_ID}:
        raise KeylessIsolationError("unsupported symbolic model identity")
    if request.model_id == MODEL_B_ID and request.model_b_artifact is None:
        raise KeylessIsolationError("Model B requires its frozen artifact")
    if request.workers < 1:
        raise KeylessIsolationError("workers must be at least one")
    if request.aggregation not in {item.value for item in AggregationMode}:
        raise KeylessIsolationError("unsupported aggregation rule")

    blind = request.blind_file.expanduser().resolve(strict=True)
    mapping = request.mapping_file.expanduser().resolve(strict=True)
    questions = request.question_bank_file.expanduser().resolve(strict=True)
    output = request.output_dir.expanduser().resolve(strict=True)
    model_b = (
        request.model_b_artifact.expanduser().resolve(strict=True)
        if request.model_b_artifact is not None
        else None
    )
    for artifact in (blind, mapping, questions):
        if not artifact.is_file():
            raise KeylessIsolationError("a required public recovery artifact is missing")
    if model_b is not None and not model_b.is_file():
        raise KeylessIsolationError("the frozen Model B artifact is missing")
    _verify_question_binding(mapping, questions)
    assert_no_blind_leakage(blind)
    assert_no_plaintext_answer_keys_in_paths((blind, mapping, questions, output))

    ephemeris_files = _ephemeris_files(request.ephemeris_path)
    cache_files = _candidate_cache_files(request.candidate_cache)
    runtime = request.python_environment.expanduser().resolve(strict=True)
    sandbox_python = _runtime_python(runtime)

    command = _bwrap_base(bwrap)
    _mount_tracked_source(command, provenance)
    if runtime != Path("/usr"):
        command.extend(
            ("--dir", str(_SANDBOX_RUNTIME), "--ro-bind", str(runtime), str(_SANDBOX_RUNTIME))
        )
    command.extend(
        (
            "--dir",
            str(_SANDBOX_PUBLIC),
            "--dir",
            str(_SANDBOX_PUBLIC / "artifacts"),
            "--dir",
            str(_SANDBOX_PUBLIC / "ephemeris"),
            "--ro-bind",
            str(blind),
            str(_SANDBOX_PUBLIC / "blind_cases.json"),
            "--ro-bind",
            str(mapping),
            str(_SANDBOX_PUBLIC / "artifacts" / "mapping_library.json"),
            "--ro-bind",
            str(questions),
            str(_SANDBOX_PUBLIC / "artifacts" / "question_bank.json"),
        )
    )
    if model_b is not None:
        command.extend(
            (
                "--ro-bind",
                str(model_b),
                str(_SANDBOX_PUBLIC / "artifacts" / "model_b.json"),
            )
        )
    for ephemeris in ephemeris_files:
        command.extend(
            (
                "--ro-bind",
                str(ephemeris),
                str(_SANDBOX_PUBLIC / "ephemeris" / ephemeris.name),
            )
        )
    command.extend(("--chmod", "0555", str(_SANDBOX_PUBLIC / "ephemeris")))
    if cache_files:
        command.extend(("--dir", str(_SANDBOX_PUBLIC / "candidate_cache")))
        for cache in cache_files:
            command.extend(
                (
                    "--ro-bind",
                    str(cache),
                    str(_SANDBOX_PUBLIC / "candidate_cache" / cache.name),
                )
            )
        command.extend(("--chmod", "0555", str(_SANDBOX_PUBLIC / "candidate_cache")))
    command.extend(
        (
            "--bind",
            str(output),
            str(_SANDBOX_OUTPUT),
            "--setenv",
            "HDMATCH_ISOLATED_SOURCE_COMMIT",
            provenance.commit,
            "--setenv",
            "HDMATCH_ISOLATED_SOURCE_TREE",
            provenance.tree,
            "--setenv",
            "HDMATCH_ISOLATED_SOURCE_ROOT",
            str(_SANDBOX_ROOT),
            "--chdir",
            str(_SANDBOX_ROOT),
            sandbox_python,
            "-B",
            "-m",
            "hdmatch.cli",
            "recover",
            "--run-dir",
            str(_SANDBOX_OUTPUT),
            "--blind-file",
            str(_SANDBOX_PUBLIC / "blind_cases.json"),
            "--ephemeris",
            str(_SANDBOX_PUBLIC / "ephemeris"),
            "--mapping",
            str(_SANDBOX_PUBLIC / "artifacts" / "mapping_library.json"),
            "--model",
            request.model_id,
            "--cache-dir",
            str(
                _SANDBOX_PUBLIC / "candidate_cache"
                if cache_files
                else _SANDBOX_OUTPUT / "candidate_cache"
            ),
            "--workers",
            str(request.workers),
            "--aggregation",
            request.aggregation,
            "--threshold",
            str(request.threshold_rubric_bits),
        )
    )
    if model_b is not None:
        command.extend(
            (
                "--model-b-artifact",
                str(_SANDBOX_PUBLIC / "artifacts" / "model_b.json"),
            )
        )
    return RecoveryMountPlan(
        command=tuple(command),
        ephemeris_files=ephemeris_files,
        candidate_cache_files=cache_files,
    )


def _artifact_hashes(files: Sequence[Path]) -> dict[str, str]:
    return {path.name: sha256_file(path) for path in sorted(files)}


def run_claim_grade_recovery(
    request: RecoveryBoundaryRequest,
    *,
    repository_root: Path,
) -> Path:
    """Run exact recovery with evaluator-secret mounts structurally absent."""

    bwrap = _require_bubblewrap()
    provenance = _source_provenance(repository_root)
    output = _prepare_output(request.output_dir)
    normalized = replace(request, output_dir=output)
    plan = build_recovery_mount_plan(normalized, provenance=provenance, bwrap=bwrap)
    completed = subprocess.run(plan.command, check=False)
    if completed.returncode != 0:
        raise KeylessIsolationError(
            f"isolated recovery failed with exit status {completed.returncode}; partial public "
            "output was retained"
        )
    manifest = output / "run.manifest.json"
    predictions = output / "predictions.json"
    if not manifest.is_file() or not predictions.is_file():
        raise KeylessIsolationError("isolated recovery did not produce its required artifacts")
    receipt: dict[str, Any] = {
        "schema_version": "keyless-recovery-isolation-receipt-v1",
        "isolation_runtime": _bubblewrap_identity(bwrap),
        "runtime_controls": {
            "network_namespace": "unshared",
            "user_namespace": "unshared-uid-gid-65534",
            "nested_user_namespaces": "disabled",
            "capabilities": "all-dropped",
            "environment": "cleared-allowlist-only",
            "tracked_decoder_source": "read-only-individual-files",
            "python_environment": "read-only-dedicated-mount",
            "public_inputs": "read-only-individual-files",
            "run_output": "single-read-write-mount",
            "evaluator_secret_mounts": "absent",
            "reveal_or_key_cli_surface": False,
        },
        "mount_contract": {
            "tracked_decoder_source": "read-only",
            "python_environment": "read-only",
            "blind_input": "read-only-single-file",
            "mapping_artifact": "read-only-single-file",
            "question_bank_artifact": "read-only-single-file",
            "model_b_artifact": (
                "read-only-single-file" if request.model_b_artifact is not None else "absent"
            ),
            "ephemeris": "read-only-declared-se1-files",
            "candidate_cache": (
                "read-only-declared-month-files" if plan.candidate_cache_files else "absent"
            ),
            "run_output": "read-write-single-directory",
            "host_parent_directories": "absent",
            "evaluator_key_plaintext_envelope": "absent",
        },
        "command_contract": {
            "entrypoint": "python -m hdmatch.cli recover",
            "workers": request.workers,
            "aggregation": request.aggregation,
            "threshold_rubric_bits": request.threshold_rubric_bits,
            "exit_status": completed.returncode,
            "key_or_reveal_arguments": False,
        },
        "software_commit": provenance.commit,
        "software_tree": provenance.tree,
        "model_id": request.model_id,
        "blind_input_sha256": sha256_file(request.blind_file),
        "mapping_sha256": sha256_file(request.mapping_file),
        "question_bank_sha256": sha256_file(request.question_bank_file),
        "model_b_artifact_sha256": (
            sha256_file(request.model_b_artifact)
            if request.model_b_artifact is not None
            else None
        ),
        "ephemeris_sha256": _artifact_hashes(plan.ephemeris_files),
        "candidate_cache_sha256": _artifact_hashes(plan.candidate_cache_files),
        "run_manifest_sha256": sha256_file(manifest),
        "prediction_sha256": sha256_file(predictions),
        "created_at_utc": datetime.now(UTC),
        "claim_boundary": (
            "OS-isolated synthetic engineering recovery only; this does not validate "
            "Human Design in humans"
        ),
    }
    destination = output / _RECEIPT_NAME
    write_new_canonical_json(destination, receipt)
    return destination


def build_isolation_harness_command(
    *,
    public_input: Path,
    output_dir: Path,
    denied_host_path: Path,
    python_environment: Path,
    provenance: SourceProvenance,
    bwrap: str,
) -> tuple[str, ...]:
    """Build the deterministic OS-boundary harness command used by tests only."""

    public = public_input.expanduser().resolve(strict=True)
    output = output_dir.expanduser().resolve(strict=True)
    denied = denied_host_path.expanduser().resolve(strict=True)
    runtime = python_environment.expanduser().resolve(strict=True)
    sandbox_python = _runtime_python(runtime)
    command = _bwrap_base(bwrap)
    _mount_tracked_source(command, provenance)
    if runtime != Path("/usr"):
        command.extend(
            ("--dir", str(_SANDBOX_RUNTIME), "--ro-bind", str(runtime), str(_SANDBOX_RUNTIME))
        )
    command.extend(
        (
            "--dir",
            str(_SANDBOX_PUBLIC),
            "--ro-bind",
            str(public),
            str(_SANDBOX_PUBLIC / "harness-input"),
            "--bind",
            str(output),
            str(_SANDBOX_OUTPUT),
            "--chdir",
            str(_SANDBOX_ROOT),
            sandbox_python,
            "-B",
            "-m",
            "hdmatch.runtime.isolation_probe",
            "--public-input",
            str(_SANDBOX_PUBLIC / "harness-input"),
            "--denied-host-path",
            str(denied),
            "--output",
            str(_SANDBOX_OUTPUT / "isolation-harness.json"),
        )
    )
    return tuple(command)


def run_isolation_harness(
    *,
    public_input: Path,
    output_dir: Path,
    denied_host_path: Path,
    python_environment: Path,
    repository_root: Path,
) -> Path:
    """Exercise the real namespace/mount boundary without chart scoring."""

    bwrap = _require_bubblewrap()
    provenance = _source_provenance(repository_root)
    output = _prepare_output(output_dir)
    command = build_isolation_harness_command(
        public_input=public_input,
        output_dir=output,
        denied_host_path=denied_host_path,
        python_environment=python_environment,
        provenance=provenance,
        bwrap=bwrap,
    )
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise KeylessIsolationError(
            f"isolation harness failed with exit status {completed.returncode}"
        )
    receipt = output / "isolation-harness.json"
    if not receipt.is_file():
        raise KeylessIsolationError("isolation harness did not produce its receipt")
    return receipt


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run-keyless-recovery",
        description=(
            "Run blind recovery inside a fail-closed Bubblewrap sandbox. This command "
            "has no answer-key, encrypted-envelope, decrypt, or reveal option."
        ),
    )
    parser.add_argument("--blind-file", required=True, type=Path)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--ephemeris", required=True, type=Path)
    parser.add_argument("--mapping", required=True, type=Path)
    parser.add_argument("--question-bank", required=True, type=Path)
    parser.add_argument("--python-environment", type=Path, default=Path(sys.prefix))
    parser.add_argument("--model", choices=(MODEL_A_ID, MODEL_B_ID), default=MODEL_A_ID)
    parser.add_argument("--model-b-artifact", type=Path)
    parser.add_argument("--candidate-cache", type=Path)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--aggregation",
        choices=tuple(item.value for item in AggregationMode),
        default=AggregationMode.DURATION_WEIGHTED_EVIDENCE.value,
    )
    parser.add_argument("--threshold", type=float, default=0.0)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    repository_root = Path(__file__).resolve().parents[3]
    request = RecoveryBoundaryRequest(
        blind_file=args.blind_file,
        output_dir=args.run_dir,
        ephemeris_path=args.ephemeris,
        mapping_file=args.mapping,
        question_bank_file=args.question_bank,
        python_environment=args.python_environment,
        model_id=str(args.model),
        model_b_artifact=args.model_b_artifact,
        candidate_cache=args.candidate_cache,
        workers=int(args.workers),
        aggregation=str(args.aggregation),
        threshold_rubric_bits=float(args.threshold),
    )
    try:
        receipt = run_claim_grade_recovery(request, repository_root=repository_root)
    except (FileNotFoundError, KeylessIsolationError, PermissionError, ValueError) as exc:
        print(f"run-keyless-recovery: error: {exc}", file=sys.stderr)
        return 2
    print("claim-grade keyless recovery completed")
    print(f"isolation receipt sha256: {sha256_file(receipt)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
