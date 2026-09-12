#!/usr/bin/env python3
"""Build the versioned Life Patterns V5 human-first calibration UI.

The accepted V5 measurement graph is machine bookkeeping, not a human task. This builder reuses
the verified final V2 auditor surface and replaces only the measurement interaction/export layer:
choices are grouped by facet, hybrid affirmative/absence components are judged separately,
stage questions appear only for multiple same-facet facts, provenance is claim-specific when
multiple exact sources exist, and final response downloads are V5 graph envelopes.

Historical V2 builders and private handoff bytes remain unchanged. The generated UI is offline and
development-only; it does not authorize human collection until owner usability acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Mapping, cast

from build_life_patterns_human_calibration_ui_v2_auditor_final import (
    _embedded_fragment,
    _replace_function,
    build_final_auditor_ui_v2,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "state" / "LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json"
EXPECTED_CONTRACT_SCHEMA = "life-patterns-facet-relation-contract-v5-candidate"
EXPECTED_CONTRACT_VERSION = "5.0.0-candidate"
EXPECTED_REVIEW_COMMIT = "ce04642146c41a7d5d94f85360572c78de887682"

# Non-hybrid absence-dependent values need a claim-specific gate even though the accepted
# contract does not split them into affirmative+absence hybrid components. Wording follows the
# accepted theory-blind codebook clarification; window kinds are drawn only from the V5 contract.
NON_HYBRID_ABSENCE_SPECS: dict[str, dict[str, str]] = {
    "R01-h": {
        "proposition": "no behavioral response during the named feasible action opportunity",
        "window_kind": "action_window",
    },
    "R03-h": {
        "proposition": "no action during the named feasible action window",
        "window_kind": "action_window",
    },
    "R05-R8": {
        "proposition": "no choice resolution during the named feasible decision window",
        "window_kind": "action_window",
    },
    "R07-a2": {
        "proposition": "absence of concrete preparation during the named feasible pre-action window",
        "window_kind": "preaction_window",
    },
    "R08-c": {
        "proposition": "no task-directed start by the narrator's previously stated intended start point",
        "window_kind": "action_window",
    },
    "R08-f": {
        "proposition": "no task-directed start during the named feasible action window",
        "window_kind": "action_window",
    },
    "R10-k": {
        "proposition": "no action on either competing course during the named feasible allocation interval",
        "window_kind": "allocation_interval",
    },
    "R11-G7": {
        "proposition": "no return to the focal goal within the stated follow-up window",
        "window_kind": "goal_followup_window",
    },
    "R13-g": {
        "proposition": "no checking action during the named feasible checking opportunity",
        "window_kind": "checking_opportunity_window",
    },
    "R14-i": {
        "proposition": "no remedial error response during the defined feasible remedial window",
        "window_kind": "remedial_response_window",
    },
    "R15-l": {
        "proposition": "no defined endpoint component completed during the named feasible endpoint assessment window",
        "window_kind": "endpoint_assessment_window",
    },
    "R16-l": {
        "proposition": "no help request during the named feasible request opportunity",
        "window_kind": "request_opportunity_window",
    },
    "R17-h": {
        "proposition": "no coordination with the relevant party during the named feasible coordination opportunity",
        "window_kind": "action_window",
    },
    "R19-f": {
        "proposition": "no response during the named feasible response window",
        "window_kind": "action_window",
    },
    "R21-k": {
        "proposition": "no repair action during the named feasible repair opportunity",
        "window_kind": "repair_opportunity_window",
    },
    "R22-g": {
        "proposition": "no required response during the named feasible rule-response opportunity",
        "window_kind": "action_window",
    },
}

HYBRID_WINDOW_KINDS: dict[str, str] = {
    "R05-O2": "preselection_search_opportunity",
    "R07-i": "transition_observation_window",
    "R15-b": "endpoint_assessment_window",
    "R15-c": "endpoint_assessment_window",
    "R16-c": "preprompt_request_opportunity",
    "R16-d2": "request_opportunity_window",
    "R16-f": "offer_use_window",
    "R18-d": "communication_opportunity_window",
    "R18-f": "preconsequence_communication_window",
    "R20-j": "repeated_position_exchange_window",
    "R21-f": "resumed_contact_discussion_window",
    "R21-i": "repair_opportunity_window",
}


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return cast(Mapping[str, Any], value)


def load_public_v5_semantics(path: str | Path = CONTRACT_PATH) -> dict[str, Any]:
    contract = json.loads(Path(path).read_text(encoding="utf-8"))
    contract = dict(_mapping(contract, "V5 contract"))
    if contract.get("schema_version") != EXPECTED_CONTRACT_SCHEMA:
        raise ValueError("unexpected V5 facet/relation contract schema")
    if contract.get("contract_version") != EXPECTED_CONTRACT_VERSION:
        raise ValueError("unexpected V5 facet/relation contract version")
    authority = _mapping(contract.get("authority"), "V5 contract authority")
    status = _mapping(contract.get("status"), "V5 contract status")
    if authority.get("historical_artifacts_immutable") is not True:
        raise ValueError("V5 contract does not preserve historical artifacts")
    if status.get("target_theory_information_used") is not False:
        raise ValueError("V5 contract is not target-theory blind")

    hybrids = dict(_mapping(contract.get("hybrid_value_components"), "hybrid values"))
    missing_windows = sorted(set(hybrids) - set(HYBRID_WINDOW_KINDS))
    extra_windows = sorted(set(HYBRID_WINDOW_KINDS) - set(hybrids))
    if missing_windows or extra_windows:
        raise ValueError(
            f"hybrid/window mapping drift; missing={missing_windows} extra={extra_windows}"
        )

    absence_specs = {key: dict(value) for key, value in NON_HYBRID_ABSENCE_SPECS.items()}
    for value_id, raw in hybrids.items():
        parts = _mapping(raw, f"hybrid {value_id}")
        affirmative = parts.get("affirmative")
        absence = parts.get("absence")
        if not isinstance(affirmative, str) or not affirmative.strip():
            raise ValueError(f"hybrid {value_id} lacks affirmative wording")
        if not isinstance(absence, str) or not absence.strip():
            raise ValueError(f"hybrid {value_id} lacks absence wording")
        absence_specs[value_id] = {
            "proposition": absence.strip(),
            "window_kind": HYBRID_WINDOW_KINDS[value_id],
        }

    return {
        "schema_version": EXPECTED_CONTRACT_SCHEMA,
        "contract_version": EXPECTED_CONTRACT_VERSION,
        "accepted_review_commit": EXPECTED_REVIEW_COMMIT,
        "hybrid_value_components": hybrids,
        "absence_specs": absence_specs,
        "default_observable_profile": contract["default_observable_profile"],
        "observable_facet_profiles": contract["observable_facet_profiles"],
        "target_theory_information_used": False,
        "development_only": True,
        "validation_use_forbidden": True,
    }


def _public_js(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).replace(
        "</", "<\\/"
    )


def _v5_helpers(public_semantics: Mapping[str, Any]) -> str:
    public_json = _public_js(public_semantics)
    return rf'''
// V5_EXPORT_HELPERS_START
const V5_PUBLIC={public_json};
const V5_REVIEW_COMMIT="{EXPECTED_REVIEW_COMMIT}";
const V5_HYBRIDS=V5_PUBLIC.hybrid_value_components||{{}};
const V5_ABSENCE=V5_PUBLIC.absence_specs||{{}};
function v5FacetTitle(id){{if(id==="substantive_response")return"Behavior";return String(id||"").replaceAll("_"," ").replace(/\b\w/g,c=>c.toUpperCase())}}
function v5Profile(u){{return V5_PUBLIC.observable_facet_profiles[u.obs.observable_id]||V5_PUBLIC.default_observable_profile}}
function v5FacetSpec(u,facetId){{return v5Profile(u)?.facets?.[facetId]||null}}
function v5FacetForValue(u,valueId){{const p=v5Profile(u),facets=p?.facets||{{}};for(const [fid,spec] of Object.entries(facets)){{if(Array.isArray(spec.value_ids)&&spec.value_ids.includes(valueId))return fid}}if(p===V5_PUBLIC.default_observable_profile||Object.keys(facets).length===1&&facets.substantive_response)return"substantive_response";return null}}
function v5FacetEntries(u){{const out=new Map();for(const v of (u.obs.allowed_values||[])){{const fid=v5FacetForValue(u,v);if(!fid)continue;if(!out.has(fid))out.set(fid,[]);out.get(fid).push(v)}}return out}}
function v5SubcodeMap(u){{return new Map((u.resolved?.subcodes||[]).map(s=>[s.subcode_id,s]))}}
function v5Label(u,v){{const s=v5SubcodeMap(u).get(v);return plainBehavior(s?.wording,v)}}
function v5GateComplete(g){{return !!g&&["awareness","opportunity","feasibility","established_nonoccurrence"].every(k=>g[k]==="established")}}
function v5GateSelect(valueId,key,current){{const labels={{awareness:"Was the narrator aware of the relevant action or requirement?",opportunity:"Was there a real opportunity for it?",feasibility:"Was it feasible in that opportunity?",established_nonoccurrence:"Does the exact source establish that it did not happen, rather than merely fail to mention it?"}};const opts=[["","Choose…"],["established","Yes"],["not_established","No"],["unclear","Can't tell"]];return`<label class="v5gateitem">${{esc(labels[key])}}<select data-v5-gate-value="${{esc(valueId)}}" data-v5-gate-key="${{esc(key)}}">${{opts.map(([v,l])=>`<option value="${{v}}" ${{current===v?"selected":""}}>${{l}}</option>`).join("")}}</select></label>`}}
function v5GateBlock(valueId,r,proposition,hybrid){{const g=(hybrid?r.v5_hybrid_components?.[valueId]?.absence_gate:r.v5_absence_gates?.[valueId])||{{}};return`<div class="v5absence"><p><b>Separate absence claim:</b> ${{esc(proposition)}}</p><p class="hint">The absence counts only when all four answers are Yes. Silence or missing detail is not a No-action finding.</p><div class="v5gate">${{["awareness","opportunity","feasibility","established_nonoccurrence"].map(k=>v5GateSelect(valueId,k,g[k]||"")).join("")}}</div>${{hybrid?'<p class="hint">If these checks are not all Yes, the affirmative fact is retained but the combined value is not asserted.</p>':""}}</div>`}}
function v5HybridCard(u,v,r){{const h=V5_HYBRIDS[v];const saved=r.v5_hybrid_components?.[v]||{{}};const positive=!!saved.affirmative_selected||((r.coded_values||[]).includes(v));return`<div class="v5choice v5hybrid"><label><input type="checkbox" data-v5-hybrid-positive="${{esc(v)}}" ${{positive?"checked":""}}> <span><b>Source shows:</b> ${{esc(h.affirmative)}}</span></label>${{positive?v5GateBlock(v,r,h.absence,true):`<p class="hint">The combined value also requires a separately established absence: ${{esc(h.absence)}}.</p>`}}</div>`}}
function v5AbsenceCard(u,v,r){{const selected=(r.coded_values||[]).includes(v);const label=v5Label(u,v);return`<div class="v5choice v5absencechoice"><label><input type="checkbox" data-value="${{esc(v)}}" ${{selected?"checked":""}}> <span>${{esc(label)}}</span></label>${{selected?v5GateBlock(v,r,V5_ABSENCE[v].proposition,false):""}}</div>`}}
function v5NormalCard(u,v,r){{const selected=(r.coded_values||[]).includes(v);return`<label class="v5choice"><input type="checkbox" data-value="${{esc(v)}}" ${{selected?"checked":""}}> <span>${{esc(v5Label(u,v))}}</span></label>`}}
function v5ConceptIds(u,r,facetId){{const ids=[];for(const v of (r.coded_values||[]))if(v5FacetForValue(u,v)===facetId&&!ids.includes(v))ids.push(v);for(const [v,d] of Object.entries(r.v5_hybrid_components||{{}}))if(d.affirmative_selected&&v5FacetForValue(u,v)===facetId&&!ids.includes(v))ids.push(v);return ids}}
function v5StageControls(u,r,facetId){{const ids=v5ConceptIds(u,r,facetId);if(ids.length<2)return"";const spec=v5FacetSpec(u,facetId)||{{}};const cfg=r.v5_facet_stage?.[facetId]||{{}};const mode=cfg.mode||"";const order=cfg.order||"";const strict=spec.cardinality==="zero_or_one";let html=`<div class="v5stages"><h4>${{strict?"These choices cannot describe the same bounded stage/window.":"Do these choices describe the same bounded moment/stage, or distinct ones?"}}</h4><div class="relationchoice">${{strict?"":`<label><input type="radio" data-v5-stage-mode="${{esc(facetId)}}" value="same" ${{mode==="same"?"checked":""}}> <span><b>Same stage</b><br><span class="hint">They are co-present; no order is implied.</span></span></label>`}}<label><input type="radio" data-v5-stage-mode="${{esc(facetId)}}" value="distinct" ${{mode==="distinct"?"checked":""}}> <span><b>Distinct stages/windows</b><br><span class="hint">The exact source clearly separates them.</span></span></label></div>`;if(mode==="distinct"){{html+=`<h4>Does the exact source establish their chronology?</h4><div class="relationchoice"><label><input type="radio" data-v5-stage-order="${{esc(facetId)}}" value="unordered" ${{order==="unordered"?"checked":""}}> <span><b>No</b> — keep the stages distinct but do not invent an order.</span></label><label><input type="radio" data-v5-stage-order="${{esc(facetId)}}" value="ordered" ${{order==="ordered"?"checked":""}}> <span><b>Yes</b> — the source establishes an order.</span></label></div>`;if(order==="ordered"){{const saved=cfg.ordered_value_ids||[];html+=`<div class="orderbox"><h4>Assign the source-supported order:</h4>${{ids.map(v=>{{const rank=saved.indexOf(v)+1;return`<label class="v5rank">${{esc(v5Label(u,v))}}<select data-v5-rank-facet="${{esc(facetId)}}" data-v5-rank-value="${{esc(v)}}"><option value="">Choose position…</option>${{ids.map((_,i)=>`<option value="${{i+1}}" ${{rank===i+1?"selected":""}}>${{i+1}}</option>`).join("")}}</select></label>`}}).join("")}}</div>`}}}}return html+"</div>"}}
function v5ReadGates(selectorValue){{const out={{}};document.querySelectorAll(`[data-v5-gate-value="${{CSS.escape(selectorValue)}}"]`).forEach(x=>out[x.dataset.v5GateKey]=x.value||"unclear");return out}}
function v5ReadFacetStages(u,r){{const out={{}};for(const [fid] of v5FacetEntries(u)){{const ids=v5ConceptIds(u,r,fid);if(ids.length<2)continue;const mode=document.querySelector(`[data-v5-stage-mode="${{CSS.escape(fid)}}"]:checked`)?.value||"";const order=document.querySelector(`[data-v5-stage-order="${{CSS.escape(fid)}}"]:checked`)?.value||"";const ranked=[];if(order==="ordered"){{document.querySelectorAll(`[data-v5-rank-facet="${{CSS.escape(fid)}}"]`).forEach(x=>{{const n=Number(x.value);if(n)ranked.push([n,x.dataset.v5RankValue])}});ranked.sort((a,b)=>a[0]-b[0])}}out[fid]={{mode,order,ordered_value_ids:ranked.map(x=>x[1])}}}}return out}}
function v5ClaimDescriptors(u,r){{const out=[];for(const v of (r.coded_values||[])){{if(V5_HYBRIDS[v])continue;if(V5_ABSENCE[v])out.push({{key:`absence:${{v}}`,label:`Absence claim: ${{V5_ABSENCE[v].proposition}}`}});else out.push({{key:`value:${{v}}`,label:v5Label(u,v)}})}}for(const [v,d] of Object.entries(r.v5_hybrid_components||{{}}))if(d.affirmative_selected){{out.push({{key:`hybrid-positive:${{v}}`,label:`Affirmative fact: ${{V5_HYBRIDS[v].affirmative}}`}});out.push({{key:`hybrid-absence:${{v}}`,label:`Absence assessment: ${{V5_HYBRIDS[v].absence}}`}})}}return out}}
function v5ReadClaimSources(u,r){{const out={{}};document.querySelectorAll('[data-v5-source-key]:checked').forEach(x=>{{const k=x.dataset.v5SourceKey;if(!out[k])out[k]=[];out[k].push(x.value)}});if((u.task.exact_source_segments||[]).length===1){{const id=u.task.exact_source_segments[0].segment_id;for(const c of v5ClaimDescriptors(u,r))out[c.key]=[id]}}return out}}
function v5TransientRerender(u){{const d=readForm(u);renderObserved(u,d);renderSources(u,d)}}
function v5Slug(s){{return String(s).toLowerCase().replace(/[^a-z0-9]+/g,"_").replace(/^_+|_+$/g,"").slice(0,96)||"absence"}}
function v5SourceMap(u,r){{const all=u.task.exact_source_segments||[];const records=all.map((s,i)=>({{source_provenance_id:`prov-${{i+1}}`,source_record_id:s.segment_id,locator:"exact source segment",exact_text_available:true}}));const byId=new Map(records.map(x=>[x.source_record_id,x.source_provenance_id]));const refs=key=>{{let raw=(r.v5_claim_sources?.[key]||[]).filter(x=>byId.has(x));if(!raw.length&&all.length===1)raw=[all[0].segment_id];return raw.map(x=>byId.get(x))}};return{{records,refs}}}}
function v5BuildGraph(u,r){{if(r.state!=="observed")return{{schema_version:"life-patterns-observable-response-v5",response_id:`v5-${{u.key}}`,observable_id:u.obs.observable_id,response_scope_id:u.kind==="episode"?u.task.episode_id:u.task.series_id,state:r.state,facet_groups:[],value_assertions:[],component_assertions:[],absence_conditions:[],source_provenance_records:[],measurement_windows:[],event_stages:[],temporal_edges:[],evidence_units:[],development_only:true,validation_use_forbidden:true}};const sm=v5SourceMap(u,r);const parentValues=[...(r.coded_values||[])];const hybridDrafts=r.v5_hybrid_components||{{}};const concepts=[];for(const v of parentValues)if(!concepts.includes(v))concepts.push(v);for(const [v,d] of Object.entries(hybridDrafts))if(d.affirmative_selected&&!concepts.includes(v))concepts.push(v);const byFacet=new Map();for(const v of concepts){{const f=v5FacetForValue(u,v);if(!f)continue;if(!byFacet.has(f))byFacet.set(f,[]);byFacet.get(f).push(v)}}let stageN=1,groupN=1,assertN=1,compN=1,absenceN=1,windowN=1;const baseStage="stage-1";const valueStage={{}};const facetCfg=r.v5_facet_stage||{{}};const orderedEdges=[];for(const [fid,ids] of byFacet){{const cfg=facetCfg[fid]||{{}};if(ids.length>1&&cfg.mode==="distinct"){{for(const v of ids)valueStage[v]=`stage-${{++stageN}}`;if(cfg.order==="ordered"){{const ordered=cfg.ordered_value_ids||[];for(let i=0;i<ordered.length-1;i++)orderedEdges.push([ordered[i],ordered[i+1]])}}}}else for(const v of ids)valueStage[v]=baseStage}}const stageIds=new Set(Object.values(valueStage));if(!stageIds.size&&concepts.length)stageIds.add(baseStage);const assertions=[],components=[],conditions=[],windows=[],groups=[];const stageAssertions=new Map([...stageIds].map(s=>[s,[]]));const stageComponents=new Map([...stageIds].map(s=>[s,[]]));const stageSources=new Map([...stageIds].map(s=>[s,new Set()]));const assertionByValue={{}};const windowByFacetScope=new Map();function addSources(stage,refs){{if(!stageSources.has(stage))stageSources.set(stage,new Set());for(const p of refs)stageSources.get(stage).add(p)}}function facetGroup(fid,stage,valueId){{const spec=v5FacetSpec(u,fid)||{{cardinality:"zero_one_or_multiple",cardinality_scope:{{scope_type:"event_stage"}}}};const cfg=facetCfg[fid]||{{}};const distinct=(byFacet.get(fid)||[]).length>1&&cfg.mode==="distinct";const key=`${{fid}}|${{distinct?stage:"shared"}}`;let existing=groups.find(g=>g._key===key);if(existing)return existing;let scope;if(spec.cardinality_scope?.scope_type==="measurement_window"){{const wkey=`facet|${{key}}`;let wid=windowByFacetScope.get(wkey);if(!wid){{wid=`window-${{windowN++}}`;windowByFacetScope.set(wkey,wid);windows.push({{window_id:wid,window_kind:spec.cardinality_scope.window_kind,event_stage_ids:distinct?[stage]:[...new Set((byFacet.get(fid)||[]).map(v=>valueStage[v]||baseStage))],source_provenance_ids:[]}})}}scope={{scope_type:"measurement_window",window_id:wid}}}}else scope={{scope_type:"event_stage",event_stage_id:stage}};const allowed=Array.isArray(spec.value_ids)?spec.value_ids:[...(u.obs.allowed_values||[])];existing={{_key:key,facet_group_id:`fg-${{groupN++}}`,facet_id:fid,state:"insufficient",cardinality:spec.cardinality||"zero_one_or_multiple",cardinality_scope:scope,allowed_value_ids:allowed,assertion_ids:[]}};groups.push(existing);return existing}}function absenceWindow(valueId,stage,refs,group){{const spec=V5_ABSENCE[valueId];const groupWindow=group.cardinality_scope?.scope_type==="measurement_window"?windows.find(w=>w.window_id===group.cardinality_scope.window_id):null;if(groupWindow&&groupWindow.window_kind===spec.window_kind){{for(const p of refs)if(!groupWindow.source_provenance_ids.includes(p))groupWindow.source_provenance_ids.push(p);return groupWindow.window_id}}const wid=`window-${{windowN++}}`;windows.push({{window_id:wid,window_kind:spec.window_kind,event_stage_ids:[stage],source_provenance_ids:[...refs]}});return wid}}for(const v of concepts){{const fid=v5FacetForValue(u,v);if(!fid)continue;const stage=valueStage[v]||baseStage;if(!stageAssertions.has(stage))stageAssertions.set(stage,[]);if(!stageComponents.has(stage))stageComponents.set(stage,[]);if(!stageSources.has(stage))stageSources.set(stage,new Set());const group=facetGroup(fid,stage,v);const hybrid=V5_HYBRIDS[v];const pureAbs=!hybrid&&V5_ABSENCE[v];if(hybrid){{const d=hybridDrafts[v]||{{}};if(!d.affirmative_selected)continue;const posRefs=sm.refs(`hybrid-positive:${{v}}`),absRefs=sm.refs(`hybrid-absence:${{v}}`);const posId=`comp-${{compN++}}`,absId=`comp-${{compN++}}`,condId=`absence-${{absenceN++}}`;const gate=d.absence_gate||{{}};const absenceObserved=v5GateComplete(gate);const parentSelected=parentValues.includes(v)&&absenceObserved;let parentId=null;if(parentSelected){{parentId=`assert-${{assertN++}}`;assertions.push({{assertion_id:parentId,value_id:v,facet_id:fid,facet_group_id:group.facet_group_id,event_stage_id:stage,evidence_unit_id:"eu-1",component_assertion_ids:[posId,absId],source_provenance_ids:[...new Set([...posRefs,...absRefs])],specificity_disposition:"direct"}});group.assertion_ids.push(parentId);group.state="observed";stageAssertions.get(stage).push(parentId);assertionByValue[v]=parentId}}components.push({{component_assertion_id:posId,parent_value_id:v,facet_id:fid,facet_group_id:group.facet_group_id,event_stage_id:stage,evidence_unit_id:"eu-1",component_role:"affirmative",state:"observed",proposition:hybrid.affirmative,source_provenance_ids:posRefs,absence_condition_id:null}});components.push({{component_assertion_id:absId,parent_value_id:v,facet_id:fid,facet_group_id:group.facet_group_id,event_stage_id:stage,evidence_unit_id:"eu-1",component_role:"absence",state:absenceObserved?"observed":"insufficient",proposition:hybrid.absence,source_provenance_ids:absenceObserved?absRefs:[],absence_condition_id:condId}});stageComponents.get(stage).push(posId,absId);addSources(stage,[...posRefs,...absRefs]);const wid=absenceWindow(v,stage,absRefs,group);conditions.push({{absence_condition_id:condId,qualified_assertion_id:parentId,qualified_component_id:absId,absent_actor:"narrator",absent_proposition_id:v5Slug(hybrid.absence),absent_proposition:hybrid.absence,window_id:wid,awareness:gate.awareness||"unclear",opportunity:gate.opportunity||"unclear",feasibility:gate.feasibility||"unclear",established_nonoccurrence:gate.established_nonoccurrence||"unclear",source_provenance_ids:absRefs}})}}else if(pureAbs){{if(!parentValues.includes(v))continue;const refs=sm.refs(`absence:${{v}}`),compId=`comp-${{compN++}}`,condId=`absence-${{absenceN++}}`,parentId=`assert-${{assertN++}}`;const gate=r.v5_absence_gates?.[v]||{{}};assertions.push({{assertion_id:parentId,value_id:v,facet_id:fid,facet_group_id:group.facet_group_id,event_stage_id:stage,evidence_unit_id:"eu-1",component_assertion_ids:[compId],source_provenance_ids:refs,specificity_disposition:"direct"}});components.push({{component_assertion_id:compId,parent_value_id:v,facet_id:fid,facet_group_id:group.facet_group_id,event_stage_id:stage,evidence_unit_id:"eu-1",component_role:"absence",state:"observed",proposition:pureAbs.proposition,source_provenance_ids:refs,absence_condition_id:condId}});group.assertion_ids.push(parentId);group.state="observed";stageAssertions.get(stage).push(parentId);stageComponents.get(stage).push(compId);assertionByValue[v]=parentId;addSources(stage,refs);const wid=absenceWindow(v,stage,refs,group);conditions.push({{absence_condition_id:condId,qualified_assertion_id:parentId,qualified_component_id:compId,absent_actor:"narrator",absent_proposition_id:v5Slug(pureAbs.proposition),absent_proposition:pureAbs.proposition,window_id:wid,awareness:gate.awareness||"unclear",opportunity:gate.opportunity||"unclear",feasibility:gate.feasibility||"unclear",established_nonoccurrence:gate.established_nonoccurrence||"unclear",source_provenance_ids:refs}})}}else{{if(!parentValues.includes(v))continue;const refs=sm.refs(`value:${{v}}`),parentId=`assert-${{assertN++}}`;assertions.push({{assertion_id:parentId,value_id:v,facet_id:fid,facet_group_id:group.facet_group_id,event_stage_id:stage,evidence_unit_id:"eu-1",component_assertion_ids:[],source_provenance_ids:refs,specificity_disposition:"direct"}});group.assertion_ids.push(parentId);group.state="observed";stageAssertions.get(stage).push(parentId);assertionByValue[v]=parentId;addSources(stage,refs)}}}}for(const w of windows){{if(!w.source_provenance_ids.length){{const src=new Set();for(const sid of w.event_stage_ids)for(const p of (stageSources.get(sid)||[]))src.add(p);w.source_provenance_ids=[...src]}}}}const stages=[...stageIds].map(s=>{{const a=stageAssertions.get(s)||[],c=stageComponents.get(s)||[],src=[...(stageSources.get(s)||[])];return{{event_stage_id:s,state:(a.length||c.some(id=>components.find(x=>x.component_assertion_id===id)?.state==="observed"))?"observed":"insufficient",evidence_unit_id:"eu-1",assertion_ids:a,component_assertion_ids:c,source_provenance_ids:src}}}});const edges=[];for(const [fromV,toV] of orderedEdges){{const from=valueStage[fromV],to=valueStage[toV];if(!from||!to||from===to)continue;const src=[...new Set([...(stageSources.get(from)||[]),...(stageSources.get(to)||[])])];edges.push({{from_event_stage_id:from,to_event_stage_id:to,relation:"before",source_provenance_ids:src}})}}for(const g of groups)delete g._key;const graphState=assertions.length?"observed":components.some(c=>c.state==="observed")?"insufficient":"insufficient";return{{schema_version:"life-patterns-observable-response-v5",response_id:`v5-${{u.key}}`,observable_id:u.obs.observable_id,response_scope_id:u.kind==="episode"?u.task.episode_id:u.task.series_id,state:graphState,facet_groups:groups,value_assertions:assertions,component_assertions:components,absence_conditions:conditions,source_provenance_records:sm.records,measurement_windows:windows,event_stages:stages,temporal_edges:edges,evidence_units:stages.length?[{{evidence_unit_id:"eu-1",response_scope_id:u.kind==="episode"?u.task.episode_id:u.task.series_id,event_stage_ids:stages.map(s=>s.event_stage_id),independence_class:u.kind==="episode"?"single_bounded_behavioral_occurrence":"repeated_series_self_report"}}]:[],development_only:true,validation_use_forbidden:true}}}}
function v5BuildEnvelope(u,r){{const graph=v5BuildGraph(u,r);const base={{task_id:u.task.task_id,corpus_id:u.task.corpus_id,corpus_sha256:u.task.corpus_sha256,observable_id:u.obs.observable_id,response_graph:graph,accepted_contract_review_commit:V5_REVIEW_COMMIT,development_only:true,validation_use_forbidden:true}};if(u.kind==="episode")return{{schema_version:"life-patterns-development-episode-annotation-response-v5",...base,episode_id:u.task.episode_id,transfer_summary_is_not_primary_source:true}};const observed=graph.state==="observed";return{{schema_version:"life-patterns-development-series-annotation-response-v5",...base,series_id:u.task.series_id,reported_recurrence_strength:observed?(r.reported_recurrence_strength||null):null,exception_status:observed?(r.exception_status||null):null,exception_frequency:observed?(r.exception_frequency||null):null,frequency_evidence_basis:observed?(r.frequency_evidence_basis||null):null,minimum_reported_occurrences:observed?(r.minimum_reported_occurrences||null):null,bounded_rate_or_count_description:observed?(r.bounded_rate_or_count_description||null):null,recurrence_scope_description:observed?(r.recurrence_scope_description||null):null,confirming_episode_counted_as_independent_frequency_evidence:false,series_is_recurrence_support_not_primary_episode:true,reported_recurrence_is_not_verified_true_frequency:true,summary_fields_are_not_primary_source:true}}}}
function v5DraftErrors(u,r){{const e=[];if(r.state!=="observed")return e;const active=v5ClaimDescriptors(u,r);if(!active.length)e.push("Choose at least one substantive behavior or affirmative component, or use Not enough information.");for(const c of active)if(!(r.v5_claim_sources?.[c.key]||[]).length)e.push(`Choose the exact quote that supports: ${{c.label}}`);for(const v of (r.coded_values||[]))if(V5_ABSENCE[v]&&!V5_HYBRIDS[v]&&!v5GateComplete(r.v5_absence_gates?.[v]))e.push(`The selected absence behavior only counts when all four checks are Yes: ${{v5Label(u,v)}}`);for(const [fid] of v5FacetEntries(u)){{const ids=v5ConceptIds(u,r,fid);if(ids.length<2)continue;const spec=v5FacetSpec(u,fid)||{{}},cfg=r.v5_facet_stage?.[fid]||{{}};if(spec.cardinality==="zero_or_one"&&cfg.mode!=="distinct")e.push(`The selected ${{v5FacetTitle(fid)}} alternatives can both count only if the source clearly separates distinct stages/windows.`);if(spec.cardinality!=="zero_or_one"&&!['same','distinct'].includes(cfg.mode))e.push(`Say whether the selected ${{v5FacetTitle(fid)}} facts belong to the same stage or distinct stages.`);if(cfg.mode==="distinct"&&!['ordered','unordered'].includes(cfg.order))e.push(`Say whether the distinct ${{v5FacetTitle(fid)}} stages have a source-established order.`);if(cfg.mode==="distinct"&&cfg.order==="ordered"){{const ordered=cfg.ordered_value_ids||[];if(ordered.length!==ids.length||new Set(ordered).size!==ids.length||ordered.some(v=>!ids.includes(v)))e.push(`Assign each selected ${{v5FacetTitle(fid)}} fact a unique source-supported position.`)}}}}if(u.kind==="series"){{if(!r.reported_recurrence_strength)e.push("Choose how often the narrator says this behavior recurs.");if(!r.exception_status)e.push("Choose whether the narrator reports exceptions or limits.");if(r.reported_recurrence_strength==="bounded_rate_or_count"&&!r.bounded_rate_or_count_description)e.push("Enter the count or rate that the narrator actually states.")}}return e}}
function v5Download(name,text){{const blob=new Blob([text],{{type:"application/json;charset=utf-8"}}),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000)}}
function v5DownloadResponses(){{const ep=[],ser=[],issues=[];for(const u of units){{const r=responses.get(u.key);if(!r){{issues.push("Complete and save every selected unit before final V5 export.");continue}}const e=v5DraftErrors(u,r);if(e.length){{issues.push(`${{u.key}}: ${{e.join(" ")}}`);continue}}const env=v5BuildEnvelope(u,r);(u.kind==="episode"?ep:ser).push(env)}}if(issues.length){{alert("V5 export is blocked:\n\n"+issues.slice(0,8).join("\n\n")+(issues.length>8?"\n\n…":""));return}}v5Download("episode_responses.completed.v5.jsonl",ep.map(x=>JSON.stringify(x)).join("\n")+"\n");v5Download("series_responses.completed.v5.jsonl",ser.map(x=>JSON.stringify(x)).join("\n")+"\n")}}
// V5_EXPORT_HELPERS_END
'''


def patch_html_for_v5_auditor(html: str, public_semantics: Mapping[str, Any]) -> str:
    embedded_before = _embedded_fragment(html)
    html = html.replace(
        "</head>",
        """<style>
