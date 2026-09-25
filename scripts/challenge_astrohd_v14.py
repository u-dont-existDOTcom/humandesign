#!/usr/bin/env python3
"""Evaluate frozen mixed-book subsets on a larger nested instant panel."""
from __future__ import annotations
import argparse, json, time
from datetime import UTC, datetime
from pathlib import Path
import numpy as np
from hdmatch.evaluation.astrohd_v13_traditions import build_snapshot
from hdmatch.evaluation.astrohd_v14_rules import feature_row
from owner_method_admission import admit
from run_astrohd_v14_staged import candidates, default_config, operation_projection, dump, sha, ranking, TASK


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache-from', type=Path, required=True)
    parser.add_argument('--model-result', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--ephemeris-root', type=Path, required=True)
    parser.add_argument('--count', type=int, default=100000)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if (args.output_dir/'freeze.json').exists():
        raise ValueError('Use a new output directory; do not overwrite a frozen run')
    config = default_config([args.count])
    owner = json.loads((TASK/'ASTROHD-V14-OWNER-METHOD-CONTRACT-20260924.json').read_text())
    admit(owner, operation_projection(config))
    prior = json.loads(args.model_result.read_text())['stages'][-1]
    old_candidates = json.loads((args.cache_from/'candidates.json').read_text())
    source_freeze = json.loads((TASK/'ASTROHD-V13-SCORING-FREEZE-20260924.json').read_text())
    rows = candidates(source_freeze, args.count, config['seed'])
    assert rows[:len(old_candidates)] == old_candidates
    union = {r['rule_id']: r for a in prior['arms'].values() for r in a['selected_rules']}
    rules = [union[k] for k in sorted(union)]
    rule_index = {r['rule_id']: i for i, r in enumerate(rules)}
    subsets = {a: [rule_index[r['rule_id']] for r in v['selected_rules']] for a, v in prior['arms'].items()}
    assert all(len({rules[i]['source_id'] for i in subset}) >= 2 for subset in subsets.values())
    dump(args.output_dir/'freeze.json', {'utc': datetime.now(UTC).isoformat(), 'config': config,
         'model_sha256': sha(args.model_result), 'runner_sha256': sha(Path(__file__)),
         'source_module_sha256': sha(TASK.parents[1]/'src/hdmatch/evaluation/astrohd_v14_rules.py'),
         'rules': rules, 'subsets': subsets, 'refitting': False})
    dump(args.output_dir/'candidates.json', rows)
    old_rules = json.loads((args.cache_from/'private-rule-inventories.json').read_text())['raw_stack']
    old_index = {r['rule_id']: i for i, r in enumerate(old_rules)}
    cached = np.load(args.cache_from/'feature-cache.npz')['matrix']
    x = np.empty((len(rows), len(rules)), dtype=np.int8)
    old_n = len(cached)
    x[:old_n] = cached[:, [old_index[r['rule_id']] for r in rules]]
    start = time.monotonic()
    for i in range(old_n, len(rows)):
        snapshot = build_snapshot(datetime.fromisoformat(rows[i]['utc']), latitude=39.9526,
                                  longitude=-75.1652, ephemeris_root=args.ephemeris_root)
        x[i] = feature_row(snapshot, rules)
        if (i + 1) % 10000 == 0:
            print('Evaluated', i+1, 'of', len(rows), flush=True)
    report = {'count': len(rows), 'classification': 'owner development challenge, not independent validation',
              'refitting': False, 'parent_status': 'OPEN', 'seconds': round(time.monotonic()-start, 3), 'arms': {}}
    for arm, subset in subsets.items():
        scores = x[:, subset].sum(axis=1, dtype=np.int32)
        report['arms'][arm] = {'full_panel': ranking(x, subset, rows),
             'new_candidates_only': ranking(x, subset, rows, start=old_n),
             'all_tied_or_higher_indices': np.flatnonzero(scores >= scores[0]).tolist()}
    np.savez_compressed(args.output_dir/'selected-feature-matrix.npz', matrix=x)
    dump(args.output_dir/'result.json', report)
    print(json.dumps(report), flush=True)

if __name__ == '__main__':
    main()
