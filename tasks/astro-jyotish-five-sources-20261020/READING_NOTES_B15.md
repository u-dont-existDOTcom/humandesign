# JYOT B15 — combinatorial completeness audit: *Sārāvalī* conjunction chapters (2026-10-21)

**Reader task:** independent five-book Jyotish source study, source-only. Full input remains user-uploaded English `Sārāvalī` PDF SHA-256 in SOURCE_MANIFEST. **Data:** `SARAVALI_CONJUNCTION_SOURCE_CROSSWALK_B15.json` contains machine-recomputable planet groups and exact source repairs.

## What was actually checked

The 150-page modern English `Sārāvalī` has numbered conjunction chapters for the seven classical planets (Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn). One set is an **unordered subset**: the same planets in different word order are the same astronomical condition. Mathematically, full enumerations of seven planets contain:

| Chapter | Number of planets | Expected unique sets | What the uploaded English says |
|---|---:|---:|---|
| 15, PDF31–33 | 2 | 21 | 21 unique, all complete |
| 16, PDF33–35 | 3 | 35 | 35 unique, all complete |
| 17, PDF35–38 | 4 | 35 | 35 rows, two `(?)` unidentified planets, one duplicated named set, three fully specified sets absent |
| 18, PDF38–39 | 5 | 21 | 22 rows, 20 distinct sets, two duplicate pairs, one mathematically absent set |
| 19, PDF39–40 | 6 | 7 | Seven unique, all complete |

This is not an estimate: each title was parsed, planet names canonically sorted, and the resulting sets compared with `choose(7,k)` mathematical universes. **Physical screenshots of PDF36 and PDF38** confirm the literal question marks and duplicate headings; this is not OCR hallucination.

## Sanskrit comparison resolves four errors in the uploaded English edition

The [Central Sanskrit University Lucknow *Sārāvalī* Chapter17](https://www.csu-lucknow.edu.in/e-books/saravali/p18.html) and [Chapter18](https://www.csu-lucknow.edu.in/e-books/saravali/p19.html) provide Sanskrit text for the same numbered verses:

| Verse | English text problem | Sanskrit-backed reading |
|---|---|---|
| Ch17.8 | Venus–Jupiter–Moon–(?) | Venus–**Sun**–Jupiter–Moon (`शुक्रार्कगुरुशशाङ्कै`) |
| Ch17.17 | Sun–Mercury–Venus–(?) | Sun–Mercury–**Jupiter**–Venus (`भानुबुधजीवशुक्रै`) |
| Ch17.24 | Moon–Mars–Jupiter–**Saturn**, falsely duplicating Ch17.25 | Moon–Mars–Jupiter–**Venus** (`शशिकुजगुरुभार्गवै`); Ch17.25 truly includes Saturn |
| Ch18.7 | Mercury–Moon–Jupiter–Sun–**Saturn**, duplicating Ch18.8 | Mercury–Moon–Jupiter–Sun–**Venus** (`बुधेन्दुरविजीवशुक्रै`); Ch18.8 does include Saturn |

With these changes **Chapter17 covers all 35 distinct four-planet sets exactly once**, and Chapter18 has **all 21 five-planet sets covered** among its 22 verses.

**One apparent duplicate survives independently of the modern English errors:** Chapter18 **verse13** and **verse20** both use **Moon–Mars–Mercury–Venus–Saturn** (`कुजशशिबुधशुक्रमन्दैः` vs `बुधेन्दुकुजशुक्ररविपुत्रैः`), and their descriptions differ. They are separate traditional source clauses, not two independent discriminators or evidence of human predictive success. A model cannot count both as confirmation for a subject, nor choose the verse whose outcomes match a known biography better.

## Other unresolved semantics

These chapters say planets are `together` or in one `Bhava`. Without a frozen definition—**same 30-degree sign, Regiomontanus/whole-sign house, or degree-based conjunction**—the reference class is not fully specified. Mathematical completeness of planet-name permutations does not imply that every conjunction can occur physically with equal prevalence. Mercury/Venus cannot arbitrarily separate far from the Sun in geocentric charts.

Each clause mixes many unrelated effects, sometimes internally qualified by strength/varga, and historically gendered/moralized claims. Source overlaps with broader chapter19.8 about general five/six conjunction hardships, and chapter20's previously audited spiritual/asceticism sets. Keep **conjunction catalog versus specific outcome and precedence** separate.

The external Sanskrit digital chapter may derive from one scanned edition and does not establish original manuscript independence. The four repairs have **high local textual support** but are not a complete critical edition of the whole book. Raw modern copyrighted editions remain outside the public GitHub branch.

**B15 status:** new correction audit only; **0 new independently observed human forecasts, 0 production-model promotions**. The source-only count remains **181** until new discrete candidates are registered. Next: broaden into unindexed non-conjunction domains and document retrograde/planetary strength variants with exact printed verse provenance.
