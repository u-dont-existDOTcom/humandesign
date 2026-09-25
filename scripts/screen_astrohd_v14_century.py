#!/usr/bin/env python3
"""Conservative numerical screening, followed by exact scoring of survivors.

Specialized to the four frozen V14c clauses. It is NOT a proof that interpolation
has a formal global error bound. The declared one-degree guards are numerical
screening allowances, never astrological or fitted weights. Exact survivors and
cache-audit errors are reported separately from the screened grid count.
"""
from __future__ import annotations
import argparse, hashlib, json, lzma, struct, time
from datetime import UTC, datetime, timedelta
from pathlib import Path
import numpy as np
import swisseph as swe
from hdmatch.evaluation.astrohd_v13_traditions import build_snapshot, PLANETS, SIGNS, RULERS
from hdmatch.evaluation.astrohd_v14_rules import feature_row
from run_astrohd_v14_staged import dump, sha, TASK, default_config, operation_projection
from owner_method_admission import admit

EXPECTED = {'lilly/lord:3/house_1_10', 'lilly/planet:saturn/benefic_trine',
            'lilly/planet:venus/house_2_5', 'phaladeepika/planet:venus/directional'}
GUARD = 1.0


def decode(path, expected_hash):
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == expected_hash
    raw = lzma.decompress(data)
    q0, d1, n, step = struct.unpack('<qiId', raw[:24])
    dd = np.frombuffer(raw[24:], dtype='<i4').astype(np.int64)
    delta = np.r_[d1, d1 + np.cumsum(dd)]
    values = np.r_[q0, q0 + np.cumsum(delta)] / 1e5
    assert len(values) == n
    return values, step


def interpolate(decoded, start_jd, jd):
    values, step = decoded
    x = (jd - start_jd) * 24 / step
    assert np.min(x) >= -1e-5 and np.max(x) <= len(values)-1+1e-5
    i = np.clip(np.floor(x).astype(int), 0, len(values)-2)
    f = x - i  # After clipping: the last endpoint must have f=1, not f=0.
    return (values[i] + f * (values[i+1]-values[i])) % 360


def separation(a, b):
    return np.abs((a-b+180) % 360-180)


def house_possible(lon, cusps, h):
    first, last = cusps[:, h-1], cusps[:, h % 12]
    return (lon-first+GUARD) % 360 <= (last-first) % 360 + 2*GUARD


