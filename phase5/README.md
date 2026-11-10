# Phase 5: independent-source access and reference-quality gate

This folder extends the Kerala flood-recovery project using the Phase 4 audit as a hard methodological gate. Phases 2–4 are unchanged. Phase 5 is **not** a validated flood map, recovery analysis, priority index or paper conclusion.

## What was executed on 8–9 November 2026

- Screened the underlying 21 August 06Hr RADARSAT-2 flood GIS lead, NRSC duration Map ID 2018/14, KSDMA depth points, 2018 paddy-area and historical-boundary routes. [Access register](data/processed/source_access_status.csv) distinguishes public PDF/viewer evidence from files actually held. [Data-request drafts](DATA_REQUESTS.md) are ready for the custodians; none were sent.
- Reviewed independent official June/July rainfall and dated flood context for 10/22 June and 4 July reference candidates. All remain **unverified dry**; see [reference QA](reference_qa.md).
- Reanalyzed the original Phase 4 45-band GeoTIFF without changing it. The JRC water-count bands are missing for **642,020 of 1,011,610** pilot pixel centers (63.47%). Early versus late reference-pair 3 dB candidate Jaccard is **0.647** (9 August) and **0.764** (21 August) on the common strict support; these are unvalidated classification-disagreement measures. Full counts are in [results](results/).
- Executed an authenticated Earth Engine query of 2014–17 JRC `waterClass` 0/1/2/3. Its four-band GeoTIFF export **completed** in task `GIHCX7SEC7VIJ4XHL6IRMAOQ`; the researcher placed the file in `data/raw/` on 9 November. Exact local class counts and a conservative water-history state raster are now in `results/` and `data/processed/`. The annual codes 0–3 match the independent Earth Engine console counts exactly. The local pilot mask includes **370 more cells**, all source-masked code 255; denominators remain explicit. All 369,590 finite Phase 4 water-history count cells agree with the annual raster.
- Identified a GeoTIFF display trap: software reads the fourth Byte band (2017 `waterClass`) as alpha; its 65 code-0 pilot cells can falsely mask bands 1–3. The audit reads raw band values and checks this condition. The [annual-class QA figure](figures/phase5_jrc_annual_classes.png) shows source no-data, not-water, seasonal, permanent and source-masked classes separately.
- Created the [support/reference QA figure](figures/phase5_support_reference_qa.png), scripts, [validation protocol](validation_protocol.md), [methods/limitations](methods_and_limitations.md), [results](results_phase5.md), [decision gate](decision_gate.md), data dictionary and reproduction commands.

## Scientific status

**NO-GO:** no independent licensed geospatial flood labels or valid surveyed footprint; no verified 2018 cultivated-rice map; no spatial exposure/outcome join. No confusion metrics, affected rice area, flood-attributable recovery, recovery duration or rank benefit is reported. The NRSC duration classes describe **within-event inundation duration**, not return to pre-flood functioning.

Start with `results_phase5.md`, `reference_qa.md` and `decision_gate.md`. To reproduce the completed computations, use `REPRODUCE.md`. The JRC download is complete. The remaining researcher action is to send the unsent source requests through an appropriate institutional route and provide any licensed GIS files with metadata; no credentials or tokens are needed.
