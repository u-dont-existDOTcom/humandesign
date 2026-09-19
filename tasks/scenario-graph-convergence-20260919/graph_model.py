"""Small, explicit-state model of the design's admission rules.

This is an AUDIT model, not an NLP classifier or a deployed interviewer.
The caller supplies reviewed annotations and an exact source binding. A false
annotation can still produce a false admission; test results do not remove that
boundary. Nothing in this module saves a participant answer or makes model calls.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Binding:
    event_id: str
    question_id: str
    context_key: str
    active: bool = True
    semantic_match: bool = True
    is_participant_source: bool = True
    topic: str = ""

@dataclass
class State:
    context_key: str = 'scene-1/current/selected-role'
    paused: bool = False
    closed_topics: set[str] = field(default_factory=set)
    applicable: bool = True
    imagined_explicitly_elected: bool = False
    useful_missing_distinction: bool = True
    already_answered: bool = False
    repeated_unresolved_probe: bool = False
    binding: Binding | None = None
    annotations: dict[str, bool] = field(default_factory=dict)
    selected_topic: str | None = None
    role_change_elected: bool = False


def admit(contract: dict[str, Any], state: State) -> str:
    """Return a review decision for ONE proposed question and ONE exact context."""
    if state.paused:
        return 'STOPPED'
    default = contract['default_topic']
    dependent = contract['context_mode'] != 'self_contained'
    source_topic = state.binding.topic if dependent and state.binding else None
    base_topic = source_topic or default
    topic = state.selected_topic or base_topic
    if topic != base_topic and not state.role_change_elected:
        return 'UNAUTHORIZED_ROLE_SUBSTITUTION'
    if topic in state.closed_topics:
        return 'TOPIC_CLOSED'
    if not state.applicable and not state.imagined_explicitly_elected:
        return 'INAPPLICABLE'
    if not state.useful_missing_distinction:
        return 'NO_USEFUL_GAP'
    if state.already_answered:
        return 'ALREADY_ANSWERED'
    if state.repeated_unresolved_probe:
        return 'MOVE_ON_UNRESOLVED'
    if contract['context_mode'] != 'self_contained':
        source = state.binding
        if source is None or not source.event_id:
            return 'NEEDS_CONTEXT'
        if not source.active:
            return 'SUPERSEDED_SOURCE'
        if source.context_key != state.context_key:
            return 'WRONG_CONTEXT'
        if not source.semantic_match:
            return 'UNVERIFIED_CONTEXT'
        if not source.is_participant_source:
            return 'STIMULUS_IS_NOT_ANSWER'
        if not source.topic:
            return 'NEEDS_SOURCE_SCOPE'
        if source.topic in state.closed_topics:
            return 'TOPIC_CLOSED'
        allowed = source.question_id in contract['context_candidates']
        if not allowed and not contract['accept_equivalent_cited_context']:
            return 'UNLISTED_CONTEXT'
    for flag in contract['required_annotations']:
        # Unknown/missing is NOT True. Require an explicit reviewed Boolean.
        if state.annotations.get(flag) is not True:
            return 'PREREQUISITE_OR_GAP_UNESTABLISHED'
    return 'ADMIT'


def validate_graph(graph: dict[str, Any], bank: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    qids=[q['id'] for q in bank['questions']]
    ids=[n['id'] for n in graph['nodes']]
    contracts=graph['routing_contracts']; by={c['id']:c for c in contracts}
    if len(ids)!=len(set(ids)): errors.append('duplicate_node')
    if len(qids)!=len(set(qids)): errors.append('duplicate_question')
    if len(contracts)!=len(qids) or set(by)!=set(qids): errors.append('contract_inventory')
    known=set(ids); adj={qid:[] for qid in qids}
    expected=set()
    for q in bank['questions']:
        qid=q['id']
        if qid not in by:continue
        c=by[qid]
        if c['context_candidates']!=q['context_sources']:errors.append('context_drift:'+qid)
        if c['possible_targets']!=q['planning_targets']:errors.append('target_drift:'+qid)
        if c['targets_are_evidence']:errors.append('stimulus_credit:'+qid)
        if c['context_mode']!='self_contained' and not c['context_candidates'] and c['context_mode']!='semantic_action':errors.append('missing_context:'+qid)
        for ref in q['context_sources']:
            typ='advisory_context' if c['context_mode'] in ('self_contained','semantic_action') else 'context_candidate'
            expected.add(('q:'+ref,'q:'+qid,typ))
        for f in q['planning_targets']:expected.add(('q:'+qid,'f:'+f,'may_inform'))
    actual={(e['from'],e['to'],e['kind']) for e in graph['edges']}
    if len(actual)!=len(graph['edges']):errors.append('duplicate_edge')
    if actual!=expected:errors.append('edge_drift')
    for e in graph['edges']:
        if e['from'] not in known or e['to'] not in known:errors.append('dangling_edge')
        if e['kind']=='may_inform' and e.get('evidence_credit') is not False:errors.append('false_evidence_edge')
        if e['kind']=='context_candidate':
            a=e['from'][2:];b=e['to'][2:]
            if a in adj and b in adj:adj[a].append(b)
    # The prerequisite graph must be acyclic. Conversation itself can revisit
    # a topic with an explicitly different context and is not constrained to a DAG.
    visiting:set[str]=set(); visited:set[str]=set()
    def visit(node: str)->None:
        if node in visiting:
            errors.append('circular_prerequisite');return
        if node in visited:return
        visiting.add(node)
        for nxt in adj[node]:visit(nxt)
        visiting.remove(node);visited.add(node)
    for qid in qids:visit(qid)
    # Semantic referent identified in the source audit, independently of
    # whatever happens to have been copied into the candidate graph.
    if 'M02' in by and 'M01' not in by['M02']['context_candidates']:errors.append('pressure_antecedent_missing')
    family_ids=[qid for family in graph['families'] for qid in family['question_ids']]
    if sorted(family_ids)!=sorted(qids):errors.append('family_inventory')
    targeted={e['to'] for e in graph['edges'] if e['kind']=='may_inform'}
    info={n['id'] for n in graph['nodes'] if n['kind']=='information'}
    if targeted!=info:errors.append('unrouted_information')
    return sorted(set(errors))


def explicit_comparison(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Check reviewed contrast records; both branches may come from one message.

    Only explicitly declared changed fields can differ. This checks record
    structure, not the truth of the answers or causal equivalence of conditions.
    """
    axes_left=set(left.get('declared_changed_fields', []))
    axes_right=set(right.get('declared_changed_fields', []))
    if not (left.get('answer_event') and right.get('answer_event')
            and left.get('condition_key') and right.get('condition_key')
            and left['condition_key'] != right['condition_key']
            and left.get('active') is True and right.get('active') is True
            and left.get('comparison_group') == right.get('comparison_group')
            and left.get('comparison_group')
            and left.get('response_task') == right.get('response_task')
            and left.get('response_task')
            and left.get('conditions_explicit') is True
            and right.get('conditions_explicit') is True
            and axes_left == axes_right and axes_left):
        return False
    for key in ('role', 'time_frame'):
        if not left.get(key) or not right.get(key):
            return False
        if left[key] != right[key] and key not in axes_left:
            return False
    return True
