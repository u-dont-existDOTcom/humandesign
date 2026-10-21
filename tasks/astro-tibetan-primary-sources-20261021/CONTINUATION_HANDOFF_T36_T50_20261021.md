# Tibetan astrology research — continuation after T50 (21 October 2026)

**Parent owner's exact request:** "ok then start reading everything you need that's free plus these, in turns, to merge into the other readings we are doing for astro system"; user continued multiple times with "continue". Root task **OPEN**: read Tibetan free and supplied books, integrate source-defined rules with Western Lilly/Ptolemy, Indian Jyotish, Chinese BaZi/Zi Wei; independently calculate traditional charts, freeze models and carry out preregistered, blinded human forward/reverse tests with chart decoys and non-astrology baselines. Never treat historical source annotation counts as human predictive validation.

## Baseline and current branch

- Accepted predecessor: branch `research/astro-tibetan-t23-obstacle-20261021`, GitHub SHA `10b0e2c68bfd7fd32ba2c9a1ad870e6d9ac173cc`, documentary notes TIB-R0001–0324 (**324**).
- New research branch `research/astro-tibetan-t36-query-illness-20261021`, isolated owner-laptop worktree `/mnt/hdd/storage/joel/development-worktrees/humandesign/astro-tibetan-t36-readback-20261021`. Verify actual remote SHA anew, as this file predates final commit.
- **447 cumulative source notes**, TIB-R0001–0447. **New 123**: T36 +20 (R0325–0344), T38 +27 (R0345–0371), T42 +16 (R0372–0387), T44 +29 (R0388–0416), T47 +18 (R0417–0434), T49 +13 (R0435–0447). T37,T39,T40,T41,T45,T48,T50 are derived comparison/lookup/variant records adding zero historical notes.
- Copyrighted source PDF remains external. Original source witness `TIB-DORJE-2001` SHA256 `485d25eece33ed6af1dd8e5080f7b03967594dbd6a908a1ebc7e090d44d62530`.

## Actual reading frontier and findings

Gyurme Dorje *Tibetan Elemental Divination Paintings* (2001), English *White Beryl* and *Moonbeams*: **main explanatory text studied through its conclusion PDF400/printed399**; after that are footnotes/bibliography not exhaustively checked. This turn covered PDF281–400, with full method-level coverage for query-hour, illness, death, thirty computational charts and thirteen Bal-mo charts. Direct Tibetan original manuscripts and rare `'Phrul-gyi mig-tshags` commentary have not been read. Main summary: `CROSS_LANE_INTEGRATION_T36_T50.md`.

Key source distinctions:
1. Consultation-hour ritual/posture/barley/house chart input is query-time, not birth-time. Household/land/tomb use vitality/destiny/luck and direction-sensitive elemental comparisons; housing geomancy table 5×5.
2. Illness counts 19 markers (16+3), 15 pine-tree starts +2 alternate school policies. Two source-count-direction conflicts **TIB-CONFLICT-008/009**. Eight date goddesses sum 30 lunar days.
3. Death chapter includes living relatives 20, deceased timeliness 58, *Moonbeams* compact funeral 187+12=199, separate public funeral 136+2784=2920; six-realm religious categories, 13 corpse types, 5 funeral methods, family-based outcomes. None provides reliable personal death guidance.
4. Original White Beryl Chapter26 lists 30 charts consecutively; *Moonbeams* uses interleaving 1–7 Chinese, 8–14 Tibetan, 15–22 Chinese, 23–30 Tibetan. Other White Beryl introduction lists of fifteen plus fifteen don't match simple chapter splits. Full 30 title/role table + separate Chinese/Tibetan starting pairs: T48. Eight markers each (30×8=240 positions) with birth-YEAR polarity traversal, not subject sex.
5. Simplified Bal-mo lding-skor 13 charts use five axes each (13×5=65), plus source references to an abridged 872 (=371+501) and elaborate 2920-pebble form. **Son-relation black** in Bal-mo vs **one white plus one black** in 30-chart system: method-dependent, don't unify. Catalog T50; chart10 start and chart13 counting direction unresolved.
6. Source description itself notes practical algorithm implementation needs living oral instruction; not license to invent missing methods.

Scientific state: **0 confirmed prospective human predictive tests, 0 Tibetan scoring runtime promotions**. Existing Western/Chinese/Jyotish accepted indices unchanged. Medical, spiritual, death and ritual claims are historical religious material, not modern clinical or safety guidance. Correlations with Chinese/BaZi/Indian Jyotish inheritances must be capped and evaluated as incremental information, not independent confirmations.

## Verification

Focused scripts in `tasks/astro-tibetan-primary-sources-20261021/`:
- `python3 verify_t36_t42_sources.py` verifies new R0325–0387 and chains T01–T35.
- `python3 verify_t44_t46_sources.py` verifies death remainder and chains earlier tests.
- `python3 verify_t47_t50_chart_catalogues.py` verifies R0417–0447 and the 30×8, 13×5, Moonbeams interleaved indexing, incomplete starting points and incompatible pebble colors; chains prior scripts.
- `python3 verify_global_source_registry.py` checks all documentary ID allocations TIB-R0001–0447 across 24 note-bearing batches, source identity and 324+123 count. Verified PASS on owner laptop.
The third passed on owner machine at remote draft HEAD `7919171989cd3af3c745e0569cce0f2a53be8f9f`; rerun on exact final remote head after this checkpoint is committed. Source-note counts, uninterrupted numbering, and unrelated-file-unchanged state should be rechecked.

## NEXT without rereading accepted T01–T50

**Source ID TIB-R0448.** Start with Philippe Cornu `Tibetan Astrology` (user-provided PDF; previously only pp102–119 and example pp216–223 excerpted), then finish Edward Henning `Kālacakra and the Tibetan Calendar` Chapters I–V and remaining VI, complete free Erlewine 865-page `Tibetan Astrology`, and Svante Janson's open mathematical text. Prioritize reproducible calendar/natal mechanics and direct, alternative Tibetan original witnesses to adjudicate source issues. Keep Phugpa/Tsurphu and Cornu (year polarity) vs Erlewine (subject sex) Papme policies distinct; never select a favorable policy from a known person. Preserve all future source notes with exact page/witness type, uncertainty and reproducible tests, and ship durable work via Git. Root remains OPEN and no routine owner permission is needed for further source reading.
