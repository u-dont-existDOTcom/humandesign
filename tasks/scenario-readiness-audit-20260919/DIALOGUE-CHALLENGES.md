# Adversarial dialogue review

All examples below are newly authored design challenges reviewed in the same Chat context. They are not independent respondents, model runs, or estimates of error rates. Each next utterance was inspected for entailment, relevance, single-task burden and context. No example is an owner answer.

## C01 — Bare agreement

Question: You have an hour free and are about to read a book you've been enjoying. A close friend messages: “I'm bored—want to hang out?” They just feel like company; nothing urgent has happened. What would you probably reply?

Fictional reply: Yes, I'd go.

Next utterance: What would make you say yes?

Keep: Would accept in this scene; motive unknown.

Reject: You feel responsible for keeping your friend happy.

Review: Open reason is warranted; neither guilt nor desire has been supplied.

## C02 — Reason already given

Question: You have an hour free and are about to read a book you've been enjoying. A close friend messages: “I'm bored—want to hang out?” They just feel like company; nothing urgent has happened. What would you probably reply?

Fictional reply: Yes, because I enjoy their company. I could read another time.

Next utterance: You have an ordinary day with no fixed appointments and can choose its shape yourself. How would you usually arrange it?

Keep: Anticipated acceptance from enjoyment, with flexible personal plan.

Reject: Would you feel guilty about not going?

Review: Move to a different topic; do not search for obligation behind the stated reason.

## C03 — Negotiated answer, not binary yes

Question: You have an hour free and are about to read a book you've been enjoying. A close friend messages: “I'm bored—want to hang out?” They just feel like company; nothing urgent has happened. What would you probably reply?

Fictional reply: I'd ask them to come over and read beside me.

Next utterance: What would make that arrangement work for you?

Keep: Proposes shared quiet activity; reason remains unspecified.

Reject: What would make you say yes to going out?

Review: Match the actual action; the respondent did not agree to go out.

## C04 — Ambiguous feeling

Question: You have an hour free and are about to read a book you've been enjoying. A close friend messages: “I'm bored—want to hang out?” They just feel like company; nothing urgent has happened. What would you probably reply?

Fictional reply: I'd go because otherwise I'd feel bad.

Next utterance: What does “feel bad” mean for you here?

Keep: Anticipated acceptance and an unresolved feeling phrase.

Reject: So you feel guilty for being selfish.

Review: Clarify the respondent’s phrase without importing a moral or emotional label.

## C05 — Already conditional

Question: You have an hour free and are about to read a book you've been enjoying. A close friend messages: “I'm bored—want to hang out?” They just feel like company; nothing urgent has happened. What would you probably reply?

Fictional reply: If they were lonely I'd go. If they just fancied company, I'd suggest tomorrow.

Next utterance: You have an ordinary day with no fixed appointments and can choose its shape yourself. How would you usually arrange it?

Keep: Two explicit branches by perceived need; no universal yes/no.

Reject: But which response is the real you?

Review: Keep both branches. Do not turn conditionality into contradiction or repeat the conditions question.

## C06 — No help antecedent

Question: You arrive while a few people are getting ready for a shared meal. Nothing has been assigned to you yet. What tends to catch your attention in a situation like this?

Fictional reply: The food, probably.

Next utterance: You are helping arrange a weekend trip. Several people have sent overlapping messages about travel, costs, and timing, and some details disagree. How would you start making sense of it?

Keep: Attention to food; helping and responsibility unreported.

Reject: What would make you leave that help to someone else?

Review: CARE-LIMIT and CARE-RESPONSIBILITY are ineligible without a specified need or helping choice.

## C07 — Specific helping, motive unclear

Question: You arrive while a few people are getting ready for a shared meal. Nothing has been assigned to you yet. What tends to catch your attention in a situation like this?

Fictional reply: I'd notice someone doing all the washing up and go over to help.

Next utterance: What would lead you to help in that situation?

Keep: Notices uneven work and anticipates helping; motive not yet specified.

Reject: You automatically take responsibility for everybody.

Review: First clarify the stated action. A separate obligation probe is only useful if still material afterwards.

## C08 — Motive and boundary already supplied

Question: In that situation, what, if anything, would you feel responsible for?

Earlier context: A shared-meal need and the form of help were already named.

Fictional reply: Only my agreed part. If somebody else had offered to wash up, I would leave it to them.

Next utterance: You are helping arrange a weekend trip. Several people have sent overlapping messages about travel, costs, and timing, and some details disagree. How would you start making sense of it?

Keep: Limited responsibility plus explicit nonintervention condition.

Reject: What would make you leave that help to someone else?

