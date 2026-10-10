"""Build documentary reference tables and bounded arithmetic receipts for B02l."""
import hashlib
import json
from pathlib import Path
from build_source_data import BATCH, SOURCE_ID, SOURCE_SHA, SCOPE, read, write
from lilly_dariot_reference import crisis_geometry, select_crisis_origin, timing_options


def build():
    ids = read("RECORD_ID_MAP.json")
    items = []
    def add(key, locals_, pages, description, data):
        items.append({"id": key, "record_ids": [ids[x] for x in locals_], "pdf_pages": pages,
                      "description": description, "data": data})
    add("crisis_origin", ["B031"], [300], "Local critical-day time hierarchy; no new universal override of earlier illness-chart rules.",
        {"preferred": "First hour of taking bed, as nearly as obtainable", "fallback_condition": "That hour cannot be obtained",
         "fallback": "First time the physician was asked to give judgment", "moon": "Correct its motion to that hour",
         "unknown_is_not_unavailable": "Conservative implementation distinction, not an additional quoted source category."})
    add("crisis_offsets", ["B032", "B033", "B034"], [300, 301], "Three explicit acute-illness offsets; no chronic extension or calendar conversion.",
        {"illness_scope": "acute, not chronic", "offset_degrees": [45, 90, 135],
         "time_language": "near those times", "tolerance": None, "angular_origin": "Moon's corrected first place",
         "better_condition": "Good aspect AND benevolent planet", "worse_condition": "Ill aspect of sixth OR eighth lord",
         "clinical_validation": False})
    add("ancient_sign_units", ["B038", "B039", "B040", "B041", "B043"], [301, 302], "Ancients' options retained alongside Lilly's discretionary conditions.",
        {"moveable": ["days"], "common": ["weeks", "months"], "fixed": ["months", "years"],
         "prior_recovery_judgment_required": True, "unit_selection_algorithm": None,
         "other_factors": ["signs and houses of both bodies", "disease quality and feasible duration", "planetary speed", "Moon's speed, sign and quality"],
         "lilly_common_sign_qualification": "Do not judge months, weeks or days mechanically; consider nature and discretion."})
    add("house_correspondence", ["B042"], [301], "Reference equivalences, not an override policy.",
        {"angular": "moveable", "succedent": "common", "cadent": "fixed", "conflict_resolution": None})
    add("solar_lunar_distances", ["B028", "B029"], [300], "Printed danger assertions preserved as historical content, without executable prognosis.",
        {"close_case": {"maximum_degrees_inclusive": 6, "phase": "Moon has not yet passed the Sun and has not yet perfected the conjunction",
                        "Aries_or_Leo": "Mitigates but does not remove the stated ill omen"},
         "other_statement": {"exact_degrees": 12, "wording": "little danger", "phase_restated": False},
         "six_to_twelve_interpolation": None, "twelve_or_more_rule": False})
    add("sixth_cusp_illustration", ["B045"], [302], "One conditional numerical illustration, without a dated enquiry or verified endpoint.",
        {"cusp": 6, "degree": 28, "sign_class": "common", "conditions_combined": "AND", "duration_relation": "strictly less than",
         "duration_weeks": 2, "event_word": "vary", "event_direction": None, "exact_day": None, "observed_case": False})
    add("local_role_groups", ["B007", "B008", "B009", "B010", "B016", "B019"], [298, 299], "Roles are local and must not be silently substituted or counted as independent bodies.",
        {"introductory_spirit_roles": ["ascending sign", "Moon", "lord of Sun's house"],
         "introductory_member_roles": ["lord of ascendant", "Moon's dispositor"],
         "B008_all_afflicted": ["ascendant", "Sun", "Moon"],
         "B010_all_or_two_impeded": ["ascendant", "Moon", "lord of Sun's house"],
         "B016_comparative_case": ["dispositor of ascendant lord", "Moon's dispositor"],
         "house_meaning_and_duplicate_counting": "Explicit interpretation dependencies; no automatic vote score."})
    add("planet_vs_aspect_quality", ["A043", "B033", "B017"], [296, 299, 300], "A good planet and a good aspect are different source predicates.",
        {"A043": "Saturn has signification and is in aspect with good planets at apparent departure; the aspect is not separately called good.",
         "B033": "At the stated crises both a good aspect and a benevolent planet are required.",
         "B017": "The adverse Mars list literally includes sextile, square and opposition; location grammar remains unresolved."})
    write("REFERENCE_TABLES.json", {"batch": "B02l", "source_only": True, "clinical_mapping": False,
        "table_count": len(items), "items": items})
    sample = 350*3600 + 15*60
    geometry = crisis_geometry(sample, "acute", "selected")
    expected = [(35*3600+15*60), (80*3600+15*60), (125*3600+15*60)]
    assert list(geometry["targets_arcsec"]) == expected
    write("ARITHMETIC_CHECKS.json", {"batch": "B02l", "sample_type": "Synthetic arithmetic example, not Lilly's chart or a patient",
        "source_offsets_record": ids["B032"], "initial_longitude": "350 degrees 15 minutes",
        "initial_longitude_arcsec": sample, "offset_degrees": [45, 90, 135],
        "method": "(initial integer arcseconds + offset integer arcseconds) modulo 1296000",
        "expected_targets_arcsec": expected, "actual_result": geometry,
        "display_targets": ["35 degrees 15 minutes", "80 degrees 15 minutes", "125 degrees 15 minutes"],
        "arithmetic_matches": True, "ephemeris_used": False, "calendar_dates": None,
        "origin_sample": select_crisis_origin("unknown", None, "known", "supplied physician-request time"),
        "unresolved_timing_sample": timing_options("common", "angular"), "predictive_accuracy_evaluated": False})
    window = read("SOURCE_WINDOW_VERIFICATION.json")
    write("READING_RECEIPT.json", {"batch": "B02l", "source_id": SOURCE_ID, "source_sha256": SOURCE_SHA,
        "scope": SCOPE, "original_source_hash_recomputed_this_turn": True,
        "root_original_page_images_read": list(range(292, 303)), "root_supplementary_original_pages_read": [888, 277, 283],
        "source_a_original_owned_pages_read": list(range(292, 298)), "source_b_original_owned_pages_read": list(range(297, 303)),
        "independent_source_first_original_pages_read": list(range(292, 303)),
        "independent_supplementary_original_pages_read": [888, 277, 283],
        "root_initial_notes_frozen_before_worker_findings": True,
        "independent_notes_frozen_before_candidate_access": True,
        "independent_notes_count_semantics": "Source unit counts are editorial, not independent predictions.",
        "author_work_original_dariot_collated": False,
        "image_authority": "Original scans. Navigation OCR is not a substitute for visual wording/glyph checks.",
        "source_window": window["artifact"], "source_window_pages": window["page_count"],
        "all_copied_pages_match_original_rasters": all(p["render_pixels_identical"] for p in window["pages"]),
        "next_heading_visible_but_not_extracted": read("SECTION_COVERAGE.json")["next"]})
    checks = [
        ("nodes", [295], ["A025"], "South Node and North Node, with sign/node attachment still open."),
        ("fixed_examples", [295], ["A030"], "Fixed class, as in Taurus, Leo, Aquarius. Three examples, not a stated exhaustive list."),
        ("mars_opening", [297], ["A047"], "Mars at the page opening, continuing the prior Mars material."),
        ("jupiter_never", [298], ["B014"], "Jupiter and never are printed; the extent of transferred contrary-hereof conditions remains unstated."),
        ("superiour", [297], ["B002"], "Superiour and fore-part remain literal, although the alternative includes under-earth placement."),
        ("mars_sextile", [299], ["B017"], "Sextile, square and opposition of Mars; twelfth-house attachment unresolved."),
        ("negative_scope", [293], ["A008"], "No second not silently inserted into Lilly's no-sickness condition chain."),
        ("errata261", [295, 888], ["A027"], "Printed261 line23: usually. Body agrees."),
        ("errata262", [296, 888], ["A045"], "Printed262 line33: returning. Body agrees."),
        ("saturn_good_planets", [296], ["A043"], "Saturn in aspect with good planets; not an expressly good aspect."),
        ("boundary", [302], ["B047"], "Entire upper practical/Hermes bridge complete before the divider. Lower Hermes heading and opening remain next."),
    ]
    write("TEXTUAL_CHECKS.json", {"checks": [{"id": k, "pdf_pages": p, "record_ids": [ids[x] for x in loc],
        "finding": f, "authority": "Original source image"} for k,p,loc,f in checks],
        "errata_search_scope": "Original errata PDF888, entries within printed258–268; only261/262 entries identified in that range. No correction found there for the other retained scope problems.",
        "not_a_full_other_edition_collation": True})
    images = [{"path": p.relative_to(BATCH).as_posix(), "bytes": p.stat().st_size,
               "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((BATCH/"evidence").glob("*")) if p.is_file()]
    write("SOURCE_IMAGE_MANIFEST.json", {"files": images,
        "window_mapping": window["pages"], "selected_crops_count": sum(p["path"].endswith(".png") for p in images),
        "worker_render_scope": "Frozen reader manifests retain their original render inventories. The packet copies semantic reader files, the full original source window and selected crops; it does not bundle every redundant worker render."})
    (BATCH / "SOURCES.md").write_text("""# Source and witness guide

William Lilly, *Christian Astrology*, London, 1647. Wellcome Collection scan, catalogue work `s7z7c46y`; original scan identity `LILLY1647_WELLCOME_B30338724`.

The catalogue identifies the edition as 1647 and the digitised work as public domain. The catalogue was opened this turn; its receipt is `SOURCE_LINK_CHECK.json`. Doctrinal claims in this batch are established by the original page images, not by catalogue metadata or a search snippet.

Original PDF SHA256: `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`; 141,842,963 bytes; 894 PDF pages.

The source-window PDF has fourteen pages in this order: original PDF292–302, then PDF888 (errata), PDF277 and PDF283 (retained timing callbacks). `SOURCE_WINDOW_VERIFICATION.json` maps every page and records exact raster comparisons. Printed page numbers for the main span are258–268.

Extraction starts at DARIOT Abridged on PDF292 and ends above the divider on PDF302. Full page context includes the already-completed preceding paragraph and the next Hermes heading/opening. That context is not counted as newly extracted content.

The source is Lilly's English presentation of Dariot and his own contributions. No independently selected original Dariot edition was collated. Local marginal author labels, first-person transitions, reported Ancients and ambiguous attribution are preserved in every record. Modern clinical equivalences, outcome validation, original-language authorship of the forthcoming Hermes text, and a modern ephemeris are outside the evidence supplied here.
""", encoding="utf-8")


if __name__ == "__main__":
    build()
