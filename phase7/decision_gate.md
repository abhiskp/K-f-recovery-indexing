# Phase 7 evidence gate

| Gate | Decision | Evidence / condition |
|---|---|---|
| Independently observed 2018 flood exposure | **NO-GO for validated spatial extent** | NRSC describes a RADARSAT-2 layer, but its GIS classes and observed/nonobserved footprint are not in the project. Phase 4 Sentinel-1 candidates and Phase 6 Tiwari Sentinel-1 positives are sensor-dependent and have no valid negative footprint. |
| Post-flood agricultural measurements | **YES, descriptive district-season rice outcomes** | 462 district × season × year cells, 2014–15 through 2024–25; published area and rice production. Wet-only yield is computable only from 2020–21 onward; the older production/area ratio has unverified component scope. Repeated district totals do not observe the same flooded fields or establish recovery duration. |
| Contemporaneous cultivated-paddy geography | **NO-GO** | No dated 2018 season-specific parcels or validated raster and unknown mask. DES district/block totals cannot be used as pixel-level paddy geometry. |
| 2018-valid boundaries/crosswalk | **NO-GO** | No verified historical GIS unit polygons, effective dates and stable DES crosswalk. |
| Geographic exposure–outcome link | **NO-GO** | Required flood class+footprint, paddy geography and historical unit alignment are jointly absent. No exposure-overlap pilot was run. |
| Flood-associated recovery model | **NO-GO** | No credible exposed versus less-exposed paddy panel, independent validation or support for an attributable trajectory. |
| Recovery index / ranking benefit | **NO-GO, out of Phase 7 scope** | A measured and valid exposure-linked recovery dimension, later held-out outcomes and ranking comparator are absent. |

## Minimum outside action

The researcher should send the prepared [RADARSAT](requests/radarsat_inundation.txt) and [paddy/boundary](requests/paddy_and_boundaries.txt) requests to the relevant custodians and preserve their replies, files, metadata and reuse terms. The [depth-point request](requests/depth_points.txt) is optional supplementary evidence. Do not share credentials. If the geospatial layers arrive, first check acquisition date, actual observed support, CRS, class semantics and independence; only then run an overlap/validation pilot with valid denominators. Restricted source files must not be committed to a public repository without permission.

## Rigorous alternative scope if access stays blocked

A defensible paper could study **seasonal heterogeneity and measurement limits in district-level Kerala rice statistics around the 2018 floods**: publish the source-checked 2014–15 to 2024–25 panel, descriptive administrative-category contrasts, pre-event trend/placebo and baseline sensitivity, later shock flags and an explicit audit of why public flood maps cannot validate exposure. It would not claim flood-attributable recovery, a recovery duration, a recovery index or improved prioritisation. Further scientific value depends on clearly separating rice-output changes from physical inundation and later events.