Review: CARE-LIMIT is already answered; a new ID cannot justify re-asking it.

## C09 — No bodily reaction

Question: Return to the cooking-class offer. Before you have weighed it up, what, if anything, would you usually notice in your body?

Earlier context: Cooking-class E0 was presented and remains the active choice.

Fictional reply: Nothing physical that I notice. I'd just compare the times and what they teach.

Next utterance: You join a group whose work interests you. They ask everyone to use a fixed schedule rather than choose their own working times. How would you usually respond?

Keep: No noticed early bodily reaction; a reasoning procedure.

Reject: How useful is that bodily reaction?

Review: Suppress R04, M10, SIGNAL-DEPENDABILITY and SIGNAL-NOT-FOLLOWED. Do not invent no sensation in every part of life.

## C10 — Rich signal answer

Question: Return to the cooking-class offer. Before you have weighed it up, what, if anything, would you usually notice in your body?

Earlier context: Same cooking-class decision; no switch to a new commitment.

Fictional reply: Sometimes a brief tightness. It doesn't repeat during one decision, and I don't trust it when I'm exhausted.

Next utterance: Outside those exhausted periods, how useful is that reaction when you decide?

Keep: Intermittent bodily reaction; within-choice brevity; stated exhaustion limitation. Usefulness outside exhaustion is unresolved.

Reject: What usually happens to that reaction as you keep considering the choice?

Review: Duration and the exhaustion condition are already given. The selected follow-up isolates only usefulness outside that condition; do not repeat either answered part.

## C11 — Unknown is not absent

Question: Return to the cooking-class offer. Before you have weighed it up, what, if anything, would you usually notice in your body?

Earlier context: Cooking-class scene is active.

Fictional reply: I don't know. I haven't paid attention to that.

Next utterance: You join a group whose work interests you. They ask everyone to use a fixed schedule rather than choose their own working times. How would you usually respond?

Keep: Uncertainty about a bodily response, not a report of no response.

Reject: Then you do not receive body signals.

Review: Preserve unknown; move on without repetitions or positive/negative evidence.

## C12 — Decision already made

Question: A nearby group is offering a free cooking class, one evening a week for a month. You like the sound of it, and the time would work for you, but you haven't tried a class with this group before. You need to sign up by tomorrow. What would you probably do next?

Fictional reply: I'd sign up straight away; I could drop it later if it wasn't useful.

Next utterance: You join a group whose work interests you. They ask everyone to use a fixed schedule rather than choose their own working times. How would you usually respond?

Keep: Prompt commitment under reversibility; no ongoing deliberation reported.

Reject: As you keep considering that choice, how does clarity change?

Review: Do not impose continued uncertainty; a body question is not compulsory merely because it remains open.

## C13 — Delayed follow-up has exact referent

Question: After the argument you described earlier, what usually happens to that tension?

Earlier context: R06: respondent reported tension during the accusation. Then G20 was discussed. Next utterance must be: After the argument you described earlier, what usually happens to that tension?

Fictional reply: It tends to last until I stop replaying what was said.

Next utterance: You have an ordinary day with no fixed appointments and can choose its shape yourself. How would you usually arrange it?

Keep: Aftermath of the earlier tense argument, not the later resources discussion.

Reject: How does your feeling about spending money settle?

Review: The delivered wording must name the argument when nonadjacent. The actual question now names the earlier argument; a source note alone would not be enough.

## C14 — No retreat need

Question: A demanding day with people has ended, and nobody needs anything further from you tonight. What would you usually want to do next?

Fictional reply: I'd probably meet another friend. I don't usually need time alone afterwards.

Next utterance: You have an ordinary day with no fixed appointments and can choose its shape yourself. How would you usually arrange it?

Keep: Anticipated further company and explicit lack of usual solitude need after that day.

Reject: What signals that you are ready to re-enter after retreat?

Review: R11 is ineligible; social intensity in the stimulus does not establish withdrawal.

## C15 — Romance declined

Question: You meet someone a few times in an ordinary setting. There is no pressure to date them. What, if anything, usually starts romantic attraction for you?

Fictional reply: I'd rather not discuss romantic relationships.

Next utterance: You have some ordinary time on your own, with no recent argument or exciting news. What would your emotional background usually be like?

Keep: Romance declined; no claim about attraction or attachment.

Reject: What about physical affection with a friend instead?

Review: Respect the closed topic. Alone-time mood can be approached without routing around the refusal.

## C16 — Inapplicable partner, not all relationships

Question: You're having a quiet evening at home and feel fairly settled. Your partner has been worrying for several days about going to a gathering where they won't know many people. Tonight they bring it up again, without asking you to do anything. What, if anything, happens to your own mood?

