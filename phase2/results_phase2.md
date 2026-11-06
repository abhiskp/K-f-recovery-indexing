# Phase 2 executed results and research decision

**Status, 27 October 2026:** The historical agricultural baseline and
retrospective rank stress test were executed. A 2018 inundation raster and
seasonally matched satellite recovery panel were **not** produced. Thus the
central hypothesis—whether *observed post-flood recovery* improves Kerala
priority rankings—remains untested.

## Reproduction and corrections

- Independently read the supplied CSV, validated its 168 unique keys and
  recomputed all 12 original crop/year state totals to their stored precision.
  A standard-library implementation reproduced **all 84 deterministic
  sensitivity-grid specifications with zero discrepancies**, plus all three
  deterministic pseudo-holdout top-five capture values. The original 25%
  percentile-rank top five and Spearman 0.972498 were also reproduced.
  Stochastic permutation draws were not independently rerun. The original scripts
  were not rerun in place because they rewrite supplied inputs/outputs and
  this environment lacks SciPy and Matplotlib. Source files are hashed in
  `results/original_input_manifest.csv`.
- The original 2020–21 wetland-rice choice is explicitly supported by the
  [2020–21 official table](https://ecostat.kerala.gov.in/storage/publications/622.pdf),
  which separates wetland, dryland and total rice. District wetland values sum
  to 626,886.087 tonnes, 1.913 below the printed rounded state total.
- The [2018–19 annual table](https://ecostat.kerala.gov.in/storage/publications/239.pdf)
  and later [compendium](https://www.ecostat.kerala.gov.in/storage/publications/626.pdf)
  differ by one tonne for Alappuzha rice (128,560 versus 128,561).
  The original annual-table entry is retained. Full cell-by-cell review of
  all 168 entries remains open.
- The archived 2020–21 pseudo-holdout is **not** a valid prospective test:
  its risk score was published in 2026. The original published vulnerability
  arithmetic adds a variable labelled adaptive capacity even though capacity
  is described as protective; its semantic direction is unresolved.

## New observed agricultural panel

The [DES historical compendium](https://www.ecostat.kerala.gov.in/storage/publications/626.pdf)
supplied 126 additional pre-flood district production observations for
2014–15 through 2016–17. The analysis now uses four pre-flood annual periods
for each of 14 districts and three crops. All nine newly transcribed
crop/year district sums equal the printed state totals. This is a stronger
reference for annual output comparisons, but it cannot adjust for the
monsoon season or identify a causal flood effect.
The provenance-bearing combined 294-row table is
`data/crop_panel_2014_2021.csv`.

State production relative to the four-year pre-flood **mean**:

| Crop | 2018–19 | 2019–20 | 2020–21 |
|---|---:|---:|---:|
| Rice | +11.8% | +13.5% | +21.2% |
| Banana | −19.7% | +2.7% | +1.9% |
| Plantain | −7.4% | −1.7% | −0.2% |

The corresponding annual district/crop deviations, coverage and explicit
non-attribution status are saved in `results/annual_output_deviations.csv`.
Values above the reference mean have zero *shortfall* in the ranking
diagnostic; they are not evidence of full restoration.

The [official 2018–19 crop-area comparison](https://ecostat.kerala.gov.in/storage/publications/239.pdf)
shows why output alone is incomplete:

| Crop | Area change | Calculated yield change | Production change |
|---|---:|---:|---:|
| Rice | +4.7% | +5.9% | +10.9% |
| Banana | −14.9% | −10.9% | −24.2% |
| Plantain | +3.2% | −2.3% | +0.9% |

These are state aggregates; no district exposure or counterfactual trend was
used. The output is in `results/state_area_yield_decomposition.csv`.

## Rank sensitivity from observed crop output

For an illustrative 75:25 mix of published 2026 vulnerability and mean annual
crop-output shortfall, the results are:

| Normalization | Shortfall reference | Spearman versus published | Top-five overlap |
|---|---|---:|---:|
| Min–max | 2017–18 alone | 0.855 | 3/5 |
| Min–max | Four-year pre-flood mean | 0.868 | 3/5 |
| Midrank percentile | 2017–18 alone | 0.972 | 5/5, cutoff tie-sensitive |
| Midrank percentile | Four-year pre-flood mean | 0.964 | 4/5 |

The complete table includes Kendall correlation, median-baseline sensitivity,
and mean rank displacement (`results/rank_sensitivity.csv`). Omitting one
pre-flood year at a time yields 3/5 or 4/5 top-five overlap under min–max
normalization (`results/leave_one_pre_year_out.csv`). Thus both the scaling
rule and baseline choice materially affect the descriptive order. There is no
scientific basis here to choose the version with the largest rank shift.

## Satellite and independent validation status

The [KSDMA 2018 inundation map](https://sdma.kerala.gov.in/wp-content/uploads/2020/11/Flood_2018-1.pdf)
was inspected. It is a reference PDF crediting NRSC, not the georeferenced
event raster required for pixel-level validation. The [crowdsourced depth
map](https://sdma.kerala.gov.in/wp-content/uploads/2020/11/CROWD_INUNDATION.pdf)
is likewise a PDF; coordinates and depth data were not obtained. The
[Sentinel-1](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD)
and [VIIRS](https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMSLCFG)
catalogs confirm relevant image collections, but no local Earth Engine
credentials exist, and the Code Editor redirected to Google sign-in. The
prepared Earth Engine script passed JavaScript syntax checking only. It has
**never been executed** and has produced no maps or satellite measurements.

Functional data that could check satellite proxies: repeated district/block
crop area and yield reports can test vegetation–agriculture association;
geocoded inundation/depth observations can test the SAR event layer; dated
house habitability, road passability and service-restoration logs could
measure infrastructure/housing recovery. The [PDNA](https://sdma.kerala.gov.in/wp-content/uploads/2019/03/PDNA-report-FINAL-FEB-2019_compressed.pdf)
contains post-disaster damage and needs, not a local repeated restoration
panel. No independent economic-recovery series was obtained. VIIRS cannot
yet be validated against economic function.

## Paper-ready interpretation and decision

> Four years of pre-flood official district production data show that the
> agricultural output baseline materially influences a retrospective ranking
> sensitivity exercise. A 25% crop-output component preserves three of five
> highest-ranked districts under min–max scaling and four under rank scaling.
> These changes do not establish that recovery information improves priority
> decisions: annual output is not linked to observed 2018 inundation, and the
> comparator vulnerability score was published in 2026.

**NO-GO for an empirical multidimensional recovery-priority index or claims of
better prioritisation at this stage.** Continue the focused 2018 feasibility
pilot after authenticated satellite access and independent event validation
data are available. An agricultural monitoring paper may become viable if a
validated inundation layer and seasonally resolved crop/vegetation trajectory
can be linked at stable local units. A predictive claim additionally requires
an independent later event with predictors frozen at decision time.

The existing manuscript remains unchanged because the new work has not
measured flood-attributable recovery. The paragraph above is suitable for an
accurately labelled audit or limitations section, alongside the new vector
figure `figures/crop_output_relative_to_four_year_baseline.svg`.
