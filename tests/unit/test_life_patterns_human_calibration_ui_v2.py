from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import zipfile
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "build_life_patterns_human_calibration_ui_v2.py"
MODULE_NAME = "life_patterns_human_calibration_ui_v2_builder_test"


def _load_ui_builder() -> ModuleType:
    spec = importlib.util.spec_from_file_location(MODULE_NAME, SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _packet(
    kind: str,
    task: dict[str, object],
    *,
    package_id: str,
    package_sha256: str,
    manual_sha256: str,
    policy_sha256: str,
    prompt_sha256: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": "life-patterns-blind-development-coder-packet-v2",
        "coder_role": "human_calibration",
        "evidence_kind": kind,
        "batch_index": 1,
        "package_id": package_id,
        "package_sha256": package_sha256,
        "corpus_id": "LPDC-" + "A" * 20,
        "corpus_sha256": "a" * 64,
        "coding_manual_sha256": manual_sha256,
        "coding_manual_text": "Synthetic theory-neutral coding manual.",
        "recurrence_policy_sha256": policy_sha256,
        "recurrence_policy_text": "Synthetic theory-neutral recurrence policy.",
        "instruction_prompt_sha256": prompt_sha256,
        "instruction_prompt_text": "Synthetic theory-neutral human prompt.",
        "tasks": [task],
        "assigned_unit_count": 1,
        "prior_automated_labels_available": False,
        "automated_consensus_available": False,
        "target_model_information_available": False,
        "birth_or_chart_data_available": False,
        "confirming_episodes_counted_as_frequency_evidence": False,
        "calibration_selection_resampled_after_revision": False,
        "ontology": {"payload": {"observables": []}},
        "procedure": {"payload": {"observable_extensions": []}},
        "resolved_view": {"payload": {"observables": []}},
    }
    digest = _sha256(_canonical_json_bytes(payload))
    return {
        "packet_id": f"LPBP2-{digest[:20].upper()}",
        "packet_sha256": digest,
        "payload": payload,
    }


def _write_synthetic_handoff(path: Path) -> None:
    package_id = "LPKG2-" + "B" * 20
    package_sha256 = "b" * 64
    manual_sha256 = "c" * 64
    policy_sha256 = "d" * 64
    prompt_sha256 = "e" * 64
    episode_task: dict[str, object] = {
        "task_id": "LPDT-" + "1" * 20,
        "episode_id": "EP-001",
        "observable_ids": ["NBM-R01"],
        "exact_source_segments": [
            {
                "segment_id": "E-S1",
                "exact_text": "PRIVATE-SYNTHETIC-EPISODE",
            }
        ],
    }
    series_task: dict[str, object] = {
        "task_id": "LPST-" + "2" * 20,
        "series_id": "SER-001",
        "observable_ids": ["NBM-R01"],
        "exact_source_segments": [
            {
                "segment_id": "S-S1",
                "exact_text": "PRIVATE-SYNTHETIC-SERIES",
            }
        ],
    }
    episode_packet = _packet(
        "episode",
        episode_task,
        package_id=package_id,
        package_sha256=package_sha256,
        manual_sha256=manual_sha256,
        policy_sha256=policy_sha256,
        prompt_sha256=prompt_sha256,
    )
    series_packet = _packet(
        "series",
        series_task,
        package_id=package_id,
        package_sha256=package_sha256,
        manual_sha256=manual_sha256,
        policy_sha256=policy_sha256,
        prompt_sha256=prompt_sha256,
    )
    episode_row = {
        "schema_version": "life-patterns-development-episode-annotation-response-v1",
        "task_id": episode_task["task_id"],
        "episode_id": "EP-001",
        "observable_id": "NBM-R01",
        "state": None,
    }
    series_row = {
        "schema_version": "life-patterns-development-series-annotation-response-v2",
        "task_id": series_task["task_id"],
        "series_id": "SER-001",
        "observable_id": "NBM-R01",
        "state": None,
    }
    files: dict[str, bytes] = {
        "README.md": b"Synthetic private handoff.",
        "packets/episode/packet-001.json": _canonical_json_bytes(episode_packet),
        "packets/series/packet-001.json": _canonical_json_bytes(series_packet),
        "episode_responses.blank.jsonl": _canonical_json_bytes(episode_row) + b"\n",
        "series_responses.blank.jsonl": _canonical_json_bytes(series_row) + b"\n",
        "episode_response.schema.json": _canonical_json_bytes(
            {
                "properties": {
                    "schema_version": {
                        "const": "life-patterns-development-episode-annotation-response-v1"
                    }
                }
            }
        ),
        "series_response.schema.json": _canonical_json_bytes(
            {
                "properties": {
                    "schema_version": {
                        "const": "life-patterns-development-series-annotation-response-v2"
                    }
                }
            }
        ),
        "auditor_attestation.blank.json": _canonical_json_bytes(
            {"schema_version": "life-patterns-human-auditor-unfilled-attestation-v2"}
        ),
    }
    receipt_payload: dict[str, Any] = {
        "schema_version": "life-patterns-private-human-handoff-receipt-v2",
        "package_id": package_id,
        "package_sha256": package_sha256,
        "packet_sha256s": [
            episode_packet["packet_sha256"],
            series_packet["packet_sha256"],
        ],
        "human_prompt_sha256": prompt_sha256,
        "recurrence_policy_sha256": policy_sha256,
        "coding_manual_sha256": manual_sha256,
        "packet_count": 2,
        "episode_unit_count": 1,
        "series_unit_count": 1,
        "episode_response_schema_version": (
            "life-patterns-development-episode-annotation-response-v1"
        ),
        "series_response_schema_version": (
            "life-patterns-development-series-annotation-response-v2"
        ),
        "files": {name: _sha256(raw) for name, raw in sorted(files.items())},
        "readiness": "awaiting_human_ui",
        "selected_unit_coverage_verified": True,
        "calibration_selection_reused_without_resampling": True,
        "confirming_episodes_are_not_frequency_counts": True,
        "response_templates_are_annotations": False,
        "human_facing_ui_required_before_collection": True,
        "auditor_identity_verified": False,
        "human_blinding_attested": False,
        "development_only": True,
        "validation_use_forbidden": True,
    }
    receipt_digest = _sha256(_canonical_json_bytes(receipt_payload))
    receipt = {
        "receipt_id": f"LPHB2-{receipt_digest[:20].upper()}",
        "receipt_sha256": receipt_digest,
        "payload": receipt_payload,
    }
    files["human_handoff_public_safe_receipt_v2.json"] = _canonical_json_bytes(receipt)

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, raw in files.items():
            archive.writestr(name, raw)


def test_builder_verifies_handoff_and_emits_networkless_standalone_ui(
    tmp_path: Path,
) -> None:
    ui = _load_ui_builder()
    handoff = tmp_path / "synthetic-handoff.zip"
    output = tmp_path / "offline-ui.html"
    _write_synthetic_handoff(handoff)

    verified = ui.verify_private_human_handoff_v2_zip(handoff)
    receipt = ui.build_standalone_human_calibration_ui_v2(handoff, output)
    html = output.read_text(encoding="utf-8")

    assert verified.episode_unit_count == 1
    assert verified.series_unit_count == 1
    assert verified.packet_count == 2
    assert receipt["network_requests_required"] is False
    assert receipt["automated_judgment_used"] is False
    assert receipt["episode_unit_count"] == 1
    assert receipt["series_unit_count"] == 1
    assert "connect-src 'none'" in html
    assert "Verify first. Then annotate." in html
    assert "PRIVATE-SYNTHETIC-EPISODE" not in html
    assert "PRIVATE-SYNTHETIC-SERIES" not in html
    assert receipt["output_html_sha256"] == _sha256(output.read_bytes())


def test_builder_fails_closed_when_receipt_bound_member_is_modified(
    tmp_path: Path,
) -> None:
    ui = _load_ui_builder()
    handoff = tmp_path / "synthetic-handoff.zip"
    tampered = tmp_path / "tampered.zip"
    _write_synthetic_handoff(handoff)

    with zipfile.ZipFile(handoff) as source, zipfile.ZipFile(tampered, "w") as target:
        for name in source.namelist():
            raw = source.read(name)
            if name == "README.md":
                raw += b"tamper"
            target.writestr(name, raw)

    with pytest.raises(ValueError, match="member hash mismatch"):
        ui.verify_private_human_handoff_v2_zip(tampered)


def test_builder_fails_closed_on_unreceipted_extra_member(tmp_path: Path) -> None:
    ui = _load_ui_builder()
    handoff = tmp_path / "synthetic-handoff.zip"
    extra = tmp_path / "extra-member.zip"
    _write_synthetic_handoff(handoff)

    with zipfile.ZipFile(handoff) as source, zipfile.ZipFile(extra, "w") as target:
        for name in source.namelist():
            target.writestr(name, source.read(name))
        target.writestr("unexpected.txt", b"not receipt-bound")

    with pytest.raises(ValueError, match="member set differs from receipt"):
        ui.verify_private_human_handoff_v2_zip(extra)
