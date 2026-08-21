#!/usr/bin/env python3
"""Generate a blinded birth-data candidate pool.

The output contains one true local date/time/IANA-zone tuple and N-1 decoys.
Only upload candidate_pool_blind.csv to the reverse-matching GPT. Keep
answer_key.json private until the ranking is frozen.

This script does not calculate Human Design charts. It only creates and seals
an auditable candidate universe.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import secrets
import sys
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones

UTC = timezone.utc


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    local_date: str
    local_time: str
    timezone: str
    utc_timestamp: str
    utc_offset: str
    fold: int


def parse_aware_utc(value: str) -> datetime:
    """Parse an ISO timestamp and return an aware UTC datetime."""
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid ISO datetime: {value}") from exc
    if dt.tzinfo is None:
        raise argparse.ArgumentTypeError("Range timestamps must include UTC offset or Z")
    return dt.astimezone(UTC)


def parse_naive_local(value: str) -> datetime:
    """Parse local civil time without an offset."""
    try:
        dt = datetime.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid local ISO datetime: {value}") from exc
    if dt.tzinfo is not None:
        raise argparse.ArgumentTypeError(
            "--true-local must not contain an offset; supply an IANA zone separately"
        )
    return dt.replace(microsecond=0)


def format_offset(delta: timedelta | None) -> str:
    if delta is None:
        raise ValueError("UTC offset unavailable")
    total = int(delta.total_seconds())
    sign = "+" if total >= 0 else "-"
    total = abs(total)
    hours, rem = divmod(total, 3600)
    minutes, seconds = divmod(rem, 60)
    if seconds:
        return f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{sign}{hours:02d}:{minutes:02d}"


def valid_local_resolutions(local_naive: datetime, zone: ZoneInfo) -> list[tuple[int, datetime]]:
    """Return valid (fold, UTC) resolutions for a local civil timestamp.

    A nonexistent spring-forward time has no valid round-trip. An ambiguous
    fall-back time has two distinct valid UTC results.
    """
    valid: list[tuple[int, datetime]] = []
    seen_utc: set[datetime] = set()
    for fold in (0, 1):
        aware = local_naive.replace(tzinfo=zone, fold=fold)
        utc_dt = aware.astimezone(UTC)
        roundtrip = utc_dt.astimezone(zone)
        if roundtrip.replace(tzinfo=None) != local_naive:
            continue
        if utc_dt not in seen_utc:
            valid.append((fold, utc_dt))
            seen_utc.add(utc_dt)
    return valid


def resolve_true_local(local_naive: datetime, zone_name: str, fold: int | None) -> tuple[int, datetime]:
    try:
        zone = ZoneInfo(zone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Unknown IANA timezone: {zone_name}") from exc

    resolutions = valid_local_resolutions(local_naive, zone)
    if not resolutions:
        raise ValueError(
            f"{local_naive.isoformat()} does not exist in {zone_name} "
            "because of a civil-time transition"
        )
    if len(resolutions) == 1:
        return resolutions[0]
    if fold is None:
        choices = ", ".join(
            f"fold={f} -> {u.isoformat().replace('+00:00', 'Z')}" for f, u in resolutions
        )
        raise ValueError(
            f"Ambiguous local time in {zone_name}; specify --true-fold 0 or 1. {choices}"
        )
    for candidate_fold, utc_dt in resolutions:
        if candidate_fold == fold:
            return candidate_fold, utc_dt
    raise ValueError(f"Requested fold {fold} is not valid for this timestamp")


def canonical_zone_names() -> list[str]:
    """Return a conservative list of ordinary IANA Area/Location names."""
    zones = []
    for name in available_timezones():
        if "/" not in name:
            continue
        if name.startswith(("Etc/", "posix/", "right/", "SystemV/")):
            continue
        zones.append(name)
    return sorted(zones)


def random_utc_second(rng: random.Random, start: datetime, end: datetime) -> datetime:
    total = int((end - start).total_seconds())
    if total <= 0:
        raise ValueError("End must be after start")
    return start + timedelta(seconds=rng.randrange(total))


def candidate_from_utc(candidate_id: str, utc_dt: datetime, zone_name: str) -> Candidate:
    zone = ZoneInfo(zone_name)
    local = utc_dt.astimezone(zone)
    return Candidate(
        candidate_id=candidate_id,
        local_date=local.date().isoformat(),
        local_time=local.time().replace(microsecond=0).isoformat(),
        timezone=zone_name,
        utc_timestamp=utc_dt.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        utc_offset=format_offset(local.utcoffset()),
        fold=int(local.fold),
    )


def candidate_id(rng: random.Random, namespace: uuid.UUID, index: int) -> str:
    token = f"{rng.getrandbits(128):032x}:{index}"
    return "C-" + uuid.uuid5(namespace, token).hex[:12].upper()


def write_csv(path: Path, candidates: Iterable[Candidate]) -> None:
    fields = [
        "candidate_id",
        "local_date",
        "local_time",
        "timezone",
        "utc_timestamp",
        "utc_offset",
        "fold",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in candidates:
            writer.writerow(asdict(row))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--true-local", required=True, type=parse_naive_local,
                        help="True local civil timestamp, e.g. 1994-01-28T14:37:00")
    parser.add_argument("--true-zone", required=True,
                        help="IANA timezone, e.g. Europe/Istanbul")
    parser.add_argument("--true-fold", type=int, choices=(0, 1), default=None,
                        help="Choose fold for an ambiguous fall-back local time")
    parser.add_argument("--count", type=int, default=1000,
                        help="Total candidates including the true tuple (default: 1000)")
    parser.add_argument("--start", type=parse_aware_utc,
                        default=parse_aware_utc("1926-08-21T00:00:00Z"))
    parser.add_argument("--end", type=parse_aware_utc,
                        default=parse_aware_utc("2026-08-21T00:00:00Z"))
    parser.add_argument("--seed", type=int, default=None,
                        help="Reproducible PRNG seed; omitted uses a cryptographic random seed")
    parser.add_argument("--output-dir", type=Path, default=Path("blind_pool"))
    parser.add_argument("--same-zone-decoys", action="store_true",
                        help="Use the true timezone for all decoys; useful for time-only rectification")
    args = parser.parse_args(argv)

    if args.count < 2:
        parser.error("--count must be at least 2")
    if args.end <= args.start:
        parser.error("--end must be after --start")

    seed = args.seed if args.seed is not None else secrets.randbits(128)
    rng = random.Random(seed)
    namespace = uuid.UUID(int=rng.getrandbits(128))

    try:
        true_fold, true_utc = resolve_true_local(args.true_local, args.true_zone, args.true_fold)
    except ValueError as exc:
        parser.error(str(exc))

    if not (args.start <= true_utc < args.end):
        parser.error("True UTC moment lies outside the declared search range")

    zones = [args.true_zone] if args.same_zone_decoys else canonical_zone_names()
    if args.true_zone not in available_timezones():
        parser.error(f"Unknown IANA timezone: {args.true_zone}")
    if not zones:
        parser.error("No IANA zones available on this system")

    candidates: list[Candidate] = []
    used_utc: set[datetime] = {true_utc.replace(microsecond=0)}

    true_id = candidate_id(rng, namespace, 0)
    true_candidate = candidate_from_utc(true_id, true_utc.replace(microsecond=0), args.true_zone)
    if true_candidate.fold != true_fold:
        # This should not occur, but preserve the user's explicit resolution.
        true_candidate = Candidate(**{**asdict(true_candidate), "fold": true_fold})
    candidates.append(true_candidate)

    index = 1
    while len(candidates) < args.count:
        utc_dt = random_utc_second(rng, args.start, args.end).replace(microsecond=0)
        if utc_dt in used_utc:
            continue
        used_utc.add(utc_dt)
        zone_name = rng.choice(zones)
        candidates.append(candidate_from_utc(candidate_id(rng, namespace, index), utc_dt, zone_name))
        index += 1

    rng.shuffle(candidates)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    blind_path = args.output_dir / "candidate_pool_blind.csv"
    key_path = args.output_dir / "answer_key.json"
    manifest_path = args.output_dir / "public_manifest.json"
    write_csv(blind_path, candidates)
    blind_hash = sha256_file(blind_path)

    public_manifest = {
        "format_version": "1.0",
        "candidate_count": args.count,
        "range_start_utc": args.start.isoformat().replace("+00:00", "Z"),
        "range_end_utc": args.end.isoformat().replace("+00:00", "Z"),
        "sampling": "uniform_utc_seconds",
        "same_zone_decoys": bool(args.same_zone_decoys),
        "candidate_pool_sha256": blind_hash,
        "instructions": "Upload only candidate_pool_blind.csv. Keep answer_key.json sealed until ranking is frozen."
    }
    manifest_path.write_text(json.dumps(public_manifest, indent=2) + "\n", encoding="utf-8")

    answer_key = {
        **public_manifest,
        "seed": str(seed),
        "true_candidate_id": true_id,
        "true_tuple": asdict(true_candidate),
        "answer_key_commitment_sha256": ""
    }
    # Commit to the answer-key contents without the commitment field itself.
    canonical = json.dumps(answer_key, sort_keys=True, separators=(",", ":")).encode("utf-8")
    answer_key["answer_key_commitment_sha256"] = hashlib.sha256(canonical).hexdigest()
    key_path.write_text(json.dumps(answer_key, indent=2) + "\n", encoding="utf-8")

    print(f"Created {blind_path}")
    print(f"Created {manifest_path}")
    print(f"Created sealed {key_path}")
    print(f"Candidate pool SHA-256: {blind_hash}")
    print("Do not upload answer_key.json until the ranking is locked.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        raise SystemExit(130)
