# Codex brief — Kerala flood recovery paper, empirical Phase 2

## Context
We are developing **Beyond Flood Risk: Does Post-Flood Recovery Change Priority Rankings in Kerala?** The repository starts from `Kerala_Flood_Recovery_Research_Bundle.zip`. Read `kerala_recovery_investigation/README.md`, `experiment.py`, `robustness.py`, `gee_recovery_proxies_UNEXECUTED.js`, and the manuscript v0.2 before changing anything.

Previous output (district rice/banana/plantain production, 2017–18 through 2020–21, and 2026 published vulnerability ranks) is **exploratory only**. It is neither flood-attributable recovery measurement nor leak-free predictive validation. Preserve the original data, scripts, outputs and provenance.

## Objective
Build the **first actual observed-recovery panel** for the 2018 Kerala flood, with spatially measured flood exposure and season-adjusted multi-year recovery observations. Start with a feasible pilot at the finest consistent geographical unit (agricultural block where historical boundaries/data permit; otherwise district or reproducible fixed grid) before scaling state-wide.

## Prioritized tasks
1. **Audit inputs and temporal validity.** Reproduce existing scripts and their published summary. Check 168 transcribed crop observations against original Ecostat PDF tables, including crop definitions, tables, page references and district naming. Identify available agricultural statistics for at least three pre-flood years if possible. Do not silently substitute missing values. Verify any intended hazard/risk baseline existed at the time of the decision: the published 2026 ranking cannot be described as a prediction made in 2018.
2. **Geographic and flood-event layer.** Acquire usable administrative boundaries with dates/provenance. Audit KSDMA's historical 2018 flood footprints or depth observations and accessible independent reference layers. Implement Sentinel-1 2018 event inundation mapping using orbit/polarization-matched pre/post composites, a permanent-water mask, appropriate terrain and layover handling, and coverage/quality masks. Validate against independent observations, and report spatial uncertainty; do NOT treat a modeled long-return-period hazard raster as an observed 2018 flood footprint.
3. **Agricultural / ecological recovery time series.** Extract Landsat 8/9 and Sentinel-2 time series with QA/cloud masks for multiple years before and after 2018, ideally through 2023/24, including valid-observation counts. Harmonize acquisition seasons. Measure NDVI/EVI/NDMI/land-cover or cultivated extent as *proxies*, not literal income, yields or full ecological restoration. Establish expected seasonal trajectories using pre-flood data and comparable less-affected control areas. Cross-check changes against independently observed crop areas and yields wherever accessible.
4. **Second recovery domain feasibility.** Test monthly VIIRS nighttime lights with stray-light and valid-coverage diagnostics as an *economic-activity proxy*. Confirm signal above noise before using it; otherwise report exclusion. Search and log verified options for independent infrastructure/housing/service restoration dates. Do not claim to have measured recovery in a domain without functional observations.
5. **Quantify observed recovery carefully.** For each event/unit/domain estimate observed versus expected function, a nonnegative deficit and cumulative deficit over predeclared windows (e.g. 6, 12 and 24 months). Record nonrecovery/censoring, repeated shocks (2019/2021 floods), baseline uncertainty, and missingness; do not infer 'time to full recovery' from only one post-event observation.
6. **Ranking comparison and validation.** Compare hazard-only, established risk/vulnerability, single-domain recovery-informed and multidomain recovery-informed rankings. Prespecify scaling and plausible weight families; report Spearman/Kendall correlations, top-10% turnover, rank displacement, data coverage and bootstrap uncertainty. Keep retrospective descriptive comparisons separate from prospective holdout tests. Only claim added predictive value when evaluation uses future, unseen recovery outcomes and no future observations have entered the predictors, weights or baseline.
7. **Deliverables.** Version-controlled, documented scripts and environment; reproducible raw-to-analysis data lineage; intermediate QA maps and tables; `data_availability_and_gaps.md`; `methods_and_limitations.md`; summary figures with truthful captions; a factual `results_phase2.md` reporting findings and failed tests; and updated manuscript *only* for completed experiments. Clearly tag unsupported/unfinished claims.

## Computational access
Use public data and available local/Google Earth Engine access. If GEE authentication, quota, export permissions or other datasets block execution, stop that dependent stage, give precise setup steps, and produce tested local/mock-independent preprocessing components. Never invent outputs, substitute synthetic values for observations, commit secrets, or describe unexecuted JavaScript as an experiment.

## Quality gates
- Document satellite acquisition dates, sensor and projection/resolution, no-data coverage and validation provenance.
- Retain spatially independent units in splits; distinguish flooded from merely adjacent areas.
- Never use 2026 publication scores as a temporally honest 2018 forecast.
- No circular validation using the same flood map as training labels and independent ground truth.
- Do not force positive rank changes or optimise weights on the evaluation outcome.
- Present an explicit GO / NO-GO recommendation on whether empirical evidence supports an expanded recovery-priority index paper.

## First milestone / stop point
Before building a complete ranking index, deliver a **2018 event-exposure raster + a seasonally matched recovery panel for a small documented pilot area, with missingness and QA**, and a table of functional data that can/cannot validate the remote-sensing proxies. This verifies whether the research is feasible.
