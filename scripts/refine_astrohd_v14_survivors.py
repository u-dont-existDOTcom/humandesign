#!/usr/bin/env python3
"""Add the fewest existing positive rules to eliminate known century false matches.

The four retained clauses already attain their maximum at the target. A new
positive clause cannot promote an excluded candidate to the enlarged maximum.
Minimum-addition optimality is conditional on retaining those four clauses.
"""
from __future__ import annotations
import argparse, fcntl, json
from datetime import UTC, datetime
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix
from owner_method_admission import admit
from run_astrohd_v14_staged import TASK, default_config, operation_projection, dump, sha, ranking
from hdmatch.evaluation.astrohd_v13_traditions import build_snapshot
from hdmatch.evaluation.astrohd_v14_rules import feature_row


def minimum_additions(x, rules, base_ids):
    base = [i for i, r in enumerate(rules) if r['rule_id'] in base_ids]
    if len(base) != len(base_ids) or not np.all(x[0, base] == 1):
        raise ValueError('Retained base is not a maximum-scoring subset')
    eligible = np.array([i for i, r in enumerate(rules) if r['rule_id'] not in base_ids and x[0, i] == 1], dtype=int)
    gaps = 1 - x[1:, eligible].astype(np.int16)
    unresolved = np.flatnonzero(np.all(gaps == 0, axis=1)) + 1
    distinguishable = np.any(gaps > 0, axis=1)
    if not np.any(distinguishable):
        return base, {'status': 'NO_DISTINGUISHABLE_SURVIVORS', 'unresolved_indices': unresolved.tolist()}
    result = milp(np.ones(len(eligible)), integrality=np.ones(len(eligible)),
                  bounds=Bounds(0, 1), constraints=LinearConstraint(csr_matrix(gaps[distinguishable]), 1, np.inf),
                  options={'time_limit': 40, 'mip_rel_gap': 0.0})
    if result.x is None:
        raise RuntimeError(f'No feasible addition within budget: {result.message}')
    chosen = np.rint(result.x).astype(int)
    if not np.all(gaps[distinguishable] @ chosen >= 1):
        raise RuntimeError('Solver output failed direct constraint check')
    selection = base + eligible[np.flatnonzero(chosen)].tolist()
    return selection, {'status': 'FITTED_POSITIVE_ADDITIONS', 'added_count': int(chosen.sum()),
                       'minimum_additions_certified': result.status == 0,
                       'solver_message': result.message, 'eligible_additions': len(eligible),
                       'unresolved_indices': unresolved.tolist()}


def main():
    parser = argparse.ArgumentParser()
    for arg in ('source-run', 'base-model', 'survivors', 'ephemeris-root', 'output-dir'):
        parser.add_argument('--' + arg, type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    lock = (args.output_dir/'runner.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if (args.output_dir/'freeze.json').exists():
        raise ValueError('Refusing to overwrite a frozen experiment')
    config = default_config([100, 1000, 10000, 100000])
    config['refinement'] = 'minimal positive additions to retained maximum-score base'
    owner = json.loads((TASK/'ASTROHD-V14-OWNER-METHOD-CONTRACT-20260924.json').read_text())
    operation = operation_projection(config)
    admit(owner, operation)
    base = json.loads(args.base_model.read_text())['selected_rules']
    base_ids = {r['rule_id'] for r in base}
    if len({r['source_id'] for r in base}) < 2:
        raise ValueError('Retained model must actually combine multiple books')
    libraries = json.loads((args.source_run/'private-rule-inventories.json').read_text())
    direct = json.loads((TASK/'ASTROHD-V13-SCORING-FREEZE-20260924.json').read_text())
    target = datetime.fromisoformat(direct['direct_queries']['target'].replace('Z', '+00:00')).isoformat()
    hits = json.loads(args.survivors.read_text())['hits']
    rows = [{'utc': target, 'group': 'target'}]
    rows += [{'utc': h['utc'], 'group': 'century_false_match'} for h in hits if h['utc'] != target]
    provenance = {'created_utc': datetime.now(UTC).isoformat(), 'config': config, 'operation': operation,
                  'base_sha256': sha(args.base_model), 'survivors_sha256': sha(args.survivors),
                  'inventory_sha256': sha(args.source_run/'private-rule-inventories.json'),
                  'runner_sha256': sha(Path(__file__)), 'source_module_sha256': sha(Path(__file__).resolve().parents[1]/'src/hdmatch/evaluation/astrohd_v14_rules.py'),
                  'claim': 'post-result owner training; numerical-screen completeness not formally proved',
                  'parent_status': 'OPEN'}
    dump(args.output_dir/'freeze.json', provenance)
    dump(args.output_dir/'candidates.json', rows)
    raw = libraries['raw_stack']
    location = direct['astronomy']['location']
    x = np.vstack([feature_row(build_snapshot(datetime.fromisoformat(r['utc']),
        latitude=location['latitude'], longitude=location['longitude'], ephemeris_root=args.ephemeris_root), raw) for r in rows])
    np.savez_compressed(args.output_dir/'feature-cache.npz', matrix=x)
    raw_columns = {r['rule_id']: i for i, r in enumerate(raw)}
    report = {'classification': provenance['claim'], 'candidate_count': len(rows), 'arms': {}, 'parent_status': 'OPEN'}
    for arm in config['arms']:
        rules = libraries[arm]
        matrix = x[:, [raw_columns[r['rule_id']] for r in rules]]
        base_columns = [i for i, r in enumerate(rules) if r['rule_id'] in base_ids]
        before = ranking(matrix, base_columns, rows)
        dump(args.output_dir/f'before-refit-{arm}.json', {'evaluated_utc': datetime.now(UTC).isoformat(), 'ranking': before})
        selection, fit = minimum_additions(matrix, rules, base_ids)
        score = matrix[:, selection].sum(axis=1, dtype=np.int32)
        if int(score[0]) != len(selection):
            raise RuntimeError('Target no longer attains theoretical score maximum')
        tied = np.flatnonzero(score == score[0])
        outcome = {'fit': fit, 'ranking': ranking(matrix, selection, rows),
                   'selected_rules': [rules[i] for i in selection],
                   'tied_instants': [rows[i]['utc'] for i in tied],
                   'tied_utc_dates': sorted({rows[i]['utc'][:10] for i in tied}),
                   'source_ablation': {s: ranking(matrix, [i for i in selection if rules[i]['source_id'] != s], rows)
                                      for s in sorted({rules[i]['source_id'] for i in selection})},
                   'completion_utc': datetime.now(UTC).isoformat(),
                   'coverage_limit': 'All retained-base maxima found by prior numerical screen; no claim of formally complete minute universe.'}
        report['arms'][arm] = outcome
        dump(args.output_dir/'result.json', report)
        print(json.dumps({'arm': arm, 'fit': fit, 'rank': outcome['ranking'],
                          'rules': [r['rule_id'] for r in outcome['selected_rules']],
                          'tied_dates': outcome['tied_utc_dates'], 'tied_instants': outcome['tied_instants']}), flush=True)
    dump(args.output_dir/'completed.json', {'completed_utc': datetime.now(UTC).isoformat(), 'result_sha256': sha(args.output_dir/'result.json')})


if __name__ == '__main__':
    main()
