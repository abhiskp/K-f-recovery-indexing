#!/usr/bin/env python3
"""Render two vector figures from executed Experiment A CSVs; standard library only."""
import csv
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
FIGURES = HERE / "figures"
FIGURES.mkdir(exist_ok=True)

def read(name):
    with (RESULTS / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def txt(x, y, s, size=14, fill="#263849", anchor="start", weight="normal"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>'

def svg(w, h, body, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
            '<rect width="100%" height="100%" fill="white"/>'
            '<style>text{font-family:Arial,Helvetica,sans-serif}</style>' + ''.join(body) + '</svg>\n')

# Annual observed state production compared with the four-year, season-matched mean.
rows = read("state_season_series.csv")
years = ["2014-15", "2015-16", "2016-17", "2017-18", "2018-19", "2019-20"]
series = {(r["year"], r["season"]): float(r["pct_vs_baseline"])
          for r in rows if r["metric"] == "production"}
colors = {"Autumn": "#b64942", "Winter": "#197798", "Summer": "#47905b"}
w, h = 1000, 600
left, right, top, bottom = 100, 930, 90, 490
ymin, ymax = -55, 65
X = lambda i: left + (right-left)*i/(len(years)-1)
Y = lambda v: bottom - (v-ymin)*(bottom-top)/(ymax-ymin)
b = [txt(55, 39, "Seasonal rice production, Kerala", 26, weight="bold"),
     txt(55, 64, "Percent deviation from 2014–15 to 2017–18 same-season mean; descriptive, not flood-attributable", 13)]
for tick in (-50, -25, 0, 25, 50):
    y = Y(tick)
    b += [f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{ "#506273" if tick == 0 else "#e4e9ec" }" stroke-width="{2 if tick == 0 else 1}"/>',
          txt(left-12, y+5, f"{tick:+d}%" if tick else "0%", 13, anchor="end")]
for i, year in enumerate(years):
    b.append(txt(X(i), bottom+29, year, 13, anchor="middle"))
for season, color in colors.items():
    points = ' '.join(f'{X(i):.1f},{Y(series[(year,season)]):.1f}' for i,year in enumerate(years))
    b.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    for i, year in enumerate(years):
        b.append(f'<circle cx="{X(i):.1f}" cy="{Y(series[(year,season)]):.1f}" r="4.5" fill="{color}"/>')
    b += [f'<line x1="{left+270*list(colors).index(season)}" y1="560" x2="{left+270*list(colors).index(season)+30}" y2="560" stroke="{color}" stroke-width="4"/>',
          txt(left+270*list(colors).index(season)+39, 565, season, 15)]
(FIGURES / "state_seasonal_rice_production.svg").write_text(svg(w,h,b,"Seasonal rice production deviations","Official DES rice production; state sums from district panel, six years and three seasons."), encoding="utf-8")

# District autumn production deviations for two observed post-event years.
rows = read("district_season_trajectories.csv")
data = [r for r in rows if r["season"] == "Autumn" and r["metric"] == "production" and r["pct_2018_vs_baseline"] != ""]
data.sort(key=lambda r: float(r["pct_2018_vs_baseline"]))
w,h = 1050, 720
left,right,top,step = 230,930,110,38
xmin,xmax = -105,80
X2 = lambda v: left+(v-xmin)*(right-left)/(xmax-xmin)
b = [txt(45,38,"District autumn rice production",25,weight="bold"),
     txt(45,64,"2018–19 and 2019–20 versus district autumn 2014–17 mean; 2018–19 sorted ascending",13)]
for tick in (-100,-75,-50,-25,0,25,50,75):
    x = X2(tick)
    b += [f'<line x1="{x:.1f}" y1="{top-20}" x2="{x:.1f}" y2="{top+step*len(data)}" stroke="{ "#647887" if tick == 0 else "#e4e9ec" }" stroke-width="{2 if tick == 0 else 1}"/>',
          txt(x,top+step*len(data)+25,f"{tick:+d}%" if tick else "0%",12,anchor="middle")]
for i,r in enumerate(data):
    y=top+i*step
    a=float(r["pct_2018_vs_baseline"]); c=float(r["pct_2019_vs_baseline"])
    b += [txt(left-13,y+5,r["district"],13,anchor="end"),
          f'<line x1="{X2(a):.1f}" y1="{y}" x2="{X2(c):.1f}" y2="{y}" stroke="#9eaeb7" stroke-width="2"/>',
          f'<circle cx="{X2(a):.1f}" cy="{y}" r="5.5" fill="#b64942"/>',
          f'<circle cx="{X2(c):.1f}" cy="{y}" r="5.5" fill="#197798"/>']
b += [f'<circle cx="{left}" cy="665" r="5.5" fill="#b64942"/>',txt(left+14,670,"2018–19",14),
      f'<circle cx="{left+200}" cy="665" r="5.5" fill="#197798"/>',txt(left+214,670,"2019–20",14),
      txt(45,705,"Wayanad excluded: zero pre-flood autumn production, so percent deviation is undefined.",12)]
(FIGURES / "district_autumn_production_deviations.svg").write_text(svg(w,h,b,"District autumn rice production deviations","District production deviations versus four-year autumn mean. Wayanad undefined due to zero baseline."), encoding="utf-8")
print("Wrote two SVG figures")
