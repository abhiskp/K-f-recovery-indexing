#!/usr/bin/env python3
"""Check Phase 7 panel provenance, source arithmetic, and descriptive gate."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P7 = ROOT / "phase7"

def read(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

panel = read(P7 / "data/processed/district_season_rice_2014_2025.csv")
old = read(ROOT / "phase3/data/processed/district_season_rice_2014_2020.csv")
qa = read(P7 / "results/state_total_reconciliation.csv")
component = read(P7 / "results/rice_component_reconciliation.csv")
trends = read(P7 / "results/pre2018_trend_diagnostics.csv")
baseline = read(P7 / "results/baseline_sensitivity_2018_19.csv")
flags = read(P7 / "results/later_event_flags.csv")
summary = json.loads((P7 / "results/descriptive_summary.json").read_text())

assert len(panel) == 462 and len(old) == 252
assert len({(r["district"],r["year"],r["season"]) for r in panel}) == 462
assert set(Counter(r["year"] for r in panel).values()) == {42}
for a,b in zip(old,panel[:252]):
    for key in ("district","year","season","area_ha","production_tonnes"):
        assert a[key] == b[key], (key,a,b)
    assert b["yield_tonnes_per_ha"] == "" and b["legacy_phase3_ratio_tonnes_per_ha"] == a["yield_tonnes_per_ha"]
assert all(r["source_decision"].startswith(("contemporaneous_DES", "final_DES")) for r in panel[252:])
assert len(qa) == 30 and max(abs(float(r["difference_district_minus_state"])) for r in qa) <= 0.074001
assert len(component) == 210
mismatch = {(r["district"],r["year"],r["season"]): round(float(r["difference_total_minus_components_tonnes"]),3)
            for r in component if r["component_status"] == "source_printed_mismatch"}
assert mismatch == {("Kozhikode","2020-21","Autumn"):-3.960,
                    ("Kasaragod","2020-21","Autumn"):0.074,
                    ("Kasaragod","2020-21","Summer"):0.475}
assert len(trends) == 84 and len(baseline) == 336 and len(flags) == 7
assert summary["independently_reproduced_2018_19_autumn_production"]["all_minus_some_pp"] == -50.15151
assert summary["pre_event_2017_18_placebo_all_minus_some_pp"] == 19.25802
print("Phase 7 validation passed: 462 unique panel cells, 30 state controls, 3 flagged source component mismatches, descriptive contrast and placebo")
