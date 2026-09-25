#!/usr/bin/env python3
"""Run nested pooled-rule development fits; prior-subset evaluation precedes refit."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import UTC, datetime, timedelta
import fcntl
import hashlib
import json
from pathlib import Path
import random
import time
from typing import Any
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix, hstack, vstack
from owner_method_admission import admit
from hdmatch.evaluation.astrohd_v13_traditions import behavior_weight_variants, build_snapshot
from hdmatch.evaluation.astrohd_v14_rules import registry, deduplicate, feature_row

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / 'tasks/scenario-owner-recovery-calibration-20260923'
CONTRACT_ID = 'astrohd-owner-cross-rulebook-v14-20260924'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, data: Any) -> None:
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
    tmp.replace(path)


def operation_projection(config: dict[str, Any]) -> dict[str, Any]:
    return {
        'owner_outcome_id': CONTRACT_ID,
        'protected_dimensions': {key: config[key] for key in ('composition', 'weight_policy', 'fitting_permission', 'stage_order')},
        'operations': list(config['arms']) + ['nested_challenges'],
        'prohibited_operations': config.get('prohibited_operations', []),
        'added_requirements': config.get('added_requirements', []),
        'parent_outcome_status': 'OPEN',
    }


def default_config(stages: list[int]) -> dict[str, Any]:
    return {'composition': 'pooled_cross_rulebook', 'weight_policy': 'equal_signed_binary_inclusion',
            'fitting_permission': 'owner_development_refit_allowed',
            'stage_order': 'evaluate_previous_frozen_subset_before_refit',
            'arms': ['raw_stack', 'lineage_dedup'], 'stages': stages,
            'seed': 2026092414, 'solver_time_limit_seconds': 40,
            'candidate_rule': 'nested unique instants: forced hard negatives, local time/date neighbors, then uniform minute sample over prior century universe',
            'precision_rule': 'full-library identical rows remain reported as unresolved; only distinguishable candidates are strict constraints; no tie broken by known time proximity',
            'optimization': 'minimize equal-vote rule count for strict target margin>=1; then maximize minimum integer margin at that cardinality; sorted input order; no fitted astrology coefficients',
            'source_coverage': 'bounded atomic strength library; not complete natal rulebooks',
            'claim': 'target-aware single-owner development, never independent human validation'}


def candidates(freeze: dict[str, Any], count: int, seed: int) -> list[dict[str, str]]:
    parse = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
    target = parse(freeze['direct_queries']['target'])
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    def add(value: datetime, group: str) -> None:
        key = value.isoformat()
        if key not in seen:
            rows.append({'utc': key, 'group': group})
            seen.add(key)
    add(target, 'target')
    add(parse(freeze['direct_queries']['persistent_competitor']), 'persistent_2013')
    for value in freeze['direct_queries']['same_date_alternative_midpoints']:
        add(parse(value), 'prior_same_date_hard_negative')
    for hour in range(24):
        add(target.replace(hour=hour), 'same_date_hourly')
    for minutes in (-120, -60, -30, -15, -5, -1, 1, 5, 15, 30, 60, 120):
        add(target + timedelta(minutes=minutes), 'fine_time_neighbor')
    for days in (-365, -30, -7, -1, 1, 7, 30, 365):
        add(target + timedelta(days=days), 'near_date')
    start = datetime(1926, 8, 24, 10, 42, tzinfo=UTC)
    end = datetime(2026, 8, 24, 10, 42, tzinfo=UTC)
    minutes = int((end - start).total_seconds() // 60)
    rng = random.Random(seed)
    while len(rows) < count:
        add(start + timedelta(minutes=rng.randrange(minutes + 1)), 'century_random')
    return rows[:count]


def ranking(matrix: np.ndarray, selection: list[int], rows: list[dict[str, str]], start: int = 1) -> dict[str, Any]:
    scores = matrix[:, selection].sum(axis=1, dtype=np.int32) if selection else np.zeros(len(matrix), dtype=np.int32)
    target = int(scores[0])
    higher = int(np.count_nonzero(scores[start:] > target))
    tied = int(np.count_nonzero(scores[start:] == target))
    competitors = list(range(start, len(scores)))
    best = sorted(competitors, key=lambda i: (-int(scores[i]), i))[:8]
    return {'target_score': target, 'rank_best': 1 + higher, 'rank_worst': 1 + higher + tied,
            'rank_mid': 1 + higher + tied / 2, 'higher_competitors': higher, 'tied_competitors': tied,
            'target_unique_top': higher == 0 and tied == 0,
            'target_top_tied': higher == 0 and tied > 0,
            'competitor_count': len(competitors),
            'strongest_competitors': [{'index': i, **rows[i], 'score': int(scores[i])} for i in best]}


def sparse_fit(matrix: np.ndarray, config: dict[str, Any]) -> dict[str, Any]:
    difference = matrix[0].astype(np.int16) - matrix[1:].astype(np.int16)
    identical = np.flatnonzero(np.all(difference == 0, axis=1)) + 1
    active_rows = np.flatnonzero(np.any(difference != 0, axis=1))
    # A never-positive column cannot improve any target-vs-competitor constraint.
    keep = np.flatnonzero(np.any(difference > 0, axis=0))
    d = difference[active_rows][:, keep].astype(float)
    dominates = np.flatnonzero(np.all(difference <= 0, axis=1) & np.any(difference < 0, axis=1)) + 1
    info: dict[str, Any] = {'full_library_identical_competitor_indices': identical.tolist(),
                             'full_library_dominating_competitor_indices': dominates.tolist(),
                             'eligible_columns': len(matrix[0]), 'useful_columns': len(keep),
                             'constraint_count': len(active_rows)}
    if len(dominates):
        return {**info, 'status': 'INFEASIBLE_DOMINATING_COMPETITOR', 'selection': []}
    if not len(active_rows) or not len(keep):
        return {**info, 'status': 'UNIDENTIFIABLE_FULL_LIBRARY', 'selection': []}
    begin = time.monotonic()
    result = milp(np.ones(len(keep)), integrality=np.ones(len(keep)),
                  bounds=Bounds(np.zeros(len(keep)), np.ones(len(keep))),
                  constraints=LinearConstraint(csr_matrix(d), 1.0, np.inf),
                  options={'time_limit': config['solver_time_limit_seconds'], 'mip_rel_gap': 0.0})
    info.update(solver_status=int(result.status), solver_message=result.message,
                solver_seconds=round(time.monotonic() - begin, 3),
                mip_nodes=int(getattr(result, 'mip_node_count', 0) or 0),
                exact_minimum_certified=result.status == 0)
    if result.x is None:
        return {**info, 'status': 'NO_SOLUTION_PROVEN_INFEASIBLE' if result.status == 2 else 'NO_SOLUTION_WITHIN_BUDGET', 'selection': []}
    chosen = np.rint(result.x).astype(int)
    if np.any(d @ chosen < 1 - 1e-7):
        raise RuntimeError('solver incumbent violates strict target margin')
    k = int(chosen.sum())
    # Maximize margin without changing minimum cardinality; margin is an
    # optimization variable, not an astrology coefficient in the scorer.
    margin_matrix = hstack([csr_matrix(d), -np.ones((len(d), 1))], format='csr')
    counts = csr_matrix(np.r_[np.ones(len(keep)), 0.0][None, :])
    second = milp(np.r_[np.zeros(len(keep)), -1.0],
                  integrality=np.ones(len(keep) + 1),
                  bounds=Bounds(np.r_[np.zeros(len(keep)), 1.0], np.r_[np.ones(len(keep)), 2.0 * k]),
                  constraints=LinearConstraint(vstack([margin_matrix, counts]),
                                               np.r_[np.zeros(len(d)), k], np.r_[np.full(len(d), np.inf), k]),
                  options={'time_limit': config['solver_time_limit_seconds'], 'mip_rel_gap': 0.0})
    if second.x is not None:
        candidate = np.rint(second.x[:-1]).astype(int)
        if candidate.sum() == k and np.all(d @ candidate >= 1):
            chosen = candidate
    selection = keep[np.flatnonzero(chosen)].tolist()
    return {**info, 'status': 'FITTED_AT_RULE_RESOLUTION', 'selection': selection,
            'selected_count': len(selection), 'minimum_margin': int(np.min(d @ chosen)),
            'margin_optimum_certified': second.status == 0,
            'minute_identified': len(identical) == 0}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--behavior', required=True, type=Path)
    parser.add_argument('--ephemeris-root', required=True, type=Path)
    parser.add_argument('--stages', default='100,1000,10000')
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    lock = (args.output_dir / 'runner.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    stages = [int(s) for s in args.stages.split(',')]
    if stages != sorted(set(stages)) or stages[0] != 100:
        raise ValueError('stages must begin at 100 and increase strictly')
    config = default_config(stages)
    owner = json.loads((TASK / 'ASTROHD-V14-OWNER-METHOD-CONTRACT-20260924.json').read_text())
    operation = operation_projection(config)
    admit(owner, operation)  # Actual runnable config, not a copied promise.
    freeze_path = TASK / 'ASTROHD-V13-SCORING-FREEZE-20260924.json'
    map_path = TASK / 'ASTROHD-V13-TARGET-BLIND-CONSENSUS-MAP-20260924.json'
    crosswalk_path = ROOT / 'reference/research/life_patterns_astrohd_owner_recovery_crosswalk_v1.json'
    freeze = json.loads(freeze_path.read_text())
    consensus = json.loads(map_path.read_text())
    behavior = json.loads(args.behavior.read_text())
    supported = set(behavior_weight_variants(behavior, json.loads(crosswalk_path.read_text()))['equal_domain'])
    raw = registry(consensus, supported)
    libraries = {'raw_stack': raw, 'lineage_dedup': deduplicate(raw)}
    candidate_rows = candidates(freeze, max(stages), config['seed'])
    provenance = {'created_utc': datetime.now(UTC).isoformat(), 'config': config,
                  'operation': operation, 'owner_contract_sha256': sha(TASK / 'ASTROHD-V14-OWNER-METHOD-CONTRACT-20260924.json'),
                  'behavior_sha256': sha(args.behavior), 'source_map_sha256': sha(map_path),
                  'source_module_sha256': sha(ROOT / 'src/hdmatch/evaluation/astrohd_v14_rules.py'),
                  'runner_sha256': sha(Path(__file__)),
                  'ephemeris_sha256': {p.name: sha(p) for p in args.ephemeris_root.glob('*.se1')},
                  'source_inventory_counts': {a: len(r) for a, r in libraries.items()}}
    dump(args.output_dir / 'freeze.json', provenance)
    dump(args.output_dir / 'candidates.json', candidate_rows)
    dump(args.output_dir / 'private-rule-inventories.json', libraries)
    report: dict[str, Any] = {'claim_scope': config['claim'], 'provenance': provenance, 'stages': [], 'root_outcome': 'OPEN'}
    previous: dict[str, list[int]] = {}
    raw_matrix: list[np.ndarray] = []
    raw_id_to_index = {r['rule_id']: i for i, r in enumerate(raw)}
    arm_indices = {a: [raw_id_to_index[r['rule_id']] for r in rows] for a, rows in libraries.items()}
    location = freeze['astronomy']['location']
    for n in stages:
        print(f'Building cached feature rows through {n}', flush=True)
        for row in candidate_rows[len(raw_matrix):n]:
            snapshot = build_snapshot(datetime.fromisoformat(row['utc']), latitude=location['latitude'], longitude=location['longitude'], ephemeris_root=args.ephemeris_root)
            raw_matrix.append(feature_row(snapshot, raw))
        matrix = np.vstack(raw_matrix)
        np.savez_compressed(args.output_dir / 'feature-cache.npz', matrix=matrix)
        stage: dict[str, Any] = {'n': n, 'started_utc': datetime.now(UTC).isoformat(), 'arms': {}}
        last_n = report['stages'][-1]['n'] if report['stages'] else 1
        for arm in config['arms']:
            rows = libraries[arm]
            x = matrix[:, arm_indices[arm]]
            outcome = {'unselected_all_rules': ranking(x, list(range(len(rows))), candidate_rows[:n])}
            if arm in previous:
                outcome['frozen_previous_subset_full_panel'] = ranking(x, previous[arm], candidate_rows[:n])
                outcome['frozen_previous_subset_new_candidates_only'] = ranking(x, previous[arm], candidate_rows[:n], start=last_n)
                outcome['frozen_previous_subset_evaluated_utc'] = datetime.now(UTC).isoformat()
                dump(args.output_dir / f'pre-refit-{n}-{arm}.json', outcome)
            fit = sparse_fit(x, config)
            outcome['fit'] = fit
            if fit['selection']:
                previous[arm] = fit['selection']
                outcome['fitted_panel_ranking'] = ranking(x, fit['selection'], candidate_rows[:n])
                outcome['selected_rules'] = [rows[i] for i in fit['selection']]
                outcome['source_counts'] = dict(Counter(rows[i]['source_id'] for i in fit['selection']))
                outcome['leave_one_rule_out'] = [ranking(x, [j for j in fit['selection'] if j != i], candidate_rows[:n]) for i in fit['selection']]
            outcome['refit_finished_utc'] = datetime.now(UTC).isoformat()
            stage['arms'][arm] = outcome
            print(json.dumps({'n': n, 'arm': arm, 'fit': {k: v for k, v in fit.items() if k != 'selection'}, 'rank': outcome.get('fitted_panel_ranking'), 'sources': outcome.get('source_counts')}), flush=True)
        report['stages'].append(stage)
        dump(args.output_dir / 'result.json', report)
        if not any(v['fit']['selection'] for v in stage['arms'].values()):
            report['stop_reason'] = 'No fitted arm at this stage; inspect representational failure before adding easy decoys.'
            dump(args.output_dir / 'result.json', report)
            break
    dump(args.output_dir / 'completed.json', {'completed_utc': datetime.now(UTC).isoformat(), 'result_sha256': sha(args.output_dir / 'result.json')})
    print('Completed bounded staged run; result.json written.', flush=True)


if __name__ == '__main__':
    main()
