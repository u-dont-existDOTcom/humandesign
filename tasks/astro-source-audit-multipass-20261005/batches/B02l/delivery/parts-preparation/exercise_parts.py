"""Isolated transport fixtures only; never contact a remote service or deliver files."""

import ast
import contextlib
import copy
import difflib
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from unittest.mock import patch
import urllib.error
import zipfile

ROOT = Path(__file__).resolve().parent
ORIGINAL = Path('/workspace/scratch/43f75264c32e/prepare_b02l_delivery.py')
REVISED = ROOT / 'prepare_b02l_delivery.py'
ORIGINAL_BYTES = ORIGINAL.read_bytes()
REVISED_BYTES = REVISED.read_bytes()
COMMIT = 'a' * 40
PREFIX = 'tasks/astro-source-audit-multipass-20261005/batches/B02l/'
RAW_PREFIX = 'https://raw.githubusercontent.com/u-dont-existDOTcom/humandesign/' + COMMIT + '/' + PREFIX
FIXTURES = ROOT / 'fixtures'
FIXTURES.mkdir(exist_ok=True)
RUN = Path(tempfile.mkdtemp(prefix='run-', dir=FIXTURES))
PRIVATE_BATCH = RUN / 'prepared-input'
PRIVATE_BATCH.mkdir()
OUTPUT = RUN / 'fixture-command.json'
ZIP_NAME = 'Astrology-Lilly-Dariot-Records-20261010.zip'
ZIP_PATH = 'deliverables/' + ZIP_NAME
ROW = '| Astrology book research | [astrology-book-research.md](astrology-book-research.md) | ChatGPT, current astrology research session; account identifier not exposed |'
OLD_INDEX = b'# Existing work notes\n| Work | Note | Context |\n| --- | --- | --- |\n| Prior | old.md | Prior context |\n'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def descriptor(path, raw):
    return {'path': path, 'filename': Path(path).name, 'bytes': len(raw),
            'sha256': sha(raw), 'git_blob_sha': blob(raw)}


archive_buffer = io.BytesIO()
with zipfile.ZipFile(archive_buffer, 'w') as archive:
    for filename, raw in [
        ('README.md', '# Synthetic archive fixture\nUnicode: é\n'.encode()),
        ('records.json', b'{"fixture_only":true}\n'),
        ('binary.dat', bytes(range(256)) + b'\0\xff\r\n'),
    ]:
        archive.writestr(zipfile.ZipInfo(filename, (2000, 1, 1, 0, 0, 0)), raw)
ZIP_BYTES = archive_buffer.getvalue()
payloads = {
    'deliverables/Astrology-Lilly-Dariot-Continue-20261010.md': b'# Fixture continuation\r\n',
    'deliverables/Astrology-Lilly-Dariot-Report-20261010.md': '# Fixture report\nUnicode: é\n'.encode(),
    'WORK_HANDOFF.md': b'# Fixture work handoff\nNot a real delivery.\n',
}
parts = []
for position in range(4):
    raw = ZIP_BYTES[len(ZIP_BYTES) * position // 4:len(ZIP_BYTES) * (position + 1) // 4]
    path = 'deliverables/parts/' + ZIP_NAME + f'.part-{position + 1:02d}-of-04'
    assert 0 < len(raw) <= 6_000_000
    payloads[path] = raw
    parts.append(descriptor(path, raw))
assert b''.join(payloads[part['path']] for part in parts) == ZIP_BYTES
zip_entry = {**descriptor(ZIP_PATH, ZIP_BYTES), 'publication_parts': parts}
manifest = {'files': [descriptor(path, payloads[path]) for path in payloads if path.startswith('deliverables/') and '/parts/' not in path]}
manifest['files'].insert(1, zip_entry)
(PRIVATE_BATCH / 'WORK_HANDOFF.md').write_bytes(payloads['WORK_HANDOFF.md'])

adapted = REVISED_BYTES.decode().replace(
    "Path('/workspace/scratch/43f75264c32e/humandesign-b02k/tasks/astro-source-audit-multipass-20261005/batches/B02l')",
    'Path(' + repr(str(PRIVATE_BATCH)) + ')',
).replace(
    "Path('/workspace/scratch/43f75264c32e/b02l-delivery-command.json')",
    'Path(' + repr(str(OUTPUT)) + ')',
)
assert adapted != REVISED_BYTES.decode()
fixture_preparer = RUN / 'prepare_fixture_only.py'
fixture_preparer.write_text(adapted)


def construct(input_manifest):
    (PRIVATE_BATCH / 'DELIVERABLES_MANIFEST.json').write_text(json.dumps(input_manifest))
    construction = subprocess.run([sys.executable, str(fixture_preparer), COMMIT], capture_output=True, text=True)
    assert construction.returncode == 0, construction.stderr
    package = json.loads(OUTPUT.read_text())
    command = package['command']
    header = "python3 - <<'PY'\n"
    assert command.startswith(header) and command.endswith('\nPY')
    body = command[len(header):-len('\nPY')]
    assert '\0' not in body
    tree = ast.parse(body)
    constants = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant)]
    assert b'\0' in constants and b'\r\n' in constants and b'\n' in constants
    pattern = next(value for value in constants if isinstance(value, bytes) and value.startswith(b'astro|'))
    assert re.search(pattern, b'Human    Design', re.I)
    expected_zip = next(entry for entry in package['expected']['files'] if entry['filename'] == ZIP_NAME)
    assert 'repo_path' not in expected_zip
    assert all(part['repo_path'] == PREFIX + part['path'] for part in expected_zip['publication_parts'])
    return body


