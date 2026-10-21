# Tibetan astrology continuing mission: exact restart after T61 — 21 October 2026

**Owner's exact authorization:** “ok then start reading everything you need that's free plus these, in turns, to merge into the other readings we are doing for astro system”. All later “continue” messages carry that goal. **Root scientific mission OPEN**: source-grounded Tibetan study including three user-uploaded books and free scholarly texts; integrate with established Lilly/Ptolemy, Jyotish, BaZi/Zi Wei source lanes; independently calculate complete natal/annual planetary/chart models and conduct preregistered blinded forward and reverse human tests against decoy charts and conventional controls. Annotation totals and synthetic/calendar tests are NOT the goal and cannot close it.

## Durable accepted predecessor, branch and location

- Predecessor accepted Tibetan branch `research/astro-tibetan-t54-janson-true-dates-20261021` exact SHA `ae5108c154b223a5aa79022bc227c0ddba6fb286`, **500** Tibetan historical-source annotations IDs TIB-R0001–0500. Exact no-human-prediction state and two independently developed calendar-date software comparisons previously verified.
- Current branch `research/astro-tibetan-t57-almanac-janson-20261021`; initial GitHub source-annotation commit `b34428ba8cc280caaf25eb54fbae6b95d8f1fe58`. **Final accepted commit will be newer**: obtain it via remote fetch, not this stale prose.
- **CRITICAL local checkout/disk recovery:** `/mnt/hdd` physical archival disk was effectively full (921MB available), so full worktree checkout failed and was superseded. A clean **cone-mode sparse checkout** containing ONLY `tasks/astro-tibetan-primary-sources-20261021` was initialized at `/tmp/hd-tibetan-t57-20261021` (root disk had 58GB free). Commands already executed: `git worktree add --no-checkout --detach ...`, `git sparse-checkout set --cone tasks/astro-tibetan-primary-sources-20261021`, `git reset --hard HEAD` (scoped to freshly created sparse checkout only). DO NOT use full checkout on archive HDD. DO NOT confuse sparse missing other files with deletions; the GitHub compare confirms only Tibetan task files change.
- Copyrighted PDF bytes remain outside repo. Owner's Edward Henning (2007), *Kālacakra and the Tibetan Calendar*, attached PDF was directly inspected (PDF pp221–228,376–382); PDF content originally mounted/materialized in container at `/mnt/data/tibetan_source_review/` with SHA256 `3fa6c44d4c25c4c69937e9575c0653265e1e77bb1b6923a19ef69ec10f539fd5`. If not mounted in later turns, search Files for the user's supplied exact title. Do not substitute unrelated scans without witness comparison. Janson 2014 HTML: `https://arxiv.org/html/1401.6285v1`.
- Newly added **42** unique source records: `batches/T57/JANSON_ALMANAC_22_SOURCE_NOTES_V1.json` IDs TIB-R0501–0522, `batches/T59/HENNING_ALMANAC_20_SOURCE_NOTES_V1.json` IDs TIB-R0523–0542; cumulative documentary registry **542**. Supplemental T58/T60/T61 are mathematical source implementation, name tables and a legible printed-caption fixture, **zero new historical-source counts**.

## Source-grounded code and tests accepted for this turn

