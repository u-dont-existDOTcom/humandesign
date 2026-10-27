"""Local synthetic browser fixture; never points to a real service or record."""
from __future__ import annotations

import argparse
import json
import tempfile
from dataclasses import replace
from pathlib import Path

import uvicorn
from fastapi.testclient import TestClient
from participant.app import create_app
from test_gpt_submission_action import auth, candidate_record, ready_review, setup_submission
from test_participant import authority

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--port", type=int, default=18765)
    args = parser.parse_args()
    origin = f"http://127.0.0.1:{args.port}"
    with tempfile.TemporaryDirectory(prefix="shared-ui-pilot-") as directory:
        folder = Path(directory)
        settings, fake, _, _ = setup_submission(folder)
        source = ROOT / "reference/empirical_astrology/cf003_secondary_question_module_v0.json"
        (folder / source.name).write_bytes(source.read_bytes())
        settings = replace(settings, public_origin=origin, secure_cookies=False)
        app = create_app(settings, provider=fake, instrument=authority())
        client = TestClient(app, base_url=origin)
        links = []
        for index in range(4):
            candidate = candidate_record()
            candidate["turns"][0]["answer_text"] = f"I wait and think. Synthetic source {index}."
            rid = ready_review(client, settings, candidate)
            link = client.post(
                f"/api/gpt/reviews/{rid}/finish-link", headers=auth(settings.submission_token)
            )
            assert link.status_code == 200, link.text
            links.append(link.json()["finish_url"])
        args.fixture.write_text(json.dumps({"origin": origin, "links": links}))
        print("Synthetic browser fixture ready on loopback.", flush=True)
        uvicorn.run(app, host="127.0.0.1", port=args.port, access_log=False, log_level="warning")


if __name__ == "__main__":
    main()
