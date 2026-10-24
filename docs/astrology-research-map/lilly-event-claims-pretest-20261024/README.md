# Original Lilly 1647: source-backed but unfrozen event-meaning candidates

**Checkpoint:** 24 October 2026. Research-only; no real participants, no historical outcomes, no chart-to-event forecasts, and no retrospective fitting.

## Parent objective: unchanged and OPEN

Accurately reproduce source-defined astrology calculation traditions, keep competing interpretations separate and numerically reproducible, then freeze actual predictions **before receiving blinded human responses** for a combined forward-blind comparison across astrology systems and appropriate alternative-chart/control baselines. The source audit, geometry engine and outcome assessment are different scientific stages. This pass begins the previously missing **interpretation mapping** stage without falsely representing source language as a ready-to-score hypothesis.

## Direct 1647 primary sources

I directly examined genuine **FIRST-EDITION 1647** photographs of William Lilly, *Christian Astrology*, Book III, in the Wellcome Collection s7z7c46y, IIIF b30338724. Eight selected high-resolution source JPEGs from printed pp.654,657,659,661,669,670,683 and 684 are preserved with per-file SHA-256 digests and exactly cited inside LILLY_1647_EVENT_CLAIM_CANDIDATES.json. Each short original excerpt is traceable to a printed page photograph. No original or modern source is assigned content solely from OCR.

Wellcome original photos are NOT the modern WorldAstrology 2003 retypesetting and not any pages of the paid Gansten book.

A separate Wellcome-page indexing error in the previous Naibod audit was caught while examining photos. The correct original printed 713–715 -> IIIF zero-based canvases 747–749, **not 746–748**. All previous source images and numerical readings were already correct; this branch corrects locator metadata and regenerates associated CSV and SHA records. Details: WELLCOME_CANVAS_LOCATION_CORRECTION.md.

## Crucial interpretive rule from Lilly himself

On printed p.654 Lilly lists general significations for planets, but explicitly says the house a planet occupies and rules in the nativity can determine which actual kind of thing the direction pertains to. The SAME page (Chapter CLVII) says the power, weakness and dignities of significator and promissor in the radix affect whether and how strongly the direction manifests. The source also discusses other timing indicators and mitigating configurations in surrounding text.

Consequently, a contact such as Sun/Venus is **NOT** a universal prediction that a given person will marry. Nor is MC/Jupiter, by itself, a universally valid prediction of a promotion. A complete historical prediction requires unimplemented interpretation preconditions, source-defined natal signification, event alternatives, a declared timing method and a pre-frozen outcome definition.

## Seven directly grounded interpretation candidates

| Code | Historic directional contact (Lilly 1647) | Source-permitted themes | Proposed independently observable event, NOT frozen |
|---|---|---|---|
| LIL-E01 | Ascendant -> body Jupiter (p657) | Gifts, patronage, public esteem | Formal award, recorded material grant or patronage |
| LIL-E02 | Ascendant -> body Mars (p659) | Conflict, lawsuits, alternative adversity | Filed formal legal proceeding with named participant |
| LIL-E03 | Ascendant -> body Venus (p661) | Love, union, marriage if age/circumstances permit | Dated civil marriage registration |
| LIL-E04 | MC -> Saturn square/opposition (p669) | Loss of existing office, employment, reputation | Recorded involuntary job loss or office removal |
| LIL-E05 | MC -> body Jupiter (pp669–670) | Formal preferment/office/honor according to situation | Documented promotion or appointment |
| LIL-E06 | Sun -> body Venus (pp683–684) | Courtship/union, marriage conditional on strong natal Venus | Registered marriage, not general happiness |
| LIL-E07 | Sun -> sextile/trine Venus (p684) | Marriage where absent OR birth of a son/daughter; other advantages | Two mutually non-equivalent alternatives — no endpoint selected |

All historical statements are separately paraphrased and accompanied by a short original text fragment, printed-page locator and original JPEG hash. Proposed contemporary event codes, documentary definitions, eligibility and eligibility caveats are flagged **ANALYST PROPOSAL, NOT LILLY'S WORDS**.

