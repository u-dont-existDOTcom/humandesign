"""Real HTTP/store/engine tests with deterministic synthetic model responses only."""

import copy
import json
import secrets
import tempfile
import threading
from pathlib import Path

import pytest
from cryptography.fernet import Fernet
from fastapi.testclient import TestClient
from participant.app import Settings, create_app
from participant.domain import (
    Admission,
    Plan,
    Question,
    Quote,
    bank,
    load_instrument,
    new_state,
    strict_json,
    validate_plan,
)
from participant.engine import ProviderError, Venice
from participant.store import Store

ROOT = Path(__file__).resolve().parents[3]
SURVEY = ROOT / "tasks/scenario-survey-v7-redesign-20260922"
CONTROLLER = ROOT / "tasks/full-survey-participant-v2-20260927/INTERVIEW-CONTROLLER-v2.md"


def authority():
    with tempfile.TemporaryDirectory() as folder:
        p = Path(folder)
        for name in (
            "INTERVIEW-PROTOCOL-v6.md",
            "interviewer-bank-v7.json",
            "EVIDENCE-GUIDE-v7.json",
        ):
            (p / name).write_bytes((SURVEY / name).read_bytes())
        (p / CONTROLLER.name).write_bytes(CONTROLLER.read_bytes())
        return load_instrument(p)


class Fake:
    configured = True

    def __init__(self):
        self.count = 0
        self.fail = False
        self.review = False
        self.block = None
        self.called = None

    def call(self, system, payload, schema, model, effort):
        self.count += 1
        if self.called:
            self.called.set()
        if self.block:
            self.block.wait(10)
        if self.fail:
            raise ProviderError("synthetic_failure")
        if schema is Admission:
            return Admission(
                approved=True,
                errors=[],
                context_supported=True,
                no_redundant_question=True,
                no_unsupported_extension=True,
                control_is_participant_request=False,
            ), {"stage": "Admission"}
        pending = payload["pending_turn_ids"]
        turns = {t["turn_id"]: t for t in payload["turns"]}
        evidence = [
            {
                "evidence_id": f"e-{i}",
                "source_quotes": [{"turn_id": i, "quote": turns[i]["answer_text"]}],
                "observation": "Describes their response in this scenario.",
                "evidence_type": "usual_response_self_report",
                "conditions": [],
                "time_frame": "current self-report",
                "relationship_context": "scenario",
                "candidate_facet_ids": ["D01.approach"],
                "supported_scope": "This answer only.",
                "unsupported_extensions": ["No global ability claim."],
            }
            for i in pending
            if turns[i]["answer_text"]
        ]
        q = next(
            q
            for q in payload["canonical_routes"]
            if q["id"] == ("G02" if payload["turns"] else "G01")
        )
        review = self.review or payload["review_only"]
        process = payload["additional_pending_batches"]
        data = {
            "action": "process" if process else "review" if review else "ask",
            "dispositions": [
                {
                    "turn_id": i,
                    "status": "answered",
                    "conditions": [],
                    "process_feedback_quotes": [],
                    "reason": "Synthetic fixture.",
                }
                for i in pending
            ],
            "evidence": evidence,
            "question": None
            if process or review
            else {
                "route_id": q["id"],
                "route_type": "canonical",
                "text": q["question"],
                "antecedent_turn_ids": [],
                "equivalent_context": False,
                "missing_distinction": "Synthetic fixture distinction.",
                "why_useful": "Synthetic fixture.",
            },
            "control_quote": None,
            "reason": "Synthetic test only.",
        }
        return Plan.model_validate(data), {"stage": "Plan"}


@pytest.fixture
def setup(tmp_path):
    config = Settings(
        database=tmp_path / "data.sqlite3",
        encryption_key=Fernet.generate_key().decode(),
        admin_token=secrets.token_urlsafe(32),
        join_token=secrets.token_urlsafe(32),
        authority=tmp_path,
        secure_cookies=False,
        live_enabled=True,
    )
    fake = Fake()
    app = create_app(config, provider=fake, instrument=authority())
    client = TestClient(app)
    return config, fake, app, client


def join(setup):
    config, fake, app, client = setup
    r = client.post("/api/join", json={"token": config.join_token})
    assert r.status_code == 200
    client.headers["X-Life-Patterns-Session"] = r.json()["session_id"]
    return r.json()


