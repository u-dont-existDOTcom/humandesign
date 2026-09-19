# Scenario-first graph index


Text-only reviewed design. Graph links do not create a fixed questionnaire or evidence credit.

## Conversation and preservation


```mermaid
flowchart TD
    read["Read the whole reply"]
    save["Preserve privately; verify or report a save failure"]
    stop["Stop requested?"]
    paused["Remain paused; no next question"]
    separate["Separate answer, correction and process feedback"]
    repair["Resolve process confusion; re-evaluate corrected sources"]
    choose["Choose one useful unanswered distinction"]
    gate["Context and prerequisites established?"]
    other["Skip this route; choose another or pause"]
    ask["Ask one contextualized question"]
    meaning["Retain only source-supported meaning"]
    information["Partial, unknown and declined stay distinct"]
    read -->|""| save
    save -->|"no saved claim without readback"| stop
    stop -->|"yes"| paused
    stop -->|"no"| separate
    separate -->|"when needed"| repair
    repair -->|""| choose
    separate -->|"otherwise"| choose
    choose -->|""| gate
    gate -->|"no"| other
    gate -->|"yes"| ask
    other -->|"another useful route"| choose
    other -->|"nothing useful remains"| paused
    ask -->|"next actual reply"| read
    separate -.->|"answer clauses"| meaning
    meaning -.->|"not a completed-profile score"| information
```

## An invitation and its reason


```mermaid
flowchart TD
    inv["Friend asks for company"]
    act["A reply is given"]
    why["Reason still missing?"]
    open["Ask an open reason question"]
    keep["Keep stated reason; do not re-ask"]
    away["Move to another useful scene"]
    inv -->|""| act
    act -->|"stop always overrides"| why
    why -->|"yes and useful"| open
    why -->|"no"| keep
    open -->|"after an actual explanation"| keep
    keep -->|"no hidden guilt search"| away
```

## A friend asks for company


```mermaid
flowchart TD
    q_A0["A0 · Friend asks for company"]
    q_D0["D0 · Repetitive practice"]
    q_G19["G19 · What matters in a conflict"]
    q_G23["G23 · What you notice"]
    q_M03["M03 · A dull promised task"]
    q_WHY["WHY · Reason for stated action"]
    q_A0 -.->|"related only"| q_WHY
    q_G23 -.->|"related only"| q_WHY
    q_G19 -.->|"related only"| q_WHY
    q_M03 -.->|"related only"| q_WHY
    q_D0 -.->|"related only"| q_WHY
```

## Noticing needs and helping


```mermaid
flowchart TD
    f_D23_noticing["D23.noticing"]
    f_D23_responsibility["D23.responsibility"]
    f_D23_withholding["D23.withholding"]
    q_A0["A0 · Friend asks for company"]
    q_CARE_LIMIT["CARE-LIMIT · Limits on helping"]
    q_CARE_RESPONSIBILITY["CARE-RESPONSIBILITY · Scope of responsibility"]
    q_G23["G23 · What you notice"]
    q_G23 -.->|"may inform"| f_D23_noticing
    q_A0 -->|"possible context"| q_CARE_RESPONSIBILITY
    q_G23 -->|"possible context"| q_CARE_RESPONSIBILITY
    q_CARE_RESPONSIBILITY -.->|"may inform"| f_D23_responsibility
    q_G23 -->|"possible context"| q_CARE_LIMIT
    q_CARE_RESPONSIBILITY -->|"possible context"| q_CARE_LIMIT
    q_CARE_LIMIT -.->|"may inform"| f_D23_withholding
```

## Competing commitments


```mermaid
flowchart TD
    f_D18_competing_values["D18.competing values"]
    f_D18_resolution_durability["D18.resolution durability"]
    q_AFTER_CHOICE["AFTER-CHOICE · Living with the choice"]
    q_G19["G19 · What matters in a conflict"]
    q_G19 -.->|"may inform"| f_D18_competing_values
    q_G19 -->|"possible context"| q_AFTER_CHOICE
    q_AFTER_CHOICE -.->|"may inform"| f_D18_resolution_durability
```

## Explaining and persuading


