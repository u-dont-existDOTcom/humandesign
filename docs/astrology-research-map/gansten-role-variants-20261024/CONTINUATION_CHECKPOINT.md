# Continuation checkpoint: role-reversed and aspect-owner primary directions

**Date:** 2026-10-24 UTC.
**Owner message:** "continue" — continue the completed, auditable Swiss-file direction engine toward the still-unmet combined astrology empirical study. Do not restart earlier work or drift into unrelated Morinus debugging.
**Root state:** OPEN. This pass contributes a new mathematical role/rotation layer; full historical reconstruction and blinded predictive validation remain open.

## Newly implemented

- A separate module, role_directions.py, with three explicit contact constructions (body conjunction, promissor zodiacal ray, significator zodiacal aspect) and three role regimes (direct primary motion, traditional role-swapped converse, modern reversed rotation diagnostic).
- Traditional role reversal keeps a promissor-owned aspect fixed and advances the natal significator body forward, **not** a sign-negated direct arc. Moving angles and role-reversed significator-aspect variants are excluded pending primary-source evidence.
- Significator-owned rays are experimental, zero-ecliptic-latitude and direct-only; no universal historical permissibility claimed.
- No backward behavior change to original conjunction and prior two aspect profiles. New CLI flags are restricted to --profile role_variants. New JSON schema includes owner of ray, physical moving/fixed point, label, raw forward arc, symbolic date key.
- Frozen synthetic 2000 chart yields: 288 traditional converse promissor-ray contacts, 364 modern reverse-ray contacts, 288 direct significator-aspect contacts, 36 traditional converse bodily contacts; all within a 100-symbolic-year model window.

## Critical method-complexity result

In the seven-planet bodily unprojected ray profile, every traditional converse promissor-ray contact is *exactly the same geometric rotation* as a direct significator-aspect contact with promissor/significator **labels swapped**. The new 288/288 comparison test confirms this item by item. They may bear different source-defined meanings, but **cannot be counted as independent astronomical events** in future blinded tests.

## Assurance

48 relevant unit/neighbor tests passed, including the prior 36. New tests compare reversed-role arcs to the independent frozen proportional-phase and Cartesian Regiomontanus reference across 350 seeded synthetic geometries. The old conjunction timeline matches its frozen baseline. Ruff and strict mypy pass. Official external Swiss files are verified by the existing ephemeris adapter. No personal natal data, historic life-event labels or fitting performed. See VERIFICATION.json for files/SHA and test commands.

## Remaining research frontier

Recover and verify **literal** Lilly Naibod table cells and their variants, which the prior Gansten audit explicitly distinguishes from a modern mean-solar rational key. Also check original historical authorial permissibility of significator aspects and traditional role directions before freezing a historical package; complete latitude aspects (Bianchini/Morin), terms, Lot of Fortune, Moon secondary motion, and other method-specific timing/interpretation. Preserve mathematical equivalences for multiple-testing corrections. Eventually compare frozen systems on untouched blind human data.

**Branch:** research/gansten-direction-roles-20261024
**Parent:** research/gansten-primary-directions-aspects-20261024
**Release:** isolated research version only; production remains unchanged.
