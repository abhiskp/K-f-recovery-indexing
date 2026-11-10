#!/usr/bin/env python3
"""Plot Phase 5 support and reference-disagreement QA, not flood extent."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "phase5-support-reference-qa"
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.warp import transform_geom

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "phase4/data/raw/phase4_s1_2018_pilot_exploratory_candidate_bands.tif"
OUT = ROOT / "phase5/figures"
OUT.mkdir(parents=True, exist_ok=True)
polygon = {"type": "Polygon", "coordinates": [[
    [76.35, 9.45], [76.60, 9.45], [76.60, 9.75],
    [76.35, 9.75], [76.35, 9.45]
]]}
with rasterio.open(SOURCE) as ds:
    inside = geometry_mask([transform_geom("EPSG:4326", ds.crs.to_string(), polygon)],
                           out_shape=ds.shape, transform=ds.transform, invert=True)
    band = {name: ds.read(i) for i, name in enumerate(ds.descriptions, 1)
            if name in {"water_valid_years_2014_17", "aug21_early_strict_qa",
                        "aug21_early_candidate_3db", "aug21_late_candidate_3db"}}
    extent = [ds.bounds.left / 1000, ds.bounds.right / 1000,
              ds.bounds.bottom / 1000, ds.bounds.top / 1000]

valid = band["water_valid_years_2014_17"]
left = np.full(ds.shape, np.nan)
left[inside & ~np.isfinite(valid)] = 0
left[inside & np.isfinite(valid)] = valid[inside & np.isfinite(valid)]
support = inside & (band["aug21_early_strict_qa"] == 1)
early = support & (band["aug21_early_candidate_3db"] == 1)
late = support & (band["aug21_late_candidate_3db"] == 1)
right = np.full(ds.shape, np.nan)
right[inside] = 0
right[support] = 1
right[early & late] = 2
right[early & ~late] = 3
right[late & ~early] = 4

fig, axes = plt.subplots(1, 2, figsize=(13.2, 7.2), constrained_layout=True)
for ax in axes:
    ax.set_xlabel("UTM easting (km, EPSG:32643)")
    ax.set_ylabel("UTM northing (km, EPSG:32643)")
    ax.tick_params(labelsize=8)
    ax.set_aspect("equal")
axes[0].imshow(left, origin="upper", extent=extent,
               cmap=ListedColormap(["#d5d8dc", "#fee8c8", "#fdbb84", "#e34a33", "#a50f15"]),
               norm=BoundaryNorm(np.arange(-0.5, 5.5, 1), 5), interpolation="nearest")
axes[0].set_title("A. Pre-2018 JRC years with known class", fontsize=11)
axes[0].text(0.98, 0.985, "Source: EC JRC/Google (GSW v1.4)",
             transform=axes[0].transAxes, ha="right", va="top", fontsize=7,
             bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.88})
axes[0].legend(handles=[Patch(facecolor=c, label=l) for c, l in zip(
    ["#d5d8dc", "#fee8c8", "#fdbb84", "#e34a33", "#a50f15"],
    ["No usable count band", "1 year", "2 years", "3 years", "4 years"])],
    loc="lower left", fontsize=8, framealpha=0.95)
axes[1].imshow(right, origin="upper", extent=extent,
               cmap=ListedColormap(["#d5d8dc", "#f8f8f8", "#5e3c99", "#e66101", "#1b9e77"]),
               norm=BoundaryNorm(np.arange(-0.5, 5.5, 1), 5), interpolation="nearest")
axes[1].set_title("B. 21 Aug candidate by reference pair (3 dB)", fontsize=11)
axes[1].legend(handles=[Patch(facecolor=c, label=l) for c, l in zip(
    ["#d5d8dc", "#f8f8f8", "#5e3c99", "#e66101", "#1b9e77"],
    ["Outside strict support", "Neither pair", "Both pairs", "June pair only", "June/July pair only"])],
    loc="lower left", fontsize=8, framealpha=0.95)
fig.suptitle("Kerala 2018 pilot: JRC support and SAR reference sensitivity — unvalidated", fontsize=13)
fig.savefig(OUT / "phase5_support_reference_qa.png", dpi=300, bbox_inches="tight")
fig.savefig(OUT / "phase5_support_reference_qa.svg", bbox_inches="tight",
            metadata={"Date": "2026-11-09"})
print("Saved Phase 5 support/reference QA figure; no flood extent inferred.")
