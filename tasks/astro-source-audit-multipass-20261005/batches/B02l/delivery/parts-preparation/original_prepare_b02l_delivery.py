"""Prepare an exact-commit delivery command; this file performs no remote write."""
import hashlib
import json
from pathlib import Path
import sys

BATCH = Path('/workspace/scratch/43f75264c32e/humandesign-b02k/tasks/astro-source-audit-multipass-20261005/batches/B02l')
commit = sys.argv[1]
assert len(commit) == 40 and all(c in '0123456789abcdef' for c in commit)
manifest = json.loads((BATCH/'DELIVERABLES_MANIFEST.json').read_text())
prefix = 'tasks/astro-source-audit-multipass-20261005/batches/B02l/'
files = [{**e, 'repo_path': prefix+e['path']} for e in manifest['files']]
raw = (BATCH/'WORK_HANDOFF.md').read_bytes()
note = {'filename': 'astrology-book-research.md', 'repo_path': prefix+'WORK_HANDOFF.md',
        'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
        'git_blob_sha': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
spec = {'commit': commit, 'files': files, 'handoff': note}
command = "python3 - <<'PY'\n" + 'SPEC = ' + repr(spec) + '\n' + r'''
from pathlib import Path
import fcntl
import hashlib
import json
import re
import subprocess
import urllib.request

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def get_exact(entry):
    url = 'https://raw.githubusercontent.com/u-dont-existDOTcom/humandesign/'+SPEC['commit']+'/'+entry['repo_path']
    request = urllib.request.Request(url, headers={'User-Agent':'HumanDesign-source-delivery'})
    with urllib.request.urlopen(request, timeout=90) as response:
        status = response.status
        raw = response.read()
    assert status == 200
    assert len(raw) == entry['bytes'] and sha(raw) == entry['sha256'] and blob(raw) == entry['git_blob_sha'], entry['filename']
    return raw, status

def install_identical_or_new(path, raw):
    if path.exists():
        assert path.is_file() and path.read_bytes() == raw, 'Existing nonidentical file: '+path.name
        operation = 'already_identical'
    else:
        with path.open('xb') as output:
            output.write(raw)
        operation = 'created'
    assert path.read_bytes() == raw
    return operation

download = Path(subprocess.check_output(['xdg-user-dir','DOWNLOAD'], text=True).strip())
assert download.is_dir()
results = []
for entry in SPEC['files']:
    raw, status = get_exact(entry)
    operation = install_identical_or_new(download/entry['filename'], raw)
    results.append({**{k:entry[k] for k in ['filename','bytes','sha256','git_blob_sha']},
                    'http_status': status, 'operation': operation, 'disk_bytes_equal_published': True})

folder = Path.home()/'claude-acceptance-transfer'/'handoffs'
index = folder/'README.md'
assert folder.is_dir() and index.is_file()
note = SPEC['handoff']
note_raw, note_status = get_exact(note)
note_operation = install_identical_or_new(folder/note['filename'], note_raw)
row = '| Astrology book research | [astrology-book-research.md](astrology-book-research.md) | ChatGPT, current astrology research session; account identifier not exposed |'
with index.open('r+b') as handle:
    fcntl.flock(handle, fcntl.LOCK_EX)
    old = handle.read()
    lines = old.splitlines(keepends=True)
    existing = [line.decode('utf-8').strip() for line in lines if re.search(rb'astro|human\s*design|lilly', line, re.I)]
    if existing:
        assert existing == [row], 'An existing work index row needs reconciliation before replacement.'
        new = old
        index_operation = 'already_identical_row'
    else:
        start = next(i for i,line in enumerate(lines) if line.lstrip().startswith(b'|') and b'work' in line.lower() and b'note' in line.lower())
        stop = start+1
        while stop < len(lines) and lines[stop].lstrip().startswith(b'|'):
            stop += 1
        prefix = b''.join(lines[:stop]); suffix = b''.join(lines[stop:])
        newline = b'\r\n' if lines[start].endswith(b'\r\n') else b'\n'
        insertion = (b'' if prefix.endswith(b'\n') else newline)+row.encode()+newline
        new = prefix+insertion+suffix
        assert new[:len(prefix)]+new[len(prefix)+len(insertion):] == old
        handle.seek(0);handle.write(new);handle.truncate();handle.flush()
        index_operation = 'added_one_work_row'
    handle.seek(0)
    assert handle.read() == new
    fcntl.flock(handle, fcntl.LOCK_UN)
assert (folder/note['filename']).read_bytes() == note_raw
assert index.read_bytes() == new and row.encode() in new
print(json.dumps({'batch':'B02l','source_commit':SPEC['commit'],
    'downloads':{'downloads_directory_basename':download.name,'file_count':len(results),'files':results,'all_delivered_and_verified':True},
    'local_handoff':{'note_filename':note['filename'],'note_bytes':len(note_raw),'note_sha256':sha(note_raw),
        'note_git_blob_sha':blob(note_raw),'http_status':note_status,'note_operation':note_operation,
        'note_disk_bytes_equal_published':True,'index_filename':'README.md','index_operation':index_operation,
        'index_before_sha256':sha(old),'index_after_sha256':sha(new),'prior_index_bytes_preserved':True,
        'matching_work_rows_after':1,'row_readback_matches':True}},ensure_ascii=False))
''' + '\nPY'
# The raw triple-quoted template keeps Python backslashes visible; convert the
# deliberate byte-literal escapes once to their executable source spelling.
command = command.replace("b'\\\\0'", "b'\\0'").replace("b'\\\\r\\\\n'", "b'\\r\\n'").replace("b'\\\\n'", "b'\\n'").replace("human\\\\s", "human\\s")
output = Path('/workspace/scratch/43f75264c32e/b02l-delivery-command.json')
output.write_text(json.dumps({'command':command,'expected':spec},ensure_ascii=False))
print(json.dumps({'output':str(output),'files':len(files),'note':note['filename'],'commit':commit}))