```mermaid
flowchart TD
    f_D05_audience_adaptation["D05.audience adaptation"]
    f_D05_capacity["D05.capacity"]
    f_D05_preferred_use["D05.preferred use"]
    f_X08_preferred_use["X08.preferred use"]
    q_F0["F0 · What you would say"]
    q_G05["G05 · Self-rated influence"]
    q_M11["M11 · Explain an arrangement"]
    q_PREFER_INFLUENCE["PREFER-INFLUENCE · Wish to persuade"]
    q_F0 -.->|"may inform"| f_D05_audience_adaptation
    q_G05 -.->|"may inform"| f_D05_capacity
    q_F0 -->|"possible context"| q_PREFER_INFLUENCE
    q_G05 -->|"possible context"| q_PREFER_INFLUENCE
    q_M11 -->|"possible context"| q_PREFER_INFLUENCE
    q_PREFER_INFLUENCE -.->|"may inform"| f_D05_preferred_use
    q_PREFER_INFLUENCE -.->|"may inform"| f_X08_preferred_use
```

## Making a practical arrangement


```mermaid
flowchart TD
    f_X08_offer_and_leverage["X08.offer and leverage"]
    q_M11["M11 · Explain an arrangement"]
    q_M11 -.->|"may inform"| f_X08_offer_and_leverage
```

## Joining a group role


```mermaid
flowchart TD
    f_D06_context_difference["D06.context difference"]
    f_D06_entry_signal["D06.entry signal"]
    f_D06_role_leadership["D06.role leadership"]
    q_G06["G06 · Taking a role unasked"]
    q_R02["R02 · Taking a role when asked"]
    q_G06 -.->|"may inform"| f_D06_entry_signal
    q_G06 -->|"possible context"| q_R02
    q_R02 -.->|"may inform"| f_D06_role_leadership
    q_R02 -.->|"may inform"| f_D06_context_difference
```

## How connections begin


```mermaid
flowchart TD
    f_D07_deliberate_pathways["D07.deliberate pathways"]
    f_D07_usual_source["D07.usual source"]
    q_G07["G07 · Usual connection pathway"]
    q_OUTREACH["OUTREACH · Creating a wanted connection"]
    q_G07 -.->|"may inform"| f_D07_usual_source
    q_G07 -->|"possible context"| q_OUTREACH
    q_OUTREACH -.->|"may inform"| f_D07_deliberate_pathways
```

## Other people expect too much


```mermaid
flowchart TD
    f_D08_experience_of_projection["D08.experience of projection"]
    f_D08_mismatch_response["D08.mismatch response"]
    q_G08["G08 · Familiarity with excess demands"]
    q_R03["R03 · Response to excess demands"]
    q_G08 -.->|"may inform"| f_D08_experience_of_projection
    q_G08 -->|"possible context"| q_R03
    q_R03 -.->|"may inform"| f_D08_mismatch_response
```

## Ability and learning


```mermaid
flowchart TD
    f_X05_ease_and_learning["X05.ease and learning"]
    f_X05_external_recognition["X05.external recognition"]
    q_M07["M07 · How a skill developed"]
    q_M08["M08 · Requests based on ability"]
    q_M07 -.->|"may inform"| f_X05_ease_and_learning
    q_M07 -->|"possible context"| q_M08
    q_M08 -.->|"may inform"| f_X05_external_recognition
```

## Making sense of information


```mermaid
flowchart TD
    f_D01_approach["D01.approach"]
    f_D01_checking_detail["D01.checking detail"]
    f_D02_audience_use["D02.audience use"]
    f_D02_output_form["D02.output form"]
    f_D03_closure_condition["D03.closure condition"]
    f_D03_return_pattern["D03.return pattern"]
    q_G01["G01 · Organize conflicting details"]
    q_G02["G02 · Share an understanding"]
    q_G03["G03 · Unresolved attention"]
    q_R01["R01 · What permits closure"]
    q_VERIFY["VERIFY · Decide what to trust"]
    q_G01 -.->|"may inform"| f_D01_approach
    q_G02 -.->|"may inform"| f_D02_output_form
    q_G02 -.->|"may inform"| f_D02_audience_use
    q_G03 -.->|"may inform"| f_D03_return_pattern
    q_G03 -->|"possible context"| q_R01
    q_R01 -.->|"may inform"| f_D03_closure_condition
    q_G01 -->|"possible context"| q_VERIFY
    q_VERIFY -.->|"may inform"| f_D01_checking_detail
```

## Following or changing a method


```mermaid
flowchart TD
    f_D04_change_threshold["D04.change threshold"]
    f_D04_use_existing["D04.use existing"]
    q_G04["G04 · A failed guide step"]
    q_WORKING_METHOD["WORKING-METHOD · A guide that works"]
    q_G04 -.->|"may inform"| f_D04_use_existing
    q_G04 -->|"possible context"| q_WORKING_METHOD
    q_WORKING_METHOD -.->|"may inform"| f_D04_change_threshold
```

