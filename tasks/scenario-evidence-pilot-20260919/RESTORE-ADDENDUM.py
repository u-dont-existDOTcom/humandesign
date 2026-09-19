#!/usr/bin/env python3
"""Restore the frozen fictional-data audit. Offline; no extracted code executes."""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import tarfile

PARTS = (
    ('part-01.bin', '3e8375634eb302e8b65175e834634d19b525d350152d9cd6dda1561b5d08dff3'),
    ('part-02.bin', '01042720af73befcf17906d0833ad8a1d6399f83a593c87b937a04699eefee79'),
)
ARCHIVE_HASH = '19b174d4f84b6fcb86890b0d5dd9a19441ad8a6be7068a87c3820b6b10f4694f'


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def restore(root: Path) -> int:
    chunks = []
    for name, expected in PARTS:
        data = (root / 'archive' / name).read_bytes()
        if len(data) != 9888 or sha256(data) != expected:
            raise ValueError(f'Archive part failed verification: {name}')
        chunks.append(data)
    archive = b''.join(chunks)
    if len(archive) != 19776 or sha256(archive) != ARCHIVE_HASH:
        raise ValueError('Combined archive failed verification')
    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:xz') as tar:
        members = tar.getmembers()
        if len(members) != 10 or sum(m.size for m in members) > 2_000_000:
            raise ValueError('Unexpected archive size')
        for member in members:
            name = member.name
            if (not member.isfile() or name in ('', '.', '..')
                    or Path(name).name != name or '\\' in name or name in files):
                raise ValueError('Unsafe or duplicate archive member')
            stream = tar.extractfile(member)
            if stream is None:
                raise ValueError('Unreadable archive member')
            files[name] = stream.read()
    manifest = json.loads(files['MANIFEST.json'])
    expected_files = manifest['files']
    if set(expected_files) != set(files) - {'MANIFEST.json'}:
        raise ValueError('Manifest coverage mismatch')
    for name, expected in expected_files.items():
        if sha256(files[name]) != expected:
            raise ValueError(f'File failed verification: {name}')
    destination = root / 'materialized'
    if destination.is_symlink():
        raise ValueError('Refusing symlink destination')
    destination.mkdir(exist_ok=True)
    for name, data in files.items():
        target = destination / name
        if target.is_symlink() or (target.exists() and target.read_bytes() != data):
            raise ValueError(f'Refusing to replace different bytes: {name}')
    for name, data in files.items():
        target = destination / name
        if not target.exists():
            with target.open('xb') as stream:
                stream.write(data)
    print(f'Verified and restored {len(files)} files into materialized/')
    return len(files)


if __name__ == '__main__':
    restore(Path(__file__).resolve().parent)
