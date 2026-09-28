"""Synthetic-only UI proof: heartbeat, elapsed, offline staleness, 402 and admin recovery."""

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

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--browser", required=True)
parser.add_argument("--output", type=pathlib.Path, required=True)
args = parser.parse_args()
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=True)
app_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(app_root))
sys.path.insert(0, str(app_root / "tests"))
from participant.app import Settings, create_app
from participant.engine import ProviderError
from test_participant import Fake, authority


class ControlledFake(Fake):
    def __init__(self):
        super().__init__()
        self.release = threading.Event()
        self.requests = 0
        self.payment = True

    def call(self, *args, **kwargs):
        self.requests += 1
        if not self.release.wait(50):
            raise ProviderError("synthetic_test_deadline")
        if self.payment:
            raise ProviderError("provider_http_402")
        return super().call(*args, **kwargs)


with tempfile.TemporaryDirectory() as temporary:
    cfg = Settings(
        database=pathlib.Path(temporary) / "study.db",
        encryption_key=Fernet.generate_key().decode(),
        admin_token=secrets.token_urlsafe(32),
        join_token=secrets.token_urlsafe(32),
        authority=pathlib.Path(temporary),
        secure_cookies=False,
        live_enabled=True,
    )
    fake = ControlledFake()
    app = create_app(cfg, provider=fake, instrument=authority())
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="error", access_log=False))
    thread = threading.Thread(target=lambda: server.run(sockets=[sock]), daemon=True)
    thread.start()
    while not server.started:
        time.sleep(0.05)
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=True, executable_path=args.browser, args=["--disable-gpu"]
            )
            page = browser.new_page(viewport={"width": 390, "height": 844})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(f"http://127.0.0.1:{port}/#join={cfg.join_token}")
            page.locator("#agree").click()
            page.locator("#question-panel").wait_for(state="visible", timeout=10000)
            resume = page.url
            page.locator("#answer").fill("I would use the hour to read alone.")
            page.locator("#send").click()
            page.locator("#processing-panel").wait_for(state="visible", timeout=10000)
            page.wait_for_timeout(1500)
            first = page.locator("#elapsed-time").inner_text()
            page.wait_for_timeout(2300)
            second = page.locator("#elapsed-time").inner_text()
            assert first != second and "awaiting" not in second
            assert page.locator("#processing-meter").get_attribute("value") is None
            assert "Server connected" in page.locator("#heartbeat-text").inner_text()
            assert page.locator("#heartbeat-dot").get_attribute("class") == "live"
            page.screenshot(path=str(out / "heartbeat-live-mobile.png"), full_page=True)
            page.route("**/api/session", lambda route: route.abort())
            page.wait_for_timeout(13500)
            assert "Connection delayed" in page.locator("#heartbeat-text").inner_text()
            assert page.locator("#heartbeat-dot").get_attribute("class") == "stale"
            assert not page.locator("#processing-meter").is_visible()
            page.screenshot(path=str(out / "heartbeat-stale-mobile.png"), full_page=True)
            page.unroute("**/api/session")
            page.locator("#check-status").click()
            page.wait_for_timeout(500)
            assert "Server connected" in page.locator("#heartbeat-text").inner_text()
            fake.release.set()
            page.locator("#provider-blocked").wait_for(state="visible", timeout=10000)
            assert "needs credit" in page.locator("#provider-title").inner_text()
            assert not page.locator("#processing-panel").is_visible()
            assert not page.locator("#retry").is_visible()
            requests = fake.requests
            page.wait_for_timeout(4000)
            page.reload()
            page.locator("#provider-blocked").wait_for(state="visible", timeout=10000)
            assert fake.requests == requests
            page.screenshot(path=str(out / "payment-blocked-mobile.png"), full_page=True)
            page.goto(f"http://127.0.0.1:{port}/admin#key={cfg.admin_token}")
            retry = page.get_by_role("button", name="Allow retry after fixing Venice API credit")
            retry.wait_for(state="visible", timeout=10000)
            fake.payment = False
            page.once("dialog", lambda dialog: dialog.accept())
            retry.click()
            page.wait_for_timeout(400)
            page.goto(resume)
            page.locator("#question").filter(has_text="[route: G02]").wait_for(
                state="visible", timeout=15000
            )
            assert not page.locator("#provider-blocked").is_visible()
            assert not errors, errors
            assert page.locator("html").evaluate("(e)=>e.scrollWidth<=window.innerWidth")
            browser.close()
            receipt = {
                "ok": True,
                "provider": "synthetic_fake_only",
                "paid_inference": False,
                "elapsed_advances": True,
                "percentage_not_fabricated": True,
                "server_staleness_detected": True,
                "worker_heartbeat_visible": True,
                "payment_stops_progress": True,
                "no_automatic_payment_retry": True,
                "admin_recovery_and_same_session_resume": True,
                "javascript_errors": errors,
            }
            (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
            print(json.dumps(receipt))
    finally:
        fake.release.set()
        server.should_exit = True
        thread.join(5)
        sock.close()
