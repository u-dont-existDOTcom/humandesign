"""Package the versioned tendency-first collection policy."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
CUSTOM = ROOT / 'reference/custom_gpt'
RELEASE = CUSTOM / 'releases/life-patterns-voice-gpt-2026-09-30'
TASK = Path(__file__).resolve().parent
VERSION = '2026-10-06.2-tendency-first'
BASE = 'c06713febb1de31b51e8241469e9271a92a66b14'
sha = lambda b: hashlib.sha256(b).hexdigest()
m = json.loads((CUSTOM/'life_patterns_voice_gpt_manifest_v2.json').read_text())
m['version'] = VERSION
for field in ('instructions','builder_config','action_schema'):
    p = ROOT/m[field]['path']
    m[field]['sha256'] = sha(p.read_bytes())
source = (ROOT/m['instructions']['path']).read_text()
m['instructions']['characters'] = len(source)
m['instructions']['strict_linebreak_count'] = len(source)+source.count('\n')
assert m['instructions']['strict_linebreak_count'] < 8000
changed = {'TENDENCY-FIRST-GUIDE-v1.json'}
if not any(row['path'].endswith('TENDENCY-FIRST-GUIDE-v1.json') for row in m['knowledge_files']):
    m['knowledge_files'].append({'path':'reference/custom_gpt/TENDENCY-FIRST-GUIDE-v1.json','sha256':''})
unchanged = []
for row in m['knowledge_files']:
    p = ROOT/row['path']
    if p.name in changed:
        row['sha256'] = sha(p.read_bytes())
    else:
        assert row['sha256'] == sha(p.read_bytes()), p
        unchanged.append(row['path'])
assert len(unchanged)==6
assert m['action_schema']['sha256']=='e842fec5d4d0dfa0437dc6ff3e11543cda437ff27eba0f31cdb321c460b75d99'
(CUSTOM/'life_patterns_voice_gpt_manifest_v2.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
readme = (TASK/'UPDATE-EXISTING-GPT.md').read_text()
(TASK/'UPDATE-EXISTING-GPT.md').write_text(readme)
(RELEASE/'README-FIRST.md').write_text(readme)
files = {
    'INSTRUCTIONS-life-patterns-voice-interviewer-v2.md': ROOT/m['instructions']['path'],
    'GPT-BUILDER-CONFIG.md': CUSTOM/'GPT-BUILDER-CONFIG.md',
    'SETUP.md': CUSTOM/'LIFE-PATTERNS-VOICE-GPT-SETUP.md',
    'MANIFEST.json': CUSTOM/'life_patterns_voice_gpt_manifest_v2.json',
    'ACTION-life-patterns-submission-openapi.yaml': ROOT/m['action_schema']['path'],
}
files.update({'knowledge/'+Path(row['path']).name: ROOT/row['path'] for row in m['knowledge_files']})
for name,p in files.items():
    dest=RELEASE/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
allfiles={'README-FIRST.md': (RELEASE/'README-FIRST.md').read_bytes()}
allfiles.update({name:p.read_bytes() for name,p in files.items()})
assert set(p.relative_to(RELEASE).as_posix() for p in RELEASE.rglob('*') if p.is_file())==set(allfiles)

def write_zip(path, contents):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(contents.items()):
            info=zipfile.ZipInfo(name,(2026,10,6,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,data)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        assert {n:z.read(n) for n in z.namelist()}==contents

full=RELEASE.parent/'life-patterns-voice-gpt-2026-09-30.zip'
write_zip(full, {'life-patterns-voice-gpt-2026-09-30/'+k:v for k,v in allfiles.items()})
update={name:allfiles[name] for name in ['INSTRUCTIONS-life-patterns-voice-interviewer-v2.md','GPT-BUILDER-CONFIG.md','knowledge/TENDENCY-FIRST-GUIDE-v1.json']}
update['UPDATE-EXISTING-GPT.md']=readme.encode()
update['UPDATE-MANIFEST.json']=(json.dumps({'version':VERSION,'full_bundle_sha256':sha(full.read_bytes()),'knowledge_replacements':sorted(changed),'action_schema_changed':False,'existing_bearer_key_changes':False,'files':{k:sha(v) for k,v in update.items()}},indent=2)+'\n').encode()
archive=RELEASE.parent/'Life-Patterns-GPT-tendency-first-update-2026-10-06.zip'
write_zip(archive,update)
report={'version':VERSION,'instructions_characters':len(source),'instructions_strict':m['instructions']['strict_linebreak_count'],'update_zip':archive.name,'sha256':sha(archive.read_bytes()),'bytes':archive.stat().st_size,'unchanged_knowledge_files':unchanged,'action_schema_changed':False,'private_data_in_package':False}
(TASK/'PACKAGE-RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
