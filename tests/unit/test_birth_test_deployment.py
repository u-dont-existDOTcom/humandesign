"""Checks at the actual unchanged Railway entrypoint."""
import base64

from fastapi.testclient import TestClient

from hdmatch.api.life_patterns_v2_owner_deployed_app import create_secured_owner_app


def test_public_development_mode_retains_old_root_and_adds_test(monkeypatch):
    monkeypatch.delenv("HDMATCH_OWNER_BASIC_PASSWORD", raising=False)
    app = create_secured_owner_app()
    client = TestClient(app)
    assert client.get("/healthz").status_code == 200
    assert client.get("/").status_code == 200
    assert client.get("/birth-test").status_code == 200
    assert client.get("/birth-test/api/contract").status_code == 200
    assert len([r for r in app.routes if getattr(r, "path", None) == "/birth-test"]) == 1


def test_enabled_auth_protects_old_and_new_routes(monkeypatch):
    monkeypatch.setenv("HDMATCH_OWNER_BASIC_USER", "synthetic-user")
    monkeypatch.setenv("HDMATCH_OWNER_BASIC_PASSWORD", "synthetic-test-password")
    client = TestClient(create_secured_owner_app())
    assert client.get("/healthz").status_code == 200
    for path in ("/", "/birth-test", "/birth-test/api/contract"):
        assert client.get(path).status_code == 401
    header = "Basic " + base64.b64encode(b"synthetic-user:synthetic-test-password").decode()
    assert client.get("/birth-test/api/contract", headers={"Authorization": header}).status_code == 200
