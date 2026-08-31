# Option B bounded methods scan — 2026-08-30

## Boundary and chronology

This is a bounded methods review for the construct-neutral purpose
`measurement_reliability_prerequisite_screen`. It began only after the independent-conception
snapshot was committed at `aaec2fecad74a1dfc9fa6fa7ec75d90a77f9c1fd`.

Bound provenance:

- owner-record SHA-256:
  `c24bb062bd90466f0be1a5be03211c8933e80bc1b4eaeee9509d5856bea02fc4`;
- accepted checkpoint-8 head: `63bfb78909a97eb5b8b31efe55e065a6f78973a2`;
- frozen conception markdown SHA-256:
  `4a9d579e4dddf773eb7532ae725cc610662396806870a4235f1d7e5cccf5cf7e`;
- frozen conception JSON SHA-256:
  `d8b1692283271c2195a802d48e4b71307371424b075ff69ab502db51ca5d3ba8`.

The exact 24 queries, search date, sites, eligibility rule, source versions/identifiers, bounded
notes, and exclusions are in
`state/NATAL-TIME-OPTION-B-SOURCE-LEDGER-V1.json`. The method-family dispositions are in
`state/NATAL-TIME-OPTION-B-METHODS-DECISION-LEDGER-V1.json`. No copyrighted full-text corpus was
downloaded or committed. The scan searched the underlying measurement problem; it did not rely on
an HD-specific search.

This review chooses no construct, content, instrument, population, language, mode, model,
coefficient, estimator, cutoff, interval, sample size, missing-data method, accessibility policy,
or participant procedure.

## Evidence and bounded decisions

### Taxonomy, repeated measurement, and measurement error — reuse directly

