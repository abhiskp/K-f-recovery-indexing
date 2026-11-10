#!/usr/bin/env python3
"""Audit Phase 4 support and reference sensitivity without calling masks flood.

If the optional four-band Earth Engine JRC export is present, also write annual
class counts and conservative composite-state raster. All counts use pixel
centers in the Phase 4 pilot rectangle; no interpolation or imputation.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.warp import transform_geom

ROOT = Path(__file__).resolve().parents[2]
P5 = ROOT / "phase5"
PHASE4_TIF = ROOT / "phase4/data/raw/phase4_s1_2018_pilot_exploratory_candidate_bands.tif"
JRC_TIF = P5 / "data/raw/phase5_jrc_waterclass_2014_2017_pilot.tif"
OUT = P5 / "results"
PROC = P5 / "data/processed"
OUT.mkdir(parents=True, exist_ok=True)
PROC.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


polygon = {"type": "Polygon", "coordinates": [[
    [76.35, 9.45], [76.60, 9.45], [76.60, 9.75],
    [76.35, 9.75], [76.35, 9.45],
]]}
with rasterio.open(PHASE4_TIF) as ds:
    assert ds.crs.to_epsg() == 32643 and ds.res == (30, 30)
    inside = geometry_mask([transform_geom("EPSG:4326", ds.crs.to_string(), polygon)],
                           out_shape=(ds.height, ds.width), transform=ds.transform,
                           invert=True)
    n = int(inside.sum())
    idx = {name: i for i, name in enumerate(ds.descriptions, 1)}

    def band(name: str) -> np.ndarray:
        return ds.read(idx[name])

    valid = band("water_valid_years_2014_17")
    permanent = band("water_permanent_years_2014_17")
    known = band("water_history_known")
    slope = band("slope_below_5deg")
    finite = inside & np.isfinite(valid) & np.isfinite(permanent)
    assert np.all(np.isclose(valid[finite], np.rint(valid[finite])))
    assert np.all(np.isclose(permanent[finite], np.rint(permanent[finite])))
    assert np.all(permanent[finite] <= valid[finite])
    assert np.all((known[finite] == 1) == (valid[finite] >= 3))
    counts = []
    for v in range(5):
        for p in range(v + 1):
            count = int(np.count_nonzero(finite & (valid == v) & (permanent == p)))
            counts.append({"valid_years": v, "permanent_years": p,
                           "pixel_centers": count, "fraction_of_pilot": count / n,
                           "interpretation": "annual seasonal/non-water classes unresolved"})
    counts.append({"valid_years": "NA", "permanent_years": "NA",
                   "pixel_centers": int(np.count_nonzero(inside & ~finite)),
                   "fraction_of_pilot": float(np.count_nonzero(inside & ~finite) / n),
                   "interpretation": "source counts absent/NaN, not known non-water"})
    write_csv(OUT / "phase4_water_valid_permanent_crosstab.csv", counts)

    early = band("pre_early_vv_db")
    late = band("pre_late_vv_db")
    pre = inside & np.isfinite(early) & np.isfinite(late)
    delta = late[pre] - early[pre]
    ref_summary = {
        "pilot_pixel_centers": n,
        "phase4_water_count_bands_finite_pixels": int(finite.sum()),
        "phase4_water_count_bands_missing_pixels": int(np.count_nonzero(inside & ~finite)),
        "jrc_class_1_vs_2_not_recoverable_from_phase4_count_bands": True,
        "reference_median_pair_overlap_pixels": int(pre.sum()),
        "late_minus_early_reference_db_p05": float(np.percentile(delta, 5)),
        "late_minus_early_reference_db_median": float(np.median(delta)),
        "late_minus_early_reference_db_p95": float(np.percentile(delta, 95)),
        "reference_pair_abs_difference_gt_3db_pixels": int(np.count_nonzero(np.abs(delta) > 3)),
        "reference_dry_status": "unverified; no ground corroboration at scene time/location",
    }
    comparison = []
    for event in ("aug09", "aug21"):
        support = inside & (band(event + "_early_strict_qa") == 1)
        early_c = support & (band(event + "_early_candidate_3db") == 1)
        late_c = support & (band(event + "_late_candidate_3db") == 1)
        both = int(np.count_nonzero(early_c & late_c))
        early_only = int(np.count_nonzero(early_c & ~late_c))
        late_only = int(np.count_nonzero(late_c & ~early_c))
        neither = int(np.count_nonzero(support & ~early_c & ~late_c))
        assert both + early_only + late_only + neither == int(support.sum())
        no_water_c = inside & (band(event + "_early_candidate_3db_no_water_exclusion") == 1)
        comparison.append({
            "event_date": "2018-08-09" if event == "aug09" else "2018-08-21",
            "strict_support_pixels": int(support.sum()), "both_positive_pixels": both,
            "early_reference_only_pixels": early_only,
            "late_reference_only_pixels": late_only,
            "neither_positive_pixels": neither,
            "candidate_union_pixels": both + early_only + late_only,
            "candidate_jaccard_within_strict_support": both / (both + early_only + late_only),
            "no_water_exclusion_candidate_pixels": int(no_water_c.sum()),
            "no_water_candidate_outside_strict_support_pixels": int(np.count_nonzero(no_water_c & ~support)),
            "interpretation": "unvalidated SAR threshold/reference sensitivity; not flood area",
        })
    write_csv(OUT / "reference_candidate_overlap.csv", comparison)
    (OUT / "reference_and_support_summary.json").write_text(
        json.dumps(ref_summary, indent=2) + "\n", encoding="utf-8")

    annual_status = {"local_jrc_annual_geotiff_present": JRC_TIF.is_file(),
                     "annual_class_spatial_map": "pending"}
    if JRC_TIF.is_file():
        with rasterio.open(JRC_TIF) as jrc:
            assert jrc.count == 4 and jrc.crs == ds.crs
            assert jrc.transform == ds.transform and jrc.shape == ds.shape
            assert jrc.descriptions == tuple(f"waterClass_{y}" for y in (2014, 2015, 2016, 2017))
            # Earth Engine/GDAL tags a four-band Byte export as RGBA. Band 4 is
            # actually the 2017 class, so its real class-0 cells become an
            # apparent alpha mask on bands 1-3. Read raw values, not masked=True.
            classes = jrc.read()
            apparent_alpha_pixels = int(np.count_nonzero(
                inside & (jrc.read_masks(1) == 0)))
            assert np.array_equal(jrc.read(4)[inside] == 0,
                                  (jrc.read_masks(1)[inside] == 0))
            assert set(np.unique(classes[:, inside])).issubset({0, 1, 2, 3, 255})
        ee_counts = json.loads((PROC / "jrc_ee_console_transcription.json")
                               .read_text(encoding="utf-8"))
        ee_denominator = ee_counts["denominator_pixel_centers"]
        assert n - ee_denominator == 370
        annual = []
        for i, year in enumerate((2014, 2015, 2016, 2017)):
            for code, name in ((0, "no_data"), (1, "not_water"),
                               (2, "seasonal_water"), (3, "permanent_water"),
                               (255, "source_masked")):
                c = int(np.count_nonzero(inside & (classes[i] == code)))
                expected = ee_counts["annual"][str(year)][str(code)]
                assert c - expected == (370 if code == 255 else 0), (year, code, c, expected)
                annual.append({"year": year, "waterClass": code,
                               "class_name": name, "pixel_centers": c,
                               "fraction_of_pilot": c / n})
        write_csv(OUT / "jrc_annual_class_counts.csv", annual)
        valid_years = np.isin(classes, (1, 2, 3)).sum(axis=0)
        perm_years = (classes == 3).sum(axis=0)
        seasonal_years = (classes == 2).sum(axis=0)
        # Conservative, disjoint summaries. State 4 is explicitly mixed/other.
        state = np.full(ds.shape, 255, dtype="uint8")
        state[inside] = 0  # <3 source-valid annual observations
        state[inside & (valid_years >= 3)] = 4
        state[inside & (valid_years == 4) & np.all(classes == 1, axis=0)] = 1
        state[inside & (valid_years >= 3) & (seasonal_years >= 1) & (perm_years < 3)] = 2
        state[inside & (valid_years >= 3) & (perm_years >= 3)] = 3
        meta = ds.profile.copy()
        meta.update(count=1, dtype="uint8", nodata=255, compress="lzw")
        with rasterio.open(PROC / "jrc_composite_state_pilot.tif", "w", **meta) as dst:
            dst.write(state, 1)
            dst.set_band_description(1, "2014_17_conservative_water_state")
        names = {0: "insufficient_data", 1: "all_four_not_water",
                 2: "seasonal_observed", 3: "permanent_at_least_three_years",
                 4: "mixed_other_known"}
        state_rows = []
        for code, name in names.items():
            c = int(np.count_nonzero(inside & (state == code)))
            assert c - ee_counts["composite"][str(code)] == (370 if code == 0 else 0)
            state_rows.append({"state_code": code, "state_name": name,
                               "pixel_centers": c, "fraction_of_pilot": c / n})
        write_csv(OUT / "jrc_composite_state_counts.csv", state_rows)
        # Compare exact annual valid/permanent sums to Phase 4 derived bands.
        same = finite & (valid_years == valid) & (perm_years == permanent)
        annual_status.update({"annual_class_spatial_map": "executed",
                              "local_minus_earth_engine_polygon_pixels": n - ee_denominator,
                              "difference_only_in_source_masked_or_insufficient_pixels": True,
                              "rgba_apparent_alpha_pixels_inside_pilot": apparent_alpha_pixels,
                              "raw_bands_used_ignoring_false_alpha_mask": True,
                              "phase4_count_band_agreement_pixels": int(same.sum()),
                              "phase4_count_band_overlap_pixels": int(finite.sum())})
    (OUT / "jrc_annual_export_status.json").write_text(
        json.dumps(annual_status, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"reference_summary": ref_summary,
                  "candidate_reference_comparison": comparison,
                  "annual_export_status": annual_status}, indent=2))
