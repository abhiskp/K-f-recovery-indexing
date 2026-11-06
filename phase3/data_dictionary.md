# Data dictionary

**Geography and period.** All district-level CSVs use the 14 Kerala districts named in `experiment_a.py`; there is no local-area geocoding or boundary file. `year` is a July–June agricultural year, from `2014-15` through `2019-20`. `season` is a **harvest** season: Autumn July–October, Winter November–February, Summer March–June (DES definition in [sources.md](sources.md)). `State` appears only in raw transcriptions and annual-report crosschecks; state result series are sums of the 14 districts. There are no monthly field observations.

**Missing values.** Blank CSV cells mean undefined or unavailable, never zero. Specifically, yield is blank for zero area, and percent deviation is blank for zero baseline. `attributable_to_2018_flood=not_established` marks absence of a causal estimate, not a numeric value. All reported 0 area or production values are literal official zeros. Percent values are percentage points relative to their comparison denominator, not fractions. Numeric output is rounded for display after calculations; original integer source cells remain in the processed panel.

## `data/processed/district_season_rice_2014_2020.csv` (252 rows)

One district × harvest season × agricultural year. `district`, `year`, `season` are the key. `area_ha` is harvested/cultivated paddy area as published (hectares); `production_tonnes` is published rice production (metric tonnes); `yield_tonnes_per_ha` is calculated production ÷ area. `area_source_printed_page`, `production_source_printed_page` are the pages printed on the source documents, with URLs in `area_source_url` and `production_source_url`. `source_decision` is `historical_compendium`, `contemporaneous_annual_report` (all 2019–20), or `annual_report_production_correction` (2017–18 Idukki Winter). Source PDF page indices and tables are listed in [sources.md](sources.md).

## Primary Experiment A outputs

| File and unit | Columns |
|---|---|
| `results/seasonal_deviations.csv`: 252 rows, district × season × post-event year × metric. | `district`, `season`, `year`, `metric` (`area`, `production`, `yield`); `observed`, `baseline_mean_2014_2017`, `baseline_median_2014_2017`, `pre_min`, `pre_max` in metric units (ha, t, or t/ha); `n_pre` number of nonmissing pre-years; `pct_vs_mean`, `pct_vs_median` = 100 × (observed/baseline − 1); `below_pre_min` is 1/0 when defined; `descriptive_shortfall` = max(0, baseline mean − observed), in metric units; `attributable_to_2018_flood` is the non-attribution marker. |
| `results/district_season_trajectories.csv`: 126 rows, district × season × metric. | `district`, `season`, `metric`; `baseline_mean_2014_2017`, `observed_2018_19`, `observed_2019_20` in metric units; `pct_2018_vs_baseline`, `pct_2019_vs_baseline`, `pct_2018_vs_2017`, `pct_2019_vs_2018` as percentages; `two_observation_shortfall` is the sum of two nonnegative deviations from the fixed pre-year mean, in ha, t or t/ha as dictated by `metric`. This is a descriptive diagnostic, **not** a flood-attributable cumulative recovery deficit; `attributable_to_2018_flood` marks this explicitly. |
| `results/state_season_series.csv`: 54 rows, year × season × metric. | `year`, `season`, `metric`; `observed`, `baseline_mean_2014_2017` in metric units; `pct_vs_baseline` as a percentage. State yield is production sum ÷ area sum, not a mean of district yields. |
| `results/state_annual_comparison.csv`: 6 rows, year. | `year`; `area_ha`, `production_tonnes`, `yield_tonnes_per_ha`; `<metric>_pct_vs_pre_mean` for each of these three metrics. Sums across the three seasons; annual yield = summed production ÷ summed area. |

## Verification and provenance outputs

| File | Meaning and columns |
|---|---|
| `results/annual_report_2018_crosscheck.csv` | 45 district/state × season comparisons. `compendium_area`, `compendium_production`, `annual_report_area`, `annual_report_production` in ha/t; `annual_report_rounded_<metric>` uses half-up integer rounding; `difference_<metric>` = compendium integer minus rounded annual-report value. Raw decimal differences beyond 0.501 also appear in the QA log. |
| `results/annual_report_2019_crosscheck.csv` | 60 district/state × season/All comparisons. `compendium_<metric>`, `annual_report_<metric>` in ha/t, `difference_<metric>` = compendium minus annual report. |
| `results/phase2_annual_comparison.csv` | 84 district × year records. `seasonal_sum_tonnes`, `phase2_annual_tonnes`, `difference_tonnes` = reconstructed minus inherited Phase 2 rice production. |
| `results/data_quality_findings.csv` | Only nonzero or material discrepancies. `check` names the reconciliation, `metric`, `year`, `district`, `season` locate the cell, `calculated`, `reported`, `difference` retain numerical values in metric units, and `source` names the document/page. Difference direction depends on the check and is specified in `experiment_a.py`. |
| `results/summary.json` | Run counts, 2019 reconciliation count, decimal state-sum checks, state post-year series, and non-attribution status. |
| `results/checksums.csv` | SHA-256 and byte length for PDFs, raw transcriptions, data and Experiment A result files. |
| `results/file_manifest.csv` | SHA-256 and byte length of each Phase 3 file other than itself, generated last. |

The two SVG files under `figures/` graph state seasonal production percentages and district autumn production percentages. These are visualizations of the CSV results, not additional observations.
