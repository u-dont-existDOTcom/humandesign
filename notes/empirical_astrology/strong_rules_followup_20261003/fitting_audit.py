"""Exploratory diagnostic: same fixed tree in-sample, held out, and label-shuffled."""
from pathlib import Path
import json
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import search_rules as s
root=Path(__file__).parent
pairs=s.load_pairs(root.parent/'murderer_birth_pattern_pilot_20261003/paired_cohort.csv')
out={}
for name, cohort, by_year in [('original',pairs,False),('exact_year',s.exact_year_pairs(pairs),True)]:
 rows,groups=s.make_rows(cohort,by_year);x,cols=s.matrix(rows,'fusion');y=np.array([r['y'] for r in rows])
 vals=[]
 for rep in range(3):
  pred=np.zeros(len(y))
  for a,b in s.group_splits(groups,5,s.SEED+rep):
   m=DecisionTreeClassifier(max_depth=4,min_samples_leaf=1,random_state=s.SEED)
   m.fit(x[a],y[a]);pred[b]=s.score(m,x[b])
  vals.append(s.summary(y,pred))
 rng=np.random.default_rng(s.SEED+999);null=[]
 for _ in range(100):
  yy=y.copy()
  for i in range(0,len(y),2):
   if rng.random()<.5: yy[i:i+2]=yy[i:i+2][::-1]
  m=DecisionTreeClassifier(max_depth=4,min_samples_leaf=1,random_state=s.SEED)
  m.fit(x,yy);null.append(s.summary(yy,s.score(m,x))['balanced_accuracy'])
 out[name]={'fixed_depth4_cv':s.mean_metrics(vals),'repetitions':vals,
            'random_label_depth4_apparent_accuracy_mean':float(np.mean(null)),
            'random_label_depth4_apparent_accuracy_min':float(min(null)),
            'random_label_depth4_apparent_accuracy_max':float(max(null)),
            'null_draws':100}
(root/'results/fitting_audit.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
