from __future__ import annotations

import json
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError
from test_development_blind_packets import PRIVATE_MARKER, _preparation

from hdmatch.evaluation.development_blind_packets import (
    BlindDevelopmentPacketArtifact,
    build_blind_development_packets,
    packet_public_safe_receipt,
)
from hdmatch.evaluation.development_episode_evidence import DevelopmentEpisodeAnnotationResponse
from hdmatch.evaluation.development_human_handoff import (
    export_development_human_calibration_bundle,
)
from hdmatch.evaluation.development_private_preparation import write_private_development_preparation
from hdmatch.evaluation.development_series_evidence import DevelopmentSeriesAnnotationResponse
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_bytes, sha256_json


@pytest.fixture
def prepared(tmp_path: Path) -> Path:
    prep = _preparation()
    root = tmp_path / "prepared"
    write_private_development_preparation(root, prep)
    for role in ("human_calibration", "automated"):
        for kind in ("episode", "series"):
            packets = build_blind_development_packets(
                prep, repo_root=Path("."), coder_role=role, evidence_kind=kind
            )
            group = root / "blind_packets" / f"{role}_{kind}"
            group.mkdir(parents=True)
            for packet in packets:
                path = group / f"packet-{packet.payload.batch_index:03d}.json"
                # Deliberately noncanonical bytes ensure the exporter cannot silently rerender.
                path.write_text(packet.model_dump_json(indent=3) + "\n", encoding="utf-8")
                path.with_suffix(".receipt.json").write_bytes(
                    canonical_json_bytes(packet_public_safe_receipt(packet))
                )
    return root


def _episode_packet(prepared: Path) -> Path:
    return prepared / "blind_packets/human_calibration_episode/packet-001.json"


def _rebind_packet(path: Path, payload: dict[str, Any]) -> None:
    digest = sha256_json(payload)
    packet = BlindDevelopmentPacketArtifact.model_validate(
        {
            "packet_id": f"LPBP-{digest[:20].upper()}",
            "packet_sha256": digest,
            "payload": payload,
        }
    )
    path.write_bytes(canonical_json_bytes(packet))
    path.with_suffix(".receipt.json").write_bytes(
        canonical_json_bytes(packet_public_safe_receipt(packet))
    )


def test_export_preserves_only_human_packets_and_leaves_all_coding_unfilled(
    prepared: Path, tmp_path: Path
) -> None:
    output = tmp_path / "human"
    result = export_development_human_calibration_bundle(prepared, output)
    payload = result["payload"]
    assert payload["episode_unit_count"] == 2
    assert payload["series_unit_count"] == 1
    assert payload["packet_count"] == 2
    assert payload["readiness"] == "awaiting_human"
    assert payload["human_blinding_attested"] is False
    assert payload["auditor_identity_verified"] is False
    assert result["receipt_sha256"] == sha256_json(payload)
    assert PRIVATE_MARKER not in json.dumps(result)
    for kind, response_model, expected_count in (
        ("episode", DevelopmentEpisodeAnnotationResponse, 2),
        ("series", DevelopmentSeriesAnnotationResponse, 1),
    ):
        source = prepared / "blind_packets" / f"human_calibration_{kind}/packet-001.json"
        copied = output / f"packets/{kind}/packet-001.json"
        assert source.read_bytes() == copied.read_bytes()
        rows = [
            json.loads(line)
            for line in (output / f"{kind}_responses.blank.jsonl").read_text().splitlines()
        ]
        assert len(rows) == expected_count
        assert len({(row["task_id"], row["observable_id"]) for row in rows}) == expected_count
        for row in rows:
            assert row["state"] is None
            assert row["coded_values"] is None
            assert row["asserts_non_action"] is None
            assert row["theory_exposure"] is None
            assert row["task_id"]
            assert row["development_only"] is True
            assert row["validation_use_forbidden"] is True
            with pytest.raises(ValidationError):
                response_model.model_validate(row)
        schema = json.loads((output / f"{kind}_response.schema.json").read_text())
        assert schema == response_model.model_json_schema()
    form = json.loads((output / "auditor_attestation.blank.json").read_text())
    assert all(value is None for key, value in form.items() if key != "schema_version")
    assert not any("automated" in path.name for path in output.rglob("*"))
    assert "Do not use an automated coder" in (output / "README.md").read_text()
    for name, digest in payload["files"].items():
        assert sha256_bytes((output / name).read_bytes()) == digest
    assert stat.S_IMODE(output.stat().st_mode) == 0o700
    for path in output.rglob("*"):
        assert stat.S_IMODE(path.stat().st_mode) == (0o700 if path.is_dir() else 0o400)


