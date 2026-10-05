#!/usr/bin/env python3
"""Check a predeclared analysis contract against artifacts, not prose assertions.

This verifies identity, references and declared execution coverage. It does NOT
certify source interpretation, blinding, astronomical correctness, or prediction.
No network access; referenced evidence must be inside the selected evidence root.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

MODES = {'DEVELOPMENT', 'RETROSPECTIVE_BLIND', 'PROSPECTIVE', 'DESCRIPTIVE'}
MODULE_STATES = {'EXECUTED', 'UNAVAILABLE', 'NOT_APPLICABLE', 'SUPERSEDED'}
CHECK_STATES = {'DONE', 'UNAVAILABLE', 'NOT_APPLICABLE', 'SUPERSEDED'}
RULE_STATES = {'ACTIVE', 'INACTIVE', 'UNRESOLVED'}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique(rows: Any, field: str, label: str, errors: list[str]) -> dict[str, dict]:
    if not isinstance(rows, list):
        errors.append(f'{label}: expected a list')
        return {}
    out = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get(field), str) or not row[field]:
            errors.append(f'{label}: missing/string {field}')
            continue
        key = row[field]
        if key in out:
            errors.append(f'{label}: duplicate {key}')
        out[key] = row
    return out


def resolve_pointer(value: Any, pointer: str) -> Any:
    if pointer == '':
        return value
    if not pointer.startswith('/'):
        raise ValueError('JSON pointer must be empty or start with /')
    for token in pointer.split('/')[1:]:
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def verify(contract_path: Path, receipt_path: Path, root: Path,
           expected_contract_sha256: str) -> dict[str, Any]:
    errors: list[str] = []
    gaps: list[str] = []
    root = root.resolve()
    if digest(contract_path) != expected_contract_sha256:
        errors.append('contract: differs from externally supplied commitment')
    contract = json.loads(contract_path.read_text())
    receipt = json.loads(receipt_path.read_text())
    if contract.get('schema_version') != 2 or receipt.get('schema_version') != 2:
        errors.append('schema_version must be 2')
    if receipt.get('contract_sha256') != expected_contract_sha256:
        errors.append('receipt: wrong contract_sha256')
    if not isinstance(contract.get('task_id'), str) or not contract['task_id']:
        errors.append('contract: missing task_id')
    if receipt.get('task_id') != contract.get('task_id'):
        errors.append('receipt: wrong task_id')
    mode = contract.get('evidence_mode')
    if mode not in MODES or receipt.get('evidence_mode') != mode:
        errors.append('evidence_mode: invalid or differs from contract')
    # These anchors are deliberately distinct from the case's outcome data.
    for anchor in ('protocol_sha256', 'catalog_sha256', 'input_manifest_sha256'):
        v = contract.get(anchor)
        if not isinstance(v, str) or len(v) != 64 or any(c not in '0123456789abcdef' for c in v):
            errors.append(f'contract: invalid {anchor}')
        if receipt.get(anchor) != v:
            errors.append(f'receipt: wrong {anchor}')

    expected = unique(contract.get('modules'), 'id', 'contract.modules', errors)
    actual = unique(receipt.get('modules'), 'id', 'receipt.modules', errors)
    if not expected:
        errors.append('contract.modules: empty plan')
    if set(expected) != set(actual):
        errors.append('module-set mismatch: '
                      f'missing={sorted(set(expected)-set(actual))}; '
                      f'extra={sorted(set(actual)-set(expected))}')
    artifacts = unique(receipt.get('artifacts'), 'id', 'artifacts', errors)
    data: dict[str, Any] = {}
    for aid, artifact in artifacts.items():
        try:
            rel = artifact['path']
            if not isinstance(rel, str) or Path(rel).is_absolute():
                raise ValueError('path must be relative')
            p = (root / rel).resolve()
            p.relative_to(root)  # also excludes escaping symbolic links
            if not p.is_file():
                raise ValueError('not a file')
            if digest(p) != artifact.get('sha256'):
                raise ValueError('content hash mismatch')
            if artifact.get('format') == 'json':
                data[aid] = json.loads(p.read_text())
            elif artifact.get('format') == 'text':
                data[aid] = p.read_text()
            else:
                raise ValueError('format must be json or text')
        except (KeyError, ValueError, TypeError, OSError) as exc:
            errors.append(f'artifact {aid}: {exc}')

    bindings = contract.get('anchor_artifact_ids', {})
    if not isinstance(bindings, dict):
        errors.append('contract: anchor_artifact_ids must be an object')
        bindings = {}
    for anchor in ('protocol_sha256', 'catalog_sha256', 'input_manifest_sha256'):
        aid = bindings.get(anchor)
        if aid not in data or artifacts.get(aid, {}).get('sha256') != contract.get(anchor):
            errors.append(f'contract: {anchor} lacks matching verified artifact')

    # The predeclared plan must account for the entire committed catalog, not
    # merely the methods the current reader happens to remember. This checks
    # membership/disposition, not whether an exclusion reason is persuasive.
    catalog = data.get(bindings.get('catalog_sha256'), {})
    catalog_rows = []
    if not isinstance(catalog, dict):
        errors.append('catalog: expected an object')
        catalog = {}
    for section in ('current_or_retained', 'important_exploratory_not_default',
                    'material_negative_or_superseded'):
        values = catalog.get(section, [])
        if not isinstance(values, list):
            errors.append(f'catalog: {section} must be a list')
        else:
            catalog_rows.extend(values)
    catalog_ids = unique(catalog_rows, 'id', 'catalog entries', errors)
    dispositions = unique(contract.get('catalog_dispositions'), 'id',
                          'contract.catalog_dispositions', errors)
    if not catalog_ids or set(catalog_ids) != set(dispositions):
        errors.append('catalog-disposition set mismatch')
    disposition_states = {'SELECTED', 'NOT_APPLICABLE', 'UNAVAILABLE',
                          'SUPERSEDED', 'RETAINED_NON_OPERATIONAL'}
    for cid, disposition in dispositions.items():
        if disposition.get('status') not in disposition_states:
            errors.append(f'catalog {cid}: invalid disposition')
        if not isinstance(disposition.get('reason'), str) or not disposition['reason'].strip():
            errors.append(f'catalog {cid}: reason required')
        if disposition.get('status') == 'SELECTED':
            linked = disposition.get('module_ids')
            if not isinstance(linked, list) or not linked or any(m not in expected for m in linked):
                errors.append(f'catalog {cid}: SELECTED needs planned module_ids')

    def reference(ref: Any, label: str) -> Any:
        if not isinstance(ref, dict):
            errors.append(f'{label}: reference must be an object')
            return None
        aid = ref.get('artifact_id')
        if aid not in data:
            errors.append(f'{label}: unverified/missing artifact {aid}')
            return None
        try:
            if artifacts[aid]['format'] == 'json':
                value = resolve_pointer(data[aid], ref.get('pointer', ''))
            else:
                start, end = ref.get('start_line'), ref.get('end_line')
                if type(start) is not int or type(end) is not int:
                    raise ValueError('text references require integer line bounds')
                lines = data[aid].splitlines()
                if not 1 <= start <= end <= len(lines):
                    raise ValueError('invalid line interval')
                value = '\n'.join(lines[start-1:end])
            if value is None:
                raise ValueError('null reference target')
            return value
        except (KeyError, IndexError, ValueError, TypeError) as exc:
            errors.append(f'{label}: unresolved reference ({exc})')
            return None

    executed = 0
    required = 0
    for mid, plan in expected.items():
        if type(plan.get('required')) is not bool:
            errors.append(f'{mid}: required must be a JSON boolean')
        is_required = plan.get('required') is True
        required += int(is_required)
        row = actual.get(mid)
        if row is None:
            continue
        state = row.get('status')
        if state not in MODULE_STATES:
            errors.append(f'{mid}: invalid module status')
            continue
        if state != 'EXECUTED':
            if not isinstance(row.get('reason'), str) or not row['reason'].strip():
                errors.append(f'{mid}: reason is required')
            if is_required:
                gaps.append(f'{mid}: {state}')
            continue
        planned_checks = plan.get('checks', [])
        if (not isinstance(planned_checks, list)
            or any(not isinstance(c, str) or not c for c in planned_checks)
            or len(set(planned_checks)) != len(planned_checks)):
            errors.append(f'{mid}: invalid planned checks')
            planned_checks = []
        checks = unique(row.get('checks'), 'id', f'{mid}.checks', errors)
        if set(checks) != set(planned_checks):
            errors.append(f'{mid}: check-set mismatch')
        complete = True
        for cid, check in checks.items():
            cs = check.get('status')
            if cs not in CHECK_STATES:
                errors.append(f'{mid}/{cid}: invalid status')
            if cs == 'DONE':
                refs = check.get('evidence_refs')
                if not isinstance(refs, list) or not refs:
                    errors.append(f'{mid}/{cid}: missing evidence_refs')
                else:
                    for ref in refs:
                        reference(ref, f'{mid}/{cid}')
            else:
                if not isinstance(check.get('reason'), str) or not check['reason'].strip():
                    errors.append(f'{mid}/{cid}: reason required')
                complete = False
                if is_required:
                    gaps.append(f'{mid}/{cid}: {cs}')
        planned_rules = plan.get('expected_rule_ids', [])
        if (not isinstance(planned_rules, list)
            or any(not isinstance(r, str) or not r for r in planned_rules)
            or len(set(planned_rules)) != len(planned_rules)):
            errors.append(f'{mid}: invalid expected_rule_ids')
            planned_rules = []
        if planned_rules:
            rules = reference(row.get('rule_results_ref'), f'{mid}.rule_results')
            results = unique(rules, 'rule_id', f'{mid}.rules', errors)
            if set(results) != set(planned_rules):
                errors.append(f'{mid}: expected/evaluated rule-set mismatch')
            for rid, result in results.items():
                if result.get('state') not in RULE_STATES:
                    errors.append(f'{mid}/{rid}: invalid rule-result state')
                if result.get('state') == 'UNRESOLVED':
                    complete = False
                    if is_required:
                        gaps.append(f'{mid}/{rid}: UNRESOLVED')
        executed += int(is_required and complete)

    claims = unique(receipt.get('claims', []), 'id', 'claims', errors)
    for cid, claim in claims.items():
        if not isinstance(claim.get('text'), str) or not claim['text'].strip():
            errors.append(f'claim {cid}: empty text')
        refs = claim.get('support_refs')
        if not isinstance(refs, list) or not refs:
            errors.append(f'claim {cid}: missing support_refs')
        else:
            for ref in refs:
                reference(ref, f'claim {cid}')
        counter = claim.get('counterevidence_refs')
        if not isinstance(counter, list):
            errors.append(f'claim {cid}: counterevidence_refs must be a list')
        else:
            for ref in counter:
                reference(ref, f'claim {cid} counterevidence')
        # No conflation of source fidelity with human prediction accuracy.
        if claim.get('evidence_mode') != mode:
            errors.append(f'claim {cid}: evidence-mode promotion')
        if claim.get('predictive_validity') != 'NOT_ESTABLISHED_BY_THIS_RECEIPT':
            errors.append(f'claim {cid}: unsupported predictive certification')
        if not isinstance(claim.get('dependency_groups'), list):
            errors.append(f'claim {cid}: dependency_groups must be a list')
    if not claims and not receipt.get('no_claims_reason'):
        errors.append('No claims: supply no_claims_reason rather than invent conclusions')

    complete = not errors and required > 0 and executed == required and not gaps
    return {
        'schema_version': 2,
        'contract_sha256': expected_contract_sha256,
        'structure_and_references_valid': not errors,
        'declared_execution_complete': complete,
        'delivery_class': ('DECLARED_PROFILE_EXECUTED' if complete else
                           'SCOPED_WITH_GAPS' if not errors else 'INVALID_RECEIPT'),
        'required_modules': required,
        'required_modules_executed': executed,
        'errors': errors,
        'gaps': gaps,
        'semantic_correctness': 'NOT_CERTIFIED_BY_MECHANICAL_CHECK',
        'actual_blinding': 'NOT_CERTIFIED_BY_MECHANICAL_CHECK',
        'predictive_validity': 'NOT_ESTABLISHED_BY_THIS_RECEIPT',
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--contract', required=True, type=Path)
    ap.add_argument('--contract-sha256', required=True)
    ap.add_argument('--receipt', required=True, type=Path)
    ap.add_argument('--evidence-root', required=True, type=Path)
    ap.add_argument('--require-executed', action='store_true')
    args = ap.parse_args()
    try:
        report = verify(args.contract, args.receipt, args.evidence_root, args.contract_sha256)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        report = {'structure_and_references_valid': False,
                  'declared_execution_complete': False,
                  'delivery_class': 'INVALID_RECEIPT', 'errors': [str(exc)]}
    print(json.dumps(report, indent=2))
    if not report['structure_and_references_valid']:
        raise SystemExit(2)
    if args.require_executed and not report['declared_execution_complete']:
        raise SystemExit(3)


if __name__ == '__main__':
    main()
