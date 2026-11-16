# Independent audit of Phase 6 — 11 November 2026

## Scope and outcome

Audited the supplied `kerala_flood_recovery_phase6_2026-11-11.zip` offline. Archive: 68 entries, including Phase 6 code/results/sources, the required Phase 3 seasonal rice panel, and the Phase 4 exploratory SAR GeoTIFF. The archive is sufficient to reproduce the Phase 6 saved-file analyses. It does not contain all original annual agricultural publications needed to re-transcribe Phase 3 from scratch.

**Audit verdict: PASS for computational reproducibility and descriptive analysis; NO-GO for exposure-attributed recovery, validated recovery-adjusted rankings, or journal claims of improved prioritisation.**

## Checks performed

1. `python phase6/scripts/checksums.py verify`: **55/55 SHA-256 records verified**.
2. Executed `audit_public_sources.py`, `audit_tiwari_s1.py`, and `notification_rice_screen.py` in an independent copy using a different available Python environment. All generated numeric CSV/JSON data files matched the saved outputs byte-for-byte; existing sources and scripts were preserved.
3. Recomputed from the raw included Phase 3 panel, without using the Phase 6 contrast outputs, all 2018–19 autumn district production baseline deviations and the two-group mean difference. Results:
   - All-village-affected districts with nonzero baseline (n=6): **−65.39108%** average district production deviation.
   - Some-village-affected districts (n=6): **−15.23957%**.
   - All-minus-some contrast: **−50.15151 percentage points**.
   - Exact unadjusted label enumeration: 16/924 = 0.017316. **This is only a descriptive permutation statistic; administrative labels are not random/exchangeable, so it is not a valid causal or design-based significance test.**
4. Checked 378-row output uniqueness: **378/378 unique** district × season × indicator × comparison keys. It is a *long-format transformation* of 252 district × season × year source observations: `14 × 3 × 3 × 3 = 378`. **No duplication error.** Wayanad's baseline-zero autumn production is correctly excluded from percentage calculations; Kasaragod is not treated as an observed dry control.
5. Visually inspected the actual scanned Kerala government order. Page 1 confirms G.O.(P) No. 6/2018/DMD (03 October 2018), amending 1,259 villages by one additional village; page 3 annexure identifies seven districts under `ALL VILLAGES` (Alappuzha, Kottayam, Pathanamthitta, Ernakulam, Thrissur, Wayanad, Idukki). The order classifies **flood OR landslide** affected, not observed rice-field inundation.
6. Reran the Tiwari S1 GeoTIFF audit against the supplied Phase 4 pilot: source positive classes and positive-only intersection counts reproduce. As documented in the package, there is no independent, observed negative or valid scene-footprint layer. The conditional 58.0772% is **same-sensor concordance, not recall, flood-area coverage or a flood map validation score**.

## Key research findings and boundaries

- There is real evidence of **heterogeneous, season-specific rice-output disruption** among district administrative categories. It is not a clean comparison of inundated vs non-inundated paddy fields.
- The 2017–18 pre-event placebo gives a **+19.2580-point** difference under a different baseline window. This warns that the groups already differed and should not be considered parallel counterfactuals.
- The 2018–19 autumn contrast in the package separates into harvested-area difference **+4.3001 points** and yield difference **−51.7996 points**. These descriptive component comparisons are compatible with a larger between-group yield disruption but do not establish its cause.
- Percent change for tiny baseline producers (e.g., Pathanamthitta 69 t and Kozhikode 74.5 t in the included panel) is volatile. Report individual districts and aggregate tonnes alongside unweighted district percentages. Alappuzha and Kottayam are large contributors to the absolute statewide shortfall.
- 2019–20 outcomes are affected by subsequent floods and other conditions, so the change is not a recovery duration for 2018 fields.
- Tiwari's GeoTIFFs share Sentinel-1 as a source with the exploratory pilot; its code `0` denotes NoData in the provided rasters. Pixel overlaps without independent observed negatives/footprints are not sensitivity, specificity, IoU or validated flood area. No reliable contemporaneous paddy-extent map was supplied.
- Other domain audits do **not** provide measured, co-geolocated economic, ecological, social/housing or service-restoration trajectories.

## Interpretation for manuscript

The data are suitable for a **methods / exploratory evidence** section discussing sensitivity of conclusions to seasonal aggregation, exposure proxies and baseline choices. They do not yet justify a flood-attributable recovery outcome, a multidimensional recovery index, retrospective or prospective priority rank improvements, or statistical causal effects. The source-code phrase `predeclared primary` should not be represented as an externally preregistered hypothesis without a dated independent protocol.

## Priority next steps

**Gate 1: Research data access (human/institutional action).** Request an independently observed 2018 NRSC/KSDMA RADARSAT-2 event inundation product **with** surveyed footprint, class dictionary, time/scene metadata, permanent-water treatment, QA and academic licence; the 2018 season-specific paddy map and 2018-valid administrative boundaries with provenance; and if available KSDMA's geocoded flood-depth observation records including dates/QA. See the prepared unsent drafts in `phase6/DATA_REQUESTS.md`. Any restricted data must retain usage terms and should not be committed to public repositories.

**Gate 2: Limited Codex work in parallel.** Harmonise public 2020–21 onward district-season rice data, document other flood years and changing crop calendars, and develop baseline/trend diagnostics only. Do not call post-2018 output changes flood-attributable recovery. Avoid more SAR-threshold tuning or arbitrary index-weight grids until Gate 1 succeeds.

**Gate 3: Conditional experiment.** Only after Gate 1 succeeds, align independently confirmed inundation × 2018 cultivated rice × time-compatible units; produce exposure fractions with valid denominators and uncertainty; then analyse subsequent same-season outcomes with rainfall/flood shocks and comparison units. If those inputs cannot be obtained, consider reframing the manuscript towards seasonal agricultural disruption and measurement limitations rather than claiming a new empirically validated recovery-priority index.
