from __future__ import annotations

import argparse
import base64
import hashlib
import json
import zipfile
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

RECEIPT_NAME = "human_handoff_public_safe_receipt_v2.json"
EPISODE_BLANK = "episode_responses.blank.jsonl"
SERIES_BLANK = "series_responses.blank.jsonl"
EPISODE_SCHEMA = "episode_response.schema.json"
SERIES_SCHEMA = "series_response.schema.json"
ATTESTATION_BLANK = "auditor_attestation.blank.json"
EXPECTED_RECEIPT_SCHEMA = "life-patterns-private-human-handoff-receipt-v2"
EXPECTED_EPISODE_SCHEMA = "life-patterns-development-episode-annotation-response-v1"
EXPECTED_SERIES_SCHEMA = "life-patterns-development-series-annotation-response-v2"
EXPECTED_ATTESTATION_BLANK_SCHEMA = "life-patterns-human-auditor-unfilled-attestation-v2"


@dataclass(frozen=True)
class VerifiedHumanHandoffV2:
    zip_sha256: str
    zip_bytes: int
    member_count: int
    receipt: dict[str, Any]
    files: dict[str, bytes]
    episode_unit_count: int
    series_unit_count: int
    packet_count: int


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _jsonl_objects(data: bytes, *, label: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(data.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{label} line {line_number} is invalid JSON") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{label} line {line_number} is not a JSON object")
        rows.append(value)
    return rows


def verify_private_human_handoff_v2_zip(path: str | Path) -> VerifiedHumanHandoffV2:
    source = Path(path)
    raw_zip = source.read_bytes()
    with zipfile.ZipFile(source) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("private human handoff v2 ZIP contains duplicate member names")
        if RECEIPT_NAME not in names:
            raise ValueError("private human handoff v2 ZIP is missing its public-safe receipt")
        if any(name.endswith("/") for name in names):
            raise ValueError("private human handoff v2 ZIP must contain files only")
        files = {name: archive.read(name) for name in names}

    try:
        receipt = json.loads(files[RECEIPT_NAME])
    except json.JSONDecodeError as exc:
        raise ValueError("private human handoff v2 receipt is invalid JSON") from exc
    if not isinstance(receipt, dict) or not isinstance(receipt.get("payload"), dict):
        raise ValueError("private human handoff v2 receipt has the wrong shape")
    payload = receipt["payload"]
    if payload.get("schema_version") != EXPECTED_RECEIPT_SCHEMA:
        raise ValueError("private human handoff uses the wrong receipt schema")
    digest = _sha256(_canonical_json_bytes(payload))
    if receipt.get("receipt_sha256") != digest or receipt.get("receipt_id") != f"LPHB2-{digest[:20].upper()}":
        raise ValueError("private human handoff v2 receipt failed content-address verification")

    declared = payload.get("files")
    if not isinstance(declared, dict) or not declared:
        raise ValueError("private human handoff v2 receipt does not declare member hashes")
    expected_names = set(declared) | {RECEIPT_NAME}
    if set(files) != expected_names:
        missing = sorted(expected_names - set(files))
        extra = sorted(set(files) - expected_names)
        raise ValueError(f"private human handoff v2 member set differs from receipt; missing={missing} extra={extra}")
    for name, expected_hash in declared.items():
        if not isinstance(expected_hash, str) or _sha256(files[name]) != expected_hash:
            raise ValueError(f"private human handoff v2 member hash mismatch: {name}")

    required_flags = {
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
    for field, expected in required_flags.items():
        if payload.get(field) is not expected:
            raise ValueError(f"private human handoff v2 has unexpected {field}")
    if payload.get("readiness") != "awaiting_human_ui":
        raise ValueError("private human handoff v2 was not exported at the awaiting-human-UI gate")
    if payload.get("episode_response_schema_version") != EXPECTED_EPISODE_SCHEMA:
        raise ValueError("private human handoff v2 episode schema version differs from expected")
    if payload.get("series_response_schema_version") != EXPECTED_SERIES_SCHEMA:
        raise ValueError("private human handoff v2 series schema version differs from expected")

    episode_rows = _jsonl_objects(files[EPISODE_BLANK], label=EPISODE_BLANK)
    series_rows = _jsonl_objects(files[SERIES_BLANK], label=SERIES_BLANK)
    if len(episode_rows) != payload.get("episode_unit_count"):
        raise ValueError("episode blank-row count disagrees with handoff receipt")
    if len(series_rows) != payload.get("series_unit_count"):
        raise ValueError("series blank-row count disagrees with handoff receipt")
    if any(row.get("state") is not None for row in (*episode_rows, *series_rows)):
        raise ValueError("blank response templates unexpectedly contain annotation state")
    if any(row.get("schema_version") != EXPECTED_EPISODE_SCHEMA for row in episode_rows):
        raise ValueError("episode blank response template uses the wrong schema")
    if any(row.get("schema_version") != EXPECTED_SERIES_SCHEMA for row in series_rows):
        raise ValueError("series blank response template uses the wrong schema")

    episode_schema = json.loads(files[EPISODE_SCHEMA])
    series_schema = json.loads(files[SERIES_SCHEMA])
    if episode_schema.get("properties", {}).get("schema_version", {}).get("const") != EXPECTED_EPISODE_SCHEMA:
        raise ValueError("episode response schema file does not bind expected response version")
    if series_schema.get("properties", {}).get("schema_version", {}).get("const") != EXPECTED_SERIES_SCHEMA:
        raise ValueError("series response schema file does not bind expected response version")
    attestation_blank = json.loads(files[ATTESTATION_BLANK])
    if attestation_blank.get("schema_version") != EXPECTED_ATTESTATION_BLANK_SCHEMA:
        raise ValueError("auditor attestation blank uses the wrong schema version")

    packet_names = sorted(name for name in files if name.startswith("packets/") and name.endswith(".json"))
    if len(packet_names) != payload.get("packet_count"):
        raise ValueError("private human handoff v2 packet count disagrees with receipt")
    packet_hashes: list[str] = []
    expected_episode_units: set[tuple[str, str, str]] = set()
    expected_series_units: set[tuple[str, str, str]] = set()
    task_signatures: dict[str, bytes] = {}
    for name in packet_names:
        packet = json.loads(files[name])
        pp = packet.get("payload")
        if not isinstance(pp, dict):
            raise ValueError(f"{name} has invalid packet payload")
        packet_digest = _sha256(_canonical_json_bytes(pp))
        if packet.get("packet_sha256") != packet_digest or packet.get("packet_id") != f"LPBP2-{packet_digest[:20].upper()}":
            raise ValueError(f"{name} failed LPBP2 content-address verification")
        packet_hashes.append(packet_digest)
        if pp.get("coder_role") != "human_calibration":
            raise ValueError(f"{name} is not a human-calibration packet")
        for field in (
            "prior_automated_labels_available",
            "automated_consensus_available",
            "target_model_information_available",
            "birth_or_chart_data_available",
            "confirming_episodes_counted_as_frequency_evidence",
            "calibration_selection_resampled_after_revision",
        ):
            if pp.get(field) is not False:
                raise ValueError(f"{name} violates blind first-pass boundary: {field}")
        if pp.get("package_id") != payload.get("package_id") or pp.get("package_sha256") != payload.get("package_sha256"):
            raise ValueError(f"{name} does not bind handoff package")
        if pp.get("coding_manual_sha256") != payload.get("coding_manual_sha256"):
            raise ValueError(f"{name} does not bind handoff coding manual")
        if pp.get("recurrence_policy_sha256") != payload.get("recurrence_policy_sha256"):
            raise ValueError(f"{name} does not bind handoff recurrence policy")
        if pp.get("instruction_prompt_sha256") != payload.get("human_prompt_sha256"):
            raise ValueError(f"{name} does not bind handoff human prompt")
        kind = pp.get("evidence_kind")
        if kind not in {"episode", "series"}:
            raise ValueError(f"{name} has unsupported evidence kind")
        for task in pp.get("tasks", []):
            if not isinstance(task, dict):
                raise ValueError(f"{name} contains an invalid task")
            task_id = task.get("task_id")
            if not isinstance(task_id, str):
                raise ValueError(f"{name} task is missing identity")
            signature = _canonical_json_bytes(task)
            if task_id in task_signatures and task_signatures[task_id] != signature:
                raise ValueError(f"task identity {task_id} has conflicting packet content")
            task_signatures[task_id] = signature
            evidence_id = task.get("episode_id") if kind == "episode" else task.get("series_id")
            for observable_id in task.get("observable_ids", []):
                unit = (task_id, evidence_id, observable_id)
                if kind == "episode":
                    if unit in expected_episode_units:
                        raise ValueError("human episode packet repeats a selected unit")
                    expected_episode_units.add(unit)
                else:
                    if unit in expected_series_units:
                        raise ValueError("human series packet repeats a selected unit")
                    expected_series_units.add(unit)

    if set(packet_hashes) != set(payload.get("packet_sha256s", [])):
        raise ValueError("LPBP2 packet content addresses differ from handoff receipt")
    actual_episode_units = {(row.get("task_id"), row.get("episode_id"), row.get("observable_id")) for row in episode_rows}
    actual_series_units = {(row.get("task_id"), row.get("series_id"), row.get("observable_id")) for row in series_rows}
    if actual_episode_units != expected_episode_units or len(actual_episode_units) != len(episode_rows):
        raise ValueError("episode blank responses do not exactly cover selected packet units")
    if actual_series_units != expected_series_units or len(actual_series_units) != len(series_rows):
        raise ValueError("series blank responses do not exactly cover selected packet units")

    return VerifiedHumanHandoffV2(
        zip_sha256=_sha256(raw_zip),
        zip_bytes=len(raw_zip),
        member_count=len(files),
        receipt=receipt,
        files=files,
        episode_unit_count=len(episode_rows),
        series_unit_count=len(series_rows),
        packet_count=len(packet_names),
    )


TEMPLATE_B64_REL = Path(__file__).with_name("life_patterns_human_calibration_ui_v2_template.zlib.b64")


def _load_html_template() -> str:
    encoded = TEMPLATE_B64_REL.read_text(encoding="ascii").encode("ascii")
    return zlib.decompress(base64.b64decode(encoded)).decode("utf-8")


def build_standalone_human_calibration_ui_v2(
    handoff_zip: str | Path,
    output_html: str | Path,
    *,
    overwrite: bool = False,
) -> dict[str, Any]:
    verified = verify_private_human_handoff_v2_zip(handoff_zip)
    output = Path(output_html)
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")
    embedded = {name: base64.b64encode(data).decode("ascii") for name, data in sorted(verified.files.items())}
    outer = {
        "zip_sha256": verified.zip_sha256,
        "zip_bytes": verified.zip_bytes,
        "member_count": verified.member_count,
        "receipt_id": verified.receipt["receipt_id"],
        "receipt_sha256": verified.receipt["receipt_sha256"],
    }
    html = _load_html_template().replace(
        "__EMBEDDED__", json.dumps(embedded, sort_keys=True, separators=(",", ":"))
    ).replace("__OUTER__", json.dumps(outer, sort_keys=True, separators=(",", ":")))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8", newline="\n")
    return {
        "schema_version": "life-patterns-human-calibration-ui-build-receipt-v2",
        "handoff_receipt_id": verified.receipt["receipt_id"],
        "handoff_receipt_sha256": verified.receipt["receipt_sha256"],
        "handoff_zip_sha256": verified.zip_sha256,
        "handoff_zip_bytes": verified.zip_bytes,
        "handoff_member_count": verified.member_count,
        "episode_unit_count": verified.episode_unit_count,
        "series_unit_count": verified.series_unit_count,
        "packet_count": verified.packet_count,
        "output_html_sha256": _sha256(output.read_bytes()),
        "output_html_bytes": output.stat().st_size,
        "network_requests_required": False,
        "automated_judgment_used": False,
        "development_only": True,
        "validation_use_forbidden": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the verified standalone offline Life Patterns human-calibration UI v2."
    )
    parser.add_argument("--handoff-zip", type=Path, required=True)
    parser.add_argument("--output-html", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    receipt = build_standalone_human_calibration_ui_v2(
        args.handoff_zip, args.output_html, overwrite=args.overwrite
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
