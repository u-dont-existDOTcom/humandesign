"""Apply only the authorized research instruction/pointer update, once."""
from pathlib import Path
import json
import subprocess

ROOT=Path(__file__).resolve().parents[2]
branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
if branch!='research/astro-method-v2-sources-20261005':
    raise SystemExit('Wrong writer branch; do not mutate a shared checkout')
p=ROOT/'AGENTS.md';s=p.read_text()
old='For a substantive astrology reading, additionally load `reference/research/ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V1.json`. Do not synthesize a supposedly deep reading until its required passes are dispositioned; use `scripts/validate_astrology_deep_analysis_receipt.py` for a durable receipt when the analysis is being saved or used as a research artifact. A striking newly noticed aspect is not permission to skip the remaining passes.'
new='For a substantive astrology reading, load the current procedure `reference/research/ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V2.json` and its normative prose. V2 preserves the twenty V1 coverage families while requiring a predeclared task contract, complete catalog disposition, conditional source rules and evidence integrity. Saved new analyses use `scripts/validate_astrology_deep_analysis_receipt_v2.py` with the externally preserved contract hash. Accounted-for gaps are not executed work, and a mechanical receipt does not certify source semantics, actual blinding or predictive validity. Use `reference/research/ASTROLOGY_SOURCE_ACQUISITION_V2.json` for the bounded corpus and access state. Keep V1 files and every historical prediction/model frozen for replay; these procedural changes do not deploy a new runtime model.'
if old in s:p.write_text(s.replace(old,new,1))
elif new not in s:raise SystemExit('Expected AGENTS block changed; reconcile before edit')
p=ROOT/'reference/research/CURRENT_PERSON_LIFE_RULESET_INDEX_V1.json';d=json.loads(p.read_text());d['astrology_deep_analysis_protocol_v1_legacy']='reference/research/ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V1.json';d['astrology_deep_analysis_protocol']='reference/research/ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V2.json';d['astrology_source_acquisition_plan']='reference/research/ASTROLOGY_SOURCE_ACQUISITION_V2.json';d['v2_method_boundary']='Current research procedure only. Actual source audit, semantic faithfulness, execution and predictive validation are separate; historical candidate rules remain unchanged.';p.write_text(json.dumps(d,indent=2)+'\n')
p=ROOT/'tests/test_person_life_ruleset_index.py';s=p.read_text();s=s.replace('assert data["astrology_deep_analysis_protocol"] == "reference/research/ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V1.json"','assert data["astrology_deep_analysis_protocol"] == "reference/research/ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V2.json"');s=s.replace('assert "ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V1.json" in agents','assert "ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V2.json" in agents');p.write_text(s)
print('Research instructions/index updated to V2; historical models unchanged')
