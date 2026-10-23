"""Independent-of-work audit reproducibility diagnostics; not a historical engine."""
from __future__ import annotations
import hashlib, json, math, random, subprocess, sys
from pathlib import Path
from geometry_reference import (
 DomainError, EquatorialPoint, ascensional_difference, proportional_semi_arc_direction,
 placidean_under_pole_east_upper_north, regiomontanus_position_circle_direction,
 position_circle_residual, phase, semi_arcs, hour_angle_from_phase)

ROOT=Path(__file__).parent

def dal(x:float)->float: return math.degrees(math.asin(x))
def dr(x:float)->float: return math.radians(x)

def gon_aux_pole(lat:float,ramc:float,fixed:EquatorialPoint,moving:EquatorialPoint)->float:
  """Re-expression of Gansten audit Appendix-I 4c auxiliary angles (north/east/above only).
  Independent algorithm from `regiomontanus_position_circle_direction`.
  """
  m=(fixed.ra_deg-ramc)%360
  if not (0 < lat < 65 and 0 < m < 90+ascensional_difference(lat,fixed.dec_deg)):
    raise DomainError('branch unsupported')
  x=math.atan(math.tan(dr(fixed.dec_deg))/math.cos(dr(m)))
  y=dr(lat)-x
  z=math.atan(math.cos(y)/(math.tan(dr(m))*math.cos(x)))
  p=dal(math.sin(dr(lat))*math.cos(z))
  return ((moving.ra_deg-ascensional_difference(p,moving.dec_deg)) -
          (fixed.ra_deg-ascensional_difference(p,fixed.dec_deg)))%360


def circular_gap(a:float,b:float)->float: return abs((a-b+180)%360-180)


def diagnostics():
  rnd=random.Random(20261023)
  cases=5000
  pchecked=0; pmx=0.0; contact=0; cmx=0.0
  for _ in range(cases):
    lat=rnd.uniform(-63,63);theta=rnd.uniform(0,360)
    fixed=EquatorialPoint(rnd.uniform(0,360),rnd.uniform(-38,38))
    moving=EquatorialPoint(rnd.uniform(0,360),rnd.uniform(-38,38))
    try:
      a,b=semi_arcs(lat,fixed.dec_deg)
      c,d=semi_arcs(lat,moving.dec_deg)
      u=phase(theta-fixed.ra_deg,a,b)
      inv=hour_angle_from_phase(u,a,b)
      pmx=max(pmx,circular_gap(inv,theta-fixed.ra_deg))
      arc=proportional_semi_arc_direction(lat,theta,fixed,moving)
      cmx=max(cmx,circular_gap(u,phase(theta+arc-moving.ra_deg,c,d)))
      pchecked+=1
    except DomainError:pass
  rng=random.Random(330013)
  compared=0; gmax=0.0; gres=0.0; skipped=0
  for i in range(6000):
    lat=rng.uniform(2,60);theta=rng.uniform(0,360)
    dfix=rng.uniform(-23,23)
    try: ad=ascensional_difference(lat,dfix)
    except DomainError: continue
    m=rng.uniform(2,min(88,90+ad-2))
    fixed=EquatorialPoint((theta+m)%360,dfix)
    moving=EquatorialPoint(rng.uniform(0,360),rng.uniform(-23,23))
    try:
      v=regiomontanus_position_circle_direction(lat,theta,fixed,moving)
      w=gon_aux_pole(lat,theta,fixed,moving)
      compared+=1
      gmax=max(gmax,circular_gap(v,w))
      gres=max(gres,abs(position_circle_residual(lat,theta,fixed,moving,v)))
    except DomainError:skipped+=1
  return {
    'phase_random_attempted':cases,'phase_random_admitted':pchecked,
    'max_phase_inversion_degrees':pmx,'max_contact_phase_degrees':cmx,
    'regio_cartesian_vs_aux_attempted':6000,'regio_cartesian_vs_aux_compared':compared,
    'regio_explicit_domain_rejections':skipped,
    'regio_max_delta_degrees':gmax,
    'regio_max_plane_residual':gres,
    'source_cases':{
       'semi_arc_example_deg':proportional_semi_arc_direction(45,0,EquatorialPoint(50,15),EquatorialPoint(80,-10)),
       'under_pole_example_deg':placidean_under_pole_east_upper_north(45,0,EquatorialPoint(50,15),EquatorialPoint(80,-10)),
       'regio_example_deg':regiomontanus_position_circle_direction(45,0,EquatorialPoint(50,15),EquatorialPoint(80,-10))},
    'scope':'synthetic frozen-coordinate spherical calculations; no external historical application, ephemeris or human outcomes'
  }

if __name__=='__main__':
  run=subprocess.run([sys.executable,'-m','unittest','-v','test_geometry_reference'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  print(run.stdout)
  if run.returncode:sys.exit(run.returncode)
  result=diagnostics()
  # Do NOT print a false 'passed' if the two algorithms diverge.
  result['same_agent_independent_formulas_within_1e-8deg']=result['regio_max_delta_degrees']<1e-8 and result['max_contact_phase_degrees']<1e-8
  result['unit_tests']=9
  result['unit_test_exit_code']=run.returncode
  (ROOT/'VERIFICATION.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
  print(json.dumps(result,indent=2))
  sys.exit(0 if result['same_agent_independent_formulas_within_1e-8deg'] else 2)
