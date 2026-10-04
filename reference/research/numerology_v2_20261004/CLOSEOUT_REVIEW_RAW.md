# Independent claim check: four-book source audit closeout and empirical design

## Verdict: **FINDS_ERROR** (bounded)

Most of the source-side package holds together. Every supplied primary excerpt agrees with its specification. I recomputed about 50 worked examples (well over 100 values) using only each specification's own rules, and all of them reproduce, with one exception. Ambiguity entry J-A07 records a Jordan prose-versus-formula conflict, but the package's own formula and inputs refute it. This is the same kind of audit misreading the reconciliation already withdrew for JB-A21, and it is still recorded as a source defect.

The larger problems are in the empirical design, which claim C11 says delivers equal false-positive and miss costs and full relevant arms. As written, the design has four problems:
- It reports a utility whose implied costs are 2:1, not equal.
- It admits event cells and negative cells under different ascertainment rules, and abstention avoids the miss cost.
- Its grid-intersection exposure rule structurally favors either calendar-anchored or birthday-anchored arms.
- It describes the main Campbell arm as both full-relevant and a labelled subset.

Each can be fixed by a short text change before any operational freeze. None requires building the reading engine. Completing the source audit needs only the D1 annotation.

## Review boundary

- **Primary text in this pass:** only the excerpts in the request:
  - Jordan pp.64, 110, 251.
  - Campbell pp.16, 27, 246. These are OCR text; the p.16 line itself renders 11 as "II".
  - Javane–Bunker pp.39–41 (summarized), 53, 54, 55.
  - There is no Cheiro primary text at all.
- **Not supplied:** CHEIRO_CHALDEAN_V1, DECOZ_CURRENT_V1, freeze_manifest.json, code and fixtures, independent_review.md, page images. Hashes, commit IDs and blob IDs are asserted but not checkable.
- **What I checked:**
  - Excerpts against the specifications.
  - Recomputation of worked examples from each specification's stated rules.
  - Consistency across the four specifications, SOURCE_RECONCILIATION.md (treated as controlling; JB-A21 not re-argued), both JSON files, the completion report and the design.
  - How the scoring rules behave as decision rules.
- **What this cannot certify:** page accuracy, accuracy of the quoted printed values, inventory completeness, edition facts, or anything about Cheiro V1 or Decoz V1. When a specification reproduces its own quoted example, that shows coherence, not fidelity to the page.

**Labels used below**
- **PASS:** the load-bearing content is verified by an excerpt, by a document fact inside the package, or by arithmetic, and nothing contradicts it.
- **UNVERIFIABLE:** at least one load-bearing part rests only on specification text or unsupplied artifacts, and no contradiction was found.
- **FAIL:** contradicted.

**Recomputed with matching results**

| Source | Examples recomputed |
|---|---|
| Cheiro | All six reproducibility pairs; the period table tiles the year |
| Campbell | Bronn Soul/Quiescent/Expression; Washington LP 28/1, Pinnacles [6,8,5,6] ending 35/44/53, Challenges [2,0,2], Inclusion [2,1,0,0,5,2,3,1,2], Ruling Passion tie {5,7}; Hoover 11; KIRK 40/4 vs 22; Henry Ford Inclusion, adjusted Ruling Passion {6,9}, Planes 2/2/3/2 and 4/4/1 from the reconstructed grid (all 26 letters appear exactly once); Ann/James Eccentric Angles; UY/UM/UD/PY/PM/PD examples; the 1910→2009 gap; Challenge counterexample [8,7,1]; all ten Eva Amy Downs tape rows; Eva Expression and Soul 7 |
| Jordan | Freda Mary Norton; John Henry Jones; Dec 18 1950; Henry Ford Heart 11/2; Doyle Destiny/Heart/Personality/Birth Force/Reality/letter count/Planes; Marconi and Pershing Planes; five Challenge patterns; Aug 6 1934; Mar 7 1912 (PY 18/9, Pinnacle change in 1962); PM examples; Feb 7 and Feb 9 1958 grids; Feb 10 1963; Race Consciousness sequences; Robert 33; Elizabeth/Ann/Anderson at age 43; Keeler; world-cycle rows |
| Javane–Bunker | Ada and Cayce core numbers; Ada PY 45/9→46/1, six period values, PM 50/5, Power 78/15/6, missing {6,8,9}→{8,9}; Ada squares and centre (matching the p.55 excerpt); Mary Geraldine Charles and Cayce squares; Cayce ages 48/51; all nine minor-entry pairs; values after age 81 |

