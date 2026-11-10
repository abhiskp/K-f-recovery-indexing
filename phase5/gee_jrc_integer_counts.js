/* Phase 5: exact pixel-center frequency counts on the Phase 4 grid.
 * Code Editor console only; no export and no flood inference.
 */
var aoi = ee.Geometry.Rectangle([76.35, 9.45, 76.60, 9.75], null, false);
var years = [2014, 2015, 2016, 2017];
var annual = years.map(function(y) {
  return ee.Image(ee.ImageCollection('JRC/GSW1_4/YearlyHistory')
    .filter(ee.Filter.eq('year', y)).first())
    .select('waterClass').unmask(255, false).toByte().rename('class_' + y);
});
var stack = ee.Image.cat(annual);
function counts(image) {
  return image.reduceRegion({
    reducer: ee.Reducer.frequencyHistogram().unweighted(), geometry: aoi,
    crs: 'EPSG:32643', crsTransform: [30, 0, 648060, 0, -30, 1078200],
    maxPixels: 2e6
  }).getInfo();
}
years.forEach(function(y, i) {
  print('PIXEL_CENTER_CLASS_' + y + ' ' + JSON.stringify(counts(annual[i])));
});
var valid = stack.gte(1).and(stack.lte(3)).reduce(ee.Reducer.sum());
var permanent = stack.eq(3).reduce(ee.Reducer.sum());
var seasonal = stack.eq(2).reduce(ee.Reducer.sum());
var allNotWater = stack.eq(1).reduce(ee.Reducer.min());
var state = ee.Image(0).where(valid.gte(3), 4)
  .where(valid.eq(4).and(allNotWater), 1)
  .where(valid.gte(3).and(seasonal.gte(1)).and(permanent.lt(3)), 2)
  .where(valid.gte(3).and(permanent.gte(3)), 3)
  .rename('conservative_state').toByte();
print('PIXEL_CENTER_COMPOSITE ' + JSON.stringify(counts(state)));
print('State 0=<3 valid years; 1=all four not-water; 2=seasonal observed; ' +
  '3=permanent >=3 years; 4=mixed/other >=3 valid years.');
