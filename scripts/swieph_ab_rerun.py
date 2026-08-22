from __future__ import annotations
import json, math, os, time, hashlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import swisseph as swe

WHEEL_START=302.0
GATE_SPAN=360.0/64.0
LINE_SPAN=GATE_SPAN/6.0
GATE_SEQ=[41,19,13,49,30,55,37,63,22,36,25,17,21,51,42,3,27,24,2,23,8,20,16,35,45,12,15,52,39,53,62,56,31,33,7,4,29,59,40,64,47,6,46,18,48,57,32,50,28,44,1,43,14,34,9,5,26,11,10,58,38,54,61,60]
CHANNELS={
(4,63):('Ajna','Head'),(24,61):('Ajna','Head'),(47,64):('Ajna','Head'),
(11,56):('Ajna','Throat'),(17,62):('Ajna','Throat'),(23,43):('Ajna','Throat'),
(1,8):('G','Throat'),(7,31):('G','Throat'),(10,20):('G','Throat'),(13,33):('G','Throat'),
(12,22):('Solar Plexus','Throat'),(16,48):('Spleen','Throat'),(20,34):('Sacral','Throat'),
(20,57):('Spleen','Throat'),(21,45):('Heart','Throat'),(35,36):('Solar Plexus','Throat'),
(2,14):('G','Sacral'),(5,15):('G','Sacral'),(10,34):('G','Sacral'),(29,46):('G','Sacral'),
(10,57):('G','Spleen'),(25,51):('G','Heart'),(3,60):('Root','Sacral'),(9,52):('Root','Sacral'),
(42,53):('Root','Sacral'),(6,59):('Sacral','Solar Plexus'),(27,50):('Sacral','Spleen'),
(34,57):('Sacral','Spleen'),(18,58):('Spleen','Root'),(19,49):('Root','Solar Plexus'),
(28,38):('Spleen','Root'),(30,41):('Root','Solar Plexus'),(32,54):('Spleen','Root'),
(37,40):('Solar Plexus','Heart'),(39,55):('Root','Solar Plexus'),(26,44):('Heart','Spleen')}
CHANNELS={tuple(sorted(k)):v for k,v in CHANNELS.items()}
GATE_CENTER={64:'Head',61:'Head',63:'Head',47:'Ajna',24:'Ajna',4:'Ajna',43:'Ajna',17:'Ajna',11:'Ajna',62:'Throat',23:'Throat',56:'Throat',35:'Throat',12:'Throat',45:'Throat',33:'Throat',31:'Throat',8:'Throat',20:'Throat',16:'Throat',1:'G',2:'G',7:'G',10:'G',13:'G',15:'G',25:'G',46:'G',21:'Heart',26:'Heart',40:'Heart',51:'Heart',36:'Solar Plexus',22:'Solar Plexus',37:'Solar Plexus',6:'Solar Plexus',49:'Solar Plexus',55:'Solar Plexus',30:'Solar Plexus',5:'Sacral',14:'Sacral',29:'Sacral',34:'Sacral',59:'Sacral',9:'Sacral',3:'Sacral',42:'Sacral',27:'Sacral',48:'Spleen',57:'Spleen',44:'Spleen',50:'Spleen',32:'Spleen',28:'Spleen',18:'Spleen',58:'Root',38:'Root',54:'Root',53:'Root',60:'Root',52:'Root',19:'Root',39:'Root',41:'Root'}
BODY_IDS={'sun':swe.SUN,'moon':swe.MOON,'mercury':swe.MERCURY,'venus':swe.VENUS,'mars':swe.MARS,'jupiter':swe.JUPITER,'saturn':swe.SATURN,'uranus':swe.URANUS,'neptune':swe.NEPTUNE,'pluto':swe.PLUTO,'north_node':swe.TRUE_NODE}
OPP={GATE_SEQ[i]:GATE_SEQ[(i+32)%64] for i in range(64)}
CHANNEL_ORDER=sorted(CHANNELS)
EPHMASK=swe.FLG_JPLEPH|swe.FLG_SWIEPH|swe.FLG_MOSEPH
FLAGS=swe.FLG_SWIEPH|swe.FLG_SPEED
TOL=0.25/86400.0
STEP=0.25
START_DT=datetime.fromisoformat(os.environ.get('HD_START','1926-08-22T05:40:00+00:00'))
END_DT=datetime.fromisoformat(os.environ.get('HD_END','2026-08-22T05:40:00+00:00'))

