#!/usr/bin/env python3
"""Publication-ready descriptive QA figure; no flood validation is implied."""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)
summary = json.loads((RESULTS / "gee_export_validation.json").read_text())
with (RESULTS / "sar_candidate_pixel_sensitivity.csv").open(newline="") as stream:
    rows = list(csv.DictReader(stream))

def pick(event, threshold, water):
    found = [r for r in rows if r["event_date"] == event
             and r["reference_acquisitions"] == "2018-06-10|2018-06-22"
             and int(r["vv_drop_threshold_db"]) == threshold
             and r["water_treatment"] == water]
    assert len(found) == 1
    return found[0]

strict = "exclude_permanent_with_3_of_4_year_history"
unexcluded = "no_permanent_water_exclusion"
support = [
    ("S1 pre/event overlap", 1.0),
    ("Slope + S1 overlap", float(pick("2018-08-09",3,unexcluded)
                                  ["analysis_support_fraction_of_pilot"])),
    ("JRC history available", summary["water_history_finite_fraction"]),
    ("Strict analysis support", float(pick("2018-08-09",3,strict)
                                      ["analysis_support_fraction_of_pilot"])),
]
# The S1 overlap is measured from the exported validity band, not assumed 100%.
support[0] = ("S1 pre/event overlap",
              summary["pre_event_overlap_pixels"]["aug09_early"]
              / summary["pilot_aoi_pixel_centers"])

plt.rcParams.update({
    "font.family":"DejaVu Sans","font.size":10,
    "axes.spines.top":False,"axes.spines.right":False,
    "savefig.facecolor":"white",
})
fig, (ax1, ax2) = plt.subplots(1,2,figsize=(11.3,4.5),
                              gridspec_kw={"width_ratios":[1.05,1]})
fig.subplots_adjust(left=.16,right=.97,bottom=.22,top=.84,wspace=.31)

labels = [x[0] for x in support][::-1]
values = [100*x[1] for x in support][::-1]
colors = ["#7d4060","#678ca8","#9db9c4","#355a73"]
bars = ax1.barh(labels,values,color=colors,height=.58)
ax1.set_xlim(0,105)
ax1.set_xlabel("Share of pilot AOI (%)")
ax1.set_title("A  Valid comparison support",loc="left",fontweight="bold")
ax1.grid(axis="x",color="#dce3e7",lw=.6)
ax1.set_axisbelow(True)
for bar,value in zip(bars,values):
    ax1.text(min(value+1.4,102),bar.get_y()+bar.get_height()/2,
             f"{value:.1f}%",va="center",fontsize=9)

for event,color,label in [
    ("2018-08-09","#17668b","9 August"),
    ("2018-08-21","#b76527","21 August"),
]:
    pct = [100*float(pick(event,t,strict)["candidate_fraction_of_support"])
           for t in (2,3,4)]
    ax2.plot([2,3,4],pct,marker="o",lw=2.2,ms=6,color=color,label=label)
    for x,y in zip((2,3,4),pct):
        ax2.annotate(f"{y:.1f}%",(x,y),xytext=(0,8),textcoords="offset points",
                     ha="center",fontsize=8,color=color)
ax2.set_xticks([2,3,4])
ax2.set_xlim(1.8,4.2)
ax2.set_ylim(0,70)
ax2.set_xlabel("VV decrease threshold (dB)")
ax2.set_ylabel("Candidate-positive share of strict support (%)")
ax2.set_title("B  Threshold sensitivity",loc="left",fontweight="bold")
ax2.grid(axis="y",color="#dce3e7",lw=.6)
ax2.legend(frameon=False,loc="upper right")
fig.text(.5,.95,"2018 Kerala pilot: SAR support and unvalidated candidate masks",
         ha="center",va="top",fontsize=15,fontweight="bold")
fig.text(.5,.08,
         "Pilot 76.35–76.60°E, 9.45–9.75°N. Early reference: 10/22 June; "
         "dry status unverified. No independent flood labels.",
         ha="center",fontsize=9,color="#435666")
fig.text(.5,.045,
         "Candidate shares use the strict QA denominator; they are not "
         "inundation rates or exposure estimates.",
         ha="center",fontsize=9,color="#435666")
for ext in ("png","pdf"):
    fig.savefig(FIGURES / f"2018_pilot_sar_support_and_candidates.{ext}",
                dpi=300)
plt.close(fig)
print(FIGURES / "2018_pilot_sar_support_and_candidates.png")
