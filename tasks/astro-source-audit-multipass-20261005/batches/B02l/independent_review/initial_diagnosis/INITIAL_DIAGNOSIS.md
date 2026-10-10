# Initial independent diagnosis — Lilly B02l

## Outcome

The complete admitted source span is represented in the candidate: all 92 independently reconstructed source units map to the 101 canonical records, and every canonical record maps back to the source. The full italic introduction and full upper paragraph ending **Judgments of this House** are included. No missing local section, skipped source unit, or intrusion into the following Hermes text was found.

This is **not an unqualified clean-fidelity result**. The initial pass identifies **six bounded candidate corrections**: one plural/singular source-record error, two substantive report meaning errors, two report wording-precision corrections, and one incomplete point-of-use citation. It also identifies one omitted byline-metadata ledger item. Two readings in my own frozen source-first notes were wrong; the candidate is correct on both, and those corrections are disclosed below. One contextual inheritance difference remains nonunique and is not classified as a definite candidate defect.

The helper implements only the documented origin selection, three-angle arithmetic and unsynthesized timing options. No bounded-helper behavior defect was found. Its copied 20-test suite passed; rerunning it adds zero distinct tests. Fifteen focused manual probes were also used as diagnostic evidence, without increasing the reported canonical test count. This establishes the inspected arithmetic and code behavior, not the historical method’s predictive accuracy.

## Exact source and candidate bindings