def jd_from_dt(dt):
    dt=dt.astimezone(timezone.utc);h=dt.hour+dt.minute/60+dt.second/3600+dt.microsecond/3.6e9
    return swe.julday(dt.year,dt.month,dt.day,h,swe.GREG_CAL)
def dt_from_jd(jd):
    y,m,d,h=swe.revjul(jd,swe.GREG_CAL);hh=int(h);mm=int((h-hh)*60);ss=((h-hh)*60-mm)*60;sec=int(ss);micro=int(round((ss-sec)*1e6))
    if micro>=1000000:sec+=1;micro-=1000000
    return datetime(y,m,d,hh,mm,sec,micro,tzinfo=timezone.utc)
START=jd_from_dt(START_DT);END=jd_from_dt(END_DT);EXP_START=START-100;EXP_END=END

def lon_speed(jd,bid):
    xx,ret=swe.calc_ut(jd,bid,FLAGS);used=ret&EPHMASK
    if used!=swe.FLG_SWIEPH:raise RuntimeError(f'EPHEMERIS_FALLBACK body={bid} jd={jd} returned={used} retflags={ret}')
    return xx[0]%360.0,xx[3]
def gate_idx(l):return int(math.floor(((l-WHEEL_START)%360)/GATE_SPAN))%64
def line_idx(l):return int(math.floor(((l-WHEEL_START)%360)/LINE_SPAN))%384
def gate_line(l):
    gi=gate_idx(l);rem=((l-WHEEL_START)%360)-gi*GATE_SPAN;li=int(math.floor(rem/LINE_SPAN))+1
    return GATE_SEQ[gi],min(6,li)
def state_at(t,bid,kind):
    l,_=lon_speed(t,bid);return gate_idx(l) if kind=='gate' else line_idx(l)
def speed_at(t,bid):return lon_speed(t,bid)[1]
def station_root(a,b,bid,sa,sb):
    lo,hi=a,b;flo,fhi=sa,sb
    for _ in range(60):
        if hi-lo<TOL:break
        mid=(lo+hi)/2;fm=speed_at(mid,bid)
        if flo==0:return lo
        if fhi==0:return hi
        if flo*fm<=0:hi=mid;fhi=fm
        else:lo=mid;flo=fm
    return (lo+hi)/2
def target_from_state(st,kind,sp):
    span=GATE_SPAN if kind=='gate' else LINE_SPAN;n=64 if kind=='gate' else 384;bi=((st+1)%n) if sp>0 else st
    return (WHEEL_START+bi*span)%360
def angdiff(x,y):return ((x-y+180)%360)-180
def boundary_root(a,b,bid,kind,left_state=None,speed_hint=None):
    if left_state is None:left_state=state_at(a,bid,kind)
    if speed_hint is None:speed_hint=speed_at((a+b)/2,bid)
    target=target_from_state(left_state,kind,speed_hint);x=(a+b)/2
    for _ in range(7):
        l,sp=lon_speed(x,bid);f=angdiff(l,target)
        if abs(f)<1e-10:return x
        if abs(sp)<1e-10:break
        xn=x-f/sp
        if not a<=xn<=b:break
        x=xn
    lo,hi=a,b
    for _ in range(40):
        if hi-lo<TOL:break
        mid=(lo+hi)/2
        if state_at(mid,bid,kind)==left_state:lo=mid
        else:hi=mid
    return (lo+hi)/2
def segment_events(a,b,bid,kind,sa,sb,sta,stb):
    out=[]
    if sa*sb<0:
        ts=station_root(a,b,bid,sa,sb);sts=state_at(ts,bid,kind)
        if sta!=sts:out.append(boundary_root(a,ts,bid,kind,sta,sa))
        if sts!=stb:out.append(boundary_root(ts,b,bid,kind,sts,sb))
    elif sta!=stb:out.append(boundary_root(a,b,bid,kind,sta,(sa+sb)/2))
    return out
