from __future__ import annotations

from fastapi.testclient import TestClient
from test_life_patterns_v2_owner_workflow import Model, op, session

from hdmatch.api.life_patterns_v2_owner_conversation import ModelProviderError
from hdmatch.api.life_patterns_v2_owner_persistent import _canonical_sha
from hdmatch.api.life_patterns_v2_owner_workflow_api import create_workflow_app, measurement_package


def client() -> TestClient:
    return TestClient(create_workflow_app(model=Model()))


def test_restore_never_overwrites_newer_live_session() -> None:
    c = client()
    first = c.post("/api/owner-v2/conversation/sessions").json()
    sid = first["session_id"]
    c.post(
        f"/api/owner-v2/conversation/sessions/{sid}/operations",
        json={"operation_id": "pause", "expected_revision": 0, "kind": "pause", "payload": {}},
    )
    restored = c.post(
        "/api/owner-v2/conversation/sessions/restore", json={"snapshot": first["snapshot"]}
    )
    assert restored.status_code == 200
    assert restored.json()["view"]["revision"] == 1
    assert restored.json()["view"]["phase"] == "paused"


def test_bad_snapshot_is_rejected_without_creating_session() -> None:
    c = client()
    r = c.post(
        "/api/owner-v2/conversation/sessions/restore",
        json={
            "snapshot": {
                "session_id": "OWNER-invalid",
                "schema": "life-patterns-hidden-ledger-session-v2",
            }
        },
    )
    assert r.status_code == 422
    assert "OWNER-invalid" not in c.app.state.recoverability_runtime.sessions


def test_measurement_includes_exact_archive_and_blueprint_without_patterns() -> None:
    s = session()
    result = measurement_package(s)
    assert result["blueprint_version"] and result["blueprint_sha256"]
    assert result["evidence_archive"]["record"]
    assert result["scientifically_validated"] is False
    digest = result.pop("measurement_bundle_sha256")
    assert digest == _canonical_sha(result)


def test_correction_preserves_historical_authority_but_excludes_current_acceptance() -> None:
    m = Model()
    m.direct = True
    s = session(m)
    s.execute(op(s, "answer", {"message": "I prefer to think alone before group decisions."}))
    original = s.core.record.model_dump(mode="json")
    pid = s.view()["patterns"][0]["proposal_id"]
    s.execute(
        op(
            s,
            "annotate",
            {"proposal_id": pid, "message": "Only with unfamiliar groups."},
            "correction",
        )
    )
    assert s.core.record.model_dump(mode="json") == original
    assert s.view()["patterns"][0]["status"] == "disputed"
    exported = measurement_package(s)
    assert exported["completed_results"][0]["status"] == "unresolved"
    assert exported["unresolved_corrections"]


def test_legacy_mutation_cannot_bypass_workflow_contract() -> None:
    c = client()
    sid = c.post("/api/owner-v2/conversation/sessions").json()["session_id"]
    result = c.post(
        f"/api/owner-v2/conversation/sessions/{sid}/turns", json={"message": "Old client"}
    )
    assert result.status_code == 409
    assert c.app.state.recoverability_runtime.sessions[sid].revision == 0


def test_legacy_backup_read_stays_raw_and_new_client_gets_atomic_view() -> None:
    c = client()
    first = c.post("/api/owner-v2/conversation/sessions").json()
    path = f"/api/owner-v2/conversation/sessions/{first['session_id']}/recovery"
    old = c.get(path).json()
    assert old["schema"] == "life-patterns-hidden-ledger-session-v2"
    assert "record" in old and "snapshot" not in old
    digest = old.pop("recovery_sha256")
    assert digest == _canonical_sha(old)
    new = c.get(path, headers={"x-life-patterns-client": "workflow-v1"}).json()
    assert new["view"]["revision"] == new["snapshot"]["workflow"]["revision"]


def test_recovered_summary_correction_is_also_unresolved_in_current_export() -> None:
    s = session()
    s.legacy_patterns = [{"status": "accepted", "wording": "A recovered earlier formulation."}]
    s.execute(
        op(s, "annotate", {"proposal_id": "legacy-0", "message": "That applied only years ago."})
    )
    assert s.view()["patterns"][0]["status"] == "disputed"
    assert measurement_package(s)["completed_results"][0]["status"] == "unresolved"


def test_credit_balance_exhaustion_is_actionable_and_preserves_revision() -> None:
    class CreditExhaustedModel(Model):
        def route_participant_turn(self, **kwargs):
            raise ModelProviderError(
                http_status=429,
                error_type="insufficient_quota",
                error_code="credit_balance_exhausted",
                retryable=False,
            )

    c = TestClient(create_workflow_app(model=CreditExhaustedModel()))
    created = c.post("/api/owner-v2/conversation/sessions").json()
    sid = created["session_id"]
    result = c.post(
        f"/api/owner-v2/conversation/sessions/{sid}/operations",
        json={
            "operation_id": "credit-exhausted",
            "expected_revision": 0,
            "kind": "answer",
            "payload": {"message": "A synthetic answer."},
        },
    )
    assert result.status_code == 503
    assert "credit balance is exhausted" in result.json()["detail"]
    assert "add API credit before retrying" in result.json()["detail"]
    assert c.app.state.recoverability_runtime.sessions[sid].revision == 0
