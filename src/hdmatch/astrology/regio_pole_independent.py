"""Independent Regiomontanian pole reconstruction, NOT a full Lilly model.

Mathematical procedure follows Rumen Kolev, 'William Lilly and the
Algorithm for His Primary Directions', pp.12-19, verified against
his published numeric example. Argoli's public-domain 1667 'Primi
mobilis tabulae', pp.3,7 and further chapters, documents the earlier
Regiomontanian rational/position-circle framework but this secondary
modern algebra is NOT silently attributed verbatim to Argoli 1610.

Only stationary equatorial significator/promissor; no zodiacal ray,
Moon's dynamic latitude, timing key, radix strength or human forecast.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

from .geometry import EquatorialPoint

_DEG = math.pi / 180.0


class PoleGeometryUnavailable(ValueError):
    """Fictitious horizon is singular, unattainable or ambiguous."""


@dataclass(frozen=True, slots=True)
class RegioPoleConstruction:
    quadrant: str
    sign_above_horizon: bool
    west_of_meridian: bool
    meridian_distance_deg: float
    zenith_distance_deg: float
    significator_pole_deg: float
    significator_ascensional_difference_deg: float
    ramc_under_pole_deg: float
    promissor_ascensional_difference_deg: float
    promissor_ascensional_coordinate_deg: float
    horizon_ascensional_coordinate_deg: float
    forward_arc_deg: float
    method_provenance: str = "KOLEV_SECONDARY_RECONSTRUCTION_NOT_EXACT_1610_ARGOLI"

    def to_dict(self) -> dict[str, str | float | bool]:
        return asdict(self)


def _asin_deg(value: float) -> float:
    if not math.isfinite(value) or abs(value) > 1 + 1e-11:
        raise PoleGeometryUnavailable("no real ascensional difference under this pole")
    return math.degrees(math.asin(max(-1.0, min(1.0, value))))


def _normal(deg: float) -> float:
    return deg % 360.0


def independent_regio_pole_arc(
    latitude_deg: float,
    ramc_deg: float,
    significator: EquatorialPoint,
    promissor: EquatorialPoint,
) -> RegioPoleConstruction:
    """Reconstruct the fixed-position-circle arc with an explicit pole.

    Implements the modern Kolev worked construction through zenith distance,
    hypothetical pole, ascensional differences and the fictitious horizon.
    The current position-circle vector engine is NOT called here.
    """
    values = (
        latitude_deg,
        ramc_deg,
        significator.ra_deg,
        significator.dec_deg,
        promissor.ra_deg,
        promissor.dec_deg,
    )
    if any(not math.isfinite(x) for x in values):
        raise ValueError("all astronomical inputs must be finite")
    if not -66 < latitude_deg < 66:
        raise ValueError("research domain excludes polar Placidus zones")
    if not 0 <= ramc_deg < 360:
        raise ValueError("RAMC must be normalized to [0, 360)")
    if not all(0 <= ra < 360 for ra in (significator.ra_deg, promissor.ra_deg)):
        raise ValueError("right ascensions must be normalized to [0, 360)")
    if not all(abs(dec) < 90 for dec in (significator.dec_deg, promissor.dec_deg)):
        raise ValueError("declinations must be strictly within (-90, 90)")

    hour = (ramc_deg - significator.ra_deg + 180.0) % 360.0 - 180.0
    if abs(math.sin(hour * _DEG)) <= 1e-12:
        raise PoleGeometryUnavailable("meridian direction branch is undefined")
    latitude = latitude_deg * _DEG
    dec = significator.dec_deg * _DEG
    ha = hour * _DEG
    sin_altitude = math.sin(latitude) * math.sin(dec) + math.cos(latitude) * math.cos(
        dec
    ) * math.cos(ha)
    if abs(sin_altitude) <= 1e-12:
        raise PoleGeometryUnavailable("significator is on the horizon")
    above = sin_altitude > 0
    west = hour > 0
    meridian_distance = 180.0 - abs(hour) if above else abs(hour)
    signed_declination = (
        significator.dec_deg * (1 if latitude_deg >= 0 else -1) * (1 if above else -1)
    )
    absolute_latitude = abs(latitude_deg) * _DEG
    numerator = math.tan(signed_declination * _DEG) * math.sin(absolute_latitude) - math.cos(
        absolute_latitude
    ) * math.cos(meridian_distance * _DEG)
    zenith_distance = 90.0 - math.degrees(math.atan2(numerator, math.sin(meridian_distance * _DEG)))
    pole = _asin_deg(math.sin(latitude) * math.sin(zenith_distance * _DEG))
    sig_ad = _asin_deg(math.tan(dec) * math.tan(pole * _DEG))
    diurnal_semiarc = 90.0 + sig_ad
    pole_ramc = _normal(
        significator.ra_deg + diurnal_semiarc if west else significator.ra_deg - diurnal_semiarc
    )
    prom_ad = _asin_deg(math.tan(promissor.dec_deg * _DEG) * math.tan(pole * _DEG))
    prom_coordinate = _normal(promissor.ra_deg + prom_ad if west else promissor.ra_deg - prom_ad)
    horizon_coordinate = _normal(pole_ramc - 90.0 if west else pole_ramc + 90.0)
    return RegioPoleConstruction(
        quadrant=("west_" if west else "east_") + ("above" if above else "below"),
        sign_above_horizon=above,
        west_of_meridian=west,
        meridian_distance_deg=meridian_distance,
        zenith_distance_deg=zenith_distance,
        significator_pole_deg=pole,
        significator_ascensional_difference_deg=sig_ad,
        ramc_under_pole_deg=pole_ramc,
        promissor_ascensional_difference_deg=prom_ad,
        promissor_ascensional_coordinate_deg=prom_coordinate,
        horizon_ascensional_coordinate_deg=horizon_coordinate,
        forward_arc_deg=_normal(prom_coordinate - horizon_coordinate),
    )
