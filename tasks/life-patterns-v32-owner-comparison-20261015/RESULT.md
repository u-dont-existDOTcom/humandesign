# V3.2 guided cognitive pilot, old-survey crosswalk and DOB inference audit — 2026-10-15

## Delivery and what changed

Created a **versioned experimental V3.2 questionnaire** (not a change to the active participant Custom GPT). Its new section presents the eight candidate prompts from the completed owner-development assessment; six are core cognitive contrasts and M05/M03 are visibly optional with scoring suspended. Original 25 V3 questions, editable previous selections/free text, eight context explanations and three unusual-behavior records are independently preserved. Each newly answered V3.2 response lives under `v3_2_answers` in an explicitly different JSON schema. The app never treats earlier source text as a response to new wording.

The generated offline HTML is deterministic. It can import a saved V3 or V3.2 export, preserve context, download the updated file, and works without external requests. The existing V3 HTML, live Custom GPT, production Railway, frozen V7/TF1 bank, and chart/scoring engine were not modified.

## Private owner delivery

Files available in the owner's `~/Téléchargements/` directory (NOT committed to Git):

- `Life-Patterns-V32-PRIVATE-2026-10-15.html`: private prefilled questionnaire with saved V3 25/25, guided followups 8/8 and three behaviors; empty new V3.2 answers; mode 0600.
- `Life-Patterns-V32-Experimental-Blank-2026-10-15.html`: empty generic offline questionnaire for new research participants.
- `.life-patterns-private-v32-20261015/Life-Patterns-V32-vs-V3-vs-Old-PRIVATE.html`: detailed owner-private, browser-readable crosswalk containing eight full source-aware revisions and their previous actual answers.
- Companion private Markdown/JSON comparison files in the same hidden directory, mode 0600.

`Life-Patterns-Researcher-Guide.html` now contains an idempotently installed link to the prefilled questionnaire and full private comparison. Original guide preserved as a local private backup.

**No private respondent wording, birth input, distinctive habits, or raw source hashes enter the committed files.**

## Reproducible evidence

Original and enriched V3 exports compared from actual owner-private source; original `selected`, `other`, `unsure` and `skip` fields preserved across all **25** entries and all **3** unique behaviors remain identical. The eight guided routes are answered; **6** distinct conditional rules and **4** actual-case fields added. The historical source crosswalk identifies **24/25** direct older question routes; 79 and 84 turn snapshots strongly overlap and cannot count as independent human observations. The eight item-by-item changes and source excerpts are only in the local private report.

The eight amended V3.2 question wordings are **not yet independently administered**, and all eight have zero scoring-admitted behavior/chart mappings or weights. The added richness is evidence for source specificity, **not** birth-date inferability.

### Birth-date question — historical comparison versus a new test

- **New V3.2 birth-date rerank:** **NOT RUN / NOT TESTABLE**, because there is no predeclared admitted bridge from these eight new questions to chart predicates. Inventing scores or choosing favorable interpretation from the known owner DOB would be circular.
- **Accepted V1.4d fitted astronomical reference:** 52,596,001-minute century scan; recorded 10:25 UTC moment is **jointly #1** with eight neighboring minute instants, and January 29, 1985 is the only maximum-scoring calendar date. The older V4.3/NetInformation #1,562 diagnostic was discarded as the owner-facing comparison benchmark. Neither result is independent survey-to-DOB validation.
- The separately frozen six-rule V1.4 selected model was fitted to the known birth, and its rare six-positive case is not evidence of generalizable date identification.
- Consequently no new claim of natal recoverability or independent validation is made.

## Verification

- Synthetic browser: eight V3.2 prompts, prior source exactly retained, export/reimport, mode-select and suspended-item state, **0 browser script errors, 0 network requests**.
- Owner-private prefilled browser: **25** prior responses, **8** context additions, **3** distinctive behaviors; **0** invented V3.2 responses; private file mode 0600; no private text logged.
- Focused Python tests: **15 pass** across four relevant modules.
- All unit tests with exact worktree interpreter path (`PYTHONPATH=src:.`): **977 pass, 6 skip** (missing production Swiss ephemeris files, unrelated to the pilot).
- Python lint for authored files: **PASS** (embedded HTML/JS long strings intentionally exempted from E501).
- Full project-wide pytest (with `PYTHONPATH=src:.`): **1051 passed, 6 skipped**; skips only for unavailable production Swiss Ephemeris files.
- Scripted generated HTML drift check: PASS.
- Source and privacy audit: only aggregate counters in Git; owner-private free text and personal birth input never staged. The new chart-scoring state remains explicitly zero.

## Reuse commands

```bash
python3 tasks/life-patterns-v32-owner-comparison-20261015/build_v32_pilot.py --check
PYTHONPATH=src:. python -m pytest -q tests/unit/test_life_patterns_v32_owner_comparison.py
PUPPETEER_MODULE=/path/to/puppeteer node tasks/life-patterns-v32-owner-comparison-20261015/test_v32_browser.cjs
```

The private comparison generator requires two prior owner exports and their previous private source crosswalk in the owner Downloads folder. It is deliberately not part of CI. Never stage its resulting personal HTML, JSON or Markdown files.

## Next scientific gate

A new versioned chart-predicate mapping, neutral behavioral coder, decoy universe and frozen model are required before a new DOB identification test. Test new participants whose chart data remain concealed during question design, and treat this one-person material as development only. The prior zero-scored state must not be silently presented as improvement.


## Reference correction — 2026-10-15

The prior V4.3 NetInformation #1,562 description in this historical note is **not the accepted comparator**. Owner-corrected reference: fitted six-rule AstroHD V1.4d's 52,596,001-minute century scan. On its one-minute grid, all nine maximum-scoring minutes occur on January 29, 1985 (10:18–10:26 UTC), including the recorded time (joint #1). The V1.5 five-domain behavioral bridge exists separately; determining typical meaningful role-entry sequence from actual episodes is the remaining measurement gap. Read the correction as superseding—not deleting—the obsolete benchmark text above. No new participant DOB recovery is claimed.
