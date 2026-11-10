#!/usr/bin/env python3
"""QA a downloaded Earth Engine scene inventory without assigning flood truth.

Input is the completed Earth Engine Drive CSV in phase4/data/raw. Output records
all 2018 scenes, exact metadata and chronology flags; scene selection remains a
separate, documented visual and independent-source review.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/raw/phase4_kerala_2016_2018_s1_pilot_full_scene_inventory.csv'
OUT = ROOT / 'data/processed/gee_scene_inventory_cleaned.csv'
SCREEN = ROOT / 'results/gee_2018_scene_screen.csv'
GROUPS = ROOT / 'results/gee_2018_acquisition_groups.csv'
SUMMARY = ROOT / 'results/gee_inventory_review_summary.json'
REQUIRED = {
    'scene_id','acquisition_utc','platform_number','absolute_orbit',
    'relative_orbit','pass_direction','instrument_mode','polarizations',
    'resolution_m','footprint_fraction_of_aoi',
    'vv_valid_fraction_of_aoi_approx_30m',
    'incidence_angle_min_deg_approx','incidence_angle_max_deg_approx',
    'incidence_angle_mean_deg_approx','aoi_id','classification',
}

def write(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n')
        w.writeheader(); w.writerows(rows)

def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f'Missing researcher-downloaded Earth Engine export: {SOURCE}')
    with SOURCE.open(newline='',encoding='utf-8-sig') as f:
        r=csv.DictReader(f)
        missing=REQUIRED-set(r.fieldnames or ())
        if missing: raise ValueError(f'Missing columns: {sorted(missing)}')
        rows=list(r)
    if len(rows)!=134 or len({r['scene_id'] for r in rows})!=len(rows):
        raise ValueError('Expected 134 unique scene IDs from completed task')
    cleaned=[]
    for row in rows:
        dt=datetime.strptime(row['acquisition_utc'],'%Y-%m-%d %H:%M:%S')
        if not datetime(2016,6,1)<=dt<datetime(2018,10,15):
            raise ValueError(f'Out-of-range acquisition: {row["scene_id"]}')
        ist=dt+timedelta(hours=5,minutes=30)
        for name in ('footprint_fraction_of_aoi','vv_valid_fraction_of_aoi_approx_30m'):
            value=float(row[name])
            if not 0<=value<=1.00001:
                raise ValueError(f'Out-of-range {name}: {row["scene_id"]}')
        for name in ('incidence_angle_min_deg_approx','incidence_angle_max_deg_approx',
                     'incidence_angle_mean_deg_approx'):
            if row[name]: float(row[name])
        if row['instrument_mode']!='IW' or 'VV' not in row['polarizations'].split('|'):
            raise ValueError(f'Unexpected SAR mode/polarization: {row["scene_id"]}')
        if row['classification']!='unreviewed_scene':
            raise ValueError(f'An unreviewed inventory scene was pre-classified: {row["scene_id"]}')
        out={k:row[k] for k in sorted(REQUIRED)}
        out['acquisition_ist']=ist.strftime('%Y-%m-%d %H:%M:%S')
        out['relative_to_first_documented_july_flood']=(
            'before_2018-07-16' if ist.date()<datetime(2018,7,16).date()
            else 'on_or_after_2018-07-16')
        out['dry_status']='unverified'
        out['event_status']='unverified'
        out['needs_scene_visual_review']=1
        cleaned.append(out)
    cleaned.sort(key=lambda r:(r['acquisition_utc'],r['scene_id']))
    write(OUT,cleaned,list(cleaned[0]))
    screen=[r for r in cleaned if '2018-01-01'<=r['acquisition_ist']<'2019-01-01']
    write(SCREEN,screen,list(cleaned[0]))
    grouped=defaultdict(list)
    for r in screen:
        key=(r['acquisition_ist'][:10],r['platform_number'],r['pass_direction'],
             r['relative_orbit'],r['absolute_orbit'])
        grouped[key].append(r)
    group_rows=[]
    for key, members in sorted(grouped.items()):
        members.sort(key=lambda r:r['acquisition_utc'])
        weights=[float(r['vv_valid_fraction_of_aoi_approx_30m']) for r in members]
        mean_angle=sum(float(r['incidence_angle_mean_deg_approx'])*w
                       for r,w in zip(members,weights))/sum(weights)
        group_rows.append({
            'acquisition_date_ist':key[0],'platform_number':key[1],
            'pass_direction':key[2],'relative_orbit':key[3],
            'absolute_orbit':key[4],
            'first_scene_acquisition_utc':members[0]['acquisition_utc'],
            'last_scene_acquisition_utc':members[-1]['acquisition_utc'],
            'first_scene_acquisition_ist':members[0]['acquisition_ist'],
            'last_scene_acquisition_ist':members[-1]['acquisition_ist'],
            'granule_count':len(members),
            'sum_granule_footprint_fractions_not_union':sum(float(r['footprint_fraction_of_aoi']) for r in members),
            'sum_granule_valid_fractions_not_union':sum(weights),
            'valid_fraction_weighted_mean_incidence_angle_deg_approx':mean_angle,
            'scene_ids_pipe_separated':'|'.join(r['scene_id'] for r in members),
            'dry_status':'unverified','event_status':'unverified',
        })
    write(GROUPS,group_rows,list(group_rows[0]))
    summary={
        'all_unique_scenes':len(cleaned),
        '2018_scenes':len(screen),
        '2018_distinct_acquisitions':len(group_rows),
        '2018_two_granule_acquisitions':sum(r['granule_count']==2 for r in group_rows),
        '2018_one_granule_acquisitions':sum(r['granule_count']==1 for r in group_rows),
        '2018_before_16_july_local':sum(r['relative_to_first_documented_july_flood']=='before_2018-07-16' for r in screen),
        '2018_on_or_after_16_july_local':sum(r['relative_to_first_documented_july_flood']=='on_or_after_2018-07-16' for r in screen),
        '2018_pass_orbit_counts':{
            f'{direction}|{orbit}':count for (direction,orbit),count in sorted(
                Counter((r['pass_direction'],r['relative_orbit']) for r in screen).items())},
        'verified_dry_acquisitions':0,
        'independently_validated_flood_acquisitions':0,
        'status_note':'Granule grouping and exploratory date selection do not establish a dry baseline or independent flood truth.',
    }
    SUMMARY.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
