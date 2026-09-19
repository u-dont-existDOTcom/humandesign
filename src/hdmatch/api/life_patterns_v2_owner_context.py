"""Request-local evidence context shared by every interview model route."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

_context: ContextVar[Callable[[], dict[str, Any]] | None] = ContextVar(
    "interview_context", default=None
)


@contextmanager
def interview_context(provider: Callable[[], dict[str, Any]]) -> Iterator[None]:
    token = _context.set(provider)
    try:
        yield
    finally:
        _context.reset(token)


def current_interview_context() -> dict[str, Any] | None:
    provider = _context.get()
    return provider() if provider is not None else None