def generate(name,bid,kind):
    out=[];t=EXP_START;l,s=lon_speed(t,bid);st=gate_idx(l) if kind=='gate' else line_idx(l)
    while t<EXP_END:
        u=min(t+STEP,EXP_END);l2,s2=lon_speed(u,bid);st2=gate_idx(l2) if kind=='gate' else line_idx(l2)
        out.extend(segment_events(t,u,bid,kind,s,s2,st,st2));t=u;s=s2;st=st2
    return out
def forward_birth(dj):
    ld,_=lon_speed(dj,swe.SUN);x=dj+89.3
    for _ in range(8):
        lx,sp=lon_speed(x,swe.SUN);f=((lx-ld)%360)-88
        if abs(f)<1e-10:return x
        x-=f/max(abs(sp),1e-9)
    lo,hi=dj+75,dj+100
    def ff(t):return ((lon_speed(t,swe.SUN)[0]-ld)%360)-88
    flo=ff(lo)
    for _ in range(80):
        mid=(lo+hi)/2;fm=ff(mid)
        if hi-lo<TOL:return mid
        if flo*fm<=0:hi=mid
        else:lo=mid;flo=fm
    return (lo+hi)/2
def design_jd(birth):
    lb,_=lon_speed(birth,swe.SUN);x=birth-89.3
    for _ in range(8):
        ld,sp=lon_speed(x,swe.SUN);f=((lb-ld)%360)-88
        if abs(f)<1e-9:return x
        x+=f/max(abs(sp),1e-9)
    lo,hi=birth-100,birth-75
    def ff(t):return ((lb-lon_speed(t,swe.SUN)[0])%360)-88
    flo=ff(lo);fhi=ff(hi)
    if flo*fhi>0:raise RuntimeError('design root not bracketed')
    for _ in range(80):
        mid=(lo+hi)/2;fm=ff(mid)
        if abs(fm)<1e-10 or hi-lo<TOL:return mid
        if flo*fm<=0:hi=mid;fhi=fm
        else:lo=mid;flo=fm
    return (lo+hi)/2
def initial_state(mid):
    dj=design_jd(mid);acts={'p':{},'d':{}}
    for side,t in [('p',mid),('d',dj)]:
        for name,bid in BODY_IDS.items():
            l,_=lon_speed(t,bid);g,ln=gate_line(l);acts[side][name]=[g,ln]
        acts[side]['earth']=[OPP[acts[side]['sun'][0]],acts[side]['sun'][1]]
        acts[side]['south_node']=[OPP[acts[side]['north_node'][0]],acts[side]['north_node'][1]]
    return acts
def gate_counter(acts):return Counter(v[0] for side in acts.values() for v in side.values())
def arch_from_gates(gates):
    channels=[];centers=set();adj={}
    for pair in CHANNEL_ORDER:
        if pair[0] in gates and pair[1] in gates:
            channels.append(pair);c1=GATE_CENTER[pair[0]];c2=GATE_CENTER[pair[1]];centers|={c1,c2};adj.setdefault(c1,set()).add(c2);adj.setdefault(c2,set()).add(c1)
    def conn(a,b):
        if a not in centers or b not in centers:return False
        seen={a};stack=[a]
        while stack:
            x=stack.pop()
            if x==b:return True
            for y in adj.get(x,()):
                if y not in seen:seen.add(y);stack.append(y)
        return False
    motor=any(conn(m,'Throat') for m in ['Root','Solar Plexus','Heart','Sacral'])
    if not centers:typ='Reflector'
    elif 'Sacral' in centers:typ='Manifesting Generator' if motor else 'Generator'
    elif motor:typ='Manifestor'
    else:typ='Projector'
    if typ=='Reflector':auth='Lunar'
    elif 'Solar Plexus' in centers:auth='Emotional'
    elif 'Sacral' in centers:auth='Sacral'
    elif 'Spleen' in centers:auth='Splenic'
    elif 'Heart' in centers:auth='Ego Manifested' if conn('Heart','Throat') else 'Ego Projected'
    elif 'G' in centers and conn('G','Throat'):auth='Self-Projected'
    else:auth='Mental/Environmental'
    comps=0;seen=set()
    for c in centers:
        if c in seen:continue
        comps+=1;seen.add(c);stack=[c]
        while stack:
            x=stack.pop()
            for y in adj.get(x,()):
                if y not in seen:seen.add(y);stack.append(y)
    definition={0:'None',1:'Single',2:'Split',3:'Triple Split',4:'Quadruple Split'}.get(comps,f'{comps}-Split')
    return tuple(channels),frozenset(centers),typ,auth,definition
