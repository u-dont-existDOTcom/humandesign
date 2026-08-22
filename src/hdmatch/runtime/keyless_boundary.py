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

from hdmatch.evaluation.behavioral_difference import (
    VerifiedBehavioralDifferenceBinding,
    load_behavioral_difference_audit,
    verify_behavioral_difference_audit,
)
from hdmatch.evaluation.leakage import assert_no_blind_leakage
from hdmatch.experiments.canonical import (
    load_json_bytes,
    sha256_file,
    write_new_canonical_json,
)
from hdmatch.experiments.manifest import create_run_manifest, write_run_manifest
from hdmatch.experiments.paired import (
    load_paired_experiment_plan,
    verify_paired_generation_receipt_binding,
)
from hdmatch.model_b_v2_new import FrozenModelBV2New
from hdmatch.runtime.chart_adapter import ExactChartAdapter, declared_ephemeris_files
from hdmatch.runtime.symbolic_adapter import (
    MODEL_A_ID,
    MODEL_B_ID,
    MODEL_B_V2_NEW_ID,
    FrozenSymbolicModel,
    load_runtime_model,
)
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
    model_b_v2_compiled: Path | None = None
    model_b_v2_freeze: Path | None = None
    model_b_v2_difference_audit: Path | None = None
    model_b_v2_difference_cache: Path | None = None
    paired_plan: Path | None = None
    paired_public_config: Path | None = None
    paired_generation_receipt: Path | None = None
    paired_generation_binding: Path | None = None
    paired_arm_id: str | None = None
    candidate_cache: Path | None = None
    workers: int = 1
    aggregation: str = AggregationMode.DURATION_WEIGHTED_EVIDENCE.value
    threshold_rubric_bits: float = 0.0


@dataclass(frozen=True, slots=True)
class RecoveryMountPlan:
    command: tuple[str, ...]
    ephemeris_files: tuple[Path, ...]
    candidate_cache_files: tuple[Path, ...]


def _paired_request_paths(
    request: RecoveryBoundaryRequest,
) -> tuple[Path, Path, Path, Path, str] | None:
    values = (
        request.paired_plan,
        request.paired_public_config,
        request.paired_generation_receipt,
        request.paired_generation_binding,
        request.paired_arm_id,
    )
    if not any(value is not None for value in values):
        return None
    if not all(value is not None for value in values):
        raise KeylessIsolationError(
            "paired recovery requires plan, public config, generation receipt, "
            "generation binding, and arm ID"
        )
    plan, config, generation, binding, arm_id = values
    assert isinstance(plan, Path)
    assert isinstance(config, Path)
    assert isinstance(generation, Path)
    assert isinstance(binding, Path)
    assert isinstance(arm_id, str)
    return (
        plan.expanduser().resolve(strict=True),
        config.expanduser().resolve(strict=True),
        generation.expanduser().resolve(strict=True),
        binding.expanduser().resolve(strict=True),
        arm_id,
    )


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
        Path(line) for line in _run_git(root, "ls-files", "--", "src/hdmatch").splitlines() if line
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


def _require_current_python_environment(python_environment: Path) -> Path:
    requested = python_environment.expanduser().resolve(strict=True)
    current = Path(sys.prefix).resolve(strict=True)
    if requested != current:
        raise KeylessIsolationError(
            "the mounted child Python environment must equal the wrapper environment"
        )
    return requested


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


