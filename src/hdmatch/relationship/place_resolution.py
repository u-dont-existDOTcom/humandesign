"""Participant-confirmed birthplace search with offline timezone resolution.

Only the birthplace query is sent to OpenStreetMap Nominatim. Birth date/time, email,
relationship responses, and hidden predictions never leave the application in this step.
"""

from __future__ import annotations

import importlib
import json
from dataclasses import dataclass
from typing import Any, cast
from urllib.parse import urlencode
from urllib.request import Request, urlopen

NOMINATIM_SEARCH = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "RelationshipPatternLab/0.1 (+https://u-dont-exist.com/)"


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
    params = urlencode(
        {
            "q": normalized,
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": limit,
        }
    )
    request = Request(
        f"{NOMINATIM_SEARCH}?{params}",
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urlopen(request, timeout=12) as response:  # noqa: S310 - fixed HTTPS endpoint
        raw: Any = json.loads(response.read().decode())
    if not isinstance(raw, list):
        raise RuntimeError("Nominatim returned an unexpected response")
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
        timezone = finder.closest_timezone_at(lat=latitude, lng=longitude)
    if not isinstance(timezone, str) or not timezone:
        raise RuntimeError("could not resolve an IANA timezone for this birthplace")
    return timezone
