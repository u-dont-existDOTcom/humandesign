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
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

from build_life_patterns_human_calibration_ui_v2_auditor_final import (
    _embedded_fragment,
    _replace_function,
    build_final_auditor_ui_v2,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT / "state" / "LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json"
)
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
        "proposition": (
            "absence of concrete preparation during the named feasible pre-action window"
        ),
        "window_kind": "preaction_window",
    },
    "R08-c": {
        "proposition": (
            "no task-directed start by the narrator's previously stated intended start point"
        ),
        "window_kind": "action_window",
    },
    "R08-f": {
        "proposition": "no task-directed start during the named feasible action window",
        "window_kind": "action_window",
    },
    "R10-k": {
        "proposition": (
            "no action on either competing course during the named feasible allocation interval"
        ),
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
        "proposition": (
            "no defined endpoint component completed during the named"
            " feasible endpoint assessment window"
        ),
        "window_kind": "endpoint_assessment_window",
    },
    "R16-l": {
        "proposition": "no help request during the named feasible request opportunity",
        "window_kind": "request_opportunity_window",
    },
    "R17-h": {
        "proposition": (
            "no coordination with the relevant party during the named"
            " feasible coordination opportunity"
        ),
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
    return (
        "\n"
        rf"""// V5_EXPORT_HELPERS_START"""
        "\n"
        rf"""const V5_PUBLIC={public_json};"""
        "\n"
        rf'''const V5_REVIEW_COMMIT="{EXPECTED_REVIEW_COMMIT}";'''
        "\n"
        rf"""const V5_HYBRIDS=V5_PUBLIC.hybrid_value_components||{{}};"""
        "\n"
        rf"""const V5_ABSENCE=V5_PUBLIC.absence_specs||{{}};"""
        "\n"
        rf"""function v5FacetTitle(id){{if(id==="substantive_response")return"""
        rf""""Behavior";return String(id||"").replaceAll("_"," """
        rf"""").replace(/\b\w/g,c=>c.toUpperCase())}}"""
        "\n"
        rf"""function v5Profile(u){{return """
        rf"""V5_PUBLIC.observable_facet_profiles[u.obs.observable_id]||V5_PUB"""
        rf"""LIC.default_observable_profile}}"""
        "\n"
        rf"""function v5FacetSpec(u,facetId){{return """
        rf"""v5Profile(u)?.facets?.[facetId]||null}}"""
        "\n"
        rf"""function v5FacetForValue(u,valueId){{const p=v5Profile(u),"""
        rf"""facets=p?.facets||{{}};for(const [fid,spec] of """
        rf"""Object.entries(facets)){{if(Array.isArray(spec.value_ids)&&spec."""
        rf"""value_ids.includes(valueId))return """
        rf"""fid}}if(p===V5_PUBLIC.default_observable_profile||Object.keys(fa"""
        rf"""cets).length===1&&facets.substantive_response)return"substantive"""
        rf"""_response";return null}}"""
        "\n"
        rf"""function v5FacetEntries(u){{const out=new Map();for(const v of """
        rf"""(u.obs.allowed_values||[])){{const fid=v5FacetForValue(u,v);"""
        rf"""if(!fid)continue;if(!out.has(fid))out.set(fid,[]);"""
        rf"""out.get(fid).push(v)}}return out}}"""
        "\n"
        rf"""function v5SubcodeMap(u){{return new """
        rf"""Map((u.resolved?.subcodes||[]).map(s=>[s.subcode_id,s]))}}"""
        "\n"
        rf"""function v5Label(u,v){{const s=v5SubcodeMap(u).get(v);return """
        rf"""plainBehavior(s?.wording,v)}}"""
        "\n"
        rf"""function v5GateComplete(g){{return !!g&&["awareness","""
        rf""""opportunity","feasibility","""
        rf""""established_nonoccurrence"].every(k=>g[k]==="established")}}"""
        "\n"
        rf"""function v5GateSelect(valueId,key,current){{const """
        rf"""labels={{awareness:"Was the narrator aware of the relevant """
        rf"""action or requirement?",opportunity:"Was there a real """
        rf"""opportunity for it?",feasibility:"Was it feasible in that """
        rf"""opportunity?",established_nonoccurrence:"Does the exact source """
        rf"""establish that it did not happen, rather than merely fail to """
        rf"""mention it?"}};const opts=[["","Choose…"],["established","Yes"],"""
        rf"""["not_established","No"],["unclear","Can't tell"]];return`<label """
        rf"""class="v5gateitem">${{esc(labels[key])}}<select """
        rf"""data-v5-gate-value="${{esc(valueId)}}" """
        rf"""data-v5-gate-key="${{esc(key)}}">${{opts.map(([v,l])=>`<option """
        rf"""value="${{v}}" ${{current===v?"selected":""}}>${{l}}</option>`)."""
        rf"""join("")}}</select></label>`}}"""
        "\n"
        rf"""function v5GateBlock(valueId,r,proposition,hybrid){{const """
        rf"""g=(hybrid?r.v5_hybrid_components?.[valueId]?.absence_gate:r.v5_a"""
        rf"""bsence_gates?.[valueId])||{{}};return`<div """
        rf"""class="v5absence"><p><b>Separate absence claim:</b> """
        rf"""${{esc(proposition)}}</p><p class="hint">The absence counts only """
        rf"""when all four answers are Yes. Silence or missing detail is not """
        rf"""a No-action finding.</p><div class="v5gate">${{["awareness","""
        rf""""opportunity","feasibility","""
        rf""""established_nonoccurrence"].map(k=>v5GateSelect(valueId,k,"""
        rf"""g[k]||"")).join("")}}</div>${{hybrid?'<p class="hint">If these """
        rf"""checks are not all Yes, the affirmative fact is retained but the """
        rf"""combined value is not asserted.</p>':""}}</div>`}}"""
        "\n"
        rf"""function v5HybridCard(u,v,r){{const h=V5_HYBRIDS[v];const """
        rf"""saved=r.v5_hybrid_components?.[v]||{{}};const """
        rf"""positive=!!saved.affirmative_selected||((r.coded_values||[]).inc"""
        rf"""ludes(v));return`<div class="v5choice v5hybrid"><label><input """
        rf"""type="checkbox" data-v5-hybrid-positive="${{esc(v)}}" """
        rf"""${{positive?"checked":""}}> <span><b>Source shows:</b> """
        rf"""${{esc(h.affirmative)}}</span></label>${{positive?v5GateBlock(v,"""
        rf"""r,h.absence,true):`<p class="hint">The combined value also """
        rf"""requires a separately established absence: """
        rf"""${{esc(h.absence)}}.</p>`}}</div>`}}"""
        "\n"
        rf"""function v5AbsenceCard(u,v,r){{const """
        rf"""selected=(r.coded_values||[]).includes(v);const label=v5Label(u,"""
        rf"""v);return`<div class="v5choice v5absencechoice"><label><input """
        rf"""type="checkbox" data-value="${{esc(v)}}" """
        rf"""${{selected?"checked":""}}> """
        rf"""<span>${{esc(label)}}</span></label>${{selected?v5GateBlock(v,r,"""
        rf"""V5_ABSENCE[v].proposition,false):""}}</div>`}}"""
        "\n"
        rf"""function v5NormalCard(u,v,r){{const """
        rf"""selected=(r.coded_values||[]).includes(v);return`<label """
        rf"""class="v5choice"><input type="checkbox" data-value="${{esc(v)}}" """
        rf"""${{selected?"checked":""}}> <span>${{esc(v5Label(u,"""
        rf"""v))}}</span></label>`}}"""
        "\n"
        rf"""function v5ConceptIds(u,r,facetId){{const ids=[];for(const v of """
        rf"""(r.coded_values||[]))if(v5FacetForValue(u,"""
        rf"""v)===facetId&&!ids.includes(v))ids.push(v);for(const [v,d] of """
        rf"""Object.entries(r.v5_hybrid_components||{{}}))if(d.affirmative_se"""
        rf"""lected&&v5FacetForValue(u,"""
        rf"""v)===facetId&&!ids.includes(v))ids.push(v);return ids}}"""
        "\n"
        rf"""function v5StageControls(u,r,facetId){{const ids=v5ConceptIds(u,"""
        rf"""r,facetId);if(ids.length<2)return"";const spec=v5FacetSpec(u,"""
        rf"""facetId)||{{}};const cfg=r.v5_facet_stage?.[facetId]||{{}};const """
        rf"""mode=cfg.mode||"";const order=cfg.order||"";const """
        rf"""strict=spec.cardinality==="zero_or_one";let html=`<div """
        rf"""class="v5stages"><h4>${{strict?"These choices cannot describe """
        rf"""the same bounded stage/window.":"Do these choices describe the """
        rf"""same bounded moment/stage, or distinct ones?"}}</h4><div """
        rf"""class="relationchoice">${{strict?"":`<label><input type="radio" """
        rf"""data-v5-stage-mode="${{esc(facetId)}}" value="same" """
        rf"""${{mode==="same"?"checked":""}}> <span><b>Same """
        rf"""stage</b><br><span class="hint">They are co-present; no order is """
        rf"""implied.</span></span></label>`}}<label><input type="radio" """
        rf"""data-v5-stage-mode="${{esc(facetId)}}" value="distinct" """
        rf"""${{mode==="distinct"?"checked":""}}> <span><b>Distinct """
        rf"""stages/windows</b><br><span class="hint">The exact source """
        rf"""clearly separates them.</span></span></label></div>`;"""
        rf"""if(mode==="distinct"){{html+=`<h4>Does the exact source """
        rf"""establish their chronology?</h4><div """
        rf"""class="relationchoice"><label><input type="radio" """
        rf"""data-v5-stage-order="${{esc(facetId)}}" value="unordered" """
        rf"""${{order==="unordered"?"checked":""}}> <span><b>No</b> — keep """
        rf"""the stages distinct but do not invent an """
        rf"""order.</span></label><label><input type="radio" """
        rf"""data-v5-stage-order="${{esc(facetId)}}" value="ordered" """
        rf"""${{order==="ordered"?"checked":""}}> <span><b>Yes</b> — the """
        rf"""source establishes an order.</span></label></div>`;"""
        rf"""if(order==="ordered"){{const saved=cfg.ordered_value_ids||[];"""
        rf"""html+=`<div class="orderbox"><h4>Assign the source-supported """
        rf"""order:</h4>${{ids.map(v=>{{const rank=saved.indexOf(v)+1;"""
        rf"""return`<label class="v5rank">${{esc(v5Label(u,v))}}<select """
        rf"""data-v5-rank-facet="${{esc(facetId)}}" """
        rf"""data-v5-rank-value="${{esc(v)}}"><option value="">Choose """
        rf"""position…</option>${{ids.map((_,i)=>`<option value="${{i+1}}" """
        rf"""${{rank===i+1?"selected":""}}>${{i+1}}</option>`).join("")}}</se"""
        rf"""lect></label>`}}).join("")}}</div>`}}}}return html+"</div>"}}"""
        "\n"
        rf"""function v5ReadGates(selectorValue){{const out={{}};"""
        rf"""document.querySelectorAll(`[data-v5-gate-value="${{CSS.escape(se"""
        rf"""lectorValue)}}"]`).forEach(x=>out[x.dataset.v5GateKey]=x.value||"""
        rf""""unclear");return out}}"""
        "\n"
        rf"""function v5ReadFacetStages(u,r){{const out={{}};for(const [fid] """
        rf"""of v5FacetEntries(u)){{const ids=v5ConceptIds(u,r,fid);"""
        rf"""if(ids.length<2)continue;const """
        rf"""mode=document.querySelector(`[data-v5-stage-mode="${{CSS.escape("""
        rf"""fid)}}"]:checked`)?.value||"";const """
        rf"""order=document.querySelector(`[data-v5-stage-order="${{CSS.escap"""
        rf"""e(fid)}}"]:checked`)?.value||"";const ranked=[];"""
        rf"""if(order==="ordered"){{document.querySelectorAll(`[data-v5-rank-"""
        rf"""facet="${{CSS.escape(fid)}}"]`).forEach(x=>{{const """
        rf"""n=Number(x.value);if(n)ranked.push([n,x.dataset.v5RankValue])}});"""
        rf"""ranked.sort((a,b)=>a[0]-b[0])}}out[fid]={{mode,order,"""
        rf"""ordered_value_ids:ranked.map(x=>x[1])}}}}return out}}"""
        "\n"
        rf"""function v5ClaimDescriptors(u,r){{const out=[];for(const v of """
        rf"""(r.coded_values||[])){{if(V5_HYBRIDS[v])continue;"""
        rf"""if(V5_ABSENCE[v])out.push({{key:`absence:${{v}}`,label:`Absence """
        rf"""claim: ${{V5_ABSENCE[v].proposition}}`}});else """
        rf"""out.push({{key:`value:${{v}}`,label:v5Label(u,v)}})}}for(const """
        rf"""[v,d] of Object.entries(r.v5_hybrid_components||{{}}))if(d.affir"""
        rf"""mative_selected){{out.push({{key:`hybrid-positive:${{v}}`,"""
        rf"""label:`Affirmative fact: ${{V5_HYBRIDS[v].affirmative}}`}});"""
        rf"""out.push({{key:`hybrid-absence:${{v}}`,label:`Absence """
        rf"""assessment: ${{V5_HYBRIDS[v].absence}}`}})}}return out}}"""
        "\n"
        rf"""function v5ReadClaimSources(u,r){{const out={{}};"""
        rf"""document.querySelectorAll('[data-v5-source-key]:checked').forEac"""
        rf"""h(x=>{{const k=x.dataset.v5SourceKey;if(!out[k])out[k]=[];"""
        rf"""out[k].push(x.value)}});if((u.task.exact_source_segments||[]).le"""
        rf"""ngth===1){{const id=u.task.exact_source_segments[0].segment_id;"""
        rf"""for(const c of v5ClaimDescriptors(u,r))out[c.key]=[id]}}return """
        rf"""out}}"""
        "\n"
        rf"""function v5TransientRerender(u){{const d=readForm(u);"""
        rf"""renderObserved(u,d);renderSources(u,d)}}"""
        "\n"
        rf"""function v5Slug(s){{return """
        rf"""String(s).toLowerCase().replace(/[^a-z0-9]+/g,"""
        rf""""_").replace(/^_+|_+$/g,"").slice(0,96)||"absence"}}"""
        "\n"
        rf"""function v5SourceMap(u,r){{const """
        rf"""all=u.task.exact_source_segments||[];const records=all.map((s,"""
        rf"""i)=>({{source_provenance_id:`prov-${{i+1}}`,"""
        rf"""source_record_id:s.segment_id,locator:"exact source segment","""
        rf"""exact_text_available:true}}));const byId=new """
        rf"""Map(records.map(x=>[x.source_record_id,x.source_provenance_id]));"""
        rf"""const refs=key=>{{let raw=(r.v5_claim_sources?.[key]||[]).filter"""
        rf"""(x=>byId.has(x));if(!raw.length&&all.length===1)raw=[all[0].segm"""
        rf"""ent_id];return raw.map(x=>byId.get(x))}};return{{records,"""
        rf"""refs}}}}"""
        "\n"
        rf"""function v5BuildGraph(u,r){{if(r.state!=="observed")return{{sche"""
        rf"""ma_version:"life-patterns-observable-response-v5","""
        rf"""response_id:`v5-${{u.key}}`,observable_id:u.obs.observable_id,"""
        rf"""response_scope_id:u.kind==="episode"?u.task.episode_id:u.task.se"""
        rf"""ries_id,state:r.state,facet_groups:[],value_assertions:[],"""
        rf"""component_assertions:[],absence_conditions:[],"""
        rf"""source_provenance_records:[],measurement_windows:[],"""
        rf"""event_stages:[],temporal_edges:[],evidence_units:[],"""
        rf"""development_only:true,validation_use_forbidden:true}};const """
        rf"""sm=v5SourceMap(u,r);const parentValues=[...(r.coded_values||[])];"""
        rf"""const hybridDrafts=r.v5_hybrid_components||{{}};const """
        rf"""concepts=[];for(const v of """
        rf"""parentValues)if(!concepts.includes(v))concepts.push(v);for(const """
        rf"""[v,d] of Object.entries(hybridDrafts))if(d.affirmative_selected&"""
        rf"""&!concepts.includes(v))concepts.push(v);const byFacet=new Map();"""
        rf"""for(const v of concepts){{const f=v5FacetForValue(u,v);"""
        rf"""if(!f)continue;if(!byFacet.has(f))byFacet.set(f,[]);"""
        rf"""byFacet.get(f).push(v)}}let stageN=1,groupN=1,assertN=1,compN=1,"""
        rf"""absenceN=1,windowN=1;const baseStage="stage-1";const """
        rf"""valueStage={{}};const facetCfg=r.v5_facet_stage||{{}};const """
        rf"""orderedEdges=[];for(const [fid,ids] of byFacet){{const """
        rf"""cfg=facetCfg[fid]||{{}};if(ids.length>1&&cfg.mode==="distinct"){{f"""
        rf"""or(const v of ids)valueStage[v]=`stage-${{++stageN}}`;"""
        rf"""if(cfg.order==="ordered"){{const """
        rf"""ordered=cfg.ordered_value_ids||[];for(let i=0;i<ordered.length-1;"""
        rf"""i++)orderedEdges.push([ordered[i],ordered[i+1]])}}}}else """
        rf"""for(const v of ids)valueStage[v]=baseStage}}const stageIds=new """
        rf"""Set(Object.values(valueStage));"""
        rf"""if(!stageIds.size&&concepts.length)stageIds.add(baseStage);const """
        rf"""assertions=[],components=[],conditions=[],windows=[],groups=[];"""
        rf"""const stageAssertions=new Map([...stageIds].map(s=>[s,[]]));"""
        rf"""const stageComponents=new Map([...stageIds].map(s=>[s,[]]));"""
        rf"""const stageSources=new Map([...stageIds].map(s=>[s,new Set()]));"""
        rf"""const assertionByValue={{}};const windowByFacetScope=new Map();"""
        rf"""function addSources(stage,"""
        rf"""refs){{if(!stageSources.has(stage))stageSources.set(stage,new """
        rf"""Set());for(const p of refs)stageSources.get(stage).add(p)}}funct"""
        rf"""ion facetGroup(fid,stage,valueId){{const spec=v5FacetSpec(u,"""
        rf"""fid)||{{cardinality:"zero_one_or_multiple","""
        rf"""cardinality_scope:{{scope_type:"event_stage"}}}};const """
        rf"""cfg=facetCfg[fid]||{{}};const """
        rf"""distinct=(byFacet.get(fid)||[]).length>1&&cfg.mode==="distinct";"""
        rf"""const key=`${{fid}}|${{distinct?stage:"shared"}}`;let """
        rf"""existing=groups.find(g=>g._key===key);if(existing)return """
        rf"""existing;let scope;if(spec.cardinality_scope?.scope_type==="meas"""
        rf"""urement_window"){{const wkey=`facet|${{key}}`;let """
        rf"""wid=windowByFacetScope.get(wkey);"""
        rf"""if(!wid){{wid=`window-${{windowN++}}`;"""
        rf"""windowByFacetScope.set(wkey,wid);windows.push({{window_id:wid,"""
        rf"""window_kind:spec.cardinality_scope.window_kind,"""
        rf"""event_stage_ids:distinct?[stage]:[...new """
        rf"""Set((byFacet.get(fid)||[]).map(v=>valueStage[v]||baseStage))],"""
        rf"""source_provenance_ids:[]}})}}scope={{scope_type:"measurement_win"""
        rf"""dow",window_id:wid}}}}else scope={{scope_type:"event_stage","""
        rf"""event_stage_id:stage}};const """
        rf"""allowed=Array.isArray(spec.value_ids)?spec.value_ids:[...(u.obs."""
        rf"""allowed_values||[])];existing={{_key:key,"""
        rf"""facet_group_id:`fg-${{groupN++}}`,facet_id:fid,"""
        rf"""state:"insufficient",cardinality:spec.cardinality||"zero_one_or_"""
        rf"""multiple",cardinality_scope:scope,allowed_value_ids:allowed,"""
        rf"""assertion_ids:[]}};groups.push(existing);return """
        rf"""existing}}function absenceWindow(valueId,stage,refs,"""
        rf"""group){{const spec=V5_ABSENCE[valueId];const """
        rf"""groupWindow=group.cardinality_scope?.scope_type==="measurement_w"""
        rf"""indow"?windows.find(w=>w.window_id===group.cardinality_scope.win"""
        rf"""dow_id):null;if(groupWindow&&groupWindow.window_kind===spec.wind"""
        rf"""ow_kind){{for(const p of """
        rf"""refs)if(!groupWindow.source_provenance_ids.includes(p))groupWind"""
        rf"""ow.source_provenance_ids.push(p);return """
        rf"""groupWindow.window_id}}const wid=`window-${{windowN++}}`;"""
        rf"""windows.push({{window_id:wid,window_kind:spec.window_kind,"""
        rf"""event_stage_ids:[stage],source_provenance_ids:[...refs]}});"""
        rf"""return wid}}for(const v of concepts){{const """
        rf"""fid=v5FacetForValue(u,v);if(!fid)continue;const """
        rf"""stage=valueStage[v]||baseStage;"""
        rf"""if(!stageAssertions.has(stage))stageAssertions.set(stage,[]);"""
        rf"""if(!stageComponents.has(stage))stageComponents.set(stage,[]);"""
        rf"""if(!stageSources.has(stage))stageSources.set(stage,new Set());"""
        rf"""const group=facetGroup(fid,stage,v);const hybrid=V5_HYBRIDS[v];"""
        rf"""const pureAbs=!hybrid&&V5_ABSENCE[v];if(hybrid){{const """
        rf"""d=hybridDrafts[v]||{{}};if(!d.affirmative_selected)continue;"""
        rf"""const posRefs=sm.refs(`hybrid-positive:${{v}}`),"""
        rf"""absRefs=sm.refs(`hybrid-absence:${{v}}`);const """
        rf"""posId=`comp-${{compN++}}`,absId=`comp-${{compN++}}`,"""
        rf"""condId=`absence-${{absenceN++}}`;const gate=d.absence_gate||{{}};"""
        rf"""const absenceObserved=v5GateComplete(gate);const """
        rf"""parentSelected=parentValues.includes(v)&&absenceObserved;let """
        rf"""parentId=null;if(parentSelected){{parentId=`assert-${{assertN++}}`"""
        rf""";assertions.push({{assertion_id:parentId,value_id:v,facet_id:fid,"""
        rf"""facet_group_id:group.facet_group_id,event_stage_id:stage,"""
        rf"""evidence_unit_id:"eu-1",component_assertion_ids:[posId,absId],"""
        rf"""source_provenance_ids:[...new Set([...posRefs,...absRefs])],"""
        rf"""specificity_disposition:"direct"}});"""
        rf"""group.assertion_ids.push(parentId);group.state="observed";"""
        rf"""stageAssertions.get(stage).push(parentId);"""
        rf"""assertionByValue[v]=parentId}}components.push({{component_assert"""
        rf"""ion_id:posId,parent_value_id:v,facet_id:fid,"""
        rf"""facet_group_id:group.facet_group_id,event_stage_id:stage,"""
        rf"""evidence_unit_id:"eu-1",component_role:"affirmative","""
        rf"""state:"observed",proposition:hybrid.affirmative,"""
        rf"""source_provenance_ids:posRefs,absence_condition_id:null}});"""
        rf"""components.push({{component_assertion_id:absId,parent_value_id:v,"""
        rf"""facet_id:fid,facet_group_id:group.facet_group_id,"""
        rf"""event_stage_id:stage,evidence_unit_id:"eu-1","""
        rf"""component_role:"absence","""
        rf"""state:absenceObserved?"observed":"insufficient","""
        rf"""proposition:hybrid.absence,"""
        rf"""source_provenance_ids:absenceObserved?absRefs:[],"""
        rf"""absence_condition_id:condId}});"""
        rf"""stageComponents.get(stage).push(posId,absId);addSources(stage,"""
        rf"""[...posRefs,...absRefs]);const wid=absenceWindow(v,stage,absRefs,"""
        rf"""group);conditions.push({{absence_condition_id:condId,"""
        rf"""qualified_assertion_id:parentId,qualified_component_id:absId,"""
        rf"""absent_actor:"narrator",absent_proposition_id:v5Slug(hybrid.abse"""
        rf"""nce),absent_proposition:hybrid.absence,window_id:wid,"""
        rf"""awareness:gate.awareness||"unclear","""
        rf"""opportunity:gate.opportunity||"unclear","""
        rf"""feasibility:gate.feasibility||"unclear","""
        rf"""established_nonoccurrence:gate.established_nonoccurrence||"uncle"""
        rf"""ar",source_provenance_ids:absRefs}})}}else """
        rf"""if(pureAbs){{if(!parentValues.includes(v))continue;const """
        rf"""refs=sm.refs(`absence:${{v}}`),compId=`comp-${{compN++}}`,"""
        rf"""condId=`absence-${{absenceN++}}`,"""
        rf"""parentId=`assert-${{assertN++}}`;const """
        rf"""gate=r.v5_absence_gates?.[v]||{{}};"""
        rf"""assertions.push({{assertion_id:parentId,value_id:v,facet_id:fid,"""
        rf"""facet_group_id:group.facet_group_id,event_stage_id:stage,"""
        rf"""evidence_unit_id:"eu-1",component_assertion_ids:[compId],"""
        rf"""source_provenance_ids:refs,specificity_disposition:"direct"}});"""
        rf"""components.push({{component_assertion_id:compId,"""
        rf"""parent_value_id:v,facet_id:fid,"""
        rf"""facet_group_id:group.facet_group_id,event_stage_id:stage,"""
        rf"""evidence_unit_id:"eu-1",component_role:"absence","""
        rf"""state:"observed",proposition:pureAbs.proposition,"""
        rf"""source_provenance_ids:refs,absence_condition_id:condId}});"""
        rf"""group.assertion_ids.push(parentId);group.state="observed";"""
        rf"""stageAssertions.get(stage).push(parentId);"""
        rf"""stageComponents.get(stage).push(compId);"""
        rf"""assertionByValue[v]=parentId;addSources(stage,refs);const """
        rf"""wid=absenceWindow(v,stage,refs,group);"""
        rf"""conditions.push({{absence_condition_id:condId,"""
        rf"""qualified_assertion_id:parentId,qualified_component_id:compId,"""
        rf"""absent_actor:"narrator",absent_proposition_id:v5Slug(pureAbs.pro"""
        rf"""position),absent_proposition:pureAbs.proposition,window_id:wid,"""
        rf"""awareness:gate.awareness||"unclear","""
        rf"""opportunity:gate.opportunity||"unclear","""
        rf"""feasibility:gate.feasibility||"unclear","""
        rf"""established_nonoccurrence:gate.established_nonoccurrence||"uncle"""
        rf"""ar",source_provenance_ids:refs}})}}else{{if(!parentValues.includ"""
        rf"""es(v))continue;const refs=sm.refs(`value:${{v}}`),"""
        rf"""parentId=`assert-${{assertN++}}`;"""
        rf"""assertions.push({{assertion_id:parentId,value_id:v,facet_id:fid,"""
        rf"""facet_group_id:group.facet_group_id,event_stage_id:stage,"""
        rf"""evidence_unit_id:"eu-1",component_assertion_ids:[],"""
        rf"""source_provenance_ids:refs,specificity_disposition:"direct"}});"""
        rf"""group.assertion_ids.push(parentId);group.state="observed";"""
        rf"""stageAssertions.get(stage).push(parentId);"""
        rf"""assertionByValue[v]=parentId;addSources(stage,refs)}}}}for(const """
        rf"""w of windows){{if(!w.source_provenance_ids.length){{const """
        rf"""src=new Set();for(const sid of w.event_stage_ids)for(const p of """
        rf"""(stageSources.get(sid)||[]))src.add(p);"""
        rf"""w.source_provenance_ids=[...src]}}}}const """
        rf"""stages=[...stageIds].map(s=>{{const a=stageAssertions.get(s)||[],"""
        rf"""c=stageComponents.get(s)||[],src=[...(stageSources.get(s)||[])];"""
        rf"""return{{event_stage_id:s,"""
        rf"""state:(a.length||c.some(id=>components.find(x=>x.component_asser"""
        rf"""tion_id===id)?.state==="observed"))?"observed":"insufficient","""
        rf"""evidence_unit_id:"eu-1",assertion_ids:a,"""
        rf"""component_assertion_ids:c,source_provenance_ids:src}}}});const """
        rf"""edges=[];for(const [fromV,toV] of orderedEdges){{const """
        rf"""from=valueStage[fromV],to=valueStage[toV];"""
        rf"""if(!from||!to||from===to)continue;const src=[...new """
        rf"""Set([...(stageSources.get(from)||[]),"""
        rf"""...(stageSources.get(to)||[])])];"""
        rf"""edges.push({{from_event_stage_id:from,to_event_stage_id:to,"""
        rf"""relation:"before",source_provenance_ids:src}})}}for(const g of """
        rf"""groups)delete g._key;const """
        rf"""graphState=assertions.length?"observed":components.some(c=>c.sta"""
        rf"""te==="observed")?"insufficient":"insufficient";"""
        rf"""return{{schema_version:"life-patterns-observable-response-v5","""
        rf"""response_id:`v5-${{u.key}}`,observable_id:u.obs.observable_id,"""
        rf"""response_scope_id:u.kind==="episode"?u.task.episode_id:u.task.se"""
        rf"""ries_id,state:graphState,facet_groups:groups,"""
        rf"""value_assertions:assertions,component_assertions:components,"""
        rf"""absence_conditions:conditions,"""
        rf"""source_provenance_records:sm.records,measurement_windows:windows,"""
        rf"""event_stages:stages,temporal_edges:edges,"""
        rf"""evidence_units:stages.length?[{{evidence_unit_id:"eu-1","""
        rf"""response_scope_id:u.kind==="episode"?u.task.episode_id:u.task.se"""
        rf"""ries_id,event_stage_ids:stages.map(s=>s.event_stage_id),"""
        rf"""independence_class:u.kind==="episode"?"single_bounded_behavioral"""
        rf"""_occurrence":"repeated_series_self_report"}}]:[],"""
        rf"""development_only:true,validation_use_forbidden:true}}}}"""
        "\n"
        rf"""function v5BuildEnvelope(u,r){{const graph=v5BuildGraph(u,r);"""
        rf"""const base={{task_id:u.task.task_id,corpus_id:u.task.corpus_id,"""
        rf"""corpus_sha256:u.task.corpus_sha256,"""
        rf"""observable_id:u.obs.observable_id,response_graph:graph,"""
        rf"""accepted_contract_review_commit:V5_REVIEW_COMMIT,"""
        rf"""development_only:true,validation_use_forbidden:true}};"""
        rf"""if(u.kind==="episode")return{{schema_version:"life-patterns-deve"""
        rf"""lopment-episode-annotation-response-v5",...base,"""
        rf"""episode_id:u.task.episode_id,"""
        rf"""transfer_summary_is_not_primary_source:true}};const """
        rf"""observed=graph.state==="observed";"""
        rf"""return{{schema_version:"life-patterns-development-series-annotat"""
        rf"""ion-response-v5",...base,series_id:u.task.series_id,"""
        rf"""reported_recurrence_strength:observed?(r.reported_recurrence_str"""
        rf"""ength||null):null,exception_status:observed?(r.exception_status|"""
        rf"""|null):null,exception_frequency:observed?(r.exception_frequency|"""
        rf"""|null):null,frequency_evidence_basis:observed?(r.frequency_evide"""
        rf"""nce_basis||null):null,minimum_reported_occurrences:observed?(r.m"""
        rf"""inimum_reported_occurrences||null):null,"""
        rf"""bounded_rate_or_count_description:observed?(r.bounded_rate_or_co"""
        rf"""unt_description||null):null,"""
        rf"""recurrence_scope_description:observed?(r.recurrence_scope_descri"""
        rf"""ption||null):null,confirming_episode_counted_as_independent_freq"""
        rf"""uency_evidence:false,series_is_recurrence_support_not_primary_ep"""
        rf"""isode:true,reported_recurrence_is_not_verified_true_frequency:tr"""
        rf"""ue,summary_fields_are_not_primary_source:true}}}}"""
        "\n"
        rf"""function v5DraftErrors(u,r){{const e=[];"""
        rf"""if(r.state!=="observed")return e;const """
        rf"""active=v5ClaimDescriptors(u,r);if(!active.length)e.push("Choose """
        rf"""at least one substantive behavior or affirmative component, or """
        rf"""use Not enough information.");for(const c of """
        rf"""active)if(!(r.v5_claim_sources?.[c.key]||[]).length)e.push(`Choo"""
        rf"""se the exact quote that supports: ${{c.label}}`);for(const v of """
        rf"""(r.coded_values||[]))if(V5_ABSENCE[v]&&!V5_HYBRIDS[v]&&!v5GateCo"""
        rf"""mplete(r.v5_absence_gates?.[v]))e.push(`The selected absence """
        rf"""behavior only counts when all four checks are Yes: ${{v5Label(u,"""
        rf"""v)}}`);for(const [fid] of v5FacetEntries(u)){{const """
        rf"""ids=v5ConceptIds(u,r,fid);if(ids.length<2)continue;const """
        rf"""spec=v5FacetSpec(u,fid)||{{}},cfg=r.v5_facet_stage?.[fid]||{{}};"""
        rf"""if(spec.cardinality==="zero_or_one"&&cfg.mode!=="distinct")e.pus"""
        rf"""h(`The selected ${{v5FacetTitle(fid)}} alternatives can both """
        rf"""count only if the source clearly separates distinct """
        rf"""stages/windows.`);if(spec.cardinality!=="zero_or_one"&&!['same',"""
        rf"""'distinct'].includes(cfg.mode))e.push(`Say whether the selected """
        rf"""${{v5FacetTitle(fid)}} facts belong to the same stage or """
        rf"""distinct stages.`);if(cfg.mode==="distinct"&&!['ordered',"""
        rf"""'unordered'].includes(cfg.order))e.push(`Say whether the """
        rf"""distinct ${{v5FacetTitle(fid)}} stages have a source-established """
        rf"""order.`);if(cfg.mode==="distinct"&&cfg.order==="ordered"){{const """
        rf"""ordered=cfg.ordered_value_ids||[];"""
        rf"""if(ordered.length!==ids.length||new """
        rf"""Set(ordered).size!==ids.length||ordered.some(v=>!ids.includes(v)"""
        rf"""))e.push(`Assign each selected ${{v5FacetTitle(fid)}} fact a """
        rf"""unique source-supported position.`)}}}}if(u.kind==="series"){{if"""
        rf"""(!r.reported_recurrence_strength)e.push("Choose how often the """
        rf"""narrator says this behavior recurs.");"""
        rf"""if(!r.exception_status)e.push("Choose whether the narrator """
        rf"""reports exceptions or limits.");"""
        rf"""if(r.reported_recurrence_strength==="bounded_rate_or_count"&&!r."""
        rf"""bounded_rate_or_count_description)e.push("Enter the count or """
        rf"""rate that the narrator actually states.")}}return e}}"""
        "\n"
        rf"""function v5Download(name,text){{const blob=new Blob([text],{{t"""
        rf"""ype:"application/json;charset=utf-8"}}),"""
        rf"""url=URL.createObjectURL(blob),a=document.createElement("a");"""
        rf"""a.href=url;a.download=name;document.body.appendChild(a);"""
        rf"""a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),"""
        rf"""1000)}}"""
        "\n"
        rf"""function v5DownloadResponses(){{const ep=[],ser=[],issues=[];"""
        rf"""for(const u of units){{const r=responses.get(u.key);"""
        rf"""if(!r){{issues.push("Complete and save every selected unit """
        rf"""before final V5 export.");continue}}const e=v5DraftErrors(u,r);"""
        rf"""if(e.length){{issues.push(`${{u.key}}: ${{e.join(" ")}}`);"""
        rf"""continue}}const env=v5BuildEnvelope(u,r);"""
        rf"""(u.kind==="episode"?ep:ser).push(env)}}if(issues.length){{alert("""
        rf""""V5 export is blocked:\n\n"+issues.slice(0,"""
        rf"""8).join("\n\n")+(issues.length>8?"\n\n…":""));"""
        rf"""return}}v5Download("episode_responses.completed.v5.jsonl","""
        rf"""ep.map(x=>JSON.stringify(x)).join("\n")+"\n");"""
        rf"""v5Download("series_responses.completed.v5.jsonl","""
        rf"""ser.map(x=>JSON.stringify(x)).join("\n")+"\n")}}"""
        "\n"
        rf"""// V5_EXPORT_HELPERS_END"""
        "\n"
    )


def patch_html_for_v5_auditor(html: str, public_semantics: Mapping[str, Any]) -> str:
    embedded_before = _embedded_fragment(html)
    html = html.replace(
        "</head>",
        (
            "<style>\n.v5facet{margin:14px 0;padding:12px 14px;border:"
            "1px solid #d7e0db;border-radius:11px;background:#fbfdfc}"
            ".v5facet>h3{margin:0 0 9px}.v5choices{display:grid;gap:8"
            "px}.v5choice{display:block;padding:10px 11px;border:1px "
            "solid #dde5e0;border-radius:9px;background:#fff}.v5hybri"
            "d,.v5absencechoice{display:grid;gap:8px}.v5absence{margi"
            "n:7px 0 0 24px;padding:10px 12px;border-left:3px solid #"
            "cbd8d1;background:#f7faf8}.v5gate{display:grid;gap:7px}."
            "v5gateitem{display:grid;grid-template-columns:minmax(0,1"
            "fr) minmax(130px,190px);gap:10px;align-items:center}.v5s"
            "tages{margin:11px 0 0;padding:10px 12px;border:1px dashe"
            "d #cbd8d1;border-radius:9px}.v5stages h4{margin:4px 0 8p"
            "x}.v5rank{display:grid;grid-template-columns:minmax(0,1f"
            "r) 160px;gap:10px;align-items:center;padding:5px 0}.v5cl"
            "aims{display:grid;gap:9px}.v5claim{padding:10px 11px;bor"
            "der:1px solid #d8e2dc;border-radius:9px;background:#f8fb"
            "f9}.v5export{margin:18px auto;max-width:980px;padding:14"
            "px 16px;border:2px solid #70877b;border-radius:12px;back"
            "ground:#f4f8f6}.v5export h2{margin-top:0}.v5export butto"
            "n{font-weight:700}\n</style>\n</head>"
        ),
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
        (
            "function renderSources(u,r){const segments=u.task.exact_"
            "source_segments||[];const quoteName=i=>segments.length=="
            '=1?"Exact quote":`Exact quote ${i+1}`;const quoteText=s='
            '>s.exact_text||s.exact_participant_text||"";const cards='
            'segments.map((s,i)=>`<article class="source"><div class='
            '"sourceid">${esc(quoteName(i))}</div><p>${esc(quoteText('
            's))}</p></article>`).join("");if(r.state!=="observed"){$'
            '("sources").innerHTML=cards;return}const claims=v5ClaimD'
            "escriptors(u,r);if(segments.length<=1||!claims.length){$"
            '("sources").innerHTML=cards;return}const saved=r.v5_clai'
            'm_sources||{};const selectors=`<div class="provenancebox'
            '"><h3>Which exact quote supports each selected claim?</h'
            '3><p class="hint">This is claim-specific source bookkeep'
            "ing. Choose only quote text that actually supports that "
            'claim.</p><div class="v5claims">${claims.map(c=>`<div cl'
            'ass="v5claim"><b>${esc(c.label)}</b><div class="provenan'
            'celist">${segments.map((s,i)=>`<label><input type="check'
            'box" data-v5-source-key="${esc(c.key)}" value="${esc(s.s'
            'egment_id)}" ${(saved[c.key]||[]).includes(s.segment_id)'
            '?"checked":""}> <span><span class="quotelabel">${esc(quo'
            'teName(i))}</span><span class="quotesnippet">${esc(quote'
            'Text(s))}</span></span></label>`).join("")}</div></div>`'
            ').join("")}</div></div>`;$("sources").innerHTML=cards+se'
            "lectors}"
        ),
    )
    html = _replace_function(
        html,
        "renderObserved",
        (
            'function renderObserved(u,r){const host=$("observedField'
            's");if(r.state!=="observed"){host.innerHTML=\'<div class='
            '"section"><p class="hint">No substantive behavior is sel'
            "ected for this unit.</p></div>';return}const facets=v5Fa"
            'cetEntries(u);let html=\'<div class="section"><h3>Which b'
            'ehavior does the exact source show?</h3><p class="hint">'
            "Choices are separated by behavioral dimension. Different"
            " dimensions may describe the same stage without implying"
            " an order.</p>';for(const [fid,values] of facets){html+="
            '`<div class="v5facet"><h3>${esc(v5FacetTitle(fid))}</h3>'
            '<div class="v5choices">${values.map(v=>V5_HYBRIDS[v]?v5H'
            "ybridCard(u,v,r):V5_ABSENCE[v]?v5AbsenceCard(u,v,r):v5No"
            'rmalCard(u,v,r)).join("")}</div>${v5StageControls(u,r,fi'
            "d)}</div>`}html+='</div>';if(u.kind===\"series\")html+=ser"
            "iesFields(r);host.innerHTML=html;host.querySelectorAll('"
            "[data-value],[data-v5-hybrid-positive],[data-v5-gate-val"
            "ue],[data-v5-stage-mode],[data-v5-stage-order]').forEach"
            '(x=>x.addEventListener("change",()=>v5TransientRerender('
            'u)));$("recurrenceStrength")?.addEventListener("change",'
            '()=>v5TransientRerender(u));$("exceptionStatus")?.addEve'
            'ntListener("change",()=>v5TransientRerender(u))}'
        ),
    )
    html = _replace_function(
        html,
        "readForm",
        (
            "function readForm(u){const base=draftFromFormSeed(u);bas"
            'e.state=document.querySelector(\'input[name="state"]:chec'
            "ked')?.value||null;base.counterevidence_source_segment_i"
            "ds=[];base.context_qualifiers=[];base.missingness_flags="
            "[];base.life_phase_qualifier=null;base.annotation_note=n"
            'ull;if(u.kind==="episode"){base.language=null;base.influ'
            'ence_relation="none_reported";base.influence_source_segm'
            "ent_ids=[]}base.v5_hybrid_components={};base.v5_absence_"
            "gates={};let vals=selectedValues();document.querySelecto"
            "rAll('[data-v5-hybrid-positive]:checked').forEach(x=>{co"
            "nst v=x.dataset.v5HybridPositive,g=v5ReadGates(v);base.v"
            "5_hybrid_components[v]={affirmative_selected:true,absenc"
            "e_gate:g};if(v5GateComplete(g)&&!vals.includes(v))vals.p"
            "ush(v)});for(const v of vals)if(V5_ABSENCE[v]&&!V5_HYBRI"
            "DS[v])base.v5_absence_gates[v]=v5ReadGates(v);base.coded"
            "_values=vals;base.value_relation=null;base.asserts_non_a"
            "ction=false;base.non_action_gate=null;base.v5_facet_stag"
            "e=v5ReadFacetStages(u,base);base.v5_claim_sources=v5Read"
            "ClaimSources(u,base);base.supporting_source_segment_ids="
            "[...new Set(Object.values(base.v5_claim_sources).flat())"
            "];base.other_specified_description=null;if(base.state!=="
            '"observed")return base;if(u.kind==="series"){base.report'
            'ed_recurrence_strength=$("recurrenceStrength")?.value||n'
            'ull;base.exception_status=$("exceptionStatus")?.value||n'
            'ull;base.exception_frequency=base.exception_status==="ex'
            'ceptions_explicitly_denied"?"none_reported":base.excepti'
            'on_status==="exceptions_reported"?($("exceptionFrequency'
            '")?.value||"unknown"):null;base.frequency_evidence_basis'
            '=base.reported_recurrence_strength==="bounded_rate_or_co'
            'unt"?"bounded_rate_or_count_self_report":"generalized_se'
            'lf_report";base.minimum_reported_occurrences=null;base.b'
            "ounded_rate_or_count_description=base.reported_recurrenc"
            'e_strength==="bounded_rate_or_count"?($("boundedDescript'
            'ion")?.value.trim()||null):null;base.recurrence_scope_de'
            "scription=null}return base}"
        ),
    )
    html = _replace_function(
        html,
        "validate",
        (
            "function validate(u,r){const sourceIds=new Set((u.task.e"
            "xact_source_segments||[]).map(s=>s.segment_id));for(cons"
            "t ids of Object.values(r.v5_claim_sources||{}))for(const"
            ' id of ids)if(!sourceIds.has(id))return["This saved resp'
            "onse no longer matches this unit. Stop and report the te"
            'chnical problem."];if(!["observed","insufficient","not_a'
            'pplicable"].includes(r.state))return["Choose Yes, Doesn\''
            't apply to this story, or Not enough information."];retu'
            "rn v5DraftErrors(u,r)}"
        ),
    )

    install = (
        "\nfunction v5InstallExportPanel(){for(const el of documen"
        "t.querySelectorAll('button,a')){const t=(el.textContent|"
        '|"").toLowerCase();if(t.includes("download")&&t.includes'
        '("response")&&!t.includes("progress")&&!t.includes("atte'
        'station"))el.style.display="none"}const panel=document.c'
        'reateElement("section");panel.className="v5export";panel'
        ".innerHTML='<h2>Final V5 response export</h2><p>Use this"
        " export for the completed calibration. It converts your "
        "human judgments into the accepted V5 facet/stage/provena"
        "nce graph automatically. Machine IDs remain hidden from "
        'the annotation task.</p><button type="button" id="v5Down'
        'loadResponses">Download V5 response files</button><p cla'
        'ss="hint">Also download the existing auditor attestation'
        ". The attestation format is unchanged.</p>';document.bod"
        'y.appendChild(panel);panel.querySelector("#v5DownloadRes'
        'ponses").addEventListener("click",v5DownloadResponses)}\n'
        'if(document.readyState==="loading")document.addEventList'
        'ener("DOMContentLoaded",v5InstallExportPanel);else v5Ins'
        "tallExportPanel();\n"
    )
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
