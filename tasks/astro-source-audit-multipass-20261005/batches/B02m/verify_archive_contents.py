"""Verify all frozen payload bytes before running tests that refresh their logs."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
def main():
    m=json.loads((ROOT/'ARCHIVE_CONTENT_MANIFEST.json').read_text())
    seen=set()
    for x in m['files']:
        p=Path(x['path'])
        if p.is_absolute() or '..' in p.parts or x['path'] in seen:raise ValueError('Invalid manifest path')
        seen.add(x['path']);raw=(ROOT/p).read_bytes()
        if len(raw)!=x['bytes'] or hashlib.sha256(raw).hexdigest()!=x['sha256']:raise ValueError('Byte mismatch: '+x['path'])
    if len(seen)!=m['payload_count']:raise ValueError('Count mismatch')
    print(json.dumps({'payload_hashes_verified':len(seen),'status':'PASS','scope':'byte integrity only'}))
if __name__=='__main__':main()
