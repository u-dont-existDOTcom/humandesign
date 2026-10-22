# B36 — Solar-elongation source contradictions and extended astronomical scan

**2026-10-21 UTC.** Five-book Jyotish reader; research-only. Two new source records in `SOURCE_CANDIDATES_B36.json`. Neither historical rulership outcomes nor birth charts were tested.

## First source rule: Sun third from Mercury

Uploaded English *Saravali* Ch35.168, physical PDF105, corresponds to Sanskrit **35.169** in [CSU chapter35](https://www.csu-lucknow.edu.in/e-books/saravali/p36.html), lines846–848. It places **Sun third from Mercury**, Venus fourth, all other planets fifth, with no debilitated or enemy-sign planet; it predicts political rule. Under **whole-sign counting**, Sun/Mercury must be at least **30°** apart. Geocentric Mercury never exceeds ~28° apparent solar elongation. The whole-sign antecedent is therefore **empty**, regardless of alleged outcomes. This is a separate source claim from earlier B35 cases.

## Second source rule: Venus mistakenly translated as Saturn, and impossible Sun aspect

Uploaded English Ch35.79, physical PDF100, lists **Mercury, Jupiter, Saturn** in fourth in own navamsas **aspected by Sun**. The [CSU Sanskrit 35.80](https://www.csu-lucknow.edu.in/e-books/saravali/p36.html), lines443–449 and [older Jain printing](https://jainqq.org/booktext/Saravali/009887), digitized text line2235, instead give **Mercury, Jupiter, Venus**. The Sanskrit compound `budha-bṛhaspati-dānava-ijyāḥ` refers to Mercury, Jupiter, **Venus** (teacher of the Asuras), not Saturn. Both sources include Sun aspects to this group.

Original text Chapter4.32–33 (uploaded PDF11) describes ordinary planetary aspects at the **3rd, 4th, 5th, 7th, 8th, 9th and 10th** signs relative to the planet, with different fractional/full strength. No solar aspect is specified to the same or immediately neighboring sign. Since Mercury remains within ~28° of Sun and thus only in Sun's same/adjacent 30° sign, it **cannot receive any such sign-defined Sun aspect**. This conclusion is conditional on Ch4's documented *graha dṛṣṭi* interpretation, not proof every conceivable interpretation of aspect is empty.

The historical source assertion and independent astronomy inference remain separate; neither claims that royal status is truly chart-predictable.

## Six-exaltation sky-support follow-up

Earlier B35 found that **six of seven** six-body exaltation subsets are ruled out geometrically; only the subset **omitting Mercury** was not immediately excluded. This leaves Sun Aries, Moon Taurus, Mars Capricorn, Jupiter Cancer, Venus Pisces, Saturn Libra.

`SIX_EXALTATION_SKY_SUPPORT_B36.json` records an exploratory **Moshier** geocentric **Lahiri sidereal**, 00:00 UTC proleptic-Gregorian scan covering astronomical years **−2999 to +2999**: **2,191,090 sampled midnights**. To avoid re-running 2.2 million complete six-body calculations, Jupiter and Saturn are screened in **ten-day blocks**, with generous **±15°** margins, and all days in candidate blocks are checked individually. The same algorithm reproduced a preexisting direct 1800–2199 daily sweep: **1,339** Jupiter/Saturn overlap days, **85** also Mars, **0** also Sun Aries.

Across the extended interval: **17,355** days had Jupiter Cancer and Saturn Libra; **1,153** also Mars Capricorn; **77** also Sun Aries; **zero** additionally had Venus Pisces, so **zero** all-six snapshots. The 77 Sun-candidate days form six episodes, and Venus instead appeared in Aquarius (14 days), Aries (10), Taurus (36), or Gemini (17). Nine candidate midnights had Moon Taurus, but none had Venus Pisces.

**This is NOT a proof of universal astronomical impossibility.** The grid may miss short sub-day opportunities, the bound-screen is not a formal continuous root isolation, and ancient-date Moshier calculations lack the project's pinned SWIEPH .se1 production provenance. Nor does zero sky support establish anything about astrology's human predictions. The subset omitting Mercury stays *not excluded by simple geometry*, with no observed full six-planet midnight in this specified study.

The exact locally executed Python file was saved as `six_exaltation_support_B36.py` and GitHub byte-verified against its tested hash. Source-only annotation count advances **407→409**, zero independent human prediction tests and zero model promotion. Next: source-critical aspect/house scope across Jataka and Parashara and specific rulership rules, with unchanged respondent/model isolation.
