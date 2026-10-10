"""Build the B02j handoff and reproducible ZIP from a fixed source-core snapshot.

Only the Python standard library is required. This script does not publish or deliver.
Run only after source-core publication has been fetched and verified.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import zipfile

HERE=Path(__file__).resolve().parent
EXCLUDED={
    "MANIFEST.json","DELIVERABLES_MANIFEST.json",
    "PACKET_USABILITY.json","TEST_PACKET_USABILITY.txt",
    "DISTRIBUTION_RECEIPT.json","DELIVERY_RECEIPT.json",
    "FINAL_PUBLICATION_RECEIPT.json","CLOSEOUT.md",
}
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build(source_core_commit):
    if not re.fullmatch(r"[0-9a-f]{40}",source_core_commit):
        raise ValueError("An exact verified source-core commit is required")
    template=(HERE/"CONTINUE_HANDOFF_TEMPLATE.md").read_text(encoding="utf-8")
    if template.count("{{SOURCE_CORE_COMMIT}}")!=1:
        raise ValueError("Expected exactly one source-core placeholder")
    handoff=template.replace("{{SOURCE_CORE_COMMIT}}",source_core_commit)
    (HERE/"CONTINUE_HANDOFF.md").write_text(handoff,encoding="utf-8",newline="\n")
    out=HERE/"deliverables"
    out.mkdir(exist_ok=True)
    report_name="Astrology-Lilly-Fifth-House-20261010.md"
    handoff_name="Astrology-Lilly-Handoff-B02j-20261010.md"
    zip_name="Astrology-Lilly-Fifth-House-Records-20261010.zip"
    shutil.copyfile(HERE/"AUDIT_REPORT.md",out/report_name)
    shutil.copyfile(HERE/"CONTINUE_HANDOFF.md",out/handoff_name)
    selected=[]
    for path in sorted(HERE.rglob("*")):
        if not path.is_file():
            continue
        rel=path.relative_to(HERE)
        if "deliverables" in rel.parts or "__pycache__" in rel.parts:
            continue
        if path.suffix==".pyc" or path.name==".gitignore":
            continue
        if len(rel.parts)==1 and rel.name in EXCLUDED:
            continue
        selected.append(path)
    manifest={
        "schema_version":1,"batch":"B02j",
        "source_core_commit":source_core_commit,
        "files_count":len(selected),
        "self_hash_excluded":True,
        "scope":"Every selected packet file is hashed; MANIFEST.json is included in the ZIP but does not hash itself. Delivery outputs and post-build receipts are excluded to avoid circularity.",
        "files":[{"path":p.relative_to(HERE).as_posix(),"bytes":p.stat().st_size,"sha256":digest(p)} for p in selected],
    }
    manifest_path=HERE/"MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    members=selected+[manifest_path]
    with zipfile.ZipFile(out/zip_name,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in sorted(members):
            info=zipfile.ZipInfo("B02j/"+path.relative_to(HERE).as_posix(),date_time=(2026,10,10,0,0,0))
            info.create_system=3
            info.external_attr=0o100644<<16
            info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,path.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    result={
        "schema_version":1,"source_core_commit":source_core_commit,
        "zip_entry_count":len(members),"manifest_hashed_files":len(selected),
        "zip_metadata":"Fixed timestamps, sorted member paths, regular-file modes, DEFLATE level9. Byte reproducibility assumes fixed input files and compatible Python/zlib runtime.",
        "files":[{"filename":name,"relative_path":"deliverables/"+name,"bytes":(out/name).stat().st_size,"sha256":digest(out/name)} for name in [report_name,zip_name,handoff_name]],
    }
    (HERE/"DELIVERABLES_MANIFEST.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(result))
    return result

if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python3 build_delivery_packet.py VERIFIED_SOURCE_CORE_COMMIT")
    build(sys.argv[1])
