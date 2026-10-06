"""Private synthetic live review check; never submits a research response.

Uses existing authorized service credentials in memory. Prints only stage metadata.
The synthetic review is withdrawn on completion or failure. No source/credential logs.
"""
from __future__ import annotations

import json
import secrets
import subprocess
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://life-patterns-participant-production.up.railway.app"
PROJECT = "97658d58-84ab-40c8-ab1d-1be06600c4b5"
SERVICE = "30746eb8-07c9-42e7-8825-152124b9337d"
ENVIRONMENT = "b9916074-da51-46a1-8d7d-fd618b3c3d2a"
DEST = Path(__file__).with_name("LIVE-TENDENCY-CANARY.json")


def main() -> int:
    variables = json.loads(subprocess.check_output([
        "railway", "variables", "--project", PROJECT, "--service", SERVICE,
        "--environment", ENVIRONMENT, "--json"], stderr=subprocess.DEVNULL))
    token = variables["PARTICIPANT_GPT_SUBMISSION_TOKEN"]
    del variables

    def request(method, path, body=None):
        raw = json.dumps(body).encode() if body is not None else None
        req = Request(BASE+path, data=raw, method=method, headers={
            "Authorization": "Bearer "+token, "Content-Type": "application/json"})
        try:
            with urlopen(req, timeout=30) as response:
                return json.load(response)
        except HTTPError as exc:
            # Do not echo request bodies, IDs or provider error messages.
            raise RuntimeError(f"HTTP_{exc.code}") from None

    policy = json.loads((ROOT/"apps/life-patterns-participant/participant/static/tendency-first-v1.json").read_text())
    original = json.loads((ROOT/"tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json").read_text())["questions"]
    selected = policy["questions"] + [row for row in original if row["id"] not in policy["retired_from_new_elicitation"] and row.get("kind") != "optional_retrospective"]
    source = {
        "schema": "life-patterns-full-survey-participant-export-v2",
        "collection_mode": "chatgpt_text", "retrospective_questions_welcome": False,
        "consent": {"research_use_consented": True},
        "evidence_authority": "synthetic_release_canary_not_participant",
        "turns": [
            {"turn_id": "synthetic-"+row["id"], "question_text": row["question"],
             "answer_text": ("My usual way of arranging it is that same approach I meant earlier."
                 if row["id"] == "TF1-M11" else
                 "I cannot give an answer to this question. Please leave it unknown rather than repeat it."),
             "canonical_question_id": row["id"], "turn_role": "behavioral"}
            for row in selected
        ],
        "participant_review": {"summary_shown": False},
        "freeze": {"record_state": "candidate", "frozen_before_birth_or_chart_reveal": False,
                   "birth_or_chart_data_in_this_export": False},
    }
    report = {"synthetic_only": True, "final_submission_attempted": False,
              "synthetic_source_turn_count": len(source["turns"]), "observations": []}
    rid = None
    start = time.monotonic()
    try:
        state = request("POST", "/api/gpt/reviews", {
            "research_use_consented": True, "request_id": secrets.token_hex(16),
            "review_protocol": "fast-batch-v1", "candidate_record": source})
        rid = state["review_id"]
        seen = None
        batches = 0
        while time.monotonic()-start < 900:
            sig = state["status"], state.get("review_stage")
            if sig != seen:
                observation = {"elapsed_seconds": round(time.monotonic()-start, 2),
                               "status": sig[0], "stage": sig[1],
                               "range": state.get("estimated_stage_seconds"),
                               "check_after_seconds": state.get("recommended_check_after_seconds"),
                               "guidance_present": bool(state.get("wait_guidance"))}
                report["observations"].append(observation)
                print(json.dumps(observation), flush=True)
                DEST.write_text(json.dumps(report, indent=2)+'\n')
                seen = sig
            if state["status"] == "ready":
                assert state.get("final_review_completed") is True
                assert isinstance(state.get("review_summary"), list)
                report.update(review_reached_ready=True, batch_rounds=batches,
                              elapsed_seconds=round(time.monotonic()-start, 2))
                break
            if state["status"] == "clarification_needed":
                if batches >= 1:
                    raise RuntimeError("canary_test_round_budget_not_participant_cap")
                questions = state.get("clarifications") or [state["clarification"]]
                report.setdefault("batch_question_counts", []).append(len(questions))
                report.setdefault("synthetic_batch_routes", []).append([q["route_id"] for q in questions])
                report.setdefault("synthetic_question_texts", []).append([q["question_text"] for q in questions])
                if any(q["route_id"] != "TF1-M11" or "meal for just the two" in q["question_text"] for q in questions):
                    raise RuntimeError("canary_wrong_new_question_policy")
                # An explicit automated skip exercises the real exact-answer transport
                # without inventing additional autobiographical evidence.
                answers = [{"clarification_id": q["clarification_id"], "answer_text": "", "skipped": True}
                           for q in questions]
                if state.get("batch_id"):
                    body = {"batch_id": state["batch_id"], "operation_id": secrets.token_hex(16), "answers": answers}
                    state = request("POST", f"/api/gpt/reviews/{rid}/clarification-batches", body)
                else:
                    state = request("POST", f"/api/gpt/reviews/{rid}/clarifications", dict(answers[0], operation_id=secrets.token_hex(16)))
                batches += 1
                continue
            if state["status"] not in {"queued", "processing"}:
                raise RuntimeError("unexpected_review_state_"+state["status"])
            time.sleep(10)
            state = request("GET", f"/api/gpt/reviews/{rid}")
        else:
            raise RuntimeError("canary_test_window_exhausted")
    except Exception as exc:
        report.update(review_reached_ready=False, error_type=type(exc).__name__)
        # Only controlled error classes/codes, never source/model strings.
        if isinstance(exc, RuntimeError) and str(exc).startswith(("HTTP_", "canary_", "unexpected_review_state_")):
            report["error_code"] = str(exc)
    finally:
        if rid:
            try:
                result = request("POST", f"/api/gpt/reviews/{rid}/control", {
                    "action": "withdraw", "operation_id": secrets.token_hex(16)})
                report["synthetic_review_withdrawn"] = result["status"] == "withdrawn"
            except Exception:
                report["synthetic_review_withdrawn"] = False
        DEST.write_text(json.dumps(report, indent=2)+'\n')
    return 0 if (report.get("review_reached_ready") and report.get("synthetic_review_withdrawn")
                 and report.get("batch_rounds", 0) >= 1) else 1


if __name__ == "__main__":
    raise SystemExit(main())