## Practice and concentration


```mermaid
flowchart TD
    f_D22_focus_depth_interruptions["D22.focus depth interruptions"]
    f_D22_repetition_value["D22.repetition value"]
    q_D0["D0 · Repetitive practice"]
    q_FOCUS_DEPTH["FOCUS-DEPTH · Uninterrupted concentration"]
    q_G22["G22 · Concentration after interruption"]
    q_PRACTICE_REASON["PRACTICE-REASON · Value of practising"]
    q_G22 -.->|"may inform"| f_D22_focus_depth_interruptions
    q_D0 -->|"possible context"| q_PRACTICE_REASON
    q_PRACTICE_REASON -.->|"may inform"| f_D22_repetition_value
    q_G22 -->|"possible context"| q_FOCUS_DEPTH
    q_FOCUS_DEPTH -.->|"may inform"| f_D22_focus_depth_interruptions
```

## Making a choice


```mermaid
flowchart TD
    f_D09_clarity_over_time["D09.clarity over time"]
    f_D09_override_state["D09.override state"]
    f_D09_presence_form["D09.presence form"]
    f_D09_repeatability_trust["D09.repeatability trust"]
    f_X07_fleeting_or_repeating["X07.fleeting or repeating"]
    q_CHOICE_TIME["CHOICE-TIME · Clarity over time"]
    q_E0["E0 · Next step in a choice"]
    q_G09["G09 · Early bodily response"]
    q_M10["M10 · Within-choice time course"]
    q_R04["R04 · Perceived usefulness"]
    q_SIGNAL_DEPENDABILITY["SIGNAL-DEPENDABILITY · Occurrence across choices"]
    q_SIGNAL_NOT_FOLLOWED["SIGNAL-NOT-FOLLOWED · When a cue is set aside"]
    q_E0 -->|"possible context"| q_G09
    q_G09 -.->|"may inform"| f_D09_presence_form
    q_G09 -->|"possible context"| q_R04
    q_R04 -.->|"may inform"| f_D09_repeatability_trust
    q_G09 -->|"possible context"| q_M10
    q_M10 -.->|"may inform"| f_X07_fleeting_or_repeating
    q_E0 -->|"possible context"| q_CHOICE_TIME
    q_CHOICE_TIME -.->|"may inform"| f_D09_clarity_over_time
    q_G09 -->|"possible context"| q_SIGNAL_DEPENDABILITY
    q_SIGNAL_DEPENDABILITY -.->|"may inform"| f_D09_repeatability_trust
    q_G09 -->|"possible context"| q_SIGNAL_NOT_FOLLOWED
    q_SIGNAL_NOT_FOLLOWED -.->|"may inform"| f_D09_override_state
```

## Noticing a possible problem


```mermaid
flowchart TD
    f_X04_context_and_limits["X04.context and limits"]
    f_X04_cue_form["X04.cue form"]
    q_M05["M05 · Noticing a warning cue"]
    q_M06["M06 · Reliance in unfamiliar contexts"]
    q_M05 -.->|"may inform"| f_X04_cue_form
    q_M05 -->|"possible context"| q_M06
    q_M06 -.->|"may inform"| f_X04_context_and_limits
```

## Adapting to a group


```mermaid
flowchart TD
    f_D10_external_adaptation["D10.external adaptation"]
    f_D10_stable_direction["D10.stable direction"]
    q_ADAPTATION["ADAPTATION · Acceptable changes"]
    q_G10["G10 · Response to external schedule"]
    q_G10 -.->|"may inform"| f_D10_stable_direction
    q_G10 -.->|"may inform"| f_D10_external_adaptation
    q_G10 -->|"possible context"| q_ADAPTATION
    q_ADAPTATION -.->|"may inform"| f_D10_external_adaptation
```

## Money, recognition and ownership


```mermaid
flowchart TD
    f_D19_resources_purpose["D19.resources purpose"]
    f_D19_status_ownership["D19.status ownership"]
    q_G20["G20 · Purpose of spare money"]
    q_OWNERSHIP["OWNERSHIP · Value of ownership"]
    q_STATUS["STATUS · Value of recognition"]
    q_G20 -.->|"may inform"| f_D19_resources_purpose
    q_G20 -.->|"related only"| q_STATUS
    q_STATUS -.->|"may inform"| f_D19_status_ownership
    q_G20 -.->|"related only"| q_OWNERSHIP
    q_OWNERSHIP -.->|"may inform"| f_D19_status_ownership
```

