# Independent-label validation protocol (not executed)

**Gate:** The underlying 21 August 2018 06Hr RADARSAT-2 GIS-ready inundation layer, its valid acquisition footprint, exact time, class key and permission must be received and checked before any confusion, area or rice-exposure calculation. The 11–21 August duration GIS product is supplementary hazard severity and shares its 21 August sensor/source with the single-date layer; it is not an independent replicate or recovery measure.

## 1. Freeze sources and target before viewing labels

Archive input files with SHA-256 and licence. Record original scene IDs, local/UTC start and end, product issue date, CRS, pixel size, classification algorithm, ground checks, and known positional and thematic limits. Use the Phase 4 frozen 9 and 21 August S1A descending orbit-165 candidates, threshold 3 dB primary and 2/4 dB sensitivity, early and late reference-pair variants, original strict water/slope mask and declared no-water-exclusion sensitivity. Do not fit thresholds on held-out labels. Version any correction separately; preserve original bands and provenance.

The NRSC 21 August product is labelled 06Hr, and Phase 4 S1A starts about 06:10 IST. The NRSC source has not supplied exact UTC, pass duration or coverage; therefore no exact temporal match is yet established. Analyze 9 and 21 August as separate targets. An 11–21 August duration class cannot directly validate a single 9 August snapshot.

## 2. Spatial and temporal alignment

Validate source geometry, CRS, class values and footprint; reproject classes with **nearest neighbor** only. Work at the coarser native resolution or predeclared common grid, not an apparent 30 m resampling of coarser evidence. Intersect: pilot/study boundary, the specific pre/event S1 valid footprints, RADARSAT valid surveyed footprint, and any quality exclusions. Distinguish genuine surveyed non-flood (`0`) from unknown/not observed. Log dropped cells at every intersection. Check scene-time separation in hours, water-level change, rainfall and flood recession between passes; if large or unknown, call comparison temporally mismatched and withhold accuracy claims.

Assess at least 0, 1 and 2 source-pixel positional buffers/erosions around label edges or use a buffer grounded in supplier geolocation accuracy. Report results with and without permanent and seasonal JRC strata. Water under vegetation, buildings and steep terrain may be missed by either radar. Avoid treating a cartographic PDF color or styled WMS transparency as a negative label.

## 3. Sampling and estimates

Sample positive and *independently surveyed negative* locations within valid overlap, retaining spatial blocks (e.g., catchment or contiguous ~5 km tiles) and land-cover strata. Do not sample negatives from outside the RADARSAT acquisition or from unmapped areas. Report TP, FP, FN, TN and coverage: evaluated km², fraction of valid SAR/paddy footprint, and class-wise unknown area. Compute precision, recall, F1, IoU, balanced accuracy and prevalence, with undefined values explicitly NA where denominators are zero. Present confusion counts and metrics for each event date and mask variant, with the selected primary variant first.

Use spatial block bootstrap or leave-one-block-out confidence intervals; random pixel bootstraps understate spatial dependence. Hold out contiguous blocks or a genuinely separate event, with no threshold choice informed by that holdout. Vary positional buffer, matched-orbit/reference choice, JRC missing/permanent-water treatment, thresholds, and comparator sampling. Report any shared interpretation lineage: the 21 August RADARSAT product is a different sensor from Sentinel-1 but may share analyst processing rules; the 11–21 duration map contains the same 21 August RADARSAT acquisition, so two products are not statistically independent. Phase 4's 9 August and 21 August 18Hr NRSC maps include Sentinel-1 and are not primary independent labels for our Sentinel-1 candidates.

KSDMA crowd depth points, if supplied, can corroborate positives only after coordinate, event-time, depth and uncertainty review. A convenience sample of positive reports cannot estimate statewide specificity, false-positive rate or precision without known sampling frame and negatives. Distinguish submission time from flood observation time.

## 4. Exposure and outcome gate

Only after a credible event layer passes validation: intersect its valid footprint with a **dated 2018 cultivated paddy/rice area** (not just present-day wetland), historical district/block boundaries, and source-native resolution. For each unit, report observed paddy area, flood-affected paddy area, missing paddy coverage, fractional exposure and uncertainty from label errors, geolocation and crop classification. If the event layer covers only parts of districts, do not call uncovered rice unexposed.

Then connect unit exposure to the Phase 3 official autumn/winter/summer rice panel, retaining harvested area (ha), production (tonnes) and yield (tonnes/ha) as separate outcomes. Match the event to planting/harvest timing. Compare with less-exposed *within-valid-footprint* units and pre-event seasonal baselines; assess pre-trends, monsoon rainfall, later 2019 floods, aid/replanting and administrative changes. Quantify absolute and relative changes with uncertainty. Descriptive association is not flood attribution unless the counterfactual design and diagnostics support it. Ecological and VIIRS tracks need their own observation-quality and control checks.

**Current implementation:** no label files or validated exposure join are local, so all numerical validation and recovery steps are deliberately unexecuted and NA. `decision_gate.md` states the exact evidence needed to reopen this protocol.
