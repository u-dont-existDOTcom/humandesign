# P1 blind-adjudication and author-configuration methods scan

Status: bounded checkpoint-12 methods scan; architecture evidence only

This scan began only after commit `7d914af30bfe4c4817692067f8e4471f3c3e3987` froze the
source-free conception. It addresses the underlying problems of prior-domain familiarity,
theory-conditioned self-description, blinded eligibility review, disagreement, role separation,
independent authorship, convergence, selection effects, privacy, and decision-history custody.
It does not search for constructs, instruments, target-domain mappings, or human-facing screening
language.

## What the evidence can and cannot support

The strongest cross-domain evidence supports structural safeguards:

- disclose relevant relationships, activities, intellectual commitments, and prior exposure, but
  do not equate disclosure with automatic disqualification;
- separate evidence custody, judgment, authorship, content custody, later evaluation, and appeal
  or oversight roles;
- use written, versioned procedures and preserve the evidence, disagreements, recusals, and later
  changes on which a decision depends;
- represent what is masked rather than treating “blind” as an all-or-nothing label;
- freeze independent judgments or conceptions before discussion or synthesis can make them
  converge;
- treat agreement statistics as diagnostics of decision consistency, not proof that the shared
  decision is valid; and
- collect the minimum metadata needed for the declared purpose while retaining enough provenance
  to audit conflicts and supersession.

The evidence does **not** establish a valid P1 evidence standard, threshold, adjudicator procedure,
appeal rule, author count, or author/adjudicator configuration. Randomized peer-review studies show
that identity masking can change some judgments but does not reliably improve review quality or
error detection. A blinded clinical outcome committee study found limited added value under one
standardized setting. Social-influence experiments show that discussion can narrow diversity, but
other network experiments show that social information can improve accuracy under some conditions.
These mixed findings rule out treating masking, multiple judgments, or isolation as universally
sufficient.

## Method-family decisions

Every family below has exactly one checkpoint-12 classification. `REUSE_DIRECTLY`, `ADAPT`, and
`COMPOSE` mean only that a structural idea is suitable for the architecture. They do not select a
future human procedure.

| Method family | Classification | Architecture use or reason |
|---|---|---|
| Transparent prior-exposure and intellectual-relationship disclosure | `ADAPT` | Represent provenance without making disclosure dispositive. |
| Disclosure as the sole bias control | `INCOMPATIBLE` | Disclosure can be insufficient and can itself alter judgment. |
| Conflict disclosure plus recusal and role separation | `COMPOSE` | Keep disclosure, conflict state, recusal, and assignment history distinct. |
| Prespecified adjudication charter and versioned decision record | `ADAPT` | Represent a future procedure version without supplying its content. |
| Explicit masking-dimension metadata | `ADAPT` | Record hidden and visible classes; do not claim complete blindness. |
| Identity-masked review as a validity guarantee | `INCOMPATIBLE` | Empirical effects are mixed and masking does not establish correctness. |
| Independent initial judgments before resolution | `ADAPT` | Preserve separate first judgments and later resolution states. |
| Third-judgment or tie-break procedure | `UNRESOLVED` | A known option, but its trigger, authority, and evidence access are unselected. |
| Inter-rater agreement or reliability statistic | `BASELINE_OR_DIAGNOSTIC_ONLY` | Can diagnose consistency/error; cannot validate the eligibility standard. |
| Independent conception before any author interaction | `ADAPT` | Temporal separation is represented as freeze-before-synthesis provenance. |
| Independent conceptions followed by governed synthesis | `COMPOSE` | Represent two stages without selecting the synthesis procedure. |
| Social-influence or convergence monitoring | `BASELINE_OR_DIAGNOSTIC_ONLY` | Relevant threat evidence is mixed; monitoring cannot guarantee independence. |
| Selection-bias accounting across exposure/belief/knowledge strata | `ADAPT` | Preserve excluded, negative, disputed, and unresolved case counts without using belief as a rule. |
| Privacy data minimization with purpose and retention metadata | `REUSE_DIRECTLY` | Use the general principles structurally; operational fields and retention remain unselected. |
| Append-only custody, disagreement, and supersession history | `ADAPT` | Preserve earlier evidence and decisions rather than overwriting them. |
| Appeals, recusal, replacement, and deviation state governance | `ADAPT` | Represent states and provenance only; no procedure or exception is selected. |
| Automated substantive human classification | `INCOMPATIBLE` | Current evidence and authority do not support an executable classifier. |
| Belief, skepticism, mismatch, accuracy, curiosity, usefulness, or interest as a proxy rule | `INCOMPATIBLE` | P1 makes these non-dispositive and the evidence does not justify them as substitutes. |

