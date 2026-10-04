# New-chat handoff — full numerology book audit

Date: 2026-10-04
Repository: `u-dont-existDOTcom/humandesign`
Branch: `research/six-rule-life-timing-20261001`
Status: GitHub is canonical. Continue from the frozen numerology methodology work; do not restart from memory.

## Owner goal

Do a **source-complete deep pass of the major numerology systems now**, using the uploaded books as primary sources, so we stop discovering important rules piecemeal after looking at outcomes.

The specific problem to solve is methodological completeness and rule creep:
- fully reconstruct each author's actual system;
- distinguish systems that only superficially share labels;
- freeze formulas/hierarchy/timing/name/relationship rules before using them on owner outcomes;
- never add a newly discovered rule to rescue an earlier miss.

Do **not** begin by retrodicting Joel's life again. Finish the source audit and freeze the systems first.

## Books the owner will attach in the new chat

Audit all four as primary sources:

1. **Cheiro — _When Were You Born?_**
2. **Florence Campbell — _Your Days Are Numbered_**
3. **Juno Jordan — _Numerology: The Romance in Your Name_**
4. **Faith Javane & Dusty Bunker — _Numerology and the Divine Triangle_**

If filenames/editions differ, identify the work by title/author and record edition/publication metadata.

Cheiro's _Book of Numbers_ has already been substantially audited and does not need to be re-uploaded unless the owner also supplies it. Use the existing project audit as the baseline and use _When Were You Born?_ to close the remaining Cheiro source gap, especially detailed zodiacal-period relationship/marriage material.

## Mandatory bootstrap before substantive reasoning

1. Fetch live default-branch:
   - `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md`
   - `u-dont-existDOTcom/universal-dev-architecture/LESSON-INDEX.md`
   - activate the relevant source/provenance/research-before-reinvention patterns.
2. Fetch live:
   - `u-dont-existDOTcom/humandesign/AGENTS.md`
3. Read these project files on the working branch before auditing books:
   - `reference/research/NUMEROLOGY_METHODOLOGY_AUDIT_V1_20261003.md`
   - `reference/research/numerology_method_registry_v1_20261003.json`
   - `docs/24_numerology_methodology_policy.md`
   - `notes/NUMEROLOGY_SYSTEM_COMPARISON_20261003.md`
   - `notes/CHALDEAN_LIFE_EVENT_RETRODIAGNOSTIC_20261003.md`
   - `experiments/astrohd/chaldean_life_event_retrodiagnostic_20261003.json`
   - `notes/NUMEROLOGY_NAME_LAYER_CORRECTION_20261003.md`
   - `notes/JOEL_NAME_GOAL_COMPARISON_CORRECTION_20261003.md`

Do not treat conversation memory as canonical when the repo has a newer artifact.

## Existing frozen systems

### CHEIRO_CHALDEAN_V1

Already frozen from _Cheiro's Book of Numbers_.

Key existing rules include:
- Birth Number = day-of-month root;
- zodiacal/planetary period kept separate;
- birth-year current kept separate;
- contextual name actually used in the relevant sphere;
- Chaldean letter table;
- name-parts reduced separately before combined name root;
- compound-number meanings;
- harmonic number families;
- special 4/8 rules;
- Birth-2 / Number-8 warning;
- lucky/action dates;
- compound future-date method;
- periodicity;
- ordinal life-year recurrence.

Important existing owner values:
- birth 1985-01-29;
- Birth Number 29 -> 2;
- Aquarius/Saturn period -> 8;
- public/use name `Joel Rosenblum`;
- Joel = 16 -> 7;
- Rosenblum = 37 -> 1;
- combined public Name root = 8.

Do **not** overwrite V1. If _When Were You Born?_ materially adds calculation or relationship rules, create an explicit **CHEIRO_CHALDEAN_V2** delta and preserve V1.

### DECOZ_CURRENT_V1

Already frozen from current official World Numerology/Decoz material.

Relevant inventory includes:
- Life Path, Birthday, Periods, Pinnacles, Challenges, Attitude, Sun Number, Age Digit;
- Expression, Heart's Desire, Personality, Maturity, Bridges, Karmic Lessons, Hidden Passions, Subconscious Self, Balance, Rational Thought, Cornerstone, First Vowel, Capstone, Planes;
- current-name Minor Expression / Minor Heart's Desire / Minor Personality / current-name Planes;
- Physical/Mental/Spiritual Transits, Essence, Personal Year/Month/Day, Duality;
- relationship/core-cycle compatibility;
- 11/22/33 Masters;
- 13/14/16/19 Karmic Debts;
- Y/W rules;
- current-name layer is minor in chart hierarchy but Decoz still claims adopted-name changes can have meaningful practical effects.

Do not silently merge Campbell/Jordan/Javane-Bunker rules into Decoz merely because they are "Pythagorean."

## Required audit outputs

For **each uploaded book/system**, reconstruct the author's method completely enough that a future worker will not need to keep discovering major layers during analysis.

At minimum extract and source:

### A. Source/edition
- exact title, author, edition/year if available;
- page-numbering scheme;
- table of contents / chapter map relevant to calculation.

### B. Input hierarchy
- birth date components;
- birth name;
- current/public/married/spiritual/nickname rules;
- whether legal status matters;
- name-change activation rules;
- contextual-name rules.

### C. Letter-number mapping
- exact alphabet table;
- vowel/consonant/Y/W policies;
- punctuation, hyphens, prefixes/titles;
- multi-part surname treatment.

