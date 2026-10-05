# Work handoff — astrology source acquisition and conditional-rule audit

## Current owner outcome

Improve the astrology methodology in the current reasoning session and develop/acquire an edition-specific source list. The V2 method and evidence-integrity checker are delivered; the full source-reading/implementation audit is not yet completed. The next executable work is to finish source access and inventory/extract the declared corpus without using participant outcomes to choose rules.

Repository: `u-dont-existDOTcom/humandesign`.
Integration branch: `research/six-rule-life-timing-20261001`.
Producer branch: `research/astro-method-v2-sources-20261005`.
Original base: `1b4553d0f9f03360a057cb7677be6a0969a8ae1e`.

Fetch live UDA AGENTS/LESSON-INDEX, then the repository's current AGENTS and person-life index/catalog. Use a fresh isolated writer branch from the current research head; do not alter production/main, runtime inference, surveys or historical prediction freezes. No purchase, author contact, participant contact or paid API use is authorized. A source-only worker must not read personal histories, outcome tables, surveys or named-case readings; route/catalog metadata may be read without following their participant-evidence links.

## Sources already downloaded on the authorized computer

Set the private source directory (no raw books in Git):

```bash
export ASTROLOGY_SOURCE_DIR="$HOME/Documents/astrology/source-audit-20261005"
```

The acquisition manifest lists the five downloaded PDF files, exact SHA-256 values, byte counts and parser page counts: Lilly 1647, Valens/Riley, Phaladeepika/Sastri 1950, Brihat Jataka/Iyer 1885, and Leo 1906. A Lilly search-text derivative is also local. Preserve publisher/translator restrictions; do not include these raw texts in Git or public delivery archives. Check existing hashes before downloading again.

These files are acquired/parser-checked, **not source-audited**. Lilly's Wellcome copy is catalogued with a missing final leaf: determine what is missing rather than assuming a blank leaf. Phaladeepika identity is confirmed on PDF page 4, but its 28-chapter text has not been read end-to-end. Riley's translation is explicitly preliminary/unperfected. Preserve editorial and pagination markers.

## Exact access gaps and available routes

InfoAccess is AVAILABLE through the existing local HTTP MCP configuration and was actually invoked. No new installation or account is required. Read the configuration privately through the authorized runtime; never print, copy into artifacts, or send its authentication headers elsewhere. Discover the current `tools/list` schema before invoking it.

The structured `title`/`author` searches returned no records, but relaxed `query` searches found some relevant witnesses. Use exact edition validation rather than trusting default “newest EPUB” ranking. The Dykes search was paginated through all 58 returned records and did not find the targeted Benjamin Dykes books. “Persian Nativities” hit a bounded 1,000-record scan; that is not a globally exhaustive absence finding.

Actual retrieval history, also stored in `INFOACCESS_ACQUISITION_REPORT.json`:

| Witness | Returned MD5 | Result |
|---|---|---|
| Dorotheus/Pingree, not the requested Dykes edition | `28738b569870c3fd51aaa836cd78672f` | `no_usable_catalog_path` |
| Waddell/Robbins combined Manetho/Tetrabiblos, listed 1964 | `c7151e1e7b087bf74eb6eefce5a67c0c` | Reader busy on initial attempt and one retry; direct-file fallback: no fast-download record |
| Greenbaum, Late Classical Astrology (2001) | `5b89ada7aac7785017efe87813614fc6` | `no_usable_catalog_path` |

Do not repeatedly resubmit unchanged terminal MD5 failures. Search for a current correctly identified record or use legitimate publisher/library/owned-copy access. A catalog hit is not a successful acquisition. Do not invent a MD5 or silently switch translations.

For a returned record, the observed current API route is `start_document_retrieval(md5, start_page, end_page)` followed by `document_retrieval_status(operation_id)`; `get_document(md5, download=true)` requests a temporary file URL. Recheck live schemas. Store book bytes privately and record only safe provenance/status/hashes in Git. Do not expose temporary URLs or credentials in the handoff.

**Ptolemy:** the complete Robbins translation is verified online at the LacusCurtius source in the manifest. Terminal HTTP capture failed. Use normal authorized browser access to save each book's linked parts, retaining headings/page anchors and a complete link manifest; do not call a homepage or selected excerpt the full work.

**Hāyanaratna:** Gansten's author page confirms open access and links DOI `10.1163/9789004433717`. OAPEN and Brill PDF endpoints returned HTTP 403 to terminal requests. Try normal browser download or an authorized open-access repository mirror; preserve the same 2020 critical edition. Do not interpret a 403 as a requirement to buy an open-access book.