def apply_event(acts,counter,side,name,kind,after_gate,after_line):
    oldg,_=acts[side][name]
    if kind=='gate' and after_gate!=oldg:
        counter[oldg]-=1
        if counter[oldg]<=0:del counter[oldg]
        counter[after_gate]+=1;acts[side][name][0]=after_gate
        if name=='sun':
            eold=acts[side]['earth'][0];enew=OPP[after_gate];counter[eold]-=1
            if counter[eold]<=0:del counter[eold]
            counter[enew]+=1;acts[side]['earth'][0]=enew
        elif name=='north_node':
            sold=acts[side]['south_node'][0];snew=OPP[after_gate];counter[sold]-=1
            if counter[sold]<=0:del counter[sold]
            counter[snew]+=1;acts[side]['south_node'][0]=snew
    if name=='sun' and kind=='line':
        acts[side]['sun'][1]=after_line;acts[side]['earth'][1]=after_line
def core_fit(typ,auth,centers,pl,dl):
    s=0.0
    if typ=='Projector':s+=30
    if auth=='Splenic':s+=30
    for c,want,w in [('Sacral',False,5),('Solar Plexus',False,5),('Spleen',True,5),('Root',False,4),('Heart',True,3),('G',True,3)]:
        if ((c in centers)==want):s+=w
    raw=sum(w for l,w in [(2,6),(4,6),(6,3)] if pl==l or dl==l);s+=min(15.0,raw/12*15)
    return s
BASE_SUPPORT=[
('original_contribution',1.0,[('channel','1-8',1.0,1.0),('gate','1',0.55,0.75),('gate','8',0.40,0.75)]),
('insight_to_structure',1.0,[('channel','23-43',1.0,1.0),('gate','43',0.55,0.75),('gate','23',0.50,0.75)]),
('existential_mystery',1.0,[('channel','24-61',1.0,0.75),('gate','61',0.65,0.75),('gate','24',0.50,0.75)]),
('purpose_through_struggle',0.75,[('channel','28-38',1.0,0.75),('gate','28',0.50,0.75),('gate','38',0.50,0.75)]),
('enterprise_persuasion',1.0,[('channel','26-44',1.0,1.0),('gate','26',0.60,0.75),('gate','44',0.50,0.75)]),
('splenic_safety_self_behavior',0.75,[('channel','10-57',1.0,1.0),('channel','20-57',0.60,0.75),('gate','57',0.50,0.75)]),
('consequential_correction',0.75,[('channel','18-58',1.0,0.75),('gate','18',0.60,0.75),('gate','58',0.35,0.50)]),
('organized_reusable_systems',0.75,[('channel','17-62',1.0,0.75),('gate','62',0.60,0.75),('gate','17',0.45,0.75)]),
('concentrated_focus',0.75,[('channel','9-52',1.0,0.75),('gate','52',0.50,0.75),('gate','9',0.50,0.75)]),
('resource_sovereignty',0.75,[('channel','21-45',0.45,0.50),('gate','21',0.55,0.75),('gate','45',0.45,0.75)]),
('care_values',0.50,[('channel','27-50',0.70,0.75),('gate','50',0.45,0.50),('gate','27',0.40,0.50)]),
('retreat_privacy',0.75,[('gate','33',0.60,0.50),('gate','40',0.40,0.50)]),('projection_field',0.75,[('profile_line','5',1.0,0.75)])]
CONTRAS=[('mastery_repetition_as_independent_drive',1.0,'channel','16-48',0.75),('hierarchical_material_ambition',1.0,'channel','32-54',0.75),('need_to_be_first_competitive',0.75,'channel','25-51',0.50)]

