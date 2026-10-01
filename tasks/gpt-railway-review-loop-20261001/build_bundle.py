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
VERSION = '2026-10-01.4-review-pilot'
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
