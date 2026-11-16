# Phase 7 data dictionary

## Conventions and geography

`district` identifies one of Kerala's 14 districts, spelling-normalised to the Phase 3/6 panel; it is **not** a GIS boundary. `year` is the DES agricultural year, e.g. `2018-19`; `season` is the report's harvest-season label `Autumn`, `Winter` or `Summer`. Seasonal cell dates are not supplied at field level. Area is published seasonal paddy area in **hectares** (explicitly wet paddy from 2019–20 onward). Production is published rice in **metric tonnes** (explicitly total wet+dry rice from 2020–21 onward). The older compendium does not state wet/dry component scope on its table, so cross-format comparability is flagged. `yield_tonnes_per_ha` is wet rice divided by wet-paddy area **only from 2020–21 onward**; the Phase 3 ratio is retained in a separate legacy field and is not analysed as validated yield. Blank numeric cells mean unavailable or mathematically undefined, **never zero**. `reported_zero` is an explicit source zero.

## `data/processed/district_season_rice_2014_2025.csv`

One row per district × harvest season × agricultural year; **462 rows**, 2014–15 through 2024–25. First 252 rows reproduce the read-only Phase 3 panel; next 210 rows are Phase 7 extraction. No geometry or exposure fraction is present.

| Column(s) | Definition |
|---|---|
| `district`, `year`, `season` | Unique key and reporting period/geography as above. |
| `area_ha`, `production_tonnes` | DES published seasonal paddy area (ha) and rice output (t). From 2019–20 area is explicitly wet paddy; from 2020–21 production is explicitly wet+dry total rice. Zero is observed zero. |
| `yield_tonnes_per_ha` | For 2020–21 onward only, `wet_rice_production_tonnes / area_ha`; blank for earlier source-scope uncertainty and zero area. Valid only as a within-period wet-paddy yield proxy, not a longitudinal pre-2018 recovery measure. |
| `wet_rice_production_tonnes`, `dry_rice_production_tonnes` | Component rice output (t), available 2020–21 onward; blank in older unsplit reports. Their sum is `production_tonnes` subject to printed rounding. |
| `production_component_status` | `not_reported_in_source` for old rows, `reconciles_within_0.01_t` or `source_printed_mismatch` for 2020–21..2023–24 printed Rice (Total) rows, `derived_sum_of_two_final_estimates` for 2024–25. |
| `legacy_phase3_ratio_tonnes_per_ha` | Original Phase 3 computed production/area ratio for 2014–15..2019–20, retained for audit only. Blank later; do not call it validated wet-paddy yield. |
| `area_scope`, `production_scope`, `yield_status` | Explicit source-component status. Earlier compendium area and Rice components are `unspecified`; 2019–20 area is explicitly wet; 2020–21 onward wet area and wet+dry rice are explicit. Yield status identifies valid wet-only calculation, zero-area undefined, or legacy mismatch. |
| `area_status`, `production_status` | `observed` or `reported_zero`; no source-missing area/production rows were created. |
| `crop_definition` | Composite source-scope code: older published seasonal paddy/rice with unspecified component, or explicit newer wet-paddy area and all-rice production. |
| `area_source_pdf`, `production_source_pdf` | Source PDF filename or original URL basename for Phase 3 rows. |
| `area_source_table`, `production_source_table` | Printed table title/number, including Phase 3 compendium Tables 17/41 and its audited annual-report corrections. |
| `area_source_printed_page`, `production_source_printed_page` | Page number printed in the report; `unpaginated` for 2024–25 final estimates. |
| `area_source_pdf_page`, `production_source_pdf_page` | One-based PDF page for every source, including page mappings taken from Phase 3's audited source register. |
| `area_source_url`, `production_source_url` | Official Kerala DES PDF URLs. |
| `source_decision` | Phase 3 source-decision code, `contemporaneous_DES_annual_report`, or `final_DES_seasonal_estimate` (with `_visual_transcription` for 2024–25 summer). |

## Raw source and provenance files

`data/raw/kerala_des_{622,664,1720,1822,1824,1844}.pdf` are official Kerala DES publications. Same-name `.txt` files are `pdftotext -layout` derivatives; `1844.txt` is empty because that PDF is scanned. `kerala_des_1844_page-{1,2}.png` are visual verification renders. `kerala_des_1844_summer_{wet,dry}_transcription.csv` each has `district` (14 plus `STATE`), `area_ha` (ha), `production_tonnes` (t), one-based `source_pdf_page` and `transcription_note`; the `STATE` row is a source control, not a fifteenth district. `Phase6_Independent_Audit_2026-11-11.md` is the researcher-supplied read-only audit copied from Downloads.

