/* Executed in Earth Engine Code Editor, 2017/2018 June–September pilot availability.
   Monthly clear-any coverage is an observational feasibility measure only.
   It is not flood attribution or vegetation/economic recovery. */
var aoi=ee.Geometry.Rectangle([76.35,9.45,76.60,9.75],null,false);
var months=['2017-06','2017-07','2017-08','2017-09','2018-06','2018-07','2018-08','2018-09'];
function coverage(col,scale) { var any=ee.Image(ee.Algorithms.If(col.size().gt(0),col.max(),ee.Image.constant(0))).unmask(0,false); return any.reduceRegion({reducer:ee.Reducer.mean(),geometry:aoi,scale:scale,maxPixels:1e8,bestEffort:true}).values().get(0); }
function row(m) { m=ee.String(m); var start=ee.Date.parse('YYYY-MM',m); var end=start.advance(1,'month');
  var l8=ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(aoi).filterDate(start,end);
  var l8clear=l8.map(function(im){var qa=im.select('QA_PIXEL'); return qa.bitwiseAnd(63).eq(0).updateMask(qa.mask()).rename('clear').toByte();});
  var s2=ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(aoi).filterDate(start,end);
  var s2clear=s2.map(function(im){var scl=im.select('SCL'); return scl.eq(4).or(scl.eq(5)).or(scl.eq(6)).updateMask(scl.mask()).rename('clear').toByte();});
  var toa=ee.ImageCollection('COPERNICUS/S2_HARMONIZED').filterBounds(aoi).filterDate(start,end);
  var toaNoCloud=toa.map(function(im){var qa=im.select('QA60'); return qa.bitwiseAnd(3072).eq(0).updateMask(qa.mask()).rename('noncloud').toByte();});
  var viirs=ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG').filterDate(start,end).select(['avg_rad','cf_cvg']);
  var v=ee.Image(ee.Algorithms.If(viirs.size().gt(0),viirs.first(),ee.Image.constant([0,0]).rename(['avg_rad','cf_cvg'])));
  var vstat=v.reduceRegion({reducer:ee.Reducer.mean(),geometry:aoi,scale:500,maxPixels:1e8,bestEffort:true});
  return ee.Feature(null,{month:m,l8_scenes:l8.size(),l8_clear_any_fraction_30m:coverage(l8clear,30),s2_sr_scenes:s2.size(),s2_sr_clear_any_fraction_20m:coverage(s2clear,20),s2_toa_scenes:toa.size(),s2_toa_qa60_noncloud_any_fraction_60m:coverage(toaNoCloud,60),viirs_monthly_images:viirs.size(),viirs_mean_cf_cvg_500m:vstat.get('cf_cvg'),viirs_mean_avg_rad_nW_sr_cm2_500m:vstat.get('avg_rad')}); }
var result=ee.FeatureCollection(ee.List(months).map(row));
print('Phase 4 independent-domain data-availability check',result);
