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
VERSION = '2026-10-05.1-fast-review-stages'
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
m['action_schema']['operation_ids'] = ['startLifePatternsReview','getLifePatternsReview','submitLifePatternsClarification','submitLifePatternsClarificationBatch','controlLifePatternsReview','submitLifePatternsRecords']
m['handoff'] = 'Queue candidate before freeze; retrieve independent review/clarifications; participant review; primary freeze; separate CF-003; strict reviewed submission.'
MANIFEST.write_text(json.dumps(m, indent=2, ensure_ascii=False)+'\n')
setup = CUSTOM/'LIFE-PATTERNS-VOICE-GPT-SETUP.md'
setup_text = setup.read_text()
setup_lines = setup_text.splitlines()
if len(setup_lines) > 2 and setup_lines[2].startswith('Version: '):
    suffix = ' Development collection surface.' if 'Development collection surface.' in setup_lines[2] else ''
    setup_lines[2] = f'Version: {VERSION}.' + suffix
setup.write_text('\n'.join(setup_lines) + ('\n' if setup_text.endswith('\n') else ''))
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
update_readme = '''# Update your existing Life Patterns GPT

Version: 2026-10-05.1-fast-review-stages

This is an UPDATE packet, not a new GPT and not a request to repeat the interview.

Before updating during an interview, ask the GPT to create its source-only live recovery checkpoint and verify its answer count. Keep the existing saved conversation and private review receipt.

## Three replacements in Edit GPT / Configure

1. Replace Instructions with the contents of INSTRUCTIONS-life-patterns-voice-interviewer-v2.md.
2. In Knowledge, remove the previous ACTION-HANDOFF-GUIDE-v1.md and upload knowledge/ACTION-HANDOFF-GUIDE-v1.md from this packet. Keep the other five Knowledge files unchanged.
3. Edit the EXISTING Action and import ACTION-life-patterns-submission-openapi.yaml (or reimport the existing schema URL). Keep its existing Bearer API credential. Do not create a duplicate Action or paste any secret into chat.

Keep Code Interpreter & Data Analysis enabled, then select Update to apply the changes. GPT-BUILDER-CONFIG.md is owner setup documentation, not a Knowledge file.

## What participants will see

New interviews use the reviewed fast first-question path. Independently useful questions arrive in a small batch but are asked one at a time in the chat. Their exact answers/skips go back in one Action. A changed premise can trigger early reconciliation instead of asking a now-invalid question.

Every waiting response must state the actual server stage, its estimated range and when to check back. The first clarification path has a roughly 1–3 minute pilot estimate. Reconciliation is provisionally 1–4 minutes. A broader omission check is provisionally 2–8 minutes. Full evidence preparation is provisionally 5–12 minutes (check after about 10), followed by an independent check provisionally 1–3 minutes. The service supplies more specific intervals for gap admission and wording review.

These are limited-pilot estimates from the start of a stage, not guaranteed total turnaround. Queue time is unknown. If the worker is offline or a stage runs long, the GPT reports that honestly instead of repeatedly promising completion. A blocked/error state needs repair, not more waiting.

Participants may leave and later send any message in the SAME saved conversation to check the same review. This workflow does not send automatic notifications. Existing queued reviews retain the legacy protocol so an update does not restart or duplicate their records.

## Short Preview check (no real participant data)

Verify the opening explains research consent, Railway approvals, and pause/skip/stop. Do not run a long real interview in Builder Preview. Use a normal saved GPT conversation for substantive records. Check that waiting guidance includes a stage, range, and check-back interval, and that the approval sentence occurs once per Action: “Please click Allow on this tool call to continue.”

## Unchanged boundaries

All participant-data/state-changing Actions still require normal consequential approval; the status GET remains read-only. No fixed lifetime clarification cap. No birth/chart data during the interview. Final primary freeze and CF-003 happen only after the independent full review is ready and the participant confirms it. A first question batch is not a completed final review.

The exact frozen behavioral instrument and other five Knowledge files are unchanged. The archive contains no participant records or credentials.
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
update_zip = RELEASE.parent/'Life-Patterns-GPT-fast-review-update-2026-10-05.zip'
with zipfile.ZipFile(update_zip, 'w', zipfile.ZIP_DEFLATED) as z:
    for name,data in sorted(update_files.items()):
        info=zipfile.ZipInfo(name,(2026,10,1,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,data)
with zipfile.ZipFile(update_zip) as z:
    assert z.testzip() is None
print(json.dumps({'update_zip_sha256':hashlib.sha256(update_zip.read_bytes()).hexdigest(),
                  'update_zip_bytes':update_zip.stat().st_size}))
