# C30 — First source-defined Hellenistic natal placement with a falsifiable *human* outcome: Dorotheus's Lot of Expedition

**25 October 2026. OWNER SCIENTIFIC GOAL OPEN:** preserve each historical tradition's authentic competing natal and temporal rules within the original 16-tradition `humandesign` framework, then freeze chart-derived person-level statements *before* concealed outcomes from untouched consenting human participants are seen. This is a **source-to-outcome bridge**, not an empirical success. **Real human predictive validations: 0. Production scoring: unchanged.**

## Why this passage, rather than another round of manuscript collection

C29 separated nine historically distinct `monomoiria` computational candidates, but its checked Paulus chapter 32–33 passage described sect-light and Ascendant-degree *computation*, not a directly measurable life outcome. For C30 I screened readily available person-specific passages in the **already acquired Hephaistio Book II**, focusing on a rule with (1) explicit source syntax, (2) a bounded astronomical calculation, (3) a narrow externally observable stated consequence, and (4) a possible contrary result.

**Best text-first candidate found:** a Greek verse attributed to Dorotheus of Sidon, quoted by Hephaistio of Thebes, *Apotelesmatics* **Book II, chapter 19**, at the transition to chapter 20. The passage names a **Lot of Expedition / military campaign** and explicitly projects the arc **Saturn → Moon from the Ascendant**. When it falls in **Aries, Scorpio, Capricorn or Aquarius**, the transmitted verse asserts that *a man* will be in campaigns. The extra clauses about battlefield renown and division of spoils have separate Mars-angularity and light requirements; they are **not** silently conflated with the initial lot-sign rule.

**Why not Hephaistio II.22 children for this first pilot:** the available Dorothean passage predicts either being without children **or mourning one's children** under a shared 6th/12th-house condition, while other passages add planet/lot dependencies. That compound/ambiguous outcome is much easier to rescue retrospectively. The clearer Lot of Expedition is still observationally difficult and historically contextual, but requires fewer unprinted modifiers.

## Original-text provenance and exact reading boundary

