from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import pytest
from fastapi import FastAPI
from starlette.types import Message, Scope

from hdmatch.api import ApiDependencies, create_app
from hdmatch.chart.ephemeris import (
    CelestialBody,
    EclipticPosition,
    EphemerisMetadata,
    NodeConvention,
)
from hdmatch.model import load_mapping_library
from hdmatch.schemas import CandidateState, ChartFeatures, LocalDateOverlap, ScoredState

PROJECT_ROOT = Path(__file__).parents[2]


class LinearProvider:
    def __init__(self, epoch: datetime) -> None:
        self.epoch = epoch
        self._metadata = EphemerisMetadata(
            provider="analytic-api-test",
            library_version="1",
            files=(),
            calculation_flags=("analytic",),
            coordinate_frame="test",
            node_convention=NodeConvention.TRUE,
        )

    @property
    def metadata(self) -> EphemerisMetadata:
        return self._metadata

    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        days = (at_utc - self.epoch).total_seconds() / 86400.0
        speed = 1.0 if body in (CelestialBody.SUN, CelestialBody.EARTH) else 0.01
        base = 100.0 + list(CelestialBody).index(body) * 17.0
        return EclipticPosition((base + speed * days) % 360.0, speed)

    def max_abs_speed_degrees_per_day(self, body: CelestialBody) -> float:
        return 1.1 if body in (CelestialBody.SUN, CelestialBody.EARTH) else 0.02

    def min_solar_speed_degrees_per_day(self) -> float:
        return 0.9


@dataclass(frozen=True)
class AsgiResponse:
    status_code: int
    headers: dict[str, str]
    json: dict[str, Any]


def request_json(
    app: FastAPI,
    method: str,
    url: str,
    body: dict[str, Any] | None = None,
) -> AsgiResponse:
    parsed = urlsplit(url)
    encoded = b"" if body is None else json.dumps(body).encode("utf-8")
    headers = [(b"accept", b"application/json")]
    if body is not None:
        headers.extend(
            (
                (b"content-type", b"application/json"),
                (b"content-length", str(len(encoded)).encode("ascii")),
            )
        )
    scope: Scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": parsed.path,
        "raw_path": parsed.path.encode("ascii"),
        "query_string": parsed.query.encode("ascii"),
        "root_path": "",
        "headers": headers,
        "client": ("test", 123),
        "server": ("testserver", 80),
        "state": {},
    }
    sent: list[Message] = []
    request_delivered = False

    async def receive() -> Message:
        nonlocal request_delivered
        if request_delivered:
            return {"type": "http.disconnect"}
        request_delivered = True
        return {"type": "http.request", "body": encoded, "more_body": False}

    async def send(message: Message) -> None:
        sent.append(message)

    asyncio.run(app(scope, receive, send))
    start = next(message for message in sent if message["type"] == "http.response.start")
    response_body = b"".join(
        message.get("body", b"")
        for message in sent
        if message["type"] == "http.response.body"
    )
    response_headers = {
        key.decode("latin-1"): value.decode("latin-1") for key, value in start["headers"]
    }
    return AsgiResponse(
        status_code=start["status"],
        headers=response_headers,
        json=json.loads(response_body),
    )


@pytest.fixture
def configured_app() -> FastAPI:
    epoch = datetime(2020, 1, 1, 12, tzinfo=UTC)
    library = load_mapping_library(PROJECT_ROOT / "mappings/mapping_library_v1.json")
    return create_app(
        ApiDependencies(
            ephemeris_provider=LinearProvider(epoch),
            mapping_library=library,
            code_commit="test-commit",
        )
    )


def test_health_and_model_metadata_disclose_readiness_and_unresolved_status(
    configured_app: FastAPI,
) -> None:
    health = request_json(configured_app, "GET", "/health")
    metadata = request_json(configured_app, "GET", "/v1/model/metadata")

    assert health.status_code == 200
    assert health.json["chart_engine"]["status"] == "ready"
    assert health.json["symbolic_model"]["status"] == "ready"
    assert health.json["answer_key_access"] == "prohibited"
    assert metadata.status_code == 200
    assert metadata.json["code_commit"] == "test-commit"
    assert metadata.json["chart"]["ephemeris"]["provider"] == "analytic-api-test"
    assert metadata.json["symbolic"]["mapping_library_sha256"]
    assert "final_report_reveal" in metadata.json["unavailable_capabilities"]
    assert metadata.json["chart"]["cross_engine_status"] == "unverified"


