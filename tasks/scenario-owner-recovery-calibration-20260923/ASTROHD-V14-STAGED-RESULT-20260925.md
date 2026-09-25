# V1.4 cross-rulebook development: staged results

Date: 2026-09-25. Classification: target-aware, single-owner development; not independent human validation.

## Owner outcome and actual method

Fit one combined model from pre-existing astrology rules to recover the recorded birth-date/time neighborhood. Do not require each tradition to succeed independently. Do not introduce fitted numerical astrology weights. Test raw and lineage-deduplicated stacking. Increase candidate timestamp panels from 100 to 1,000 and onward; record the previous frozen model before refitting.

The implemented library contains 390 operational rule instances, or 361 after the declared lineage-equivalence grouping, across Lilly, Ptolemy, Valens, and Phaladeepika. These are not 390 independent historical predictions. The library is a bounded collection of planetary/significator strength conditions, not the complete natal contents of those books. BPHS contributes to the inherited semantic-source packet, not a separately implemented fifth book in this run.

The behavioral bridge is the existing target-blind source-only consensus map. Rule eligibility uses supported owner behavioral domains. No new behavioral meanings were chosen after the V1.4 results. Binary subset selection is intentionally target-aware. Source grounding establishes historical provenance, not scientific truth of the behavioral bridge.

## Staged execution

| Panel / stage | What happened |
|---|---|
| 100 timestamps | Four-rule mixed-book models found in both arms. The target tied only with three deliberately included nearby times on the same date. |
| 1,000 timestamps | Both frozen four-rule models retained the same result without refitting. |
| 10,000 timestamps | The old raw model gained one off-date tie; the old deduplicated model gained five. New four-rule fits removed those false matches. |
| 100,000 timestamps | The frozen raw model gained a 1956 off-date tie. The deduplicated four-rule model did not. An explicit revision adopted that already eligible four-rule subset in both arms; the original raw failure remains preserved. |
| 52,596,001-minute century screen | The four-rule model tied on 632 minute instants across 49 UTC dates, including the recorded date. This was not accepted as unique date recovery. |
| Direct repair of all 632 discovered maxima | Two additional existing equal-vote rules eliminated all off-date matches. Both arms selected the same six rules. Nine minute instants remained, all on 1985-01-29. |

The 100/1,000/etc. counts refer to candidate timestamps for one person, not independent participants. Forced hard negatives, same-date times, near dates, and seeded century-random instants are included. Larger nested panels preserve smaller ones. V1.4b is a declared development replay after the initial V1.4a experiment, not a fresh untouched candidate test.

## Final six-rule model

Every selected condition has weight +1 when present. The rules are selected, not continuously reweighted. No preference for proximity to the known date or time is used to break score ties.

1. `lilly/lord:3/house_1_10`
2. `lilly/planet:saturn/benefic_trine`
3. `lilly/planet:venus/house_2_5`
4. `phaladeepika/planet:venus/directional`
5. `lilly/lord:10/benefic_conjunction`
6. `lilly/lord:7/house_4_7_11`

The final two rules were chosen by integer optimization over the existing positive-at-target clauses, while retaining the earlier four. Two additions are certified minimal under that constraint. This is not a proof that six is the globally smallest possible model under every allowed revision.

The maximum possible score is six and the target scores six. A candidate that failed one of the retained four rules cannot reach six by gaining the two new votes. Therefore checking all discovered four-rule maxima is sufficient for this refinement within the screened candidate set; adding millions of easy negatives again would not change that result.

The six selected clauses are nonredundant under the declared lineage scheme, so raw and deduplicated scores coincide. This does not establish that deduplication is generally better, nor that six votes are statistically independent. Source ablations are preserved in the private result.

## Recovered date and time resolution

The only maximum-score date among the discovered century candidates is **1985-01-29**. The surviving minute-grid samples are **10:18 through 10:26 UTC**, including the recorded **10:25 UTC**. All 390 library features, not just the selected six, are identical across those nine samples. Selecting another subset of this unchanged library cannot distinguish those samples.

A cold exact Swiss Ephemeris readback brackets the continuous score plateau from **10:17:51.738282–10:17:51.796875 UTC** at its start to **10:26:12.011719–10:26:12.070313 UTC** at its end. These are computational transition brackets, not evidence that the birth time is accurate to fractions of a second. The model identifies an approximately eight-minute-twenty-second interval, not uniquely 10:25.

The exact recorded instant scores **6**. The persistent **2013-01-28 08:30 UTC** comparator scores **1** under the same six rules.

## Numerical and scientific limits

The century pass screened 52,596,001 minute-grid positions using the verified pre-existing ephemeris cache, one-degree numerical guard allowances, and exact Swiss calculations for 5,392 surviving candidates. It found 632 exact four-rule maxima. A target-independent 512-point coordinate audit found maximum observed longitude error below 0.00035 degrees. The guards are numerical screening allowances, not fitted astrology weights.

A formal global interpolation-error bound has **not** been proved. Therefore the result is one surviving date within the screened century search, not a mathematically certified exhaustive continuous-time uniqueness proof. The local plateau and scored surviving candidates use exact ephemeris calls, with fallback rejection inherited from the chart engine.

