# Astrology deep analysis — V2 method and source plan

5 October 2026

This package improves the research procedure and its evidence-integrity checks. It does not contain a newly validated astrology model, a completed reading of the source corpus, or any private participant outcomes. Full book files remain outside Git and outside this package.

## Read first

- **[Methodology V2](../../reference/research/ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V2.md)** — the substantive protocol, including conditional source rules, whole-chart synthesis, information boundaries, timing and source completeness.
- **[Source reading/acquisition list](../../reference/research/ASTROLOGY_SOURCE_READING_LIST_V2.md)** — 17 prioritized titles, exact editions, their purpose and current access state.
- **[Work handoff](WORK_HANDOFF.md)** — exact continuation, available InfoAccess route, retrieval failures, source-audit sequence and shell commands.

## What changed

V1's validator accepted a synthetic record in which every required module was unavailable and the only claim cited a nonexistent file. That test demonstrated a coverage-check weakness, not an astrology result.

V2 separately checks the committed plan, complete catalog disposition, actual artifact hashes and references, expected module/check/rule sets, and evidence-mode identity. Missing execution remains a visible gap. The checker explicitly does not certify semantic correctness, actual blinding or predictive validity.

The methodological revision also preserves prerequisites and exceptions within each source rule, separates original authors from commentary and modern interpretations, retains meaningful combinations, and distinguishes forecast-time knowledge from later outcomes. Knowing a future ephemeris position is not itself outcome leakage; selecting a rule after the event is.

## Source acquisition achieved

Five PDFs were actually downloaded and parser/hash checked on the authorized computer: Lilly 1647 (Books I–III facsimile), Valens/Riley, Phaladeepika/Sastri 1950, Brihat Jataka/Iyer 1885 and Leo/The Progressed Horoscope 1906. The source manifest gives exact hashes, page counts and caveats. None has been fully source-audited in this task.

InfoAccess was reachable and used. Relevant catalog records did not yield a successful full-file retrieval in the attempted paths. Unresolved works are explicitly marked, with authorized publisher/library alternatives and Work instructions. No purchase or paid API was made.

## Files and tests

Machine authorities: `ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V2.json` and `ASTROLOGY_SOURCE_ACQUISITION_V2.json` in `reference/research/`.

Executable tools:

```bash
python3 -m pytest tests/test_astrology_receipt_v2.py -q
python3 scripts/new_astrology_deep_analysis_receipt_v2.py --help
python3 scripts/validate_astrology_deep_analysis_receipt_v2.py --help
python3 scripts/acquire_astrology_sources_v2.py --help
```

The new tests use synthetic evidence only. Templates in `templates/astrology/` are intentionally unfinished and must not pass as completed work. When integrating, also run the retained V1 catalog/protocol regression tests.

Repository: `u-dont-existDOTcom/humandesign`; research integration branch `research/six-rule-life-timing-20261001`. The revision changes research procedure only; it does not modify historical candidate rules, prediction freezes, production/main, participant surveys or deployed applications.