**Greek text checked directly:** public modern Greek rendition of Dorotheus fragments as transmitted in Hephaistio, `2d.1`, [Eulogikon document](https://eulogikon.org/works/dorotheus-sidon-hephaestion-fragments-oho-aa), [downloaded plain Markdown](https://eulogikon.org/works/dorotheus-sidon-hephaestion-fragments-oho-aa.md) (17,560 UTF-8 bytes, SHA-256 `4a24067e680e385ea527e7aa36d5b5dcf44cbee075f9dac62f2d731cf08564e6`). Brief actual Greek source anchors include `ἐκ Φαίνοντος ... μέχρι Σελήνης` (from Saturn to Moon), `ἐξ ὥρης` (from the Ascendant), `Σκορπίον ... Ἀρνειοῖο ... Αἰγοκέρωτα καὶ Ὑδροχόον` (Scorpio, Aries, Capricorn, Aquarius), and `στρατίῃσιν ἔνεσται κεῖνος ἀνήρ` (that man will be in campaigns). These are **distinct shortened excerpt anchors**, not one connected ancient sentence.

**Independent owned English comparison directly checked visually:** Robert Schmidt, *Hephaistio of Thebes: Apotelesmatics, Book II* (1998), **printed page 68 / owned study PDF page 40**. The actual two-page PDF leaf was rendered and inspected, not merely its OCR. SHA-256 of complete owner-side PDF **`e1f11be1a21924345770d2a31766caa0e15a53274403c360057a3c4bc5221073`**. Schmidt footnote 177 says this military/profession fragment is **not found in the surviving Arabic Dorotheus**. No source scans or copyrighted translation pages are redistributed or committed.

**Editorial limits:** The online Greek is a modern literary transcription, not Pingree's original critical printed apparatus and not a new paleographically verified codex. The original work of Dorotheus does not survive intact; this is a **quotation preserved by Hephaistio**, not direct Dorotheus autograph evidence. The passage does not specify a different nocturnal arc; the C30 **research candidate does not invent one**. Ancient zodiac longitudes must still be computed by an independently verified ephemeris with one declared tropical/sidereal convention and exact Ascendant geometry before any real-person predictions could exist.

## Tested calculation and the one-way, not exclusive, claim

The research-only module `hellenistic_c30_dorotheus_expedition_lot.py` accepts exact zodiac longitudes for **Ascendant, Saturn and Moon** and calculates:

```text
LOT_LONGITUDE = (ASC_LONGITUDE + (MOON_LONGITUDE - SATURN_LONGITUDE modulo 360)) modulo 360
INDICATOR = LOT_SIGN in {Aries, Scorpio, Capricorn, Aquarius}
```

Its core claim output is **`SOURCE_PREDICTS_MILITARY_CAMPAIGN`** when the indicator is true. In *all other signs*, the return value is **`NO_POSITIVE_CLAIM_FROM_THIS_CONDITION`**, *not* the fabricated opposite "never a military campaign." No other Hephaistio prognostications are included in the function.

**Important literal negative check:** in the same Eulogikon digital collection, separately numbered `2d,1.1`, a following Greek commentary example discusses a military campaign with the lot in **Taurus** and additional Jupiter/Mars testimony. That contextual example is **not present in the specifically inspected Schmidt page-68 excerpt**, and its manuscript/recensional status has not been independently verified. It reinforces why the transmitted four-sign verse must **not be turned into an exclusive rule**. It does *not* nullify the verse's one-way affirmative implication.

The module uses `Decimal`, rejects invalid/nonfinite/unwrapped longitude inputs, handles exact 30° sign boundaries and Saturn–Moon zodiac crossing without a negative-modulo error, and refuses to certify continuous birth-time stability from mere finite sampling. Its documentation and machine-readable [C30 source evidence](HELLENISTIC_C30_DOROTHEUS_EXPEDITION_SOURCE_V1.json) preserve each distinction.

## An honest prospective test design: feasible claim, NOT a trial in progress

[C30 draft prospective study plan](HELLENISTIC_C30_EXPEDITION_BLIND_TEST_DESIGN_DRAFT_V1.json) separates the ancient categorical assertion from a modern statistical association hypothesis. A participant would need a documented birth date/time/place; a **verified** chart engine, geometric Ascendant, longitudes and birth-time uncertainty proof; and an adjudicated independent outcome about **being deployed on a military campaign in an armed conflict**, not just conscription, peacetime barracks, fighting sports, travel or political activism. The ancient phrase does not map perfectly onto modern service/deployment; this **construct-translation uncertainty** must appear in any later claim.

The initial source-faithful scope is **adult men**, because the original language says `ἀνήρ`, and any generalization beyond that would require a separately frozen study arm. A modern study should control for birth cohort, social geography, conscription status and *actual opportunity* to have experienced warfare. The birth-data/ephemeris version, sign-selection and outcomes must be frozen first; evaluators stay blind to placement, and negatives/unknowns remain visible. Charts and outcome records must not be selected retrospectively from people whose biographies we know.

**Two distinct scientific summaries would be mandatory**: (a) literal-prediction audit of every exposed person without a known campaign by the observation cutoff (with age-censoring qualifications) and (b) a one-directional, preregistered enrichment test against matched birth-year/geography/opportunity baselines, including permutation tests where exchangeability is justified. No "nonindicator means never served" arm. Recruiting exclusively soldiers/combatants would invalidate the design. The current file is explicitly an **UNREGISTERED DEVELOPMENT DRAFT**: sample size/power, observation cutoff and exact null implementation must be finalized before any real enrollment or prediction.

## Scope boundaries, validation and owner outcome

C30 is the first one in this particular Hellenistic continuation with a **literal person-specific consequence** and an executable chart feature. That does **not** mean the feature is scientifically supported, historically error-free, predictive, or ready for deployment. No consenting person, actual natal chart, question response, military service record, synthetic success fraction or privately known life was used to select/tune a winning rule. The entire C29 source matrix and earlier contradictions remain untouched; the independent active `participant-session-v1` task lock and production scoring remain unchanged.

The historical source math can now move into the project's source-to-test evaluation workflow **when the actual chart backend, eligibility definitions, prospective participant consent and pre-answer freeze gates are met**. The remaining Hellenistic manuscript/access questions do not have to be resolved first. A valid negative result is as important as any positive.

**Research-only deliverables:** `hellenistic_c30_dorotheus_expedition_lot.py`; `HELLENISTIC_C30_DOROTHEUS_EXPEDITION_SOURCE_V1.json`; `HELLENISTIC_C30_EXPEDITION_BLIND_TEST_DESIGN_DRAFT_V1.json`; `test_hellenistic_c30_expedition_source.py`; `HELLENISTIC_CONTINUATION_C30_20261025.md`. No copyrighted book or photograph files committed.


## Verification results (25 October 2026)

- Focused C30: `python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_c30_*.py' -v` — **13/13 PASS**.
- Full Hellenistic historical-source suite: `python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py'` — **291/291 PASS** (278 inherited, 13 C30).
- Python source is research-only and has no link to the production scorer. The unit tests verify arithmetic, provenance constraints, candidate/unknown status and protocol metadata; they **cannot** establish historical manuscript authenticity, future human predictions or societal causation.
- The user's original broader 16-tradition experimental objective remains **OPEN**. The prepared study design is *not* preregistered and has **0** real-human outcome validations.