Under LIL-E07, **do not award success for whichever of marriage or childbirth happened retrospectively**. These are separate possible hypotheses; specifying what to test, for whom, over what interval and with what base-rate control must precede knowing outcomes.

The seven claims belong to correlated outcome groups (relationship union, career office, litigation and patronage). Their claims, multiple aspects and geometries are NOT independent confirmations simply because they make different records. The earlier exactly duplicated 288/288 promissor/significator role-swapped arcs must likewise be counted only once as astronomical rotation evidence.

No high-stakes medical, mortality, safety, legal advice or interpersonal instructions should be inferred from these classical passages.

## Implementation and actual code scope

- generate_source_claims.py deterministically emits source-grounded LILLY_1647_EVENT_CLAIM_CANDIDATES.json and readable CSV, retaining exact source versus analyst fields, key prerequisites and no-success status.
- A small **pure geometry-contact matcher** maps the historic promissor/significator/contact/aspect names to *already implemented* direct-role engine records. It refuses to match traditional role-reversed converse or modern reverse-rotation under a direct-only claim.
- Matching is a **mathematical proxy**: it does not certify exact 1647 computational method parity. No prior SWIEPH sources, key defaults, source witnesses or participant-facing scoring modules are modified.
- generate_synthetic_coverage.py runs ONLY an invented 2000-01-01 12:00 UTC, 45°N 0°E chart with a 125° geometric window. It reports contact-pattern counts across the existing three geometry algorithms, WITHOUT ages/dates or actual event results. Out of 7 claim definitions, 4 have some mathematical contacts in this one arbitrary sky, while LIL-E02, LIL-E03 and LIL-E06 have none. **This is neither predictive success nor falsification.** Neither the sky date nor chart time was selected to make contacts match.
- In a synthetic example, the same angle contact may appear under all 3 projection methods. Three geometric output rows are NOT three successful forecasts.
- tests/unit/test_lilly_1647_event_claims.py checks original image hashes, corrected source canvas offsets, labels, source/analyst boundary, historical conditions, alternate-outcome multiplicity, direct-role matching and synthetic-only data handling.

No temporal windows, key selection, subjective event classification thresholds, calibration, blinded controls or model freeze is claimed. The measured historical tables and all previously published math outputs are unchanged.

## Runnable owner handoff

Complete repository checkout on authorized Zorin Linux, when this new branch is cloned:

    $HOME/.local/share/hdmatch/research-checkouts/lilly-event-claims-source-engine

To regenerate the source claim register:

    cd "$HOME/.local/share/hdmatch/research-checkouts/lilly-event-claims-source-engine"
    export PYTHONPATH="$PWD/src"
    $HOME/humandesign/.venv/bin/python \
      docs/astrology-research-map/lilly-event-claims-pretest-20261024/generate_source_claims.py

To inspect the *synthetic, unscored* pattern-coverage diagnostic:

    HDMATCH_PRIMARY_DIR_EPHE_DIR="$HOME/.local/share/hdmatch/ephemeris/1800-2399" \
      $HOME/humandesign/.venv/bin/python \
      docs/astrology-research-map/lilly-event-claims-pretest-20261024/generate_synthetic_coverage.py

Run the new regression tests with the existing project virtualenv. Earlier source and mathematical tests also remain valid.

## Real next priority: make claims falsifiable without retrospectively selecting outcomes

1. Independently source and calculate the required **natal house rulership, essential dignity, affliction and significator prerequisites** for a bounded Lilly rule family, with disagreements preserved; do not interpret raw contacts as sufficient.
2. Distinguish and prospectively define ONE primary observable event measure per frozen hypothesis, or an explicitly preregistered joint/composite rule. For the source marriage/childbirth disjunction, choose testable eligible subgroups based on baseline states without seeing future events.
3. Select and freeze a small set of methods, geometries, time keys, event windows, baseline definitions, cohorts and competing decoy charts. Declare family-wise multiplicity and dependence BEFORE collecting the scored answers.
4. Keep this Western-primary-direction lane and the other astrology systems separate during development but eligible for a single prospective combined evaluation once independently frozen. No participant, consent or study-enrollment authority is claimed in this report.

**State:** seven source-attested conditional interpretations extracted and indexed; no ready-to-score predictions, no human validity results; original root goal OPEN.
