from pathlib import Path
from docx import Document
from docx.shared import Pt,Inches,RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
import csv
root=Path('/mnt/data/kerala_recovery_investigation')
infile=Path('/mnt/data/Kerala_Flood_Recovery_Priority_Manuscript_Working_Draft.docx')
out=Path('/mnt/data/Kerala_Flood_Recovery_Manuscript_v0_2.docx')
d=Document(infile)
for p in d.paragraphs:
 if p.text.startswith('STATUS: Hypotheses and methods drafted'):
  p.text='STATUS (21 October 2026): Protocol plus exploratory agricultural-data pilot completed. 168 official district–crop–year production observations and the published district vulnerability ranking were examined. These are NOT event-attributable recovery measurements, and no multi-domain recovery index or validated predictive model has yet been produced.'
 if p.text.startswith('Crucial temporal caution: Ecostat 2018–19 reports show'):
  p.text='Observed agricultural data audit: Kerala district-level rice, banana and plantain production for 2017–18 through 2020–21 has been reconstructed (168 entries). Statewide 2018–19 output relative to 2017–18 rose for rice (+10.9%) and plantain (+0.9%) but declined for banana (−24.2%). This is neither proof nor disproof of local flood damage: counterfactual crop production, flooded agricultural area, cropping choices and seasonal variability are unmeasured. See exploratory results appendix.'
 if p.text=='11. Planned figures and tables (all results pending)':
  p.text='11. Planned main-study figures and tables (recovery-model results pending)'

# Appendix after references for transparent pilot, with existing manuscript preserved.
d.add_page_break()
d.add_heading('Appendix A — Exploratory Empirical Pilot (21 October 2026)',level=1)
d.add_paragraph('Scope: these analyses use actual state agricultural observations and published vulnerability scores to test data feasibility and index sensitivity. They do NOT demonstrate post-flood recovery, attributable disaster losses, causal mechanisms or superiority of any index.')
d.add_heading('A1. Official district data and observed agricultural trajectories',level=2)
d.add_paragraph('Agricultural Statistics Reports 2017–18, 2018–19, 2019–20, and 2020–21, Kerala Department of Economics and Statistics, Table 4: 14 districts × three crops (rice, banana and plantain) × four agricultural years (168 reported district-level production values). The 2020–21 rice observations use the wetland series for consistency with the earlier years. Manual transcription and report-page provenance are supplied with the experiment files.')
d.add_picture(str(root/'figure_01_state_crop_trajectories.png'),width=Inches(6.4))
d.add_paragraph('Figure A1. Observed production as a percentage of 2017–18; not flood-attributable losses or a measure of time to functional recovery.')
d.add_heading('A2. Illustrative ranking stress test',level=2)
d.add_paragraph('Define annual district-crop production shortfall against 2017–18 as max(0, 1 – reported production / 2017–18 production); average over three crops and three follow-up years. Form a hypothetical composite (1–α) × scaled published district score + α × scaled agricultural shortfall. The 2026 source score postdates the agricultural outcomes, making this purely retrospective.')
d.add_paragraph('At α=0.25, 3/5 published top-five districts remained when components were min–max normalized, versus 5/5 under percentile-rank normalization (cutoff ties make exact membership tie-sensitive). The rankings changed across 28 plausible crop sets, time windows and normalizations: 3/5 overlap in four cases, 4/5 in seventeen, and 5/5 in seven. Ranking movement should not be interpreted as index improvement.')
d.add_picture(str(root/'figure_04_normalization_comparison.png'),width=Inches(6.5))
d.add_paragraph('Figure A2. Alternative 25% illustrative composites. No weight has yet been supported by policy outcomes or independent recovery observations.')
d.add_heading('A3. Diagnostic pseudo-holdout and baseline audit',level=2)
d.add_paragraph('An illustrative 2020–21 crop-output-shortfall check showed that top-five areas selected by the published risk score captured 36.9% of the 2020–21 crop shortfall proxy, compared with 59.4% using a 25% min–max-normalized blend of earlier crop shortfall and published risk; permutation exceedance fraction 0.077 (10,000 draws). This is NOT a leak-free event-held-out experiment, as the vulnerability score appeared in 2026, contains post-event-derived information and is evaluated against autocorrelated agricultural outcomes. It is not a publication-quality claim of predictive performance.')
d.add_paragraph('The published baseline table is arithmetically consistent with 0.30 × hazard + 0.25 × exposure + 0.25 × sensitivity + 0.20 × the variable labelled adaptive capacity (max error 0.0005). Since the text also calls higher adaptive capacity protective, the intended direction should be verified before any rank comparison is reported as an empirical result.')
d.add_heading('A4. Measurement still required',level=2)
for item in [
 'Flood footprint/exposure by location (Sentinel-1 and ground-truthed maps); rainfall, soil and crop calendar controls; multiple years of pre-flood production.',
 'Seasonal agricultural and ecological trajectories at fixed administrative units, with cloud and observation coverage diagnostics; validate remote-sensing proxies against field data.',
 'At least one independent functional recovery dataset (housing, services, income/expenditure or infrastructure restoration records).',
 'A decision-time-specific ranking protocol and actual later-event holdout to compare rank stability and capture of cumulative recovery burden.'
]:d.add_paragraph(item,style='List Bullet')
# Companion reproducibility information supplied in the separate README.md
d.save(out)
print(out)
