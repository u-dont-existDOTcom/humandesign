"""Original photographed Placidus Latin 1657, distinct from Cooper English 1814.

The original language was read from three public-domain source images,
not inferred solely from poor OCR. This is a source-label audit, NOT proof
of astrology's predictive validity or completeness of historical algorithm.
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
    PLACIDUS_1657_LATIN,
    PLACIDUS_1814,
    WitnessStatus,
    placidus_1657_latin_role_assessment,
    placidus_1814_role_assessment,
    solar_key_source_assessment,
)
from hdmatch.astrology.timeline import generate_timeline

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/astrology-research-map/gansten-placidus-latin-1657-20261024"
EPHE = Path(
    os.environ.get(
        "HDMATCH_PRIMARY_DIR_EPHE_DIR",
        str(Path.home() / ".local/share/hdmatch/ephemeris/1800-2399"),
    )
)


@pytest.fixture(scope="module")
def original():
    return json.loads((DOC / "ORIGINAL_1657_LATIN_COLLATION.json").read_text())


def test_original_1657_latin_cited_as_direct_photo_not_ocr(original) -> None:
    edition = original["original"]
    assert edition["year"] == 1657
    assert edition["original_images_read"] is True
    assert edition["original_Latin_OCR_is_support_only"] is True
    assert edition["printed_pages"] == [11, 12, 19]
    assert edition["leaf_index_zero_based"] == [30, 31, 48]
    assert edition["original_Latin_not_fully_read"] is True
    assert edition["full_1657_PDF_available_locally"] is False
    assert edition["scanned_catalog"].startswith("https://archive.org/details/")


def test_original_scan_images_match_sha256_and_are_nonempty(original) -> None:
    for leaf, checksum in original["original"]["image_sha256"].items():
        path = DOC / "facsimile_pages" / f"placidus1657_leaf_{leaf.zfill(4)}.jpg"
        blob = path.read_bytes()
        assert len(blob) > 150_000
        assert blob.startswith(bytes.fromhex("ffd8"))
        assert hashlib.sha256(blob).hexdigest() == checksum


def test_original_all_named_theses_are_on_printed_page_11(original) -> None:
    paragraphs = original["passages"]
    theses = [x for x in paragraphs if "thesis" in x]
    assert {x["thesis"] for x in theses} == {58, 59, 60, 61, 62, 65}
    assert all(x["image_leaf"] == 30 and x["printed_page"] == 11 for x in theses)
    assert all(x["confidence"] == "photo_verified" for x in theses)
    assert len([x for x in paragraphs if "canon" in x]) == 1


def test_first_edition_exact_zodiacal_converse_restriction(original) -> None:
    text = next(x for x in original["passages"] if x.get("thesis") == 61)
    assert "nullo modo in zodiaco" in text["latin_short"]
    attested = placidus_1657_latin_role_assessment(
        "zodiacal_promissor_ray", "traditional_role_reversed_converse"
    )
    assert attested.source_id == PLACIDUS_1657_LATIN
    assert attested.status is WitnessStatus.INCOMPATIBLE_WITNESS
    assert "theses 61-62" in attested.evidence
    assert "mathematical candidate" in attested.limit


def test_original_first_edition_explicit_moving_angle_converse_restriction() -> None:
    record = placidus_1657_latin_role_assessment(
        "bodily_conjunction", "traditional_role_reversed_converse", moving_angle=True
    )
    assert record.status is WitnessStatus.INCOMPATIBLE_WITNESS
    assert "thesis 60" in record.evidence
    assert "Cardines" in record.evidence


def test_1814_translation_independently_agrees_on_narrow_bans() -> None:
    args = ("zodiacal_promissor_ray", "traditional_role_reversed_converse")
    latin = placidus_1657_latin_role_assessment(*args)
    english = placidus_1814_role_assessment(*args)
    assert latin.status is english.status is WitnessStatus.INCOMPATIBLE_WITNESS
    assert latin.source_id == PLACIDUS_1657_LATIN
    assert english.source_id == PLACIDUS_1814
    latin_angle = placidus_1657_latin_role_assessment(
        "bodily_conjunction", "traditional_role_reversed_converse", moving_angle=True
    )
    translated_angle = placidus_1814_role_assessment(
        "bodily_conjunction", "traditional_role_reversed_converse", moving_angle=True
    )
    assert latin_angle.status is translated_angle.status is WitnessStatus.INCOMPATIBLE_WITNESS


def test_solar_key_promoted_to_original_latin_source_not_full_certification() -> None:
    entry = solar_key_source_assessment("placidus_cumulative_true_solar_ra")
    assert entry.source_id == PLACIDUS_1657_LATIN
    assert entry.status is WitnessStatus.COMPATIBLE_SELECTED_RULE
    assert "thesis 65" in entry.evidence
    assert "1814 translation" in entry.limit
    assert "TT/UT" in entry.limit
    brahe = solar_key_source_assessment("brahe_true_midnight_birth_day")
    assert brahe.status is WitnessStatus.PARTIAL_SOURCE_SUPPORT


def test_modern_reverse_rotation_not_falsely_attributed_to_1657() -> None:
    record = placidus_1657_latin_role_assessment(
        "bodily_conjunction", "modern_reverse_rotation_diagnostic"
    )
    assert record.status is WitnessStatus.NOT_ESTABLISHED
    assert "printed p19" in record.evidence


def test_generic_algorithm_still_available_with_nonblocking_historical_warning() -> None:
    if not EPHE.is_dir():
        pytest.skip("official ephemeris unavailable")
    birth = snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=EPHE,
    )
    source = generate_role_timeline(
        birth,
        construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
        regime=RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE,
    )
    assert len(source.directions) == 288
    output = source.to_dict()
    scope = output["movement_provenance"]["placidus_1657_original_latin_source_scope"]
    assert scope["status"] == "incompatible_witness"
    assert "zodiaco" in scope["evidence"]
    old = json.loads(
        (
            ROOT
            / "docs/astrology-research-map/gansten-role-variants-20261024"
            / "examples/synthetic_2000_traditional_ray_converse.json"
        ).read_text()
    )
    assert output["directions"] == old["directions"]
    assert output["coverage"] == old["coverage"]


def test_original_1657_solar_timing_preserves_old_contact_ages_and_arcs() -> None:
    if not EPHE.is_dir():
        pytest.skip("official ephemeris unavailable")
    birth = snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=EPHE,
    )
    engine = SolarRAEngine(birth, EPHE)
    report = apply_solar_key(
        generate_timeline(birth, max_age_years=125).to_dict(),
        engine,
        SolarTimeKey.PLACIDUS_CUMULATIVE_TRUE_SOLAR_RA,
        requested_max_age=100,
    )
    frozen = json.loads(
        (
            ROOT
            / "docs/astrology-research-map/gansten-solar-time-keys-20261024"
            / "examples/synthetic_2000_placidus_true_ra.json"
        ).read_text()
    )
    assert report["directions"] == frozen["directions"]
    assert report["coverage"] == frozen["coverage"]
    assert len(report["directions"]) == 114
    assert report["solar_time_key"]["primary_source_scope"]["source_id"] == PLACIDUS_1657_LATIN
