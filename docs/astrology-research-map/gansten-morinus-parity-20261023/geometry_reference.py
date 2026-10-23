"""Research-only, frozen-coordinate spherical-geometry comparison.

Independent implementations for Gansten audit's synthetic example 1.
This is NOT a production primary-direction engine, historical-authority
certificate, or forecast model. No birth date/ephemeris is used.

Inputs are declinations, right ascensions and local RAMC in *degrees*.
Phase and Regiomontanian functions cover ordinary rising/setting geometry.
The Placidean under-pole formula implements only the source audit's
northern/eastern/above-horizon demonstration branch.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import acos, asin, atan, atan2, cos, degrees, radians, sin, sqrt, tan

TOL = 1e-12


class DomainError(ValueError):
    """No standard solution for this branch/domain, not a zero-angle result."""


@dataclass(frozen=True)
class EquatorialPoint:
    ra_deg: float
    dec_deg: float


def normalize(angle: float) -> float:
    return angle % 360.0


def _d_sin(v: float) -> float:
    return sin(radians(v))


def _d_cos(v: float) -> float:
    return cos(radians(v))


def _d_tan(v: float) -> float:
    return tan(radians(v))


def _asin_deg(v: float) -> float:
    if abs(v) > 1.0 + TOL:
        raise DomainError('no ordinary horizon crossing / inverse sine outside domain')
    return degrees(asin(max(-1.0, min(1.0, v))))


def ascensional_difference(latitude_deg: float, declination_deg: float) -> float:
    if abs(latitude_deg) >= 90 or abs(declination_deg) >= 90:
        raise DomainError('pole or celestial pole requires a separate construction')
    return _asin_deg(_d_tan(latitude_deg) * _d_tan(declination_deg))


def semi_arcs(latitude_deg: float, dec_deg: float) -> tuple[float, float]:
    ad = ascensional_difference(latitude_deg, dec_deg)
    return 90.0 + ad, 90.0 - ad


def phase(hour_angle_deg: float, dsa: float, nsa: float) -> float:
    """Natal position in normalized diurnal quarters; MC=0, Desc=90, IC=180, Asc=270."""
    h = normalize(hour_angle_deg)
    if h <= dsa:
        return 90.0 * h / dsa
    if h <= 180.0:
        return 90.0 + 90.0 * (h-dsa) / nsa
    if h <= 360.0-dsa:
        return 180.0 + 90.0 * (h-180.0) / nsa
    return 270.0 + 90.0 * (h-360.0+dsa) / dsa


def hour_angle_from_phase(position: float, dsa: float, nsa: float) -> float:
    u = normalize(position)
    if u <= 90:
        return u * dsa / 90.0
    if u <= 180:
        return dsa + (u-90.0) * nsa / 90.0
    if u <= 270:
        return 180.0 + (u-180.0) * nsa / 90.0
    return 360.0 - dsa + (u-270.0) * dsa / 90.0


def proportional_semi_arc_direction(
    lat: float, ramc: float, fixed: EquatorialPoint, moving: EquatorialPoint
) -> float:
    """First forward-rotation contact at equal normalized semi-arc phase."""
    fa, fb = semi_arcs(lat, fixed.dec_deg)
    ma, mb = semi_arcs(lat, moving.dec_deg)
    u = phase(ramc-fixed.ra_deg, fa, fb)
    target_h = hour_angle_from_phase(u, ma, mb)
    return normalize(moving.ra_deg + target_h - ramc)


def _point_vector(p: EquatorialPoint) -> tuple[float, float, float]:
    return (_d_cos(p.dec_deg)*_d_cos(p.ra_deg),
            _d_cos(p.dec_deg)*_d_sin(p.ra_deg),
            _d_sin(p.dec_deg))


def _cross(a: tuple[float,float,float], b: tuple[float,float,float]) -> tuple[float,float,float]:
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def _dot(a: tuple[float,float,float], b: tuple[float,float,float]) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def position_circle_residual(
    lat: float, ramc: float, fixed: EquatorialPoint, moving: EquatorialPoint, arc: float
) -> float:
    n_horizon = (-_d_sin(lat)*_d_cos(ramc),
                 -_d_sin(lat)*_d_sin(ramc), _d_cos(lat))
    norm = _cross(n_horizon, _point_vector(fixed))
    rotated = EquatorialPoint(moving.ra_deg-arc, moving.dec_deg)
    return _dot(norm, _point_vector(rotated))


def regiomontanus_position_circle_direction(
    lat: float, ramc: float, fixed: EquatorialPoint, moving: EquatorialPoint
) -> float:
    """Cartesian independent plane-intersection, no Regio auxiliary pole formulas.

    The great circle passes through the fixed point and north/south horizon
    points. Reject the antipodal semicircle. Returns first forward crossing.
    """
    if abs(lat) >= 90 or abs(fixed.dec_deg) >= 90 or abs(moving.dec_deg) >= 90:
        raise DomainError('singular geographic/celestial poles')
    north = (-_d_sin(lat)*_d_cos(ramc),
             -_d_sin(lat)*_d_sin(ramc), _d_cos(lat))
    s = _point_vector(fixed)
    normal = _cross(north, s)
    normal_len = sqrt(_dot(normal,normal))
    if normal_len < TOL:
        raise DomainError('position circle undefined when fixed equals horizon pole')
    # Fixed-side semicircle basis perpendicular to the northern horizon point.
    ns = _dot(north,s)
    fixed_half = tuple(s[i]-ns*north[i] for i in range(3))
    horiz_len = sqrt(normal[0]**2+normal[1]**2)
    if horiz_len < TOL:
        raise DomainError('underdetermined polar position circle')
    cos_arg = -normal[2] * _d_tan(moving.dec_deg) / horiz_len
    if abs(cos_arg) > 1 + TOL:
        raise DomainError('moving declination does not intersect position circle')
    v = acos(max(-1.0,min(1.0,cos_arg)))
    gamma = atan2(normal[1], normal[0])
    solutions = []
    for angle in (gamma+v, gamma-v):
        crossed_ra = degrees(angle)
        arc = normalize(moving.ra_deg-crossed_ra)
        crossed_vec = _point_vector(EquatorialPoint(crossed_ra,moving.dec_deg))
        if _dot(crossed_vec,fixed_half) > TOL:
            if abs(position_circle_residual(lat,ramc,fixed,moving,arc)) > 1e-9:
                raise AssertionError('Cartesian circle residual failed')
            solutions.append(arc)
    if not solutions:
        raise DomainError('no intersection with required fixed-side semicircle')
    return min(solutions)


def placidean_under_pole_east_upper_north(
    lat: float, ramc: float, fixed: EquatorialPoint, moving: EquatorialPoint
) -> float:
    """Only 0 < lat < 90 and fixed strictly EAST ABOVE upper meridian.

    The general Placidean solver requires independent all-quadrant equations.
    Avoid accidentally reusing this demonstrator in unsupported quadrants.
    """
    if not 0 < lat < 90 or abs(fixed.dec_deg) >= 90:
        raise DomainError('branch requires northern latitude and nonpolar fixed point')
    ad_s = ascensional_difference(lat, fixed.dec_deg)
    dsa = 90+ad_s
    md = normalize(fixed.ra_deg-ramc)
    if not 0 < md < dsa:
        raise DomainError('fixed point must be east and above the upper meridian')
    r = md / dsa
    if abs(fixed.dec_deg) < 1e-10:
        pole = degrees(atan(r*_d_tan(lat)))
    else:
        pole = degrees(atan(_d_sin(r*ad_s)/_d_tan(fixed.dec_deg)))
    ad_sp = ascensional_difference(pole,fixed.dec_deg)
    ad_mp = ascensional_difference(pole,moving.dec_deg)
    return normalize((moving.ra_deg-ad_mp) - (fixed.ra_deg-ad_sp))


def ptolemy_rounded_linear_interpolation(meridian_arc: float, setting_arc: float,
                                          hours_west_of_meridian: float) -> float:
    """His stated interpolation SHORTCUT, not proportional phase geometry."""
    if not 0 <= hours_west_of_meridian <= 6:
        raise DomainError('rounded shortcut defined only within selected quadrant')
    return meridian_arc + hours_west_of_meridian / 6 * (setting_arc-meridian_arc)


def one_degree_per_year(arc_deg: float) -> float:
    return arc_deg


def rational_mean_solar_years(arc_deg: float) -> float:
    """Modern exact 360/365.25 diagnostic; NOT identical to Lilly printed Naibod tables."""
    return arc_deg*365.25/360.0