def command(client, state, action, text="", target=None, op=None):
    return client.post(
        "/api/operations",
        headers={"X-Life-Patterns-Session": state["session_id"]},
        json={
            "revision": state["revision"],
            "operation_id": op or secrets.token_hex(10),
            "action": action,
            "text": text,
            "target": target,
        },
    )


def begin(setup):
    _, fake, _, client = setup
    s = join(setup)
    s = command(client, s, "consent").json()
    s = client.post("/api/next", json={}).json()
    assert s["phase"] == "awaiting_answer"
    assert "[route: A0]" in s["question"]["text"]
    assert fake.count == 0
    return s


def test_unauthenticated_routes_and_no_config_leaks(setup):
    cfg, fake, app, c = setup
    for path in ["/api/session", "/api/export", "/api/admin/sessions"]:
        assert c.get(path).status_code == 401
    text = c.get("/healthz").text + c.get("/").text
    assert cfg.admin_token not in text and cfg.encryption_key not in text
    assert "venice" in text.lower()
    assert c.get("/docs").status_code == 404


def test_consent_before_inference_and_decline_has_no_export(setup):
    _, fake, _, c = setup
    s = join(setup)
    assert c.post("/api/next", json={}).status_code == 409
    assert fake.count == 0
    s = command(c, s, "decline").json()
    assert s["phase"] == "declined"
    assert c.get("/api/export").status_code == 403
    assert c.post("/api/next", json={}).status_code == 409


def test_disabled_service_cannot_start_inference(setup):
    cfg, fake, app, _ = setup
    from dataclasses import replace

    c = TestClient(
        create_app(replace(cfg, live_enabled=False), provider=fake, instrument=authority())
    )
    assert c.post("/api/join", json={"token": cfg.join_token}).status_code == 503
    assert c.post("/api/next", json={}).status_code == 503
    assert fake.count == 0


def test_saved_answer_survives_provider_error_and_restart(setup):
    cfg, fake, app, c = setup
    s = begin(setup)
    raw = "  I ask the organiser; it depends on the cost.\nNo global claim.  "
    s = command(c, s, "answer", raw).json()
    fake.fail = True
    assert c.post("/api/next", json={}).json()["phase"] == "error"
    saved = c.get("/api/export").json()
    assert saved["turns"][-1]["answer_text"] == raw
    assert saved["interview_status"] == "partial"
    new_app = create_app(cfg, provider=Fake(), instrument=authority())
    new_client = TestClient(new_app)
    new_client.cookies.update(c.cookies)
    assert new_client.get("/api/session").json()["turns"][-1]["answer_text"] == raw
    assert raw.encode() not in cfg.database.read_bytes()


def test_idempotent_duplicate_and_stale_revision(setup):
    _, fake, _, c = setup
    s = begin(setup)
    op = secrets.token_hex(10)
    first = command(c, s, "answer", "I organise the messages.", op=op)
    second = command(c, s, "answer", "I organise the messages.", op=op)
    assert first.json()["revision"] == second.json()["revision"]
    assert len(second.json()["turns"]) == 1
    assert command(c, s, "answer", "Different text.", op=op).status_code == 409
    assert command(c, s, "answer", "Another response.").status_code == 409


def test_pause_stop_invalidate_inflight_and_frozen_bytes(setup):
    cfg, fake, app, c = setup
    s = begin(setup)
    s = command(c, s, "answer", "I make a list.").json()
    fake.called = threading.Event()
    fake.block = threading.Event()
    token = c.cookies.get("lp_session")
    thread = threading.Thread(target=lambda: app.state.engine.advance(token))
    thread.start()
    assert fake.called.wait(2)
    stopped = command(c, s, "stop").json()  # stale revision must not prevent a stop
    assert stopped["phase"] == "stopped"
    before = c.get("/api/export").content
    fake.block.set()
    thread.join(3)
    assert not thread.is_alive()
    assert c.get("/api/session").json()["phase"] == "stopped"
    assert c.get("/api/export").content == before


def test_skip_is_unknown_not_negative(setup):
    _, fake, _, c = setup
    s = begin(setup)
    s = command(c, s, "skip").json()
    assert s["phase"] == "ready"
    record = c.get("/api/export").json()
    assert record["turns"][-1]["answer_text"] is None
    assert record["turns"][-1]["answer_status"] == "skipped"
    assert record["neutral_evidence"] == []


