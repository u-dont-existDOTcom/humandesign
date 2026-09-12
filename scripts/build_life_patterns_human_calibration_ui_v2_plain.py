#!/usr/bin/env python3
"""Build the verified Life Patterns v2 offline UI with a plain-language human layer.

This is a presentation-only transform applied after the verified portable UI is built. It does
not alter embedded private evidence, selected calibration units, response schemas, code values,
content addresses, blinding rules, or network behavior. It makes the existing observable-specific
judgment understandable to a human who did not author the codebook.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from build_life_patterns_human_calibration_ui_v2_portable import (
    build_portable_standalone_human_calibration_ui_v2,
)

PLAIN_OBSERVABLES: dict[str, dict[str, str]] = {
    "NBM-R01": {
        "episode": "Does this story show how the narrator responded to a genuinely optional opportunity to join, enter, try, or participate in something?",
        "series": "Does the narrator report a recurring way of responding to genuinely optional opportunities to join, enter, try, or participate?",
        "boundary": "The opportunity must really be optional for the narrator.",
    },
    "NBM-R02": {
        "episode": "Does this story show the narrator deliberately trying to get factual information because they knew something relevant was unknown?",
        "series": "Does the narrator report a recurring way of seeking factual information when they know something relevant is unknown?",
        "boundary": "Unsolicited information and practical help are different things.",
    },
    "NBM-R03": {
        "episode": "Does this story show what the narrator did while an important unknown was still unresolved at the point they could act?",
        "series": "Does the narrator report a recurring response to acting while an important unknown is still unresolved?",
        "boundary": "The narrator must have recognized the uncertainty at the time.",
    },
    "NBM-R04": {
        "episode": "Does this story show how the narrator limited, staged, backed up, shared, or accepted an action after recognizing a specific possible loss or downside?",
        "series": "Does the narrator report a recurring way of setting exposure after recognizing a specific possible loss or downside?",
        "boundary": "The narrator must have recognized the downside before acting and had more than one feasible exposure level.",
    },
    "NBM-R05": {
        "episode": "Does this story show a real choice point and how the narrator formed or resolved the available options?",
        "series": "Does the narrator report a recurring way of forming or resolving choices between recognized alternatives?",
        "boundary": "Do not invent alternatives that the narrator never recognized.",
    },
    "NBM-R06": {
        "episode": "Does this story show what the narrator did with a definite earlier decision when later information, changed circumstances, another person's intervention, or reconsideration created a chance to revise it?",
        "series": "Does the narrator report a recurring way of revising or maintaining earlier decisions when a real reconsideration point appears?",
        "boundary": "There must be a definite earlier decision, not merely an option or possibility.",
    },
    "NBM-R07": {
        "episode": "Does this story show concrete preparation the narrator did before or at the start of a focal action?",
        "series": "Does the narrator report a recurring way of preparing before or at the start of focal actions?",
        "boundary": "Thinking, hoping, or worrying alone is not preparation.",
    },
    "NBM-R08": {
        "episode": "Does this story show when or how the narrator actually started an accepted task, requirement, or definite intended action?",
        "series": "Does the narrator report a recurring pattern in when or how they start accepted tasks or definite intended actions?",
        "boundary": "Required preparation is not automatically delay.",
    },
    "NBM-R09": {
        "episode": "Does this story show the narrator using, creating, changing, bypassing, or deliberately rejecting an external reminder, schedule, environment, access condition, or accountability structure for a target behavior?",
        "series": "Does the narrator report a recurring way of using or rejecting external structures such as reminders, schedules, environments, or accountability?",
        "boundary": "A structure merely existing around the narrator does not count unless the narrator acts on or uses it.",
    },
    "NBM-R10": {
        "episode": "Does this story show how the narrator allocated a limited resource when two or more recognized demands or actions genuinely competed for it?",
        "series": "Does the narrator report a recurring way of allocating limited time, attention, money, effort, or access among competing demands?",
        "boundary": "The demands must actually compete for the same limited resource.",
    },
    "NBM-R11": {
        "episode": "Does this story show what the narrator did after a concrete barrier, setback, interruption, rejection, illness episode, conflict, or other disruption impeded an ongoing goal?",
        "series": "Does the narrator report a recurring response after disruptions impede an ongoing goal?",
        "boundary": "There must be an identifiable ongoing goal and a real disruption.",
    },
    "NBM-R12": {
        "episode": "Does this story show whether or how the narrator changed the method used toward the same goal across attempts or after feedback/results?",
        "series": "Does the narrator report a recurring way of changing or repeating methods across attempts or after feedback/results?",
        "boundary": "A different later action is not enough unless the same goal and attempt/feedback sequence are clear.",
    },
    "NBM-R13": {
        "episode": "Does this story show the narrator deliberately checking an outcome, accuracy, completion, receipt, consequence, or quality, or actively asking for outcome-relevant feedback?",
        "series": "Does the narrator report a recurring way of checking outcomes or actively obtaining feedback?",
        "boundary": "Automatic or unsolicited feedback does not by itself count as the narrator checking.",
    },
    "NBM-R14": {
        "episode": "Does this story show what the narrator did after recognizing or being told about a specific possible mistake in their own earlier action or omission?",
        "series": "Does the narrator report a recurring way of responding after recognizing possible mistakes in their own actions?",
        "boundary": "An unfavorable outcome is not enough unless a specific possible error is recognized.",
    },
    "NBM-R15": {
        "episode": "Does this story show how the narrator handled a clearly defined task, deliverable, agreement, promise, or commitment when its endpoint became due or relevant?",
        "series": "Does the narrator report a recurring way of handling defined endpoints, promises, or commitments when they become due?",
        "boundary": "A vague aspiration with no defined endpoint does not count.",
    },
    "NBM-R16": {
        "episode": "Does this story show the narrator seeking, signaling for, accepting, declining, delegating to, or using another person's help for the narrator's own concrete task, obstacle, or need?",
        "series": "Does the narrator report a recurring way of seeking, accepting, declining, delegating to, or using another person's help for the narrator's own task or need?",
        "boundary": "This is about the narrator receiving or seeking help. The narrator offering help to someone else does not count as R16.",
    },
    "NBM-R17": {
        "episode": "Does this story show the narrator initiating or aligning roles, timing, responsibilities, or interdependent actions in a concrete shared task?",
        "series": "Does the narrator report a recurring way of coordinating roles, timing, or responsibilities in shared interdependent tasks?",
        "boundary": "Ordinary conversation or one-directional helping without a shared interdependent task does not count.",
    },
    "NBM-R18": {
        "episode": "Does this story show the narrator communicating their own need, capacity limit, constraint, lack of knowledge, or uncertainty to someone for whom it mattered to shared action?",
        "series": "Does the narrator report a recurring way of communicating their own needs, limits, constraints, lack of knowledge, or uncertainty when it matters to shared action?",
        "boundary": "The condition must belong to the narrator, not another person.",
    },
    "NBM-R19": {
        "episode": "Does this story show how the narrator responded after another person made a concrete request, demand, boundary, refusal, capacity limit, or condition that called for a response?",
        "series": "Does the narrator report a recurring way of responding to other people's concrete requests, limits, boundaries, or conditions?",
        "boundary": "Voluntary help the narrator initiated without a request is not R19.",
    },
    "NBM-R20": {
        "episode": "Does this story show what the narrator did after recognizing a real disagreement with another person's position, interpretation, plan, or demand?",
        "series": "Does the narrator report a recurring way of handling recognized disagreements with other people?",
        "boundary": "Private dislike or a disagreement the narrator did not recognize does not count.",
    },
    "NBM-R21": {
        "episode": "Does this story show what the narrator did after recognizing relational strain, offense, misunderstanding, broken trust, or interpersonal harm and having a chance to address it?",
        "series": "Does the narrator report a recurring way of responding after recognizing interpersonal strain or harm and having a chance to repair it?",
        "boundary": "Regret alone is not repair behavior, and lack of repair cannot be coded before the narrator knew about the strain or harm.",
    },
    "NBM-R22": {
        "episode": "Does this story show what the narrator did when an explicit rule, instruction, agreed procedure, or formal requirement applied and they knew about it?",
        "series": "Does the narrator report a recurring way of responding to explicit rules, instructions, procedures, or formal requirements they know about?",
        "boundary": "A vague norm, custom, or etiquette is not enough.",
    },
}

HUMAN_LABELS: dict[str, str] = {
    "universal_language": "Uses ‘always/every time’ language",
    "near_universal": "Almost always",
    "usually": "Usually",
    "often": "Often / frequently",
    "sometimes": "Sometimes",
    "rarely": "Rarely",
    "repeated_unquantified": "Repeated, but frequency not stated",
    "bounded_rate_or_count": "A specific count or rate is stated",
    "context_conditional": "Depends on the situation / context",
    "changed_over_time": "Changed over time",
    "unclear": "Recurs, but strength is unclear",
    "exceptions_explicitly_denied": "Narrator explicitly says there are no exceptions",
    "exceptions_reported": "Narrator reports exceptions or boundary conditions",
    "exceptions_not_probed_or_unknown": "Not stated / not established",
    "none_reported": "No exceptions reported",
    "almost_never": "Almost never",
    "context_dependent": "Depends on context",
    "rough_rate_or_count": "A rough exception count/rate is stated",
    "unknown": "Unknown / not stated",
    "generalized_self_report": "General recurrence statement by the narrator",
    "bounded_rate_or_count_self_report": "Narrator gives a bounded count/rate",
    "sampled_opportunities": "Opportunities were sampled systematically",
    "external_record_or_observation": "External record or observation",
    "mixed_basis": "More than one evidence basis",
    "narrator_explicit_influence": "Narrator explicitly says something affected this behavior",
    "temporal_precedence_only": "Something happened earlier, but no influence is claimed",
    "established": "Yes",
    "not_established": "No",
}


def _replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"plain-language UI patch expected exactly one {label}; found {count}")
    return text.replace(old, new, 1)


def _replace_function(text: str, name: str, replacement: str) -> str:
    start = text.find(f"function {name}(")
    if start < 0:
        raise ValueError(f"plain-language UI patch could not find function {name}")
    candidates = [
        text.find("\nfunction ", start + 1),
        text.find("\nconst attestQs=", start + 1),
        text.find("\n</script>", start + 1),
    ]
    end = min(value for value in candidates if value >= 0)
    return text[:start] + replacement + text[end:]


def _embedded_fragment(html: str) -> str:
    start = html.find("const EMBEDDED = ")
    end = html.find("\nconst OUTER = ", start)
    if start < 0 or end < 0:
        raise ValueError("plain-language UI patch cannot locate embedded handoff payload")
    return html[start:end]


def patch_html_for_plain_human_ui(html: str) -> str:
    """Apply presentation-only human-comprehension corrections and fail closed on drift."""

    embedded_before = _embedded_fragment(html)
    target = 'const INFLUENCE = ["none_reported","narrator_explicit_influence","temporal_precedence_only"];'
    constants = (
        target
        + "\nconst PLAIN_OBSERVABLES = "
        + json.dumps(PLAIN_OBSERVABLES, ensure_ascii=False, separators=(",", ":"))
        + ";\nconst HUMAN_LABELS = "
        + json.dumps(HUMAN_LABELS, ensure_ascii=False, separators=(",", ":"))
        + ";"
    )
    html = _replace_once(html, target, constants, label="influence constant")

    html = _replace_once(
        html,
        '<details class="details" open><summary>Criteria and evidence requirements</summary>',
        '<details class="details"><summary>Formal definition and coding rules (open only if needed)</summary>',
        label="formal criteria disclosure",
    )
    html = _replace_once(
        html,
        '<h2 style="font-size:20px;margin:8px 0 6px">Exact participant source</h2><p class="hint">Primary evidence. Select citations here for the response.</p>',
        '<h2 style="font-size:20px;margin:8px 0 6px">What the narrator actually said</h2><p class="hint">Read this first. “Narrator” means the person whose story is being coded. Do not make the story fit the question on the right.</p>',
        label="source heading",
    )
    html = _replace_once(
        html,
        '<div class="section"><h3>Uncertainty and context</h3><div class="field"><span class="labelish">Missingness / uncertainty flags</span>',
        '<details class="section details" id="advancedContext"><summary>Optional uncertainty / context notes</summary><div class="field"><span class="labelish">Missing or uncertain information</span>',
        label="advanced-context opening",
    )
    html = _replace_once(
        html,
        '<div class="field"><label for="note">Coder note <span class="hint">optional; not part of consensus semantics</span></label><textarea id="note"></textarea></div></div><div id="unitErrors"',
        '<div class="field"><label for="note">Optional note</label><textarea id="note"></textarea></div></details><div id="unitErrors"',
        label="advanced-context closing",
    )
    html = _replace_once(
        html,
        "</head>",
        """<style>