The current official [COSMIN manual](https://www.cosmin.nl/wp-content/uploads/COSMIN-manual-V2_final.pdf)
and its official [reliability/measurement-error risk-of-bias tool](https://www.cosmin.nl/wp-content/uploads/COSMIN-RoB-tool_reliability-and-measurement-error_1.pdf)
separate relative reliability from measurement error and require the instrument/version,
construct, varied sources, repeated components, and population to be explicit. The tool treats
stability, interval appropriateness, and similar conditions as study-design questions rather than
defaults. The architecture therefore reuses the distinctions and prerequisite slots, not a
specific statistic or study design.

### Reporting — reuse directly, with version caution

The [GRRAS checklist](https://www.equator-network.org/wp-content/uploads/2012/12/GRRAS-checklist-for-reporting-of-studies-of-reliability-and-agreement.pdf)
requires transparent reporting of subjects/objects, raters, replicate observations, sampling,
process, interval, available information, blinding, independence, analysis, estimates, and
uncertainty. Those reporting fields are reusable. The original guideline is currently being
revised by the [GRRAS-COSMIN project](https://www.grras-cosmin.org/) during 2025–2027, so this
slice does not treat the 2011 checklist as a final current analysis prescription.

### Intended use and error sources — reuse directly

The open-access [Standards for Educational and Psychological Testing](https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf)
require evidence and documentation to match intended interpretations and uses, populations,
administration/scoring, raters, forms, modes, accommodations, and relevant error sources. They
also state that no single preferred reliability/precision approach or index covers every
situation. The architecture therefore blocks any unqualified declaration that a measure is simply
reliable and prohibits a universal index or threshold.

### Test–retest, agreement, and correlation — reuse distinctions; select nothing

COSMIN and [Berchtold's test–retest methods paper](https://journals.sagepub.com/doi/full/10.1177/2059799116672875)
support separating rank-order reliability from absolute agreement and measurement error.
Correlation can remain high despite systematic differences, so correlation-only evidence cannot
satisfy agreement. A future test–retest branch must first resolve temporal ontology, expected
stability, recall, interim events, condition equivalence, and interval rationale. No interval,
occasion count, or estimator is chosen.

### Inter-rater/intra-rater design and coder drift — adapt

GRRAS requires reporting independence, blinding, rater characteristics, and replicate counts.
Primary experimental work indexed as [ERIC ED161897](https://eric.ed.gov/?id=ED161897) demonstrates
coder drift as a distinct threat. The methods debate summarized in
[O'Connor and Joffe](https://journals.sagepub.com/doi/10.1177/1609406919899220) also makes the
appropriate coding approach depend on the later epistemic purpose. The repository may therefore
encode independent frozen commitments, prior-code visibility, immutable originals, adjudication
separation, drift threat state, and protocol lineage. It may not select coder count, training,
categories, adjudication rules, or a coefficient.

### Facet-based error models — baseline or diagnostic only

The original [generalizability-theory paper](https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/j.2044-8317.1963.tb00206.x)
shows why multiple observation facets and their interactions can matter. This supports a neutral
registry of candidate replication facets. It does not justify selecting a facet set, variance
model, design, or coefficient before the measurement object and intended use exist.

### Internal consistency — presently incompatible

The COSMIN taxonomy makes internal consistency interpretable only under prerequisites that include
a reflective model and appropriate internal structure. Neither may be assumed in this slice.
Internal consistency therefore remains an ineligible future branch, not a substitute for temporal
or rater reliability; no statistic or item rule exists.

### Missingness — adapt provenance and defer handling

The National Academies' [missing-data report](https://www.ncbi.nlm.nih.gov/books/NBK209904/)
emphasizes prevention, explicit assumptions, and sensitivity. Current official
[AAPOR disclosure standards](https://aapor.org/standards-and-ethics/disclosure-standards/) and
[standard definitions](https://aapor.org/standards-and-ethics/standard-definitions/) reinforce
mode/language/process disclosure and disposition/denominator provenance. The architecture may
distinguish item absence, occasion absence, dropout, refusal, technical failure, accessibility
failure, structural non-applicability, and unknown cause. It may not convert absence to a value or
select deletion, imputation, weighting, complete-case, or sensitivity methods.

### Response style, desirability, and reverse wording — adapt threats; reject default remedy

[Longitudinal response-style evidence](https://pubmed.ncbi.nlm.nih.gov/20230106/) shows that
acquiescence, disacquiescence, midpoint, and extreme response styles can themselves have stable
components. A primary [reverse-wording study](https://pubmed.ncbi.nlm.nih.gov/29694314/) found that
mixed positive/reversed wording can add method variance and weaken structure. The architecture
therefore registers response-style and desirability threats separately, and rejects reverse
wording as an automatic construct-neutral fix. No control item, response format, adjustment, or
score is selected.

### Personal validation and expectancy — baseline/diagnostic threat only

[Forer's original demonstration](https://pubmed.ncbi.nlm.nih.gov/18110193/) shows that people can
accept the same broadly applicable description as personally accurate. Stable acceptance of a
generic description is therefore not target reliability. Prior feedback, chart/label exposure,
authority cues, positive-valence asymmetry, familiarity, expectancy, and demand remain recorded
threats. This slice writes no generic statement, suggestibility item, manipulation, or score.

### Invariance and differential functioning — block pooling; later Pro review

The testing standards and the classic
[cross-cultural equivalence paper](https://pubmed.ncbi.nlm.nih.gov/26751106/) support requiring
comparability evidence before group interpretation. A current 2026
[methodological critique](https://pubmed.ncbi.nlm.nih.gov/40515498/) warns that automatic invariance
workflows can import inappropriate cross-group assumptions and must be tied to the intended
question. The only present decision is to block pooling/comparison while equivalence is
unresolved. Groups, models, fit rules, differential-functioning procedures, and partial-equivalence
policies require later review.

### Translation and cultural adaptation — adapt versioning; select no language

The testing standards and [Beaton et al.](https://pubmed.ncbi.nlm.nih.gov/11124735/) treat
translation/cultural adaptation as more than word substitution and require documented process and
evidence. Every translation or material cultural adaptation must therefore receive a new version
identifier. No language, culture, translation workflow, or equivalence declaration is selected.

### Accessibility, mode, and accommodation — adapt lineage; future target only

[WCAG 2.2](https://www.w3.org/TR/WCAG22/) is testable through automated and human evaluation but
does not cover every cognitive, language, or learning need. W3C supplies separate
[cognitive-accessibility guidance](https://www.w3.org/WAI/WCAG2/supplemental/). The architecture may
record a future WCAG 2.2 AA target, cognitive review requirement, and distinct mode/form/
accommodation lineage. It makes no conformance claim, implements no interface, chooses no mode or
accommodation, and never treats accommodation-related variation automatically as participant
error.

### Connected-component leakage and repeat participation — architecture retained, later review

The bounded scan found no established instrument or protocol that substantially overlaps the
project's proposed graph-level leakage boundary. The independent conception is retained: aliases,
repeated participation, partners, households, shared recruiters/sources/custodians/coders, role
changes, and transitive edges must be representable. No split algorithm, cohort allocation, live
relationship source, or role assignment is implemented. This family requires later Pro review.

## Independent-conception comparison

| Independent insight | Post-scan disposition | Reason |
|---|---|---|
| Claims conditional on versions, conditions, facets, and use | Reused | Current standards and reliability guidance directly require conditional evidence. |
| Leakage as a connected graph | Still novel | No direct overlapping protocol was retained in the bounded scan. |
| Contamination as monotonic history | Still novel | Source work supports blinding/independence; append-only exposure lineage is the repository's stricter architecture. |
| Missingness is provenance, not a value | Adapted | Missing-data and survey standards support cause/denominator preservation and explicit assumptions. |
| Agreement does not prove correct coding | Adapted | Reporting/coding work separates reproducibility from correctness and makes purpose material. |
| Stable response can reflect stable artifacts | Adapted | Response-style and personal-validation evidence directly supports the threat. |
| Version lineage for form/language/mode/accommodation | Adapted | Testing, adaptation, and accessibility sources require distinct documentation/evidence. |
| Synthetic validator proves closure only | Still novel | This is a repository safety boundary, not a literature-derived measurement method. |

No independent insight was superseded. None has been converted into an active empirical method.

## Final bounded disposition

Reuse: taxonomy/measurement-error distinctions, conditional intended-use logic, stable-condition
questions, and reporting fields.

Adapt: coding independence, contamination and drift provenance, missingness provenance,
response-threat registry, translation/version lineage, and accessibility/equivalence gates.

Reject as incompatible now: global score, universal coefficient/cutoff, correlation as agreement,
internal consistency without prerequisites, automatic reverse wording, silent missing-value
conversion, and unqualified pooling.

Remain unresolved or require later review: measurement identity/source, measurement model/content,
all quantitative choices, population/language/mode/accommodation, burden, coding design,
equivalence method, connected split, missing-data method, participant procedure, and progression.

No overlapping established instrument was found, no bespoke instrument was proposed, and no owner
decision is required to finish the current construct-neutral architecture. The owner gates already
identified by Pro remain blocked and unchanged.
