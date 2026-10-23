# Hellenistic astrology source research — C08 handoff

**Dated:** 23 October 2026. **Research objective:** OPEN. **Human chart predictive validations:** 0. **Source-arithmetic regression:** 49/49 PASS, last tested from the `humandesign` research branch.

## Immediate instruction to successor

**Continue the actual Hellenistic source research from C08; do not restart.** Bootstrap live `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md` + `LESSON-INDEX.md`, and `u-dont-existDOTcom/humandesign/AGENTS.md`. Respect the repository's test/blinding/spec rules. Read the C08 report and corrected witness before assuming the C07 values were literally printed.

The user has already obtained local astrology books; their Amazon-purchased Martin Gansten *Primary Directions* ebook is **not being extracted using Work**. Keep that boundary. Save all work to `humandesign`. No purchase, publication, merge into production, chart-specific fitting to known biographies, alteration of other astrology lanes, or retrospective human validation is authorized.

**Branch:** `research/astro-missing-book-audit-20261022`  
**Canonical research map:** `docs/astrology-research-map/README.md`

## Complete current work / exact new correction

1. **Direct critical Greek source:** David Pingree's *Hephaestionis Thebani apotelesmaticorum libri tres*, Vol. I (1973), SHA-256 `f2f803c457b7ba62df23f5c51d6f49ffff3644e17723c6673f5795298514ecae` (a temporary authorized study copy, not committed), main Hephaistio Book II.29 printed pp200–201 and II.36 pp225–226. This source has a 129-month period, main Saturn→Mercury **150** in II.29, a five-day annual supplement directly stated in II.29, and competing annual **360** principal / **365** finer allocation figures in II.36. Pingree's apparatus has an editorial suggestion of Mercury **52** where finer main Greek body reads **57**, plus an added 365-day note from manuscript P.
2. **Separate recensional Greek text:** Pingree's *Epitomae Quattuor*, Vol. II (1974), SHA-256 `6ee168a3a39d414620b7c820145c1ffe06dd437617bf79fdc6c9842f51c47f8a` (temporary bounded source review only), Epitome IV §37 printed pp240–242 (PDF pp270–272), and §44 pp264–265 (PDF pp294–295). Five-day annual supplement and a **365-day** principal allocation are **explicit source passages**. But this is a related late textual witness, not a second independent ancient author.
3. **Crucial C08 correction of C07:** Epitome IV §37 **literally prints Saturn→Mercury μ = 40, not 140**; its printed Saturn row is `[210,84,105,133,57,40,105]`, sum **734**, with corrupt numbers explicitly acknowledged in Pingree's apparatus. The chapter's own *approximation rule* (Saturn 30 months = 900 days, seven planetary months total 129, approximate multiplier 7) **derives** `[210,84,105,133,56,140,175]`, sum **903**, only +3 from 900 due rounding. This mathematical **140** agrees with a **later Valens appendical** reading of 140, whereas the main Hephaistio Greek *printed* row has 150. **Do not claim the Epitome prints 140 or that the formula determines what an ancient autograph said.**
4. **Additional Epitome IV §44 defects:** Primary annual Saturn/Jupiter/Mars/Sun/Venus/Mercury/Moon allocation is `[85,34,42,54,22,57,71]`, total **365**. Yet the examined child entries for Saturn total **86 vs parent 85**, Sun **55 vs54**, and Venus **23 vs parent22**. In the Venus finer heading the edited body reads **κγ = 23**, while Pingree's p265 apparatus says `legendum κβ` = **22**. Replacing the heading does not resolve all child totals. **No fully source-authentic exact 365-day subperiod chart algorithm is complete.** Seven parents' *all* child rows have NOT been independently audited to the same visual standard; do not claim they have.
5. The old C07 report/test had confused a reconstructed sevenfold row with the printed Epitome row, despite **45 green tests**. Its registry and test have now been corrected to distinguish `printed=40` from `derived=140`; the dedicated new C08 witness and four tests preserve the source error. Prior C07, C06, C02 reports were annotated/corrected. **49/49 source-only tests passed after branch update.**

## Surviving older Hellenistic results (do not repeat)

- Paulus Greek ch2/ch32 nocturnal trigon narrative can be reconstructed, but the reconstructed day canon differs from Greenbaum's printed corrected 120-cell table in **34/120** cells; without Boer/Greek manuscript diagrams this is a disputed modern implementation, not human prediction.
- Separate Egyptian/Greek calendar and timing approaches in Ptolemy, Hephaistio, Paulus, Valens and Firmicus remain versioned; avoid a merged opportunistic chronology.
- The 319 CE P.Berl. 9825 papyrus by-sign monomoiria historical calculation agrees **6/7** labels (Mercury mismatch); P.Oxy. LXI 4277 agrees **1/3** of three readable labels (two mismatches), based on scholarly texts, not verified original papyrus image. These rates measure **historical scribal-document reconstruction, not astrology's ability to predict people's lives**.
- Rhetorius Holden ch83 printed page140 remains absent from acquired scan; do not invent material.
- This corpus and Chinese/Jyotish/Tibetan/Maya readers are separate source lanes; a combined human test is deferred until source rules and concealed questionnaires are independently frozen.

## Exact files to read / continuation instructions

1. [C08 source comparison report](HELLENISTIC_SOURCE_C08_CORRUPT_EPITOME_AND_RECONSTRUCTION_20261023.md) — corrections, source page locations and methodological boundaries.
2. [C08 literal-versus-derived machine witness](HEPHAISTIO_C08_LITERAL_VS_DERIVED_SUBPERIOD_WITNESS_V1.json).
3. [Corrected Epitome IV C07 register](HEPHAISTIO_C07_EPITOME_IV_INDEPENDENT_RECENSION_V1.json) + [its corrected test](test_hellenistic_c07_epitome_iv.py).
4. [C08 exact-source test](test_hellenistic_c08_source_literal.py) and [C07 five-day source report](HELLENISTIC_SOURCE_C07_FIVEDAY_CALENDAR_MANUSCRIPTS_20261023.md).
5. Read the existing root research map and C01–C06 handoffs *only as needed*, respecting C08 corrections.

**Next executable research frontier:** compare the **remaining Epitome IV §37/§44 parent→recipient numeric rows** with source pages and Pingree apparatus, recording uncertain glyphs and each row's literal sum separately from the sevenfold reconstruction. After that, inspect Boer 1958/1962 Paulus/Heliodorus scholarly diagrams to adjudicate the 34/120 daytime-vs-narrative cell disagreements. Seek the original P.Oxy. 4277 image/first-edition reading when accessible without bypassing its access controls. Never choose a variant because a known person's biography fits.

**Exact narrow reproducible test:**
```shell
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```
**Last receipt: 49 tests passed from a fresh branch-pulled sparse checkout, exit code 0**. No release/merge gate or scientifically blinded human evaluation was run.

**Resume one-liner:** Work from C08's **literal 40 versus reconstructed 140** correction; finish visually auditing the rest of Epitome IV's 365-day child tables, then Paulus's 34 unresolved cells. Save all results in `humandesign`, no Amazon ebook extraction.
