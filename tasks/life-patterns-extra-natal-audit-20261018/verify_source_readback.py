"""Prove bounded source phrase readback without publishing copyrighted source text.

Online readback is an explicit discretionary research operation, not part of
ordinary CI. Offline tests verify its accepted receipt and frozen inventory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import urllib.request
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

TASK = Path(__file__).resolve().parent
DATA = TASK / "SOURCE-ANCHORS-v2.json"
OUTPUT = TASK / "SOURCE-READBACK-v2.json"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).casefold()


def inspect(valens_repo: Path) -> dict[str, Any]:
    spec = json.loads(DATA.read_text(encoding="utf-8"))
    actual_commit = subprocess.check_output(
        ["git", "-C", str(valens_repo), "rev-parse", "HEAD"], text=True
    ).strip()
    expected_commit = spec["new_sources"][0]["git_commit"]
    assert actual_commit == expected_commit, (actual_commit, expected_commit)
    outcomes = []
    content_by_source = {}
    receipts = {}
    for source in spec["new_sources"]:
        ident = source["id"]
        if source["type"] == "local_pinned_annotated_translation":
            path = valens_repo / source["local_relative"]
            raw = path.read_bytes()
            sha = hashlib.sha256(raw).hexdigest()
            assert sha == source["sha256"], ident
            text = raw.decode("utf-8")
            mode = "source_git_commit_and_exact_local_file_sha"
        else:
            req = urllib.request.Request(
                source["url"],
                headers={"User-Agent": "Mozilla/5.0 (LifePatterns source audit readback)"},
            )
            with urllib.request.urlopen(req, timeout=22) as response:
                assert response.status == 200, (ident, response.status)
                raw = response.read(2500000)
            sha = hashlib.sha256(raw).hexdigest()
            html = BeautifulSoup(raw, "html.parser")
            for tag in html(["script", "style", "noscript"]):
                tag.decompose()
            text = html.get_text(separator=" ", strip=True)
            mode = "retrieved_web_html_short_phrase_check"
        receipts[ident] = {
            "id": ident,
            "source_type": source["type"],
            "content_sha256": sha,
            "byte_count": len(raw),
            "checked_full_document": True,
            "mode": mode,
            "url": source["url"],
            "source_translation_status": source["status"],
        }
        content_by_source[ident] = normalize(text)
    for item in spec["source_anchors"]:
        ident = item["witness_id"]
        needle = normalize(item["proof_fragment"])
        exists = needle in content_by_source[ident]
        outcomes.append(
            {
                "anchor_id": item["id"],
                "witness_id": ident,
                "proof_fragment": item["proof_fragment"],
                "short_anchor_present": exists,
                "disposition": item["disposition"],
                "not_predictive_validation": True,
            }
        )
    missing = [x for x in outcomes if not x["short_anchor_present"]]
    heading_counts = {}
    for number in range(1, 10):
        chapter = valens_repo / f"book{number:02}"
        assert chapter.is_dir(), chapter
        heading_counts[str(number)] = sum(
            len(re.findall(r"\\(?:sub)?section\*?\{", path.read_text(encoding="utf-8")))
            for path in chapter.glob("*.tex")
        )
    assert sum(heading_counts.values()) >= 200
    result = {
        "schema": "life-patterns-cross-tradition-source-phrase-readback-v2",
        "retrieved_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "status": "PASS" if not missing else "INCOMPLETE_PLEASE_RESOLVE_MISSING_ANCHORS",
        "valens_nine_book_section_heading_scan": {
            "headings_by_book": heading_counts,
            "total_headings": sum(heading_counts.values()),
            "full_section_contents_exhaustively_reviewed": False,
            "scope": (
                "Section and subsection headings only: not natal rule extraction "
                "or a proof of no remaining topical omissions."
            ),
        },
        "source_files_or_pages": receipts,
        "anchor_readbacks": outcomes,
        "counts": {
            "source_witnesses": len(receipts),
            "claimed_source_rows": len(outcomes),
            "verified_short_phrase_rows": len(outcomes) - len(missing),
            "missing_rows": len(missing),
            "dispositions": dict(Counter(x["disposition"] for x in outcomes)),
        },
        "missing_anchor_ids": [x["anchor_id"] for x in missing],
        "scope": (
            "Brief translated words confirm source topics. No ancient chart prediction "
            "or questionnaire response validity is inferred."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--valens-dir", type=Path, required=True)
    options = parser.parse_args()
    data = inspect(options.valens_dir)
    print(
        json.dumps(
            {
                "status": data["status"],
                "counts": data["counts"],
                "missing": data["missing_anchor_ids"],
                "record_file": OUTPUT.name,
            }
        )
    )
    if data["missing_anchor_ids"]:
        raise SystemExit(1)
