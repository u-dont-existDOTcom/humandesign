"""Historically separated movement roles and zodiacal-aspect ownership.

SOURCE BASIS: Martin Gansten, Primary Directions (2009), as independently
paraphrased in the previously reviewed purchased-book audit
GANSTEN_PRIMARY_DIRECTIONS_AUDIT.md:
  Ch.1 pp.5-7, note pp.9-10: moving promissor / significator roles.
  Ch.5 pp.65-71, Ch.8 pp.88-101: zodiacal aspect placement, competing
  direction and converse traditions, aspects of the significator.
  Audit lines 76-80, 110-116 and 174: NEVER infer traditional converse
  from a mere negative arc; a zodiacal aspect is placed in longitude.

These are deliberately limited, model-separated geometric candidates,
NOT one historically universal prediction rule. In particular, zodiacal
aspects OF the significator are documented as a distinct and disputed
experimental construction, and are NOT enabled in role-reversed converse.
Bianchini latitude rays, planetary motion after birth, historically precise
key tables and point/house interpretations remain unsupported.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import timedelta
from enum import StrEnum

from .aspect_points import (
    RayAspect,
    RayBranch,
    aspect_branches,
    ecliptic_to_equatorial,
    zodiacal_promissor_ray,
)
from .aspect_timeline import SignificatorProjection
from .geometry import (
    GeometryMethod,
    GeometryUnavailable,
    direction_arc,
    normalize,
)
from .sky import CLASSICAL_BODIES, DirectionBirthSnapshot
from .timeline import MODERN_MEAN_TROPICAL_YEAR_DAYS, TimeKey, degrees_per_symbolic_year


class ContactConstruction(StrEnum):
    BODY_CONJUNCTION = "bodily_conjunction"
    ZODIACAL_PROMISSOR_RAY = "zodiacal_promissor_ray"
    ZODIACAL_SIGNIFICATOR_ASPECT = "zodiacal_significator_aspect"


class RotationRegime(StrEnum):
    DIRECT_PRIMARY_MOTION = "direct_primary_motion"
    TRADITIONAL_ROLE_REVERSED_CONVERSE = "traditional_role_reversed_converse"
    MODERN_REVERSE_ROTATION_DIAGNOSTIC = "modern_reverse_rotation_diagnostic"


@dataclass(frozen=True, slots=True)
class RoleDirectionRecord:
    method: str
    time_key: str
    construction: str
    rotation_regime: str
    promissor: str
    significator: str
    ray_owner: str | None
    aspect: str | None
    aspect_offset_branch: str | None
    ray_longitude_deg: float | None
    ray_latitude_deg: float | None
    significator_projection: str
    geometric_fixed_point: str
    geometric_moving_point: str
    original_forward_arc_deg: float
    arc_degrees: float
    rotation_label: str
    symbolic_age_years: float
    model_date_utc: str

    def to_dict(self) -> dict[str, str | float | None]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RoleTimeline:
    natal: DirectionBirthSnapshot
    construction: ContactConstruction
    regime: RotationRegime
    significator_projection: SignificatorProjection
    time_key: TimeKey
    methods: tuple[GeometryMethod, ...]
    max_age_years: float
    directions: tuple[RoleDirectionRecord, ...]
    evaluated: int
    rejected_by_reason: tuple[tuple[str, int], ...]
    outside_age_window: int

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": "astro-primary-direction-role-variants-v1",
            "status": "RESEARCH_GEOMETRY_NOT_HISTORICAL_CERTIFICATION_OR_PREDICTIVE_VALIDATION",
            "birth": {
                "utc": self.natal.birth_utc.isoformat(),
                "latitude_north_deg": self.natal.latitude_deg,
                "longitude_east_deg": self.natal.longitude_east_deg,
                "ramc_deg": self.natal.ramc_deg,
            },
            "astronomy_provenance": self.natal.provenance(),
            "movement_provenance": {
                "construction": self.construction.value,
                "rotation_regime": self.regime.value,
                "method_names": [x.value for x in self.methods],
                "significator_projection": self.significator_projection.value,
                "allowed_latitude": (
                    "zodiacal aspect rays are on beta=0, with bodily source coordinates"
                ),
                "source_basis": (
                    "Gansten 2009, audited Ch.1 pp.5-7; Ch.5 pp.65-71; Ch.8 pp.88-101; "
                    "this is a mathematical reconstruction, not an endorsement "
                    "of all historical rulership/aspect selection methods"
                ),
                "regime_meaning": {
                    RotationRegime.DIRECT_PRIMARY_MOTION: (
                        "moving physical promissor or its constructed zodiacal ray "
                        "toward a fixed natal significator/its constructed ray"
                    ),
                    RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE: (
                        "fixed promissor (or its fixed zodiacal ray); natal "
                        "significator is the moving point, still forward primary motion"
                    ),
                    RotationRegime.MODERN_REVERSE_ROTATION_DIAGNOSTIC: (
                        "modern reversed-angular-motion candidate, no role swap; "
                        "360° minus forward arc, separately named and not traditional converse"
                    ),
                }[self.regime],
                "is_significator_aspect_experimental": (
                    self.construction is ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT
                ),
                "role_label_duplicate_geometry": (
                    "For bodily unprojected zodiacal ray constructions, traditional "
                    "role-reversed promissor rays and direct significator aspects "
                    "can have the same arcs with planet labels exchanged. Do not "
                    "treat them as independent empirical events."
                    if self.construction is ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT
                    or (
                        self.construction is ContactConstruction.ZODIACAL_PROMISSOR_RAY
                        and self.regime is RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE
                        and self.significator_projection is SignificatorProjection.RETAIN_BODILY
                    )
                    else None
                ),
                "moving_angles_not_supported": True,
                "time_key": self.time_key.value,
                "degrees_per_symbolic_year": degrees_per_symbolic_year(self.time_key),
                "date_conversion_days_per_model_year": MODERN_MEAN_TROPICAL_YEAR_DAYS,
                "unsupported": [
                    "physical movement of MC/ASC (rather than a newly sourced natal degree)",
                    "traditional converse of significator rays",
                    "Bianchini/Morin ray-latitude constructions",
                    "mundane Regiomontanian rays and non-conjunction mundane phase variants",
                    "literal Naibod printed tables and other historical time keys",
                    "Moon secondary motion, Fortune, bounds, stars, hyleg, interpretive rules",
                ],
            },
            "coverage": {
                "evaluated": self.evaluated,
                "accepted": len(self.directions),
                "out_of_window": self.outside_age_window,
                "unavailable": dict(self.rejected_by_reason),
                "max_symbolic_age_years": self.max_age_years,
            },
            "directions": [record.to_dict() for record in self.directions],
        }


def _aspect_specs(
    construction: ContactConstruction,
    aspects: Iterable[RayAspect] | None,
) -> tuple[tuple[RayAspect | None, RayBranch | None], ...]:
    if construction is ContactConstruction.BODY_CONJUNCTION:
        if aspects is not None:
            raise ValueError("bodily conjunction construction accepts no aspect-ray selection")
        return ((None, None),)
    names = tuple(
        dict.fromkeys(RayAspect(a) for a in (aspects if aspects is not None else tuple(RayAspect)))
    )
    if not names:
        raise ValueError("ray construction requires at least one aspect")
    return tuple((a, branch) for a in names for branch in aspect_branches(a))


def generate_role_timeline(
    natal: DirectionBirthSnapshot,
    *,
    construction: ContactConstruction,
    regime: RotationRegime,
    methods: Iterable[GeometryMethod] = tuple(GeometryMethod),
    aspects: Iterable[RayAspect] | None = None,
    significator_projection: SignificatorProjection = SignificatorProjection.RETAIN_BODILY,
    time_key: TimeKey = TimeKey.PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR,
    max_age_years: float = 100.0,
) -> RoleTimeline:
    """Compute audited role variants as different algorithms, not sign aliases.

    These regime-specific outputs must not be pooled as independent predictive
    successes or tuned using real-life outcomes.
    """
    construction = ContactConstruction(construction)
    regime = RotationRegime(regime)
    projection = SignificatorProjection(significator_projection)
    key = TimeKey(time_key)
    methods = tuple(dict.fromkeys(GeometryMethod(x) for x in methods))
    if not methods:
        raise ValueError("at least one geometry method is required")
    if not math.isfinite(max_age_years) or not 0 < max_age_years <= 125:
        raise ValueError("max_age_years must be finite within (0,125]")
    aspect_specs = _aspect_specs(construction, aspects)
    if (
        construction is ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT
        and regime is not RotationRegime.DIRECT_PRIMARY_MOTION
    ):
        raise ValueError(
            "zodiacal significator aspects are supported for direct motion only; "
            "traditional role-reversed aspect semantics are unresolved"
        )
    if (
        construction is not ContactConstruction.ZODIACAL_PROMISSOR_RAY
        and projection is not SignificatorProjection.RETAIN_BODILY
    ):
        raise ValueError("this construction does not support significator projection")
    if construction is not ContactConstruction.BODY_CONJUNCTION:
        if natal.true_obliquity_deg is None:
            raise ValueError("zodiacal aspects require verified true obliquity-of-date")
        needed = {x.value for x in CLASSICAL_BODIES}
        if not needed.issubset(natal.ecliptic_lookup()):
            raise ValueError("zodiacal aspects require verified planetary ecliptic longitude")

    body_names = tuple(x.value for x in CLASSICAL_BODIES)
    points = natal.lookup()
    if not set(body_names + ("asc", "mc")).issubset(points):
        raise ValueError("missing natal classical planet or angle coordinates")
    ecl = natal.ecliptic_lookup()
    output: list[RoleDirectionRecord] = []
    errors: dict[str, int] = {}
    evaluated = excluded = 0

    for prom_name in body_names:
        for sig_name in body_names + ("asc", "mc"):
            if prom_name == sig_name:
                continue
            if regime is RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE and sig_name in (
                "asc",
                "mc",
            ):
                # An angle is a meridian/horizon circle. Moving it as a
                # point is an additional natal-longitude construction.
                continue
            if construction is ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT and sig_name in (
                "asc",
                "mc",
            ):
                # Angles are great circles, not zodiacal bodies.
                continue

            body_prom = points[prom_name]
            body_sig = points[sig_name]
            sign_projection = (
                "exact_angle"
                if sig_name in ("asc", "mc")
                else SignificatorProjection.RETAIN_BODILY.value
            )
            if (
                construction is ContactConstruction.ZODIACAL_PROMISSOR_RAY
                and projection is SignificatorProjection.PROJECT_TO_ECLIPTIC
                and sig_name not in ("asc", "mc")
            ):
                longitude, _latitude = ecl[sig_name]
                assert natal.true_obliquity_deg is not None
                body_sig = ecliptic_to_equatorial(longitude, 0, natal.true_obliquity_deg)
                sign_projection = SignificatorProjection.PROJECT_TO_ECLIPTIC.value

            for aspect, branch in aspect_specs:
                moving_prom, fixed_sig = body_prom, body_sig
                ray_owner: str | None = None
                ray_lon: float | None = None
                ray_lat: float | None = None
                if aspect is not None and branch is not None:
                    assert natal.true_obliquity_deg is not None
                    owner_name = (
                        sig_name
                        if construction is ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT
                        else prom_name
                    )
                    longitude, _latitude = ecl[owner_name]
                    ray = zodiacal_promissor_ray(
                        longitude,
                        aspect=aspect,
                        branch=branch,
                        obliquity_deg=natal.true_obliquity_deg,
                    )
                    ray_owner = owner_name
                    ray_lon, ray_lat = ray.ecliptic_longitude_deg, ray.ecliptic_latitude_deg
                    if construction is ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT:
                        fixed_sig = ray.equatorial
                        sign_projection = "constructed_significator_zodiacal_aspect_beta_zero"
                    else:
                        moving_prom = ray.equatorial

                if regime is RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE:
                    fixed, moving = moving_prom, fixed_sig
                    fixed_id = "natal_promissor_ray" if ray_owner else "natal_promissor_body"
                    moving_id = "natal_significator_body"
                    label = "traditional_role_reversed_converse"
                else:
                    fixed, moving = fixed_sig, moving_prom
                    fixed_id = (
                        "natal_significator_aspect"
                        if construction is ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT
                        else (
                            "natal_angle_circle"
                            if sig_name in ("asc", "mc")
                            else "natal_significator_body"
                        )
                    )
                    moving_id = (
                        "promissor_zodiacal_ray"
                        if construction is ContactConstruction.ZODIACAL_PROMISSOR_RAY
                        else "natal_promissor_body"
                    )
                    label = (
                        "direct_primary_motion"
                        if regime is RotationRegime.DIRECT_PRIMARY_MOTION
                        else "modern_reverse_rotation_converse"
                    )

                for method in methods:
                    evaluated += 1
                    try:
                        raw = direction_arc(
                            method, natal.latitude_deg, natal.ramc_deg, fixed, moving
                        )
                    except GeometryUnavailable as exc:
                        why = f"{method.value}:{exc}"
                        errors[why] = errors.get(why, 0) + 1
                        continue
                    arc = (
                        normalize(360 - raw)
                        if regime is RotationRegime.MODERN_REVERSE_ROTATION_DIAGNOSTIC
                        else raw
                    )
                    age = arc / degrees_per_symbolic_year(key)
                    if age > max_age_years:
                        excluded += 1
                        continue
                    result_date = natal.birth_utc + timedelta(
                        days=age * MODERN_MEAN_TROPICAL_YEAR_DAYS
                    )
                    output.append(
                        RoleDirectionRecord(
                            method=method.value,
                            time_key=key.value,
                            construction=construction.value,
                            rotation_regime=regime.value,
                            promissor=prom_name,
                            significator=sig_name,
                            ray_owner=ray_owner,
                            aspect=aspect.value if aspect is not None else None,
                            aspect_offset_branch=branch.value if branch is not None else None,
                            ray_longitude_deg=ray_lon,
                            ray_latitude_deg=ray_lat,
                            significator_projection=sign_projection,
                            geometric_fixed_point=fixed_id,
                            geometric_moving_point=moving_id,
                            original_forward_arc_deg=raw,
                            arc_degrees=arc,
                            rotation_label=label,
                            symbolic_age_years=age,
                            model_date_utc=result_date.isoformat(),
                        )
                    )
    output.sort(
        key=lambda x: (
            x.symbolic_age_years,
            x.method,
            x.promissor,
            x.significator,
            x.aspect or "",
            x.aspect_offset_branch or "",
        )
    )
    return RoleTimeline(
        natal=natal,
        construction=construction,
        regime=regime,
        significator_projection=projection,
        time_key=key,
        methods=methods,
        max_age_years=max_age_years,
        directions=tuple(output),
        evaluated=evaluated,
        rejected_by_reason=tuple(sorted(errors.items())),
        outside_age_window=excluded,
    )