def test_chart_endpoint_returns_complete_deterministic_record(configured_app: FastAPI) -> None:
    response = request_json(
        configured_app,
        "POST",
        "/v1/chart",
        {"birth_utc": "2020-01-01T12:00:00Z"},
    )

    assert response.status_code == 200
    assert response.json["personality_utc"] == "2020-01-01T12:00:00Z"
    assert len(response.json["personality_activations"]) == len(CelestialBody)
    assert len(response.json["design_activations"]) == len(CelestialBody)
    assert len(response.json["complete_feature_hash"]) == 64
    assert response.json["engine_metadata"]["cross_engine_status"] == "unverified"
    assert (
        response.json["engine_metadata"]["advanced_substructure_status"]
        == "unavailable_unvalidated"
    )


def test_state_interval_endpoint_returns_half_open_complete_partition(
    configured_app: FastAPI,
) -> None:
    response = request_json(
        configured_app,
        "POST",
        "/v1/chart/state-intervals",
        {
            "range_start_utc": "2020-01-01T12:00:00Z",
            "range_end_utc": "2020-01-01T12:00:01Z",
            "feature_layers": ["architecture", "gate_line"],
            "boundary_tolerance_seconds": 0.1,
        },
    )

    assert response.status_code == 200
    assert len(response.json["intervals"]) == 1
    interval = response.json["intervals"][0]
    assert interval["start_utc"] == "2020-01-01T12:00:00Z"
    assert interval["end_utc"] == "2020-01-01T12:00:01Z"
    assert interval["state_id"].startswith("STATE-")
    assert interval["cross_engine_status"] == "unverified"


def test_symbolic_scoring_exposes_unresolved_questions_without_inventing_support(
    configured_app: FastAPI,
) -> None:
    response = request_json(
        configured_app,
        "POST",
        "/v1/model/symbolic-score",
        {
            "chart_features": {
                "type": "generator",
                "strategy": "wait_to_respond",
                "authority": "sacral",
                "profile": "1/3",
                "defined_centers": ["sacral"],
            },
            "responses": [
                {
                    "question_id": "UNMAPPED",
                    "cluster_id": "UNKNOWN",
                    "answer": "unknown",
                    "behavioral_confidence": 1.0,
                    "measurement_reliability": 1.0,
                }
            ],
            "prevalence_by_anchor": {},
        },
    )

    assert response.status_code == 200
    assert response.json["score"]["net_rubric_bits"] == 0.0
    assert response.json["score"]["unresolved_question_ids"] == ["UNMAPPED"]


def _candidate_state(
    state_id: str, local_date: date, score_hash: str = "a" * 64
) -> CandidateState:
    start = datetime.combine(local_date, datetime.min.time(), tzinfo=UTC)
    chart = ChartFeatures(
        personality_utc=start,
        design_utc=start - timedelta(days=88),
        type="generator",
        strategy="wait_to_respond",
        authority="sacral",
        profile="1/3",
        definition="single_definition",
        activations={},
    )
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=start + timedelta(days=1),
        chart_features_hash=score_hash,
        chart_features=chart,
        local_date_overlaps=(LocalDateOverlap(date=local_date, seconds=86400),),
    )


def _score(state_id: str, value: float) -> ScoredState:
    return ScoredState(
        state_id=state_id,
        net_rubric_bits=value,
        evidence_rubric_bits=max(value, 0.0),
        contradiction_rubric_bits=max(-value, 0.0),
        detailed_support=50,
        core_fit=50,
        meaningful_contradictions=0,
    )


