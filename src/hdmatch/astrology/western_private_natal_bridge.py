"""Private-input adapter for a RESEARCH-ONLY modern Western direction model.

Uses source-verified seven-body Swiss Ephemeris skies. Input birth times and
natal features remain private in memory; a keyed HMAC, not plain SHA-256 of
guessable dates, identifies private input and feature vectors. This adapter
does NOT certify historical Lilly/Argoli accuracy, temporal rectification,
consent, true birth data, independent outcome ascertainment, or external
write-once preregistration. No human results are tested here.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import math
import os
import re
import stat
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .aspect_points import RayAspect
from .aspect_timeline import AspectProfile, generate_aspect_timeline
from .geometry import GeometryMethod
from .sky import DirectionBirthSnapshot, snapshot_from_swiss_files
from .timeline import TimeKey, generate_timeline
from .western_forward_blind import (
    SOURCE_CANDIDATES,
    Contact,
    canonical,
    contact_uncertainty_envelopes,
    sealed_prediction_receipt,
)

ROOT = Path(__file__).resolve().parents[3]
METHOD = GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE
TIME_KEY = TimeKey.PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR
AGE_MIN = 18.0
AGE_MAX = 65.0
EXPECTED_EPHEMERIS = {
    "sepl_18.se1": "ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66",
    "semo_18.se1": "1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7",
}
SOURCE_FILES = {
    "LILLY_1647_EVENT_CANDIDATES.json": (
        "66719c3ba3f8c3877b3684b30fb8c31537d56a33ae95909be348246374d42c87"
    ),
    "ASPECT_SOURCE_COVERAGE_DIAGNOSTIC.json": (
        "dc219e072bd03835c3e6527a41a70680bd24197d1e0840a6250495f33e4ae11d"
    ),
}
SOURCE_ROOT = ROOT / "docs/astrology-research-map/primary-direction-event-hypotheses-20261024"
METHOD_SPEC = {
    "schema": "WESTERN_MODERN_REGIOMONTANIAN_DIAGNOSTIC_V0",
    "geometry": METHOD.value,
    "time_key": TIME_KEY.value,
    "direction": "software_shortest_signed_direct_not_historical_Argolus",
    "contact_age_domain": [AGE_MIN, AGE_MAX],
    "ray_aspects": [v.value for v in RayAspect],
    "zodiacal_ray_beta_degrees": 0,
    "retained_source_candidate_rules": list(SOURCE_CANDIDATES),
    "birth_time_offset_grid": "all_integer_minutes_symmetrical",
    "historical_model_authentication": False,
}
PRIVATE_KEYS = frozenset(
    {
        "schema",
        "pseudonymous_participant_id",
        "birth_utc",
        "latitude_deg",
        "longitude_east_deg",
        "birth_time_uncertainty_minutes",
        "birth_time_quality",
    }
)
PRIVATE_SCHEMA = "PRIVATE_WESTERN_NATAL_INPUT_V0"


@dataclass(frozen=True, slots=True)
class PrivateNatalTuple:
    pseudonymous_participant_id: str
    birth_utc: datetime
    latitude_deg: float
    longitude_east_deg: float
    birth_time_uncertainty_minutes: int
    birth_time_quality: str

    @classmethod
    def from_json(cls, payload: dict[str, Any]) -> PrivateNatalTuple:
        if not isinstance(payload, dict) or set(payload) != PRIVATE_KEYS:
            raise ValueError("private input has missing or undeclared fields")
        if payload["schema"] != PRIVATE_SCHEMA:
            raise ValueError("unsupported private-input schema")
        pseudonym = payload["pseudonymous_participant_id"]
        if not isinstance(pseudonym, str) or not re.fullmatch(r"[A-Za-z0-9_-]{5,64}", pseudonym):
            raise ValueError("a short nonidentifying pseudonym is required")
        raw_time = payload["birth_utc"]
        if not isinstance(raw_time, str):
            raise ValueError("normalized UTC time must be an ISO-8601 string")
        try:
            moment = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("private birth UTC time must be ISO-8601") from exc
        if moment.tzinfo is None or moment.utcoffset() != timedelta(0):
            raise ValueError("birth time must ALREADY be normalized to explicit UTC")
        if not 1800 <= moment.year < 2400:
            raise ValueError("only pinned 1800–2399 Swiss ephemeris dates are supported")
        lat = payload["latitude_deg"]
        lon = payload["longitude_east_deg"]
        if any(type(v) not in (int, float) or not math.isfinite(v) for v in (lat, lon)):
            raise ValueError("finite numeric geographic coordinates required")
        if not (-66 <= lat <= 66 and -180 <= lon <= 180):
            raise ValueError("outside the supported northern/southern natal latitude domain")
        minutes = payload["birth_time_uncertainty_minutes"]
        if type(minutes) is not int or not 0 <= minutes <= 15:
            raise ValueError("integer-minute uncertainty must be between 0 and 15")
        quality = payload["birth_time_quality"]
        if quality not in (
            "certified_minute",
            "family_recalled",
            "documented_uncertain",
            "unknown_or_rectified",
        ):
            raise ValueError("unsupported birth-time source-quality category")
        return cls(pseudonym, moment.astimezone(UTC), float(lat), float(lon), minutes, quality)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_fixed_rules() -> tuple[dict[tuple[str, str], str], dict[tuple[str, str], dict[str, Any]]]:
    records = {}
    for name, digest in SOURCE_FILES.items():
        source = SOURCE_ROOT / name
        if _sha256(source) != digest:
            raise ValueError("original first-edition Lilly candidate rules were modified")
        records[name] = json.loads(source.read_text(encoding="utf-8"))
    bodily = records["LILLY_1647_EVENT_CANDIDATES.json"]["source_to_construct_rules"]
    aspects = records["ASPECT_SOURCE_COVERAGE_DIAGNOSTIC.json"]["families"]
    if len(bodily) != 4 or len(aspects) != 4:
        raise ValueError("expected four source-body and four source-ray candidate families")
    body_map = {(r["promissor"], r["target_role"]): r["id"] for r in bodily}
    aspect_map = {(r["promissor"], r["significator"]): r for r in aspects}
    if (
        len(body_map) != 4
        or len(aspect_map) != 4
        or {*body_map.values(), *(r["id"] for r in aspect_map.values())} != set(SOURCE_CANDIDATES)
    ):
        raise ValueError("source-rule identifiers must remain exactly the prior eight")
    if records["ASPECT_SOURCE_COVERAGE_DIAGNOSTIC.json"]["study_ready"] is not False:
        raise ValueError("source aspects were unexpectedly promoted to a scored study")
    return body_map, aspect_map


def _verify_ephemeris(snapshot: DirectionBirthSnapshot) -> None:
    if snapshot.ephemeris_mode != "SWIEPH verified for all seven classical bodies":
        raise RuntimeError("birth sky did not prove the requested Swiss Ephemeris mode")
    if dict(snapshot.ephemeris_file_sha256) != EXPECTED_EPHEMERIS:
        raise RuntimeError("pinned Swiss source-file hashes do not match")


def _contacts_for_sky(
    snapshot: DirectionBirthSnapshot,
    body_map: dict[tuple[str, str], str],
    aspect_map: dict[tuple[str, str], dict[str, Any]],
) -> tuple[Contact, ...]:
    bodily = generate_timeline(
        snapshot, methods=(METHOD,), time_key=TIME_KEY, max_age_years=AGE_MAX
    )
    rays = generate_aspect_timeline(
        snapshot,
        profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS,
        methods=(METHOD,),
        aspects=tuple(RayAspect),
        time_key=TIME_KEY,
        max_age_years=AGE_MAX,
    )
    output: list[Contact] = []
    for direction in bodily.directions:
        rule = body_map.get((direction.promissor, direction.significator))
        if (
            rule is not None
            and direction.contact == "body_to_angle"
            and direction.direction == "direct"
            and AGE_MIN <= direction.symbolic_age_years < AGE_MAX
        ):
            output.append(
                Contact(
                    key=rule + "/body",
                    rule_id=rule,
                    symbolic_age_years=round(direction.symbolic_age_years, 9),
                )
            )
    for ray_direction in rays.directions:
        rule_entry = aspect_map.get((ray_direction.promissor, ray_direction.significator))
        if (
            rule_entry is not None
            and ray_direction.ray_aspect in rule_entry["aspects"]
            and ray_direction.direction == "direct"
            and AGE_MIN <= ray_direction.symbolic_age_years < AGE_MAX
        ):
            label = rule_entry["id"]
            output.append(
                Contact(
                    key=f"{label}/{ray_direction.ray_aspect}/{ray_direction.ray_offset_branch}",
                    rule_id=label,
                    symbolic_age_years=round(ray_direction.symbolic_age_years, 9),
                )
            )
    if len({x.key for x in output}) != len(output):
        raise ValueError("ambiguous duplicate source-rule/aspect contact identity")
    return tuple(sorted(output, key=lambda x: x.key))


def _private_feature_vector(snapshot: DirectionBirthSnapshot) -> dict[str, Any]:
    # Every coordinate is only handed to an HMAC; never serialized to a public
    # receipt or logs. This includes actual ascendant/MC and ecliptic positions.
    return {
        "ramc_deg": snapshot.ramc_deg,
        "asc_ecliptic_deg": snapshot.ascendant_ecliptic_lon_deg,
        "mc_ecliptic_deg": snapshot.midheaven_ecliptic_lon_deg,
        "equatorial": [(name, pt.ra_deg, pt.dec_deg) for name, pt in snapshot.points],
        "ecliptic": snapshot.ecliptic_positions,
        "true_obliquity_deg": snapshot.true_obliquity_deg,
    }


def _hmac_sha256(secret: bytes, raw: object) -> str:
    if not isinstance(secret, bytes) or len(secret) < 32:
        raise ValueError("independently stored random HMAC secret must have >=32 bytes")
    return hmac.new(secret, canonical(raw), hashlib.sha256).hexdigest()


def build_sealed_direction_diagnostic(
    supplied_private: PrivateNatalTuple,
    *,
    secret: bytes,
    ephemeris_directory: str | Path,
) -> dict[str, Any]:
    """Build a sanitized modern-diagnostic artifact using actual Swiss skies.

    The caller supplies an independently normalized UTC birth tuple. This
    function does not collect consent or independently verify records.
    Everything birth-identifying is HMACed; no raw timestamp, location,
    planetary RA/Dec or model date is included in the returned record.
    """
    body_rules, aspect_rules = _read_fixed_rules()
    if not isinstance(secret, bytes) or len(secret) < 32:
        raise ValueError("a high-entropy external HMAC secret is required")
    offsets = tuple(
        range(
            -supplied_private.birth_time_uncertainty_minutes,
            supplied_private.birth_time_uncertainty_minutes + 1,
        )
    )
    collected: dict[int, Sequence[Contact]] = {}
    raw_private_features: list[tuple[int, dict[str, Any]]] = []
    base_provenance: dict[str, object] | None = None
    for offset in offsets:
        sky = snapshot_from_swiss_files(
            supplied_private.birth_utc + timedelta(minutes=offset),
            latitude_deg=supplied_private.latitude_deg,
            longitude_east_deg=supplied_private.longitude_east_deg,
            ephemeris_directory=ephemeris_directory,
        )
        _verify_ephemeris(sky)
        provenance = sky.provenance()
        if base_provenance is None:
            base_provenance = provenance
        elif provenance != base_provenance:
            raise RuntimeError("ephemeris provenance changed within one uncertain natal sample")
        raw_private_features.append((offset, _private_feature_vector(sky)))
        collected[offset] = list(_contacts_for_sky(sky, body_rules, aspect_rules))
    if base_provenance is None:
        raise AssertionError("every private input requires at least the baseline sky")
    windows = contact_uncertainty_envelopes(collected)
    original_tuple = {
        "schema": PRIVATE_SCHEMA,
        "pseudonymous_participant_id": supplied_private.pseudonymous_participant_id,
        "birth_utc": supplied_private.birth_utc.isoformat(),
        "latitude_deg": supplied_private.latitude_deg,
        "longitude_east_deg": supplied_private.longitude_east_deg,
        "birth_time_uncertainty_minutes": supplied_private.birth_time_uncertainty_minutes,
        "birth_time_quality": supplied_private.birth_time_quality,
    }
    birth_digest = _hmac_sha256(secret, original_tuple)
    chart_digest = _hmac_sha256(secret, raw_private_features)
    method_files = (
        "western_private_natal_bridge.py",
        "western_forward_blind.py",
        "sky.py",
        "geometry.py",
        "timeline.py",
        "aspect_timeline.py",
        "aspect_points.py",
    )
    code_hashes = {name: _sha256(Path(__file__).resolve().parent / name) for name in method_files}
    code_digest = hashlib.sha256(canonical(code_hashes)).hexdigest()
    rules_digest = hashlib.sha256(
        canonical({"method": METHOD_SPEC, "source_files": SOURCE_FILES})
    ).hexdigest()
    design_path = (
        ROOT / "docs/astrology-research-map/"
        "western-primary-direction-blind-pilot-20261025/PILOT_V0_METHOD_CONTRACT.json"
    )
    design_digest = _sha256(design_path)
    receipt = sealed_prediction_receipt(
        pseudonymous_participant_id=supplied_private.pseudonymous_participant_id,
        birth_input_sha256=birth_digest,
        chart_features_sha256=chart_digest,
        calculation_code_sha256=code_digest,
        rules_sha256=rules_digest,
        comparison_design_sha256=design_digest,
        birth_time_quality=supplied_private.birth_time_quality,
        windows=windows,
    )
    permitted = sum(w.timing is not None for w in windows)
    return {
        "schema": "PRIVATE_SOURCE_BOUND_WESTERN_DIAGNOSTIC_RECEIPT_V0",
        "stage": "ENGINEERING_ONLY_NOT_A_HUMAN_MODEL_OR_OUTCOME_FREEZE",
        "private_input_digest_scheme": "HMAC-SHA256_WITH_EXTERNAL_32_BYTE_OR_LONGER_KEY",
        "private_chart_digest_scheme": "HMAC-SHA256_WITH_SAME_EXTERNAL_KEY",
        "birth_local_time_timezone_verified": "NOT_ATTESTED_BY_THIS_ADAPTER",
        "ephemeris_requested_and_returned_mode": ("SWIEPH verified for all seven classical bodies"),
        "ephemeris_source_sha256": EXPECTED_EPHEMERIS,
        "source_rule_files_sha256": SOURCE_FILES,
        "calculation_module_hashes": code_hashes,
        "method_contract": METHOD_SPEC,
        "minute_samples_count": len(offsets),
        "deduplicated_candidate_contacts": len(windows),
        "tentative_modern_timing_windows_for_future_freeze": permitted,
        "all_windows_never_historically_authenticated": True,
        "sealed_diagnostic_receipt": receipt,
        "real_birth_inputs_in_output": False,
        "human_outcome_observations": "NONE",
        "human_predictive_accuracy": "UNTESTED",
    }


def _file_outside_source_tree(path: Path) -> Path:
    if not path.is_absolute():
        raise ValueError("use an absolute path outside the Git source checkout")
    expanded = path.expanduser()
    if expanded.is_symlink():
        raise ValueError("private file paths must be non-symlink paths")
    resolved = expanded.resolve()
    if resolved.is_relative_to(ROOT):
        raise ValueError("private birth/key/receipt files must be outside the Git repository")
    return resolved


def _read_private_bytes(path: Path) -> bytes:
    path = _file_outside_source_tree(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError("private input must be a regular non-symlink file")
    permission = stat.S_IMODE(path.stat().st_mode)
    if permission & 0o077:
        raise ValueError("private birth and HMAC key files require owner-only permissions")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as file:
        return file.read()


def write_private_receipt_once(destination: Path, result: dict[str, Any]) -> None:
    """Secure write-once JSON receipt; no raw natal data in the result."""
    target = _file_outside_source_tree(destination)
    if not target.parent.is_dir():
        raise ValueError("external destination directory must already exist")
    if result.get("real_birth_inputs_in_output") is not False:
        raise ValueError("only redacted human-safe output schemas are permitted")
    payload = canonical(result)
    if b'"birth_utc"' in payload or b'"latitude_deg"' in payload:
        # Birth/location field names should NEVER appear in a public receipt,
        # including future schema revisions.
        raise ValueError("output unexpectedly contains raw private natal fields")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(target, flags, 0o600)
    try:
        with os.fdopen(fd, "wb") as file:
            file.write(payload)
            file.flush()
            os.fsync(file.fileno())
    except BaseException:
        target.unlink(missing_ok=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-input", type=Path, required=True)
    parser.add_argument("--secret-key-file", type=Path, required=True)
    parser.add_argument("--ephemeris-dir", type=Path, required=True)
    parser.add_argument("--external-receipt", type=Path, required=True)
    args = parser.parse_args()
    key = _read_private_bytes(args.secret_key_file)
    if len(key) < 32:
        raise ValueError("private HMAC key file contains fewer than 32 random bytes")
    private_payload = json.loads(_read_private_bytes(args.private_input))
    input_record = PrivateNatalTuple.from_json(private_payload)
    result = build_sealed_direction_diagnostic(
        input_record,
        secret=key,
        ephemeris_directory=args.ephemeris_dir,
    )
    write_private_receipt_once(args.external_receipt, result)
    # Intentionally omit name/pseudonym, birth time, place, chart positions,
    # future event dates, and output-location logging.
    print(
        "RESEARCH_ONLY_SANITIZED_RECEIPT_WRITTEN",
        "candidate_contacts",
        result["deduplicated_candidate_contacts"],
        "human_predictive_validity",
        result["human_predictive_accuracy"],
    )


if __name__ == "__main__":
    main()
