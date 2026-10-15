"""Package B02v unaccepted documentary source work with actual extract/replay.

No canonical index mutation, source-fidelity certification, human outcomes, or
predictive validity claim is authorized by a successful archive/test run.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile
import zipfile

B = Path(__file__).resolve().parent
DEST = Path("/mnt/hdd/home/joel/Téléchargements")
FILENAME = "Astrology-Lilly-B02v-Provisional-Source-Packet-v5-20261014.zip"
ARCHIVE = B / "independent_review" / FILENAME
MANIFEST_NAME = "SOURCE_PACKET_MANIFEST.json"
SUITES = [
    "test_b02v_staging.py",
    "test_source_integrity_v8.py",
    "independent_review/test_reconciled_draft.py",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def zipinfo(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=(2026, 10, 14, 0, 0, 0))
    info.create_system = 3
    info.external_attr = 0o644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def select():
    files = []
    for path in B.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(B)
        parts = rel.parts
        if "__pycache__" in parts or "review_images" in parts:
            continue
        if path == ARCHIVE or rel.name.endswith(".zip"):
            continue
        if rel.name == MANIFEST_NAME or rel.name.startswith("."):
            continue
        if path.suffix not in {".json", ".md", ".py", ".png"}:
            continue
        if any(part in {"..", ".git"} for part in parts):
            raise ValueError("Unexpected path " + str(rel))
        files.append(rel)
    return sorted(files, key=lambda p: p.as_posix())


def main():
    files = select()
    assert len(files) >= 45, len(files)
    relative = {p.as_posix() for p in files}
    assert {f"evidence/pdf-{p}.png" for p in range(381, 401)} <= relative
    assert "evidence/errata-888.png" in relative
    assert set(SUITES) <= relative
    counts = json.loads((B / "COUNTS.json").read_text())
    assert counts["accepted_new_documentary_records"] == 0
    assert counts["proposed_new_documentary_records"] == 402
    manifest = {
        "kind": "UNACCEPTED_B02v_ORIGINAL_SOURCE_RESEARCH_ONLY",
        "source": "William Lilly, Christian Astrology (1647), original PDF381-400 inclusive, errata PDF888",
        "source_sha256": "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        "accepted_lilly_remains": 2572,
        "provisional_documentary_units": 402,
        "source_uncertainty_ledger_count": 58,
        "source_correction_R2835": "Original printed page360 SIXTH house for servant; first-house transcription rejected",
        "source_correction_R2674_R2675": "Haly/Leo/Venus printed attribution and configuration",
        "source_correction_R2973": "Moon eighth OPPOSITION to Mars second, not conjunction",
        "source_corrections_U56_U58": "Restored retrieval consequent, plural significators, and unresolved beholding actor",
        "cumulative_if_accepted_is_not_current": 2974,
        "source_semantics_independently_fully_reviewed": False,
        "source_book_completion_admitted": False,
        "source_record_experimental_outcomes": 0,
        "files": [],
    }
    for rel in files:
        blob = (B / rel).read_bytes()
        manifest["files"].append({
            "path": rel.as_posix(),
            "size": len(blob),
            "sha256": sha256(blob),
        })
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as z:
        for rel in files:
            z.writestr(zipinfo(rel.as_posix()), (B / rel).read_bytes())
        z.writestr(zipinfo(MANIFEST_NAME), json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")

    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == relative | {MANIFEST_NAME}
        archive_manifest = json.loads(z.read(MANIFEST_NAME))
        assert archive_manifest == manifest
        for file in manifest["files"]:
            payload = z.read(file["path"])
            assert (len(payload), sha256(payload)) == (file["size"], file["sha256"]), file["path"]

    replay = {}
    with tempfile.TemporaryDirectory(prefix="lilly-b02v-replay-") as tmp:
        with zipfile.ZipFile(ARCHIVE) as z:
            for info in z.infolist():
                assert not PurePosixPath(info.filename).is_absolute()
                assert ".." not in PurePosixPath(info.filename).parts
            z.extractall(tmp)
        for suite in SUITES:
            proc = subprocess.run(["python3", str(Path(tmp) / suite)], capture_output=True, text=True, timeout=180)
            replay[suite] = {
                "exit_code": proc.returncode,
                "last_lines": (proc.stdout + proc.stderr).splitlines()[-5:],
            }
            if proc.returncode != 0:
                print(json.dumps({"failed_replay": replay}, indent=2))
                raise RuntimeError(f"Extracted source-only test failed: {suite}")

    DEST.mkdir(parents=True, exist_ok=True)
    target = DEST / FILENAME
    digest = sha256(ARCHIVE.read_bytes())
    if target.exists():
        assert sha256(target.read_bytes()) == digest, "Existing owner download differs; refusing overwrite"
    else:
        with target.open("xb") as fh:
            with ARCHIVE.open("rb") as src:
                shutil.copyfileobj(src, fh)
    assert sha256(target.read_bytes()) == digest
    receipt = {
        "archive_status": manifest["kind"],
        "source_count": len(files),
        "source_png_count": len([x for x in files if x.suffix == ".png" and x.parts[0] == "evidence"]),
        "archive_size_bytes": ARCHIVE.stat().st_size,
        "archive_sha256": digest,
        "owner_download_path": str(target),
        "owner_download_sha256": sha256(target.read_bytes()),
        "archive_crc_pass": True,
        "all_archived_files_sha256_pass": True,
        "actual_extraction_pass": True,
        "actual_extracted_tests": replay,
        "full_independent_semantic_review": False,
        "source_accepted": False,
        "canonical_index_advanced": False,
    }
    receipt_path = B / "independent_review" / "PROVISIONAL_SOURCE_PACKET_RECEIPT_v5_20261014.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
