#!/usr/bin/env python3
"""Restore the frozen, fictional study using only checked-in bytes. No network."""
from __future__ import annotations
import hashlib
import io
import json
from pathlib import Path
import tarfile


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def restore(root: Path) -> int:
    manifest = json.loads((root / 'ARCHIVE-MANIFEST.json').read_text())
    chunks = []
    for part in manifest['parts']:
        name = part['name']
        if Path(name).name != name or not name.startswith('part-'):
            raise ValueError('Unsafe part name')
        data = (root / 'archive' / name).read_bytes()
        if len(data) != part['bytes'] or digest(data) != part['sha256']:
            raise ValueError(f'Archive part failed verification: {name}')
        chunks.append(data)
    archive = b''.join(chunks)
    if len(archive) != 120512 or digest(archive) != manifest['archive_sha256']:
        raise ValueError('Combined archive failed verification')
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:xz') as tar:
        members = tar.getmembers()
        if len(members) != 35 or sum(m.size for m in members) > 10_000_000:
            raise ValueError('Unexpected archive size')
        for member in members:
            name = member.name
            if not member.isfile() or name in ('', '.', '..') or Path(name).name != name or '\\' in name or name in files:
                raise ValueError('Unsafe or duplicate archive member')
            handle = tar.extractfile(member)
            if handle is None:
                raise ValueError('Unreadable archive member')
            files[name] = handle.read()
    inner = json.loads(files['MANIFEST.json'])
    expected = inner['files']
    if inner['algorithm'] != 'sha256' or set(expected) != set(files) - {'MANIFEST.json'}:
        raise ValueError('Inner manifest coverage mismatch')
    for name, expected_hash in expected.items():
        if digest(files[name]) != expected_hash:
            raise ValueError(f'Study file failed verification: {name}')
    destination = root / 'materialized'
    if destination.is_symlink():
        raise ValueError('Refusing symlink destination')
    destination.mkdir(exist_ok=True)
    for name, data in files.items():
        target = destination / name
        if target.is_symlink() or (target.exists() and target.read_bytes() != data):
            raise ValueError(f'Refusing to replace different existing bytes: {name}')
    for name, data in files.items():
        target = destination / name
        if not target.exists():
            with target.open('xb') as handle:
                handle.write(data)
    print(f'Verified and restored {len(files)} files into materialized/')
    return len(files)


if __name__ == '__main__':
    restore(Path(__file__).resolve().parent)