## C01–C12

**C01: UNVERIFIABLE.**
- There is no Cheiro excerpt.
- Internally the specification is clean:
  - The twelve inclusive intervals tile the year, with Feb 29 inside Pisces.
  - Elements and central opposites are correct, and Jan 29 maps to Aquarius (chapter II).
  - All six example pairs recompute.
  - Central opposites are always Fire–Air or Water–Earth, so CENTRAL_OPPOSITE and FIRE_WATER_CONFLICT can never collide.
- "Not a new year recurrence" is a claim of absence and needs a whole-book reading.

**C02: PASS.**
- The p.27 excerpt directly supports a private, at-rest construct: "your own secret … you when you are alone, concerned only with your own dreams, relieved from responding to outside influences".
- "Secret" excludes a public-presentation reading.
- The label "Quiescent Self" and Impression's separate status (pp.38–42) come from the specification only.

**C03: UNVERIFIABLE.**
- p.16 verifies the literal half: K=11 and V=22, "left unreduced".
- The compact-example half and the p.232 two-year/four-year duration half come from the specification only. The request itself says p.232 is "detailed in the supplied specification".
- Internal support:
  - The Eva tape rows quoted as printed reproduce only if V lasts 4 years.
  - KIRK gives 40/4 under literal values and 22 under compact values.
- The excerpt's "II" shows that Campbell's numerals carry real OCR risk.

**C04: UNVERIFIABLE.**
- p.246 verifies the ten position–planet pairings and that Pluto is unresolved.
- The rule of the 1 Personal Year nearest age 28/56 comes from the specification only.
- "Differs from Decoz" depends on DECOZ_CURRENT_V1, which is not in the package.

**C05: PASS (operational content).**
- p.64 verifies that 11 and 22 are reduced (stated "for all names").
- p.110 verifies an AEIOU-only Heart that excludes W and Y.
- Recomputed:
  - Henry Ford Heart: E5+O6 = 11/2.
  - Doyle Heart: 4.
  - Doyle Personality reaches 19→10→1 only if both Y and W count as consonants. This supports J07 internally.
- Boundary: two parts rest on specification pages beyond the excerpt (pp.64–66, 272–281):
  - extending the reduction to date-derived totals;
  - "retains qualitative importance".

**C06: PASS.**
- p.251 verifies three eight-hour periods with boundaries at midnight, 08:00 and 16:00.
- The accuracy disclaimer is a correct evidence boundary.
- The excerpt does not show which Pinnacle or Challenge fills which period.
- The excerpt also does not confirm J19's "P4 = whole-month vibration". "The other three Pinnacles" implies one Pinnacle is excluded but does not state its scope. P4 = r(month+year) does not depend on the day, so the specification's reading is at least coherent.

**C07: PASS.**
- pp.53–55 verify:
  - nine-year lines;
  - successive placement of W23, Y25 and N14;
  - "the last name is never used";
  - unreduced addition.
- Ada's squares (17/8, 74/11, 33) and centre (37/1) recompute exactly from ADAWYNN with birth sides 11, 12 and 14.
- That core names use reduced 1–9 values comes from the specification only. However, p.55's "in this process" marks the contrast, and Ada's core numbers (12/3, 29/11, 41/5) recompute.

**C08: UNVERIFIABLE.**
- The timing half is verified by pp.39–41.
- The masters 11/22/33/44 and the two 1–78 banks come from the specification only. p.55's unreduced "33" is weak corroboration.

