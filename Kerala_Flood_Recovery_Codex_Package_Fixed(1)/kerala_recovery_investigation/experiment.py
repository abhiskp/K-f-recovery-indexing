"""Reproducible *descriptive* Kerala agricultural-trend/rank sensitivity audit.

Human-transcribed values from Kerala Department of Economics and Statistics
Agricultural Statistics annual reports 2017-18 to 2020-21, Table 4.
Published vulnerability score and components: Kendagannaswamy et al. (2026),
J Indian Soc Remote Sens Table 9, uploaded Meenachil.pdf p18.

IMPORTANT: changes in annual crop production are NOT causally attributed to
flooding; these are annual district aggregates and include other shocks.
2016/17 or multi-year pre-flood counterfactual has not yet been built.
"""
from pathlib import Path
import csv, json
import numpy as np
from scipy.stats import spearmanr, kendalltau
import matplotlib.pyplot as plt

OUT=Path(__file__).parent
DISTRICTS=['Thiruvananthapuram','Kollam','Pathanamthitta','Alappuzha','Kottayam','Idukki','Ernakulam','Thrissur','Palakkad','Malappuram','Kozhikode','Wayanad','Kannur','Kasaragod']
# Each row reports rice, banana and plantain as production in tonnes.
# 2020-21 rice uses *wetland* crop Table 4 (626888 t statewide, to avoid
# a discontinuity from newly itemized dryland rice 6850 t that year).
PROD={
'2017-18':{
'rice':[4551,4302,8843,105676,49509,2293,12888,69114,198626,23571,3960,21792,11318,4867],
'banana':[21240,23599,16528,4386,25818,33165,49510,19431,186572,60912,14032,83517,20336,6783],
'plantain':[59730,46028,21848,14166,21650,31914,40981,31476,37320,25882,16546,8358,12636,11148]},
'2018-19':{
'rice':[5167,4514,11676,128560,61917,1562,11191,69454,215285,26984,3439,22340,11143,5024],
'banana':[27818.147,25970.833,17322.444,1937.911,29188.160,29604.958,35128.826,8203.624,102811.983,40493.548,12981.503,74562.156,17313.030,5722.549],
'plantain':[65560.783,44018.474,19088.922,13212.688,22279.665,28524.192,37871.769,34401.612,50333.424,24832.602,15290.520,6537.955,11512.412,9637.031]},
'2019-20':{
'rice':[4540,4183,11383,112592,50051,1467,10860,76556,248199,28214,2867,19513,11804,4849],
'banana':[32031.076,23678.09,18086.22,2343.855,32500.15,33622.165,47861.372,17786.239,114043.826,48924.412,13652.335,133596.792,23238.938,7059.831],
'plantain':[73583,42546,22143,15088,21509,31538,37364,34563,58176,25748,15797,8006,11836,9005]},
'2020-21':{
'rice':[5659.665,5218.356,11143.253,125803.121,54268,1899.223,10971,87655.448,246992.67,30504,2663,23088.373,14408.429,6611.549],
'banana':[26620.569,21239.462,17524.272,2308.272,31087.726,33194.542,50643.309,22972.585,153892.892,39129.062,26701.702,91892.45,20329.519,6652.355],
'plantain':[68604.61,45211.318,23244.711,11214.794,22641.538,26428.217,46494.514,41070.727,53423.568,24508.188,23275.092,7610.798,11026.252,8110.072]}
}
PUBLISHED={
'Malappuram':(.831,.999,.906,.779,.548), 'Palakkad':(.719,.946,.469,.596,.846),
'Wayanad':(.581,.700,.060,.699,.907), 'Thrissur':(.562,.998,.652,.218,.223),
'Kozhikode':(.558,.873,.701,.287,.247), 'Idukki':(.528,.604,.030,.644,.890),
'Kollam':(.524,.833,.541,.329,.285), 'Ernakulam':(.514,1.,.702,.125,.037),
'Alappuzha':(.504,.907,.556,.287,.104), 'Thiruvananthapuram':(.495,.551,.888,.263,.209),
'Kottayam':(.473,.952,.383,.269,.122), 'Kannur':(.467,.682,.457,.310,.352),
'Pathanamthitta':(.414,.819,.144,.312,.272), 'Kasaragod':(.317,.000,.199,.467,.750)}
URL={
'2017-18':'https://ecostat.kerala.gov.in/storage/publications/247.pdf',
'2018-19':'https://ecostat.kerala.gov.in/storage/publications/239.pdf',
'2019-20':'https://www.ecostat.kerala.gov.in/storage/publications/3.pdf',
'2020-21':'https://ecostat.kerala.gov.in/storage/publications/622.pdf',
}
SOURCE_PAGES={ '2017-18':(149,150),'2018-19':(146,147),'2019-20':(154,156),'2020-21':(156,158)} # PDF page indices 1-based as rendered by web source
for year, values in PROD.items():
 for crop,a in values.items():
  assert len(a)==14,(year,crop)
 assert len(values)==3