def main():
    ephe=Path(os.environ.get('EPHE_PATH','data/ephemeris')).resolve();swe.set_ephe_path(str(ephe));print('EPHE_PATH',ephe,flush=True)
    for fn in ['sepl_18.se1','semo_18.se1']:
        p=ephe/fn
        if not p.exists():raise RuntimeError(f'missing {p}')
        print('EPHE_FILE',fn,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest(),flush=True)
    for dt in [START_DT,datetime(1985,1,29,tzinfo=timezone.utc),END_DT]:
        jd=jd_from_dt(dt)
        for name in ['sun','moon','mars','pluto']:lon_speed(jd,BODY_IDS[name])
        print('SWIEPH_PROBE_OK',dt.isoformat(),flush=True)
    t0=time.time();raw={}
    for name,bid in BODY_IDS.items():
        st=time.time();raw[(name,'gate')]=generate(name,bid,'gate');print('EVENTS',name,len(raw[(name,'gate')]),'sec',round(time.time()-st,2),flush=True)
    raw[('sun','line')]=generate('sun',swe.SUN,'line');print('EVENTS sun_lines',len(raw[('sun','line')]),flush=True)
    events=[];eps=2/86400.0
    for (name,kind),evs in raw.items():
        bid=BODY_IDS[name]
        for e in evs:
            la,_=lon_speed(e+eps,bid);ag,al=gate_line(la)
            if START<e<END:events.append((e,'p',name,kind,ag,al))
            if START-95<e<END-80:
                b=forward_birth(e)
                if START<b<END:events.append((b,'d',name,kind,ag,al))
    events.sort(key=lambda x:x[0]);groups=[]
    for ev in events:
        if groups and abs(ev[0]-groups[-1][0][0])*86400<=0.5:groups[-1].append(ev)
        else:groups.append([ev])
    bounds=[START]+[sum(e[0] for e in g)/len(g) for g in groups]+[END];print('BOUNDARIES',len(bounds),'elapsed',round(time.time()-t0,1),flush=True)
    acts=initial_state((bounds[0]+bounds[1])/2);counter=gate_counter(acts);states=[]
    for i in range(len(bounds)-1):
        a,b=bounds[i],bounds[i+1]
        if i>0:
            for _,side,name,kind,ag,al in groups[i-1]:apply_event(acts,counter,side,name,kind,ag,al)
        gates=frozenset(counter);channels,centers,typ,auth,definition=arch_from_gates(gates);pl=acts['p']['sun'][1];dl=acts['d']['sun'][1]
        states.append({'start':a,'end':b,'dur':b-a,'gates':gates,'channels':channels,'centers':centers,'type':typ,'auth':auth,'definition':definition,'pl':pl,'dl':dl,'pmoon':acts['p']['moon'][0],'dmars':acts['d']['mars'][0]})
    total=sum(s['dur'] for s in states);gate_d={g:0.0 for g in range(1,65)};ch_d={p:0.0 for p in CHANNEL_ORDER};line_d={l:0.0 for l in range(1,7)};pmoon24=dmars61=0.0
    for s in states:
        d=s['dur']
        for g in s['gates']:gate_d[g]+=d
        for p in s['channels']:ch_d[p]+=d
        for l in set([s['pl'],s['dl']]):line_d[l]+=d
        if s['pmoon']==24:pmoon24+=d
        if s['dmars']==61:dmars61+=d
    gp={g:v/total for g,v in gate_d.items()};cp={p:v/total for p,v in ch_d.items()};lp={l:v/total for l,v in line_d.items()};pp24=pmoon24/total;dp61=dmars61/total
    def ib(p):return min(6.0,-math.log2(max(p,1e-15)))
    def present(s,k,key):
        if k=='gate':return int(key) in s['gates']
        if k=='channel':return tuple(sorted(map(int,key.split('-')))) in s['channels']
        if k=='profile_line':return int(key) in (s['pl'],s['dl'])
    def prev(k,key):
        if k=='gate':return gp[int(key)]
        if k=='channel':return cp[tuple(sorted(map(int,key.split('-'))))]
        return lp[int(key)]
    for s in states:
        ev=0.0
        for _,conf,alts in BASE_SUPPORT:
            best=0.0
            for k,key,supp,flex in alts:
                if present(s,k,key):best=max(best,conf*supp*flex*ib(prev(k,key)))
            ev+=best
        if s['pmoon']==24:ev+=0.50*0.45*ib(pp24)
        if s['dmars']==61:ev+=0.75*0.75*0.75*ib(dp61)
        con=0.0;meaning=0
        for _,conf,k,key,sev in CONTRAS:
            if present(s,k,key):con+=conf*sev*4;meaning+=1 if sev>=0.5 else 0
        s['core']=core_fit(s['type'],s['auth'],s['centers'],s['pl'],s['dl']);s['evidence']=ev;s['contra']=con;s['net']=ev-con;s['legacy_total']=s['core']+s['net'];s['meaning']=meaning
        num=den=0.0
        for _,conf,alts in BASE_SUPPORT:
            den+=conf;best=0.0
            for k,key,supp,_ in alts:
                if present(s,k,key):best=max(best,supp)
            num+=conf*best
        s['detail']=100*num/den if den else 0
    merged=[]
    for s in states:
        sig=(round(s['legacy_total'],12),round(s['net'],12),round(s['core'],12),round(s['detail'],12),s['meaning'],s['type'],s['auth'],s['pl'],s['dl'],s['pmoon'],s['dmars'],s['channels'])
        if merged and merged[-1]['sig']==sig:merged[-1]['end']=s['end'];merged[-1]['dur']+=s['dur']
        else:t=dict(s);t['sig']=sig;merged.append(t)
    legacy=sorted(merged,key=lambda s:(-s['legacy_total'],-s['core'],-s['evidence'],s['start']))
    v43=sorted(merged,key=lambda s:(-s['net'],s['meaning'],-s['detail'],-s['core'],-s['dur'],s['start']))
    def rank(arr,keyfn):
        r=0;prev=None
        for j,s in enumerate(arr,1):
            k=keyfn(s)
            if k!=prev:r=j;prev=k
            s['_rank']=r
    rank(legacy,lambda s:(round(s['legacy_total'],9),round(s['core'],9),round(s['evidence'],9),round(s['contra'],9)))
    print('TOP_LEGACY_AB')
    for j,s in enumerate(legacy[:20],1):print(json.dumps({'order':j,'rank':s['_rank'],'start':dt_from_jd(s['start']).isoformat(),'end':dt_from_jd(s['end']).isoformat(),'score':round(s['legacy_total'],6),'net':round(s['net'],6),'core':round(s['core'],3),'type':s['type'],'authority':s['auth'],'profile':f"{s['pl']}/{s['dl']}",'pmoon':s['pmoon'],'dmars':s['dmars'],'channels':['-'.join(map(str,p)) for p in s['channels']]},sort_keys=True))
    rank(v43,lambda s:(round(s['net'],9),-s['meaning'],round(s['detail'],9),round(s['core'],9),round(s['dur'],9)))
    print('TOP_V43_ORDER_USING_SAME_EVIDENCE_TERMS_NONCANONICAL')
    for j,s in enumerate(v43[:20],1):print(json.dumps({'order':j,'rank':s['_rank'],'start':dt_from_jd(s['start']).isoformat(),'end':dt_from_jd(s['end']).isoformat(),'net':round(s['net'],6),'core':round(s['core'],3),'detail':round(s['detail'],3),'type':s['type'],'authority':s['auth'],'profile':f"{s['pl']}/{s['dl']}",'pmoon':s['pmoon'],'dmars':s['dmars'],'channels':['-'.join(map(str,p)) for p in s['channels']]},sort_keys=True))
    print('DONE elapsed',round(time.time()-t0,1),flush=True)
if __name__=='__main__':main()
