"""Deliver the accepted Lilly III contents and complete original OCR to owner Downloads.

Only public-domain original source and researcher-written aggregate artifacts;
no participant files, birth/chart data, service credential, or GPT edits.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FOLDER = "Life-Patterns-Astrology-Source-Audit-2026-10-17/Lilly-Book-III-Contents-Census"
RECORDS = (
    "LILLY3-NATAL-DOMAIN-CENSUS-v1.json",
    "SOURCE-TO-SURVEY-RESULT.md",
    "VERIFICATION-RECEIPT.json",
    "build_toc_census.py",
)
FULL_OCR_NAME = "original-public-domain-Lilly-1647-full-ocr.txt"
EXPECTED_HASH = "7c08b55359c41049c5d43901b8da869a326f8eb852e4a30603a4b698533626aa"
README = """# Lilly Book III original contents to Life Patterns V7

Open SOURCE-TO-SURVEY-RESULT.md. The accompanying JSON records 29 original
1647 contents topics and their exact source OCR anchor text/character offsets,
with conservative labels for V7 coverage and ethically sensitive historical
claims. The full original public-domain 1647 archived OCR witness is included
for independent reproduction. Printed folios and planet glyphs still need
facsimile comparison before an executable natal chart rule is written.

This is not the Lilly III religion/dream 31-source-unit rule extraction; that
separate accepted project already exists in the parent astrology audit folder.
This is not a claim that traditional astrology predicts any human outcome.
No existing questionnaires, GPT, Railway service, or chart scoring changed.
"""


def downloads_path() -> Path:
    try:
        cp = subprocess.run(
            ["xdg-user-dir", "DOWNLOAD"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        if cp.returncode == 0 and cp.stdout.strip():
            path = Path(cp.stdout.strip())
            if path.exists():
                return path
    except (OSError, subprocess.TimeoutExpired):
        pass
    path = Path.home() / "Téléchargements"
    if not path.is_dir():
        raise ValueError("Cannot resolve owner's existing Downloads directory")
    return path


def check_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        if path.read_bytes() != content:
            raise ValueError("Existing owner file has other contents: " + path.name)
    else:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(content)
    path.chmod(0o600)
    if hashlib.sha256(path.read_bytes()).digest() != hashlib.sha256(content).digest():
        raise ValueError("Owner download readback failed: " + path.name)


def deliver(ocr: Path, downloads: Path) -> dict:
    original = ocr.read_bytes()
    if hashlib.sha256(original).hexdigest() != EXPECTED_HASH:
        raise ValueError("The public historical source is not the accepted 1647 OCR bytes")
    target = downloads / FOLDER
    for filename in RECORDS:
        check_write(target / filename, (HERE / filename).read_bytes())
    check_write(target / FULL_OCR_NAME, original)
    check_write(target / "START-HERE.md", README.encode("utf-8"))
    return {
        "owner_downloads": str(target),
        "records": len(RECORDS),
        "original_witness_bytes": len(original),
        "total_files": len(RECORDS) + 2,
        "copy_readback": "MATCHED_EXACT_SOURCE_BYTES",
        "questionnaire_unchanged": True,
        "no_private_human_source": True,
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ocr", type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(deliver(a.ocr, downloads_path()), ensure_ascii=False))
