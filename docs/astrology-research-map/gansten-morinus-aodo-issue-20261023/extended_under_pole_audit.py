#!/usr/bin/env python3
"""All-quadrant hemisphere parity of unmodified Morinus under-the-pole source.

Synthetic RA/declination only. Signed-oblique-ascension oracle derived
separately from geometric semi-arcs. One expression patched in-memory solely
for diagnosis. No original project file or installed application is altered.
"""
import ast,math,random,sys,json,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path("/tmp/gansten_morinus_compare_20261023")
sys.path.insert(0,str(ROOT))
import compare_morinus_source as m
OUT=Path(__file__).resolve().parent
S=ROOT/"Morinus"/"placidianutppd.py"
s=lambda x:math.sin(math.radians(x))
t=lambda x:math.tan(math.radians(x))
ai=lambda x:math.degrees(math.asin(x))
ang=lambda a,b:(a-b+180)%360-180

def oracle(lat,ramc,ras,decs,rap,decp):
    x=t(lat)*t(decs)
    if abs(x)>=1:raise ValueError("no ordinary semi-arc")
    ad=ai(x); dsa=90+ad;nsa=90-ad
    H=(ras-ramc)%360
    east=H<180
    above=H<dsa or H>360-dsa
    md=min(H,360-H) if above else abs(H-180)
    sa=dsa if above else nsa
    assert 0<md<sa
    adphi=(md/sa)*ad
    if abs(decs)<1e-8: pole=math.degrees(math.atan(md/sa*t(lat)))
    else:pole=math.degrees(math.atan(s(adphi)/t(decs)))
    arg=t(decp)*t(pole)
    if abs(arg)>=1:raise ValueError("promissor fails crossing")
    Q=ai(arg)
    sigcoord=ras-adphi if east else ras+adphi
    movcoord=rap-Q if east else rap+Q
    return ((movcoord-sigcoord)%360,east,above,sigcoord,pole)

def patched_method():
    tree=ast.parse(S.read_text())
    cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=="PlacidianUTPPD")
    fn=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=="toPlanet")
    candidates=[n for n in ast.walk(fn) if isinstance(n,ast.Assign) and len(n.targets)==1
        and isinstance(n.targets[0],ast.Name) and n.targets[0].id=="aodosig"
        and isinstance(n.value,ast.Call) and getattr(n.value.func,"attr",None)=="fabs"]
    assert len(candidates)==1
    candidate=candidates[0]
    original=candidate.value.args[0]
    candidate.value=ast.IfExp(
        test=ast.Name(id="sigeastern",ctx=ast.Load()),body=original,
        orelse=ast.UnaryOp(op=ast.USub(),operand=ast.parse(ast.unparse(original),mode="eval").body))
    ast.fix_missing_locations(fn)
    ns={"math":math,"chart":m.chart,"planets":m.planets,
        "primdirs":m.primdirs,"astrology":m.astrology,"util":m.util}
    exec(compile(ast.Module(body=[fn],type_ignores=[]),str(S),"exec"),ns)
    return ns["toPlanet"],candidate.lineno

def main():
    fn,line=patched_method()
    rng=random.Random(202610232337)
    rows=[];errors=[];tot=Counter();max_fix=0.0;max_old=0.0
    for hemi in (1,-1):
      for quad in ("EU","EL","WL","WU"):
        for region in ("near0","near360","interior"):
          c=Counter()
          for _ in range(400):
            lat=hemi*rng.uniform(8,65)
            decs=rng.uniform(-23,23)
            ad=ai(t(lat)*t(decs))
            dsa=90+ad
            ranges={"EU":(5,dsa-5),"EL":(dsa+5,175),
                    "WL":(185,360-dsa-5),"WU":(360-dsa+5,355)}
            h=rng.uniform(*ranges[quad])
            ras= (rng.uniform(0.05,12) if region=="near0"
                  else rng.uniform(348,359.95) if region=="near360"
                  else rng.uniform(60,300))
            ramc=(ras-h)%360
            rap=rng.uniform(0,360);decp=rng.uniform(-20,20)
            inp=(lat,ramc,ras,decs,rap,decp)
            try:ref,east,above,physical,pole=oracle(*inp)
            except ValueError:c["rejected"]+=1;continue
            pl,ps,rs=m.synthetic(lat,ramc,ras,decs)
            assert pl.eastern==east and pl.abovehorizon==above
            assert abs(ps.speculum[12]-pole)<1e-7,(inp,pole,ps.speculum[12])
            runner=m.Runner(pl,lat,ramc)
            try:
              original=runner.call(m.utp_method,True,99,-1,rap,decp,0,0,0)
              candidate=runner.call(fn,True,99,-1,rap,decp,0,0,0)
            except AssertionError:
              c["rejected"]+=1;continue
            err=abs(ang(original,ref));e2=abs(ang(candidate,ref))
            bad=err>1e-7
            c["valid"]+=1;c["bad"]+=bad;c["patched_bad"]+=e2>1e-7
            c["negative_coordinate"]+=physical<0
            c["unexplained_bad"]+=bad and physical>=0
            c["negative_but_good"]+=physical<0 and not bad
            max_fix=max(max_fix,e2);max_old=max(max_old,err)
            if bad and len(errors)<22:
              errors.append(dict(inputs=[round(x,10) for x in inp],
                group=[hemi,quad,region],signed_sigcoord=physical,
                encoded_AODO=ps.speculum[13],source=original,reference=ref,
                in_memory_fixed=candidate,original_error=err))
          rows.append(dict(hemisphere="N" if hemi==1 else "S",quad=quad,region=region,**c))
          tot.update(c)
    status=("PASS" if tot["patched_bad"]==0 and tot["bad"]==tot["negative_coordinate"]
        and tot["negative_but_good"]==0 and tot["unexplained_bad"]==0 else "INVESTIGATE")
    record=dict(status=status,samples_generated=9600,seed=202610232337,totals=dict(tot),
        source_commit="020492d5fce1c7a3d6b81186cef6cf04d93fb694",
        source_sha256=hashlib.sha256(S.read_bytes()).hexdigest(),
        location=f"placidianutppd.py:{line}",
        maximum_error_degrees=max_old,maximum_diagnostic_residual_deg=max_fix,
        matrix=rows,first_mismatches=errors,
        limits="original method+speculum without GUI/ephemeris; only conjunction synthetic RA/dec; no chart event predictions")
    (OUT/"CROSS_QUADRANT_PARITY.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps({k:v for k,v in record.items() if k not in ("matrix","first_mismatches")},indent=2))
    for q in rows:print(q)
    print("EXAMPLES",json.dumps(errors[:3],indent=2))
    if status!="PASS":raise SystemExit(1)
if __name__=="__main__":main()
