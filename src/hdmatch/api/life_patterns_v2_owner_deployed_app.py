"""HTTP-authenticated deployment wrapper for the owner-only Life Patterns v2 prototype."""

from __future__ import annotations

import base64
import os
import secrets
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import PlainTextResponse

from .life_patterns_v2_owner_app import create_life_patterns_v2_owner_app


def _unauthorized() -> PlainTextResponse:
    return PlainTextResponse(
        "Owner authentication required.",
        status_code=401,
        headers={"WWW-Authenticate": 'Basic realm="Life Patterns Owner"'},
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


def create_secured_owner_app():  # type: ignore[no-untyped-def]
    expected_username = os.environ.get("HDMATCH_OWNER_BASIC_USER", "owner")
    expected_password = os.environ.get("HDMATCH_OWNER_BASIC_PASSWORD", "").strip()
    if not expected_password:
        raise RuntimeError("HDMATCH_OWNER_BASIC_PASSWORD is required for the deployed owner app")

    app = create_life_patterns_v2_owner_app()

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
