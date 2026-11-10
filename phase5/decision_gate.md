# Phase 5 decision gate — 9 November 2026

**Status: NO-GO for independently supported flood exposure linked to measured recovery.**

Executed work establishes source access routes and a reproducible audit of reference-pair instability and actual 2014–17 JRC annual water-history classes. The downloaded raster is on the exact Phase 4 grid; its 370-cell AOI denominator difference is confined to source-masked cells. It does not establish a validated flood mask, flood-duration raster, exposed rice area, causal recovery trajectory or ranking benefit. No ranking experiment was run in Phase 5.

## Conditions before flood-mask validation

1. Obtain the **actual** NRSC/KSDMA 21 August 06Hr RADARSAT-2 inundation raster/vector and valid surveyed footprint, exact sensor time/ID, class dictionary (including surveyed non-flood versus unknown), spatial/thematic QA and research-use licence. The report's statement of transmission does not satisfy possession or permission.
2. Verify reference states on 10/22 June and 4 July with independent dated pilot flood/rain/river evidence. If no scene is demonstrably dry, use a declared alternative design or bound the uncertainty; never relabel an unverified scene dry.
3. **Completed:** the four-band JRC annual-class GeoTIFF is local and matches the Phase 4 grid. The 370-cell EE-versus-Rasterio difference lies wholly in local code-255 source-masked cells. Retain separate denominators and 0/255 as unknown, 1 not-water, 2 seasonal, 3 permanent; read raw values because the fourth band is misinterpreted as alpha by GDAL.
4. Freeze target times, footprints, label dependence and SAR rules as in `validation_protocol.md`; then compute spatially blocked confusion and coverage with true surveyed negatives. A single positive-point layer cannot estimate precision.

## Conditions before agricultural exposure/recovery

5. Obtain a dated, georeferenced **2018 cultivated rice/paddy-by-season** layer and 2018-valid district/block boundaries, with source QA/licence. Present-day wetland or OSM boundaries are insufficient.
6. Intersect credible flood exposure and rice area only within the mutually valid footprint. Report exposed rice hectares and fraction, missing coverage and spatial uncertainty by unit.
7. Only then connect to Phase 3 district-season area/production/yield and additional later years if harmonized. Check planting/harvest timing, rainfall, 2019 floods, aid/replanting, trends and control comparability. Report descriptive association separately from causal attribution.

## Minimum researcher intervention

- Send the drafted requests in `DATA_REQUESTS.md` through your institution to KSDMA/NRSC and KSLUB/KSREC (and boundary/gauge custodians if available). Provide any licensed resulting data files plus their permission/metadata sheets; do not send private identifiers or credentials in chat.

The 21 August duration product may later characterize **event hazard severity** after its class/footprint algorithm is checked. Its 0–3, 4–6, 7–9, >10 day classes are not post-flood recovery durations. The success gate remains an independently checked spatial exposure linked to an observed outcome with transparent denominators and uncertainty.
