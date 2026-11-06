/*
2018 Kerala flood pilot: candidate Sentinel-1 event layer plus optical and
night-lights QA time series. STATUS: UNEXECUTED. Requires an authenticated
Earth Engine Code Editor project and manual review of printed scene inventory.

The fixed AOI is a pilot rectangle near Alappuzha/Vembanad, not an asserted
flooded unit or a historical administrative boundary. Exported SAR pixels are
candidate water-change detections, NOT validated 2018 flood exposure.
*/
var aoi = ee.Geometry.Rectangle([76.35, 9.45, 76.60, 9.75], null, false);
Map.centerObject(aoi, 11);
Map.addLayer(aoi, {color: 'yellow'}, 'Pilot AOI');

// Homogeneous Sentinel-1 pass/polarization/relative-orbit stack.
var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(aoi)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
  .select('VV');
var preAll = s1.filterDate('2018-07-01', '2018-08-01');
var eventAll = s1.filterDate('2018-08-16', '2018-09-01');
var commonOrbits = ee.List(preAll.aggregate_array('relativeOrbitNumber_start')).distinct()
  .intersection(ee.List(eventAll.aggregate_array('relativeOrbitNumber_start')).distinct());
print('Pre scenes (date, orbit, pass)', preAll.aggregate_array('system:time_start'),
  preAll.aggregate_array('relativeOrbitNumber_start'));
print('Event scenes (date, orbit, pass)', eventAll.aggregate_array('system:time_start'),
  eventAll.aggregate_array('relativeOrbitNumber_start'));
print('Common relative orbits; STOP if empty', commonOrbits);
// The first common orbit is a deterministic pilot choice; audit its scene dates.
var orbit = ee.Number(commonOrbits.get(0));
var pre = preAll.filter(ee.Filter.eq('relativeOrbitNumber_start', orbit));
var event = eventAll.filter(ee.Filter.eq('relativeOrbitNumber_start', orbit));
print('Selected orbit, pre/event scene counts', orbit, pre.size(), event.size());
var preImage = pre.median();
var eventImage = event.median();
var preCount = pre.count().rename('pre_valid_count');
var eventCount = event.count().rename('event_valid_count');
var valid = preCount.gt(0).and(eventCount.gt(0)).rename('valid_comparison');
var dbDrop = preImage.subtract(eventImage).rename('vv_drop_db');
// This masks recurrent water and steep terrain; it does not solve layover,
// wind roughening, dense vegetation, or backscatter-change confounding.
var occurrence = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence');
var slope = ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003'));
var analysisMask = valid.and(occurrence.lt(90)).and(slope.lt(5));
var candidate = dbDrop.gte(3).and(eventImage.lt(-15)).updateMask(analysisMask)
  .rename('candidate_inundation_3db');
var lower = dbDrop.gte(2).and(eventImage.lt(-15)).updateMask(analysisMask)
  .rename('candidate_inundation_2db');
var upper = dbDrop.gte(4).and(eventImage.lt(-15)).updateMask(analysisMask)
  .rename('candidate_inundation_4db');
Map.addLayer(candidate.selfMask(), {palette:['#1986b4']}, 'Candidate SAR change, 3 dB');
var sarQa = candidate.unmask(0).addBands(lower.unmask(0)).addBands(upper.unmask(0))
  .addBands(dbDrop.updateMask(valid)).addBands(preCount).addBands(eventCount)
  .addBands(valid).addBands(analysisMask.rename('terrain_water_qa'));
Export.image.toDrive({image:sarQa, description:'kerala_2018_s1_pilot_candidate_qa',
  region:aoi, scale:30, crs:'EPSG:32643', maxPixels:1e9, fileFormat:'GeoTIFF'});

// Landsat 8 Collection 2 L2 reflectance. Quarterly values are a seasonality
// panel; do not estimate recovery from this export without cloud/coverage QA.
function l8Indices(image) {
  var qa=image.select('QA_PIXEL');
  var clear=qa.bitwiseAnd(63).eq(0).and(image.select('QA_RADSAT').eq(0));
  var sr=image.select(['SR_B4','SR_B5','SR_B6'],['red','nir','swir'])
    .multiply(0.0000275).add(-0.2);
  var red=sr.select('red'), nir=sr.select('nir'), swir=sr.select('swir');
  var ndvi=nir.subtract(red).divide(nir.add(red)).rename('ndvi');
  var ndmi=nir.subtract(swir).divide(nir.add(swir)).rename('ndmi');
  var blue=image.select('SR_B2').multiply(0.0000275).add(-0.2);
  var evi=nir.subtract(red).multiply(2.5)
    .divide(nir.add(red.multiply(6)).subtract(blue.multiply(7.5)).add(1))
    .rename('evi');
  return ndvi.addBands(ndmi).addBands(evi).updateMask(clear)
    .copyProperties(image,['system:time_start']);
}
var l8=ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(aoi).map(l8Indices);
var quarters=ee.List.sequence(2015,2021).map(function(year){
  return ee.List.sequence(1,4).map(function(quarter){
    var start=ee.Date.fromYMD(ee.Number(year),1,1)
      .advance(ee.Number(quarter).subtract(1).multiply(3),'month');
    var col=l8.filterDate(start,start.advance(3,'month'));
    var count=col.select('ndvi').count().rename('valid_obs_per_pixel');
    var composite=col.median().addBands(count)
      .addBands(count.gt(0).rename('has_valid_obs'));
    var means=composite.reduceRegion({reducer:ee.Reducer.mean(),geometry:aoi,
      scale:30,maxPixels:1e8});
    return ee.Feature(null,means).set({year:year,quarter:quarter,
      start:start.format('YYYY-MM-dd'),scene_count:col.size(),
      sensor:'Landsat 8 C2 L2',aoi_id:'alappuzha_vembanad_pilot'});
  });
}).flatten();
Export.table.toDrive({collection:ee.FeatureCollection(quarters),
  description:'kerala_2018_pilot_l8_quarterly_qa',fileFormat:'CSV'});

// VIIRS is a coarse illumination proxy and must clear noise/coverage checks.
var viirs=ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG')
  .filterBounds(aoi);
var months=ee.List.sequence(2016,2021).map(function(year){
  return ee.List.sequence(1,12).map(function(month){
    var start=ee.Date.fromYMD(ee.Number(year),ee.Number(month),1);
    var images=viirs.filterDate(start,start.advance(1,'month'));
    var image=ee.Image(images.first());
    var coverage=image.select('cf_cvg');
    var rad=image.select('avg_rad').updateMask(coverage.gte(3))
      .rename('radiance_cf3');
    var means=rad.addBands(coverage.rename('cloudfree_count'))
      .addBands(coverage.gte(3).rename('fraction_pixels_cf3'))
      .reduceRegion({reducer:ee.Reducer.mean(),geometry:aoi,
        scale:500,maxPixels:1e8});
    return ee.Feature(null,means).set({year:year,month:month,
      start:start.format('YYYY-MM-dd'),scene_count:images.size(),
      sensor:'VIIRS VCMSLCFG',aoi_id:'alappuzha_vembanad_pilot'});
  });
}).flatten();
Export.table.toDrive({collection:ee.FeatureCollection(months),
  description:'kerala_2018_pilot_viirs_monthly_qa',fileFormat:'CSV'});

// Before using any output: inspect scene dates, geometry, no-data, incidence
// angle, SAR thresholds, cropland/vegetation masks, independent flood labels,
// seasonal control areas, and later 2019/2021 shocks. See methods report.