**Commercial editions:** prioritize the five P1 titles, using owned/licensed library access or an approved purchase. No spending without explicit approval. For BPHS require both volumes of the named translation, not an anonymous partial PDF. For Abu Ma’shar use Persian Nativities **IV**, not the partial III. Dorotheus requires the current second updated Dykes edition, not a silently substituted Pingree witness. Keep alternative witnesses as separate source IDs.

An idempotent public-download helper is available for entries with a verified direct-file URL:

```bash
python3 scripts/acquire_astrology_sources_v2.py \
  --manifest reference/research/ASTROLOGY_SOURCE_ACQUISITION_V2.json \
  --dest "$ASTROLOGY_SOURCE_DIR" \
  --ids LILLY1647 VALENSRILEY PHALA1950 BRIHAT1885 LEO1906
```

This checks hashes for existing files and does not override access restrictions. Review its per-title receipt; exit success alone does not certify complete acquisition. The current manifest has no direct download URL for unresolved commercial titles.

## Source-audit sequence

1. **Fix a bounded corpus.** Start with P0; admit P1 for the named missing families and treat P2 as declared extensions. Do not keep enlarging the corpus to explain known outcomes.
2. **Inventory every section.** Record work/edition/file hash, printed versus PDF pagination, chapter/verse IDs, missing pages, translations, commentary, tables and figures. Use `templates/astrology/SOURCE_SECTION_V2.template.json`. A page count or keyword search is not full coverage.
3. **Read and extract conditional rules.** Use `RULE_SPEC_V2.template.json`: source genre, frame, prerequisites, antecedents, exceptions, modifying conditions, consequence, exact calculation conventions, semantic attribution, dependencies, ambiguous alternatives and fixtures. Quote only what is needed and permitted; do not redistribute whole copyright texts.
4. **Maintain genre separation.** Natal, horary, mundane, electional, Parāśari and Tājika statements do not silently substitute for one another. Translation/editor interpretation is not the original author's assertion.
5. **Reconcile ambiguities without outcome-fitting.** Preserve author variants as branches. Check crucial translation terms against the original or an independent translation where materially relevant. Do not resolve disputed choices by which one fits a participant.
6. **Implement the admitted dependency closure.** Full geometry, opposite aspect orientation, 0/360 wrap, conditional states, birth-time uncertainty, calendrical conventions and source-native modifications must have deterministic tests. A strength-house proxy is not a complete strength calculation.
7. **Replay worked examples carefully.** Verify historic calendar, local-time convention, coordinates, sexagesimal values and translator corrections before deciding the implementation is wrong or the source succeeded. Source examples test reproduction, not independent human prediction.
8. **Freeze a case-specific analysis contract.** Account for every catalog entry, select relevant modules, pin protocol/catalog/input hashes, and commit the expected rule universe before scoring outcomes. A narrow name question need not run every technique, but omissions must be explicit.
9. **Use V2 receipts.** Populate real artifact hashes and JSON pointers/line spans. Validate against the externally preserved contract SHA. The verifier checks identity/coverage—not semantic correctness or actual blinding. No invented claims to fill a form.
10. **Only then assess added predictive value.** Retain original candidates, false peaks and scope restrictions. New source-derived or fitted combinations are allowed as new versions. Do not claim that agreement between reused chart facts is independent evidence.

## Executable V2 check

Author the run contract from `RUN_CONTRACT_V2.template.json`; the template is intentionally invalid until populated. Preserve its hash outside the mutable receipt before outcome evaluation.

```bash
python3 scripts/new_astrology_deep_analysis_receipt_v2.py \
  --contract path/to/committed-contract.json --out path/to/receipt.json

python3 scripts/validate_astrology_deep_analysis_receipt_v2.py \
  --contract path/to/committed-contract.json \
  --contract-sha256 ACTUAL_PRECOMMITTED_SHA256 \
  --receipt path/to/receipt.json \
  --evidence-root path/to/evidence-directory \
  --require-executed
```

A generated template must fail until completed. A correctly recorded unavailable module returns `SCOPED_WITH_GAPS`; it cannot be labelled fully executed. Outcomes after forecast time must stay unavailable to the forecast, but future ephemeris positions that were calculable at issue time are not themselves outcome leakage. Historical centered/trailing candidates remain unchanged.

## Completion evidence

Update the acquisition manifest and section/rule coverage as work progresses. Finish at the actual achieved level: acquired, source-extracted, implemented, example-reproduced, or evaluated. Report unresolved access and interpretation separately. Source completeness is bounded to the declared editions/sections, not “all astrology.” Preserve a precise executable continuation; do not ask the owner to reconstruct the history or redownload verified files.