Fictional reply: I don't have a partner; I'd be able to answer about a close friend.

Next utterance: Using a close friend instead: they keep worrying about an upcoming gathering and are not asking you to do anything. What, if anything, would happen to your own mood?

Keep: User-elects friend context; keep romance unavailable and record the changed role.

Reject: Mark this as romantic emotional permeability.

Review: A role substitution is permitted by the answer and explicitly recorded; it is not a psychometrically equivalent partner answer.

## C17 — Cancelled plans are not novelty resistance

Question: You were looking forward to meeting a friend this afternoon. Shortly before you would leave, they cancel because they have a mild cold. You haven't spent money or rearranged other commitments. What is your first reaction?

Fictional reply: I'd be disappointed because I wanted to see them, but glad to have the afternoon free.

Next utterance: You have an ordinary day with no fixed appointments and can choose its shape yourself. How would you usually arrange it?

Keep: Mixed reaction: missing the friend and welcoming free time.

Reject: You find disruptions to routine difficult.

Review: Keep the actual reasons; use ROUTINE-CHANGE only if novelty choice still matters.

## C18 — Invitation contrast retains task

Question: Consider the same shared-meal scene, except someone asks you to coordinate the work. What would you usually do?

Earlier context: G06 answer: I would start chopping vegetables without waiting.

Fictional reply: I'd coordinate the food but let someone else handle the rest.

Next utterance: You find yourself starting an activity with someone you did not know before. In your own life, how do connections like that usually begin?

Keep: Accepts bounded coordination when asked, compared with the original small-task response.

Reject: An invitation is required for you to act at all.

Review: Compare actual scoped branches; no global rule or causal mechanism.

## C19 — Retrospective change without improvement assumption

Question: Return to the friend-and-book scene. At an earlier stage of your life that you remember reasonably well, what would your usual reply have been?

Earlier context: Current A0 answer is known; retrospective comparison is welcome.

Fictional reply: Earlier I would go even when I didn't want to. Now I'd often offer another time.

Next utterance: What do you think contributed to that change?

Keep: Reported earlier/current difference in the friend scene.

Reject: What healed you so that you can now set boundaries?

Review: Ask attributed contributors without asserting pathology, improvement, treatment or a true original self.

## C20 — Plain correction

Question: You have an hour free and are about to read a book you've been enjoying. A close friend messages: “I'm bored—want to hang out?” They just feel like company; nothing urgent has happened. What would you probably reply?

Fictional reply: Actually, I meant I'd suggest tomorrow, not go now.

Next utterance: What would make you suggest tomorrow?

Keep: Append correction; supersede immediate acceptance and dependent interpretations only. The corrected action has no stated reason yet.

Reject: You are inconsistent about your social priorities.

Review: Explicit correction is not a contradictory trait. Do not seek approval of the corrected paraphrase.

## C21 — Answer plus stop

Question: You have an hour free and are about to read a book you've been enjoying. A close friend messages: “I'm bored—want to hang out?” They just feel like company; nothing urgent has happened. What would you probably reply?

Fictional reply: Probably yes, but let's stop for now.

Next utterance: We’ll stop here.

Keep: Save anticipated acceptance with motive unknown, plus pause; no follow-up.

Reject: What would make you say yes?

Review: Stopping wins over the otherwise useful WHY question. Save status must be reported only after actual write verification.

## C22 — Norm and personal response in one message

Question: You have an hour free and are about to read a book you've been enjoying. A close friend messages: “I'm bored—want to hang out?” They just feel like company; nothing urgent has happened. What would you probably reply?

Fictional reply: People ought to make time for friends, but I'd probably stay home because I wanted to read.

Next utterance: You have an ordinary day with no fixed appointments and can choose its shape yourself. How would you usually arrange it?

Keep: Normative view separate from anticipated personal refusal and reason.

Reject: You always prioritise friends because you believe people should.

Review: Classify clauses separately; do not make the whole message normative or behavioral.

## C23 — Repeated confusion does not complete the profile

Question: While planning a shared meal, someone gives a time that you believe is wrong. Nothing has been booked yet. What would you usually do?

Earlier context: One clarification of the meal time mistake was already given.

Fictional reply: I still can't tell what kind of mistake you're talking about.

Next utterance: You have an ordinary day with no fixed appointments and can choose its shape yourself. How would you usually arrange it?

Keep: Question remains unclear after repair; no correction-threshold evidence.

Reject: We have enough information to finish your profile.

Review: Leave this scene aside and move to a different concrete task; do not call confusion success or silently end the interview.

## C24 — Promise does not imply continued effort

