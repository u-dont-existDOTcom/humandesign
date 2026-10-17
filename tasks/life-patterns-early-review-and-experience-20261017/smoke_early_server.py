"""Local synthetic browser fixture; never use real research records."""

from __future__ import annotations

import argparse
import secrets
import socket
import sys
import tempfile
import threading
import time
from dataclasses import replace
from pathlib import Path

import uvicorn
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "apps/life-patterns-participant"
sys.path[:0] = [str(APP), str(APP / "tests")]

from participant.app import create_app  # noqa: E402
from test_gpt_submission_action import (  # noqa: E402
    auth,
    candidate_record,
    setup_submission,
)
from test_participant import authority  # noqa: E402


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("--url-file", type=Path, required=True)
    cli.add_argument("--mode", choices=["answer", "close", "legacy"], required=True)
    args = cli.parse_args()
    with tempfile.TemporaryDirectory(prefix="life-patterns-early-smoke-") as tmp:
        root = Path(tmp)
        settings, fake, _, _ = setup_submission(root)
        (root / "cf003_secondary_question_module_v0.json").write_bytes(
            (
                ROOT / "reference/empirical_astrology/cf003_secondary_question_module_v0.json"
            ).read_bytes()
        )
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        origin = f"http://127.0.0.1:{port}"
        settings = replace(
            settings,
            public_origin=origin,
            secure_cookies=False,
            fast_review_enabled=True,
        )
        app = create_app(settings, provider=fake, instrument=authority())
        with TestClient(app, base_url=origin) as test:
            review_payload = {
                "candidate_record": candidate_record(),
                "research_use_consented": True,
                "request_id": secrets.token_hex(16),
            }
            if args.mode != "legacy":
                review_payload["review_protocol"] = "fast-batch-v1"
            started = test.post(
                "/api/gpt/reviews",
                headers=auth(settings.submission_token),
                json=review_payload,
            )
            assert started.status_code == 200, started.text
            rid = started.json()["review_id"]
            store = app.state.store
            with store.connection() as db:
                db.execute("BEGIN IMMEDIATE")
                row = db.execute(
                    "SELECT payload FROM gpt_review_jobs WHERE id=?", (rid,)
                ).fetchone()
                job = store.decode(row[0])
                question = {
                    "route_id": "TF1-M11",
                    "clarification_id": "Q-" + secrets.token_hex(16),
                    "route_type": "missing_piece_followup",
                    "question_text": "When do you choose to wait before acting?",
                    "participant_purpose": "An example of review detail",
                    "antecedent_turn_ids": ["t1"],
                }
                job.update(
                    status="clarification_needed",
                    pending_clarification=question,
                    pending_clarifications=[] if args.mode == "legacy" else [question],
                    pending_batch_id=None
                    if args.mode == "legacy"
                    else "B-" + secrets.token_hex(16),
                )
                db.execute(
                    "UPDATE gpt_review_jobs SET payload=?,status=? WHERE id=?",
                    (store.encode(job), "clarification_needed", rid),
                )
                db.commit()
            issued = test.post(
                f"/api/gpt/reviews/{rid}/finish-link", headers=auth(settings.submission_token)
            )
            assert issued.status_code == 200, issued.text
            link = issued.json()["finish_url"]
        args.url_file.write_text(link)
        args.url_file.chmod(0o600)

        def simulated_worker():
            # Browser transport QA only. Full independent reviewer is tested
            # separately; NEVER identify a synthetic ready as real evidence.
            while True:
                state = store.gpt_review_read(rid)
                if state.get("clarification_history") or state.get("clarification_intake_closed"):
                    time.sleep(1.2)
                    with store.connection() as db:
                        db.execute("BEGIN IMMEDIATE")
                        row = db.execute(
                            "SELECT payload FROM gpt_review_jobs WHERE id=?", (rid,)
                        ).fetchone()
                        state = store.decode(row[0])
                        if state["status"] != "queued":
                            db.commit()
                            continue
                        state.update(
                            status="ready",
                            worker_state={
                                "phase": "review",
                                "evidence": [],
                                "fast_review": {"final_review_completed": True},
                                "gpt_review_answers_processed": len(
                                    state.get("clarification_history") or []
                                ),
                            },
                        )
                        db.execute(
                            "UPDATE gpt_review_jobs SET status=?,payload=? WHERE id=?",
                            ("ready", store.encode(state), rid),
                        )
                        db.commit()
                    return
                time.sleep(0.25)

        threading.Thread(target=simulated_worker, daemon=True).start()
        print("EARLY_REVIEW_BROWSER_SYNTHETIC_READY", args.mode, flush=True)
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="error", access_log=False)


if __name__ == "__main__":
    main()