def test_review_then_confirm_freezes_exact_export(setup):
    _, fake, _, c = setup
    s = begin(setup)
    s = command(c, s, "answer", "I ask whoever booked it.").json()
    fake.review = True
    s = c.post("/api/next", json={}).json()
    assert s["phase"] == "review"
    assert command(c, s, "confirm").status_code == 409
    s = command(c, s, "review_seen").json()
    s = command(c, s, "confirm").json()
    assert s["phase"] == "complete"
    assert c.get("/api/export").content == c.get("/api/export").content
    assert c.get("/api/export").json()["participant_review"]["confirmed"]
    assert command(c, s, "answer", "change").status_code == 409


def test_import_exact_original_metadata_and_no_analyst_prompt(setup):
    cfg, fake, app, c = setup
    join(setup)
    record = {
        "assessment": "ANALYST_ONLY_NOT_FOR_MODEL",
        "turns": [
            {
                "question_text": "Edited question?",
                "answer_text": "  I wait.\n```</script>  ",
                "conditions": ["alone"],
                "corrections": ["old correction"],
                "process_feedback": ["unclear"],
            },
            {"answer_text": None},
            {"answer_text": "Answer-only note."},
        ],
    }
    r = c.post("/api/import", json={"record": record, "source_type": "edited_response_record"})
    assert r.status_code == 200
    token = c.cookies.get("lp_session")
    actual = app.state.store.read(token)
    assert actual["source_records"][0]["record_as_received"] == record
    from participant.domain import semantic_turns

    assert "ANALYST_ONLY" not in json.dumps(semantic_turns(actual))
    assert actual["turns"][0]["answer_text"] == record["turns"][0]["answer_text"]
    assert fake.count == 0


def test_other_session_cannot_read_first_record(setup):
    cfg, fake, app, c = setup
    first = begin(setup)
    command(c, first, "answer", "SECRET_PARTICIPANT_ONE")
    c2 = TestClient(app)
    second = c2.post("/api/join", json={"token": cfg.join_token}).json()
    assert first["session_id"] != second["session_id"]
    assert "SECRET_PARTICIPANT_ONE" not in c2.get("/api/session").text
    assert c2.get("/api/admin/exports/" + first["session_id"]).status_code == 401


def test_admin_invitation_preloads_without_consent_or_inference(setup):
    cfg, fake, app, c = setup
    headers = {"Authorization": "Bearer " + cfg.admin_token}
    r = c.post(
        "/api/admin/invitations",
        headers=headers,
        json={"record": {"turns": [{"answer_text": "old"}]}},
    )
    assert r.status_code == 200 and r.json()["turn_count"] == 1
    value = r.json()["resume_path"].split("=", 1)[1]
    resumed = c.post("/api/resume", json={"token": value}).json()
    c.headers["X-Life-Patterns-Session"] = resumed["session_id"]
    assert resumed["phase"] == "consent" and resumed["turns"][0]["answer_text"] == "old"
    assert c.get("/api/admin/exports/" + resumed["session_id"], headers=headers).status_code == 403
    assert fake.count == 0


def test_birth_fields_blocked_and_typed_birth_quarantined(setup):
    cfg, fake, app, c = setup
    s = join(setup)
    r = c.post("/api/import", json={"record": {"birth_date": "1900-01-01", "turns": []}})
    assert r.status_code == 422
    s = command(c, s, "consent").json()
    s = c.post("/api/next", json={}).json()
    s = command(c, s, "answer", "My date of birth is 1900-01-01").json()
    assert s["phase"] == "awaiting_answer" and len(s["turns"]) == 0
    assert len(app.state.store.read(c.cookies.get("lp_session"))["quarantined_turns"]) == 1


def test_cross_origin_body_limit_and_sanitized_validation(setup):
    cfg, fake, app, c = setup
    assert (
        c.post(
            "/api/join", headers={"Origin": "https://other.example"}, json={"token": cfg.join_token}
        ).status_code
        == 403
    )
    assert c.post("/api/join", content=b"x" * 2_000_001).status_code == 413
    r = c.post("/api/join", json={"token": "PRIVATE_SHORT_VALUE"})
    assert r.status_code == 422 and "PRIVATE_SHORT_VALUE" not in r.text


def test_strict_json_and_provider_only():
    with pytest.raises(ValueError):
        strict_json('{"a":1,"a":2}')
    with pytest.raises(ValueError):
        strict_json('{"a":NaN}')
    with pytest.raises(ValueError):
        Venice("https://another-provider.example/v1", "x")
    with pytest.raises(ValueError):
        Venice("http://api.venice.ai/api/v1", "x")


