"""Assemble the existing GPT's cumulative, source-preserving update package.

Only three authored payloads change: Instructions, one Knowledge presentation
rule, and a new evidence-preservation guide. All other runtime/Knowledge bytes
come from the exact already-published v1.9 package. No service calls are made.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
RELEASE = ROOT / "reference/custom_gpt/releases/life-patterns-shared-evidence-2026-10-26"
OUT = RELEASE.parent / "Life-Patterns-GPT-Shared-Evidence-2026-10-26.zip"
SOURCE_REF = "7de212f027e14c198fb58dc91d11df3068d58e56"
SOURCE_PATH = "reference/custom_gpt/releases/Life-Patterns-GPT-Experience-and-Railway-v1.9-2026-10-17.zip"
SOURCE_SHA256 = "bc16e98b7dc08a4bbfe1059dac40aca1762e04ea08a6f558e570cee84b952c8b"
INSTRUCTIONS = "INSTRUCTIONS-life-patterns-2026-10-26.txt"
TF = "knowledge/TENDENCY-FIRST-GUIDE-v1.json"
CAPTURE = "knowledge/SHARED-EVIDENCE-CAPTURE-GUIDE-v1.md"
ACTION = "ACTION-life-patterns-submission-openapi.yaml"
CF = "knowledge/cf003_secondary_question_module_v0.json"
EM = "knowledge/experience-meaning-v2.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-zip", type=Path)
    args = parser.parse_args()
    source = (
        args.source_zip.read_bytes() if args.source_zip else subprocess.check_output(
            ["git", "show", f"{SOURCE_REF}:{SOURCE_PATH}"], cwd=ROOT
        )
    )
    assert sha(source) == SOURCE_SHA256, "Wrong predecessor package"
    with zipfile.ZipFile(io.BytesIO(source)) as archive:
        old = {name: archive.read(name) for name in archive.namelist()}
    old_manifest = json.loads(old["UPDATE-MANIFEST.json"])
    assert all(sha(old[name]) == digest for name, digest in old_manifest["files"].items())

    files = {
        name: content for name, content in old.items()
        if name.startswith("knowledge/") or name == ACTION
    }
    for name in [INSTRUCTIONS, TF, CAPTURE, "UPDATE-EXISTING-GPT.md"]:
        files[name] = (RELEASE / name).read_bytes()

    text = files[INSTRUCTIONS].decode("utf-8")
    strict_chars = len(text.replace("\n", "\r\n"))
    assert strict_chars <= 8000, f"Instructions too long: {strict_chars}"
    assert len(files[INSTRUCTIONS].replace(b"\n", b"\r\n")) <= 8000
    assert len([name for name in files if name.startswith("knowledge/")]) == 11
    for name in files:
        if name.endswith(".json"):
            json.loads(files[name])
    for name in re.findall(r"\b[A-Z][A-Z0-9-]+-v\d+\.(?:md|json)\b", text):
        assert f"knowledge/{name}" in files, f"Missing Instructions companion: {name}"

    old_tf, new_tf = json.loads(old[TF]), json.loads(files[TF])
    assert old_tf.keys() == new_tf.keys()
    assert all(old_tf[key] == new_tf[key] for key in old_tf if key != "rules")
    assert len(old_tf["rules"]) == len(new_tf["rules"])
    changed_rules = [i for i, pair in enumerate(zip(old_tf["rules"], new_tf["rules"])) if pair[0] != pair[1]]
    assert changed_rules == [8], f"Unexpected TF rule changes: {changed_rules}"
    assert len(new_tf["questions"]) == 25
    assert len(json.loads(files[CF])["questions"]) == 3
    em = json.loads(files[EM])
    em_items = em.get("items", em.get("questions"))
    assert len(em_items) == 8
    unchanged_knowledge = [name for name in old if name.startswith("knowledge/") and name != TF]
    assert len(unchanged_knowledge) == 9
    assert all(files[name] == old[name] for name in unchanged_knowledge)
    assert files[ACTION] == old[ACTION]
    action = json.loads(files[ACTION])
    assert action["info"]["version"] == "1.9.0"
    public = json.loads((TASK / "PUBLIC_SERVICE_READBACK.json").read_text())
    live = public["/action-openapi.yaml"]
    assert live["status"] == 200 and live["sha256"] == sha(files[ACTION])
    assert live["byte_equal_package_action"] is True

    manifest = {
        "schema": "LIFE_PATTERNS_GPT_UPDATE_PACKAGE_V1",
        "version": "2026-10-26.1-shared-evidence",
        "owner_supplied_installed_instructions_sha256": sha((TASK / "SOURCE_INSTALLED_INSTRUCTIONS_20261026.txt").read_bytes()),
        "source_release_commit": SOURCE_REF,
        "source_package_path": SOURCE_PATH,
        "source_package_sha256": SOURCE_SHA256,
        "instructions_lf_characters": len(text),
        "instructions_crlf_characters": strict_chars,
        "instructions_utf8_bytes": len(files[INSTRUCTIONS]),
        "knowledge_files": 11,
        "unchanged_knowledge_files": len(unchanged_knowledge),
        "tendency_first_question_objects_unchanged": 25,
        "cf003_question_objects_unchanged": 3,
        "experience_question_objects_unchanged": 8,
        "legacy_bank_bytes_unchanged": True,
        "new_behavioral_question_objects": 0,
        "new_required_questions": 0,
        "action_version": "1.9.0",
        "action_schema_unchanged": True,
        "public_live_action_byte_match": True,
        "runtime_question_policy_unchanged": True,
        "runtime_policy": public["/healthz"]["health"]["question_policy"],
        "same_existing_gpt_and_action_authentication": True,
        "private_data_in_package": False,
        "editor_applied": False,
        "service_deployed_by_this_update": False,
        "adaptive_23_plus_7_candidate_activated": False,
        "structured_event_adapter_implemented": False,
        "files": {name: sha(content) for name, content in sorted(files.items())},
    }
    files["UPDATE-MANIFEST.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode()
    (RELEASE / "UPDATE-MANIFEST.json").write_bytes(files["UPDATE-MANIFEST.json"])
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 26, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, content)
    data = out.getvalue()
    OUT.write_bytes(data)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(files)
        assert all(archive.read(name) == content for name, content in files.items())
        assert all(sha(archive.read(name)) == digest for name, digest in manifest["files"].items())

    verification = {
        "status": "PASS_PACKAGE_INTEGRITY_AND_CONTRACT_CHECKS",
        "package_path": str(OUT.relative_to(ROOT)),
        "package_sha256": sha(data),
        "package_bytes": len(data),
        "instructions_sha256": sha(files[INSTRUCTIONS]),
        "instructions_crlf_characters": strict_chars,
        "source_baseline_sha256": manifest["owner_supplied_installed_instructions_sha256"],
        "preservation": {key: manifest[key] for key in ["tendency_first_question_objects_unchanged", "cf003_question_objects_unchanged", "experience_question_objects_unchanged", "legacy_bank_bytes_unchanged", "unchanged_knowledge_files", "action_schema_unchanged", "runtime_question_policy_unchanged"]},
        "independent_review": {
            "reviewer": "/root/gpt_contract_audit",
            "result": "PASS_NO_CONCRETE_MUST_FIX_FINDINGS",
            "scope": "Full semantic comparison to owner-pasted baseline and eight scenario inspections; not a deployed participant test or scientific validation.",
            "instructions_sha256": sha(files[INSTRUCTIONS]),
            "capture_guide_sha256": sha(files[CAPTURE]),
            "tendency_guide_sha256": sha(files[TF]),
        },
        "public_service_schema_match": True,
        "authenticated_cli_result": "NO_OUTPUT_FROM_DEVICE_TRANSPORT; OWNER_REPORTS_LOGIN_SUCCEEDED",
        "worker_heartbeat_verified": False,
        "private_gpt_installed": False,
        "runtime_changes": False,
        "human_predictive_validation": False,
    }
    (TASK / "VERIFICATION.json").write_text(json.dumps(verification, indent=2) + "\n")
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