**C09: PASS.**
- The reconciliation and ambiguities.json do withdraw JB-A21.
- Recomputation confirms:
  - Doyle's consonant roots are 6, 8, 5, giving 19→10→1.
  - At completed age 43 the active letters are E, N, D: Elizabeth (43) restarts at E; Ann gives 43 mod 11 = 10, the second N; Anderson gives 43 mod 36 = 7, which is D.
- The wheel image itself is outside my boundary.

**C10: UNVERIFIABLE.**
- The disclaimers are accurate and match the not_claimed list in source_coverage.json.
- The positive core, that every major layer was inventoried, cannot be confirmed from bounded excerpts.
- The "explicit ambiguities" deliverable it relies on contains at least one entry the package itself refutes (D1).

**C11: FAIL.**
- The architecture is sound: separate arms, frozen branches, UNKNOWN treated as not-negative, abstention treated as not-negative, exposure charging, person clusters, controls, multiplicity correction.
- But as specified, the design does not deliver equal FP/miss costs or a non-contradictory full-arm scope. See D2–D5.

**C12: PASS.**
- This is a document fact. The admission contract marks official_decoz_resources and campbell_hybrid_scope OPEN, launch_ready = false and study_launched = false. This matches design §3 and §10 and the report.
- The Campbell prerequisite's wording is part of the D5 contradiction, but the status claim is accurate.

## Defects (fix before relying on the closeout)

### D1: J-A07 records an audit misreading as a Jordan source conflict

**What the register says:** "Doyle final Pinnacle prose 9 versus formula 11/2."

**Counterexample from the package's own rules.** Apply J16 to the specification's own Doyle inputs: March 6, 1932, so m=3, d=6, y=r(1+9+3+2)=6. These are the same inputs that reproduce the specification's Birth Force 15/6 and Reality 11/2.

| Position | Calculation | Result |
|---|---|---|
| P1 | r(3+6) | 9 |
| P2 | r(6+6) | 12/3 |
| P3 | r(9+3) | 12/3 |
| P4 | r(3+6) | 9 |
| Challenges | — | [3, 0, 3, 3] |

- The final Pinnacle is 9, which agrees with the p.263 prose.
- No Pinnacle route gives 11/2. Using the unreduced year (15), P4 is 18/9.
- 11/2 is Doyle's **Reality**. J04–J08 itself warns that Reality sits next to "Pinnacle 9 or Challenge 3" on p.262.
- So the entry is false under the package's own formula, whatever the page shows.

**Impact:**
- No computed value changes, because the formula controls the fixtures.
- But the register counts an auditor error against the author, which the reconciliation explicitly forbids.
- Any fixture written from J-A07's text would encode 11/2.

**Minimal repair.** Issue a versioned reconciliation addendum before any operational freeze:
- Mark J-A07 WITHDRAWN_AUDIT_ERROR, unless a visual recheck of p.262 finds 11/2 printed inside a Pinnacle cell. In that case, relabel it "printed cell versus formula and prose (both 9)".
- Add a fixture: Doyle P = [9,3,3,9], C = [3,0,3,3].
- Re-derive every other RETAINED_SOURCE_ISSUE that names a worked example in the same way.

### D2: The reported utility contradicts equal costs

**The problem.** §7 and the admission contract (TP reward 1, FP cost 1, FN cost 1) define utility = TP − FP − FN.
- TP + FN equals the fixed number of observed events E, so utility = 2·TP − FP − E.
- Turning a miss into a hit is worth 2; removing a false alarm is worth 1.
- For a cell with event probability p:
  - Under the utility, a positive forecast is optimal when p > 1/3.
  - Under the primary metric (FP+FN)/N, a positive forecast is optimal only when p > 1/2.

**Counterexample at p = 0.4:**

| Metric | Forecast positive | Forecast negative | Preferred |
|---|---|---|---|
| Ut

| Metric | Forecast positive | Forecast negative | Preferred |
|---|---|---|---|
| Utility TP − FP − FN | −0.2 | −0.4 | positive |
| Error (FP + FN)/N | 0.6 | 0.4 | negative |