def test_instrument_pins_and_hash_drift(tmp_path):
    a = authority()
    store = Store(tmp_path / "db", Fernet.generate_key().decode())
    v = store.pin_instrument(a)
    b = copy.deepcopy(a)
    b["version"] = "future-version"
    assert store.pin_instrument(b) != v
    assert store.instrument(v) == a
    with pytest.raises(RuntimeError):
        for name in (
            "INTERVIEW-PROTOCOL-v6.md",
            "interviewer-bank-v7.json",
            "EVIDENCE-GUIDE-v7.json",
        ):
            (tmp_path / name).write_text("altered")
        load_instrument(tmp_path)


def example_state():
    a = authority()
    s = new_state("test", "openai-gpt-56-sol", "xhigh")
    s["turns"] = [
        {
            "turn_id": "t1",
            "question_text": "Which?",
            "answer_text": "I organise the messages.",
            "canonical_question_id": "G01",
        }
    ]
    return a, s


def example_plan():
    return Plan.model_validate(
        {
            "action": "review",
            "question": None,
            "control_quote": None,
            "reason": "test",
            "dispositions": [
                {
                    "turn_id": "t1",
                    "status": "answered",
                    "conditions": [],
                    "process_feedback_quotes": [],
                    "reason": "test",
                }
            ],
            "evidence": [
                {
                    "evidence_id": "e1",
                    "source_quotes": [{"turn_id": "t1", "quote": "I organise the messages."}],
                    "observation": "Reports organising this information.",
                    "evidence_type": "usual_response_self_report",
                    "conditions": [],
                    "time_frame": "current",
                    "relationship_context": "scenario",
                    "candidate_facet_ids": ["D01.approach"],
                    "supported_scope": "This scenario",
                    "unsupported_extensions": ["No general intelligence claim."],
                }
            ],
        }
    )


def test_source_quote_and_facet_integrity():
    a, s = example_state()
    p = example_plan()
    validate_plan(p, s, a, ["t1"])
    p.evidence[0].source_quotes[0].quote = "INVENTED"
    with pytest.raises(ValueError):
        validate_plan(p, s, a, ["t1"])
    p = example_plan()
    p.evidence[0].candidate_facet_ids = ["NOT_A_FACET"]
    with pytest.raises(ValueError):
        validate_plan(p, s, a, ["t1"])
    p = example_plan()
    p.dispositions[0].status = "process_only"
    with pytest.raises(ValueError):
        validate_plan(p, s, a, ["t1"])


def test_dependent_routes_need_actual_matching_antecedent():
    a, s = example_state()
    p = example_plan()
    route = next(q for q in bank(a)["questions"] if q["id"] == "R02")
    p.action = "ask"
    p.question = Question(
        route_id="R02",
        route_type="canonical",
        text=route["question"],
        antecedent_turn_ids=[],
        equivalent_context=False,
        missing_distinction="test",
        why_useful="test",
    )
    with pytest.raises(ValueError):
        validate_plan(p, s, a, ["t1"])
    p.question.antecedent_turn_ids = ["t1"]
    with pytest.raises(ValueError):
        validate_plan(p, s, a, ["t1"])
    s["turns"][0]["canonical_question_id"] = "G06"
    validate_plan(p, s, a, ["t1"])


def test_wrong_canonical_wording_or_repeat_rejected():
    a, s = example_state()
    p = example_plan()
    route = next(q for q in bank(a)["questions"] if q["id"] == "G01")
    p.action = "ask"
    p.question = Question(
        route_id="G01",
        route_type="canonical",
        text="Made up question?",
        antecedent_turn_ids=[],
        equivalent_context=False,
        missing_distinction="test",
        why_useful="test",
    )
    with pytest.raises(ValueError):
        validate_plan(p, s, a, ["t1"])
    p.question.text = route["question"]
    with pytest.raises(ValueError):
        validate_plan(p, s, a, ["t1"])


def test_stop_requires_current_quote_not_missing_or_old():
    a, s = example_state()
    p = example_plan()
    p.action = "stop"
    with pytest.raises(ValueError):
        validate_plan(p, s, a, ["t1"])
    p.control_quote = Quote(turn_id="t1", quote="not actually in the answer")
    with pytest.raises(ValueError):
        validate_plan(p, s, a, ["t1"])


