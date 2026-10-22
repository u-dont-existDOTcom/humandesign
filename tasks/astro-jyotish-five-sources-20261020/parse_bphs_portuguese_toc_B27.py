"""Reconstruct headings from the original uploaded Portuguese BPHS text, without republishing it.

Usage: python3 parse_bphs_portuguese_toc_B27.py '/local/source.txt' [--output headings.json]
One-based locators reflect the Portuguese TRANSLATION, not original Sanskrit chapters.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

SOURCE_SHA256 = "d271b96457dade884ae4fd0c268d09e88696beeca707fce2b1d2159aa6084b62"
NUMBERED_HEADING = re.compile(r"^\d{1,3}\.\s+\S")
KNOWN_EXTRAS = {743, 2528, 2562, 2653, 3142, 5404, 5533, 5581, 5743}


def normalize(value: str) -> str:
    folded = "".join(char for char in unicodedata.normalize("NFKD", value)
                     if not unicodedata.combining(char)).casefold().strip()
    return re.sub(r"\s+", " ", folded)


def build(path: Path) -> dict:
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError(f"Wrong edition/file: SHA-256 {digest} != {SOURCE_SHA256}")
    lines = data.decode("cp1252").splitlines()
    if len(lines) != 5941 or lines[9].strip() != "Contents":
        raise ValueError("Changed source structure or nonmatching table of contents")
    toc = [(ix + 1, lines[ix].strip()) for ix in range(15, 189, 2)]
    if len(toc) != 87 or toc[-1][1] != "Conclusão":
        raise ValueError("87 headings including conclusion not found")
    prev = 189
    headings = []
    for original_idx, title in toc:
        candidates = [idx for idx in range(prev + 1, len(lines))
                      if normalize(lines[idx]) == normalize(title)]
        if not candidates:
            raise ValueError(f"Body heading missing or out of order: {title}")
        found = candidates[0]
        headings.append({"title": title, "toc_line_1based": original_idx,
                         "body_line_1based": found + 1})
        prev = found
    numbered = [{"body_line_1based": ix + 1, "heading": line.strip()}
                for ix, line in enumerate(lines[190:], start=190)
                if NUMBERED_HEADING.match(line.strip())]
    numbered_lines = {item["body_line_1based"] for item in numbered}
    if numbered_lines != KNOWN_EXTRAS:
        raise ValueError(f"Numbered hidden heading set changed: {numbered_lines}")
    extra = [ix + 1 for ix, line in enumerate(lines)
             if normalize(line) == normalize("Remédio Para Nascimento Gandanta de Jyeshtha")]
    if extra != [5892]:
        raise ValueError(f"Gandanta subsection moved: {extra}")
    if [item["body_line_1based"] for item in headings][:3] != [214, 245, 256]:
        raise ValueError("Early heading line check failed")
    return {"schema_version": 1, "source_sha256": digest,
            "line_count": len(lines), "source_encoding": "cp1252",
            "toc_count_including_conclusion": len(headings), "toc_headings": headings,
            "body_only_numbered_headings": numbered,
            "additional_unnumbered_headings": [{
                "body_line_1based": 5892,
                "heading": "Remédio Para Nascimento Gandanta de Jyeshtha"}],
            "scope": "Edition navigation audit, not Sanskrit or predictive verification."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.source)
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(json.dumps({"toc_count": result["toc_count_including_conclusion"],
                          "body_only_numbered": len(result["body_only_numbered_headings"]),
                          "additional_unnumbered": len(result["additional_unnumbered_headings"]),
                          "source_sha256": result["source_sha256"]}))


if __name__ == "__main__":
    main()
