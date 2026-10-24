# First-edition Lilly primary directions: observable event-target candidates

**24 October 2026 — Source-backed candidate interpretation, NOT a frozen predictive model or a human astrology result.**

## Owner outcome (remains OPEN)

Accurately compute distinct historically attested astrology techniques across traditions and compare **precommitted chart-derived predictions** with untouched forward-blind human behavior/event evidence and controls. The previous 12-method primary-direction inventory is one Western supporting lane. Source transcription, program correctness, prediction interpretability, and prediction accuracy are separate accomplishments.

This stage moves forward from the 12-method source inventory, **not** back to the unresolved 1647 numerical Naibod table. An incomplete historical table is never passed off as a complete timing key. It also does not make its incompleteness a blocking requirement for unrelated well-specified diagnostic arms.

## Primary evidence actually examined

William Lilly, *Christian Astrology*, Book III, **first printing 1647**, Chapter CLIX printed pp.657–659 and Chapter CLX printed pp.668–670. These are six **visually inspected facsimile pages**, sourced through Wellcome Collection's original book scan (`b30338724`) and copied under `witness_pages/`. Digests and image identifiers are in `LILLY_1647_EVENT_CANDIDATES.json`. **These images are the original witness**, not the later 2003 retypesetting, and are public domain according to the Wellcome catalogue.

Four *body-to-angle conjunction* passages (the existing engine can compute this shape):

| ID | Historical feature | Primary page | Historically stated consequence | Bounded, modern discriminator (researcher inference) |
| --- | --- | --- | --- | --- |
| L1647-MC-JUP-BODY | Midheaven directed to Jupiter body | 669–670 | Preferment; professional office or dignity according to circumstance | Dated new formal role, promotion or appointment with changed responsibility |
| L1647-MC-SAT-BODY | Midheaven directed to Saturn body | 668 | Loss of office, favor, trust or honor; adverse social consequences | Dated involuntary dismissal/demotion or removal from organizational office |
| L1647-ASC-JUP-BODY | Ascendant directed to Jupiter body | 657–658 | Gifts/patronage, prosperity and **several alternative effects** | Dated material grant, property gift or outside-kin patronage of independently prespecified significance |
| L1647-ASC-MARS-BODY | Ascendant directed to Mars body | 659 | Controversies, lawsuits and other adverse effects | A dated formally lodged legal/dispute complaint naming the participant |

The table is a **translation from historical claims to test candidates**, *not* four literal unconditional predictions by Lilly. The original repeatedly distinguishes social roles, nativity context, benefic/malefic aspects, and multiple alternative manifestations. No one may rescue a missed modern predicate afterward by claiming an unspecific alternative effect confirmed the rule. The Asc–Jupiter materiality threshold is not yet chosen; that candidate cannot be frozen as written.

**Critically:** Midheaven to Saturn's *body* (p.668) must not be conflated with Midheaven to Saturn's *square/opposition* (p.669). Jupiter body's potential professional preferment also cannot be counted as independent of Jupiter aspects without a real dependence analysis.

## Interpretation versus implementation

- `LILLY_1647_EVENT_CANDIDATES.json` separates source excerpts and page references from our modern exact outcome definitions and exclusions.
- `src/hdmatch/astrology/event_hypothesis_windows.py` reads an existing **conjunction-only** timeline and projects all four candidate rule exposures as research-only age windows. It **never reads event histories or participant answers**.
- Research-preview settings, **not historically authenticated timing rules**: age 18–65, half-open contact window [age − 0.5, age + 0.5) clipped to eligibility boundaries; only the software's `direct` direction-sense; one degree/year as a diagnostic; all three existing geometry outputs retained separately unless exactly coincident.
- Historical `in that year` or `yeer` does not establish the above half-year tolerance centered on the model date. Modern model dates use the existing mean tropical year, NOT Lilly's 1647 original numerical table.
- Geometry equal to within 1e-9 symbolic year for one rule is one exposure with multiple method labels, **not multiple confirmations**. Nonidentical geometry or time-key timings remain competing arms: it would be invalid to accept whichever hits an event.

## Falsifiability and independent outcome ascertainment

For genuine forward-blind evaluation, freeze the exact calculation algorithms and source choices, natal data/ephemerides and uncertainty, timing tolerances, evidence collection rules, causal/exposure eligibility, thresholds, all competitor predictions, method dependencies, and null/randomization before **future events occur or their coded outcomes are collected**. A prior life history can serve retrospective **blind** development, but it is not a new forward-prospective outcome.

Possible study unit: a participant-calendar interval with prespecified eligible occupational or dispute ascertainment status; coded binary independent event indicator in each preannounced window. If a participant has no eligible professional role to lose, record that opportunity separately without declaring a hit; this denominator must be frozen before chart reveal. Record missed outcomes, incomplete documentation and never suppress failed predictions. No medical, mortality or safety advice derives from this corpus.

Use an age- and opportunity-matched exposure comparator and a genuine chart-label permutation null when a sufficient cohort exists; also report unadjusted/family-wise uncertainty, all 4 rules, geometry alternatives, background event rates and unmatched event counts. Calibrated probabilities and final primary endpoint **have not yet been specified**. Proper scoring must not be claimed from symbolic support without calibration.

Source-based **candidate selection is not automatically independent from past conversation knowledge**. This agent has access to older contextual knowledge about individuals; it did not query personal event records in this phase, but these four candidates must be developed and judged on participants wholly untouched by any model fit or anecdote.

## Sparse exposure diagnostic

Four body-to-angle conjunctions are just a deliberately small source-check pilot: many real charts may contain **none of these exact contact directions** in adult ages. An empty projection is a valid result, not evidence of predictive failure or success. Do not enlarge the method set or change the time key post hoc to manufacture hits. A larger, source-grounded *aspect* arm can later be preregistered separately, avoiding conflation with the body's conjunction.

## Provenance and rebuild

Parent: `research/primary-direction-method-inventory-20261024`, commit `f6f922a9449932118c44a2c2c4166a9fcdec73f7`. This branch is **independent** of Hellenistic, Jyotish, Chinese and human survey worktrees. Original 1647 images already committed as reproducible source evidence; no paid Kindle text or personal natal/events are added.

Run from checkout:

```bash
export PYTHONPATH="$PWD/src"
"$HOME/humandesign/.venv/bin/python" -m pytest -q tests/unit/test_primary_direction_event_hypotheses.py
"$HOME/humandesign/.venv/bin/python" docs/astrology-research-map/primary-direction-event-hypotheses-20261024/build_preview.py
```

The preview uses ONLY the repository's published synthetic 2000 timeline. It never builds or scores an actual person's chart or outcome. Use the resulting `PRE_FREEZE_SYNTHETIC_EXPOSURE_DIAGNOSTIC.json` for coverage **diagnostics**, not for selecting rules to improve fit.

## Next research question

Before a prediction freeze, examine source-backed *aspect* versions and the exact original direction sense; then select a priori method arms and event thresholds, and design an adequately powered untouched cohort test across the complete astrology-tradition comparison. The 1647 source passages do not by themselves establish an advantage over chance.
