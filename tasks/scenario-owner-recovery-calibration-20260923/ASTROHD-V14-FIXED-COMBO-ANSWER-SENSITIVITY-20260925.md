# V1.4d fixed-combination answer-sensitivity diagnostic

Date: 2026-09-25. Scope: explanation and source/code inspection only. No new combinations, changes to answers, source mappings, numerical weights, or century calculations were performed.

## Current owner request

Before trying other rule combinations or a further full-century calculation, identify which questionnaire questions or answer changes could make the recorded instant rank uniquely first under the current six-rule combination. Preserve this ordering; the current request is not permission to launch another optimization before answering.

## Finding

There is no such answer-change set under the fixed six-rule model. The recorded date already ranks first among the dates containing discovered maximum-score candidates. The recorded minute shares the maximum with nearby times on that same date. A rank interval of 1–9 means nine tied maximum-scoring minute samples, not eight higher-scoring candidates or dates.

The previous exact readback reports score 6 at the recorded instant, score 1 at the persistent 2013 comparator, and the same six-feature vector at the nine samples from 10:18 through 10:26 UTC on 1985-01-29. The continuous local maximum is approximately 10:17:52–10:26:12 UTC. Existing evidence is in `ASTROHD-V14-STAGED-RESULT-20260925.md` and its private direct-readback hash; this diagnostic did not recompute astronomy.

## Actual answer-to-score dependency

Inspection of `scripts/score_astrohd_v14_model.py` shows that the fixed-model scorer loads the saved six rule IDs, a generic source map, and chart coordinates computed from candidate time and place. It does not load a participant questionnaire or behavioral confidence values. The selected IDs are fixed in the manifest.

In the preceding development stage, measured behavior determined which source-linked significators were eligible; target-aware optimization selected a subset. Once that subset is held fixed, editing an answer is not an input operation implemented by this scorer. It therefore cannot raise 10:25 above an otherwise identical candidate.

Even a hypothetical extension that allowed answers to activate, reverse, or reweight the same six predicates would not solve the local tie. Let phi(t) be the six rule outcomes and a be any answer vector. For any deterministic scoring function depending only on those inputs, phi(t)=phi(u) implies F(a,phi(t))=F(a,phi(u)). The reported tied samples have phi=(1,1,1,1,1,1). This is a representational limitation, not evidence that a particular interview answer is wrong or insufficiently emphatic.

The prior run additionally found all 390 eligible library features identical across the nine surviving samples. No subset of that unchanged library can separate them either. This statement is limited to the verified samples; it is not a claim that astronomical coordinates themselves stop moving.

## Questionnaire-topic trace for the fixed combination

These are topics in the frozen neutral-domain mapping, not verbatim original questionnaire wording and not proposed replacements for the owner's responses.

| Fixed rule | Neutral topic(s) in the existing mapping |
|---|---|
| `lilly/lord:3/house_1_10` | `insight_translation`: expressing/explaining understanding |
| `lilly/planet:saturn/benefic_trine` | `retreat_privacy`, `work_energy_range`: solitude/privacy and sustained-work capacity/limits |
| `lilly/planet:venus/house_2_5` | `romantic_attachment`: affection, attraction and pair-bonding |
| `phaladeepika/planet:venus/directional` | `persuasion_strategy`, `romantic_attachment`: persuasive communication and attachment |
| `lilly/lord:10/benefic_conjunction` | `recognition_entry`: entry into roles through recognition/appointment |
| `lilly/lord:7/house_4_7_11` | `romantic_attachment`: partners/pair-bonding |

Source: `ASTROHD-V13-TARGET-BLIND-CONSENSUS-MAP-20260924.json`, registry construction in `src/hdmatch/evaluation/astrohd_v14_rules.py`, and the six-rule manifest. The bridge is a modern interpretation of source significators, not six verbatim historical personality questions. Changing responses in those domains could change eligibility during a newly declared model revision; that is different from changing the rank under this fixed combination.

## Historical clarification about Lilly

It is inaccurate to treat Lilly as exclusively a horary author who did not discuss character. Christian Astrology Book III addresses nativities and includes treatments of temperament, manners and understanding. The current experiment nevertheless uses selected strength/house/aspect clauses with the separately attributed modern behavioral bridge, not an implementation of his complete natal-character method.

Primary-text reproduction consulted: https://archive.org/stream/ChristianAstrologyByWilliamLilly/Lilly_William-Christian_astrology_djvu.txt (Book III, approximately printed pp.531–545; manners and understanding sections). Volume description: https://www.skyscript.co.uk/CA/.

## Scope, evidence and continuation

The earlier century calculation screened the full declared century minute grid and exactly rescored survivors. Its formal global interpolation-error bound was not proved. Thus unique-date recovery remains a claim within the screened search, not certified continuous-time exhaustiveness. This distinction does not alter the impossibility of breaking the already observed identical-feature tie by changing answers alone.

No private response transcripts or coding were accessed or published for this diagnostic. One combined remote inspection command was blocked with an indeterminate platform safety response; it was not retried. Repository code, the existing result receipt and the generic source mapping were sufficient to answer the question. No claim of a new numerical run is made.

UDA activation: live default-branch root read for this turn; current owner-method preservation rule checked at the explanation/persistence boundary. Current user restriction controls: preserve the model and answer the diagnostic before any further combination search or broad execution. This diagnostic is complete. The larger research objective and prospective full-century follow-up remain distinct, and no background work is claimed.
