"""Synthetic evidence-integrity regressions, not tests of astrological validity."""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('receipt_v2', ROOT/'scripts/validate_astrology_deep_analysis_receipt_v2.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def fixture(tmp_path):
    data = {'rules': [{'rule_id': 'R1', 'state': 'ACTIVE'},
                      {'rule_id': 'R2', 'state': 'INACTIVE'}]}
    ep = tmp_path/'evidence.json'; ep.write_text(json.dumps(data))
    c = {'schema_version': 2, 'task_id': 'synthetic-fixture', 'evidence_mode': 'DEVELOPMENT',
         'protocol_sha256': 'a'*64, 'catalog_sha256': 'b'*64, 'input_manifest_sha256': 'c'*64,
         'catalog_dispositions': [{'id': 'synthetic_library', 'status': 'SELECTED', 'reason': 'synthetic test', 'module_ids': ['geometry']}],
         'modules': [{'id': 'geometry', 'required': True, 'checks': ['pair_matrix'],
                      'expected_rule_ids': ['R1', 'R2']}]}
    anchors=[]
    c['anchor_artifact_ids']={}
    for name in ('protocol', 'catalog', 'input_manifest'):
        ap=tmp_path/(name+'.json')
        contents = {'current_or_retained':[{'id':'synthetic_library'}]} if name=='catalog' else {'synthetic_anchor':name}
        ap.write_text(json.dumps(contents))
        c[name+'_sha256']=mod.digest(ap)
        c['anchor_artifact_ids'][name+'_sha256']=name
        anchors.append({'id':name,'path':ap.name,'sha256':mod.digest(ap),'format':'json'})
    cp = tmp_path/'contract.json'; cp.write_text(json.dumps(c)); ch = mod.digest(cp)
    ref = {'artifact_id': 'data', 'pointer': '/rules'}
    r = {'schema_version': 2, 'task_id': c['task_id'], 'evidence_mode': c['evidence_mode'],
         'protocol_sha256': c['protocol_sha256'], 'catalog_sha256': c['catalog_sha256'],
         'input_manifest_sha256': c['input_manifest_sha256'], 'contract_sha256': ch,
         'artifacts': [{'id': 'data', 'path': 'evidence.json', 'sha256': mod.digest(ep), 'format': 'json'}]+anchors,
         'modules': [{'id': 'geometry', 'status': 'EXECUTED', 'rule_results_ref': ref,
                      'checks': [{'id': 'pair_matrix', 'status': 'DONE', 'evidence_refs': [ref]}]}],
         'claims': [{'id': 'C1', 'text': 'A synthetic predicate is active; not a human conclusion.',
                     'support_refs': [{'artifact_id': 'data', 'pointer': '/rules/0'}],
                     'counterevidence_refs': [], 'evidence_mode': 'DEVELOPMENT',
                     'predictive_validity': 'NOT_ESTABLISHED_BY_THIS_RECEIPT',
                     'dependency_groups': ['test_geometry']} ]}
    rp = tmp_path/'receipt.json'; rp.write_text(json.dumps(r))
    return cp, rp, ch, r, ep


def run(tmp_path, mutate=None):
    cp, rp, ch, r, ep = fixture(tmp_path)
    if mutate: mutate(r, ep)
    rp.write_text(json.dumps(r))
    return mod.verify(cp, rp, tmp_path, ch)


def test_verified_fixture_does_not_claim_semantic_or_scientific_certainty(tmp_path):
    out = run(tmp_path)
    assert out['declared_execution_complete']
    assert out['semantic_correctness'] == 'NOT_CERTIFIED_BY_MECHANICAL_CHECK'
    assert out['predictive_validity'] == 'NOT_ESTABLISHED_BY_THIS_RECEIPT'


def test_all_unavailable_is_accounted_but_not_complete(tmp_path):
    def mutate(r, p): r['modules'] = [{'id': 'geometry', 'status': 'UNAVAILABLE', 'reason': 'fixture'}]
    out = run(tmp_path, mutate)
    assert out['structure_and_references_valid']
    assert not out['declared_execution_complete']
    assert out['delivery_class'] == 'SCOPED_WITH_GAPS'


@pytest.mark.parametrize('mutation', [
    lambda r,p: r['modules'].append(copy.deepcopy(r['modules'][0])),
    lambda r,p: r['artifacts'].append(copy.deepcopy(r['artifacts'][0])),
    lambda r,p: r['claims'].append(copy.deepcopy(r['claims'][0])),
    lambda r,p: r['modules'].clear(),
    lambda r,p: r['modules'][0]['checks'].clear(),
    lambda r,p: r['modules'][0]['checks'][0].update(evidence_refs=['I checked it']),
    lambda r,p: r['claims'][0]['support_refs'][0].update(artifact_id='nonexistent'),
    lambda r,p: r['claims'][0]['support_refs'][0].update(pointer='/missing'),
    lambda r,p: r['artifacts'][0].update(path='../outside.json'),
    lambda r,p: r['artifacts'][0].update(sha256='0'*64),
    lambda r,p: r.update(contract_sha256='0'*64),
    lambda r,p: r.update(protocol_sha256='0'*64),
    lambda r,p: r['claims'][0].update(evidence_mode='PROSPECTIVE'),
    lambda r,p: r['claims'][0].update(predictive_validity='VALIDATED'),
    lambda r,p: p.write_text('{"rules": []}'),
])
def test_invalid_or_laundered_receipts_fail(tmp_path, mutation):
    assert not run(tmp_path, mutation)['structure_and_references_valid']


def test_hidden_rule_omission_rejected_even_with_correct_file_hash(tmp_path):
    def mutate(r, p):
        d=json.loads(p.read_text());d['rules'].pop();p.write_text(json.dumps(d))
        r['artifacts'][0]['sha256']=mod.digest(p)
    assert not run(tmp_path,mutate)['structure_and_references_valid']


def test_changed_contract_not_accepted_under_old_commitment(tmp_path):
    cp,rp,ch,r,ep=fixture(tmp_path)
    c=json.loads(cp.read_text());c['modules'][0]['required']=False;cp.write_text(json.dumps(c))
    assert not mod.verify(cp,rp,tmp_path,ch)['structure_and_references_valid']


def test_no_claims_can_be_an_honest_result(tmp_path):
    def mutate(r,p): r.update(claims=[],no_claims_reason='No supported interpretations in this synthetic test')
    assert run(tmp_path,mutate)['structure_and_references_valid']


def test_catalog_entry_cannot_be_forgotten_even_under_a_new_contract(tmp_path):
    cp,rp,ch,r,ep=fixture(tmp_path)
    c=json.loads(cp.read_text());c['catalog_dispositions']=[]
    cp.write_text(json.dumps(c));ch=mod.digest(cp)
    r['contract_sha256']=ch;rp.write_text(json.dumps(r))
    out=mod.verify(cp,rp,tmp_path,ch)
    assert not out['structure_and_references_valid']
    assert 'catalog-disposition set mismatch' in out['errors']


def test_selected_catalog_entry_requires_a_real_planned_module(tmp_path):
    cp,rp,ch,r,ep=fixture(tmp_path)
    c=json.loads(cp.read_text());c['catalog_dispositions'][0]['module_ids']=['imaginary']
    cp.write_text(json.dumps(c));ch=mod.digest(cp)
    r['contract_sha256']=ch;rp.write_text(json.dumps(r))
    assert not mod.verify(cp,rp,tmp_path,ch)['structure_and_references_valid']


def test_generated_template_is_not_mistaken_for_execution(tmp_path):
    import subprocess
    import sys
    cp,rp,ch,r,ep=fixture(tmp_path)
    dest=tmp_path/'generated.json'
    z=subprocess.run([sys.executable,str(ROOT/'scripts/new_astrology_deep_analysis_receipt_v2.py'),
                      '--contract',str(cp),'--out',str(dest)],capture_output=True,text=True)
    assert z.returncode==0, z.stderr
    out=mod.verify(cp,dest,tmp_path,ch)
    assert not out['structure_and_references_valid']
    assert not out['declared_execution_complete']
