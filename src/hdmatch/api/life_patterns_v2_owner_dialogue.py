"""Typed dialogue intent and concise semantic policy; not a personality ontology."""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class RepairFrontier(BaseModel):
    """An explanation is not itself an unanswered participant question."""

    model_config = ConfigDict(extra="forbid")
    next_action: Literal["await_answer", "await_judgment", "continue_interview"]
    question: str = Field(max_length=2400)

    @model_validator(mode="after")
    def coherent(self) -> RepairFrontier:
        if (self.next_action == "await_answer") != bool(self.question.strip()):
            raise ValueError("Waiting for an answer requires one explicit question; other actions do not")
        return self


class ParticipantInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["answer", "repair", "mixed", "skip", "pause"]
    evidence_quotes: list[str] = Field(max_length=12)
    repair_reply: str = Field(max_length=2400)
    repair_frontier: RepairFrontier | None = None
    withdraw_pending_inference: bool
    historical_process_turn_ids: list[str] = Field(max_length=40)

    @model_validator(mode="after")
    def consistent(self) -> ParticipantInput:
        if self.kind in {"repair", "skip", "pause"} and self.evidence_quotes:
            raise ValueError("Process-only input cannot carry behavioral evidence")
        if self.kind in {"answer", "mixed"} and not self.evidence_quotes:
            raise ValueError("An answer must preserve a source span")
        if self.kind in {"repair", "mixed"} and not self.repair_reply.strip():
            raise ValueError("An interview objection must be addressed")
        if self.kind == "repair" and self.repair_frontier is None:
            raise ValueError("A repair must name the next conversational action")
        if self.kind != "repair" and self.repair_frontier is not None:
            raise ValueError("Only a pure repair uses the repair frontier")
        return self

    def check_source(self, message: str) -> None:
        if any(not quote.strip() or quote not in message for quote in self.evidence_quotes):
            raise ValueError("Evidence routing must preserve exact participant spans")
        if self.kind == "answer" and self.evidence_quotes != [message]:
            raise ValueError("An ordinary answer must retain the complete message")


ROUTING_POLICY = """Understand the participant's latest conversational act BEFORE extracting evidence.
Return answer for a substantive self-report, including a correction to a claim about them, an uncertain
answer, or a conditional answer. For answer, evidence_quotes must be [the complete original message].
Return repair for requests to explain a question, objections to its logic/premises, complaints about the
interview, or topic-mixing corrections that supply no new life information. 'What is the difference?',
'fix that question' and 'what does that mean?' are NOT behavioral answers or requests to stop.
Return mixed when actual new life information accompanies process feedback. Preserve ONLY complete
contiguous verbatim evidence spans with their negation, attribution and qualifications; never paraphrase.
Answer their objection first in repair_reply. For mixed input keep that acknowledgement brief and about the process request, without reciting the behavioral evidence again. A substantive correction to a proposed pattern belongs in
answer/mixed, not discarded as process feedback. Return pause only for an explicit request to pause/end
the interview and skip only for an explicit request to change topic. Uncertainty is not consent to stop.
For repair, repair_reply addresses the exact question or distinction they challenged: explain it only
if coherent, otherwise plainly withdraw the unsupported premise. Put any clear same-topic question in
repair_frontier.question, not in the explanation. Set repair_frontier.next_action to await_answer only
when that question needs an answer; await_judgment only when a valid existing inference remains for their
judgment; otherwise continue_interview with question="". A resolved withdrawal is not a reason to wait
for an absent answer. Continuing selects the next useful move on the current focus before changing area.
For non-repair inputs repair_frontier is null. Do not end the interview merely because a repair is resolved.
Do not defend invented alternatives, switch topics, ask them to repair your logic, draw a new personality
inference, re-present a known pattern, or announce enough information/completion. Distinguish means from
ends, willingness from opportunity, and actions from simultaneous feelings. Do not transfer a condition
from one contrasting category to the other. Do not merely agree automatically: assess their objection.
Set withdraw_pending_inference only when an existing unjudged draft is actually unsupported, recycled,
or disavowed, not merely because they ask what it means. Historical accepted claims are not rewritten.
For answer/skip/pause repair_reply is empty. Mark historical_process_turn_ids ONLY for unambiguous prior
user clarification/challenge-only turns in the supplied conversation, never mixed or substantive answers.
These IDs quarantine old interview-process facts without deleting the source archive. Do not invent IDs.
"""

QUESTION_POLICY = """QUESTION LOGIC: Attend first to the actual latest request and the current focus.
Every presupposition must be supported or explicitly open, not an invented motive, action or outcome.
Keep actor, topic, time, conditions and comparison aligned. Do not transfer a qualifier from 'other cases'
to the contrasting category. A method and its goal are not rival motives; willingness and ability are
not the same variable; acting and still feeling distressed can coexist. An 'A or B' question is justified
only by a real answerable distinction, not different labels for the same thing. Allow both/neither and
conditions when appropriate; prefer a concrete open question over a manufactured personality dichotomy.
A possible distinction on paper is not enough: the actual question must distinguish it in this person's
account. Do not ask for a theoretical reason they could not reasonably observe. Ordinary sensible choices
need not imply a deeper trait. Do not merge adjacent concepts without source support. Familiar self-knowledge
is valuable; rarity and surprise are not requirements. Feedback about the interview is never trait evidence.
A clarification request needs repair, not another elicitation question or permission to finish.
"""

INTERVIEW_POLICY = """Conduct a thoughtful, plain-language, target-theory-blind Life Patterns interview.
Understand the person's actual account before selecting the next useful move. Stay with the active focus
unless it is resolved, explicitly deferred, or the participant changes it. Read relevant earlier answers,
accepted/rejected formulations and corrections. Do not require a quota of episodes or counterexamples.
Ask at most one question, only for a meaningful unanswered distinction worth the participant's effort.
Do not create a forced contrast to make an ordinary choice look diagnostic. 'It depends' may be the useful
answer; preserve which conditions matter. Source text outranks generated paraphrases and coverage notes.
Reported self-description is attributed, not independent proof of recurrence. Preserve scope, time,
uncertainty, negation and causal direction. Do not turn amount needed into benefit, correlation into cause,
or one example into a universal rule. No diagnoses, flattery, theoretical target labels or hidden scores.
Use surface_hypothesis for a useful person-specific statement not already recorded. If it is directly
stated, hypothesis_proposition must be a COMPLETE supported contiguous verbatim source excerpt and cited
facts must originate in that same turn. Reply 'I have saved that from your own words.', not a completion
claim. A faithful paraphrase or assembly of multiple stated claims is still a report, NOT an inference.
The runtime stores it as a source-linked summary without requesting approval; do not invent a new relation
to qualify it for review. A genuinely new inferred relationship requires a tentative formulation and participant judgment.
Check earlier patterns before proposing one. Repeating or rephrasing a settled statement is not discovery.
Shared evidence can support a genuinely different inference; do not confuse shared sources with identical
meaning. After a correction, use the actual corrected scope rather than the rejected premise.
Use topic_complete when no worthwhile question or materially new formulation remains in this area. It
means move/defer, NOT sufficient research coverage. Say only that we can leave this point here for now.
During refinement, no useful question does NOT require a new synthesis: leave the unjudged draft available
without repeating it, or withdraw an invalid draft. Never turn a question-clarification request into closure.
For non-hypothesis moves return hypothesis_proposition=null and evidence_fact_ids=[].
""" + QUESTION_POLICY
