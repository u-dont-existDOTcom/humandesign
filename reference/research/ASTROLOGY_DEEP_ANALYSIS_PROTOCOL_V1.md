# Astrology Deep Analysis Protocol V1

Status: CURRENT DEVELOPMENT PROTOCOL

## Goal

Prevent person-specific astrology readings from depending on whichever aspect, rule, or tradition happens to catch the reader's attention first. A deep reading is a coverage-controlled analysis, not an improvisational narrative.

The machine-readable authority is `ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V1.json`. Before synthesis, every required pass must be explicitly dispositioned and a receipt must pass `scripts/validate_astrology_deep_analysis_receipt.py`.

## Core structure

1. **Authority first.** Load the current person-life ruleset index and consolidated catalog. Older retained models cannot be silently skipped because a newer chat is focused elsewhere.
2. **Information firewall.** Classify the analysis as clean-room, retrospective-blind, development or prospective. For a new clean-room person, freeze the first pass before opening biography/survey/history.
3. **Input provenance.** Resolve historical timezone, birth-time source quality, location precision and uncertainty before using houses or angles.
4. **Birth-time sensitivity.** Recompute angle/house-sensitive claims across the declared uncertainty interval and keep unstable claims conditional or set-valued.
5. **Astronomy first.** Produce the complete planetary/angle/house state from verified Swiss Ephemeris before interpretation.
6. **Geometry pass.** Enumerate all frozen major planet-planet and planet-angle aspects mechanically, rank the tightest, and preserve hard as well as supportive geometry.
7. **Lilly pass.** Run essential and accidental strength/debility, motion, visibility, Moon phase and frozen partile benefic/malefic conditions.
8. **Hellenistic pass.** Run the currently encoded Ptolemy/Valens dignity, sect, joy and whole-sign/ruler structures.
9. **Jyotish pass.** Run the currently encoded Lahiri/Phaladeepika sign, house and strength structures.
10. **House-ruler topology.** Inspect all twelve house rulers, where they land, concentrated rulership and topic-specific derived houses only when source-grounded.
11. **Full V1.4 vector.** Run the whole source-grounded library, not merely a hand-picked subset. The six-rule owner-fitted signature is a secondary comparator only.
12. **Contradiction pass.** Preserve simultaneous strength/debility, public/private tensions, and mixed testimonies. Deduplicate shared astronomy across traditions.
13. **Topic pass.** Only after the generic chart is complete, activate the relevant endpoint modules from the merged timing registry.
14. **Timing state.** For dated questions, separate slow-state evidence from medium-range progressions/solar arcs/profections.
15. **Day trigger.** For exact-date questions, add fast triggers only under a predeclared trigger rule and measure false-positive burden over the declared horizon.
16. **Experimental candidates.** Consider CF-003 and retained timing candidates only when their prerequisites and endpoint scope match.
17. **Cross-system fusion.** If numerology or Human Design is requested, compute each separately first, then report convergence, complement, contradiction and dependencies.
18. **Completeness gate.** No final synthesis until every required pass has a valid status and evidence/reason.
19. **Layered synthesis.** Report stable high-confidence themes, contradictions, time-sensitive claims, nulls, uncertainties and evidence status.

## Why this is deeper than the previous workflow

The current V1.4 executable library is broad but still **not “all of astrology.”** It operationalizes hundreds of source-grounded atomic conditions from Lilly, Ptolemy, Valens and Phaladeepika, but whole traditional subfields remain outside the frozen implementation. Examples include Hellenistic Lots and time-lord systems, fuller reception/bonification/maltreatment doctrine, primary directions, a fully source-audited solar-return system, and large Jyotish families such as nakshatras, Vimshottari dashas, vargas and yogas.

Those are not ignored. The protocol requires them to appear as an explicit **UNAVAILABLE / not-yet-frozen frontier** rather than being silently forgotten or improvised after an outcome is known.

## What “fool-proof” means here

It cannot guarantee that every historical astrology technique has been encoded. It can make the omission visible and mechanically block a supposedly complete analysis that skipped one of the currently required families.

The protection has three levels:

- **Catalog:** what important rulesets currently exist.
- **Routing index:** which of them must be considered for this person's question.
- **Coverage receipt validator:** whether the analyst actually dispositioned every required pass **and every required subcheck** before synthesis.

A new strong ruleset changes the catalog/registry first. Future analyses therefore inherit it automatically instead of relying on chat memory.
