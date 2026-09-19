#!/usr/bin/env python3
"""Private immutable Chat records; no network, Git or background monitoring."""
from pathlib import Path
import argparse, fcntl, json, os, re, stat, sys, tempfile
KINDS={'presented_question','participant_answer','design_feedback','correction','inference_proposal','adjudication','pause','checkpoint'}
SOURCES={'usual_scenario_self_report','imagined_prediction','retrospective_usual_report','reported_actual_event','normative_view','unknown','declined','inapplicable'}
ID=re.compile(r'^[A-Za-z0-9_-]{1,80}$')
DEFAULT_ROOT=Path.home()/'.local/share/humandesign/private/chat-pilot-20260919'
def private_dir(path):
    if path.is_symlink(): raise ValueError('Symlink directory refused')
    if not path.exists(): path.mkdir(mode=0o700,parents=True)
    if not path.is_dir() or path.stat().st_uid!=os.getuid(): raise ValueError('Directory ownership/type refused')
    if stat.S_IMODE(path.stat().st_mode)&0o077: raise ValueError('Directory must be owner-private')
    for parent in [path,*path.parents]:
        if parent.is_symlink() or (parent/'.git').exists(): raise ValueError('Symlink ancestry or Git checkout refused')
def load_events(root):
    events=[]
    for path in sorted((root/'events').glob('*.json')):
        if path.is_symlink() or not path.is_file(): raise ValueError('Unsafe event file')
        if path.stat().st_uid!=os.getuid() or stat.S_IMODE(path.stat().st_mode)&0o077: raise ValueError('Event file must be owner-private')
        obj=json.loads(path.read_text(encoding='utf-8'))
        if obj.get('event_id')!=path.stem: raise ValueError('Event identity mismatch')
        events.append(obj)
    return events
def validate(event,existing):
    if not isinstance(event,dict) or event.get('kind') not in KINDS: raise ValueError('Unknown record kind')
    if not ID.fullmatch(str(event.get('event_id',''))): raise ValueError('Invalid event ID')
    for key in ('text','captured_at','source_surface'):
        if not isinstance(event.get(key),str) or not event[key]: raise ValueError('Missing event field: '+key)
    by_id={e['event_id']:e for e in existing}
    if event['kind']=='participant_answer':
        question=by_id.get(event.get('question_event_id'))
        if not question or question['kind']!='presented_question': raise ValueError('Answer requires a saved question')
        if event.get('source_kind') not in SOURCES: raise ValueError('Answer requires explicit evidence mode')
        if event.get('is_design_example') is not False: raise ValueError('Do not admit a design example as a participant answer')
    if event['kind'] in {'correction','adjudication'} and event.get('revises_event_id') not in by_id: raise ValueError('Revision must reference a saved event')
    if event['kind']=='presented_question' and (not event.get('scenario_id') or not event.get('scenario_version')): raise ValueError('Question requires scenario identity and version')
def encoded(obj): return (json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')
def sync_dir(root):
    fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)
def append_event(root,event):
    private_dir(root);private_dir(root/'events')
    lock_path=root/'.capture.lock'
    if lock_path.is_symlink(): raise ValueError('Symlink lock refused')
    fd=os.open(lock_path,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'a+') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        existing=load_events(root);validate(event,existing)
        target=root/'events'/(event['event_id']+'.json');payload=encoded(event);created=False
        if target.exists():
            if target.is_symlink() or target.read_bytes()!=payload: raise ValueError('Existing event ID has different bytes; append a correction instead')
        else:
            tmp_fd,temp_name=tempfile.mkstemp(prefix='.pending-',dir=root/'events')
            try:
                with os.fdopen(tmp_fd,'wb') as handle:
                    handle.write(payload);handle.flush();os.fsync(handle.fileno())
                os.link(temp_name,target);sync_dir(root/'events');created=True
            finally: os.unlink(temp_name)
        if target.read_bytes()!=payload: raise ValueError('Readback verification failed')
        events=load_events(root)
        return {'saved':True,'created':created,'event_count':len(events),'participant_answers':sum(e['kind']=='participant_answer' for e in events),'readback_verified':True}
def export(root):
    private_dir(root);events=load_events(root)
    return {'schema':'humandesign-private-chat-pilot-v1','not_a_railway_import_format':True,'source_sent_times_are_unknown_unless_explicit':True,'event_count':len(events),'participant_answers':sum(e['kind']=='participant_answer' for e in events),'events':events}
def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['append','export','status']);p.add_argument('--root',type=Path,default=DEFAULT_ROOT);a=p.parse_args()
    if a.action=='append': print(json.dumps(append_event(a.root,json.load(sys.stdin))))
    elif a.action=='export': print(encoded(export(a.root)).decode('utf-8'),end='')
    else:
        d=export(a.root);print(json.dumps({k:d[k] for k in ('event_count','participant_answers')}))
if __name__=='__main__': main()
