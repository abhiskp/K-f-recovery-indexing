# Data dictionary and missing-value conventions

## Common scope

The unit of the crop panels is **Kerala district × crop × agricultural year**, with 14 districts and three reported crops: rice, banana and plantain. `agricultural_year` values such as `2018-19` denote Kerala DES reporting years, **not** calendar years or an August 2018 event window. Phase 2 uses 2014–15 through 2017–18 as pre-flood annual reference years and 2018–19 through 2020–21 as follow-up years. District names in the package are harmonized to the 14 spellings used in `phase2/analysis.py`; no polygon boundaries or sub-district geometry are included. Production is in **metric tonnes**; area is in **hectares**; yield is **tonnes per hectare**. Percent changes are percentage points relative to the earlier value, e.g. `100 × (new/old − 1)`. Ratios and deficits are unitless fractions, not percentages.

No CSV in this handoff has a blank field. **Absence of a blank is not evidence that all desired recovery data exist.** There are no satellite recovery, flood exposure or infrastructure restoration observations in the package. No missing crop values were imputed. A computed deficit of zero means production met or exceeded the chosen historical reference, not that flooding caused no damage or that full recovery was observed. The strings `data_coverage` and `attribution` are explicit interpretive flags, not quantitative uncertainty intervals. `source_pdf_page` is the PDF page index used by the original transcription or the historical compendium; `source_printed_page` is the printed page stated in the official report.

## Phase 2 data files

### `phase2/data/pre2018_crop_production.csv` (126 rows)

| Column | Definition |
|---|---|
| `district` | One of 14 harmonized Kerala district names. |
| `agricultural_year` | 2014–15, 2015–16 or 2016–17. |
| `crop` | `rice`, `banana` or `plantain`. |
| `production_tonnes` | Official annual production rounded to whole metric tonnes in the historical compendium. |
| `source_pdf_url` | Official source PDF URL. |
| `source_pdf_page` | PDF page containing the crop table: rice 95, banana 101, plantain 102. |
| `source_table` | Historical compendium table number: 41, 44 or 45 respectively. |
| `precision_note` | Records whole-tonne historical compendium precision. |

### `phase2/data/crop_panel_2014_2021.csv` (294 rows)

This is the joined seven-year panel. `district`, `agricultural_year`, `crop`, `production_tonnes`, `source_pdf_url` and `source_pdf_page` have the meanings above. `source_table` is 41/44/45 for added historical values and 4 for inherited annual-report values. `precision_note` distinguishes whole-tonne historical data from inherited annual-report precision and warns that the latter full cell audit is pending. `provenance` identifies either Phase 2 historical transcription or the inherited Phase 1 CSV. The compound key `(district, crop, agricultural_year)` is unique.

## Phase 2 result tables

### `phase2/results/annual_output_deviations.csv` (126 rows)

One row per district, crop and follow-up agricultural year (2018–19, 2019–20, 2020–21).

| Column | Definition |
|---|---|
| `district`, `crop`, `agricultural_year` | District/crop/year key as above. |
| `production_tonnes` | Reported follow-up production, metric tonnes. |
| `pre_mean_tonnes` | Mean annual production across 2014–15 to 2017–18 for that district and crop, tonnes. |
| `pre_median_tonnes` | Median of those four annual values, tonnes. |
| `ratio_to_pre_mean` | Follow-up production divided by `pre_mean_tonnes`, unitless. |
| `deficit_vs_pre_mean` | `max(0, 1 − ratio_to_pre_mean)`, unitless annual output shortfall fraction. |
| `deficit_vs_pre_median` | `max(0, 1 − production_tonnes/pre_median_tonnes)`, unitless. |
| `original_deficit_vs_2017_18` | `max(0, 1 − production_tonnes/2017–18 production)`, unitless inherited-style comparison. |
| `data_coverage` | Text stating four annual pre-observations and one annual follow-up observation for the row. |
| `attribution` | Text stating the output deviation is unattributed and not linked to 2018 inundation. |

### `phase2/results/state_area_yield_decomposition.csv` (3 rows)

One row per crop, **statewide** only, comparing 2017–18 with 2018–19. `crop` is as above. `area_2017_18_ha` and `area_2018_19_ha` are official reported area in hectares. `production_2017_18_tonnes` and `production_2018_19_tonnes` are reconstructed district sums in tonnes. `area_pct_change` and `production_pct_change` equal `100 × (2018–19 / 2017–18 − 1)`. `yield_2017_18_t_per_ha` and `yield_2018_19_t_per_ha` equal production divided by area, tonnes/hectare. `yield_pct_change` compares those calculated yields in percent. `source_pdf_url` points to the official 2018–19 report; `source_printed_page` is 126. This decomposition is descriptive, not causal.