@pytest.mark.parametrize(
    "damage", ["hash", "extra_unit", "duplicate", "missing", "mixed_package", "automated"]
)
def test_invalid_packets_fail_before_creating_output(
    prepared: Path, tmp_path: Path, damage: str
) -> None:
    path = _episode_packet(prepared)
    value = json.loads(path.read_bytes())
    if damage == "hash":
        value["payload"]["tasks"][0]["episode_narrative"] = "Changed synthetic narrative."
        path.write_bytes(canonical_json_bytes(value))
    elif damage == "extra_unit":
        task = value["payload"]["tasks"][0]
        extra = next(
            f"NBM-R{i:02d}" for i in range(1, 23) if f"NBM-R{i:02d}" not in task["observable_ids"]
        )
        task["observable_ids"].append(extra)
        value["payload"]["assigned_unit_count"] += 1
        _rebind_packet(path, value["payload"])
    elif damage == "duplicate":
        value["payload"]["tasks"].append(value["payload"]["tasks"][0])
        value["payload"]["assigned_unit_count"] *= 2
        _rebind_packet(path, value["payload"])
    elif damage == "missing":
        path.unlink()
    elif damage == "mixed_package":
        value["payload"]["package_sha256"] = "f" * 64
        _rebind_packet(path, value["payload"])
    else:
        automated = prepared / "blind_packets/automated_episode/packet-001.json"
        path.write_bytes(automated.read_bytes())
        path.with_suffix(".receipt.json").write_bytes(
            automated.with_suffix(".receipt.json").read_bytes()
        )
    output = tmp_path / "human"
    with pytest.raises(ValueError):
        export_development_human_calibration_bundle(prepared, output)
    assert not output.exists()


@pytest.mark.parametrize(
    "filename", ["development_calibration_manifest.json", "development_episode_tasks.json"]
)
def test_changed_frozen_selection_or_tasks_fail_before_writing(
    prepared: Path, tmp_path: Path, filename: str
) -> None:
    path = prepared / filename
    value = json.loads(path.read_bytes())
    if filename == "development_calibration_manifest.json":
        value["manifest_sha256"] = "0" * 64
    else:
        value[0]["episode_narrative"] = "Changed synthetic task."
    path.chmod(0o600)
    path.write_bytes(canonical_json_bytes(value))
    output = tmp_path / "human"
    with pytest.raises(ValueError):
        export_development_human_calibration_bundle(prepared, output)
    assert not output.exists()


def test_existing_output_is_never_replaced(prepared: Path, tmp_path: Path) -> None:
    output = tmp_path / "human"
    export_development_human_calibration_bundle(prepared, output)
    original = (output / "human_handoff_public_safe_receipt.json").read_bytes()
    with pytest.raises(FileExistsError):
        export_development_human_calibration_bundle(prepared, output)
    assert (output / "human_handoff_public_safe_receipt.json").read_bytes() == original


def test_cli_does_not_print_private_validation_input(prepared: Path, tmp_path: Path) -> None:
    path = _episode_packet(prepared)
    value = json.loads(path.read_bytes())
    value["payload"]["tasks"][0]["corpus_id"] = PRIVATE_MARKER
    path.write_bytes(canonical_json_bytes(value))
    output = tmp_path / "human"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/export_life_patterns_human_calibration_bundle.py",
            "--prepared-dir",
            str(prepared),
            "--output-dir",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert PRIVATE_MARKER not in result.stdout + result.stderr
    assert "Traceback" not in result.stderr
    assert not output.exists()
