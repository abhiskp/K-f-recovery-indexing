#!/usr/bin/env python3
"""Inspect Tiwari et al. S1 GeoTIFFs; zeros/nodata are unknown, not negatives."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.warp import Resampling, reproject

ROOT = Path(__file__).resolve().parents[2]
P6 = ROOT / "phase6"
TIFDIR = P6 / "data/raw/tiwari_s1/Data for submission/Flood data analysis"
PILOT = ROOT / "phase4/data/raw/phase4_s1_2018_pilot_exploratory_candidate_bands.tif"
RESULTS = P6 / "results"
RESULTS.mkdir(exist_ok=True)
NAMES = sorted(p.name for p in TIFDIR.glob("*.tif"))
assert len(NAMES) == 11


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


inventory = []
for name in NAMES:
    path = TIFDIR / name
    with rasterio.open(path) as src:
        counts = {0: 0, 1: 0, "other": 0}
        for _, window in src.block_windows(1):
            a = src.read(1, window=window)
            counts[0] += int(np.count_nonzero(a == 0))
            counts[1] += int(np.count_nonzero(a == 1))
            counts["other"] += int(np.count_nonzero((a != 0) & (a != 1)))
        assert counts["other"] == 0
        assert src.nodata == 0
        inventory.append({"file": name, "bytes": path.stat().st_size,
                          "sha256": sha256(path), "crs": str(src.crs),
                          "width_px": src.width, "height_px": src.height,
                          "left": src.bounds.left, "bottom": src.bounds.bottom,
                          "right": src.bounds.right, "top": src.bounds.top,
                          "band_count": src.count, "data_type": src.dtypes[0],
                          "nodata_value": src.nodata, "positive_value": 1,
                          "positive_pixel_count_whole_raster": counts[1],
                          "unknown_zero_count_whole_raster": counts[0],
                          "other_values_count": counts["other"],
                          "valid_negative_class_available": "no",
                          "scene_footprint_in_archive": "no",
                          "exact_acquisition_utc_in_archive": "no"})
write_csv(RESULTS / "tiwari_s1_raster_inventory.csv", inventory)

pilot_results = []
with rasterio.open(PILOT) as pilot:
    qa = pilot.read(pilot.descriptions.index("aug21_early_strict_qa") + 1)
    candidate = pilot.read(pilot.descriptions.index("aug21_early_candidate_3db") + 1)
    qa = np.isfinite(qa) & (qa == 1)
    candidate = np.isfinite(candidate) & (candidate == 1)
    # Rasters have water-positive cells but no explicit valid negative/footprint.
    # Reprojection preserves 0 as unknown, never as observed non-water.
    for name in ("5Jan2018.tif", "28July2018.tif", "9Aug2018.tif", "21Aug2018.tif", "26sept2018.tif"):
        with rasterio.open(TIFDIR / name) as src:
            positive = np.zeros((pilot.height, pilot.width), dtype=np.uint8)
            reproject(source=rasterio.band(src, 1), destination=positive,
                      src_transform=src.transform, src_crs=src.crs, src_nodata=0,
                      dst_transform=pilot.transform, dst_crs=pilot.crs, dst_nodata=0,
                      resampling=Resampling.nearest)
            pos = positive == 1
            valid_overlap = pos & qa
            pilot_results.append({"published_raster": name,
                                  "pilot_grid_pixels": pilot.width*pilot.height,
                                  "published_positive_pixels_on_pilot_grid": int(pos.sum()),
                                  "phase4_aug21_strict_qa_pixels": int(qa.sum()),
                                  "published_positive_and_phase4_qa_pixels": int(valid_overlap.sum()),
                                  "published_positive_and_phase4_candidate_pixels": int((valid_overlap & candidate).sum()),
                                  "candidate_fraction_among_published_positives_on_qa":
                                  round(float((valid_overlap & candidate).sum()/valid_overlap.sum()), 6)
                                  if valid_overlap.any() else "",
                                  "interpretation": "same-sensor descriptive concordance; not validation; zero is unknown"})
write_csv(RESULTS / "tiwari_phase4_positive_overlap.csv", pilot_results)

rain = P6 / "data/raw/tiwari_s1/Data for submission/Climate data analysis/kerala_point_flood.csv"
with rain.open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream))
assert len(rows) == 3286
assert rows[0]["system:time_start"] == "2010-01-01"
assert rows[-1]["system:time_start"] == "2018-12-30"
summary = {"raster_count": len(inventory), "all_rasters_binary_positive_only": True,
           "all_rasters_zero_is_nodata": True,
           "rainfall_point_rows": len(rows), "rainfall_first_date": rows[0]["system:time_start"],
           "rainfall_last_date": rows[-1]["system:time_start"],
           "rainfall_sites": list(rows[0])[1:],
           "archive_contains_validation_point_labels": False,
           "archive_contains_gee_source_code": False,
           "archive_contains_valid_scene_footprints": False,
           "pilot_overlap": pilot_results,
           "use_as_independent_validation": False}
(RESULTS / "tiwari_s1_audit.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
