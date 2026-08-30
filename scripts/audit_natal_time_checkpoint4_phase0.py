"""Generate and validate checkpoint-4 Phase-0 lineage/source attestations."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import subprocess
from collections import deque
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.util import canonical_json_bytes, sha256_json

BASELINE = "b7660b8c9bcf52cbb14bc5442c13a3a8635aad32"
REVIEWED_CHECKPOINT3_HEAD = "8cc97025f1e30c52a156e3c7bb5068baf5aea39b"
CHECKPOINT3_RULING_COMMIT = "5251c6f81c11f132eb227e8c5bffd614d5b06980"
REPLAY_SOURCE = "1c59b8aae3c096c84a8116d49c0cb0525029837e"
EVALUATED_HEAD = "90220a3d67e847d883b2060fa3578fe5026cc414"
EXPECTED_REPLAY_INDEX_SHA256 = (
    "f7ead3c9b3b4eb7102cfff5c74e3de3e261e3f6b8491ccfe8881fbf882b75435"
)
EXPECTED_REPLAY_AGGREGATE_SHA256 = (
    "ee8b4882785bb1102b8f14cd23e0d4cc18416118109b0040b8313f86e6be1665"
)

LINEAGE_SCHEMA = "natal-time-checkpoint4-lineage-attestation-v1"
SOURCE_SCHEMA = "natal-time-replay-affecting-source-manifest-v1"

DIFF_PAIRS = (
    ("baseline_to_evaluated_head", BASELINE, EVALUATED_HEAD),
    (
        "reviewed_checkpoint3_to_ruling_commit",
        REVIEWED_CHECKPOINT3_HEAD,
        CHECKPOINT3_RULING_COMMIT,
    ),
    (
        "ruling_commit_to_replay_source",
        CHECKPOINT3_RULING_COMMIT,
        REPLAY_SOURCE,
    ),
    ("replay_source_to_evaluated_head", REPLAY_SOURCE, EVALUATED_HEAD),
)

PROTECTED_PATHS = (
    "scripts/audit_natal_time_api_trace.py",
    "scripts/audit_natal_time_evidence_matrix.py",
    "scripts/audit_natal_time_foundation.py",
    "scripts/audit_natal_time_real_engine_fixtures.py",
    "scripts/audit_natal_time_real_engine_identity.py",
    "src/hdmatch/api/natal_time_app.py",
    "src/hdmatch/chart/__init__.py",
    "src/hdmatch/chart/astronomy_reference.py",
    "src/hdmatch/chart/bodygraph.py",
    "src/hdmatch/chart/boundaries.py",
    "src/hdmatch/chart/calculator.py",
    "src/hdmatch/chart/design_moment.py",
    "src/hdmatch/chart/ephemeris.py",
    "src/hdmatch/chart/ephemeris_audit.py",
    "src/hdmatch/chart/jpl_ephemeris.py",
    "src/hdmatch/chart/progressions.py",
    "src/hdmatch/chart/rave_mandala.py",
    "src/hdmatch/chart/timezone.py",
    "src/hdmatch/chart/validation.py",
    "src/hdmatch/natal_time/__init__.py",
    "src/hdmatch/natal_time/conformance.py",
    "src/hdmatch/natal_time/enumerator.py",
    "src/hdmatch/natal_time/evidence.py",
    "src/hdmatch/natal_time/models.py",
    "src/hdmatch/natal_time/provenance.py",
    "src/hdmatch/natal_time/public.py",
    "src/hdmatch/natal_time/records.py",
    "src/hdmatch/natal_time/service.py",
    "src/hdmatch/natal_time/store.py",
    "src/hdmatch/natal_time/synthetic.py",
    "src/hdmatch/natal_time/workflow.py",
    "src/hdmatch/runtime/chart_adapter.py",
    "src/hdmatch/schemas/__init__.py",
    "src/hdmatch/schemas/core.py",
    "src/hdmatch/search/__init__.py",
    "src/hdmatch/search/adaptive.py",
    "src/hdmatch/search/candidate_universe.py",
    "src/hdmatch/search/date_aggregator.py",
    "src/hdmatch/util/__init__.py",
    "src/hdmatch/util/canonical.py",
    "state/NATAL-TIME-EVIDENCE-TRANSITION-MATRIX.json",
    "state/NATAL-TIME-FOUNDATION-AUDIT.json",
    "state/NATAL-TIME-REAL-ENGINE-FIXTURES.json",
    "state/NATAL-TIME-REAL-ENGINE-IDENTITY-V2.json",
    "state/NATAL-TIME-REAL-ENGINE-IDENTITY-V3.json",
    "state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json",
    "state/NATAL-TIME-REAL-ENGINE-IDENTITY.json",
    "state/NATAL-TIME-WEEKDAY-LOCK-TRACE.json",
)

IMMUTABLE_JSON_HASH_FIELDS = {
    "state/NATAL-TIME-EVIDENCE-TRANSITION-MATRIX.json": "matrix_sha256",
    "state/NATAL-TIME-FOUNDATION-AUDIT.json": "audit_sha256",
    "state/NATAL-TIME-REAL-ENGINE-FIXTURES.json": "audit_sha256",
    "state/NATAL-TIME-REAL-ENGINE-IDENTITY-V2.json": "packet_sha256",
    "state/NATAL-TIME-REAL-ENGINE-IDENTITY-V3.json": "packet_sha256",
    "state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json": "packet_sha256",
    "state/NATAL-TIME-REAL-ENGINE-IDENTITY.json": "packet_sha256",
    "state/NATAL-TIME-WEEKDAY-LOCK-TRACE.json": "trace_sha256",
}

REPLAY_ENTRY_PATHS = ("scripts/replay_natal_time_real_engine_fixtures.py",)
REPLAY_NON_PYTHON_INPUTS = (
    "pyproject.toml",
    "requirements-dev.lock",
    "state/NATAL-TIME-REAL-ENGINE-FIXTURES.json",
    "state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json",
)

REPLAY_REQUIRED_SURFACE_COVERAGE = {
    "replay_orchestration": (
        "scripts/replay_natal_time_real_engine_fixtures.py",
        "src/hdmatch/natal_time/replay.py",
    ),
    "receipt_schemas_and_canonicalization": (
        "src/hdmatch/natal_time/replay.py",
        "src/hdmatch/util/canonical.py",
    ),
    "source_integrity_checks": ("src/hdmatch/natal_time/replay.py",),
    "fixture_definitions": (
        "scripts/audit_natal_time_real_engine_fixtures.py",
        "state/NATAL-TIME-REAL-ENGINE-FIXTURES.json",
    ),
    "engine_adapter_invocation": (
        "src/hdmatch/natal_time/replay.py",
        "src/hdmatch/runtime/chart_adapter.py",
    ),
    "independent_verifier_invocation": (
        "src/hdmatch/natal_time/replay.py",
        "src/hdmatch/natal_time/enumerator.py",
    ),
    "coverage_and_result_digest_construction": ("src/hdmatch/natal_time/replay.py",),
    "aggregate_index_construction_and_validation": ("src/hdmatch/natal_time/replay.py",),
}

ALLOWED_REPLAY_SOURCE_DIFFERENCES = {
    "state/CURRENT-STATE.md": (
        "recovery documentation updated after replay; never imported or executed"
    ),
    "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/index.json": (
        "new replay output index generated from the exact replay source"
    ),
    "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts/dst-fold-2024-11-03.json": (
        "new immutable replay output receipt"
    ),
    "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts/dst-gap-2024-03-10.json": (
        "new immutable replay output receipt"
    ),
    "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts/historical-second-offset-1970-01-01.json": (
        "new immutable replay output receipt"
    ),
    "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts/leap-day-2024-02-29.json": (
        "new immutable replay output receipt"
    ),
    "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts/non-integer-offset-2024-01-15.json": (
        "new immutable replay output receipt"
    ),
    "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts/non-one-hour-dst-2024-04-07.json": (
        "new immutable replay output receipt"
    ),
    "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts/ordinary-and-multiple-dates-2024-01-15.json": (
        "new immutable replay output receipt"
    ),
    "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts/ordinary-and-multiple-dates-2024-01-16.json": (
        "new immutable replay output receipt"
    ),
    "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts/skipped-civil-date-2011-12-30.json": (
        "new immutable fail-closed replay output receipt"
    ),
    "tests/unit/test_natal_time_real_engine_replay.py": (
        "test-only aggregate verifier and formatting; not in the production import closure"
    ),
}


class AttestationError(ValueError):
    """Raised when a required Git or content assertion does not hold."""


def _run(
    root: Path, arguments: list[str], *, text: bool = False, check: bool = True
) -> bytes | str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=check,
        capture_output=True,
        text=text,
    )
    return cast(bytes | str, completed.stdout)


def _text(root: Path, arguments: list[str]) -> str:
    output = _run(root, arguments, text=True)
    assert isinstance(output, str)
    return output.strip()


def _bytes(root: Path, arguments: list[str]) -> bytes:
    output = _run(root, arguments)
    assert isinstance(output, bytes)
    return output


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_file(root: Path, commit: str, path: str) -> bytes:
    return _bytes(root, ["show", f"{commit}:{path}"])


def _file_record(root: Path, commit: str, path: str) -> dict[str, Any]:
    data = _git_file(root, commit, path)
    return {
        "path": path,
        "git_blob_oid": _text(root, ["rev-parse", f"{commit}:{path}"]),
        "byte_count": len(data),
        "sha256": _sha256(data),
    }


def _commit_record(root: Path, commit: str) -> dict[str, Any]:
    return {
        "commit": commit,
        "tree_oid": _text(root, ["rev-parse", f"{commit}^{{tree}}"]),
        "parents": _text(root, ["show", "-s", "--format=%P", commit]).split(),
        "subject": _text(root, ["show", "-s", "--format=%s", commit]),
    }


def _name_status(root: Path, before: str, after: str) -> tuple[list[dict[str, str]], bytes]:
    raw = _bytes(root, ["diff", "--no-renames", "--name-status", "-z", before, after])
    tokens = [item for item in raw.split(b"\0") if item]
    if len(tokens) % 2:
        raise AttestationError("name-status output has an incomplete record")
    records: list[dict[str, str]] = []
    for status, path in zip(tokens[::2], tokens[1::2], strict=True):
        records.append(
            {
                "status": status.decode("ascii"),
                "path": path.decode("utf-8", errors="surrogateescape"),
            }
        )
    return records, raw


def _numstat(root: Path, before: str, after: str) -> tuple[list[dict[str, Any]], bytes]:
    raw = _bytes(root, ["diff", "--no-renames", "--numstat", "-z", before, after])
    records: list[dict[str, Any]] = []
    for token in (item for item in raw.split(b"\0") if item):
        additions, deletions, path = token.split(b"\t", 2)
        records.append(
            {
                "path": path.decode("utf-8", errors="surrogateescape"),
                "additions": None if additions == b"-" else int(additions),
                "deletions": None if deletions == b"-" else int(deletions),
            }
        )
    return records, raw


def _diff_record(root: Path, pair_id: str, before: str, after: str) -> dict[str, Any]:
    names, name_raw = _name_status(root, before, after)
    nums, num_raw = _numstat(root, before, after)
    stat_raw = _bytes(root, ["diff", "--no-renames", "--stat=120", before, after])
    shortstat_raw = _bytes(root, ["diff", "--no-renames", "--shortstat", before, after])
    patch_raw = _bytes(
        root,
        ["diff", "--no-renames", "--binary", "--full-index", before, after],
    )
    numeric = [item for item in nums if item["additions"] is not None]
    return {
        "pair_id": pair_id,
        "from_commit": before,
        "to_commit": after,
        "name_status": names,
        "name_status_sha256": _sha256(name_raw),
        "numstat": nums,
        "numstat_sha256": _sha256(num_raw),
        "file_count": len(names),
        "total_additions": sum(item["additions"] for item in numeric),
        "total_deletions": sum(item["deletions"] for item in numeric),
        "stat_text": stat_raw.decode("utf-8", errors="surrogateescape").rstrip("\n"),
        "stat_sha256": _sha256(stat_raw),
        "shortstat_text": shortstat_raw.decode("utf-8").strip(),
        "shortstat_sha256": _sha256(shortstat_raw),
        "full_patch_sha256": _sha256(patch_raw),
    }


def _is_ancestor(root: Path, before: str, after: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", before, after],
        cwd=root,
        capture_output=True,
    )
    if completed.returncode not in (0, 1):
        raise AttestationError("git merge-base ancestry check failed")
    return completed.returncode == 0


def _embedded_json_hash(data: bytes, hash_field: str) -> tuple[str, str, bool]:
    value = json.loads(data)
    if not isinstance(value, dict):
        raise AttestationError("immutable JSON artifact is not an object")
    unhashed = deepcopy(value)
    embedded = unhashed.pop(hash_field, None)
    computed = sha256_json(unhashed)
    return str(embedded), computed, embedded == computed


def build_lineage_attestation(repository_root: Path) -> dict[str, Any]:
    """Build the exact baseline-to-evaluated-head lineage attestation."""

    root = repository_root.resolve(strict=True)
    anchors = {
        "baseline": {
            **_commit_record(root, BASELINE),
            "role": "fresh-main baseline audited before natal-time continuation",
        },
        "reviewed_checkpoint3_head": {
            **_commit_record(root, REVIEWED_CHECKPOINT3_HEAD),
            "role": "exact deterministic-foundation head supplied to checkpoint-3 review",
        },
        "checkpoint3_ruling_commit": {
            **_commit_record(root, CHECKPOINT3_RULING_COMMIT),
            "role": (
                "direct doc-only child recording the checkpoint-3 Pro ruling; not a merge "
                "and not a substitute for the reviewed 8cc97025 head"
            ),
        },
        "replay_source": {
            **_commit_record(root, REPLAY_SOURCE),
            "role": "clean exact source commit used for all local real-engine replay receipts",
        },
        "evaluated_head": {
            **_commit_record(root, EVALUATED_HEAD),
            "role": "exact checkpoint-4 head evaluated by Pro",
        },
    }
    commits = _text(
        root,
        [
            "rev-list",
            "--reverse",
            f"{REVIEWED_CHECKPOINT3_HEAD}^..{EVALUATED_HEAD}",
        ],
    ).split()
    ordered = [_commit_record(root, commit) for commit in commits]
    direct_chain = all(
        current["parents"] == [previous["commit"]]
        for previous, current in zip(ordered, ordered[1:], strict=False)
    )
    merge_commits = _text(
        root,
        ["rev-list", "--merges", f"{REVIEWED_CHECKPOINT3_HEAD}..{EVALUATED_HEAD}"],
    )
    checkpoint_diff = _diff_record(
        root,
        "reviewed_checkpoint3_to_ruling_commit",
        REVIEWED_CHECKPOINT3_HEAD,
        CHECKPOINT3_RULING_COMMIT,
    )
    expected_ruling_change = [
        {"status": "A", "path": "docs/PRO_SUPERVISION_CHECKPOINT_3_20260830.md"}
    ]
    if checkpoint_diff["name_status"] != expected_ruling_change:
        raise AttestationError("checkpoint-3 ruling commit is not doc-only")

    protected: list[dict[str, Any]] = []
    for path in PROTECTED_PATHS:
        reviewed = _file_record(root, REVIEWED_CHECKPOINT3_HEAD, path)
        evaluated = _file_record(root, EVALUATED_HEAD, path)
        item: dict[str, Any] = {
            "path": path,
            "reviewed_checkpoint3": reviewed,
            "evaluated_head": evaluated,
            "byte_identical": reviewed["sha256"] == evaluated["sha256"],
            "git_blob_identical": reviewed["git_blob_oid"] == evaluated["git_blob_oid"],
        }
        hash_field = IMMUTABLE_JSON_HASH_FIELDS.get(path)
        if hash_field is not None:
            embedded, computed, valid = _embedded_json_hash(
                _git_file(root, EVALUATED_HEAD, path), hash_field
            )
            item["embedded_hash_assertion"] = {
                "field": hash_field,
                "embedded": embedded,
                "computed": computed,
                "valid": valid,
            }
        protected.append(item)
    if not all(
        item["byte_identical"]
        and item["git_blob_identical"]
        and item.get("embedded_hash_assertion", {}).get("valid", True)
        for item in protected
    ):
        raise AttestationError("protected deterministic component assertion failed")

    ancestry = {
        "baseline_is_ancestor_of_reviewed_checkpoint3": _is_ancestor(
            root, BASELINE, REVIEWED_CHECKPOINT3_HEAD
        ),
        "reviewed_checkpoint3_is_parent_of_ruling_commit": anchors[
            "checkpoint3_ruling_commit"
        ]["parents"]
        == [REVIEWED_CHECKPOINT3_HEAD],
        "ruling_commit_is_ancestor_of_replay_source": _is_ancestor(
            root, CHECKPOINT3_RULING_COMMIT, REPLAY_SOURCE
        ),
        "replay_source_is_ancestor_of_evaluated_head": _is_ancestor(
            root, REPLAY_SOURCE, EVALUATED_HEAD
        ),
        "reviewed_checkpoint3_is_ancestor_of_evaluated_head": _is_ancestor(
            root, REVIEWED_CHECKPOINT3_HEAD, EVALUATED_HEAD
        ),
    }
    if not all(ancestry.values()) or not direct_chain or merge_commits:
        raise AttestationError("lineage ancestry/no-merge assertion failed")

    payload: dict[str, Any] = {
        "schema_version": LINEAGE_SCHEMA,
        "scope": "exact Git-object lineage through the checkpoint-4 evaluated head",
        "anchors": anchors,
        "ordered_commit_count": len(ordered),
        "ordered_commits": ordered,
        "ordered_commit_topology_sha256": sha256_json(ordered),
        "diffs": [_diff_record(root, *pair) for pair in DIFF_PAIRS],
        "assertions": {
            **ancestry,
            "ordered_commits_form_one_direct_first_parent_chain": direct_chain,
            "merge_commit_count_after_reviewed_checkpoint3": 0,
            "merge_commits_after_reviewed_checkpoint3": [],
            "checkpoint3_ruling_commit_is_doc_only": True,
            "checkpoint3_ruling_commit_changed_paths": expected_ruling_change,
            "protected_file_count": len(protected),
            "all_protected_files_byte_identical": True,
            "all_immutable_embedded_hashes_valid": True,
        },
        "protected_files": protected,
    }
    payload["attestation_sha256"] = sha256_json(payload)
    return payload


def _module_map(root: Path, commit: str) -> tuple[dict[str, str], set[str]]:
    paths = set(_text(root, ["ls-tree", "-r", "--name-only", commit]).splitlines())
    mapping: dict[str, str] = {}
    for path in sorted(paths):
        module: str | None = None
        if path.startswith("src/") and path.endswith(".py"):
            module = path[4:-3].replace("/", ".")
        elif path.startswith("scripts/") and path.endswith(".py"):
            module = path[:-3].replace("/", ".")
        if module is None:
            continue
        if module.endswith(".__init__"):
            module = module[: -len(".__init__")]
        mapping[module] = path
    return mapping, paths


def _local_imports(path: str, source: bytes, module_map: dict[str, str]) -> set[str]:
    tree = ast.parse(source, filename=path)
    current = next((name for name, value in module_map.items() if value == path), None)
    if current is None:
        raise AttestationError(f"entry in import closure has no module name: {path}")
    package = current if path.endswith("/__init__.py") else current.rpartition(".")[0]
    discovered: set[str] = set()
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base: str | None = None
            if node.level:
                relative = "." * node.level + (node.module or "")
                try:
                    base = importlib.util.resolve_name(relative, package)
                except (ImportError, ValueError) as exc:
                    raise AttestationError(f"cannot resolve relative import in {path}") from exc
            elif node.module:
                base = node.module
            if base is not None:
                names.append(base)
                names.extend(
                    f"{base}.{alias.name}" for alias in node.names if alias.name != "*"
                )
        for name in names:
            candidate = name
            while candidate:
                if candidate in module_map:
                    discovered.add(module_map[candidate])
                    break
                candidate = candidate.rpartition(".")[0]
    return discovered


def _implicit_package_initializers(path: str, module_map: dict[str, str]) -> set[str]:
    current = next((name for name, value in module_map.items() if value == path), None)
    if current is None:
        raise AttestationError(f"entry in import closure has no module name: {path}")
    parts = current.split(".")
    package_depth = len(parts) if path.endswith("/__init__.py") else len(parts) - 1
    initializers: set[str] = set()
    for depth in range(1, package_depth + 1):
        candidate = module_map.get(".".join(parts[:depth]))
        if candidate is not None and candidate.endswith("/__init__.py"):
            initializers.add(candidate)
    initializers.discard(path)
    return initializers


def _import_closure(root: Path, commit: str) -> tuple[str, ...]:
    module_map, paths = _module_map(root, commit)
    if not set(REPLAY_ENTRY_PATHS).issubset(paths):
        raise AttestationError("replay entry path is absent")
    queue: deque[str] = deque(REPLAY_ENTRY_PATHS)
    visited: set[str] = set()
    while queue:
        path = queue.popleft()
        if path in visited:
            continue
        visited.add(path)
        for initializer in sorted(_implicit_package_initializers(path, module_map)):
            if initializer not in visited:
                queue.append(initializer)
        for imported in sorted(_local_imports(path, _git_file(root, commit, path), module_map)):
            if imported not in visited:
                queue.append(imported)
    return tuple(sorted(visited))


def _verify_replay_aggregate(root: Path, evaluated_head: str) -> dict[str, Any]:
    index_path = "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/index.json"
    index = json.loads(_git_file(root, evaluated_head, index_path))
    if not isinstance(index, dict):
        raise AttestationError("replay index is not an object")
    unhashed = deepcopy(index)
    embedded_index = unhashed.pop("index_sha256", None)
    if embedded_index != sha256_json(unhashed):
        raise AttestationError("replay index self-hash mismatch")
    source = index.get("source_verification")
    if not isinstance(source, dict):
        raise AttestationError("replay source verification is missing")
    source_unhashed = deepcopy(source)
    embedded_source = source_unhashed.pop("source_verification_sha256", None)
    if embedded_source != sha256_json(source_unhashed):
        raise AttestationError("replay source-verification self-hash mismatch")
    if embedded_source != index.get("source_verification_sha256"):
        raise AttestationError("index/source-verification digest mismatch")
    if (
        index.get("repository_commit") != REPLAY_SOURCE
        or index.get("commit_tree_oid")
        != _text(root, ["rev-parse", f"{REPLAY_SOURCE}^{{tree}}"])
        or index.get("execution_mode") != "real_engine_production"
        or index.get("real_engine_executor") is not True
        or index.get("synthetic_orchestration_test_only") is not False
    ):
        raise AttestationError("replay index provenance mismatch")
    receipt_refs = index.get("receipt_hashes")
    if not isinstance(receipt_refs, list) or len(receipt_refs) != 9:
        raise AttestationError("replay index must bind nine receipts")
    receipts: list[dict[str, Any]] = []
    for reference in receipt_refs:
        receipt_id = reference["receipt_id"]
        path = f"state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts/{receipt_id}.json"
        receipt = json.loads(_git_file(root, evaluated_head, path))
        receipt_unhashed = deepcopy(receipt)
        embedded_receipt = receipt_unhashed.pop("receipt_sha256", None)
        if embedded_receipt != sha256_json(receipt_unhashed):
            raise AttestationError(f"replay receipt self-hash mismatch: {receipt_id}")
        if embedded_receipt != reference["receipt_sha256"]:
            raise AttestationError(f"replay receipt/index mismatch: {receipt_id}")
        if (
            receipt.get("repository_commit") != REPLAY_SOURCE
            or receipt.get("execution_mode") != "real_engine_production"
            or receipt.get("real_engine_executor") is not True
            or receipt.get("synthetic_orchestration_test_only") is not False
        ):
            raise AttestationError(f"replay receipt provenance mismatch: {receipt_id}")
        receipts.append(receipt)
    actual_paths = tuple(
        sorted(
            path
            for path in _text(
                root,
                [
                    "ls-tree",
                    "-r",
                    "--name-only",
                    evaluated_head,
                    "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts",
                ],
            ).splitlines()
        )
    )
    expected_paths = tuple(
        sorted(
            "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1/receipts/"
            f"{reference['receipt_id']}.json"
            for reference in receipt_refs
        )
    )
    if actual_paths != expected_paths:
        raise AttestationError("replay receipt directory has missing or extra files")
    aggregate_input = {
        "execution_mode": index["execution_mode"],
        "repository_commit": index["repository_commit"],
        "commit_tree_oid": index["commit_tree_oid"],
        "source_verification_sha256": index["source_verification_sha256"],
        "fixture_artifact_file_sha256": index["fixture_artifact_file_sha256"],
        "fixture_artifact_audit_sha256": index["fixture_artifact_audit_sha256"],
        "engine_identity_file_sha256": index["engine_identity_file_sha256"],
        "engine_identity_packet_sha256": index["engine_identity_packet_sha256"],
        "receipt_hashes": receipt_refs,
    }
    computed_aggregate = sha256_json(aggregate_input)
    if computed_aggregate != index.get("aggregate_sha256"):
        raise AttestationError("receipt-only aggregate digest mismatch")
    if embedded_index != EXPECTED_REPLAY_INDEX_SHA256:
        raise AttestationError("replay index does not match the checkpoint-4 expected digest")
    if computed_aggregate != EXPECTED_REPLAY_AGGREGATE_SHA256:
        raise AttestationError("replay aggregate does not match the checkpoint-4 expected digest")
    return {
        "evaluated_head": evaluated_head,
        "replay_source_commit": index["repository_commit"],
        "replay_source_tree_oid": index["commit_tree_oid"],
        "receipt_count": len(receipts),
        "successful_civil_day_count": sum(item["status"] == "success" for item in receipts),
        "fail_closed_civil_day_count": sum(
            item["status"] == "fail_closed" for item in receipts
        ),
        "receipt_hashes": receipt_refs,
        "source_verification_sha256": index["source_verification_sha256"],
        "aggregate_sha256": computed_aggregate,
        "expected_aggregate_sha256": EXPECTED_REPLAY_AGGREGATE_SHA256,
        "aggregate_matches_checkpoint4_expected_sha256": True,
        "index_sha256": embedded_index,
        "expected_index_sha256": EXPECTED_REPLAY_INDEX_SHA256,
        "index_matches_checkpoint4_expected_sha256": True,
        "transition_recomputation_performed": False,
        "aggregate_rebuilt_from_receipt_hashes_only": True,
        "current_evaluated_head_match_via_source_byte_identity": True,
    }


def build_replay_source_manifest(repository_root: Path) -> dict[str, Any]:
    """Prove replay-affecting bytes unchanged and revalidate the receipt-only aggregate."""

    root = repository_root.resolve(strict=True)
    source_closure = _import_closure(root, REPLAY_SOURCE)
    evaluated_closure = _import_closure(root, EVALUATED_HEAD)
    if source_closure != evaluated_closure:
        raise AttestationError("local real-engine replay import closure changed")
    source_paths = tuple(sorted(set(source_closure).union(REPLAY_NON_PYTHON_INPUTS)))
    required_surface_paths = {
        path for paths in REPLAY_REQUIRED_SURFACE_COVERAGE.values() for path in paths
    }
    if not required_surface_paths.issubset(source_paths):
        raise AttestationError("required replay surface is absent from the source manifest")
    files: list[dict[str, Any]] = []
    for path in source_paths:
        source = _file_record(root, REPLAY_SOURCE, path)
        evaluated = _file_record(root, EVALUATED_HEAD, path)
        files.append(
            {
                "path": path,
                "classification": (
                    "transitive_python_import"
                    if path in source_closure
                    else "explicit_non_python_runtime_or_frozen_input"
                ),
                "replay_source": source,
                "evaluated_head": evaluated,
                "byte_identical": source["sha256"] == evaluated["sha256"],
                "git_blob_identical": source["git_blob_oid"] == evaluated["git_blob_oid"],
            }
        )
    if not all(item["byte_identical"] and item["git_blob_identical"] for item in files):
        raise AttestationError("replay-affecting file changed after replay source")
    differences, diff_raw = _name_status(root, REPLAY_SOURCE, EVALUATED_HEAD)
    actual_difference_paths = {item["path"] for item in differences}
    if actual_difference_paths != set(ALLOWED_REPLAY_SOURCE_DIFFERENCES):
        raise AttestationError("replay-source allowed-difference inventory is incomplete")
    if set(source_paths).intersection(actual_difference_paths):
        raise AttestationError("allowed difference overlaps replay-affecting source")
    allowed = [
        {
            **item,
            "reason": ALLOWED_REPLAY_SOURCE_DIFFERENCES[item["path"]],
            "replay_affecting": False,
        }
        for item in differences
    ]
    aggregate = _verify_replay_aggregate(root, EVALUATED_HEAD)
    payload: dict[str, Any] = {
        "schema_version": SOURCE_SCHEMA,
        "scope": (
            "fail-closed local real-engine replay import closure, frozen inputs, explicit allowed "
            "differences, and receipt-hash-only aggregate"
        ),
        "replay_source": _commit_record(root, REPLAY_SOURCE),
        "evaluated_head": _commit_record(root, EVALUATED_HEAD),
        "entry_paths": list(REPLAY_ENTRY_PATHS),
        "python_import_closure": list(source_closure),
        "python_import_closure_sha256": sha256_json(source_closure),
        "explicit_non_python_inputs": list(REPLAY_NON_PYTHON_INPUTS),
        "required_surface_coverage": [
            {"category": category, "paths": list(paths)}
            for category, paths in REPLAY_REQUIRED_SURFACE_COVERAGE.items()
        ],
        "replay_affecting_file_count": len(files),
        "replay_affecting_files": files,
        "allowed_difference_count": len(allowed),
        "allowed_differences": allowed,
        "source_to_evaluated_name_status_sha256": _sha256(diff_raw),
        "aggregate_only_verification": aggregate,
        "assertions": {
            "replay_source_is_ancestor_of_evaluated_head": _is_ancestor(
                root, REPLAY_SOURCE, EVALUATED_HEAD
            ),
            "import_closure_identical": True,
            "all_replay_affecting_files_byte_identical": True,
            "all_replay_affecting_git_blobs_identical": True,
            "all_required_replay_surface_categories_bound": True,
            "all_differences_explicitly_allowed": True,
            "allowed_differences_overlap_replay_affecting_files": False,
            "current_evaluated_head_aggregate_only_match": True,
            "transition_recomputation_performed": False,
        },
    }
    payload["manifest_sha256"] = sha256_json(payload)
    return payload


def _verify_content_hash(payload: dict[str, Any], field: str) -> None:
    unhashed = deepcopy(payload)
    embedded = unhashed.pop(field, None)
    if embedded != sha256_json(unhashed):
        raise AttestationError(f"content hash mismatch: {field}")


def validate_lineage_attestation(repository_root: Path, payload: dict[str, Any]) -> None:
    _verify_content_hash(payload, "attestation_sha256")
    if payload != build_lineage_attestation(repository_root):
        raise AttestationError("lineage attestation does not match exact Git objects")


def validate_replay_source_manifest(repository_root: Path, payload: dict[str, Any]) -> None:
    _verify_content_hash(payload, "manifest_sha256")
    if payload != build_replay_source_manifest(repository_root):
        raise AttestationError("replay source manifest does not match exact Git objects")


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict):
        raise AttestationError(f"artifact is not a JSON object: {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--lineage-output",
        type=Path,
        default=Path("state/NATAL-TIME-CHECKPOINT4-LINEAGE-ATTESTATION.json"),
    )
    parser.add_argument(
        "--source-output",
        type=Path,
        default=Path("state/NATAL-TIME-REPLAY-SOURCE-MANIFEST-V1.json"),
    )
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    root = args.repository_root.resolve(strict=True)
    lineage_path = (
        args.lineage_output
        if args.lineage_output.is_absolute()
        else root / args.lineage_output
    )
    source_path = (
        args.source_output
        if args.source_output.is_absolute()
        else root / args.source_output
    )
    if args.validate_only:
        validate_lineage_attestation(root, _load_object(lineage_path))
        validate_replay_source_manifest(root, _load_object(source_path))
        print("CHECKPOINT4_PHASE0_ATTESTATIONS_OK")
        return 0
    lineage = build_lineage_attestation(root)
    source = build_replay_source_manifest(root)
    write_new_bytes(lineage_path, canonical_json_bytes(lineage) + b"\n")
    write_new_bytes(source_path, canonical_json_bytes(source) + b"\n")
    print(f"LINEAGE_ATTESTATION_SHA256:{lineage['attestation_sha256']}")
    print(f"REPLAY_SOURCE_MANIFEST_SHA256:{source['manifest_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
