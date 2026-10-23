#!/usr/bin/env python3
"""Bounded, research-only parity of unchanged Morinus SE source methods.

Executes three original Morinus toPlanet methods and original speculum classes
with harmless dependency stubs and synthetic equatorial points. Does not run
the complete wxPython application, build natal charts, or validate forecasts.
"""
import ast
import hashlib
import importlib.util
import json
import math
import random
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE / "Morinus"
EXPECTED = {
    "semi_arc": 42.17434402835047,
    "under_pole": 42.20081504892782,
    "regiomontanus": 46.449117851278395,
}
s = lambda d: math.sin(math.radians(d))
c = lambda d: math.cos(math.radians(d))
t = lambda d: math.tan(math.radians(d))
ai = lambda x: math.degrees(math.asin(x))

# The instrumented algorithm bodies are loaded unmodified from the pinned
# independent Morinus checkout; these tiny substitutes avoid wx/ephemeris.
chart = types.ModuleType("chart")
chart.Chart = types.SimpleNamespace(NONE=-1, CONJUNCTIO=0, OPPOSITIO=10,
        Aspects=[0.,30.,45.,60.,72.,90.,120.,135.,144.,150.,180.])
planets = types.ModuleType("planets")
planets.Planet = types.SimpleNamespace(
    LONG=0,LAT=1,RA=2,DECL=3,ADLAT=4,SA=5,MD=6,
    PMP=10,POH=12,AODO=13,POLE=7,W=9)
primdirs = types.ModuleType("primdirs")
primdirs.PrimDir = types.SimpleNamespace(NONE=-1)
primdirs.PrimDirs = types.SimpleNamespace(
    PLACSPECULUM=0,REGIOSPECULUM=1,
    SZNEITHER=0,SZPROMISSOR=1,SZSIGNIFICATOR=2,SZBOTH=3)
astrology = types.ModuleType("astrology")
astrology.SE_MOON = 1
houses = types.ModuleType("houses")
houses.Houses = types.SimpleNamespace(MC=0,RA=1)
util = types.ModuleType("util")
util.normalize = lambda a: a % 360.0
for mod in [chart, planets, primdirs, astrology, houses, util]:
    sys.modules[mod.__name__] = mod

def load_module(name):
    path=ROOT/(name+".py")
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

def original_method(filename,cls,func):
    """Compile exact original method AST, no source edits or rewrites."""
    path=ROOT/filename
    tree=ast.parse(path.read_text(encoding="utf-8"))
    owner=next(node for node in tree.body if isinstance(node,ast.ClassDef) and node.name==cls)
    node=next(node for node in owner.body if isinstance(node,ast.FunctionDef) and node.name==func)
    body=ast.Module(body=[node],type_ignores=[])
    ns={"math":math,"chart":chart,"planets":planets,
        "primdirs":primdirs,"astrology":astrology,"util":util}
    exec(compile(body,str(path),"exec"),ns)
    return ns[func], (node.lineno,node.end_lineno)

PS=load_module("placspec").PlacidianSpeculum
RS=load_module("regiospec").RegiomontanianSpeculum
semi_method,semi_lines=original_method("placidiansapd.py","PlacidianSAPD","toPlanet")
utp_method,utp_lines=original_method("placidianutppd.py","PlacidianUTPPD","toPlanet")
reg_method,reg_lines=original_method("regiomontanpd.py","RegiomontanPD","toPlanet")
getvars,_=original_method("placidiansapd.py","PlacidianSAPD","getvars")
getdiff,_=original_method("primdirs.py","PrimDirs","getDiff")

def synthetic(lat,ramc,ras,decs):
    ascmc2=[[None,ramc]]
    p=PS(lat,ascmc2,0.0,0.0,ras,decs)
    r=RS(lat,ascmc2,None,0.0,0.0,ras,decs)
    planet=types.SimpleNamespace(speculums=[p.speculum,r.speculum],
        eastern=p.eastern,abovehorizon=p.abovehorizon)
    return planet, p, r

class Runner:
    getvars=getvars
    getDiff=getdiff
    def __init__(self,planet,lat,ramc):
        self.chart=types.SimpleNamespace(planets=types.SimpleNamespace(planets=[planet]),
            place=types.SimpleNamespace(lat=lat))
        self.options=types.SimpleNamespace(subzodiacal=3,
            bianchini=False,pdsecmotion=False)
        self.ramc=ramc
        self.raic=(ramc+180)%360
        self.arcs=[]
    def create(self,mundane,prom,prom2,sig,promasp,sigasp,arc):
        self.arcs.append(arc)
    def call(self,method,*args):
        method(self,*args,calcsecmotion=False)
        if len(self.arcs)!=1:
            raise AssertionError("expected exactly one source algorithm arc "+str(self.arcs))
        return self.arcs.pop()%360