def test_proxy_origin_uses_configured_public_origin(setup):
    from dataclasses import replace

    cfg, fake, app, c = setup
    app = create_app(
        replace(cfg, public_origin="https://study.example"), provider=fake, instrument=authority()
    )
    c = TestClient(app, base_url="http://internal")
    assert (
        c.post(
            "/api/join", headers={"Origin": "https://study.example"}, json={"token": cfg.join_token}
        ).status_code
        == 200
    )


def test_provider_stream_is_parsed_and_wrong_model_rejected():
    import io
    from email.message import Message

    class Stream(io.BytesIO):
        def __init__(self, model):
            frames = [
                {
                    "model": model,
                    "choices": [
                        {
                            "delta": {
                                "content": json.dumps(
                                    {
                                        "approved": True,
                                        "errors": [],
                                        "context_supported": True,
                                        "no_redundant_question": True,
                                        "no_unsupported_extension": True,
                                        "control_is_participant_request": False,
                                    }
                                )
                            },
                            "finish_reason": "stop",
                        }
                    ],
                },
                {"choices": [], "usage": {"prompt_tokens": 12, "completion_tokens": 4}},
            ]
            super().__init__(
                b"".join(b"data: " + json.dumps(x).encode() + b"\n\n" for x in frames)
                + b"data: [DONE]\n\n"
            )
            self.headers = Message()
            self.headers["content-type"] = "text/event-stream"

    class Opener:
        def __init__(self, model):
            self.model = model

        def open(self, request, timeout):
            payload = json.loads(request.data)
            assert payload["store"] is False and payload["stream"] is True
            assert payload["reasoning_effort"] == "xhigh"
            assert "another-provider" not in request.full_url
            return Stream(self.model)

    provider = Venice(
        "https://venice-model-gateway-production.up.railway.app/v1", "synthetic-not-real"
    )
    provider.opener = Opener("openai-gpt-56-sol")
    answer, meta = provider.call(
        "test", {"synthetic": True}, Admission, "openai-gpt-56-sol", "xhigh"
    )
    assert answer.approved and meta["prompt_tokens"] == 12
    provider.opener = Opener("unexpected-model")
    with pytest.raises(ProviderError):
        provider.call("test", {}, Admission, "openai-gpt-56-sol", "xhigh")


def test_declared_raw_import_is_not_verified_provenance(setup):
    _, _, app, c = setup
    join(setup)
    r = c.post(
        "/api/import",
        json={
            "record": {
                "turns": [{"question_text": "An old question", "answer_text": "An old answer"}]
            },
            "source_type": "raw_transcript",
        },
    )
    assert r.status_code == 200
    state = app.state.store.read(c.cookies.get("lp_session"))
    assert state["source_records"][0]["original_wording_verified"] is None
    assert state["turns"][0]["question_wording_status"] != "verified_original"


def test_duplicate_import_keys_rejected_and_empty_import_cannot_repeat(setup):
    _, _, _, c = setup
    join(setup)
    r = c.post(
        "/api/import",
        json={"record_text": '{"turns":[{"answer_text":"first","answer_text":"second"}]}'},
    )
    assert r.status_code == 422
    assert c.post("/api/import", json={"record": {"turns": []}}).status_code == 200
    assert c.post("/api/import", json={"record": {"turns": []}}).status_code == 409


def test_old_tab_cannot_write_or_read_different_session(setup):
    _, fake, _, c = setup
    a = join(setup)
    b = join(setup)
    assert command(c, a, "decline").status_code == 409
    assert command(c, a, "stop").status_code == 409
    headers = {"X-Life-Patterns-Session": a["session_id"]}
    assert c.post("/api/import", headers=headers, json={"record": {"turns": []}}).status_code == 409
    assert c.post("/api/next", headers=headers, json={}).status_code == 409
    assert c.get("/api/session", headers=headers).status_code == 409
    assert c.get("/api/export?session_id=" + a["session_id"]).status_code == 409
    assert c.get("/api/session").json()["session_id"] == b["session_id"]
    assert fake.count == 0


def test_review_pause_and_correction_do_not_reopen_questioning(setup):
    _, fake, app, c = setup
    s = begin(setup)
    s = command(c, s, "answer", "I check the options.").json()
    fake.review = True
    s = c.post("/api/next", json={}).json()
    s = command(c, s, "review_seen").json()
    s = command(c, s, "pause").json()
    s = command(c, s, "resume").json()
    assert s["phase"] == "review"
    source = s["turns"][0]["turn_id"]
    s = command(c, s, "correct", "Only when time permits.", target=source).json()
    fake.review = False
    current = app.state.store.read(c.cookies.get("lp_session"))
    assert current["review_only"] is True
    assert c.post("/api/next", json={}).json()["phase"] == "review"


