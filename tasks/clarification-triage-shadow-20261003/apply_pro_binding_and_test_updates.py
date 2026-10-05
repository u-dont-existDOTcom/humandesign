"""Preserve admitted recovery bindings and adapt fixtures to the corrected contract."""
from pathlib import Path
import ast

ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'apps/life-patterns-participant/participant/shadow_triage.py'
s=p.read_text()

def change(old,new):
 global s
 assert s.count(old)==1,(old[:80],s.count(old))
 s=s.replace(old,new)

change('''    admission_source_review_complete: bool = False
    unreviewed_route_ids:''','''    admission_source_review_complete: bool = False
    admitted_specs: list[GapSpecCandidate] = Field(default_factory=list, max_length=80)
    unreviewed_route_ids:''')
change('''    audit.admission_reviews = []
    audit.unreviewed_route_ids = []''','''    audit.admission_reviews = []
    audit.admitted_specs = []
    audit.unreviewed_route_ids = []''')
change('''        audit.admission_reviews.extend(reviewed.reviews)
        accepted += sum(r.approved for r in reviewed.reviews)''','''        audit.admission_reviews.extend(reviewed.reviews)
        approved = {r.route_id for r in reviewed.reviews if r.approved}
        audit.admitted_specs.extend(c for c in specs.candidates if c.route_id in approved)
        accepted += len(approved)''')
change('''    audit_by_route = {review.route_id: review for review in match_audit.reviews}
    compact_route_by_id''','''    audit_by_route = {review.route_id: review for review in match_audit.reviews}
    recovered_specs = {spec.route_id: spec for spec in match_audit.admitted_specs}
    compact_route_by_id''')
change('''            original_question_text = candidate.question.text
        else:
            if audit_review is None:
                raise ValueError("Recovered route has no deterministic audit binding.")
            source_anchor_turn_ids = list(audit_review.source_turn_ids)
            antecedent_turn_ids = list(audit_review.source_turn_ids)
            missing_distinction = (
                "The route-requested response remains preliminary or contradictory in source."
            )''','''            original_question_text = candidate.question.text
            equivalent_context = candidate.question.equivalent_context
        else:
            recovered_spec = recovered_specs.get(route_id)
            if audit_review is None or recovered_spec is None:
                raise ValueError("Recovered route lacks independently admitted source bindings.")
            source_anchor_turn_ids = list(recovered_spec.source_anchor_turn_ids)
            antecedent_turn_ids = list(recovered_spec.antecedent_turn_ids)
            equivalent_context = recovered_spec.equivalent_context
            missing_distinction = recovered_spec.missing_distinction''')
change('''                "candidate_mode": compact_route.get("candidate_mode"),
                "source_anchor_turn_ids": source_anchor_turn_ids,''','''                "candidate_mode": compact_route.get("candidate_mode"),
                "equivalent_context": equivalent_context,
                "source_anchor_turn_ids": source_anchor_turn_ids,''')
change('''            candidate_mode = spec.get("candidate_mode")
            question = Question(''','''            question = Question(''')
change('''                equivalent_context=candidate_mode != "repair_only",''','''                equivalent_context=bool(spec.get("equivalent_context", False)),''')
p.write_text(s)

