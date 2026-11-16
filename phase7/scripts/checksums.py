#!/usr/bin/env python3
"""Create/verify SHA-256 manifest for Phase 7 and read-only upstream inputs."""
from __future__ import annotations
import csv
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P7 = ROOT / "phase7"
OUT = P7 / "results/checksums.csv"
UPSTREAM = [ROOT / "phase3/data/processed/district_season_rice_2014_2020.csv",
            ROOT / "phase6/data/processed/official_district_notification_status.csv",
            ROOT / "phase6/decision_gate.md", ROOT / "phase6/DATA_REQUESTS.md"]

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

if len(sys.argv) != 2 or sys.argv[1] not in {"write", "verify"}:
    raise SystemExit("Usage: python3 phase7/scripts/checksums.py write|verify")
if sys.argv[1] == "write":
    files = [p for p in P7.rglob("*") if p.is_file() and p != OUT and
             not p.name.startswith(".DS_Store") and "__pycache__" not in p.parts]
    files += UPSTREAM
    rows = [{"path_from_project_root": str(p.relative_to(ROOT)), "sha256": sha(p),
             "bytes": p.stat().st_size} for p in sorted(files)]
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} SHA-256 records")
else:
    with OUT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    mismatches = [(r["path_from_project_root"], r["sha256"],
                   sha(ROOT / r["path_from_project_root"]) if (ROOT / r["path_from_project_root"]).exists() else "MISSING")
                  for r in rows if not (ROOT / r["path_from_project_root"]).exists() or
                  sha(ROOT / r["path_from_project_root"]) != r["sha256"]]
    print(f"verified {len(rows)-len(mismatches)}/{len(rows)} SHA-256 records")
    if mismatches:
        print(mismatches[:10]); raise SystemExit(1)