assert len(PUBLISHED)==14

with open(OUT/'district_crop_panel.csv','w',newline='') as f:
 w=csv.writer(f); w.writerow(['district','agricultural_year','crop','production_tonnes','source_pdf_url','source_pdf_page','geography','measurement_note'])
 for year, cs in PROD.items():
  for crop, a in cs.items():
   page=SOURCE_PAGES[year][0] if crop=='rice' else SOURCE_PAGES[year][1]
   for name,v in zip(DISTRICTS,a):
    w.writerow([name,year,crop,v,URL[year],page,'Kerala district','Annual production; NOT flood-attributable recovery; 2020-21 rice is wetland rice' if crop=='rice' else 'Annual production; NOT flood-attributable recovery'])

pub=np.array([PUBLISHED[d][0] for d in DISTRICTS])
base='2017-18'; ys=['2018-19','2019-20','2020-21']; cropnames=['rice','banana','plantain']
B=np.zeros((14,3,3));relative=np.zeros_like(B)
for k,c in enumerate(cropnames):
 b=np.array(PROD[base][c],float)
 for t,y in enumerate(ys):
  s=np.array(PROD[y][c],float)/b
  relative[:,k,t]=s
  B[:,k,t]=np.clip(1-s,0,1)

# Equal weight within agriculture ONLY, not a multidomain resilience score.
burden_all=B.mean(axis=(1,2))
burden_early=B[:,:,:2].mean(axis=(1,2))
with np.errstate(invalid='ignore'):
 target=B[:,:,2].mean(axis=1)

def ordinal_score(x):
 from scipy.stats import rankdata
 return (rankdata(x,method='average')-1)/(len(x)-1)

def ranking(x):
 from scipy.stats import rankdata
 return rankdata(-x,method='min').astype(int)

riskpercent=ordinal_score(pub)
rev=ordinal_score(burden_all)
early=ordinal_score(burden_early)
base_rank=ranking(pub)

def combine(a, bx=rev):return (1-a)*riskpercent+a*bx

def utility(score,k=5):
 idx=np.argsort(-score)[:k]
 return sum(target[idx])/sum(target) if sum(target)>0 else np.nan

# Sensitivity rank tests for information not yet causally attributable to flooding.
weight_summaries=[]
for alpha in [0,0.10,0.25,0.50]:
 score=combine(alpha)
 weight_summaries.append(dict(alpha=alpha,spearman_vs_published=float(spearmanr(pub,score).statistic),
  kendall_vs_published=float(kendalltau(pub,score).statistic),mean_abs_rank_shift=float(abs(ranking(score)-base_rank).mean()),
  max_abs_rank_shift=int(abs(ranking(score)-base_rank).max()),
  top5_overlap=int(len(set(np.argsort(-score)[:5])&set(np.argsort(-pub)[:5]))),
  new_top5=[DISTRICTS[i] for i in np.argsort(-score)[:5]]))

