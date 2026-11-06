# Data availability and gaps as of 27 October 2026

| Domain | Verified source | Functional observation available here | Current disposition |
|---|---|---|---|
| Agricultural output | [Kerala DES historical compendium](https://www.ecostat.kerala.gov.in/storage/publications/626.pdf), Tables 41, 44, 45; [2017–18](https://ecostat.kerala.gov.in/storage/publications/247.pdf), [2018–19](https://ecostat.kerala.gov.in/storage/publications/239.pdf), [2019–20](https://www.ecostat.kerala.gov.in/storage/publications/3.pdf), [2020–21](https://ecostat.kerala.gov.in/storage/publications/622.pdf) annual reports | District annual production, 2014–15 to 2020–21 for three crops | **Measured and analysed**, but event attribution and within-year recovery are unavailable. |
| Crop area and yield | [DES 2018–19 comparison table](https://ecostat.kerala.gov.in/storage/publications/239.pdf), printed p. 126 | State crop area for 2017–18 and 2018–19; yield calculated as production/area | **Measured diagnostic**. Extend district areas/yields before functional agricultural claims. |
| Event flood extent | [KSDMA 2018 map](https://sdma.kerala.gov.in/wp-content/uploads/2020/11/Flood_2018-1.pdf) credits NRSC inundation | A one-page reference map, no georeferenced pixel layer obtained | **Reference only**. Obtain underlying NRSC/KSDMA GeoTIFF/shapefile with acquisition dates, scale and legend; do not digitize this PDF as validation ground truth without georeferencing error analysis. |
| Flood depths | [KSDMA crowdsourced 2018 depth map](https://sdma.kerala.gov.in/wp-content/uploads/2020/11/CROWD_INUNDATION.pdf) | Visual points in PDF; raw coordinates/depth/quality metadata not obtained | **No analysis**. Request geocoded, timestamped point data and sampling method from KSDMA/KSEOC. |
| Sentinel-1 | [Earth Engine S1 GRD catalog](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD) | Archive is suitable in principle; no authenticated scene export | Prepared `gee_2018_pilot_UNEXECUTED.js`; **no raster produced**. |
| Optical vegetation | [Landsat 8 L2 catalog](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2); [Sentinel-2 harmonized catalog](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_HARMONIZED) | No pixels or valid-count series obtained | Landsat QA export prepared; Sentinel-2 harmonization and ecological land-cover validation remain open. NDVI/EVI/NDMI are spectral proxies. |
| Night lights | [VIIRS VCMSLCFG catalog](https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMSLCFG) | No monthly radiance/`cf_cvg` series obtained | QA export prepared. Rural signal and temporary lights must be tested; no economic recovery claim. |
| Housing, roads, services | [2018 PDNA](https://sdma.kerala.gov.in/wp-content/uploads/2019/03/PDNA-report-FINAL-FEB-2019_compressed.pdf) | Assessment reports one-off damage and needs; no repeated district/block restoration series extracted | **Excluded from index**. Seek dated house habitability/completion, road passability and power/water restoration records with stable location keys. |
| Existing vulnerability | Kendagannaswamy et al. (2026), [DOI](https://doi.org/10.1007/s12524-026-02440-y), Table 9 values in original script | 14 published district scores and four components | Reconstructed **only as retrospective comparator**; unavailable for a 2018 decision and adaptive-capacity direction ambiguous. |

## Access findings and exact unblock steps

The workspace has no Earth Engine credentials at `~/.config/earthengine`, the
Python Earth Engine package is absent, and a direct visit to the Code Editor
opened the Google sign-in page. The terminal also could not resolve
`ecostat.kerala.gov.in` (`curl: (6) Could not resolve host`), so official PDFs
could be read via the research web tool but not downloaded to the local
workspace for batch extraction. No credentials were requested or stored.

To execute the satellite pilot, the researcher should sign in to an
[Earth Engine registered account](https://earthengine.google.com/signup/) in
the Code Editor, select a Cloud project enabled for Earth Engine, and allow
the three Drive exports. Provide the project ID or run the saved script in
that session; **do not send a password or token**. If execution must be local,
provide an authenticated Earth Engine environment with outbound access and
an authorized project. Exported GeoTIFF/CSVs can then be placed under
`phase2/data/` with acquisition metadata for subsequent QA and analysis.

For independent 2018 event validation, provide the original georeferenced
NRSC/KSDMA inundation layer and, if possible, KSDMA's geocoded depth records.
The PDF map alone lacks pixel-level accuracy and acquisition-time information.
No financial or administrative restoration data should be treated as a time
series without location, observation date and a definition of restored
function.
