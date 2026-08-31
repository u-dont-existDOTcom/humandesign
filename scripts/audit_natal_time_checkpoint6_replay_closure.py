"""Build the checkpoint-6 final replay-source provenance closure."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.natal_time import replay
from hdmatch.util import canonical_json_bytes, sha256_json

RECEIPT_SOURCE = "1c59b8aae3c096c84a8116d49c0cb0525029837e"
ACCEPTANCE_SOURCE = "2f707858425cb51f61c5d57e6a0364faf092b841"
IMPLEMENTATION_SOURCE = "067ed6cdd504b368b88c203ca6d058c20b2fb913"
SUBMISSION_SOURCE = "a7a516fe7dc679909fba392a511570ae603e4fe3"

SOURCE_MANIFEST_PATH = "state/NATAL-TIME-REPLAY-SOURCE-MANIFEST-V1.json"
PRIOR_ATTESTATION_PATH = "state/NATAL-TIME-CHECKPOINT5-REPLAY-DELTA-ATTESTATION.json"
FIXTURE_PATH = "state/NATAL-TIME-REAL-ENGINE-FIXTURES.json"
IDENTITY_PATH = "state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json"
REPLAY_ROOT = "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1"
INDEX_PATH = f"{REPLAY_ROOT}/index.json"
SUBMISSION_DOC = "docs/NATAL_TIME_CHECKPOINT6_ACCEPTANCE_20260830.md"

ANCHORS = (
    ("receipt_generation_source", RECEIPT_SOURCE),
    ("checkpoint5_acceptance_source", ACCEPTANCE_SOURCE),
    ("checkpoint6_implementation_source", IMPLEMENTATION_SOURCE),
    ("checkpoint6_submission_source", SUBMISSION_SOURCE),
)

SEMANTIC_FUNCTIONS = (
    ("fixture_inputs", "src/hdmatch/natal_time/replay.py", "_build_expectations"),
    ("fixture_inputs", "src/hdmatch/natal_time/replay.py", "_execute_fail_closed"),
    (
        "fixture_inputs",
        "scripts/audit_natal_time_real_engine_fixtures.py",
        "build_audit",
    ),
    (
        "engine_invocation",
        "src/hdmatch/natal_time/replay.py",
        "real_engine_fixture_executor",
    ),
    (
        "engine_invocation",
        "src/hdmatch/runtime/chart_adapter.py",
        "ExactChartAdapter",
    ),
    ("engine_invocation", "src/hdmatch/chart/calculator.py", "calculate_chart"),
    (
        "event_interval_construction",
        "src/hdmatch/natal_time/replay.py",
        "real_engine_fixture_executor",
    ),
    (
        "event_interval_construction",
        "src/hdmatch/natal_time/replay.py",
        "_event_key",
    ),
    (
        "event_interval_construction",
        "src/hdmatch/natal_time/enumerator.py",
        "enumerate_manifest",
    ),
    (
        "event_interval_construction",
        "src/hdmatch/chart/boundaries.py",
        "build_chart_state_intervals",
    ),
    (
        "independent_verification",
        "src/hdmatch/natal_time/replay.py",
        "_independent_verification",
    ),
    (
        "independent_verification",
        "src/hdmatch/natal_time/conformance.py",
        "independently_enumerate_line_transitions",
    ),
    (
        "receipt_semantic_fields",
        "src/hdmatch/natal_time/replay.py",
        "ReplayExpectation",
    ),
    (
        "receipt_semantic_fields",
        "src/hdmatch/natal_time/replay.py",
        "make_receipt",
    ),
    (
        "receipt_semantic_fields",
        "src/hdmatch/natal_time/replay.py",
        "_validate_receipt",
    ),
    (
        "canonical_serialization",
        "src/hdmatch/util/canonical.py",
        "canonical_json_bytes",
    ),
    (
        "canonical_serialization",
        "src/hdmatch/experiments/canonical.py",
        "canonical_json_bytes",
    ),
    ("digest_construction", "src/hdmatch/natal_time/replay.py", "make_receipt"),
    (
        "digest_construction",
        "src/hdmatch/natal_time/replay.py",
        "build_aggregate_index",
    ),
    ("digest_construction", "src/hdmatch/util/canonical.py", "sha256_json"),
    (
        "index_construction_validation",
        "src/hdmatch/natal_time/replay.py",
        "build_aggregate_index",
    ),
    (
        "index_construction_validation",
        "src/hdmatch/natal_time/replay.py",
        "_load_valid_receipts",
    ),
    (
        "index_construction_validation",
        "src/hdmatch/natal_time/replay.py",
        "_reject_unexpected_receipt_files",
    ),
    (
        "durable_write_resume",
        "src/hdmatch/natal_time/replay.py",
        "_run_replay",
    ),
    (
        "durable_write_resume",
        "src/hdmatch/natal_time/replay.py",
        "_load_valid_receipts",
    ),
    (
        "durable_write_resume",
        "src/hdmatch/natal_time/replay.py",
        "_load_json_object",
    ),
    (
        "durable_write_resume",
        "src/hdmatch/experiments/canonical.py",
        "write_new_bytes",
    ),
    (
        "durable_write_resume",
        "scripts/replay_natal_time_real_engine_fixtures.py",
        "main",
    ),
)


class ReplayClosureError(ValueError):
    """Raised when the final replay-source closure cannot validate."""


class RouteBRequiredError(ReplayClosureError):
    """Raised when a replay-affecting byte changed after the accepted source."""


def _git(root: Path, arguments: Sequence[str], *, text: bool = False) -> bytes | str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, check=True, capture_output=True, text=text
    )
    return cast(bytes | str, result.stdout)


def _git_text(root: Path, arguments: Sequence[str]) -> str:
    output = _git(root, arguments, text=True)
    assert isinstance(output, str)
    return output.strip()


def _git_bytes(root: Path, arguments: Sequence[str]) -> bytes:
    output = _git(root, arguments)
    assert isinstance(output, bytes)
    return output


def _git_file(root: Path, commit: str, path: str) -> bytes:
    return _git_bytes(root, ("show", f"{commit}:{path}"))


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _commit_record(root: Path, commit: str) -> dict[str, Any]:
    return {
        "commit": commit,
        "tree_oid": _git_text(root, ("rev-parse", f"{commit}^{{tree}}")),
        "parents": _git_text(root, ("show", "-s", "--format=%P", commit)).split(),
        "subject": _git_text(root, ("show", "-s", "--format=%s", commit)),
    }


def _name_status(root: Path, before: str, after: str) -> list[dict[str, str]]:
    raw = _git_bytes(
        root, ("diff", "--no-renames", "--name-status", "-z", before, after)
    )
    tokens = [item for item in raw.split(b"\0") if item]
    if len(tokens) % 2:
        raise ReplayClosureError("incomplete Git name-status record")
    return [
        {"status": status.decode("ascii"), "path": path.decode("utf-8")}
        for status, path in zip(tokens[::2], tokens[1::2], strict=True)
    ]


def _self_hash(value: Mapping[str, Any], field: str) -> str:
    unhashed = dict(value)
    embedded = unhashed.pop(field, None)
    computed = sha256_json(unhashed)
    if embedded != computed:
        raise ReplayClosureError(f"self-hash mismatch: {field}")
    return computed


def _require_ancestor(root: Path, before: str, after: str) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", before, after], cwd=root, check=False
    )
    if result.returncode != 0:
        raise ReplayClosureError(f"declared source is not an ancestor: {before} -> {after}")


def _definition_sha(source: bytes, path: str, symbol: str) -> str:
    tree = ast.parse(source, filename=path)
    matches = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node.name == symbol
    ]
    if len(matches) != 1:
        raise ReplayClosureError(f"missing or duplicate semantic symbol: {path}:{symbol}")
    return _sha256(ast.dump(matches[0], include_attributes=False).encode("utf-8"))


def _assert_unchanged_replay_bytes(
    path: str, accepted_bytes: bytes, implementation_bytes: bytes
) -> None:
    """Fail Route A when one replay-affecting path changes after acceptance."""

    if accepted_bytes != implementation_bytes:
        raise RouteBRequiredError(f"replay-affecting byte changed after acceptance: {path}")


def _source_manifest(root: Path) -> tuple[dict[str, Any], tuple[str, ...]]:
    payload = json.loads(_git_file(root, IMPLEMENTATION_SOURCE, SOURCE_MANIFEST_PATH))
    if not isinstance(payload, dict):
        raise ReplayClosureError("replay-source manifest is not an object")
    _self_hash(payload, "manifest_sha256")
    entries = payload.get("replay_affecting_files")
    if not isinstance(entries, list):
        raise ReplayClosureError("replay-source manifest has no file inventory")
    paths = tuple(sorted(cast(str, item["path"]) for item in entries))
    if len(paths) != len(set(paths)) or len(paths) != 58:
        raise ReplayClosureError("replay-source inventory is incomplete or duplicated")
    required = {
        "src/hdmatch/natal_time/replay.py",
        FIXTURE_PATH,
        IDENTITY_PATH,
    }
    if not required.issubset(paths):
        raise ReplayClosureError("replay-source inventory omits a required surface")
    return payload, paths


def _file_closure(
    root: Path, paths: tuple[str, ...]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    probes: list[dict[str, Any]] = []
    for path in paths:
        versions = {
            name: {
                "commit": commit,
                "git_blob_oid": _git_text(root, ("rev-parse", f"{commit}:{path}")),
                "sha256": _sha256(_git_file(root, commit, path)),
            }
            for name, commit in ANCHORS
        }
        accepted = _git_file(root, ACCEPTANCE_SOURCE, path)
        implementation = _git_file(root, IMPLEMENTATION_SOURCE, path)
        submission = _git_file(root, SUBMISSION_SOURCE, path)
        _assert_unchanged_replay_bytes(path, accepted, implementation)
        _assert_unchanged_replay_bytes(path, accepted, submission)
        current = root / path
        if not current.is_file() or current.read_bytes() != implementation:
            raise ReplayClosureError(f"current replay surface differs from 067ed6c: {path}")
        mutation = bytearray(implementation)
        if not mutation:
            mutation.extend(b"checkpoint6-mutation")
        else:
            mutation[0] ^= 1
        rejected = False
        try:
            _assert_unchanged_replay_bytes(path, accepted, bytes(mutation))
        except RouteBRequiredError:
            rejected = True
        if not rejected:
            raise ReplayClosureError(f"semantic-byte mutation did not force Route B: {path}")
        records.append(
            {
                "path": path,
                "versions": versions,
                "byte_identical_acceptance_implementation_submission": True,
                "current_worktree_matches_implementation_source": True,
            }
        )
        probes.append(
            {
                "path": path,
                "mutation": "toggle first byte or add bytes when empty",
                "route_b_required": True,
            }
        )
    return records, probes


def _function_closure(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for category, path, symbol in SEMANTIC_FUNCTIONS:
        hashes = {
            name: _definition_sha(_git_file(root, commit, path), path, symbol)
            for name, commit in ANCHORS
        }
        post_acceptance = {
            hashes["checkpoint5_acceptance_source"],
            hashes["checkpoint6_implementation_source"],
            hashes["checkpoint6_submission_source"],
        }
        if len(post_acceptance) != 1:
            raise RouteBRequiredError(
                f"replay semantic function changed after acceptance: {path}:{symbol}"
            )
        records.append(
            {
                "category": category,
                "path": path,
                "symbol": symbol,
                "ast_sha256_by_source": hashes,
                "ast_identical_acceptance_implementation_submission": True,
            }
        )
    return records


def _validate_receipts_at_implementation(root: Path) -> dict[str, Any]:
    index_bytes = _git_file(root, IMPLEMENTATION_SOURCE, INDEX_PATH)
    index = json.loads(index_bytes)
    if not isinstance(index, dict):
        raise ReplayClosureError("implementation replay index is not an object")
    _self_hash(index, "index_sha256")
    source = index.get("source_verification")
    if not isinstance(source, dict):
        raise ReplayClosureError("implementation index omits source verification")
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
        raise ReplayClosureError("implementation index does not bind nine receipts")
    receipts: dict[str, dict[str, Any]] = {}
    records: list[dict[str, Any]] = []
    for reference in references:
        receipt_id = cast(str, reference["receipt_id"])
        path = f"{REPLAY_ROOT}/receipts/{receipt_id}.json"
        data = _git_file(root, IMPLEMENTATION_SOURCE, path)
        payload = json.loads(data)
        if not isinstance(payload, dict):
            raise ReplayClosureError(f"receipt is not an object: {receipt_id}")
        expectation = expectations.get(receipt_id)
        if expectation is None:
            raise ReplayClosureError(f"receipt has no expectation: {receipt_id}")
        replay._validate_receipt(context, expectation, payload)
        if payload["receipt_sha256"] != reference["receipt_sha256"]:
            raise ReplayClosureError(f"receipt/index hash mismatch: {receipt_id}")
        blobs = {
            name: _git_text(root, ("rev-parse", f"{commit}:{path}"))
            for name, commit in ANCHORS[1:]
        }
        if len(set(blobs.values())) != 1:
            raise RouteBRequiredError(f"immutable receipt bytes changed: {receipt_id}")
        receipts[receipt_id] = payload
        records.append(
            {
                "receipt_id": receipt_id,
                "receipt_sha256": payload["receipt_sha256"],
                "file_sha256": _sha256(data),
                "git_blob_oid_by_source": blobs,
                "byte_identical_acceptance_implementation_submission": True,
                "implementation_validator_status": "passed",
            }
        )
    rebuilt = replay.build_aggregate_index(context, receipts)
    if rebuilt != index or canonical_json_bytes(rebuilt) + b"\n" != index_bytes:
        raise RouteBRequiredError("implementation index does not reproduce byte-for-byte")
    index_blobs = {
        name: _git_text(root, ("rev-parse", f"{commit}:{INDEX_PATH}"))
        for name, commit in ANCHORS[1:]
    }
    if len(set(index_blobs.values())) != 1:
        raise RouteBRequiredError("immutable replay index changed")

    probe_id = cast(str, references[0]["receipt_id"])
    probe = deepcopy(receipts[probe_id])
    fixture_input = cast(dict[str, Any], probe["fixture_input"])
    candidate_dates = cast(list[str], fixture_input["source_candidate_dates"])
    candidate_dates[0] = "2099-01-01"
    unhashed = dict(probe)
    unhashed.pop("receipt_sha256", None)
    probe["receipt_sha256"] = sha256_json(unhashed)
    failure: str | None = None
    try:
        replay._validate_receipt(context, expectations[probe_id], probe)
    except replay.ReplayValidationError as exc:
        failure = str(exc)
    if failure != "replay receipt fixture input mismatch":
        raise ReplayClosureError("semantic receipt mutation did not fail at exact binding")
    return {
        "validated_source": IMPLEMENTATION_SOURCE,
        "receipt_count": len(records),
        "receipt_records": records,
        "all_nine_receipts_valid": True,
        "rebuilt_index_byte_equivalent": True,
        "index_git_blob_oid_by_source": index_blobs,
        "index_sha256": rebuilt["index_sha256"],
        "aggregate_sha256": rebuilt["aggregate_sha256"],
        "semantic_input_mutation_probe": {
            "receipt_id": probe_id,
            "mutated_field": "fixture_input.source_candidate_dates[0]",
            "receipt_self_hash_recomputed": True,
            "rejected": True,
            "failure": failure,
        },
    }


def build_replay_closure(repository_root: Path) -> dict[str, Any]:
    """Build the exact checkpoint-6 replay closure or require Route B."""

    root = repository_root.resolve(strict=True)
    for (_before_name, before), (_after_name, after) in zip(
        ANCHORS, ANCHORS[1:], strict=False
    ):
        _require_ancestor(root, before, after)
    submission = _commit_record(root, SUBMISSION_SOURCE)
    if submission["parents"] != [IMPLEMENTATION_SOURCE]:
        raise ReplayClosureError("checkpoint-6 submission is not the direct implementation child")
    doc_delta = _name_status(root, IMPLEMENTATION_SOURCE, SUBMISSION_SOURCE)
    if doc_delta != [{"status": "A", "path": SUBMISSION_DOC}]:
        raise ReplayClosureError("checkpoint-6 submission delta is not documentation-only")

    prior = json.loads(_git_file(root, IMPLEMENTATION_SOURCE, PRIOR_ATTESTATION_PATH))
    if not isinstance(prior, dict):
        raise ReplayClosureError("prior replay attestation is not an object")
    prior_sha = _self_hash(prior, "attestation_sha256")
    if (root / PRIOR_ATTESTATION_PATH).read_bytes() != _git_file(
        root, IMPLEMENTATION_SOURCE, PRIOR_ATTESTATION_PATH
    ):
        raise ReplayClosureError("prior replay attestation was overwritten")

    source_manifest, paths = _source_manifest(root)
    file_records, mutation_probes = _file_closure(root, paths)
    function_records = _function_closure(root)
    full_delta = _name_status(root, ACCEPTANCE_SOURCE, IMPLEMENTATION_SOURCE)
    replay_delta = [item for item in full_delta if item["path"] in set(paths)]
    if replay_delta:
        raise RouteBRequiredError(
            f"replay-affecting path changed after acceptance: {replay_delta}"
        )
    validation = _validate_receipts_at_implementation(root)

    payload: dict[str, Any] = {
        "schema_version": "natal-time-checkpoint6-final-replay-source-closure-v1",
        "synthetic_only": True,
        "route_decision": {
            "route": "A_final_source_equivalence",
            "route_a_established": True,
            "route_b_regeneration_required": False,
            "basis": (
                "All 58 replay-affecting files and 28 explicitly inventoried semantic functions "
                "are byte/AST identical at the checkpoint-5 acceptance, checkpoint-6 "
                "implementation, and documentation-only submission sources."
            ),
        },
        "anchors": {name: _commit_record(root, commit) for name, commit in ANCHORS},
        "ancestor_chain_verified": True,
        "submission_direct_parent_verified": True,
        "submission_documentation_only_delta": doc_delta,
        "prior_checkpoint5_attestation": {
            "path": PRIOR_ATTESTATION_PATH,
            "attestation_sha256": prior_sha,
            "git_blob_oid_at_implementation": _git_text(
                root,
                ("rev-parse", f"{IMPLEMENTATION_SOURCE}:{PRIOR_ATTESTATION_PATH}"),
            ),
            "preserved_not_overwritten": True,
        },
        "source_manifest_binding": {
            "path": SOURCE_MANIFEST_PATH,
            "manifest_sha256": source_manifest["manifest_sha256"],
            "replay_affecting_file_count": len(paths),
        },
        "replay_affecting_file_inventory": file_records,
        "replay_affecting_file_count": len(file_records),
        "semantic_function_inventory": function_records,
        "semantic_function_count": len(function_records),
        "acceptance_to_implementation_delta": {
            "changed_path_count": len(full_delta),
            "changed_paths": full_delta,
            "changed_paths_sha256": sha256_json(full_delta),
            "replay_affecting_intersection": replay_delta,
            "replay_affecting_intersection_count": 0,
            "classification": "outside_closed_replay_affecting_inventory",
        },
        "semantic_byte_mutation_probes": mutation_probes,
        "semantic_byte_mutation_probe_count": len(mutation_probes),
        "implementation_source_validation": validation,
        "assertions": {
            "all_four_anchors_form_ancestor_chain": True,
            "implementation_is_direct_parent_of_submission": True,
            "submission_delta_is_only_checkpoint_document": True,
            "all_replay_affecting_bytes_identical_acceptance_through_submission": True,
            "all_semantic_functions_identical_acceptance_through_submission": True,
            "every_semantic_byte_probe_forces_route_b": True,
            "all_nine_receipts_validate_at_implementation_source": True,
            "index_and_aggregate_reproduce_at_implementation_source": True,
            "semantic_input_mutation_fails_closed": True,
            "prior_attestation_and_receipts_preserved": True,
            "no_replay_receipt_relabeling": True,
        },
        "claim_limits": [
            "This closure establishes source equivalence only for the exact committed anchors.",
            "It does not rerun astronomy, regenerate receipts, or change their source label.",
            "Any later replay-affecting byte change requires Route B review.",
            "No inference, ranking, participant workflow, or live record is in scope.",
        ],
    }
    payload["closure_sha256"] = sha256_json(payload)
    return payload


def validate_replay_closure(root: Path, payload: dict[str, Any]) -> None:
    _self_hash(payload, "closure_sha256")
    if payload != build_replay_closure(root):
        raise ReplayClosureError("final replay-source closure does not reproduce exactly")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("state/NATAL-TIME-CHECKPOINT6-FINAL-REPLAY-SOURCE-CLOSURE.json"),
    )
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    root = args.repository_root.resolve(strict=True)
    output = args.output if args.output.is_absolute() else root / args.output
    if args.validate_only:
        payload = json.loads(output.read_bytes())
        if not isinstance(payload, dict):
            raise ReplayClosureError("saved final replay closure is not an object")
        validate_replay_closure(root, payload)
        print("CHECKPOINT6_FINAL_REPLAY_SOURCE_CLOSURE_OK")
        return 0
    payload = build_replay_closure(root)
    write_new_bytes(output, canonical_json_bytes(payload) + b"\n")
    print(f"CHECKPOINT6_REPLAY_CLOSURE_SHA256:{payload['closure_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
