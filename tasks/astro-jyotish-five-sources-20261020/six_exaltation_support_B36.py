"""Source-neutral astronomical feasibility guard scan. Moshier research only, no natal human data."""
import json,argparse
from collections import Counter
import swisseph as swe
swe.set_sid_mode(swe.SIDM_LAHIRI)
F=swe.FLG_MOSEPH|swe.FLG_SIDEREAL
P={'Sun':swe.SUN,'Moon':swe.MOON,'Mars':swe.MARS,'Venus':swe.VENUS,'Jupiter':swe.JUPITER,'Saturn':swe.SATURN}
SIGNS={'Jupiter':3,'Saturn':6,'Mars':9,'Sun':0,'Venus':11,'Moon':1}
def lon(j,n):
 v,fl=swe.calc_ut(j,P[n],F)
 if not (fl&swe.FLG_MOSEPH and fl&swe.FLG_SIDEREAL):raise ValueError((n,fl))
 return v[0]%360

def isclose(l,s,guard=15):
 x=s*30
 dist=(l-x)%360
 return dist < 30+guard or dist>360-guard

def scan(start,end):
 A=swe.julday(start,1,1,0,swe.GREG_CAL)
 Z=swe.julday(end,1,1,0,swe.GREG_CAL)
 n=round(Z-A);counts=Counter();matches=[];prefix_days=[]
 # 10-day sample plus +/- 15-degree sign guard. Jupiter/Saturn cannot move 15 degrees in 10 days.
 for block in range(0,n,10):
  jd=A+block
  if not isclose(lon(jd,'Jupiter'),3):continue
  if not isclose(lon(jd,'Saturn'),6):continue
  counts['guarded_10day_blocks']+=1
  for day in range(block,min(block+10,n)):
   t=A+day
   if int(lon(t,'Jupiter')//30)!=3:continue
   counts['Jupiter Cancer']+=1
   if int(lon(t,'Saturn')//30)!=6:continue
   counts['Jup Cancer + Sat Libra']+=1
   if int(lon(t,'Mars')//30)!=9:continue
   counts['+ Mars Capricorn']+=1
   if int(lon(t,'Sun')//30)!=0:continue
   counts['+ Sun Aries']+=1
   y,m,d,_=swe.revjul(t,swe.GREG_CAL)
   prefix_days.append(f'{y:+05d}-{m:02d}-{d:02d}')
   if int(lon(t,'Venus')//30)!=11:continue
   counts['+ Venus Pisces']+=1
   if int(lon(t,'Moon')//30)!=1:continue
   counts['+ Moon Taurus']+=1;matches.append(prefix_days[-1])
 return {'start_year_inclusive':start,'end_year_exclusive':end,'days':n,'counts':dict(counts),'sun_aries_candidate_days':prefix_days[:80],'full_six_exalted_matches':matches,'mode':'Moshier geocentric Lahiri sidereal 00UTC proleptic Gregorian','guard':'10-day blocks, 15-deg external padding for slow Jupiter and Saturn; confirm outer occupancy on every day in guarded blocks'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--start',type=int,default=1800);p.add_argument('--end',type=int,default=2200);a=p.parse_args()
 r=scan(a.start,a.end)
 if (a.start,a.end)==(1800,2200):
  assert r['days']==146097 and r['counts']['Jup Cancer + Sat Libra']==1339 and r['counts']['+ Mars Capricorn']==85
  assert r['counts'].get('+ Sun Aries',0)==0
 print(json.dumps(r,indent=2))
