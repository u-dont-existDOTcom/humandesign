#!/usr/bin/env python3
"""Generate the mechanical final convergence audit for AstroHD draft PR #23."""

from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import importlib.util
import json
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "afc0bb82de0e481ae5a5d3453e0bcaf82b2a0286"
AUDITED_HEAD = "b3da97274c161a31e44cee3ef4159ca0d1d9a0dd"
RANK_CORRECTION_START = "f5a967c2efbb0f73a7a56c42a06fe4d7fb7e2b59"
OUTPUT_PATH = Path("reference/audits/astrohd_pr23_convergence_v1.json")

MAPPING_PATH = Path("mappings/mapping_library_v1.json")
QUESTION_BANK_PATH = Path("reference/core/question_bank_v1.json")
FUTURE_CORE_PATH = Path("reference/research/astrohd_future_core_coverage_candidate_matrix_v1.json")
CROSS_CLASS_AUDIT_PATH = Path("reference/audits/astrohd_cross_class_core_fit_v1.json")
DOWNSTREAM_AUDIT_PATH = Path("reference/audits/astrohd_rank_tiebreak_downstream_v1.json")
THEORY_LANGUAGE_MODULE_PATH = Path("src/hdmatch/evaluation/theory_language_exposure.py")
PARTICIPANT_BACKEND_PATH = Path("src/hdmatch/participant/backend.py")
DATE_AGGREGATOR_PATH = Path("src/hdmatch/search/date_aggregator.py")

EXPECTED_MAPPING_SHA256 = "3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200"
EXPECTED_QUESTION_BANK_SHA256 = "31f813efc3da7263569ef010a8336b1b1b0c44801b7aa0f91e33b3fa4587d820"
EXPECTED_CROSS_CLASS_AUDIT_SHA256 = (
    "a113fb53de13f38d5053955975912a1fb194f527c57f610c82d0efc38bc32a70"
)
EXPECTED_DOWNSTREAM_AUDIT_SHA256 = (
    "c9fb9ee6060c4bbb346c7ac6981a543d3d602a60bb1da83e245cea638a680103"
)

REMNANT_TERMS = (
    "completion_policy",
    "completion policy",
    "completion-policy",
    "completionPolicy",
    "required_question_count",
    "target_question_count",
    "questionnaire_complete",
    "questionnaire_incomplete",
    "23-versus-76",
    "23 vs 76",
    "76-item acceptance",
    "76 item acceptance",
)
RUNTIME_IDENTIFIER_FRAGMENTS = (
    "completion_policy",
    "completion_requirement",
    "required_question",
    "questionnaire_complete",
    "unresolved_policy",
)
COORDINATION_DOCUMENTS = (
    Path("CURRENT_PLAN.md"),
    Path("docs/36_astrohd_owner_pilot.md"),
    Path("state/CURRENT-STATE.md"),
    Path("state/OWNER-CORRECTION-2026-09-02.md"),
)

JsonObject = dict[str, Any]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def render_json(payload: JsonObject) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def _git(repository_root: Path, *arguments: str) -> bytes:
    completed = subprocess.run(
        ("git", *arguments),
        cwd=repository_root,
        check=True,
        capture_output=True,
    )
    return completed.stdout


def _git_blob(repository_root: Path, ref: str, path: Path) -> bytes:
    return _git(repository_root, "show", f"{ref}:{path.as_posix()}")


def _git_paths(repository_root: Path, ref: str) -> tuple[str, ...]:
    output = _git(repository_root, "ls-tree", "-r", "--name-only", ref).decode()
    return tuple(path for path in output.splitlines() if path)


def _path_category(path: str) -> str:
    for prefix in ("src", "tests", "scripts", "reference", "docs", "state"):
        if path == prefix or path.startswith(f"{prefix}/"):
            return prefix
    return "repository_root_or_other"


