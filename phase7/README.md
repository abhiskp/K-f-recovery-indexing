# Phase 7 — data-gated Kerala flood–rice research handoff

**Status (16 November 2026): NO-GO for an exposure-attributed recovery measure, recovery index, or priority-ranking claim.** This phase follows the independent [Phase 6 audit](data/raw/Phase6_Independent_Audit_2026-11-11.md), which passed computation and descriptive analysis but found no validated independent flood-label footprint × contemporaneous paddy geography. Previous phases are unchanged.

## Executed

- Recomputed the Phase 6 autumn 2018–19 production contrast directly from the 252-row Phase 3 source panel and official administrative categories: **−50.15151 percentage points**, descriptive only. The 378-row Phase 6 join is a verified **long-format transformation** with unique district × season × indicator × comparison keys, not duplicate input observations.
- Downloaded and examined official Kerala DES annual agricultural-statistics PDFs for 2020–21 through 2023–24 and final seasonal estimates for 2024–25. Extended the district × season panel from 252 to **462** observations. Area is published seasonal paddy area (explicitly wet paddy from 2019–20 onward); production is published rice before 2020–21 and explicitly total wet+dry rice thereafter. A source-scope break is marked, and historical production/area ratios are **not** treated as validated yield. Each new row identifies source PDF, PDF and printed page, table, units, URL and crop/season decision.
- Reconciled all 30 new annual-season area/production district sums to printed state controls. The largest absolute difference is **0.074 tonnes** in a 2020–21 rice-production row. The image-only 2024–25 summer wet and dry tables have separate visual transcription CSVs; summer wet area differs from its rounded state row by 0.005 ha.
- Ran four-point pre-2018 descriptive trend and baseline sensitivity diagnostics. Logged later event evidence without coding unreviewed years as flood-free. Prepared a source/permission tracker, nonagricultural functional-observation matrix and three **unsent** access requests.

## Blocked

The required 21 August 2018 RADARSAT-2 GIS classification and valid observed footprint, actual season-specific 2018 cultivated-paddy geography, and 2018-valid geographic crosswalks are not present. The optional KSDMA depth-point records are also absent. A public map or WMS colour tile is not an independent class label. Without the first three inputs, no inundated-rice denominator, independent validation, local exposure–outcome link or rank-benefit evaluation is possible.

## Files

- [results_phase7.md](results_phase7.md): executed numbers and source discrepancies.
- [decision_gate.md](decision_gate.md): explicit gate decisions and alternative paper scope.
- [source_access_matrix.csv](source_access_matrix.csv): essential inputs, custodian, permission and status.
- [nonagricultural_coverage_matrix.csv](nonagricultural_coverage_matrix.csv): functional observation coverage by domain.
- [data_dictionary.md](data_dictionary.md), [methods_and_limitations.md](methods_and_limitations.md), [REPRODUCE.md](REPRODUCE.md): schema, design limits and exact commands.
- `data/raw/`: official PDFs and extraction text, scanned-page verification images, summer transcription and independent audit.
- `data/processed/`: extended rice panel.
- `results/`: reconciliation, trends, baseline sensitivity, event flags, source-panel recheck and SHA-256 manifest.
- `scripts/`: deterministic standard-library Python; no Earth Engine authentication or random seed.
- `requests/`: drafts only; **no email was sent**.

Public PDFs are retained for local source verification; institutional rights to redistribute restricted GIS files are not presumed. Preserve any released source licence before sharing such files.
