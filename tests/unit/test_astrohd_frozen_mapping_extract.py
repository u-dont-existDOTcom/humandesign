from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).parents[2]
SOURCE_PATH = ROOT / "mappings/mapping_library_v1.json"
EXTRACT_PATH = ROOT / "reference/audits/astrohd_frozen_rule_prompt_mapping_v1.json"


def _runner() -> ModuleType:
    path = ROOT / "scripts" / "extract_astrohd_frozen_rule_prompt_mapping.py"
    spec = importlib.util.spec_from_file_location(
        "extract_astrohd_frozen_rule_prompt_mapping", path
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_frozen_mapping_extract_is_exactly_27_rules_and_23_prompts() -> None:
    report = _runner().build_extract(SOURCE_PATH)

    assert report["source"]["path"] == "mappings/mapping_library_v1.json"
    assert report["source"]["status_filter"] == "frozen"
    assert report["distinct_rule_count"] == 27
    assert report["distinct_mapped_prompt_count"] == 23
    assert report["acceptance"] == {
        "expected_distinct_rule_count": 27,
        "expected_distinct_mapped_prompt_count": 23,
        "counts_match": True,
    }


def test_extract_contains_only_mechanical_rule_prompt_relationships() -> None:
    report = _runner().build_extract(SOURCE_PATH)

    assert len(report["rules"]) == 27
    assert len(report["prompts"]) == 23
    assert all(
        rule["mapped_prompt_count"] == len(rule["mapped_prompt_identifiers"])
        for rule in report["rules"]
    )
    assert all(
        prompt["mapped_rule_count"] == len(prompt["mapped_rule_identifiers"])
        for prompt in report["prompts"]
    )
    assert all(
        prompt["mapped_rule_count"] > 1 for prompt in report["prompts_shared_by_multiple_rules"]
    )
    assert all(
        rule["mapped_prompt_count"] > 1 for rule in report["rules_mapped_to_multiple_prompts"]
    )


def test_committed_extract_reproduces_from_frozen_mapping_source() -> None:
    generated = _runner().build_extract(SOURCE_PATH)
    committed = json.loads(EXTRACT_PATH.read_text(encoding="utf-8"))

    assert committed == generated
