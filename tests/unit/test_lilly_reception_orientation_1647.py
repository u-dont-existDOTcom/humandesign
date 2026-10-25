"""First-print 1647 reception and angle-direction source examples, no events."""

from __future__ import annotations

import math

import pytest

from hdmatch.astrology.lilly_angle_progression import (
    AngularAxis,
    source_forward_angular_arc,
)
from hdmatch.astrology.lilly_essential_dignity import (
    CLASSICAL,
    essential_components,
)
from hdmatch.astrology.lilly_reception import (
    DignityPlacement,
    all_chart_receptions,
    host_rulers,
    reception_between,
)


def at(planet: str, longitude: float, is_day: bool = True) -> DignityPlacement:
    source = essential_components(planet, longitude, is_day_chart=is_day)
    return DignityPlacement(
        planet,
        source.zodiac_sign,
        source.chart_sect,
        source.table_term_ruler,
        source.table_face_ruler,
    )


def test_1647_page112_domicile_reception_example_is_reciprocal() -> None:
    # Textual example: Sun Aries; Mars Leo.
    r = reception_between(at("sun", 5.0), at("mars", 125.0))
    assert r is not None
    assert "domicile" in r.same_mode_receptions
    assert r.source_house_reception_alternative_points == 5
    assert r.source_exaltation_reception_alternative_points == 0
    assert r.full_lilly_radix_strength == "UNRESOLVED"
    # 'House' is sign domicile, not natal mundane house 1-12.
    assert host_rulers(at("sun", 5.0))["domicile"] == "mars"
    assert host_rulers(at("mars", 125.0))["domicile"] == "sun"


def test_1647_page112_day_triplicity_example_changes_at_night() -> None:
    # Textual example: Venus Aries; Sun Taurus, by day.
    day = reception_between(at("venus", 5, True), at("sun", 35, True))
    assert day is not None and "triplicity" in day.same_mode_receptions
    assert day.source_house_reception_alternative_points == 0
    assert day.source_exaltation_reception_alternative_points == 0
    night = reception_between(at("venus", 5, False), at("sun", 35, False))
    assert night is None or "triplicity" not in night.same_mode_receptions


def test_1647_page112_term_example_reproduced() -> None:
    # Textual example: Venus Aries 24th and Mars Gemini 16th.
    rec = reception_between(at("venus", 24.0), at("mars", 76.0))
    assert rec is not None
    assert rec.a_in_b_modes == ("domicile", "term")
    assert rec.b_in_a_modes == ("term",)
    assert rec.same_mode_receptions == ("term",)
    assert rec.mixed_only is False


def test_1647_page115_exaltation_reception_is_alternative_four_points() -> None:
    # Sun in Saturn's exaltation (Libra); Saturn in Sun's (Aries).
    rec = reception_between(at("sun", 182), at("saturn", 2))
    assert rec is not None
    assert "exaltation" in rec.same_mode_receptions
    assert rec.source_exaltation_reception_alternative_points == 4
    assert rec.full_lilly_radix_strength == "UNRESOLVED"


def test_one_sided_guest_is_not_a_mutual_reception() -> None:
    # Mars in Leo is in Sun's house, while Sun in Taurus is NOT in Mars's house.
    assert reception_between(at("mars", 124), at("sun", 31)) is None


def test_invalid_multiple_chart_sects_rejected() -> None:
    with pytest.raises(ValueError, match="SAME birth chart"):
        reception_between(at("venus", 5, True), at("sun", 35, False))
    with pytest.raises(ValueError, match="two distinct"):
        reception_between(at("sun", 5), at("sun", 40))


def test_exact_seven_unique_planets_and_pair_dedup() -> None:
    positions = tuple(at(name, 5 + 30 * i) for i, name in enumerate(CLASSICAL))
    receptions = all_chart_receptions(positions)
    keys = [(r.planet_a, r.planet_b) for r in receptions]
    assert keys == sorted(set(keys))
    assert len(receptions) <= 21
    with pytest.raises(ValueError, match="exactly one"):
        all_chart_receptions(positions[:-1])


