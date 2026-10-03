#!/usr/bin/env python3
"""Exploratory cohort-pattern diagnostics. Not an individual-risk tool.
Run: python search_rules.py human; python search_rules.py calendar_null
Uses local input/pairs.tsv; exact input and output hashes are recorded.
"""
from __future__ import annotations
import argparse, calendar, hashlib, json, re, sys, unicodedata
from datetime import date, timedelta
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import numpy as np
import pandas as pd
import sklearn
import swisseph as swe
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.tree import DecisionTreeClassifier, export_text
from audit_baseline import numerology, reduce_num
ROOT=Path(__file__).parent
SEEDS=[20261003,20261017,20261031]
NAMES=['sun','mercury','venus','mars','jupiter','saturn','uranus','neptune','pluto']
PLANETS=[swe.SUN,swe.MERCURY,swe.VENUS,swe.MARS,swe.JUPITER,swe.SATURN,swe.URANUS,swe.NEPTUNE,swe.PLUTO]
SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
ASPECTS={0:'conjunction',60:'sextile',90:'square',120:'trine',180:'opposition'}
DOM=[{4},{2,5},{1,6},{0,7},{8,11},{9,10}]
EXALT=[0,5,11,9,3,6]
REQUEST=swe.FLG_MOSEPH|swe.FLG_SPEED
RETURN_FLAGS=set()

def write_json(path: Path, data: dict|list) -> None:
 path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def ascii_name(s: str) -> str:
 return ''.join(c for c in unicodedata.normalize('NFKD',s).upper() if 'A'<=c<='Z')

def cats(prefix: str, n: int, values=(*range(1,10),11,22,33)) -> dict[str,float]:
 return {f'{prefix}={v}':float(n==v) for v in values}

def date_nums(d:date) -> dict[str,float]:
 nf=numerology(d);out={}
 for k in ['lp','day','att','yearroot']:
  out.update(cats(f'date_{k}',int(nf[k])))
 out.update(cats('date_month',d.month,range(1,13)))
 total=int(nf['digit_sum']);out['date_digit_sum']=float(total)
 out.update(cats('date_straight_sum_root',reduce_num(total)))
 for k in ['lp_master','day_master','att_master']:out[f'date_{k}']=float(nf[k])
 return out

def name_nums(name:str) -> dict[str,float]:
 s=ascii_name(name);p={chr(65+i):i%9+1 for i in range(26)}
 c={ch:n for n,chs in enumerate(['AIJQY','BKR','CGLS','DMT','EHNX','UVW','OZ','FP'],1) for ch in chs}
 out={}
 for mn,mp in [('cyclic',p),('chaldean',c)]:
  for kind,seq in [('expression',s),('vowels',''.join(ch for ch in s if ch in 'AEIOU')),('consonants',''.join(ch for ch in s if ch not in 'AEIOU'))]:
   n=sum(mp[ch] for ch in seq);pre=f'name_{mn}_{kind}'
   out.update(cats(pre,reduce_num(n)));out[pre+'_raw_sum']=float(n)
 return out

@lru_cache(maxsize=None)
def sky(d:date) -> tuple[np.ndarray,np.ndarray]:
 jd=swe.julday(d.year,d.month,d.day,0.);lon=[];vel=[]
 for offset in np.linspace(-14.,36.,9):
  a=[];v=[]
  for p in PLANETS:
   value,flags=swe.calc_ut(jd+offset/24.,p,REQUEST);RETURN_FLAGS.add(flags)
   assert flags&swe.FLG_MOSEPH and not(flags&swe.FLG_SWIEPH),'Wrong ephemeris mode'
   a.append(value[0]%360.);v.append(value[3])
  lon.append(a);vel.append(v)
 return np.array(lon),np.array(vel)

