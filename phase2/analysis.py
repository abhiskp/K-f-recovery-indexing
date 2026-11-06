"""Independent, standard-library audit of Kerala annual crop output.

This script never modifies the supplied Phase 1 package. All estimates are
descriptive output deviations, not 2018 flood-attributable recovery.
Run: python3 phase2/analysis.py
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
OLD = ROOT / "Kerala_Flood_Recovery_Codex_Package_Fixed(1)" / "kerala_recovery_investigation"
PANEL = OLD / "district_crop_panel.csv"
COM = "https://www.ecostat.kerala.gov.in/storage/publications/626.pdf"
DISTRICTS = ["Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha", "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad", "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"]
CROPS = ["rice", "banana", "plantain"]
PREYEARS = ["2014-15", "2015-16", "2016-17", "2017-18"]
POSTYEARS = ["2018-19", "2019-20", "2020-21"]

# Values independently read from official historical compendium Table 41
# (rice, PDF p. 95), Table 44 (banana, PDF p. 101), Table 45 (plantain,
# PDF p. 102). Annual reports retain more decimal precision from 2017-18 on.
HIST = {
 "rice": {
  "2014-15": [5561,3150,7573,103095,49393,1803,9974,76016,236398,22279,3423,26168,11164,6095],
  "2015-16": [5453,3351,8396,89335,49506,2198,12652,78886,228459,23649,3608,23704,11518,8560],
  "2016-17": [3069,2396,8837,102439,48030,1631,10695,57478,144275,17211,2935,20647,10623,6217]},
 "banana": {
  "2014-15": [15999,17032,17091,3733,23152,31893,44953,18980,175132,58163,14536,100284,19593,4890],
  "2015-16": [18338,20399,16375,4135,23625,30115,46730,19803,152109,64990,17723,92295,22503,7015],
  "2016-17": [19826,19511,16528,3743,21749,29359,47781,19069,139231,58564,17264,71357,18342,6998]},
 "plantain": {
  "2014-15": [67266,45467,19871,16086,23823,39546,37303,45477,95729,28463,14886,10501,12627,11275],
  "2015-16": [64661,40324,21582,14927,20987,39164,35881,33229,58353,27379,18626,10764,14325,11424],
  "2016-17": [60035,42801,21036,14126,21968,38110,35158,28579,55411,28463,17885,7608,13669,10957]}}
HIST_STATE_TOTALS={
 'rice':{'2014-15':562092,'2015-16':549275,'2016-17':436483},
 'banana':{'2014-15':545431,'2015-16':536155,'2016-17':489322},
 'plantain':{'2014-15':468320,'2015-16':411626,'2016-17':395806}}

# Published 2026 vulnerability scores are used only for ex-post rank sensitivity.
PUBLISHED = {"Malappuram":.831,"Palakkad":.719,"Wayanad":.581,"Thrissur":.562,"Kozhikode":.558,"Idukki":.528,"Kollam":.524,"Ernakulam":.514,"Alappuzha":.504,"Thiruvananthapuram":.495,"Kottayam":.473,"Kannur":.467,"Pathanamthitta":.414,"Kasaragod":.317}

def write_csv(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

def ranks(values):
    # Average ranks for ties, 1 highest. This matches scipy rankdata(-x).
    order = sorted(range(len(values)), key=lambda i: -values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1): out[order[k]] = (i + j + 2) / 2
        i = j + 1
    return out

def ascending_ranks(values):
    return [len(values) + 1 - x for x in ranks(values)]

def corr(x, y):
    xm, ym = mean(x), mean(y)
    a = [v - xm for v in x]; b = [v - ym for v in y]
    den = (sum(v*v for v in a) * sum(v*v for v in b)) ** .5
    return sum(u*v for u,v in zip(a,b)) / den if den else None

def spearman(x, y): return corr(ascending_ranks(x), ascending_ranks(y))

def kendall(x, y):
    c = d = tx = ty = 0
    for i in range(len(x)):
        for j in range(i+1, len(x)):
            a = (x[i] > x[j]) - (x[i] < x[j]); b = (y[i] > y[j]) - (y[i] < y[j])
            if a == 0 and b == 0: continue
            if a == 0: tx += 1
            elif b == 0: ty += 1
            elif a == b: c += 1
            else: d += 1
    return (c-d)/((c+d+tx)*(c+d+ty))**.5

def minmax(values):
    lo, hi = min(values), max(values)
    return [(v-lo)/(hi-lo) for v in values] if hi > lo else [0.0]*len(values)

def rankscale(values):
    a = ascending_ranks(values)
    return [(v-1)/(len(values)-1) for v in a]

def top5(values):
    # Deterministic tie break favors the higher published score at the cutoff.
    return [DISTRICTS[i] for i in sorted(range(14), key=lambda i:(-values[i],-PUBLISHED[DISTRICTS[i]],i))[:5]]

def main():
    assert all(len(a) == 14 for ys in HIST.values() for a in ys.values())
    assert all(sum(HIST[c][y])==v for c,ys in HIST_STATE_TOTALS.items() for y,v in ys.items())
    raw = list(csv.DictReader(PANEL.open()))
    assert len(raw) == 168 and len({(r['district'],r['crop'],r['agricultural_year']) for r in raw}) == 168
    obs = {(r['district'],r['crop'],r['agricultural_year']):float(r['production_tonnes']) for r in raw}
    assert set(r['district'] for r in raw)==set(DISTRICTS)
    assert set(r['crop'] for r in raw)==set(CROPS)
    pre=[]
    for crop, years in HIST.items():
        page = {'rice':95,'banana':101,'plantain':102}[crop]
        for year, values in years.items():
            for district, value in zip(DISTRICTS, values):
                pre.append(dict(district=district,agricultural_year=year,crop=crop,production_tonnes=value,source_pdf_url=COM,source_pdf_page=page,source_table={'rice':41,'banana':44,'plantain':45}[crop],precision_note='rounded whole tonnes in historical compendium'))
                obs[district,crop,year] = float(value)
    write_csv(OUT/'data'/'pre2018_crop_production.csv', pre)
    assert len(pre)==126
    combined=[]
    for r in pre:
        combined.append(dict(district=r['district'],agricultural_year=r['agricultural_year'],
            crop=r['crop'],production_tonnes=r['production_tonnes'],
            source_pdf_url=r['source_pdf_url'],source_pdf_page=r['source_pdf_page'],
            source_table=r['source_table'],precision_note=r['precision_note'],
            provenance='official historical compendium; Phase 2 transcription'))
    for r in raw:
        combined.append(dict(district=r['district'],agricultural_year=r['agricultural_year'],
            crop=r['crop'],production_tonnes=r['production_tonnes'],
            source_pdf_url=r['source_pdf_url'],source_pdf_page=r['source_pdf_page'],
            source_table='4',precision_note='as in inherited annual-report transcription; full cell audit pending',
            provenance='inherited Phase 1 district_crop_panel.csv'))
    assert len(combined)==294
    write_csv(OUT/'data'/'crop_panel_2014_2021.csv',combined)

    # State totals independently reconstructed from CSV, then compared to old JSON.
    totals={year:{crop:sum(obs[d,crop,year] for d in DISTRICTS) for crop in CROPS} for year in PREYEARS+POSTYEARS}
    legacy=json.loads((OLD/'experiment_results.json').read_text())
    reproduce={}
    for year in ['2017-18']+POSTYEARS:
        reproduce[year]={crop:{'recomputed':totals[year][crop],'archived':legacy['states'][year][crop], 'abs_difference':abs(totals[year][crop]-legacy['states'][year][crop])} for crop in CROPS}
    assert max(v['abs_difference'] for ys in reproduce.values() for v in ys.values()) < .0011
    base=[PUBLISHED[d] for d in DISTRICTS]
    oldburden=[mean(max(0,1-obs[d,c,y]/obs[d,c,'2017-18']) for c in CROPS for y in POSTYEARS) for d in DISTRICTS]
    oldscore=[.75*a+.25*b for a,b in zip(rankscale(base),rankscale(oldburden))]
    oldtop=top5(oldscore)
    archived=next(x for x in legacy['sensitivity_rank'] if x['alpha']==.25)
    assert set(oldtop)==set(archived['new_top5'])
    # The cutoff is mathematically tied for Idukki/Kozhikode, so membership
    # depends on the stated secondary sort, although rho is reproducible.
    assert abs(spearman(base,oldscore)-archived['spearman_vs_published'])<1e-12
    old_rank_rows={r['district']:r for r in csv.DictReader((OLD/'district_descriptive_ranks.csv').open())}
    reconstructed=[]
    reversed_capacity=[]
    for d in DISTRICTS:
        row=old_rank_rows[d]
        h,e,s,a=[float(row[k]) for k in ('hazard','exposure','sensitivity','adaptive_capacity_as_labelled')]
        reconstructed.append(.30*h+.25*e+.25*s+.20*a)
        reversed_capacity.append(.30*h+.25*e+.25*s+.20*(1-a))
    formula_audit={'max_abs_difference':max(abs(a-b) for a,b in zip(base,reconstructed)),
        'reverse_capacity_spearman':spearman(base,reversed_capacity),
        'reverse_capacity_top5_overlap':len(set(top5(base))&set(top5(reversed_capacity)))}
    assert abs(formula_audit['max_abs_difference']-.0005)<1e-12

    rows=[]
    for d in DISTRICTS:
        for c in CROPS:
            years=[obs[d,c,y] for y in PREYEARS]
            baseline=mean(years); med=median(years)
            for y in POSTYEARS:
                value=obs[d,c,y]
                rows.append(dict(district=d,crop=c,agricultural_year=y,production_tonnes=value,
                    pre_mean_tonnes=baseline,pre_median_tonnes=med,
                    ratio_to_pre_mean=value/baseline,deficit_vs_pre_mean=max(0,1-value/baseline),
                    deficit_vs_pre_median=max(0,1-value/med),
                    original_deficit_vs_2017_18=max(0,1-value/obs[d,c,'2017-18']),
                    data_coverage='4 annual pre; 1 annual observation for this follow-up year',
                    attribution='unattributed crop output deviation; no 2018 inundation linked'))
    write_csv(OUT/'results'/'annual_output_deviations.csv',rows)
    assert len(rows)==126
    # Official statewide comparison table in Agricultural Statistics 2018-19,
    # printed p. 126. P = area * yield; this decomposition shows why a raw
    # production change is not a direct measure of crop productivity.
    areas={'rice':(189086,198026),'banana':(62108,52869),'plantain':(54455,56211)}
    area_yield=[]
    for c,(a0,a1) in areas.items():
        p0,p1=totals['2017-18'][c],totals['2018-19'][c]
        area_yield.append(dict(crop=c,area_2017_18_ha=a0,area_2018_19_ha=a1,
            production_2017_18_tonnes=p0,production_2018_19_tonnes=p1,
            area_pct_change=100*(a1/a0-1),yield_2017_18_t_per_ha=p0/a0,
            yield_2018_19_t_per_ha=p1/a1,yield_pct_change=100*((p1/a1)/(p0/a0)-1),
            production_pct_change=100*(p1/p0-1),
            source_pdf_url='https://ecostat.kerala.gov.in/storage/publications/239.pdf',
            source_printed_page=126))
    write_csv(OUT/'results'/'state_area_yield_decomposition.csv',area_yield)
    scores={d:mean(float(r['deficit_vs_pre_mean']) for r in rows if r['district']==d) for d in DISTRICTS}
    meds={d:mean(float(r['deficit_vs_pre_median']) for r in rows if r['district']==d) for d in DISTRICTS}
    old={d:oldburden[i] for i,d in enumerate(DISTRICTS)}
    comp=[]
    for norm in ('minmax','rank'):
        scale=minmax if norm=='minmax' else rankscale
        for kind, values in [('2017_only',old),('four_year_mean',scores),('four_year_median',meds)]:
            v=[values[d] for d in DISTRICTS]
            score=[.75*a+.25*b for a,b in zip(scale(base),scale(v))]
            rs=ranks(score); rb=ranks(base)
            comp.append(dict(normalization=norm,output_baseline=kind,alpha=.25,
                spearman_vs_published=round(spearman(base,score),6),kendall_vs_published=round(kendall(base,score),6),
                top5_overlap=len(set(top5(score))&set(top5(base))),
                mean_abs_rank_shift=round(mean(abs(a-b) for a,b in zip(rs,rb)),3),
                top5=';'.join(top5(score))))
    write_csv(OUT/'results'/'rank_sensitivity.csv',comp)

    # Leave-one-pre-year-out is baseline-choice sensitivity, not a confidence interval.
    loo=[]
    for omit in PREYEARS:
        v=[]
        for d in DISTRICTS:
            deficits=[]
            for c in CROPS:
                b=mean(obs[d,c,y] for y in PREYEARS if y!=omit)
                deficits += [max(0,1-obs[d,c,y]/b) for y in POSTYEARS]
            v.append(mean(deficits))
        score=[.75*a+.25*b for a,b in zip(minmax(base),minmax(v))]
        loo.append(dict(omitted_pre_year=omit,top5=';'.join(top5(score)),top5_overlap=len(set(top5(score))&set(top5(base))),spearman_vs_published=round(spearman(base,score),6)))
    write_csv(OUT/'results'/'leave_one_pre_year_out.csv',loo)

    summary={'input_rows':len(raw),'new_pre_flood_rows':len(pre),'pre_years':PREYEARS,'post_years':POSTYEARS,
      'totals_tonnes':totals,'area_yield_2018_19':area_yield,'legacy_reproduction':reproduce,
      'published_formula_audit':formula_audit,
      'legacy_alpha25_rank_top5_reproduced':oldtop,
      'baseline_comparison':comp,'leave_one_pre_year_out':loo,
      'interpretation':'Annual crop output deviations, not observed flood recovery, attribution, time to recovery, or predictive validation.'}
    (OUT/'results'/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')

    # Small vector figure with explicit source and limitation in the caption.
    colors={'rice':'#2366a8','banana':'#bd5f18','plantain':'#368064'}
    xs=[105+i*112 for i in range(7)]
    lines=['<svg xmlns="http://www.w3.org/2000/svg" width="950" height="540" viewBox="0 0 950 540">',
      '<rect width="950" height="540" fill="white"/>',
      '<text x="70" y="37" font-family="Arial" font-size="20" font-weight="bold">Kerala crop output around the 2018 flood</text>',
      '<text x="70" y="60" font-family="Arial" font-size="13">State totals relative to the 2014–15 to 2017–18 mean for each crop</text>',
      '<rect x="497" y="85" width="366" height="337" fill="#f3f5f7"/>']
    years=PREYEARS+POSTYEARS; bycrop={c:[totals[y][c]/mean(totals[z][c] for z in PREYEARS)*100 for y in years] for c in CROPS}
    for val in [50,75,100,125,150]:
        py=420-(val-50)*3.1
        lines += [f'<line x1="80" y1="{py:.1f}" x2="875" y2="{py:.1f}" stroke="#d6dde3"/>',f'<text x="68" y="{py+4:.1f}" text-anchor="end" font-family="Arial" font-size="11">{val}</text>']
    lines += ['<line x1="80" y1="85" x2="80" y2="420" stroke="#596575"/>','<line x1="80" y1="420" x2="875" y2="420" stroke="#596575"/>','<text x="20" y="270" transform="rotate(-90 20 270)" font-family="Arial" font-size="12">Production (% of pre-flood mean)</text>']
    for c,vals in bycrop.items():
        pts=' '.join(f'{x},{420-(v-50)*3.1:.1f}' for x,v in zip(xs,vals))
        lines.append(f'<polyline points="{pts}" fill="none" stroke="{colors[c]}" stroke-width="2.5"/>')
        for x,v in zip(xs,vals): lines.append(f'<circle cx="{x}" cy="{420-(v-50)*3.1:.1f}" r="4" fill="{colors[c]}"/>')
    for x,y in zip(xs,years): lines.append(f'<text x="{x}" y="442" text-anchor="middle" font-family="Arial" font-size="11">{y}</text>')
    for i,c in enumerate(CROPS):
        x=625+i*92;lines += [f'<line x1="{x}" y1="78" x2="{x+20}" y2="78" stroke="{colors[c]}" stroke-width="3"/>',f'<text x="{x+25}" y="82" font-family="Arial" font-size="12">{c.title()}</text>']
    lines += ['<text x="80" y="481" font-family="Arial" font-size="12">Shading marks annual periods after the August 2018 event.</text>',
      '<text x="80" y="501" font-family="Arial" font-size="12">Annual production is affected by other shocks and is not an estimate of flood-caused loss or recovery.</text>',
      '<text x="80" y="522" font-family="Arial" font-size="11">Sources: Kerala DES annual reports and Agriculture Statistics 2005–20, Tables 41, 44, 45.</text>','</svg>']
    (OUT/'figures'/'crop_output_relative_to_four_year_baseline.svg').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'rows':len(rows),'rank_comparison':comp,'loo':loo},indent=2))

if __name__=='__main__': main()
