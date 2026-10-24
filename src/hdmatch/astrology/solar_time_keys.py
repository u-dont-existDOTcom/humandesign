"""Swiss-file RA solar timing keys, independent of direction geometry.

GROUNDED MODEL: Gansten Primary Directions chapter 6 pp.73–80, prior
purchased-Kindle audit §4: Brahe = RA(Sun) across the two TRUE local solar
midnights bracketing birth (fixed birth-day rate); Placidus = elapsed
postnatal days until the moving Sun's accumulated RA increment equals the
directional arc. Compare https://mail.skyscript.co.uk/forums/viewtopic.php?t=4872
(author Gansten on Brahe/Kepler naming).

The geometrical midnight definition here is H_sun = 180° (geocentric
apparent RA and local sidereal time), *not* UTC midnight or a 24-hour
sample from the natal instant. We do NOT assert that the specific Swiss
nutation/UT/TT implementation is identically that of the 1573/17th-century
historical ephemerides.

Solar days map symbolically to years and are NOT directly historical calendar
anniversaries. No life outcomes/prediction fitting. Swiss .se1 returned flags
and actually used planetary file must be verified at every sample.
"""

from __future__ import annotations

import bisect
import copy
import importlib
import math
from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Any, cast

from hdmatch.chart.ephemeris import (
    _SWISS_LOCK,
    CelestialBody,
    SwissEphemerisProvider,
)

from .sky import DirectionBirthSnapshot
from .timeline import MODERN_MEAN_TROPICAL_YEAR_DAYS


class SolarTimeKey(StrEnum):
    BRAHE_TRUE_MIDNIGHT_BIRTH_DAY = "brahe_true_midnight_birth_day"
    PLACIDUS_CUMULATIVE_TRUE_SOLAR_RA = "placidus_cumulative_true_solar_ra"


class SolarTimeKeyDomainError(ValueError):
    """Time key unavailable without fabricating unobserved solar ephemeris."""


def _wrapped_signed(delta: float) -> float:
    return (delta + 180.0) % 360.0 - 180.0


@dataclass(frozen=True, slots=True)
class SolarKeyMetadata:
    solar_key: SolarTimeKey
    birth_utc: datetime
    longitude_east_deg: float
    brahe_midnight_start: datetime | None
    brahe_midnight_end: datetime | None
    brahe_birth_day_rate_deg: float | None
    astronomical_provenance: dict[str, object]
    mathematical_scope: str

    def to_dict(self) -> dict[str, object]:
        return {
            "method": self.solar_key.value,
            "birth_utc": self.birth_utc.isoformat(),
            "longitude_east_deg": self.longitude_east_deg,
            "true_solar_midnight_before_birth_utc": (
                self.brahe_midnight_start.isoformat() if self.brahe_midnight_start else None
            ),
            "true_solar_midnight_after_birth_utc": (
                self.brahe_midnight_end.isoformat() if self.brahe_midnight_end else None
            ),
            "true_solar_midnight_rate_deg_per_symbolic_year": self.brahe_birth_day_rate_deg,
            "ephemeris": self.astronomical_provenance,
            "original_historical_ephemeris_equivalence": "NOT VERIFIED",
            "sun_ra_coordinate_convention": self.mathematical_scope,
            "symbolic_year_calendar_days": MODERN_MEAN_TROPICAL_YEAR_DAYS,
            "authorities": (
                "Gansten 2009 Ch.6 pp.73-80 (from purchased-book research audit);"
                " Brahe 1573 original primary witness not re-read this pass"
            ),
            "not_a_forecast": True,
        }


