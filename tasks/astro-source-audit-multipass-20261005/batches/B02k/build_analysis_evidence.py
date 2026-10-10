"""Build bounded arithmetic and callback receipts from actual local evidence."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path

import lilly_sixth_opening_reference as ref

ROOT = Path(__file__).parent


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    motion = []
    for label, seconds in [("13°09′59″", 47399), ("13°10′00″", 47400),
                           ("13°10′18″", 47418), ("13°10′36″", 47436)]:
        result = ref.moon_speed_comparisons(seconds)
        motion.append({"input_dms": label, "input_arcseconds_per_24_hours": seconds, **result})
    assert ref.MEAN_MOON_ARCSECONDS - ref.RETROGRADE_ANALOGY_ARCSECONDS == 36
    assert motion[1]["below_stated_mean"] and not motion[1]["under_retrograde_analogy_threshold"]
    result = ref.remaining_degrees_in_sign(29, 30, 0)
    assert result["remaining_degrees"] == Fraction(1, 2) and result["time_unit"] is None
    rejected = []
    for coordinates in [(Fraction(59, 2), 59, 0), (Fraction(59, 2), 30, 0)]:
        try:
            ref.remaining_degrees_in_sign(*coordinates)
        except ValueError as exc:
            rejected.append({"coordinates": [str(x) for x in coordinates], "exception": str(exc)})
    assert len(rejected) == 2
    save("ARITHMETIC_CHECKS.json", {
        "batch": "B02k", "execution": "python build_analysis_evidence.py", "executed_successfully": True,
        "input_class": "Controlled examples for exact source-reference arithmetic; no historical horoscope is computed.",
        "stated_mean": {"dms": "13°10′36″", "arcseconds": ref.MEAN_MOON_ARCSECONDS,
                        "source_pdf_page": 114, "retained_record": "LI.1647.I.14.R192"},
        "retrograde_analogy": {"dms": "13°10′00″", "strictly_less_than": True,
                               "arcseconds": ref.RETROGRADE_ANALOGY_ARCSECONDS,
                               "source_pdf_page": 114, "retained_records": ["LI.1647.I.14.R195", "LI.1647.I.14.R221"]},
        "threshold_difference_arcseconds": 36, "motion_comparisons": motion,
        "remaining_arc_example": {"input_dms": "29°30′00″", "remaining_degrees_exact": "1/2", "time_unit": None,
                                  "source_pdf_page": 283, "record_id": "LI.1647.II.XLIV.R1438"},
        "aggregate_domain_counterexamples_rejected": rejected,
        "arithmetic_checks_are_not_additional_unittest_identities": True,
        "predictive_or_clinical_validation": False,
        "helper_sha256": hashlib.sha256((ROOT / "lilly_sixth_opening_reference.py").read_bytes()).hexdigest()})
    retained = json.loads((ROOT / "RETAINED_SOURCE_EXCERPTS.json").read_text())
    assert len(retained["excerpts"]) == 4
    save("CROSS_SOURCE_COMPARISONS.json", {
        "batch": "B02k", "comparison_type": "Targeted within-Lilly callbacks; not a completed multi-author synthesis.",
        "comparisons": [
            {"id": "CB01", "new_records": ["LI.1647.II.XLIV.R1364", "LI.1647.II.XLIV.R1365", "LI.1647.II.XLIV.R1366"],
             "new_source_pages": [277, 278], "retained_record": "LI.1647.I.XIX.R523", "retained_source_page": 153,
             "source_connection": "Lilly expressly names printed page119 for planet-in-sign body members.",
             "result": "Saturn/Cancer cell is Reins, Belly, Secrets. The separate house/sign/planet disease catalogues are not substituted for this cell.",
             "uncertainty": "The illustration adds symptoms and offers alternatives; the cell alone is not a diagnosis. Other altered cells remain unfilled.",
             "new_record_count_increment": 0},
            {"id": "CB02", "new_record": "LI.1647.II.XLIV.R1467", "new_source_pages": [285, 286],
             "retained_records": ["LI.1647.I.14.R192", "LI.1647.I.14.R195", "LI.1647.I.14.R221"],
             "retained_source_page": 114,
             "source_connection": "XLIV names the Moon's mean motion without a number; the audit explicitly uses Lilly's earlier stated mean.",
             "result": "Mean13°10′36″ differs from the strict under13°10′ analogy. The same-work link is declared by the audit, not an explicit printed page-reference in XLIV.",
             "uncertainty": "This does not establish actual physical retrogradation or compute the full aspect-qualified sickness rule.",
             "new_record_count_increment": 0}],
        "future_dependencies": [
            {"source_pdf_pages": [289, 290], "dependency": "Natal positions, profection and five hylegical places; local prerequisites retained, later nativity method not completed in this block."},
            {"source_pdf_page": 289, "dependency": "Crisis timing is invoked without completing the later Dariot material."},
            {"source_pdf_page": 292, "dependency": "DARIOT Abridged heading and full italic introduction are the next extraction, not admitted records in B02k."}],
        "retained_excerpt_file": "RETAINED_SOURCE_EXCERPTS.json", "retained_excerpt_count": 4,
        "additional_source_records": 0})
    ptolemy = json.loads((ROOT / "RETAINED_PTOLEMY_INDEX_SNAPSHOT.json").read_text())
    batch_total = sum(x["records_count"] for x in ptolemy["source_batches"])
    book_total = sum(x["records"] for x in ptolemy["books"].values())
    assert batch_total == book_total == ptolemy["source_records"] == 1066
    save("PTOLEMY_COUNT_RECEIPT.json", {
        "count_basis": "Retained published Ptolemy index, carried through B02j; no Ptolemy source rereading is claimed in B02k.",
        "retained_file": "RETAINED_PTOLEMY_INDEX_SNAPSHOT.json", "retained_file_sha256": hashlib.sha256((ROOT / "RETAINED_PTOLEMY_INDEX_SNAPSHOT.json").read_bytes()).hexdigest(),
        "retained_batches": len(ptolemy["source_batches"]), "sum_of_batch_counts": batch_total, "sum_of_book_counts": book_total,
        "new_ptolemy_records": 0, "new_lilly_cumulative": 1549, "combined_inventory": 1549 + batch_total,
        "independent_predictions_or_accuracy_denominator": False})
    print(json.dumps({"arithmetic_receipt": "executed", "retained_callbacks": 4, "retained_ptolemy_batches": len(ptolemy["source_batches"]), "combined_inventory": 1549 + batch_total}))


if __name__ == "__main__":
    main()
