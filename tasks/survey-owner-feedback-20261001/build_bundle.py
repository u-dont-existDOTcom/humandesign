"""Rebuild the pinned Custom GPT pilot archive without secrets or participant data."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]
CUSTOM = ROOT / 'reference/custom_gpt'
RELEASE = CUSTOM / 'releases/life-patterns-voice-gpt-2026-09-30'
MANIFEST = CUSTOM / 'life_patterns_voice_gpt_manifest_v2.json'
VERSION = '2026-10-01.5-feedback-recovery'
m = json.loads(MANIFEST.read_text())
m['version'] = VERSION
for field in ('instructions', 'builder_config', 'action_schema'):
    source = ROOT / m[field]['path']
    m[field]['sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
text = (ROOT / m['instructions']['path']).read_text()
m['instructions']['characters'] = len(text)
m['instructions']['strict_linebreak_count'] = len(text) + text.count('\n')
assert m['instructions']['strict_linebreak_count'] <= 8000
for item in m['knowledge_files']:
    assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest() == item['sha256']
m['action_schema']['operation_ids'] = ['startLifePatternsReview','getLifePatternsReview','submitLifePatternsClarification','controlLifePatternsReview','submitLifePatternsRecords']
m['handoff'] = 'Queue candidate before freeze; retrieve independent review/clarifications; participant review; primary freeze; separate CF-003; strict reviewed submission.'
MANIFEST.write_text(json.dumps(m, indent=2, ensure_ascii=False)+'\n')
setup = CUSTOM/'LIFE-PATTERNS-VOICE-GPT-SETUP.md'
setup.write_text(setup.read_text().replace('Version: 2026-10-01.4.', f'Version: {VERSION}.'))
files = {
    CUSTOM/'life_patterns_voice_interviewer_v2.md': RELEASE/'INSTRUCTIONS-life-patterns-voice-interviewer-v2.md',
    CUSTOM/'GPT-BUILDER-CONFIG.md': RELEASE/'GPT-BUILDER-CONFIG.md',
    setup: RELEASE/'SETUP.md',
    MANIFEST: RELEASE/'MANIFEST.json',
    ROOT/m['action_schema']['path']: RELEASE/'ACTION-life-patterns-submission-openapi.yaml',
}
files.update({ROOT/item['path']: RELEASE/'knowledge'/Path(item['path']).name for item in m['knowledge_files']})
for src,dest in files.items():
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src,dest)
allowed = set(files.values()) | {RELEASE/'README-FIRST.md'}
assert {p for p in RELEASE.rglob('*') if p.is_file()} == allowed
out = RELEASE.parent/'life-patterns-voice-gpt-2026-09-30.zip'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(allowed):
        name = str(p.relative_to(RELEASE.parent))
        info = zipfile.ZipInfo(name, (2026,10,1,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info,p.read_bytes())
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
print(json.dumps({'version':VERSION,'instructions_strict':m['instructions']['strict_linebreak_count'],
                  'files':len(allowed),'zip_sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2))

# Current update adds one handoff guide; prior five knowledge files remain unchanged.
update_readme = '''# Update the installed GPT: progress and recoverable review requests

1. Replace Instructions with INSTRUCTIONS-life-patterns-voice-interviewer-v2.md.
2. Add knowledge/ACTION-HANDOFF-GUIDE-v1.md as the SIXTH Knowledge file. Keep the previous five files.
3. Reimport ACTION-life-patterns-submission-openapi.yaml into the EXISTING Action. Same URL, same Bearer credential; no second Action.
4. Keep Code Interpreter & Data Analysis enabled; save/update the GPT.

Before submitting, the GPT must now create and link the exact unfrozen candidate backup, construct the correct three-field JSON envelope, and say: “Please click accept on this tool call to submit your results for analysis.”

A rejected request must produce both the preserved candidate backup and a safe diagnostic artifact. New server validation responses name the field/type without echoing private answers. A past generic error does not reveal which field was rejected.

Questions gain an honest stage/count footer. This also moves the question above the native down-arrow area; it does not change ChatGPT CSS or prove that the native button is fixed. No fabricated percentage, question quota, or time guarantee.

For an existing completed interview, read all usable prior answers first. Do not repeat a distinction merely because a prompt was reworded. The separately supplied hybrid question trial/audit is a development candidate, NOT silently substituted for frozen v7. This hotfix does not require another full interview.

To recover the current failed attempt, paste:
“Do not ask more interview questions. Preserve every existing imported answer and new answer from this chat with its original wording and corrections. Follow ACTION-HANDOFF-GUIDE-v1.md: create and link my unfrozen candidate backup, then show me the error diagnostic if one is available. Only then rebuild the valid start-review envelope and ask me to approve submission. Do not claim missing source text was recovered.”
'''
update_files = {name: (RELEASE/name).read_bytes() for name in (
    'INSTRUCTIONS-life-patterns-voice-interviewer-v2.md',
    'GPT-BUILDER-CONFIG.md', 'ACTION-life-patterns-submission-openapi.yaml')}
update_files['knowledge/ACTION-HANDOFF-GUIDE-v1.md'] = (CUSTOM/'ACTION-HANDOFF-GUIDE-v1.md').read_bytes()
update_files['UPDATE-EXISTING-GPT.md'] = update_readme.encode()
update_files['UPDATE-MANIFEST.json'] = (json.dumps({
    'version': VERSION,
    'full_bundle_sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
    'knowledge_files_changed': True,
    'existing_bearer_key_changes': False,
    'files': {name: hashlib.sha256(data).hexdigest() for name,data in update_files.items()},
}, indent=2)+'\n').encode()
update_zip = RELEASE.parent/'Life-Patterns-GPT-feedback-recovery-update-2026-10-01.zip'
with zipfile.ZipFile(update_zip, 'w', zipfile.ZIP_DEFLATED) as z:
    for name,data in sorted(update_files.items()):
        info=zipfile.ZipInfo(name,(2026,10,1,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,data)
with zipfile.ZipFile(update_zip) as z:
    assert z.testzip() is None
print(json.dumps({'update_zip_sha256':hashlib.sha256(update_zip.read_bytes()).hexdigest(),
                  'update_zip_bytes':update_zip.stat().st_size}))
