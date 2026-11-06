"""Robustness and illustrative pseudo-future checks; NOT validated recovery prediction."""
import runpy,contextlib,io,json,csv,itertools
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr,rankdata
OUT=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):
 m=runpy.run_path(str(OUT/'experiment.py'))
D=m['DISTRICTS'];pub=m['pub'];B=m['B'];V=m['PUBLISHED'];

def scale(x,rule):
 x=np.asarray(x,float)
 if rule=='minmax':return (x-x.min())/(x.max()-x.min()) if x.max()>x.min() else np.zeros_like(x)
 if rule=='rank':return (rankdata(x,method='average')-1)/(len(x)-1)
 raise ValueError(rule)

def order(score):
 # Deterministic secondary sort on the original published rank in exact ties.
 return np.lexsort((-pub,-score))

def cap(score, outcome,k=5):
 return sum(np.asarray(outcome)[order(score)[:k]])/sum(outcome) if sum(outcome)>0 else None
risk_rank=rankdata(-pub)
seq=[]
for norm in ['minmax','rank']:
 r=scale(pub,norm)
 for horizon in [2,3]:
  for num in range(1,4):
   for combo in itertools.combinations(range(3),num):
    bur=B[:,combo,:horizon].mean(axis=(1,2));br=scale(bur,norm)
    for alpha in [.1,.25,.5]:
     score=(1-alpha)*r+alpha*br
     ix=order(score)[:5]; same=len(set(ix)&set(order(pub)[:5]))
     seq.append(dict(normalization=norm,years=horizon,crops='-'.join(m['cropnames'][j] for j in combo),alpha=alpha,
         spearman_risk_vs_blend=float(spearmanr(pub,score).statistic),top5_overlap=same,
         mean_abs_rank_shift=float(np.abs(rankdata(-score)-risk_rank).mean()),
         top5=';'.join(D[j] for j in ix)))
with open(OUT/'sensitivity_grid.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(seq[0]));w.writeheader();w.writerows(seq)

T=B[:,:,2].mean(axis=1)
E=B[:,:,:2].mean(axis=(1,2))
R=scale(pub,'minmax');X=scale(E,'minmax')
obs={}
for a in [.1,.25,.5]:
 s=(1-a)*R+a*X
 rng=np.random.default_rng(1937+int(a*100))
 null=np.array([cap((1-a)*R+a*scale(rng.permutation(E),'minmax'),T) for _ in range(10000)])
 observed=cap(s,T)
 obs[str(a)]={'observed_top5_capture':observed,'risk_only_top5_capture':cap(R,T),
              'null_mean_top5_capture':float(null.mean()),'null_p_greater_equal':float(np.mean(null>=observed)),
              'null_95pct_range':[float(v) for v in np.quantile(null,[.025,.975])],
              'observed_top5':[D[i] for i in order(s)[:5]]}
summary={
  'definition':'Illustrative, NOT validated, equal-weight crop production shortfalls relative to one pre-flood year',
  'grid_n':len(seq),
  'alpha_25_minmax_3_crops_3_years':next(d for d in seq if d['normalization']=='minmax' and d['years']==3 and d['crops']=='rice-banana-plantain' and d['alpha']==.25),
  'alpha_25_rank_3_crops_3_years':next(d for d in seq if d['normalization']=='rank' and d['years']==3 and d['crops']=='rice-banana-plantain' and d['alpha']==.25),
  'alpha_25_count_top5_overlap':{str(n):sum(1 for d in seq if d['alpha']==.25 and d['top5_overlap']==n) for n in range(0,6)},
  'year2020_pseudo_holdout':obs,
  'interpretation':'Permutation tests are descriptive negative controls and do not address confounding, geographic dependence, or published-baseline time leakage.'
}
(OUT/'robustness_results.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
