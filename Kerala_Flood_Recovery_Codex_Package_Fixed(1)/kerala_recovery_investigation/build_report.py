from pathlib import Path
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_BREAK
import json,csv
root=Path(__file__).resolve().parent
r=json.loads((root/'experiment_results.json').read_text());s=json.loads((root/'robustness_results.json').read_text())

def style(d):
 sec=d.sections[0];sec.top_margin=Inches(.7);sec.bottom_margin=Inches(.65);sec.left_margin=Inches(.8);sec.right_margin=Inches(.8)
 styles=d.styles;styles['Normal'].font.name='Aptos';styles['Normal'].font.size=Pt(9.5)
 styles['Normal'].paragraph_format.space_after=Pt(5)
 for h,z in [('Title',21),('Heading 1',13),('Heading 2',11)]:
  st=styles[h];st.font.name='Aptos Display';st.font.size=Pt(z);st.font.bold=True;st.font.color.rgb=RGBColor(25,47,65)

def para(d,txt,style=None):return d.add_paragraph(txt,style)
def hd(d,txt):d.add_heading(txt,1)
def small(d,txt):
 p=d.add_paragraph(txt);p.style='Caption';return p

def tbl(d,headers,rows,sz=8.0):
 t=d.add_table(rows=1, cols=len(headers));t.style='Light Shading Accent 1';t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for i,h in enumerate(headers):t.rows[0].cells[i].text=str(h)
 for row in rows:
  cc=t.add_row().cells
  for i,val in enumerate(row):cc[i].text=str(val)
 for row in t.rows:
  for cell in row.cells:
   cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   for p in cell.paragraphs:
    for run in p.runs:run.font.size=Pt(sz)
 return t

d=Document();style(d)
d.add_heading('Kerala Flood Recovery and Priority Rankings',0)
p=d.add_paragraph('Exploratory empirical investigation  |  21 October 2026');p.style='Subtitle'
para(d,'RESEARCH STATUS  •  Real agricultural district panel reconstructed and analysed; recovery attributed to flooding and multi-domain recovery remain unmeasured. All altered priorities below are sensitivity scenarios, not proposed operational rankings.')
hd(d,'Executive findings')
for text in [
  'Data built: 14 Kerala districts × 3 crops (rice, banana, plantain) × 4 agricultural years (2017–18 to 2020–21): 168 crop-production entries manually transcribed from official agricultural reports. District-wise baseline flood-vulnerability scores are taken from Table 9 of Kendagannaswamy et al. (2026).',
  'Observed statewide agricultural production moved in different directions in 2018–19 relative to 2017–18: rice +10.9%, banana −24.2%, plantain +0.9%. By 2020–21, rice was +20.3%, banana −3.8% and plantain +8.7%. These are NOT causal flood impacts.',
  'The original ranking is sensitive to the treatment of a hypothetical agricultural component. At a 25% illustrative weight, minimum–maximum normalization preserves only 3 of the original top 5 districts, while percentile ranks preserve 5 (with a tie at the priority cutoff). Across 28 alternative specifications at that weight, top-5 overlap ranges from 3 to 5.',
  'An exploratory pseudo-holdout (2018–20 annual output changes used to predict 2020–21 output shortfalls) appears to improve top-five capture under some settings. This is NOT independently validated prediction: the published 2026 risk score postdates the outcomes; crop production is confounded by subsequent shocks and the weights were selected after inspection.',
  'An audit of the published vulnerability formula identifies a directionality ambiguity in its adaptive-capacity variable. The reported published scores are reconstructed by adding 20% of the variable labelled adaptive capacity, although the prose interprets high capacity as protective. Definition and coding must be checked against the original authors before drawing conclusions.'
]: para(d,'• '+text)
hd(d,'1. Scope: recovery is not just economic')
tbl(d,['Recovery domain','What counts as observed recovery','Empirical status today'],[
 ('Agricultural','Season-adjusted crop output, planted area, yield or crop cycle returning to expected counterfactual','Four annual district production years collected; NOT flood-attributed'),
 ('Economic / livelihoods','Return of income, expenditure, employment, business and local activity','Prior NIPFP Kerala 2018 study reviewed; no new microdata analysis'),
 ('Infrastructure / services','Functional restoration of roads, power, water, healthcare and schools','2018 PDNA sector loss estimates located; no local recovery time series'),
 ('Environmental / ecological','Restoration of vegetation, land cover, wetland and soil functioning relative to comparable areas','Landsat/GEE export code drafted, NOT executed'),
 ('Housing and social','Return to safe shelter, schooling, healthcare access and displaced households','One-off needs assessments identified; no longitudinal local records')],7.9)
