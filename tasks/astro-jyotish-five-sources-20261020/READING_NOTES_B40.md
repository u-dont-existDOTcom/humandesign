# Jyotish B40 — Jupiter special-aspect discontinuity and a modern conjectural repair (2026-10-21)

**Status:** Source-critical comparison, 0 new original-five-book annotations, 0 human outcomes, 0 model promotions. Accepted original-five-book documentary count remains **417** (414 at B38 + three BPHS Sanskrit26.10–12 claims in B39). New files: `JUPITER_ASPECT_CRITICAL_VARIANTS_B40.json`, `jupiter_eighth_variant_B40.py`, `test_jupiter_eighth_variant_B40.py`.

## What the transmitted Sanskrit says

In the Sanskrit recension of *Bṛhat Parāśara Horā Śāstra*, **Chapter 26 verse 12**, the clause for the fourth and eighth full-sign offsets includes `dviguṇais tu lavaiś conāḥ kharasāḥ`. In context the common transmitted calculation is **60 virūpas minus twice the degrees traversed into that 30° sign interval**. With directed target-minus-Jupiter longitude, the specified 8-sign sector is **240°–270°**; literal implementation `60 − 2 × (d − 240)`. This goes **60 at 240°, 50 at 245°, 30 at 255°, 2 at 269°**, approaching **0** immediately before 270°. The **general** Ch26.6–9 fallback then gives **15** exactly at 270°, so the literal joined piecewise function has a **15-virūpa jump**.

The Portuguese second-hand source at line2343 agrees with subtraction in both the fourth/eighth intervals. The available Sanskrit witness is [BPHS Ch26.12](https://vedicpupil.in/library/books/brihat-parashara-hora-shastra/chapter-26/verse-12). We have not established a manuscript-critical archetype or that discontinuity was intended; nevertheless silently smoothing the transmitted arithmetic would falsely attribute a new formula to that Sanskrit.

## A clearly labeled modern correction, not another Sanskrit manuscript

Ernst Wilhelm's *Graha Sutras* (Kala Occult Publishers; [publisher book description](https://vedic-astrology.net/Books/Graha-Sutras.asp)), *Graha Dṛṣṭi*, printed **p329**, explicitly criticizes the transmitted eighth-interval instruction and proposes a **different formula** for the 240°–270° interval: `15 + 1.5 × (270 − d)`. A hosted [excerpt](https://pdfcoffee.com/graha-drishtipdf-pdf-free.html) discusses this as his own correction, not the literal Parāśara text. The alternative gives **60 at 240°, 52.5 at 245°, 37.5 at 255° and 16.5 at 269°**, approaching **15** at 270°, thus joining the ordinary rule continuously.

His hypothesis is motivated by numerical smoothness, but **continuity alone does not establish predictive accuracy, original authorship or correctness of a historical manuscript**. Preserve `sanskrit_literal` versus `wilhelm_editorial_repair` as distinct explicitly named research methods. The official book listing identifies Wilhelm as author of the modern commentary, while the excerpt gives the numerical proposal. We have NOT uploaded or reproduced the copyrighted book.

## Another publicly documented derivative table cannot be used without checking

The [Saravali open-source astrology documentation](https://saravali.github.io/astrology/drishti_sputa.html) (site states updated 2017-11-06) says aspect values always stay in **0–60** virūpas, yet its general **150°–180°** row literally says `2 × (150−a)`, which gives **−20 at 160°**. For Jupiter **240°–270°** it prints `15 + 2 × (270−a)/3`, which gives **35 at 240°**, contradicting the same page's declaration that Jupiter has a full **60** at 240°. These are **internal arithmetic errors** in a secondary software-reference table—not new historical source variants or evidence against astrology.

No routine was copied from that problematic modern table. Its two errors are preserved in `JUPITER_ASPECT_CRITICAL_VARIANTS_B40.json` to prevent an unverified calculator from inheriting them.

## Mechanical checking, and what remains open

The new source-version-gated `jupiter_eighth_variant_B40.py` uses the unmodified B39 literal method, and applies Wilhelm's proposal **only** for 240≤d<270 if `version='wilhelm_editorial_repair'` is explicitly passed. There is no default. `test_jupiter_eighth_variant_B40.py` has **five passing local tests**, checking unchanged original, published example 245°/52.5, known divergence, boundary behavior, input validation and 0–60 bounds. B38 general and B39 special method tests additionally passed **14**, total **19/19** in this turn. Both B40 Git blob hashes match the locally tested files exactly.

**No human predictive accuracy was evaluated**. The difference in output is a calculation-method comparison only. The user still wants thorough reading of the five uploaded works; the source critical study must continue beyond this narrow aspect passage with source-version fidelity and true forward-blind participants when ready.
