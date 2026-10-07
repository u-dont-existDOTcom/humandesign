# B01o: general method and regional context

Read `REPORT.md` for scope and findings. `RULES.json` retains all 37 records from English II.1–II.2; `GENERAL_CONTEXT_TABLES.json` preserves the taxonomy, five context-specific definitions, six historical portraits and local modifiers. `SECTION_COVERAGE.json`, `READING_RECEIPT.json`, `SOURCE_PAGE_QC.json` and `UNRESOLVED_INTERPRETATIONS.json` separate read material, locators, commentary and unresolved choices.

`b01o_reference.py` is only a source-reference reader, not a chart or population classifier. Run `python3 -m pytest -q tasks/astro-source-audit-multipass-20261005/batches/B01o/test_b01o_reference.py` from the repository root. It uses only Python and pytest and does not require the private PDF.

`B01n_RECOVERY_VERIFICATION.json` records the completed archive restoration and the fresh recovered cumulative test run. Original B01n reports retain their original pending-status statements as historical receipts; they were not rewritten to suggest earlier work had occurred.

`VERIFICATION.json` records the final combined run for this increment. Source records, reading claims, bounded software tests and empirical validation are different evidence classes. No raw books, full OCR, personal data or page images are part of this packet. The next exact reading boundary is in `NEXT_HEADINGS.json` and the canonical task checkpoint.
