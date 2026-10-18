#!/usr/bin/env python3
"""Build provisional Naibod table records from a frozen public-domain text witness.

Input: locally cached HTML-readable transcription of Lilly's 1647 volume III
from a modern public scan/reprint; never treat secondary text as authoritative
over original 1647 Wellcome photographs. No OCR, ephemeris or chart calculation.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

B = Path(__file__).resolve().parent
SOURCE_URL = "https://pdfcoffee.com/william-lilly-christian-astrology-volume-3-pdf-free.html"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def table_degrees(content: str):
    start = content.index("A most exact Table according to the opinion of Naibod")
    end = content.index("A table for the converting of minutes", start)
    snippet = content[start:end]
    parts = re.split(r"\bDEG ", snippet)[1:]
    assert len(parts) == 3
    rows = []
    for group, part in enumerate(parts):
        degrees, rest = part.split(" YR. ", 1)
        years, rest = rest.split(" DAY ", 1)
        days, hours = rest.split(" HR. ", 1)
        numbers = [
            [int(s) for s in re.findall(r"\b\d+\b", field)]
            for field in (degrees, years, days, hours)
        ]
        if group == 1:
            assert numbers[2][-1] == 713, "Remove only the printed folio 713"
            numbers[2] = numbers[2][:-1]
        assert all(len(column) == 30 for column in numbers), [len(c) for c in numbers]
        for row in zip(*numbers, strict=True):
            deg, secondary_year, day, hour = row
            original_year = deg + 1 if deg >= 69 else deg
            # Original PDF747 visibly normalizes full-year rollover beginning
            # with degree 69; modern flattening transcription fails to carry.
            rows.append(
                {
                    "equatorial_degrees": deg,
                    "printed_1647_years": original_year,
                    "printed_1647_days": day,
                    "printed_1647_hours": hour,
                    "secondary_transcript_years": secondary_year,
                    "original_pdf_frame": 747,
                    "printed_original_folio": 713,
                    "visual_source_conflict_with_secondary_year": deg >= 69,
                    "full_critical_edition_collation": False,
                    "arithmetic_or_personal_prediction_validated": False,
                }
            )
    assert [r["equatorial_degrees"] for r in rows] == list(range(1, 91))
    assert all(r["secondary_transcript_years"] == r["equatorial_degrees"] for r in rows)
    assert rows[68]["printed_1647_years"] == 70
    assert rows[-1]["printed_1647_years"] == 91
    return rows, sha_bytes(snippet.encode("utf-8"))


def table_minutes(content: str):
    start = content.index("A table for the converting of minutes into Dayes and Hours.")
    end = content.index("You see here two Tables,", start)
    snippet = content[start:end]
    marker = "Mn. day Hour Mn. days Hour"
    raw = snippet[snippet.index(marker) + len(marker) :]
    numbers = [int(s) for s in re.findall(r"\b\d+\b", raw)]
    assert len(numbers) == 177
    rows = []
    for pos in range(0, 174, 6):
        minute, day, hour, rminute, rday, rhour = numbers[pos : pos + 6]
        rows.extend(((minute, day, hour), (rminute, rday, rhour)))
    rows.append(tuple(numbers[174:177]))
    rows.sort(key=lambda x: x[0])
    assert [r[0] for r in rows] == [n for n in range(1, 61) if n != 27]
    records = []
    for minute, day, hour in rows:
        notes = []
        if minute == 1:
            notes.append(
                "Primary JPEG seems to read day 5; secondary reads 6. Keep both as unresolved."
            )
        if minute == 8:
            notes.append("Both copies read day 44; neighboring cells imply ~49. Keep 44.")
        if minute in (28, 29, 30):
            notes.append("Original source skips label 27; numbers 28–30 appear offset by a row.")
        if minute == 44:
            notes.append(
                "Source shows 271d 8h, while flanking entries suggest hour digit may be omitted."
            )
        if minute == 60:
            notes.append("Both copies show 374d 14h, against an expected ~370d 14h.")
        records.append(
            {
                "equatorial_arcminutes_as_printed": minute,
                "secondary_days": day,
                "secondary_hours": hour,
                "original_photo_day_ambiguity": [5, 6] if minute == 1 else None,
                "original_pdf_frame": 748,
                "original_printed_folio": 714,
                "source_printed_not_inferred": True,
                "source_anomaly_notes": notes,
                "full_critical_edition_collation": False,
                "usable_without_source_reconciliation_for_timing": not notes,
                "human_event_prediction_validated": False,
            }
        )
    return records, sha_bytes(snippet.encode("utf-8"))


def build(cache: Path):
    raw = cache.read_text(encoding="utf-8")
    degree, hash_degree = table_degrees(raw)
    minute, hash_minute = table_minutes(raw)
    first_edition = json.loads((B / "ORIGINAL_SOURCE_WINDOW_V1.json").read_text())
    assert first_edition["accepted_lilly_before"] == 12472
    assert first_edition["full_source_pdf_sha256"] == (
        "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
    )
    photos = first_edition["photos"]
    for n in ("747", "748"):
        file = B / photos[n]["file"]
        assert sha_bytes(file.read_bytes()) == photos[n]["sha256"]
    minute_missing = sorted(
        set(range(1, 61)) - {r["equatorial_arcminutes_as_printed"] for r in minute}
    )
    assert minute_missing == [27]
    source = {
        "schema": "LILLY_1647_NAIBOD_TWO_TABLES_SOURCE_FIRST_PROVISIONAL_V1",
        "batch": "B07x",
        "research_type": "historic_table_transcription_not_engine_verified",
        "original_source": (
            "William Lilly, Christian Astrology, original first edition 1647, Wellcome b30338724"
        ),
        "first_edition_pdf_sha256": first_edition["full_source_pdf_sha256"],
        "first_edition_degree_photo_sha256": photos["747"]["sha256"],
        "first_edition_minute_photo_sha256": photos["748"]["sha256"],
        "modern_text_transcription_aid_url": SOURCE_URL,
        "text_transcription_note": (
            "Modern searchable rendering is a derivative of a public-domain 1647 text "
            "and may normalize, omit or mistranscribe old digits. Manually observed "
            "primary edition overrides are distinguished from the secondary text."
        ),
        "frozen_secondary_degree_section_sha256": hash_degree,
        "frozen_secondary_minute_section_sha256": hash_minute,
        "degree_rows": degree,
        "minute_rows": minute,
        "degree_rows_count": 90,
        "minute_rows_currently_visible_count": 59,
        "missing_source_minute_labels": minute_missing,
        "minute_degree_0_row_applicable": False,
        "all_minute_rows_unambiguous": False,
        "all_degree_years_crosschecked_expert": False,
        "full_astrological_birth_chart_engine_verified": False,
        "independent_person_outcome_validation_count": 0,
        "runtime_promotions": 0,
    }
    target = B / "NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json"
    target.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "path": str(target.name),
                "degrees": len(degree),
                "minutes": len(minute),
                "missing_minute_labels": minute_missing,
                "year_disagreements_with_secondary": sum(
                    r["visual_source_conflict_with_secondary_year"] for r in degree
                ),
                "minute_anomaly_rows": [
                    r["equatorial_arcminutes_as_printed"]
                    for r in minute
                    if r["source_anomaly_notes"]
                ],
                "sha256": sha_bytes(target.read_bytes()),
                "canonical_index_changed": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cached-readable-text", type=Path, required=True)
    build(parser.parse_args().cached_readable_text)