def test_search_endpoints_delegate_to_existing_pure_search_services(
    configured_app: FastAPI,
) -> None:
    states = (
        _candidate_state("S1", date(2020, 1, 1)),
        _candidate_state("S2", date(2020, 1, 2), "b" * 64),
    )
    aggregation = request_json(
        configured_app,
        "POST",
        "/v1/search/date-aggregation",
        {
            "states": [state.model_dump(mode="json") for state in states],
            "scores": {
                "S1": _score("S1", 1.0).model_dump(mode="json"),
                "S2": _score("S2", 2.0).model_dump(mode="json"),
            },
            "mode": "best_state",
        },
    )
    question = request_json(
        configured_app,
        "POST",
        "/v1/search/next-question",
        {
            "candidate_weights": [1.0, 1.0],
            "likelihoods_by_question": {
                "Q1": [{"a": 1.0}, {"b": 1.0}],
                "Q2": [{"a": 0.5, "b": 0.5}, {"a": 0.5, "b": 0.5}],
            },
        },
    )

    assert aggregation.status_code == 200
    assert aggregation.json["results"][0]["local_date"] == "2020-01-02"
    assert aggregation.json["results"][0]["date_rank"] == 1.0
    assert question.status_code == 200
    assert question.json["selection"]["question_id"] == "Q1"
    assert question.json["selection"]["expected_information_gain"] == pytest.approx(1.0)


def test_unconfigured_components_fail_with_explicit_service_errors() -> None:
    app = create_app()
    response = request_json(
        app,
        "POST",
        "/v1/chart",
        {"birth_utc": "2020-01-01T12:00:00Z"},
    )
    invalid = request_json(app, "POST", "/v1/chart", {})
    incomplete_layers = request_json(
        app,
        "POST",
        "/v1/chart/state-intervals",
        {
            "range_start_utc": "2020-01-01T12:00:00Z",
            "range_end_utc": "2020-01-01T12:00:01Z",
            "feature_layers": ["architecture"],
        },
    )
    missing = request_json(app, "GET", "/does-not-exist")

    assert response.status_code == 503
    assert response.json["error"]["code"] == "EPHEMERIS_NOT_CONFIGURED"
    assert invalid.status_code == 422
    assert invalid.json["error"]["code"] == "REQUEST_VALIDATION_FAILED"
    assert incomplete_layers.status_code == 422
    assert incomplete_layers.json["error"]["code"] == "REQUEST_VALIDATION_FAILED"
    assert missing.status_code == 404
    assert missing.json["error"]["code"] == "HTTP_ERROR"


@pytest.mark.parametrize(
    ("method", "url"),
    (
        ("POST", "/v1/runs"),
        ("POST", "/v1/runs/R/profile"),
        ("POST", "/v1/runs/R/candidates"),
        ("POST", "/v1/runs/R/search/bounded"),
        ("POST", "/v1/runs/R/search/global"),
        ("GET", "/v1/runs/R/opaque-results"),
        ("GET", "/v1/runs/R/differences"),
        ("POST", "/v1/runs/R/answers"),
        ("POST", "/v1/runs/R/freeze-finalists"),
        ("POST", "/v1/runs/R/reveal-holdout"),
        ("POST", "/v1/runs/R/robustness"),
        ("GET", "/v1/runs/R/final-report?reveal=true"),
    ),
)
def test_stateful_normative_routes_fail_closed(method: str, url: str) -> None:
    response = request_json(create_app(), method, url)

    assert response.status_code == 501
    assert response.json["error"]["code"] == "UNRESOLVED_ENDPOINT"
    assert "no answer key" in response.json["error"]["message"]


def test_openapi_declares_supported_and_fail_closed_contracts(configured_app: FastAPI) -> None:
    schema = configured_app.openapi()

    assert schema["paths"]["/v1/chart"]["post"]["operationId"] == "calculateChart"
    assert schema["paths"]["/v1/runs"]["post"]["operationId"] == "createRun"
    assert "501" in schema["paths"]["/v1/runs"]["post"]["responses"]
    final_errors = schema["paths"]["/v1/runs/{run_id}/final-report"]["get"]["responses"]
    assert final_errors["422"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/ErrorResponse"
    }
    assert "ErrorResponse" in schema["components"]["schemas"]
    request_schemas = json.dumps(
        {
            path: operations
            for path, operations in schema["paths"].items()
            if path != "/v1/model/metadata"
        }
    )
    assert "answer_key_path" not in request_schemas
    assert "secret_key" not in request_schemas