def compute(lat,ramc,ras,decs,ram,decm):
    obj,p,r=synthetic(lat,ramc,ras,decs)
    opts=Runner(obj,lat,ramc)
    prom_ad=ai(t(lat)*t(decm))
    semi=opts.call(semi_method,True,99,-1,ram,prom_ad,0,0,0)
    utp=opts.call(utp_method,True,99,-1,ram,decm,0,0,0)
    regio=opts.call(reg_method,True,99,-1,0,0,ram,decm,0,0,0)
    return {"semi_arc":semi,"under_pole":utp,"regiomontanus":regio,
      "source_speculum":{"POH":p.speculum[12],"AODO":p.speculum[13],
         "REGIO_POLE":r.speculum[7],"REGIO_W":r.speculum[9]}}

def angular_diff(a,b):
    return (a-b+180)%360-180

def main():
    got=compute(45,0,50,15,80,-10)
    checks={}
    for name,expect in EXPECTED.items():
        checks[name]={"morinus":got[name],"prior_independent":expect,
             "abs_delta":abs(angular_diff(got[name],expect))}
        assert checks[name]["abs_delta"]<1e-8,checks[name]
    checks["source_speculum"]=got["source_speculum"]
    # Random independent tests: exact position-circle Cartesian source from
    # the previous project package and unchanged Morinus source under one
    # declared northern/east/above quadrant. Any failure is retained.
    import zipfile
    pkg=Path("/mnt/hdd/home/joel/Téléchargements/gansten-astro/Gansten_Primary_Directions_Reconciliation_20261023.zip")
    if not pkg.exists():
        pkg=Path("/mnt/data/Gansten_Primary_Directions_Reconciliation_20261023.zip")
    reference_file=HERE/"geometry_reference.py"
    if reference_file.exists():
        raw=reference_file.read_bytes()
    else:
        with zipfile.ZipFile(pkg) as z:
            raw=z.read("geometry_reference.py")
    refmod=types.ModuleType("gansten_reference_recovered")
    sys.modules[refmod.__name__]=refmod
    refns=refmod.__dict__
    exec(compile(raw,"reference_geometry.py","exec"),refns)
    from_ref=refns["EquatorialPoint"]
    rng=random.Random(20261023)
    max_delta={"semi_arc":0.,"regiomontanus":0.,"under_pole":0.}
    attempts=0;passed=0;unmatched=[]
    for i in range(1200):
        lat=rng.uniform(10,65)
        ramc=rng.uniform(0,360)
        decs=rng.uniform(-25,25)
        ad=ai(t(lat)*t(decs))
        ras=(ramc+rng.uniform(4,90+ad-4))%360
        decm=rng.uniform(-20,20)
        ram=(ramc+rng.uniform(4,165))%360
        attempts+=1
        try:
            mor=compute(lat,ramc,ras,decs,ram,decm)
            fix=from_ref(ras,decs);mov=from_ref(ram,decm)
            refs={
             "semi_arc":refns["proportional_semi_arc_direction"](lat,ramc,fix,mov),
             "regiomontanus":refns["regiomontanus_position_circle_direction"](lat,ramc,fix,mov),
             "under_pole":refns["placidean_under_pole_east_upper_north"](lat,ramc,fix,mov)
            }
            deltas={k:abs(angular_diff(mor[k],refs[k])) for k in max_delta}
            if any(d>1e-7 for d in deltas.values()):
                unmatched.append({"case":i,"input":[lat,ramc,ras,decs,ram,decm],
                    "morinus":{k:mor[k] for k in max_delta},"reference":refs,"deltas":deltas})
            else:passed+=1
            for k,v in deltas.items():max_delta[k]=max(max_delta[k],v)
        except Exception as e:
            unmatched.append({"case":i,"error":type(e).__name__+": "+str(e),
                         "input":[lat,ramc,ras,decs,ram,decm]})
    report={
       "status":"MORINUS_SOURCE_ROUTINES_ONLY_NOT_FULL_APPLICATION",
       "program":"IngenieriaAstrologica/Morinus",
       "commit":"020492d5fce1c7a3d6b81186cef6cf04d93fb694",
       "execution":"original AST method bodies and original speculum classes, using dependency stubs on synthetic points",
       "synthetic":checks,
       "grid":{"attempts":attempts,"passed":passed,
              "mismatches_or_rejected":len(unmatched),
              "max_abs_deltas":max_delta,"first_failures":unmatched[:15]},
       "method_lines":{"semi_arc":semi_lines,"under_pole":utp_lines,"regiomontanus":reg_lines},
       "source_sha256":{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in [
          "placspec.py","regiospec.py","placidiansapd.py",
          "placidianutppd.py","regiomontanpd.py"]},
       "reference_sha256":hashlib.sha256(raw).hexdigest(),
       "full_application":False,
       "actual_ephemeris":False,
       "human_predictive_validation":False}
    output=HERE/"MORINUS_PARITY.json"
    output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print("SYNTH",json.dumps(checks,indent=2))
    print("GRID",json.dumps(report["grid"],indent=2))
    print("OUTPUT",output)
    if unmatched:
        raise SystemExit(1)
if __name__=="__main__":main()
