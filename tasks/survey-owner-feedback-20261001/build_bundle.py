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
VERSION = '2026-10-02.3-review-context-recovery'
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
    source = ROOT/item['path']
    if item['path'] == 'reference/custom_gpt/ACTION-HANDOFF-GUIDE-v1.md':
        item['sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    else:
        assert hashlib.sha256(source.read_bytes()).hexdigest() == item['sha256']
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
update_readme = '''# Update the installed GPT: large-record review recovery

1. Replace Instructions with INSTRUCTIONS-life-patterns-voice-interviewer-v2.md.
2. Replace the existing Knowledge file ACTION-HANDOFF-GUIDE-v1.md with knowledge/ACTION-HANDOFF-GUIDE-v1.md. Keep the other five Knowledge files unchanged.
3. Reimport ACTION-life-patterns-submission-openapi.yaml into the EXISTING Action. Keep the same schema URL and Bearer credential; do not create a second Action.
4. Keep Code Interpreter & Data Analysis enabled; save/update the GPT.

This bundle includes the prior Action-approval and durable review-handoff repair. Before Railway Actions, the GPT explains the permission cards and that several per-step approvals can appear.

Large recovered records now keep every exact imported source turn while compacting only redundant admission-transport material. A `resource_limited / model_context_budget_exceeded` result remains pending, not complete. After the service-side repair is deployed, the GPT can `retry` the SAME saved review ID; it must not start a replacement review.

Before queueing, the GPT still creates `life-patterns-candidate-backup.json` and `life-patterns-review-handoff.json`; after queue success it preserves `life-patterns-review-receipt.json` when possible.

Frozen v7 question wording, source evidence semantics, independent admission, and CF-003 ordering are unchanged.
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
update_zip = RELEASE.parent/'Life-Patterns-GPT-review-context-recovery-update-2026-10-02.zip'
with zipfile.ZipFile(update_zip, 'w', zipfile.ZIP_DEFLATED) as z:
    for name,data in sorted(update_files.items()):
        info=zipfile.ZipInfo(name,(2026,10,1,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,data)
with zipfile.ZipFile(update_zip) as z:
    assert z.testzip() is None
print(json.dumps({'update_zip_sha256':hashlib.sha256(update_zip.read_bytes()).hexdigest(),
                  'update_zip_bytes':update_zip.stat().st_size}))