para(d,'The index cannot be called “multi-domain” until at least two independently measured, validated domains have been integrated. Vegetation spectral recovery cannot substitute for ecological function; nighttime lights cannot substitute for household welfare.')
hd(d,'2. Observed agricultural production (official data)')
tbl(d,['Crop','2017–18 (tonnes)','2018–19 change','2020–21 change'],[
 ['Rice','521,310','+10.9%','+20.3%'],['Banana','565,829','−24.2%','−3.8%'],['Plantain','379,683','+0.9%','+8.7%']])
d.add_picture(str(root/'figure_01_state_crop_trajectories.png'),width=Inches(6.6))
small(d,'Figure 1. Statewide crop-production trends indexed to 2017–18 = 100. Annual output is an observational agricultural outcome, not an estimate of 2018 flood damages or recovery duration.')
hd(d,'3. What we calculated')
para(d,'For each district and crop, annual relative output = production in year t / production in 2017–18. An illustrative output-shortfall proxy is max(0, 1 − relative output). We averaged this across three crops and three follow-up years; each crop-year received equal weight. Excess output is treated as zero deficit, not negative damage. This does NOT account for counterfactual growth, crop prices, sowing area, crop yield, flood footprint, and other changes.');
para(d,'We then combined the published district-vulnerability score with the output-shortfall proxy using a mixing coefficient α: Score(α) = (1−α) × scaled published score + α × scaled shortfall. Scaling was performed either by minimum–maximum values or by rank percentiles, and α varied between 0.10, 0.25 and 0.50. These α are stress tests, not estimated or justified policy weights.')

d.add_picture(str(root/'figure_04_normalization_comparison.png'),width=Inches(6.7))
small(d,'Figure 2. Published rank and two alternative composite rankings at 25% illustrative agricultural weight. At the percentile-based cutoff, districts tie; membership in a rigid top-five can depend on tie-breaking. Rankings are descriptive scenarios.')
hd(d,'4. Robustness: do ranks change because of useful information?')
tbl(d,['25% agricultural scenario','Top-five overlap','Spearman vs original','Avg absolute rank movement'],[
 ('Percentile rank scaling','5/5 (tie-sensitive)','0.972','0.64'),
 ('Min–max scaling','3/5','0.855','1.43')])
