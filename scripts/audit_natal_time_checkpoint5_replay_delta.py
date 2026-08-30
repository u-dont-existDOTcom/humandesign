"""Build the checkpoint-5 post-closure replay-delta attestation."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.natal_time import replay as acceptance_replay
from hdmatch.util import canonical_json_bytes, sha256_json

RECEIPT_SOURCE = "1c59b8aae3c096c84a8116d49c0cb0525029837e"
EVALUATED_SOURCE = "90220a3d67e847d883b2060fa3578fe5026cc414"
OPERATIONAL_SOURCE = "b3e5314f8f0cc611ea1b3784bc55c798323ae1d3"
PHASE1_SOURCE = "3c12801a8ec44e97579f869a96643aebc24a37f9"
ACCEPTANCE_SOURCE = "2f707858425cb51f61c5d57e6a0364faf092b841"

REPLAY_PATH = "src/hdmatch/natal_time/replay.py"
SOURCE_MANIFEST_PATH = "state/NATAL-TIME-REPLAY-SOURCE-MANIFEST-V1.json"
FIXTURE_PATH = "state/NATAL-TIME-REAL-ENGINE-FIXTURES.json"
IDENTITY_PATH = "state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json"
REPLAY_ROOT = "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1"
INDEX_PATH = f"{REPLAY_ROOT}/index.json"

ANCHORS = (
    ("receipt_source", RECEIPT_SOURCE),
    ("evaluated_source", EVALUATED_SOURCE),
    ("operational_source", OPERATIONAL_SOURCE),
    ("phase1_source", PHASE1_SOURCE),
    ("acceptance_source", ACCEPTANCE_SOURCE),
)

PAIRS = (
    ("receipt_to_evaluated", RECEIPT_SOURCE, EVALUATED_SOURCE),
    ("evaluated_to_operational", EVALUATED_SOURCE, OPERATIONAL_SOURCE),
    ("operational_to_phase1", OPERATIONAL_SOURCE, PHASE1_SOURCE),
    ("phase1_to_acceptance", PHASE1_SOURCE, ACCEPTANCE_SOURCE),
)

PRO_CATEGORIES = (
    "scientific_engine_input",
    "fixture_definition",
    "event_interval_construction",
    "receipt_semantic_construction",
    "canonical_serialization",
    "digest_construction",
    "independent_verification",
    "resumption_durability_orchestration_only",
    "test_documentation_output_only",
)

SEMANTIC_SURFACES = (
    (
        "scientific_engine_input",
        REPLAY_PATH,
        "real_engine_fixture_executor",
    ),
    (
        "scientific_engine_input",
        "src/hdmatch/runtime/chart_adapter.py",
        "ExactChartAdapter",
    ),
    (
        "scientific_engine_input",
        "src/hdmatch/chart/calculator.py",
        "calculate_chart",
    ),
    ("fixture_definition", REPLAY_PATH, "_build_expectations"),
    ("fixture_definition", REPLAY_PATH, "_execute_fail_closed"),
    ("event_interval_construction", REPLAY_PATH, "real_engine_fixture_executor"),
    ("event_interval_construction", REPLAY_PATH, "_event_key"),
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
    ("receipt_semantic_construction", REPLAY_PATH, "ReplayExpectation"),
    ("receipt_semantic_construction", REPLAY_PATH, "make_receipt"),
    ("receipt_semantic_construction", REPLAY_PATH, "_validate_receipt"),
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
    ("digest_construction", REPLAY_PATH, "make_receipt"),
    ("digest_construction", REPLAY_PATH, "build_aggregate_index"),
    ("digest_construction", "src/hdmatch/util/canonical.py", "sha256_json"),
    ("independent_verification", REPLAY_PATH, "_independent_verification"),
    (
        "independent_verification",
        "src/hdmatch/natal_time/conformance.py",
        "independently_enumerate_line_transitions",
    ),
)


class ReplayDeltaError(ValueError):
    """Raised when the post-closure replay attestation cannot validate."""


class RouteBRequiredError(ReplayDeltaError):
    """Raised when a receipt-semantic change prevents Route A."""


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


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _self_hash(value: Mapping[str, Any], field: str) -> str:
    unhashed = dict(value)
    embedded = unhashed.pop(field, None)
    computed = sha256_json(unhashed)
    if embedded != computed:
        raise ReplayDeltaError(f"self-hash mismatch: {field}")
    return computed


def _commit_record(root: Path, commit: str) -> dict[str, Any]:
    return {
        "commit": commit,
        "tree_oid": _git_text(root, ["rev-parse", f"{commit}^{{tree}}"]),
        "parents": _git_text(root, ["show", "-s", "--format=%P", commit]).split(),
        "subject": _git_text(root, ["show", "-s", "--format=%s", commit]),
    }


def _name_status(root: Path, before: str, after: str) -> list[dict[str, str]]:
    raw = _git_bytes(
        root, ["diff", "--no-renames", "--name-status", "-z", before, after]
    )
    tokens = [token for token in raw.split(b"\0") if token]
    if len(tokens) % 2:
        raise ReplayDeltaError("incomplete name-status record")
    return [
        {"status": status.decode("ascii"), "path": path.decode("utf-8")}
        for status, path in zip(tokens[::2], tokens[1::2], strict=True)
    ]


def _definition_nodes(source: bytes, path: str) -> dict[str, ast.AST]:
    tree = ast.parse(source, filename=path)
    result: dict[str, ast.AST] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name in result:
                raise ReplayDeltaError(f"duplicate top-level definition: {path}:{node.name}")
            result[node.name] = node
    return result


def _ast_sha(node: ast.AST) -> str:
    return _sha256(ast.dump(node, include_attributes=False).encode("utf-8"))


def _definition_record(root: Path, commit: str, path: str, symbol: str) -> dict[str, str]:
    nodes = _definition_nodes(_git_file(root, commit, path), path)
    node = nodes.get(symbol)
    if node is None:
        raise ReplayDeltaError(f"missing semantic symbol: {path}:{symbol}@{commit}")
    return {"commit": commit, "ast_sha256": _ast_sha(node)}


def _module_nondefinition_sha(source: bytes, path: str) -> str:
    tree = ast.parse(source, filename=path)
    tree.body = [
        node
        for node in tree.body
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    ]
    return _ast_sha(tree)


def _successful_json_loader_sha(node: ast.AST) -> str:
    clone = deepcopy(node)
    if not isinstance(clone, ast.FunctionDef):
        raise ReplayDeltaError("JSON loader is not a function")
    if clone.body and isinstance(clone.body[0], ast.Try):
        wrapper = clone.body[0]
        if len(wrapper.body) != 1 or wrapper.orelse or wrapper.finalbody:
            raise RouteBRequiredError("JSON loader try wrapper changes its successful path")
        if len(wrapper.handlers) != 1:
            raise RouteBRequiredError("JSON loader has an unexpected handler shape")
        handler = wrapper.handlers[0]
        if handler.type is None:
            raise RouteBRequiredError("JSON loader uses an unbounded exception handler")
        caught = ast.dump(handler.type, include_attributes=False)
        required = ast.dump(
            ast.Tuple(
                elts=[
                    ast.Attribute(
                        ast.Name("json", ctx=ast.Load()),
                        "JSONDecodeError",
                        ctx=ast.Load(),
                    ),
                    ast.Name("UnicodeDecodeError", ctx=ast.Load()),
                    ast.Name("OSError", ctx=ast.Load()),
                ],
                ctx=ast.Load(),
            ),
            include_attributes=False,
        )
        if caught != required:
            raise RouteBRequiredError("JSON loader catches an unexpected exception set")
        if len(handler.body) != 1 or not isinstance(handler.body[0], ast.Raise):
            raise RouteBRequiredError(
                "JSON loader exception path is not a single fail-closed raise"
            )
        raised = handler.body[0]
        if (
            not isinstance(raised.exc, ast.Call)
            or not isinstance(raised.exc.func, ast.Name)
            or raised.exc.func.id != "ReplayValidationError"
            or not isinstance(raised.cause, ast.Name)
            or raised.cause.id != "exc"
        ):
            raise RouteBRequiredError(
                "JSON loader exception path does not chain ReplayValidationError"
            )
        clone.body = [*wrapper.body, *clone.body[1:]]
    return _ast_sha(clone)


def _semantic_surface_evidence(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for category, path, symbol in SEMANTIC_SURFACES:
        versions = [
            _definition_record(root, commit, path, symbol) for _name, commit in ANCHORS
        ]
        hashes = {item["ast_sha256"] for item in versions}
        if len(hashes) != 1:
            raise RouteBRequiredError(f"receipt-semantic surface changed: {path}:{symbol}")
        records.append(
            {
                "category": category,
                "path": path,
                "symbol": symbol,
                "versions": versions,
                "ast_identical_across_all_sources": True,
            }
        )
    return records


def _load_source_inventory(root: Path) -> tuple[dict[str, Any], tuple[str, ...]]:
    source_manifest = json.loads(_git_file(root, OPERATIONAL_SOURCE, SOURCE_MANIFEST_PATH))
    if not isinstance(source_manifest, dict):
        raise ReplayDeltaError("source manifest is not an object")
    _self_hash(source_manifest, "manifest_sha256")
    files = source_manifest.get("replay_affecting_files")
    if not isinstance(files, list):
        raise ReplayDeltaError("source manifest file inventory is absent")
    paths = tuple(sorted(cast(str, item["path"]) for item in files))
    if REPLAY_PATH not in paths or FIXTURE_PATH not in paths or IDENTITY_PATH not in paths:
        raise ReplayDeltaError("source inventory omits a required replay input")
    return source_manifest, paths


def _source_delta_evidence(root: Path, paths: tuple[str, ...]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    changed: list[str] = []
    for path in paths:
        versions = [
            {
                "commit": commit,
                "git_blob_oid": _git_text(root, ["rev-parse", f"{commit}:{path}"]),
                "sha256": _sha256(_git_file(root, commit, path)),
            }
            for _name, commit in ANCHORS
        ]
        unique = {item["sha256"] for item in versions}
        if len(unique) > 1:
            changed.append(path)
        records.append(
            {
                "path": path,
                "versions": versions,
                "byte_identical_across_all_sources": len(unique) == 1,
            }
        )
    if changed != [REPLAY_PATH]:
        raise RouteBRequiredError(f"unexpected replay-affecting path delta: {changed}")

    replay_definitions = {
        name: {
            symbol: _ast_sha(node)
            for symbol, node in _definition_nodes(
                _git_file(root, commit, REPLAY_PATH), REPLAY_PATH
            ).items()
        }
        for name, commit in ANCHORS
    }
    symbol_names = set(replay_definitions["receipt_source"])
    if any(set(value) != symbol_names for value in replay_definitions.values()):
        raise RouteBRequiredError("replay top-level definition inventory changed")
    changed_symbols = sorted(
        symbol
        for symbol in symbol_names
        if len({value[symbol] for value in replay_definitions.values()}) > 1
    )
    if changed_symbols != ["_load_json_object"]:
        raise RouteBRequiredError(f"unexpected changed replay definitions: {changed_symbols}")

    module_static = {
        name: _module_nondefinition_sha(_git_file(root, commit, REPLAY_PATH), REPLAY_PATH)
        for name, commit in ANCHORS
    }
    if len(set(module_static.values())) != 1:
        raise RouteBRequiredError("replay module imports/constants changed")
    loader_versions = {
        name: _definition_nodes(_git_file(root, commit, REPLAY_PATH), REPLAY_PATH)[
            "_load_json_object"
        ]
        for name, commit in ANCHORS
    }
    normalized = {name: _successful_json_loader_sha(node) for name, node in loader_versions.items()}
    if len(set(normalized.values())) != 1:
        raise RouteBRequiredError("JSON loader successful-path semantics changed")
    return {
        "replay_affecting_path_count": len(records),
        "path_records": records,
        "changed_replay_affecting_paths": changed,
        "changed_replay_definitions": [
            {
                "path": REPLAY_PATH,
                "symbol": "_load_json_object",
                "category": "resumption_durability_orchestration_only",
                "rationale": (
                    "Wraps invalid JSON, Unicode, and filesystem read failures in the existing "
                    "fail-closed ReplayValidationError; successful object loading is mechanically "
                    "AST-equivalent."
                ),
                "raw_ast_sha256_by_source": {
                    name: _ast_sha(node) for name, node in loader_versions.items()
                },
                "successful_path_ast_sha256_by_source": normalized,
                "successful_path_mechanically_equivalent": True,
                "receipt_semantic_construction_changed": False,
            }
        ],
        "module_imports_and_constants_ast_sha256_by_source": module_static,
        "module_imports_and_constants_identical": True,
    }


def _classify_changed_path(path: str) -> tuple[str, str]:
    if path == REPLAY_PATH:
        return (
            "resumption_durability_orchestration_only",
            "Only _load_json_object changed; its valid-input path is mechanically equivalent.",
        )
    return (
        "test_documentation_output_only",
        (
            "Outside the replay-affecting import/input inventory, or an immutable replay output; "
            "therefore it cannot change receipt construction under the attested source route."
        ),
    )


def _changed_path_evidence(root: Path) -> list[dict[str, Any]]:
    pair_records: list[dict[str, Any]] = []
    for pair_id, before, after in PAIRS:
        changed = _name_status(root, before, after)
        classified = []
        for item in changed:
            category, rationale = _classify_changed_path(item["path"])
            if category not in PRO_CATEGORIES:
                raise ReplayDeltaError(f"unknown Pro category: {category}")
            classified.append({**item, "category": category, "rationale": rationale})
        pair_records.append(
            {
                "pair_id": pair_id,
                "from_commit": before,
                "to_commit": after,
                "changed_path_count": len(classified),
                "changed_paths": classified,
                "changed_paths_sha256": sha256_json(classified),
            }
        )
    return pair_records


def _verify_source_receipt(root: Path, source: Mapping[str, Any]) -> None:
    unhashed = dict(source)
    embedded = unhashed.pop("source_verification_sha256", None)
    if embedded != sha256_json(unhashed):
        raise ReplayDeltaError("source verification self-hash mismatch")
    if (
        source.get("repository_commit") != RECEIPT_SOURCE
        or source.get("commit_tree_oid")
        != _git_text(root, ["rev-parse", f"{RECEIPT_SOURCE}^{{tree}}"])
    ):
        raise ReplayDeltaError("source verification does not bind the receipt source tree")


def _acceptance_validator_evidence(
    root: Path, replay_affecting_paths: tuple[str, ...]
) -> dict[str, Any]:
    acceptance_bytes = _git_file(root, ACCEPTANCE_SOURCE, REPLAY_PATH)
    for path in replay_affecting_paths:
        if (root / path).read_bytes() != _git_file(root, ACCEPTANCE_SOURCE, path):
            raise ReplayDeltaError(
                f"loaded replay runtime differs from acceptance-source bytes: {path}"
            )
    index_bytes = _git_file(root, ACCEPTANCE_SOURCE, INDEX_PATH)
    index = json.loads(index_bytes)
    if not isinstance(index, dict):
        raise ReplayDeltaError("committed replay index is not an object")
    _self_hash(index, "index_sha256")
    source = index.get("source_verification")
    if not isinstance(source, dict):
        raise ReplayDeltaError("replay index source verification is absent")
    _verify_source_receipt(root, source)
    for path in (FIXTURE_PATH, IDENTITY_PATH):
        if (root / path).read_bytes() != _git_file(root, ACCEPTANCE_SOURCE, path):
            raise ReplayDeltaError(f"worktree pinned input differs from acceptance source: {path}")
    context = acceptance_replay._load_pinned_context(
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
        raise ReplayDeltaError("index does not bind nine receipts")
    expected_receipt_paths = sorted(
        f"{REPLAY_ROOT}/receipts/{item['receipt_id']}.json" for item in references
    )
    actual_receipt_paths = sorted(
        _git_text(
            root,
            [
                "ls-tree",
                "-r",
                "--name-only",
                ACCEPTANCE_SOURCE,
                f"{REPLAY_ROOT}/receipts",
            ],
        ).splitlines()
    )
    if actual_receipt_paths != expected_receipt_paths:
        raise ReplayDeltaError("acceptance receipt directory has missing or extra files")
    receipts: dict[str, dict[str, Any]] = {}
    receipt_records: list[dict[str, Any]] = []
    for reference in references:
        receipt_id = cast(str, reference["receipt_id"])
        path = f"{REPLAY_ROOT}/receipts/{receipt_id}.json"
        data = _git_file(root, ACCEPTANCE_SOURCE, path)
        payload = json.loads(data)
        if not isinstance(payload, dict):
            raise ReplayDeltaError(f"receipt is not an object: {receipt_id}")
        expectation = expectations.get(receipt_id)
        if expectation is None:
            raise ReplayDeltaError(f"receipt has no acceptance expectation: {receipt_id}")
        acceptance_replay._validate_receipt(context, expectation, payload)
        if payload["receipt_sha256"] != reference["receipt_sha256"]:
            raise ReplayDeltaError(f"receipt/index hash mismatch: {receipt_id}")
        versions = [
            _git_text(root, ["rev-parse", f"{commit}:{path}"])
            for commit in (
                EVALUATED_SOURCE,
                OPERATIONAL_SOURCE,
                PHASE1_SOURCE,
                ACCEPTANCE_SOURCE,
            )
        ]
        if len(set(versions)) != 1:
            raise RouteBRequiredError(f"committed receipt bytes changed: {receipt_id}")
        receipts[receipt_id] = payload
        receipt_records.append(
            {
                "receipt_id": receipt_id,
                "receipt_sha256": payload["receipt_sha256"],
                "file_sha256": _sha256(data),
                "git_blob_oid": versions[0],
                "byte_identical_evaluated_through_acceptance": True,
                "acceptance_validator_status": "passed",
            }
        )
    rebuilt = acceptance_replay.build_aggregate_index(context, receipts)
    if rebuilt != index or canonical_json_bytes(rebuilt) + b"\n" != index_bytes:
        raise RouteBRequiredError("acceptance-source index reconstruction differs")
    index_blobs = {
        name: _git_text(root, ["rev-parse", f"{commit}:{INDEX_PATH}"])
        for name, commit in ANCHORS[1:]
    }
    if len(set(index_blobs.values())) != 1:
        raise RouteBRequiredError("committed index bytes changed after evaluated source")

    probe_receipt_id = cast(str, references[0]["receipt_id"])
    probe = deepcopy(receipts[probe_receipt_id])
    fixture_input = cast(dict[str, Any], probe["fixture_input"])
    candidate_dates = cast(list[str], fixture_input["source_candidate_dates"])
    candidate_dates[0] = "2099-01-01"
    unhashed_probe = dict(probe)
    unhashed_probe.pop("receipt_sha256", None)
    probe["receipt_sha256"] = sha256_json(unhashed_probe)
    mutation_failure: str | None = None
    try:
        acceptance_replay._validate_receipt(
            context, expectations[probe_receipt_id], probe
        )
    except acceptance_replay.ReplayValidationError as exc:
        mutation_failure = str(exc)
    if mutation_failure != "replay receipt fixture input mismatch":
        raise RouteBRequiredError("semantic-input mutation did not fail at its exact binding")
    return {
        "acceptance_validator_path": REPLAY_PATH,
        "acceptance_validator_file_sha256": _sha256(acceptance_bytes),
        "acceptance_runtime_surface_file_count": len(replay_affecting_paths),
        "acceptance_runtime_surface_matches_git_source": True,
        "receipt_count": len(receipt_records),
        "receipt_records": receipt_records,
        "all_nine_receipts_valid": True,
        "rebuilt_index_byte_equivalent": True,
        "index_git_blob_oid_by_source": index_blobs,
        "index_byte_identical_evaluated_through_acceptance": True,
        "index_sha256": rebuilt["index_sha256"],
        "aggregate_sha256": rebuilt["aggregate_sha256"],
        "semantic_input_mutation_probe": {
            "receipt_id": probe_receipt_id,
            "mutated_field": "fixture_input.source_candidate_dates[0]",
            "receipt_self_hash_recomputed_after_mutation": True,
            "acceptance_validator_rejected": True,
            "failure": mutation_failure,
        },
    }


def build_replay_delta_attestation(repository_root: Path) -> dict[str, Any]:
    """Build Route-A evidence or fail with RouteBRequiredError."""

    root = repository_root.resolve(strict=True)
    source_manifest, paths = _load_source_inventory(root)
    source_delta = _source_delta_evidence(root, paths)
    semantic_surfaces = _semantic_surface_evidence(root)
    acceptance = _acceptance_validator_evidence(root, paths)
    path_evidence = _changed_path_evidence(root)
    payload: dict[str, Any] = {
        "schema_version": "natal-time-checkpoint5-post-closure-replay-delta-v1",
        "route_decision": {
            "route": "A_equivalence_proof",
            "route_a_established": True,
            "route_b_regeneration_required": False,
            "basis": (
                "The only replay-affecting delta is fail-closed JSON-read validation. All "
                "receipt-semantic AST surfaces and pinned inputs are unchanged; acceptance-source "
                "validation reproduces the nine receipts, index, aggregate, and mutation failure."
            ),
        },
        "anchors": {name: _commit_record(root, commit) for name, commit in ANCHORS},
        "pro_classification_categories": list(PRO_CATEGORIES),
        "pairwise_changed_path_classification": path_evidence,
        "prior_source_manifest_binding": {
            "path": SOURCE_MANIFEST_PATH,
            "manifest_sha256": source_manifest["manifest_sha256"],
            "replay_affecting_file_count": len(paths),
        },
        "replay_source_delta": source_delta,
        "receipt_semantic_surface_evidence": semantic_surfaces,
        "receipt_semantic_surface_count": len(semantic_surfaces),
        "frozen_inputs": [],
        "acceptance_source_validation": acceptance,
        "assertions": {
            "replay_import_and_input_inventory_unchanged": True,
            "only_json_loader_validation_changed": True,
            "json_loader_successful_path_mechanically_equivalent": True,
            "engine_invocation_unchanged": True,
            "fixture_inputs_unchanged": True,
            "event_and_interval_construction_unchanged": True,
            "receipt_semantic_fields_unchanged": True,
            "canonicalization_unchanged": True,
            "digest_construction_unchanged": True,
            "independent_verification_unchanged": True,
            "all_nine_receipts_validate_at_acceptance_source": True,
            "index_and_aggregate_reproduce_exactly": True,
            "semantic_input_mutation_fails_closed": True,
        },
        "claim_limits": [
            "Route A applies only to the exact five attested sources and committed replay bytes.",
            "The attestation does not rerun astronomy or relabel the receipt source commit.",
            "Any future receipt-semantic delta requires Route B review and new immutable outputs.",
        ],
    }
    for path in (FIXTURE_PATH, IDENTITY_PATH):
        hashes = {
            name: _sha256(_git_file(root, commit, path)) for name, commit in ANCHORS
        }
        if len(set(hashes.values())) != 1:
            raise RouteBRequiredError(f"frozen replay input changed: {path}")
        cast(list[dict[str, Any]], payload["frozen_inputs"]).append(
            {
                "path": path,
                "sha256_by_source": hashes,
                "byte_identical_across_all_sources": True,
            }
        )
    payload["attestation_sha256"] = sha256_json(payload)
    return payload


def validate_replay_delta_attestation(root: Path, payload: dict[str, Any]) -> None:
    _self_hash(payload, "attestation_sha256")
    if payload != build_replay_delta_attestation(root):
        raise ReplayDeltaError("post-closure replay attestation does not reproduce exactly")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("state/NATAL-TIME-CHECKPOINT5-REPLAY-DELTA-ATTESTATION.json"),
    )
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    root = args.repository_root.resolve(strict=True)
    output = args.output if args.output.is_absolute() else root / args.output
    if args.validate_only:
        value = json.loads(output.read_bytes())
        if not isinstance(value, dict):
            raise ReplayDeltaError("saved replay attestation is not an object")
        validate_replay_delta_attestation(root, value)
        print("CHECKPOINT5_REPLAY_DELTA_ATTESTATION_OK")
        return 0
    payload = build_replay_delta_attestation(root)
    write_new_bytes(output, canonical_json_bytes(payload) + b"\n")
    print(f"REPLAY_DELTA_ATTESTATION_SHA256:{payload['attestation_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
