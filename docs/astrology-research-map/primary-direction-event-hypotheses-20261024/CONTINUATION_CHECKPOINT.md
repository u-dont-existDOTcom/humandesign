# Continuation checkpoint — Western primary directions, historical event meanings

**Date:** 2026-10-24
**Task:** western-primary-direction-event-targets-v0
**Research branch:** `research/primary-direction-event-hypotheses-20261024`
**Parent:** `research/primary-direction-method-inventory-20261024` (`f6f922a9449932118c44a2c2c4166a9fcdec73f7`)
**Primary owner outcome:** **OPEN** — historically reproducible competing astrology systems and a properly frozen, combined forward-blind prospective evaluation in untouched human participants, compared with controls. This source-meaning subtask contributes but does not satisfy the parent.

## Accomplished (do not repeat)

1. Reopened the previous verified 12-arm source/method inventory, not the older checkout's unrelated development branch.
2. Examined full original 1647 Wellcome Lilly scans for printed pp.657, 658, 659, 668, 669 and 670. All six source images and SHA-256 values are bundled under `witness_pages/` and indexed by the machine-readable registry. Unlike the 2003 retype, these are photographs of the original.
3. Source-anchored four bodily-conjunction interpretation candidate families:
   - MC → Jupiter body: formal preferment/role advancement, 1647 pp.669–670.
   - MC → Saturn body: loss of formal office/honour, p.668.
   - Ascendant → Jupiter body: material gifts/patronage and alternatives, pp.657–658.
   - Ascendant → Mars body: controversies and lawsuits, p.659.
4. Drafted outcome coding, exclusions, opportunity qualifiers and independent ascertainment forms. Explicitly distinguish quote versus interpretation.
5. Added a pure, research-only exposure projector with exact-geometry equivalence collapse. It will refuse other profiles/keys and does not read actual life events or evaluate truth.
6. Diagnostic synthetic fixture dated 2000 had **zero adult-age direct exposures** among these four very narrow contacts; preserved as an honest coverage finding, not a reason to change the rules after seeing humans.
7. Suite: **129 passed** with official Swiss ephemeris files, focused Ruff check and mypy pass. Pre-existing original Lilly table anomalies remain unchanged.

## Uncertainty and honest limits

- `CANDIDATES_UNFROZEN` means no actual human predictive interpretation, model key, questionnaire or participant was preregistered. Original 1647 fractional Naibod table remains incomplete, and neither 1°/year nor Placidus geometry is falsely attributed as fully authentic Lilly.
- Geometric `direct` uses current shortest-signed-arc software convention; historical direction sense remains to be researched before any literal-authenticity claim.
- Four body-to-angle pairings can be sparse and are not a powered prospective study on their own.
- The modern outcome categories are *derived, stricter subsets* of many 17th-century possibilities, with occupational opportunity constraints and unchosen external patronage magnitude threshold.
- A participant's own known historical events, including any owner history already in a conversation, would be DEVELOPMENT knowledge; never claim independent validation on those data. No person's natal/event data was read into these files or preview.
- No medical, violent, death, legal advice or high-stakes individual prognosis is issued; observed lawsuit filing is a neutral retrospective/prospective event type only.
- Quantitative null, exact test statistic, multiple-testing correction and prospective cohort design remain to be frozen.

## The next safe research action (no owner question)

Compare Lilly's **precise angle-to-aspect passages** on pp.657–670 against the already implemented direct zodiacal ray candidate arm, while preserving true promissor vs significator ownership; assess how many additional adult-age exposures become available using **synthetic-only** charts. This is *source-based coverage research*, never fitting to participants. Register any accepted aspect rules as distinct, evidence-dependent arms and choose a parsimonious source-method/key target for untouched scoring **before** seeing outcome records. Preserve the original four bodily rules and their failure/unknown statuses throughout.

After that, finalize numeric event thresholds and the forward-blind study freeze with all participating traditions. Do not claim entire project finished on code/tests.

## Rebuild

From this repository branch:

```bash
export PYTHONPATH="$PWD/src"
export HDMATCH_PRIMARY_DIR_EPHE_DIR="$HOME/.local/share/hdmatch/ephemeris/1800-2399"
"$HOME/humandesign/.venv/bin/python" -m pytest -q \
 tests/unit/test_primary_direction_event_hypotheses.py \
 tests/unit/test_primary_direction_inventory.py \
 tests/unit/test_lilly_1647_photo.py \
 tests/unit/test_historical_naibod.py \
 tests/unit/test_naibod_original_1647.py \
 tests/unit/test_solar_primary_source_scope.py \
 tests/unit/test_placidus_1657_latin.py \
 tests/unit/test_solar_time_keys.py \
 tests/unit/test_primary_direction_roles.py \
 tests/unit/test_primary_direction_aspects.py \
 tests/unit/test_primary_directions.py
"$HOME/humandesign/.venv/bin/python" -m ruff check \
 src/hdmatch/astrology/event_hypothesis_windows.py \
 tests/unit/test_primary_direction_event_hypotheses.py \
 docs/astrology-research-map/primary-direction-event-hypotheses-20261024/build_preview.py
"$HOME/humandesign/.venv/bin/python" -m mypy src/hdmatch/astrology/event_hypothesis_windows.py
```

No mass re-transcription of the six unreadable 1647 numerical minute rows without a materially new witness.