## Evidence synthesis by problem

### Exposure, conflict, and role assignment

ICMJE treats disclosure as necessary transparency while explicitly noting that a relationship does
not always imply problematic influence. It includes intellectual beliefs, rivalries, and academic
competition and separates author, reviewer, and editor responsibilities. Reviewers and editors
with relevant conflicts should recuse. This supports distinct disclosure, conflict, recusal, and
role states rather than an exposure-equals-exclusion rule.

Experimental conflict-disclosure research warns that disclosure alone can license exaggeration or
leave recipients insufficiently corrected. The architecture therefore cannot treat disclosure as
a completed safeguard.

### Masking and adjudication

Regulatory clinical guidance uses independent committees, masked evidence, written charters,
managed conflicts, documented decisions, and defined disagreement resolution to reduce bias in
context. Those are transferable structural patterns. They are not evidence that the clinical
committee configuration is valid for P1.

Randomized studies of masked manuscript review show no dependable improvement in review quality or
error detection, while other studies find changes in recommendations or prestige effects. A
clinical committee evaluation likewise found that a blinded committee had limited added value in
one standardized trial. Accordingly, masking metadata is adaptable, but “masked review guarantees
validity” is incompatible.

### Agreement and disagreement

GRRAS treats reliability and agreement results as information about classification error and
requires transparent reporting of sample selection, design, and analysis. Agreement is therefore
a future diagnostic option, not a substantive eligibility standard. Two independent judgments and
a later resolution are representable, but the number of adjudicators and tie-break authority stay
unresolved.

### Independent authorship and convergence

Experiments on social influence show that exposure to others' estimates can reduce diversity and
undermine aggregate performance. Group discussion also produces convergence. Counterevidence shows
that social information can improve accuracy in some network conditions. The defensible
architecture is temporal provenance—freeze independent conception before synthesis—not a claim
that individual or group authorship is universally superior.

### Selection effects and self-description

Selection-bias literature shows that participation or exclusion associated with exposure-relevant
characteristics can distort the resulting sample. Demand-characteristics research shows that
self-reports can respond to perceived expectations and prior beliefs, but the evidence is
heterogeneous and does not supply a P1 classifier. The architecture should preserve the provenance
of belief/knowledge strata and negative or disputed determinations while leaving all human-facing
evidence standards unresolved.

### Privacy, records, and dispute preservation

GDPR Article 5 and the NIST Privacy Framework support purpose limitation, data minimization,
accuracy, storage governance, access control, and minimized audit logs. ORI rules and policies
support role-separated adjudication/appeal, custody of evidence, complete records, recorded
comments or denials, and preservation of decisions even when an investigation does not proceed.
HHS audit guidance illustrates append-or-link treatment of disputed amendments rather than silent
replacement. The checkpoint-12 architecture reuses or adapts those principles without selecting a
retention period, appeal procedure, or personal-data collection plan.

## Scientific limitations

- Most direct evidence comes from clinical adjudication, peer review, group estimation, research
  integrity, or general privacy governance—not P1 eligibility.
- “Semantic contamination” and self-concept integration do not have a validated P1 measurement.
- Masking can fail through inferable identity or contextual cues.
- Agreement can be high under a consistently biased standard and low under an underspecified but
  potentially useful one.
- Independent work reduces some convergence paths but can increase cost, burden, and duplication.
- Excluding all experts, believers, skeptics, or negative cases could create a systematically
  selected author pool.
- Data minimization and long-lived auditability create a genuine design tradeoff.

Scientific adequacy therefore remains `WARN`: the scan supports a decision architecture and threat
model, not a validated human process.

## Sources

The immutable query/source ledger is
`state/NATAL-TIME-P1-ADJUDICATION-SOURCE-LEDGER-V1.json`. Core sources include current official
ICMJE recommendations; EMA ICH E6(R3); FDA endpoint and monitoring guidance; ORI policies and the
2025 sample procedures; GDPR Article 5; NIST Privacy Framework 1.0; GRRAS; randomized masked-review
studies; blinded-adjudication evaluation; social-influence experiments; demand-characteristics
review; and selection-bias studies. Every included and excluded source has an explicit eligibility
decision in that ledger.

No screening method, evidence cutoff, operational workflow, author/adjudicator configuration, or
human action is selected.