def astro(d:date,n:int) -> dict[str,float]:
 lon,vel=sky(d);lon=lon[:,:n];vel=vel[:,:n];sign=(lon//30).astype(int);out={}
 for i,pn in enumerate(NAMES[:n]):
  out[pn+'_sin']=float(np.sin(np.deg2rad(lon[:,i])).mean())
  out[pn+'_cos']=float(np.cos(np.deg2rad(lon[:,i])).mean())
  for k,sn in enumerate(SIGNS):out[pn+'_in_'+sn]=float((sign[:,i]==k).mean())
  out[pn+'_retrograde']=float((vel[:,i]<0).mean())
  if i<6:
   out[pn+'_domicile']=float(np.isin(sign[:,i],list(DOM[i])).mean())
   out[pn+'_detriment']=float(np.isin(sign[:,i],[(k+6)%12 for k in DOM[i]]).mean())
   out[pn+'_exaltation']=float((sign[:,i]==EXALT[i]).mean())
   out[pn+'_fall']=float((sign[:,i]==(EXALT[i]+6)%12).mean())
 for i,j in combinations(range(n),2):
  sep=np.abs((lon[:,i]-lon[:,j]+180.)%360.-180.)
  for angle,an in ASPECTS.items():
   for orb in [3,6]:out[f'{NAMES[i]}_{an}_{NAMES[j]}_orb{orb}']=float((abs(sep-angle)<=orb).mean())
 for k in range(3):out[f'modality_count_{k}']=float((sign%3==k).sum(axis=1).mean())
 for k in range(4):out[f'element_count_{k}']=float((sign%4==k).sum(axis=1).mean())
 return out

def feature_blocks(d:date,name:str) -> dict[str,dict[str,float]]:
 theta=2*np.pi*(d.timetuple().tm_yday-1)/365.2425
 fmt={'name_length':float(len(ascii_name(name))),'name_words':float(len(name.split())),
      'name_initials':float(len(re.findall(r'(?:^|\s)[A-Za-z]\.',name))),
      'name_jr_suffix':float(bool(re.search(r'\bJr\.?$',name))),
      'name_nonascii':float(sum(ord(ch)>127 for ch in name))}
 dn=date_nums(d);nn=name_nums(name);a6=astro(d,6);a9=astro(d,9)
 return {'calendar':{'birth_year':float(d.year),'year_squared':(d.year-1960.)**2/100.,'doy_sin':float(np.sin(theta)),'doy_cos':float(np.cos(theta))},
 'name_format':fmt,'date_numerology':dn,'name_numerology':nn,'astrology6':a6,'astrology9':a9,
 'combined_date':{**dn,**a9},'combined_name':{**dn,**nn,**a9}}

def dataset(df:pd.DataFrame, random_dates:list[date]|None=None):
 blocks=[];ys=[];gs=[];ids=[]
 for idx,row in enumerate(df.itertuples()):
  for side,y in [('offender',1),('control',0)]:
   d=date.fromisoformat(getattr(row,side+'_dob'));name=getattr(row,side+'_name')
   if y==0 and random_dates is not None:d=random_dates[idx];name='CALENDAR CONTROL'
   blocks.append(feature_blocks(d,name));ys.append(y);gs.append(int(row.pair_id));ids.append(f'{row.pair_id}_{side}')
 out={};columns={}
 for fam in blocks[0]:
  cols=sorted(blocks[0][fam]);out[fam]=np.array([[b[fam][k] for k in cols] for b in blocks]);columns[fam]=cols
 return out,columns,np.array(ys),np.array(gs),ids

def folds(g:np.ndarray,n:int,seed:int):
 uniq=np.unique(g)
 return [(np.flatnonzero(np.isin(g,uniq[a])),np.flatnonzero(np.isin(g,uniq[b])))
         for a,b in KFold(n,shuffle=True,random_state=seed).split(uniq)]

def metrics(y,p) -> dict[str,float]:
 return {'auc':float(roc_auc_score(y,p)), 'balanced_accuracy':float(balanced_accuracy_score(y,p>=.5))}

def nested_tree(x,y,g,seed,cols):
 pred=np.zeros(len(y));receipts=[]
 for fold,(tr,te) in enumerate(folds(g,5,seed)):
  assert not set(g[tr])&set(g[te])
  model=GridSearchCV(DecisionTreeClassifier(random_state=seed),
   {'max_depth':[1,2,3,4],'min_samples_leaf':[4,8,12]},
   cv=folds(g[tr],3,seed+fold+1),scoring='roc_auc',n_jobs=1,refit=True,error_score='raise')
  model.fit(x[tr],y[tr]);pred[te]=model.predict_proba(x[te])[:,1]
  receipts.append({'fold':fold,'parameters':model.best_params_,'training':metrics(y[tr],model.predict_proba(x[tr])[:,1]),
   'test_pairs':sorted(map(int,set(g[te]))),'rules':export_text(model.best_estimator_,feature_names=cols,decimals=3)})
 return pred,receipts

def forest_cv(x,y,g,seed):
 pred=np.zeros(len(y))
 for tr,te in folds(g,5,seed):
  m=RandomForestClassifier(n_estimators=128,max_depth=4,min_samples_leaf=6,random_state=seed,n_jobs=1)
  m.fit(x[tr],y[tr]);pred[te]=m.predict_proba(x[te])[:,1]
 return pred

def run_human(df):
 xs,cols,y,g,ids=dataset(df);out={'status':'EXPLORATORY_INTERNAL_VALIDATION_ONLY','feature_counts':{f:x.shape[1] for f,x in xs.items()},'results':{}};raw=[]
 gap=np.repeat(abs(pd.to_datetime(df.offender_dob).dt.year-pd.to_datetime(df.control_dob).dt.year).to_numpy()<=5,2)
 for family,x in xs.items():
  records=[];receipts=[]
  for seed in SEEDS:
   p,rec=nested_tree(x,y,g,seed,cols[family]);rf=forest_cv(x,y,g,seed)
   records.append({'seed':seed,'nested_tree':metrics(y,p),'fixed_forest':metrics(y,rf)})
   receipts.append({'seed':seed,'folds':rec})
   for i in range(len(y)):raw.append({'id':ids[i],'pair':int(g[i]),'label':int(y[i]),'family':family,'seed':seed,'tree_score':float(p[i]),'forest_score':float(rf[i])})
  fit=DecisionTreeClassifier(max_depth=3,min_samples_leaf=8,random_state=SEEDS[0]).fit(x,y)
  deep=DecisionTreeClassifier(random_state=SEEDS[0]).fit(x,y)
  p53,_=nested_tree(x[gap],y[gap],g[gap],SEEDS[0],cols[family])
  out['results'][family]={'repeats':records,'mean_tree_auc':float(np.mean([r['nested_tree']['auc'] for r in records])),
   'mean_tree_balanced_accuracy':float(np.mean([r['nested_tree']['balanced_accuracy'] for r in records])),
   'mean_forest_auc':float(np.mean([r['fixed_forest']['auc'] for r in records])),
   'mean_forest_balanced_accuracy':float(np.mean([r['fixed_forest']['balanced_accuracy'] for r in records])),
   'whole_data_fit_depth3_leaf8':metrics(y,fit.predict_proba(x)[:,1]),'unrestricted_whole_data_fit':metrics(y,deep.predict_proba(x)[:,1]),
   'sensitivity_gap_le5_n53_nested_tree':metrics(y[gap],p53),'whole_data_rules':export_text(fit,feature_names=cols[family],decimals=3)}
  write_json(ROOT/f'fold_rules_{family}.json',receipts);write_json(ROOT/'human_results.json',out)
  print(family, {k:v for k,v in out['results'][family].items() if k.startswith('mean_')},flush=True)
 pd.DataFrame(raw).to_csv(ROOT/'heldout_predictions.csv',index=False)
 write_json(ROOT/'features.json',cols)
 np.savez_compressed(ROOT/'feature_matrices.npz',**xs,y=y,groups=g)
 return out

def run_null(df):
 out=[]
 for panel in range(10):
  rng=np.random.default_rng(SEEDS[0]+panel)
  ds=[date.fromisoformat(d) for d in df.offender_dob]
  controls=[date(d.year,1,1)+timedelta(days=int(rng.integers(366 if calendar.isleap(d.year) else 365))) for d in ds]
  xs,cols,y,g,_=dataset(df,controls)
  for family in ['date_numerology','astrology6','astrology9','combined_date']:
   x=xs[family];pred=np.zeros(len(y))
   for tr,te in folds(g,5,SEEDS[0]):
    m=DecisionTreeClassifier(max_depth=3,min_samples_leaf=8,random_state=SEEDS[0]);m.fit(x[tr],y[tr]);pred[te]=m.predict_proba(x[te])[:,1]
   rf=forest_cv(x,y,g,SEEDS[0]);out.append({'panel':panel,'family':family,'tree':metrics(y,pred),'forest':metrics(y,rf)})
  write_json(ROOT/'calendar_null.json',out);print('calendar panel',panel,flush=True)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['human','calendar_null']);args=ap.parse_args()
 path=ROOT/'input/pairs.tsv';df=pd.read_csv(path,sep='\t')
 assert len(df)==82 and df.pair_id.is_unique
 assert df.offender_name.nunique()==82 and df.control_name.nunique()==82
 for col in ['offender_dob','control_dob']:
  for v in df[col]:date.fromisoformat(v)
 assert reduce_num(33)==33 and reduce_num(39)==3 and reduce_num(22,False)==4
 assert len(ascii_name('Hâle'))==4
 if args.mode=='human':run_human(df)
 else:run_null(df)
 write_json(ROOT/f'manifest_{args.mode}.json',{'mode':args.mode,'source_projection_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'numpy':np.__version__,'pandas':pd.__version__,
 'sklearn':sklearn.__version__,'swisseph':swe.version,'ephemeris_requested':REQUEST,'ephemeris_returned':sorted(RETURN_FLAGS),
 'ephemeris':'MOSEPH exploratory noncanonical','v4_3_compliant':False,'scope':'Group-level diagnostic only; no individual-risk inference',
 'seeds':SEEDS,'unknown_time_samples_UTC_hours':list(map(float,np.linspace(-14,36,9))),'command':sys.argv})
if __name__=='__main__':main()
