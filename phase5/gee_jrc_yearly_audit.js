/* Phase 5: JRC annual water-class audit on the Phase 4 pilot grid.
 * Earth Engine Code Editor. Run while signed in to an enabled project.
 * The console prints four annual class histograms. An export task sends the
 * four source-class bands to the researcher's Drive. No flood classification.
 */
var aoi = ee.Geometry.Rectangle([76.35, 9.45, 76.60, 9.75], null, false);
var years = [2014, 2015, 2016, 2017];
var collection = ee.ImageCollection('JRC/GSW1_4/YearlyHistory');
var classImages = years.map(function(y) {
  var one = collection.filter(ee.Filter.eq('year', y)).select('waterClass');
  if (one.size().getInfo() !== 1) throw new Error('Expected one JRC image for ' + y);
  return ee.Image(one.first()).unmask(255, false).toByte().rename('waterClass_' + y);
});
var stack = ee.Image.cat(classImages);
years.forEach(function(y, i) {
  var histogram = ee.Image(classImages[i]).reduceRegion({
    reducer: ee.Reducer.frequencyHistogram(), geometry: aoi,
    crs: 'EPSG:32643', crsTransform: [30, 0, 648060, 0, -30, 1078200],
    maxPixels: 2e6
  });
  print('HIST_' + y + ' ' + JSON.stringify(histogram.getInfo()));
});
print('Phase 4 grid: EPSG:32643, 30 m, origin 648060/1078200, 921 x 1111');
print('JRC annual classes 0=no data, 1=not water, 2=seasonal, 3=permanent; 255=masked');
Export.image.toDrive({image: stack, description: 'phase5_jrc_waterclass_2014_2017_pilot',
  region: aoi, crs: 'EPSG:32643',
  crsTransform: [30, 0, 648060, 0, -30, 1078200],
  maxPixels: 2e6, fileFormat: 'GeoTIFF'});
