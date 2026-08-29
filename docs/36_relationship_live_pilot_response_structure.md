# 36 — Relationship live-pilot response structure correction

Status: participant-UX and measurement correction after the first live capture-safe pilot. This does not alter the frozen AstroRRF relationship model or retroactively change any frozen participant response.

## Observed failure mode

The first live pilot rendered each broad relationship domain as:

- one long compound prompt;
- several additional probes;
- one free-text answer box.

That structure was technically narrative-first but behaviorally unrealistic. A respondent can answer the most salient part of a prompt while silently omitting several other requested distinctions. The absence of an answer to one embedded subquestion is then indistinguishable from an intentional `unknown`, a forgotten item, an implicit answer, or simple survey fatigue.

The same pilot also reached freeze without an explicit mechanism for the respondent to mark and clarify mixed or context-dependent answers.

## Permanent design rule

A participant-facing response control must correspond to a narrow answerable unit.

Do not present a hidden checklist of independent constructs above one textarea when those constructs matter separately to scoring/classification.

Broad domains may remain as navigation/progress groups, but the answer surface must provide separate labeled response fields for the distinctions the model intends to preserve.

## Guided-fields correction

The public pilot now uses:

`reference/relationship/relationship_guided_response_fields_v1.json`

The six core domains remain:

1. relationship timeline/context;
2. love/attraction/Eros;
3. sexual system;
4. mind/communication;
5. emotional climate/autonomy;
6. practical future fit.

They are rendered as 24 narrower fields rather than six compound textareas.

Each field requires one explicit status:

- `clear`;
- `mixed`;
- `context_dependent`;
- `unknown`;
- `not_applicable`.

`clear`, `mixed`, and `context_dependent` require narrative evidence. `mixed` and `context_dependent` additionally require a field-specific clarification response. `unknown` remains a valid unknown rather than being converted to moderate/neutral.

## Review-before-freeze rule

Before freeze, the participant must be shown:

- every field response;
- every uncertainty/status marker;
- the count of fields still marked mixed/context-dependent;
- the count of genuinely unknown fields;
- an edit path for every section.

A mixed/context-dependent field cannot freeze without its required clarification text. Unknown fields may freeze as unknown.

## Legacy frozen sessions

A response that was already frozen under the original single-textarea pilot must remain immutable.

Do not edit or replace its original freeze receipt.

Instead, the same private session may create a separately frozen **guided clarification addendum**. The addendum:

- references the original freeze hash;
- uses the current guided-field schema;
- receives its own freeze hash;
- is treated as later clarification, not as if it existed before the original freeze.

This permits early pilot data to be repaired for development use without falsifying provenance.

## Remaining semantic-ambiguity layer

Guided fields solve omission and self-identified ambiguity. They do **not** guarantee that prose marked `clear` is semantically unambiguous to the blind phenotype classifier.

The later blind-classifier integration must therefore be allowed to return unresolved axes and request targeted adaptive follow-ups before final phenotype freeze/reveal. Those semantic follow-up/retry thresholds remain downstream of the Survey-v2 noise audit and relationship-specific reliability testing.

## Regression criterion

Future participant UIs fail this requirement if a respondent is again expected to answer materially independent scored constructs inside one undifferentiated text box without separate response controls or explicit uncertainty handling.