Question: You agreed to prepare something for a shared meal. Finishing it is dull, and nobody is checking on you. What would you usually do?

Fictional reply: I'd probably put it off, and tell them I might not finish.

Next utterance: What would make you put it off?

Keep: Anticipates postponement and communication; motive unresolved.

Reject: What keeps you following through on every promise?

Review: The revised action task admits not continuing; WHY must match the actual action.

## C25 — Deliberate counterfactual preserves earlier no

Question: For this version, suppose you chose to join the project and have put a month into it, but progress is poor. What would make you stop investing in it?

Earlier context: G16 answer was no. R10 explicitly introduced a different imagined participation premise.

Fictional reply: If I had joined, I'd stay only while there was a useful next step.

Next utterance: You have an ordinary day with no fixed appointments and can choose its shape yourself. How would you usually arrange it?

Keep: Conditional hypothetical persistence after a clearly stipulated participation.

Reject: You spent a month restoring the space.

Review: A knowingly imagined contrast is allowed; never back-fill an actual decision or event.

## C26 — Stable signal absence does not close generic clarity

Question: As you keep considering that choice, what, if anything, usually changes in how clear it feels?

Earlier context: E0 decision is still under consideration; G09 reported no sensation.

Fictional reply: Even with no body sensation, I usually become clearer once I understand the timetable.

Next utterance: You join a group whose work interests you. They ask everyone to use a fixed schedule rather than choose their own working times. How would you usually respond?

Keep: Clarity through information without a reported bodily signal.

Reject: No bodily signal means there is no decision process to ask about.

Review: General clarity is independent of signal-specific follow-ups.

## C27 — Context added by respondent

Question: Suppose a tool you find useful is reliably available whenever you need it, but it belongs to someone else. What, if anything, would make owning it yourself matter?

Fictional reply: If there were restrictions on lending it to others, I'd want my own.

Next utterance: You have an ordinary day with no fixed appointments and can choose its shape yourself. How would you usually arrange it?

Keep: Ownership motive conditional on a respondent-added access restriction.

Reject: You need ownership for status.

Review: Store the condition and its origin; it is neither supplied fact nor a status motive.

## C28 — Pressure without action change

Question: You are handling a manageable task when someone nearby starts urging you to hurry, although the actual deadline has not changed. What would usually happen inside you?

Fictional reply: I'd feel rushed but keep doing it at the same pace.

Next utterance: That person leaves and the pressure to hurry stops; the task and deadline stay the same. What would usually change for you?

Keep: Internal urgency without reported speed change.

Reject: You speed up whenever someone pressures you.

Review: Aftermath can be asked in the same task; action and internal reaction remain distinct.

## C29 — Affection is not desire

Question: In that relationship, what place, if any, would physical affection have for you?

Fictional reply: I like cuddling, but I'd rather not talk about sex.

Next utterance: You have some ordinary time on your own, with no recent argument or exciting news. What would your emotional background usually be like?

Keep: Affection preference recorded; sexual topic declined.

Reject: Your sexual desire is high.

Review: Keep private scope; do not substitute affection for desire or ask another sexual probe.

## C30 — Uncertainty plus usable condition

Question: You have an ordinary day with no fixed appointments and can choose its shape yourself. How would you usually arrange it?

Fictional reply: I'm not sure overall; when I'm rested I like leaving the day open.

Next utterance: You will be using an unfamiliar room for work or a quiet activity for a week. What would you pay attention to before settling in?

Keep: Qualified preference under rest; general rhythm unknown.

Reject: No usable information because the answer began I am not sure.

Review: Preserve the explicit condition without promoting it to an overall preference.

## C31 — No identified skill

Question: Choose a familiar activity that you do reasonably well. How did you come to be good at it?

Fictional reply: Nothing comes to mind.

Next utterance: You are helping arrange a weekend trip. Several people have sent overlapping messages about travel, costs, and timing, and some details disagree. How would you start making sense of it?

Keep: No named activity; skill history unassessed.

Reject: What do people ask you to do because of that ability?

Review: M08 is ineligible. Do not transform retrieval difficulty into absence of talent.

## C32 — Refusal with enough information

Question: A close friend has twice agreed to help you with a practical task, then not turned up and explained only afterwards. What difference, if any, would that usually make to your trust?

Fictional reply: I'd rely on them less for tasks, and I don't want to talk about repairing it.

Next utterance: You have an ordinary day with no fixed appointments and can choose its shape yourself. How would you usually arrange it?

Keep: Task reliability reduced; repair topic closed.

Reject: What could make you trust them again?

Review: Retain the answered part and respect refusal of the rest; do not erase trust evidence or reopen repair.

