# Phase 6 data dictionary

**Geography/time:** The Phase 4/5 pilot is `[76.35, 9.45, 76.60, 9.75]` WGS84 bounds and a 30 m EPSG:32643 output grid. Phase 3 rice observations are Kerala districts × **harvest** season × July–June agricultural year; Autumn is July–October, Winter November–February, Summer March–June. The 3 October 2018 order is a district/village administrative designation for the 2018 southwest monsoon and includes floods **or** landslides. The Tiwari raster filenames give image dates, but exact UTC scene times are unavailable in S1. IFI v3 event dates are transcribed as published.

**Missing conventions:** Blank CSV cell means missing, unavailable or mathematically undefined, never measured zero. `not_listed` is not a dry/non-flood class. Tiwari GeoTIFF `0` is **NoData/unknown**, `1` is water-positive as supplied; it contains no explicit observed non-water class or surveyed footprint. Sentinel Asia overlay transparency is **unrendered/unknown**. The Phase 4 candidate zeros outside strict QA are not negatives. Group percentages exclude zero-baseline districts; sums of levels retain true zero production/area. `not_established` and `no` are inference flags, not numeric data.

## Source files

| File/group | Columns or bands, units | Time and geography | Missing/coverage |
|---|---|---|---|
| `data/raw/sentinel_asia_eos_alos2_20180812.kmz` | KML three GroundOverlays (WGS84 lat/lon), RGBA PNG rendered colors and legend | Embedded ALOS-2 layers named 11 Aug and 28 Jul 2018; approx. 11.25–12.14° N | Alpha=0 is unknown; no vector, raw class raster, valid footprint or exact UTC |
| `data/raw/tiwari_pone_0237324_s001.7z`, extracted `tiwari_s1/` | Eleven single-band uint8 GeoTIFFs; 1 water-positive, 0 NoData. R script is rainfall plotting code. | Filename dates 2015–2018; six 2018 rasters EPSG:4326, others EPSG:32642; exact grids per `tiwari_s1_raster_inventory.csv` | No observed negative, scene footprint, validation samples or exact acquisition IDs |
| `tiwari_s1/.../kerala_point_flood.csv` | `system:time_start` ISO day; `Edanad`, `Aranmula`, `Chengannur`, `Kureepuzha`, `Pandanad`, `Ranni` daily CHIRPS rainfall values (interpreted mm/day from article/R script) | 3,286 dates 2010-01-01–2018-12-30; six named locations, point coordinates absent from S1 | No class labels; not local gauge validation |
| `data/raw/ifi_india_flood_inventory_v3.csv` | 23 published fields incl. `UEI`, dates, `State`, `Districts`, coordinates, `Area Affected`, casualties and source | 6,876 India event rows 1967–2023; 11 2018 Kerala mentions | Blanks retained; inconsistent dates flagged, no event polygon |
| `data/raw/ifi_district_flooded_area_v3.csv` | `Dist_Name`, `Percent_Flooded_Area`, `Parmanent_Water`, `Corrected_Percent_Flooded_Area`; published percentage-like values | 732 static districts, no event date | Historical/model values, not 2018 area; spelling retained |
| `data/raw/ifi_district_flood_impact_v3.csv` | `Dist_Name`, `Human_fatality`, `Human_injured`, `Population`, `Mean_Flood_Duration` (days as published) | 732 static districts, no event date | Historical/model aggregate, not 2018 recovery |
| `data/raw/kerala_go_flood_notification_2018_20181003.pdf` | Printed village/taluk/district names and counts | 3 Oct 2018 amended official order, 13 districts | No CRS/geometry, inundated area, or functioning metric |

## Processed CSVs and experimental outputs

| File | Columns and meaning |
|---|---|
| `data/processed/official_district_notification_status.csv` | `district`; `notification_status` (`all_villages`, `some_villages`, `not_listed`); `notified_village_count_if_all` (only for full-district rows); source order/URL; text interpretation. Fourteen district rows. |
| `data/processed/notification_rice_join.csv` | 378 rows: `district`, status, `season`, `metric` (`area_ha`, `production_tonnes`, `yield_tonnes_per_ha`), `unit`; `comparison` (2017-18 placebo, 2018-19, 2019-20); baseline years/mean, observed, absolute deviation, percent deviation, `baseline_zero`, attribution marker. Area in ha; production in metric tonnes; yield in tonnes/ha; percentages versus own same-season baseline. |
| `results/notification_rice_contrasts.csv` | 27 season × metric × comparison rows; group sizes, defined-percentage sizes, mean/median percent changes, all-minus-some percentage-point difference, descriptive exact permutation probability, leave-one-district-out min/max in pp, absolute-deviation sums in metric units, baseline/observed group level sums and aggregate percent changes for area/production only. `inundated_rice_area_ha` blank throughout; `flood_effect_established=no`. |
| `data/processed/ifi_2018_kerala_event_screen.csv` | 11 published Kerala-mention records: UEI, start/end, reported duration, calculated inclusive calendar span and mismatch flag, state/district text, number of listed names, latitude/longitude, area/impact fields and source. No coordinate CRS because coordinates are missing for these records. |
| `data/processed/ifi_kerala_historical_district_metrics.csv` | Fourteen name-matched IFI static flooded-area/impact metrics; each row explicitly `not_2018_event_exposure=yes`. Percent and count/day labels are as published; no 2018 interpretation. |
| `results/tiwari_s1_raster_inventory.csv` | Per GeoTIFF name, byte length, SHA-256, CRS, pixel width/height/bounds, band/dtype, nodata, positive/zero counts, and absent-footprint/negative/time flags. Pixel counts are raster cells, **not area**. |
| `results/tiwari_phase4_positive_overlap.csv` | Five published dates resampled onto Phase 4 grid: total grid cells, Tiwari-positive cells, Phase 4 August 21 strict-QA cells, positive/QA intersection, positive/QA/candidate intersection, candidate fraction conditional on Tiwari positive and QA. Not confusion or recall. |
| `results/sentinel_asia_kmz_structure.json`, `results/ifi_source_audit.json`, `results/tiwari_s1_audit.json`, `results/notification_rice_summary.json` | Machine-readable source audit counts, selected results and interpretation flags. |
| `results/raw_file_provenance.csv`, `results/checksums.csv` | Source URLs plus MD5/SHA-256 for downloaded files; full Phase 6 and input-panel SHA-256 manifest. |
| `data/processed/recovery_source_register.csv` | Domain, source, period, unit, observed measurement, local access status, assessment and URL; this is an audit register, not a harmonized measurement panel. |

`data/processed/sentinel_asia_layer0_visual.png` and `sentinel_asia_legend_visual.png` are extracted raw visual overlays. The SVG/PNG figure depicts district rice changes and contains no new observations. For original Phase 3 column-level provenance, see `../phase3/data_dictionary.md` and `../phase3/sources.md`.
