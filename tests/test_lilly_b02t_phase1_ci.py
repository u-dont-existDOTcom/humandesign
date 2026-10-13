"""Run Lilly Chapter L Phase1 historical-source assertions in repository CI."""
from pathlib import Path
import subprocess,sys,json
B=Path(__file__).resolve().parents[1]/"tasks/astro-source-audit-multipass-20261005/batches/B02t"
def test_lilly_phase1_documentary_source():
 result=subprocess.run([sys.executable,str(B/"run_verification.py")],cwd=B,capture_output=True,text=True,timeout=120,check=False)
 assert result.returncode==0,result.stdout+result.stderr
 receipt=json.loads((B/"TEST_RUN_SUMMARY.json").read_text())
 assert receipt["successful"] and receipt["tests_run"]==receipt["distinct_test_count"]>=233
 assert receipt["failures"]==receipt["errors"]==0
 assert json.loads((B/"SOURCE_IDENTITY.json").read_text())["next_numbered_chapter"]=="LI from original PDF400 below divider"
 assert not json.loads((B/"COUNTS.json").read_text())["all_chapter_l_complete"]
