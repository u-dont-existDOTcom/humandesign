"""Push-to-talk transcription for Discover Your Unique Life Patterns.

Raw audio is authenticated, forwarded to the configured transcription provider, and then
discarded. The API returns advisory text for participant review; it does not itself write
transcription text into the research evidence record.
"""

from __future__ import annotations

import json
import os
import secrets
from pathlib import Path
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request as URLRequest
from urllib.request import urlopen

from fastapi import FastAPI, Header, HTTPException, Request

from .life_patterns_app import LifePatternsFileStore, OpenAILifePatternsMapper
from .life_patterns_interview_app import (
    OpenAILifePatternsInterviewer,
    create_life_patterns_interview_app,
)
from .life_patterns_recovery import LifePatternsRecoveryService, LifePatternsRecoverySettings

MAX_AUDIO_BYTES = 20 * 1024 * 1024
_ALLOWED_AUDIO_TYPES = {
    "audio/webm",
    "audio/ogg",
    "audio/mp4",
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
}


class OpenAILifePatternsTranscriber:
    def __init__(
        self,
        *,
        api_key: str | None,
        model: str = "gpt-4o-mini-transcribe",
        endpoint: str = "https://api.openai.com/v1/audio/transcriptions",
        timeout_seconds: float = 120.0,
    ) -> None:
        self.api_key = api_key.strip() if api_key else None
        self.model = model
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds

    @classmethod
    def from_env(cls) -> OpenAILifePatternsTranscriber:
        return cls(
            api_key=os.environ.get("HDMATCH_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY"),
            model=os.environ.get(
                "HDMATCH_LIFE_PATTERNS_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe"
            ).strip(),
            endpoint=os.environ.get(
                "HDMATCH_LIFE_PATTERNS_TRANSCRIBE_URL",
                "https://api.openai.com/v1/audio/transcriptions",
            ).strip(),
            timeout_seconds=float(
                os.environ.get("HDMATCH_LIFE_PATTERNS_TRANSCRIBE_TIMEOUT_SECONDS", "120")
            ),
        )

    def transcribe(self, audio: bytes, content_type: str) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("Life Patterns transcription is not configured")
        if not audio:
            raise ValueError("audio recording is empty")
        media_type = content_type.partition(";")[0].strip().lower()
        if media_type not in _ALLOWED_AUDIO_TYPES:
            raise ValueError("unsupported audio format")
        if len(audio) > MAX_AUDIO_BYTES:
            raise ValueError("audio recording is too large; use a shorter voice turn")
        extension = {
            "audio/webm": "webm",
            "audio/ogg": "ogg",
            "audio/mp4": "mp4",
            "audio/mpeg": "mp3",
            "audio/wav": "wav",
            "audio/x-wav": "wav",
        }[media_type]
        boundary = f"life-patterns-{secrets.token_hex(16)}"
        body = _multipart_body(
            boundary,
            fields={"model": self.model, "response_format": "json"},
            filename=f"voice-turn.{extension}",
            media_type=media_type,
            audio=audio,
        )
        request = URLRequest(
            self.endpoint,
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:  # noqa: S310
                raw = cast(bytes, response.read())
        except HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:1000]
            raise RuntimeError(f"Life Patterns transcription HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"Life Patterns transcription network error: {exc.reason}") from exc
        try:
            payload: Any = json.loads(raw.decode())
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError("transcription provider returned invalid JSON") from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("text"), str):
            raise RuntimeError("transcription provider returned no transcript text")
        text = str(payload["text"]).strip()
        if not text:
            raise RuntimeError("transcription provider returned an empty transcript")
        return {
            "text": text,
            "model": self.model,
            "advisory_transcript_requires_user_review": True,
            "raw_audio_stored": False,
        }


def _multipart_body(
    boundary: str,
    *,
    fields: dict[str, str],
    filename: str,
    media_type: str,
    audio: bytes,
) -> bytes:
    pieces: list[bytes] = []
    for name, value in fields.items():
        pieces.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                value.encode(),
                b"\r\n",
            ]
        )
    pieces.extend(
        [
            f"--{boundary}\r\n".encode(),
            (
                f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            ).encode(),
            f"Content-Type: {media_type}\r\n\r\n".encode(),
            audio,
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
    return b"".join(pieces)


def _bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="resume authorization is required")
    scheme, separator, token = authorization.partition(" ")
    if separator != " " or scheme.casefold() != "bearer" or len(token) < 16:
        raise HTTPException(status_code=401, detail="invalid resume authorization")
    return token


def register_life_patterns_voice_routes(
    app: FastAPI,
    *,
    store: LifePatternsFileStore,
    transcriber: OpenAILifePatternsTranscriber | Any,
) -> None:
    @app.post("/api/life-patterns/interview/sessions/{session_id}/transcribe")
    async def transcribe_voice(
        session_id: str,
        request: Request,
        authorization: str | None = Header(default=None),
    ) -> dict[str, Any]:
        token = _bearer_token(authorization)
        payload = store.read(session_id, token)
        if payload.get("consent_to_llm_processing") is not True:
            raise HTTPException(status_code=409, detail="AI-processing consent is missing")
        content_type = request.headers.get("content-type", "").partition(";")[0].strip().lower()
        if content_type not in _ALLOWED_AUDIO_TYPES:
            raise HTTPException(status_code=415, detail="unsupported audio format")
        declared_length = request.headers.get("content-length")
        if declared_length and declared_length.isdigit() and int(declared_length) > MAX_AUDIO_BYTES:
            raise HTTPException(status_code=413, detail="audio recording is too large")
        audio = await request.body()
        if len(audio) > MAX_AUDIO_BYTES:
            raise HTTPException(status_code=413, detail="audio recording is too large")
        try:
            return cast(dict[str, Any], transcriber.transcribe(audio, content_type))
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(
                status_code=502,
                detail="Voice transcription failed; no audio was stored. You can retry or type instead.",
            ) from exc


def create_life_patterns_voice_app_from_env() -> FastAPI:
    root_value = os.environ.get("HDMATCH_LIFE_PATTERNS_STORE", "").strip()
    if not root_value:
        raise RuntimeError("HDMATCH_LIFE_PATTERNS_STORE is required")
    store = LifePatternsFileStore(Path(root_value))
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=OpenAILifePatternsInterviewer.from_env(),
        mapper=OpenAILifePatternsMapper.from_env(),
        recovery=LifePatternsRecoveryService(store, LifePatternsRecoverySettings.from_env()),
    )
    register_life_patterns_voice_routes(
        app,
        store=store,
        transcriber=OpenAILifePatternsTranscriber.from_env(),
    )
    return app