- Original source: `/workspace/scratch/bd2460f96de0/Lilly-1647-Christian-Astrology-I-III.pdf`, 894 pages; SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`.
- Candidate: `/workspace/scratch/43f75264c32e/review-candidate-b02l-01`; manifest SHA256 `41a5d97ba5c0a560c16fedbcfd24d8bd09a185b116d5d884374881f5194cbf48`.
- All 43 manifest-listed files matched their declared bytes and SHA256 values. Candidate integrity does not by itself establish source meaning.
- Main source: PDF292/printed258, **DARIOT Abridged** and its complete introduction, through PDF302/printed268, the entire upper bridge ending **Judgments of this House**. Preceding **shew death** paragraph and lower Hermes heading/text are outside this batch. Chapter XLIV remains incomplete.
- Separate context: original errata PDF888; earlier timing callbacks PDF277/printed243 and PDF283/printed249. These were independently read before candidate exposure and were not counted as new source records.

## Candidate corrections

### IF-01 — source record grammatical number mismatch

**Scope:** substantive source fidelity repair. Candidate: RULES.json: R1560/A011 title, source_statement, prerequisites[0].source_clauses[1], qualifications_and_limits[0], and duplicated source_fields proposition/conditions/uncertainties.

**Source:** PDF294/printed260, “or from the principall Significators in the Figure.”

**Diagnosis:** The original visibly prints Significators, plural. The candidate narrows that named source group to a singular significator. The repeated from and its grammatical ambiguity are otherwise retained.

**Bounded repair:** Restore plural significators in every affected canonical field and its duplicate, while preserving the existing uncertainty about how the alternatives attach. The plural does not establish a new all-of-group or vote-count rule.

**Evidence and uncertainty:** The printed plural s is directly legible in an enlarged original-PDF crop.

### IF-02 — report quantifier and exclusion drift

**Scope:** substantive source meaning repair. Candidate: AUDIT_REPORT.md: outward-cause paragraph; CLAIM_LEDGER.json: C10 text and regenerated hash.

**Source:** PDF294/printed260, “either Saturn or Mars ... and neither of them be Lords of the sixt, or Dispositors of the Moon.”

**Diagnosis:** The report restricts the exclusions to the actual afflictor. The source says neither of the two planets. A case where Mars afflicts but Saturn rules the sixth would pass the report paraphrase while failing the printed exclusions. R1562 correctly preserves neither of those two, so this is report/ledger drift.

**Bounded repair:** Say that neither Saturn nor Mars is lord of the sixth or dispositor of the Moon. Retain the strength and square/opposition conditions and the unwell/yet-not-perfectly-sick distinction. R1562 does not need alteration.

**Evidence and uncertainty:** Explicit neither of them after the Saturn/Mars pair.

### IF-03 — report callback referent error

**Scope:** substantive source meaning repair. Candidate: AUDIT_REPORT.md: earlier timing callback paragraph; CLAIM_LEDGER.json: C35 text and regenerated hash.

**Source:** PDF283/printed249, “according to the nature and quality of the Signe.”

**Diagnosis:** Printed249 attaches the selector to the sign, not the disease. The later printed267 discussion does use disease quality/nature and discretion. The report conflates these distinct selectors. The retained R1438 excerpt is already correct.

**Bounded repair:** Describe the earlier callback as referring to the sign's nature and quality; distinguish the later disease-quality/discretion qualifications. Preserve the conclusion that these passages do not supply a new combined numerical algorithm.

**Evidence and uncertainty:** The earlier original clause explicitly names the Signe.

### IF-04 — point of use source locator incomplete

**Scope:** citation repair. Candidate: AUDIT_REPORT.md: inward-cause paragraph source citation; CLAIM_LEDGER.json: C09 original_pdf_pages and bound text as needed.

**Source:** PDF293/printed259, “any Planet may in [page break] this case be malignant, if he be Lord of the eighth, twelfth or sixt.”

**Diagnosis:** The semantic statement is supported, but the sixth/eighth/twelfth lordship list is on PDF294/printed260 after the page break. R1559 correctly locates the two-page span.

**Bounded repair:** Add PDF294/printed260 to the report citation and ledger page list.

**Evidence and uncertainty:** Visible physical page break.

### IF-05 — report reference frame precision

**Scope:** wording precision repair. Candidate: AUDIT_REPORT.md: natal/mundane callback paragraph; CLAIM_LEDGER.json: C24 text and regenerated hash.

**Source:** PDF300/printed266, “the Signe of the eighth House of the yearly revolution of the World.”

**Diagnosis:** The report drops House from the source relationship. In context it likely intends the right frame, and R1629 is correct, but eighth sign is less precise and can be mistaken for an ordinal zodiac sign. This review does not claim the report explicitly says Scorpio.

**Bounded repair:** Use the sign of the eighth house of the yearly revolution of the World.

**Evidence and uncertainty:** Explicit eighth House in the source; the risk lies in the report abbreviation.

### IF-06 — report consequence connector precision

**Scope:** wording precision repair. Candidate: AUDIT_REPORT.md: no-sickness chain paragraph; CLAIM_LEDGER.json: C08 text and regenerated hash.

**Source:** PDF293/printed259, “they were not sick, or that no sicknesse would succeed upon this Quere, but that their mistrust ... was grounded upon some sudden distemper of Body.”

**Diagnosis:** The final or makes the explanatory transient-distemper clause look like a third alternative. The source gives alternative no-sickness judgments followed by an explanation of the suspicion. R1557 preserves that connection correctly.

**Bounded repair:** Describe the alternative judgments of no present or ensuing sickness together with the explanation that suspicion arose from a sudden bodily distemper soon rectified. Keep the opening negative-scope uncertainty.

**Evidence and uncertainty:** The conjunction is visible; this is a report relationship/precision correction, not a claim that an extra patient outcome has been fabricated.

## Corrections to the evaluator’s frozen source-first reading

The source-first freeze is left byte-for-byte unchanged. The diagnosis uses the original source readings after direct enlarged inspection. These are errors in my initial reading, not candidate errors:

| Correction | Original location | Frozen source-first reading | Source-adjudicated reading | Candidate disposition |
|---|---|---|---|---|
| SC-01 | PDF295/printed261; SF-026 | viscous | **vitious** | R1578 and C14 are correct. |
| SC-02 | PDF295/printed261; SF-019 anchor | the man **he** longs after | the man **she** longs after | R1569 is correct. |

Enlarged original crops `diagnostic_pdf295_vitious_reading.png` and `diagnostic_pdf295_youth_pronoun.png` support these corrections. The source-first paraphrase of the youth clause was largely neutral, but its anchor had the wrong pronoun. The cold/moist symptom paraphrase as well as its anchor had the wrong lexical reading.

The original body words **usually** and **returning** also agree with the two targeted errata entries. The enlarged returning crop shows the crowded **rn** shape; it does not support changing that word to a different spelling. This confirms C17 rather than adding a new candidate defect.

## A retained interpretive difference

IC-01 concerns the Venus/fire-sign sentence followed by **but if Mars joyne in signification** on PDF297/printed263. My source-first map left the reach of the fiery-sign condition open because it is not repeated. R1601 explicitly calls it inherited context, which is a plausible connected reading. I therefore do not label the candidate as silently inventing a condition. A qualification that this condition is inherited rather than repeated would be precise. No one-day duration is transferred to the Mars variant, and joining in signification is not falsely made a physical conjunction.

The exact intended inheritance remains uncertain. A directly inspected corresponding authorial source or explicit textual clarification could settle it. This observation does not impose another research or acceptance gate.

## All-claim and whole-report coverage

All 41 ledger texts occur exactly once in the frozen report and match their text hashes. I read the full report separately and inspected the residual text after masking those 41 units. Every substantive body paragraph and every table is bound. All **25 data rows** were individually checked: ten inventory rows, nine source-coverage rows, three arithmetic rows and three timing-correspondence rows.

`ALL_CLAIM_RESULTS.json` retains each original bound text, every component check, all table rows, the source-unit links, and the exact diagnosis. The table below gives the per-item outcome; a supported status includes the qualifications stated in the corresponding detailed result.

| Ledger item | Diagnostic result |
|---|---|
| C01 | supported with stated limits |
| C02 | supported with stated limits |
| C03 | supported with stated limits |
| C04 | supported with documentary or observability limits |
| C05 | supported with stated limits |
| C06 | supported with stated limits |
| C07 | supported with stated limits |
| C08 | report precision repair — IF-06 |
| C09 | source locator repair — IF-04 |
| C10 | source meaning repair required — IF-02 |
| C11 | supported with stated limits |
| C12 | supported with stated limits |
| C13 | supported with stated limits |
| C14 | supported with stated limits |
| C15 | supported with stated limits |
| C16 | supported with stated limits |
| C17 | supported with stated limits |
| C18 | supported with stated limits |
| C19 | supported with stated limits |
| C20 | supported with stated limits |
| C21 | supported with stated limits |
| C22 | supported with stated limits |
| C23 | supported with stated limits |
| C24 | report precision repair — IF-05 |
| C25 | supported with stated limits |
| C26 | supported with stated limits |
| C27 | supported with stated limits |
| C28 | supported with stated limits |
| C29 | supported with stated limits |
| C30 | supported with stated limits |
| C31 | supported with stated limits |
| C32 | supported with stated limits |
| C33 | supported with stated limits |
| C34 | supported with stated limits |
| C35 | source meaning repair required — IF-03 |
| C36 | supported with documentary or observability limits |
| C37 | supported with documentary or observability limits |
| C38 | supported with stated limits |
| C39 | supported with stated limits |
| C40 | supported with documentary or observability limits |
| C41 | supported with documentary or observability limits |

**Unledgered metadata MC-01:** the byline **Book II, Chapter XLIV continuation — source audit B02l, 10 October 2026.** is outside the 41 ledger texts. Its facts are supported by the source context, task batch and provided start-date metadata. Add a small metadata item, or explicitly state that the 41 ledger units exclude title/byline metadata. No substantive source text needs changing for this item. The remaining unbound headings are organizational labels or restatements reviewed in their associated sections; no additional unbound substantive body claim was found.

## Inventory, arithmetic and source-window checks

Counts were recomputed from the supplied data: 101 new records, previous Lilly 1,549, current Lilly 1,650, retained Ptolemy 1,066 and combined 2,716. Canonical source-reader tags split 54/47. Record kinds sum to 101: 7 dependency, 67 general rule, 8 illustration, 8 author experience and 11 method. These are editorial inventory categories, not independent observations or predictions.

The original span contains no individuated dated enquiry, reconstructible worked horoscope, clinical outcome series, independently checked endpoint or denominator from which an accuracy fraction can be computed. It does contain general rules, constructed examples, authorial claims about customary practice, claimed remembered success, prognostic acts and a forward promise of figures. The source-first evidence inventory keeps these categories distinct. The forward promise contributes no chart or completed case inside this span.

The 42 issue entries consist of 36 retained limits/anomalies and 6 source-resolved readings. The resolved IDs are SA-I06, B-SI-10 and ROOT-SR01 through ROOT-SR04. Source review supports the fixed-sign example construction, printed Mars sextile, node glyphs, opening Mars glyph, and body/errata usually/returning readings. A resolved glyph does not settle a separate grammatical attachment.

The 14-page window was independently rendered page-by-page and compared to the original PDF. All dimensions and all RGB sample bytes matched for main pages 292–302, errata 888 and callbacks 277/283. The eleven selected candidate crops were also visually inspected against the original-page content; this latter inspection is not described as an additional pixel-for-pixel crop provenance proof.

The synthetic 350°15′ example gives 35°15′, 80°15′ and 125°15′ after 45°, 90° and 135° displacements modulo 360°. In integer arcseconds the targets are 126,900, 288,900 and 450,900. No ephemeris, date or clinical prediction is involved.

## Helper boundaries and execution evidence

The inspected helper retains first-bed-hour priority and permits the first physician-judgment-request fallback only when the bed hour is unavailable. Its distinction between unknown and unavailable is a disclosed conservative implementation choice. Labels pass through unchanged; neither time-zone conversion nor calendar parsing occurs. A known bed hour wins over an available physician hour; unknown bed-hour availability does not authorize fallback.

Only acute-course selected-origin inputs with a supplied integer-arcsecond longitude emit the three modular targets. Zero is a valid longitude, while missing longitude is unresolved. Chronic course is not applicable. The caller must supply a longitude already corrected to the chosen hour; the helper does not validate an ephemeris or construct a chart. It supplies no contact tolerance, fourth angle, calendar date, disease outcome or treatment.

Timing options preserve moveable→days, common→weeks/months, fixed→months/years and angular/succedent/cadent correspondences as separate input dimensions. Conflicts remain unresolved. The result keeps selected unit and date empty and carries the prior-recovery-judgment requirement. It does not implement the whole illness catalogue, mind/body allocation, six/twelve-degree danger language or a clinical classifier.

The original 20-test receipt binds the tested files by hash, and all those hashes matched. The copied suite passed 20 tests with no failures/errors/skips in the private directory. This is the same 20 tests; the repeat contributes 0 distinct tests. Fifteen focused manual helper executions corroborated the source-boundary behavior and the displayed arithmetic; they are not added to the canonical count. These mechanical checks are recorded in `INDEPENDENT_INVENTORY_CHECK.json`, `HELPER_BEHAVIOR_CHECKS.json`, and the private test log/summary.

## Exposure, independence and practical limits

The source-first notes/map were completed and frozen before the candidate was opened. Original page images, rather than OCR, established source readings. OCR was only a navigation aid. The subsequent candidate pass read all canonical record fields, the full report and ledger, supporting source-data tables, the issue register, retained timing excerpts, helper/test code and relevant numeric/image data. Embedded producer descriptions in canonical records and the issue register were read after the source-first freeze as candidate claims, not as independent evidence.

I did not open separate root/producer narrative notes, rationales, reconciliation/confidence summaries, other workers’ summaries, or earlier audit narratives. I did not use an agent inventory or contact other workers. I wrote only in the private independent directory and did not change the candidate or canonical files.

Own source-first separation is directly known. Other participants’ claimed internal reading chronology is not independently observable. A file hash binds evidence identity; it does not prove that someone read an image at an earlier time. C37 therefore has an explicit observability qualification. Similarly, retained Ptolemy counts are verified against the supplied numeric snapshot and its hash, not by a new Ptolemy source audit. Reference-only flags and code behavior are visible, while external deployment, publishing, preservation and owner-delivery operations remain outside this role.

This is same-family contextual separation, not cross-family review, an expert historical edition, clinical review or IV&V. The findings are diagnostic and source-adjudicated. Root retains the authority to apply or reject a flag with source evidence. The agreed continuation is at most two checks of changed items if requested, with no additional assurance gates.

## Artifact map

- `DIAGNOSTIC_FINDINGS.json`: six candidate corrections, two evaluator corrections, one interpretive difference.
- `SOURCE_RECORD_COVERAGE.json`: all 92 source units, all 101 reverse record mappings, source anchors, conditions/qualification checks and evidence inventory.
- `ALL_CLAIM_RESULTS.json`: all 41 ledger items, every component and 25 table rows, plus the independent missed-claim scan.
- `EXPOSURE_AND_METHOD.json`: exact method, exposure sequence, consulted and unconsulted material, observability limits and role scope.
- `CANDIDATE_INTEGRITY_CHECK.json`, `CLAIM_TEXT_BINDING_CHECK.json`, `FIELD_CONSISTENCY_CHECK.json`: file/text/duplicate-field bindings.
- `INDEPENDENT_SOURCE_WINDOW_CHECK.json`, `INDEPENDENT_INVENTORY_CHECK.json`, `HELPER_BEHAVIOR_CHECKS.json`: independent mechanical checks.
- `diagnostic_test_copy/INDEPENDENT_TEST_RUN.log` and `diagnostic_test_copy/TEST_RUN_SUMMARY.json`: actual private repeat of the copied suite.
- `INITIAL_DIAGNOSIS_FREEZE.json`: byte counts and SHA256 bindings for this complete initial diagnosis and its supporting evidence.