p=ROOT/'apps/life-patterns-participant/tests/test_shadow_triage.py'
s=p.read_text()
# Add a fully explicit fake admission response at the newly required stage.
helper='''def approved_recovery_admission(payload):
    return GapSpecAdmission(source_review_complete=True, reviews=[
        GapSpecAdmissionReview(
            candidate_id=c["candidate_id"], route_id=c["route_id"], approved=True,
            source_references_valid=True, not_already_answered=True, premise_supported=True,
            antecedent_supported=True, context_supported=True, material_information_gain=True,
            independent_for_batch=True, failure_codes=[],
        ) for c in payload["proposed_gap_specs"]
    ]), {"duration_seconds": 2.0, "prompt_tokens": 1000, "completion_tokens": 80}


'''
assert s.count('class OmissionRecoveryFake:')==1
s=s.replace('class OmissionRecoveryFake:',helper+'class OmissionRecoveryFake:',1)
# Modify only the named fake classes, preserving tests of the live provider boundary.
for cls in ['OmissionRecoveryFake','FastSpecOmissionRecoveryFake']:
 tree=ast.parse(s); node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls)
 lines=s.splitlines(keepends=True); chunk=''.join(lines[node.lineno-1:node.end_lineno])
 needle='''        if schema is GapMatchAuditResponse:
'''
 assert chunk.count(needle)==1
 chunk=chunk.replace(needle,'''        if schema is GapSpecAdmission:
            return approved_recovery_admission(payload)
        if schema is GapMatchAuditResponse:
''')
 s=''.join(lines[:node.lineno-1])+chunk+''.join(lines[node.end_lineno:])
# Test projections must include actual ready wording, not assume a gap is a question.
node=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name=='test_admitted_batch_order_follows_source_anchor_order_not_model_rank')
lines=s.splitlines(keepends=True); chunk=''.join(lines[node.lineno-1:node.end_lineno])
chunk=chunk.replace('''            "match_audit": GapMatchAudit(reviews=[]),''','''            "match_audit": GapMatchAudit(reviews=[]),
            "final_questions": {c.question.route_id: c.question for c in triage.candidates},''')
s=''.join(lines[:node.lineno-1])+chunk+''.join(lines[node.end_lineno:])
# Old test codified the unsafe bypass. Keep it, but require rejection to remain binding.
s=s.replace('def test_match_audit_can_recover_proposed_route_rejected_only_on_answer_completeness():','def test_match_audit_cannot_override_full_source_admission_rejection():')
node=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name=='test_match_audit_cannot_override_full_source_admission_rejection')
lines=s.splitlines(keepends=True); chunk=''.join(lines[node.lineno-1:node.end_lineno])
chunk=chunk.replace('assert summary["admitted_route_ids"] == ["G19"]','assert summary["admitted_route_ids"] == []').replace('assert summary["recovered_omission_route_ids"] == ["G19"]','assert summary["recovered_omission_route_ids"] == []\n    assert summary["shadow_outcome"] == "no_admitted_candidate"')
s=''.join(lines[:node.lineno-1])+chunk+''.join(lines[node.end_lineno:])
node=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name=='test_contradictory_match_audit_recovers_route')
lines=s.splitlines(keepends=True); chunk=''.join(lines[node.lineno-1:node.end_lineno])
chunk=chunk.replace('''    audit = GapMatchAudit(
        reviews=[''','''    audit = GapMatchAudit(
        admission_source_review_complete=True,
        admission_reviews=[GapSpecAdmissionReview(
            candidate_id="C1", route_id="G23", approved=True,
            source_references_valid=True, not_already_answered=True, premise_supported=True,
            antecedent_supported=True, context_supported=True, material_information_gain=True,
            independent_for_batch=True, failure_codes=[],
        )],
        reviews=[''')
s=''.join(lines[:node.lineno-1])+chunk+''.join(lines[node.end_lineno:])
s=s.replace('''        "GapSpecTriage",
        "GapMatchAudit",
        "GapQuestionRender",''','''        "GapSpecTriage",
        "GapMatchAudit",
        "GapMatchAdmission",
        "GapQuestionRender",''')
s=s.replace('''    assert len(fake.calls) == 4
    assert fake.calls[1][1]["pairs"]
    assert fake.calls[2][1]["render_specs"]
    assert fake.calls[3][1]["items"]''','''    assert len(fake.calls) == 5
    assert fake.calls[1][1]["pairs"]
    assert fake.calls[2][1]["proposed_gap_specs"]
    assert fake.calls[3][1]["render_specs"]
    assert fake.calls[4][1]["items"]''')
p.write_text(s)
print('BINDINGS_AND_FIXTURES_UPDATED')
