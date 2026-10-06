"""Package the collection-only correction and verify unchanged scientific/runtime bytes."""
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
VERSION = '2026-10-06.1-intro-progress-recovery'
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
changed = {'RECOVERY-GUIDE-v2.md','ACTION-HANDOFF-GUIDE-v1.md'}
unchanged = []
for row in m['knowledge_files']:
    p = ROOT/row['path']
    if p.name in changed:
        row['sha256'] = sha(p.read_bytes())
    else:
        assert row['sha256'] == sha(p.read_bytes()), p
        unchanged.append(row['path'])
assert len(unchanged)==4
assert m['action_schema']['sha256']=='e842fec5d4d0dfa0437dc6ff3e11543cda437ff27eba0f31cdb321c460b75d99'
(CUSTOM/'life_patterns_voice_gpt_manifest_v2.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
readme = '''# Life Patterns: intro, progress and recovery update

Version: 2026-10-06.1-intro-progress-recovery

Update the EXISTING GPT. This fixes collection behavior; the fast-review API, Action schema and credential are unchanged.

## Apply these three replacements

1. Replace Instructions with `INSTRUCTIONS-life-patterns-voice-interviewer-v2.md`.
2. Replace the old Knowledge file `RECOVERY-GUIDE-v2.md` with `knowledge/RECOVERY-GUIDE-v2.md`.
3. Replace the old Knowledge file `ACTION-HANDOFF-GUIDE-v1.md` with `knowledge/ACTION-HANDOFF-GUIDE-v1.md`.

Keep the other FOUR Knowledge files, existing Action and Bearer credential. Keep Code Interpreter & Data Analysis enabled. Select Update. `GPT-BUILDER-CONFIG.md` is owner setup documentation, not a seventh Knowledge file. The previous update changed only one guide; this one changes BOTH. Leaving the old recovery guide installed leaves the conflicting multiple-candidate rule in place.

If an interview is in progress, preserve its exact source-only checkpoint before updating. Keep its saved conversation and review receipt. Do not start a duplicate review or re-answer the interview.

## What changes

The only setup question is research consent when needed. The introduction says, “You are welcome to type or talk.” Useful earlier-life comparisons default to welcome, with skipping and explicit opt-out retained. Defaults are not recorded as something the participant explicitly said. Mode remains unknown unless supported by actual metadata or the participant's statement; no mode confirmation is required at freeze.

Progress now gives estimated remaining QUESTIONS and ANSWERING MINUTES until independent review, not just imported-reply counts or a topic. It uses the current revisable plan and a stated pace assumption when actual pace is unknown. Approximate percentages describe that plan, not scientific completeness, quality or the full study. Service waiting time is separate. A complete recovered interview shows zero new main-interview questions planned; the independent reviewer may still find useful clarifications.

Library recovery searches filename aliases and all canonical schemas, follows relevant pagination, and compares actual source provenance before selecting. Verified duplicates and successors are resolved automatically. Only genuine source conflicts or unrelated plausible lineages require a choice. A newer upload is not necessarily newer evidence; an empty or partial file cannot replace fuller preserved source. Incomplete recovery pauses interviewing instead of spawning new questions. Unrecovered turns remain explicitly unknown.

## Existing data and review

This package contains no participant answers or credentials. The frozen scientific instrument and four unchanged Knowledge files are preserved. CF-003 is **required in this bundle**, after reviewed primary freeze and before chart reveal; development-secondary status does not make it optional. Historical completion does not mean that independent review or final freeze has occurred. Existing review IDs/envelopes still govern any pending review. The previously delivered fast-batch workflow and stage-specific server wait estimates remain in force.

These are changes to the supplied GPT Instructions and Knowledge. Repository tests and isolated model probes cannot prove that an unedited private GPT is already running them. The editor must receive all three replacements above.
'''
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
update={name:allfiles[name] for name in ['INSTRUCTIONS-life-patterns-voice-interviewer-v2.md','GPT-BUILDER-CONFIG.md','knowledge/RECOVERY-GUIDE-v2.md','knowledge/ACTION-HANDOFF-GUIDE-v1.md']}
update['UPDATE-EXISTING-GPT.md']=readme.encode()
update['UPDATE-MANIFEST.json']=(json.dumps({'version':VERSION,'full_bundle_sha256':sha(full.read_bytes()),'knowledge_replacements':sorted(changed),'action_schema_changed':False,'existing_bearer_key_changes':False,'files':{k:sha(v) for k,v in update.items()}},indent=2)+'\n').encode()
archive=RELEASE.parent/'Life-Patterns-GPT-intro-progress-recovery-update-2026-10-06.zip'
write_zip(archive,update)
report={'version':VERSION,'instructions_characters':len(source),'instructions_strict':m['instructions']['strict_linebreak_count'],'update_zip':archive.name,'sha256':sha(archive.read_bytes()),'bytes':archive.stat().st_size,'unchanged_knowledge_files':unchanged,'action_schema_changed':False,'private_data_in_package':False}
(TASK/'PACKAGE-RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
