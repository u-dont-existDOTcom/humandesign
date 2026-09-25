#!/usr/bin/env python3
"""Replay the public six-rule manifest without any private behavioral answers."""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime
from pathlib import Path
from hdmatch.evaluation.astrohd_v13_traditions import build_snapshot
from hdmatch.evaluation.astrohd_v14_rules import registry, feature_row

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / 'tasks/scenario-owner-recovery-calibration-20260923'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=TASK/'ASTROHD-V14-SIX-RULE-MODEL-20260925.json')
    parser.add_argument('--when', action='append', required=True, help='Timezone-aware ISO timestamp; repeat for comparisons')
    parser.add_argument('--ephemeris-root', type=Path, required=True)
    parser.add_argument('--latitude', type=float, default=39.9526)
    parser.add_argument('--longitude', type=float, default=-75.1652)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    model = json.loads(args.manifest.read_text())
    if digest(ROOT/model['rule_module']) != model['rule_module_sha256']:
        raise ValueError('Frozen rule-module hash mismatch')
    source_path = ROOT/model['source_map_path']
    if digest(source_path) != model['source_map_sha256']:
        raise ValueError('Frozen source-map hash mismatch')
    consensus = json.loads(source_path.read_text())
    # Use the full generic ontology; selected IDs are fixed in the manifest.
    all_rules = registry(consensus, {d['domain_id'] for d in consensus['domains']})
    lookup = {r['rule_id']: r for r in all_rules}
    rules = [lookup[key] for key in model['selected_rule_ids']]
    if len(set(model['selected_rule_ids'])) != len(rules):
        raise ValueError('Duplicate selected rule IDs')
    if model['weight_per_selected_rule'] != 1:
        raise ValueError('This manifest requires equal one-vote rules')
    results = []
    for stamp in args.when:
        when = datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        snapshot = build_snapshot(when, latitude=args.latitude, longitude=args.longitude,
                                  ephemeris_root=args.ephemeris_root)
        values = feature_row(snapshot, rules)
        results.append({'utc': when.isoformat(), 'score': int(values.sum()),
                        'rule_values': dict(zip(model['selected_rule_ids'], values.tolist()))})
    report = {'model_sha256': digest(args.manifest), 'private_answers_required': False,
              'classification': model['classification'], 'results': results}
    text = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
