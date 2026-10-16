"""Serve a complete *synthetic only* ready review for browser QA on localhost."""

from __future__ import annotations

import argparse
import socket
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

import uvicorn
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "apps/life-patterns-participant"
sys.path.insert(0, str(APP))
sys.path.insert(0, str(APP / "tests"))

from participant.app import create_app  # noqa: E402
from test_gpt_submission_action import (  # noqa: E402
    auth,
    candidate_record,
    ready_review,
    setup_submission,
)
from test_participant import authority  # noqa: E402


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("--url-file", type=Path, required=True)
    args = cli.parse_args()
    with tempfile.TemporaryDirectory(prefix="lp-finish-synthetic-") as directory:
        root = Path(directory)
        settings, fake, _app, _client = setup_submission(root)
        (root / "cf003_secondary_question_module_v0.json").write_bytes(
            (
                ROOT / "reference/empirical_astrology/cf003_secondary_question_module_v0.json"
            ).read_bytes()
        )
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        origin = f"http://127.0.0.1:{port}"
        settings = replace(settings, public_origin=origin, secure_cookies=False)
        app = create_app(settings, provider=fake, instrument=authority())
        with TestClient(app, base_url=origin) as test:
            rid = ready_review(test, settings, candidate_record())
            with app.state.store.connection() as db:
                db.execute("BEGIN IMMEDIATE")
                row = db.execute(
                    "SELECT payload FROM gpt_review_jobs WHERE id=?", (rid,)
                ).fetchone()
                state = app.state.store.decode(row[0])
                state["worker_state"]["evidence"] = [
                    {
                        "evidence_id": "SYNTHETIC-E1",
                        "observation": "<img src=x onerror=alert('bad')>",
                        "conditions": ["Only when normally rested"],
                        "time_frame": "Ordinary days",
                        "relationship_context": "Unspecified",
                        "source_quotes": [{"turn_id": "t1", "quote": "I wait and think."}],
                        "candidate_facet_ids": [],
                        "supported_scope": "Reflection on decisions",
                        "review_status": "independent_semantic_admission_passed",
                    }
                ]
                db.execute(
                    "UPDATE gpt_review_jobs SET payload=? WHERE id=?",
                    (app.state.store.encode(state), rid),
                )
                db.commit()
            issued = test.post(
                f"/api/gpt/reviews/{rid}/finish-link",
                headers=auth(settings.submission_token),
            )
            assert issued.status_code == 200, issued.text
            url = issued.json()["finish_url"]
        args.url_file.write_text(url)
        args.url_file.chmod(0o600)
        print("SYNTHETIC_FINISH_SERVER_READY", flush=True)
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=port,
            log_level="error",
            access_log=False,
        )


if __name__ == "__main__":
    main()