def _verify_v2_difference_request(
    request: RecoveryBoundaryRequest,
    *,
    expected_binding: VerifiedBehavioralDifferenceBinding | None = None,
) -> VerifiedBehavioralDifferenceBinding:
    if (
        request.model_b_v2_compiled is None
        or request.model_b_v2_freeze is None
        or request.model_b_v2_difference_audit is None
        or request.model_b_v2_difference_cache is None
        or request.candidate_cache is None
    ):
        raise KeylessIsolationError(
            "MODEL-B-DETAILED-V2-NEW requires compiled, freeze, difference-audit, "
            "audited-cache artifacts, and the retained candidate-cache directory"
        )
    model_a = load_runtime_model(
        MODEL_A_ID,
        model_a_mapping_path=request.mapping_file,
    )
    model_b = load_runtime_model(
        MODEL_B_V2_NEW_ID,
        model_a_mapping_path=request.mapping_file,
        model_b_v2_compiled_path=request.model_b_v2_compiled,
        model_b_v2_freeze_path=request.model_b_v2_freeze,
    )
    if not isinstance(model_a, FrozenSymbolicModel) or not isinstance(model_b, FrozenModelBV2New):
        raise KeylessIsolationError("V2 difference verification loaded incompatible models")
    audit = load_behavioral_difference_audit(request.model_b_v2_difference_audit)
    engine = ExactChartAdapter(request.ephemeris_path)
    binding = verify_behavioral_difference_audit(
        request.model_b_v2_difference_audit,
        model_a=model_a,
        model_b=model_b,
        candidate_cache_path=request.model_b_v2_difference_cache,
        candidate_request=audit.candidate_universe_request.to_runtime(),
        engine_fingerprint=engine.fingerprint,
        expected_binding=expected_binding,
    )
    if binding.audited_at_utc < model_b.freeze_receipt.frozen_at_utc:
        raise KeylessIsolationError("V2 difference audit must follow the model freeze")
    return binding


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

    if request.model_id not in {MODEL_A_ID, MODEL_B_ID, MODEL_B_V2_NEW_ID}:
        raise KeylessIsolationError("unsupported symbolic model identity")
    if request.model_id == MODEL_B_ID and request.model_b_artifact is None:
        raise KeylessIsolationError("Model B requires its frozen artifact")
    if request.model_id == MODEL_B_V2_NEW_ID and (
        request.model_b_v2_compiled is None
        or request.model_b_v2_freeze is None
        or request.model_b_v2_difference_audit is None
        or request.model_b_v2_difference_cache is None
    ):
        raise KeylessIsolationError(
            "MODEL-B-DETAILED-V2-NEW requires compiled, freeze, difference-audit, "
            "and audited-cache artifacts"
        )
    if request.model_id != MODEL_B_V2_NEW_ID and (
        request.model_b_v2_difference_audit is not None
        or request.model_b_v2_difference_cache is not None
    ):
        raise KeylessIsolationError(
            "behavioral-difference inputs are only valid for MODEL-B-DETAILED-V2-NEW"
        )
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
    model_b_v2_compiled = (
        request.model_b_v2_compiled.expanduser().resolve(strict=True)
        if request.model_b_v2_compiled is not None
        else None
    )
    model_b_v2_freeze = (
        request.model_b_v2_freeze.expanduser().resolve(strict=True)
        if request.model_b_v2_freeze is not None
        else None
    )
    model_b_v2_difference_audit = (
        request.model_b_v2_difference_audit.expanduser().resolve(strict=True)
        if request.model_b_v2_difference_audit is not None
        else None
    )
    model_b_v2_difference_cache = (
        request.model_b_v2_difference_cache.expanduser().resolve(strict=True)
        if request.model_b_v2_difference_cache is not None
        else None
    )
    paired = _paired_request_paths(request)
    for artifact in (blind, mapping, questions):
        if not artifact.is_file():
            raise KeylessIsolationError("a required public recovery artifact is missing")
    if model_b is not None and not model_b.is_file():
        raise KeylessIsolationError("the frozen Model B artifact is missing")
    if model_b_v2_compiled is not None and not model_b_v2_compiled.is_file():
        raise KeylessIsolationError("the compiled Model B V2 artifact is missing")
    if model_b_v2_freeze is not None and not model_b_v2_freeze.is_file():
        raise KeylessIsolationError("the Model B V2 freeze receipt is missing")
    if model_b_v2_difference_audit is not None and not model_b_v2_difference_audit.is_file():
        raise KeylessIsolationError("the Model B V2 difference audit is missing")
    if model_b_v2_difference_cache is not None and not model_b_v2_difference_cache.is_file():
        raise KeylessIsolationError("the Model B V2 audited cache is missing")
    if paired is not None and any(not path.is_file() for path in paired[:4]):
        raise KeylessIsolationError("a required paired public artifact is missing")
    _verify_question_binding(mapping, questions)
    assert_no_blind_leakage(blind)
    assert_no_plaintext_answer_keys_in_paths(
        (
            blind,
            mapping,
            questions,
            output,
            *((model_b_v2_compiled,) if model_b_v2_compiled is not None else ()),
            *((model_b_v2_freeze,) if model_b_v2_freeze is not None else ()),
            *((model_b_v2_difference_audit,) if model_b_v2_difference_audit is not None else ()),
            *((model_b_v2_difference_cache,) if model_b_v2_difference_cache is not None else ()),
            *(paired[:4] if paired is not None else ()),
        )
    )

    if request.model_id == MODEL_B_V2_NEW_ID:
        _verify_v2_difference_request(request)

    ephemeris_files = _ephemeris_files(request.ephemeris_path)
    cache_files = _candidate_cache_files(request.candidate_cache)
    if model_b_v2_difference_cache is not None and model_b_v2_difference_cache not in cache_files:
        raise KeylessIsolationError(
            "the V2 audited cache must be present in the retained candidate-cache directory"
        )
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
    if paired is not None:
        paired_plan, paired_config, paired_generation, paired_binding, _ = paired
        command.extend(
            (
                "--ro-bind",
                str(paired_plan),
                str(_SANDBOX_PUBLIC / "artifacts" / "paired_plan.json"),
                "--ro-bind",
                str(paired_config),
                str(_SANDBOX_PUBLIC / "artifacts" / "paired_config.yaml"),
                "--ro-bind",
                str(paired_generation),
                str(_SANDBOX_PUBLIC / "artifacts" / "paired_generation.receipt.json"),
                "--ro-bind",
                str(paired_binding),
                str(_SANDBOX_PUBLIC / "artifacts" / "paired_generation.binding.json"),
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
    if model_b_v2_compiled is not None and model_b_v2_freeze is not None:
        assert model_b_v2_difference_cache is not None
        command.extend(
            (
                "--ro-bind",
                str(model_b_v2_compiled),
                str(_SANDBOX_PUBLIC / "artifacts" / "model_b_v2_compiled.json"),
                "--ro-bind",
                str(model_b_v2_freeze),
                str(_SANDBOX_PUBLIC / "artifacts" / "model_b_v2_freeze.json"),
            )
        )
    if model_b_v2_difference_audit is not None and model_b_v2_difference_cache is not None:
        command.extend(
            (
                "--ro-bind",
                str(model_b_v2_difference_audit),
                str(_SANDBOX_PUBLIC / "artifacts" / "model_b_v2_difference_audit.json"),
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
    if model_b_v2_compiled is not None and model_b_v2_freeze is not None:
        assert model_b_v2_difference_cache is not None
        command.extend(
            (
                "--model-b-v2-compiled",
                str(_SANDBOX_PUBLIC / "artifacts" / "model_b_v2_compiled.json"),
                "--model-b-v2-freeze",
                str(_SANDBOX_PUBLIC / "artifacts" / "model_b_v2_freeze.json"),
                "--model-b-v2-difference-audit",
                str(_SANDBOX_PUBLIC / "artifacts" / "model_b_v2_difference_audit.json"),
                "--model-b-v2-difference-cache",
                str(_SANDBOX_PUBLIC / "candidate_cache" / model_b_v2_difference_cache.name),
            )
        )
    if paired is not None:
        command.extend(
            (
                "--paired-plan",
                str(_SANDBOX_PUBLIC / "artifacts" / "paired_plan.json"),
                "--paired-public-config",
                str(_SANDBOX_PUBLIC / "artifacts" / "paired_config.yaml"),
                "--paired-generation-receipt",
                str(_SANDBOX_PUBLIC / "artifacts" / "paired_generation.receipt.json"),
                "--paired-generation-binding",
                str(_SANDBOX_PUBLIC / "artifacts" / "paired_generation.binding.json"),
                "--paired-arm-id",
                paired[4],
            )
        )
    return RecoveryMountPlan(
        command=tuple(command),
        ephemeris_files=ephemeris_files,
        candidate_cache_files=cache_files,
    )


def _artifact_hashes(files: Sequence[Path]) -> dict[str, str]:
    return {path.name: sha256_file(path) for path in sorted(files)}


def _precreate_public_manifest(
    request: RecoveryBoundaryRequest,
    *,
    output: Path,
    repository_root: Path,
    provenance: SourceProvenance,
) -> Path:
    """Create the public manifest before isolation; the child only verifies/resumes it."""

    blind = load_json_bytes(request.blind_file, require_canonical=True)
    if not isinstance(blind, dict):
        raise KeylessIsolationError("blind input must contain an object")
    model = load_runtime_model(
        request.model_id,
        model_a_mapping_path=request.mapping_file,
        model_b_artifact_path=request.model_b_artifact,
        model_b_v2_compiled_path=request.model_b_v2_compiled,
        model_b_v2_freeze_path=request.model_b_v2_freeze,
    )
    difference_gate: VerifiedBehavioralDifferenceBinding | None = None
    if isinstance(model, FrozenModelBV2New):
        try:
            expected_gate = VerifiedBehavioralDifferenceBinding.model_validate(
                blind.get("model_b_v2_difference_gate")
            )
        except ValueError as exc:
            raise KeylessIsolationError(
                "V2 blind input lacks a valid behavioral-difference binding"
            ) from exc
        difference_gate = _verify_v2_difference_request(
            request,
            expected_binding=expected_gate,
        )
    paired = _paired_request_paths(request)
    paired_manifest_binding: dict[str, Any] | None = None
    if paired is not None:
        plan_path, config_path, generation_path, binding_path, arm_id = paired
        paired_plan = load_paired_experiment_plan(plan_path)
        paired_receipt = verify_paired_generation_receipt_binding(
            binding_path,
            plan_path=plan_path,
            public_config_path=config_path,
            generation_receipt_path=generation_path,
            expected_arm_id=arm_id,
        )
        arm = paired_plan.arm(arm_id)
        if (
            arm.model_id != model.model_id
            or arm.model_sha256 != model.model_sha256
            or arm.mapping_sha256 != model.mapping_sha256
            or arm.question_bank_sha256 != model.question_bank_sha256
        ):
            raise KeylessIsolationError("recovery runtime does not match the paired arm")
        if paired_receipt.blind_input_sha256 != sha256_file(request.blind_file):
            raise KeylessIsolationError("blind input does not match the paired generation binding")
        if isinstance(model, FrozenModelBV2New) and (
            difference_gate is None or difference_gate != paired_plan.verified_v2_audit
        ):
            raise KeylessIsolationError("V2 recovery gate does not match the paired plan")
        paired_manifest_binding = {
            "schema_version": "paired-recovery-binding-v1",
            "paired_experiment_id": paired_plan.paired_experiment_id,
            "paired_plan_file_sha256": sha256_file(plan_path),
            "paired_plan_semantic_sha256": paired_plan.plan_sha256,
            "paired_generation_receipt_sha256": sha256_file(generation_path),
            "paired_generation_binding_sha256": sha256_file(binding_path),
            "public_config_file_sha256": sha256_file(config_path),
            "public_config_semantic_sha256": paired_plan.public_config.semantic_sha256,
            "generation_seed_commitment_sha256": (paired_plan.generation_seed_commitment_sha256),
            "arm_id": arm.arm_id,
            "arm_role": arm.role,
        }
    input_hashes = {
        "blind_cases.json": sha256_file(request.blind_file),
        "model_a_mapping_library": sha256_file(request.mapping_file),
    }
    if paired is not None:
        input_hashes.update(
            {
                "paired_experiment_plan": sha256_file(paired[0]),
                "paired_public_config": sha256_file(paired[1]),
                "paired_generation_receipt": sha256_file(paired[2]),
                "paired_generation_binding": sha256_file(paired[3]),
            }
        )
    if model.model_id == MODEL_B_ID:
        assert request.model_b_artifact is not None
        input_hashes["model_b_artifact"] = sha256_file(request.model_b_artifact)
    if model.model_id == MODEL_B_V2_NEW_ID:
        assert request.model_b_v2_compiled is not None
        assert request.model_b_v2_freeze is not None
        input_hashes["model_b_v2_compiled_artifact"] = sha256_file(request.model_b_v2_compiled)
        input_hashes["model_b_v2_freeze_receipt"] = sha256_file(request.model_b_v2_freeze)
        assert difference_gate is not None
        input_hashes.update(
            {
                "model_b_v2_difference_audit": difference_gate.audit_file_sha256,
                "model_b_v2_difference_cache": (difference_gate.candidate_cache_file_sha256),
                "model_b_v2_model_semantic": difference_gate.model_b_sha256,
                "model_b_v2_question_bank": difference_gate.question_bank_sha256,
                "model_b_v2_difference_candidate_universe": (
                    difference_gate.candidate_universe_sha256
                ),
            }
        )
    for ephemeris in declared_ephemeris_files(request.ephemeris_path):
        input_hashes[f"ephemeris:{ephemeris.name}"] = sha256_file(ephemeris)
    public_seed = int(input_hashes["blind_cases.json"][:16], 16)
    config: dict[str, Any] = {
        "aggregation": request.aggregation,
        "threshold_rubric_bits": request.threshold_rubric_bits,
        "workers": request.workers,
        "cache_policy": "hash-bound exact month universes",
    }
    if difference_gate is not None:
        config["model_b_v2_difference_gate"] = difference_gate.model_dump(mode="json")
    if paired_manifest_binding is not None:
        config["paired_experiment"] = paired_manifest_binding
    manifest = create_run_manifest(
        experiment_id=str(blind["experiment_id"]),
        seed=public_seed,
        repository_root=repository_root,
        candidate_universe=str(blind["candidate_universe"]),
        aggregation_rule=request.aggregation,
        model_id=model.model_id,
        input_hashes=input_hashes,
        config=config,
        declared_outputs=("predictions.json", "prediction.freeze.json"),
    )
    if (
        isinstance(model, FrozenModelBV2New)
        and model.freeze_receipt.frozen_at_utc > manifest.created_at_utc
    ):
        raise KeylessIsolationError("V2 model freeze must predate the recovery manifest")
    if difference_gate is not None and difference_gate.audited_at_utc > manifest.created_at_utc:
        raise KeylessIsolationError(
            "V2 behavioral-difference audit must predate the recovery manifest"
        )
    if manifest.software_commit != provenance.commit or manifest.software_dirty:
        raise KeylessIsolationError("public manifest source provenance is not the clean checkout")
    destination = output / "run.manifest.json"
    write_run_manifest(manifest, destination)
    return destination


def run_claim_grade_recovery(
    request: RecoveryBoundaryRequest,
    *,
    repository_root: Path,
) -> Path:
    """Run exact recovery with evaluator-secret mounts structurally absent."""

    _require_current_python_environment(request.python_environment)
    bwrap = _require_bubblewrap()
    provenance = _source_provenance(repository_root)
    output = _prepare_output(request.output_dir)
    normalized = replace(request, output_dir=output)
    plan = build_recovery_mount_plan(normalized, provenance=provenance, bwrap=bwrap)
    _precreate_public_manifest(
        normalized,
        output=output,
        repository_root=provenance.repository_root,
        provenance=provenance,
    )
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
    public_copies = [(normalized.blind_file, output / "blind_cases.json")]
    if normalized.paired_generation_receipt is not None:
        if normalized.paired_generation_binding is None:
            raise KeylessIsolationError("paired generation binding is missing")
        public_copies.extend(
            (
                (
                    normalized.paired_generation_receipt,
                    output / "generation.receipt.json",
                ),
                (
                    normalized.paired_generation_binding,
                    output / "paired-generation.binding.json",
                ),
            )
        )
    for source, destination in public_copies:
        if source is None or destination.exists():
            raise KeylessIsolationError("public recovery artifact staging is inconsistent")
        shutil.copyfile(source, destination)
    difference_gate = (
        _verify_v2_difference_request(normalized) if request.model_id == MODEL_B_V2_NEW_ID else None
    )
    paired = _paired_request_paths(normalized)
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
            "model_b_v2_compiled_artifact": (
                "read-only-single-file" if request.model_b_v2_compiled is not None else "absent"
            ),
            "model_b_v2_freeze_receipt": (
                "read-only-single-file" if request.model_b_v2_freeze is not None else "absent"
            ),
            "model_b_v2_difference_audit": (
                "read-only-single-file"
                if request.model_b_v2_difference_audit is not None
                else "absent"
            ),
            "model_b_v2_difference_cache": (
                "read-only-single-file"
                if request.model_b_v2_difference_cache is not None
                else "absent"
            ),
            "paired_plan": "read-only-single-file" if paired is not None else "absent",
            "paired_public_config": ("read-only-single-file" if paired is not None else "absent"),
            "paired_generation_receipt": (
                "read-only-single-file" if paired is not None else "absent"
            ),
            "paired_generation_binding": (
                "read-only-single-file" if paired is not None else "absent"
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
            sha256_file(request.model_b_artifact) if request.model_b_artifact is not None else None
        ),
        "model_b_v2_compiled_sha256": (
            sha256_file(request.model_b_v2_compiled)
            if request.model_b_v2_compiled is not None
            else None
        ),
        "model_b_v2_freeze_sha256": (
            sha256_file(request.model_b_v2_freeze)
            if request.model_b_v2_freeze is not None
            else None
        ),
        "model_b_v2_difference_audit_sha256": (
            sha256_file(request.model_b_v2_difference_audit)
            if request.model_b_v2_difference_audit is not None
            else None
        ),
        "model_b_v2_difference_cache_sha256": (
            sha256_file(request.model_b_v2_difference_cache)
            if request.model_b_v2_difference_cache is not None
            else None
        ),
        "paired_plan_sha256": sha256_file(paired[0]) if paired is not None else None,
        "paired_public_config_sha256": (sha256_file(paired[1]) if paired is not None else None),
        "paired_generation_receipt_sha256": (
            sha256_file(paired[2]) if paired is not None else None
        ),
        "paired_generation_binding_sha256": (
            sha256_file(paired[3]) if paired is not None else None
        ),
        "paired_arm_id": paired[4] if paired is not None else None,
        "model_b_v2_difference_gate": (
            difference_gate.model_dump(mode="json") if difference_gate is not None else None
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
    parser.add_argument(
        "--model",
        choices=(MODEL_A_ID, MODEL_B_ID, MODEL_B_V2_NEW_ID),
        default=MODEL_A_ID,
    )
    parser.add_argument("--model-b-artifact", type=Path)
    parser.add_argument("--model-b-v2-compiled", type=Path)
    parser.add_argument("--model-b-v2-freeze", type=Path)
    parser.add_argument("--model-b-v2-difference-audit", type=Path)
    parser.add_argument("--model-b-v2-difference-cache", type=Path)
    parser.add_argument("--paired-plan", type=Path)
    parser.add_argument("--paired-public-config", type=Path)
    parser.add_argument("--paired-generation-receipt", type=Path)
    parser.add_argument("--paired-generation-binding", type=Path)
    parser.add_argument("--paired-arm-id")
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
        model_b_v2_compiled=args.model_b_v2_compiled,
        model_b_v2_freeze=args.model_b_v2_freeze,
        model_b_v2_difference_audit=args.model_b_v2_difference_audit,
        model_b_v2_difference_cache=args.model_b_v2_difference_cache,
        paired_plan=args.paired_plan,
        paired_public_config=args.paired_public_config,
        paired_generation_receipt=args.paired_generation_receipt,
        paired_generation_binding=args.paired_generation_binding,
        paired_arm_id=args.paired_arm_id,
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