# Exploratory future-crop shortfall; rank mixed from 2018-19 and 2019-20 only.
# WARNING: 2026 published baseline potentially leaks 2018/2019/2021 labels.
holdout=[]
for alpha in [0,0.10,0.25,0.50]:
 s=combine(alpha,early)
 holdout.append(dict(alpha=alpha,top5_capture_2020_crop_shortfall=float(utility(s)),
     spearman_2020_crop_shortfall=float(spearmanr(s,target).statistic)))

# Permutation null: random vulnerability-uncorrelated factor changes rankings too.
# Tests the incorrect inference 'a ranking changed; therefore indicator is valuable.'
rng=np.random.default_rng(101)
a=.25
obs=float(abs(ranking(combine(a))-base_rank).mean())
perm=np.array([float(abs(ranking(combine(a,rng.permutation(rev)))-base_rank).mean()) for _ in range(4000)])
null=dict(observed_mean_rank_displacement=obs,permutation_mean=float(perm.mean()),
         permutation_q05=float(np.quantile(perm,.05)),permutation_q95=float(np.quantile(perm,.95)),
         fraction_permutations_with_equal_or_greater_displacement=float(np.mean(perm>=obs)))

rows=[]
for i,d in enumerate(DISTRICTS):
 item={'district':d,'published_vulnerability_2026':pub[i], 'published_rank':int(base_rank[i]),'hazard':PUBLISHED[d][1],
       'exposure':PUBLISHED[d][2],'sensitivity':PUBLISHED[d][3],'adaptive_capacity_as_labelled':PUBLISHED[d][4],
       'relative_output_rice_2018_19':relative[i,0,0], 'relative_output_rice_2019_20':relative[i,0,1],
       'relative_output_rice_2020_21':relative[i,0,2],
       'relative_output_banana_2018_19':relative[i,1,0], 'relative_output_banana_2019_20':relative[i,1,1],
       'relative_output_banana_2020_21':relative[i,1,2],
       'relative_output_plantain_2018_19':relative[i,2,0], 'relative_output_plantain_2019_20':relative[i,2,1],
       'relative_output_plantain_2020_21':relative[i,2,2],
       'observed_agricultural_output_shortfall_2018_2020':burden_all[i],
       'observed_agricultural_output_shortfall_2018_2019':burden_early[i],
       'agricultural_output_shortfall_2020_21':target[i]}
 for alpha in [.10,.25,.50]:
  key=str(alpha).replace('.','p');item[f'illustrative_rank_alpha_{key}']=int(ranking(combine(alpha))[i]);item[f'rank_change_alpha_{key}']=int(base_rank[i]-ranking(combine(alpha))[i])
 rows.append(item)