class SolarRAEngine:
    """In-memory Swiss RA evaluator; no Moshier/DE-planet fallback permitted."""

    def __init__(
        self,
        birth: DirectionBirthSnapshot,
        ephemeris_directory: str | Path,
        *,
        _swe: Any | None = None,
    ) -> None:
        if not -180 <= birth.longitude_east_deg <= 180:
            raise ValueError("longitude outside east-positive [-180,180]")
        if birth.birth_utc.utcoffset() is None:
            raise ValueError("birth instant requires timezone")
        self.birth = birth
        self.birth_utc = birth.birth_utc.astimezone(UTC)
        self.root = Path(ephemeris_directory).expanduser().resolve()
        self.swe = _swe if _swe is not None else importlib.import_module("swisseph")
        self.strict = SwissEphemerisProvider(
            (self.root / "sepl_18.se1", self.root / "semo_18.se1"),
            _swe_module=self.swe,
        )
        manifest = {Path(rec.path).name: rec.sha256 for rec in self.strict.metadata.files}
        original = dict(birth.ephemeris_file_sha256)
        if manifest != original:
            raise SolarTimeKeyDomainError("natal and solar timing key ephemeris file hashes differ")
        self.ra_cache: dict[datetime, float] = {}
        self._daily_unwrapped: list[float] | None = None
        self.ra_birth = self.ra_at(self.birth_utc)

    def _jd(self, utc: datetime) -> float:
        return float(
            self.swe.julday(
                utc.year,
                utc.month,
                utc.day,
                (utc.hour + utc.minute / 60 + utc.second / 3600 + utc.microsecond / 3_600_000_000),
                self.swe.GREG_CAL,
            )
        )

    def ra_at(self, dt: datetime) -> float:
        if dt.tzinfo is None or dt.utcoffset() is None:
            raise ValueError("solar sample requires timezone-aware datetime")
        utc = dt.astimezone(UTC)
        if not 1800 <= utc.year < 2400:
            raise SolarTimeKeyDomainError("Swiss-file time key is restricted to 1800–2399 UTC")
        if utc in self.ra_cache:
            return self.ra_cache[utc]
        with _SWISS_LOCK:
            # Existing adapter checks the requested/returned Swiss mode,
            # actual loaded source file, and hashes the declared inputs.
            self.strict.position(CelestialBody.SUN, utc)
            self.swe.set_ephe_path(str(self.root))
            values, flags = self.swe.calc_ut(
                self._jd(utc),
                self.swe.SUN,
                int(self.swe.FLG_SWIEPH) | int(self.swe.FLG_EQUATORIAL),
            )
            if (
                flags & int(self.swe.FLG_MOSEPH)
                or not (flags & int(self.swe.FLG_SWIEPH))
                or not (flags & int(self.swe.FLG_EQUATORIAL))
            ):
                raise SolarTimeKeyDomainError(f"Sun RA returned incompatible mode flags {flags}")
            self.strict._verify_current_file(0, CelestialBody.SUN, utc)
        ra = float(values[0]) % 360.0
        if not math.isfinite(ra):
            raise SolarTimeKeyDomainError("non-finite solar RA")
        self.ra_cache[utc] = ra
        return ra

    def _sun_hour_angle_minus_180(self, dt: datetime) -> float:
        utc = dt.astimezone(UTC)
        jd = self._jd(utc)
        with _SWISS_LOCK:
            sidereal = float(self.swe.sidtime(jd)) * 15
        ra = self.ra_at(utc)
        h = (sidereal + self.birth.longitude_east_deg - ra) % 360
        return _wrapped_signed(h - 180.0)

    def _true_midnight_near(self, approximate_utc: datetime) -> datetime:
        """Find Sun's lower meridian transit from a local mean-midnight seed."""
        current = approximate_utc
        for _ in range(10):
            deviation = self._sun_hour_angle_minus_180(current)
            if abs(deviation) < 3e-7:
                return current
            # H_sun grows approximately 360 degrees per mean solar day.
            current -= timedelta(days=deviation / 360.0)
        if abs(self._sun_hour_angle_minus_180(current)) >= 4e-6:
            raise SolarTimeKeyDomainError("true solar midnight root did not converge")
        return current

    def brahe_midnights(self) -> tuple[datetime, datetime]:
        lon = self.birth.longitude_east_deg
        local_mean_date = (self.birth_utc + timedelta(hours=lon / 15.0)).date()
        civil_mean_midnight_utc = datetime.combine(
            local_mean_date, time(0), tzinfo=UTC
        ) - timedelta(hours=lon / 15.0)
        previous = self._true_midnight_near(civil_mean_midnight_utc)
        if previous > self.birth_utc:
            previous = self._true_midnight_near(civil_mean_midnight_utc - timedelta(days=1))
        next_ = self._true_midnight_near(previous + timedelta(days=1))
        if not previous <= self.birth_utc < next_:
            raise SolarTimeKeyDomainError("failed to bracket birth by true midnights")
        if not 23.95 < (next_ - previous).total_seconds() / 3600 < 24.05:
            raise SolarTimeKeyDomainError("solar midnight interval unexpectedly large")
        return previous, next_

    def birth_date_brahe_rate(self) -> tuple[float, datetime, datetime]:
        low, high = self.brahe_midnights()
        delta = (self.ra_at(high) - self.ra_at(low)) % 360.0
        if not 0.85 < delta < 1.15:
            raise SolarTimeKeyDomainError("solar RA over birth-day beyond domain")
        return delta, low, high

    def _build_daily(self) -> list[float]:
        if self._daily_unwrapped is not None:
            return self._daily_unwrapped
        values = [
            (self.ra_at(self.birth_utc + timedelta(days=d)) - self.ra_birth) % 360.0
            for d in range(126)
        ]
        if values[0] != 0.0:
            raise SolarTimeKeyDomainError("zero-age solar RA is not zero")
        if not all(0.8 < nxt - prev < 1.15 for prev, nxt in zip(values, values[1:], strict=False)):
            raise SolarTimeKeyDomainError(
                "true-solar accumulated motion is not monotonically positive"
            )
        self._daily_unwrapped = values
        return values

    def true_solar_arc_at_age(self, symbolic_years: float) -> float:
        if not math.isfinite(symbolic_years) or not 0 <= symbolic_years <= 125:
            raise ValueError("model years must be 0..125")
        day = int(symbolic_years)
        if symbolic_years == day:
            return self._build_daily()[day]
        ra = self.ra_at(self.birth_utc + timedelta(days=symbolic_years))
        return (ra - self.ra_birth) % 360.0

    def placidus_age_for_arc(self, arc_deg: float) -> float:
        if not math.isfinite(arc_deg) or not 0 <= arc_deg <= 125:
            raise ValueError("direction arc must be within [0,125] degrees")
        values = self._build_daily()
        if arc_deg > values[-1]:
            raise SolarTimeKeyDomainError("directional arc outside 125-day solar range")
        if arc_deg == 0:
            return 0.0
        high_day = bisect.bisect_left(values, arc_deg)
        if values[high_day] == arc_deg:
            return float(high_day)
        lower, upper = float(high_day - 1), float(high_day)
        for _ in range(33):
            center = (lower + upper) / 2
            solar_arc = self.true_solar_arc_at_age(center)
            if solar_arc < arc_deg:
                lower = center
            else:
                upper = center
        result = (lower + upper) / 2
        if abs(self.true_solar_arc_at_age(result) - arc_deg) > 2e-7:
            raise SolarTimeKeyDomainError("solar inversion residual too large")
        return result

    def metadata(self, profile: SolarTimeKey) -> SolarKeyMetadata:
        profile = SolarTimeKey(profile)
        rate = before = after = None
        if profile is SolarTimeKey.BRAHE_TRUE_MIDNIGHT_BIRTH_DAY:
            rate, before, after = self.birth_date_brahe_rate()
        return SolarKeyMetadata(
            solar_key=profile,
            birth_utc=self.birth_utc,
            longitude_east_deg=self.birth.longitude_east_deg,
            brahe_midnight_start=before,
            brahe_midnight_end=after,
            brahe_birth_day_rate_deg=rate,
            astronomical_provenance=self.birth.provenance(),
            mathematical_scope=(
                "geocentric apparent Sun RA, tropical equator/equinox of date; "
                "Swiss SWIEPH UT with TT internally resolved, local true midnight "
                "defined by solar lower-meridian transit (Sun H=180°)"
            ),
        )