def _pr_delta_inventory(repository_root: Path) -> JsonObject:
    raw = _git(
        repository_root,
        "diff",
        "--name-status",
        "--find-renames",
        f"{BASE_COMMIT}...{AUDITED_HEAD}",
    ).decode()
    rows: list[JsonObject] = []
    for line in raw.splitlines():
        fields = line.split("\t")
        status = fields[0]
        path = fields[-1]
        row: JsonObject = {
            "category": _path_category(path),
            "path": path,
            "sha256": None
            if status.startswith("D")
            else sha256_bytes(_git_blob(repository_root, AUDITED_HEAD, Path(path))),
            "status": status,
        }
        if status.startswith(("R", "C")):
            row["previous_path"] = fields[1]
        rows.append(row)
    counts = Counter(str(row["category"]) for row in rows)
    return {
        "category_counts": {
            category: counts.get(category, 0)
            for category in (
                "src",
                "tests",
                "scripts",
                "reference",
                "docs",
                "state",
                "repository_root_or_other",
            )
        },
        "changed_file_count": len(rows),
        "files": rows,
        "range": f"{BASE_COMMIT}...{AUDITED_HEAD}",
    }


def _active_scan_paths(all_paths: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        path
        for path in all_paths
        if (path.startswith("src/hdmatch/") and path.endswith(".py"))
        or path.startswith("reference/custom_gpt/")
        or path in {"docs/36_astrohd_owner_pilot.md", "CURRENT_PLAN.md"}
    )


def _literal_occurrences(
    repository_root: Path,
    paths: tuple[str, ...],
    terms: tuple[str, ...],
) -> list[JsonObject]:
    rows: list[JsonObject] = []
    for path in paths:
        source = _git_blob(repository_root, AUDITED_HEAD, Path(path)).decode("utf-8")
        for line_number, line in enumerate(source.splitlines(), start=1):
            folded_line = line.casefold()
            for term in terms:
                folded_term = term.casefold()
                start = 0
                while True:
                    column = folded_line.find(folded_term, start)
                    if column < 0:
                        break
                    rows.append(
                        {
                            "column": column + 1,
                            "line": line_number,
                            "matched_term": term,
                            "minimal_excerpt": line.strip(),
                            "path": path,
                        }
                    )
                    start = column + max(1, len(folded_term))
    return rows


def _owner_correction_remnant_scan(repository_root: Path) -> JsonObject:
    all_paths = _git_paths(repository_root, AUDITED_HEAD)
    active_paths = _active_scan_paths(all_paths)
    state_paths = tuple(path for path in all_paths if path.startswith("state/"))
    active = _literal_occurrences(repository_root, active_paths, REMNANT_TERMS)
    historical = _literal_occurrences(repository_root, state_paths, REMNANT_TERMS)
    return {
        "active_surfaces": {
            "occurrence_count": len(active),
            "occurrences": active,
            "scanned_file_count": len(active_paths),
            "scanned_paths": list(active_paths),
        },
        "case_handling": "case_insensitive_literal_matching",
        "search_terms": list(REMNANT_TERMS),
        "state_surfaces": {
            "classification": "historical_or_state_records_not_runtime_scan",
            "occurrence_count": len(historical),
            "occurrences": historical,
            "scanned_file_count": len(state_paths),
            "scanned_paths": list(state_paths),
        },
    }


def _matching_identifier(identifier: str) -> bool:
    folded = identifier.casefold()
    return any(fragment.casefold() in folded for fragment in RUNTIME_IDENTIFIER_FRAGMENTS)