with open(OUT/'district_descriptive_ranks.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)

# Published table internal consistency audit, does 0.3H+0.25E+0.25S+0.2A reproduce published?
pred=np.array([.3*PUBLISHED[d][1]+.25*PUBLISHED[d][2]+.25*PUBLISHED[d][3]+.2*PUBLISHED[d][4] for d in DISTRICTS])
minus=np.array([.3*PUBLISHED[d][1]+.25*PUBLISHED[d][2]+.25*PUBLISHED[d][3]+.2*(1-PUBLISHED[d][4]) for d in DISTRICTS])
audit={'max_abs_difference_positive_capacity_formula':float(np.max(np.abs(pred-pub))),
       'pearson_positive_capacity_formula':float(np.corrcoef(pred,pub)[0,1]),
       'published_vs_reverse_capacity_spearman':float(spearmanr(pub,minus).statistic),
       'published_vs_reverse_capacity_top5_overlap':int(len(set(np.argsort(-pub)[:5])&set(np.argsort(-minus)[:5])))}

states={year:{c:round(sum(PROD[year][c]),3) for c in cropnames} for year in PROD}
# Note: published reports include possible rounding; district sum should be within small tolerance.
expected={'2017-18':{'rice':521310,'banana':565829,'plantain':379683},'2018-19':{'rice':578256,'banana':429059.672,'plantain':383102.049},'2019-20':{'rice':587078,'banana':548425.301,'plantain':406902},'2020-21':{'rice':626888,'banana':544188.717,'plantain':412864.399}}
checks={y:{c:round(states[y][c]-expected[y][c],3) for c in cropnames} for y in PROD}
results={'states':states,'state_reported_difference':checks,'crop_index_spearman_with_published':float(spearmanr(pub,burden_all).statistic),
         'crop_index_vs_baseline_rank_spearman':float(spearmanr(riskpercent,rev).statistic),
         'sensitivity_rank':weight_summaries,'holdout_diagnostic':holdout,'permutation_negative_control':null,
         'vulnerability_formula_audit':audit,'n_districts':14,
         'critical_limitations':['Annual agricultural district output is not flood-attributable recovery',
          'One pre-flood year is insufficient counterfactual','Multiple flood events and COVID affect post-years',
          'Existing vulnerability baseline was published in 2026 and cannot serve as a pre-2018 forecast',
          'Crop output affected by area and yield; reflects economic production not underlying welfare',
          'No observed time-to-recovery, only annually aggregated shortfall','No economic, infrastructure, environmental, housing or health recovery series analysed',
          'Weights are illustrative and not a new validated index']}
(OUT/'experiment_results.json').write_text(json.dumps(results,indent=2))

plt.rcParams['font.size']=10
fig,ax=plt.subplots(figsize=(9,4.7))
x=np.arange(4)
for crop in cropnames:
 vals=np.array([states[y][crop] for y in PROD],float)
 ax.plot(x,vals/vals[0]*100,marker='o',linewidth=2,label=crop.capitalize())
ax.set_xticks(x,list(PROD));ax.set_ylabel('Production relative to 2017–18 (%)');ax.set_xlabel('Kerala agricultural year')
ax.axhline(100,linestyle='--',linewidth=1);ax.legend(loc='best')
ax.set_title('Observed Kerala crop production changes — not flood-attributable recovery')
fig.tight_layout(); fig.savefig(OUT/'figure_01_state_crop_trajectories.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(9,6))
order=np.argsort(-pub)
y=np.arange(14)
ranks=ranking(combine(.25))
ax.scatter(base_rank[order],y,marker='o',label='Published vulnerability rank')
ax.scatter(ranks[order],y,marker='s',label='Illustrative 25% agricultural output-shortfall mix')
for j,i in enumerate(order):ax.plot([base_rank[i],ranks[i]],[j,j],alpha=.4,linewidth=1)
ax.set_yticks(y,[DISTRICTS[i] for i in order]);ax.invert_yaxis();ax.set_xticks(range(1,15));ax.set_xlabel('Rank (1 = highest)');ax.set_title('Ranking sensitivity: descriptive agriculture proxy, not validated flood recovery');ax.legend(loc='lower right')
fig.tight_layout();fig.savefig(OUT/'figure_02_rank_sensitivity.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(8.5,4.5))
for alpha in [0,.1,.25,.5]:
 s=combine(alpha,early)
 ax.scatter(alpha,utility(s),marker='o')
ax.plot([0,.1,.25,.5],[utility(combine(a,early)) for a in [0,.1,.25,.5]],linewidth=1.5)
ax.set_xticks([0,.1,.25,.5]);ax.set_ylim(0,1);ax.set_ylabel('Share of 2020–21 crop shortfall within selected top 5');ax.set_xlabel('Illustrative weight on 2018–20 agricultural shortfall')
ax.set_title('Exploratory temporal check — not independent flood-recovery validation')
fig.tight_layout();fig.savefig(OUT/'figure_03_early_late_top5.png',dpi=160);plt.close(fig)
print(json.dumps(results,indent=2))
