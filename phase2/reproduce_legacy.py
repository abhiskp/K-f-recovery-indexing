"""Independently rerun deterministic Phase 1 ranking grid without SciPy.

Reads the supplied CSV and archived outputs; never rewrites source files.
The stochastic permutation draws in Phase 1 are outside this deterministic
comparison. Run: python3 phase2/reproduce_legacy.py
"""
import csv
import itertools
import json
from pathlib import Path
from statistics import mean

import analysis as a

def main():
    obs={(r['district'],r['crop'],r['agricultural_year']):float(r['production_tonnes'])
         for r in csv.DictReader(a.PANEL.open())}
    pub=[a.PUBLISHED[d] for d in a.DISTRICTS]
    B={(d,c,y):max(0,1-obs[d,c,y]/obs[d,c,'2017-18'])
       for d in a.DISTRICTS for c in a.CROPS for y in a.POSTYEARS}
    old={(r['normalization'],int(r['years']),r['crops'],float(r['alpha'])):r
         for r in csv.DictReader((a.OLD/'sensitivity_grid.csv').open())}
    differences=[]
    for norm,horizon,num in itertools.product(('minmax','rank'),(2,3),(1,2,3)):
        scale=a.minmax if norm=='minmax' else a.rankscale
        for combo in itertools.combinations(a.CROPS,num):
            vals=[mean(B[d,c,y] for c in combo for y in a.POSTYEARS[:horizon])
                  for d in a.DISTRICTS]
            for alpha in (.1,.25,.5):
                score=[(1-alpha)*u+alpha*v for u,v in zip(scale(pub),scale(vals))]
                key=(norm,horizon,'-'.join(combo),alpha)
                expected=old[key]
                computed={'spearman_risk_vs_blend':a.spearman(pub,score),
                    'top5_overlap':len(set(a.top5(score))&set(a.top5(pub))),
                    'mean_abs_rank_shift':mean(abs(x-y) for x,y in zip(a.ranks(pub),a.ranks(score))),
                    'top5':';'.join(a.top5(score))}
                for field,val in computed.items():
                    archived=expected[field]
                    mismatch=(abs(val-float(archived))>1e-9 if field in ('spearman_risk_vs_blend','mean_abs_rank_shift')
                              else str(val)!=archived)
                    if mismatch: differences.append({'spec':key,'field':field,
                        'recomputed':val,'archived':archived})
    target=[mean(B[d,c,'2020-21'] for c in a.CROPS) for d in a.DISTRICTS]
    early=[mean(B[d,c,y] for c in a.CROPS for y in a.POSTYEARS[:2]) for d in a.DISTRICTS]
    R=a.minmax(pub);X=a.minmax(early)
    archived=json.loads((a.OLD/'robustness_results.json').read_text())['year2020_pseudo_holdout']
    holdout=[]
    for alpha in (.1,.25,.5):
        score=[(1-alpha)*r+alpha*x for r,x in zip(R,X)]
        selected=a.top5(score)
        capture=sum(target[a.DISTRICTS.index(d)] for d in selected)/sum(target)
        prev=archived[str(alpha)]['observed_top5_capture']
        holdout.append({'alpha':alpha,'recomputed_capture':capture,'archived_capture':prev,
            'abs_difference':abs(capture-prev),'selected':selected})
    result={'grid_specifications':len(old),'grid_discrepancies':differences,
            'pseudo_holdout_deterministic':holdout,
            'stochastic_permutations':'not independently rerun; would require reproducing NumPy RNG and is not a valid prospective test'}
    (a.OUT/'results'/'legacy_reproduction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'grid_specifications':len(old),'discrepancy_count':len(differences),
        'holdout_max_abs_difference':max(x['abs_difference'] for x in holdout)},indent=2))

if __name__=='__main__': main()
