"""Explicit JSON error boundary shared by every API route."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from hdmatch.api.models import ErrorDetail, ErrorIssue, ErrorResponse, jsonable_error


class ApiProblem(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        *,
        issues: tuple[ErrorIssue, ...] = (),
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.issues = issues


ERROR_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {"model": ErrorResponse, "description": "Invalid domain request"},
    422: {"model": ErrorResponse, "description": "Request schema validation failed"},
    500: {"model": ErrorResponse, "description": "Internal service failure"},
    503: {"model": ErrorResponse, "description": "Required deterministic component unavailable"},
}


def install_error_handlers(service: FastAPI) -> None:
    @service.exception_handler(ApiProblem)
    async def api_problem_handler(_request: Request, exc: ApiProblem) -> JSONResponse:
        response = ErrorResponse(
            error=ErrorDetail(code=exc.code, message=exc.message, issues=exc.issues)
        )
        return JSONResponse(status_code=exc.status_code, content=jsonable_error(response))

    @service.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        issues = tuple(
            ErrorIssue(
                location=tuple(
                    str(item) if not isinstance(item, int) else item for item in error["loc"]
                ),
                message=str(error["msg"]),
                type=str(error["type"]),
            )
            for error in exc.errors()
        )
        response = ErrorResponse(
            error=ErrorDetail(
                code="REQUEST_VALIDATION_FAILED",
                message="request did not conform to the declared schema",
                issues=issues,
            )
        )
        return JSONResponse(status_code=422, content=jsonable_error(response))

    @service.exception_handler(StarletteHTTPException)
    async def http_error_handler(
        _request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        response = ErrorResponse(
            error=ErrorDetail(
                code="HTTP_ERROR",
                message=str(exc.detail),
                issues=(
                    ErrorIssue(location=("path",), message=str(exc.detail), type="http_error"),
                ),
            )
        )
        return JSONResponse(status_code=exc.status_code, content=jsonable_error(response))

    @service.exception_handler(Exception)
    async def internal_error_handler(_request: Request, _exc: Exception) -> JSONResponse:
        response = ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message="the deterministic service failed without producing a result",
            )
        )
        return JSONResponse(status_code=500, content=jsonable_error(response))


def domain_problem(exc: Exception) -> ApiProblem:
    return ApiProblem(
        400,
        "INVALID_DOMAIN_REQUEST",
        str(exc),
        issues=(ErrorIssue(location=("body",), message=str(exc), type="domain_error"),),
    )


def engine_problem(exc: Exception) -> ApiProblem:
    return ApiProblem(
        503,
        "DETERMINISTIC_ENGINE_UNAVAILABLE",
        str(exc),
        issues=(ErrorIssue(location=("engine",), message=str(exc), type="engine_error"),),
    )