## Descriptive results

| File | Row unit and columns |
|---|---|
| `results/state_total_reconciliation.csv` | 30 year × season × `metric` (`area_ha`, `production_tonnes`) rows for 2020–21..2024–25. `unit`, `district_sum`, `printed_state_total`, `difference_district_minus_state` are source-unit numbers; for 2024–25 total rice, the control is the **sum of two printed wet/dry state rows**, indicated by `state_control_basis`. `source_pdf`, `source_printed_page`, `source_pdf_page` locate the control; `+` joins wet/dry page numbers. `-0.000` is floating formatting, numerically zero. |
| `results/rice_component_reconciliation.csv` | 210 new district × season × year cells. `printed_or_derived_total_rice_tonnes`, `wet_rice_tonnes`, `dry_rice_tonnes`, `difference_total_minus_components_tonnes` preserve the component arithmetic in tonnes; `component_status` marks source mismatch or derived sum; `source_pdf`/`source_pdf_page` locate the row. |
| `results/state_season_trajectory.csv` | 33 agricultural year × season rows, 2014–15..2024–25. `district_rows`=14; `published_seasonal_paddy_area_ha` (earlier compendium component uncertain) and `published_or_total_rice_production_tonnes` (earlier Rice component unsplit) are **separate** district sums; no cross-scope yield is calculated. `interpretation` prevents causal use. |
| `results/pre2018_trend_diagnostics.csv` | 84 district × season × `metric` rows for area/production only. `pre_years`=2014–15..2017–18; `n_observed`=0–4; `ols_slope_per_agricultural_year` is the straight-line four-point slope in source units per agricultural year; `pre_mean` likewise; `pre_cv` is population standard deviation divided by mean; blanks indicate insufficient observations or zero mean. `interpretation` labels the diagnostic. |
| `results/baseline_sensitivity_2018_19.csv` | 336 district × season × area/production `metric` × `baseline_method` rows. `notification_status` is administrative flood/landslide category; `target_year`=2018–19. `baseline_value`, `observed_value`, `absolute_deviation` use the metric's units; `percent_deviation` is `100×(observed/baseline−1)` and blank for nonpositive baseline, with `percent_undefined_reason`. Methods: `pre4_mean`, `pre4_median`, `pre3_mean`, `pre4_linear_extrapolation`. `interpretation` is descriptive. |
| `results/autumn_production_baseline_group_sensitivity.csv` | Four baseline-method group summaries for autumn production. `n_all_defined`, `n_some_defined` count defined district percentages; `all_mean_percent_change`, `some_mean_percent_change` are unweighted means in **percent**; `difference_all_minus_some_pp` is **percentage points**; `all_sum_absolute_deviation_tonnes`, `some_sum_absolute_deviation_tonnes` are sums of district absolute departures in **tonnes**; `interpretation` is descriptive. |
| `results/descriptive_summary.json` | Key row/year counts; independently recomputed Phase 6 contrast means and sample counts; placebo difference in pp; interpretation. No inferential p-value is calculated. |
| `results/later_event_flags.csv` | One record per 2018–19..2024–25 agricultural year. `calendar_event_year` is its starting calendar year; `event_flag` states documented flood/landslide or not systematically classified; `evidence_note` and `source_url` give official evidence. `not_systematically_classified` does **not** mean no flood. |
| `results/checksums.csv` | `path_from_project_root`, SHA-256 digest `sha256`, and `bytes` for Phase 7 files plus four upstream read-only inputs. Manifest excludes itself. |

## Access and nonagricultural matrices

`source_access_matrix.csv` has one row per essential/optional missing input. `input_id` and `priority` identify the request; `custodian`, `source_evidence_url`, `requested_data`, `local_data_status`, `verified_public_substitute`, `missing_metadata_or_fields`, `reuse_permission_status`, `validation_role` and `next_action` document source, licence and gate. No row asserts possession of restricted GIS data.

`nonagricultural_coverage_matrix.csv` has one row per domain/source. `domain`, `verified_public_source`, `observation_period`, `geographic_unit`, `dated_measurement`, `measures_functioning`, `compatible_with_2018_flooded_paddy_geography`, `local_observation_status`, `phase7_assessment` and `source_url` distinguish a dated functional observation from a proxy, damage estimate or missing panel. `partial_state_milestone` in `measures_functioning` refers only to statewide electricity restoration and is not a district recovery series.
