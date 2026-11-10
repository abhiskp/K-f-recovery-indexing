#!/usr/bin/env python3
"""Check manually transcribed, actually executed EE class-count console output."""
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "data/processed/jrc_ee_console_transcription.json"
record = json.loads(path.read_text(encoding="utf-8"))
denom = record["denominator_pixel_centers"]
assert denom == 1011240
assert record["phase4_rasterio_pilot_denominator"] - denom == 370
for year, classes in record["annual"].items():
    assert set(classes) == {"0", "1", "2", "3", "255"}, year
    assert sum(classes.values()) == denom, year
assert sum(record["composite"].values()) == denom
assert sum(record["annual"]["2015"][str(k)] for k in (0, 1, 2, 3)) == 369590
print("Four annual histograms and composite sum to 1,011,240 EE pixel centers.")
print("Boundary denominator differs from Phase 4 local AOI by 370; not merged.")
