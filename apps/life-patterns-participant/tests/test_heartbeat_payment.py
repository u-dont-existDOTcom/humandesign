"""No paid inference: real endpoints/store with synthetic liveness and payment failures."""

import io
import json
import threading
import time
import urllib.error

import pytest
from participant.domain import Admission
from participant.engine import PAYMENT_ERROR, ProviderError, Venice
from participant.store import Conflict
from test_participant import begin, command, wait_phase
from test_participant import setup as participant_fixture

setup = participant_fixture


def payment_failure(*args, **kwargs):
    raise ProviderError(PAYMENT_ERROR)


def fail_after_answer(setup):
    _, fake, _, client = setup
    state = begin(setup)
    state = command(
        client, state, "answer", "I keep that hour free unless a friend needs help."
    ).json()
    fake.call = payment_failure
    state = client.post("/api/next", json={}).json()
    if state["phase"] == "planning":
        state = wait_phase(client, {"provider_blocked"})
    return state


def test_402_is_terminal_saved_partial_and_never_automatically_retried(setup):
    _, fake, app, c = setup
    state = fail_after_answer(setup)
    assert state["phase"] == "provider_blocked"
    assert state["provider_issue"]["code"] == "payment_required"
    assert state["provider_issue"]["automatic_retry"] is False
    assert "provider_http_402" not in state["error"]
    assert state["processing"] is None
    calls = []
    fake.call = lambda *a, **k: calls.append(1)
    for _ in range(3):
        assert c.get("/api/session").json()["phase"] == "provider_blocked"
        assert c.post("/api/next", json={}).json()["phase"] == "provider_blocked"
    assert calls == []
    record = c.get("/api/export").json()
    assert record["interview_status"] == "partial"
    assert record["stop_reason"] == "provider_payment_required"
    assert record["turns"][0]["answer_text"].startswith("I keep that hour")
    assert app.state.store.read(c.cookies.get("lp_session"))["lease"] is None


def test_legacy_402_migrates_without_inference_and_resume_preserves_block(setup):
    _, fake, app, c = setup
    state = begin(setup)

    def legacy(s):
        s["phase"], s["error"] = "error", PAYMENT_ERROR

    app.state.store.change(c.cookies.get("lp_session"), legacy)
    state = c.get("/api/session").json()
    assert state["phase"] == "provider_blocked" and fake.count == 0
    state = command(c, state, "pause").json()
    state = command(c, state, "resume").json()
    assert state["phase"] == "provider_blocked"
    assert c.post("/api/next", json={}).json()["phase"] == "provider_blocked"
    state = command(c, state, "stop").json()
    assert state["phase"] == "stopped"
    with pytest.raises(Conflict):
        app.state.engine.advance(c.cookies.get("lp_session"))
    assert c.get("/api/session").json()["phase"] == "stopped"


def test_only_researcher_can_acknowledge_billing_recovery_no_inference(setup):
    cfg, fake, _, c = setup
    state = fail_after_answer(setup)
    path = f"/api/admin/sessions/{state['session_id']}/resume-provider"
    assert c.post(path, json={"billing_issue_resolved": True}).status_code == 401
    headers = {"Authorization": "Bearer " + cfg.admin_token}
    assert c.post(path, headers=headers, json={"billing_issue_resolved": False}).status_code == 422
    requests = []
    fake.call = lambda *a, **k: requests.append(1)
    response = c.post(path, headers=headers, json={"billing_issue_resolved": True})
    assert response.status_code == 200 and response.json()["inference_started"] is False
    assert c.get("/api/session").json()["phase"] == "ready"
    assert requests == []
    assert c.post(path, headers=headers, json={"billing_issue_resolved": True}).status_code == 409


def test_worker_heartbeat_and_total_start_survive_slow_provider_then_stop(setup):
    _, fake, app, c = setup
    state = begin(setup)
    state = command(c, state, "answer", "I keep the time for reading.").json()
    fake.block = threading.Event()
    fake.called = threading.Event()
    try:
        state = c.post("/api/next", json={}).json()
        assert fake.called.wait(1)
        first = state["processing"]
        assert first["started_at"] and first["stage_started_at"]
        deadline = time.monotonic() + 7
        while time.monotonic() < deadline:
            current = c.get("/api/session").json()
            if current["processing"]["worker_heartbeat_at"] != first["worker_heartbeat_at"]:
                break
            time.sleep(0.1)
        else:
            raise AssertionError("worker heartbeat did not advance")
        assert current["processing"]["started_at"] == first["started_at"]
        assert current["processing"]["attempt"] == 1
        assert current["server_time"] != state["server_time"]
        stopped = command(c, current, "stop").json()
        assert stopped["processing"] is None
        frozen = c.get("/api/export").content
    finally:
        fake.block.set()
    time.sleep(0.1)
    assert c.get("/api/session").json()["phase"] == "stopped"
    assert c.get("/api/export").content == frozen


def test_stage_transition_preserves_elapsed_and_marks_revision_pass(setup):
    _, fake, _, c = setup
    state = begin(setup)
    state = command(c, state, "answer", "I would read alone.").json()
    original = fake.call
    snapshots = []
    rejects = [True]

    def observed(system, payload, schema, model, effort):
        snapshots.append(c.get("/api/session").json()["processing"])
        result, meta = original(system, payload, schema, model, effort)
        if schema is Admission and rejects:
            rejects.pop()
            result.approved = False
            result.errors = ["synthetic repair required"]
        return result, meta

    fake.call = observed
    state = c.post("/api/next", json={}).json()
    if state["phase"] == "planning":
        state = wait_phase(c, {"awaiting_answer", "error"})
    assert state["phase"] == "awaiting_answer"
    assert [x["stage"] for x in snapshots] == ["planner", "admission", "planner", "admission"]
    assert [x["attempt"] for x in snapshots] == [1, 1, 2, 2]
    assert len({x["started_at"] for x in snapshots}) == 1


def test_stream_activity_is_metadata_only_and_402_body_is_not_exposed():
    class Stream(io.BytesIO):
        def __init__(self):
            answer = {
                "approved": True,
                "errors": [],
                "context_supported": True,
                "no_redundant_question": True,
                "no_unsupported_extension": True,
                "control_is_participant_request": False,
            }
            super().__init__(
                (
                    "data: "
                    + json.dumps(
                        {
                            "model": "openai-gpt-56-sol",
                            "choices": [
                                {"delta": {"content": json.dumps(answer)}, "finish_reason": "stop"}
                            ],
                        }
                    )
                    + "\n\ndata: [DONE]\n\n"
                ).encode()
            )
            self.headers = {"content-type": "text/event-stream"}

    class Opener:
        def open(self, *a, **kw):
            return Stream()

    client = Venice("https://venice-model-gateway-production.up.railway.app/v1", "synthetic")
    client.opener = Opener()
    events = []
    answer, _ = client.call(
        "SYNTHETIC PRIVATE PROMPT",
        {},
        Admission,
        "openai-gpt-56-sol",
        "xhigh",
        on_activity=events.append,
    )
    assert answer.approved and events and events[-1]["stream_events_received"] >= 1
    assert all(set(e) == {"model_activity_at", "stream_events_received"} for e in events)

    class Reject:
        def open(self, *a, **kw):
            raise urllib.error.HTTPError(
                "https://example.test", 402, "payment required", {}, io.BytesIO(b"PRIVATE_SECRET")
            )

    client.opener = Reject()
    with pytest.raises(ProviderError, match="^provider_http_402$"):
        client.call(
            "private", {}, Admission, "openai-gpt-56-sol", "xhigh", on_activity=events.append
        )
