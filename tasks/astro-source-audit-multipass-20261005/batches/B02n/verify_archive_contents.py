"""Verify actual extracted payload bytes against frozen manifest before running mutable tests."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
def main():
 m=json.loads((B/'ARCHIVE_CONTENT_MANIFEST.json').read_text())
 seen=set()
 for v in m['files']:
  p=Path(v['path'])
  if p.is_absolute() or '..' in p.parts or str(p) in seen:raise ValueError('Invalid manifest member')
  seen.add(str(p))
  raw=(B/p).read_bytes()
  if len(raw)!=v['bytes'] or hashlib.sha256(raw).hexdigest()!=v['sha256']:raise ValueError('Manifest mismatch: '+str(p))
 if len(seen)!=m['file_count']:raise ValueError('Payload count mismatch')
 print(json.dumps({'files_verified':len(seen),'status':'PASS','validation':'exact bytes, not source meaning'}))
if __name__=='__main__':main()