1. `batches/T58/tibetan_almanac.py`, **new code**, Janson §10 almanac: exact Fraction Moon tithi end/start, Sun tithi end, weekday, 27 mansion index, 27 angular yoga index, 60 karaṇa half-position IDs. Explicit calendar policies `system` (Phugpa/Tsurphu), epoch (source epochs), anomaly policy; explicit dawn half-tithi policy `undetermined` or `henning_equal_duration` (source ambiguity, no default). Handles skipped/duplicated lunar days without inventing birth times or the physical sky. `verify_t57_t58_almanac.py` passed over **3,066** calendar entries with exact source identities, color/label caveats and prior T54 suites chained.
2. `batches/T60/henning_almanac_names.py`, **new code**, source-name lookups from Henning Chapter IV printed pp203–204 + Appendix I printed pp356–362. Names:
   - 10 *elemental yogas* = unordered weekday-element × lunar-mansion-element 4-element multiset (Siddhi, Amṛta, Yauvana, Pragati, Sampanna, Balayukta, Alābha, Pratikūla, Dahana, Maraṇa); Henning's Saturday/Earth + Rohiṇī/Earth → Siddhi example independently checked.
   - 27 **angular** yoga names with Phugpa Viṣkambha index0 vs Tsurphu Vaidhṛti index0 source-name shift; **not** the same system as elemental yoga.
   - Additional 28 **weekday–mansion** combinations are known as a different source family but **full lookup remains UNKNOWN**; no invented assignments.
   - 27 mansion index names/elements with **Tibetan Śravaṇa** versus **Indian Abhijit** at index21; separate Chinese 28-station zero-point starts Citrā; source vocabulary not normalized across traditions.
   - 11 named karaṇas: fixed Kintughna, Śakuni, Catuṣpada, Nāga; changing Vava, Valava, Kaulava, Taitila, Gara, Vaṇija, Viṣṭi. Half-day positions H1,58,59,60 fixed. Naming from source appendix is not evidence of precise half-tithi time split.
   - `verify_t59_t60_henning.py` passed all 27/10/60 lookups and Janson-almanac integration, chains prior suites. Actual model predictions about humans = ZERO.
3. `batches/T61/HENNING_CAPTION_2003_JUNE8_SOURCE_FIXTURE_V1.json` and `verify_t61_henning_caption.py`: directly inspected original Henning printed p203 / PDF p223 **English caption**: **Gregorian 8 June 2003 = Water Sheep, month4 lunar-day8**. Independent T54 Gregorian conversion matches JDN2452799. Output Janson almanac for that date (Sunday, Moon mansion index10, angular yoga index13) is retained as **code-computed only**, **NOT independent reading of tiny Tibetan numeric columns** (which were not reliably deciphered). Test PASS and chains T59–T60.
4. `CROSS_LANE_INTEGRATION_T57_T61.md`: full source/algorithm/reconciliation/independence report. This file: recovery instructions.

## Important research boundaries

- Source math **does not prove astrology works**. No participant data touched, zero real human prediction scores; no clinical, mortality, spiritual efficacy or relationship-safety claim; no production-model promotion.
- Janson source explicitly adds Sun-at-tithi-end to approximate Moon-at-civil-day-start for angular yoga: **different temporal instants**, not a physical planetary conjunction. Half-tithi karaṇa at dawn remains ambiguous; equality halves is **an explicit optional research policy** only.
- Tibetan lunar mansion 27 numeric vs Chinese mansion 28 and Indian zero-point tradition; elemental yoga 10 vs angular yoga 27 vs weekday–mansion yoga 28, never unified by name alone. Chinese/Indian inherited mechanics cannot be counted as independent corroboration of Western/Jyotish/BaZi.
- Earlier nine Cornu/White Beryl internal-source issues, Henning numerics and Papme year-polarity vs subject-sex remain open, not silently corrected. This turn added no retrospective human fitting.

## Next authorized executable frontier; do not repeat T01–T61

**Next source annotation ID TIB-R0543.** Continue Henning Chapter V's Sanskrit `Kālacakra Tantra` and `Vimalaprabhā` mathematical source translation and Janson Appendix D's planets and Rahu, then finish Henning chapters, Cornu unread sections, full free Erlewine and original Tibetan/alternate witness manuscripts. For planetary calculations distinguish Kālacakra karaṇa astronomical scheme from karaṇa half-tithi ritual names, and modern physical ephemerides. Source mechanical parity, interpretation mapping, then frozen untouched blinded people comparisons remain owner goals. No human gate/purchase/third-party participant outreach needed for continued source reading.

## Verify and delivery

From `/tmp/hd-tibetan-t57-20261021/tasks/astro-tibetan-primary-sources-20261021/`:
`python3 verify_t61_henning_caption.py` (chains `verify_t59_t60_henning.py` then `verify_t57_t58_almanac.py` then previous T01–T56 suites). It must PASS at the **exact committed remote Git SHA**. Also verify changed path list contains **only** Tibetan task tree. Report/handoff and code should be copied to owner's `~/Téléchargements/` if disk permits; omit copyrighted PDFs and original Tibetan figure images.

**ROOT STATUS OPEN; no human validation claims.**
