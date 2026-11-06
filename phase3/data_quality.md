# Source and calculation audit

The main panel has **252 unique district × season × year observations**, with no missing area or production cells. Literal source zeros can make calculated yield or percent change undefined. For the pre/post comparison, all 14 Winter and Summer district production series have positive pre-event baselines; Wayanad Autumn has a zero pre-event production baseline and is excluded from percentage comparisons.

`experiment_a.py` logs **33 source discrepancies** in `results/data_quality_findings.csv`. The material ones are:

| Source issue | Evidence | Phase 3 resolution |
|---|---|---|
| 2019–20 compendium paddy area annual totals fail component sums in eight districts, including Malappuram (printed 9,672 vs seasonal 8,625 ha) and Kozhikode (printed 921 vs seasonal 2,128 ha). The compendium also places 425 summer ha in Kannur and 6 in Wayanad, while the original annual report has 6 and 425, respectively. | Compendium Table 17 p.56 vs original 2019–20 report Table 3 p.38; `annual_report_2019_crosscheck.csv`. | Use all 2019–20 original annual-report seasonal area values. All its 15 row totals and four state totals reconcile. |
| 2019–20 compendium Winter rice production is 65 t higher for Wayanad and 65 t lower for Kannur than the original report. | Compendium Table 41 p.88 vs original 2019–20 report Table 4 p.142. | Use original annual-report production for all 2019–20 cells. All its row and state totals reconcile. |
| 2017–18 Idukki Winter production is 1,809 t in the later compendium, 1,808 t in the annual report. The 1,808 t value reconciles with the printed district annual 2,293 t and state Winter 218,934 t. | Compendium Table 41 p.88 vs 2017–18 report Table 4 p.143. | Correct this one cell to 1,808 t, recording the source decision. |
| 2018–19 seasonal compendium integers differ slightly from the annual report's decimal cells. Alappuzha Winter is 40,184 t versus 40,183.376 t. | Compendium Table 41 p.88 vs original 2018–19 report Table 6 p.183. | Keep the compendium integers for a consistent six-year published panel; retain original decimal crosscheck and note rounding. |

The 2019–20 original annual report passes **38 exact checks**: 15 district/state rows × 2 metrics and four season/All state columns × 2 metrics. The 2018–19 decimal district sums equal printed state totals for production in all three seasons and for area in Winter/Summer; autumn district area sum differs by only −0.02 ha, compatible with printed decimal precision. All original compendium transcriptions and annual-source comparisons remain included for audit.

Against Phase 2's 84 annual district rice cells, the seasonal reconstruction has just **two nonzero differences**, both in 2018–19: Alappuzha +1 t and Palakkad −1 t. Their signs offset at state level. This is a source rounding/selection difference, not a new measured flood effect. Phase 2 files and conclusions were not rewritten.

The official tables are administrative survey estimates, and the record includes no published standard errors for these district-season cells. We report source discrepancies and pre-period range/median sensitivity, but cannot attach calibrated measurement confidence intervals. Temporal baseline uncertainty, structural crop shifts, district aggregation and later flood effects remain material.
