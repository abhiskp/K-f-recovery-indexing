# Data dictionary

All local CSV files are UTF-8 with header rows. Empty fields denote **unknown/unavailable**, never zero. Literal `NA` in the status table means no estimable result. Boolean fields are `0/1` in CSV or `false/true` in GeoJSON. Longitude/latitude use WGS 84 decimal degrees unless specified. Dates in source labels are preserved as printed; `acquisition_utc` is UTC once provided by Earth Engine.

## `data/processed/official_event_chronology.csv`

Each row is a reported satellite observation/product date, not a statewide flood duration. `observation_date_local` is calendar date in Kerala; `source` and `source_item` identify the publisher/product; `observed_condition` is a qualitative source statement; `sensor_as_reported` is not a verified scene ID; `exact_acquisition_utc_available_in_source` is `no` where time/zone is not reported unambiguously; `source_url` is the primary page/PDF; `interpretation` records chronology/independence caveats. No inundated-area value is imputed.

## `data/processed/bhuvan_kerala_2018_wms_layers.csv`

One row per public Kerala 2018 viewer WMS layer (16 rows). `layer_id` and `viewer_date_label` are literal viewer values. `wms_endpoint` is the service URL. `viewer_zoom_bbox_min_lon`, `viewer_zoom_bbox_min_lat`, `viewer_zoom_bbox_max_lon`, `viewer_zoom_bbox_max_lat` are **viewer zoom extents**, decimal degrees, not source-valid footprints. `viewer_bbox_intersects_pilot` is the rectangle intersection screen (1/0), not a statement that the pilot was observed by a satellite. `single_date_label_id_mismatch` and `hour_label_id_mismatch` are 1 when parsed single-date/hour strings conflict; blank means not comparable, 0 means no detected conflict. `per_pixel_valid_footprint_available` and `validation_role` state access/interpretation.

## `data/processed/bhuvan_pilot_wms_geotiff_metadata.csv`

Three rows, one for each styled WMS GeoTIFF. `file` is project-relative path; `width_px`, `height_px` and `channels` are raster dimensions; `epsg=4326`; bbox fields are the returned rendering extent in degrees; `sha256` and `bytes` identify the exact snapshot; `data_type` explicitly distinguishes styled RGBA from categorical flood labels. Pixel spacing is 0.00048828125° longitude and 0.0005859375° latitude at 512 × 512, **not** sensor resolution. Corresponding PNGs are visual snapshots.

## `results/gfd_2018_event_screen.csv`

One row per GFD/QC event whose `Began` date is in 2018 (32 rows). `dfo_id` is Dartmouth Flood Observatory event ID; `country`, `other_country`, `began`, `ended`, `centroid_lon`, `centroid_lat` are source metadata. `dfo_polygon_bbox_*` are the min/max coordinates parsed from the producer QC geometry; `bbox_intersects_kerala_search_box` is 1/0 for rectangle `[74.8,8.0,77.5,12.8]`. `object_name`, `object_bytes` are the matching public bucket ZIP object and byte size. This is a catalog screen, not a flood/no-flood observation of Kerala.

## `data/processed/kerala_districts_osm_candidate.geojson`

Fourteen district Polygon/MultiPolygon features. `district` is canonical Phase 3 name; `source` is OSM via Open Data Kerala; `source_osm_id` and `source_osm_timestamp` preserve provenance; `boundary_year_2018_verified=false` for every feature. Coordinates are WGS 84 degrees. Geometry is candidate administrative geography and has not been used to calculate flooded hectares.

## `data/processed/nrsc_2018_08_21_06_reported_inundation.csv`

Five district rows transcribed from NRSC's 21 August 2018 06Hr Radarsat-2 report Table 2. `district` is canonical district; `reported_inundated_area_ha` is printed inundated area in hectares; `partial_satellite_coverage_marked=1` preserves source asterisk for Alappuzha and Ernakulam; `observation_local` is the report's local observation label and does not specify UTC; `source_url` is the PDF. These figures omit districts with under 100 ha per report and do not represent statewide flood exposure. The printed total (36,658 ha) is not inserted as a district row; it exceeds the five-row sum by 1 ha, as computed in `results/nrsc_2018_08_21_06_area_check.json`.