**Why it matters.**
- The two metrics prescribe opposite decisions in the same cell.
- In the utility, the FP and FN entries are equal (−1 each), but the regrets are not: a false alarm costs 1 and a miss costs 2. The equal-cost requirement is normally read as equal regret.
- The admission contract lists `true_positive_reward: 1` inside the equal-cost constraint block.
- The design never says which objective the thresholds frozen on development data must optimize. An arm tuned on the utility will over-forecast and can rank differently from the same arm tuned on the primary metric.

**Minimal repair.**
- Report −(FP + FN) as the utility. TP + TN − FP − FN is also acceptable, because it is a linear transform of the primary error.
- If TP − FP − FN is kept, label it a 2:1 miss-weighted sensitivity analysis and exclude it from thresholding and confirmatory ranking.
- State that every threshold targets the primary equal-cost metric.
- Move `true_positive_reward` out of the equal-cost constraint block.

### D3: Cell-eligibility rules let forecasts escape cost

**(a) Unequal ascertainment.**
- TP and FN need only a "qualifying observed event". FP and TN need confirmed absence.
- Nothing requires an event's window to have passed the completeness test.
- In retrospective life histories, events are recalled far more readily than absence is confirmed, so positive forecasts become cheaper than negative ones.
- **Counterexample:** a window of 12 monthly cells has 2 recalled events and no completeness rating.
  - An always-positive arm scores 2 TP and 0 FP, because the other ten cells are UNKNOWN.
  - An always-negative arm scores 2 FN.
  - Under complete observation, the always-positive arm would carry 10 FP.
- Equal unit costs therefore become unequal effective costs, which favors arms that forecast often.
- §9's "observed windows" may have been meant to prevent this, but the text does not say so.

**(b) Abstention and silence.**
- FN is defined only for a *negative forecast*.
- The denominator `N_observed_cells` is not defined with respect to abstentions.
- As written, an arm that abstains everywhere has zero errors (0/N, or an undefined 0/0) and ties a perfect forecaster.
- A positive-only reading never incurs FN unless its silence is declared a negative forecast.
- The common-coverage rule mitigates this only if the coverage level *and the cell set* are identical across arms. The text requires neither.

**(c) UNKNOWN cells.** A positive forecast placed in an UNKNOWN cell costs nothing. Arms whose forecasts concentrate in poorly documented periods (early childhood, remote years) are charged less.

**Minimal repair.**
1. Define the primary analysis set as the domain × period windows that blinded coders rate observation-complete. The rating rule must not depend on whether an event was found. Events outside those windows go only to a sensitivity analysis.
2. In the complete-coverage primary metric, an abstention on an eligible event cell counts as a miss; it still earns no TN credit.
3. The frozen translation step declares whether silence within a domain the arm addresses is a negative forecast.
4. Selective metrics use the identical cell set at matched coverage.
5. NONSCORABLE is assigned by the frozen arm-agnostic translation rule, not at the arm reader's discretion.

### D4: Grid intersection systematically penalizes misaligned arms

**The problem.**
- The rule "covers every common-unit cell it intersects", combined with a person-year grid, charges a twelve-month forecast that straddles a boundary for two cells.
- Birthday-anchored layers:
  - Javane–Bunker Personal Years and Triangle ages;
  - Jordan's Race Consciousness;
  - the Campbell and Jordan letter tapes.
- January-anchored layers: the Campbell and Jordan Personal Years.

**Counterexample from the package.**
- Ada's PY 45/9 runs from Nov 12, 1975 to Nov 12, 1976, so it intersects calendar cells 1975 and 1976.
- A Campbell or Jordan calendar PY occupies one cell.
- On an age-year grid, the penalty reverses.
- With rare events and equal costs, doubled exposure is net-negative. The grid's anchoring, not forecasting skill, can therefore order the arms. This is the kind of artifact §9 tries to exclude.