def _runtime_symbol_scan(repository_root: Path) -> JsonObject:
    paths = tuple(
        path
        for path in _git_paths(repository_root, AUDITED_HEAD)
        if path.startswith("src/hdmatch/") and path.endswith(".py")
    )
    rows: list[JsonObject] = []
    for path in paths:
        source = _git_blob(repository_root, AUDITED_HEAD, Path(path)).decode("utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            candidates: list[tuple[str, str]] = []
            if isinstance(node, ast.Name):
                context = "definition" if isinstance(node.ctx, ast.Store) else "reference"
                candidates.append((node.id, f"name_{context}"))
            elif isinstance(node, ast.Attribute):
                context = "definition" if isinstance(node.ctx, ast.Store) else "reference"
                candidates.append((node.attr, f"attribute_{context}"))
            elif isinstance(node, ast.arg):
                candidates.append((node.arg, "argument_definition"))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                candidates.append((node.name, "function_definition"))
            elif isinstance(node, ast.ClassDef):
                candidates.append((node.name, "class_definition"))
            elif isinstance(node, ast.alias):
                candidates.append((node.asname or node.name, "import_binding"))
            elif isinstance(node, ast.keyword) and node.arg is not None:
                candidates.append((node.arg, "keyword_reference"))
            for identifier, category in candidates:
                if _matching_identifier(identifier):
                    rows.append(
                        {
                            "identifier": identifier,
                            "line": getattr(node, "lineno", 0),
                            "path": path,
                            "syntactic_category": category,
                        }
                    )
    rows = [
        dict(row)
        for row in sorted(
            {json.dumps(row, sort_keys=True): row for row in rows}.values(),
            key=lambda row: (
                row["path"],
                row["line"],
                row["identifier"],
                row["syntactic_category"],
            ),
        )
    ]
    return {
        "expected_production_runtime_occurrence_count": 0,
        "identifier_fragments": list(RUNTIME_IDENTIFIER_FRAGMENTS),
        "occurrence_count": len(rows),
        "occurrences": rows,
        "scanned_file_count": len(paths),
    }


def _find_function(tree: ast.AST, name: str) -> ast.FunctionDef | ast.AsyncFunctionDef:
    matches = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name == name
    ]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one function named {name}, observed {len(matches)}")
    return matches[0]


def _tuple_expressions(node: ast.AST) -> list[str]:
    if not isinstance(node, ast.Tuple):
        raise ValueError(f"expected tuple expression, observed {type(node).__name__}")
    return [ast.unparse(element) for element in node.elts]


def _call_key_tuple(function: ast.AST, call_name: str) -> list[str]:
    matches: list[ast.Lambda] = []
    for node in ast.walk(function):
        if not isinstance(node, ast.Call):
            continue
        called_name = node.func.id if isinstance(node.func, ast.Name) else None
        if called_name != call_name:
            continue
        for keyword in node.keywords:
            if keyword.arg == "key" and isinstance(keyword.value, ast.Lambda):
                matches.append(keyword.value)
    if len(matches) != 1:
        raise ValueError(f"expected one {call_name} key lambda, observed {len(matches)}")
    return _tuple_expressions(matches[0].body)


def _return_tuple(function: ast.AST) -> list[str]:
    returns = [node for node in ast.walk(function) if isinstance(node, ast.Return)]
    if len(returns) != 1 or returns[0].value is None:
        raise ValueError("expected one return value")
    return _tuple_expressions(returns[0].value)


def _function_source(source: str, name: str) -> str:
    tree = ast.parse(source)
    segment = ast.get_source_segment(source, _find_function(tree, name))
    if segment is None:
        raise ValueError(f"could not extract source for {name}")
    return segment


