#!/usr/bin/env python3
"""Source boundary and exact original first-edition photographs for printed CLXI."""

import hashlib
import json
import shutil
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PARENT = B.parent / "B07q"
PARENT_WINDOW = json.loads((PARENT / "ORIGINAL_SOURCE_WINDOW_V1.json").read_text())
CANONICAL = (
    ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
)


def hash_bytes(b):
    return hashlib.sha256(b).hexdigest()


i = json.loads(CANONICAL.read_text())
assert i["records_count"] == 11325 and i["batches"][-1]["id"] == "B07q"
assert i["next"]["chapter"] == "CLXI"
assert i["next"]["pdf_page"] == 711
assert PARENT_WINDOW["printed_CLX"]["ends_original_pdf"] == 711
assert PARENT_WINDOW["following_printed_CLXI"]["heading_original_pdf"] == 711
assert PARENT_WINDOW["following_printed_CLXII"]["heading_original_pdf"] == 713
out = {}
for n in range(711, 715):
    source = PARENT / "evidence" / f"pdf_1647-{n}.jpg"
    target = B / "evidence" / source.name
    original = source.read_bytes()
    proof = PARENT_WINDOW["photos"][str(n)]
    assert original[:2] == b"\xff\xd8" and len(original) == proof["bytes"]
    assert hash_bytes(original) == proof["sha256"]
    if not target.exists():
        shutil.copyfile(source, target)
    assert target.read_bytes() == original
    out[str(n)] = {
        "file": str(target.relative_to(B)),
        "bytes": len(original),
        "sha256": hash_bytes(original),
        "original_pdf_frame": n,
        "printed_page": n - 34,
        "chapter_role": (
            "CLXI_PRINTED_BODY_OVERLAP_PREVIOUS_CLX"
            if n == 711
            else "CLXI_PRINTED_BODY_OVERLAP_NEXT_CLXII"
            if n == 713
            else "CLXI_PRINTED_BODY"
            if n == 712
            else "CLXII_NEXT_SOURCE_CONTEXT_ONLY"
        ),
    }

new = {
    "schema": "LILLY_1647_PRINTED_CLXI_SOURCE_WINDOW_V1",
    "batch": "B07r",
    "source": "William Lilly, Christian Astrology, original 1647 first edition, Wellcome b30338724",
    "original_full_pdf_sha256": PARENT_WINDOW["original_pdf_894_frames_sha256"],
    "accepted_before_clxi": 11325,
    "next_R": "R11326",
    "accepted_chapter_before": "CLX",
    "expected_chapter": "CLXI",
    "body_original_pdf_frames": [711, 712, 713],
    "chapter_starts_frame": 711,
    "chapter_ends_frame": 713,
    "following_separate_heading": "CHAP CLXII The Sunne directed to Promittors",
    "next_chapter_starts_frame": 713,
    "source_seam": (
        "PDF711 prior CLX above divider, CLXI body below; "
        "PDF713 CLXI above divider, CLXII body below."
    ),
    "photos": out,
    "source_only": True,
    "empirical_person_validations": 0,
    "runtime_promotions": 0,
    "prior_index_sha256": hash_bytes(CANONICAL.read_bytes()),
    "chinese_v2_records": 97,
}
(B / "ORIGINAL_SOURCE_WINDOW_V1.json").write_text(
    json.dumps(new, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print("B07r photographic witness complete", [(n, v["sha256"][:12]) for n, v in out.items()])
