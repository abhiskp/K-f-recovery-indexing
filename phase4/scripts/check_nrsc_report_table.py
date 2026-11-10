#!/usr/bin/env python3
"""Arithmetic QA of NRSC 21 August 06Hr reported partial-coverage table."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'data/processed/nrsc_2018_08_21_06_reported_inundation.csv'
OUT=ROOT/'results/nrsc_2018_08_21_06_area_check.json'
PRINTED_TOTAL_HA=36658

def main() -> None:
    with SOURCE.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    if len(rows)!=5 or len({r['district'] for r in rows})!=5:
        raise ValueError('Expected five unique district rows')
    sum_ha=sum(int(r['reported_inundated_area_ha']) for r in rows)
    summary={
        'source':'NRSC/NDEM Kerala flood report 21 August 2018 06Hr, Table 2',
        'sensor':'Radarsat-2 SAR',
        'district_rows':len(rows),
        'sum_of_printed_district_values_ha':sum_ha,
        'printed_total_ha':PRINTED_TOTAL_HA,
        'printed_total_minus_row_sum_ha':PRINTED_TOTAL_HA-sum_ha,
        'partially_covered_districts':[r['district'] for r in rows if r['partial_satellite_coverage_marked']=='1'],
        'interpretation':'Operational partial-coverage summary, not statewide flood area or independent pixel labels.'
    }
    if sum_ha!=36657 or PRINTED_TOTAL_HA-sum_ha!=1:
        raise ValueError('NRSC table transcription does not match checked source')
    OUT.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