def _rank_semantics(repository_root: Path) -> JsonObject:
    backend_bytes = _git_blob(repository_root, AUDITED_HEAD, PARTICIPANT_BACKEND_PATH)
    backend_source = backend_bytes.decode("utf-8")
    backend_tree = ast.parse(backend_source)
    rank_function = _find_function(backend_tree, "_rank_states")
    tie_function = _find_function(backend_tree, "_evidence_tie_key")

    top_current = _function_source(backend_source, "_top_net_margin")
    top_baseline_source = _git_blob(
        repository_root, RANK_CORRECTION_START, PARTICIPANT_BACKEND_PATH
    ).decode("utf-8")
    top_baseline = _function_source(top_baseline_source, "_top_net_margin")

    date_current_bytes = _git_blob(repository_root, AUDITED_HEAD, DATE_AGGREGATOR_PATH)
    date_current = date_current_bytes.decode("utf-8")
    date_baseline = _git_blob(repository_root, RANK_CORRECTION_START, DATE_AGGREGATOR_PATH).decode(
        "utf-8"
    )
    date_function = _find_function(ast.parse(date_current), "aggregate_dates")
    date_diff = list(
        difflib.unified_diff(
            date_baseline.splitlines(),
            date_current.splitlines(),
            fromfile=f"{RANK_CORRECTION_START}:{DATE_AGGREGATOR_PATH.as_posix()}",
            tofile=f"{AUDITED_HEAD}:{DATE_AGGREGATOR_PATH.as_posix()}",
            lineterm="",
        )
    )
    directed_line = "                item.core_fit,\n"
    date_only_directed_removal = (
        date_baseline.count(directed_line) == 1
        and date_baseline.replace(directed_line, "", 1) == date_current
    )

    return {
        "date_aggregator": {
            "audited_head_file_sha256": sha256_bytes(date_current_bytes),
            "best_state_key_expressions": _call_key_tuple(date_function, "max"),
            "core_fit_in_best_state_key": "item.core_fit" in _call_key_tuple(date_function, "max"),
            "date_score_and_midrank_source_unchanged_except_directed_core_fit_removal": (
                date_only_directed_removal
            ),
            "diff_from_rank_correction_start": date_diff,
            "path": DATE_AGGREGATOR_PATH.as_posix(),
            "rank_correction_start_file_sha256": sha256_bytes(date_baseline.encode()),
        },
        "participant_backend": {
            "audited_head_file_sha256": sha256_bytes(backend_bytes),
            "core_fit_in_evidence_tie_key": any(
                "core_fit" in expression for expression in _return_tuple(tie_function)
            ),
            "core_fit_in_rank_ordering_key": any(
                "core_fit" in expression for expression in _call_key_tuple(rank_function, "sorted")
            ),
            "evidence_tie_key_expressions": _return_tuple(tie_function),
            "path": PARTICIPANT_BACKEND_PATH.as_posix(),
            "rank_ordering_key_expressions": _call_key_tuple(rank_function, "sorted"),
            "top_net_margin": {
                "audited_head_sha256": sha256_bytes(top_current.encode()),
                "rank_correction_start_sha256": sha256_bytes(top_baseline.encode()),
                "source_excerpt": top_current,
                "unchanged_from_rank_correction_start": top_current == top_baseline,
            },
        },
        "rank_correction_start": RANK_CORRECTION_START,
    }


def _range_contains(node: ast.AST, line: int, column: int) -> bool:
    start_line = getattr(node, "lineno", 0)
    end_line = getattr(node, "end_lineno", start_line)
    if not start_line or not end_line or not (start_line <= line <= end_line):
        return False
    if line == start_line and column < getattr(node, "col_offset", 0):
        return False
    return not (line == end_line and column > getattr(node, "end_col_offset", 10**9))


def _enclosing_name(tree: ast.AST, line: int) -> str:
    classes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
        and node.lineno <= line <= (node.end_lineno or node.lineno)
    ]
    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and node.lineno <= line <= (node.end_lineno or node.lineno)
    ]
    class_node = min(
        classes,
        key=lambda node: (node.end_lineno or node.lineno) - node.lineno,
        default=None,
    )
    function_node = min(
        functions,
        key=lambda node: (node.end_lineno or node.lineno) - node.lineno,
        default=None,
    )
    if class_node is not None and function_node is not None:
        return f"{class_node.name}.{function_node.name}"
    if function_node is not None:
        return function_node.name
    if class_node is not None:
        return class_node.name
    return "<module>"


def _key_contexts(tree: ast.AST) -> tuple[list[ast.AST], list[ast.AST], list[ast.AST]]:
    sort_keys: list[ast.AST] = []
    extrema_keys: list[ast.AST] = []
    rank_keys: list[ast.AST] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name: str | None = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            for keyword in node.keywords:
                if keyword.arg != "key":
                    continue
                if name in {"sorted", "sort"}:
                    sort_keys.append(keyword.value)
                if name in {"max", "min"}:
                    extrema_keys.append(keyword.value)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and (
            node.name == "_evidence_tie_key" or "rank_equality_key" in node.name
        ):
            rank_keys.append(node)
    return sort_keys, extrema_keys, rank_keys


