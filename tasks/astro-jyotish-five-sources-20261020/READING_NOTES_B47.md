# B47 — Two BPHS marriage-age statements can fire together in a real sky (2026-10-22)

**This is a source-consistency calculation only.** Online Sanskrit-transcription witnesses of Brihat Parashara Hora Shastra Ch18 **vv22 and 23** contain distinct ages: v22 **5 or 9**, v23 **7 or 11**. The first contains *śubha-rāśi*, translated either as **benefic-owned sign** or in one edition as the **ninth house**; the second says Sun in the seventh with its dispositor (the seventh lord in this setup) joined Venus. No personal natal chart or answer was accessed.

I constructed an **astronomically real possible arrangement** at a location deliberately treated as synthetic (0° latitude, 0° longitude), 10 February 1908 at **17:30 UTC**, then calculated with installed Swiss Ephemeris 2.10.03, **Moshier explicitly requested and returned**, Lahiri sidereal, whole-sign houses. Exact source provenance and longitudes in AGE_RULE_COACTIVATION_B47.json; runnable Python and isolated unittest suite are versioned with it. This is NOT canonical Swiss SWIEPH .se1 research infrastructure and must not be represented as a production chart.

- Ascendant **Cancer 16.890°** (106.890° total) -> seventh **Capricorn**, ninth **Pisces**.
- Sun **Capricorn 28.032°** (298.032°) is in the seventh sign.
- Saturn (seventh lord) **Pisces 2.913°** (332.913°) is in the ninth **and** Jupiter-owned Pisces, hence qualifies under BOTH current readings of *śubha-rāśi*.
- Venus **Pisces 3.322°** (333.322°) is exalted and conjunct Saturn within **0.409°**—satisfies even close-orb interpretation of 'joined'. Solar-Venus separation ~35.29° is astronomically ordinary.
- Consequently the isolated source implementation emits **{5,9}** for verse22 AND **{7,11}** for verse23; intersection is empty.

This is a consequential ***first-marriage timing*** source collision if both verses are read as forecasts of the same person's **single first marriage**. The classical verses say 'marriage' and might permit separate successive marriages or contain an unknown explicit precedence/exception, so this is **not an unconditional formal inconsistency in the ancient text**, much less evidence that astrology fails/succeeds. If one event at first marriage is the target, the model cannot secretly choose v22/v23 after seeing the marriage age. It must specify an **a priori** aggregation/abstention/precedence policy or report multiple incompatible candidate ages and every resulting miss.

**Verification:** Eight isolated unit tests actually passed locally. They check returned MOSEPH+sidereal flags, exact longitudes, sign assignments, angular proximity, coactivation and disjoint ages, mutations deactivating rules, and fail-closed unsupported ascendant. Preserve exact tested blobs when publishing.

**Ethics:** These verses refer to historical childhood marriage ages, are not contemporary prescriptive suggestions and cannot be quietly interpreted as age twenty-five, twenty-seven or twenty-nine to rescue known adult histories. The owner questionnaire and all existing human profiles were untouched.

**Next:** Source-level precedence rules in BPHS and original Portuguese alignment; compare other overlapping historical rules with chart-computable negative outcomes without using a known person's answer to choose among them.