The model is fitted to one known owner case. New decoys test search specificity for that case; they do not substitute for unchanged-model testing on new people. Historical provenance and a sparse equal-vote fit are not scientific validation. This limitation qualifies the result and did not veto the authorized development experiment.

## Source audit

Lilly's published strength table supplies the house groups and partile benefic aspects used here: Christian Astrology p.115, reproduced at https://www.skyscript.co.uk/dig5.html. The one-degree partile operationalization follows that reproduction's note 5. It is a declared implementation convention, not a newly fitted orb.

Phaladeepika IV.2 supplies Venus/Moon strength in the fourth house. The source translation and original page image were rechecked: https://www.wisdomlib.org/hinduism/book/phaladeepika-by-mantreswara-text-and-translation/d/doc1621576.html and https://www.wisdomlib.org/uploads/ocr/essays/phaladeepika/phaladeepika-2nd-ed-1950-by-v-subrahmanya-sastri-text/71.jpg. The implementation uses sidereal Lahiri whole-sign houses. The modern behavioral correspondence remains separately attributed to the frozen semantic bridge.

## Durable UDA repair

The observed failure was a change in the object being built: a pooled model became a contest in which whole traditions had to pass independently. A supporting diagnostic was then treated as a stopping point. The verified enforcement gap was that the existing policies and tests did not bind the actual experiment configuration to the owner's permitted method; prose-presence checks could pass while the method was substituted. This does not establish an unobserved internal model mechanism.

A bounded Claude Opus 5.5 review independently examined this failure framing and proposed execution/closure regressions. The repair extends the existing UDA requirement-accretion pattern rather than creating another supervisor. It preserves composition, fitting permission, prohibited weights, requested arms and parent completion scope at actual launch. Evidence limitations qualify claims rather than prohibit authorized fitting.

The repair is merged on UDA's default branch via **PR #253**, merge commit `91e4be060ca99151264f1f90ad4f9c19aaf05bcb`: https://github.com/u-dont-existDOTcom/universal-dev-architecture/pull/253. The final local UDA suite passed **446 tests**; the comparator has **13 behavioral tests**. Temporarily disabling the comparator in memory caused **9 test failures**, with no production source modification. Hosted deterministic audit, Mission Control application, relay and CodeQL checks passed on the merged change's reviewed head.

The research launchers call `owner_method_admission.py` on their runnable configuration. The affected V1.4 fitting, tie-resolution, combination and launch-regression suite passed **12 tests**. This is durable policy plus a tested consumer binding, not a guarantee that every future model/session can never violate the goal.

## Evidence identities and data boundary

Private answer transcripts, participant coding, source-filtered inventories and full candidate matrices remain outside Git. The following SHA-256 values identify private execution artifacts without publishing their contents:

| Artifact | SHA-256 |
|---|---|
| Mixed-book staged run, V1.4b | `2108dc03d1d0ccc3e1174715b8ee687b3978467de592ea44a232f0ed936c3a96` |
| 100,000-candidate repair, V1.4c | `e221649466f509b4a3a612b05e023b94b6038b0fc7c46ca9cb8ad82de05491aa` |
| Four-rule century screen | `0f7eb82f84e9b8dcbd068f03a822a073490948708432ebbac351df67f8e2ed6a` |
| Six-rule survivor repair, V1.4d | `aeb9bffc5e6a40884aa4bb2b4080ebf8b2c9771188dbbb7a2501d9428d20da8b` |
| Cold exact direct/time readback | `250f79ed74089e0db8ff466238db2674c9acbaa42f5c125efd1e1816f18dd7cc` |
| Claude UDA-method review | `7deea926d1556271a874ea09331be9d6a5d18a9e7d56eda80e9863a722d26434` |

## Completion boundary

The requested UDA repair, workflow re-examination, staged fitting and executed search are complete at the stated owner-development boundary. The recovered date and honest unresolved time interval are direct results, not a diagnostic proxy. The broader research project remains open: no new-person validity, exact-minute recovery or formally exhaustive continuous-time uniqueness is claimed. Do not silently restore the superseded whole-tradition-success gate or forbid further explicitly versioned owner development.

## Independent replay of the saved model

The public model manifest has SHA-256 `4bd0b02cc099142f932cc608e821d5db6539e1ec88a67c1d4f93f638d4cc0e83`. `scripts/score_astrohd_v14_model.py` loads only that manifest, generic source-map data and ephemeris files; it does not load private answers or consult the target date to compute a score. A separate process reproduced scores 6 at recorded 10:25, 1 at the 2013 comparator, 6 at 10:24 and 5 at 10:27.

In the project's Python environment, with `EPHEMERIS_ROOT` pointing to the verified local Swiss files:

```sh
PYTHONPATH=src python scripts/score_astrohd_v14_model.py \
  --ephemeris-root "$EPHEMERIS_ROOT" \
  --when 1985-01-29T10:25:00Z \
  --when 2013-01-28T08:30:00Z
```

The saved historical conception and initial method contract are provenance, not current restrictions on development. The current contract distinguishes normalized goal text from the exact owner request.
