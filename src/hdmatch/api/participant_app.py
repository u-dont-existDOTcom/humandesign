"""Environment-configured FastAPI factory for the participant interview service."""

from __future__ import annotations

import os

from fastapi import FastAPI

from hdmatch.model import load_mapping_library
from hdmatch.participant import ParticipantSessionService, ParticipantSessionStore
from hdmatch.participant.century_backend import CenturyCapableParticipantBackend

from .app import ApiDependencies, create_app


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"required environment variable is missing: {name}")
    return value


def create_participant_app_from_env() -> FastAPI:
    """Build the deployable participant API from explicit artifact paths.

    Required environment variables:

    - ``HDMATCH_EPHEMERIS_PATH``: directory/file containing authorized Swiss ``.se1`` files
    - ``HDMATCH_MAPPING_PATH``: frozen mapping-library JSON
    - ``HDMATCH_QUESTION_BANK_PATH``: matching frozen question-bank JSON
    - ``HDMATCH_PARTICIPANT_STORE``: private persistent session directory

    Optional:

    - ``HDMATCH_CANDIDATE_CACHE``: persistent exact month-universe cache directory
    - ``HDMATCH_CENTURY_CACHE``: verified exact century-wide candidate cache directory
    - ``HDMATCH_CENTURY_MANIFEST_SHA256``: exact released manifest hash for fast month slices
    - ``HDMATCH_CENTURY_CANONICAL_ROWS_SHA256``: released logical-universe hash
    - ``HDMATCH_CODE_COMMIT``: deployed source revision for prediction provenance
    """

    ephemeris_path = _required_env("HDMATCH_EPHEMERIS_PATH")
    mapping_path = _required_env("HDMATCH_MAPPING_PATH")
    question_bank_path = _required_env("HDMATCH_QUESTION_BANK_PATH")
    session_store = _required_env("HDMATCH_PARTICIPANT_STORE")
    candidate_cache = os.environ.get("HDMATCH_CANDIDATE_CACHE") or None
    century_cache = os.environ.get("HDMATCH_CENTURY_CACHE") or None
    century_manifest_sha256 = os.environ.get("HDMATCH_CENTURY_MANIFEST_SHA256") or None
    century_canonical_rows_sha256 = os.environ.get("HDMATCH_CENTURY_CANONICAL_ROWS_SHA256") or None
    code_commit = os.environ.get("HDMATCH_CODE_COMMIT", "unknown")

    backend = CenturyCapableParticipantBackend(
        ephemeris_path=ephemeris_path,
        mapping_path=mapping_path,
        question_bank_path=question_bank_path,
        candidate_cache_dir=candidate_cache,
        century_cache_dir=century_cache,
        century_manifest_sha256=century_manifest_sha256,
        century_canonical_rows_sha256=century_canonical_rows_sha256,
        code_commit=code_commit,
    )
    sessions = ParticipantSessionService(
        store=ParticipantSessionStore(session_store),
        backend=backend,
    )
    return create_app(
        ApiDependencies(
            ephemeris_provider=backend.chart_engine.provider,
            mapping_library=load_mapping_library(mapping_path),
            participant_sessions=sessions,
            code_commit=code_commit,
        )
    )
