"""Frozen v0 horary predictor. No outcome-file or network dependency."""
from __future__ import annotations
import argparse, dataclasses, hashlib, importlib.metadata, json, os, time
from datetime import datetime, timezone
from pathlib import Path

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def verdict(witnesses, evaluable=True):
    if not evaluable:
        return "DEFER"
    positive = {"DIRECT", "TRANSLATION", "COLLECTION"}
    states = [s for k, s in witnesses if k in positive]
    if "PRESENT" in states:
        return "YES"
    if "INDETERMINATE" in states:
        return "DEFER"
    return "NO"

def serialize(value):
    if isinstance(value, datetime): return value.isoformat()
    if hasattr(value, "value"): return value.value
    if isinstance(value, Path): return str(value)
    raise TypeError(type(value).__name__)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=Path,required=True)
    ap.add_argument("--kernel",type=Path,required=True)
    ap.add_argument("--run-id",default="pilot-v0")
    args=ap.parse_args()
    os.environ["MOIRA_KERNEL_PATH"]=str(args.kernel)
    from moira import Moira
    from moira.horary import (HoraryQuestionReceipt,HoraryQuestionTimeReceipt,
        HoraryEvidenceState,HoraryQuestionTimeBasis,HorarySourceCalendar,
        HoraryHousePolicy,HoraryPerfectionState)
    from moira.constants import HouseSystem
    from moira.julian import jd_from_datetime,utc_to_ut1
    import moira
    assert importlib.metadata.version("moira-astro")=="6.2.0"
    inputs=args.root/"protocols"/args.run_id
    run=args.root/"runs"/args.run_id
    run.mkdir(parents=True,exist_ok=True)
    out=run/"predictions.jsonl"
    if out.exists(): raise RuntimeError("Existing predictions are immutable; inspect rather than overwrite")
    package_root=Path(moira.__file__).parent
    package_hashes={str(p.relative_to(package_root)):sha(p) for p in sorted(package_root.rglob('*'))
        if p.is_file() and (p.suffix in ('.py','.so'))}
    freeze={"run_id":args.run_id,"frozen_at":datetime.now(timezone.utc).isoformat(),
        "method_sha256":sha(inputs/"METHOD-FREEZE.md"),"corpus_sha256":sha(inputs/"CORPUS-v0.json"),
        "normalization_sha256":sha(inputs/"NORMALIZATION-FREEZE.md"),
        "runner_sha256":sha(__file__),"moira_version":"6.2.0",
        "package_code_sha256":hashlib.sha256(json.dumps(package_hashes,sort_keys=True).encode()).hexdigest(),
        "kernel_filename":args.kernel.name,"kernel_sha256":sha(args.kernel),
        "prediction_input_policy":"only frozen corpus and protocol; no source snapshots or outcome labels",
        "classification":"exploratory outcome-withheld algorithmic pilot; not independent replication"}
    (run/"pre-prediction-freeze.json").write_text(json.dumps(freeze,indent=2)+'\n')
    (run/"package-hashes.json").write_text(json.dumps(package_hashes,indent=2)+'\n')
    engine=Moira(kernel_path=str(args.kernel))
    corpus=json.loads((inputs/"CORPUS-v0.json").read_text())
    for c in corpus["cases"]:
        start=time.monotonic()
        instant=datetime.fromisoformat(c["normalized_utc"].replace('Z','+00:00'))
        jd=utc_to_ut1(jd_from_datetime(instant))
        question=HoraryQuestionReceipt(c["case_id"],c["latitude_deg"],c["longitude_deg"],
            HoraryQuestionTimeReceipt(HoraryEvidenceState.EVALUATED,
                HoraryQuestionTimeBasis.QUESTION_PROPOSED_AND_FIGURE_ERECTED,
                "Original forum opening-post question-chart timestamp; normalization frozen separately",
                HorarySourceCalendar.GREGORIAN,c["source_local_datetime"],instant,jd,
                "frozen_iana_civil_timezone_to_utc_then_moira_ut1_v0",None),(),c["topic_house"])
        try:
            profile=engine.horary_evidence_at(question,
                house_policy=HoraryHousePolicy(HouseSystem.REGIOMONTANUS),perfection_jd_end=jd+31.0)
            evidence=dataclasses.asdict(profile)
            (run/(c["case_id"]+"-evidence.json")).write_text(json.dumps(evidence,indent=2,default=serialize)+'\n')
            evaluable=profile.perfection.state==HoraryPerfectionState.COMPOSED
            witnesses=[(w.kind.name,w.state.name) for w in profile.perfection.analysis.witnesses] if evaluable else []
            pred={"case_id":c["case_id"],"prediction":verdict(witnesses,evaluable),
                "witnesses":witnesses,"evaluable":evaluable,
                "reason":profile.perfection.reason,"runtime_seconds":round(time.monotonic()-start,3),
                "timestamp":datetime.now(timezone.utc).isoformat()}
        except Exception as ex:
            pred={"case_id":c["case_id"],"prediction":"DEFER","engine_error":type(ex).__name__+': '+str(ex),
                "runtime_seconds":round(time.monotonic()-start,3),"timestamp":datetime.now(timezone.utc).isoformat()}
        with out.open('a') as f:
            f.write(json.dumps(pred)+'\n');f.flush();os.fsync(f.fileno())
        print(json.dumps(pred),flush=True)
    seal={"sealed_at":datetime.now(timezone.utc).isoformat(),"predictions_sha256":sha(out),
        "case_count":len(corpus["cases"]),"pre_prediction_freeze_sha256":sha(run/"pre-prediction-freeze.json")}
    (run/"prediction-seal.json").write_text(json.dumps(seal,indent=2)+'\n')
    print('SEALED',json.dumps(seal),flush=True)
if __name__=='__main__':main()
