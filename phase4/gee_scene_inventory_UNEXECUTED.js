/*
PHASE 4: PREPARED, UNEXECUTED until an Earth Engine account/project is signed in.
Inventories every Sentinel-1 GRD scene intersecting the Alappuzha/Vembanad pilot,
2016-06-01 through 2018-10-15. Dates are UTC. This deliberately spans earlier
seasonal comparators, months before the 2018 monsoon, the documented 16 July
flooding, 9/21 August observations, and later scenes. No scene is automatically
called "unflooded". See sources.md and qa_validation.md before selection.

Run in Earth Engine Code Editor. Inspect printed count and start the CSV task.
No secret or project ID is embedded. Source: COPERNICUS/S1_GRD official catalog.
*/
var aoi = ee.Geometry.Rectangle([76.35, 9.45, 76.60, 9.75], null, false);
var START_INVENTORY_EXPORT = true;
var collection = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(aoi)
  .filterDate('2016-06-01', '2018-10-15')
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
  .sort('system:time_start');

function sceneFeature(image) {
  image = ee.Image(image);
  var valid = image.select('VV').mask().unmask(0, false).rename('valid');
  var validity = valid.reduceRegion({reducer: ee.Reducer.mean(), geometry: aoi,
    scale: 30, maxPixels: 1e8, bestEffort: true});
  var angleStats = image.select('angle').reduceRegion({
    reducer: ee.Reducer.minMax().combine({reducer2:ee.Reducer.mean(),sharedInputs:true}),
    geometry:aoi, scale:1000, maxPixels:1e8, bestEffort:true});
  var footprintFraction = image.geometry().intersection(aoi, ee.ErrorMargin(100))
    .area(100).divide(aoi.area(100));
  return ee.Feature(null, {
    scene_id: image.get('system:index'),
    acquisition_utc: ee.Date(image.get('system:time_start')).format('YYYY-MM-dd HH:mm:ss'),
    platform_number: image.get('platform_number'),
    absolute_orbit: image.get('orbitNumber_start'),
    relative_orbit: image.get('relativeOrbitNumber_start'),
    pass_direction: image.get('orbitProperties_pass'),
    instrument_mode: image.get('instrumentMode'),
    polarizations: ee.List(image.get('transmitterReceiverPolarisation')).join('|'),
    resolution_m: image.get('resolution_meters'),
    footprint_fraction_of_aoi: footprintFraction,
    vv_valid_fraction_of_aoi_approx_30m: validity.get('valid'),
    incidence_angle_min_deg_approx: angleStats.get('angle_min'),
    incidence_angle_max_deg_approx: angleStats.get('angle_max'),
    incidence_angle_mean_deg_approx: angleStats.get('angle_mean'),
    aoi_id: 'alappuzha_vembanad_pilot',
    classification: 'unreviewed_scene'
  });
}
var inventory = ee.FeatureCollection(collection.toList(collection.size()).map(sceneFeature));
print('Pilot AOI', aoi);
print('Scene count; review every row before selecting a baseline', collection.size());
print('Complete scene inventory', inventory);
print('Documented flood observations: NRSC 16 July; IIRS 9 and 21 August 2018. '
  + 'July 2018 cannot be labeled dry by date alone.');
Map.centerObject(aoi, 11);
Map.addLayer(aoi, {color:'yellow'}, 'Inventory AOI');
if (START_INVENTORY_EXPORT) {
  Export.table.toDrive({collection:inventory,
    description:'phase4_kerala_2016_2018_s1_pilot_full_scene_inventory',
    fileFormat:'CSV'});
}