### D. Reduction rules
- reduce components separately or total string;
- when to preserve compounds;
- master numbers;
- karmic debt/special compounds;
- whether zeros matter;
- treatment of 10+ / 100+ totals.

### E. Personality/chart architecture
Inventory every declared chart number and its hierarchy:
- core vs secondary/minor;
- date-derived vs name-derived;
- bridges, planes, lessons, hidden passions, challenges, cycles, etc.;
- which numbers authors say matter most.

### F. Timing/forecasting
Extract exact formulas and time boundaries for every timing system:
- Personal Years/Months/Days;
- Pinnacles/Periods/Challenges;
- Transits/Essence;
- age/ordinal-life-year rules;
- periodicity/recurrence;
- lucky dates;
- event tables;
- temporary vibrations;
- any date-selection method;
- whether cycles run Jan-Dec, birthday-birthday, or overlap.

### G. Name change
- how a new/current name modifies the birth pattern;
- how strong the author claims the effect is;
- lag/activation period;
- whether public vs private name differs;
- whether deliberate spelling optimization is recommended.

### H. Relationship methodology
- compatibility rules;
- marriage/partner-selection rules;
- name/date compatibility;
- cycle compatibility;
- whether different relationship contexts use different names.

### I. Event interpretation
- any source-defined mapping from numbers/cycles to beginnings, endings, relationships, spiritual change, danger, loss, career, travel, etc.;
- preserve exact scope and hierarchy rather than making a generic keyword dictionary.

### J. Peripheral modules
Catalog but keep disabled by default:
- health/medical claims;
- colors/jewels;
- addresses/house numbers;
- business/place names;
- Tarot/astrology synthesis;
- lost objects;
- gambling, etc.

### K. Ambiguities/conflicts
For every unclear or contradictory rule:
- quote/paraphrase the competing passages with page references;
- state whether the conflict can be resolved;
- otherwise preserve an explicit unresolved branch rather than choosing whichever helps a later result.

## New system IDs

After source audit, create separate frozen systems rather than a merged "best numerology":

- `CAMPBELL_YOUR_DAYS_V1`
- `JORDAN_ROMANCE_NAME_V1`
- `JAVANE_BUNKER_DIVINE_TRIANGLE_V1`

For Cheiro:
- keep `CHEIRO_CHALDEAN_V1` unchanged;
- create `CHEIRO_CHALDEAN_V2` only if the uploaded _When Were You Born?_ adds material rules required for current project questions.

For Decoz:
- keep `DECOZ_CURRENT_V1` unchanged unless a primary Decoz source itself requires correction.

Do not activate a historical system until its primary book has been audited enough to reproduce its formulas.

## Comparison matrix required

Produce a cross-system matrix showing, side by side:

- birth-name importance;
- current/use-name importance;
- legal-name relevance;
- name-change magnitude;
- letter table;
- compound/master-number policy;
- core-number hierarchy;
- timing systems;
- relationship systems;
- event timing resolution;
- spiritual/occult claims;
- source completeness;
- major ambiguities.

Explicitly flag where the systems make genuinely incompatible predictions.

Do not average conflicting systems.

## Empirical protocol after audit

Only after all four books are audited and system specs frozen:

1. Design a fair comparison using the **full relevant frozen layers** of each system.
2. Do not compare full Cheiro against one Decoz number, or vice versa.
3. Owner-history retrodiction remains DEVELOPMENT only.
4. Historical dates carry chronology quality:
   - documentary/contemporaneous;
   - strongly anchored memory;
   - approximate memory;
   - uncertain.
5. Unknown years remain UNKNOWN, not negatives.
6. False positives matter as much as hits.
7. Do not retune on Joel and call the result validation.
8. The real evidential target is frozen cross-person/prospective comparison.

## Known owner-history caution

2008 must stay labeled:
- **moderately consequential, not top-major**;
- college period;
- relationship rupture involving Sarita/Martha;
- substantial guilt/depression;
- do not upgrade it to "major" just because it appears in Cheiro's 1985 -> 2008 -> 2018 -> 2029 periodicity.

2018 is major.
2029 is prospective.

## Deliverables to save in the repo

At minimum:

1. `reference/research/NUMEROLOGY_BOOK_AUDIT_V2_<date>.md`
   - detailed source audit with page-level provenance.

2. `reference/research/numerology_method_registry_v2_<date>.json`
   - machine-readable complete method registry.

3. Separate per-system source/spec files where useful:
   - Campbell
   - Jordan
   - Javane/Bunker
   - Cheiro V2 delta if warranted.

4. Update `docs/24_numerology_methodology_policy.md` only if the audit reveals a genuinely necessary methodological control.
   - Do not weaken no-rule-creep/versioning protections.

5. A concise owner-facing summary:
   - what was genuinely new;
   - which prior assumptions were wrong;
   - whether any book materially changes how Joel should be analyzed;
   - what remains unresolved;
   - what books are still needed, if any.

## Stop condition

Do not stop at "I found some extra rules."

The source audit is complete only when:
- every major calculation/timing/name/relationship layer in each uploaded book has been inventoried;
- formulas are reproducible;
- ambiguities are recorded;
- separate system IDs are frozen;
- cross-system comparison is written;
- the registry is updated;
- no newly discovered rule can be silently inserted into a prior model.

If the books are long, continue autonomously through them and checkpoint progress in GitHub rather than asking the owner to choose which one to read first.