para(d,'Across 28 settings at α=0.25 (2 normalizations × 2 time horizons × 7 crop combinations), only 7 preserved all 5 original top districts, 17 preserved 4, and 4 preserved 3. This proves sensitivity to design choices, not that the recovery component is better.')
para(d,'A negative-control permutation of the agricultural factor showed that random indicators frequently produce as much or more rank movement than the observed proxy. Rank reversal by itself is not evidence of validity.')
hd(d,'5. Exploratory temporal diagnostic — not a flood-event validation')
para(d,'We fitted no machine-learning model. Instead we formed descriptive 2018–19 and 2019–20 crop-output shortfalls, combined them with the published vulnerability score, and checked whether the selected top five districts contained more 2020–21 production shortfall. With min–max scaling, the risk-only top five accounted for 36.9% of 2020–21 shortfall; a 25%-weighted blend accounted for 59.4%. Against randomized agricultural input, this result had an empirical exceedance fraction around 0.077 in 10,000 permutations.')
para(d,'This is an exploratory check, not robust evidence of improvement: (i) the 2026 risk score is chronologically unavailable in a true 2020 prediction, (ii) the 2018 flood contribution is unidentified, (iii) agriculture is autocorrelated, (iv) n=14, (v) other floods and COVID may change annual production, (vi) weights and normalization were explored after seeing data, and (vii) independent per-area functional recovery was not observed. No significance claim is warranted.')
hd(d,'6. Diagnostic: adaptive capacity semantics')
para(d,'Published vulnerability Table 9 reports four components: hazard (0.30), exposure (0.25), sensitivity (0.25) and adaptive capacity (0.20). Reconstructed weighted sum 0.30H+0.25E+0.25S+0.20A matches the published vulnerability score to within ±0.0005 across all 14 districts. Yet the prose interprets high A as “strong adaptive capacity,” which ordinarily reduces vulnerability. A sensitivity test replacing A with (1−A) changes the rank order substantially (Spearman 0.376; only 3/5 original top-five retained).')
para(d,'This ambiguity may arise from reporting terminology, scaling or coding. It should be resolved by checking the complete original methods and, ideally, contacting the authors. It must not be represented as a proven mathematical error.')
hd(d,'7. Feasibility verdict and controlled next experiments')
for txt in [
 'E1 | Flood attribution and pre-event baseline: obtain 2014–18 pre-flood crop observations, 2018 satellite-observed inundation, district/block area exposed, local rainfall, and a comparison group. Use event-study or difference-in-differences designs with seasonality and concurrent shocks represented. Compare total output, cultivated area and yield separately.',
 'E2 | Actual recovery curves: export seasonal Landsat NDVI and moisture metrics and monthly VIIRS nighttime light. Compare flood-exposed versus matched reference places. Record valid observation fractions and masking; define cumulative deficit over a prespecified recovery horizon.',
 'E3 | Add at least two independent functional outcomes: agricultural statistics plus verified economic surveys/transactions, infrastructure restoration records or housing completion. No imputation of social/economic function from spectral greenness.',
 'E4 | Retrospective ranking first: use risk-only and risk-plus-observed-recovery indices at the same administrative scale. Predeclare scaling and weights; present full sensitivity region, not one selected ranking.',
 'E5 | Independent decision validation: using outcomes and risk inputs available before a subsequent flood, predict subsequent event-specific cumulative loss. Use spatial blocks and event-held-out tests, top-K capture and uncertainty. Only claim predictive value if leakage-safe.',
 'STOP / PIVOT | If neither time-stamped local outcome data nor attributable flood exposure exists, narrow to agricultural recovery monitoring rather than claim a multidimensional, operational flood-priority index.'
]:para(d,'• '+txt)
hd(d,'8. Sources and provenance')
refs=[
 '[1] Kerala Dept. of Economics and Statistics. Agricultural Statistics 2017–18. Table 4. https://ecostat.kerala.gov.in/storage/publications/247.pdf',
 '[2] Kerala Dept. of Economics and Statistics. Agricultural Statistics 2018–19. Table 4. https://ecostat.kerala.gov.in/storage/publications/239.pdf',
 '[3] Kerala Dept. of Economics and Statistics. Agricultural Statistics 2019–20. Table 4. https://www.ecostat.kerala.gov.in/storage/publications/3.pdf',
 '[4] Kerala Dept. of Economics and Statistics. Agricultural Statistics 2020–21. Table 4. https://ecostat.kerala.gov.in/storage/publications/622.pdf (wetland rice series used to avoid change in dryland treatment)',
 '[5] Kendagannaswamy et al. (2026). Improving Flood Susceptibility Assessment in Kerala: Integration of Advanced Machine Learning Models with Socioeconomic Vulnerability Analysis. Journal of Indian Society of Remote Sensing. doi:10.1007/s12524-026-02440-y. Table 9 of attached PDF.',
 '[6] Government of Kerala / World Bank / ADB / UN / EU. 2018 Kerala Floods and Landslides Post Disaster Needs Assessment. https://sdma.kerala.gov.in/wp-content/uploads/2019/03/PDNA-report-FINAL-FEB-2019_compressed.pdf',
 '[7] Beyer, Narayanan & Thakur (2022). Natural Disasters and Economic Dynamics: Evidence from the Kerala Floods. NIPFP Working Paper 383. https://nipfp.org.in/media/medialibrary/2022/04/WP_383_2022.pdf',
 '[8] Ali & George (2022). Modelling a Community Resilience Index for Urban Flood-Prone Areas of Kerala, India. Natural Hazards. doi:10.1007/s11069-022-05299-7.'
]
for ref in refs:small(d,ref)
para(d,'Reproducibility: experiment.py and robustness.py regenerate the tables, ranks, robustness summary and figures from manually transcribed official crop values; see data sources and source PDF page fields in district_crop_panel.csv. GEE script is prepared but explicitly unexecuted.')