def test_imported_correction_preserves_source_wording_status(setup):
    _, _, app, c = setup
    s = join(setup)
    s = c.post(
        "/api/import",
        json={
            "record": {
                "turns": [{"question_text": "Edited question", "answer_text": "Earlier answer"}]
            }
        },
    ).json()
    s = command(c, s, "consent").json()
    s = command(c, s, "correct", "A clarified answer.", target=s["turns"][0]["turn_id"]).json()
    record = app.state.store.read(c.cookies.get("lp_session"))
    assert record["turns"][-1]["route_type"] == "participant_correction"
    assert (
        record["turns"][-1]["question_wording_status"]
        == record["turns"][0]["question_wording_status"]
    )
    assert record["turns"][-1]["id_basis"] == record["turns"][0]["id_basis"]


def test_hold_is_distinct_from_stop_and_excludes_target_source(setup):
    from participant.domain import ControlQuote, semantic_turns

    _, fake, app, c = setup
    s = begin(setup)
    s = command(c, s, "answer", "SYNTHETIC_TARGET_DETAIL").json()
    original = fake.call

    def held(system, payload, schema, model, effort):
        if schema is Admission:
            return Admission(
                approved=True,
                errors=[],
                context_supported=True,
                no_redundant_question=True,
                no_unsupported_extension=True,
                control_is_participant_request=False,
                target_information_detected=True,
            ), {"stage": "Admission"}
        plan, meta = original(system, payload, schema, model, effort)
        plan.action = "hold"
        plan.question = None
        plan.evidence = []
        plan.control_quote = ControlQuote(
            turn_id=payload["pending_turn_ids"][0], quote="SYNTHETIC_TARGET_DETAIL"
        )
        return plan, meta

    fake.call = held
    s = c.post("/api/next", json={}).json()
    assert s["phase"] == "paused"
    record = app.state.store.read(c.cookies.get("lp_session"))
    assert record["contamination_notes"]
    assert "SYNTHETIC_TARGET_DETAIL" not in json.dumps(semantic_turns(record))
    assert "SYNTHETIC_TARGET_DETAIL" not in c.get("/api/export").text
    assert record["quarantined_turns"][0].get("text") is None
    assert (
        c.get("/api/export").json()["blinding"]["birth_or_chart_data_used_by_interviewer"] is None
    )
    s = command(c, s, "resume").json()
    assert s["phase"] == "awaiting_answer"


def test_unexpected_provider_failure_releases_lease_and_counts_attempt(setup):
    _, fake, app, c = setup
    s = begin(setup)
    s = command(
        c, s, "answer", "I would usually keep my reading time unless something changed."
    ).json()

    def fail(*args, **kwargs):
        raise AttributeError("PRIVATE_FAILURE_BODY")

    fake.call = fail
    s = c.post("/api/next", json={}).json()
    assert s["phase"] == "error" and "PRIVATE_FAILURE_BODY" not in json.dumps(s)
    record = app.state.store.read(c.cookies.get("lp_session"))
    assert record["lease"] is None and record["calls"][-1]["stage"] == "failed_attempt"


def test_call_limit_stays_partial_without_false_participant_stop(setup):
    _, fake, app, c = setup
    s = begin(setup)
    s = command(c, s, "answer", "I would probably keep the hour for myself.").json()
    app.state.engine.maximum_calls = 1
    s = c.post("/api/next", json={}).json()
    assert s["phase"] == "resource_limited"
    result = c.get("/api/export").json()
    assert result["interview_status"] == "partial"
    assert result["stop_reason"] == "infrastructure_model_call_limit"
    assert fake.count == 0


def test_public_question_does_not_expose_internal_interpretation(setup):
    s = begin(setup)
    assert set(s["question"]) == {"text", "question_id"}


def test_controller_modification_rejected(tmp_path):
    for name in ("INTERVIEW-PROTOCOL-v6.md", "interviewer-bank-v7.json", "EVIDENCE-GUIDE-v7.json"):
        (tmp_path / name).write_bytes((SURVEY / name).read_bytes())
    (tmp_path / CONTROLLER.name).write_text("Changed controller")
    with pytest.raises(RuntimeError):
        load_instrument(tmp_path)
