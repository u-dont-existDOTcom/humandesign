"""Participant-confirmed birthplace search with offline timezone resolution.

Only the birthplace query is sent to the configured geocoder. Birth date/time, email,
relationship responses, and hidden predictions never leave the application in this step.
The default public Nominatim backend is cached and globally rate-limited to comply with
its public-service usage policy.
"""

from __future__ import annotations

import importlib
import json
import os
import threading
import time
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, cast
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_NOMINATIM_SEARCH = "https://nominatim.openstreetmap.org/search"
DEFAULT_USER_AGENT = "RelationshipPatternLab/0.1 (+https://u-dont-exist.com/)"
_RATE_LOCK = threading.Lock()
_LAST_UPSTREAM_REQUEST = 0.0
_MIN_REQUEST_INTERVAL_SECONDS = 1.05


@dataclass(frozen=True, slots=True)
class PlaceCandidate:
    provider: str
    provider_id: str
    display_name: str
    latitude: float
    longitude: float
    iana_timezone: str
    country_code: str | None
    category: str | None
    place_type: str | None

    def public_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "provider_id": self.provider_id,
            "display_name": self.display_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "iana_timezone": self.iana_timezone,
            "country_code": self.country_code,
            "category": self.category,
            "place_type": self.place_type,
        }


def search_birthplaces(query: str, *, limit: int = 5) -> tuple[PlaceCandidate, ...]:
    normalized = " ".join(query.split())
    if len(normalized) < 2 or len(normalized) > 200:
        raise ValueError("birthplace query must be between 2 and 200 characters")
    if limit < 1 or limit > 8:
        raise ValueError("birthplace result limit must be between 1 and 8")
    endpoint = os.environ.get("HDMATCH_GEOCODER_URL", DEFAULT_NOMINATIM_SEARCH).strip()
    user_agent = os.environ.get("HDMATCH_GEOCODER_USER_AGENT", DEFAULT_USER_AGENT).strip()
    if not endpoint.startswith("https://"):
        raise RuntimeError("birthplace geocoder must use HTTPS")
    if not user_agent:
        raise RuntimeError("birthplace geocoder User-Agent must be configured")
    return _search_birthplaces_cached(normalized, limit, endpoint, user_agent)


@lru_cache(maxsize=512)
def _search_birthplaces_cached(
    normalized: str,
    limit: int,
    endpoint: str,
    user_agent: str,
) -> tuple[PlaceCandidate, ...]:
    params = urlencode(
        {
            "q": normalized,
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": limit,
        }
    )
    request = Request(
        f"{endpoint}?{params}",
        headers={"User-Agent": user_agent, "Accept": "application/json"},
    )
    global _LAST_UPSTREAM_REQUEST
    with _RATE_LOCK:
        now = time.monotonic()
        wait_seconds = _MIN_REQUEST_INTERVAL_SECONDS - (now - _LAST_UPSTREAM_REQUEST)
        if wait_seconds > 0:
            time.sleep(wait_seconds)
        with urlopen(request, timeout=12) as response:  # noqa: S310 - configured HTTPS endpoint
            raw: Any = json.loads(response.read().decode())
        _LAST_UPSTREAM_REQUEST = time.monotonic()
    if not isinstance(raw, list):
        raise RuntimeError("birthplace geocoder returned an unexpected response")
    results: list[PlaceCandidate] = []
    for row_any in raw:
        if not isinstance(row_any, dict):
            continue
        row = cast(dict[str, Any], row_any)
        try:
            latitude = float(row["lat"])
            longitude = float(row["lon"])
            display_name = str(row["display_name"])
            osm_type = str(row["osm_type"])
            osm_id = str(row["osm_id"])
        except (KeyError, TypeError, ValueError):
            continue
        timezone = timezone_for_coordinates(latitude, longitude)
        address = row.get("address")
        country_code = None
        if isinstance(address, dict) and isinstance(address.get("country_code"), str):
            country_code = str(address["country_code"]).casefold()
        results.append(
            PlaceCandidate(
                provider="OpenStreetMap Nominatim",
                provider_id=f"{osm_type}:{osm_id}",
                display_name=display_name,
                latitude=latitude,
                longitude=longitude,
                iana_timezone=timezone,
                country_code=country_code,
                category=str(row["category"]) if row.get("category") is not None else None,
                place_type=str(row["type"]) if row.get("type") is not None else None,
            )
        )
    return tuple(results)


def timezone_for_coordinates(latitude: float, longitude: float) -> str:
    module: Any = importlib.import_module("timezonefinder")
    finder = module.TimezoneFinder(in_memory=True)
    timezone = finder.timezone_at(lat=latitude, lng=longitude)
    if not isinstance(timezone, str) or not timezone:
        raise RuntimeError("could not resolve an IANA timezone for this birthplace")
    return timezone
