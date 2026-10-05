import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "reference" / "research" / "ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V1.json"
VALIDATOR = ROOT / "scripts" / "validate_astrology_deep_analysis_receipt.py"


def test_deep_protocol_has_all_required_coverage_families():
    data = json.loads(PROTOCOL.read_text())
    ids = {row["id"] for row in data["required_passes"]}
    assert {
        "P00_authority","P00b_information_firewall","P01_input","P01b_time_sensitivity","P02_ephemeris","P03_inventory","P04_geometry",
        "P05_lilly","P06_hellenistic","P07_jyotish","P08_houses_rulers","P09_domains",
        "P10_contradictions","P11_topic","P12_timing_state","P13_timing_trigger",
        "P14_special_candidates","P15_cross_system","P16_completeness","P17_synthesis",
    } <= ids
    assert data["synthesis_gate"]["block_if_missing_required_pass"] is True
    assert data["synthesis_gate"]["require_evidence_for_applied"] is True
    assert data["synthesis_gate"]["require_subcheck_disposition"] is True
    assert "SOURCE_TRADITION_COMPLETE" in data["completion_levels"]
    assert "NOT_YET_ACHIEVED" in data["current_source_completeness"]
    assert data["source_completeness_frontier"] == "reference/research/ASTROLOGY_SOURCE_COMPLETENESS_FRONTIER_V1.json"


def test_receipt_validator_rejects_missing_required_pass(tmp_path):
    receipt = {
        "conditions": {
            "when timing is asked": False,
            "when exact date/localization is asked": False,
            "when requested": False,
        },
        "passes": [{"id":"P00_authority","status":"APPLIED","evidence":["loaded index"]}],
    }
    path=tmp_path/"bad.json"
    path.write_text(json.dumps(receipt))
    run=subprocess.run(["python3",str(VALIDATOR),str(path)],capture_output=True,text=True)
    assert run.returncode != 0
    assert "missing required pass" in run.stdout


def test_receipt_validator_accepts_complete_non_timing_receipt(tmp_path):
    protocol=json.loads(PROTOCOL.read_text())
    passes=[]
    for row in protocol["required_passes"]:
        if row["required"] is True:
            passes.append({
                "id":row["id"],
                "status":"APPLIED",
                "evidence":["test evidence"],
                "check_results":{check:{"status":"DONE","evidence":["test evidence"]} for check in row.get("checks",[])}
            })
    receipt={
        "conditions":{
            "when timing is asked":False,
            "when exact date/localization is asked":False,
            "when requested":False,
        },
        "passes":passes,
        "claim_ledger":[{
            "claim_id":"C1",
            "claim":"test claim",
            "support_refs":["test evidence"],
            "counterevidence_refs":[],
            "dependency_group":"test",
            "stability_class":"DATE_STABLE",
            "evidence_status":"SOURCE_GROUNDED"
        }],
    }
    path=tmp_path/"good.json"
    path.write_text(json.dumps(receipt))
    run=subprocess.run(["python3",str(VALIDATOR),str(path)],capture_output=True,text=True)
    assert run.returncode == 0, run.stdout+run.stderr
    assert '"valid": true' in run.stdout.lower()


def test_receipt_generator_materializes_all_active_passes(tmp_path):
    out=tmp_path/"receipt.json"
    generator=ROOT/"scripts"/"new_astrology_deep_analysis_receipt.py"
    run=subprocess.run(["python3",str(generator),"--out",str(out),"--timing","--exact-date","--cross-system","--subject-label","test"],capture_output=True,text=True)
    assert run.returncode == 0, run.stdout+run.stderr
    receipt=json.loads(out.read_text())
    protocol=json.loads(PROTOCOL.read_text())
    expected={row["id"] for row in protocol["required_passes"]}
    assert {row["id"] for row in receipt["passes"]} == expected
    assert all(row["status"] == "TODO" for row in receipt["passes"])
    rejected=subprocess.run(["python3",str(VALIDATOR),str(out)],capture_output=True,text=True)
    assert rejected.returncode != 0
