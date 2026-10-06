"""Finish narrowly scoped release fixes identified at the adapter boundary."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
assert subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip() == '764ff0fa547975b1fb014aeb0732f956eccd4535'
lease = json.loads(Path(__file__).with_name('WRITER-LEASE.json').read_text())
assert lease['status'] == 'active' and lease['owned_branch'] == 'release/fast-review-guidance-20261005'
app = ROOT / 'apps/life-patterns-participant'
p = app / 'participant/shadow_triage.py'
s = p.read_text()
old = '''    addressed = set(state.get("addressed_routes", {}))
    retrospective_ok = (
'''
new = '''    addressed = set(state.get("addressed_routes", {}))
    # An explicit skip is not an unanswered gap to pursue again. Keep its source
    # in the record, but do not re-offer that route during this review.
    skipped_routes = {
        str(turn["canonical_question_id"])
        for turn in turns
        if turn.get("canonical_question_id") and turn.get("answer_status") == "skipped"
    }
    retrospective_ok = (
'''
assert s.count(old) == 1
s = s.replace(old, new).replace('        if route_id in addressed:\n', '        if route_id in addressed or route_id in skipped_routes:\n', 1)
p.write_text(s)
p = app / 'participant/inference_context.py'
s = p.read_text()
old = '''        "question_wording_status": turn.get("question_wording_status"),
    }
'''
new = '''        "question_wording_status": turn.get("question_wording_status"),
    }
    if turn.get("answer_status") == "skipped":
        card["answer_status"] = "skipped"
'''
assert s.count(old) == 1
p.write_text(s.replace(old, new))
p = app / 'participant/review_timing.py'
s = p.read_text()
old = '\n\ndef review_guidance(payload: dict, *, now: float | None = None) -> dict:\n'
new = '''

# Do not describe extrapolated integrated-stage ranges as measured quantiles.
ESTIMATE_BASIS = {
    "initial_triage": "limited pilot; two 81-turn first-batch runs around 112-114 seconds",
    "gap_admission": "limited pilot stage timings; broad planning range, not a deadline",
    "question_render": "limited pilot wording-stage timings; retries can take longer",
    "reconciliation": "provisional; informed by legacy follow-up timings, not calibrated batch timings",
    "omission_audit": "provisional; informed by a prior omission-audit run, not a calibrated distribution",
    "final_synthesis": "provisional; informed by legacy full-review timings, not a measured synthesis-only range",
    "final_admission": "provisional; informed by earlier independent-review timings",
    "legacy_review": "limited pilot; prior complete-review observation around eight minutes",
    "legacy_followup": "limited pilot; earlier follow-up observations around one to two minutes",
}


def review_guidance(payload: dict, *, now: float | None = None) -> dict:
'''
assert s.count(old) == 1
s = s.replace(old, new)
s = s.replace('f"Estimated stage duration: {format_range(lower, upper)} from its start. "', 'f"Provisional stage estimate: {format_range(lower, upper)} from its start. "')
s = s.replace('"estimate_basis": "limited_pilot_observations_not_a_guarantee" if waiting else None,', '"estimate_basis": ESTIMATE_BASIS[stage] if waiting else None,')
p.write_text(s)
print('SKIP_AND_ESTIMATE_BOUNDARIES_UPDATED')
