"""Fail-closed placeholders for normative stateful run operations."""

from __future__ import annotations

from typing import Any, NoReturn

from fastapi import FastAPI

from hdmatch.api.errors import ERROR_RESPONSES, ApiProblem
from hdmatch.api.models import ErrorIssue, ErrorResponse


def _unresolved(operation: str) -> NoReturn:
    raise ApiProblem(
        501,
        "UNRESOLVED_ENDPOINT",
        (
            f"{operation} requires run-state/orchestration services that are not implemented; "
            "no answer key or concealed birth tuple was read"
        ),
        issues=(
            ErrorIssue(
                location=("operation", operation),
                message="capability is explicitly unresolved",
                type="not_implemented",
            ),
        ),
    )


def register_unresolved_run_routes(service: FastAPI) -> None:
    responses: dict[int | str, dict[str, Any]] = {
        501: {
            "model": ErrorResponse,
            "description": "Normative operation is explicitly unresolved and fail-closed",
        },
        422: ERROR_RESPONSES[422],
    }

    @service.post("/v1/runs", status_code=501, responses=responses, operation_id="createRun")
    async def create_run() -> None:
        _unresolved("create_run")

    @service.post(
        "/v1/runs/{run_id}/profile",
        status_code=501,
        responses=responses,
        operation_id="uploadFrozenProfile",
    )
    async def upload_profile(run_id: str) -> None:
        _unresolved(f"upload_profile:{run_id}")

    @service.post(
        "/v1/runs/{run_id}/candidates",
        status_code=501,
        responses=responses,
        operation_id="uploadCandidates",
    )
    async def upload_candidates(run_id: str) -> None:
        _unresolved(f"upload_candidates:{run_id}")

    @service.post(
        "/v1/runs/{run_id}/search/bounded",
        status_code=501,
        responses=responses,
        operation_id="runBoundedSearch",
    )
    async def bounded_search(run_id: str) -> None:
        _unresolved(f"bounded_search:{run_id}")

    @service.post(
        "/v1/runs/{run_id}/search/global",
        status_code=501,
        responses=responses,
        operation_id="runGlobalSearch",
    )
    async def global_search(run_id: str) -> None:
        _unresolved(f"global_search:{run_id}")

    @service.get(
        "/v1/runs/{run_id}/opaque-results",
        status_code=501,
        responses=responses,
        operation_id="getOpaqueResults",
    )
    async def opaque_results(run_id: str) -> None:
        _unresolved(f"opaque_results:{run_id}")

    @service.get(
        "/v1/runs/{run_id}/differences",
        status_code=501,
        responses=responses,
        operation_id="getOpaqueDifferences",
    )
    async def differences(run_id: str) -> None:
        _unresolved(f"differences:{run_id}")

    @service.post(
        "/v1/runs/{run_id}/answers",
        status_code=501,
        responses=responses,
        operation_id="appendFrozenAnswersAndRerun",
    )
    async def answers(run_id: str) -> None:
        _unresolved(f"answers:{run_id}")

    @service.post(
        "/v1/runs/{run_id}/freeze-finalists",
        status_code=501,
        responses=responses,
        operation_id="freezeFinalists",
    )
    async def freeze_finalists(run_id: str) -> None:
        _unresolved(f"freeze_finalists:{run_id}")

    @service.post(
        "/v1/runs/{run_id}/reveal-holdout",
        status_code=501,
        responses=responses,
        operation_id="revealHoldout",
    )
    async def reveal_holdout(run_id: str) -> None:
        _unresolved(f"reveal_holdout:{run_id}")

    @service.post(
        "/v1/runs/{run_id}/robustness",
        status_code=501,
        responses=responses,
        operation_id="runRobustness",
    )
    async def robustness(run_id: str) -> None:
        _unresolved(f"robustness:{run_id}")

    @service.get(
        "/v1/runs/{run_id}/final-report",
        status_code=501,
        responses=responses,
        operation_id="getFinalReport",
    )
    async def final_report(run_id: str, reveal: bool = False) -> None:
        suffix = "reveal_requested_but_not_performed" if reveal else "concealed"
        _unresolved(f"final_report:{run_id}:{suffix}")