## Following through on a promise


```mermaid
flowchart TD
    f_X03_follow_through["X03.follow through"]
    f_X03_will_vs_available_energy["X03.will vs available energy"]
    q_M03["M03 · A dull promised task"]
    q_M04["M04 · Intention when tired"]
    q_M03 -.->|"may inform"| f_X03_follow_through
    q_M03 -->|"possible context"| q_M04
    q_M04 -.->|"may inform"| f_X03_will_vs_available_energy
```

## Routine and change


```mermaid
flowchart TD
    f_D21_novelty_disruption["D21.novelty disruption"]
    f_D21_ordinary_rhythm["D21.ordinary rhythm"]
    f_X06_change_condition["X06.change condition"]
    f_X06_preserved_value["X06.preserved value"]
    q_C0["C0 · Reaction to cancellation"]
    q_G21["G21 · Shape of a free day"]
    q_M09["M09 · Keep or change a system"]
    q_ROUTINE_CHANGE["ROUTINE-CHANGE · Familiar versus new"]
    q_G21 -.->|"may inform"| f_D21_ordinary_rhythm
    q_M09 -.->|"may inform"| f_X06_preserved_value
    q_M09 -.->|"may inform"| f_X06_change_condition
    q_G21 -.->|"related only"| q_ROUTINE_CHANGE
    q_ROUTINE_CHANGE -.->|"may inform"| f_D21_novelty_disruption
```

## Room and surroundings


```mermaid
flowchart TD
    f_D11_conditions["D11.conditions"]
    f_D11_functional_effect["D11.functional effect"]
    q_G11["G11 · Room conditions noticed"]
    q_ROOM_EFFECT["ROOM-EFFECT · Effect of the condition"]
    q_G11 -.->|"may inform"| f_D11_conditions
    q_G11 -->|"possible context"| q_ROOM_EFFECT
    q_ROOM_EFFECT -.->|"may inform"| f_D11_functional_effect
```

## Romantic connection


```mermaid
flowchart TD
    f_D12_attraction["D12.attraction"]
    f_D12_deepening["D12.deepening"]
    f_D12_sensuality["D12.sensuality"]
    f_D12_weakening_boundaries["D12.weakening boundaries"]
    q_G12["G12 · What starts attraction"]
    q_G13["G13 · What deepens closeness"]
    q_PHYSICAL_CLOSENESS["PHYSICAL-CLOSENESS · Physical affection"]
    q_R05["R05 · More contact"]
    q_ROMANCE_FADE["ROMANCE-FADE · What weakens closeness"]
    q_G12 -.->|"may inform"| f_D12_attraction
    q_G13 -.->|"may inform"| f_D12_deepening
    q_R05 -.->|"may inform"| f_D12_weakening_boundaries
    q_G13 -->|"possible context"| q_PHYSICAL_CLOSENESS
    q_PHYSICAL_CLOSENESS -.->|"may inform"| f_D12_sensuality
    q_G13 -->|"possible context"| q_ROMANCE_FADE
    q_ROMANCE_FADE -.->|"may inform"| f_D12_weakening_boundaries
```

## Mood alone and with others


```mermaid
flowchart TD
    f_D13_conflict_effect["D13.conflict effect"]
    f_D13_others_effect["D13.others effect"]
    f_D13_recovery["D13.recovery"]
    f_D13_solo_baseline["D13.solo baseline"]
    q_B0["B0 · Response to another’s worry"]
    q_G14["G14 · Mood when alone"]
    q_MOOD_AFTER["MOOD-AFTER · Emotional aftermath"]
    q_R06["R06 · Mood during disagreement"]
    q_G14 -.->|"may inform"| f_D13_solo_baseline
    q_B0 -.->|"may inform"| f_D13_others_effect
    q_R06 -.->|"may inform"| f_D13_conflict_effect
    q_B0 -->|"possible context"| q_MOOD_AFTER
    q_R06 -->|"possible context"| q_MOOD_AFTER
    q_MOOD_AFTER -.->|"may inform"| f_D13_recovery
```

## External pressure to hurry


```mermaid
flowchart TD
    f_X02_after_pressure_removed["X02.after pressure removed"]
    f_X02_under_pressure["X02.under pressure"]
    q_M01["M01 · Internal urgency"]
    q_M02["M02 · After pressure stops"]
    q_M01 -.->|"may inform"| f_X02_under_pressure
    q_M01 -->|"possible context"| q_M02
    q_M02 -.->|"may inform"| f_X02_after_pressure_removed
```