def _core_fit_usage_inventory(repository_root: Path) -> JsonObject:
    paths = tuple(
        path
        for path in _git_paths(repository_root, AUDITED_HEAD)
        if path.startswith("src/hdmatch/") and path.endswith(".py")
    )
    rows: list[JsonObject] = []
    pattern = re.compile(r"\.core_fit|core_fit")
    for path in paths:
        source = _git_blob(repository_root, AUDITED_HEAD, Path(path)).decode("utf-8")
        tree = ast.parse(source)
        sort_keys, extrema_keys, rank_keys = _key_contexts(tree)
        for line_number, line in enumerate(source.splitlines(), start=1):
            for match in pattern.finditer(line):
                column = match.start()
                rows.append(
                    {
                        "column": column + 1,
                        "enclosing_function_or_class": _enclosing_name(tree, line_number),
                        "inside_max_or_min_key": any(
                            _range_contains(node, line_number, column) for node in extrema_keys
                        ),
                        "inside_rank_equality_key": any(
                            _range_contains(node, line_number, column) for node in rank_keys
                        ),
                        "inside_sort_key": any(
                            _range_contains(node, line_number, column) for node in sort_keys
                        ),
                        "line": line_number,
                        "matched_text": match.group(0),
                        "minimal_source_excerpt": line.strip(),
                        "path": path,
                    }
                )
    keyed = [
        row
        for row in rows
        if row["inside_sort_key"] or row["inside_max_or_min_key"] or row["inside_rank_equality_key"]
    ]
    return {
        "key_context_occurrence_count": len(keyed),
        "key_context_occurrences": keyed,
        "occurrence_count": len(rows),
        "occurrences": rows,
        "scanned_file_count": len(paths),
    }


def _public_module_symbols(tree: ast.Module) -> tuple[str, ...]:
    symbols = [
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("_")
    ]
    return tuple(sorted(symbols))


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _theory_language_runtime_isolation(repository_root: Path) -> JsonObject:
    paths = tuple(
        path
        for path in _git_paths(repository_root, AUDITED_HEAD)
        if path.startswith("src/hdmatch/") and path.endswith(".py")
    )
    defining_source = _git_blob(repository_root, AUDITED_HEAD, THEORY_LANGUAGE_MODULE_PATH).decode(
        "utf-8"
    )
    public_symbols = _public_module_symbols(ast.parse(defining_source))
    import_rows: list[JsonObject] = []
    call_rows: list[JsonObject] = []
    for path in paths:
        if path == THEORY_LANGUAGE_MODULE_PATH.as_posix():
            continue
        source = _git_blob(repository_root, AUDITED_HEAD, Path(path)).decode("utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == (
                "hdmatch.evaluation.theory_language_exposure"
            ):
                import_rows.append(
                    {
                        "imported_names": sorted(alias.name for alias in node.names),
                        "line": node.lineno,
                        "path": path,
                    }
                )
            elif isinstance(node, ast.Import):
                imported = [
                    alias.name
                    for alias in node.names
                    if alias.name == "hdmatch.evaluation.theory_language_exposure"
                ]
                if imported:
                    import_rows.append(
                        {"imported_names": imported, "line": node.lineno, "path": path}
                    )
            elif isinstance(node, ast.Call):
                called = _call_name(node.func)
                if called in public_symbols or called == "classify_theory_language_exposure":
                    call_rows.append({"called_symbol": called, "line": node.lineno, "path": path})
    return {
        "call_site_count_outside_defining_module": len(call_rows),
        "call_sites_outside_defining_module": call_rows,
        "defining_module": THEORY_LANGUAGE_MODULE_PATH.as_posix(),
        "importer_count_outside_defining_module": len({row["path"] for row in import_rows}),
        "imports_outside_defining_module": import_rows,
        "public_symbols": list(public_symbols),
    }


def _future_core_authorization_invariant(repository_root: Path) -> JsonObject:
    raw = _git_blob(repository_root, AUDITED_HEAD, FUTURE_CORE_PATH)
    payload = json.loads(raw)
    rows = payload.get("targets") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        raise ValueError("future-core candidate matrix must contain a targets array")
    fields = (
        "runtime_authorized",
        "mapping_authorized",
        "question_change_authorized",
        "owner_policy",
    )
    return {
        "path": FUTURE_CORE_PATH.as_posix(),
        "row_count": len(rows),
        "rows": [
            {
                "authorization_fields": {field: row[field] for field in fields},
                "target_id": row["target_id"],
            }
            for row in rows
        ],
        "sha256": sha256_bytes(raw),
        "target_ids": sorted(row["target_id"] for row in rows),
    }


