"""Deployment wrapper for the Life Patterns development prototype.

HTTP Basic Auth is enabled only when ``HDMATCH_OWNER_BASIC_PASSWORD`` is non-empty.
Leaving the password empty intentionally exposes the development surface without a login.
"""

from __future__ import annotations

import base64
import os
import secrets
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse

from .life_patterns_v2_owner_coverage import create_life_patterns_v2_owner_coverage_app


def _unauthorized() -> PlainTextResponse:
    return PlainTextResponse(
        "Development authentication required.",
        status_code=401,
        headers={"WWW-Authenticate": 'Basic realm="Life Patterns Development"'},
    )


def _basic_authorized(
    authorization: str | None, *, expected_username: str, expected_password: str
) -> bool:
    if not authorization or not authorization.startswith("Basic "):
        return False
    try:
        decoded = base64.b64decode(authorization[6:], validate=True).decode("utf-8")
        supplied_username, supplied_password = decoded.split(":", 1)
    except (ValueError, UnicodeDecodeError):
        return False
    return secrets.compare_digest(supplied_username, expected_username) and secrets.compare_digest(
        supplied_password, expected_password
    )


def create_secured_owner_app() -> FastAPI:
    expected_username = os.environ.get("HDMATCH_OWNER_BASIC_USER", "owner").strip() or "owner"
    expected_password = os.environ.get("HDMATCH_OWNER_BASIC_PASSWORD", "").strip()
    auth_enabled = bool(expected_password)

    app = create_life_patterns_v2_owner_coverage_app()
    app.state.owner_basic_auth_enabled = auth_enabled

    if not auth_enabled:
        return app

    @app.middleware("http")
    async def require_owner_auth(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if request.url.path == "/healthz":
            return await call_next(request)
        if not _basic_authorized(
            request.headers.get("authorization"),
            expected_username=expected_username,
            expected_password=expected_password,
        ):
            return _unauthorized()
        return await call_next(request)

    return app


app = create_secured_owner_app()
