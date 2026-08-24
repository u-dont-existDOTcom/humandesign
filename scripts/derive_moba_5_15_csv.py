#!/usr/bin/env python3
"""Derive the frozen MoBa 5-15 predictor from secure registry birth times.

Input CSV columns:
- ``record_id``: pseudonymous identifier to preserve row linkage;
- ``birth_date``: ISO ``YYYY-MM-DD`` Norwegian civil date;
- ``hhmm``: four-digit Norwegian civil clock time.

The output intentionally omits raw birth date/time.  It contains only the
frozen predictor, derivation status, and frozen calendar/time control basis
needed by ``reference/validation/moba_vitality_5_15_freeze_v1.json``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any

from hdmatch.chart.ephemeris import SwissEphemerisProvider
from hdmatch.human.moba_5_15 import derive_moba_5_15
from hdmatch.provenance.swisseph_files import (
    REQUIRED_EPHEMERIS_FILES,
    verify_ephemeris_directory,
)

ROOT = Path(__file__).resolve().parents[1]
INPUT_COLUMNS = ("record_id", "birth_date", "hhmm")
OUTPUT_COLUMNS = (
    "record_id",
    "derivation_status",
    "z_5_15",
    "birth_year",
    "day_of_year_sin_1",
    "day_of_year_cos_1",
    "day_of_year_sin_2",
    "day_of_year_cos_2",
    "time_of_day_sin_1",
    "time_of_day_cos_1",
    "time_of_day_sin_2",
    "time_of_day_cos_2",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, dest="input_path")
    parser.add_argument("--output", required=True, type=Path, dest="output_path")
    parser.add_argument("--receipt", required=True, type=Path, dest="receipt_path")
    parser.add_argument(
        "--ephemeris-dir",
        required=True,
        type=Path,
        dest="ephemeris_dir",
        help="Directory containing the pinned canonical Swiss .se1 files.",
    )
    args = parser.parse_args()

    verified = verify_ephemeris_directory(
        source_manifest_path=ROOT / "data" / "ephemeris" / "manifest.json",
        ephemeris_directory=args.ephemeris_dir,
    )
    provider = SwissEphemerisProvider(
        tuple(args.ephemeris_dir / name for name in REQUIRED_EPHEMERIS_FILES)
    )
    provider.verify_production_configuration()

    input_sha256 = _sha256_file(args.input_path)
    rows = _read_input(args.input_path)
    output_rows: list[dict[str, Any]] = []
    resolved = 0
    ambiguous_resolved = 0
    unresolved_dst = 0

    with provider.capture_calculation_audit() as audit:
        for row in rows:
            record_id = row["record_id"]
            try:
                birth_date = date.fromisoformat(row["birth_date"])
            except ValueError as exc:
                raise ValueError(
                    f"invalid birth_date for record_id={record_id!r}: {row['birth_date']!r}"
                ) from exc
            result = derive_moba_5_15(
                provider,
                birth_date=birth_date,
                hhmm=row["hhmm"],
            )
            if result.status == "resolved":
                resolved += 1
            elif result.status == "ambiguous_resolved":
                ambiguous_resolved += 1
            else:
                unresolved_dst += 1
            controls = asdict(result.controls)
            output_rows.append(
                {
                    "record_id": record_id,
                    "derivation_status": result.status,
                    "z_5_15": "" if result.z_5_15 is None else int(result.z_5_15),
                    **controls,
                }
            )

    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    with args.output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(output_rows)

    output_sha256 = _sha256_file(args.output_path)
    audit_snapshot = audit.snapshot()
    receipt = {
        "schema": "moba-5-15-secure-derivation-receipt-v1",
        "phase": "VALIDATION",
        "predictor_id": "RAW_CHANNEL_5_15_FULL_ACTIVATION_SET",
        "input_sha256": input_sha256,
        "input_rows": len(rows),
        "output_sha256": output_sha256,
        "output_rows": len(output_rows),
        "status_counts": {
            "resolved": resolved,
            "ambiguous_resolved": ambiguous_resolved,
            "unresolved_dst": unresolved_dst,
        },
        "raw_birth_fields_exported": False,
        "ephemeris": verified.model_dump(mode="json"),
        "calculation_audit": asdict(audit_snapshot),
    }
    args.receipt_path.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(f"DERIVATION_OK:{len(rows)}:{output_sha256}")
    print(f"OUTPUT:{args.output_path}")
    print(f"RECEIPT:{args.receipt_path}")
    return 0


def _read_input(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("input CSV has no header")
        missing = [name for name in INPUT_COLUMNS if name not in reader.fieldnames]
        if missing:
            raise ValueError("input CSV missing required columns: " + ", ".join(missing))
        rows = []
        seen_ids: set[str] = set()
        for index, row in enumerate(reader, start=2):
            normalized = {name: (row.get(name) or "").strip() for name in INPUT_COLUMNS}
            if not all(normalized.values()):
                raise ValueError(f"blank required field at CSV line {index}")
            record_id = normalized["record_id"]
            if record_id in seen_ids:
                raise ValueError(f"duplicate record_id at CSV line {index}: {record_id!r}")
            seen_ids.add(record_id)
            rows.append(normalized)
    return rows


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
