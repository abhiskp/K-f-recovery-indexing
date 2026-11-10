#!/usr/bin/env python3
"""Technical QA and descriptive candidate counts for unvalidated S1 exports.

No row or pixel is interpreted as independently verified flood exposure.
All raster counts use 30 m pixel centers inside the fixed lon/lat pilot AOI.
"""
import csv
import json
import math
from pathlib import Path

import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.warp import transform_geom

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
QA_CSV = RAW / "phase4_s1_2018_pilot_selected_acquisition_qa.csv"
TIF = RAW / "phase4_s1_2018_pilot_exploratory_candidate_bands.tif"
SELECTED = ROOT / "results/selected_2018_pilot_acquisitions.csv"
CONSOLE = ROOT / "results/gee_selected_acquisition_qa_console_transcription.csv"
OUT_JSON = ROOT / "results/gee_export_validation.json"
OUT_CANDIDATES = ROOT / "results/sar_candidate_pixel_sensitivity.csv"
OUT_BANDS = ROOT / "results/sar_band_diagnostics.csv"
PIXEL_AREA_KM2 = 30 * 30 / 1_000_000

def rows(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))

def write_csv(path, values):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(values[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(values)

source = rows(QA_CSV)
selected = {r["acquisition_date_ist"]: r for r in rows(SELECTED)}
console = {r["date_utc"]: r for r in rows(CONSOLE)}
assert len(source) == len(selected) == len(console) == 6
assert {r["date_utc"] for r in source} == set(selected)
for row in source:
    d = row["date_utc"]
    assert row["dry_status"] == "unverified"
    assert row["flood_label_status"] == "unvalidated"
    assert int(row["scene_count"]) == 2
    assert row["scene_ids"] == selected[d]["scene_ids_pipe_separated"]
    assert row["absolute_orbits"] == selected[d]["absolute_orbit"]
    for key in ("mosaic_valid_fraction_aoi_approx_30m",
                "mean_incidence_angle_deg_approx"):
        assert math.isclose(float(row[key]), float(console[d][key]),
                            rel_tol=0, abs_tol=1e-12), (d, key)

poly = {"type":"Polygon", "coordinates":[
    [[76.35,9.45],[76.60,9.45],[76.60,9.75],[76.35,9.75],[76.35,9.45]]
]}
candidate_rows = []
band_rows = []
overlap_counts = {}
with rasterio.open(TIF) as raster:
    assert raster.crs.to_epsg() == 32643
    assert raster.width == 921 and raster.height == 1111
    assert raster.res == (30.0, 30.0)
    assert raster.count == 45
    assert set(raster.dtypes) == {"float32"}
    assert len(set(raster.descriptions)) == raster.count
    projected = transform_geom("EPSG:4326", raster.crs.to_string(), poly)
    inside = geometry_mask([projected], out_shape=(raster.height,raster.width),
                           transform=raster.transform, invert=True)
    aoi_pixels = int(inside.sum())
    assert aoi_pixels > 0
    band_index = {name:i for i,name in enumerate(raster.descriptions,1)}
    def read(name):
        return raster.read(band_index[name])
    def count_true(values):
        return int(np.count_nonzero(inside & np.isfinite(values) & (values == 1)))
    def count_finite(values):
        return int(np.count_nonzero(inside & np.isfinite(values)))
    water_valid = read("water_valid_years_2014_17")
    water_known = read("water_history_known")
    slope_low = read("slope_below_5deg")
    water_history_finite_pixels = count_finite(water_valid)
    water_history_known_pixels = count_true(water_known)
    low_slope_pixels = count_true(slope_low)
    assert water_history_known_pixels <= water_history_finite_pixels
    diagnostics = [
        "pre_early_vv_db","pre_late_vv_db","jul16_vv_db",
        "aug09_vv_db","aug21_vv_db",
        "pre_early_angle_deg","pre_late_angle_deg",
        "aug09_angle_deg","aug21_angle_deg",
        "aug09_early_drop_db","aug21_early_drop_db",
        "aug09_early_angle_diff_deg","aug21_early_angle_diff_deg",
    ]
    for name in diagnostics:
        array = read(name)
        values = array[inside & np.isfinite(array)]
        band_rows.append({
            "band":name,"finite_aoi_pixels":len(values),
            "finite_fraction_of_aoi":len(values)/aoi_pixels,
            "minimum":float(values.min()),"p05":float(np.percentile(values,5)),
            "median":float(np.median(values)),
            "p95":float(np.percentile(values,95)),
            "maximum":float(values.max()),
            "units":"degrees" if "angle" in name else "dB",
        })
    for event in ("aug09","aug21"):
        valid = read(event+"_valid")
        event_valid_pixels = count_true(valid)
        for baseline in ("early","late"):
            overlap = read(event+"_"+baseline+"_overlap")
            strict = read(event+"_"+baseline+"_strict_qa")
            overlap_pixels = count_true(overlap)
            overlap_counts[event+"_"+baseline] = overlap_pixels
            support_pixels = count_true(strict)
            assert support_pixels <= overlap_pixels <= event_valid_pixels
            for threshold in ((2,3,4) if baseline=="early" else (3,)):
                name = f"{event}_{baseline}_candidate_{threshold}db"
                mask = read(name)
                assert np.all(np.isin(mask[inside],(0,1)))
                assert not np.any((mask==1) & inside & ~(strict==1))
                count = count_true(mask)
                candidate_rows.append({
                    "event_date": "2018-08-09" if event=="aug09" else "2018-08-21",
                    "reference_acquisitions":(
                        "2018-06-10|2018-06-22" if baseline=="early"
                        else "2018-06-22|2018-07-04"),
                    "reference_dry_status":"unverified",
                    "water_treatment":"exclude_permanent_with_3_of_4_year_history",
                    "vv_drop_threshold_db":threshold,
                    "event_vv_ceiling_db":-15,
                    "analysis_support_pixels":support_pixels,
                    "analysis_support_fraction_of_pilot":support_pixels/aoi_pixels,
                    "candidate_pixels":count,
                    "candidate_fraction_of_support":count/support_pixels,
                    "candidate_pixel_area_km2_approx":count*PIXEL_AREA_KM2,
                    "interpretation":"unvalidated SAR candidate, not flood extent",
                })
        # The no-water variant still requires valid pre/event overlap and low slope.
        no_water = read(event+"_early_candidate_3db_no_water_exclusion")
        early_overlap = read(event+"_early_overlap")
        no_water_support = inside & (early_overlap==1) & (slope_low==1)
        assert not np.any((no_water==1) & inside & ~no_water_support)
        count = count_true(no_water)
        support = int(np.count_nonzero(no_water_support))
        candidate_rows.append({
            "event_date":"2018-08-09" if event=="aug09" else "2018-08-21",
            "reference_acquisitions":"2018-06-10|2018-06-22",
            "reference_dry_status":"unverified",
            "water_treatment":"no_permanent_water_exclusion",
            "vv_drop_threshold_db":3,
            "event_vv_ceiling_db":-15,
            "analysis_support_pixels":support,
            "analysis_support_fraction_of_pilot":support/aoi_pixels,
            "candidate_pixels":count,
            "candidate_fraction_of_support":count/support,
            "candidate_pixel_area_km2_approx":count*PIXEL_AREA_KM2,
            "interpretation":"unvalidated SAR candidate, not flood extent",
        })
    for event in ("aug09","aug21"):
        c2=read(event+"_early_candidate_2db")
        c3=read(event+"_early_candidate_3db")
        c4=read(event+"_early_candidate_4db")
        assert np.all(c4[inside] <= c3[inside])
        assert np.all(c3[inside] <= c2[inside])
    summary = {
        "source_qa_csv_rows":len(source),
        "qa_csv_exactly_matches_console_transcription":True,
        "raster_width":raster.width,"raster_height":raster.height,
        "raster_band_count":raster.count,
        "crs":str(raster.crs),"pixel_size_m":30,
        "raster_has_explicit_nodata":raster.nodata is not None,
        "raster_band_masks_all_valid_even_where_float_nan":bool(
            np.all(raster.read_masks(1)==255)
            and np.isnan(read("pre_early_vv_db")).any()),
        "pilot_aoi_pixel_centers":aoi_pixels,
        "pilot_aoi_pixel_area_km2_approx":aoi_pixels*PIXEL_AREA_KM2,
        "water_history_finite_pixels":water_history_finite_pixels,
        "water_history_finite_fraction":water_history_finite_pixels/aoi_pixels,
        "water_history_known_pixels":water_history_known_pixels,
        "water_history_known_fraction":water_history_known_pixels/aoi_pixels,
        "low_slope_pixels":low_slope_pixels,
        "low_slope_fraction":low_slope_pixels/aoi_pixels,
        "pre_event_overlap_pixels":overlap_counts,
        "independent_flood_label_comparison":"not available",
        "candidate_area_interpretation":"Classified pixel counts only, not validated inundated hectares.",
    }
write_csv(OUT_CANDIDATES,candidate_rows)
write_csv(OUT_BANDS,band_rows)
OUT_JSON.write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
