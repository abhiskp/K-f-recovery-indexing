#!/usr/bin/env python3
"""Document the fixed exploratory acquisition choices from the reviewed inventory."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/gee_2018_acquisition_groups.csv"
OUTPUT = ROOT / "results/selected_2018_pilot_acquisitions.csv"
DESIGN = {
    "2018-06-10": ("reference_early", "Before first dated NRSC flood map; dry status unverified"),
    "2018-06-22": ("reference_early_and_late", "Before first dated NRSC flood map; dry status unverified"),
    "2018-07-04": ("reference_late", "Before first dated NRSC flood map; dry status unverified"),
    "2018-07-16": ("chronology_check", "NRSC mapped flooding on this date; excluded from reference"),
    "2018-08-09": ("event_candidate_09_aug", "Dated NRSC Sentinel-1 flood product; not independent validation"),
    "2018-08-21": ("event_candidate_21_aug_morning", "Morning S1A acquisition; NRSC 06Hr Radarsat-2 time is approximate"),
}

with SOURCE.open(newline="") as stream:
    rows = list(csv.DictReader(stream))
selected = []
for date, (role, note) in DESIGN.items():
    matches = [row for row in rows if row["acquisition_date_ist"] == date
               and row["platform_number"] == "A"
               and row["pass_direction"] == "DESCENDING"
               and row["relative_orbit"] == "165.0"]
    if len(matches) != 1:
        raise ValueError(f"Expected one selected acquisition on {date}; found {len(matches)}")
    row = matches[0]
    if int(row["granule_count"]) != 2:
        raise ValueError(f"{date}: adjacent granule count changed")
    if not 0.99 <= float(row["sum_granule_valid_fractions_not_union"]) <= 1.01:
        raise ValueError(f"{date}: approximate combined validity changed")
    selected.append({
        "acquisition_date_ist": date,
        "role": role,
        "platform": row["platform_number"],
        "pass_direction": row["pass_direction"],
        "relative_orbit": row["relative_orbit"],
        "absolute_orbit": row["absolute_orbit"],
        "first_granule_start_utc": row["first_scene_acquisition_utc"],
        "last_granule_start_utc": row["last_scene_acquisition_utc"],
        "first_granule_start_ist": row["first_scene_acquisition_ist"],
        "last_granule_start_ist": row["last_scene_acquisition_ist"],
        "granule_count": row["granule_count"],
        "sum_granule_valid_fractions_not_union": row[
            "sum_granule_valid_fractions_not_union"],
        "mean_incidence_angle_deg_approx": row[
            "valid_fraction_weighted_mean_incidence_angle_deg_approx"],
        "scene_ids_pipe_separated": row["scene_ids_pipe_separated"],
        "dry_status": "unverified",
        "independent_pixel_label_status": "unavailable",
        "selection_note": note,
    })

with OUTPUT.open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=selected[0].keys())
    writer.writeheader()
    writer.writerows(selected)
print(f"Selected {len(selected)} dated acquisitions; output: {OUTPUT}")
