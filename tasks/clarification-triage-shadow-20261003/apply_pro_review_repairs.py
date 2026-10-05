"""One-shot, exact-base repair script retained for review provenance."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
assert subprocess.check_output(["git", "-C", str(ROOT), "branch", "--show-current"], text=True).strip() == "pro/gap-triage-review-20261005"
p = ROOT / "apps/life-patterns-participant/participant/shadow_triage.py"
s = p.read_text()


def replace(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:80], s.count(old), count)
    s = s.replace(old, new)


replace('source_turn_ids: list[str] = Field(min_length=1, max_length=4)',
        'source_turn_ids: list[str] = Field(min_length=1, max_length=1000)')
replace('class GapMatchAudit(StrictModel):\n    reviews: list[GapMatchedRouteReview] = Field(default_factory=list, max_length=80)\n',
'''class GapMatchAudit(StrictModel):
    reviews: list[GapMatchedRouteReview] = Field(default_factory=list, max_length=80)
    # Caller-owned evidence: the detector response cannot populate these fields.
    admission_reviews: list[GapSpecAdmissionReview] = Field(default_factory=list, max_length=80)
    admission_source_review_complete: bool = False
    unreviewed_route_ids: list[str] = Field(default_factory=list, max_length=80)
    prior_admission_blocked_route_ids: list[str] = Field(default_factory=list, max_length=80)
''')
replace('def _shadow_route_cards(state: dict, instrument: dict) -> list[dict]:',
'''def _shadow_route_cards(
    state: dict, instrument: dict, *, allow_semantic_context: bool = False
) -> list[dict]:''')
replace('''            and not context_match_turn_ids
        ):
            continue''','''            and not context_match_turn_ids
            and not (allow_semantic_context and turns)
        ):
            continue''')
replace('''def make_gap_triage_context(state: dict, instrument: dict) -> dict:
    turns = _complete_behavioral_source(state)
    candidate_routes = _shadow_route_cards(state, instrument)''','''def make_gap_triage_context(
    state: dict, instrument: dict, *, allow_semantic_context: bool = False
) -> dict:
    turns = _complete_behavioral_source(state)
    candidate_routes = _shadow_route_cards(
        state, instrument, allow_semantic_context=allow_semantic_context
    )''')
replace('''    full = make_gap_triage_context(state, instrument)
    turns = full["turns"]''','''    full = make_gap_triage_context(state, instrument, allow_semantic_context=True)
    turns = full["turns"]''')
replace('''self-contained unasked route needs no antecedent. Name candidate dependencies only when a later
candidate actually depends on an earlier candidate's answer.''','''self-contained unasked route needs no antecedent. A dependent route in the menu is NOT proof
that its required context exists. With no supplied match, use a real answered source turn only if
it semantically supplies that context, set equivalent_context true, and let independent admission
verify it. If there is no such turn, do not propose the route. Name candidate dependencies only
when a later candidate actually depends on an earlier candidate's answer.''')

helper = '''def admit_gap_match_audit(
    state: dict,
    instrument: dict,
    triage: GapTriage,
    admission: GapAdmission,
    audit: GapMatchAudit,
    provider: SemanticProvider,
    *,
    model: str,
    effort: str,
) -> tuple[GapMatchAudit, list[dict]]:
    """Refute newly detected omissions against complete source before they can be asked.

    The local detector is a proposal source, not an admission authority. It cannot
    reverse an existing independent veto in the same pass. Excess proposals remain
    explicit deferred work rather than being mistaken for a completed review.
    """
    proposed_ids = {c.question.route_id for c in triage.candidates}
    approved_ids = {r.route_id for r in admission.reviews if r.approved}
    candidates = [
        r for r in audit.reviews
        if r.status in {"preliminary_gap", "contradictory_gap"}
        and r.independent_for_batch and r.route_id not in proposed_ids
    ]
    audit.prior_admission_blocked_route_ids = [
        r.route_id for r in audit.reviews
        if r.status in {"preliminary_gap", "contradictory_gap"}
        and r.route_id in proposed_ids and r.route_id not in approved_ids
    ]
    order = {str(t["turn_id"]): i for i, t in enumerate(_complete_behavioral_source(state))}
    candidates.sort(key=lambda r: (min(order[x] for x in r.source_turn_ids), r.route_id))
    context = make_gap_spec_triage_context(state, instrument)
    capacity = max(0, MAX_GAP_CANDIDATES - len(approved_ids))
    calls: list[dict] = []
    audit.admission_reviews = []
    audit.unreviewed_route_ids = []
    accepted = 0
    offset = 0
    while offset < len(candidates) and accepted < capacity:
        chunk = candidates[offset:offset + min(MAX_GAP_CANDIDATES, capacity - accepted)]
        offset += len(chunk)
        specs = GapSpecTriage(
            decision="clarification_needed",
            candidates=[
                GapSpecCandidate(
                    candidate_id=f"C{i}", rank=i, route_id=r.route_id,
                    # Bounded navigation anchors; admission still receives every exact turn.
                    source_anchor_turn_ids=list(r.source_turn_ids[-2:]),
                    missing_distinction=(
                        "A source-matched response may be preliminary or contradictory. "
                        "Determine whether the exact route-requested distinction is still "
                        "unresolved after reviewing all source, including later answers."
                    ),
                ) for i, r in enumerate(chunk, 1)
            ],
        )
        normalize_gap_spec_bindings(specs, context)
        validate_gap_spec_triage(specs, context)
        payload = make_gap_spec_admission_context(state, instrument, context, specs)
        value, call = provider.call(
            GAP_SPEC_ADMISSION_PROMPT, payload, GapSpecAdmission, model, effort
        )
        reviewed = GapSpecAdmission.model_validate(value)
        validate_gap_spec_admission(reviewed, specs)
        audit.admission_reviews.extend(reviewed.reviews)
        accepted += sum(r.approved for r in reviewed.reviews)
        calls.append({"shadow_stage": "GapMatchAdmission", **dict(call)})
    audit.unreviewed_route_ids = [r.route_id for r in candidates[offset:]]
    audit.admission_source_review_complete = not audit.unreviewed_route_ids
    # Each admitted group was source-complete even when another group remains pending.
    if audit.admission_reviews:
        audit.admission_source_review_complete = True
    return audit, calls


'''
replace('def run_shadow_fast_spec_path(\n', helper + 'def run_shadow_fast_spec_path(\n')
# Place the same admission boundary in both execution lanes, not only the benchmark.
needle='''    (
        render_context,
        final_questions,
        render_route_ids,
    ) = make_gap_question_render_context('''
insertion='''    if match_audit.reviews:
        match_audit, audit_admission_calls = admit_gap_match_audit(
            state, instrument, triage, admission, match_audit, provider,
            model=model, effort=effort,
        )
        calls.extend(audit_admission_calls)
        match_audit_pending = match_audit_pending or bool(match_audit.unreviewed_route_ids)

'''
replace(needle, insertion + needle, count=2)
# A raw deferred audit stays detection-only. The caller must send its proposals through
# the same admission helper; it cannot authorize participant questions by itself.
replace('''    answer_completeness_codes = {"already_answered", "low_information_gain"}
    for review in match_audit.reviews:''','''    recovered_approved = {
        r.route_id for r in match_audit.admission_reviews if r.approved
    } if match_audit.admission_source_review_complete else set()
    for review in match_audit.reviews:''')
replace('''        proposed = candidate_by_route.get(review.route_id)
        if proposed is not None:
            admission_review = admission_by_candidate.get(proposed.candidate_id)
            if admission_review is None:
                continue
            gap_failure_codes = set(admission_review.failure_codes).difference(
                {
                    "not_construct_discriminating",
                    "multiple_response_tasks",
                    "unsupported_extension",
                }
            )
            non_answer_failures = gap_failure_codes.difference(answer_completeness_codes)
            if non_answer_failures:
                continue
''','''        if review.route_id in candidate_by_route or review.route_id not in recovered_approved:
            continue
''')
replace('    admission_by_candidate = {review.candidate_id: review for review in admission.reviews}\n', '')
# Outcome projection distinguishes route existence, usable wording and unfinished review.
replace('''    failure_counts = Counter(code for review in admission.reviews for code in review.failure_codes)
    calls = []''','''    final_questions = result.get("final_questions", {})
    ready_routes = [route_id for route_id in approved if route_id in final_questions]
    pending = bool(result.get("match_audit_pending", False) or match_audit.unreviewed_route_ids)
    unresolved_audit = bool(match_audit.prior_admission_blocked_route_ids)
    if ready_routes:
        outcome = "clarification_recommended"
    elif approved:
        outcome = "question_generation_failed"
    elif pending:
        outcome = "review_pending"
    elif triage.decision != "review_ready" or unresolved_audit:
        outcome = "no_admitted_candidate"
    else:
        outcome = "review_ready"
    failure_counts = Counter(
        code for review in [*admission.reviews, *match_audit.admission_reviews]
        for code in review.failure_codes
    )
    calls = []''')
replace('''        "match_audit_pending": bool(result.get("match_audit_pending", False)),''','''        "match_audit_pending": pending,''')
replace('''        "shadow_outcome": (
            "clarification_recommended"
            if approved
            else "review_ready"
            if triage.decision == "review_ready"
            else "no_admitted_candidate"
        ),
        "selected_route_id": approved[0] if approved else None,''','''        "shadow_outcome": outcome,
        "selected_route_id": ready_routes[0] if ready_routes else None,
        "ready_question_route_ids": ready_routes,
        "final_review_completed": False,
        "unreviewed_omission_route_ids": list(match_audit.unreviewed_route_ids),
        "prior_admission_blocked_route_ids": list(match_audit.prior_admission_blocked_route_ids),''')
p.write_text(s)
# The replay must not turn blocked/pending outcomes into passing review-ready results.
p=ROOT/'apps/life-patterns-participant/scripts/replay_shadow_validation.py'
s=p.read_text()
old='''            actual_decision = (
                "clarification_needed"
                if row["shadow_outcome"] == "clarification_recommended"
                else "review_ready"
            )'''
new='''            actual_decision = {
                "clarification_recommended": "clarification_needed",
                "review_ready": "review_ready",
            }.get(row["shadow_outcome"], row["shadow_outcome"])
            delivered_routes = row["ready_question_route_ids"]'''
assert s.count(old)==1
s=s.replace(old,new).replace('admitted = set(row["admitted_route_ids"])','admitted = set(delivered_routes)').replace('route_ok = row["admitted_route_ids"] == expected_route_ids','route_ok = delivered_routes == expected_route_ids').replace('target["route_id"] in row["admitted_route_ids"]','target["route_id"] in delivered_routes')
s=s.replace('''                    "admitted_route_ids": row["admitted_route_ids"],''','''                    "admitted_route_ids": row["admitted_route_ids"],
                    "ready_question_route_ids": delivered_routes,''')
p.write_text(s)
print('PRO_REPAIRS_APPLIED')
