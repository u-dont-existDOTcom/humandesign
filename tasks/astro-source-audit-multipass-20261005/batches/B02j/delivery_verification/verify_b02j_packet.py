#!/usr/bin/env python3
"""Actually extract the B02j packet, verify every hash, and repeat its 36 tests.
Standard-library driver adapted by root from Reader A's proposed verifier.
Receipts/logs are outside the extracted packet. No predictive validation.
"""
import hashlib,json,os,re,shutil,stat,subprocess,sys,unicodedata,zipfile,zlib
from pathlib import Path

def need(ok,message):
    if not ok: raise ValueError(message)

def digest(path):
    data=path.read_bytes()
    return {"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}

def unique(pairs):
    d={}
    for k,v in pairs:
        need(k not in d,"Duplicate JSON key: "+str(k))
        d[k]=v
    return d

def parts(name):
    need(isinstance(name,str),"Path must be text")
    need(not any(c in name for c in '\\:*?"<>|\0'),"Unsafe path: "+repr(name))
    need(not any(ord(c)<32 or ord(c)==127 for c in name),"Control character in path")
    p=name.split("/")
    need(len(p)>=2 and p[0]=="B02j","Path outside B02j")
    need(all(x not in ("",".","..") and x==x.rstrip(" .") for x in p),"Unsafe path component")
    for x in p:
        need(not re.fullmatch(r"CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9]",x.split(".")[0],re.I),"Reserved portable path")
    return p

def snapshot(packet):
    d={}
    for p in sorted(packet.rglob("*")):
        mode=p.lstat().st_mode
        need(not stat.S_ISLNK(mode),"Unexpected symlink")
        if stat.S_ISDIR(mode): continue
        need(stat.S_ISREG(mode),"Unexpected special file")
        d[p.relative_to(packet).as_posix()]=digest(p)
    return d

def main():
    receipt={"schema_version":1,"batch":"B02j","status":"FAIL",
        "python":{"executable":sys.executable,"version":sys.version},
        "zlib":{"compiled_version":zlib.ZLIB_VERSION,"runtime_version":getattr(zlib,"ZLIB_RUNTIME_VERSION",None)},
        "test_semantics":{"execution_kind":"Repeat execution of the existing frozen 36-test suite","new_unique_test_methods_added":0,"not_additional_unique_test_coverage":True},
        "scope":"ZIP integrity, actual extraction, every manifest byte/hash, repeat existing focused data-integrity and source-arithmetic tests, and post-test file integrity. No runtime, ephemeris, human or predictive validation.",
        "verification_driver":digest(Path(__file__).resolve())}
    output=None
    try:
        need(len(sys.argv)==4,"Usage: verify_b02j_packet.py ZIP EXPECTED_SHA256 EMPTY_OUTPUT_DIR")
        zip_path=Path(sys.argv[1]).resolve(strict=True)
        expected_sha=sys.argv[2].lower()
        need(bool(re.fullmatch(r"[0-9a-f]{64}",expected_sha)),"Invalid expected ZIP SHA256")
        arg=Path(sys.argv[3])
        need(not arg.is_symlink(),"Output directory must not be a symlink")
        output=arg.resolve()
        for b in [p for p in zip_path.parents if p.name=="B02j"]:
            need(output!=b and b not in output.parents,"Output must be outside source B02j")
        need(not output.exists() or (output.is_dir() and not any(output.iterdir())),"Output must be new or empty")
        output.mkdir(parents=True,exist_ok=True)
        receipt.update({"zip_path":str(zip_path),"output_directory":str(output),"expected_zip_sha256":expected_sha,"zip_actual":digest(zip_path)})
        need(receipt["zip_actual"]["sha256"]==expected_sha,"ZIP SHA mismatch")
        with zipfile.ZipFile(zip_path) as zf:
            entries=zf.infolist()
            names,aliases={},{}
            for e in entries:
                n=e.filename
                pp=parts(n)
                need(e.orig_filename==n,"Filename transformation")
                need(n not in names,"Duplicate ZIP entry")
                need(not e.is_dir() and not (e.external_attr&0x10),"Directory ZIP entry")
                need(not (e.flag_bits&1),"Encrypted ZIP entry")
                need(stat.S_IFMT(e.external_attr>>16) in (0,stat.S_IFREG),"Special ZIP entry")
                names[n]=e
                for k in range(1,len(pp)+1):
                    spelling="/".join(pp[:k])
                    key=unicodedata.normalize("NFC",spelling.casefold())
                    need(aliases.get(key,spelling)==spelling,"Portable path collision")
                    aliases[key]=spelling
            for n in names:
                pp=n.split("/")
                need(not any("/".join(pp[:k]) in names for k in range(1,len(pp))),"File/directory collision")
            need("B02j/MANIFEST.json" in names,"Missing manifest")
            mb=zf.read("B02j/MANIFEST.json")
            md={"bytes":len(mb),"sha256":hashlib.sha256(mb).hexdigest()}
            m=json.loads(mb.decode("utf-8"),object_pairs_hook=unique)
            need(m.get("batch")=="B02j" and m.get("self_hash_excluded") is True,"Manifest identity/self-hash mismatch")
            rows=m.get("files")
            need(isinstance(rows,list),"Manifest files must be a list")
            need(type(m.get("files_count")) is int and m["files_count"]==len(rows),"Manifest count mismatch")
            declared={}
            for row in rows:
                p,n,s=row.get("path"),row.get("bytes"),row.get("sha256")
                parts("B02j/"+p)
                need(p!="MANIFEST.json" and p not in declared,"Manifest duplicate/self-entry")
                need(type(n) is int and n>=0,"Invalid byte count")
                need(isinstance(s,str) and bool(re.fullmatch(r"[0-9a-fA-F]{64}",s)),"Invalid SHA256")
                declared[p]={"bytes":n,"sha256":s.lower()}
            need(set(names)=={"B02j/"+p for p in declared}|{"B02j/MANIFEST.json"},"Manifest/ZIP membership mismatch")
            need(len(entries)==len(declared)+1,"ZIP count mismatch")
            verified=0
            for p,expected in declared.items():
                data=zf.read("B02j/"+p)
                actual={"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
                need(actual==expected,"ZIP bytes/hash mismatch: "+p)
                verified+=1
            for n in sorted(names):
                target=output.joinpath(*parts(n))
                target.parent.mkdir(parents=True,exist_ok=True)
                with zf.open(n) as src,target.open("xb") as dst:
                    shutil.copyfileobj(src,dst,1024*1024)
        packet=output/"B02j"
        expected=dict(declared)
        expected["MANIFEST.json"]=md
        before=snapshot(packet)
        need(before==expected,"Extracted bytes/hash/inventory mismatch")
        receipt.update({"source_core_commit_from_manifest":m.get("source_core_commit"),"manifest_actual":md,
            "zip_entry_count":len(entries),"declared_file_count":len(declared),"verified_zip_payload_file_count":verified,
            "manifest_self_exclusion_verified":True,"exact_manifest_zip_membership":True,
            "extracted_file_count":len(before),"before_test_files":before})
        command=[sys.executable,"-B","-m","unittest","-v","test_lilly_fifth_house"]
        environment=os.environ.copy()
        for key in ("PYTHONPATH","PYTHONHOME","PYTHONSAFEPATH"):
            environment.pop(key,None)
        environment["PYTHONNOUSERSITE"]="1"
        environment["PYTHONDONTWRITEBYTECODE"]="1"
        timed_out=False
        try:
            test=subprocess.run(command,cwd=packet,env=environment,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60,check=False)
            log,code=test.stdout,test.returncode
        except subprocess.TimeoutExpired as exc:
            log,code,timed_out=exc.stdout or b"",None,True
        lp=output/"TEST_PACKET_USABILITY.txt"
        lp.write_bytes(log)
        counts=[int(n) for n in re.findall(rb"(?m)^Ran (\d+) tests? in [^\r\n]+\r?$",log)]
        receipt["test_execution"]={"command":command,"cwd":str(packet),"exit_code":code,"timed_out":timed_out,
            "observed_summary_counts":counts,"tests_run":counts[0] if len(counts)==1 else None,"log_path":str(lp),"log_actual":digest(lp)}
        after=snapshot(packet)
        receipt.update({"after_test_files":after,"post_test_file_count":len(after),
            "all_packet_files_unchanged_after_test":after==before,"verified_unchanged_manifest_payload_file_count":len(declared)})
        need(after==before,"Packet changed after tests")
        need(not timed_out and code==0,"Existing suite did not exit successfully")
        need(counts==[36],"Expected exactly one 36-test summary")
        receipt["status"]="PASS"
    except Exception as exc:
        receipt["error"]=type(exc).__name__+": "+str(exc)
    summary={k:v for k,v in receipt.items() if k not in ("before_test_files","after_test_files")}
    if output is not None and output.is_dir():
        rp=output/"PACKET_USABILITY.json"
        rp.write_text(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
        summary["receipt_path"]=str(rp)
        summary["receipt_actual"]=digest(rp)
    print("B02J_JSON "+json.dumps(summary,sort_keys=True))
    return 0 if receipt["status"]=="PASS" else 1

if __name__=="__main__":
    sys.exit(main())
