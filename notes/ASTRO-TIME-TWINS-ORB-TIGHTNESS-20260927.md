# Astro time-twins: orb tightness / conjunction-strength note

Date: 2026-09-27

## Question

Does the existing time-twin literature, or the current theory-neutral same-hospital protocol, account for the astrological claim that a chart is expressed more strongly when conjunctions/aspects are very tight (small orb)?

## Finding

Not in the primary time-twin analyses.

- Roberts & Greengrass (1994), and French, Leadbetter & Dean's 1997 re-analysis, compared personality resemblance with birth-time separation. Their published/reported statistical analysis does not condition the result on conjunction/aspect orb.
- Dean & Kelly (2003) deliberately avoided interpreting chart factors: near-simultaneous birth was used as a proxy for chart similarity, and personality/behavioral resemblance was tested by chronological proximity. The primary analysis therefore does not ask whether pairs with unusually tight aspects are more similar than pairs with wider aspects.
- Dean et al.'s later *Understanding Astrology* (2022) does contain a chart-specific follow-up using the same 1958 cohort. It notes shared aspects during the week and examines an especially strong Saturn configuration: Saturn exactly opposite the Ascendant and square the Moon within 0.1 degrees / about one minute. The predicted extraversion dip was not observed (reported p=.22). This is relevant to the "tight aspect" objection, but it is not the original general time-twin analysis and should be treated as an exploratory/targeted follow-up.
- Michael Startup (1985), in the *British Journal of Social Psychology*, directly tested astrological aspects against personality. One study examined whether personality varied as a function of the angular separation between planets at birth; no supporting evidence was reported. This is closer to an orb/tightness test than the time-twin papers.
- Within the astrology-focused journal *Correlation*, Kyösti Tarvainen (2022) specifically tested the claim that tight aspects are stronger than wide aspects across four datasets totaling >50,000 charts and reported no consistent support. A 2021 review by Tarvainen characterized the average tight-vs-wide tendency as weak, with the clearest change occurring near the maximum working orb rather than a simple "tighter = much stronger" gradient. These claims come from astrology-focused research literature and should be kept distinct from mainstream psychometric evidence.

## Interpretation of the Reddit claim

The Reddit claim is a real astrological hypothesis, not merely a semantic point: smaller orb is often treated by astrologers as greater aspect strength. But the example combines at least two proposed modifiers:

1. Moon-Pluto conjunction tightness.
2. Angularity: the Moon-Pluto conjunction is also described as being on the Ascendant.

Those should be tested separately. The anecdote itself cannot test the claim because there is no comparison group of otherwise similar charts with wider Moon-Pluto/Ascendant distances.

## Current protocol status

The current proposed same-hospital time-twin protocol is intentionally theory-neutral and therefore does **not** currently use aspect/conjunction tightness in its primary analysis. That is appropriate for the first-stage question: does precise birth time/place contain any reproducible information about personality at all?

However, orb tightness should be added as a **pre-registered secondary astrology-specific moderator**, not introduced after seeing results.

## Recommended protocol amendment

Keep the primary analysis unchanged. Add a frozen secondary "chart-strength moderation" layer before collecting outcomes.

### A. Geometry

For every participant, calculate from the frozen ephemeris:

- exact ecliptic longitude for the predeclared planet/point set;
- conjunction orb = absolute angular distance from 0 degrees;
- other major-aspect orb = distance from the exact target angle;
- Ascendant/MC angular distances separately;
- applying vs separating status as a secondary descriptor.

Do not tune orb cutoffs from the personality outcomes.

### B. Predeclared tightness variables

Use both continuous orb and a small number of frozen descriptive bands, e.g.:

- exact/tight: <=1 degree
- moderate: >1 to 3 degrees
- wider: >3 to the predeclared maximum orb

The continuous analysis should be primary within this secondary module so conclusions do not depend on arbitrary bins.

Separate:
- personal/luminary aspects;
- aspects involving Ascendant/MC;
- slow-planet-only aspects, which can be shared by large birth cohorts and are therefore less person-discriminating.

### C. Pair-level moderation test

For each time-twin pair, test whether personality-profile similarity is greater when the shared chart contains tighter predeclared aspects.

A suitable model is conceptually:

personality similarity ~ birth-time separation + location match + chart-tightness + (birth-time separation x chart-tightness) + frozen covariates

The key term is the interaction: if the Reddit hypothesis is right, near-time pairs with very tight salient aspects should be more alike than equally near-time pairs whose charts lack such tight aspects.

### D. Specific-aspect test

A stronger test of a claim such as "tight Moon-Pluto conjunction produces caricature-like emotional intensity" requires a trait mapping frozen before outcomes are seen.

Use an independent astrologer panel to specify:
- which measurable traits Moon-Pluto is predicted to affect;
- expected direction;
- maximum orb;
- whether angularity modifies it;
- whether applying/separating matters.

Translate those predictions into validated questionnaire scales/items and freeze the mapping before participant data are unblinded. Otherwise the study can test only generic pair similarity, not whether a specific aspect means what astrologers say it means.

### E. Multiple-comparison protection

Do not scan hundreds of aspects after seeing the data and report the best one. Either:
- choose a small preregistered set of aspect hypotheses;
- use a held-out replication cohort; or
- use multiplicity correction with all tested aspect hypotheses declared.

The cleanest architecture is:

1. **Primary theory-neutral test:** exact birth time/place -> personality similarity.
2. **Secondary preregistered astrology moderator:** does predeclared aspect tightness strengthen the signal?
3. **Specific confirmatory aspect tests:** e.g. Moon-Pluto + angularity -> predeclared psychological outcomes.
4. **Held-out replication:** required before treating any discovered aspect rule as established.

## Sources

- Dean, G. & Kelly, I. W. (2003), "Is Astrology Relevant to Consciousness and Psi?", *Journal of Consciousness Studies* 10(6-7), 175-198: https://journalpsyche.org/articles/0xc062.pdf
- French, C. C., Leadbetter, H. & Dean, G. (1997), "The Astrology of Time Twins: A Re-Analysis", *Journal of Scientific Exploration* 11(2), 147-155.
- Startup, M. (1985), "The astrological doctrine of 'aspects': A failure to validate with personality measures", *British Journal of Social Psychology* 24, 307-315: https://doi.org/10.1111/j.2044-8309.1985.tb00693.x
- Dean et al. (2022), *Understanding Astrology*, time-twin chart follow-up, section 8.7.11: https://astrology-and-science.com/UA-4.pdf
- Tarvainen, K. (2022), "On the strength of tight versus wide and applying versus separating aspects", *Correlation* 35(1), 17-23: https://correlationjournal.com/on-the-strength-of-tight-versus-wide-and-applying-versus-separating-aspects/
- Tarvainen, K. (2021), "Statistical studies have started to advance astrological techniques", *Correlation* 33(2), 55-64: https://www.astrologicalassociation.com/wp-content/uploads/2021/05/c20213302-1.pdf