## Earth Engine inventory and cleaned scene CSVs

The actual file `data/raw/phase4_kerala_2016_2018_s1_pilot_full_scene_inventory.csv` has one row per 134 Sentinel-1 GRD IW/VV **granules** intersecting the pilot from 2016-06-01 inclusive to 2018-10-15 exclusive. `scene_id` is Earth Engine system index; `acquisition_utc` is UTC timestamp; `platform_number` distinguishes spacecraft; `absolute_orbit`, `relative_orbit`, `pass_direction`, `instrument_mode`, `polarizations`, `resolution_m` are scene metadata. `footprint_fraction_of_aoi` is intersection area / AOI area in [0,1]. `vv_valid_fraction_of_aoi_approx_30m` is mean validity mask sampled at ~30 m over the AOI, [0,1]; `incidence_angle_min_deg_approx`, `_max_deg_approx`, `_mean_deg_approx` are approximate angle statistics at 1000 m. `aoi_id` is constant; `classification=unreviewed_scene` intentionally makes no dry/flood assignment. Earth Engine's system index and `.geo` are retained as provided. The cleaned `data/processed/gee_scene_inventory_cleaned.csv` normalizes and checks these columns. `results/gee_2018_scene_screen.csv` adds Indian local time, chronology class and screening notes for 51 granules.

## `results/gee_2018_acquisition_groups.csv`

One row per 2018 date/platform/pass/relative+absolute orbit (27 rows). `acquisition_date_ist` is the Indian local calendar date; `first_scene_acquisition_utc`/`last_scene_acquisition_utc` and `first_scene_acquisition_ist`/`last_scene_acquisition_ist` are the **start times** of the first and last adjacent granules, not complete acquisition end times. `granule_count` is 1 or 2. `sum_granule_footprint_fractions_not_union` and `sum_granule_valid_fractions_not_union` add the two per-granule AOI fractions; slight overlap can make sums exceed one, and these are **not a mosaic union-coverage estimate**. `valid_fraction_weighted_mean_incidence_angle_deg_approx` is the weighted mean of per-granule approximate angles. `scene_ids_pipe_separated` gives exact Earth Engine IDs; `dry_status` and `event_status` are `unverified`.

## `results/selected_2018_pilot_acquisitions.csv`

Six fixed S1A descending orbit-165 dates drawn deterministically from acquisition groups. `role` distinguishes early/late reference candidates, 16 July chronology check and two separate August event candidates. `first_granule_start_utc`, `last_granule_start_utc` and IST equivalents are start timestamps; `sum_granule_valid_fractions_not_union` has the same non-union caveat as above. `dry_status=unverified` and `independent_pixel_label_status=unavailable` apply to all rows. `selection_note` records the source chronology constraint.

## `results/gee_selected_acquisition_qa_console_transcription.csv`

Six rows of **actual Earth Engine Code Editor console output**, manually transcribed from the executed `acquisitionQA` FeatureCollection before the exact Drive CSV arrived. `date_utc` is the selected acquisition UTC date; `scene_count` counts granules (two per date, not two independent observations); `mosaic_valid_fraction_aoi_approx_30m` is the fraction of the pilot with valid VV in the **mosaic**, sampled at approximately 30 m; `mean_incidence_angle_deg_approx` is the mosaic angle mean sampled at 1000 m. `source` names the console row; `transcription_status` records the subsequent exact-export verification. The original export is now in `data/raw/` and matches the transcription. These QA values do not establish that a reference image was dry or that an event image shows floodwater.

## Original Earth Engine selected-acquisition exports in `data/raw/`

`phase4_s1_2018_pilot_selected_acquisition_qa.csv` has six rows. `system:index` is Earth Engine's row index; `absolute_orbits`, `date_utc`, `scene_count`, `scene_ids`, `dry_status`, `flood_label_status`, `mean_incidence_angle_deg_approx` and `mosaic_valid_fraction_aoi_approx_30m` have the meanings above; `.geo` is an empty Earth Engine geometry. The full scene and orbit IDs match the inventory; numerical values match the console transcription exactly.

