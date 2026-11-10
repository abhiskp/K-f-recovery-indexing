#!/usr/bin/env python3
"""Check the eight observed Earth Engine feasibility rows transcribed from UI."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'results/pilot_2017_2018_optical_viirs_feasibility.csv'
OUT=ROOT/'results/domain_feasibility_summary.json'
MONTHS=['2017-06','2017-07','2017-08','2017-09','2018-06','2018-07','2018-08','2018-09']

def main() -> None:
    with SOURCE.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    if [r['month'] for r in rows]!=MONTHS: raise ValueError('Unexpected month order/coverage')
    for row in rows:
        for key in ('l8_scenes','s2_sr_scenes','s2_toa_scenes','viirs_monthly_images'):
            if int(row[key])<0: raise ValueError(f'Negative count: {row}')
        for key in ('l8_clear_any_fraction_30m','s2_sr_clear_any_fraction_20m',
                    's2_toa_qa60_noncloud_any_fraction_60m'):
            if not 0<=float(row[key])<=1: raise ValueError(f'Invalid fraction: {row}')
        for key in ('viirs_mean_cf_cvg_500m','viirs_mean_avg_rad_nW_sr_cm2_500m'):
            if not math.isfinite(float(row[key])): raise ValueError(f'Nonfinite VIIRS value: {row}')
        if int(row['s2_sr_scenes'])==0 and float(row['s2_sr_clear_any_fraction_20m'])!=0:
            raise ValueError(f'S2 SR coverage without a scene: {row}')
    by={r['month']:r for r in rows}
    summary={
        'months':len(rows),
        'sentinel2_surface_reflectance_scenes_total':sum(int(r['s2_sr_scenes']) for r in rows),
        'sentinel2_toa_scenes_2018_july':int(by['2018-07']['s2_toa_scenes']),
        'sentinel2_toa_scenes_2018_august':int(by['2018-08']['s2_toa_scenes']),
        'landsat8_scenes_2018_july':int(by['2018-07']['l8_scenes']),
        'landsat8_august_2018_clear_any_fraction':float(by['2018-08']['l8_clear_any_fraction_30m']),
        'viirs_mean_cloud_free_observations_2018_july':float(by['2018-07']['viirs_mean_cf_cvg_500m']),
        'viirs_mean_cloud_free_observations_2018_august':float(by['2018-08']['viirs_mean_cf_cvg_500m']),
        'interpretation':'Availability/QA only; S2 TOA QA60 excludes opaque cloud/cirrus but not shadows, and low VIIRS cf_cvg precludes direct economic inference.'
    }
    OUT.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