## Workload and energy


```mermaid
flowchart TD
    f_D14_burst["D14.burst"]
    f_D14_ordinary_engagement["D14.ordinary engagement"]
    f_D14_prolonged_overload["D14.prolonged overload"]
    f_D14_stopping_recovery["D14.stopping recovery"]
    q_G15["G15 · Ordinary-work energy"]
    q_R07["R07 · Energy after a burst"]
    q_R08["R08 · Energy after prolonged overload"]
    q_R09["R09 · Stopping cues"]
    q_WORK_RECOVERY["WORK-RECOVERY · Energy after stopping"]
    q_G15 -.->|"may inform"| f_D14_ordinary_engagement
    q_G15 -->|"possible context"| q_R07
    q_R07 -.->|"may inform"| f_D14_burst
    q_G15 -->|"possible context"| q_R08
    q_R08 -.->|"may inform"| f_D14_prolonged_overload
    q_G15 -->|"possible context"| q_R09
    q_R07 -->|"possible context"| q_R09
    q_R08 -->|"possible context"| q_R09
    q_R09 -.->|"may inform"| f_D14_stopping_recovery
    q_G15 -->|"possible context"| q_WORK_RECOVERY
    q_R07 -->|"possible context"| q_WORK_RECOVERY
    q_R08 -->|"possible context"| q_WORK_RECOVERY
    q_WORK_RECOVERY -.->|"may inform"| f_D14_stopping_recovery
```

## Effort worth making


```mermaid
flowchart TD
    f_D15_continue_disengage["D15.continue disengage"]
    f_D15_mobilizer["D15.mobilizer"]
    q_G16["G16 · What makes effort worthwhile"]
    q_R10["R10 · When to disengage"]
    q_G16 -.->|"may inform"| f_D15_mobilizer
    q_G16 -->|"possible context"| q_R10
    q_R10 -.->|"may inform"| f_D15_continue_disengage
```

## Time away and re-entry


```mermaid
flowchart TD
    f_D17_reentry["D17.reentry"]
    f_D17_withdrawal_need_activity["D17.withdrawal need activity"]
    q_G18["G18 · After a social day"]
    q_R11["R11 · Readiness to re-engage"]
    q_G18 -.->|"may inform"| f_D17_withdrawal_need_activity
    q_G18 -->|"possible context"| q_R11
    q_R11 -.->|"may inform"| f_D17_reentry
```

## Earlier and current responses


```mermaid
flowchart TD
    f_D20_continuity["D20.continuity"]
    f_D20_learned_management["D20.learned management"]
    f_D20_phases["D20.phases"]
    q_A0["A0 · Friend asks for company"]
    q_G24["G24 · Earlier-life response"]
    q_LIFE_PHASE["LIFE-PHASE · When change emerged"]
    q_R12["R12 · Attributed contributors"]
    q_A0 -->|"possible context"| q_G24
    q_G24 -.->|"may inform"| f_D20_continuity
    q_G24 -->|"possible context"| q_R12
    q_LIFE_PHASE -->|"possible context"| q_R12
    q_R12 -.->|"may inform"| f_D20_learned_management
    q_G24 -->|"possible context"| q_LIFE_PHASE
    q_LIFE_PHASE -.->|"may inform"| f_D20_phases
```

## Pointing out a mistake


```mermaid
flowchart TD
    f_D16_challenge_threshold["D16.challenge threshold"]
    f_D16_context_cost["D16.context cost"]
    q_CORRECTION_REASON["CORRECTION-REASON · When correction matters"]
    q_G17["G17 · Response to an error"]
    q_G17 -.->|"may inform"| f_D16_challenge_threshold
    q_G17 -->|"possible context"| q_CORRECTION_REASON
    q_CORRECTION_REASON -.->|"may inform"| f_D16_context_cost
    q_CORRECTION_REASON -.->|"may inform"| f_D16_challenge_threshold
```

## Trust and reliability


```mermaid
flowchart TD
    f_X01_repair_access["X01.repair access"]
    f_X01_trust_change["X01.trust change"]
    q_G25["G25 · Trust after missed commitments"]
    q_R13["R13 · Future reliance"]
    q_G25 -.->|"may inform"| f_X01_trust_change
    q_G25 -->|"possible context"| q_R13
    q_R13 -.->|"may inform"| f_X01_repair_access
```
