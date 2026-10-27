"""Build the cumulative optional shared-topics package from a verified predecessor."""
from __future__ import annotations

import hashlib
import io
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).parent
RELEASE = ROOT / "reference/custom_gpt/releases/life-patterns-shared-topics-v1.10"
BASE = ROOT / "reference/custom_gpt/releases/Life-Patterns-GPT-Shared-Evidence-2026-10-26.zip"
BASE_SHA = "95c2d75d25db191a1a46bf7d3061188d9a6459e376481b33d7e86f68d4a111c3"
OUT = ROOT / "reference/custom_gpt/releases/Life-Patterns-GPT-Shared-Topics-v1.10-2026-10-26.zip"
STATIC = ROOT / "apps/life-patterns-participant/participant/static"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    assert sha(BASE.read_bytes()) == BASE_SHA
    with zipfile.ZipFile(BASE) as archive:
        old = {name: archive.read(name) for name in archive.namelist()}
    files = {name: data for name, data in old.items() if name.startswith("knowledge/")}
    handoff_name = "knowledge/ACTION-HANDOFF-GUIDE-v1.md"
    appendix = """

## Action 1.10: optional shared life topics

On the usual getLifePatternsReview call, set include_shared_evidence=true with
the installed 1.10 Action. This adds no external call. Legacy clients omit the
query and keep their old response shape. Only shared_evidence_available=true
admits the optional shared-topic offer; ready alone does not permit appending
answers to a review already finally submitted.

After primary/CF003 freeze, follow POST-REVIEW-OPTIONAL-MODULES-v1.md. The neutral
SHARED-LIFE-TOPICS-v3.json is the permitted participant bank. Shared answers need
their own actual opt-in and remain a separate development, unscored record.
On opt-in only, include the complete shared_evidence_record_json in the same
final submitLifePatternsRecords call. Preserve all existing required fields and
the separately consented experience_record_json behavior. Verify exact source
references against the final composites and preserve all files before calling.
The receipt's shared_evidence_record_sha256 confirms that optional record's
storage. Exact retries reuse the entire identical envelope. The phase remains
one final storage call and one expected Allow card.
"""
    files[handoff_name] += appendix.encode()
    files["knowledge/POST-REVIEW-OPTIONAL-MODULES-v1.md"] = (
        RELEASE / "POST-REVIEW-OPTIONAL-MODULES-v1.md"
    ).read_bytes()
    files["knowledge/SHARED-LIFE-TOPICS-v3.json"] = (
        STATIC / "shared-life-topics-v3.json"
    ).read_bytes()
    files["ACTION-life-patterns-submission-openapi.yaml"] = (
        STATIC / "action-openapi-v1.10.yaml"
    ).read_bytes()
    name = "INSTRUCTIONS-life-patterns-v1.10.txt"
    files[name] = (RELEASE / name).read_bytes()
    files["UPDATE-EXISTING-GPT.md"] = (RELEASE / "UPDATE-EXISTING-GPT.md").read_bytes()
    instruction_text = files[name].decode()
    strict_chars = len(instruction_text.replace("\n", "\r\n"))
    assert strict_chars <= 8000, strict_chars
    assert len([key for key in files if key.startswith("knowledge/")]) == 13
    unchanged = [key for key in old if key.startswith("knowledge/") and key != handoff_name]
    assert len(unchanged) == 10
    assert all(files[key] == old[key] for key in unchanged)
    assert files[handoff_name].startswith(old[handoff_name])
    bank = json.loads(files["knowledge/SHARED-LIFE-TOPICS-v3.json"])
    assert len(bank["questions"]) == 23 and len(bank["optional_microprobes"]) == 7
    assert json.loads(files["ACTION-life-patterns-submission-openapi.yaml"])["info"]["version"] == "1.10.0"
    manifest = {
        "schema": "life-patterns-gpt-update-package-v1",
        "version": "1.10.0-shared-topics-20261026",
        "status": "LOCAL_VERIFIED_CANDIDATE_NOT_DEPLOYMENT_RECEIPT",
        "base_package_sha256": BASE_SHA,
        "base_editor_status": "installed_by_owner_report_done_continue",
        "instructions_strict_characters": strict_chars,
        "knowledge_files": 13,
        "unchanged_knowledge_files": 10,
        "new_mandatory_questions": 0,
        "shared_topic_count": 23,
        "shared_conditional_probe_count": 7,
        "all_existing_behavioral_wording_preserved": True,
        "runtime_tendency_policy_unchanged": True,
        "independent_review_worker_unchanged": True,
        "shared_answers_chart_scored": False,
        "backend_deployed_by_package_build": False,
        "private_gpt_editor_updated_by_package_build": False,
        "private_data_in_package": False,
        "files": {key: sha(value) for key, value in sorted(files.items())},
    }
    files["UPDATE-MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as archive:
        for key, value in sorted(files.items()):
            info = zipfile.ZipInfo(key, date_time=(2026, 10, 26, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, value)
    data = out.getvalue()
    OUT.write_bytes(data)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(files)
        assert all(archive.read(key) == value for key, value in files.items())
    (RELEASE / "UPDATE-MANIFEST.json").write_bytes(files["UPDATE-MANIFEST.json"])
    verification = {
        "status": "PASS",
        "package": str(OUT.relative_to(ROOT)),
        "sha256": sha(data),
        "bytes": len(data),
        "instructions_sha256": sha(files[name]),
        "instructions_strict_characters": strict_chars,
        "knowledge_files": 13,
        "ten_previous_knowledge_files_byte_identical": True,
        "handoff_previous_content_preserved": True,
        "archive_round_trip": True,
        "editor_or_deployment_verified": False,
    }
    (TASK / "PACKAGE-VERIFICATION.json").write_text(json.dumps(verification, indent=2) + "\n")
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
