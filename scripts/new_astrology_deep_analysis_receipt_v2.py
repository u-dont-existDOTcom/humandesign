#!/usr/bin/env python3
"""Create an intentionally unfinished receipt from a predeclared V2 contract.

This does not select the case's method, calculate a chart or certify a source.
The external commitment must be preserved before outcome inspection/evaluation.
"""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--contract', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    contract = json.loads(args.contract.read_text())
    if contract.get('schema_version') != 2 or not contract.get('modules'):
        ap.error('Expected a nonempty predeclared V2 contract')
    commitment = hashlib.sha256(args.contract.read_bytes()).hexdigest()
    receipt = {key: contract[key] for key in
               ('schema_version', 'task_id', 'evidence_mode', 'protocol_sha256',
                'catalog_sha256', 'input_manifest_sha256')}
    receipt.update(contract_sha256=commitment, artifacts=[], claims=[],
                   no_claims_reason='NOT_YET_ANALYZED', modules=[])
    for plan in contract['modules']:
        receipt['modules'].append({
            'id': plan['id'], 'status': 'TODO', 'reason': '',
            'checks': [{'id': cid, 'status': 'TODO', 'evidence_refs': [], 'reason': ''}
                       for cid in plan['checks']],
            'rule_results_ref': None,
        })
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({'receipt': str(args.out), 'contract_sha256': commitment,
                      'status': 'UNFINISHED_TEMPLATE_NOT_EXECUTION'}, indent=2))


if __name__ == '__main__':
    main()