class Response(io.BytesIO):
    status = 200


def layout(case):
    home = RUN / 'cases' / case / 'home'
    download = RUN / 'cases' / case / 'downloads'
    folder = home / 'claude-acceptance-transfer' / 'handoffs'
    folder.mkdir(parents=True)
    download.mkdir()
    index = folder / 'README.md'
    index.write_bytes(OLD_INDEX)
    return home, download, folder, index


def execute_fixture(body, home, download, remote_payloads):
    calls = []

    def fake_urlopen(request, timeout):
        assert timeout == 90
        assert request.full_url.startswith(RAW_PREFIX), request.full_url
        relative = request.full_url[len(RAW_PREFIX):]
        calls.append(relative)
        assert relative != ZIP_PATH, 'Complete ZIP must never be requested as one remote blob.'
        if relative not in remote_payloads:
            raise urllib.error.HTTPError(request.full_url, 404, 'Fixture part missing', {}, None)
        return Response(remote_payloads[relative])

    def fake_check_output(argv, text):
        assert argv == ['xdg-user-dir', 'DOWNLOAD'] and text is True
        return str(download) + '\n'

    captured = io.StringIO()
    error = None
    with patch('urllib.request.urlopen', side_effect=fake_urlopen), \
         patch('subprocess.check_output', side_effect=fake_check_output), \
         patch.object(Path, 'home', return_value=home), \
         contextlib.redirect_stdout(captured):
        try:
            exec(compile(body, '<isolated-parts-fixture>', 'exec'), {'__name__': '__main__'})
        except Exception as exc:
            error = exc
    raw_receipt = captured.getvalue()
    receipt = json.loads(raw_receipt) if raw_receipt else None
    assert str(home) not in raw_receipt and str(download) not in raw_receipt and str(ROOT) not in raw_receipt
    return receipt, error, calls


body = construct(manifest)
home, download, folder, index = layout('valid_join')
receipt, error, calls = execute_fixture(body, home, download, payloads)
assert error is None, error
assert (download / ZIP_NAME).read_bytes() == ZIP_BYTES
with zipfile.ZipFile(download / ZIP_NAME) as archive:
    assert archive.testzip() is None
    assert archive.read('binary.dat') == bytes(range(256)) + b'\0\xff\r\n'
assert index.read_bytes() == OLD_INDEX + ROW.encode() + b'\n'
assert receipt['source_commit'] == COMMIT
zip_receipt = next(entry for entry in receipt['downloads']['files'] if entry['filename'] == ZIP_NAME)
assert zip_receipt['transport'] == 'reconstructed_archive'
assert zip_receipt['complete_archive_is_single_published_git_blob'] is False
assert zip_receipt['content_derived_git_blob_sha'] == blob(ZIP_BYTES)
assert 'http_status' not in zip_receipt and 'git_blob_sha' not in zip_receipt
assert 'disk_bytes_equal_published' not in zip_receipt
assert zip_receipt['disk_bytes_equal_verified_artifact'] is True
assert zip_receipt['reconstruction_order'] == 'publication_parts_list_order'
for position, check in enumerate(zip_receipt['publication_parts'], start=1):
    expected = parts[position - 1]
    assert check['position'] == position and check['http_status'] == 200
    assert check['repo_path'] == PREFIX + expected['path']
    assert all(check[key] == expected[key] for key in ['filename', 'bytes', 'sha256', 'git_blob_sha'])
    assert all(check[key] is True for key in ['byte_count_verified', 'sha256_verified', 'git_blob_sha_verified'])
assert all(entry['transport'] == 'direct_http_file' for entry in receipt['downloads']['files'] if entry['filename'] != ZIP_NAME)
assert receipt['local_handoff']['transport'] == 'direct_http_file'
assert [path for path in calls if '/parts/' in path] == [part['path'] for part in parts]
assert len(calls) == 7
valid_receipt = copy.deepcopy(receipt)
before_repeat = index.read_bytes()
receipt, error, _ = execute_fixture(body, home, download, payloads)
assert error is None, error
assert index.read_bytes() == before_repeat
assert receipt['local_handoff']['index_operation'] == 'already_identical_row'
assert receipt['local_handoff']['note_operation'] == 'already_identical'
assert all(entry['operation'] == 'already_identical' for entry in receipt['downloads']['files'])
outcomes = [{'case': 'valid_join', 'parts': 4, 'exact_archive_bytes_installed': True,
             'archive_reads_as_valid_zip': True, 'per_part_receipt_checks_verified': True,
             'complete_zip_remote_request_count': 0, 'repeat_is_idempotent': True}]


