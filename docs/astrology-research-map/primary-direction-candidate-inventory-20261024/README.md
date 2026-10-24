# Primary directions: source-attributed pre-freeze method inventory

Checkpoint 24 October 2026. This package advances the original astrology project purpose: accurately calculate competing historical systems, freeze rule choices before seeing the human answers, and compare predictions prospectively in a combined forward-blind test against matched controls.

**This is an inventory, NOT a frozen predictive model and NOT permission to begin scoring human participants.** No new mandatory historical book audit is imposed on unrelated valid methods. Human prediction interpretations and event/behavioral targets remain unconstructed at this stage.

## Why this matters now

After many source audits and increasingly sophisticated calculations, it was possible for the root objective to drift into endlessly improving software or transcribing faint digits. The preceding original-Lilly 1647 table work is now source-audited to 53 legible minute rows, 23 confirmed original-vs-2003 numerical cell differences, six faint rows and the absent label 27. Its conclusions are preserved separately without inventing values for the uncertainty.

This inventory consolidates the computational choices into TWELVE bounded method families and records the current source evidence and exactly what remains unresolved. It does not invent favorable event interpretations, perform retrospective target fitting, or treat synthetic arithmetic parity as human behavioral evidence.

## Key source distinctions preserved

1. **Original Placidus 1657, thesis 65** supports the timing principle of accumulating the Sun's successive daily equatorial right-ascension increments. The full historical mathematical/chronology configuration still needs certification. The current Swiss-file Placidus solar-key solver is a clearly named modern astronomical reconstruction, not automatically the author's entire system.
2. **Original Placidus 1657, theses 60–62** exclude angular significators and zodiacal rays in converse for that author. The generic mathematical role-reversed zodiacal ray algorithm remains available for other source-author questions. It is explicitly NOT presented as authenticated Placidus.
3. **Brahe 1573 Latin text**, preserved in a critical scholarly transcription, supports true varying solar daily motion. The exact two local-true-midnight endpoint choice in our modern algorithm is not proven by the inspected first-person passage.
4. **Original Lilly 1647 versus 2003 retypeset** retain separate literal-table readouts; neither should be confused with a smooth fixed 59′08″ key. Missing original minute rows and seconds are not silently interpolated.
5. **Traditional converse role swaps** and modern 360-degree complement reversal remain distinct mathematical constructions.
6. The earlier bodily/unprojected experiment demonstrated a **288/288 exact geometry overlap** between role-reversed promissor rays and direct significator aspects after swapping names. The two variants may retain different source meanings but do not furnish two independent astronomical confirmations.

## Inventory outputs

- PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY.json — machine-readable descriptions of 12 families, CLI flags for the 10 currently runnable algorithm arms, known source status, nonindependence groups, and an explicit NOT FROZEN/NOT VALIDATED flag for every arm.
- PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY.csv — one concise row per family, suitable for inspection/comparison.
- generate_inventory.py — deterministic reconstruction from existing calculation enums, original Lilly missing-cell constants, and previously inspected source-witness assessment functions.
- tests/unit/test_primary_direction_inventory.py — checks exact count, CSV/JSON consistency, source incompatibility, duplicate group and prohibition of false human validation claims.

This is a bounded **decision-preparation** artifact. It neither changes default computations nor disables existing math.

## How to regenerate from the durable Zorin checkout

After cloning the branch into its persistent folder:

    cd "$HOME/.local/share/hdmatch/research-checkouts/primary-direction-method-inventory"
    export PYTHONPATH="$PWD/src"
    "$HOME/humandesign/.venv/bin/python" \
      docs/astrology-research-map/primary-direction-candidate-inventory-20261024/generate_inventory.py
    "$HOME/humandesign/.venv/bin/python" -m pytest -q \
      tests/unit/test_primary_direction_inventory.py

The associated prior source audits and all existing historic examples remain readable in the repository.

## Explicit frontier and next action

The currently open task is NOT selecting more geometries after seeing a participant's life events. Before a predictive experiment can be described as a real astrology test, one must source and freeze **a limited set of exact interpretable target rules**: which promissor/significator/house/ray configurations are claimed to predict what independently assessable future outcome, what age-window tolerance, and how each target and control will be scored. The owner has expressly asked to allow combined source systems; no single Lilly/Placidus default is automatically preferred.

The first next safe research deliverable is a bounded, source-anchored comparison of historically stated **event meanings** (without consulting user-specific life histories), with hypotheses for blinded evaluation. This can be prepared independently of participant recruitment. Independent participant consent, blinding, freezing and score calibration remain separate non-negotiable human-study requirements when an actual prospective study is undertaken.

**Closure:** source inventory completed, project root objective OPEN, historical numerical correctness DOES NOT equal validated predictive power.
