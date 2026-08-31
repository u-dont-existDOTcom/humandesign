# A1/GPT-heavy pre-elicitation independent conception

Date frozen: 2026-08-31

Status: source-free conception prepared before every checkpoint-13 methods query

## Problem

The owner selected one prospective chart-blind human semantic source and requires GPT to perform
most of the work. The architecture must minimize the human's procedural burden without letting GPT
quietly become the source of the meanings that later work is supposed to treat as independently
human-originated.

This creates two simultaneous requirements:

1. preserve the human origin and final authority of every controlling semantic proposition; and
2. automate transcription, organization, provenance, verification, and source-constrained
   derivative work as far as that origin boundary permits.

The current child must solve only the content-free workflow problem. It must not evaluate a real
person, obtain human semantic material, or create content.

## Human origin versus GPT processing

Human origin means that the substantive phenomena, distinctions, meanings, boundaries, and
decisions first come from the designated human source. GPT processing means operations performed
on already-preserved human material without granting GPT final semantic authority.

Some processing is mechanically low-risk: byte preservation, timestamps, hashes, identifiers,
exact quotation, source offsets, and meaning-neutral formatting. Other processing can change
meaning even when it looks clerical: paraphrase, grouping, naming, deduplication, omission,
prioritization, splitting, merging, and contradiction resolution. The architecture must represent
that difference rather than labeling every GPT action as generic assistance.

## Proposed two-freeze model

### Raw human-origin freeze

The original human contribution becomes immutable before any GPT transformation that can alter or
add meaning. A normalized transcript may coexist with the original, but cannot replace it. Any
uncertainty remains linked to the exact source location.

### Clean conception freeze

After permitted source-constrained processing, every controlling unit must link to human-source
evidence and an explicit human decision. Candidate GPT output remains non-authoritative until that
decision. Contradictions and unresolved variants remain visible. Once the human attests fidelity,
the complete package becomes immutable before any later protected use.

The two freezes prevent a polished derivative from erasing where its meaning came from.

## GPT context classes

The workflow appears to require at least three distinct GPT context classes:

1. a governance context that knows the repository and enforces contracts but cannot access
   unsealed content;
2. an isolated adjudication context that receives only a future authorized evidence packet and
   cannot author content; and
3. an isolated content-support context that can operate only on the permitted human-source corpus
   and cannot access protected external semantics.

Context identity, run identity, input packet identity, access history, output commitment, and
authority level must remain separate. A common underlying model must not be represented as several
independent models merely because several runs exist.

## Owner/author dual-role risks

The same human is both project owner and prospective semantic source. That creates risks even if
the person lacks protected-domain interpretation knowledge:

- owner authority could pressure an eligibility or content-custody decision;
- an owner action could be confused with an author semantic decision;
- the person knows the project intends a later comparison and could favor apparently useful
  material;
- one human source provides no cross-author comparison; and
- later revision could silently replace a pre-exposure package.

Candidate controls are distinct owner/author event types, immutable initial evidence and decisions,
no owner override into clean eligibility, fail-closed bypass states, explicit single-author claim
limits, and a freeze that later information cannot overwrite.

## Adjudication-run separation

The owner selected GPT as the adjudicator actor class. A single GPT run creates a single-point
interpretation risk. Candidate architecture therefore represents multiple sealed initial run slots
and a separate reconciliation slot without selecting any model or decision procedure.

Each initial run must be unable to see another run's unsealed output. Every initial decision must
be committed before reconciliation. Reconciliation may add a later record but may not rewrite the
initial decisions or erase disagreement. The architecture must not infer that separate runs remove
shared-model error.

## Provenance and fidelity concerns

The architecture must preserve:

- original-source bytes and identity;
- source locations for extracted material;
- every derivative's immediate and ultimate ancestry;
- transformation type and authority level;
- uncertainty and unresolved conflict;
- the human decision accepting, rejecting, rewriting, or deferring a derivative;
- access events and context class;
- freeze identity and supersession history; and
- proof that protected information was unavailable before the required boundary.

A high-coverage derivative can still be semantically wrong. Mechanical coverage checks and human
fidelity authority must therefore remain distinct.

## Independent candidate mechanisms

Before outside research, the candidate mechanisms are:

1. closed role and context registries with fail-closed permissions;
2. append-only raw-source, derivative, decision, access, and freeze events;
3. a directed source-to-derivative lineage in which every controlling unit reaches an original
   human record;
4. explicit non-authoritative states for every GPT semantic derivative;
5. typed human acceptance receipts that name the exact derivative and source support;
6. a two-freeze state machine that blocks semantic transformation before raw freeze and protected
   access before clean freeze;
7. independent adjudication-run slots with sealed outputs and separate reconciliation;
8. distinct owner and author event types for the same actor;
9. content-custody receipts that expose access without exposing content; and
10. hostile tests that try to create authority without human source, overwrite prior decisions,
    convert similarity into equivalence, or bypass the freeze.

These are independent candidate mechanisms, not selected external methods or evidence of validity.

## Constraints

- The child remains local, reversible, metadata-only, and synthetic-test-only.
- No real person is evaluated or assigned clean access.
- No human-facing question, instruction, or consent language is written.
- No semantic content, construct, instrument, category, or authoritative label is created.
- No specific model, provider, configuration, evidence standard, threshold, or reconciliation rule
  is selected.
- No protected-domain content or later comparison content is created or accessed.
- No production, API, user interface, database, storage, external service, publication, or release
  surface changes.
- Existing accepted artifacts remain immutable.
- The current work establishes architecture completeness only, not scientific validity or real
  workflow readiness.

## Open questions

- Which established approaches best preserve human authorship while allowing extensive automated
  derivative work?
- How can non-leading facilitation be bounded so it refers only to already-originated human
  material?
- Which transformations are reliably mechanical, and which require explicit semantic authority?
- What evidence proves that a derivative is fully source-supported without assuming semantic
  fidelity?
- How should disagreement among sealed GPT runs be represented without manufactured consensus?
- How should shared-model correlation limit claims about independent runs?
- Which dual-role controls are necessary when owner and human source are the same person?
- What minimum custody records prove that protected information was unavailable at each freeze?
- Which failure states must block progression rather than merely create a warning?

## Pre-search attestation

This conception contains no external citation, source, named external method, human-facing prompt,
semantic content example, selected model/provider/version, evidence standard, threshold, real
eligibility judgment, instrument, or later comparison content. It must remain byte-identical after
the checkpoint-13 scan.

