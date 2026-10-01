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

# Compact owner update: the five installed Knowledge files are unchanged.
update_readme = '''# Update your existing Life Patterns GPT

This packet updates the GPT you already installed. Keep its existing five Knowledge files and its existing API-key/Bearer credential.

1. Replace the GPT's Instructions with the complete contents of INSTRUCTIONS-life-patterns-voice-interviewer-v2.md.
2. In Actions, reimport the existing schema URL or paste ACTION-life-patterns-submission-openapi.yaml. It contains valid JSON-formatted OpenAPI. Keep API key -> Bearer and the same key. Do not create a second duplicate Action.
3. Copy the Description and Conversation starters from GPT-BUILDER-CONFIG.md. The fourth starter is now: Check my independent Life Patterns review.
4. Keep Code Interpreter & Data Analysis enabled and save/update the GPT.

The backend and local review worker are deployed separately. The participant's next interview uses this sequence:
collect exact source -> queue an unfrozen candidate -> check review later -> ask any exact admitted clarification -> independent neutral review -> primary freeze -> three CF-003 questions -> final submission.

Queued work does not require the chat to remain open. The local review worker needs the researcher's computer online. The GPT does not wake itself later; return to the same chat and ask it to check the review. Keep the review ID private.

For your own test, attach your completed source-only interview record, not the older checkpoint containing hidden model interpretation. The GPT must preserve usable answers rather than restart or pretend it read a file that is absent.

No Knowledge-file change or new participant API key is required. This is a development pilot, not a prospectively validated scientific instrument. The full bundle remains available in the humandesign repository and the researcher's Downloads folder.
'''
update_files = {name: (RELEASE/name).read_bytes() for name in (
    'INSTRUCTIONS-life-patterns-voice-interviewer-v2.md',
    'GPT-BUILDER-CONFIG.md', 'ACTION-life-patterns-submission-openapi.yaml')}
update_files['UPDATE-EXISTING-GPT.md'] = update_readme.encode()
update_files['UPDATE-MANIFEST.json'] = (json.dumps({
    'version': VERSION,
    'full_bundle_sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
    'knowledge_files_changed': False,
    'existing_bearer_key_changes': False,
    'files': {name: hashlib.sha256(data).hexdigest() for name,data in update_files.items()},
}, indent=2)+'\n').encode()
update_zip = RELEASE.parent/'Life-Patterns-GPT-update-async-review-2026-10-01.zip'
with zipfile.ZipFile(update_zip, 'w', zipfile.ZIP_DEFLATED) as z:
    for name,data in sorted(update_files.items()):
        info=zipfile.ZipInfo(name,(2026,10,1,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,data)
with zipfile.ZipFile(update_zip) as z:
    assert z.testzip() is None
print(json.dumps({'update_zip_sha256':hashlib.sha256(update_zip.read_bytes()).hexdigest(),
                  'update_zip_bytes':update_zip.stat().st_size}))
