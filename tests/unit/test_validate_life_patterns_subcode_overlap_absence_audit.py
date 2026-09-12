from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate_life_patterns_subcode_overlap_absence_audit.py"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("lp_overlap_audit_validator_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _finding(index: int, observable_id: str) -> dict[str, object]:
    return {
        "finding_id": f"OA-{index:03d}",
        "observable_id": observable_id,
        "subcode_ids": [f"R{index:02d}-a"],
        "finding_type": "facet_structure",
        "classification": "no_change_needed",
        "exact_issue": "No material facet problem beyond the finding used to establish coverage.",
        "human_coding_consequence": "No additional human-coding consequence.",
        "recommended_disposition": "no_change",
        "confidence": "high",
    }


def _summary(findings: list[dict[str, object]]) -> dict[str, object]:
    return {
        "schema_version": "life-patterns-subcode-overlap-absence-audit-v1",
        "observables_reviewed": 22,
        "material_findings": len(findings),
        "presentation_only_count": 0,
        "response_contract_limitation_count": 0,
        "substantive_codebook_overlap_count": 0,
        "no_change_needed_count": len(findings),
        "r05_disposition": "no_change",
        "human_calibration_safe_to_start_without_revision": True,
        "blocking_findings": [],
        "notes": "Synthetic validator test.",
    }


def test_validator_accepts_complete_sequential_22_observable_fixture(tmp_path: Path) -> None:
    module = _load()
    findings = [_finding(i, f"NBM-R{i:02d}") for i in range(1, 23)]
    findings_path = tmp_path / "findings.jsonl"
    findings_path.write_text("\n".join(json.dumps(row) for row in findings) + "\n", encoding="utf-8")
    rows = module._load_jsonl(findings_path)
    for index, row in enumerate(rows, start=1):
        module._validate_finding(row, index)
    module._validate_summary(_summary(findings), rows)


def test_validator_rejects_markdown_escaped_json_keys(tmp_path: Path) -> None:
    module = _load()
    path = tmp_path / "bad.jsonl"
    path.write_text('{"finding\\_id":"OA-001"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="invalid JSON"):
        module._load_jsonl(path)


def test_validator_rejects_nonsequential_finding_ids() -> None:
    module = _load()
    row = _finding(2, "NBM-R01")
    with pytest.raises(ValueError, match="expected OA-001"):
        module._validate_finding(row, 1)


def test_validator_rejects_summary_count_mismatch() -> None:
    module = _load()
    findings = [_finding(i, f"NBM-R{i:02d}") for i in range(1, 23)]
    summary = _summary(findings)
    summary["no_change_needed_count"] = 21
    with pytest.raises(ValueError, match="no_change_needed_count"):
        module._validate_summary(summary, findings)
