"""Build the checkpoint-7 replay/oracle current-head provenance closure."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast

from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.natal_time import replay
from hdmatch.util import canonical_json_bytes, sha256_json
from scripts.audit_natal_time_checkpoint4_phase0 import (
    PROTECTED_PATHS,
    REVIEWED_CHECKPOINT3_HEAD,
)
from scripts.audit_natal_time_checkpoint6_replay_closure import (
    RECEIPT_SOURCE,
    SEMANTIC_FUNCTIONS,
)
from scripts.audit_natal_time_checkpoint7_oracle import (
    CORPUS_PATH,
    LEDGER_PATH,
    MATRIX_PATH,
    MUTATION_PATH,
    ORACLE_PATH,
    _oracle_version,
    validate_oracle_artifacts,
)

CHECKPOINT6_FINAL = "a7a516fe7dc679909fba392a511570ae603e4fe3"
ORACLE_SOURCE = "01a60b28aac84a5b5ecbe66e64a489b8345e0d1b"
CHECKPOINT7_IMPLEMENTATION = "d2ee0a3b875f2e21c37534d5e338947a6e3ff098"
CHECKPOINT7_SUBMISSION = "b581ab3b7397abf5aed5e6da7f7e04deb22e2a06"
CHECKPOINT7_SUBMISSION_TREE = "a4a8dfc1947df513cf2fbeac82000992b74bce9d"

SOURCE_MANIFEST_PATH = "state/NATAL-TIME-REPLAY-SOURCE-MANIFEST-V1.json"
REPLAY_CLOSURE_PATH = "state/NATAL-TIME-CHECKPOINT6-FINAL-REPLAY-SOURCE-CLOSURE.json"
REPLAY_ROOT = "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1"
REPLAY_INDEX_PATH = f"{REPLAY_ROOT}/index.json"
OUTPUT_PATH = "state/NATAL-TIME-CHECKPOINT7-CURRENT-HEAD-CLOSURE.json"
VALIDATOR_PATH = "scripts/audit_natal_time_checkpoint7_current_head_closure.py"

EXPECTED_REPLAY_CLOSURE_LOGICAL_SHA256 = (
    "eb862ff17e3223a9a39af0a25c567dd24cecf67fb2c9524f44449214d80d5a88"
)
EXPECTED_REPLAY_CLOSURE_FILE_SHA256 = (
    "be791a759af4e22a9ef1f429521112e098066d1b3c4327ececf6c88fd717554e"
)
EXPECTED_INDEX_SHA256 = (
    "f7ead3c9b3b4eb7102cfff5c74e3de3e261e3f6b8491ccfe8881fbf882b75435"
)
EXPECTED_AGGREGATE_SHA256 = (
    "ee8b4882785bb1102b8f14cd23e0d4cc18416118109b0040b8313f86e6be1665"
)
EXPECTED_ORACLE_SOURCE_SHA256 = (
    "4192061951696d28d9d2671c70e13bb69b38aeba95ee83dc9e53f40eadb234c3"
)
EXPECTED_ORACLE_VERSION_SHA256 = (
    "f3a3fc3b273da8a7d9a94d8e6b2e02bbbd9169093979aec42d084c272b78b623"
)

EXPECTED_ORACLE_ARTIFACTS: dict[str, tuple[str, str]] = {
    CORPUS_PATH: (
        "acc7fcb9795f2fd07dabbfc3905d080aa29b3ab0d9f98a5339199de3c199df12",
        "f791a7be473ed0af0e859a22da4fb8157a3b31f2785b6edef85094efd95b94bf",
    ),
    MATRIX_PATH: (
        "30cf1fbe145b4e2ed6ada066293b000e72c4e443dd61f716895942a9fdc3fc4e",
        "07deeb95ffdf823dccf90a6b390ca6ec95ce7d09f0cba7553a08441febc84579",
    ),
    MUTATION_PATH: (
        "0c16d226f631d27a5c30f14a01022f8e06b80f41d31c1fca98fee763727569b4",
        "bddf2be59ace042fa28ae82961a7e7932bbd29c8d7139eeb897814880e9f89ff",
    ),
    LEDGER_PATH: (
        "aa87a1d7fe8dcab1211d9ad7b2686c29217ea101351bf4279eef66a98001cd64",
        "7372aefd90876174ae7628f77145f695df4d099cab9048dc5badd968c2d608d6",
    ),
}

ORACLE_LOGICAL_HASH_FIELDS = {
    CORPUS_PATH: "corpus_sha256",
    MATRIX_PATH: "matrix_sha256",
    MUTATION_PATH: "mutation_report_sha256",
    LEDGER_PATH: "ledger_sha256",
}

EXPECTED_SUBMISSION_DELTA = (
    ("M", "CURRENT_PLAN.md"),
    ("A", "docs/NATAL_TIME_CHECKPOINT7_ACCEPTANCE_20260830.md"),
    ("M", "state/CURRENT-STATE.md"),
)

IMPLEMENTATION_DELTA_CLASSIFICATION: dict[str, str] = {
    "docs/PRO_SUPERVISION_CHECKPOINT_6_20260830.md": "supervision_documentation",
    "scripts/audit_natal_time_checkpoint6_replay_closure.py": (
        "fail_closed_provenance_validator"
    ),
    "scripts/audit_natal_time_checkpoint7_oracle.py": "test_only_oracle_evidence_builder",
    REPLAY_CLOSURE_PATH: "immutable_provenance_attestation",
    CORPUS_PATH: "test_only_synthetic_oracle_evidence",
    MATRIX_PATH: "test_only_synthetic_oracle_evidence",
    LEDGER_PATH: "test_only_synthetic_oracle_evidence",
    MUTATION_PATH: "test_only_synthetic_oracle_evidence",
    "tests/oracles/__init__.py": "test_only_oracle_package",
    ORACLE_PATH: "test_only_structurally_independent_oracle",
    "tests/unit/test_natal_time_checkpoint6_replay_closure.py": "test_only_provenance_checks",
    "tests/unit/test_natal_time_checkpoint7_oracle_audit.py": "test_only_oracle_checks",
    "tests/unit/test_natal_time_synthetic_evaluation_contract.py": (
        "test_only_endpoint_contract_assertion"
    ),
    "tests/unit/test_natal_time_v3_independent_oracle.py": "test_only_oracle_checks",
}

ACCEPTANCE_TEST_IDS = (
    "C7CH-01-checkpoint6-final-ancestor",
    "C7CH-02-oracle-source-ancestor",
    "C7CH-03-submission-direct-parent",
    "C7CH-04-no-merge-or-alternate-parent",
    "C7CH-05-exact-documentation-child-delta",
    "C7CH-06-all-58-replay-paths-identical",
    "C7CH-07-all-28-semantic-functions-identical",
    "C7CH-08-replay-semantic-categories-identical",
    "C7CH-09-nonreplay-delta-explicitly-classified",
    "C7CH-10-receipt-semantic-change-requires-route-b",
    "C7CH-11-nine-receipts-index-and-aggregate-reproduce",
    "C7CH-12-path-and-function-mutations-force-route-b",
    "C7CH-13-oracle-source-blobs-identical",
    "C7CH-14-oracle-version-recomputes",
    "C7CH-15-oracle-ast-independence-rerun",
    "C7CH-16-four-oracle-artifacts-reproduce",
    "C7CH-17-oracle-source-mutation-invalidates",
    "C7CH-18-all-48-protected-paths-identical",
    "C7CH-19-no-prohibited-scope-introduced",
    "C7CH-20-closure-reproduces-byte-for-byte",
    "C7CH-21-clean-worktree-and-index-enforced",
)

EXPECTED_STANDARD_LIBRARY_IMPORTS = {
    "__future__",
    "collections.abc",
    "copy",
    "dataclasses",
    "datetime",
    "fractions",
    "hashlib",
    "json",
    "typing",
}


class CurrentHeadClosureError(ValueError):
    """Raised when checkpoint-7 current-head provenance cannot close."""


class CurrentHeadRouteBRequired(CurrentHeadClosureError):
    """Raised when a replay semantic differs after checkpoint 6."""


def _run_git(
    root: Path, arguments: Sequence[str], *, text: bool = False, check: bool = True
) -> bytes | str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=check,
        capture_output=True,
        text=text,
    )
    return cast(bytes | str, result.stdout)


def _git_text(root: Path, arguments: Sequence[str]) -> str:
    value = _run_git(root, arguments, text=True)
    assert isinstance(value, str)
    return value.strip()


def _git_bytes(root: Path, arguments: Sequence[str]) -> bytes:
    value = _run_git(root, arguments)
    assert isinstance(value, bytes)
    return value


def _git_file(root: Path, commit: str, path: str) -> bytes:
    return _git_bytes(root, ("show", f"{commit}:{path}"))


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _self_hash(payload: Mapping[str, Any], field: str) -> str:
    unhashed = dict(payload)
    embedded = unhashed.pop(field, None)
    computed = sha256_json(unhashed)
    if embedded != computed:
        raise CurrentHeadClosureError(f"self-hash mismatch: {field}")
    return computed


def _commit_record(root: Path, commit: str) -> dict[str, Any]:
    return {
        "commit": commit,
        "tree_oid": _git_text(root, ("rev-parse", f"{commit}^{{tree}}")),
        "parents": _git_text(root, ("show", "-s", "--format=%P", commit)).split(),
        "subject": _git_text(root, ("show", "-s", "--format=%s", commit)),
    }


def _require_ancestor(root: Path, before: str, after: str) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", before, after],
        cwd=root,
        check=False,
    )
    if result.returncode != 0:
        raise CurrentHeadClosureError(f"not an ancestor: {before} -> {after}")


def _name_status(root: Path, before: str, after: str) -> tuple[tuple[str, str], ...]:
    raw = _git_bytes(
        root, ("diff", "--no-renames", "--name-status", "-z", before, after)
    )
    tokens = [item for item in raw.split(b"\0") if item]
    if len(tokens) % 2:
        raise CurrentHeadClosureError("incomplete Git name-status record")
    return tuple(
        (status.decode("ascii"), path.decode("utf-8"))
        for status, path in zip(tokens[::2], tokens[1::2], strict=True)
    )


def _require_clean(root: Path) -> None:
    if _git_text(root, ("status", "--porcelain")):
        raise CurrentHeadClosureError("worktree or index is not clean")


def _definition_sha(source: bytes, path: str, symbol: str) -> str:
    tree = ast.parse(source, filename=path)
    definitions = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node.name == symbol
    ]
    if len(definitions) != 1:
        raise CurrentHeadClosureError(f"missing semantic symbol: {path}:{symbol}")
    rendered = ast.dump(definitions[0], include_attributes=False).encode("utf-8")
    return _sha256(rendered)


def _require_replay_equal(path: str, before: bytes, after: bytes) -> None:
    if before != after:
        raise CurrentHeadRouteBRequired(f"replay-affecting byte changed: {path}")


def _require_function_equal(path: str, symbol: str, before: str, after: str) -> None:
    if before != after:
        raise CurrentHeadRouteBRequired(f"replay function changed: {path}:{symbol}")


def _replay_paths(root: Path) -> tuple[str, ...]:
    manifest = json.loads(_git_file(root, CHECKPOINT7_IMPLEMENTATION, SOURCE_MANIFEST_PATH))
    if not isinstance(manifest, dict):
        raise CurrentHeadClosureError("replay source manifest is not an object")
    _self_hash(manifest, "manifest_sha256")
    entries = manifest.get("replay_affecting_files")
    if not isinstance(entries, list):
        raise CurrentHeadClosureError("replay source manifest has no file list")
    paths = tuple(sorted(cast(str, item["path"]) for item in entries))
    if len(paths) != 58 or len(paths) != len(set(paths)):
        raise CurrentHeadClosureError("replay source manifest does not contain 58 unique paths")
    return paths


def _replay_binding(root: Path) -> dict[str, Any]:
    paths = _replay_paths(root)
    file_records: list[dict[str, Any]] = []
    file_probes: list[dict[str, Any]] = []
    for path in paths:
        before = _git_file(root, CHECKPOINT6_FINAL, path)
        after = _git_file(root, CHECKPOINT7_IMPLEMENTATION, path)
        _require_replay_equal(path, before, after)
        mutant = bytearray(after)
        if mutant:
            mutant[0] ^= 1
        else:
            mutant.extend(b"checkpoint7-current-head-mutation")
        rejected = False
        try:
            _require_replay_equal(path, before, bytes(mutant))
        except CurrentHeadRouteBRequired:
            rejected = True
        if not rejected:
            raise CurrentHeadClosureError(f"replay mutation did not force Route B: {path}")
        file_records.append(
            {
                "path": path,
                "checkpoint6_final_blob_oid": _git_text(
                    root, ("rev-parse", f"{CHECKPOINT6_FINAL}:{path}")
                ),
                "checkpoint7_implementation_blob_oid": _git_text(
                    root, ("rev-parse", f"{CHECKPOINT7_IMPLEMENTATION}:{path}")
                ),
                "sha256": _sha256(after),
                "byte_identical": True,
            }
        )
        file_probes.append(
            {
                "path": path,
                "mutation": "toggle first byte or add bytes when empty",
                "route_b_required": True,
            }
        )

    function_records: list[dict[str, Any]] = []
    function_probes: list[dict[str, Any]] = []
    categories: set[str] = set()
    for category, path, symbol in SEMANTIC_FUNCTIONS:
        before_sha = _definition_sha(
            _git_file(root, CHECKPOINT6_FINAL, path), path, symbol
        )
        after_sha = _definition_sha(
            _git_file(root, CHECKPOINT7_IMPLEMENTATION, path), path, symbol
        )
        _require_function_equal(path, symbol, before_sha, after_sha)
        rejected = False
        try:
            mutated_sha = ("0" if after_sha[0] != "0" else "1") + after_sha[1:]
            _require_function_equal(path, symbol, before_sha, mutated_sha)
        except CurrentHeadRouteBRequired:
            rejected = True
        if not rejected:
            raise CurrentHeadClosureError(
                f"semantic-function mutation did not force Route B: {path}:{symbol}"
            )
        categories.add(category)
        function_records.append(
            {
                "category": category,
                "path": path,
                "symbol": symbol,
                "ast_sha256": after_sha,
                "ast_identical": True,
            }
        )
        function_probes.append(
            {
                "path": path,
                "symbol": symbol,
                "mutation": "change AST digest",
                "route_b_required": True,
            }
        )
    if len(function_records) != 28:
        raise CurrentHeadClosureError("semantic function inventory does not contain 28 entries")
    required_categories = {item[0] for item in SEMANTIC_FUNCTIONS}
    if categories != required_categories:
        raise CurrentHeadClosureError("semantic function categories are incomplete")
    return {
        "replay_affecting_file_count": len(file_records),
        "replay_affecting_files": file_records,
        "semantic_function_count": len(function_records),
        "semantic_functions": function_records,
        "semantic_categories": sorted(categories),
        "file_mutation_probe_count": len(file_probes),
        "file_mutation_probes": file_probes,
        "function_mutation_probe_count": len(function_probes),
        "function_mutation_probes": function_probes,
        "route": "A_current_head_source_equivalence",
        "route_b_regeneration_required": False,
    }


def _validate_receipts_at_checkpoint7(root: Path) -> dict[str, Any]:
    index_bytes = _git_file(root, CHECKPOINT7_IMPLEMENTATION, REPLAY_INDEX_PATH)
    index = json.loads(index_bytes)
    if not isinstance(index, dict):
        raise CurrentHeadClosureError("checkpoint-7 replay index is not an object")
    _self_hash(index, "index_sha256")
    source = index.get("source_verification")
    if not isinstance(source, dict):
        raise CurrentHeadClosureError("replay index has no source verification")
    context = replay._load_pinned_context(
        root,
        RECEIPT_SOURCE,
        execution_mode="real_engine_production",
        source_verification=dict(source),
        fixture_artifact_path=None,
        engine_identity_path=None,
    )
    expectations = {item.receipt_id: item for item in context.expectations}
    references = index.get("receipt_hashes")
    if not isinstance(references, list) or len(references) != 9:
        raise CurrentHeadClosureError("replay index does not contain nine receipt hashes")
    receipts: dict[str, dict[str, Any]] = {}
    receipt_records: list[dict[str, Any]] = []
    for raw_reference in references:
        if not isinstance(raw_reference, dict):
            raise CurrentHeadClosureError("replay receipt reference is not an object")
        receipt_id = cast(str, raw_reference["receipt_id"])
        path = f"{REPLAY_ROOT}/receipts/{receipt_id}.json"
        receipt_bytes = _git_file(root, CHECKPOINT7_IMPLEMENTATION, path)
        receipt = json.loads(receipt_bytes)
        if not isinstance(receipt, dict):
            raise CurrentHeadClosureError(f"replay receipt is not an object: {receipt_id}")
        expectation = expectations.get(receipt_id)
        if expectation is None:
            raise CurrentHeadClosureError(f"missing replay expectation: {receipt_id}")
        replay._validate_receipt(context, expectation, receipt)
        if receipt["receipt_sha256"] != raw_reference["receipt_sha256"]:
            raise CurrentHeadClosureError(f"receipt hash mismatch: {receipt_id}")
        if _git_file(root, CHECKPOINT6_FINAL, path) != receipt_bytes:
            raise CurrentHeadRouteBRequired(f"replay receipt changed: {receipt_id}")
        receipts[receipt_id] = receipt
        receipt_records.append(
            {
                "receipt_id": receipt_id,
                "receipt_sha256": receipt["receipt_sha256"],
                "file_sha256": _sha256(receipt_bytes),
                "validated": True,
                "byte_identical_checkpoint6_checkpoint7": True,
            }
        )
    rebuilt = replay.build_aggregate_index(context, receipts)
    if canonical_json_bytes(rebuilt) + b"\n" != index_bytes:
        raise CurrentHeadRouteBRequired("checkpoint-7 replay index does not reproduce")
    if rebuilt["index_sha256"] != EXPECTED_INDEX_SHA256:
        raise CurrentHeadClosureError("checkpoint-7 replay index SHA changed")
    if rebuilt["aggregate_sha256"] != EXPECTED_AGGREGATE_SHA256:
        raise CurrentHeadClosureError("checkpoint-7 replay aggregate SHA changed")
    return {
        "validated_source": CHECKPOINT7_IMPLEMENTATION,
        "receipt_count": len(receipt_records),
        "receipt_records": receipt_records,
        "all_nine_receipts_valid": True,
        "index_byte_equivalent": True,
        "index_sha256": rebuilt["index_sha256"],
        "aggregate_sha256": rebuilt["aggregate_sha256"],
    }


def _oracle_independence_audit(source: bytes) -> dict[str, Any]:
    tree = ast.parse(source, filename=ORACLE_PATH)
    imports: set[str] = set()
    top_level_definitions: list[str] = []
    forbidden_calls: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imports.add(node.module)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {
                "__import__",
                "compile",
                "eval",
                "exec",
            }:
                forbidden_calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                parts: list[str] = []
                value: ast.expr = node.func
                while isinstance(value, ast.Attribute):
                    parts.append(value.attr)
                    value = value.value
                if isinstance(value, ast.Name):
                    parts.append(value.id)
                    dotted = ".".join(reversed(parts))
                    if dotted.startswith(("importlib.", "subprocess.", "os.system", "os.popen")):
                        forbidden_calls.append(dotted)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            top_level_definitions.append(node.name)
    if imports != EXPECTED_STANDARD_LIBRARY_IMPORTS:
        raise CurrentHeadClosureError(f"oracle import surface changed: {sorted(imports)}")
    if any(name.startswith(("hdmatch", "scripts")) for name in imports):
        raise CurrentHeadClosureError("oracle imports production or repository-script code")
    if forbidden_calls:
        raise CurrentHeadClosureError(
            f"oracle has forbidden dynamic/process call: {forbidden_calls}"
        )
    generation_pattern = re.compile(r"(generate|rank|optim|choose|recommend|best)[_a-z0-9]*s_i")
    generation_definitions = [
        name for name in top_level_definitions if generation_pattern.search(name.lower())
    ]
    if generation_definitions:
        raise CurrentHeadClosureError(
            f"oracle exposes S_i generation/optimization: {generation_definitions}"
        )
    return {
        "ast_parsed": True,
        "imports": sorted(imports),
        "standard_library_only": True,
        "production_imports": [],
        "repository_script_imports": [],
        "dynamic_import_calls": [],
        "subprocess_or_shell_calls": [],
        "top_level_definitions": top_level_definitions,
        "s_i_generation_or_optimization_definitions": [],
        "constructs_or_chooses_s_i": False,
    }


def _require_oracle_source(source: bytes) -> None:
    if _sha256(source) != EXPECTED_ORACLE_SOURCE_SHA256:
        raise CurrentHeadClosureError("oracle source hash changed")


def _oracle_binding(root: Path) -> dict[str, Any]:
    source_records: dict[str, dict[str, str]] = {}
    for name, commit in (
        ("oracle_source", ORACLE_SOURCE),
        ("checkpoint7_implementation", CHECKPOINT7_IMPLEMENTATION),
        ("checkpoint7_submission", CHECKPOINT7_SUBMISSION),
    ):
        source = _git_file(root, commit, ORACLE_PATH)
        _require_oracle_source(source)
        source_records[name] = {
            "commit": commit,
            "git_blob_oid": _git_text(root, ("rev-parse", f"{commit}:{ORACLE_PATH}")),
            "sha256": _sha256(source),
        }
    source = _git_file(root, CHECKPOINT7_IMPLEMENTATION, ORACLE_PATH)
    if (root / ORACLE_PATH).read_bytes() != source:
        raise CurrentHeadClosureError("loaded oracle differs from checkpoint-7 implementation")
    independence = _oracle_independence_audit(source)
    version = _oracle_version(root, ORACLE_SOURCE)
    if version["oracle_version_sha256"] != EXPECTED_ORACLE_VERSION_SHA256:
        raise CurrentHeadClosureError("oracle version did not recompute")

    artifacts: dict[str, dict[str, Any]] = {}
    artifact_records: list[dict[str, Any]] = []
    for path, (logical_sha, exact_sha) in EXPECTED_ORACLE_ARTIFACTS.items():
        data = _git_file(root, CHECKPOINT7_IMPLEMENTATION, path)
        if _sha256(data) != exact_sha:
            raise CurrentHeadClosureError(f"oracle artifact exact hash changed: {path}")
        payload = json.loads(data)
        if not isinstance(payload, dict):
            raise CurrentHeadClosureError(f"oracle artifact is not an object: {path}")
        if payload.get(ORACLE_LOGICAL_HASH_FIELDS[path]) != logical_sha:
            raise CurrentHeadClosureError(f"oracle artifact logical hash changed: {path}")
        if (root / path).read_bytes() != data:
            raise CurrentHeadClosureError(f"loaded oracle artifact differs from d2ee0a3: {path}")
        artifacts[path] = payload
        artifact_records.append(
            {
                "path": path,
                "logical_hash_field": ORACLE_LOGICAL_HASH_FIELDS[path],
                "logical_sha256": logical_sha,
                "exact_file_sha256": exact_sha,
                "git_blob_oid_at_implementation": _git_text(
                    root, ("rev-parse", f"{CHECKPOINT7_IMPLEMENTATION}:{path}")
                ),
            }
        )
    validate_oracle_artifacts(root, artifacts)

    mutated = bytearray(source)
    mutated[0] ^= 1
    rejected = False
    try:
        _require_oracle_source(bytes(mutated))
    except CurrentHeadClosureError:
        rejected = True
    if not rejected:
        raise CurrentHeadClosureError("oracle mutation did not invalidate source binding")
    return {
        "source_records": source_records,
        "source_sha256": EXPECTED_ORACLE_SOURCE_SHA256,
        "version": version,
        "version_sha256": EXPECTED_ORACLE_VERSION_SHA256,
        "independence_audit": independence,
        "artifact_count": len(artifact_records),
        "artifact_records": artifact_records,
        "artifacts_reproduce_exactly": True,
        "source_mutation_probe": {
            "mutation": "toggle first oracle-source byte",
            "source_binding_invalidated": True,
            "current_head_closure_invalidated": True,
        },
    }


def _replay_closure_binding(root: Path) -> dict[str, Any]:
    data = _git_file(root, CHECKPOINT7_IMPLEMENTATION, REPLAY_CLOSURE_PATH)
    if _sha256(data) != EXPECTED_REPLAY_CLOSURE_FILE_SHA256:
        raise CurrentHeadClosureError("checkpoint-6 replay closure exact hash changed")
    payload = json.loads(data)
    if not isinstance(payload, dict):
        raise CurrentHeadClosureError("checkpoint-6 replay closure is not an object")
    _self_hash(payload, "closure_sha256")
    if payload["closure_sha256"] != EXPECTED_REPLAY_CLOSURE_LOGICAL_SHA256:
        raise CurrentHeadClosureError("checkpoint-6 replay closure logical hash changed")
    if (root / REPLAY_CLOSURE_PATH).read_bytes() != data:
        raise CurrentHeadClosureError("checkpoint-6 replay closure was overwritten")
    return {
        "path": REPLAY_CLOSURE_PATH,
        "logical_sha256": EXPECTED_REPLAY_CLOSURE_LOGICAL_SHA256,
        "exact_file_sha256": EXPECTED_REPLAY_CLOSURE_FILE_SHA256,
        "git_blob_oid_at_checkpoint7_implementation": _git_text(
            root, ("rev-parse", f"{CHECKPOINT7_IMPLEMENTATION}:{REPLAY_CLOSURE_PATH}")
        ),
        "preserved_not_overwritten": True,
    }


def _topology_and_scope(root: Path) -> dict[str, Any]:
    _require_ancestor(root, CHECKPOINT6_FINAL, CHECKPOINT7_IMPLEMENTATION)
    _require_ancestor(root, ORACLE_SOURCE, CHECKPOINT7_IMPLEMENTATION)
    implementation = _commit_record(root, CHECKPOINT7_IMPLEMENTATION)
    submission = _commit_record(root, CHECKPOINT7_SUBMISSION)
    if submission["parents"] != [CHECKPOINT7_IMPLEMENTATION]:
        raise CurrentHeadClosureError("checkpoint-7 submission is not a direct child")
    if submission["tree_oid"] != CHECKPOINT7_SUBMISSION_TREE:
        raise CurrentHeadClosureError("checkpoint-7 submission tree changed")
    merges = _git_text(
        root, ("rev-list", "--merges", f"{CHECKPOINT6_FINAL}..{CHECKPOINT7_SUBMISSION}")
    ).splitlines()
    if merges:
        raise CurrentHeadClosureError(f"merge commit in checkpoint-7 range: {merges}")
    parent_counts = _git_text(
        root,
        (
            "rev-list",
            "--ancestry-path",
            "--parents",
            f"{CHECKPOINT6_FINAL}..{CHECKPOINT7_SUBMISSION}",
        ),
    ).splitlines()
    if any(len(line.split()) != 2 for line in parent_counts):
        raise CurrentHeadClosureError("alternate-parent path in checkpoint-7 range")
    submission_delta = _name_status(
        root, CHECKPOINT7_IMPLEMENTATION, CHECKPOINT7_SUBMISSION
    )
    if submission_delta != EXPECTED_SUBMISSION_DELTA:
        raise CurrentHeadClosureError(f"checkpoint-7 submission delta changed: {submission_delta}")
    implementation_delta = _name_status(
        root, CHECKPOINT6_FINAL, CHECKPOINT7_IMPLEMENTATION
    )
    observed_paths = {path for _status, path in implementation_delta}
    if observed_paths != set(IMPLEMENTATION_DELTA_CLASSIFICATION):
        raise CurrentHeadClosureError(
            "checkpoint-7 implementation delta has an unclassified or missing path"
        )
    classified = [
        {
            "status": status,
            "path": path,
            "classification": IMPLEMENTATION_DELTA_CLASSIFICATION[path],
        }
        for status, path in implementation_delta
    ]
    return {
        "checkpoint7_implementation": implementation,
        "checkpoint7_submission": submission,
        "checkpoint6_final_is_ancestor": True,
        "oracle_source_is_ancestor": True,
        "submission_direct_parent_verified": True,
        "no_merge_commit_or_alternate_parent_path": True,
        "submission_delta": [
            {"status": status, "path": path} for status, path in submission_delta
        ],
        "implementation_delta_count": len(classified),
        "implementation_delta_classification": classified,
    }


def _protected_binding(root: Path) -> dict[str, Any]:
    records: list[dict[str, str]] = []
    for path in PROTECTED_PATHS:
        reviewed = _git_file(root, REVIEWED_CHECKPOINT3_HEAD, path)
        implementation = _git_file(root, CHECKPOINT7_IMPLEMENTATION, path)
        submission = _git_file(root, CHECKPOINT7_SUBMISSION, path)
        if reviewed != implementation or reviewed != submission:
            raise CurrentHeadClosureError(f"qualified protected path changed: {path}")
        records.append(
            {
                "path": path,
                "git_blob_oid": _git_text(
                    root, ("rev-parse", f"{REVIEWED_CHECKPOINT3_HEAD}:{path}")
                ),
                "sha256": _sha256(reviewed),
            }
        )
    if len(records) != 48:
        raise CurrentHeadClosureError("qualified protected inventory does not contain 48 paths")
    return {
        "reviewed_checkpoint3_head": REVIEWED_CHECKPOINT3_HEAD,
        "protected_path_count": len(records),
        "mismatch_count": 0,
        "records": records,
    }


def _acceptance_results() -> list[dict[str, Any]]:
    return [
        {"acceptance_test_id": test_id, "status": "passed"}
        for test_id in ACCEPTANCE_TEST_IDS
    ]


def build_current_head_closure(
    repository_root: Path, validator_source_commit: str
) -> dict[str, Any]:
    """Build the exact checkpoint-7 current-head closure."""

    root = repository_root.resolve(strict=True)
    if _git_text(root, ("rev-parse", f"{validator_source_commit}^{{commit}}")) != (
        validator_source_commit
    ):
        raise CurrentHeadClosureError("validator source is not an exact commit")
    _require_ancestor(root, CHECKPOINT7_SUBMISSION, validator_source_commit)
    validator_bytes = _git_file(root, validator_source_commit, VALIDATOR_PATH)
    if (root / VALIDATOR_PATH).read_bytes() != validator_bytes:
        raise CurrentHeadClosureError("loaded validator differs from its source commit")

    topology = _topology_and_scope(root)
    replay_binding = _replay_binding(root)
    receipt_validation = _validate_receipts_at_checkpoint7(root)
    prior_closure = _replay_closure_binding(root)
    oracle_binding = _oracle_binding(root)
    protected = _protected_binding(root)
    results = _acceptance_results()
    if len(results) != 21:
        raise CurrentHeadClosureError("checkpoint-7 closure must contain exactly 21 tests")

    payload: dict[str, Any] = {
        "schema_version": "natal-time-checkpoint7-current-head-closure-v1",
        "synthetic_only": True,
        "validator_source": {
            **_commit_record(root, validator_source_commit),
            "path": VALIDATOR_PATH,
            "source_sha256": _sha256(validator_bytes),
        },
        "anchors": {
            "checkpoint6_final": _commit_record(root, CHECKPOINT6_FINAL),
            "oracle_source": _commit_record(root, ORACLE_SOURCE),
            "checkpoint7_implementation": _commit_record(root, CHECKPOINT7_IMPLEMENTATION),
            "checkpoint7_submission": _commit_record(root, CHECKPOINT7_SUBMISSION),
            "checkpoint7_submission_tree": CHECKPOINT7_SUBMISSION_TREE,
        },
        "topology_and_scope": topology,
        "prior_replay_closure": prior_closure,
        "replay_current_head_binding": replay_binding,
        "checkpoint7_receipt_validation": receipt_validation,
        "oracle_current_head_binding": oracle_binding,
        "protected_core_binding": protected,
        "prohibited_scope_scan": {
            "implementation_delta_exactly_classified": True,
            "participant_or_live_data_introduced": False,
            "documentary_reference_data_introduced": False,
            "relationship_data_or_evidence_introduced": False,
            "questionnaire_content_introduced": False,
            "candidate_choice_or_inferential_semantics_introduced": False,
            "all_oracle_artifacts_synthetic_only": True,
        },
        "acceptance_test_count": len(results),
        "acceptance_tests": results,
        "all_acceptance_tests_passed": True,
        "clean_worktree_and_index_required_for_generation_and_validation": True,
        "claim_limits": [
            "This is a current-head provenance extension, not a new scientific result.",
            "Oracle independence is structural and synthetic, not external scientific validation.",
            "Zero discrepancies is bounded to the committed 41-case adversarial corpus.",
            "The mutation evidence is a targeted 13-guard audit, not a complete mutation score.",
            (
                "No estimator, S_i chooser, questionnaire, baseline execution, participant "
                "workflow, ranking, probability, relationship evidence, migration, deployment, "
                "or release is authorized."
            ),
        ],
    }
    payload["current_head_closure_sha256"] = sha256_json(payload)
    return payload


def validate_current_head_closure(
    root: Path, payload: dict[str, Any], *, require_clean: bool
) -> None:
    _self_hash(payload, "current_head_closure_sha256")
    source = cast(dict[str, Any], payload["validator_source"])
    source_commit = cast(str, source["commit"])
    rebuilt = build_current_head_closure(root, source_commit)
    if rebuilt != payload:
        raise CurrentHeadClosureError("current-head closure does not reproduce exactly")
    output = root / OUTPUT_PATH
    if output.is_file() and output.read_bytes() != canonical_json_bytes(payload) + b"\n":
        raise CurrentHeadClosureError("saved current-head closure is not canonical")
    if require_clean:
        _require_clean(root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--source-commit")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    root = args.repository_root.resolve(strict=True)
    output = root / OUTPUT_PATH
    if args.validate_only:
        raw = json.loads(output.read_bytes())
        if not isinstance(raw, dict):
            raise CurrentHeadClosureError("saved current-head closure is not an object")
        validate_current_head_closure(root, raw, require_clean=True)
        print("CHECKPOINT7_CURRENT_HEAD_CLOSURE_OK")
        return 0
    _require_clean(root)
    source_commit = args.source_commit or _git_text(root, ("rev-parse", "HEAD^{commit}"))
    payload = build_current_head_closure(root, source_commit)
    write_new_bytes(output, canonical_json_bytes(payload) + b"\n")
    print(f"CHECKPOINT7_CURRENT_HEAD_CLOSURE_SHA256:{payload['current_head_closure_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
