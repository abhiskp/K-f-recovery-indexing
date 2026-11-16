# Executed Phase 7 results (descriptive only)

## Independent Phase 6 calculation check

From the Phase 3 source panel, the 2018–19 **autumn published rice production** change versus each district's 2014–15 to 2017–18 autumn mean is **−65.39108%** across six `all_villages` districts with nonzero baselines and **−15.23957%** across six `some_villages` districts. The unweighted all-minus-some contrast is **−50.15151 percentage points**. The corresponding sums of district absolute departures are **−42,604.75 t** and **−13,997.50 t**. Wayanad's autumn baseline is zero, so its percentage is undefined; Kasaragod was not in either group. The Phase 6 378-row product has one row per district × season × indicator × comparison, `14 × 3 × 3 × 3`; it is not 378 duplicated source observations. The 2017–18 pre-event placebo using a three-year baseline gives **+19.25802 pp**, a warning against a parallel-trends or causal reading. The administrative order includes flood **or landslide**, and no inundated-rice denominator exists. See `results/descriptive_summary.json` and the independent audit in `data/raw/`.

## Extended official rice panel

The source-checked panel now has **462 unique district × rice-harvest-season × agricultural-year rows**: 14 districts, Autumn/Winter/Summer, 2014–15 to **2024–25**. Phase 7 adds 210 rows from 2020–21 through 2024–25. The latest listed 2025–26 official seasonal releases were incomplete across all three seasons at this audit, so they were not appended. New columns retain source PDF/table/printed page/PDF page/URL and status flags. For the newer reports, the main production field uses **Rice (Total)**, not Rice (Wet land); wet and dry components are retained separately. The historical source labels Rice without a component split, so production comparability across that format break is plausible but not fully demonstrated. Pre-2020 production/area ratios are not carried forward as validated yield. All 30 new year × season × metric sums were compared with state controls; the maximum absolute discrepancy is **0.074 tonnes**.

The state sum of published/total autumn rice production is **148,913 t in 2017–18**, **101,943 t in 2018–19**, **142,946 t in 2019–20**, **151,212.272 t in 2020–21**, **125,127.443 t in 2021–22**, **137,051.772 t in 2022–23**, **116,269.383 t in 2023–24**, and **115,407.632 t in 2024–25**. These are successive district totals, not a same-field recovery trajectory. The 2018–19 to 2019–20 change cannot be treated as recovery from 2018 because a separate 2019 flood/landslide affected many districts. Later floods, weather, cultivation shifts and reporting also matter.

## Source and transcription checks

| Source | Table used | Printed / PDF page | State-total finding |
|---|---|---|---|
| [DES 2020–21](https://www.ecostat.kerala.gov.in/storage/publications/622.pdf) | Wet paddy area Table 3; **Rice (Total)** Table 4 | 42/52; 146/157 | Area exact. Autumn total-rice district sum is 0.074 t above printed state row; winter and summer differ by 0.003 t from rounded state rows. Three printed district Rice (Total) cells fail wet+dry component reconciliation: Kozhikode Autumn −3.960 t; Kasaragod Autumn +0.074 t and Summer +0.475 t. They are retained as published and flagged. |
| [DES 2021–22](https://www.ecostat.kerala.gov.in/storage/publications/664.pdf) | Wet paddy Table 3; **Rice (Total)** Table 4 | 38/50; 144/156 | Six state seasonal sums exact at recorded precision. Two winter area cells wrap above their district lines in PDF text: Kollam 1,177.08 ha and Pathanamthitta 217.24 ha; both explicitly repaired. |
| [DES 2022–23](https://www.ecostat.kerala.gov.in/storage/publications/1720.pdf) | Table 3 wet paddy; **Rice (Total)**, not preceding paddy-grain, Table 4 | 42/53; 201/212 | Area exact; autumn total-rice district/state difference 0.002 t, consistent with row rounding. |
| [DES 2023–24](https://www.ecostat.kerala.gov.in/storage/publications/1822.pdf) | Table 3 wet paddy; **Rice (Total)**, not preceding paddy-grain, Table 8 | 43/60; 222/239 | Area and total-rice production exact at 0.001 t. Using the preceding paddy-grain table would mix product definitions and materially overstate rice production. |
| [DES 2024–25 Autumn/Winter](https://www.ecostat.kerala.gov.in/storage/publications/1824.pdf), [Summer](https://www.ecostat.kerala.gov.in/storage/publications/1844.pdf) | Final wet-paddy area, wet+dry rice production; wet-only yield can be computed separately | Unpaginated PDF pp. 4+3, 2+1, 1+2 | Wet and dry production state controls checked before combining. Summer scanned wet/dry tables were visually transcribed; wet-area district sum 66,384.925 ha versus printed 66,384.93 ha (0.005 ha rounding). |

These source PDFs are archived under `data/raw/`. Public availability does not establish an unrestricted redistribution licence for future protected GIS datasets.

## Pre-2018 trend and baseline sensitivity

The four-point pre-event slope file has **84 district × season × indicator rows** for area and production; historical derived yield is excluded because its numerator/denominator component alignment is not verified. Of 14 autumn production district series, **8 have negative descriptive 2014–15 to 2017–18 slopes**. Four years are too few for a reliable local counterfactual. Baseline choices for the 2018–19 autumn administrative group contrast are:

| Same-season baseline | All villages mean % | Some villages mean % | Difference (pp) |
|---|---:|---:|---:|
| Four-year mean | −65.391080 | −15.239570 | −50.151510 |
| Four-year median | −63.856802 | −13.047071 | −50.809731 |
| First-three-year mean | −64.734395 | −18.040367 | −46.694028 |
| Four-point linear extrapolation | −59.775597 | −2.039480 | −57.736118 |

All four remain negative **as descriptive contrasts**; they do not identify flooding as the cause. Percent changes for tiny baseline districts are unstable, and absolute tonnes and area should accompany any future interpretation. A comparable pre-event wet-rice yield series remains unavailable. The placebo and later flood flags prevent calling the subsequent years a measured recovery duration.

## Data availability outcome

No independent GIS-ready 2018 inundation class **and observed/nonobserved footprint** was received. No dated 2018 cultivated-paddy geometry or 2018-valid boundary crosswalk was received. KSDMA depth points remain optional and absent. Thus **no exposure-overlap pilot, mask accuracy metric, flood-attributable recovery model or ranking experiment was executed**. See [source_access_matrix.csv](source_access_matrix.csv), [nonagricultural_coverage_matrix.csv](nonagricultural_coverage_matrix.csv) and [decision_gate.md](decision_gate.md).
