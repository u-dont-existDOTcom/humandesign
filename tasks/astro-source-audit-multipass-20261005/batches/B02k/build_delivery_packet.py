"""Build a complete packet, then actually extract, hash-check and execute it."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

BATCH = Path(__file__).resolve().parent
NAME = "Astrology-Lilly-Sixth-House-Opening-Records-20261010"
EXCLUDED_NAMES = {
    "ARCHIVE_CONTENT_MANIFEST.json", "DELIVERABLES_MANIFEST.json", "DELIVERY_RECEIPT.json",
    "PACKET_USABILITY.json", "TEST_PACKET_USABILITY.txt", "FINAL_PRESERVATION_CHECK.json",
    "FINAL_PUBLICATION_RECEIPT.json", "FINAL_RESPONSE.md", "FINAL_RESPONSE_TEMPLATE.md",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    destination = BATCH / "deliverables"
    destination.mkdir(exist_ok=True)
    entries = []
    for path in sorted(BATCH.rglob("*")):
        relative = path.relative_to(BATCH)
        if not path.is_file() or any(part in {"deliverables", "__pycache__", ".pytest_cache", "final_gate"} for part in relative.parts):
            continue
        if path.name in EXCLUDED_NAMES or path.name.startswith("."):
            continue
        data = path.read_bytes()
        entries.append({"path": str(relative), "bytes": len(data), "sha256": sha(data)})
    manifest = {"batch": "B02k", "payload_file_count": len(entries), "files": entries,
                "self_exclusion": "This manifest does not hash itself. ZIP and extracted-run receipts are external.",
                "test_entrypoint": "python run_verification.py"}
    manifest_raw = (json.dumps(manifest, indent=2) + "\n").encode()
    (BATCH / "ARCHIVE_CONTENT_MANIFEST.json").write_bytes(manifest_raw)
    zip_path = destination / (NAME + ".zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for entry in entries:
            archive.write(BATCH / entry["path"], "B02k/" + entry["path"])
        archive.writestr("B02k/ARCHIVE_CONTENT_MANIFEST.json", manifest_raw)
    verification = Path(tempfile.mkdtemp(prefix="lilly-b02k-actual-zip-"))
    with zipfile.ZipFile(zip_path) as archive:
        assert archive.testzip() is None
        archive.extractall(verification)
    extracted = verification / "B02k"
    verified = []
    for entry in entries:
        raw = (extracted / entry["path"]).read_bytes()
        assert len(raw) == entry["bytes"] and sha(raw) == entry["sha256"], entry["path"]
        verified.append(entry["path"])
    assert (extracted / "ARCHIVE_CONTENT_MANIFEST.json").read_bytes() == manifest_raw
    hash_check = subprocess.run([sys.executable, "verify_archive_contents.py"], cwd=extracted,
                                capture_output=True, text=True)
    assert hash_check.returncode == 0, hash_check.stdout + hash_check.stderr
    execution = subprocess.run([sys.executable, "run_verification.py"], cwd=extracted,
                               capture_output=True, text=True)
    log = execution.stdout + execution.stderr
    (BATCH / "TEST_PACKET_USABILITY.txt").write_text(log)
    summary = json.loads((extracted / "TEST_RUN_SUMMARY.json").read_text())
    assert execution.returncode == 0 and summary["successful"], log
    published_summary = json.loads((BATCH / "TEST_RUN_SUMMARY.json").read_text())
    assert summary["discovered_test_ids"] == published_summary["discovered_test_ids"]
    assert summary["test_files"] == published_summary["test_files"]
    receipt = {"batch": "B02k", "archive_filename": zip_path.name, "archive_bytes": zip_path.stat().st_size,
               "archive_sha256": sha(zip_path.read_bytes()), "actual_extraction": True,
               "zip_crc_check": "PASS", "payload_file_hashes_verified": len(verified),
               "manifest_itself_verified_separately": True, "payload_paths_verified": verified,
               "archive_hash_checker_exit_code": hash_check.returncode,
               "standalone_test_command": "python run_verification.py", "test_exit_code": execution.returncode,
               "tests_run": summary["tests_run"], "failures": summary["failures"], "errors": summary["errors"],
               "unique_test_ids_match_source_suite": True, "tested_code_and_data_hashes_match": True,
               "distinct_tests_added_by_archive_repeat": 0,
               "test_log_sha256": sha(log.encode()), "clinical_or_predictive_validation": False,
               "extraction_location": "fresh temporary directory; exact transient path omitted from delivery metadata"}
    (BATCH / "PACKET_USABILITY.json").write_text(json.dumps(receipt, indent=2) + "\n")
    files = [(BATCH / "AUDIT_REPORT.md", "Astrology-Lilly-Sixth-House-Opening-20261010.md"),
             (BATCH / "CONTINUE_HANDOFF.md", "Astrology-Lilly-Handoff-B02k-20261010.md")]
    for source, filename in files:
        shutil.copyfile(source, destination / filename)
    outputs = []
    for path in sorted(destination.iterdir()):
        if path.is_file():
            data = path.read_bytes()
            outputs.append({"path": str(path.relative_to(BATCH)), "filename": path.name,
                            "bytes": len(data), "sha256": sha(data),
                            "git_blob_sha": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()})
    (BATCH / "DELIVERABLES_MANIFEST.json").write_text(json.dumps({"batch": "B02k", "files": outputs}, indent=2) + "\n")
    print(json.dumps({"archive": str(zip_path), "verified_payload_files": len(verified),
                      "standalone_tests": summary["tests_run"], "output_files": len(outputs),
                      "archive_sha256": receipt["archive_sha256"]}))


if __name__ == "__main__":
    main()
