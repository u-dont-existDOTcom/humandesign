# Hellenistic source-reading checkpoint C04 — 23 October 2026

**SUPERCEDING C05 SOURCE UPDATE (23 October):** [Paulus nocturnal C05 source report](HELLENISTIC_SOURCE_C05_NIGHT_AND_SECOND_PAPYRUS_20261023.md) checks Greek Paulus ch2/ch32 and reconstructs nighttime seven-star cycle with an explicit source/edited table discrepancy of **34/120 day cells**. A second ancient horoscope (P.Oxy. 4277), reported by Tolsa 2017, matches the by-sign arithmetic in **1/3** entries and retains two negatives. [C05 checkpoint](HELLENISTIC_CONTINUATION_C05_20261023.md) replaces C04's previous claim that no nighttime source instructions could be located. An authenticated separate nighttime manuscript *table* remains absent, and the Greek transcription's exact critical-edition lineage remains unverified. Source-only test suite 31/31, zero human validations.


Status: **SOURCE_RESEARCH_ACTIVE / SCIENTIFIC_PROGRAM_OPEN**. Research branch only; **no human prediction has been frozen, evaluated, promoted or validated**. Owner instruction: continue reading astrology primary books already available; preserve everything in `humandesign`; do not use Work mode to extract Amazon *Primary Directions*.

## Authoritative recovery path

This checkpoint supersedes narrower C03 next-action notes only where described; it does not overwrite other Western/Jyotish/Chinese/Tibetan/Maya research branches or the canonical `docs/astrology-research-map/WORKFLOW.mmd`.

1. [C04 substantive source report](HELLENISTIC_SOURCE_C04_GREEK_PAULUS_PAPYRUS_20261023.md) — Greek Hephaistio numerical variants, Greenbaum Paulus monomoiria by trigon, separate chapter-5 by-sign reconstruction on 319 CE papyrus and completion of Paulus ch33–37. This report is the source of C04's actual conclusions.
2. [Versioned Greek/English numeric ledger](HEPHAISTIO_C04_GREEK_ENGLISH_NUMERIC_VARIANTS_V1.json) — Greek transcription source SHA-256 and disputed numbers.
3. [Paulus corrected editorial *by-trigon* daytime canon](paulus_monomoiria_source_c04.py) — four triplicities, each of 30 degrees; **no** fully resolved night rule, not a generic face/decan; a scholion example conflicts.
4. [Paulus *by-sign* papyrus reader](paulus_bysign_papyrus_c04.py) — Chaldean-order formula and seven unambiguous ancient data rows. Six match; **Mercury fails and remains a negative result**, not silently corrected.
5. [C04 source-to-test registry](HELLENISTIC_C04_SOURCE_TO_TEST_CANDIDATES_V1.json) — four **not-eligible-for-human-prediction** research candidates. Cross-tradition map index `README.md` updated; prior C02/C03 source notes have supersession notes.

## New evidence and precise status

- Accessible Eulogikon Greek Book II ch29/ch36 directly inspected at `https://eulogikon.org/works/hephaestion-thebes-effects-tco-ab.md`; **905747-byte file SHA256** `2265293a6088920adbb487fe91ede7d275db21674da6b997fb98a9584a6c6d63`, retrieved 2026-10-23. Host dynamic metadata may change; **not independently collated manuscript** and exact critical-edition lineage remains unverified. Keep English and Greek source variants separate.
- Hephaistio Greek main = **360** days; Greek finer headings = **365**; Schmidt English finer headings = **375** due to printed **Moon 81** instead of Greek **71**. Greek's **Mercury 52→57** and other finer-table ±1 discrepancies remain unresolved; potential 5-day intercalation is *not demonstrated* by the immediately checked text. Saturn→Mercury **150** present both Greek and English, versus 140 in later interpolated Valens appendix. No original-variant “correction” admitted.
- Paulus Greenbaum ch32, printed pp66–69, visual source checked: editorial corrected **day** table. One scholion gives **Cancer degree 8 = Venus**, printed table **Mars**. Only that example of variant is witnessed: do not generate hypothetical night table from it.
- Independent *historical calculation* artifact: 319 CE papyrus P.Berl. 9825, via Greenbaum & Jones, `ISAW Papers` 12 (2017), PDF pp13–14 and scholarly analysis p31. By-sign monomoiria reconstructs **six of seven** unambiguous recorded attributions. Mercury on the papyrus is **incorrect compared with the algorithm**; no life events were checked. Jupiter “its own monomoiria” is ambiguous and excluded from the denominator. **This is ancient calculation/fidelity evidence, NOT human astrology predictive validation.**
- More Paulus actual reading complete in the owned truncated scan: ch33–37 printed pp68–77. Ch34 provides a neutral source example **8 directed zodiac degrees × 14 months per degree = 112 months = 9 years 4 months** at a specific ancient klima, but no verified event or historical calendar; ch36 contains selection rules and lifespan claims that are not safe clinical forecasts; ch37 *Thema Mundi* is hypothetical cosmology, not an empirical human record. The full Olympiodorus commentary remains **absent** from the owner's PDF.

## Test receipt

Exact versioned inputs for the test suite were **fetched fresh** from GitHub contents API into a temporary directory on authorized owner laptop (no source file copied into public Git), then:
```
python3 -m unittest discover -s <temporary_source_directory> -p 'test_hellenistic_*.py' -v
```
**22/22 tests PASSED**, covering 4 prior arithmetic tests, 5 daily-rate tests, 7 C04 Greek and edited by-trigon tests and 6 C04 papyrus by-sign tests. None is a behavioral or predictive-efficacy test. Existing C01/C02 tests were not retrofitted to “validate” sources.

## Safe next scientific steps after C04

1. **Critical edition origin:** determine provenance of Eulogikon Greek, compare primary Hephaistio II.29/36 numerals to independently published Pingree Greek critical apparatus where legitimately accessible. Distinguish typo/editing, cross-edition variants, and calendar hypotheses. No ungrounded correction to 129-month subperiods.
2. **Day/night trigon:** inspect Greek Paulus ch32 and surviving manuscript tables (or verified Greenbaum annotations) for a real nocturnal cycle, rather than generating it from one scholion. Source-first any nightly reconstruction separately from printed corrected day table.
3. **Historical parity extension:** verify surviving documentation for the Jupiter and prenatal full Moon 319 CE entries and papyrus line citations. Only then enlarge the seven-entry historical parity denominator; the single Mercury failure must remain reported. Add independent ancient papyri if available without selecting by fit.
4. **Map real outcome domains cautiously:** historically distinct job, relationship, annual or daily methods must retain source-specific alternatives and explicit failures. Synthetic neutral chart calculations are permitted; original language ambiguities remain flags. No owner/private-biography retrospective model selection; no new human validation unless a frozen prospective, consenting cohort.
5. Continue parallel traditions on their respective latest authoritative lanes. Leave main/production scoring untouched and the current single cross-tradition research workflow intact.

**Owner-local source paths and file identity:** already in earlier authorized-workflow records; do not put private home path into public repo. Owner has a purchased Amazon Gansten *Primary Directions* ebook that is not in local corpus and is not being extracted through Work; it is not a blocker to these source-level activities.

**One-line handoff:** resume with Hephaistio original Greek apparatus and the Paulus nocturnal monomoiria ambiguity, using C04 report and verified file hashes; don't repeat the already documented C01–C04 source scans or 22 source tests unchanged.
