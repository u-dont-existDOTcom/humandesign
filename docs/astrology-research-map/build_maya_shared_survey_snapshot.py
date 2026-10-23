#!/usr/bin/env python3
"""Build a privacy-safe metadata-only index of pre-existing survey instruments.

No participant responses, identity, chart predictions, credentials, or
private files. The cross-tradition bridge must reuse the survey banks
instead of spawning an independent Maya interview.

Requires local Git refs for the exact preexisting Life Patterns source
version. Retains a lightweight committed snapshot for offline tests and
cold-extracted handoffs; it never edits the underlying instruments.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
from pathlib import Path

BRANCH = "7971b3c1564d9c38bce17abe4c4575affcba2c76"
SOURCE = "tasks/life-patterns-external-questionnaire-merge-20261021/LIFE-PATTERNS-ADAPTIVE-SURVEY-v3-CANDIDATE.json"
TF = "apps/life-patterns-participant/participant/static/tendency-first-v1.json"
EXPERIENCE = "apps/life-patterns-participant/participant/static/experience-meaning-v2.json"
CORE = "reference/core/question_bank_v1.json"
SELECTED = ("ART","VOCATION","LEARNING_HISTORY","TRAVEL",
            "RECIPROCITY","BONDS","ANGER_REPAIR","RESOURCES",
            "PLAY","BELIEF","SENSORY_ENJOYMENT")
TARGET = "MAYA_SHARED_SURVEY_EXISTING_INSTRUMENT_SNAPSHOT_V1.json"

def _git(root:Path, ref:str,path:str) -> bytes:
    return subprocess.check_output(
      ["git","-C",str(root),"show",f"{ref}:{path}"],
      stderr=subprocess.DEVNULL
    )

def record(root:Path,ref:str,path:str) -> tuple[dict,dict]:
    raw=_git(root,ref,path)
    obj=json.loads(raw)
    return obj,{
      "git_ref":ref,
      "path":path,
      "sha256_original_bytes":hashlib.sha256(raw).hexdigest(),
      "schema_or_version":obj.get("schema",obj.get("version")),
      "source_status":obj.get("status","REFERENCE_SOURCE_NOT_VERIFIED_LIVE")
    }

def compile_inventory(root:Path) -> dict:
    v3, v3_meta=record(root,BRANCH,SOURCE)
    tf, tf_meta=record(root,BRANCH,TF)
    exp,exp_meta=record(root,BRANCH,EXPERIENCE)
    hd,hd_meta=record(root,"HEAD",CORE)
    question_ids=[q["id"] for q in v3["questions"]]
    if len(question_ids)!=23 or len(set(question_ids))!=23:
        raise ValueError("Exact preexisting 23 opt-in items required")
    if not set(SELECTED).issubset(set(question_ids)):
        raise ValueError("Existing shared survey item missing; no silent replacement")
    micro_ids=[q["id"] for q in v3["optional_microprobes"]]
    if len(micro_ids)!=7 or len(set(micro_ids))!=7:
        raise ValueError("Existing seven conditional microprobe ids changed")
    tfids=[q["id"] for q in tf["questions"]]
    hdids=[q["id"] for q in hd["questions"]]
    expids=[q["id"] for q in exp["items"]]
    if len(set(tfids))!=len(tfids) or len(set(hdids))!=len(hdids) or len(set(expids))!=len(expids):
        raise ValueError("Preexisting questionnaire contains repeated ids")
    return {
      "schema":"MAYA_SHARED_SURVEY_REFERENCES_EXISTING_UNMODIFIED_INSTRUMENTS_V1",
      "status":"SOURCE_METADATA_ONLY_NO_LIVE_SURVEY_EDIT_OR_SCORING",
      "prepared_utc_date":"2026-10-23",
      "survey_v3":v3_meta | {
        "git_commit":BRANCH,
        "question_count":len(question_ids),
        "optional_microprobe_count":len(micro_ids),
        "max_base_optional_topics_per_session":v3["max_base_optional_topics_per_session"],
        "max_additional_conditional_probes_per_session":v3["max_additional_conditional_probes_per_session"],
        "decline_all_allowed":v3["decline_all_allowed"],
        "question_ids":question_ids,
        "microprobe_ids":micro_ids,
        "all_existing_question_object_sha256":{
           q["id"]:hashlib.sha256(json.dumps(q,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode("utf-8")).hexdigest()
           for q in v3["questions"]
        },
        "all_existing_microprobe_object_sha256":{
           q["id"]:hashlib.sha256(json.dumps(q,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode("utf-8")).hexdigest()
           for q in v3["optional_microprobes"]
        },
        "selected_existing_question_definitions":[{
          "id":q["id"],"question":q["question"],
          "answer_dimensions":q["answer_dimensions"],
          "source_domains":q["source_domains"],
          "already_live":q.get("already_live",False),
          "question_sha256":hashlib.sha256(q["question"].encode("utf-8")).hexdigest()
        } for q in v3["questions"] if q["id"] in SELECTED],
      },
      "tendency_first":tf_meta | {
        "question_count":len(tfids),"question_ids":tfids
      },
      "experience_meaning":exp_meta | {
        "question_count":len(expids),"question_ids":expids,
        "score_status":"SEPARATE_OPTIONAL_UNSCORED" if "UNSCORED" in exp["status"] else "VERIFY_POLICY"
      },
      "human_design_survey_bank":hd_meta | {
        "question_count":len(hdids),"question_ids":hdids,
        "scope":"Existing HD V4.3/V3.6-specific measurement; not Maya scoring"
      },
      "privacy":"No participant inputs, answers, dates, passwords or source respondent files read or emitted.",
      "deployment":"The V3 question bank is a development opt-in candidate; this index is not a modification or deployment of the live Life Patterns app.",
      "human_validation":0
    }

if __name__=="__main__":
    here=Path(__file__).resolve().parent
    root=here.parents[1]
    obj=compile_inventory(root)
    target=here/TARGET
    target.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(target, len(obj["survey_v3"]["question_ids"]),
          len(obj["tendency_first"]["question_ids"]),
          len(obj["human_design_survey_bank"]["question_ids"]))
