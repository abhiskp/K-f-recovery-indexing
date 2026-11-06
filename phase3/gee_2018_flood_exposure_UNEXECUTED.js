/*
Phase 3 Experiment B. STATUS: PREPARED, SYNTAX-CHECKED, UNEXECUTED.
Alappuzha/Vembanad pilot only. Two-run workflow: first inspect scene inventory,
then enter two comparable scene IDs, inspect QA, and set START_EXPORTS=true.
No exported candidate layer is ground truth or an observed flood extent.
Source: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD
*/
var aoi = ee.Geometry.Rectangle([76.35, 9.45, 76.60, 9.75], null, false);
var PASS = 'ASCENDING';
var POLARIZATION = 'VV';
var PRE_SCENE_ID = null;       // Set exact system:index from the inventory below.
var EVENT_SCENE_ID = null;     // Set exact system:index from the inventory below.
var START_EXPORTS = false;    // Enable only after reviewing matching acquisition metadata and coverage.
Map.centerObject(aoi, 11);
Map.addLayer(aoi, {color: 'yellow'}, 'Pilot rectangle');

var stack = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(aoi)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.eq('orbitProperties_pass', PASS))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', POLARIZATION));
var preInventory = stack.filterDate('2018-07-01', '2018-08-01');
var eventInventory = stack.filterDate('2018-08-16', '2018-09-01');

function sceneInventory(collection, period) {
  return ee.FeatureCollection(collection.toList(collection.size()).map(function(item) {
    var image = ee.Image(item);
    var footprintFraction = image.geometry().intersection(aoi, ee.ErrorMargin(100))
      .area(100).divide(aoi.area(100));
    var validFraction = image.select(POLARIZATION).mask().reduceRegion({
      reducer: ee.Reducer.mean(), geometry: aoi, scale: 100,
      maxPixels: 1e8, bestEffort: true
    }).get(POLARIZATION);
    var angleMean = image.select('angle').reduceRegion({
      reducer: ee.Reducer.mean(), geometry: aoi, scale: 1000,
      maxPixels: 1e8, bestEffort: true
    }).get('angle');
    return ee.Feature(null, {
      period: period,
      scene_id: image.get('system:index'),
      acquisition_utc: ee.Date(image.get('system:time_start')).format('YYYY-MM-dd HH:mm'),
      relative_orbit: image.get('relativeOrbitNumber_start'),
      pass: image.get('orbitProperties_pass'),
      mode: image.get('instrumentMode'),
      polarizations: image.get('transmitterReceiverPolarisation'),
      footprint_fraction_of_aoi: footprintFraction,
      valid_fraction_of_aoi_approx: validFraction,
      mean_incidence_angle_deg_approx: angleMean
    });
  }));
}
print('Pre-event scene inventory', sceneInventory(preInventory, 'pre'));
print('Event scene inventory', sceneInventory(eventInventory, 'event'));
print('Common relative orbits', ee.List(preInventory.aggregate_array('relativeOrbitNumber_start'))
  .distinct().intersection(ee.List(eventInventory.aggregate_array('relativeOrbitNumber_start')).distinct()));

if (PRE_SCENE_ID !== null && EVENT_SCENE_ID !== null) {
  var preCollection = preInventory.filter(ee.Filter.eq('system:index', PRE_SCENE_ID));
  var eventCollection = eventInventory.filter(ee.Filter.eq('system:index', EVENT_SCENE_ID));
  print('Selected pre/event counts; both must equal 1', preCollection.size(), eventCollection.size());
  var pre = ee.Image(preCollection.first());
  var event = ee.Image(eventCollection.first());
  var sameOrbit = ee.Number(pre.get('relativeOrbitNumber_start'))
    .eq(ee.Number(event.get('relativeOrbitNumber_start')));
  print('Selected scene metadata', sceneInventory(preCollection, 'selected_pre'),
    sceneInventory(eventCollection, 'selected_event'));
  print('Same relative orbit? Must be true', sameOrbit);
  print('CHECK manually: same relative orbit, IW mode, ASCENDING pass, VV polarization, '
    + 'similar angle, adequate AOI overlap, suitable 2018 flood observation dates.');

  // A dB decrease plus low event backscatter is an exploratory threshold.
  var preVV = pre.select(POLARIZATION).rename('pre_vv_db');
  var eventVV = event.select(POLARIZATION).rename('event_vv_db');
  var preValid = preVV.mask().rename('pre_valid');
  var eventValid = eventVV.mask().rename('event_valid');
  var overlap = preValid.and(eventValid).rename('valid_overlap');
  var drop = preVV.subtract(eventVV).rename('vv_drop_db');
  var preAngle = pre.select('angle').rename('pre_angle_deg');
  var eventAngle = event.select('angle').rename('event_angle_deg');
  var waterOccurrence = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence');
  var nonPermanent = waterOccurrence.lt(90).rename('nonpermanent_water');
  var lowSlope = ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003'))
    .lt(5).rename('low_slope');
  var qaMask = overlap.and(nonPermanent).and(lowSlope)
    .and(ee.Image.constant(sameOrbit)).rename('analysis_valid');
  var candidate2 = drop.gte(2).and(eventVV.lt(-15)).updateMask(qaMask)
    .rename('candidate_2db');
  var candidate3 = drop.gte(3).and(eventVV.lt(-15)).updateMask(qaMask)
    .rename('candidate_3db');
  var candidate4 = drop.gte(4).and(eventVV.lt(-15)).updateMask(qaMask)
    .rename('candidate_4db');
  Map.addLayer(preVV, {min:-25,max:0}, 'Selected pre VV');
  Map.addLayer(eventVV, {min:-25,max:0}, 'Selected event VV');
  Map.addLayer(candidate3.selfMask(), {palette:['#1879b7']}, 'Candidate change 3 dB');
  Map.addLayer(qaMask.selfMask(), {palette:['#32a852']}, 'Valid analysis support', false);
  print('Candidate km2 by threshold; only within valid analysis support',
    ee.Image.pixelArea().divide(1e6).updateMask(candidate2).reduceRegion({
      reducer: ee.Reducer.sum(), geometry:aoi, scale:30, maxPixels:1e9}),
    ee.Image.pixelArea().divide(1e6).updateMask(candidate3).reduceRegion({
      reducer: ee.Reducer.sum(), geometry:aoi, scale:30, maxPixels:1e9}),
    ee.Image.pixelArea().divide(1e6).updateMask(candidate4).reduceRegion({
      reducer: ee.Reducer.sum(), geometry:aoi, scale:30, maxPixels:1e9}));
  if (START_EXPORTS) {
    // Masked pixels are no-data, not zero. Export includes both raw observations
    // and QA, so zero candidate pixels can be distinguished from exclusions.
    var output = candidate2.addBands(candidate3).addBands(candidate4)
      .addBands(preVV).addBands(eventVV).addBands(drop)
      .addBands(preAngle).addBands(eventAngle)
      .addBands(preValid).addBands(eventValid).addBands(overlap)
      .addBands(nonPermanent).addBands(lowSlope).addBands(qaMask);
    Export.image.toDrive({image:output, description:'kerala_2018_s1_selected_pair_candidate_qa',
      region:aoi, scale:30, crs:'EPSG:32643', maxPixels:1e9, fileFormat:'GeoTIFF'});
    Export.table.toDrive({collection:sceneInventory(preCollection, 'selected_pre')
      .merge(sceneInventory(eventCollection, 'selected_event')),
      description:'kerala_2018_s1_selected_pair_metadata', fileFormat:'CSV'});
  }
}
