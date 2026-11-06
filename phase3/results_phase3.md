# Phase 3 executed results

## Experiment A: official seasonal rice panel

The executed panel contains **252 district-season-year observations**: 14 districts, three harvest seasons, and six agricultural years from 2014–15 to 2019–20. Area is in hectares, production in metric tonnes, and yield is calculated tonnes per hectare. The four agricultural years 2014–15 through 2017–18 define a same-season pre-event reference. The official source pages and documented corrections are in [sources.md](sources.md) and [data_quality.md](data_quality.md).

The report's 2018–19 state production changes relative to **2017–18** are independently reproduced from reconstructed district sums:

| Harvest season | 2017–18 t | 2018–19 t | Change |
|---|---:|---:|---:|
| Autumn | 148,913 | 101,943 | −31.5419% |
| Winter | 218,934 | 279,529 | +27.6773% |
| Summer | 153,463 | 196,784 | +28.2290% |
| **Annual** | **521,310** | **578,256** | **+10.9236%** |

This confirms the key annual-masking pattern: the autumn contraction coexists with a positive annual total. An annual gain cannot establish that every season or district recovered.

Against the **2014–15 to 2017–18 same-season mean**, state results are:

| Year, season | Area (ha; % vs baseline) | Production (t; % vs baseline) | Yield (t/ha; % vs baseline) |
|---|---:|---:|---:|
| 2018–19 Autumn | 60,718; +1.50% | 101,943; −36.13% | 1.679; −37.21% |
| 2018–19 Winter | 88,450; +6.73% | 279,529; +30.25% | 3.160; +23.33% |
| 2018–19 Summer | 48,858; +5.78% | 196,784; +37.55% | 4.028; +30.07% |
| 2019–20 Autumn | 54,694; −8.57% | 142,946; −10.44% | 2.614; −2.26% |
| 2019–20 Winter | 80,049; −3.40% | 244,794; +14.06% | 3.058; +19.34% |
| 2019–20 Summer | 56,308; +21.91% | 199,338; +39.34% | 3.540; +14.32% |

State annual production was **+11.7857%** above its four-year annual mean in 2018–19 and **+13.4911%** in 2019–20; its annual yield was +6.8635% and +12.4547%. Thus annual output remains positive while same-season autumn output is below its historical mean. State yield is production divided by area, so the autumn production decline with nearly flat area in 2018–19 is associated with a substantially lower calculated yield. It cannot be assigned to inundation from these statistics alone.

District variation is substantial. Of the 13 districts with a positive pre-event Autumn production baseline, **11/13** were below that mean in 2018–19 and **11/13** in 2019–20. **9/13** fell below their own four-year pre-event minimum in 2018–19, and **7/13** in 2019–20. Wayanad had a zero pre-event autumn production baseline, making its percentage deviation undefined. Selected autumn production changes versus the four-year mean:

| District | 2018–19 | 2019–20 |
|---|---:|---:|
| Alappuzha | −95.33% | −34.33% |
| Kottayam | −92.30% | −71.55% |
| Pathanamthitta | −75.36% | −34.78% |
| Thrissur | −50.93% | −24.87% |
| Kozhikode | −50.34% | −62.42% |

The count below the **pre-event median** is also 11/13 for Autumn in each post-event year. Winter differs in 2019–20: 7/14 districts are below the pre-event mean, but 9/14 are below the median. Baseline choice therefore changes some district classifications even when the broad autumn pattern is stable.

The 2019–20 values show improvement from 2018–19 in some districts and further decline in others. They support a **two-observation descriptive trajectory**, not a measured time to recover. The 2019 flood season, changing rice management and other shocks are not separated here. `district_season_trajectories.csv` records both post-year values, their percent changes and a descriptive sum of below-baseline amounts. That sum is **not** a flood-attributable cumulative deficit.

The vector figures are [state seasonal production](figures/state_seasonal_rice_production.svg) and [district autumn production](figures/district_autumn_production_deviations.svg). Underlying values are in `state_season_series.csv` and `district_season_trajectories.csv`.

## Experiment B and C status

The revised Sentinel-1 pilot script inventories scene IDs, UTC dates, relative orbit, pass/mode/polarization, AOI coverage and incidence angle before a manual scene pair is selected. It exports both candidate thresholds and QA bands only after explicit user-set activation. It passed JavaScript syntax checking; **no Earth Engine imagery was queried or exported** because this workspace has neither Earth Engine CLI/Python access nor a signed-in Code Editor session. Its candidate outputs, if run, require independent inundation validation.

Seasonal rice statistics are a feasible observed agricultural **monitoring** dimension. No ecological, economic, housing or infrastructure recovery measurements were executed. No spatially linked flood exposure or independent recovery outcome exists here. We therefore did **not** create a recovery-adjusted ranking or run a purported validation of its prioritisation. Phase 2's earlier rank-sensitivity calculations remain a separate retrospective output-shortfall exercise, not a recovery-priority test.

## Interpretation for the paper

> Official district-season rice statistics demonstrate that Kerala's 2018–19 annual production increase concealed a marked autumn decrease and major geographic heterogeneity. Against a four-year same-season reference, statewide autumn production was 36.1% lower in 2018–19, whereas winter and summer production were 30.2% and 37.6% higher. These are observed production deviations, not estimates of flood-caused damage or duration of recovery. The evidence motivates exposure-linked, seasonally controlled recovery analysis, but it does not establish that including recovery improves vulnerability rankings.