def test_source_1647_mc_page515_ascending_ra_difference() -> None:
    # Lilly: MC RAMC=222°10'; Mercury-terms RA=229°35';
    # explained result 7°25' (his printed intermediate table reads 7°45').
    mc = source_forward_angular_arc(
        AngularAxis.MC_RIGHT_ASCENSION,
        222 + 10 / 60,
        229 + 35 / 60,
    )
    assert mc.forward_source_arc_degrees == pytest.approx(7 + 25 / 60)
    assert mc.original_printed_page == 515
    assert mc.axis == "mc_right_ascension"
    assert mc.semantic_status.endswith("ARITHMETIC_ONLY")
    # A separately visible example on the same page: Venus-term RA 222°31'.
    another = source_forward_angular_arc(
        AngularAxis.MC_RIGHT_ASCENSION, 222 + 10 / 60, 222 + 31 / 60
    )
    assert another.forward_source_arc_degrees == pytest.approx(21 / 60)


def test_source_1647_asc_page517_oblique_ascent_progression() -> None:
    # Lilly's Ascendant specimen baseline OAsc 312°10':
    # first row 313°34' -> 1°24'; last row 332°02' -> 19°52'.
    asc = source_forward_angular_arc(
        AngularAxis.ASC_OBLIQUE_ASCENSION,
        312 + 10 / 60,
        313 + 34 / 60,
    )
    assert asc.forward_source_arc_degrees == pytest.approx(1 + 24 / 60)
    assert asc.original_printed_page == 517
    last = source_forward_angular_arc(
        AngularAxis.ASC_OBLIQUE_ASCENSION, 312 + 10 / 60, 332 + 2 / 60
    )
    assert last.forward_source_arc_degrees == pytest.approx(19 + 52 / 60)


def test_forward_angular_direction_wrap_is_not_shortest_signed_selection() -> None:
    assert source_forward_angular_arc(
        AngularAxis.MC_RIGHT_ASCENSION, 359, 2
    ).forward_source_arc_degrees == pytest.approx(3)
    backward_looking = source_forward_angular_arc(AngularAxis.MC_RIGHT_ASCENSION, 2, 359)
    # Preserve the long forward-progression, not relabel it as a source
    # converse direction of one year or claim authorial equivalence.
    assert backward_looking.forward_source_arc_degrees == pytest.approx(357)


def test_direction_inputs_are_finite_normalized_degree_coordinates() -> None:
    for bad in (float("nan"), math.inf, -1, 360):
        with pytest.raises(ValueError):
            source_forward_angular_arc(AngularAxis.MC_RIGHT_ASCENSION, bad, 10)
        with pytest.raises(ValueError):
            source_forward_angular_arc(AngularAxis.ASC_OBLIQUE_ASCENSION, 10, bad)


def test_reception_never_decides_radix_strength() -> None:
    planet_pairs = all_chart_receptions(
        (
            at("sun", 5),
            at("moon", 35),
            at("mercury", 65),
            at("venus", 95),
            at("mars", 125),
            at("jupiter", 245),
            at("saturn", 305),
        )
    )
    assert all(r.full_lilly_radix_strength == "UNRESOLVED" for r in planet_pairs)


def test_source_mc_direct_arc_agrees_with_all_three_geometric_labels() -> None:
    # For the exact meridian and zero-declination ray used in the original
    # example, all 3 research geometries reduce to RA(promissor)-RAMC.
    from hdmatch.astrology.geometry import (
        EquatorialPoint,
        GeometryMethod,
        direction_arc,
    )

    ramc = 222 + 10 / 60
    mc = EquatorialPoint(ramc, 0)
    ray = EquatorialPoint(229 + 35 / 60, 0)
    source = source_forward_angular_arc(AngularAxis.MC_RIGHT_ASCENSION, ramc, ray.ra_deg)
    for method in GeometryMethod:
        measured = direction_arc(method, 53, ramc, mc, ray)
        assert measured == pytest.approx(source.forward_source_arc_degrees, abs=1e-8)
    # This parity covers this very narrow meridian geometry only.
    assert source.original_printed_page == 515


