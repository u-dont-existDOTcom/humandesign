"""CI entrypoint for all B02u original-source regressions."""
from pathlib import Path
import json,subprocess,sys
B=Path(__file__).resolve().parents[1]/"tasks/astro-source-audit-multipass-20261005/batches/B02u"
def test_lilly_B02u_source_fidelity():
    run=subprocess.run([sys.executable,str(B/"run_verification.py")],
                       cwd=B,text=True,capture_output=True,timeout=120,check=False)
    assert run.returncode==0,run.stdout+run.stderr
    j=json.loads((B/"TEST_RUN_SUMMARY.json").read_text())
    assert j["successful"] and j["tests_run"]==j["distinct_test_count"]==314
    assert j["failures"]==j["errors"]==j["skipped"]==0
