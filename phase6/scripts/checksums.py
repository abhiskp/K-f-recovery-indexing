#!/usr/bin/env python3
"""Write or verify the Phase 6 SHA-256 file inventory (and read-only Phase 3 input)."""
from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P6 = ROOT / "phase6"
DEST = P6 / "results/checksums.csv"
EXCLUDE = {DEST, P6 / "MANIFEST.md"}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def records() -> list[dict]:
    paths = sorted(p for p in P6.rglob("*") if p.is_file() and p not in EXCLUDE)
    paths.append(ROOT / "phase3/data/processed/district_season_rice_2014_2020.csv")
    paths.append(ROOT / "phase4/data/raw/phase4_s1_2018_pilot_exploratory_candidate_bands.tif")
    return [{"path_from_project_root": str(p.relative_to(ROOT)),
             "bytes": p.stat().st_size, "sha256": digest(p)} for p in paths]


def main() -> None:
    assert len(sys.argv) == 2 and sys.argv[1] in {"write", "verify"}, "usage: checksums.py write|verify"
    actual = records()
    if sys.argv[1] == "write":
        with DEST.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(actual[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(actual)
        print(f"wrote {len(actual)} SHA-256 records")
    else:
        with DEST.open(newline="", encoding="utf-8") as stream:
            expected = list(csv.DictReader(stream))
        assert expected == [{k: str(v) for k, v in r.items()} for r in actual], "checksum/manifest mismatch"
        print(f"verified {len(actual)} SHA-256 records")


if __name__ == "__main__":
    main()
