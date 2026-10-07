"""Exercise real storage with clearly synthetic fixtures, never human records.

NON_UNIVERSAL / EXAMPLE_OWNER_DEPLOYMENT: uses the existing authorized
Life Patterns pilot deployment. Runtime credentials never enter the report.
"""

import copy
import hashlib
import json
import os
import secrets
import subprocess
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
DEST = Path(__file__).with_name("LIVE-SUBMISSION-CANARY.json")
PRIVATE = Path.home() / ".local/state/life-patterns-closeout-canary-20261007"
BASE = "https://life-patterns-participant-production.up.railway.app"


def main():
    os.umask(0o077)
    PRIVATE.mkdir(parents=True, exist_ok=True)
    v = json.loads(
        subprocess.check_output(
            [
                "railway",
                "variables",
                "--project",
                "97658d58-84ab-40c8-ab1d-1be06600c4b5",
                "--service",
                "30746eb8-07c9-42e7-8825-152124b9337d",
                "--environment",
                "b9916074-da51-46a1-8d7d-fd618b3c3d2a",
                "--json",
            ],
            stderr=subprocess.DEVNULL,
        )
    )
    client = httpx.Client()
    client.headers["Authorization"] = "Bearer " + v["PARTICIPANT_GPT_SUBMISSION_TOKEN"]
    del v
    report = {"synthetic_only": True, "human_record_modified": False, "events": []}

    def req(method, path, body=None):
        r = client.request(method, BASE + path, json=body, timeout=35)
        if r.status_code >= 400:
            raise RuntimeError("HTTP_" + str(r.status_code))
        return r.json()

    def save():
        DEST.write_text(json.dumps(report, indent=2) + "\n")

    f = PRIVATE / "handoff.json"
    if f.exists():
        envelope = json.loads(f.read_text())
    else:
        policy = json.loads(
            (
                ROOT / "apps/life-patterns-participant/participant/static/tendency-first-v1.json"
            ).read_text()
        )
        bank = json.loads(
            (
                ROOT / "tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json"
            ).read_text()
        )["questions"]
        selected = policy["questions"] + [
            r for r in bank if r["id"] not in policy["retired_from_new_elicitation"]
        ]
        source = {
            "schema": "life-patterns-full-survey-participant-export-v2",
            "collection_mode": "chatgpt_text",
            "retrospective_questions_welcome": False,
            "synthetic_release_test": True,
            "evidence_authority": "synthetic_release_canary_not_participant",
            "consent": {"research_use_consented": True},
            "turns": [],
            "participant_review": {"summary_shown": False},
            "freeze": {
                "record_state": "candidate",
                "frozen_before_birth_or_chart_reveal": False,
                "birth_or_chart_data_in_this_export": False,
            },
        }
        for r in selected:
            source["turns"].append(
                {
                    "turn_id": "synthetic-" + r["id"],
                    "canonical_question_id": r["id"],
                    "question_text": r["question"],
                    "answer_text": "I prefer meeting people through small shared activities."
                    if r["id"] == "G07"
                    else None,
                    "answer_status": "answered" if r["id"] == "G07" else "skipped",
                    "turn_role": "behavioral",
                }
            )
        envelope = {
            "request_id": secrets.token_hex(16),
            "research_use_consented": True,
            "review_protocol": "fast-batch-v1",
            "candidate_record": source,
        }
        f.write_text(json.dumps(envelope))
    state = req("POST", "/api/gpt/reviews", envelope)
    rid = state["review_id"]
    (PRIVATE / "review.json").write_text(json.dumps(state))
    start = time.monotonic()
    last = None
    try:
        while time.monotonic() - start < 900:
            sig = (state["status"], state.get("review_stage"))
            if sig != last:
                e = {
                    "status": sig[0],
                    "stage": sig[1],
                    "elapsed_seconds": round(time.monotonic() - start, 1),
                }
                report["events"].append(e)
                print(json.dumps(e), flush=True)
                save()
                last = sig
            if state["status"] == "ready":
                break
            if state["status"] not in ("queued", "processing"):
                raise RuntimeError("unexpected_" + state["status"])
            time.sleep(10)
            state = req("GET", "/api/gpt/reviews/" + rid)
        else:
            raise RuntimeError("bounded_window_expired")
        report["full_review_ready"] = state.get("final_review_completed") is True
        primary = copy.deepcopy(envelope["candidate_record"])
        primary["participant_review"] = {
            "summary_shown": True,
            "confirmed": True,
            "basis": "automated_synthetic_fixture_check_not_human",
        }
        primary["freeze"] = {
            "record_state": "final",
            "frozen_before_birth_or_chart_reveal": True,
            "birth_or_chart_data_in_this_export": False,
        }
        module = json.loads(
            (
                ROOT / "reference/empirical_astrology/cf003_secondary_question_module_v0.json"
            ).read_text()
        )
        secondary = {
            "schema_version": "life-patterns-cf003-secondary-v0",
            "synthetic_release_test": True,
            "turns": [
                {
                    "question_id": r["question_id"],
                    "question_text": r["question"],
                    "answer_text": "Synthetic fixture, not a human research answer.",
                    "turn_role": "behavioral",
                }
                for r in module["questions"]
            ],
        }
        wire = {
            "research_use_consented": True,
            "review_id": rid,
            "primary_record_json": json.dumps(primary, ensure_ascii=False),
            "cf003_record_json": json.dumps(secondary, ensure_ascii=False),
        }
        (PRIVATE / "submission.json").write_text(json.dumps(wire))
        bad = client.post(
            BASE + "/api/gpt/reviewed-submissions",
            json=dict(wire, primary_record_json="{not-json"),
            timeout=35,
        )
        report["malformed_rejected_before_storage"] = (
            bad.status_code == 422 and bad.json().get("request_accepted") is False
        )
        receipt = req("POST", "/api/gpt/reviewed-submissions", wire)
        (PRIVATE / "receipt.json").write_text(json.dumps(receipt))
        repeated = req("POST", "/api/gpt/reviewed-submissions", wire)
        report["stored_encrypted"] = receipt.get("stored_encrypted") is True
        report["receipt_has_submission_id"] = bool(receipt.get("submission_id"))
        report["exact_retry_idempotent"] = repeated.get("duplicate") is True and repeated.get(
            "submission_id"
        ) == receipt.get("submission_id")
        report["primary_hash_matches"] = (
            receipt["primary_record_sha256"]
            == hashlib.sha256(
                json.dumps(
                    primary, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                ).encode()
            ).hexdigest()
        )
        report["synthetic_record_retained_and_marked"] = True
        report["success"] = all(
            report[k]
            for k in [
                "full_review_ready",
                "malformed_rejected_before_storage",
                "stored_encrypted",
                "receipt_has_submission_id",
                "exact_retry_idempotent",
                "primary_hash_matches",
            ]
        )
    except Exception as exc:
        report["success"] = False
        report["error_type"] = type(exc).__name__
        if isinstance(exc, RuntimeError):
            report["error_code"] = str(exc)
    save()
    print(json.dumps(report), flush=True)
    return 0 if report.get("success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
