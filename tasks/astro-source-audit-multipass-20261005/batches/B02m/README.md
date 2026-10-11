# Hermes in Lilly: source-record packet

Start with **AUDIT_REPORT.md**, then **ACCEPTANCE.json** and **SOURCE_REVIEW_STATUS.json** for the actual review stage. **CONTINUE_HANDOFF.md** gives the exact next passage. Publication, delivery and extracted-archive usability are separate recorded operations; none is implied by a draft or a successful test.

This packet preserves the Hermes-headed section of Lilly’s 1647 Christian Astrology, original PDF302 below the divider through PDF316 above the next divider. It contains52 documentary records, not52 independent predictions. Original page images govern the wording; the JSON is a normalized, condition-preserving source representation, not a diplomatic edition or modern medical guidance.

## Run the portable checks

Extract the ZIP to a new directory, then from its B02m directory run:

    python3 verify_archive_contents.py
    python3 run_verification.py

The second command runs36 distinct standard-library tests and refreshes TEST_RUN.log and TEST_RUN_SUMMARY.json. Check the archive hashes first, because those two execution files change when rerun. Repeated executions add zero test identities. No original full PDF, private repository checkout, network access or external Python package is required by this entrypoint.

## Authority and history

RULES.json must be read using source_statement, source_details, prerequisites and exceptions together. REFERENCE_TABLES.json links the two twelve-sign catalogues. MATERIA_MEDICA_TABLES.json preserves column-level source entries and unresolved lexemes. TEXTUAL_CHECKS.json separates body readings, printed errata and damaged pagination. UNRESOLVED.json retains24 qualifications and unresolved issues; it is not a count of scientific errors.

The material under recovery/original_draft and source_drafts is historical producer work, not current authority. In particular, the original draft dropped the word no in the Scorpio/Saturn urinary statement. The correction and all other recovery amendments remain traceable to the original draft and original scan. Some original maintenance scripts assume their original directory layout; the only portable verification entrypoints promised here are the two commands above.

The initial independent-review input manifest binds the exact candidate reviewed; its eight minor defects and an ambiguous printed negative have been documented and corrected or preserved as unresolved. Its findings and any later reconciliation are kept separately; producer corrections are never relabeled as independent review. Byte hashes and passing structural tests are not proof of source meaning, ancient authorship, medical efficacy or predictive accuracy.

The full source PDF remains external:894 pages,141842963 bytes, SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b. The fifteen included PNGs matched fresh renders from it in RGB. The next passage is original PDF316 below the divider, Astrologicall Aphorismes beneficiall for Physicians, beginning with the first aphorism. Next recordR1703. ChapterXLIV and the wider audit remain open.
