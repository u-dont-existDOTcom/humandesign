"""Build checkpoint-4 operational diagnostics and changed-file lint evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.util import canonical_json_bytes, sha256_json

REVIEWED_CHECKPOINT3_HEAD = "8cc97025f1e30c52a156e3c7bb5068baf5aea39b"
CHECKPOINT4_EVALUATED_HEAD = "90220a3d67e847d883b2060fa3578fe5026cc414"
PHASE0_CLOSURE_HEAD = "50118dc5d15f5a1e5ecff4a4bfa60cd2646d4455"
REPLAY_SOURCE = "1c59b8aae3c096c84a8116d49c0cb0525029837e"
REPLAY_ARTIFACT_COMMIT = "c79202f2604a6a99612c1dc267ce6e1753b17e27"

IDENTITY_PATH = "state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json"
REPLAY_ROOT = "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1"
INDEX_PATH = f"{REPLAY_ROOT}/index.json"
RUFF_VERSION = "ruff 0.16.4"

# One-time observation of the original ext4 files written by the local real-engine replay.
# Git does not preserve these timestamps; their limitations are explicit in the artifact.
FILESYSTEM_TIMESTAMPS = {
    f"{REPLAY_ROOT}/receipts/ordinary-and-multiple-dates-2024-01-15.json": {
        "birth_time_utc": "2026-08-30T04:20:25.993468665Z",
        "modification_time_utc": "2026-08-30T04:20:25.994283486Z",
        "status_change_time_utc": "2026-08-30T04:20:26.018468649Z",
    },
    f"{REPLAY_ROOT}/receipts/ordinary-and-multiple-dates-2024-01-16.json": {
        "birth_time_utc": "2026-08-30T04:20:26.018468649Z",
        "modification_time_utc": "2026-08-30T04:20:26.019885629Z",
        "status_change_time_utc": "2026-08-30T04:20:26.049468629Z",
    },
    f"{REPLAY_ROOT}/receipts/leap-day-2024-02-29.json": {
        "birth_time_utc": "2026-08-30T04:23:34.370352088Z",
        "modification_time_utc": "2026-08-30T04:23:34.371505821Z",
        "status_change_time_utc": "2026-08-30T04:23:34.374352086Z",
    },
    f"{REPLAY_ROOT}/receipts/dst-gap-2024-03-10.json": {
        "birth_time_utc": "2026-08-30T04:26:05.064264346Z",
        "modification_time_utc": "2026-08-30T04:26:05.065470774Z",
        "status_change_time_utc": "2026-08-30T04:26:05.067264344Z",
    },
    f"{REPLAY_ROOT}/receipts/dst-fold-2024-11-03.json": {
        "birth_time_utc": "2026-08-30T04:29:18.090157018Z",
        "modification_time_utc": "2026-08-30T04:29:18.091916847Z",
        "status_change_time_utc": "2026-08-30T04:29:18.094157016Z",
    },
    f"{REPLAY_ROOT}/receipts/non-one-hour-dst-2024-04-07.json": {
        "birth_time_utc": "2026-08-30T04:32:31.277053626Z",
        "modification_time_utc": "2026-08-30T04:32:31.277354856Z",
        "status_change_time_utc": "2026-08-30T04:32:31.280053625Z",
    },
    f"{REPLAY_ROOT}/receipts/historical-second-offset-1970-01-01.json": {
        "birth_time_utc": "2026-08-30T04:35:30.999959935Z",
        "modification_time_utc": "2026-08-30T04:35:31.000792056Z",
        "status_change_time_utc": "2026-08-30T04:35:31.002959933Z",
    },
    f"{REPLAY_ROOT}/receipts/non-integer-offset-2024-01-15.json": {
        "birth_time_utc": "2026-08-30T04:39:12.884846521Z",
        "modification_time_utc": "2026-08-30T04:39:12.885417201Z",
        "status_change_time_utc": "2026-08-30T04:39:12.887846519Z",
    },
    f"{REPLAY_ROOT}/receipts/skipped-civil-date-2011-12-30.json": {
        "birth_time_utc": "2026-08-30T04:39:12.927846499Z",
        "modification_time_utc": "2026-08-30T04:39:12.928697188Z",
        "status_change_time_utc": "2026-08-30T04:39:12.929846498Z",
    },
    INDEX_PATH: {
        "birth_time_utc": "2026-08-30T04:39:12.960846482Z",
        "modification_time_utc": "2026-08-30T04:39:12.961399200Z",
        "status_change_time_utc": "2026-08-30T04:39:12.962846481Z",
    },
}


class OperationalEvidenceError(ValueError):
    """Raised when operational evidence no longer satisfies its fixed bindings."""


def _git(root: Path, arguments: list[str], *, text: bool = False) -> bytes | str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, check=True, capture_output=True, text=text
    )
    return cast(bytes | str, result.stdout)


def _git_text(root: Path, arguments: list[str]) -> str:
    output = _git(root, arguments, text=True)
    assert isinstance(output, str)
    return output.strip()


def _git_bytes(root: Path, arguments: list[str]) -> bytes:
    output = _git(root, arguments)
    assert isinstance(output, bytes)
    return output


def _git_file(root: Path, commit: str, path: str) -> bytes:
    return _git_bytes(root, ["show", f"{commit}:{path}"])


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _verify_self_hash(value: dict[str, Any], field: str) -> str:
    unhashed = deepcopy(value)
    embedded = unhashed.pop(field, None)
    computed = sha256_json(unhashed)
    if embedded != computed:
        raise OperationalEvidenceError(f"self-hash mismatch: {field}")
    return computed


def _epoch_nanoseconds(value: str) -> int:
    if not value.endswith("Z") or "." not in value:
        raise OperationalEvidenceError(f"timestamp is not nanosecond UTC: {value}")
    whole, fraction = value[:-1].split(".", 1)
    if len(fraction) != 9 or not fraction.isdigit():
        raise OperationalEvidenceError(f"timestamp fraction is not nine digits: {value}")
    seconds = int(datetime.fromisoformat(whole).replace(tzinfo=UTC).timestamp())
    return seconds * 1_000_000_000 + int(fraction)


def _name_status(root: Path, before: str, after: str) -> list[dict[str, str]]:
    raw = _git_bytes(
        root, ["diff", "--no-renames", "--name-status", "-z", before, after]
    )
    tokens = [token for token in raw.split(b"\0") if token]
    if len(tokens) % 2:
        raise OperationalEvidenceError("incomplete git name-status record")
    return [
        {"status": status.decode("ascii"), "path": path.decode("utf-8")}
        for status, path in zip(tokens[::2], tokens[1::2], strict=True)
    ]


def _lint_scope(root: Path, scope_id: str, before: str, after: str) -> dict[str, Any]:
    changed = _name_status(root, before, after)
    lint_paths = [
        item["path"]
        for item in changed
        if item["status"] != "D" and item["path"].endswith(".py")
    ]
    argv = [".venv/bin/ruff", "check", *lint_paths]
    return {
        "scope_id": scope_id,
        "from_commit": before,
        "from_tree_oid": _git_text(root, ["rev-parse", f"{before}^{{tree}}"]),
        "to_commit": after,
        "to_tree_oid": _git_text(root, ["rev-parse", f"{after}^{{tree}}"]),
        "all_changed_path_count": len(changed),
        "all_changed_paths": changed,
        "all_changed_paths_sha256": sha256_json(changed),
        "lint_path_selection": "ACMR Python paths from git diff --no-renames --name-status",
        "lint_changed_path_count": len(lint_paths),
        "lint_changed_paths": lint_paths,
        "lint_changed_paths_sha256": sha256_json(lint_paths),
        "ruff_argv": argv,
        "ruff_shell_command": shlex.join(argv),
        "ruff_version": RUFF_VERSION,
        "observed_at_clean_head": PHASE0_CLOSURE_HEAD,
        "observed_exit_code": 0,
        "observed_stdout": "All checks passed!",
    }


def _runtime_evidence(root: Path, index: dict[str, Any]) -> dict[str, Any]:
    identity_bytes = _git_file(root, REPLAY_SOURCE, IDENTITY_PATH)
    identity = json.loads(identity_bytes)
    if not isinstance(identity, dict):
        raise OperationalEvidenceError("identity packet is not an object")
    _verify_self_hash(identity, "packet_sha256")
    facts = identity.get("runtime", {}).get("facts")
    runtime_sha = identity.get("runtime", {}).get("sha256")
    if not isinstance(facts, dict) or runtime_sha != sha256_json(facts):
        raise OperationalEvidenceError("identity runtime facts do not match their digest")
    if (
        index.get("engine_identity_file_sha256") != _sha256(identity_bytes)
        or index.get("engine_identity_packet_sha256") != identity.get("packet_sha256")
    ):
        raise OperationalEvidenceError("replay index does not bind the pinned identity packet")
    return {
        "source": "engine identity V4 bound by the replay index",
        "identity_path": IDENTITY_PATH,
        "identity_git_blob_oid": _git_text(
            root, ["rev-parse", f"{REPLAY_SOURCE}:{IDENTITY_PATH}"]
        ),
        "identity_file_sha256": _sha256(identity_bytes),
        "identity_packet_sha256": identity["packet_sha256"],
        "runtime_facts_sha256": runtime_sha,
        "runtime_facts": facts,
        "ephemeris_provider": identity["ephemeris"]["provider_metadata"]["provider"],
        "ephemeris_library_version": identity["ephemeris"]["provider_metadata"][
            "library_version"
        ],
        "timezone_database_version": identity["timezone_database"]["version"],
        "interpretation": (
            "Pinned runtime/engine context, not live process telemetry or a machine benchmark."
        ),
    }


def _durable_write_evidence(root: Path, index: dict[str, Any]) -> dict[str, Any]:
    references = index.get("receipt_hashes")
    if not isinstance(references, list) or len(references) != 9:
        raise OperationalEvidenceError("expected nine replay receipt references")
    receipt_hashes = {
        f"{REPLAY_ROOT}/receipts/{item['receipt_id']}.json": item["receipt_sha256"]
        for item in references
    }
    expected_paths = set(receipt_hashes).union({INDEX_PATH})
    if expected_paths != set(FILESYSTEM_TIMESTAMPS):
        raise OperationalEvidenceError("timestamp observation paths do not match replay files")
    observations: list[dict[str, Any]] = []
    for path, timestamps in FILESYSTEM_TIMESTAMPS.items():
        data = _git_file(root, REPLAY_ARTIFACT_COMMIT, path)
        item: dict[str, Any] = {
            "path": path,
            "kind": "aggregate_index" if path == INDEX_PATH else "fixture_receipt",
            "byte_count": len(data),
            "file_sha256": _sha256(data),
            **timestamps,
        }
        if path == INDEX_PATH:
            item["semantic_self_sha256"] = index["index_sha256"]
        else:
            receipt = json.loads(data)
            if receipt.get("receipt_sha256") != receipt_hashes[path]:
                raise OperationalEvidenceError(f"receipt/index digest mismatch: {path}")
            item["semantic_self_sha256"] = receipt["receipt_sha256"]
        observations.append(item)
    observations.sort(key=lambda item: _epoch_nanoseconds(item["birth_time_utc"]))
    earliest = observations[0]
    final_index = next(item for item in observations if item["path"] == INDEX_PATH)
    inode_birth_span_ns = _epoch_nanoseconds(
        final_index["birth_time_utc"]
    ) - _epoch_nanoseconds(earliest["birth_time_utc"])
    lower_bound_ns = _epoch_nanoseconds(
        final_index["modification_time_utc"]
    ) - _epoch_nanoseconds(
        earliest["status_change_time_utc"]
    )
    if inode_birth_span_ns != 1_126_967_377_817 or lower_bound_ns != 1_126_942_930_551:
        raise OperationalEvidenceError("unexpected durable-write lower-bound span")
    return {
        "classification": "one-time local filesystem metadata observation",
        "capture_command": "stat -c '%n|%s|%w|%y|%z' <nine-receipts> <index>",
        "capture_tool": "GNU coreutils stat 9.4",
        "observed_filesystem_type": "ext4",
        "observations": observations,
        "earliest_durable_receipt_path": earliest["path"],
        "earliest_durable_receipt_birth_time_utc": earliest["birth_time_utc"],
        "earliest_receipt_status_change_time_utc": earliest["status_change_time_utc"],
        "final_index_birth_time_utc": final_index["birth_time_utc"],
        "final_index_modification_time_utc": final_index["modification_time_utc"],
        "observed_inode_birth_span_nanoseconds": inode_birth_span_ns,
        "observable_lower_bound_span_nanoseconds": lower_bound_ns,
        "observable_lower_bound_span_seconds": "1126.942930551",
        "observable_lower_bound_span_iso8601": "PT18M46.942930551S",
        "interpretation": (
            "The conservative lower bound subtracts the earliest receipt status-change time "
            "from the final index modification time. The writer fsyncs file contents before "
            "hard-link publication, so these endpoints avoid treating temporary-inode birth "
            "times as exact publication times."
        ),
        "limits": [
            (
                "This is not end-to-end fixture-generation duration; work before the first "
                "durable receipt is absent."
            ),
            (
                "No process start/stop timestamps, CPU load, memory, scheduler, or per-fixture "
                "execution timers were captured."
            ),
            (
                "Git does not preserve filesystem birth or modification times; a checkout or "
                "copy may replace them."
            ),
            (
                "The writer fsyncs file contents but not the containing directory; this is not "
                "a claim of directory-entry survival across sudden power loss."
            ),
            (
                "The timestamps do not isolate computation from verification, serialization, "
                "filesystem, or orchestration overhead."
            ),
            (
                "The observation is not a benchmark, service-level objective, capacity "
                "estimate, or performance guarantee."
            ),
        ],
    }


def build_operational_evidence(repository_root: Path) -> dict[str, Any]:
    """Build the bounded operational and lint evidence packet."""

    root = repository_root.resolve(strict=True)
    index = json.loads(_git_file(root, REPLAY_ARTIFACT_COMMIT, INDEX_PATH))
    if not isinstance(index, dict):
        raise OperationalEvidenceError("replay index is not an object")
    _verify_self_hash(index, "index_sha256")
    scopes = [
        _lint_scope(
            root,
            "checkpoint4_evaluated_diff",
            REVIEWED_CHECKPOINT3_HEAD,
            CHECKPOINT4_EVALUATED_HEAD,
        ),
        _lint_scope(
            root,
            "phase0_closure_diff",
            CHECKPOINT4_EVALUATED_HEAD,
            PHASE0_CLOSURE_HEAD,
        ),
    ]
    payload: dict[str, Any] = {
        "schema_version": "natal-time-checkpoint4-operational-evidence-v1",
        "classification": {
            "operational_diagnostics_only": True,
            "scientific_identity_input": False,
            "scientific_result_input": False,
            "performance_guarantee": False,
            "deployment_or_railway_observation": False,
        },
        "anchor_commits": {
            "reviewed_checkpoint3_head": REVIEWED_CHECKPOINT3_HEAD,
            "checkpoint4_evaluated_head": CHECKPOINT4_EVALUATED_HEAD,
            "phase0_closure_head": PHASE0_CLOSURE_HEAD,
            "replay_source": REPLAY_SOURCE,
            "replay_artifact_commit": REPLAY_ARTIFACT_COMMIT,
        },
        "replay_index_binding": {
            "path": INDEX_PATH,
            "git_blob_oid": _git_text(
                root, ["rev-parse", f"{REPLAY_ARTIFACT_COMMIT}:{INDEX_PATH}"]
            ),
            "file_sha256": _sha256(_git_file(root, REPLAY_ARTIFACT_COMMIT, INDEX_PATH)),
            "index_sha256": index["index_sha256"],
            "aggregate_sha256": index["aggregate_sha256"],
        },
        "pinned_runtime_context": _runtime_evidence(root, index),
        "durable_write_diagnostics": _durable_write_evidence(root, index),
        "changed_file_lint": {
            "path_scopes": scopes,
            "path_scope_count": len(scopes),
            "ruff_version": RUFF_VERSION,
            "observation_head": PHASE0_CLOSURE_HEAD,
            "observation_tracked_worktree_clean": True,
            "phase1_paths_included": False,
            "phase1_recording_boundary": (
                "Phase-1 changed paths and lint commands are outside this artifact and must "
                "be recorded separately at checkpoint 5."
            ),
            "legacy_repo_wide_baseline": {
                "argv": [
                    ".venv/bin/ruff",
                    "check",
                    "src",
                    "tests",
                    "scripts",
                    "--output-format",
                    "json",
                ],
                "shell_command": (
                    ".venv/bin/ruff check src tests scripts --output-format json"
                ),
                "ruff_version": RUFF_VERSION,
                "observed_at_clean_head": PHASE0_CLOSURE_HEAD,
                "observed_exit_code": 1,
                "observed_violation_count": 1812,
                "interpretation": (
                    "Historical repo-wide debt remains nonzero. Both Git-derived changed-file "
                    "scopes pass independently, so the legacy total cannot hide a changed-path "
                    "lint regression. This records evidence; it does not waive or erase debt."
                ),
            },
        },
        "claim_limits": [
            (
                "No end-to-end replay duration is claimed because no defensible start "
                "timestamp exists."
            ),
            "No per-fixture runtime or throughput is inferred from spacing between durable writes.",
            "No scientific, predictive, relationship, deployment, or Railway conclusion follows.",
            "No future-machine performance or completion-time guarantee is made.",
        ],
    }
    payload["artifact_sha256"] = sha256_json(payload)
    return payload


def validate_operational_evidence(root: Path, payload: dict[str, Any]) -> None:
    _verify_self_hash(payload, "artifact_sha256")
    if payload != build_operational_evidence(root):
        raise OperationalEvidenceError("operational evidence does not reproduce exactly")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("state/NATAL-TIME-CHECKPOINT4-OPERATIONAL-EVIDENCE.json"),
    )
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    root = args.repository_root.resolve(strict=True)
    output = args.output if args.output.is_absolute() else root / args.output
    if args.validate_only:
        value = json.loads(output.read_bytes())
        if not isinstance(value, dict):
            raise OperationalEvidenceError("saved operational evidence is not an object")
        validate_operational_evidence(root, value)
        print("CHECKPOINT4_OPERATIONAL_EVIDENCE_OK")
        return 0
    payload = build_operational_evidence(root)
    write_new_bytes(output, canonical_json_bytes(payload) + b"\n")
    print(f"OPERATIONAL_EVIDENCE_SHA256:{payload['artifact_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
