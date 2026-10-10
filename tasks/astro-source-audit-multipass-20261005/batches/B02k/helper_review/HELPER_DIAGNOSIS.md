# Frozen helper diagnosis — source reader A

## Status and scope

**Two bounded changes are warranted:** validate the aggregate within-sign coordinate and retain the complete decreasing-and-leaving exception. The ordered timing fallback, distinct lunar thresholds, missing-data handling, unresolved time units, and benevolent-planet exclusion otherwise preserve the inspected passages within this helper's stated scope.

This is a **second-reader implementation check using existing source-first context**, not a fresh-context independent full-source evaluation. This document and its JSON companion were written before opening the producer test file or executing the helper. Findings below come from visual inspection of original page images and static code reading. No repository, catalogue, source image, or source PDF was edited.

Reviewed helper: `/workspace/scratch/43f75264c32e/humandesign-b02k/tasks/astro-source-audit-multipass-20261005/batches/B02k/lilly_sixth_opening_reference.py`  
SHA256: `972076c053dc8ad340d6369ecdbf3893f3b1d1354231a087d0ade88b2a1f180f`

Original PDF: `/workspace/scratch/bd2460f96de0/Lilly-1647-Christian-Astrology-I-III.pdf`  
SHA256: `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`

Live UDA main AGENTS.md read for this turn: `c27948c88cf7553f95241cbae7edab27f87689d2`. The companion JSON identifies each inspected source image and its hash.

## H-A01 — aggregate coordinate can fall outside a sign

**Change needed; implementation input-domain gap.** `remaining_degrees_in_sign`, lines 125–139, permits exact Fraction values in each component but validates only each component's separate range. Its sum can reach or exceed 30 degrees. Static arithmetic gives the counterexample `(Fraction(59, 2), 59, 0)`: every component passes, but the summed position is `1829/60` degrees and the returned remainder is `-29/60` degrees. This counterexample has not been executed at freeze.

The source asks for the degrees wanted before the planet gets out of its sign; the adjacent timing qualification remains months, weeks or days according to the sign's nature and quality. **Anchor:** original PDF283 / printed249, upper-middle paragraph beginning “If an infortunate Planet be in the sixt,” then “When, or how long” and “see how many degrees the malevolent Planet wants ere he can get out of the Signe.”

Validate the aggregate position as `0 <= position < 30`, or restrict the DMS representation enough to guarantee that invariant. Preserve current missing-data and unknown-time-unit behavior. This identifies a defect in the helper's declared within-sign domain; it does not attribute a Fraction API to Lilly.

## H-A02 — the Saturn exception loses “and leaving”

**Change needed; source qualification loss.** The source says “unlesse the disease be in its decrease and leaving the Patient or Querent.” **Anchor:** original PDF286 / printed252, opening paragraph, after the Moon decreasing in light and motion and coming to conjunction, square or opposition of Saturn.

The helper's `disease_already_decreasing` input and “already-declining exception” docstring, lines 147–153, do not preserve the full phrase. A caller who establishes decreasing but has no evidence about leaving can currently establish the entire exception and receive `CONTRADICTED`. The source includes the leaving qualification.

Use a caller-qualified aggregate explicitly defined as the whole phrase, for example `disease_decreasing_and_leaving`, or represent the two parts and negate their conjunction with three-valued semantics. If separate inputs are chosen, the form is `NOT(decreasing AND leaving)`, not `NOT(decreasing) AND NOT(leaving)`.

The phrase may describe one diminishing/leaving process, rather than two independent observations. A fully named aggregate preserves that ambiguity without inventing a clinical model. Also make the aspect input explicitly Moon-to-Saturn; the function name currently supplies that context, so this is a contract clarification, not another finding. The source's “for the most part” remains attached to the historical assertion. These predicates match prerequisites only and do not validate that assertion.

## Mechanisms with no blocking source finding

### Ordered timing and stage-3 alternatives

**Anchor:** original PDF277 / printed243, XLIV opening first, Secondly, and Thirdly paragraphs.

The first time is the first enforced bed or repose time, excluding the first slight symptom. The next alternative, if that time cannot be obtained, is the first urine inquiry carried to someone, physician or not. The third stage, if no such time is obtainable, gives the physician's first speaking, access, or first urine receipt without ranking them.

The helper preserves this order, does not fall through an earlier unknown availability, retains known stage-3 candidates, and does not choose among distinct event tokens by an invented rank. Selecting multiple candidates with one token rests on the explicit caller token-identity contract. Unknown availability is not converted into unavailability.

`UNKNOWN` and `CHOICE_UNRESOLVED` are implementation labels. At stage 3, `UNKNOWN` means the selection remains unresolved; it does not mean no admissible candidate is known. Lilly does not require the availability of all three alternatives to be established before considering one. The current conservative result retains that distinction by returning the known candidates.

### Two lunar thresholds

**Anchors:** original PDF114 / printed80, Chapter XIII's Motion paragraph and following slow-motion paragraph; original PDF286 / printed252, opening less-than-mean clause.

PDF114 gives mean motion as 13 degrees 10 minutes 36 seconds. Its distinct retrograde analogy uses strictly less than 13 degrees 10 minutes in 24 hours and expressly says the Moon is never physically retrograde. The helper keeps 47436 and 47400 arcseconds distinct and applies strict less-than comparisons, so the 36-second interval is preserved. Equality does not satisfy either predicate's own less-than comparison. Missing speed stays unknown.

The helper returns comparisons only. It does not execute the aspect-to-ascendant-lord condition adjoining the mean-motion clause on PDF286. It also does not equate below-mean speed with the separate “decreases in light and motion” condition.

### Missing coordinate components and time units

**Anchor:** original PDF283 / printed249, remaining-degrees paragraph cited in H-A01.

Apart from the aggregate range defect, the helper preserves missing coordinates instead of supplying zeros and returns exact remaining arc with an unknown time unit. Lilly's “Moneth, Weeks or Dayes according to the nature and quality of the Signe” is not turned into one fixed conversion. Requiring explicit zero components is a conservative input policy, not a rule about historical data entry. The surrounding sixth-house, malefic, and sign-transition conditions are outside this pure arithmetic helper.

### Benevolent-planet exclusion

**Anchor:** original PDF284 / printed250, opening paragraph: “a Benevolent Planet well fortified in the sixt, and he not author of the Disease.”

`benevolent_sixth_predicate` preserves benevolence, fortification, sixth-house placement, and the explicit non-author exclusion. Unknown authorship remains unknown when the positive facts hold; established authorship contradicts this predicate. The awkward following source wording “is not, or will be permanent” is outside the prerequisite helper and is not repaired or turned into an output here.

## Frozen-before-tests receipt

No producer tests have been inspected. No helper execution or probe result supports this initial diagnosis. The companion JSON records the planned bounded follow-up. After both diagnosis files are written and hashed, producer-test inspection and a small pure-function probe are permitted. No whole-suite claim is authorized: the assignment says the reference tables and rule bundle had not yet been written. The original diagnosis will remain unchanged; any changed-item reconciliation will be separate.

