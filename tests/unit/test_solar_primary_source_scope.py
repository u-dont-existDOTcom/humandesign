"""Historical-primary-source scope checks, separate from geometric verification.

These tests confirm that direct source content is neither upgraded to invented
historical implementation details nor used as a new restriction on generic
mathematical candidates. No real human natal or outcome data.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.astrology.role_directions import (
    ContactConstruction,
    RotationRegime,
    generate_role_timeline,
)
from hdmatch.astrology.sky import snapshot_from_swiss_files
from hdmatch.astrology.solar_time_keys import (
    SolarRAEngine,
    SolarTimeKey,
    apply_solar_key,
)
from hdmatch.astrology.source_witness_scope import (
    BRAHE_1573,
    PLACIDUS_1657_LATIN,
    WitnessStatus,
    placidus_1814_role_assessment,
    solar_key_source_assessment,
)
from hdmatch.astrology.timeline import generate_timeline

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "docs/astrology-research-map/gansten-solar-original-text-20261024"
EPHE = Path(
    os.environ.get(
        "HDMATCH_PRIMARY_DIR_EPHE_DIR",
        str(Path.home() / ".local/share/hdmatch/ephemeris/1800-2399"),
    )
)


def test_source_file_preserves_two_distinct_edition_witnesses() -> None:
    document = json.loads((AUDIT / "SOURCE_WITNESS_AUDIT.json").read_text())
    assert len(document["source_evidence_classes"]) == 2
    brahe, placidus = document["source_evidence_classes"]
    assert brahe["id"] == "BRAHE_1573"
    assert brahe["original_publication_year"] == 1573
    assert brahe["direct_text_url"].startswith("https://tekstnet.dk/")
    assert brahe["source_quality"].find("not original facsimile") >= 0
    assert placidus["id"] == "PLACIDUS_COOPER_1814"
    assert placidus["work_original_year"] == 1657
    assert placidus["translation_publication_year"] == 1814
    assert placidus["pdf_pages_1_based"] == [40, 41, 42]
    assert placidus["printed_pages"] == [23, 24, 25]
    assert placidus["catalog_original_1657"]["original_scan_found"].endswith("NOT read this pass")


def test_all_inspected_page_images_are_exactly_hashed() -> None:
    document = json.loads((AUDIT / "SOURCE_WITNESS_AUDIT.json").read_text())
    witness = document["source_evidence_classes"][1]
    hashes = witness["scanned_page_images"]
    assert len(hashes) == 3
    for key, digest in hashes.items():
        path = AUDIT / "source_page_images" / f"placidus_1814_pdf_page_{key}.png"
        raw = path.read_bytes()
        assert len(raw) > 100_000
        assert hashlib.sha256(raw).hexdigest() == digest


def test_brahe_1573_true_nonuniform_day_is_partial_evidence_only() -> None:
    assessment = solar_key_source_assessment("brahe_true_midnight_birth_day")
    assert assessment.source_id == BRAHE_1573
    assert assessment.status is WitnessStatus.PARTIAL_SOURCE_SUPPORT
    assert "TRUE" not in assessment.limit.upper() or "true-solar midnight" in assessment.limit
    assert "NOT specify" in assessment.limit
    assert "varying" in assessment.evidence


def test_placidus_cumulative_key_now_attested_in_original_1657_latin() -> None:
    assessment = solar_key_source_assessment("placidus_cumulative_true_solar_ra")
    assert assessment.source_id == PLACIDUS_1657_LATIN
    assert assessment.status is WitnessStatus.COMPATIBLE_SELECTED_RULE
    assert "first" in assessment.evidence and "second" in assessment.evidence
    assert "original" in assessment.limit
    assert "Latin" in assessment.limit
    with pytest.raises(ValueError):
        solar_key_source_assessment("unknown_fictional_source")


def test_placidus_1814_explicit_no_zodiacal_converse() -> None:
    result = placidus_1814_role_assessment(
        "zodiacal_promissor_ray", "traditional_role_reversed_converse"
    )
    assert result.status is WitnessStatus.INCOMPATIBLE_WITNESS
    assert "pp.23-24" in result.evidence
    assert "zodiacal" in result.evidence
    assert "not be called" in result.limit


def test_placidus_1814_excludes_moving_angles_in_converse() -> None:
    result = placidus_1814_role_assessment(
        "bodily_conjunction",
        "traditional_role_reversed_converse",
        moving_angle=True,
    )
    assert result.status is WitnessStatus.INCOMPATIBLE_WITNESS
    assert "thesis 60" in result.evidence


def test_no_retroactive_universal_ban_on_generic_converse_geometry() -> None:
    result = placidus_1814_role_assessment(
        "zodiacal_promissor_ray", "modern_reverse_rotation_diagnostic"
    )
    assert result.status is WitnessStatus.NOT_ESTABLISHED
    ordinary = placidus_1814_role_assessment("zodiacal_promissor_ray", "direct_primary_motion")
    assert ordinary.status is WitnessStatus.NOT_ESTABLISHED


@pytest.mark.skipif(not EPHE.is_dir(), reason="explicit local official ephemeris unavailable")
def test_output_solar_key_source_metadata_does_not_change_numeric_arcs() -> None:
    birth = snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=EPHE,
    )
    engine = SolarRAEngine(birth, EPHE)
    geometric = generate_timeline(birth, max_age_years=125).to_dict()
    prior_dir = ROOT / "docs/astrology-research-map/gansten-solar-time-keys-20261024" / "examples"
    for profile, file in [
        (SolarTimeKey.BRAHE_TRUE_MIDNIGHT_BIRTH_DAY, "synthetic_2000_brahe_birth_day.json"),
        (SolarTimeKey.PLACIDUS_CUMULATIVE_TRUE_SOLAR_RA, "synthetic_2000_placidus_true_ra.json"),
    ]:
        calculated = apply_solar_key(geometric, engine, profile, requested_max_age=100)
        frozen = json.loads((prior_dir / file).read_text())
        # Keep every previously tested physical contact and timing value.
        assert calculated["directions"] == frozen["directions"]
        assert calculated["coverage"] == frozen["coverage"]
        # Only source-provenance is augmented by this research.
        scope = calculated["solar_time_key"]["primary_source_scope"]
        assert scope["source_id"] in (BRAHE_1573, PLACIDUS_1657_LATIN)
        assert scope["status"] in ("partial_source_support", "compatible_selected_rule")


@pytest.mark.skipif(not EPHE.is_dir(), reason="explicit local official ephemeris unavailable")
def test_generic_candidate_kept_even_when_not_placidus_historical() -> None:
    birth = snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=EPHE,
    )
    result = generate_role_timeline(
        birth,
        construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
        regime=RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE,
    )
    assert len(result.directions) == 288
    historical = placidus_1814_role_assessment(result.construction.value, result.regime.value)
    assert historical.status is WitnessStatus.INCOMPATIBLE_WITNESS
    assert all(r.ray_owner == r.promissor for r in result.directions)