def check_failure(case, input_manifest, remote_payloads, expected_type, expected_message):
    body = construct(input_manifest)
    home, download, folder, index = layout(case)
    receipt, error, calls = execute_fixture(body, home, download, remote_payloads)
    assert isinstance(error, expected_type), (case, error)
    assert expected_message in str(error), (case, error)
    assert not (download / ZIP_NAME).exists(), case
    assert index.read_bytes() == OLD_INDEX, case
    assert not (folder / 'astrology-book-research.md').exists(), case
    assert receipt is None, case
    outcomes.append({'case': case, 'rejected': True, 'error_type': type(error).__name__,
                     'error_category': expected_message, 'archive_not_installed': True,
                     'work_index_unchanged': True, 'completed_receipt_emitted': False,
                     'parts_requested': len([path for path in calls if '/parts/' in path])})


corrupted = dict(payloads)
target = parts[1]['path']
corrupted[target] = bytes([corrupted[target][0] ^ 1]) + corrupted[target][1:]
check_failure('corrupted_part', manifest, corrupted, AssertionError, 'SHA256 mismatch')

missing = dict(payloads)
del missing[target]
check_failure('missing_http_part', manifest, missing, urllib.error.HTTPError, '404')

out_of_order = copy.deepcopy(manifest)
out_of_order['files'][1]['publication_parts'][0:2] = reversed(out_of_order['files'][1]['publication_parts'][0:2])
check_failure('out_of_order_parts', out_of_order, payloads, AssertionError, 'SHA256 mismatch')

missing_descriptor = copy.deepcopy(manifest)
missing_descriptor['files'][1]['publication_parts'].pop()
check_failure('missing_listed_part', missing_descriptor, payloads, AssertionError, 'Byte count mismatch')

truncated = dict(payloads)
truncated[target] = truncated[target][:-1]
check_failure('truncated_part', manifest, truncated, AssertionError, 'Byte count mismatch')

wrong_part_git = copy.deepcopy(manifest)
wrong_part_git['files'][1]['publication_parts'][1]['git_blob_sha'] = '0' * 40
check_failure('wrong_part_git_blob_sha', wrong_part_git, payloads, AssertionError, 'Git blob SHA mismatch')

wrong_archive_git = copy.deepcopy(manifest)
wrong_archive_git['files'][1]['git_blob_sha'] = '0' * 40
check_failure('wrong_archive_content_git_sha', wrong_archive_git, payloads, AssertionError, 'Git blob SHA mismatch')


def unchanged_block(start, end):
    original = ORIGINAL_BYTES.decode().split(start, 1)[1].split(end, 1)[0]
    revised = REVISED_BYTES.decode().split(start, 1)[1].split(end, 1)[0]
    assert original == revised
    return True


unchanged = {
    'install_identical_or_new': unchanged_block('def install_identical_or_new(', '\ndownload = '),
    'work_index_and_handoff_installation': unchanged_block("folder = Path.home()", '\nprint(json.dumps('),
    'escape_normalization_and_output': unchanged_block('# The raw triple-quoted template', '\nTHIS_SENTINEL_IS_ABSENT'),
}
assert ORIGINAL.read_bytes() == ORIGINAL_BYTES
assert REVISED.read_bytes() == REVISED_BYTES
report = {
    'fixture_only': True,
    'actual_remote_calls': 0,
    'actual_delivery_performed': False,
    'canonical_source_test_count_unchanged': 20,
    'canonical_source_tests_added': 0,
    'original_preparer_sha256': sha(ORIGINAL_BYTES),
    'revised_preparer_sha256': sha(REVISED_BYTES),
    'original_preparer_unchanged': True,
    'normal_path_evidence': {
        'prior_fixture_diagnosis': '../delivery-diagnosis/FIXTURE_DIAGNOSIS.json',
        'unchanged_blocks_verified': unchanged,
        'direct_companions_and_handoff_also_exercised_in_valid_join': True,
    },
    'generated_source_compiles': True,
    'nul_newline_regex_values_preserved': True,
    'part_repo_paths_use_normal_batch_prefix': True,
    'private_filesystem_locators_omitted_from_receipts': True,
    'fixture_results': outcomes,
    'fixture_success_receipt_example': valid_receipt,
    'actual_issues_found': [],
}
(ROOT / 'EXECUTION_DIAGNOSIS.json').write_text(json.dumps(report, indent=2) + '\n')
(ROOT / 'PREPARER.diff').write_text(''.join(difflib.unified_diff(
    ORIGINAL_BYTES.decode().splitlines(keepends=True), REVISED_BYTES.decode().splitlines(keepends=True),
    fromfile='original/prepare_b02l_delivery.py', tofile='revised/prepare_b02l_delivery.py')))
print(json.dumps({key: value for key, value in report.items() if key != 'fixture_success_receipt_example'}, indent=2))