def screen(jd, decoded, start_jd, rulers):
    sat, jup, ven = [interpolate(decoded[p], start_jd, jd) for p in ('saturn', 'jupiter', 'venus')]
    possible = (np.abs(separation(sat, jup)-120) <= 1+2*GUARD) | (np.abs(separation(sat, ven)-120) <= 1+2*GUARD)
    indices = np.flatnonzero(possible)
    small_jd, ven = jd[indices], ven[indices]
    if not len(indices):
        return indices, 0
    cusps = np.array([swe.houses_ex(float(t), 39.9526, -75.1652, b'R', 0)[0] for t in small_jd])
    keep = house_possible(ven, cusps, 2) | house_possible(ven, cusps, 5)
    indices, small_jd, ven, cusps = indices[keep], small_jd[keep], ven[keep], cusps[keep]
    if not len(indices):
        return indices, int(possible.sum())
    ayan = np.array([swe.get_ayanamsa_ut(float(t)) for t in small_jd])
    asc = cusps[:, 0]
    keep = np.zeros(len(indices), dtype=bool)
    for da in (-GUARD, 0, GUARD):
        for dv in (-GUARD, 0, GUARD):
            a = np.floor(((asc-ayan+da) % 360)/30).astype(int)
            v = np.floor(((ven-ayan+dv) % 360)/30).astype(int)
            keep |= (v-a) % 12 == 3
    indices, small_jd, cusps = indices[keep], small_jd[keep], cusps[keep]
    if not len(indices):
        return indices, int(possible.sum())
    longitudes = np.column_stack([interpolate(decoded[p], start_jd, small_jd) for p in PLANETS])
    keep = np.zeros(len(indices), dtype=bool)
    for offset in (-GUARD, 0, GUARD):
        signs = np.floor(((cusps[:, 2]+offset) % 360)/30).astype(int)
        lord_lon = longitudes[np.arange(len(indices)), rulers[signs]]
        keep |= house_possible(lord_lon, cusps, 1) | house_possible(lord_lon, cusps, 10)
    return indices[keep], int(possible.sum())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache-dir', type=Path, required=True)
    parser.add_argument('--model-result', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--ephemeris-root', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if (args.output_dir/'freeze.json').exists():
        raise ValueError('Refusing to overwrite a frozen run')
    contract = json.loads((TASK / "ASTROHD-V14-OWNER-METHOD-CONTRACT-20260924.json").read_text())
    admit(contract, operation_projection(default_config([52596001])))
    model = json.loads(args.model_result.read_text())
    rules = model['selected_rules']
    assert {r['rule_id'] for r in rules} == EXPECTED
    manifest = json.loads((args.cache_dir/'manifest.json').read_text())
    for name, entry in manifest['ephemeris_files'].items():
        assert sha(args.ephemeris_root/name) == entry['sha256']
    decoded = {p: decode(args.cache_dir/(p+'.d2xz'), manifest['bodies'][p]['sha256']) for p in PLANETS}
    start = datetime(1926, 8, 24, 10, 42, tzinfo=UTC)
    end = datetime(2026, 8, 24, 10, 42, tzinfo=UTC)
    count = int((end-start).total_seconds()/60)+1
    start_jd = swe.julday(start.year, start.month, start.day, start.hour+start.minute/60)
    rulers = np.array([PLANETS.index(RULERS[s]) for s in SIGNS])
    swe.set_ephe_path(str(args.ephemeris_root))
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    dump(args.output_dir/'freeze.json', {'utc': datetime.now(UTC).isoformat(), 'runner_sha256': sha(Path(__file__)),
         'model_sha256': sha(args.model_result), 'cadence_minutes': 1, 'count': count, 'start': start.isoformat(), 'end': end.isoformat(),
         'numerical_coordinate_guard_degrees': GUARD, 'limitations': 'Screening guard is conservative but not a formally proved global interpolation error bound; survivors are recomputed exactly.'})
    # Check numerical behavior on a target-independent, seeded audit sample.
    rng = np.random.default_rng(140025)
    audit_minutes = rng.integers(0, count, size=512)
    audit_jd = start_jd + audit_minutes/1440
    approximations = {p: interpolate(decoded[p], manifest['start_jd'], audit_jd) for p in PLANETS}
    max_error = {p: 0.0 for p in PLANETS}
    for i, minute in enumerate(audit_minutes):
        snapshot = build_snapshot(start+timedelta(minutes=int(minute)), latitude=39.9526,
                                  longitude=-75.1652, ephemeris_root=args.ephemeris_root)
        for p in PLANETS:
            max_error[p] = max(max_error[p], float(separation(approximations[p][i], snapshot.tropical_longitudes[p])))
    assert max(max_error.values()) < GUARD
    dump(args.output_dir/'numerical-audit.json', {'sample_count': 512, 'max_observed_longitude_error_degrees': max_error,
                                               'global_error_bound_proved': False})
    report = {'classification': 'single-owner development; screened century grid with exact survivor scoring',
              'grid_count': count, 'screened': 0, 'exact_survivors': 0, 'maximum_score': len(rules), 'hits': [],
              'parent_status': 'OPEN', 'numerical_audit': max_error}
    begin = time.monotonic()
    for first in range(0, count, 365*1440):
        stop = min(count, first+365*1440)
        jd = start_jd+np.arange(first, stop)/1440
        survivors, broad = screen(jd, decoded, manifest['start_jd'], rulers)
        for relative in survivors:
            minute = first+int(relative)
            when = start+timedelta(minutes=minute)
            snapshot = build_snapshot(when, latitude=39.9526, longitude=-75.1652, ephemeris_root=args.ephemeris_root)
            if int(feature_row(snapshot, rules).sum()) == len(rules):
                report['hits'].append({'minute_index': minute, 'utc': when.isoformat()})
        report['screened'] = stop
        report['exact_survivors'] += len(survivors)
        report['seconds'] = round(time.monotonic()-begin, 3)
        dump(args.output_dir/'result.json', report)
        if first % (10*365*1440) == 0 or stop == count:
            print('Screened', stop, 'of', count, 'matching minutes', len(report['hits']), flush=True)
    report['distinct_utc_dates'] = sorted({row['utc'][:10] for row in report['hits']})
    dump(args.output_dir/'result.json', report)
    print('Completed century screen', report['distinct_utc_dates'], flush=True)

if __name__ == '__main__':
    main()