def test_frozen_96_chart_reception_inventory_has_distinct_statuses() -> None:
    import json
    from collections import Counter
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    folder = root / "docs/astrology-research-map/primary-direction-reception-orientation-20261025"
    summary = json.loads((folder / "RECEPTION_SYNTHETIC_SUMMARY.json").read_text())
    recorded = json.loads((folder / "RECEPTION_RELATIONS.json").read_text())
    assert len(recorded) == summary["n_synthetic_charts"] == 96
    assert sum(len(v) for v in recorded.values()) == 462
    assert summary["n_unordered_reception_pairs"] == 462
    strict = [r for pairs in recorded.values() for r in pairs if not r["mixed_only"]]
    mixed = [r for pairs in recorded.values() for r in pairs if r["mixed_only"]]
    assert len(strict) == summary["n_same_mode_reception_pairs"] == 172
    assert len(mixed) == summary["mixed_only_pairs_not_history_scored"] == 290
    assert sum(any(not x["mixed_only"] for x in pairs) for pairs in recorded.values()) == 89
    assert all(r["same_mode_receptions"] for r in strict)
    assert all(not r["same_mode_receptions"] for r in mixed)
    assert all(r["full_lilly_radix_strength"] == "UNRESOLVED" for r in strict + mixed)
    # Multiple same-class tags on ONE relation are still ONE unordered pair.
    modes = Counter(m for r in strict for m in r["same_mode_receptions"])
    assert dict(sorted(modes.items())) == summary["same_dignity_mode_pair_counts"]


def test_frozen_jupiter_mc_receptions_do_not_create_human_predictions() -> None:
    import json
    from pathlib import Path

    folder = Path(__file__).resolve().parents[2] / (
        "docs/astrology-research-map/primary-direction-reception-orientation-20261025"
    )
    contacts = json.loads((folder / "RECEPTION_MC_JUPITER_CROSSWALK.json").read_text())
    summary = json.loads((folder / "RECEPTION_SYNTHETIC_SUMMARY.json").read_text())
    assert len(contacts) == 47
    assert sum(bool(x["source_reciprocal_same_modes"]) for x in contacts) == 19
    assert (
        sum(
            x["has_source_domicile_reception"] or x["has_source_exaltation_reception"]
            for x in contacts
        )
        == 8
    )
    assert summary["mc_jupiter_contacts_with_any_same_mode"] == 19
    assert summary["mc_jupiter_contacts_with_dom_or_exaltation_reception"] == 8
    assert summary["mc_jupiter_contacts_full_strength_certified"] == 0
    assert all(x["complete_jupiter_strength"] is None for x in contacts)
    assert all(x["full_lilly_direction_prediction"] is None for x in contacts)
    assert all(x["frozen_direction_key"].startswith("L1647-MC-JUP-SOFT/") for x in contacts)


def test_complete_reception_replay_and_five_original_witnesses() -> None:
    import hashlib
    import importlib.util
    import json
    from pathlib import Path

    folder = Path(__file__).resolve().parents[2] / (
        "docs/astrology-research-map/primary-direction-reception-orientation-20261025"
    )
    spec = importlib.util.spec_from_file_location(
        "reception_replay_check", folder / "verify_reception_replay.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected = json.loads((folder / "RECEPTION_REPLAY_VERIFICATION.json").read_text())
    assert module.replay() == expected
    assert expected["status"] == "FOUR_OF_FOUR_COMPLETE_SOURCE_DATA_OUTPUTS_BYTE_IDENTICAL"
    assert expected["human_predictive_accuracy"] == "UNTESTED"
    for filename, sha in expected["file_sha256"].items():
        assert hashlib.sha256((folder / filename).read_bytes()).hexdigest() == sha
    witness_images = list((folder / "witness_pages").glob("*.jpg"))
    assert {p.stem.split("_")[-1] for p in witness_images} == {"112", "510", "511", "515", "517"}
    assert all(p.stat().st_size > 900_000 for p in witness_images)


def test_published_1647_source_image_and_code_integrity_manifest() -> None:
    import hashlib
    import importlib.util
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    here = root / "docs/astrology-research-map/primary-direction-reception-orientation-20261025"
    spec = importlib.util.spec_from_file_location(
        "verified_sources", here / "build_verification.py"
    )
    assert spec and spec.loader
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    manifest = json.loads((here / "VERIFICATION.json").read_text())
    assert helper.build() == manifest
    assert manifest["human_predictive_validity"] == "UNTESTED"
    assert manifest["complete_Jupiter_natal_strength_authenticated"] is False
    assert manifest["full_Argolus_method_authenticated"] is False
    assert manifest["new_original_witness_pages"] == [112, 510, 511, 515, 517]
    for path, evidence in manifest["files"].items():
        assert hashlib.sha256((root / path).read_bytes()).hexdigest() == evidence["sha256"]