.v5facet{margin:14px 0;padding:12px 14px;border:1px solid #d7e0db;border-radius:11px;background:#fbfdfc}.v5facet>h3{margin:0 0 9px}.v5choices{display:grid;gap:8px}.v5choice{display:block;padding:10px 11px;border:1px solid #dde5e0;border-radius:9px;background:#fff}.v5hybrid,.v5absencechoice{display:grid;gap:8px}.v5absence{margin:7px 0 0 24px;padding:10px 12px;border-left:3px solid #cbd8d1;background:#f7faf8}.v5gate{display:grid;gap:7px}.v5gateitem{display:grid;grid-template-columns:minmax(0,1fr) minmax(130px,190px);gap:10px;align-items:center}.v5stages{margin:11px 0 0;padding:10px 12px;border:1px dashed #cbd8d1;border-radius:9px}.v5stages h4{margin:4px 0 8px}.v5rank{display:grid;grid-template-columns:minmax(0,1fr) 160px;gap:10px;align-items:center;padding:5px 0}.v5claims{display:grid;gap:9px}.v5claim{padding:10px 11px;border:1px solid #d8e2dc;border-radius:9px;background:#f8fbf9}.v5export{margin:18px auto;max-width:980px;padding:14px 16px;border:2px solid #70877b;border-radius:12px;background:#f4f8f6}.v5export h2{margin-top:0}.v5export button{font-weight:700}
</style>
</head>""",
        1,
    )
    helpers = _v5_helpers(public_semantics)
    marker = "\nconst attestQs="
    if marker not in html:
        raise ValueError("V5 UI patch cannot locate final-auditor helper insertion point")
    html = html.replace(marker, helpers + marker, 1)

    html = _replace_function(
        html,
        "renderSources",
        r'''function renderSources(u,r){const segments=u.task.exact_source_segments||[];const quoteName=i=>segments.length===1?"Exact quote":`Exact quote ${i+1}`;const quoteText=s=>s.exact_text||s.exact_participant_text||"";const cards=segments.map((s,i)=>`<article class="source"><div class="sourceid">${esc(quoteName(i))}</div><p>${esc(quoteText(s))}</p></article>`).join("");if(r.state!=="observed"){$("sources").innerHTML=cards;return}const claims=v5ClaimDescriptors(u,r);if(segments.length<=1||!claims.length){$("sources").innerHTML=cards;return}const saved=r.v5_claim_sources||{};const selectors=`<div class="provenancebox"><h3>Which exact quote supports each selected claim?</h3><p class="hint">This is claim-specific source bookkeeping. Choose only quote text that actually supports that claim.</p><div class="v5claims">${claims.map(c=>`<div class="v5claim"><b>${esc(c.label)}</b><div class="provenancelist">${segments.map((s,i)=>`<label><input type="checkbox" data-v5-source-key="${esc(c.key)}" value="${esc(s.segment_id)}" ${(saved[c.key]||[]).includes(s.segment_id)?"checked":""}> <span><span class="quotelabel">${esc(quoteName(i))}</span><span class="quotesnippet">${esc(quoteText(s))}</span></span></label>`).join("")}</div></div>`).join("")}</div></div>`;$("sources").innerHTML=cards+selectors}''',
    )
    html = _replace_function(
        html,
        "renderObserved",
        r'''function renderObserved(u,r){const host=$("observedFields");if(r.state!=="observed"){host.innerHTML='<div class="section"><p class="hint">No substantive behavior is selected for this unit.</p></div>';return}const facets=v5FacetEntries(u);let html='<div class="section"><h3>Which behavior does the exact source show?</h3><p class="hint">Choices are separated by behavioral dimension. Different dimensions may describe the same stage without implying an order.</p>';for(const [fid,values] of facets){html+=`<div class="v5facet"><h3>${esc(v5FacetTitle(fid))}</h3><div class="v5choices">${values.map(v=>V5_HYBRIDS[v]?v5HybridCard(u,v,r):V5_ABSENCE[v]?v5AbsenceCard(u,v,r):v5NormalCard(u,v,r)).join("")}</div>${v5StageControls(u,r,fid)}</div>`}html+='</div>';if(u.kind==="series")html+=seriesFields(r);host.innerHTML=html;host.querySelectorAll('[data-value],[data-v5-hybrid-positive],[data-v5-gate-value],[data-v5-stage-mode],[data-v5-stage-order]').forEach(x=>x.addEventListener("change",()=>v5TransientRerender(u)));$("recurrenceStrength")?.addEventListener("change",()=>v5TransientRerender(u));$("exceptionStatus")?.addEventListener("change",()=>v5TransientRerender(u))}''',
    )
    html = _replace_function(
        html,
        "readForm",
        r'''function readForm(u){const base=draftFromFormSeed(u);base.state=document.querySelector('input[name="state"]:checked')?.value||null;base.counterevidence_source_segment_ids=[];base.context_qualifiers=[];base.missingness_flags=[];base.life_phase_qualifier=null;base.annotation_note=null;if(u.kind==="episode"){base.language=null;base.influence_relation="none_reported";base.influence_source_segment_ids=[]}base.v5_hybrid_components={};base.v5_absence_gates={};let vals=selectedValues();document.querySelectorAll('[data-v5-hybrid-positive]:checked').forEach(x=>{const v=x.dataset.v5HybridPositive,g=v5ReadGates(v);base.v5_hybrid_components[v]={affirmative_selected:true,absence_gate:g};if(v5GateComplete(g)&&!vals.includes(v))vals.push(v)});for(const v of vals)if(V5_ABSENCE[v]&&!V5_HYBRIDS[v])base.v5_absence_gates[v]=v5ReadGates(v);base.coded_values=vals;base.value_relation=null;base.asserts_non_action=false;base.non_action_gate=null;base.v5_facet_stage=v5ReadFacetStages(u,base);base.v5_claim_sources=v5ReadClaimSources(u,base);base.supporting_source_segment_ids=[...new Set(Object.values(base.v5_claim_sources).flat())];base.other_specified_description=null;if(base.state!=="observed")return base;if(u.kind==="series"){base.reported_recurrence_strength=$("recurrenceStrength")?.value||null;base.exception_status=$("exceptionStatus")?.value||null;base.exception_frequency=base.exception_status==="exceptions_explicitly_denied"?"none_reported":base.exception_status==="exceptions_reported"?($("exceptionFrequency")?.value||"unknown"):null;base.frequency_evidence_basis=base.reported_recurrence_strength==="bounded_rate_or_count"?"bounded_rate_or_count_self_report":"generalized_self_report";base.minimum_reported_occurrences=null;base.bounded_rate_or_count_description=base.reported_recurrence_strength==="bounded_rate_or_count"?($("boundedDescription")?.value.trim()||null):null;base.recurrence_scope_description=null}return base}''',
    )
    html = _replace_function(
        html,
        "validate",
        r'''function validate(u,r){const sourceIds=new Set((u.task.exact_source_segments||[]).map(s=>s.segment_id));for(const ids of Object.values(r.v5_claim_sources||{}))for(const id of ids)if(!sourceIds.has(id))return["This saved response no longer matches this unit. Stop and report the technical problem."];if(!["observed","insufficient","not_applicable"].includes(r.state))return["Choose Yes, Doesn't apply to this story, or Not enough information."];return v5DraftErrors(u,r)}''',
    )

    install = r'''
function v5InstallExportPanel(){for(const el of document.querySelectorAll('button,a')){const t=(el.textContent||"").toLowerCase();if(t.includes("download")&&t.includes("response")&&!t.includes("progress")&&!t.includes("attestation"))el.style.display="none"}const panel=document.createElement("section");panel.className="v5export";panel.innerHTML='<h2>Final V5 response export</h2><p>Use this export for the completed calibration. It converts your human judgments into the accepted V5 facet/stage/provenance graph automatically. Machine IDs remain hidden from the annotation task.</p><button type="button" id="v5DownloadResponses">Download V5 response files</button><p class="hint">Also download the existing auditor attestation. The attestation format is unchanged.</p>';document.body.appendChild(panel);panel.querySelector("#v5DownloadResponses").addEventListener("click",v5DownloadResponses)}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",v5InstallExportPanel);else v5InstallExportPanel();
'''
    end_marker = "\n</script>"
    if end_marker not in html:
        raise ValueError("V5 UI patch cannot locate script terminator")
    html = html.replace(end_marker, install + end_marker, 1)

    if _embedded_fragment(html) != embedded_before:
        raise ValueError("V5 auditor UI patch altered embedded private handoff bytes")
    outside = html.replace(_embedded_fragment(html), "")
    required = (
        "Final V5 response export",
        "episode_responses.completed.v5.jsonl",
        "series_responses.completed.v5.jsonl",
        "v5BuildEnvelope",
        "v5_hybrid_components",
        "Which exact quote supports each selected claim?",
        "Does the exact source establish their chronology?",
    )
    for text in required:
        if text not in outside:
            raise ValueError(f"V5 auditor UI is missing required behavior: {text}")
    for forbidden in (
        "If more than one behavior is selected, how do they relate?",
        "Partially",
    ):
        if forbidden in outside:
            raise ValueError(f"V5 auditor UI still exposes obsolete/global behavior: {forbidden}")
    return html


def build_human_calibration_ui_v5(
    handoff_zip: str | Path,
    output_html: str | Path,
    *,
    overwrite: bool = False,
) -> dict[str, Any]:
    output = Path(output_html)
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")
    public_semantics = load_public_v5_semantics()
    with tempfile.TemporaryDirectory(prefix="life-patterns-ui-v5-") as temporary:
        previous = Path(temporary) / "final-v2.html"
        base_receipt = build_final_auditor_ui_v2(handoff_zip, previous)
        before = previous.read_text(encoding="utf-8")
        after = patch_html_for_v5_auditor(before, public_semantics)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(after, encoding="utf-8", newline="\n")
    raw = output.read_bytes()
    receipt = dict(base_receipt)
    receipt.update(
        schema_version="life-patterns-human-calibration-ui-build-receipt-v5",
        accepted_contract_schema=EXPECTED_CONTRACT_SCHEMA,
        accepted_contract_version=EXPECTED_CONTRACT_VERSION,
        accepted_contract_review_commit=EXPECTED_REVIEW_COMMIT,
        output_html_sha256=hashlib.sha256(raw).hexdigest(),
        output_html_bytes=len(raw),
        historical_v2_builder_modified=False,
        human_choices_grouped_by_facet=True,
        global_value_relation_removed=True,
        hybrid_affirmative_absence_separated=True,
        partial_hybrid_affirmative_preserved=True,
        claim_specific_provenance=True,
        stage_questions_same_facet_only=True,
        chronology_requires_explicit_human_support=True,
        final_response_export_version="v5",
        auditor_attestation_format_changed=False,
        embedded_private_handoff_unchanged=True,
        selected_calibration_units_changed=False,
        recurrence_v2_semantics_preserved=True,
        target_model_information_used=False,
        automated_judgment_used=False,
        network_requests_required=False,
        development_only=True,
        validation_use_forbidden=True,
        owner_usability_review_required_before_collection=True,
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-zip", type=Path, required=True)
    parser.add_argument("--output-html", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    receipt = build_human_calibration_ui_v5(
        args.handoff_zip,
        args.output_html,
        overwrite=args.overwrite,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
