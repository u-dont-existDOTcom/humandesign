"""Prepare B02l companions, then actually extract, hash-check and run the suite.

Adapted from B02k/build_delivery_packet.py. Root must invoke this only after its
final review acceptance. This script does not grant or replace that acceptance.

From a private preparation directory, pass --batch /absolute/path/to/B02l.
Once copied into the canonical B02l directory, the parent directory is the
default. This module has no packaging side effects when imported.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile


BATCH_ID = "B02l"
ARCHIVE_NAME = "Astrology-Lilly-Dariot-Records-20261010.zip"
REPORT_NAME = "Astrology-Lilly-Dariot-Report-20261010.md"
CONTINUE_NAME = "Astrology-Lilly-Dariot-Continue-20261010.md"
MANIFEST_NAME = "ARCHIVE_CONTENT_MANIFEST.json"
COMPANION_SOURCES = {
    "AUDIT_REPORT.md": REPORT_NAME,
    "CONTINUE_HANDOFF.md": CONTINUE_NAME,
}

# Outputs produced by packaging, delivery, publication or the final-clock phase
# must not become inputs to a later packaging pass. Review/acceptance evidence
# itself remains eligible; the word FINAL alone is deliberately not excluded.
EXCLUDED_NAMES = {
    MANIFEST_NAME,
    "DELIVERABLES_MANIFEST.json",
    "DELIVERY_RECEIPT.json",
    "OWNER_DELIVERY_PREFLIGHT.json",
    "PACKET_USABILITY.json",
    "TEST_PACKET_USABILITY.txt",
    "TEST_ARCHIVE_HASHES.txt",
    "FINAL_PRESERVATION_CHECK.json",
    "FINAL_INTEGRATION_READBACK.json",
    "FINAL_PUBLICATION_RECEIPT.json",
    "FINAL_RESPONSE.md",
    "FINAL_RESPONSE_TEMPLATE.md",
    "GATE_EVIDENCE_DRAFT.json",
    ARCHIVE_NAME,
    REPORT_NAME,
    CONTINUE_NAME,
}
EXCLUDED_DIRECTORY_NAMES = {
    "deliverables", "delivery", "archives", "archive", "packets",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "final_gate", "final_clock", "clock_receipts",
}
ARCHIVE_SUFFIXES = {
    ".zip", ".tar", ".tgz", ".gz", ".bz2", ".xz", ".7z", ".rar",
}
GENERATED_METADATA_SUFFIXES = {".json", ".md", ".txt", ".log"}
REQUIRED_PAYLOAD_PATHS = {
    "AUDIT_REPORT.md",
    "CONTINUE_HANDOFF.md",
    "RULES.json",
    "SECTION_COVERAGE.json",
    "UNRESOLVED.json",
    "REFERENCE_TABLES.json",
    "LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json",
    "RETAINED_LILLY_INDEX_BEFORE.json",
    "SOURCE_IDENTITY.json",
    "SOURCE_WINDOW_VERIFICATION.json",
    "evidence/Lilly-Dariot-Original-Source-Window.pdf",
    "lilly_dariot_reference.py",
    "test_lilly_dariot.py",
    "run_verification.py",
    "TEST_RUN_SUMMARY.json",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def excluded(relative):
    """Return an exclusion reason, or None for an eligible batch-relative path."""
    if any(part.startswith(".") for part in relative.parts):
        return "hidden file or directory"
    if any(part.lower() in EXCLUDED_DIRECTORY_NAMES for part in relative.parts):
        return "cache, prior delivery/archive directory, or final-clock directory"
    if relative.name in EXCLUDED_NAMES:
        return "generated delivery/archive/final-output receipt"
    if relative.suffix.lower() in ARCHIVE_SUFFIXES:
        return "existing archive"
    upper = relative.name.upper()
    if relative.suffix.lower() in GENERATED_METADATA_SUFFIXES:
        if upper.startswith(("ASTROLOGY-LILLY-", "ASTROLOGY_LILLY_")):
            return "existing owner-facing companion output"
        if "PUBLICATION" in upper:
            return "publication metadata"
        if "CLOCK" in upper and ("FINAL" in upper or "RECEIPT" in upper):
            return "final-clock receipt"
        if upper.startswith(("DELIVERY_", "DELIVERABLES_", "ARCHIVE_", "PACKET_USABILITY")):
            return "generated delivery/archive metadata"
        if upper.startswith("OWNER_DELIVERY_"):
            return "owner delivery metadata"
    return None


def snapshot_payload(batch):
    """Read each eligible file once; those exact bytes form both ZIP and hashes."""
    payload = {}
    exclusions = []
    for path in sorted(batch.rglob("*")):
        relative = path.relative_to(batch)
        reason = excluded(relative)
        if path.is_symlink():
            exclusions.append({"path": relative.as_posix(), "reason": "symbolic link"})
            continue
        if not path.is_file():
            continue
        if reason:
            exclusions.append({"path": relative.as_posix(), "reason": reason})
            continue
        payload[relative.as_posix()] = path.read_bytes()
    missing = sorted(REQUIRED_PAYLOAD_PATHS - payload.keys())
    require(not missing, "Completed batch payload is missing: " + ", ".join(missing))
    require(any(name.startswith("independent_review/") for name in payload),
            "Completed batch must include its independent-review evidence.")
    return payload, exclusions


def manifest_for(payload):
    entries = [
        {"path": name, "bytes": len(raw), "sha256": sha(raw)}
        for name, raw in sorted(payload.items())
    ]
    return {
        "batch": BATCH_ID,
        "payload_file_count": len(entries),
        "files": entries,
        "self_exclusion": (
            "This manifest does not hash itself. The archive and extracted-run, "
            "delivery, publication and final-clock receipts are external."
        ),
        "test_entrypoint": "python run_verification.py",
        "repeat_accounting": "The extracted execution repeats the same suite and adds zero distinct tests.",
    }


def validate_source_suite(payload):
    summary = json.loads(payload["TEST_RUN_SUMMARY.json"])
    require(summary.get("successful") is True, "Source standalone suite has no successful result.")
    ids = summary.get("discovered_test_ids")
    require(isinstance(ids, list) and bool(ids), "Source suite has no recorded test identities.")
    require(summary.get("distinct_test_count") == len(set(ids)),
            "Source summary's distinct-test count does not match its test identities.")
    tested_files = summary.get("test_files")
    require(isinstance(tested_files, list) and bool(tested_files),
            "Source summary has no tested code/data hash manifest.")
    for entry in tested_files:
        name = entry["path"]
        require(name in payload, "Tested file is absent from payload: " + name)
        require(sha(payload[name]) == entry["sha256"],
                "Source test result no longer matches the payload bytes: " + name)
    return summary


def write_zip(zip_path, payload, manifest_raw):
    """Use deterministic ZIP metadata; the fixed date is not an issuance time."""
    members = dict(payload)
    members[MANIFEST_NAME] = manifest_raw
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(BATCH_ID + "/" + name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def actual_extract_and_verify(zip_path, extraction_parent, manifest, manifest_raw):
    expected = {BATCH_ID + "/" + item["path"] for item in manifest["files"]}
    expected.add(BATCH_ID + "/" + MANIFEST_NAME)
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "Archive has duplicate member names.")
        require(set(names) == expected, "Archive member set differs from the payload manifest.")
        for name in names:
            relative = PurePosixPath(name)
            require(not relative.is_absolute() and ".." not in relative.parts,
                    "Unsafe archive member path: " + name)
        bad_crc = archive.testzip()
        require(bad_crc is None, "ZIP CRC check failed: " + str(bad_crc))
        archive.extractall(extraction_parent)
    extracted = extraction_parent / BATCH_ID
    checked = []
    for entry in manifest["files"]:
        raw = (extracted / entry["path"]).read_bytes()
        require(len(raw) == entry["bytes"] and sha(raw) == entry["sha256"],
                "Extracted payload content mismatch: " + entry["path"])
        checked.append(entry["path"])
    require((extracted / MANIFEST_NAME).read_bytes() == manifest_raw,
            "The extracted manifest differs from its separately checked original bytes.")
    return extracted, checked


def run_extracted_suite(extracted, published_summary):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    checker = None
    checker_log = "No separate checker file; the builder verified every extracted payload hash.\n"
    if (extracted / "verify_archive_contents.py").is_file():
        checker = subprocess.run(
            [sys.executable, "verify_archive_contents.py"], cwd=extracted,
            capture_output=True, text=True, env=env,
        )
        checker_log = checker.stdout + checker.stderr
        require(checker.returncode == 0, "Extracted archive checker failed:\n" + checker_log)
    execution = subprocess.run(
        [sys.executable, "run_verification.py"], cwd=extracted,
        capture_output=True, text=True, env=env,
    )
    suite_log = execution.stdout + execution.stderr
    require(execution.returncode == 0, "Extracted standalone suite failed:\n" + suite_log)
    summary = json.loads((extracted / "TEST_RUN_SUMMARY.json").read_bytes())
    require(summary.get("successful") is True, "Extracted suite was not successful:\n" + suite_log)
    require(summary["discovered_test_ids"] == published_summary["discovered_test_ids"],
            "Extracted suite discovered different test identities.")
    require(summary["test_files"] == published_summary["test_files"],
            "Extracted suite's tested code/data hashes differ from the source suite.")
    for entry in summary["test_files"]:
        require(sha((extracted / entry["path"]).read_bytes()) == entry["sha256"],
                "Tested code/data changed during the extracted suite: " + entry["path"])
    for key in ("tests_run", "distinct_test_count", "failures", "errors", "skipped"):
        require(summary[key] == published_summary[key],
                "Extracted/source test summaries differ at " + key)
    log = ("=== Extracted archive hash verification ===\n" + checker_log
           + "\n=== Extracted standalone suite ===\n" + suite_log)
    return summary, execution.returncode, None if checker is None else checker.returncode, log


def atomic_write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    staged = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix="." + path.name + ".", delete=False) as stream:
            staged = Path(stream.name)
            stream.write(raw)
        staged.replace(path)
    finally:
        if staged is not None and staged.exists():
            staged.unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, default=Path(__file__).resolve().parent,
                        help="Completed canonical B02l directory; default is this script's parent.")
    args = parser.parse_args(argv)
    batch = args.batch.resolve()
    require(batch.is_dir(), "Batch directory does not exist: " + str(batch))
    require(batch.name == BATCH_ID, "Expected the canonical B02l directory; pass --batch explicitly.")

    payload, exclusions = snapshot_payload(batch)
    source_summary = validate_source_suite(payload)
    manifest = manifest_for(payload)
    manifest_raw = json_bytes(manifest)

    # Stage and verify first. No completed-delivery files are replaced until the
    # actual extracted payload and repeated standalone suite have both passed.
    with tempfile.TemporaryDirectory(prefix="lilly-b02l-actual-zip-") as temporary:
        staging = Path(temporary)
        staged_zip = staging / ARCHIVE_NAME
        write_zip(staged_zip, payload, manifest_raw)
        extracted, checked = actual_extract_and_verify(
            staged_zip, staging / "extracted", manifest, manifest_raw,
        )
        summary, test_exit, checker_exit, log = run_extracted_suite(extracted, source_summary)
        archive_raw = staged_zip.read_bytes()

    receipt = {
        "batch": BATCH_ID,
        "archive_filename": ARCHIVE_NAME,
        "archive_bytes": len(archive_raw),
        "archive_sha256": sha(archive_raw),
        "actual_extraction": True,
        "zip_crc_check": "PASS",
        "archive_member_set_matches_manifest": True,
        "payload_file_hashes_verified": len(checked),
        "payload_paths_verified": checked,
        "manifest_itself_verified_separately": True,
        "payload_hash_verification_method": "Every extracted file checked against its expected byte count and SHA-256 before tests.",
        "archive_hash_checker_exit_code": checker_exit,
        "separate_archive_checker_present": checker_exit is not None,
        "standalone_test_command": "python run_verification.py",
        "test_exit_code": test_exit,
        "tests_run": summary["tests_run"],
        "distinct_test_count": summary["distinct_test_count"],
        "failures": summary["failures"],
        "errors": summary["errors"],
        "skipped": summary["skipped"],
        "unique_test_ids_match_source_suite": True,
        "tested_code_and_data_hashes_match": True,
        "tested_files": summary["test_files"],
        "distinct_tests_added_by_archive_repeat": 0,
        "repeat_purpose": "Portability and usability check of the same standalone suite.",
        "test_log_sha256": sha(log.encode("utf-8")),
        "clinical_or_predictive_validation": False,
        "independent_review_created_by_packaging": False,
        "extraction_location": "Fresh temporary directory; exact transient path omitted from delivery metadata.",
        "excluded_existing_files": exclusions,
    }
    destination = batch / "deliverables"
    output_bytes = {ARCHIVE_NAME: archive_raw}
    output_bytes.update({name: payload[source] for source, name in COMPANION_SOURCES.items()})
    outputs = []
    for name, raw in sorted(output_bytes.items()):
        atomic_write(destination / name, raw)
        outputs.append({
            "path": "deliverables/" + name,
            "filename": name,
            "bytes": len(raw),
            "sha256": sha(raw),
            "git_blob_sha": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
        })
    atomic_write(batch / MANIFEST_NAME, manifest_raw)
    atomic_write(batch / "TEST_PACKET_USABILITY.txt", log.encode("utf-8"))
    atomic_write(batch / "PACKET_USABILITY.json", json_bytes(receipt))
    atomic_write(batch / "DELIVERABLES_MANIFEST.json", json_bytes({"batch": BATCH_ID, "files": outputs}))
    print(json.dumps({
        "archive": str(destination / ARCHIVE_NAME),
        "verified_payload_files": len(checked),
        "standalone_tests": summary["tests_run"],
        "distinct_test_count": summary["distinct_test_count"],
        "distinct_tests_added_by_archive_repeat": 0,
        "output_files": [entry["filename"] for entry in outputs],
        "archive_sha256": receipt["archive_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()