.unitquestion{background:#edf8f3;border:1px solid #b8d9ca;border-radius:12px;padding:14px 15px;margin:8px 0 12px}
.unitquestion strong{display:block;font-size:18px;line-height:1.35;margin-bottom:7px}
.unitquestion p{margin:0;color:#43534c}.unitwhy{font-size:12px;color:var(--muted);margin-top:7px}
.value code{opacity:.45;font-size:10px;float:right}.value .minimum{display:none}
.secondary .label{text-transform:none;letter-spacing:0}
details.section>summary{font-weight:720;cursor:pointer;margin-bottom:8px}
</style>
</head>""",
        label="head closing",
    )

    helper_old = 'function human(s){return String(s??"").replaceAll("_"," ").replace(/\\b\\w/g,c=>c.toUpperCase())}\nfunction listHtml(title,items){return items&&items.length?`<div><b>${esc(title)}</b><ul>${items.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>`:""}'
    helper_new = '''function human(s){return String(s??"").replaceAll("_"," ").replace(/\\b\\w/g,c=>c.toUpperCase())}
function humanLabel(x){return HUMAN_LABELS[x]||human(x)}
function plainObservable(u){return PLAIN_OBSERVABLES[u.obs.observable_id]||{episode:u.obs.definition,series:u.obs.definition,boundary:"Judge only the narrator's behavior described by the exact source."}}
function plainBehavior(w,v){if(v==="OS")return"Another behavior that fits this question but is not listed";let s=String(w||"").trim();if(!s)return"Behavior "+v;s=s.replace(/[.;]+$/," ").trim();if(/^the narrator\\b/i.test(s))return s.charAt(0).toUpperCase()+s.slice(1);return"The narrator "+s}
function listHtml(title,items){return items&&items.length?`<div><b>${esc(title)}</b><ul>${items.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>`:""}'''
    html = _replace_once(html, helper_old, helper_new, label="human/list helper block")

    html = _replace_function(
        html,
        "render",
        '''function render(){const u=units[current];const r=responses.get(u.key)||draftFromFormSeed(u);const p=plainObservable(u);$("kindBadge").textContent=u.kind==="episode"?"One story":"Repeated pattern";$("kindBadge").className="badge "+(u.kind==="series"?"series":"");$("taskIdentity").textContent=u.evidenceId;$("observableId").textContent=`${u.obs.observable_id} · ${u.obs.label}`;$("observableLabel").textContent="Question for this unit";$("observableDefinition").innerHTML=`<div class="unitquestion"><strong>${esc(u.kind==="episode"?p.episode:p.series)}</strong><p>${esc(p.boundary)}</p><div class="unitwhy">This story/question pair does not have to match. Choose No when the prerequisite is absent; choose Can't tell when the source is too unclear.</div></div>`;$("criteria").innerHTML=`<div><b>Formal definition</b><p>${esc(u.obs.definition)}</p></div>`+listHtml("Counts when",u.obs.inclusion_criteria)+listHtml("Does not count when",u.obs.exclusion_criteria)+listHtml("Minimum evidence",u.obs.evidence_requirements);$("evidenceMeta").innerHTML=[u.task.approximate_age_life_phase].filter(Boolean).map(x=>`<span class="chip">${esc(x)}</span>`).join("");renderSources(u,r);renderSecondary(u);renderStates(u,r);renderObserved(u,r);renderCommon(u,r);updateProgress();$("unitErrors").classList.add("hidden");$("unitErrors").textContent="";$("languageField").classList.toggle("hidden",u.kind!=="episode");$("unitDone").innerHTML=responses.has(u.key)?'<span class="done">✓ saved</span>':'';$("prevBtn").disabled=current===0;$("nextBtn").textContent=current===units.length-1?"Save unit →":"Save & next →";$("jumpSelect").value=String(current);window.scrollTo({top:0,behavior:"smooth"})}''',
    )
    html = _replace_function(
        html,
        "renderSources",
        '''function renderSources(u,r){const support=new Set(r.supporting_source_segment_ids||[]),counter=new Set(r.counterevidence_source_segment_ids||[]);const observed=r.state==="observed";$("sources").innerHTML=u.task.exact_source_segments.map(s=>`<article class="source"><div class="sourceid">${esc(s.segment_id)}</div><p>${esc(s.exact_text||s.exact_participant_text||"")}</p>${observed?`<div class="sourcechecks"><label><input type="checkbox" data-source="support" value="${esc(s.segment_id)}" ${support.has(s.segment_id)?"checked":""}> Use this quote as evidence for the behavior I selected</label><label><input type="checkbox" data-source="counter" value="${esc(s.segment_id)}" ${counter.has(s.segment_id)?"checked":""}> This quote qualifies or goes against my selected behavior</label></div>`:`<div class="hint">No quote checkbox is needed unless you answer Yes.</div>`}</article>`).join("")}''',
    )
    html = _replace_function(
        html,
        "renderSecondary",
        '''function renderSecondary(u){let rows=[];if(u.kind==="episode"){rows.push(["Context summary",u.task.episode_narrative])}else{rows.push(["Period / context",u.task.bounded_period_context],["Participant's recurrence wording",u.task.recurrence_language],["Reported repeated behavior",u.task.behavior_reportedly_recurred],["Rough opportunity count",u.task.rough_opportunity_count],["Exceptions / limits",u.task.explicit_exceptions_or_limits],["Memory uncertainty",u.task.memory_source_uncertainty])}rows=rows.filter(x=>x[1]);$("secondaryContext").innerHTML=rows.length?`<div class="secondary"><div class="label">Context summary — secondary orientation only</div><p class="hint">Use the exact quote above as the evidence for your answer. This summary only helps you understand the situation.</p>${rows.map(([a,b])=>`<p><b>${esc(a)}:</b> ${esc(b)}</p>`).join("")}</div>`:""}''',
    )
    html = _replace_function(
        html,
        "renderStates",
        '''function renderStates(u,r){const opts=[["observed","Yes — clearly shown","The exact quote clearly shows the narrator doing the behavior asked about."],["not_applicable","No — does not fit","The required situation is absent. Do not reinterpret the story to make it fit."],["insufficient","Can't tell","The behavior might fit, but the exact quote is not clear enough to decide reliably."]];$("stateGrid").innerHTML=`<h3 style="grid-column:1/-1;margin:0">Does the exact source answer the question above?</h3>`+opts.map(([v,l,d])=>`<label class="state"><b><input type="radio" name="state" value="${v}" ${r.state===v?"checked":""}>${l}</b><span>${d}</span></label>`).join("");updateStateSemantics(u,r.state);document.querySelectorAll('input[name="state"]').forEach(el=>el.addEventListener("change",()=>{const next={...readForm(u),state:el.value};updateStateSemantics(u,el.value);renderSources(u,next);renderObserved(u,next)}))}''',
    )
    html = _replace_function(
        html,
        "updateStateSemantics",
        '''function updateStateSemantics(u,state){$("stateSemantics").textContent=state==="observed"?"If Yes, choose the behavior below and cite the exact quote that shows it.":state==="not_applicable"?"No behavioral value is needed.":state==="insufficient"?"No behavioral value is needed; use an uncertainty flag or note only if it helps explain why.":""}''',
    )
    html = _replace_function(
        html,
        "gateSelect",
        '''function gateSelect(k,v){const q={awareness:"Did the narrator know about the relevant option / request / problem?",opportunity:"Was there a real opportunity or response window?",feasibility:"Was the action realistically possible?",established_non_action:"Does the exact source clearly establish that the narrator did not act?"}[k]||human(k);return`<div class="field"><label>${esc(q)}</label><select data-gate="${k}"><option value="">Choose…</option>${["established","not_established","unclear"].map(x=>`<option value="${x}" ${v===x?"selected":""}>${esc(humanLabel(x))}</option>`).join("")}</select></div>`}''',
    )
    html = _replace_function(
        html,
        "selectField",
        '''function selectField(id,label,values,current,blank=true){return`<div class="field"><label for="${id}">${esc(label)}</label><select id="${id}">${blank?'<option value="">Choose…</option>':""}${values.map(x=>`<option value="${x}" ${current===x?"selected":""}>${esc(humanLabel(x))}</option>`).join("")}</select></div>`}''',
    )
    html = _replace_function(
        html,
        "seriesFields",
        '''function seriesFields(r){return`<div class="section"><h3>How often does the narrator report this behavior recurring?</h3><p class="hint">Code the narrator's report, not a claim that the true frequency has been externally verified. A confirming anecdote is not an extra frequency observation.</p>${selectField("recurrenceStrength","Reported recurrence",RECURRENCE_STRENGTH,r.reported_recurrence_strength)}${selectField("exceptionStatus","Does the source establish exceptions?",EXCEPTION_STATUS,r.exception_status)}${selectField("exceptionFrequency","If exceptions are established, how often?",EXCEPTION_FREQ,r.exception_frequency)}${selectField("frequencyBasis","What is this frequency statement based on?",FREQ_BASIS,r.frequency_evidence_basis)}<div class="field"><label for="recurrenceScope">What situations does the recurrence claim apply to? <span class="hint">optional</span></label><textarea id="recurrenceScope">${esc(r.recurrence_scope_description||"")}</textarea></div><details class="details"><summary>Optional count/rate fields — only when the exact source gives one</summary><div class="field"><label for="minimumOccurrences">Minimum number of occurrences directly supported by the source</label><input id="minimumOccurrences" type="number" min="2" step="1" value="${r.minimum_reported_occurrences??""}"></div><div class="field"><label for="boundedDescription">Count/rate wording from the source</label><textarea id="boundedDescription">${esc(r.bounded_rate_or_count_description||"")}</textarea></div></details></div>`}''',
    )
    html = _replace_function(
        html,
        "episodeInfluence",
        '''function episodeInfluence(u,r){const rel=r.influence_relation||"none_reported";const inf=new Set(r.influence_source_segment_ids||[]);return`<details class="section details"><summary>Optional: does the narrator explicitly say something influenced the behavior you selected?</summary><p class="hint">This is only about the behavior you coded above. Do not record a causal statement about some other action in the story.</p>${selectField("influenceRelation","Relation to the selected behavior",INFLUENCE,rel,false)}${rel!=="none_reported"?`<div class="field"><span class="labelish">Which exact quote states or establishes that relation?</span><div class="checkgrid">${u.task.exact_source_segments.map(s=>`<label class="checkpill"><input type="checkbox" data-source="influence" value="${esc(s.segment_id)}" ${inf.has(s.segment_id)?"checked":""}> ${esc(s.segment_id)}</label>`).join("")}</div></div>`:""}</details>`}''',
    )
    html = _replace_function(
        html,
        "renderObserved",
        '''function renderObserved(u,r){const host=$("observedFields");if(r.state!=="observed"){host.innerHTML='<div class="section"><p class="hint">No behavioral subcode is needed for this answer.</p></div>';return}const subMap=new Map((u.resolved?.subcodes||[]).map(s=>[s.subcode_id,s]));const selected=new Set(r.coded_values||[]);const values=u.obs.allowed_values||[];const relation=r.value_relation||(selected.size===1?"single":"");let html=`<div class="section"><h3>Which behavior does the exact source show?</h3><div class="values">${values.map(v=>{const s=subMap.get(v);const non=u.ext.non_action_values.includes(v);return`<label class="value"><input type="checkbox" data-value="${esc(v)}" ${selected.has(v)?"checked":""}><div><div><span class="wording">${esc(plainBehavior(s?.wording,v))}</span> <code>${esc(v)}</code></div></div>${non?'<span class="tag">no-action rule</span>':""}</label>`}).join("")}</div><div class="relationrow"><span class="labelish">If more than one behavior is selected, how do they relate?</span><select id="valueRelation"><option value="">Choose…</option><option value="single" ${relation==="single"?"selected":""}>One behavior</option><option value="ordered_sequence" ${relation==="ordered_sequence"?"selected":""}>They happened in this order</option><option value="unordered_multiple" ${relation==="unordered_multiple"?"selected":""}>More than one; order is not established</option></select></div><div class="ordered" id="orderedValues"></div></div>`;if(u.kind==="series")html+=seriesFields(r);else html+=episodeInfluence(u,r);html+=`<div class="section hidden" id="osField"><div class="field"><label for="osDescription">Describe the behavior that is not listed above</label><textarea id="osDescription">${esc(r.other_specified_description||"")}</textarea></div></div><div class="section hidden" id="nonActionField"><h3>Extra check required for a “did not act” code</h3><p class="hint">Only use a no-action value when all four questions below can be answered Yes from the supplied evidence. Otherwise choose a different behavior or Can't tell.</p><div class="gate">${["awareness","opportunity","feasibility","established_non_action"].map(k=>gateSelect(k,r.non_action_gate?.[k])).join("")}</div></div>`;host.innerHTML=html;host.querySelectorAll('[data-value]').forEach(x=>x.addEventListener("change",()=>{syncSpecial(u);const vals=selectedValues();const vr=$("valueRelation");if(vr){if(vals.length===1)vr.value="single";else if(vals.length>1&&vr.value==="single")vr.value=""}}));$("valueRelation")?.addEventListener("change",()=>renderOrdered());$("influenceRelation")?.addEventListener("change",()=>renderObserved(u,readForm(u)));if(r.value_relation==="ordered_sequence")orderOverrides.set(u.key,[...(r.coded_values||[])]);else orderOverrides.delete(u.key);syncSpecial(u)}''',
    )

    html = _replace_once(
        html,
        'const rel=$("valueRelation")?.value||null;',
        'const rel=$("valueRelation")?.value||(vals.length===1?"single":null);',
        label="single-value relation read",
    )
    html = _replace_once(
        html,
        'o.textContent=`${Number(o.value)+1}. ${u.kind==="episode"?"Episode":"Series"} · ${u.obs.observable_id}${responses.has(u.key)?" ✓":""}`',
        'o.textContent=`${Number(o.value)+1}. ${u.kind==="episode"?"Story":"Repeated pattern"} · ${u.obs.label}${responses.has(u.key)?" ✓":""}`',
        label="jump-list display",
    )
    html = _replace_once(
        html,
        '<h1>Verify first. Then annotate.</h1><p>This file contains the frozen private calibration handoff. It makes no network requests. Before any evidence is shown, it verifies the handoff receipt, every embedded member hash, all packet content addresses, and the selected unit coverage.</p>',
        '<h1>Read one story. Answer one behavior question.</h1><p>This private file works entirely on your device. Each screen asks whether one specific behavior is shown in one story. The correct answer may be Yes, No, or Can’t tell. You never need to make a story fit the question.</p>',
        label="intro copy",
    )

    if len(PLAIN_OBSERVABLES) != 22:
        raise ValueError("plain-language UI must define exactly 22 observable questions")
    if _embedded_fragment(html) != embedded_before:
        raise ValueError("plain-language UI patch altered embedded private handoff bytes")
    if " Supporting</label>" in html or "Narrator influence / precedence" in html:
        raise ValueError("plain-language UI patch left known ambiguous labels in the interface")
    return html


def build_plain_standalone_human_calibration_ui_v2(
    handoff_zip: str | Path,
    output_html: str | Path,
    *,
    overwrite: bool = False,
) -> dict[str, Any]:
    output = Path(output_html)
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")

    with tempfile.TemporaryDirectory(prefix="life-patterns-ui-v2-plain-") as temporary:
        portable = Path(temporary) / "portable.html"
        base_receipt = build_portable_standalone_human_calibration_ui_v2(
            handoff_zip,
            portable,
        )
        before = portable.read_text(encoding="utf-8")
        after = patch_html_for_plain_human_ui(before)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(after, encoding="utf-8", newline="\n")
    raw = output.read_bytes()
    receipt = dict(base_receipt)
    receipt.update(
        schema_version="life-patterns-human-calibration-ui-plain-build-receipt-v2",
        output_html_sha256=hashlib.sha256(raw).hexdigest(),
        output_html_bytes=len(raw),
        plain_language_observable_questions=22,
        embedded_private_handoff_unchanged=True,
        selected_calibration_units_changed=False,
        response_contract_changed=False,
        measurement_semantics_changed=False,
        target_model_information_used=False,
        automated_judgment_used=False,
        network_requests_required=False,
        supersedes_prior_ui_for_human_collection=True,
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-zip", type=Path, required=True)
    parser.add_argument("--output-html", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    receipt = build_plain_standalone_human_calibration_ui_v2(
        args.handoff_zip,
        args.output_html,
        overwrite=args.overwrite,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
