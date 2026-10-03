"""Post-result diagnostics of the 0.753 internal 53-pair result, not confirmation.
No retuning of primary method; repeat predeclared seeds and test nuisance baselines.
Random encodings preserve each encoding's letter-value multiset.
"""
import json,hashlib
import numpy as np,pandas as pd
from pathlib import Path
import search_rules as m
R=Path(__file__).parent

def evaluate(x,y,g,cols,seeds):
 out=[]
 for seed in seeds:
  p,rec=m.nested_tree(x,y,g,seed,cols)
  out.append({'seed':seed,**m.metrics(y,p)})
 return out

def randomized_name(name,rng):
 s=m.ascii_name(name);letters=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
 standard={chr(65+i):i%9+1 for i in range(26)}
 ch={c:n for n,cs in enumerate(['AIJQY','BKR','CGLS','DMT','EHNX','UVW','OZ','FP'],1) for c in cs}
 maps={}
 for label,d in [('cyclic',standard),('chaldean',ch)]:
  vals=rng.permutation([d[c] for c in letters]);maps[label]=dict(zip(letters,map(int,vals)))
 return s,maps

def main():
 df=pd.read_csv(R/'input/pairs.tsv',sep='\t');gap=abs(pd.to_datetime(df.offender_dob).dt.year-pd.to_datetime(df.control_dob).dt.year)
 df=df.loc[gap<=5].copy();xs,cols,y,g,ids=m.dataset(df);out={'status':'POST_RESULT_DIAGNOSTIC_NOT_CONFIRMATORY','n_pairs':len(df),'repeats':{}}
 for fam in ['date_numerology','name_numerology','astrology6','astrology9','combined_date','combined_name','calendar','name_format']:
  out['repeats'][fam]=evaluate(xs[fam],y,g,cols[fam],m.SEEDS)
  m.write_json(R/'candidate_checks.json',out);print(fam,out['repeats'][fam],flush=True)
 base=np.column_stack([xs['calendar'],xs['name_format']]);bc=cols['calendar']+cols['name_format']
 out['calendar_and_name_format']=evaluate(base,y,g,bc,m.SEEDS)
 # Evaluate performance of arbitrary replacement name encodings, not adjusted p-values.
 names=[getattr(r,side+'_name') for r in df.itertuples() for side in ['offender','control']]
 shuffled=[]
 for rep in range(10):
  rng=np.random.default_rng(20261101+rep)
  _,maps=randomized_name('ABC',rng);blocks=[]
  for name in names:
   s=m.ascii_name(name);d={}
   for mn,mp in maps.items():
    for kind,seq in [('expression',s),('vowels',''.join(c for c in s if c in 'AEIOU')),('consonants',''.join(c for c in s if c not in 'AEIOU'))]:
     n=sum(mp[c] for c in seq);pre=f'name_{mn}_{kind}';d.update(m.cats(pre,m.reduce_num(n)));d[pre+'_raw_sum']=float(n)
   blocks.append(d)
  nc=cols['name_numerology'];a=np.array([[b[c] for c in nc] for b in blocks])
  x=np.column_stack([xs['combined_date'],a]);columns=cols['combined_date']+nc
  p,_=m.nested_tree(x,y,g,m.SEEDS[0],columns)
  shuffled.append({'encoding_id':rep,**m.metrics(y,p)})
  out['random_letter_mapping_diagnostic']=shuffled;m.write_json(R/'candidate_checks.json',out);print('random encoding',rep,shuffled[-1],flush=True)
 m.write_json(R/'candidate_checks.json',out)
if __name__=='__main__':main()
