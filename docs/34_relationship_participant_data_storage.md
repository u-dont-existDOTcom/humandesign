# 34 — Relationship Participant Data Storage

Status: storage/privacy architecture for the relationship questionnaire and automatic-learning track.

## Core rule

The public `humandesign` repository is **not** the storage location for raw participant responses or exact third-party birth records.

The system must separate:

1. **Private participant store** — raw, potentially identifying or intimate data used by the questionnaire, classifier, chart engine, and development learner.
2. **Public research repository** — code, frozen schemas, versioned model definitions, hashes/receipts, de-identified aggregate learning summaries, and public-safe audit artifacts.

This separation is mandatory even when a participant uses an alias.

## Private participant store

Store privately:

- verbatim free-text questionnaire answers;
- exact date/time/place of birth for either partner;
- birth-certificate/source images or metadata;
- real names, email addresses, phone numbers, or contact details;
- resume/session tokens;
- detailed sexual/relationship narratives;
- third-party allegations or sensitive behavioral episodes;
- consent records and deletion/export requests;
- classifier evidence spans that reproduce intimate participant text;
- full per-person chart input packages where those inputs can identify an absent third party.

The questionnaire and automatic-learning pipeline may read these records under the declared study permissions, but they must not be committed to public Git history.

## Public repository

The repo may contain:

- questionnaire/rubric/classifier source files;
- versioned HD/Western/AstroRRF model definitions;
- deterministic chart/relationship-analysis code;
- public-safe pseudonymous case IDs such as `pair_006`;
- source-quality categories such as `birth_certificate_verified` without the exact birth tuple;
- frozen input/response **commitments** produced with a non-public salt/key or another non-enumerable binding method;
- model/questionnaire/classifier hashes;
- de-identified axis-level evaluation outcomes where release is ethically appropriate;
- aggregate hit/miss/partial/unresolved statistics;
- learning curves, noise audits, and model-comparison reports;
- V-next revision proposals that contain no raw participant prose;
- public-safe tombstones marking superseded or stale evaluations.

Do not publish a plain unsalted SHA-256 of exact birth date/time/place as a privacy mechanism: the input space is small enough to enumerate.

## Automatic learning flow

The learning system can still use every consenting participant response:

```text
private raw answers + private birth inputs
        ↓
blind narrative classifier
        ↓
private structured phenotype
        ↓
frozen chart/model comparison
        ↓
private case-level evaluation
        ↓
public-safe aggregate learning ledger
        ↓
V-next proposal
```

Case-level raw text is therefore available to the learner without being public.

A development/proposal agent may inspect private development-case text to discover conflated constructs, recurring context moderators, or missing questionnaire distinctions. Its persisted public output must be a structured proposal that removes identifying/raw narrative content.

## Validation separation

For untouched validation participants:

- do not use their responses to modify the model being evaluated;
- seal/freeze their response and prediction packages first;
- evaluate under the frozen model;
- only after that evaluation is closed may their data enter a later development pool if the study consent permits it;
- any resulting revision must become a new model/questionnaire version.

## Recommended hosted-app storage

For the public questionnaire application:

- persistent private database for sessions/responses/consent;
- encryption at rest where supported;
- separate table/namespace for contact data;
- separate researcher-only chart/prediction packages;
- access controls that keep raw records out of public frontend bundles and logs;
- deletion/export by opaque participant/session ID;
- periodic private backups;
- de-identified export job that writes only approved aggregate/public-safe artifacts to the GitHub repo.

A local development SQLite database is acceptable for a pilot if it is excluded from Git and backed up privately. A hosted deployment should use a private managed database rather than a repository file.

## Git safeguards

Before public deployment, add/verify `.gitignore` coverage for at least:

- local questionnaire databases;
- raw response exports;
- consent/contact exports;
- private birth-input files;
- uploaded birth-record images;
- session secrets/tokens;
- private classifier transcripts;
- private learning-case packages.

Automated export code should fail closed if a candidate public artifact contains fields matching the private-data schema.

## Existing development records

Older development commits may predate this stricter separation. Current files should be migrated toward public-safe tombstones or de-identified summaries, and no new exact partner birth records or intimate verbatim narratives should be added to public history.
