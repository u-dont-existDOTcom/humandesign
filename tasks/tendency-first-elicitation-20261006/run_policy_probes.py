"""Three fixed synthetic full-menu probes. No private participant record is read."""
from pathlib import Path
import copy, importlib.util, json, tempfile, sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"apps/life-patterns-participant"))
from participant.domain import load_instrument, new_state, import_record
from participant.question_policy import activate, identity
from participant.shadow_triage import run_shadow_fast_spec_path, privacy_safe_case_summary
spec=importlib.util.spec_from_file_location("policy_probe_worker",ROOT/"apps/life-patterns-participant/scripts/gpt_review_worker.py")
worker=importlib.util.module_from_spec(spec);spec.loader.exec_module(worker)
TASK=Path(__file__).resolve().parent
cases=[
 {"id":"general_answer_already_complete","question":"When sharing work or costs with someone, how do you usually work out an arrangement?", "answer":"I usually ask what contribution each person can comfortably make, explain what I can offer, and adjust the plan together. With family I am more flexible. I do not have one fixed division for every situation.", "route":"TF1-M11", "skipped":False, "expected":"No repeated question about arrangements or meal role-play."},
 {"id":"unresolved_general_reference","question":"When sharing work or costs with someone, how do you usually work out an arrangement?", "answer":"My usual way of arranging it is that same approach I meant earlier.", "route":"TF1-M11", "skipped":False, "expected":"Ask a direct clarification of the usual approach, not the old meal-cost hypothetical."},
 {"id":"legacy_meal_skipped","question":"You and a friend are planning a meal for just the two of you. You offer to organise and cook it, which will take several hours, and ask your friend to buy the ingredients. They say, \"I'd like to do the meal, but paying for all the ingredients feels like too much for me.\" What would you say next?", "answer":None, "route":"M11", "skipped":True, "expected":"No M11, TF1-M11, PREFER-EXCHANGE or TF1-PREFER-EXCHANGE question; do not evade skip."}
]
(TASK/"SEMANTIC-PROBE-INPUTS.json").write_text(json.dumps({"synthetic_only":True,"policy":identity(),"cases":cases},indent=2)+"\n")
provider=worker.CodexCliProvider(timeout_seconds=600)
with tempfile.TemporaryDirectory(prefix="lp-tendency-probe-") as folder:
    instrument=load_instrument(worker.authority_copy(Path(folder)/"authority"))
    with (TASK/"SEMANTIC-PROBE-OUTPUTS.jsonl").open("w") as out:
        for case in cases:
            state=new_state("synthetic", "gpt-5.6-sol", "xhigh");activate(state)
            record={"turns":[{"turn_id":"source-1", "question_text":case["question"],"answer_text":case["answer"],"canonical_question_id":case["route"]}]}
            import_record(state,record,"prior_json",instrument)
            if case["skipped"]:
                state["turns"][0]["answer_status"]="skipped"
                state["dispositions"][state["turns"][0]["turn_id"]]={"turn_id":state["turns"][0]["turn_id"],"status":"skipped","reason":"Explicit synthetic skip"}
            result=run_shadow_fast_spec_path(state,instrument,provider,model="gpt-5.6-sol",effort="xhigh")
            summary=privacy_safe_case_summary(case["id"],state,result)
            value={"case_id":case["id"],"summary":summary,"questions":{k:v.model_dump() for k,v in result["final_questions"].items()}}
            out.write(json.dumps(value,ensure_ascii=False)+"\n");out.flush()
            print(json.dumps({"case_id":case["id"],"outcome":summary.get("shadow_outcome"),"question_routes":list(value["questions"])}),flush=True)