out=Path('/mnt/data/Kerala_Flood_Recovery_Experimental_Findings.docx');d.save(out);print(out)

readme='''# Kerala recovery-priority research: exploratory pilot (21 October 2026)\n\n## What is actually measured\n\n* Agricultural production for 14 Kerala districts, three crops, four annual periods: 168 official report values.\n* Published district vulnerability scores from Kendagannaswamy et al (2026), attached Meenachil.pdf, Table 9.\n* Sensitivity experiments involving **hypothetical weighted combinations**, descriptive pseudo-holdout, and rank changes.\n\n## NOT yet measured / must NOT claim\n\n* No recovery durations or flood-attributable loss estimates. Annual production is affected by cropping area, yield, rainfall, prices, interventions and repeat disasters.\n* No independent Kerala-wide economic, housing, infrastructure, social or environmental recovery data extracted.\n* No machine learning flood or recovery predictions trained.\n* `gee_recovery_proxies_UNEXECUTED.js` is a proposal for Earth Engine and has **not been run**; it requires access, authentication and validation.\n* Baseline vulnerability was published in 2026, so analyses of years 2018–2021 with that score are ex post and cannot be characterized as leak-free temporal validation.\n* Ranking changes are sensitive to the scaling rule and weights and do NOT demonstrate a superior priority policy.\n\n## Sources\n\nOfficial Kerala Dept of Economics & Statistics agricultural PDFs:\n* 2017–18 https://ecostat.kerala.gov.in/storage/publications/247.pdf\n* 2018–19 https://ecostat.kerala.gov.in/storage/publications/239.pdf\n* 2019–20 https://www.ecostat.kerala.gov.in/storage/publications/3.pdf\n* 2020–21 https://ecostat.kerala.gov.in/storage/publications/622.pdf\n\nBaseline: Kendagannaswamy et al (2026), https://doi.org/10.1007/s12524-026-02440-y , Table 9.\n\nThe district_crop_panel.csv rows preserve source PDF URLs and page numbers. Manual transcription should be checked independently against the published PDF tables before journal submission.\n\n## Reproduce\n\n    python experiment.py\n    python robustness.py\n    python make_comparison_figure.py\n\nPython packages: numpy, scipy, matplotlib, pandas (view optional).\n\n## Files\n\n* `district_crop_panel.csv`: source data\n* `district_descriptive_ranks.csv`: district rank and output-shortfall sensitivity\n* `experiment_results.json`: numeric checks and methods\n* `robustness_results.json`, `sensitivity_grid.csv`: robustness results\n* `figure_01_*`, `figure_02_*`, `figure_03_*`, `figure_04_*`: visual diagnostics\n* `gee_recovery_proxies_UNEXECUTED.js`: **draft only**, not empirical data\n* `Kerala_Flood_Recovery_Experimental_Findings.docx` (at /mnt/data level) research report.\n\n## Why this is only a pilot\n\nOne earlier 2017–18 agricultural season is NOT a suitable estimate of normal function, and one-year observations cannot establish time to recovery. Event-level flood footprints and two or more independently measured functional recovery dimensions are necessary before testing the paper's central hypothesis.\n'''
(root/'README.md').write_text(readme)
