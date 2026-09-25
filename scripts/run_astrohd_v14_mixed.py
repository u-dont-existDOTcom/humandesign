#!/usr/bin/env python3
"""Mixed-book fitting on cached nested panels; retain a passing frozen subset."""
from __future__ import annotations
import argparse, json, time
from datetime import UTC, datetime
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix, hstack, vstack
from owner_method_admission import admit
from run_astrohd_v14_staged import default_config, operation_projection, dump, sha, ranking, TASK


def fit_mixed(x, rules, seconds=40):
    difference = x[0].astype(np.int16) - x[1:].astype(np.int16)
    identical = np.all(difference == 0, axis=1)
    # Composition constraints can make a neutral column necessary; do not prune it.
    keep = np.arange(x.shape[1])
    d = difference[~identical][:, keep].astype(float)
    sources = np.array([r['source_id'] for r in rules])[keep]
    # A selected rule outside EVERY single book requires an actual mixture.
    diversity = np.array([(sources != s).astype(float) for s in sorted(set(sources))])
    constraints = np.vstack([d, diversity])
    start = time.monotonic()
    result = milp(np.ones(len(keep)), integrality=np.ones(len(keep)), bounds=Bounds(0, 1),
                  constraints=LinearConstraint(csr_matrix(constraints), 1, np.inf),
                  options={'time_limit': seconds, 'mip_rel_gap': 0.0})
    if result.x is None:
        return {'status': 'INFEASIBLE' if result.status == 2 else 'NO_INCUMBENT', 'solver_status': int(result.status), 'selection': []}
    chosen = np.rint(result.x).astype(int)
    assert np.all(constraints @ chosen >= 1)
    k = int(chosen.sum())
    augmented = vstack([hstack([csr_matrix(d), -np.ones((len(d), 1))]),
                        hstack([csr_matrix(diversity), np.zeros((len(diversity), 1))]),
                        csr_matrix(np.r_[np.ones(len(keep)), 0][None, :])])
    second = milp(np.r_[np.zeros(len(keep)), -1.0], integrality=np.ones(len(keep) + 1),
                  bounds=Bounds(np.r_[np.zeros(len(keep)), 1], np.r_[np.ones(len(keep)), 2*k]),
                  constraints=LinearConstraint(augmented, np.r_[np.zeros(len(d)), np.ones(len(diversity)), k],
                                               np.r_[np.full(len(d)+len(diversity), np.inf), k]),
                  options={'time_limit': seconds, 'mip_rel_gap': 0.0})
    if second.x is not None:
        trial = np.rint(second.x[:-1]).astype(int)
        if trial.sum() == k and np.all(constraints @ trial >= 1):
            chosen = trial
    selection = keep[np.flatnonzero(chosen)].tolist()
    assert len({rules[i]['source_id'] for i in selection}) >= 2
    return {'status': 'FITTED_MIXED_BOOKS', 'selection': selection, 'selected_count': k,
            'minimum_cardinality_certified': result.status == 0, 'margin_certified': second.status == 0,
            'minimum_margin': int(np.min(d @ chosen)), 'solver_seconds': round(time.monotonic()-start, 3),
            'full_library_identical_competitor_indices': (np.flatnonzero(identical)+1).tolist()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache-from', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    libraries = json.loads((args.cache_from/'private-rule-inventories.json').read_text())
    candidates = json.loads((args.cache_from/'candidates.json').read_text())
    matrix = np.load(args.cache_from/'feature-cache.npz')['matrix']
    old_freeze = json.loads((args.cache_from/'freeze.json').read_text())
    config = default_config([100, 1000, 10000])
    config.update(minimum_selected_sources=2, retain_passing_subset=True)
    contract = json.loads((TASK/'ASTROHD-V14-OWNER-METHOD-CONTRACT-20260924.json').read_text())
    contract['protected_dimensions']['minimum_selected_sources'] = 2
    operation = operation_projection(config)
    operation['protected_dimensions']['minimum_selected_sources'] = config['minimum_selected_sources']
    admit(contract, operation)
    dump(args.output_dir/'freeze.json', {'config': config, 'contract': contract, 'operation': operation,
         'created_utc': datetime.now(UTC).isoformat(), 'runner_sha256': sha(Path(__file__)),
         'matrix_sha256': sha(args.cache_from/'feature-cache.npz'), 'source_freeze': old_freeze,
         'exposure_note': 'Panels previously used in V14a; this is declared development replay, not independent validation.'})
    id_to_col = {r['rule_id']: i for i, r in enumerate(libraries['raw_stack'])}
    report = {'claim': 'single-owner source-grounded development, not independent validation', 'stages': [], 'parent_status': 'OPEN'}
    previous, previous_fit = {}, {}
    for n in config['stages']:
        stage = {'n': n, 'arms': {}}
        for arm in config['arms']:
            rules = libraries[arm]
            x = matrix[:n, [id_to_col[r['rule_id']] for r in rules]]
            outcome = {}
            identical = np.all(x == x[0], axis=1)
            retain = False
            if arm in previous:
                outcome['before_refit'] = ranking(x, previous[arm], candidates[:n])
                old_n = report['stages'][-1]['n']
                outcome['new_candidates_only'] = ranking(x, previous[arm], candidates[:n], start=old_n)
                outcome['before_refit_utc'] = datetime.now(UTC).isoformat()
                dump(args.output_dir/f'before-{n}-{arm}.json', outcome)
                scores = x[:, previous[arm]].sum(axis=1, dtype=np.int32)
                retain = bool(np.all(scores[0] > scores[~identical]))
            if retain:
                fit = dict(previous_fit[arm], status='RETAINED_FROZEN_SUBSET', solver_seconds=0.0,
                           minimum_margin=int(np.min(scores[0]-scores[~identical])),
                           minimum_cardinality_proof='prior certified minimum remains feasible under enlarged constraints')
            else:
                fit = fit_mixed(x, rules)
            outcome['fit'] = fit
            if fit['selection']:
                selected = fit['selection']
                assert len({rules[i]['source_id'] for i in selected}) >= config['minimum_selected_sources']
                previous[arm], previous_fit[arm] = selected, fit
                outcome['ranking'] = ranking(x, selected, candidates[:n])
                outcome['selected_rules'] = [rules[i] for i in selected]
                outcome['source_ablation'] = {s: ranking(x, [i for i in selected if rules[i]['source_id'] != s], candidates[:n]) for s in sorted({rules[i]['source_id'] for i in selected})}
            stage['arms'][arm] = outcome
            print(json.dumps({'n': n, 'arm': arm, 'fit': fit, 'ranking': outcome.get('ranking'), 'selected': [r['rule_id'] for r in outcome.get('selected_rules', [])]}), flush=True)
        report['stages'].append(stage)
        dump(args.output_dir/'result.json', report)
    dump(args.output_dir/'completed.json', {'completed_utc': datetime.now(UTC).isoformat(), 'result_sha256': sha(args.output_dir/'result.json')})

if __name__ == '__main__':
    main()
