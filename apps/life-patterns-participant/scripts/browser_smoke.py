import argparse
import json
import pathlib
import secrets
import socket
import sys
import tempfile
import threading
import time

import uvicorn
from cryptography.fernet import Fernet
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(
    description="Headless synthetic-only participant UI test; no provider credentials used."
)
parser.add_argument("--output", type=pathlib.Path, required=True)
parser.add_argument("--browser", type=str, required=True)
args = parser.parse_args()
r = args.output.resolve()
r.mkdir(parents=True, exist_ok=True)
app_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(app_root))
sys.path.insert(0, str(app_root / "tests"))
from participant.app import Settings, create_app
from test_participant import Fake, authority


class SlowFake(Fake):
    def call(self, system, payload, schema, model, effort):
        time.sleep(1.2)
        return super().call(system, payload, schema, model, effort)


with tempfile.TemporaryDirectory() as folder:
    config = Settings(
        database=pathlib.Path(folder) / "study.db",
        encryption_key=Fernet.generate_key().decode(),
        admin_token=secrets.token_urlsafe(32),
        join_token=secrets.token_urlsafe(32),
        authority=pathlib.Path(folder),
        secure_cookies=False,
        live_enabled=True,
    )
    fake = SlowFake()
    app = create_app(config, provider=fake, instrument=authority())
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="error", access_log=False))
    thread = threading.Thread(target=lambda: server.run(sockets=[sock]), daemon=True)
    thread.start()
    for _ in range(100):
        if server.started:
            break
        time.sleep(0.05)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True, executable_path=args.browser, args=["--disable-gpu"]
            )
            page = browser.new_page(viewport={"width": 390, "height": 844})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(f"http://127.0.0.1:{port}/#join={config.join_token}")
            page.locator("#agree").wait_for(state="visible")
            assert page.locator("#retrospective-ok").is_checked() is False
            page.locator("#agree").click()
            page.locator("#question-panel").wait_for(state="visible", timeout=15000)
            assert "[route: A0]" in page.locator("#question").inner_text()
            page.screenshot(path=str(r / "browser-first-question.png"), full_page=True)
            page.locator("#answer").fill("I sort messages by travel, cost and time.")
            page.locator("#send").click()
            page.locator("#status").filter(has_text="semantic pass").wait_for(
                state="visible", timeout=10000
            )
            page.locator("#question").filter(has_text="[route: G23]").wait_for(
                state="visible", timeout=15000
            )
            fake.review = True
            page.locator("#answer").fill("I explain one point at a time.")
            page.locator("#send").click()
            page.locator("#review-panel").wait_for(state="visible", timeout=15000)
            page.wait_for_timeout(400)
            page.locator("#confirm").click()
            page.locator("#done").wait_for(state="visible", timeout=10000)
            with page.expect_download() as download:
                page.locator("#done a").click()
            download.value.save_as(str(r / "browser-synthetic-export.json"))
            data = json.loads((r / "browser-synthetic-export.json").read_text())
            assert len(data["turns"]) == 2 and data["interview_status"] == "complete"
            assert data["participant_review"]["confirmed"] is True
            assert data["collection_preferences"]["retrospective_questions_welcome"] is False
            assert data["turns"][0]["answer_text"] == "I sort messages by travel, cost and time."
            page.reload()
            page.locator("#done").wait_for(state="visible", timeout=10000)
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            page.screenshot(path=str(r / "browser-completed-mobile.png"), full_page=True)
            page.goto(f"http://127.0.0.1:{port}/admin#key={config.admin_token}")
            page.locator("#status").filter(has_text="Session list loaded").wait_for(
                state="visible", timeout=10000
            )
            assert page.url.endswith("/admin")
            page.reload()
            page.locator("#status").filter(has_text="Session list loaded").wait_for(
                state="visible", timeout=10000
            )
            assert not errors, errors
            browser.close()
            receipt = {
                "ok": True,
                "actual_provider": "synthetic_mock_only",
                "mobile_viewport": [390, 844],
                "consent_question_answer_review_export_reload": "pass",
                "javascript_errors": errors,
                "export_turns": 2,
                "horizontal_overflow": False,
                "venice_live_test": False,
            }
            (r / "browser-receipt.json").write_text(json.dumps(receipt, indent=2))
            print(json.dumps(receipt))
    finally:
        server.should_exit = True
        thread.join(5)
        sock.close()
