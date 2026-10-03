"""Algorithm-level replay of the saved pilot; not a copy of its source bytes."""
from pathlib import Path
import json,math
from datetime import date
from collections import Counter
import numpy as np,pandas as pd,swisseph as swe,sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,balanced_accuracy_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
ROOT=Path(__file__).parent
MASTERS={11,22,33}
PLANETS=[swe.SUN,swe.MERCURY,swe.VENUS,swe.MARS,swe.JUPITER,swe.SATURN]
PNAMES=['sun','mercury','venus','mars','jupiter','saturn']
def reduce_num(n,preserve_master=True):
 while n>9 and not(preserve_master and n in MASTERS): n=sum(map(int,str(n)))
 return n
def numerology(d):
 m=reduce_num(d.month);day=reduce_num(d.day);yr=reduce_num(sum(map(int,str(d.year))))
 lp=reduce_num(m+day+yr);att=reduce_num(d.month+d.day)
 return dict(lp=lp,day=day,att=att,month=d.month,yearroot=yr,lp_master=int(lp in MASTERS),day_master=int(day in MASTERS),att_master=int(att in MASTERS),digit_sum=sum(map(int,f'{d.year:04d}{d.month:02d}{d.day:02d}')))
def astrology(d):
 out={};signs=[]
 for p,name in zip(PLANETS,PNAMES):
  lon=float(swe.calc_ut(swe.julday(d.year,d.month,d.day,12.),p)[0][0]%360.);rad=math.radians(lon)
  out[f'{name}_sin']=math.sin(rad);out[f'{name}_cos']=math.cos(rad);signs.append(int(lon//30))
 out['mutable_count']=sum(s%3==2 for s in signs)
 for k in range(3):out[f'modality_{k}_count']=sum(s%3==k for s in signs)
 for k in range(4):out[f'element_{k}_count']=sum(s%4==k for s in signs)
 return out
def features(d,family):
 out={}
 if family=='calendar':
  t=2.*math.pi*(d.timetuple().tm_yday-1)/365.2425
  out.update(doy_sin=math.sin(t),doy_cos=math.cos(t),year=d.year,year2=((d.year-1960)**2)/100.)
 if family in {'numerology','combined'}:
  nf=numerology(d)
  for key in ['lp','day','att','month','yearroot']:
   for v in range(1,13) if key=='month' else [*range(1,10),11,22,33]:out[f'{key}_{v}']=int(nf[key]==v)
  for k in ['lp_master','day_master','att_master','digit_sum']:out[k]=nf[k]
 if family in {'astrology','combined'}:out.update(astrology(d))
 return out
def cv(rows,fam):
 ds=[features(r[1],fam) for r in rows];cols=sorted({k for d in ds for k in d});x=np.array([[d.get(c,0.) for c in cols] for d in ds]);y=np.array([r[2] for r in rows]);g=np.array([r[0] for r in rows]);pred=np.zeros(len(y))
 for tr,te in GroupKFold(5).split(x,y,g):
  model=make_pipeline(StandardScaler(),LogisticRegression(C=.25,max_iter=3000,solver='liblinear'))
  model.fit(x[tr],y[tr]);pred[te]=model.predict_proba(x[te])[:,1]
 return dict(auc=float(roc_auc_score(y,pred)),balanced_accuracy=float(balanced_accuracy_score(y,pred>=.5)))
def main():
 df=pd.read_csv(ROOT/'input/pairs.tsv',sep='\t');rows=[];delta=[]
 for r in df.itertuples():
  a=date.fromisoformat(r.offender_dob);b=date.fromisoformat(r.control_dob);delta.append(a.year-b.year)
  if abs(a.year-b.year)<=5:rows += [(r.pair_id,a,1),(r.pair_id,b,0)]
 result={'scope':'Algorithm-level replay from source-transcribed projection, no published p-values replayed','versions':{'numpy':np.__version__,'sklearn':sklearn.__version__,'swe':swe.version},'pairs':len(df),'pairs_gap_le5':len(rows)//2,'newer_case_pairs':sum(x>0 for x in delta),'newer_control_pairs':sum(x<0 for x in delta),'same_year_pairs':sum(x==0 for x in delta),'mean_year_delta':float(np.mean(delta)),'replayed_53_pair_metrics':{f:cv(rows,f) for f in ['calendar','numerology','astrology','combined']},'life_path_counts':dict(sorted(Counter(numerology(date.fromisoformat(d))['lp'] for d in df.offender_dob).items()))}
 (ROOT/'baseline_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