**Minimal repair.** Choose one of the following before outcomes and blind to the arms; native intervals remain secondary outputs.
- (i) Charge FP by the observed-negative person-time a forecast covers, fractionally. Score TP when the event onset falls within the interval, with conservative bounds for imprecise dates.
- (ii) Require the primary conclusion to hold on both a calendar-anchored and a birthday-anchored grid.
- (iii) Assign each forecast to the single cell it overlaps most, with a declared tie rule.

### D5: The Campbell principal arm's scope contradicts itself and is asymmetric with Javane–Bunker

**The contradiction.**
- §3 lets the main numerology comparison run with the p.246 hybrid labelled inactive.
- The admission contract calls that arm a "numerology-only subset" that "must be labeled as such".
- The same contract sets `full_relevant_system_per_arm: true`.
- §1 says an incomplete arm blocks "the advertised full-system comparison".
- One arm cannot be both full-relevant and an admitted subset.

**Why it is gameable.** Leaving the disposition OPEN preserves a post-outcome excuse: "the hybrid would have rescued it."

**The asymmetry.**
- JB17 records an analogous suggestion: personal numbers "may be compared qualitatively with an independently constructed horoscope", with no weights or orbs.
- Yet the Javane–Bunker arm is neither blocked nor labelled.

**Minimal repair.** State the rule now and apply it symmetrically:
- The research question is numerology-layer prediction.
- Author-suggested qualitative horoscope overlays (Campbell p.246, JB17) are outside the question's scope for every arm.
- Claims are titled accordingly, for example "Campbell numerology layers (p.246 overlay out of scope)".
- Any hybrid is a later, separately frozen arm whose results cannot amend these.
- The opposite choice is equally consistent: treat both overlays as relevant and block both arms.
- If a hybrid study might ever run, collect birth time and place at intake with a quality grade. The Ascendant and houses require them, and §4 currently treats them as non-inputs.

## Omitted load-bearing claims

**O1. Register provenance.** No claim states that every RETAINED_SOURCE_ISSUE tied to a worked example was re-derived from the frozen formulas and classified as either a source defect or an auditor reading. D1 shows such a claim is needed, and the closeout implicitly relies on it.

**O2. Decoz dependency.**
- C04, C12 and specification statements such as "not Decoz's 36-minus-Life-Path, then 27 years" rest on DECOZ_CURRENT_V1.
- That file is outside the reviewed package.
- The ledger should label those comparison halves as resting on an unreviewed artifact.

**O3. Freeze binding.** Two things need to be claimed, and neither is verifiable here:
- the hashed specification blobs are exactly the reviewed texts plus the reconciliation overlay, with its precedence rule;
- later corrections, including D1, enter only as versioned overlays before any operational freeze.
"Immutable" depends on both.

**O4. Cheiro V1/V2 period layer.**
- V2's inheritance section says V1 already has "separate zodiac-period … layers".
- Whether V1's period boundaries and meanings equal C2-01's is never stated.
- That determines whether the V2 arm carries two conflicting period definitions, and what exactly the ablation removes.
- The ablation also withholds C2-10's period character catalogue. So it bears on personality endpoints too, and "relationship-layer ablation" understates the delta.

**O5. The 53/90 correction.**
- "Final roots unchanged" is guaranteed by arithmetic, because digital roots are additive mod 9. Compound meanings are not guaranteed.
- The closeout should state whether any earlier owner reading used those compound meanings.
- It should also state that the componentwise provenance is V1's, not WWYB's, which has no name chapter.
- This affects development only, but it separates "the V1 rule" from "historical outputs labelled V1".

**O6. Scorable residue.**
- Every interpretation bank has constructive and adverse alternatives with no a-priori selector (C2-A09, C-A23, J-A11/J-A13, JB-A15).
- Before launch, the design needs an estimate, made on development data, of what share of each arm's relevant layers will yield scorable cards.
- Without it, "full system" can describe a test of a thin mechanical residue.
- The precision simulation in §9 also needs this number.

