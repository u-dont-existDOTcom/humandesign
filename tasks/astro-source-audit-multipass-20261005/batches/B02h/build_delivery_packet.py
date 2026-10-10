"""Package the published B02h core and its required computational companion."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parent
REPORT='Astrology-Lilly-Relatives-Reports-20261010.md'
ZIP='Astrology-Lilly-Relatives-Reports-Records-20261010.zip'
HANDOFF='Astrology-Lilly-Handoff-B02h-20261010.md'

VERIFY='''from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'PACKET_CONTENTS.json').read_text())
for row in m['files']:
    p=root/row['path']
    assert p.is_file(),str(p)
    assert len(p.read_bytes())==row['bytes'],str(p)
    assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],str(p)
print(json.dumps({'status':'PASS','verified_files':len(m['files'])}))
'''


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    receipt=json.loads((ROOT/'SOURCE_PUBLICATION_RECEIPT.json').read_text())
    commit=receipt['remote_source_commit'];out=ROOT/'deliverables';out.mkdir(exist_ok=True)
    shutil.copyfile(ROOT/'AUDIT_REPORT.md',out/REPORT)
    handoff=f'''# Continue Lilly source audit after the third-house section

The third-house source span is complete: PDF221 below divider through235, including XXIX–XXXI and all intervening sections. Published source revision: `{commit}`. Publication transport and owner delivery have separate receipts; this handoff identifies the immutable source revision used to build the packet.

## Exact next reading

Start **PDF236 / printed202** at **Of the fourth House, and the Judgment depending thereupon.** Include its whole preamble, then Chapter XXXII, **To find a thing hid or mislaid**, on that same page. The boundary page was inspected, not extracted. Never resume only at the numbered heading and drop the preamble.

## What is complete

-112 new source records, R897–R1008:75 general,37 worked-example records.
-1,008 cumulative Lilly plus1,066 retained Ptolemy =2,074 source records.
-15 original extraction page images checked; separate236 boundary check.
-Two printed charts/two historical enquiries, one hypothetical sibling reuse; two reported operational episodes within the absent-brother enquiry.
-44 coordinate rows;29 source/interpretation limitations retained.
-115 distinct focused tests passed:24 new,28 retained B02g,31 retained B02f,32 methodology/index. The ZIP's standalone new suite has24.

## Use the delivered files

The full report is `{REPORT}`. Extract `{ZIP}`, read `B02h/AUDIT_REPORT.md` and `B02h/README.md`, then run `python3 verify_packet.py` and `python3 -B -m unittest discover -s B02h -p 'test_*.py' -v` from the packet root. The required unchanged `B02f/lilly_presence_ship_reference.py` is included. No dependency has to be reconstructed from chat.

The packet contains the complete B02h inventory, transcribed numeric inputs, source/context/evidence ledgers, code, review material and logs, plus23 retained source records needed for its comparisons. It is not the whole cumulative corpus or originalPDF.

## Preserve the distinctions already established

House turning coexists with explicit original-figure6/8/12 references; the absent-brother example checks both eighth lords. Fear, distress, illness and death claims are separate outcomes with separate modalities. News truth, harm and political benefit differ. Cambridge's prospective non-capture has no stated horizon or separate confirming endpoint in these pages. Its sibling reuse is hypothetical, and exact sibling counts are explicitly declined.

CH01 Jupiter degree/sign remain null; conditional4/14/provisional24 readings are not resolved by the trine prose. CH01 node minutes and CH02 Venus minutes remain null. Printed Venus28:53 leaves1:07 to Capricorn; the source's one-degree/week statement remains qualitative and question-specific. No historical calendar, Eichstadius meridian reduction or physical future contact was recomputed.

## Recovery and boundaries

HumanDesign source index: `tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json`. Current dated checkpoint: `state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261010_B02h.md`. Full batch: `tasks/astro-source-audit-multipass-20261005/batches/B02h/`.

Retained original: `Lilly-1647-Christian-Astrology-I-III.pdf`, source `LILLY1647_WELLCOME_B30338724`, SHA-256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. Raw source stays outsideGit. Reuse the retained original; no new hash run was claimed inB02h.

Load current owner/project/source-provenance instructions before continuing. Earlier batches, old dated states, fitted models and prediction freezes remain unchanged. Do not replay historical blocked payloads at `state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md`, task `CURRENT_PASS.json` or `PASS_PLAN.json`. Ordinary new, authorized source-batch publication is a distinct operation.

The wider multi-author audit remains OPEN. This completed source-sized batch is an authorized saved pause boundary. No background continuation is claimed, no runtime model was promoted and no empirical predictive accuracy was established.
'''
    # Ensure CommonMark bullets have a space and do not resemble negative counts.
    handoff=handoff.replace('\n-112','\n- 112').replace('\n-1,008','\n- 1,008').replace('\n-15','\n- 15').replace('\n-Two','\n- Two').replace('\n-44','\n- 44').replace('\n-115','\n- 115')
    (out/HANDOFF).write_text(handoff)
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    repo=ROOT.parents[3]
    with tempfile.TemporaryDirectory() as folder:
        packet=Path(folder)
        for item in manifest['files']:
            src=repo/item['path']
            assert src.stat().st_size==item['bytes'],str(src)
            assert sha(src)==item['sha256'],str(src)
            rel=Path(item['path'])
            if str(rel).startswith('tasks/astro-source-audit-multipass-20261005/batches/B02h/'):
                dest=packet/'B02h'/src.relative_to(ROOT)
            else:
                dest=packet/'context'/src.name
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
        for name in ['MANIFEST.json','SOURCE_PUBLICATION_RECEIPT.json']:
            shutil.copyfile(ROOT/name,packet/'B02h'/name)
        (packet/'B02f').mkdir()
        shutil.copyfile(ROOT.parent/'B02f/lilly_presence_ship_reference.py',packet/'B02f/lilly_presence_ship_reference.py')
        shutil.copyfile(out/HANDOFF,packet/HANDOFF)
        (packet/'verify_packet.py').write_text(VERIFY)
        (packet/'READ_ME.md').write_text('# Lilly third-house packet\n\nStart with B02h/AUDIT_REPORT.md and B02h/README.md. Run python3 verify_packet.py, then the 24-test B02h suite documented there.\n\nEvidence ledgers preserve source-repository paths. The included Lilly and Ptolemy index snapshots and dated continuation state are under context/. The required earlier geometry helper is under B02f/. This packet contains the complete new batch and its declared companions, not every earlier source record.\n')
        files=[{'path':str(p.relative_to(packet)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(packet.rglob('*')) if p.is_file()]
        (packet/'PACKET_CONTENTS.json').write_text(json.dumps({'source_revision':commit,'files':files,'self_excluded':'PACKET_CONTENTS.json is excluded from its own recursive hash list.'},indent=2)+'\n')
        with zipfile.ZipFile(out/ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in sorted(packet.rglob('*')):
                if p.is_file():
                    info=zipfile.ZipInfo(str(p.relative_to(packet)),date_time=(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
                    info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
    rows=[{'filename':name,'path':'deliverables/'+name,'bytes':(out/name).stat().st_size,'sha256':sha(out/name)} for name in [REPORT,ZIP,HANDOFF]]
    (ROOT/'DELIVERABLES_MANIFEST.json').write_text(json.dumps({'source_revision':commit,'files':rows,'owner_destination':'OS-designated Downloads','report_matches_core':sha(out/REPORT)==sha(ROOT/'AUDIT_REPORT.md')},indent=2)+'\n')
    print(json.dumps({'source_revision':commit,'files':rows}))

if __name__=='__main__':main()
