#!/usr/bin/env python3
"""Map actual 2014-17 JRC source classes on the Phase 4 pilot grid, not flood."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "phase5-jrc-annual-classes"
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.warp import transform_geom

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "phase5/data/raw/phase5_jrc_waterclass_2014_2017_pilot.tif"
OUT = ROOT / "phase5/figures"
OUT.mkdir(parents=True, exist_ok=True)
polygon = {"type": "Polygon", "coordinates": [[
    [76.35, 9.45], [76.60, 9.45], [76.60, 9.75],
    [76.35, 9.75], [76.35, 9.45]
]]}
with rasterio.open(SOURCE) as ds:
    assert ds.descriptions == tuple(f"waterClass_{y}" for y in range(2014, 2018))
    inside = geometry_mask([transform_geom("EPSG:4326", ds.crs.to_string(), polygon)],
                           out_shape=ds.shape, transform=ds.transform, invert=True)
    # GDAL interprets band 4 as alpha in a four-band Byte export. It is 2017
    # waterClass, so read raw values to retain true class-0 cells.
    classes = ds.read()
    extent = [ds.bounds.left / 1000, ds.bounds.right / 1000,
              ds.bounds.bottom / 1000, ds.bounds.top / 1000]

colors = ["#542788", "#d8b365", "#80cdc1", "#01665e", "#d9d9d9"]
labels = ["0: source no data", "1: not water", "2: seasonal water",
          "3: permanent water", "255: source masked"]
cmap = ListedColormap(colors)
norm = BoundaryNorm(np.arange(-0.5, 5.5), 5)
fig, axes = plt.subplots(2, 2, figsize=(11, 12))
fig.subplots_adjust(left=0.07, right=0.97, top=0.89, bottom=0.16,
                    hspace=0.34, wspace=0.22)
for i, (year, ax) in enumerate(zip(range(2014, 2018), axes.flat)):
    view = np.full(ds.shape, np.nan)
    for code, display in ((0, 0), (1, 1), (2, 2), (3, 3), (255, 4)):
        view[inside & (classes[i] == code)] = display
    ax.imshow(view, origin="upper", extent=extent, cmap=cmap, norm=norm,
              interpolation="nearest")
    ax.set_title(f"{year} JRC YearlyHistory waterClass", fontsize=11)
    ax.set_xlabel("UTM easting (km, EPSG:32643)")
    ax.set_ylabel("UTM northing (km, EPSG:32643)")
    ax.set_aspect("equal")
    ax.tick_params(labelsize=8)
fig.legend(handles=[Patch(facecolor=c, label=l) for c, l in zip(colors, labels)],
           loc="lower center", bbox_to_anchor=(0.5, 0.065), ncol=3,
           fontsize=9, frameon=False)
fig.suptitle("Pre-2018 JRC water-history source classes in the Kerala pilot\n"
             "Water history and missingness; not 2018 flood labels", fontsize=13,
             y=0.98)
fig.text(0.5, 0.025, "Source: EC JRC/Google, JRC/GSW1_4/YearlyHistory. "
         "Outside pilot is blank; 255 is source-masked, distinct from class 0.",
         ha="center", fontsize=8)
fig.savefig(OUT / "phase5_jrc_annual_classes.png", dpi=300, bbox_inches="tight")
fig.savefig(OUT / "phase5_jrc_annual_classes.svg", bbox_inches="tight",
            metadata={"Date": "2026-11-09"})
print("Saved annual JRC class QA figure; no 2018 flood extent inferred.")
