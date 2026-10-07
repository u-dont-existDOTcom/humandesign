# B01m — Ptolemy IV.9 source audit

Read `REPORT.md` first. `RULES.json` contains 59 conditional source records with edition/page/attribution links. `QUALITY_OF_DEATH_TABLES.json` structures five planetary spectra and twenty conditional examples without making them independent observations. `SECTION_COVERAGE.json`, `READING_RECEIPT.json` and `SOURCE_PAGE_QC.json` specify exactly what was read.

`UNRESOLVED_INTERPRETATIONS.json` retains twenty open issues. `CROSS_SOURCE_COMPARISONS.json` contains three bounded Rhetorius comparisons, not a complete Rhetorius chapter audit. `INTRASOURCE_QUALIFICATIONS.json` records dependencies within Ptolemy. `CLAIM_CHECK.json` is a documented self-check, not independent adjudication.

The standalone `b01m_reference.py` retrieves source rows and evaluates caller-supplied Boolean/unknown conditions only. It computes no natal chart, longevity estimate, medical diagnosis, violence propensity, or individual forecast. Required `scope` and role labels prevent accidental reuse as generic planetary descriptions. False/unknown branches provide no contrary real-world conclusion.

Run the isolated tests with `python -m pytest -q test_b01m_reference.py` from this directory. `VERIFICATION.json` records the actually run combined suite, while `PROTECTED_CONTENT_VERIFICATION.json` records preservation. `APPLY_CHECKPOINT.py` is a one-time base-bound update of the four current progress files, not a reusable reset command.

Original PDFs, full OCR, and page images are kept in the owner's private source store, not in this packet or Git. Next batch: full IV.10 and both endings; exact locators in `NEXT_HEADINGS.json`.
