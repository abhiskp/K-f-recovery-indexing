#!/usr/bin/env python3
"""Check console-transcribed Earth Engine acquisition QA against local inventory."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELECTED = ROOT / "results/selected_2018_pilot_acquisitions.csv"
QA = ROOT / "results/gee_selected_acquisition_qa_console_transcription.csv"
OUT = ROOT / "results/gee_selected_acquisition_qa_summary.json"

with SELECTED.open(newline="") as stream:
    selected = {r["acquisition_date_ist"]: r for r in csv.DictReader(stream)}
with QA.open(newline="") as stream:
    qa = list(csv.DictReader(stream))
assert len(selected) == len(qa) == 6
assert {r["date_utc"] for r in qa} == set(selected)
for row in qa:
    date = row["date_utc"]
    assert int(row["scene_count"]) == int(selected[date]["granule_count"]) == 2
    coverage = float(row["mosaic_valid_fraction_aoi_approx_30m"])
    angle = float(row["mean_incidence_angle_deg_approx"])
    grouped_angle = float(selected[date]["mean_incidence_angle_deg_approx"])
    assert 0.95 <= coverage <= 1.0
    # Weighted per-granule means and a mean of the date mosaic differ slightly.
    assert abs(angle - grouped_angle) < 0.05
    assert row["source"].startswith("Earth Engine Code Editor acquisitionQA feature ")
coverage = [float(r["mosaic_valid_fraction_aoi_approx_30m"]) for r in qa]
angles = [float(r["mean_incidence_angle_deg_approx"]) for r in qa]
summary = {
    "acquisitions": len(qa),
    "granules_per_acquisition": 2,
    "mosaic_valid_fraction_min_approx_30m": min(coverage),
    "mosaic_valid_fraction_max_approx_30m": max(coverage),
    "mean_angle_min_deg_approx": min(angles),
    "mean_angle_max_deg_approx": max(angles),
    "mean_angle_range_deg_approx": max(angles) - min(angles),
    "source": "Console-transcribed executed Earth Engine FeatureCollection; exact exported CSV is checked separately by validate_gee_exports.py.",
    "interpretation": "Mosaic coverage and geometry QA only; not dry-baseline or flood-label validation.",
}
OUT.write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
