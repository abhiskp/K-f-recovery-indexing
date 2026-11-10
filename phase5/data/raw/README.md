# Phase 5 incoming source files

The Earth Engine task `phase5_jrc_waterclass_2014_2017_pilot` completed on 8 November 2026 under ID `GIHCX7SEC7VIJ4XHL6IRMAOQ`. The researcher downloaded its four-band GeoTIFF here on 9 November as `phase5_jrc_waterclass_2014_2017_pilot.tif`. `scripts/audit_reference_and_jrc.py` verified its exact Phase 4 grid, annual class counts and conservative composite-state raster. The fourth band is 2017 `waterClass`, although GDAL may interpret it as alpha; read raw band values as the audit does.

No licensed NRSC/KSDMA geospatial flood, duration or depth data have been supplied. Preserve any subsequently received files with their source licence and do not place private credentials or personal point identifiers in a shared ZIP.