**O7. Reader isolation.**
- The report and the admission contract carry owner-event labels (2008, 2018, 2029).
- The firewall should state that these artifacts are excluded from every reader context.
- I did not evaluate the labels themselves.

## Weakest step

**Design side.** The weakest step is §7's translation of "equal FP/miss costs" and "UNKNOWN not negative" into cell accounting.
- Each rule on its own is defensible: UNKNOWN cells excluded, abstention not treated as negative, exposure charged on observed negatives, a TP reward for transparency.
- Combined, their effective costs depend on ascertainment, abstention, silence and grid anchoring, and all four differ by arm.
- The step is presented as complete.
- It is the step most able to decide the ranking through bookkeeping rather than forecasting.
- The owner contract names equal costs explicitly.

**Source side.** The weakest step is turning single-pass readings of chart pages into source-defect labels without re-deriving them from the formulas. This has misfired twice: JB-A21 was withdrawn; J-A07 was not.

## Optional refinements (not defects)

**R1. C-A16 (Eva, age 19).**
- The printed 7 matches if "at 19" means "in the nineteenth year".
- The specification's own reading of pp.233–234 is that the first year is completed age 0. On that reading, the nineteenth year is completed age 18, which gives V/Y/N = 16/7.
- The table's printed age-12 value of 2 fits completed-age indexing.
- So the discrepancy depends on how the prose ordinal is read. Annotate it; do not shift the tape.

**R2. J20 (Race Consciousness runs).**
- Odd runs are always five long: completed ages ≡ 0–4 mod 9, for example 18–22 and 27–31.
- Even runs are always four long.
- The "19–22" example leaves out age 18 (9+1 = 10 → 1).
- The conclusion is unchanged.

**R3. JB13 / JB-A17 naming.** "Power 42/6" is the Power-phase square, not the JB07 Power Number. Cayce's Power Number would be 45+44 = 89 → 17/8. Rename it to avoid confusing the two fields.

**R4. Withdrawn wheel sentence.** JB17 and JB19 still carry the withdrawn wheel sentence; precedence currently comes only from the overlay. Add an inline "superseded" marker.

**R5. Campbell OCR risk.**
- Add an explicit OCR-numeral risk entry citing the p.16 "II".
- List which tables are corroborated by worked examples:
  - the letter table, via Bronn, Washington and Ford;
  - the Planes grid, via Ford.
- List which are not. For example, the p.221 planet list gives both 1 and 8 as Sun; flag it as a source-or-OCR question. That module is disabled.

**R6. Trivial controls.** Make constant-negative and base-rate forecasters explicit controls. Under equal costs and rare events, they are the floor every arm must beat.

**R7. Ranking rule.** The rule used to equalize coverage should be the same for every arm, for example the count of distinct supporting rule IDs, since no book supplies weights.

**R8. Cell key.** Put valence and impact into the cell key. A forecast with the wrong valence then scores an FP in its own cell, and the event scores an FN in its own. "Must match" alone leaves this undefined.

**R9. Time unit.** Choose the primary time unit blind to forecasts and to arm-level results. "Justified by observation quality" is close to outcome information.

**R10. Owner observation.** Classify any 2029 owner observation explicitly as non-confirmatory.

**R11. Branch selection.** Have branch selections made by someone blind to development outcomes, or by a fixed precedence rule. Otherwise "a reason independent of outcome fit" cannot be audited.

**R12. Contamination probes.** Add implementation-verification probes that detect a model reader silently importing another author's rules:
- Jordan's Y/W exclusion;
- the Javane–Bunker birthday year;
- Campbell's K/V values;
- the Cheiro letter table.

## Minimal path to AGREES

- **D1:** one reconciliation addendum and one fixture.
- **D2–D5:** text edits to design §1, §3 and §7 and to the admission contract.
- No source-rule changes, no imports, and no engine build are needed.
- The UNVERIFIABLE results (C01, C03, C04, C08, C10) remain so until a reviewer has page images or full primary text. That is a limit of this review, not a defect in the package.