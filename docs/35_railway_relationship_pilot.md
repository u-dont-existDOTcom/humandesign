# 35 — Railway Relationship Pilot Deployment

Status: current deployment target for the public relationship questionnaire pilot.

## Decision

The Replit prototype is no longer the deployment target. GitHub remains the canonical source of truth and Railway is the target host.

The initial Railway service runs:

```text
hdmatch.api.relationship_public_app:create_relationship_public_app_from_env
```

This first deployable layer deliberately implements only chart-blind response capture:

- one question per screen;
- the six frozen relationship core anchors in their canonical order;
- pseudonymous session IDs;
- private resume tokens;
- answer persistence outside Git;
- pause/resume;
- participant review;
- immutable response freeze with SHA-256 receipt;
- no astrology/HD prediction leakage during questioning.

It intentionally does **not** yet guess adaptive follow-up routing from keywords. Adaptive follow-ups require the blind classifier to emit unresolved axes and fixed applicability flags. The relationship fingerprint, classifier, automatic-learning export, and post-freeze Astro/HD audit remain subsequent layers.

## Railway service setup

Create a Railway project from the GitHub repository `u-dont-existDOTcom/humandesign` and deploy the repository root. `railway.json` supplies the build and start commands.

Attach a persistent Railway Volume mounted at:

```text
/data
```

Set this required environment variable:

```text
HDMATCH_RELATIONSHIP_STORE=/data/relationship_sessions
```

Optional override:

```text
HDMATCH_RELATIONSHIP_QUESTIONNAIRE=reference/relationship/relationship_dynamic_questionnaire_v1.json
```

The service fails closed if `HDMATCH_RELATIONSHIP_STORE` is missing. This is intentional: raw participant narratives must never silently fall back to Git or an unspecified local path.

## Health check

Railway should use:

```text
/healthz
```

A successful service returns `{"status":"ok"}`.

## Data boundary

The Railway Volume is private operational storage for the pilot. Raw responses, resume tokens, exact birth records, and intimate narratives must not be committed to this public repository.

GitHub may receive only public-safe artifacts defined in `docs/34_relationship_participant_data_storage.md`, such as:

- frozen schemas and model versions;
- questionnaire hashes;
- de-identified phenotype summaries;
- aggregate learning/error statistics;
- V-next proposals;
- audit receipts without intimate raw text.

## Next implementation layers

1. blind narrative classifier producing relationship-axis results, unresolved axes, and fixed applicability flags;
2. adaptive follow-up routing through the existing relationship questionnaire selector;
3. participant-editable review before freeze;
4. personalized non-astrological Relationship Fingerprint;
5. optional private birth-data intake after/alongside the appropriate freeze boundary;
6. post-freeze Astro/HD raw-signal and unresolved reveal, without formal hit/miss
   labels until a separate calibration version exists;
7. de-identified automatic-learning ledger export;
8. authenticated researcher/admin tools;
9. migration from volume-backed JSON to Postgres when recruitment scale or operational requirements justify it.

## Deployment boundary

The repository is Railway-ready after this configuration is merged. Creating the Railway project and attaching the Volume require access to the owner's Railway account; those account-level actions cannot be performed through the current ChatGPT connector set because no Railway connector is available.
