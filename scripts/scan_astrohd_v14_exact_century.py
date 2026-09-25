#!/usr/bin/env python3
"""Audit every minute of the declared century without interpolated screening.

The target already reaches the Boolean model's maximum of six. Finding every
six-point instant therefore establishes its complete tied rank on this grid.
Early rejection evaluates an actual necessary rule, not a numerical surrogate.
This is a fixed-model audit, never rule selection or a new-person validation.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import UTC, datetime, timedelta
import fcntl
import hashlib
import json
from pathlib import Path
import random
import time

import swisseph as swe

from hdmatch.evaluation.astrohd_v13_traditions import (
    BODY_IDS, RULERS, SIGNS, build_snapshot, datetime_to_jd,
)
from hdmatch.evaluation.astrohd_v14_rules import feature_row, registry
from hdmatch.relationship.western import house_for_longitude

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / 'tasks/scenario-owner-recovery-calibration-20260923'
EXPECTED = {
    'lilly/lord:3/house_1_10', 'lilly/planet:saturn/benefic_trine',
    'lilly/planet:venus/house_2_5', 'phaladeepika/planet:venus/directional',
    'lilly/lord:10/benefic_conjunction', 'lilly/lord:7/house_4_7_11',
}
FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED
SID_FLAGS = FLAGS | swe.FLG_SIDEREAL
SIGN_RULERS = tuple(BODY_IDS[RULERS[s]] for s in SIGNS)
LATITUDE, LONGITUDE = 39.9526, -75.1652


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, data: object) -> None:
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
    temporary.replace(path)


def initialize(ephemeris: str) -> None:
    swe.set_ephe_path(ephemeris)
    swe.set_sid_mode(swe.SIDM_LAHIRI)


def longitude(jd: float, body: int, flags: int = FLAGS) -> float:
    values, returned = swe.calc_ut(jd, body, flags)
    if not returned & swe.FLG_SWIEPH or returned & swe.FLG_MOSEPH:
        raise RuntimeError(f'Ephemeris fallback: jd={jd}, body={body}, flags={returned}')
    return float(values[0]) % 360.0


def separation(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def first_failure(jd: float) -> int:
    """Return first failed necessary clause, or 6 if all six are satisfied.

    The order is directional, Venus house, Saturn trine, lord-3 house,
    lord-10 conjunction, lord-7 house. Longitude/house semantics match V1.4d.
    """
    venus_sidereal = longitude(jd, swe.VENUS, SID_FLAGS)
    _, asc = swe.houses_ex(jd, LATITUDE, LONGITUDE, b'P', swe.FLG_SIDEREAL)
    if (int(venus_sidereal // 30) - int((asc[0] % 360) // 30)) % 12 != 3:
        return 0
    raw_cusps, _ = swe.houses_ex(jd, LATITUDE, LONGITUDE, b'R', 0)
    cusps = tuple(float(x) % 360.0 for x in raw_cusps[:12])
    venus = longitude(jd, swe.VENUS)
    if house_for_longitude(venus, cusps) not in {2, 5}:
        return 1
    cache = {swe.VENUS: venus}

    def planet(body: int) -> float:
        if body not in cache:
            cache[body] = longitude(jd, body)
        return cache[body]

    saturn, jupiter = planet(swe.SATURN), planet(swe.JUPITER)
    if not any(abs(separation(saturn, other) - 120.0) <= 1.0
               for other in (jupiter, venus)):
        return 2
    lord3 = SIGN_RULERS[int(cusps[2] // 30)]
    if house_for_longitude(planet(lord3), cusps) not in {1, 10}:
        return 3
    lord10 = SIGN_RULERS[int(cusps[9] // 30)]
    if not any(other != lord10 and separation(planet(lord10), planet(other)) <= 1.0
               for other in (swe.JUPITER, swe.VENUS)):
        return 4
    lord7 = SIGN_RULERS[int(cusps[6] // 30)]
    if house_for_longitude(planet(lord7), cusps) not in {4, 7, 11}:
        return 5
    return 6


def run_chunk(start_jd: float, first: int, stop: int) -> dict:
    begin = time.perf_counter()
    counts = [0] * 7
    hits = []
    for index in range(first, stop):
        stage = first_failure(start_jd + index / 1440.0)
        counts[stage] += 1
        if stage == 6:
            hits.append(index)
    return {'first': first, 'stop': stop, 'count': stop - first,
            'first_failure_counts_then_matches': counts, 'hit_indices': hits,
            'elapsed_seconds': round(time.perf_counter() - begin, 6)}


def parity_audit(start: datetime, count: int, model: dict, ephemeris: Path) -> dict:
    source = json.loads((ROOT / model['source_map_path']).read_text())
    generic = registry(source, {row['domain_id'] for row in source['domains']})
    lookup = {row['rule_id']: row for row in generic}
    rules = [lookup[key] for key in model['selected_rule_ids']]
    rng = random.Random(14002509)
    target = datetime.fromisoformat(model['target_utc'].replace('Z', '+00:00'))
    timestamps = [start + timedelta(minutes=rng.randrange(count)) for _ in range(1024)]
    timestamps += [target + timedelta(minutes=i) for i in range(-90, 91)]
    # Explicitly check the previous continuous transition brackets.
    timestamps += [target.replace(minute=17, second=51, microsecond=u)
                   for u in (700000, 800000, 900000)]
    timestamps += [target.replace(minute=26, second=12, microsecond=u)
                   for u in (0, 100000, 200000)]
    positives = 0
    for when in timestamps:
        full = build_snapshot(when, latitude=LATITUDE, longitude=LONGITUDE,
                              ephemeris_root=ephemeris)
        expected = int(feature_row(full, rules).sum()) == 6
        actual = first_failure(datetime_to_jd(when)) == 6
        if expected != actual:
            raise RuntimeError(f'Exact fast-path parity failed at {when.isoformat()}')
        positives += int(actual)
    return {'compared': len(timestamps), 'maximum_score_cases': positives,
            'disagreements': 0, 'method': 'original full snapshot and six-rule evaluator'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ephemeris-root', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--start', default='1926-08-24T10:42:00Z')
    parser.add_argument('--end', default='2026-08-24T10:42:00Z')
    parser.add_argument('--workers', type=int, default=6)
    parser.add_argument('--chunk-size', type=int, default=250000)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    start = datetime.fromisoformat(args.start.replace('Z', '+00:00'))
    end = datetime.fromisoformat(args.end.replace('Z', '+00:00'))
    if start.tzinfo is None or end.tzinfo is None or end < start:
        raise ValueError('A valid timezone-aware ordered interval is required')
    seconds = (end - start).total_seconds()
    if seconds % 60 or start.second or start.microsecond:
        raise ValueError('This audit uses an exact UTC minute grid')
    count = int(seconds // 60) + 1
    if args.workers < 1 or args.chunk_size < 1:
        raise ValueError('Workers and chunk size must be positive')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    lock = (args.output_dir / 'writer.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    model_path = TASK / 'ASTROHD-V14-SIX-RULE-MODEL-20260925.json'
    model = json.loads(model_path.read_text())
    if set(model['selected_rule_ids']) != EXPECTED or len(model['selected_rule_ids']) != 6:
        raise ValueError('This exact evaluator is specialized to the unchanged six rules')
    if model['weight_per_selected_rule'] != 1 or model['maximum_score'] != 6:
        raise ValueError('Model weight/maximum mismatch')
    for path_key, hash_key in [('rule_module', 'rule_module_sha256'),
                               ('source_map_path', 'source_map_sha256')]:
        if sha(ROOT / model[path_key]) != model[hash_key]:
            raise ValueError('Frozen source hash mismatch')
    cache = json.loads((ROOT / 'data/ephemeris/astrohd_generic_v2_swieph/manifest.json').read_text())
    ephemeris_hashes = {name: sha(args.ephemeris_root / name)
                        for name in cache['ephemeris_files']}
    if any(ephemeris_hashes[name] != row['sha256']
           for name, row in cache['ephemeris_files'].items()):
        raise ValueError('Ephemeris files differ from original production files')
    freeze = {'schema': 'v14d-exact-minute-grid-audit-v1', 'start': start.isoformat(),
              'end': end.isoformat(), 'count': count, 'cadence_seconds': 60,
              'model_sha256': sha(model_path), 'runner_sha256': sha(Path(__file__)),
              'ephemeris_sha256': ephemeris_hashes, 'engine_version': swe.version,
              'chunk_size': args.chunk_size, 'numerical_screening': False,
              'rule_refitting': False, 'max_score': 6,
              'proof': 'Every UTC minute evaluated; first false necessary Boolean clause safely excludes score six.'}
    freeze_path = args.output_dir / 'freeze.json'
    if freeze_path.exists():
        if not args.resume or json.loads(freeze_path.read_text()) != freeze:
            raise ValueError('Existing freeze requires an exact-matching explicit resume')
    else:
        write_json(freeze_path, freeze)
    initialize(str(args.ephemeris_root))
    audit = parity_audit(start, count, model, args.ephemeris_root)
    write_json(args.output_dir / 'parity.json', audit)
    chunks = [(first, min(count, first + args.chunk_size))
              for first in range(0, count, args.chunk_size)]
    complete = {}
    for first, stop in chunks:
        path = args.output_dir / f'chunk-{first:09d}.json'
        if path.exists():
            row = json.loads(path.read_text())
            if (row['first'], row['stop'], row['count']) != (first, stop, stop - first):
                raise ValueError('Stored chunk coverage mismatch')
            complete[first] = row
    begin = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers, initializer=initialize,
                             initargs=(str(args.ephemeris_root),)) as pool:
        pending = {pool.submit(run_chunk, datetime_to_jd(start), first, stop): first
                   for first, stop in chunks if first not in complete}
        for future in as_completed(pending):
            row = future.result()
            write_json(args.output_dir / f"chunk-{row['first']:09d}.json", row)
            complete[row['first']] = row
            progress = {'completed_minutes': sum(r['count'] for r in complete.values()),
                        'total_minutes': count, 'chunks': len(complete),
                        'matches': sum(len(r['hit_indices']) for r in complete.values()),
                        'observed_utc': datetime.now(UTC).isoformat()}
            write_json(args.output_dir / 'progress.json', progress)
            if len(complete) % 10 == 0 or len(complete) == len(chunks):
                print(json.dumps(progress), flush=True)
    if len(complete) != len(chunks) or sum(r['count'] for r in complete.values()) != count:
        raise RuntimeError('Incomplete century coverage')
    hits = sorted(index for row in complete.values() for index in row['hit_indices'])
    if len(hits) != len(set(hits)):
        raise RuntimeError('Duplicate grid hits')
    stamps = [(start + timedelta(minutes=i)).isoformat() for i in hits]
    result = {'status': 'COMPLETED_EXACT_MINUTE_GRID', 'freeze': freeze, 'parity': audit,
              'evaluated_minutes': count, 'maximum_score': 6,
              'matching_minutes': len(hits), 'hit_indices': hits, 'hit_utc': stamps,
              'dates_utc': sorted({stamp[:10] for stamp in stamps}),
              'first_failure_counts_then_matches': [sum(row['first_failure_counts_then_matches'][i]
                                                        for row in complete.values()) for i in range(7)],
              'elapsed_this_invocation_seconds': round(time.perf_counter() - begin, 3),
              'completed_utc': datetime.now(UTC).isoformat(),
              'limits': 'Exact over the specified minute grid using the frozen numerical engine; not continuous-time or new-person validation.'}
    target = datetime.fromisoformat(model['target_utc'].replace('Z', '+00:00'))
    target_index = (target - start).total_seconds() / 60
    if target_index.is_integer() and int(target_index) in hits:
        result['recorded_target_rank'] = {'best': 1, 'worst': len(hits), 'higher_candidates': 0}
    write_json(args.output_dir / 'result.json', result)
    print(json.dumps({k: v for k, v in result.items() if k not in {'hit_indices', 'freeze'}}), flush=True)


if __name__ == '__main__':
    main()