def _mapping_question_bank_invariants(repository_root: Path) -> JsonObject:
    mapping_bytes = _git_blob(repository_root, AUDITED_HEAD, MAPPING_PATH)
    question_bank_bytes = _git_blob(repository_root, AUDITED_HEAD, QUESTION_BANK_PATH)
    mapping = json.loads(mapping_bytes)
    frozen = [row for row in mapping["mappings"] if row.get("status") == "frozen"]
    rule_ids = sorted({row["mapping_id"] for row in frozen})
    prompt_ids = sorted(
        {question_id for row in frozen for question_id in row.get("question_ids", [])}
    )
    return {
        "descriptive_only_not_a_completeness_denominator": True,
        "distinct_frozen_mapped_prompt_count": len(prompt_ids),
        "distinct_frozen_mapped_prompt_ids": prompt_ids,
        "distinct_frozen_rule_count": len(rule_ids),
        "distinct_frozen_rule_ids": rule_ids,
        "mapping_library": {
            "expected_sha256": EXPECTED_MAPPING_SHA256,
            "path": MAPPING_PATH.as_posix(),
            "sha256": sha256_bytes(mapping_bytes),
            "stored_frozen_mapping_count": len(frozen),
        },
        "question_bank": {
            "expected_sha256": EXPECTED_QUESTION_BANK_SHA256,
            "path": QUESTION_BANK_PATH.as_posix(),
            "sha256": sha256_bytes(question_bank_bytes),
        },
    }


def _load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _historical_write_result(repository_root: Path, script_name: str) -> JsonObject:
    script_path = repository_root / "scripts" / script_name
    module = _load_module(script_path, f"convergence_{script_path.stem}")
    expected_exception = module.HistoricalAuditSourceMismatch
    with tempfile.TemporaryDirectory() as temporary:
        output = Path(temporary) / "must-not-exist.json"
        try:
            module.write_audit(repository_root, output=output)
        except expected_exception as exc:
            return {
                "exception_class": type(exc).__name__,
                "message": str(exc),
                "output_created": output.exists(),
                "script": f"scripts/{script_name}",
            }
    raise AssertionError(f"{script_name} did not raise HistoricalAuditSourceMismatch")


def _historical_audit_invariants(repository_root: Path) -> JsonObject:
    cross_bytes = _git_blob(repository_root, AUDITED_HEAD, CROSS_CLASS_AUDIT_PATH)
    downstream_bytes = _git_blob(repository_root, AUDITED_HEAD, DOWNSTREAM_AUDIT_PATH)
    return {
        "artifacts": [
            {
                "expected_sha256": EXPECTED_CROSS_CLASS_AUDIT_SHA256,
                "path": CROSS_CLASS_AUDIT_PATH.as_posix(),
                "sha256": sha256_bytes(cross_bytes),
            },
            {
                "expected_sha256": EXPECTED_DOWNSTREAM_AUDIT_SHA256,
                "path": DOWNSTREAM_AUDIT_PATH.as_posix(),
                "sha256": sha256_bytes(downstream_bytes),
            },
        ],
        "generator_results_against_current_source": [
            _historical_write_result(repository_root, "audit_astrohd_cross_class_core_fit.py"),
            _historical_write_result(repository_root, "audit_astrohd_rank_tiebreak_downstream.py"),
        ],
    }


def _dict_assignment(function: ast.AST, name: str) -> dict[str, str]:
    matches = [
        node.value
        for node in ast.walk(function)
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)
    ]
    if len(matches) != 1 or not isinstance(matches[0], ast.Dict):
        raise ValueError(f"expected one dict assignment for {name}")
    result: dict[str, str] = {}
    for key, value in zip(matches[0].keys, matches[0].values, strict=True):
        if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
            raise ValueError(f"non-string key in {name}")
        result[key.value] = ast.unparse(value)
    return result


