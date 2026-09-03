# Life Patterns Behavioral Freeze — Established-Work Scan

Date: 2026-09-03  
Independent conception snapshots: `18eccfe` and `d876f97`  
Scope: provenance/versioning, participant correction, immutable records, and
reproducible evaluation separation

## Disposition

The result is **adapt + compose**, not a novel provenance framework.

The project should compose a small application-specific schema from established
patterns:

- W3C PROV's separation of entities, activities, agents, derivations, and revisions;
- established electronic research-record controls that retain initial values and
  attribute later changes;
- participant/respondent validation used as an error-reduction and meaning-checking
  step, not as automatic proof that an interpretation is objectively true;
- content-addressed, versioned research objects with rich provenance; and
- time-ordered separation of data finalization from model analysis, with downstream
  evaluation documented independently.

This repository does not claim regulatory compliance with clinical-trial, FDA, or EU
law merely because it borrows sound record-integrity patterns from them.

## 1. Provenance and versioning

### Established work

The [W3C PROV-O Recommendation](https://www.w3.org/TR/prov-o/) models fixed-aspect
entities, the activities that use or generate them, and agents bearing responsibility.
It also distinguishes derivation, primary source, and revision. That is a close match
for this pipeline:

`participant turn -> provisional extraction -> participant review -> map -> freeze`

The [FAIR Guiding Principles](https://www.nature.com/articles/sdata201618) treat
detailed provenance as part of reusability and apply the same stewardship concern to
data, algorithms, tools, and workflows. [Datasheets for
Datasets](https://arxiv.org/abs/1803.09010) similarly recommends recording motivation,
composition, collection process, intended uses, and restrictions so downstream users
can assess fitness and reproduce results.

### Project adaptation

Use explicit source IDs, UTC timestamps, schema identifiers, provider receipts, and
canonical SHA-256 bindings. Preserve each stage as a distinguishable record. Do not
implement RDF or claim full PROV-O conformance in this bounded milestone; encode the
useful semantics directly in typed JSON.

Decision: **adapt**.

## 2. Participant review and correction

### Established work

Qualitative research calls checking an interpretation with respondents "member
checking" or "respondent validation." A useful methods overview, [How to use and
assess qualitative research methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC7650082/),
describes returning transcript summaries to participants for clarification or
elaboration and treating the feedback as additional data.

The practice has material limits. [Assessing quality in qualitative
research](https://pmc.ncbi.nlm.nih.gov/articles/PMC1117321/) recommends treating
respondent validation as error reduction that generates further data requiring
interpretation, rather than as a definitive validity test. A recent methods review,
[Optimizing qualitative methods in implementation
research](https://pmc.ncbi.nlm.nih.gov/articles/PMC12797730/), warns that unreflexive
post-hoc member checking can threaten validity and recommends stating why it is used,
how consent covers it, and how feedback enters the research process.

The [ICH E6(R3) Guideline](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106_ErrorCorrections_2025_1024.pdf)
provides a stronger record-integrity pattern: systems should document initial entries
and later changes; corrections should be attributed, justified, supported by source
records, and timely; and participant-requested corrections should be allowed without
undetectable sponsor changes.

The [GDPR text](https://eur-lex.europa.eu/eli/reg/2016/679/oj) provides relevant rights
context rather than an implementation shortcut: Article 16 includes rectification and
completion by supplementary statement, while Article 89 requires safeguards and data
minimisation for research and permits only law-dependent derogations. Immutability must
therefore not be designed as a claim that participant data can never be corrected,
restricted, or otherwise handled under applicable law.

### Project adaptation

Preserve the provisional AI extraction, append the participant's approve/edit/reject
event, and keep the corrected value separately attributable. At profile freeze, record
approval or a participant-authored correction addendum without erasing the reviewed AI
map. Describe review as participant confirmation/correction of representation, not as
proof of objective truth.

This milestone deliberately stops before a post-freeze supersession workflow. Its
schema declares that later correction requires a new linked version. Erasure,
restriction, retention, and jurisdiction-specific compliance remain governance work;
read-only filesystem permissions must never be represented as overriding legal or
ethical participant rights.

Decision: **compose + adapt**.

## 3. Immutable electronic research records

### Established work

[21 CFR 11.10](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10)
requires controls for authenticity and integrity, accurate copies, protected retrieval,
secure time-stamped audit trails, and changes that do not obscure prior information.
Although this product is not claiming Part 11 applicability or compliance, those are
useful engineering properties.

ICH E6(R3) adds three directly relevant lifecycle rules: workflow actions belong in the
audit trail; dataset-finalization activities before analysis should be confirmed and
documented under prespecified procedures; and retained data plus metadata should be
protected from unauthorized alteration.

The [OSF registration model](https://help.osf.io/article/330-welcome-to-registrations)
demonstrates the research distinction this project needs: a project can continue to
evolve while a time-stamped, read-only registration preserves a particular historical
state. New states do not rewrite the registration.

### Project adaptation

Create a dedicated canonical JSON freeze artifact with exclusive-create semantics and
a digest over exact bytes. Keep the live session and frozen artifact conceptually
separate. Block application-level behavioral mutations after freeze. Retain provider
and participant-review metadata. Treat file permissions as defense in depth; the digest
and refusal to overwrite provide the testable integrity contract.

Decision: **adapt**.

## 4. Reproducible model-evaluation separation

### Established work

The [Center for Open Science preregistration
guidance](https://www.cos.io/initiatives/prereg) states the central problem plainly:
the same data should not be used to generate and test a hypothesis without clearly
distinguishing exploratory from confirmatory work. It recommends frozen plans, held-out
data, and explicit labels for later data-driven analyses.

The [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) calls
for scientific-integrity and construct-validity considerations to be documented,
repeatable testing/evaluation/verification/validation, recorded test sets and metrics,
and independent review where appropriate. [Model Cards for Model
Reporting](https://arxiv.org/abs/1810.03993) likewise separates model documentation and
evaluation procedures from dataset documentation.

### Project adaptation

The immutable behavioral profile is one versioned input object, not a mutable database
query. A future model tournament must create a separate evaluation record bound to the
behavioral-freeze digest plus exact evaluator/model/mapping versions, candidate and
baseline specification, code commit, seeds, and outputs. No model output may write into
or select evidence inside the frozen profile.

The current milestone adds only this boundary contract. It does not add any scorer,
reveal, candidate panel, or result.

Decision: **compose**.

## Changes to the independent conception after the scan

The scan supports the conception with these refinements:

1. Call the participant action confirmation/correction, not validation of truth.
2. Preserve a participant correction as new attributed data and an addendum; never
   overwrite the original AI candidate.
3. Explicitly distinguish immutable research versioning from data-subject rights and
   future governance actions.
4. Record workflow actions and exact UTC times, not only final values.
5. Keep the live participant-owned personal model logically capable of future evolution
   even though this bounded MVP blocks mutation after its first freeze. A later
   supersession design should separate mutable personal state from immutable research
   snapshots more completely.
6. Make downstream evaluation provenance a separate artifact family bound to the
   freeze digest.

## Implementation authorization boundary

This scan supports implementation of the bounded participant-reviewed freeze on PR #24.
It does not authorize merge, deployment, participant recruitment, birth-model scoring,
or claims of compliance with any cited regulation or standard.