def apply_solar_key(
    report: dict[str, object],
    engine: SolarRAEngine,
    profile: SolarTimeKey,
    *,
    requested_max_age: float,
) -> dict[str, object]:
    """Re-date an oversampled arc list without altering geometric solutions.

    Caller MUST generate the geometric candidates using a 125° degree-based
    age window, because a 100-symbolic-year solar key can consume ~103°.
    This tool requires a requested <=100 years to prove completeness from
    the 125° geometric preselection. The output retains source baseline
    coverage plus newly filtered candidates.
    """
    if not math.isfinite(requested_max_age) or not 0 < requested_max_age <= 100:
        raise ValueError("solar profiles presently support (0,100] years")
    profile = SolarTimeKey(profile)
    data = copy.deepcopy(report)
    coverage = data.get("coverage")
    if not isinstance(coverage, dict):
        raise ValueError("missing geometric candidate coverage")
    if float(coverage.get("max_symbolic_age_years", float("nan"))) != 125:
        raise ValueError("source geometry must be generated with 125° arc window")
    directions = data.get("directions")
    if not isinstance(directions, list):
        raise ValueError("missing geometric contact records")
    settings = engine.metadata(profile)
    rate = settings.brahe_birth_day_rate_deg
    accepted: list[dict[str, object]] = []
    additional_outside = 0
    for item in directions:
        if not isinstance(item, dict):
            raise ValueError("invalid geometric contact record")
        arc = float(item["arc_degrees"])
        if profile is SolarTimeKey.BRAHE_TRUE_MIDNIGHT_BIRTH_DAY:
            assert rate is not None
            symbolic_age = arc / rate
        else:
            # For solar motion after birth, early eligibility cutoff avoids
            # spending on contacts that are already too late for the window.
            if arc > engine.true_solar_arc_at_age(requested_max_age) + 1e-9:
                additional_outside += 1
                continue
            symbolic_age = engine.placidus_age_for_arc(arc)
        if symbolic_age > requested_max_age:
            additional_outside += 1
            continue
        item["symbolic_age_years"] = symbolic_age
        item["model_date_utc"] = (
            engine.birth_utc + timedelta(days=symbolic_age * MODERN_MEAN_TROPICAL_YEAR_DAYS)
        ).isoformat()
        item["time_key"] = profile.value
        accepted.append(item)
    accepted.sort(
        key=lambda a: (
            cast(float, a["symbolic_age_years"]),
            str(a.get("method", "")),
            str(a.get("promissor", "")),
            str(a.get("significator", "")),
            str(a.get("aspect", a.get("ray_aspect", ""))),
            str(a.get("ray_offset_branch", "")),
        )
    )
    data["directions"] = accepted
    if "accepted_records" in coverage:
        coverage["accepted_records"] = len(accepted)
        coverage["outside_age_window"] = (
            int(coverage.get("outside_age_window", 0)) + additional_outside
        )
    else:
        coverage["accepted"] = len(accepted)
        coverage["out_of_window" if "out_of_window" in coverage else "outside_age_window"] = (
            cast(int, coverage.get("out_of_window", coverage.get("outside_age_window", 0)))
            + additional_outside
        )
    coverage["max_symbolic_age_years"] = requested_max_age
    coverage["source_geometric_oversample_arc_degrees"] = 125.0
    data["solar_time_key"] = settings.to_dict()
    data["status"] = "RESEARCH_SOLAR_KEY_GEOMETRIC_RETIMER_NOT_PREDICTIVE_VALIDATION"
    for key in ("technique_provenance", "method_provenance", "movement_provenance"):
        metadata = data.get(key)
        if isinstance(metadata, dict):
            metadata["time_key"] = profile.value
            metadata.pop("time_key_degrees_per_symbolic_year", None)
            metadata.pop("degrees_per_symbolic_year", None)
            metadata["key_rate_interpretation"] = (
                "birth-day constant solar RA rate"
                if rate is not None
                else "variable cumulative solar RA, numerically inverted for each arc"
            )
            metadata["historical_calendar_policy"] = (
                "modern 365.2422-day model conversion, not a historical anniversary"
            )
    return data
