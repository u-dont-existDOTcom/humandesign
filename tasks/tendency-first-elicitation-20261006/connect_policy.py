"""Wire one prospective-question policy through all live review consumers."""
from pathlib import Path
import subprocess, json
ROOT=Path(__file__).resolve().parents[2]
APP=ROOT/'apps/life-patterns-participant'
assert subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()=='52ef9d4349eabd3938e32649f7ad95ede176ed11'
assert json.loads(Path(__file__).with_name('WRITER-LEASE.json').read_text())['status']=='active'
def load(name):return (APP/name).read_text()
def save(name,s):(APP/name).write_text(s)
def replace(s,old,new,count=1):
    assert s.count(old)==count,(old[:120],s.count(old),count)
    return s.replace(old,new)

name='participant/domain.py';s=load(name)
s=replace(s,'def bank(instrument: dict) -> dict:\n    return strict_json(instrument["interviewer-bank-v7.json"])',
'''def bank(instrument: dict, state: dict | None = None) -> dict:
    from .question_policy import view
    return view(strict_json(instrument["interviewer-bank-v7.json"]), state)''')
s=replace(s,'    walk(record)\n    questions = bank(instrument)["questions"]',
'''    walk(record)
    if record.get("question_policy") is not None:
        from .question_policy import active
        state["question_policy"] = copy.deepcopy(record["question_policy"])
        active(state)  # validate identity; do not infer it from a title or participant text
    questions = bank(instrument, state)["questions"]''')
s=s.replace('bank(instrument)["questions"]','bank(instrument, state)["questions"]')
s=replace(s,'        route = routes[q.route_id]\n        if q.route_type',
'''        route = routes[q.route_id]
        from .question_policy import selectable
        if not selectable(route, state):
            raise ValueError("This retired or skipped route is not available for new elicitation.")
        if q.route_type''')
s=replace(s,'        "schema": "life-patterns-full-survey-participant-export-v2",',
'''        "schema": "life-patterns-full-survey-participant-export-v2",
        **({"question_policy": copy.deepcopy(state["question_policy"])}
           if state.get("question_policy") else {}),''')
save(name,s)

name='participant/inference_context.py';s=load(name)
s=s.replace('bank(instrument)["questions"]','bank(instrument, state)["questions"]')
s=replace(s,'def full_route_cards(instrument: dict, route_ids: Iterable[str]) -> list[dict]:',
'''def full_route_cards(
    instrument: dict, route_ids: Iterable[str], state: dict | None = None
) -> list[dict]:''')
s=s.replace('full_route_cards(instrument, route_ids)','full_route_cards(instrument, route_ids, state)')
s=s.replace('full_route_cards(instrument, full_question_ids)','full_route_cards(instrument, full_question_ids, state)')
s=replace(s,'        if route_id in presented or route_id in addressed:',
'''        from .question_policy import selectable
        if not selectable(route, state):
            continue
        if route_id in presented or route_id in addressed:''')
s=replace(s,'    if bulk_import:\n        retrospective_ok = (',
'''    from .question_policy import selectable
    if bulk_import:
        retrospective_ok = (''')
s=replace(s,'            if route["id"] not in already_presented',
'''            if selectable(route, state)
            and route["id"] not in already_presented''')
s=replace(s,'        if not route:\n            continue\n',
'''        if not route or not selectable(route, state):
            continue
''')
save(name,s)

name='participant/shadow_triage.py';s=load(name)
s=s.replace('bank(instrument)["questions"]','bank(instrument, state)["questions"]')
s=replace(s,'    for route in all_routes:\n        route_id = str(route["id"])',
'''    from .question_policy import selectable
    for route in all_routes:
        if not selectable(route, state):
            continue
        route_id = str(route["id"])''')
# The live fast path and all its nested admission/render/recovery calls use the
# same wrapper. The old development path remains reproducible without activation.
start=s.index('def run_shadow_fast_spec_path(')
pos=s.index('    triage_context = make_gap_spec_triage_context(state, instrument)',start)
s=s[:pos]+'''    from .question_policy import PolicyProvider
    provider = PolicyProvider(provider, state)
'''+s[pos:]
save(name,s)

name='participant/fast_review.py';s=load(name)
s=replace(s,'from .store import canonical, digest','from .store import canonical, digest\nfrom .question_policy import activate')
s=replace(s,'        state = new_state(version, job["model"], job["effort"])',
'''        state = new_state(version, job["model"], job["effort"])
        activate(state)''')
s=replace(s,'    state = copy.deepcopy(prior)','    state = copy.deepcopy(prior)\n    activate(state)')
s=replace(s,'        "instrument_version": version,','        "instrument_version": version,\n        "question_policy": state["question_policy"],')
save(name,s)

name='scripts/gpt_review_worker.py';s=load(name)
s=replace(s,'from participant.engine import Engine','from participant.engine import Engine\nfrom participant.question_policy import activate, PolicyProvider')
s=replace(s,'        state = new_state(instrument_version, job["model"], job["effort"])',
'''        state = new_state(instrument_version, job["model"], job["effort"])
        activate(state)''')
s=replace(s,'    state = json.loads(canonical(prior))','    state = json.loads(canonical(prior))\n    activate(state)')
s=replace(s,'        engine = Engine(store, provider, maximum_calls=12)',
'''        provider = PolicyProvider(provider, state)
        engine = Engine(store, provider, maximum_calls=12)''')
s=replace(s,'            "instrument_version": instrument_version,','            "instrument_version": instrument_version,\n            "question_policy": state["question_policy"],')
save(name,s)

name='participant/engine.py';s=load(name)
s=replace(s,'(q for q in bank(instrument)["questions"] if q["id"] == route_id)',
            '(q for q in bank(instrument, s)["questions"] if q["id"] == route_id)')
s=replace(s,'            first = bank(instrument)["questions"][0]',
'''            from .question_policy import selectable
            first = next(q for q in bank(instrument, state)["questions"] if selectable(q, state))''')
save(name,s)

name='participant/app.py';s=load(name)
s=replace(s,'            routes = {row["id"]: row for row in bank(pinned)["questions"]}',
'''            from .question_policy import selectable
            routes = {row["id"]: row for row in bank(pinned, body.worker_state)["questions"]}''')
s=replace(s,'                if route is None:\n                    raise ValueError("Worker returned an unknown survey route.")',
'''                if route is None:
                    raise ValueError("Worker returned an unknown survey route.")
                if not selectable(route, body.worker_state or {}):
                    raise ValueError("Worker returned a retired or skipped elicitation route.")''')
save(name,s)
print('POLICY_WIRED_SOURCE_STATE_CANDIDATES_ADMISSION_HTTP_AND_FINAL_FALLBACK')