def _freeze_runtime_binding(repository_root: Path) -> JsonObject:
    raw = _git_blob(repository_root, AUDITED_HEAD, PARTICIPANT_BACKEND_PATH)
    source = raw.decode("utf-8")
    function = _find_function(ast.parse(source), "assert_freeze_compatible")
    expected = _dict_assignment(function, "expected")
    frozen = _dict_assignment(function, "frozen")
    bound_names = (
        "source commit",
        "chart engine",
        "model version",
        "model bytes",
        "mapping bytes",
        "question bank version",
        "question bank bytes",
    )
    return {
        "bound_fields": [
            {
                "active_runtime_expression": expected[name],
                "field": name,
                "frozen_expression": frozen[name],
            }
            for name in bound_names
        ],
        "method_sha256": sha256_bytes(
            _function_source(source, "assert_freeze_compatible").encode()
        ),
        "path": PARTICIPANT_BACKEND_PATH.as_posix(),
        "source_commit_binding": {
            "active_runtime_expression": expected["source commit"],
            "frozen_expression": frozen["source commit"],
            "present": (
                expected["source commit"] == "self.code_commit"
                and frozen["source commit"] == "freeze.code_commit"
            ),
        },
    }


def _coordination_document_headings(repository_root: Path) -> list[JsonObject]:
    rows: list[JsonObject] = []
    for path in COORDINATION_DOCUMENTS:
        raw = _git_blob(repository_root, AUDITED_HEAD, path)
        lines = raw.decode("utf-8").splitlines()
        h1 = [line[2:].strip() for line in lines if line.startswith("# ")]
        h2 = [line[3:].strip() for line in lines if line.startswith("## ")]
        rows.append(
            {
                "first_h1": h1[0] if h1 else None,
                "h2_headings": h2,
                "path": path.as_posix(),
                "sha256": sha256_bytes(raw),
            }
        )
    return rows


def build_audit(repository_root: Path = ROOT) -> JsonObject:
    _git(repository_root, "cat-file", "-e", f"{BASE_COMMIT}^{{commit}}")
    _git(repository_root, "cat-file", "-e", f"{AUDITED_HEAD}^{{commit}}")
    return {
        "audited_head": AUDITED_HEAD,
        "base_commit": BASE_COMMIT,
        "coordination_document_headings": _coordination_document_headings(repository_root),
        "core_fit_usage_inventory": _core_fit_usage_inventory(repository_root),
        "freeze_runtime_binding": _freeze_runtime_binding(repository_root),
        "future_core_authorization_invariant": _future_core_authorization_invariant(
            repository_root
        ),
        "historical_audit_invariants": _historical_audit_invariants(repository_root),
        "mapping_question_bank_invariants": _mapping_question_bank_invariants(repository_root),
        "owner_correction_remnant_scan": _owner_correction_remnant_scan(repository_root),
        "pr_delta_inventory": _pr_delta_inventory(repository_root),
        "rank_semantics": _rank_semantics(repository_root),
        "runtime_symbol_scan": _runtime_symbol_scan(repository_root),
        "schema_version": "astrohd-pr23-convergence-audit-v1",
        "status": "mechanical_final_pr_convergence_audit_no_runtime_effect",
        "theory_language_runtime_isolation": _theory_language_runtime_isolation(repository_root),
    }


def write_audit(
    repository_root: Path = ROOT,
    *,
    output: Path | None = None,
) -> Path:
    output_path = output or repository_root / OUTPUT_PATH
    output_path.write_bytes(render_json(build_audit(repository_root)))
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    repository_root = arguments.repository_root.resolve()
    output = arguments.output.resolve() if arguments.output else None
    output_path = write_audit(repository_root, output=output)
    audit = json.loads(output_path.read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "audited_head": audit["audited_head"],
                "changed_file_count": audit["pr_delta_inventory"]["changed_file_count"],
                "core_fit_key_context_occurrence_count": audit["core_fit_usage_inventory"][
                    "key_context_occurrence_count"
                ],
                "output": output_path.as_posix(),
                "runtime_symbol_occurrence_count": audit["runtime_symbol_scan"]["occurrence_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
