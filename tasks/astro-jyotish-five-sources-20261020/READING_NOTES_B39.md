# Jyotish B39 — BPHS special Saturn, Mars and Jupiter aspects (2026-10-21)

**Status: new source-only documentary annotations, not human validation.** The already-committed `SOURCE_CANDIDATES_B39.json` contains three source-located claims concerning *Bṛhat Parāśara Horā Śāstra* Sanskrit Chapter 26 verses **10–12**. Corresponding user-supplied Portuguese translation is at CP1252 lines **2323–2343**. `SPECIAL_ASPECT_SOURCE_AUDIT_B39.json` gives the literal piecewise arithmetic with source origins and numerical caveats.

## Different aspects are not one interchangeable calculation

B38 already documented the general **exact directional longitude separation** aspect strength in BPHS Chapter26.6–9 and kept it apart from *Sārāvalī*'s discrete Sanskrit-restored house fractions and Rath's Jaimini sign aspects. This B39 extends ONLY the exact longitudinal BPHS component. The special planetary definitions are not independent observed successes merely because three texts transmit related fractions.

- **Saturn (26.10):** for signed directed differences within 30°–60° (first sign after natal location), double elapsed degrees; 60°–90°, subtract half within-sign degrees from 60; 240°–270°, add within-sign degrees to 30; 270°–300°, double remaining degrees.
- **Mars (26.11):** 60°–90° gives `15 + 1.5×(d−60)`; 90°–120° gives `60−(d−90)`; 180°–210° full 60; 210°–240° gives `60−(d−210)`. Outside these intervals use B38 general aspect.
- **Jupiter (26.12):** 90°–120° and 210°–240° give `45 + 0.5×(within-sign degrees)`; 120°–150° and 240°–270° give `60−2×(within-sign degrees)`. Outside use B38 general. The last 240°–270° phrase is **what is actually transmitted in the cited Sanskrit witness**, not yet an independently reviewed manuscript-critical original.

Reproduced sources: [VedicPupil BPHS26 Sanskrit](https://vedicpupil.in/library/books/brihat-parashara-hora-shastra/chapter-26), [Enjoy Learning Sanskrit BPHS Ch26](https://enjoylearningsanskrit.com/scriptures/parashara/chapter-26/), and the user-provided CP1252 Portuguese text. The modern explanatory English at the second site is inconsistent in places with the Sanskrit of 26.11–12; it should NOT override source clauses without critical scrutiny.

## An explicit numerical source problem, not a silently smoothed function

The **literal Jupiter source plus the B38 general-rule fallback is discontinuous** at directed angle **270°**: immediately below, the 240°–270° source rule approaches **0 virūpas**; exactly 270°, ordinary BPHS returns **15 virūpas**. The code preserves that result. It could reflect a transmitted defect or an unmodeled boundary convention, but no modern repair is attributed to Parāśara without textual evidence. A subsequent B40 comparison will record Ernst Wilhelm's distinct **modern proposed repair** with its own source and variant label.

`bphs_special_aspect_B39.py` and `test_bphs_special_aspect_B39.py` were already remotely committed before this continued turn; new direct local execution of those seven tests plus seven B38 tests passed **14/14**. The B39 test suite explicitly preserves the 270° jump rather than hiding it. Re-running tests validates **the stated arithmetic**, not any prediction or manuscript reliability.

**B39 adds three source-only records:** last accepted status B38 **414**, B39 source-only baseline **417** once status is updated. Zero participant charts/outcomes or live model changes. Next: source-specific documented alternative for Jupiter's eighth-sign sector, not a silent modification of this B39 evidence.