`phase4_s1_2018_pilot_exploratory_candidate_bands.tif` is a 45-band Float32, LZW-compressed, 30 m GeoTIFF in EPSG:32643 (921 × 1111 pixels). Bands 1–4 are early/late reference VV dB and mean angle degrees; bands 5–7 are 16 July VV, angle and validity; bands 8–13 are 2014–17 JRC valid/permanent-water-year counts, known/non-permanent flags, slope degrees and slope <5° flag. Bands 14–29 are 9 August VV/angle, event validity, reference overlap, angle differences, strict QA, VV-drop dB and 2/3/4 dB or no-water-exclusion binary candidates. Bands 30–45 repeat those fields for 21 August. Exact band names are in the GeoTIFF and checked by `validate_gee_exports.py`. The raster has **no declared nodata value**; analytic bands have Float NaNs outside data support, while candidate bands encode unsupported areas as 0. Use explicit QA bands and the pilot AOI mask before any count. A 1 is an **unvalidated SAR candidate**; a 0 is not necessarily a confirmed non-flood pixel.

## `results/sar_candidate_pixel_sensitivity.csv` and `sar_band_diagnostics.csv`

Each sensitivity row is one event date, early/late reference pair, water-treatment option and VV-drop threshold. `analysis_support_pixels` counts eligible 30 m pixel centers within the fixed pilot AOI; `analysis_support_fraction_of_pilot` divides by 1,011,610 pilot centers. `candidate_pixels` counts mask=1 within support; `candidate_fraction_of_support` uses that variant's support denominator; `candidate_pixel_area_km2_approx` is count × 0.0009 km², not a validated flood area. `reference_dry_status` and `interpretation` carry the evidence caveat. The diagnostics file gives finite-pixel count/fraction and minimum, 5th percentile, median, 95th percentile, maximum for named backscatter/angle bands inside the AOI; units are dB or degrees. `results/gee_export_validation.json` records raster dimensions, CRS, missingness and mask-encoding checks.

## `results/pilot_2017_2018_optical_viirs_feasibility.csv`

Eight monthly observations for June–September of 2017 and 2018 over the same pilot rectangle. `month` is UTC image-composite month (`YYYY-MM`); `l8_scenes` is Landsat 8 C2 L2 scene count; `l8_clear_any_fraction_30m` is the fraction of pilot pixels with at least one Landsat QA_PIXEL observation where fill, dilated cloud, cirrus, cloud, cloud shadow and snow bits 0–5 were all zero (approximately 30 m). `s2_sr_scenes` is Sentinel-2 harmonized Level-2A SR scene count; `s2_sr_clear_any_fraction_20m` uses SCL classes 4 vegetation, 5 bare soils or 6 water (approximately 20 m). `s2_toa_scenes` is Sentinel-2 harmonized Level-1C TOA count; `s2_toa_qa60_noncloud_any_fraction_60m` is the fraction with at least one scene where QA60 opaque cloud and cirrus bits are both zero (approximately 60 m), **without cloud-shadow screening**. All fractions are [0,1] and are observational availability, not vegetation index values. `viirs_monthly_images` is monthly VCMSLCFG composite count; `viirs_mean_cf_cvg_500m` is the pilot mean number of cloud-free DNB observations per pixel; `viirs_mean_avg_rad_nW_sr_cm2_500m` is mean radiance in nW/sr/cm² at approximately 500 m. Means include mixed lake/rural/settlement pixels and are not economic outcomes. Zero scenes and zero fractions are observed zero availability, unlike `NA` missing-evidence status.

## Results/status files

`results/source_screen_summary.json` contains executed source counts, screening bbox and interpretation. `results/earth_engine_inventory_task.json` records the live query/task status. `results/gee_inventory_review_summary.json` records the 134/51/27 inventory counts; it selects no scene as dry. `results/domain_feasibility_summary.json` verifies and summarizes the eight availability rows. `results/exploratory_and_heldout_status.csv` has one analysis line with status, numerical result if any, and missing-evidence reason. `results/checksums.csv` contains project-relative `file`, `bytes`, `sha256` for all other Phase 4 files. No rank, mask-accuracy or recovery-effect CSV exists because none was estimated.