### `phase2/results/rank_sensitivity.csv` (6 rows)

One row per normalization × crop-output baseline. `normalization` is `minmax` (range scaling) or `rank` (midrank percentile scaling). `output_baseline` is `2017_only`, `four_year_mean` or `four_year_median`. `alpha` is the illustrative crop-output weight (0.25); the published vulnerability weight is 0.75. `spearman_vs_published` and `kendall_vs_published` are unitless full-order rank correlations with the published 2026 vulnerability score. `top5_overlap` is the integer count of common districts between the original and blended top fives. `mean_abs_rank_shift` is the mean absolute district rank displacement, in rank positions. `top5` is a semicolon-separated ordered list of the selected districts; exact score ties use the higher original vulnerability score as secondary order.

### `phase2/results/leave_one_pre_year_out.csv` (4 rows)

`omitted_pre_year` is the excluded reference agricultural year. The other three pre-flood years form the district/crop mean. `top5` is the semicolon-separated retrospective 25% min–max blend order; `top5_overlap` is the count common with the original top five; `spearman_vs_published` is a unitless correlation. This is baseline-choice sensitivity, **not** a confidence interval.

### `phase2/results/original_input_manifest.csv` (21 archived entries)

`path` is a path relative to the former project root, `bytes` is file size, and `sha256` is the file's SHA-256 digest at the original audit. Its `.DS_Store` entry is not included in this ZIP; see `MANIFEST.md` for current package contents and hashes.

## Inherited baseline CSVs

### `Kerala_Flood_Recovery_Codex_Package_Fixed(1)/kerala_recovery_investigation/district_crop_panel.csv` (168 rows)

`district`, `agricultural_year`, `crop`, `production_tonnes`, `source_pdf_url`, and `source_pdf_page` have the definitions above; periods are 2017–18 to 2020–21. `geography` is a text scale label, and `measurement_note` records annual-output and rice-series limitations. The 2020–21 rice values are **wetland rice**, chosen for continuity with earlier years.

### `.../district_descriptive_ranks.csv` (14 rows)

One row per district. `district` is the harmonized name; `published_vulnerability_2026` is the reported normalized score and `published_rank` its descending rank (1 highest). `hazard`, `exposure`, `sensitivity`, and `adaptive_capacity_as_labelled` are the four reported normalized score components. `relative_output_{rice|banana|plantain}_{2018_19|2019_20|2020_21}` are nine production ratios to the same district/crop's 2017–18 output. `observed_agricultural_output_shortfall_2018_2020` is the equal-weight mean of nonnegative crop/year shortfalls across all three follow-up years; `observed_agricultural_output_shortfall_2018_2019` uses the first two follow-up years; `agricultural_output_shortfall_2020_21` uses the third year. Despite the inherited column prefix `observed`, these are descriptive output shortfalls, **not measured flood-attributable recovery**. `illustrative_rank_alpha_{0p1|0p25|0p5}` is a blended descending rank at crop weights 0.10/0.25/0.50. `rank_change_alpha_{0p1|0p25|0p5}` is published rank minus illustrative rank, in rank positions; positive values indicate movement toward rank 1.

### `.../sensitivity_grid.csv` (84 rows)

`normalization` is `minmax` or `rank`; `years` is 2 or 3 follow-up agricultural years from 2018–19 onward; `crops` is a hyphen-separated subset of rice, banana, plantain; `alpha` is the crop-output weight (0.10, 0.25, 0.50); `spearman_risk_vs_blend` is unitless rank correlation with the published score; `top5_overlap` is the integer count common with the published top five; `mean_abs_rank_shift` is in rank positions; and `top5` is a semicolon-separated ordered district list. These are hypothetical retrospective blends.

### `Kerala_Flood_Recovery_Data_Audit.csv` (15 rows)

This is a 21 October 2026 source inventory, not an observation panel. `dataset` names a candidate source; `role` states its proposed use; `spatial_scale` and `temporal_coverage` describe proposed coverage; `verification_status_as_of_2026-10-21` records audit status at that date; `source_url` is provenance; `next_action` is the outstanding verification step. Catalog availability is not evidence that imagery was extracted.

## JSON and figure outputs

`phase2/results/summary.json` stores panel counts, year lists, state totals, area/yield calculations, inherited-total checks, vulnerability-formula audit, ranking specifications and leave-one-out checks. `phase2/results/legacy_reproduction.json` stores the 84-grid discrepancy list (empty), three deterministic pseudo-holdout checks, and a note that stochastic permutations were not rerun. The inherited `experiment_results.json` and `robustness_results.json` preserve their original summaries and random-test outputs. JSON `null`, if present, means no calculable statistic; it must not be treated as zero. The SVG figure is state crop output relative to the four-year mean with a non-attribution caption; original PNGs are inherited exploratory figures.
